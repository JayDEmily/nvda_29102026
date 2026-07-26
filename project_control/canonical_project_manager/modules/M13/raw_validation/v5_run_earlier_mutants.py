from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
RAW = ROOT / "project_control/canonical_project_manager/modules/M13/raw_validation"
OUTPUT = RAW / "v5_worker_runs/earlier_mutants"
RUNNER = RAW / "v5_run_variant.py"
MUTANTS = (
    (
        "durable_label",
        "mutant_durable_label_source.py",
        "exports_the_accepted_public_contract",
        b"AssertionError: assert 'durable'",
    ),
    (
        "duplicate_reexec",
        "mutant_duplicate_reexec_source.py",
        "exact_duplicate_returns_original_identity",
        b"assert 2 == 1",
    ),
    (
        "scope_value_only",
        "mutant_scope_value_only_source.py",
        "idempotency_key_is_scoped",
        b"IdempotencyConflictError: conflicting idempotency-key reuse",
    ),
    (
        "ignore_version",
        "mutant_ignore_version_source.py",
        "stale_expected_version_fails_before_mutation",
        b"DID NOT RAISE",
    ),
    (
        "commit_on_exception",
        "mutant_commit_on_exception_source.py",
        "mutation_failure_rolls_back_state_version",
        b"assert 1 == 0",
    ),
    (
        "accept_invalid_receipt",
        "mutant_accept_invalid_receipt_source.py",
        "invalid_receipt_result_rolls_back",
        b"DID NOT RAISE",
    ),
    (
        "commit_before_receipt",
        "mutant_commit_before_receipt_source.py",
        "receipt_write_failure_rolls_back_every_visible_change",
        b"assert 1 == 0",
    ),
    (
        "no_participant_rollback",
        "mutant_no_participant_rollback_source.py",
        "receipt_write_failure_rolls_back_every_visible_change",
        b"Left contains one more item",
    ),
    (
        "register_after_prepare",
        "mutant_register_after_prepare_source.py",
        "prepare_failure_rolls_back_failing_participant",
        b"rollback_calls",
    ),
    (
        "rollback_only_failing_prepare_participant",
        "mutant_rollback_only_failing_prepare_participant_source.py",
        "later_prepare_failure_rolls_back_every_prepared_participant",
        b"rollback_calls",
    ),
    (
        "pm_v4_failed_attempt_binding",
        "pm_v4_mutant_failed_attempt_reserves_idempotency_source.py",
        "failed_transaction_does_not_bind_idempotency_key",
        b"failed attempt reserved idempotency key",
    ),
)


def _run(source: Path, extra_args: list[str]) -> tuple[list[str], subprocess.CompletedProcess[bytes]]:
    command = [sys.executable, str(RUNNER), str(source), *extra_args]
    return command, subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def _retain(mutant_id: str, run_type: str, command: list[str], result: subprocess.CompletedProcess[bytes]) -> None:
    stem = OUTPUT / f"{mutant_id}.{run_type}"
    stem.with_suffix(stem.suffix + ".txt").write_bytes(result.stdout)
    stem.with_suffix(stem.suffix + ".exit_code").write_text(
        f"{result.returncode}\n",
        encoding="utf-8",
    )
    stem.with_suffix(stem.suffix + ".command.txt").write_text(
        " ".join(command) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    summary = [
        "mutant_id\tsource\ttarget_case\tfull_exit_code\ttarget_exit_code"
        "\tintended_rejection_observed"
    ]
    passed = True
    for mutant_id, source_name, target_case, intended_token in MUTANTS:
        source = RAW / source_name
        full_command, full_result = _run(source, [])
        target_command, target_result = _run(source, ["--case", target_case])
        _retain(mutant_id, "full", full_command, full_result)
        _retain(mutant_id, "target", target_command, target_result)
        intended = (
            full_result.returncode == 1
            and target_result.returncode == 1
            and intended_token in target_result.stdout
            and b"1 failed, 45 deselected" in target_result.stdout
        )
        passed = passed and intended
        summary.append(
            f"{mutant_id}\t{source_name}\t{target_case}\t{full_result.returncode}"
            f"\t{target_result.returncode}\t{'PASS' if intended else 'FAIL'}"
        )
    summary.append(f"earlier_mutant_count={len(MUTANTS)}")
    summary.append(f"all_intended_rejections={'PASS' if passed else 'FAIL'}")
    (OUTPUT / "summary.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
