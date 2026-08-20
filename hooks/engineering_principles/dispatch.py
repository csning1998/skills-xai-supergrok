"""Hook event dispatch and process entry."""

from __future__ import annotations

import json
import sys
import traceback
from typing import Any

from engineering_principles.config import MUTATING_TOOLS
from engineering_principles.config import READ_TOOLS
from engineering_principles.evaluate import apply_leave
from engineering_principles.evaluate import evaluate_write
from engineering_principles.evaluate import record_read
from engineering_principles.module_stateless import composed_module_text
from engineering_principles.module_stateless import emit_post_write_scan
from engineering_principles.module_stateless import module_stateless_reason
from engineering_principles.module_stateless import record_skill_module_write
from engineering_principles.module_stateless import resolve_skill_module_paths
from engineering_principles.module_stateless import shell_write_payloads
from engineering_principles.module_stateless import stop_stateless_reason
from engineering_principles.payload import command
from engineering_principles.payload import file_path
from engineering_principles.payload import new_text
from engineering_principles.payload import norm_event
from engineering_principles.payload import norm_tool
from engineering_principles.payload import old_text
from engineering_principles.payload import prompt_text
from engineering_principles.payload import tool_input
from engineering_principles.state import hook_disabled
from engineering_principles.state import load_state
from engineering_principles.state import workspace_root


def deny(reason: str) -> int:
    """Print a deny decision and return exit code 2."""
    print(
        json.dumps({"decision": "deny", "reason": reason}, ensure_ascii=False)
    )
    return 2


def block_stop(reason: str) -> int:
    """Print a Stop block decision and return exit code 2."""
    print(
        json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False)
    )
    return 2


def allow(extra: dict[str, Any] | None = None) -> int:
    """Print an allow decision and return exit code 0."""
    body: dict[str, Any] = {"decision": "allow"}
    if extra:
        body.update(extra)
    print(json.dumps(body, ensure_ascii=False))
    return 0


def handle_pre_tool_use(payload: dict[str, Any]) -> int:
    """Evaluate a PreToolUse payload and deny forbidden writes."""
    tool = norm_tool(payload)
    tool_input_data = tool_input(payload)
    path = file_path(tool_input_data)
    text = new_text(tool_input_data)
    command_text = command(tool_input_data)
    before = old_text(tool_input_data, path)
    file_before = old_text({}, path)
    root = str(workspace_root(payload))
    cwd = str(payload.get("cwd") or root)

    if tool in READ_TOOLS and path:
        record_read(payload, path)
        return allow()

    if tool not in MUTATING_TOOLS:
        return allow()

    content = ""
    if isinstance(tool_input_data.get("content"), str):
        content = tool_input_data["content"]
    elif isinstance(tool_input_data.get("contents"), str):
        content = tool_input_data["contents"]
    old_string = tool_input_data.get("old_string")
    new_string = tool_input_data.get("new_string")
    scan = composed_module_text(
        content,
        file_before,
        old_string if isinstance(old_string, str) else "",
        new_string if isinstance(new_string, str) else "",
    )
    blobs = [
        item for item in (scan, *shell_write_payloads(command_text)) if item
    ]
    for item in resolve_skill_module_paths(path, command_text, cwd, root):
        for blob in blobs:
            module_reason = module_stateless_reason(item, blob)
            if module_reason:
                return deny(module_reason)

    reason = evaluate_write(payload, path, text, command_text, before=before)
    if reason:
        return deny(reason)
    return allow()


def handle_post_tool_use(payload: dict[str, Any]) -> int:
    """Record reads and scan a skill-module file after a successful write."""
    tool = norm_tool(payload)
    tool_input_data = tool_input(payload)
    path = file_path(tool_input_data)
    command_text = command(tool_input_data)
    root = str(workspace_root(payload))
    cwd = str(payload.get("cwd") or root)
    if tool in READ_TOOLS and path:
        record_read(payload, path)
    if tool in MUTATING_TOOLS:
        for item in resolve_skill_module_paths(path, command_text, cwd, root):
            record_skill_module_write(payload, item)
            emit_post_write_scan(item, root)
    return 0


def handle_stop(payload: dict[str, Any]) -> int:
    """Block the turn when a written skill-module file still bakes state."""
    reason = stop_stateless_reason(payload)
    if reason:
        return block_stop(reason)
    return 0


def handle_user_prompt(payload: dict[str, Any]) -> int:
    """Record leave phrases. Inject no context."""
    prompt = prompt_text(payload)
    if prompt:
        apply_leave(payload, prompt)
    return 0


def handle_session_start(payload: dict[str, Any]) -> int:
    """Create session state. Inject no context."""
    load_state(payload)
    return 0


def dispatch(payload: dict[str, Any]) -> int:
    """Route one hook payload to the matching handler."""
    if hook_disabled():
        return allow() if norm_event(payload) == "pretooluse" else 0
    event = norm_event(payload)
    if event == "pretooluse":
        return handle_pre_tool_use(payload)
    if event == "posttooluse":
        return handle_post_tool_use(payload)
    if event == "userpromptsubmit":
        return handle_user_prompt(payload)
    if event == "sessionstart":
        return handle_session_start(payload)
    if event in {"stop", "subagentstop"}:
        return handle_stop(payload)
    return 0


def main() -> int:
    """Read stdin JSON and dispatch. Tests live in pytest."""
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid hook payload: {exc}\n")
        return 0
    if not isinstance(payload, dict):
        return 0
    try:
        return dispatch(payload)
    except Exception as exc:  # noqa: BLE001
        event = norm_event(payload)
        sys.stderr.write(f"engineering-principles hook error: {exc}\n")
        traceback.print_exc(file=sys.stderr)
        if event == "pretooluse" and norm_tool(payload) in MUTATING_TOOLS:
            return deny(f"hook error while evaluating a write: {exc}")
        return 0
