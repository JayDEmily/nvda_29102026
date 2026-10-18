#!/usr/bin/env python3
"""Run exactly one admitted claim with complete observed proof and integrity."""

from __future__ import annotations

import argparse
import os
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path

from product_proof_claims import governed_snapshot, load_product_proof_claim, read_json
from product_proof_outcomes import validate_outcomes


def _git_status(repository_root: Path) -> str:
    return subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=repository_root, text=True
    )


def run_product_proof(repository_root: Path, aggregate_id: str) -> int:
    root = repository_root.resolve()
    before = _git_status(root)
    if before:
        print("FAIL: worktree is not clean before product-proof aggregate")
        return 2
    try:
        claim = load_product_proof_claim(root, aggregate_id)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {exc}")
        return 3 if "unknown" in str(exc) else 1
    print(f"product-proof aggregate: {claim.claim_id} state={claim.state}")
    if claim.state != "READY_FOR_PROOF" or claim.target_status != "active":
        print("FAIL: selected claim has no ready active admitted proof target")
        return 4
    paths = [family.path for family in claim.families]
    if not paths:
        return 5
    expected = {family.path: family.required_test_names for family in claim.families}
    nonce = secrets.token_hex(32)
    result = 1
    try:
        with tempfile.TemporaryDirectory(prefix="nvda-product-outcomes-") as directory:
            report_path = Path(directory) / "outcomes.json"
            env = os.environ.copy()
            env.pop("PYTEST_ADDOPTS", None)
            env["NVDA_PROOF_REPORT"] = str(report_path)
            env["NVDA_PROOF_NONCE"] = nonce
            env["PYTHONPATH"] = os.pathsep.join([str(root / "tools"), str(root / "src")])
            env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
            print(f"authority={claim.authority_sha256} generation={claim.generation_sha256}")
            candidate = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True)
            print(f"candidate={candidate.strip()}")
            completed = subprocess.run(
                [sys.executable, "-m", "pytest", "-p", "product_proof_outcomes", *paths],
                cwd=root,
                env=env,
                check=False,
            )
            result = validate_outcomes(
                read_json(report_path), nonce, expected, completed.returncode
            )
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL: attributable proof execution/report failure: {exc}")
        result = 1
    finally:
        try:
            if _git_status(root) != before or governed_snapshot(root) != claim.governed_files:
                print("FAIL: governed bytes or repository state changed during proof")
                result = 6
        except (ValueError, OSError, subprocess.SubprocessError):
            result = 6
    print(f"observed aggregate outcome: exit={result}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aggregate", default="raw_signal_occurrence_truth_sqlite")
    parser.add_argument("--repository", type=Path)
    args = parser.parse_args()
    root = (args.repository or Path(__file__).resolve().parents[1]).resolve()
    return run_product_proof(root, args.aggregate)


if __name__ == "__main__":
    raise SystemExit(main())
