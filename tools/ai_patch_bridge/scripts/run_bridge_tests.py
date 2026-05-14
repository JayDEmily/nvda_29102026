#!/usr/bin/env python3
"""Repo-local wrapper for the stdlib-only bridge test runner."""

from __future__ import annotations

from contextlib import suppress
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[0]
SRC = REPO_ROOT / "src"
with suppress(ValueError):
    sys.path.remove(str(SCRIPT_DIR))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ai_patch_bridge.test_runner import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
