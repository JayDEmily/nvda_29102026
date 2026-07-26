"""Rerun every retained M13 false-positive and mutant against the frozen proof."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
RAW = REPO_ROOT / "project_control/canonical_project_manager/modules/M13/raw_validation"
RUNNER = RAW / "v5_run_variant.py"
OUTPUT = Path(__file__).resolve().parent / "retained_falsification_runs"

PM_V5 = (
    (
        "pm_v5_mutation_failure_reservation",
        "pm_v5_mutant_mutation_failure_reserves_idempotency_source.py",
        b"mutation failure reserved idempotency key",
    ),
    (
        "pm_v5_command_id_only_binding",
        "pm_v5_mutant_failed_binding_command_id_only_source.py",
        b"failed attempt reserved command identity",
    ),
)

EARLIER = (
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

BOUNDARIES = (
    "stale_expected_state_version",
    "owner_mutation_exception",
    "invalid_mutation_result_mapping",
    "invalid_or_empty_receipt_id",
    "invalid_or_empty_result_id",
    "repository_participant_prepare_failure",
    "repository_participant_commit_failure",
    "attesting_receipt_writer_failure",
)
COMPARISON_CASES = {
    "command_id": "same-command-id-different-fingerprint",
    "semantic_input_fingerprint": "different-command-id-same-fingerprint",
    "policy_version": "different-command-id-same-fingerprint",
    "complete_command_identity": "same-command-id-different-fingerprint",
}
BOUNDARY_LABELS = {
    "stale_expected_state_version": "stale-expected-state-version",
    "owner_mutation_exception": "owner-mutation-exception",
    "invalid_mutation_result_mapping": "invalid-mutation-result-mapping",
    "invalid_or_empty_receipt_id": "invalid-or-empty-receipt-id",
    "invalid_or_empty_result_id": "invalid-or-empty-result-id",
    "repository_participant_prepare_failure": "repository-participant-prepare-failure",
    "repository_participant_commit_failure": "repository-participant-commit-failure",
    "attesting_receipt_writer_failure": "attesting-receipt-writer-failure",
}


def _run(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def _retain(prefix: str, command: str, result: subprocess.CompletedProcess[bytes]) -> None:
    (OUTPUT / f"{prefix}.command.txt").write_text(command + "\n", encoding="utf-8")
    (OUTPUT / f"{prefix}.txt").write_bytes(result.stdout)
    (OUTPUT / f"{prefix}.exit_code").write_text(f"{result.returncode}\n", encoding="utf-8")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    pm_rows = ["mutant_id\told_fourteen_exit\tfull_exit\tintended_rejection"]
    for mutant_id, source_name, token in PM_V5:
        source = RAW / source_name
        old_args = [str(source), "--frozen-fourteen"]
        full_args = [str(source)]
        old = _run(old_args)
        full = _run(full_args)
        _retain(f"{mutant_id}.old_fourteen", " ".join(old_args), old)
        _retain(f"{mutant_id}.full", " ".join(full_args), full)
        ok = (
            old.returncode == 0
            and b"14 passed, 32 deselected" in old.stdout
            and full.returncode == 1
            and token in full.stdout
            and b"ERROR" not in full.stdout
        )
        pm_rows.append(
            f"{mutant_id}\t{old.returncode}\t{full.returncode}\t" f"{'PASS' if ok else 'FAIL'}"
        )
        if not ok:
            raise AssertionError(f"{mutant_id}: PM V5 intended rejection not established")
    (OUTPUT / "pm_v5_summary.tsv").write_text("\n".join(pm_rows) + "\n", encoding="utf-8")

    configurable_rows = ["mutant_id\tboundary\tcomparison\tcase_id\texit_code\tintended_rejection"]
    configurable_source = RAW / "v5_configurable_failed_binding_mutant_source.py"
    for boundary in BOUNDARIES:
        for comparison, dimension in COMPARISON_CASES.items():
            suffix = (
                "complete-command-identity-corrected-version"
                if boundary == "stale_expected_state_version"
                and comparison == "complete_command_identity"
                else dimension
            )
            case_id = f"{BOUNDARY_LABELS[boundary]}--{suffix}"
            mutant_id = f"{boundary}__{comparison}"
            env = os.environ.copy()
            env["M13_MUTATION_BOUNDARY"] = boundary
            env["M13_BINDING_COMPARISON"] = comparison
            args = [str(configurable_source), "--case", case_id]
            result = _run(args, env)
            _retain(f"configurable.{mutant_id}", " ".join(args), result)
            ok = (
                result.returncode == 1
                and b"hidden failed-attempt binding falsely conflicts" in result.stdout
                and case_id.encode() in result.stdout
                and b"1 failed, 45 deselected" in result.stdout
                and b"ERROR" not in result.stdout
            )
            configurable_rows.append(
                f"{mutant_id}\t{boundary}\t{comparison}\t{case_id}\t"
                f"{result.returncode}\t{'PASS' if ok else 'FAIL'}"
            )
            if not ok:
                raise AssertionError(
                    f"{mutant_id}: configurable intended rejection not established"
                )
    (OUTPUT / "configurable_summary.tsv").write_text(
        "\n".join(configurable_rows) + "\n", encoding="utf-8"
    )

    earlier_rows = ["mutant_id\tfull_exit\ttarget_exit\tintended_rejection"]
    for mutant_id, source_name, target_case, token in EARLIER:
        source = RAW / source_name
        full_args = [str(source)]
        target_args = [str(source), "--case", target_case]
        full = _run(full_args)
        target = _run(target_args)
        _retain(f"earlier.{mutant_id}.full", " ".join(full_args), full)
        _retain(f"earlier.{mutant_id}.target", " ".join(target_args), target)
        ok = (
            full.returncode == 1
            and target.returncode == 1
            and token in target.stdout
            and b"1 failed, 45 deselected" in target.stdout
            and b"ERROR" not in target.stdout
        )
        earlier_rows.append(
            f"{mutant_id}\t{full.returncode}\t{target.returncode}\t" f"{'PASS' if ok else 'FAIL'}"
        )
        if not ok:
            raise AssertionError(f"{mutant_id}: earlier intended rejection not established")
    (OUTPUT / "earlier_summary.tsv").write_text("\n".join(earlier_rows) + "\n", encoding="utf-8")

    print(f"pm_v5_mutants={len(PM_V5)}")
    print(f"configurable_mutants={len(BOUNDARIES) * len(COMPARISON_CASES)}")
    print(f"earlier_mutants={len(EARLIER)}")
    print("all_intended_rejections=PASS")


if __name__ == "__main__":
    main()
