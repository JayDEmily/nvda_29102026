"""Rerun all retained M13 falsification sets into V7-owned evidence."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

WORKER = Path(__file__).resolve().parent
V6_RUNNER = WORKER.parent / "v6_worker/run_retained_regression.py"
SPEC = importlib.util.spec_from_file_location("_m13_v7_retained", V6_RUNNER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load retained runner: {V6_RUNNER}")
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)
module.OUTPUT = WORKER / "retained_mutant_runs"

if __name__ == "__main__":
    module.main()
