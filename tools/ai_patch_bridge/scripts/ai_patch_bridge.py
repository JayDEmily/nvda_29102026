#!/usr/bin/env python3
"""Repo-local wrapper for the AI_PATCH_V1 bridge CLI."""

from __future__ import annotations

import sys
from contextlib import suppress
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[0]
SRC = REPO_ROOT / "src"
# Avoid this wrapper file shadowing the real ai_patch_bridge package.
with suppress(ValueError):
    sys.path.remove(str(SCRIPT_DIR))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ai_patch_bridge.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
