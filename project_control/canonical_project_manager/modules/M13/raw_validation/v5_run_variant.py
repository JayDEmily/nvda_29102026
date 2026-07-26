from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import pytest


MATRIX_TEST_NAME = "test_m13_unsuccessful_execute_attempt_leaves_no_binding_matrix"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the M13 V5 proof family against an isolated evidence implementation."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--frozen-fourteen", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument(
        "--test-file",
        default="tests/tier_a/persistence/test_m13_state_kernel_contract.py",
    )
    args = parser.parse_args()

    module_name = "nvda_desk.m13_state_kernel"
    spec = importlib.util.spec_from_file_location(module_name, args.source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load M13 evidence source: {args.source}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    pytest_args = ["-q" if args.quiet else "-vv", args.test_file]
    if args.frozen_fourteen:
        pytest_args.extend(["-k", f"not {MATRIX_TEST_NAME}"])
    elif args.case:
        pytest_args.extend(["-k", args.case])
    return int(pytest.main(pytest_args))


if __name__ == "__main__":
    raise SystemExit(main())
