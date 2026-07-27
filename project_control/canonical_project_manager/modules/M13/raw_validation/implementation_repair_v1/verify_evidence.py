"""Verify the tracked M13 implementation-repair evidence inventory."""

from __future__ import annotations

import hashlib
from pathlib import Path

WORKER = Path(__file__).resolve().parent
INVENTORY = WORKER / "M13_IMPLEMENT_REPAIR_V1_EVIDENCE_SHA256SUMS.txt"


def main() -> None:
    checked = 0
    for line in INVENTORY.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        expected, relative = line.split("\t", 1)
        actual = hashlib.sha256((WORKER / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"evidence hash mismatch: {relative}")
        checked += 1
    print(f"evidence_files_verified={checked}")
    print("evidence_integrity=PASS")


if __name__ == "__main__":
    main()
