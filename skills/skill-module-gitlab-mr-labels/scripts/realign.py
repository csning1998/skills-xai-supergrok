#!/usr/bin/env python3
"""Apply layer supplied merge request label tables through glab."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

from glab import list_merge_requests
from glab import run_glab
from labels import compute_labels
from labels import label_names
from labels import project_path
from labels import validate_tables


def fail(error: str) -> dict[str, Any]:
    """Return a failed GitlabMrLabelResult body."""
    return {
        "ok": False,
        "error": error,
        "mode": None,
        "total": 0,
        "noop": 0,
        "changed": 0,
        "applied": 0,
        "failed": [],
        "changes": [],
    }


def main() -> int:
    """Read payload_path, compute changes, optionally PUT labels."""
    if len(sys.argv) != 2:
        json.dump(fail("payload_path missing"), sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 1
    payload_path = Path(sys.argv[1])
    cfg = json.loads(payload_path.read_text(encoding="utf-8"))
    mode = cfg.get("mode")
    group = cfg.get("group")
    tables = cfg.get("tables")
    if (
        mode not in {"dry-run", "apply"}
        or not group
        or not isinstance(tables, dict)
    ):
        json.dump(
            fail("mode, group, or tables missing"),
            sys.stdout,
            ensure_ascii=False,
        )
        sys.stdout.write("\n")
        return 1
    table_error = validate_tables(tables)
    if table_error:
        json.dump(fail(table_error), sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 1

    auth = run_glab(["auth", "status"])
    if auth.returncode != 0:
        json.dump(
            fail(auth.stderr or "glab auth status failed"),
            sys.stdout,
            ensure_ascii=False,
        )
        sys.stdout.write("\n")
        return 1

    listed = list_merge_requests(
        group, bool(cfg.get("include_subgroups", True))
    )
    if isinstance(listed, str):
        json.dump(fail(listed), sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 1

    only_if_changed = bool(cfg.get("only_if_changed", True))
    allow_clear = bool(cfg.get("allow_clear", False))
    sleep_s = float(cfg.get("sleep_s", 0.25))
    changes: list[dict[str, Any]] = []
    noop = 0
    for mr in listed:
        old = sorted(label_names(mr.get("labels")))
        path = project_path(mr)
        try:
            new = compute_labels(mr.get("title") or "", old, path, tables)
        except (ValueError, KeyError, TypeError) as exc:
            json.dump(
                fail(f"label tables: {exc}"),
                sys.stdout,
                ensure_ascii=False,
            )
            sys.stdout.write("\n")
            return 1
        if only_if_changed and old == new:
            noop += 1
            continue
        if not new and not allow_clear:
            noop += 1
            continue
        changes.append(
            {
                "project_id": mr.get("project_id"),
                "iid": mr.get("iid"),
                "path": path,
                "title": mr.get("title"),
                "web_url": mr.get("web_url"),
                "old": old,
                "new": new,
            }
        )

    applied = 0
    failed: list[dict[str, str]] = []
    if mode == "apply":
        for index, row in enumerate(changes, 1):
            ident = f"{row['path']}!{row['iid']}"
            value = ",".join(row["new"])
            proc = run_glab(
                [
                    "api",
                    "--method",
                    "PUT",
                    (
                        f"projects/{row['project_id']}"
                        f"/merge_requests/{row['iid']}"
                    ),
                    "-f",
                    f"labels={value}",
                ]
            )
            if proc.returncode == 0:
                applied += 1
            else:
                err = (proc.stderr or proc.stdout or "")[:500]
                failed.append({"id": ident, "error": err})
                print(f"# FAIL {ident}", file=sys.stderr, flush=True)
            if index % 20 == 0 or index == len(changes):
                print(
                    f"# progress {index}/{len(changes)} "
                    f"applied={applied} fail={len(failed)}",
                    file=sys.stderr,
                    flush=True,
                )
            time.sleep(sleep_s)

    result = {
        "ok": len(failed) == 0,
        "error": None if not failed else f"{len(failed)} apply failures",
        "mode": mode,
        "total": len(listed),
        "noop": noop,
        "changed": len(changes),
        "applied": applied,
        "failed": failed,
        "changes": changes,
    }
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
