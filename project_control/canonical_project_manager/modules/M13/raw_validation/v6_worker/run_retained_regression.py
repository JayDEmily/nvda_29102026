"""Rerun every retained M13 mutant without overwriting prior evidence."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
RAW = REPO_ROOT / "project_control/canonical_project_manager/modules/M13/raw_validation"
WORKER = Path(__file__).resolve().parent
OUTPUT = WORKER / "retained_mutant_runs"
RUNNER = RAW / "v5_run_variant.py"

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
        b"IdempotencyConflictError",
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

PM_V5 = (
    (
        "pm_v5_mutation_failure_reserves_idempotency",
        "pm_v5_mutant_mutation_failure_reserves_idempotency_source.py",
        "owner-mutation-exception--same-command-id-different-fingerprint",
        b"mutation failure reserved idempotency key",
    ),
    (
        "pm_v5_failed_binding_command_id_only",
        "pm_v5_mutant_failed_binding_command_id_only_source.py",
        "repository-participant-prepare-failure--same-command-id-different-fingerprint",
        b"failed attempt reserved command identity",
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
BOUNDARY_LABELS = {item: item.replace("_", "-") for item in BOUNDARIES}


def _run(
    source: Path,
    *,
    case: str | None = None,
    env_updates: dict[str, str] | None = None,
) -> tuple[list[str], subprocess.CompletedProcess[bytes]]:
    command = [sys.executable, str(RUNNER), str(source), "--quiet"]
    if case:
        command[3:3] = ["--case", case]
    env = os.environ.copy()
    env.update(env_updates or {})
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return command, result


def _retain(
    directory: Path,
    stem: str,
    command: list[str],
    result: subprocess.CompletedProcess[bytes],
    *,
    env_prefix: str = "",
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{stem}.command.txt").write_text(
        f"{env_prefix}{' '.join(command)}\n",
        encoding="utf-8",
    )
    (directory / f"{stem}.txt").write_bytes(result.stdout)
    (directory / f"{stem}.exit_code").write_text(
        f"{result.returncode}\n",
        encoding="utf-8",
    )


def _run_earlier() -> list[str]:
    directory = OUTPUT / "earlier"
    summary = ["mutant_id\tfull_exit\ttarget_exit\tintended_rejection"]
    for mutant_id, source_name, target_case, token in EARLIER:
        source = RAW / source_name
        full_command, full = _run(source)
        target_command, target = _run(source, case=target_case)
        _retain(directory, f"{mutant_id}.full", full_command, full)
        _retain(directory, f"{mutant_id}.target", target_command, target)
        intended = (
            full.returncode == 1
            and target.returncode == 1
            and token in target.stdout
            and b"ERROR" not in target.stdout
        )
        summary.append(
            f"{mutant_id}\t{full.returncode}\t{target.returncode}\t"
            f"{'PASS' if intended else 'FAIL'}"
        )
        if not intended:
            raise AssertionError(f"{mutant_id}: intended retained rejection not observed")
    return summary


def _run_pm_v5() -> list[str]:
    directory = OUTPUT / "pm_v5"
    summary = ["mutant_id\tfull_exit\ttarget_exit\tintended_rejection"]
    for mutant_id, source_name, target_case, token in PM_V5:
        source = RAW / source_name
        full_command, full = _run(source)
        target_command, target = _run(source, case=target_case)
        _retain(directory, f"{mutant_id}.full", full_command, full)
        _retain(directory, f"{mutant_id}.target", target_command, target)
        intended = (
            full.returncode == 1
            and target.returncode == 1
            and token in target.stdout
            and b"ERROR" not in target.stdout
        )
        summary.append(
            f"{mutant_id}\t{full.returncode}\t{target.returncode}\t"
            f"{'PASS' if intended else 'FAIL'}"
        )
        if not intended:
            raise AssertionError(f"{mutant_id}: intended PM V5 rejection not observed")
    return summary


def _run_v5_configurable() -> list[str]:
    directory = OUTPUT / "v5_configurable"
    source = RAW / "v5_configurable_failed_binding_mutant_source.py"
    summary = ["mutant_id\texit\tintended_false_conflict"]
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
            updates = {
                "M13_MUTATION_BOUNDARY": boundary,
                "M13_BINDING_COMPARISON": comparison,
            }
            command, result = _run(source, case=case_id, env_updates=updates)
            prefix = f"M13_MUTATION_BOUNDARY={boundary} " f"M13_BINDING_COMPARISON={comparison} "
            _retain(directory, mutant_id, command, result, env_prefix=prefix)
            intended = (
                result.returncode == 1
                and b"hidden failed-attempt binding falsely conflicts" in result.stdout
                and case_id.encode() in result.stdout
                and b"ERROR" not in result.stdout
            )
            summary.append(f"{mutant_id}\t{result.returncode}\t{'PASS' if intended else 'FAIL'}")
            if not intended:
                raise AssertionError(f"{mutant_id}: V5 false conflict not observed")
    return summary


def _run_implementation_derived() -> None:
    path = RAW / "implementation_worker/run_implementation_mutants.py"
    spec = importlib.util.spec_from_file_location("_m13_impl_mutants_v6", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load implementation mutant runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.OUTPUT_ROOT = OUTPUT / "implementation_derived"
    module.main()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    earlier = _run_earlier()
    pm_v5 = _run_pm_v5()
    configurable = _run_v5_configurable()
    _run_implementation_derived()
    (OUTPUT / "earlier_summary.tsv").write_text("\n".join(earlier) + "\n", encoding="utf-8")
    (OUTPUT / "pm_v5_summary.tsv").write_text("\n".join(pm_v5) + "\n", encoding="utf-8")
    (OUTPUT / "v5_configurable_summary.tsv").write_text(
        "\n".join(configurable) + "\n",
        encoding="utf-8",
    )
    print(f"earlier_mutants={len(EARLIER)}")
    print(f"pm_v5_mutants={len(PM_V5)}")
    print(f"v5_configurable_mutants={len(BOUNDARIES) * len(COMPARISON_CASES)}")
    print("implementation_derived_mutants=8")
    print("all_targeted_intended_rejections=PASS")


if __name__ == "__main__":
    main()
