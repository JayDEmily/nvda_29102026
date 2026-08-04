#!/usr/bin/env python3
from pathlib import Path

from nvda_desk.architecture.dependencies import analyse_repository

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    violations = [item for item in analyse_repository(root) if item.code == "PRIVATE_SEAM"]
    for violation in violations:
        print(f"{violation.source_file}:{violation.line}: {violation.message}")
    raise SystemExit(1 if violations else 0)
