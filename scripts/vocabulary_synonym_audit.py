from __future__ import annotations

import importlib
import sys
from pathlib import Path

_REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_REPO_SRC) not in sys.path:
    sys.path.insert(0, str(_REPO_SRC))

_audit = importlib.import_module("nvda_desk.vocabulary_synonym_audit")
build_report = _audit.build_report
main = _audit.main
write_report = _audit.write_report
write_stamp = _audit.write_stamp

__all__ = ["build_report", "main", "write_report", "write_stamp"]

if __name__ == "__main__":
    raise SystemExit(main())
