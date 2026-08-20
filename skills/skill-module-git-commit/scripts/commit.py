#!/usr/bin/env python3
"""Run or print batched git add and git commit. Never push."""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


def fail(error: str) -> dict[str, Any]:
    """Return a failed GitCommitResult body."""
    return {
        "ok": False,
        "error": error,
        "execute": False,
        "commands": [],
        "committed": [],
    }


def emit_fail(error: str) -> int:
    """Print a failed GitCommitResult and return 1."""
    json.dump(fail(error), sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 1


def run_git(repo: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run git in repo_root."""
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def shell_commit_command(paths: list[str], message: str) -> list[str]:
    """Return printable add and commit lines for the owner."""
    joined = " ".join(shlex.quote(item) for item in paths)
    return [
        f"git add {joined}",
        f"git commit -m {shlex.quote(message)}",
    ]


def load_payload(path: str) -> dict[str, Any] | str:
    """Return the JSON object, or an error string."""
    try:
        raw = Path(path).read_text(encoding="utf-8")
        cfg = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return "payload is not valid JSON"
    if not isinstance(cfg, dict):
        return "payload is not valid JSON"
    return cfg


def git_toplevel(repo: Path) -> Path | None:
    """Return the resolved git toplevel for repo, or None."""
    proc = run_git(repo, ["rev-parse", "--show-toplevel"])
    if proc.returncode != 0:
        return None
    top = (proc.stdout or "").strip()
    if not top:
        return None
    return Path(top).resolve()


def path_is_inside_repo(repo: Path, path: str) -> bool:
    """Return True when path stays under the resolved repo root."""
    resolved = (repo / path).resolve()
    root = repo.resolve()
    return root in resolved.parents or resolved == root


def batch_paths(batch: Any) -> list[str] | None:
    """Return path strings from one commit batch, or None."""
    if not isinstance(batch, dict):
        return None
    paths = batch.get("paths")
    if not isinstance(paths, list) or not paths:
        return None
    if not all(isinstance(item, str) and item for item in paths):
        return None
    return paths


def main() -> int:
    """Read payload_path and add plus commit, or print commands."""
    if len(sys.argv) != 2:
        return emit_fail("payload_path missing")
    cfg = load_payload(sys.argv[1])
    if isinstance(cfg, str):
        return emit_fail(cfg)
    repo = Path(cfg.get("repo_root") or "")
    commits = cfg.get("commits")
    try:
        header_max = int(cfg.get("header_max") or 100)
    except (TypeError, ValueError):
        return emit_fail("invalid header_max")
    execute = bool(cfg.get("execute"))
    if not repo or not isinstance(commits, list):
        return emit_fail("repo_root or commits missing")
    if not repo.is_absolute():
        return emit_fail("repo_root must be an absolute path")
    top = git_toplevel(repo)
    if top is None or top != repo.resolve():
        return emit_fail("repo_root is not the git toplevel")
    if cfg.get("allow_push"):
        return emit_fail("git push is forbidden")

    commands: list[str] = []
    committed: list[str] = []
    for batch in commits:
        paths = batch_paths(batch)
        message = batch.get("message") if isinstance(batch, dict) else None
        if paths is None or not isinstance(message, str) or not message:
            return emit_fail("each commit needs paths and message")
        if "\n" in message or len(message) >= header_max:
            return emit_fail(f"invalid header: {message!r}")
        for path in paths:
            if not path_is_inside_repo(repo, path):
                return emit_fail(f"path outside repo_root: {path}")
        commands.extend(shell_commit_command(paths, message))
        if not execute:
            continue
        add = run_git(repo, ["add", "--", *paths])
        if add.returncode != 0:
            return emit_fail(add.stderr or "git add failed")
        commit = run_git(repo, ["commit", "-m", message])
        if commit.returncode != 0:
            return emit_fail(commit.stderr or "git commit failed")
        sha = run_git(repo, ["rev-parse", "HEAD"])
        committed.append((sha.stdout or "").strip())

    result = {
        "ok": True,
        "error": None,
        "execute": execute,
        "commands": commands,
        "committed": committed,
    }
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
