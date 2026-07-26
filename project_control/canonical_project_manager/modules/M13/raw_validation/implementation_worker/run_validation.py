"""Run and retain the bounded implementation and repository-shadow validation."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
OUTPUT = Path(__file__).resolve().parent / "validation_runs"
TEST_FILE = "tests/tier_a/persistence/test_m13_state_kernel_contract.py"


@dataclass(frozen=True)
class Check:
    name: str
    args: tuple[str, ...]
    expected_exit: int = 0


CHECKS = (
    Check("m13_frozen_proof", ("-m", "pytest", TEST_FILE, "-vv")),
    Check(
        "m13_collection",
        ("-m", "pytest", TEST_FILE, "--collect-only", "-q"),
    ),
    Check(
        "public_contract",
        (
            "project_control/canonical_project_manager/modules/M13/raw_validation/"
            "implementation_worker/validate_public_contract.py",
        ),
    ),
    Check("persistence_tier_a", ("-m", "pytest", "tests/tier_a/persistence", "-q")),
    Check("proof_blocks", ("scripts/run_proof_block.py", "--check-all")),
    Check(
        "proof_executor",
        ("-m", "pytest", "tests/tier_b/proof_model/test_proof_executor_contract.py", "-q"),
    ),
    Check(
        "checkpoint_shadow",
        ("-m", "pytest", "tests/tier_b/proof_model/test_checkpoint_receipt_contract.py", "-q"),
    ),
    Check(
        "vocabulary_builder_exact_parity",
        (
            "-m",
            "pytest",
            "tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py::"
            "test_canonical_vocabulary_matches_builder_output_via_both_import_paths",
            "-q",
        ),
    ),
    Check(
        "vocabulary_parity_shadow",
        (
            "-m",
            "pytest",
            "tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py",
            "-q",
        ),
        expected_exit=1,
    ),
    Check(
        "architecture_boundary",
        (
            "project_control/canonical_project_manager/modules/M13/raw_validation/"
            "implementation_worker/validate_architecture_boundary.py",
        ),
    ),
    Check(
        "repository_integrity",
        (
            "project_control/canonical_project_manager/modules/M13/raw_validation/"
            "implementation_worker/validate_integrity.py",
        ),
    ),
    Check(
        "ruff",
        (
            "-m",
            "ruff",
            "check",
            "src/nvda_desk/m13_state_kernel",
            "project_control/canonical_project_manager/modules/M13/raw_validation/"
            "implementation_worker",
        ),
    ),
    Check(
        "black",
        (
            "-m",
            "black",
            "--check",
            "src/nvda_desk/m13_state_kernel",
            "project_control/canonical_project_manager/modules/M13/raw_validation/"
            "implementation_worker",
        ),
    ),
)


def _retain(name: str, command: list[str], result: subprocess.CompletedProcess[bytes]) -> None:
    (OUTPUT / f"{name}.command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")
    (OUTPUT / f"{name}.txt").write_bytes(result.stdout)
    (OUTPUT / f"{name}.exit_code").write_text(f"{result.returncode}\n", encoding="utf-8")


def _run(
    name: str,
    args: tuple[str, ...],
    *,
    cwd: Path,
) -> subprocess.CompletedProcess[bytes]:
    command = [sys.executable, *args]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cwd / "src")
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    _retain(name, command, result)
    return result


def _failed_nodes(output: bytes) -> set[str]:
    prefix = b"FAILED "
    return {
        line[len(prefix) :].split(b" - ", 1)[0].decode("utf-8")
        for line in output.splitlines()
        if line.startswith(prefix)
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: run_validation.py BASELINE_REPOSITORY")
    baseline = Path(sys.argv[1]).resolve()
    assert (baseline / ".git").is_dir()

    OUTPUT.mkdir(parents=True, exist_ok=True)
    summary = ["check\texit_code\texpected_exit\tresult"]
    for check in CHECKS:
        result = _run(check.name, check.args, cwd=REPO_ROOT)
        passed = result.returncode == check.expected_exit
        summary.append(
            f"{check.name}\t{result.returncode}\t{check.expected_exit}\t"
            f"{'PASS' if passed else 'FAIL'}"
        )
        if not passed:
            raise AssertionError(f"{check.name}: unexpected exit {result.returncode}")

    current = _run("repository_shadow_current", ("-m", "pytest", "-q"), cwd=REPO_ROOT)
    baseline_result = _run("repository_shadow_baseline", ("-m", "pytest", "-q"), cwd=baseline)
    if current.returncode != 1 or baseline_result.returncode != 1:
        raise AssertionError("repository shadows must retain the admitted expected-red state")

    current_failures = _failed_nodes(current.stdout)
    baseline_failures = _failed_nodes(baseline_result.stdout)
    resolved = baseline_failures - current_failures
    new = current_failures - baseline_failures
    expected_resolved = {node for node in baseline_failures if f"{TEST_FILE}::" in node}
    if new or resolved != expected_resolved or len(resolved) != 46:
        raise AssertionError(
            "shadow comparison differs beyond the 46 resolved M13 expected-red cases"
        )

    comparison = [
        "classification\tcount",
        f"baseline_failures\t{len(baseline_failures)}",
        f"current_failures\t{len(current_failures)}",
        f"resolved_m13_expected_red\t{len(resolved)}",
        f"new_or_changed_failures\t{len(new)}",
        "result\tPASS",
        "",
        "unchanged_unrelated_legacy_shadow_failures",
        *sorted(current_failures),
        "",
        "resolved_m13_failures",
        *sorted(resolved),
    ]
    (OUTPUT / "repository_shadow_comparison.txt").write_text(
        "\n".join(comparison) + "\n", encoding="utf-8"
    )
    summary.extend(
        (
            f"repository_shadow_current\t{current.returncode}\t1\tPASS",
            f"repository_shadow_baseline\t{baseline_result.returncode}\t1\tPASS",
            "repository_shadow_comparison\t0\t0\tPASS",
        )
    )
    (OUTPUT / "validation_summary.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    print("resolved_m13_expected_red=46")
    print("new_or_changed_failures=0")


if __name__ == "__main__":
    main()
