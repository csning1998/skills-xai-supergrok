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


def deny(reason: str) -> int:
    """Print a deny decision and return exit code 2."""
    print(
        json.dumps({"decision": "deny", "reason": reason}, ensure_ascii=False)
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

    if tool in READ_TOOLS and path:
        record_read(payload, path)
        return allow()

    if tool not in MUTATING_TOOLS:
        return allow()

    reason = evaluate_write(payload, path, text, command_text, before=before)
    if reason:
        return deny(reason)
    return allow()


def handle_post_tool_use(payload: dict[str, Any]) -> int:
    """Record a successful read path after the tool completes."""
    tool = norm_tool(payload)
    path = file_path(tool_input(payload))
    if tool in READ_TOOLS and path:
        record_read(payload, path)
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
