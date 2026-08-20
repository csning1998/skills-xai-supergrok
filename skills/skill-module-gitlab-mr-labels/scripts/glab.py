"""glab subprocess helper with HTTP 429 backoff and a 60s timeout."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from typing import Any


GLAB_TIMEOUT_S = 60
GLAB_TIMEOUT_TRIES = 5


def _timeout_proc(
    args: list[str], timeouts: int
) -> subprocess.CompletedProcess[str]:
    """Return a failed process record for a hung glab call."""
    return subprocess.CompletedProcess(
        args=["glab", *args],
        returncode=124,
        stdout="",
        stderr=(
            f"glab timed out after {GLAB_TIMEOUT_S}s "
            f"({timeouts}/{GLAB_TIMEOUT_TRIES})"
        ),
    )


def run_glab(
    args: list[str], retries: int = 8
) -> subprocess.CompletedProcess[str]:
    """Run glab. Retry rate limits. Retry timeouts up to five times."""
    wait = 10
    last: subprocess.CompletedProcess[str] | None = None
    timeouts = 0
    for _ in range(retries):
        try:
            last = subprocess.run(
                ["glab", *args],
                capture_output=True,
                text=True,
                timeout=GLAB_TIMEOUT_S,
                check=False,
            )
        except subprocess.TimeoutExpired:
            timeouts += 1
            last = _timeout_proc(args, timeouts)
            print(f"# {last.stderr}", file=sys.stderr, flush=True)
            if timeouts >= GLAB_TIMEOUT_TRIES:
                print(
                    "# glab timeout exhausted. Tell the owner.",
                    file=sys.stderr,
                    flush=True,
                )
                last.stderr = (
                    f"glab timed out after {GLAB_TIMEOUT_S}s on "
                    f"{GLAB_TIMEOUT_TRIES} tries. Tell the owner."
                )
                return last
            continue
        combined = (last.stderr or "") + (last.stdout or "")
        if last.returncode == 0:
            return last
        limited = (
            "429" in combined
            or "Too Many Requests" in combined
            or "rate limit" in combined.lower()
        )
        if limited:
            print(f"# 429 sleep {wait}s", file=sys.stderr, flush=True)
            time.sleep(wait)
            wait = min(60, wait + 10)
            continue
        return last
    assert last is not None
    return last


def list_merge_requests(
    group: str, include_subgroups: bool
) -> list[dict[str, Any]] | str:
    """Page group merge requests. Return an error string on failure."""
    records: list[dict[str, Any]] = []
    page = 1
    flag = "true" if include_subgroups else "false"
    while True:
        path = (
            f"groups/{group}/merge_requests"
            f"?scope=all&state=all&include_subgroups={flag}"
            f"&per_page=100&page={page}"
        )
        proc = run_glab(["api", path])
        if proc.returncode != 0:
            return (proc.stderr or proc.stdout or "glab api list failed")[:800]
        chunk = json.loads(proc.stdout) if proc.stdout.strip() else []
        if not chunk:
            break
        records.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1
        time.sleep(0.2)
    return records
