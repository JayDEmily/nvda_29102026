"""Build six production-derived M13 repair mutants and retain their rejection."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
SOURCE_PACKAGE = REPO_ROOT / "src/nvda_desk/m13_state_kernel"
TEST_FILE = REPO_ROOT / "tests/tier_a/persistence/test_m13_state_kernel_contract.py"
OUTPUT = Path(
    os.environ.get(
        "M13_REPAIR_MUTANT_OUTPUT",
        Path(__file__).resolve().parent / "repair_mutant_runs",
    )
)


@dataclass(frozen=True)
class Mutant:
    mutant_id: str
    source_file: str
    target_node: str
    old: str
    new: str
    intended_defect: str


MUTANTS = (
    Mutant(
        "no_active_attempt_guard",
        "in_memory.py",
        "test_m13_v7_same_instance_rejection_and_distinct_instance_admission_hold_together",
        """        if self._active_attempt:
            raise RuntimeError("UnitOfWork.execute attempt is already active")

        self._active_attempt = True
        try:
            return self._execute_active(command=command, mutation=mutation)
        finally:
            self._active_attempt = False
""",
        """        return self._execute_active(command=command, mutation=mutation)
""",
        "same-instance nested execution is admitted because exclusion is absent",
    ),
    Mutant(
        "module_global_active_attempt_guard",
        "in_memory.py",
        (
            "test_m13_v7_active_attempt_exclusion_is_owned_by_one_unit_of_work_instance"
            "[phase-owner-mutation--scope-different-command-and-unit--b-succeeds--a-succeeds]"
        ),
        """        if self._active_attempt:
            raise RuntimeError("UnitOfWork.execute attempt is already active")

        self._active_attempt = True
        try:
            return self._execute_active(command=command, mutation=mutation)
        finally:
            self._active_attempt = False
""",
        """        global _MODULE_ACTIVE_ATTEMPT
        if _MODULE_ACTIVE_ATTEMPT:
            raise RuntimeError("UnitOfWork.execute attempt is already active")

        _MODULE_ACTIVE_ATTEMPT = True
        try:
            return self._execute_active(command=command, mutation=mutation)
        finally:
            _MODULE_ACTIVE_ATTEMPT = False
""",
        "one module-global flag falsely couples distinct UnitOfWork instances",
    ),
    Mutant(
        "active_guard_installed_after_mutation",
        "in_memory.py",
        (
            "test_m13_v6_single_active_attempt_excludes_nested_execute_matrix"
            "[phase-owner-mutation--scope-different-key-same-command-type-and-unit--"
            "outer-outer-commits-caught--nested-runtime-rejection]"
        ),
        """        self._active_attempt = True
        try:
            return self._execute_active(command=command, mutation=mutation)
        finally:
            self._active_attempt = False
""",
        """        def mutation_before_guard(state: Any) -> Mapping[str, str]:
            result = mutation(state)
            self._active_attempt = True
            return result

        try:
            return self._execute_active(command=command, mutation=mutation_before_guard)
        finally:
            self._active_attempt = False
""",
        "owner mutation begins before the active-attempt guard is installed",
    ),
    Mutant(
        "active_guard_cleared_before_participant_commit",
        "in_memory.py",
        (
            "test_m13_v6_single_active_attempt_excludes_nested_execute_matrix"
            "[phase-participant-commit--scope-different-key-same-command-type-and-unit--"
            "outer-outer-commits-caught--nested-runtime-rejection]"
        ),
        """            for participant in self._repository_ports:
                participant.commit()
""",
        """            self._active_attempt = False
            for participant in self._repository_ports:
                participant.commit()
""",
        "the guard clears after prepare and admits re-entry during participant commit",
    ),
    Mutant(
        "receipt_scope_checks_only_command_type",
        "contracts.py",
        (
            "test_m13_v6_atomic_receipt_rejects_contradictory_or_invalid_truth_matrix"
            "[scope-consistency-unit-mismatches-embedded-key]"
        ),
        """        if self.consistency_unit_id != self.idempotency_key.consistency_unit_id:
            raise ValueError("consistency_unit_id must match the idempotency key scope")
""",
        "",
        "receipt scope validation omits consistency-unit coherence",
    ),
    Mutant(
        "resulting_version_accepts_float_and_bool",
        "contracts.py",
        (
            "test_m13_v6_atomic_receipt_rejects_contradictory_or_invalid_truth_matrix"
            "[resulting-state-version-float-is-not-exact-int]"
        ),
        """        if type(self.resulting_state_version) is not int or self.resulting_state_version < 1:
            raise ValueError("resulting_state_version must be a positive integer")
""",
        """        if (
            not isinstance(self.resulting_state_version, (int, float))
            or self.resulting_state_version < 1
        ):
            raise ValueError("resulting_state_version must be a positive number")
""",
        "resulting-state version validation accepts float and bool impostors",
    ),
)


def _run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
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
    OUTPUT.mkdir(parents=True, exist_ok=True)
    summary = ["mutant_id\tfull_exit\ttarget_exit\tintended_rejection\tintended_defect"]
    for mutant in MUTANTS:
        with tempfile.TemporaryDirectory(prefix=f"m13-repair-{mutant.mutant_id}-") as temp:
            overlay = Path(temp) / "src/nvda_desk"
            overlay.mkdir(parents=True)
            shutil.copy2(REPO_ROOT / "src/nvda_desk/__init__.py", overlay / "__init__.py")
            shutil.copytree(SOURCE_PACKAGE, overlay / "m13_state_kernel")

            source_path = overlay / "m13_state_kernel" / mutant.source_file
            source = source_path.read_text(encoding="utf-8")
            if mutant.mutant_id == "module_global_active_attempt_guard":
                marker = "_CommandIdentity = tuple[str, str, str]\n"
                if source.count(marker) != 1:
                    raise AssertionError("module-global insertion anchor is not unique")
                source = source.replace(marker, f"{marker}_MODULE_ACTIVE_ATTEMPT = False\n")
            if source.count(mutant.old) != 1:
                raise AssertionError(
                    f"{mutant.mutant_id}: expected one mutation anchor, "
                    f"found {source.count(mutant.old)}"
                )
            source_path.write_text(source.replace(mutant.old, mutant.new), encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONPATH"] = os.pathsep.join((str(Path(temp) / "src"), str(REPO_ROOT / "src")))
            full_command = [
                sys.executable,
                "-m",
                "pytest",
                "-c",
                os.devnull,
                str(TEST_FILE),
                "-q",
            ]
            target_command = [
                sys.executable,
                "-m",
                "pytest",
                "-c",
                os.devnull,
                f"{TEST_FILE}::{mutant.target_node}",
                "-q",
            ]
            full = _run(full_command, env)
            target = _run(target_command, env)

            for kind, command, result in (
                ("full", full_command, full),
                ("target", target_command, target),
            ):
                (OUTPUT / f"{mutant.mutant_id}.{kind}.command.txt").write_text(
                    " ".join(command) + "\n", encoding="utf-8"
                )
                (OUTPUT / f"{mutant.mutant_id}.{kind}.txt").write_text(
                    result.stdout, encoding="utf-8"
                )
                (OUTPUT / f"{mutant.mutant_id}.{kind}.exit_code").write_text(
                    f"{result.returncode}\n", encoding="utf-8"
                )

            intended = (
                full.returncode == 1
                and target.returncode == 1
                and "1 failed" in target.stdout
                and "ERROR" not in target.stdout
            )
            summary.append(
                "\t".join(
                    (
                        mutant.mutant_id,
                        str(full.returncode),
                        str(target.returncode),
                        "PASS" if intended else "FAIL",
                        mutant.intended_defect,
                    )
                )
            )
            if not intended:
                raise AssertionError(f"{mutant.mutant_id}: intended rejection not observed")

    (OUTPUT / "summary.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"repair_mutants={len(MUTANTS)}")
    print("full_family_rejection=PASS")
    print("targeted_intended_rejection=PASS")


if __name__ == "__main__":
    main()
