#!/usr/bin/env python3
"""Grok hook entry. The package lives beside this script."""

from __future__ import annotations

import sys
from pathlib import Path


_HOOKS_ROOT = Path(__file__).resolve().parent.parent
if str(_HOOKS_ROOT) not in sys.path:
    sys.path.insert(0, str(_HOOKS_ROOT))

from engineering_principles.dispatch import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
