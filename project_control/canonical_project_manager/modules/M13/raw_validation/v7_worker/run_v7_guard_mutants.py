"""Run every V7 over-broad guard mutant with auditable raw evidence."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
WORKER = Path(__file__).resolve().parent
SOURCE = WORKER / "v7_overbroad_guard_mutant_source.py"
RUNNER = (
    REPO_ROOT
    / "project_control/canonical_project_manager/modules/M13/raw_validation/v5_run_variant.py"
)
OUTPUT = WORKER / "guard_mutant_runs"


@dataclass(frozen=True)
class Mutant:
    mutant_id: str
    intended_case: str
    false_behaviour: str
    frozen_v6_passes: bool = True


MUTANTS = (
    Mutant(
        "module_global_active_flag",
        "phase-owner-mutation--scope-different-command-and-unit--b-succeeds--a-succeeds",
        "one module-global flag falsely blocks every distinct instance",
    ),
    Mutant(
        "class_global_static_active_flag",
        "phase-owner-mutation--scope-different-command-and-unit--b-succeeds--a-succeeds",
        "one static class flag falsely blocks every distinct instance",
    ),
    Mutant(
        "universal_active_marker_registry",
        "phase-owner-mutation--scope-different-command-and-unit--b-succeeds--a-succeeds",
        "one universal process-registry marker falsely blocks every distinct instance",
    ),
    Mutant(
        "guard_keyed_only_by_command_type",
        "phase-owner-mutation--scope-same-command-different-unit--b-succeeds--a-fails",
        "process registry keyed only by command type couples independent instances",
    ),
    Mutant(
        "guard_keyed_only_by_consistency_unit_id",
        "phase-owner-mutation--scope-different-command-same-unit--b-fails--a-succeeds",
        "process registry keyed only by textual consistency-unit ID couples owners",
    ),
    Mutant(
        "guard_keyed_only_by_command_type_and_consistency_unit_id",
        "phase-owner-mutation--scope-same-command-and-unit-different-keys--b-fails--a-fails",
        "process registry keyed only by command/unit strings couples distinct instances",
    ),
    Mutant(
        "guard_shared_by_concrete_class",
        "phase-owner-mutation--scope-different-command-and-unit--b-succeeds--a-succeeds",
        "one marker per concrete class falsely couples every instance of that class",
    ),
    Mutant(
        "early_clear_before_participant_commit_with_global_coupling",
        "same_instance_rejection_and_distinct_instance_admission_hold_together",
        "guard clears before commit, admitting same-instance re-entry while globally coupled",
        frozen_v6_passes=False,
    ),
)


def _run(command: list[str], *, mode: str) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["M13_V7_GUARD_MUTANT"] = mode
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
        f"M13_V7_GUARD_MUTANT={mutant_id} {' '.join(command)}\n",
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
        "mutant_id\tfrozen_v6_exit\tfull_exit\ttarget_exit\t"
        "frozen_v6_disposition\tintended_rejection\tintended_case\tfalse_behaviour"
    ]
    for mutant in MUTANTS:
        base = [sys.executable, str(RUNNER), str(SOURCE)]
        frozen_command = [*base, "--case", "not m13_v7", "--quiet"]
        full_command = [*base, "--quiet"]
        target_command = [*base, "--case", mutant.intended_case, "--quiet"]
        frozen = _run(frozen_command, mode=mutant.mutant_id)
        full = _run(full_command, mode=mutant.mutant_id)
        target = _run(target_command, mode=mutant.mutant_id)
        _retain(mutant.mutant_id, "frozen_v6", frozen_command, frozen)
        _retain(mutant.mutant_id, "full", full_command, full)
        _retain(mutant.mutant_id, "target", target_command, target)

        target_text = target.stdout.decode("utf-8", errors="replace")
        intended = (
            full.returncode == 1
            and target.returncode == 1
            and "1 failed" in target_text
            and "ERROR" not in target_text
        )
        frozen_ok = frozen.returncode == (0 if mutant.frozen_v6_passes else 1)
        summary.append(
            "\t".join(
                (
                    mutant.mutant_id,
                    str(frozen.returncode),
                    str(full.returncode),
                    str(target.returncode),
                    "PASS" if frozen_ok else "FAIL",
                    "PASS" if intended else "FAIL",
                    mutant.intended_case,
                    mutant.false_behaviour,
                )
            )
        )
        if not frozen_ok or not intended:
            raise AssertionError(f"{mutant.mutant_id}: falsification gate failed")

    (OUTPUT / "summary.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"v7_guard_mutants={len(MUTANTS)}")
    print("frozen_v6_false_positive_check=PASS")
    print("full_and_targeted_intended_rejection=PASS")


if __name__ == "__main__":
    main()
