from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
RAW = ROOT / "project_control/canonical_project_manager/modules/M13/raw_validation"
OUTPUT = RAW / "v5_worker_runs/additional_mutants"
RUNNER = RAW / "v5_run_variant.py"
SOURCE = RAW / "v5_configurable_failed_binding_mutant_source.py"
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
CASE_BOUNDARY_LABELS = {
    "stale_expected_state_version": "stale-expected-state-version",
    "owner_mutation_exception": "owner-mutation-exception",
    "invalid_mutation_result_mapping": "invalid-mutation-result-mapping",
    "invalid_or_empty_receipt_id": "invalid-or-empty-receipt-id",
    "invalid_or_empty_result_id": "invalid-or-empty-result-id",
    "repository_participant_prepare_failure": "repository-participant-prepare-failure",
    "repository_participant_commit_failure": "repository-participant-commit-failure",
    "attesting_receipt_writer_failure": "attesting-receipt-writer-failure",
}


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    summary = [
        "mutant_id\tboundary\tcomparison\tcase_id\texit_code"
        "\tintended_false_conflict_observed"
    ]
    passed = True
    for boundary in BOUNDARIES:
        for comparison, dimension in COMPARISON_CASES.items():
            suffix = (
                "complete-command-identity-corrected-version"
                if boundary == "stale_expected_state_version"
                and comparison == "complete_command_identity"
                else dimension
            )
            case_id = f"{CASE_BOUNDARY_LABELS[boundary]}--{suffix}"
            mutant_id = f"{boundary}__{comparison}"
            command = [
                sys.executable,
                str(RUNNER),
                str(SOURCE),
                "--case",
                case_id,
            ]
            env = os.environ.copy()
            env["M13_MUTATION_BOUNDARY"] = boundary
            env["M13_BINDING_COMPARISON"] = comparison
            completed = subprocess.run(
                command,
                cwd=ROOT,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            output = completed.stdout
            (OUTPUT / f"{mutant_id}.txt").write_bytes(output)
            (OUTPUT / f"{mutant_id}.exit_code").write_text(
                f"{completed.returncode}\n",
                encoding="utf-8",
            )
            command_text = (
                f"M13_MUTATION_BOUNDARY={boundary} "
                f"M13_BINDING_COMPARISON={comparison} "
                + " ".join(command)
                + "\n"
            )
            (OUTPUT / f"{mutant_id}.command.txt").write_text(
                command_text,
                encoding="utf-8",
            )
            false_conflict = (
                completed.returncode == 1
                and b"hidden failed-attempt binding falsely conflicts" in output
                and case_id.encode("utf-8") in output
                and b"1 failed, 45 deselected" in output
            )
            passed = passed and false_conflict
            summary.append(
                f"{mutant_id}\t{boundary}\t{comparison}\t{case_id}"
                f"\t{completed.returncode}\t{'PASS' if false_conflict else 'FAIL'}"
            )
    summary.append(f"configured_variant_count={len(BOUNDARIES) * len(COMPARISON_CASES)}")
    summary.append(f"all_intended_false_conflicts={'PASS' if passed else 'FAIL'}")
    (OUTPUT / "summary.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
