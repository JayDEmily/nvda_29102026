"""Run every V6 configurable mutant and retain full and intended-case outputs."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
WORKER = Path(__file__).resolve().parent
SOURCE = WORKER / "v6_configurable_mutant_source.py"
RUNNER = (
    REPO_ROOT
    / "project_control/canonical_project_manager/modules/M13/raw_validation/v5_run_variant.py"
)
OUTPUT = WORKER / "mutant_runs"


@dataclass(frozen=True)
class Mutant:
    mutant_id: str
    intended_case: str
    false_behaviour: str


MUTANTS = (
    Mutant(
        "nested_allowed_different_key",
        "single_active_attempt_excludes_nested_execute_matrix",
        "active guard rejects only the same scoped key and admits a different key",
    ),
    Mutant(
        "nested_allowed_different_consistency_unit",
        "single_active_attempt_excludes_nested_execute_matrix",
        "active guard rejects only the same consistency unit",
    ),
    Mutant(
        "nested_receipt_commits_later_loses_state",
        "nested_state_and_receipt_truth_cannot_be_orphaned",
        "nested receipt remains while the outer publication overwrites nested state",
    ),
    Mutant(
        "nested_state_commits_without_receipt",
        "nested_state_and_receipt_truth_cannot_be_orphaned",
        "nested state is published without a matching committed receipt",
    ),
    Mutant(
        "nested_and_outer_reuse_sequence",
        "nested_and_outer_cannot_reuse_sequence_or_resulting_version",
        "nested and outer successes both claim the same committed sequence",
    ),
    Mutant(
        "nested_and_outer_reuse_resulting_version",
        "nested_and_outer_cannot_reuse_sequence_or_resulting_version",
        "nested and outer successes both claim the same resulting state version",
    ),
    Mutant(
        "active_guard_set_after_mutation_starts",
        "single_active_attempt_excludes_nested_execute_matrix",
        "owner mutation begins before the active-attempt guard is installed",
    ),
    Mutant(
        "active_guard_cleared_before_participant_commit",
        "single_active_attempt_excludes_nested_execute_matrix",
        "active-attempt guard clears after prepare and before participant commit",
    ),
    Mutant(
        "active_guard_not_cleared_after_failure",
        "active_attempt_state_clears_after_every_terminal_outcome",
        "failed terminal outcome leaves the active-attempt guard set",
    ),
    Mutant(
        "receipt_scope_checks_only_command_type",
        "atomic_receipt_rejects_contradictory_or_invalid_truth_matrix",
        "receipt validation omits consistency-unit scope coherence",
    ),
    Mutant(
        "receipt_scope_checks_only_consistency_unit",
        "atomic_receipt_rejects_contradictory_or_invalid_truth_matrix",
        "receipt validation omits command-type scope coherence",
    ),
    Mutant(
        "receipt_version_validation_accepts_floats",
        "atomic_receipt_rejects_contradictory_or_invalid_truth_matrix",
        "receipt version and sequence validation accepts floats",
    ),
    Mutant(
        "receipt_version_validation_accepts_booleans",
        "atomic_receipt_rejects_contradictory_or_invalid_truth_matrix",
        "receipt version and sequence validation accepts booleans",
    ),
    Mutant(
        "receipt_resulting_version_may_equal_prior",
        "atomic_receipt_rejects_contradictory_or_invalid_truth_matrix",
        "receipt resulting version may equal its prior version",
    ),
    Mutant(
        "receipt_sequence_may_be_nonpositive",
        "atomic_receipt_rejects_contradictory_or_invalid_truth_matrix",
        "receipt sequence may be zero or negative",
    ),
    Mutant(
        "replay_response_alters_committed_identity",
        "duplicate_replay_preserves_every_committed_receipt_truth_field",
        "duplicate replay fabricates different receipt and result identities",
    ),
)


def _run(command: list[str], *, mode: str) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["M13_V6_MUTANT"] = mode
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def _retain(
    mutant_id: str,
    kind: str,
    command: list[str],
    result: subprocess.CompletedProcess[bytes],
) -> None:
    (OUTPUT / f"{mutant_id}.{kind}.command.txt").write_text(
        f"M13_V6_MUTANT={mutant_id} {' '.join(command)}\n",
        encoding="utf-8",
    )
    (OUTPUT / f"{mutant_id}.{kind}.txt").write_bytes(result.stdout)
    (OUTPUT / f"{mutant_id}.{kind}.exit_code").write_text(
        f"{result.returncode}\n",
        encoding="utf-8",
    )


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    summary = [
        "mutant_id\tfull_exit\ttarget_exit\tintended_rejection\tintended_case\tfalse_behaviour"
    ]
    for mutant in MUTANTS:
        full_command = [
            sys.executable,
            str(RUNNER),
            str(SOURCE),
            "--quiet",
        ]
        target_command = [
            sys.executable,
            str(RUNNER),
            str(SOURCE),
            "--case",
            mutant.intended_case,
            "--quiet",
        ]
        full = _run(full_command, mode=mutant.mutant_id)
        target = _run(target_command, mode=mutant.mutant_id)
        _retain(mutant.mutant_id, "full", full_command, full)
        _retain(mutant.mutant_id, "target", target_command, target)
        target_text = target.stdout.decode("utf-8", errors="replace")
        intended = (
            full.returncode == 1
            and target.returncode == 1
            and "failed" in target_text
            and "ERROR" not in target_text
        )
        summary.append(
            "\t".join(
                (
                    mutant.mutant_id,
                    str(full.returncode),
                    str(target.returncode),
                    "PASS" if intended else "FAIL",
                    mutant.intended_case,
                    mutant.false_behaviour,
                )
            )
        )
        if not intended:
            raise AssertionError(
                f"{mutant.mutant_id} was not rejected by its intended semantic case"
            )
    (OUTPUT / "summary.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"v6_mutants={len(MUTANTS)}")
    print("full_family_rejection=PASS")
    print("targeted_intended_rejection=PASS")


if __name__ == "__main__":
    main()
