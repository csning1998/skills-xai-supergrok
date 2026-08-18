#!/usr/bin/env python3
"""Gate low-level IaC mistakes without injecting stack docs into context."""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import sys
import tempfile
import traceback
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any

OLD_TEXT_MAX_BYTES = 1_048_576


def _hook_disabled() -> bool:
    return os.environ.get("ENGINEERING_PRINCIPLES_HOOK", "1") == "0"


def _state_root() -> Path:
    return Path(
        os.environ.get(
            "ENGINEERING_PRINCIPLES_STATE_DIR",
            str(Path.home() / ".grok" / "hooks" / "state"),
        )
    )


def _session_id(payload: dict[str, Any]) -> str:
    value = (
        os.environ.get("GROK_SESSION_ID")
        or payload.get("sessionId")
        or payload.get("session_id")
    )
    if value:
        return str(value)
    return f"ephemeral-{os.getpid()}-{secrets.token_hex(8)}"


def _workspace_root(payload: dict[str, Any]) -> Path:
    raw = (
        os.environ.get("GROK_WORKSPACE_ROOT")
        or os.environ.get("CLAUDE_PROJECT_DIR")
        or payload.get("workspaceRoot")
        or payload.get("workspace_root")
        or payload.get("cwd")
        or os.getcwd()
    )
    return Path(str(raw)).expanduser()


def _state_path(payload: dict[str, Any]) -> Path:
    workspace = _workspace_root(payload)
    digest = hashlib.sha256(str(workspace.resolve()).encode("utf-8")).hexdigest()[:16]
    key = f"{_session_id(payload)}__{digest}"
    return _state_root() / f"{key}.json"


def _empty_state(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": 2,
        "session_id": _session_id(payload),
        "workspace_root": str(_workspace_root(payload)),
        "read_paths": [],
        "generic_leave": False,
        "generic_leave_modules": [],
        "guest_sql_leave": False,
        "last_prompt": "",
    }


def load_state(payload: dict[str, Any]) -> dict[str, Any]:
    path = _state_path(payload)
    if not path.is_file():
        return _empty_state(payload)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _empty_state(payload)
    if not isinstance(data, dict):
        return _empty_state(payload)
    merged = _empty_state(payload)
    merged.update(data)
    if not isinstance(merged.get("read_paths"), list):
        merged["read_paths"] = []
    if not isinstance(merged.get("generic_leave_modules"), list):
        merged["generic_leave_modules"] = []
    return merged


def save_state(payload: dict[str, Any], state: dict[str, Any]) -> None:
    path = _state_path(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(state, ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=path.name, dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(encoded)
        os.replace(tmp_name, path)
    except OSError:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


GENERIC_MODULE_NAME_RE = re.compile(
    r"terraform/modules/[\w./-]+|utils_[a-z0-9_]+|"
    r"vault-credential|vault-pki-setup|vault-workload-identity",
    re.I,
)
ENV_ALIAS_RE = re.compile(r"\b(prod|stg|staging|dev|development)\b", re.I)
PROVISIONER_RE = re.compile(r'provisioner\s+"(local-exec|remote-exec)"')
ANSIBLE_SHELL_RE = re.compile(r"ansible\.builtin\.(shell|command)\b")
ANSIBLE_IDEMPOTENT_RE = re.compile(r"\b(changed_when|creates|removes)\b")
GOVERNED_DIR_PARTS = ("terraform", "ansible", "packer", "planning")
GENERIC_MODULE_RE = re.compile(
    r"(?:^|/)terraform/modules(?:/|$)|(?:^|/)ansible/roles/utils_[^/]+(?:/|$)"
)
SECRET_MINT_LAYER_RE = re.compile(
    r"(?:^|/)terraform/layers/[^/]*(?:vault|credential|pki|identity|approle)[^/]*",
    re.I,
)
PRODUCT_TOKEN_RE = re.compile(
    r"\b(harbor-origin|harbor_origin|harbor-bootstrapper|"
    r"harbor_bootstrapper|keycloak|gitlab-omnibus)\b",
    re.I,
)
TAUTOLOGICAL_PROVIDER_RE = re.compile(
    r"providers\s*=\s*\{[^}]*\bvault\s*=\s*vault\b[^}]*\}",
    re.S,
)
HARDCODED_VAULT_PRODUCTION_RE = re.compile(r"\bvault\.production\b")
RANDOM_PASSWORD_RE = re.compile(r'\bresource\s+"random_password"')
VAULT_CREDENTIAL_MODULE_RE = re.compile(
    r"modules/vault-provisioning/vault-credential|"
    r'source\s*=\s*"[^"]*vault-credential"'
)
ANSIBLE_SQL_RE = re.compile(
    r"(community\.postgresql|\bpostgresql_query\b|\bpostgresql_user\b|"
    r"\bansible\.builtin\.shell\b[^\n]{0,80}\bpsql\b)",
    re.I,
)
GUEST_SQL_CMD_RE = re.compile(
    r"(?:"
    r"(?:^|[;&|])\s*\bpsql\b"
    r"|"
    r"\bssh\b[^\n]{0,200}\bpsql\b"
    r"|"
    r"\bdocker\s+exec\b[^\n]{0,200}\bpsql\b"
    r"|"
    r"\bpsql\b[^\n]{0,200}\bALTER\s+(?:USER|ROLE)\b"
    r"|"
    r"\bssh\b[^\n]{0,200}\bALTER\s+(?:USER|ROLE)\b"
    r"|"
    r"\bdocker\s+exec\b[^\n]{0,200}\bALTER\s+(?:USER|ROLE)\b"
    r")",
    re.I,
)
READ_ONLY_CMD_RE = re.compile(
    r"^\s*(ls|ll|cat|less|head|tail|rg|grep|find|sed\s+-n|awk|"
    r"terraform\s+(fmt\s+-check|validate|plan|show|state\s+list|version)|"
    r"ansible-playbook\s+[^\n]*--check|git\s+(status|diff|log|show|rev-parse))\b"
)
WRITE_CMD_RE = re.compile(
    r"(?:\bsed\s+-i\b|\btee\b|\bmv\s|\bcp\s|\brm\s|\btruncate\b|"
    r"(?:^|[;&|])\s*(?:cat|printf|echo)\s.*>)"
)
LEAVE_GENERIC_RE = re.compile(
    r"(允許改通用模組|授權改通用模組|你可以改這個通用|"
    r"leave\s+generic\s+module|authorized\s+to\s+edit\s+generic)",
    re.I,
)
LEAVE_GUEST_SQL_RE = re.compile(
    r"(允許 guest\s*sql|授權 guest\s*sql|allow\s+guest\s+sql)",
    re.I,
)
BOOTSTRAPPER_NAME_RE = re.compile(r"bootstrapper", re.I)
ARCHITECTURE_STEM_RE = re.compile(r"^architecture_(.+)$")

MUTATING_TOOLS = {
    "write",
    "searchreplace",
    "multiedit",
    "edit",
    "runterminalcommand",
    "bash",
}
READ_TOOLS = {"readfile", "read"}


def _norm_event(payload: dict[str, Any]) -> str:
    raw = (
        os.environ.get("GROK_HOOK_EVENT")
        or payload.get("hookEventName")
        or payload.get("hook_event_name")
        or ""
    )
    return re.sub(r"[^a-z]", "", str(raw).lower())


def _norm_tool(payload: dict[str, Any]) -> str:
    raw = payload.get("toolName") or payload.get("tool_name") or ""
    return re.sub(r"[^a-z]", "", str(raw).lower())


def _tool_input(payload: dict[str, Any]) -> dict[str, Any]:
    value = payload.get("toolInput") or payload.get("tool_input") or {}
    return value if isinstance(value, dict) else {}


def _prompt_text(payload: dict[str, Any]) -> str:
    for key in ("prompt", "userPrompt", "user_prompt", "text"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _file_path(tool_input: dict[str, Any]) -> str:
    for key in ("file_path", "target_file", "path", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _new_text(tool_input: dict[str, Any]) -> str:
    chunks: list[str] = []
    for key in ("content", "contents", "new_string", "command"):
        value = tool_input.get(key)
        if isinstance(value, str):
            chunks.append(value)
    return "\n".join(chunks)


def _old_text(tool_input: dict[str, Any], path: str) -> str:
    value = tool_input.get("old_string")
    if isinstance(value, str) and value:
        return value
    if not path:
        return ""
    candidate = Path(path).expanduser()
    try:
        if not candidate.is_file():
            return ""
        if candidate.stat().st_size > OLD_TEXT_MAX_BYTES:
            return ""
        return candidate.read_text(encoding="utf-8")
    except OSError:
        return ""


def _posix(path: str) -> str:
    return path.replace("\\", "/")


def _is_self_path(path: str) -> bool:
    expanded = str(Path(path).expanduser())
    home_grok = str(Path.home() / ".grok")
    return expanded.startswith(home_grok + os.sep) or expanded == home_grok


def _added(before: str, after: str, pattern: re.Pattern[str]) -> bool:
    if not after or not pattern.search(after):
        return False
    before_hits = len(pattern.findall(before)) if before else 0
    after_hits = len(pattern.findall(after))
    return after_hits > before_hits


def is_governed_path(path: str) -> bool:
    parts = Path(_posix(path)).parts
    return any(part in GOVERNED_DIR_PARTS for part in parts)


def is_generic_module(path: str) -> bool:
    return bool(GENERIC_MODULE_RE.search(_posix(path)))


def is_secret_mint_layer(path: str) -> bool:
    posix = _posix(path)
    if "/terraform/layers/" not in posix:
        return False
    return bool(SECRET_MINT_LAYER_RE.search(posix))


def is_consumer_layer(path: str) -> bool:
    posix = _posix(path)
    if "/terraform/layers/" not in posix:
        return False
    return not is_secret_mint_layer(posix)


def introduces_bootstrapper_name(path: str) -> bool:
    candidate = Path(path).expanduser()
    if not BOOTSTRAPPER_NAME_RE.search(_posix(str(candidate))):
        return False
    current = candidate
    while not current.exists() and current != current.parent:
        if BOOTSTRAPPER_NAME_RE.search(current.name):
            parent = current.parent
            for ancestor in [parent, *parent.parents]:
                if ancestor.exists() and BOOTSTRAPPER_NAME_RE.search(ancestor.name):
                    return False
            return True
        current = current.parent
    return False


def find_planning_root(start: Path) -> Path | None:
    cursor = start.resolve() if start.exists() else start
    seen: set[Path] = set()
    while cursor not in seen:
        seen.add(cursor)
        candidate = cursor / "planning"
        if (candidate / "decisions.md").is_file() or (
            candidate / "architecture.md"
        ).is_file():
            return candidate
        if cursor.parent == cursor:
            break
        cursor = cursor.parent
    return None


def _architecture_repo_tokens(planning: Path) -> list[str]:
    tokens: list[str] = []
    for item in planning.glob("architecture*.md"):
        match = ARCHITECTURE_STEM_RE.match(item.stem)
        if match is None:
            continue
        repo = match.group(1).split("_", 1)[0].strip()
        if repo and repo not in tokens:
            tokens.append(repo)
    return tokens


def path_needs_planning_gate(path: str, planning: Path | None) -> bool:
    if planning is None or not path:
        return False
    posix = _posix(path)
    try:
        resolved = Path(path).expanduser().resolve()
    except OSError:
        resolved = Path(posix)
    try:
        if resolved == planning.resolve() or planning.resolve() in resolved.parents:
            return True
    except OSError:
        if "/planning/" in posix:
            return True
    if not is_governed_path(posix):
        return False
    tokens = _architecture_repo_tokens(planning)
    if not tokens:
        return True
    return any(token in posix for token in tokens)


def record_read(payload: dict[str, Any], path: str) -> dict[str, Any]:
    state = load_state(payload)
    resolved = str(Path(path).expanduser())
    reads = [str(item) for item in state.get("read_paths", [])]
    if resolved not in reads:
        reads.append(resolved)
    state["read_paths"] = reads
    save_state(payload, state)
    return state


def apply_leave(payload: dict[str, Any], prompt: str) -> dict[str, Any]:
    state = load_state(payload)
    changed = False
    if prompt and prompt != state.get("last_prompt"):
        state["last_prompt"] = prompt
        changed = True
    if LEAVE_GENERIC_RE.search(prompt):
        state["generic_leave"] = True
        named = [item.group(0) for item in GENERIC_MODULE_NAME_RE.finditer(prompt)]
        if named:
            existing = [str(item) for item in state.get("generic_leave_modules", [])]
            for item in named:
                if item not in existing:
                    existing.append(item)
            state["generic_leave_modules"] = existing
        changed = True
    if LEAVE_GUEST_SQL_RE.search(prompt):
        state["guest_sql_leave"] = True
        changed = True
    if changed:
        save_state(payload, state)
    return state


def generic_leave_covers(state: dict[str, Any], path: str) -> bool:
    if not state.get("generic_leave"):
        return False
    modules = [str(item) for item in state.get("generic_leave_modules", [])]
    if not modules:
        return True
    posix = _posix(path)
    return any(fragment in posix for fragment in modules)


def _env_alias_in_generic(text: str) -> bool:
    for line in text.splitlines():
        if not ENV_ALIAS_RE.search(line):
            continue
        if re.search(r"(forbid|禁止|MUST NOT|do not)", line, re.I):
            continue
        if line.lstrip().startswith("#"):
            continue
        return True
    return False


def _cite(rule: str, text: str, pattern: re.Pattern[str] | None, message: str) -> str:
    lines: list[str] = []
    if pattern is not None and text:
        for index, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                lines.append(str(index))
    location = f" lines {', '.join(lines)}" if lines else ""
    return (
        f"99-hook-contract.md {rule}{location}. {message} "
        "Do not rewrite the content to evade this rule."
    )


def planning_status(payload: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    planning = find_planning_root(_workspace_root(payload))
    if planning is None:
        cwd = payload.get("cwd")
        if cwd:
            planning = find_planning_root(Path(str(cwd)))
    if planning is None:
        return {
            "planning_root": None,
            "decisions_required": False,
            "architecture_required": False,
            "decisions_read": True,
            "architecture_read": True,
        }
    decisions = planning / "decisions.md"
    architecture_files = sorted(planning.glob("architecture*.md"))
    reads = {str(Path(item).expanduser()) for item in state.get("read_paths", [])}
    decisions_read = (not decisions.is_file()) or str(decisions) in reads
    architecture_read = (not architecture_files) or any(
        str(item) in reads for item in architecture_files
    )
    return {
        "planning_root": str(planning),
        "decisions_required": decisions.is_file(),
        "architecture_required": bool(architecture_files),
        "decisions_read": decisions_read,
        "architecture_read": architecture_read,
        "decisions_path": str(decisions) if decisions.is_file() else None,
        "architecture_paths": [str(item) for item in architecture_files],
        "repo_tokens": _architecture_repo_tokens(planning),
    }


def _missing_planning_reason(path: str, status: dict[str, Any]) -> str | None:
    root = status.get("planning_root")
    if root is None:
        return None
    if not path_needs_planning_gate(path, Path(str(root))):
        return None
    missing: list[str] = []
    if status["decisions_required"] and not status["decisions_read"]:
        missing.append(status["decisions_path"])
    if status["architecture_required"] and not status["architecture_read"]:
        shown = status.get("architecture_paths") or []
        missing.append(
            "at least one of: " + ", ".join(shown[:4])
            if shown
            else "planning/architecture*.md"
        )
    if not missing:
        return None
    return _cite(
        "Section 3 Item A.1",
        "",
        None,
        "Architecture gate: read these files with read_file before mutating "
        "this covered tree: "
        + "; ".join(missing)
        + ". Then state move, name, DAG, and whether this edit is in scope.",
    )


def _deny(reason: str) -> int:
    print(json.dumps({"decision": "deny", "reason": reason}, ensure_ascii=False))
    return 2


def _allow(extra: dict[str, Any] | None = None) -> int:
    body: dict[str, Any] = {"decision": "allow"}
    if extra:
        body.update(extra)
    print(json.dumps(body, ensure_ascii=False))
    return 0


def _command(tool_input: dict[str, Any]) -> str:
    for key in ("command", "cmd", "shell_command", "script"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def evaluate_write(
    payload: dict[str, Any],
    path: str,
    text: str,
    command: str,
    before: str = "",
) -> str | None:
    state = load_state(payload)
    if path and _is_self_path(path):
        return None

    if (
        command
        and GUEST_SQL_CMD_RE.search(command)
        and not state.get("guest_sql_leave")
    ):
        return _cite(
            "Section 3 Item A.5",
            command,
            GUEST_SQL_CMD_RE,
            "Guest SQL is forbidden. Do not run psql, ALTER USER, or "
            "docker exec into a database to repair IaC drift.",
        )

    if command and not path:
        if WRITE_CMD_RE.search(command) and GENERIC_MODULE_RE.search(_posix(command)):
            if not generic_leave_covers(state, command):
                return _cite(
                    "Section 3 Item A.2",
                    command,
                    GENERIC_MODULE_RE,
                    "A shell write targeting terraform/modules or "
                    "ansible/roles/utils_* needs owner leave this session. "
                    "Owner phrase: 允許改通用模組.",
                )
        if READ_ONLY_CMD_RE.search(command):
            return None
        if WRITE_CMD_RE.search(command) and is_governed_path(command):
            return _missing_planning_reason(command, planning_status(payload, state))
        return None

    if not path:
        return None

    if is_generic_module(path) and not generic_leave_covers(state, path):
        return _cite(
            "Section 3 Item A.2",
            "",
            None,
            f"Generic module {path} is shared. Do not edit it without owner "
            "leave for this module in this session. Owner phrase: 允許改通用模組.",
        )

    if is_generic_module(path) and generic_leave_covers(state, path):
        if _added(before, text, HARDCODED_VAULT_PRODUCTION_RE):
            return _cite(
                "Section 3 Item A.3",
                text,
                HARDCODED_VAULT_PRODUCTION_RE,
                "Generic module still cannot hardcode vault.production. "
                "The caller binds the Vault provider.",
            )
        if _added(before, text, TAUTOLOGICAL_PROVIDER_RE):
            return _cite(
                "Section 3 Item A.3",
                text,
                TAUTOLOGICAL_PROVIDER_RE,
                "Tautological providers map vault = vault is forbidden.",
            )
        if _added(before, text, PRODUCT_TOKEN_RE):
            return _cite(
                "Section 3 Item A.4",
                text,
                PRODUCT_TOKEN_RE,
                "Generic module still cannot name a product in variables, "
                "resources, tags, or outputs. The caller supplies those values.",
            )
        if _env_alias_in_generic(text) and (
            not before or not _env_alias_in_generic(before)
        ):
            return _cite(
                "Section 3 Item A.3",
                text,
                ENV_ALIAS_RE,
                "Generic module still cannot hardcode environment aliases "
                "such as prod, stg, or dev.",
            )

    if path and introduces_bootstrapper_name(path):
        return (
            "99-hook-contract.md Section 3 Item A.4. Name gate: do not create "
            "a new path that still says bootstrapper. Existing leftover paths "
            "may stay until the planned rename. "
            "Do not rewrite the content to evade this rule."
        )

    if is_consumer_layer(path) and (
        _added(before, text, RANDOM_PASSWORD_RE)
        or _added(before, text, VAULT_CREDENTIAL_MODULE_RE)
    ):
        return _cite(
            "Section 3 Item A.5 / ENGINEERING_PRINCIPLES Section 3",
            text,
            RANDOM_PASSWORD_RE
            if RANDOM_PASSWORD_RE.search(text)
            else VAULT_CREDENTIAL_MODULE_RE,
            "Secret ownership: random_password and vault-credential writes "
            "belong in a vault, credential, pki, identity, or approle layer. "
            "This consumer layer reads a Vault path.",
        )

    if _added(before, text, TAUTOLOGICAL_PROVIDER_RE):
        return _cite(
            "Section 3 Item A.3",
            text,
            TAUTOLOGICAL_PROVIDER_RE,
            "Tautological providers map vault = vault is forbidden.",
        )

    if _added(before, text, PROVISIONER_RE):
        return _cite(
            "Section 3 Item A.5",
            text,
            PROVISIONER_RE,
            "local-exec and remote-exec are forbidden in automation.",
        )

    posix = _posix(path)
    if ("/ansible/" in posix) and _added(before, text, ANSIBLE_SHELL_RE):
        if not ANSIBLE_IDEMPOTENT_RE.search(text):
            return _cite(
                "Section 3 Item A.5",
                text,
                ANSIBLE_SHELL_RE,
                "ansible.builtin.shell and command require changed_when, "
                "creates, or removes.",
            )

    if ("/ansible/" in posix) and _added(before, text, ANSIBLE_SQL_RE):
        if not re.search(r"(forbid|禁止|MUST NOT|do not).{0,40}psql", text, re.I):
            return _cite(
                "Section 3 Item A.5",
                text,
                ANSIBLE_SQL_RE,
                "Ansible must not run psql or community.postgresql to patch "
                "guest passwords.",
            )

    if is_governed_path(path):
        return _missing_planning_reason(path, planning_status(payload, state))
    return None


def handle_pre_tool_use(payload: dict[str, Any]) -> int:
    tool = _norm_tool(payload)
    tool_input = _tool_input(payload)
    path = _file_path(tool_input)
    text = _new_text(tool_input)
    command = _command(tool_input)
    before = _old_text(tool_input, path)

    if tool in READ_TOOLS and path:
        record_read(payload, path)
        return _allow()

    if tool not in MUTATING_TOOLS:
        return _allow()

    reason = evaluate_write(payload, path, text, command, before=before)
    if reason:
        return _deny(reason)
    return _allow()


def handle_post_tool_use(payload: dict[str, Any]) -> int:
    tool = _norm_tool(payload)
    path = _file_path(_tool_input(payload))
    if tool in READ_TOOLS and path:
        record_read(payload, path)
    return 0


def handle_user_prompt(payload: dict[str, Any]) -> int:
    prompt = _prompt_text(payload)
    if prompt:
        apply_leave(payload, prompt)
    return 0


def handle_session_start(payload: dict[str, Any]) -> int:
    load_state(payload)
    return 0


def dispatch(payload: dict[str, Any]) -> int:
    if _hook_disabled():
        return _allow() if _norm_event(payload) == "pretooluse" else 0
    event = _norm_event(payload)
    if event == "pretooluse":
        return handle_pre_tool_use(payload)
    if event == "posttooluse":
        return handle_post_tool_use(payload)
    if event == "userpromptsubmit":
        return handle_user_prompt(payload)
    if event == "sessionstart":
        return handle_session_start(payload)
    return 0


def _self_test() -> int:
    failures: list[str] = []

    def expect(name: str, got: str | None, want_substr: str | None) -> None:
        if want_substr is None:
            if got is not None:
                failures.append(f"{name}: expected allow, got {got!r}")
            return
        if got is None or want_substr not in got:
            failures.append(f"{name}: expected {want_substr!r} in {got!r}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        planning = tmp_path / "planning"
        planning.mkdir()
        (planning / "decisions.md").write_text("adjudication\n", encoding="utf-8")
        (planning / "architecture.md").write_text("overview\n", encoding="utf-8")
        (planning / "architecture_meta-platform.md").write_text(
            "meta-platform\n", encoding="utf-8"
        )
        os.environ["ENGINEERING_PRINCIPLES_STATE_DIR"] = str(tmp_path / "state")
        os.environ["GROK_SESSION_ID"] = "test-session"
        os.environ["GROK_WORKSPACE_ROOT"] = str(tmp_path)
        os.environ.pop("ENGINEERING_PRINCIPLES_HOOK", None)
        payload = {
            "hookEventName": "PreToolUse",
            "sessionId": "test-session",
            "workspaceRoot": str(tmp_path),
            "cwd": str(tmp_path),
        }

        module_path = str(
            tmp_path
            / "meta-platform/terraform/modules/vault-provisioning/vault-credential/resources.tf"
        )
        layer_path = str(
            tmp_path / "meta-platform/terraform/layers/shared-harbor-frontend/main.tf"
        )
        mint_path = str(
            tmp_path / "meta-platform/terraform/layers/foundation-vault-bastion/main.tf"
        )
        fullstack_tf = str(tmp_path / "personal/app-content-matter/terraform/main.tf")

        expect(
            "generic-deny",
            evaluate_write(payload, module_path, "variable x {}", ""),
            "Generic module",
        )
        apply_leave(payload, "允許改通用模組")
        expect(
            "generic-leave-overfit",
            evaluate_write(
                payload,
                module_path,
                'name = "harbor-origin/frontend"\n',
                "",
            ),
            "cannot name a product",
        )
        expect(
            "generic-leave-production",
            evaluate_write(payload, module_path, "provider = vault.production\n", ""),
            "vault.production",
        )
        expect(
            "generic-leave-tautology",
            evaluate_write(
                payload,
                module_path,
                "providers = { vault = vault }\n",
                "",
            ),
            "Tautological",
        )
        expect(
            "generic-leave-clean",
            evaluate_write(
                payload,
                module_path,
                'resource "vault_kv_secret_v2" "this" {}\n',
                "",
            ),
            "Architecture gate",
        )

        record_read(payload, str(planning / "decisions.md"))
        record_read(payload, str(planning / "architecture.md"))
        expect(
            "generic-after-arch",
            evaluate_write(
                payload,
                module_path,
                'resource "vault_kv_secret_v2" "this" {}\n',
                "",
            ),
            None,
        )

        expect(
            "consumer-secret",
            evaluate_write(
                payload,
                layer_path,
                'resource "random_password" "db" {}\n',
                "",
            ),
            "Secret ownership",
        )
        expect(
            "consumer-module",
            evaluate_write(
                payload,
                layer_path,
                'source = "../../modules/vault-provisioning/vault-credential"\n',
                "",
            ),
            "Secret ownership",
        )
        expect(
            "mint-layer-ok",
            evaluate_write(
                payload,
                mint_path,
                'source = "../../modules/vault-provisioning/vault-credential"\n',
                "",
            ),
            None,
        )
        expect(
            "guest-sql",
            evaluate_write(
                payload,
                "",
                "",
                "ssh harbor psql -c 'ALTER USER postgres PASSWORD foo'",
            ),
            "Guest SQL",
        )
        expect(
            "read-only-psql-mention",
            evaluate_write(payload, "", "", "rg -n psql ansible/roles"),
            None,
        )
        leftover = (
            tmp_path
            / "meta-platform/terraform/layers/shared-harbor-bootstrapper-frontend"
        )
        leftover.mkdir(parents=True)
        expect(
            "new-bootstrapper-name",
            evaluate_write(
                payload,
                str(
                    tmp_path
                    / "meta-platform/terraform/layers/new-harbor-bootstrapper/main.tf"
                ),
                "locals {}\n",
                "",
            ),
            "Name gate",
        )
        expect(
            "legacy-bootstrapper-tree",
            evaluate_write(
                payload,
                str(leftover / "data.tf"),
                "locals {}\n",
                "",
            ),
            None,
        )
        expect(
            "ansible-sql",
            evaluate_write(
                payload,
                str(
                    tmp_path
                    / "meta-platform/ansible/roles/shared_harbor/tasks/C-deploy.yaml"
                ),
                "- ansible.builtin.shell: psql -c 'select 1'\n",
                "",
            ),
            "Section 3 Item A.5",
        )
        expect(
            "fullstack-tf-no-arch",
            evaluate_write(payload, fullstack_tf, "locals {}\n", ""),
            None,
        )
        expect(
            "unpinned-image-allowed",
            evaluate_write(
                payload,
                layer_path,
                'image = "goharbor/harbor-core:v2.13.1"\n',
                "",
            ),
            None,
        )
        lock_path = str(tmp_path / "meta-platform/terraform/.terraform.lock.hcl")
        expect(
            "lockfile-allowed",
            evaluate_write(payload, lock_path, "provider hashes\n", ""),
            None,
        )

        existing_play = (
            tmp_path / "meta-platform/ansible/roles/shared_harbor/tasks/keep.yaml"
        )
        existing_play.parent.mkdir(parents=True, exist_ok=True)
        existing_body = "- name: already present\n  ansible.builtin.shell: echo hi\n"
        existing_play.write_text(existing_body, encoding="utf-8")
        expect(
            "existing-shell-untouched",
            evaluate_write(
                payload,
                str(existing_play),
                existing_body + "- name: comment only\n  debug: msg=x\n",
                "",
                before=existing_body,
            ),
            None,
        )
        expect(
            "new-shell-without-changed-when",
            evaluate_write(
                payload,
                str(existing_play),
                existing_body + "- ansible.builtin.shell: wipe\n",
                "",
                before=existing_body,
            ),
            "Section 3 Item A.5",
        )

        fresh = {
            "hookEventName": "PreToolUse",
            "sessionId": "fresh-session",
            "workspaceRoot": str(tmp_path),
            "cwd": str(tmp_path),
        }
        os.environ["GROK_SESSION_ID"] = "fresh-session"
        expect(
            "arch-before-layer",
            evaluate_write(fresh, layer_path, "locals {}\n", ""),
            "Architecture gate",
        )
        expect(
            "arch-not-required-for-fullstack",
            evaluate_write(fresh, fullstack_tf, "locals {}\n", ""),
            None,
        )

        os.environ["GROK_SESSION_ID"] = "dispatch-session"
        os.environ["GROK_WORKSPACE_ROOT"] = str(tmp_path)
        os.environ.pop("GROK_HOOK_EVENT", None)
        deny_payload = {
            "hookEventName": "PreToolUse",
            "sessionId": "dispatch-session",
            "workspaceRoot": str(tmp_path),
            "cwd": str(tmp_path),
            "toolName": "search_replace",
            "toolInput": {
                "file_path": module_path,
                "new_string": "locals {}\n",
            },
        }
        buf = StringIO()
        with redirect_stdout(buf):
            code = handle_pre_tool_use(deny_payload)
        if code != 2 or "Generic module" not in buf.getvalue():
            failures.append(
                f"dispatch-generic: expected deny Generic module, got {code} {buf.getvalue()!r}"
            )

        prompt_payload = {
            "hookEventName": "UserPromptSubmit",
            "sessionId": "dispatch-session",
            "workspaceRoot": str(tmp_path),
            "cwd": str(tmp_path),
            "prompt": "請處理 terraform layer 的密鑰生命週期",
        }
        buf = StringIO()
        with redirect_stdout(buf):
            code = handle_user_prompt(prompt_payload)
        out = buf.getvalue().strip()
        if code != 0 or out:
            failures.append(
                f"prompt-silent: expected no context injection, got {code} {out!r}"
            )
        buf = StringIO()
        with redirect_stdout(buf):
            handle_user_prompt({**prompt_payload, "prompt": "今天天氣如何"})
        quiet = buf.getvalue().strip()
        if quiet:
            failures.append(f"non-pe-prompt: expected silence, got {quiet!r}")

        start_payload = {
            "hookEventName": "SessionStart",
            "sessionId": "dispatch-session",
            "workspaceRoot": str(tmp_path),
            "cwd": str(tmp_path),
        }
        buf = StringIO()
        with redirect_stdout(buf):
            handle_session_start(start_payload)
        start_out = buf.getvalue().strip()
        if start_out:
            failures.append(
                f"session-start-silent: expected silence, got {start_out!r}"
            )

        os.environ["GROK_SESSION_ID"] = "scope-session"
        scope_payload = {
            "hookEventName": "PreToolUse",
            "sessionId": "scope-session",
            "workspaceRoot": str(tmp_path),
            "cwd": str(tmp_path),
        }
        apply_leave(scope_payload, "允許改通用模組 vault-credential")
        record_read(scope_payload, str(planning / "decisions.md"))
        record_read(scope_payload, str(planning / "architecture.md"))
        other_module = str(
            tmp_path
            / "meta-platform/terraform/modules/kvm-foundation-resources/main.tf"
        )
        expect(
            "scoped-leave-other-module",
            evaluate_write(scope_payload, other_module, "locals {}\n", ""),
            "Section 3 Item A.2",
        )
        expect(
            "local-exec",
            evaluate_write(
                scope_payload,
                layer_path,
                'provisioner "local-exec" { command = "true" }\n',
                "",
            ),
            "Section 3 Item A.5",
        )
        expect(
            "alter-user-in-commit-message",
            evaluate_write(
                payload,
                "",
                "",
                "git commit -m 'document ALTER USER flow'",
            ),
            None,
        )
        expect(
            "alter-user-via-psql",
            evaluate_write(
                payload,
                "",
                "",
                "psql -c 'ALTER USER postgres PASSWORD foo'",
            ),
            "Guest SQL",
        )

        huge = tmp_path / "huge-old.txt"
        huge.write_bytes(b"x" * (OLD_TEXT_MAX_BYTES + 1))
        if _old_text({}, str(huge)) != "":
            failures.append("old-text-cap: expected empty string for oversized file")

        cmd_alias_input = {"cmd": "ssh harbor psql -c 'select 1'"}
        if "psql" not in _command(cmd_alias_input):
            failures.append("command-alias: expected cmd key to be read")

        saved_session = os.environ.pop("GROK_SESSION_ID", None)
        bare = {"workspaceRoot": str(tmp_path), "cwd": str(tmp_path)}
        first_id = _session_id(bare)
        second_id = _session_id(bare)
        if first_id == second_id or first_id == "unknown" or second_id == "unknown":
            failures.append(
                f"session-ephemeral: expected distinct non-unknown ids, got {first_id!r} {second_id!r}"
            )
        leave_payload = {
            "hookEventName": "UserPromptSubmit",
            "workspaceRoot": str(tmp_path),
            "cwd": str(tmp_path),
        }
        apply_leave(leave_payload, "允許改通用模組")
        other_payload = {
            "hookEventName": "PreToolUse",
            "workspaceRoot": str(tmp_path),
            "cwd": str(tmp_path),
        }
        expect(
            "missing-session-no-leave-leak",
            evaluate_write(other_payload, module_path, "variable x {}", ""),
            "Generic module",
        )
        if saved_session is not None:
            os.environ["GROK_SESSION_ID"] = saved_session

    if failures:
        sys.stderr.write("self-test failed:\n" + "\n".join(failures) + "\n")
        return 1
    sys.stderr.write("self-test passed\n")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
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
        event = _norm_event(payload)
        sys.stderr.write(f"engineering-principles hook error: {exc}\n")
        traceback.print_exc(file=sys.stderr)
        if event == "pretooluse" and _norm_tool(payload) in MUTATING_TOOLS:
            return _deny(f"hook error while evaluating a write: {exc}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
