"""Run and retain the complete M13 V6 proof and repository-shadow validation."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
WORKER = Path(__file__).resolve().parent
OUTPUT = WORKER / "validation_runs"
TEST_FILE = "tests/tier_a/persistence/test_m13_state_kernel_contract.py"
RAW = "project_control/canonical_project_manager/modules/M13/raw_validation"


@dataclass(frozen=True)
class Check:
    name: str
    args: tuple[str, ...]
    expected_exit: int = 0


CHECKS = (
    Check(
        "rejected_frozen_46",
        ("-m", "pytest", TEST_FILE, "-k", "not v6", "-vv"),
    ),
    Check(
        "rejected_repaired_family_expected_red",
        ("-m", "pytest", TEST_FILE, "-vv"),
        expected_exit=1,
    ),
    Check(
        "conforming_repaired_family",
        (
            f"{RAW}/v5_run_variant.py",
            f"{RAW}/v6_worker/v6_reference_conforming_source.py",
        ),
    ),
    Check(
        "repaired_family_collection",
        ("-m", "pytest", TEST_FILE, "--collect-only", "-q"),
    ),
    Check(
        "frozen_proof_preservation",
        (f"{RAW}/v6_worker/verify_frozen_proof.py",),
    ),
    Check(
        "pm_reentrant_probe",
        (f"{RAW}/pm_implementation_v1_review/pm_v1_reentrant_execute_probe.py",),
        expected_exit=1,
    ),
    Check(
        "pm_atomic_receipt_probe",
        (f"{RAW}/pm_implementation_v1_review/pm_v1_atomic_receipt_contract_probe.py",),
        expected_exit=1,
    ),
    Check("proof_blocks_structural", ("scripts/run_proof_block.py", "--check-all")),
    Check(
        "proof_executor",
        ("-m", "pytest", "tests/tier_b/proof_model/test_proof_executor_contract.py", "-q"),
    ),
    Check(
        "persistence_tier_a_expected_red",
        ("-m", "pytest", "tests/tier_a/persistence", "-q"),
        expected_exit=1,
    ),
    Check(
        "persistence_tier_a_without_m13",
        (
            "-m",
            "pytest",
            "tests/tier_a/persistence",
            "--ignore",
            TEST_FILE,
            "-q",
        ),
    ),
    Check(
        "checkpoint_shadow",
        (
            "-m",
            "pytest",
            "tests/tier_b/proof_model/test_checkpoint_receipt_contract.py",
            "-q",
        ),
    ),
    Check(
        "architecture_boundary",
        (f"{RAW}/implementation_worker/validate_architecture_boundary.py",),
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
    Check("integrity", (f"{RAW}/v6_worker/validate_v6_integrity.py",)),
    Check(
        "ruff",
        (
            "-m",
            "ruff",
            "check",
            TEST_FILE,
            f"{RAW}/v6_worker",
        ),
    ),
    Check(
        "black",
        (
            "-m",
            "black",
            "--check",
            TEST_FILE,
            f"{RAW}/v6_worker",
        ),
    ),
)


def _run(
    name: str,
    args: tuple[str, ...],
    *,
    cwd: Path,
) -> subprocess.CompletedProcess[bytes]:
    command = [sys.executable, *args]
    env = os.environ.copy()
    site_packages = os.environ.get("M13_SITE_PACKAGES", "")
    env["PYTHONPATH"] = os.pathsep.join(item for item in (site_packages, str(cwd / "src")) if item)
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / f"{name}.command.txt").write_text(
        f"PYTHONPATH={env['PYTHONPATH']} {' '.join(command)}\n",
        encoding="utf-8",
    )
    (OUTPUT / f"{name}.txt").write_bytes(result.stdout)
    (OUTPUT / f"{name}.exit_code").write_text(
        f"{result.returncode}\n",
        encoding="utf-8",
    )
    return result


def _failed_nodes(output: bytes) -> set[str]:
    return {
        line[len(b"FAILED ") :].split(b" - ", 1)[0].decode("utf-8")
        for line in output.splitlines()
        if line.startswith(b"FAILED ")
    }


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: run_v6_validation.py BASELINE_REPOSITORY SOURCE_ARCHIVE")
    baseline = Path(sys.argv[1]).resolve()
    source_archive = Path(sys.argv[2]).resolve()
    assert (baseline / ".git").exists()
    assert source_archive.is_file()

    results: dict[str, subprocess.CompletedProcess[bytes]] = {}
    summary = ["check\texit_code\texpected_exit\tresult"]
    source_result = _run(
        "source_checkpoint",
        (
            f"{RAW}/v6_worker/verify_source_checkpoint.py",
            str(source_archive),
        ),
        cwd=REPO_ROOT,
    )
    results["source_checkpoint"] = source_result
    summary.append(
        f"source_checkpoint\t{source_result.returncode}\t0\t"
        f"{'PASS' if source_result.returncode == 0 else 'FAIL'}"
    )
    if source_result.returncode != 0:
        raise AssertionError(f"source_checkpoint: unexpected exit {source_result.returncode}")
    for check in CHECKS:
        result = _run(check.name, check.args, cwd=REPO_ROOT)
        results[check.name] = result
        passed = result.returncode == check.expected_exit
        summary.append(
            f"{check.name}\t{result.returncode}\t{check.expected_exit}\t"
            f"{'PASS' if passed else 'FAIL'}"
        )
        if not passed:
            raise AssertionError(f"{check.name}: unexpected exit {result.returncode}")

    rejected_failures = _failed_nodes(results["rejected_repaired_family_expected_red"].stdout)
    assert len(rejected_failures) == 43
    assert all("::test_m13_v6_" in node for node in rejected_failures)
    assert b"46 passed, 85 deselected" in results["rejected_frozen_46"].stdout
    assert b"131 passed" in results["conforming_repaired_family"].stdout
    assert b"131 tests collected" in results["repaired_family_collection"].stdout
    assert b"result=PASS" in results["frozen_proof_preservation"].stdout
    assert b"receipt_count=2" in results["pm_reentrant_probe"].stdout
    assert b"receipt_sequences=[1, 1]" in results["pm_reentrant_probe"].stdout
    assert b"scope_matches=False" in results["pm_atomic_receipt_probe"].stdout
    assert b"resulting_version_type=float" in results["pm_atomic_receipt_probe"].stdout

    persistence_failures = _failed_nodes(results["persistence_tier_a_expected_red"].stdout)
    assert persistence_failures == rejected_failures

    current_shadow = _run(
        "repository_shadow_current",
        ("-m", "pytest", "-q"),
        cwd=REPO_ROOT,
    )
    baseline_shadow = _run(
        "repository_shadow_baseline",
        ("-m", "pytest", "-q"),
        cwd=baseline,
    )
    assert current_shadow.returncode == 1
    assert baseline_shadow.returncode == 1
    current_failures = _failed_nodes(current_shadow.stdout)
    baseline_failures = _failed_nodes(baseline_shadow.stdout)
    new_failures = current_failures - baseline_failures
    resolved_failures = baseline_failures - current_failures
    assert new_failures == rejected_failures
    assert not resolved_failures

    comparison = [
        "classification\tcount",
        f"baseline_failures\t{len(baseline_failures)}",
        f"current_failures\t{len(current_failures)}",
        f"new_expected_red_v6_m13\t{len(new_failures)}",
        f"resolved_or_changed_baseline_failures\t{len(resolved_failures)}",
        "new_unexplained_regressions\t0",
        "result\tPASS",
        "",
        "new_expected_red_v6_m13_nodes",
        *sorted(new_failures),
        "",
        "unchanged_baseline_shadow_nodes",
        *sorted(baseline_failures),
    ]
    (OUTPUT / "repository_shadow_comparison.txt").write_text(
        "\n".join(comparison) + "\n",
        encoding="utf-8",
    )
    summary.extend(
        (
            f"repository_shadow_current\t{current_shadow.returncode}\t1\tPASS",
            f"repository_shadow_baseline\t{baseline_shadow.returncode}\t1\tPASS",
            "repository_shadow_comparison\t0\t0\tPASS",
        )
    )
    (OUTPUT / "validation_summary.tsv").write_text(
        "\n".join(summary) + "\n",
        encoding="utf-8",
    )
    print("\n".join(summary))
    print("frozen_cases_green_on_rejected=46")
    print("repaired_expected_red_v6_cases=43")
    print("conforming_repaired_cases=131")
    print(f"baseline_shadow_failures={len(baseline_failures)}")
    print(f"current_shadow_failures={len(current_failures)}")
    print("new_unexplained_regressions=0")


if __name__ == "__main__":
    main()
