"""Validate the SQLite C engine actually linked into the selected Python runtime.

SQLite is not a Python package pin. The exact external C engine version is
recorded in pyproject.toml [tool.nvda.runtime] and must be checked at runtime.
This utility is a non-product environment preflight, not an NVDA acceptance test.
"""

from __future__ import annotations

import json
import sqlite3
import sys
import tomllib
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    with (repo_root / "pyproject.toml").open("rb") as f:
        spec = tomllib.load(f)

    pin = spec["tool"]["nvda"]["runtime"]["sqlite3_version"]
    required_python = spec["project"]["requires-python"].removeprefix("==")
    actual_python = ".".join(str(x) for x in sys.version_info[:3])
    with sqlite3.connect(":memory:") as c:
        source_id = c.execute("SELECT sqlite_source_id()").fetchone()[0]

    ok = actual_python == required_python and sqlite3.sqlite_version == pin
    print(
        json.dumps(
            {
                "check": "NVDA_RUNTIME_SQLITE_PIN",
                "python_expected": required_python,
                "python_actual": actual_python,
                "sqlite_expected": pin,
                "sqlite_actual": sqlite3.sqlite_version,
                "sqlite_source_id": source_id,
                "pass": ok,
                "scope": "non-product, runtime pin only",
            },
            sort_keys=True,
        )
    )
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
