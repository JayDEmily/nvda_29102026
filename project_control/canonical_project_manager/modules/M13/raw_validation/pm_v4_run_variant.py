from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import pytest


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the M13 proof against an isolated evidence implementation.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--original-twelve", action="store_true")
    parser.add_argument("--original-thirteen", action="store_true")
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

    pytest_args = ["-q", args.test_file]
    if args.original_thirteen:
        pytest_args.extend(["-k", "not test_m13_failed_transaction_does_not_bind_idempotency_key_and_fresh_reuse_commits_once"])
    elif args.original_twelve:
        pytest_args.extend(
            [
                "-k",
                "not test_m13_later_prepare_failure_rolls_back_every_prepared_participant_and_allows_clean_retry",
            ]
        )
    return int(pytest.main(pytest_args))


if __name__ == "__main__":
    raise SystemExit(main())
