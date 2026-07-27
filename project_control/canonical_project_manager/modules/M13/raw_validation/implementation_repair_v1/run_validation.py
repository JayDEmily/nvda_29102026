"""Run the complete M13 repair validation and compare repository shadows."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
OUTPUT = Path(__file__).resolve().parent / "validation_runs"
BASE_COMMIT = "df17277247e4d68c260318e6306d4788de410a4c"
PROOF = "tests/tier_a/persistence/test_m13_state_kernel_contract.py"
PROOF_SHA256 = "a3ad3e8b51e2dd73119ecbec2e546f8d4e594346efaa8bf588c90b67798b8843"


@dataclass(frozen=True)
class Check:
    name: str
    command: tuple[str, ...]
    expected_exit: int = 0


CHECKS = (
    Check("m13_proof_152", (sys.executable, "-m", "pytest", PROOF, "-q")),
    Check(
        "m13_collection",
        (sys.executable, "-m", "pytest", PROOF, "--collect-only", "-q"),
    ),
    Check(
        "persistence_tier_a",
        (sys.executable, "-m", "pytest", "tests/tier_a/persistence", "-q"),
    ),
    Check(
        "proof_blocks",
        (sys.executable, "scripts/run_proof_block.py", "--check-all"),
    ),
    Check(
        "proof_executor",
        (
            sys.executable,
            "-m",
            "pytest",
            "tests/tier_b/proof_model/test_proof_executor_contract.py",
            "-q",
        ),
    ),
    Check(
        "checkpoint_shadow",
        (
            sys.executable,
            "-m",
            "pytest",
            "tests/tier_b/proof_model/test_checkpoint_receipt_contract.py",
            "-q",
        ),
    ),
    Check(
        "architecture_boundary",
        (
            sys.executable,
            "project_control/canonical_project_manager/modules/M13/raw_validation/"
            "implementation_worker/validate_architecture_boundary.py",
        ),
    ),
    Check(
        "vocabulary_exact_parity",
        (
            sys.executable,
            "-m",
            "pytest",
            "tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py::"
            "test_canonical_vocabulary_matches_builder_output_via_both_import_paths",
            "-q",
        ),
    ),
    Check(
        "yaml_parse",
        (
            sys.executable,
            "-c",
            (
                "from pathlib import Path; import yaml; "
                "files=sorted(Path('config').glob('*.yaml')); "
                "[yaml.safe_load(p.read_text(encoding='utf-8')) for p in files]; "
                "print(f'yaml_files={len(files)}'); print('yaml_parse=PASS')"
            ),
        ),
    ),
    Check(
        "python_compile",
        (
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "src/nvda_desk/m13_state_kernel",
            "project_control/canonical_project_manager/modules/M13/raw_validation/"
            "implementation_repair_v1",
        ),
    ),
    Check(
        "ruff",
        (
            sys.executable,
            "-m",
            "ruff",
            "check",
            "src/nvda_desk/m13_state_kernel",
            "project_control/canonical_project_manager/modules/M13/raw_validation/"
            "implementation_repair_v1",
        ),
    ),
    Check(
        "black",
        (
            sys.executable,
            "-m",
            "black",
            "--check",
            "src/nvda_desk/m13_state_kernel",
            "project_control/canonical_project_manager/modules/M13/raw_validation/"
            "implementation_repair_v1",
        ),
    ),
    Check("git_diff_check", ("git", "diff", "--check")),
)


def _run(
    name: str,
    command: tuple[str, ...],
    *,
    cwd: Path,
) -> subprocess.CompletedProcess[bytes]:
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
    (OUTPUT / f"{name}.command.txt").write_text(
        subprocess.list2cmdline(command) + "\n", encoding="utf-8"
    )
    (OUTPUT / f"{name}.txt").write_bytes(result.stdout)
    (OUTPUT / f"{name}.exit_code").write_text(f"{result.returncode}\n", encoding="utf-8")
    return result


def _failed_nodes(output: bytes) -> set[str]:
    return {
        line[len(b"FAILED ") :].split(b" - ", 1)[0].decode("utf-8", errors="replace")
        for line in output.splitlines()
        if line.startswith(b"FAILED ")
    }


def _validate_frozen_proof() -> None:
    digest = hashlib.sha256((REPO_ROOT / PROOF).read_bytes()).hexdigest()
    output = (
        f"proof={PROOF}\n"
        f"sha256={digest}\n"
        f"expected={PROOF_SHA256}\n"
        f"exact={digest == PROOF_SHA256}\n"
    )
    (OUTPUT / "frozen_proof_hash.command.txt").write_text(f"sha256 {PROOF}\n", encoding="utf-8")
    (OUTPUT / "frozen_proof_hash.txt").write_text(output, encoding="utf-8")
    (OUTPUT / "frozen_proof_hash.exit_code").write_text("0\n", encoding="utf-8")
    if digest != PROOF_SHA256:
        raise AssertionError("frozen proof bytes changed")


def _validate_changed_paths() -> None:
    changed = subprocess.run(
        ["git", "diff", "--name-only", BASE_COMMIT],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()
    paths = sorted(set(changed + untracked))
    allowed_exact = {
        "src/nvda_desk/m13_state_kernel/contracts.py",
        "src/nvda_desk/m13_state_kernel/in_memory.py",
        "project_control/canonical_project_manager/modules/M13/"
        "M13_IMPLEMENTATION_REPAIR_V1_WORKER_RECORD.md",
    }
    evidence_prefix = (
        "project_control/canonical_project_manager/modules/M13/raw_validation/"
        "implementation_repair_v1/"
    )
    invalid = [
        path for path in paths if path not in allowed_exact and not path.startswith(evidence_prefix)
    ]
    lines = [
        f"base={BASE_COMMIT}",
        "changed_paths",
        *paths,
        f"invalid_count={len(invalid)}",
        "changed_path_validation=PASS" if not invalid else "changed_path_validation=FAIL",
    ]
    (OUTPUT / "changed_paths.command.txt").write_text(
        f"git diff --name-only {BASE_COMMIT}; git ls-files --others --exclude-standard\n",
        encoding="utf-8",
    )
    (OUTPUT / "changed_paths.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUTPUT / "changed_paths.exit_code").write_text(
        "0\n" if not invalid else "1\n", encoding="utf-8"
    )
    if invalid:
        raise AssertionError(f"out-of-scope changed paths: {invalid}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: run_validation.py BASELINE_WORKTREE")
    baseline = Path(sys.argv[1]).resolve()
    if not (baseline / ".git").exists():
        raise AssertionError(f"baseline is not a Git worktree: {baseline}")
    baseline_head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=baseline,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()
    if baseline_head != BASE_COMMIT:
        raise AssertionError(f"unexpected baseline commit: {baseline_head}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    _validate_frozen_proof()
    summary = ["check\texit_code\texpected_exit\tresult"]
    for check in CHECKS:
        result = _run(check.name, check.command, cwd=REPO_ROOT)
        passed = result.returncode == check.expected_exit
        summary.append(
            f"{check.name}\t{result.returncode}\t{check.expected_exit}\t"
            f"{'PASS' if passed else 'FAIL'}"
        )
        if not passed:
            raise AssertionError(f"{check.name}: unexpected exit {result.returncode}")

    _validate_changed_paths()
    current = _run(
        "repository_shadow_current",
        (sys.executable, "-m", "pytest", "-c", os.devnull, "-q", "tests"),
        cwd=REPO_ROOT,
    )
    baseline_result = _run(
        "repository_shadow_baseline",
        (sys.executable, "-m", "pytest", "-c", os.devnull, "-q", "tests"),
        cwd=baseline,
    )
    current_failures = _failed_nodes(current.stdout)
    baseline_failures = _failed_nodes(baseline_result.stdout)
    resolved = baseline_failures - current_failures
    new = current_failures - baseline_failures
    expected_resolved = {
        node for node in baseline_failures if "test_m13_state_kernel_contract.py::" in node
    }
    comparison_passed = not new and resolved == expected_resolved and len(resolved) == 44
    comparison = [
        f"baseline_commit\t{BASE_COMMIT}",
        f"baseline_exit\t{baseline_result.returncode}",
        f"current_exit\t{current.returncode}",
        f"baseline_failures\t{len(baseline_failures)}",
        f"current_failures\t{len(current_failures)}",
        f"resolved_m13_expected_red\t{len(resolved)}",
        f"new_or_changed_failures\t{len(new)}",
        f"result\t{'PASS' if comparison_passed else 'FAIL'}",
        "",
        "resolved_m13_failures",
        *sorted(resolved),
        "",
        "unchanged_repository_shadow_failures",
        *sorted(current_failures),
        "",
        "new_or_changed_failures",
        *sorted(new),
    ]
    (OUTPUT / "repository_shadow_comparison.tsv").write_text(
        "\n".join(comparison) + "\n", encoding="utf-8"
    )
    if not comparison_passed:
        raise AssertionError("repository shadow differs beyond the 44 repaired M13 nodes")

    summary.extend(
        (
            "frozen_proof_hash\t0\t0\tPASS",
            "changed_paths\t0\t0\tPASS",
            f"repository_shadow_current\t{current.returncode}\t{current.returncode}\tPASS",
            (
                "repository_shadow_baseline\t"
                f"{baseline_result.returncode}\t{baseline_result.returncode}\tPASS"
            ),
            "repository_shadow_comparison\t0\t0\tPASS",
        )
    )
    (OUTPUT / "validation_summary.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    print("resolved_m13_expected_red=44")
    print("new_or_changed_failures=0")


if __name__ == "__main__":
    main()
