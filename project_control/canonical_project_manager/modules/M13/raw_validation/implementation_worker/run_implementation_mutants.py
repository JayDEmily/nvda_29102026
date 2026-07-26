"""Generate bounded mutants from the production M13 source and execute frozen proof."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
SOURCE_PACKAGE = REPO_ROOT / "src/nvda_desk/m13_state_kernel"
TEST_FILE = REPO_ROOT / "tests/tier_a/persistence/test_m13_state_kernel_contract.py"
OUTPUT_ROOT = Path(__file__).resolve().parent / "implementation_mutant_runs"


@dataclass(frozen=True)
class Mutant:
    mutant_id: str
    target_node: str
    old: str
    new: str
    intended_defect: str


MUTANTS = (
    Mutant(
        mutant_id="publish_binding_before_participant_prepare",
        target_node=(
            "test_m13_failed_transaction_does_not_bind_idempotency_key_"
            "and_fresh_reuse_commits_once"
        ),
        old="""        self._coordinate_participants(
            command=command,
            working_state=working_state,
            receipt=receipt,
        )
""",
        new="""        self._bindings[scope] = _CommittedBinding(command_identity, receipt)
        self._coordinate_participants(
            command=command,
            working_state=working_state,
            receipt=receipt,
        )
""",
        intended_defect="failed participant attempt leaves a committed scoped-key binding",
    ),
    Mutant(
        mutant_id="publish_internal_state_before_final_participant_commit",
        target_node=(
            "test_m13_repository_participant_failure_rolls_back_participant_" "and_internal_truth"
        ),
        old="""        self._coordinate_participants(
            command=command,
            working_state=working_state,
            receipt=receipt,
        )

        # Internal truth is published only after every external participant
        # reports a successful commit. Failed attempts create no binding.
        self._state = working_state
        self._state_version = resulting_version
        self._committed_sequence = proposed_sequence
""",
        new="""        self._state = working_state
        self._state_version = resulting_version
        self._committed_sequence = proposed_sequence
        self._coordinate_participants(
            command=command,
            working_state=working_state,
            receipt=receipt,
        )

""",
        intended_defect="participant commit failure leaves internal state/version visible",
    ),
    Mutant(
        mutant_id="omit_rollback_of_prepare_raiser",
        target_node=(
            "test_m13_prepare_failure_rolls_back_failing_participant_"
            "and_allows_uncontaminated_retry"
        ),
        old="""                rollback_responsibility.append(participant)
                participant.prepare(
                    command=command,
                    working_state=deepcopy(working_state),
                    receipt=deepcopy(receipt),
                )
""",
        new="""                participant.prepare(
                    command=command,
                    working_state=deepcopy(working_state),
                    receipt=deepcopy(receipt),
                )
                rollback_responsibility.append(participant)
""",
        intended_defect="participant establishing pending truth then raising is not rolled back",
    ),
    Mutant(
        mutant_id="omit_rollback_of_earlier_participant",
        target_node=(
            "test_m13_later_prepare_failure_rolls_back_every_prepared_"
            "participant_and_allows_clean_retry"
        ),
        old="            for participant in reversed(rollback_responsibility):\n",
        new="            for participant in reversed(rollback_responsibility[-1:]):\n",
        intended_defect="earlier prepared or committed participant retains transaction truth",
    ),
    Mutant(
        mutant_id="mutate_stored_receipt_on_duplicate_replay",
        target_node=(
            "test_m13_failed_transaction_does_not_bind_idempotency_key_"
            "and_fresh_reuse_commits_once"
        ),
        old="            return replace(deepcopy(committed.receipt), duplicate_replay=True)\n",
        new="""            object.__setattr__(committed.receipt, "duplicate_replay", True)
            return deepcopy(committed.receipt)
""",
        intended_defect="duplicate response changes the originally stored committed receipt",
    ),
    Mutant(
        mutant_id="leak_mutable_snapshot_state",
        target_node="test_m13_state_and_receipt_readbacks_are_detached_copies",
        old="        return deepcopy(self._state)\n",
        new="        return self._state\n",
        intended_defect="caller mutation of snapshot changes committed state",
    ),
    Mutant(
        mutant_id="ignore_policy_version_in_committed_identity",
        target_node=(
            "test_m13_same_scoped_key_with_different_input_or_command_identity_" "is_conflict"
        ),
        old="""        return (
            command.command_id,
            command.input_fingerprint,
            command.policy_version,
        )
""",
        new="""        return (
            command.command_id,
            command.input_fingerprint,
            "",
        )
""",
        intended_defect="policy-version-only key reuse is treated as an exact duplicate",
    ),
    Mutant(
        mutant_id="increment_sequence_on_failed_attempt",
        target_node=(
            "test_m13_unsuccessful_execute_attempt_leaves_no_binding_matrix"
            "[repository-participant-prepare-failure--complete-command-identity]"
        ),
        old="""        self._coordinate_participants(
            command=command,
            working_state=working_state,
            receipt=receipt,
        )
""",
        new="""        self._committed_sequence = proposed_sequence
        self._coordinate_participants(
            command=command,
            working_state=working_state,
            receipt=receipt,
        )
""",
        intended_defect="failed participant attempt consumes committed sequence",
    ),
)


def _run(command: list[str], *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def main() -> None:
    python = os.environ.get("M13_PYTHON")
    site_packages = os.environ.get("M13_SITE_PACKAGES")
    if not python or not site_packages:
        raise RuntimeError("M13_PYTHON and M13_SITE_PACKAGES must be set")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    summary_lines = [
        "mutant_id\tfull_exit_code\ttarget_exit_code\tintended_rejection\tintended_defect"
    ]

    for mutant in MUTANTS:
        with tempfile.TemporaryDirectory(prefix=f"m13-{mutant.mutant_id}-") as temp:
            overlay = Path(temp) / "src/nvda_desk"
            overlay.mkdir(parents=True)
            shutil.copy2(REPO_ROOT / "src/nvda_desk/__init__.py", overlay / "__init__.py")
            shutil.copytree(SOURCE_PACKAGE, overlay / "m13_state_kernel")

            source_path = overlay / "m13_state_kernel/in_memory.py"
            source = source_path.read_text(encoding="utf-8")
            occurrences = source.count(mutant.old)
            if occurrences != 1:
                raise AssertionError(
                    f"{mutant.mutant_id}: expected one mutation anchor, found {occurrences}"
                )
            source_path.write_text(source.replace(mutant.old, mutant.new), encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONPATH"] = os.pathsep.join(
                (str(Path(temp) / "src"), str(REPO_ROOT / "src"), site_packages)
            )
            full_command = [
                python,
                "-m",
                "pytest",
                "-c",
                os.devnull,
                str(TEST_FILE),
                "-q",
            ]
            target_command = [
                python,
                "-m",
                "pytest",
                "-c",
                os.devnull,
                f"{TEST_FILE}::{mutant.target_node}",
                "-q",
            ]
            full = _run(full_command, env=env)
            target = _run(target_command, env=env)

            (OUTPUT_ROOT / f"{mutant.mutant_id}.full.command.txt").write_text(
                " ".join(full_command) + "\n", encoding="utf-8"
            )
            (OUTPUT_ROOT / f"{mutant.mutant_id}.full.txt").write_text(full.stdout, encoding="utf-8")
            (OUTPUT_ROOT / f"{mutant.mutant_id}.full.exit_code").write_text(
                f"{full.returncode}\n", encoding="utf-8"
            )
            (OUTPUT_ROOT / f"{mutant.mutant_id}.target.command.txt").write_text(
                " ".join(target_command) + "\n", encoding="utf-8"
            )
            (OUTPUT_ROOT / f"{mutant.mutant_id}.target.txt").write_text(
                target.stdout, encoding="utf-8"
            )
            (OUTPUT_ROOT / f"{mutant.mutant_id}.target.exit_code").write_text(
                f"{target.returncode}\n", encoding="utf-8"
            )

            intended_rejection = (
                full.returncode != 0
                and target.returncode != 0
                and "1 failed" in target.stdout
                and "ERROR" not in target.stdout
            )
            summary_lines.append(
                "\t".join(
                    (
                        mutant.mutant_id,
                        str(full.returncode),
                        str(target.returncode),
                        "PASS" if intended_rejection else "FAIL",
                        mutant.intended_defect,
                    )
                )
            )
            if not intended_rejection:
                raise AssertionError(
                    f"{mutant.mutant_id} was not rejected by its intended proof case"
                )

    (OUTPUT_ROOT / "summary.tsv").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"implementation_mutants={len(MUTANTS)}")
    print("full_family_rejection=PASS")
    print("targeted_intended_rejection=PASS")


if __name__ == "__main__":
    main()
