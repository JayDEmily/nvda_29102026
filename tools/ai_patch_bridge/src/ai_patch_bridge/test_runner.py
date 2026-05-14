#!/usr/bin/env python3
"""Stdlib-only bridge test runner.

This avoids making the bridge's own smoke/regression tests depend on pytest.
Project repos can still run pytest/ruff/black as their own Makefile gates.
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from types import ModuleType


def load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load test module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    test_dir = repo_root / "tests"
    if str(repo_root / "src") not in sys.path:
        sys.path.insert(0, str(repo_root / "src"))

    tests: list[tuple[str, object]] = []
    for path in sorted(test_dir.glob("test_*.py")):
        module = load_module(path)
        for name in sorted(dir(module)):
            obj = getattr(module, name)
            if name.startswith("test_") and callable(obj):
                tests.append((f"{path.name}::{name}", obj))

    failures = 0
    for name, test in tests:
        try:
            test()
        except Exception:  # noqa: BLE001 - test runner must report all failures.
            failures += 1
            print(f"FAIL {name}")
            traceback.print_exc()
        else:
            print(f"PASS {name}")

    print(f"Ran {len(tests)} bridge tests; failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
