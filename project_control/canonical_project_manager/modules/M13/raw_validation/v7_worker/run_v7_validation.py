"""Run and retain the complete bounded M13 V7 validation campaign."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
WORKER = Path(__file__).resolve().parent
OUTPUT = WORKER / "validation_runs"
RAW = Path("project_control/canonical_project_manager/modules/M13/raw_validation")
TEST = Path("tests/tier_a/persistence/test_m13_state_kernel_contract.py")
REFERENCE = RAW / "v6_worker/v6_reference_conforming_source.py"
PM_GLOBAL = RAW / "pm_v7_review/pm_v6_mutant_global_active_guard.py"
PM_PROBE = RAW / "pm_v7_review/pm_v6_two_instance_guard_probe.py"
RUNNER = RAW / "v5_run_variant.py"
BASELINE = "cf44a74385536672237de4747d084faaa7971b47"
SOURCE_ARCHIVE_HASH = "45dcf20a8a09bbc4edf026269c04b3fa948f9dfc709be1211cee611a2da4a109"


@dataclass(frozen=True)
class Check:
    name: str
    args: tuple[str, ...]
    expected_exit: int = 0


CHECKS = (
    Check(
        "collection",
        ("-m", "pytest", "-c", os.devnull, os.fspath(TEST), "--collect-only", "-q"),
    ),
    Check(
        "frozen_v6_preservation",
        (os.fspath(RAW / "v7_worker/verify_v7_frozen_proof.py"),),
    ),
    Check(
        "conforming_complete_family",
        (os.fspath(RUNNER), os.fspath(REFERENCE), "--quiet"),
    ),
    Check(
        "conforming_v7_addition",
        (os.fspath(RUNNER), os.fspath(REFERENCE), "--case", "m13_v7", "--quiet"),
    ),
    Check(
        "rejected_frozen_v6_expected_red",
        (
            "-m",
            "pytest",
            "-c",
            os.devnull,
            os.fspath(TEST),
            "-k",
            "not m13_v7",
            "-q",
        ),
        1,
    ),
    Check(
        "rejected_complete_family_expected_red",
        ("-m", "pytest", "-c", os.devnull, os.fspath(TEST), "-q"),
        1,
    ),
    Check(
        "pm_global_guard_frozen_v6_false_positive",
        (os.fspath(RUNNER), os.fspath(PM_GLOBAL), "--case", "not m13_v7", "--quiet"),
    ),
    Check(
        "pm_global_guard_complete_rejection",
        (os.fspath(RUNNER), os.fspath(PM_GLOBAL), "--quiet"),
        1,
    ),
    Check(
        "pm_two_instance_reference_probe",
        (os.fspath(PM_PROBE), os.fspath(REFERENCE)),
    ),
    Check(
        "pm_two_instance_global_guard_probe",
        (os.fspath(PM_PROBE), os.fspath(PM_GLOBAL)),
        1,
    ),
    Check(
        "v7_guard_mutants",
        (os.fspath(RAW / "v7_worker/run_v7_guard_mutants.py"),),
    ),
    Check(
        "retained_v6_mutants",
        (os.fspath(RAW / "v7_worker/run_v7_retained_v6_mutants.py"),),
    ),
    Check(
        "retained_all_prior_mutants",
        (os.fspath(RAW / "v7_worker/run_v7_retained_regression.py"),),
    ),
    Check("proof_blocks", ("scripts/run_proof_block.py", "--check-all")),
    Check(
        "proof_executor",
        ("-m", "pytest", "tests/tier_b/proof_model/test_proof_executor_contract.py", "-q"),
    ),
    Check(
        "persistence_without_m13",
        (
            "-m",
            "pytest",
            "tests/tier_a/persistence",
            "--ignore",
            os.fspath(TEST),
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
        (os.fspath(RAW / "implementation_worker/validate_architecture_boundary.py"),),
    ),
    Check(
        "vocabulary_exact_parity",
        (
            "-m",
            "pytest",
            "tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py::"
            "test_canonical_vocabulary_matches_builder_output_via_both_import_paths",
            "-q",
        ),
    ),
    Check(
        "python_compile",
        (
            "-m",
            "compileall",
            "-q",
            os.fspath(TEST),
            os.fspath(RAW / "v7_worker"),
        ),
    ),
    Check(
        "ruff",
        ("-m", "ruff", "check", os.fspath(TEST), os.fspath(RAW / "v7_worker")),
    ),
    Check(
        "black",
        (
            "-m",
            "black",
            "--check",
            os.fspath(TEST),
            os.fspath(RAW / "v7_worker"),
        ),
    ),
)


def _run(
    name: str,
    args: tuple[str, ...],
    *,
    cwd: Path = REPO_ROOT,
) -> subprocess.CompletedProcess[bytes]:
    command = [sys.executable, *args]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.fspath(cwd / "src")
    env["M13_PYTHON"] = sys.executable
    env["M13_SITE_PACKAGES"] = os.pathsep.join(sys.path)
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
    nodes = set()
    for line in output.splitlines():
        if not line.startswith(b"FAILED "):
            continue
        node = line[len(b"FAILED ") :].split(b" - ", 1)[0]
        nodes.add(b"::" + node.rsplit(b"::", 1)[-1])
    return {node.decode("utf-8") for node in nodes}


def _source_checkpoint(source_archive: Path) -> None:
    digest = hashlib.sha256(source_archive.read_bytes()).hexdigest()
    integrity = subprocess.run(
        ["tar", "-tzf", os.fspath(source_archive)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=False,
    )
    output = (
        f"archive={source_archive}\n"
        f"sha256={digest}\n"
        f"expected_sha256={SOURCE_ARCHIVE_HASH}\n"
        f"tar_integrity_exit={integrity.returncode}\n"
        "source_branch=review/m13-proof-v7\n"
        f"source_commit={BASELINE}\n"
    )
    (OUTPUT / "source_checkpoint.txt").write_text(output, encoding="utf-8")
    (OUTPUT / "source_checkpoint.exit_code").write_text("0\n", encoding="utf-8")
    assert digest == SOURCE_ARCHIVE_HASH
    assert integrity.returncode == 0


def _git_boundaries() -> None:
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASELINE],
        cwd=REPO_ROOT,
        text=True,
    ).splitlines()
    allowed = {
        TEST.as_posix(),
        "project_control/canonical_project_manager/modules/M13/M13_PROOF_RECORD.md",
    }
    invalid = [
        path
        for path in changed
        if path not in allowed
        and not path.startswith(
            "project_control/canonical_project_manager/modules/M13/raw_validation/v7_worker/"
        )
    ]
    source_diff = subprocess.run(
        ["git", "diff", "--exit-code", BASELINE, "--", "src"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    frozen_surfaces = subprocess.run(
        [
            "git",
            "diff",
            "--exit-code",
            BASELINE,
            "--",
            "00_TASK",
            "AGENTS.md",
            "PLANS.md",
            "docs",
            "config",
            "ROADMAP_LEDGER_V2.md",
            "project_control/canonical_project_manager/EXEC_PLAN.md",
            "project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md",
        ],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    diff_check = subprocess.run(
        [
            "git",
            "diff",
            "--check",
            BASELINE,
            "--",
            os.fspath(TEST),
            "project_control/canonical_project_manager/modules/M13/M13_PROOF_RECORD.md",
        ],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    lines = [
        f"baseline={BASELINE}",
        f"changed_path_count={len(changed)}",
        f"invalid_changed_path_count={len(invalid)}",
        f"source_diff_exit={source_diff.returncode}",
        f"normative_config_control_diff_exit={frozen_surfaces.returncode}",
        f"non_evidence_diff_check_exit={diff_check.returncode}",
        "changed_paths",
        *changed,
        "invalid_changed_paths",
        *invalid,
    ]
    (OUTPUT / "changed_path_validation.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    assert not invalid
    assert source_diff.returncode == 0
    assert frozen_surfaces.returncode == 0
    assert diff_check.returncode == 0


def _yaml_validation() -> None:
    import yaml

    paths = (
        REPO_ROOT / "config/proof_blocks.yaml",
        REPO_ROOT / "config/retained_test_registry.yaml",
    )
    for path in paths:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    (OUTPUT / "yaml_validation.txt").write_text(
        "\n".join(f"{path.relative_to(REPO_ROOT)}=PASS" for path in paths) + "\n",
        encoding="utf-8",
    )
    (OUTPUT / "yaml_validation.exit_code").write_text("0\n", encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: run_v7_validation.py SOURCE_ARCHIVE BASELINE_REPOSITORY")
    source_archive = Path(sys.argv[1]).resolve()
    baseline_repo = Path(sys.argv[2]).resolve()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    _source_checkpoint(source_archive)

    results: dict[str, subprocess.CompletedProcess[bytes]] = {}
    summary = ["check\texit_code\texpected_exit\tresult"]
    for check in CHECKS:
        result = _run(check.name, check.args)
        results[check.name] = result
        passed = result.returncode == check.expected_exit
        summary.append(
            f"{check.name}\t{result.returncode}\t{check.expected_exit}\t"
            f"{'PASS' if passed else 'FAIL'}"
        )
        if not passed:
            raise AssertionError(f"{check.name}: unexpected exit {result.returncode}")

    assert b"152 tests collected" in results["collection"].stdout
    assert b"result=PASS" in results["frozen_v6_preservation"].stdout
    assert b"152 passed" in results["conforming_complete_family"].stdout
    assert b"21 passed" in results["conforming_v7_addition"].stdout
    assert b"43 failed, 88 passed" in results["rejected_frozen_v6_expected_red"].stdout
    assert b"44 failed, 108 passed" in results["rejected_complete_family_expected_red"].stdout
    assert b"131 passed" in results["pm_global_guard_frozen_v6_false_positive"].stdout
    assert b"21 failed, 131 passed" in results["pm_global_guard_complete_rejection"].stdout
    assert b"two_instance_independence=PASS" in results["pm_two_instance_reference_probe"].stdout
    assert b"already active" in results["pm_two_instance_global_guard_probe"].stdout

    current_shadow = _run(
        "repository_shadow_current",
        ("-m", "pytest", "-c", os.devnull, "-q", "tests"),
    )
    baseline_shadow = _run(
        "repository_shadow_baseline",
        ("-m", "pytest", "-c", os.devnull, "-q", "tests"),
        cwd=baseline_repo,
    )
    assert current_shadow.returncode == baseline_shadow.returncode == 1
    current_failures = _failed_nodes(current_shadow.stdout)
    baseline_failures = _failed_nodes(baseline_shadow.stdout)
    new_failures = current_failures - baseline_failures
    resolved = baseline_failures - current_failures
    expected_new = {
        "::test_m13_v7_same_instance_rejection_and_distinct_instance_admission_hold_together"
    }
    assert new_failures == expected_new
    assert not resolved
    comparison = [
        "classification\tcount",
        f"baseline_failures\t{len(baseline_failures)}",
        f"current_failures\t{len(current_failures)}",
        f"new_expected_red_v7_m13\t{len(new_failures)}",
        f"resolved_baseline_failures\t{len(resolved)}",
        "new_unexplained_regressions\t0",
        "result\tPASS",
        "new_expected_red_nodes",
        *sorted(new_failures),
    ]
    (OUTPUT / "repository_shadow_comparison.tsv").write_text(
        "\n".join(comparison) + "\n",
        encoding="utf-8",
    )
    summary.extend(
        (
            "repository_shadow_current\t1\t1\tPASS",
            "repository_shadow_baseline\t1\t1\tPASS",
            "repository_shadow_comparison\t0\t0\tPASS",
        )
    )
    _yaml_validation()
    _git_boundaries()
    summary.extend(
        (
            "yaml_validation\t0\t0\tPASS",
            "changed_path_validation\t0\t0\tPASS",
        )
    )
    (OUTPUT / "validation_summary.tsv").write_text(
        "\n".join(summary) + "\n",
        encoding="utf-8",
    )
    print("\n".join(summary))
    print("frozen_v6_cases=131")
    print("v7_cases=21")
    print("conforming_complete_cases=152")
    print("new_unexplained_regressions=0")


if __name__ == "__main__":
    main()
