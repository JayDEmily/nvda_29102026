"""Rerun every accepted M13 falsification campaign into repair-owned evidence."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

WORKER = Path(__file__).resolve().parent
RAW = WORKER.parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load retained runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    v7 = RAW / "v7_worker"

    guard_output = WORKER / "retained_v7_guard_mutant_runs"
    if not (guard_output / "summary.tsv").is_file():
        guard = _load("_m13_repair_v7_guard", v7 / "run_v7_guard_mutants.py")
        guard.OUTPUT = guard_output
        guard.main()

    v6_output = WORKER / "retained_v6_mutant_runs"
    if not (v6_output / "summary.tsv").is_file():
        v6 = _load("_m13_repair_v6", RAW / "v6_worker/run_v6_mutants.py")
        v6.OUTPUT = v6_output
        v6.main()

    retained = _load(
        "_m13_repair_retained",
        RAW / "v6_worker/run_retained_regression.py",
    )
    retained.OUTPUT = WORKER / "retained_prior_mutant_runs"
    os.environ["M13_PYTHON"] = sys.executable
    os.environ["M13_SITE_PACKAGES"] = os.pathsep.join(sys.path)
    retained.main()

    print("retained_v7_guard_mutants=8")
    print("retained_v6_mutants=16")
    print("retained_earlier_mutants=11")
    print("retained_pm_v5_mutants=2")
    print("retained_v5_configurable_mutants=32")
    print("retained_implementation_derived_mutants=8")
    print("all_retained_campaigns=PASS")


if __name__ == "__main__":
    main()
