"""Console entrypoint for ai-patch-bridge."""

from __future__ import annotations

import sys

from ai_patch_bridge.receipt_failure_hardening import main

if __name__ == "__main__":
    raise SystemExit(main())
