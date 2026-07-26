"""Configurable proof-only V6 false-positive implementation.

Each M13_V6_MUTANT value activates one bounded semantic defect while the
conforming source remains the common successful-behaviour base.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from typing import Any

MODE = os.environ.get("M13_V6_MUTANT", "")
MODES = {
    "nested_allowed_different_key",
    "nested_allowed_different_consistency_unit",
    "nested_receipt_commits_later_loses_state",
    "nested_state_commits_without_receipt",
    "nested_and_outer_reuse_sequence",
    "nested_and_outer_reuse_resulting_version",
    "active_guard_set_after_mutation_starts",
    "active_guard_cleared_before_participant_commit",
    "active_guard_not_cleared_after_failure",
    "receipt_scope_checks_only_command_type",
    "receipt_scope_checks_only_consistency_unit",
    "receipt_version_validation_accepts_floats",
    "receipt_version_validation_accepts_booleans",
    "receipt_resulting_version_may_equal_prior",
    "receipt_sequence_may_be_nonpositive",
    "replay_response_alters_committed_identity",
}
if MODE not in MODES:
    raise ValueError(f"unsupported M13_V6_MUTANT: {MODE!r}")

REFERENCE_PATH = Path(__file__).with_name("v6_reference_conforming_source.py")
SPEC = importlib.util.spec_from_file_location("_m13_v6_reference", REFERENCE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load V6 conforming reference: {REFERENCE_PATH}")
_reference = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = _reference
SPEC.loader.exec_module(_reference)

IdempotencyConflictError = _reference.IdempotencyConflictError
StateVersionConflictError = _reference.StateVersionConflictError
IdempotencyKey = _reference.IdempotencyKey
TransactionCommand = _reference.TransactionCommand
RepositoryPort = _reference.RepositoryPort
UnitOfWork = _reference.UnitOfWork
AtomicReceipt = _reference.AtomicReceipt


def _receipt_validation_with_mutation(receipt: Any) -> None:
    for field in (
        "receipt_id",
        "result_id",
        "command_id",
        "command_type",
        "consistency_unit_id",
        "input_fingerprint",
        "policy_version",
    ):
        _reference._non_empty(getattr(receipt, field), field)
    if not isinstance(receipt.idempotency_key, IdempotencyKey):
        raise TypeError("idempotency_key must be an IdempotencyKey")
    if (
        MODE != "receipt_scope_checks_only_consistency_unit"
        and receipt.command_type != receipt.idempotency_key.command_type
    ):
        raise ValueError("receipt command_type must match idempotency key scope")
    if (
        MODE != "receipt_scope_checks_only_command_type"
        and receipt.consistency_unit_id != receipt.idempotency_key.consistency_unit_id
    ):
        raise ValueError("receipt consistency_unit_id must match idempotency key scope")

    version_fields = (
        "prior_state_version",
        "resulting_state_version",
        "sequence",
    )
    for field in version_fields:
        value = getattr(receipt, field)
        if MODE == "receipt_version_validation_accepts_floats":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError(f"{field} must be numeric")
        elif MODE == "receipt_version_validation_accepts_booleans":
            if not isinstance(value, int):
                raise TypeError(f"{field} must be an integer")
        else:
            _reference._exact_int(value, field)

    if receipt.prior_state_version < 0:
        raise ValueError("prior_state_version must be non-negative")
    if (
        MODE != "receipt_resulting_version_may_equal_prior"
        and receipt.resulting_state_version != receipt.prior_state_version + 1
    ):
        raise ValueError("resulting_state_version must be the exact next version")
    if MODE == "receipt_resulting_version_may_equal_prior":
        if receipt.resulting_state_version < receipt.prior_state_version:
            raise ValueError("resulting_state_version cannot go backwards")
    if MODE != "receipt_sequence_may_be_nonpositive" and receipt.sequence <= 0:
        raise ValueError("sequence must be positive")
    if type(receipt.duplicate_replay) is not bool:
        raise TypeError("duplicate_replay must be a bool")


if MODE.startswith("receipt_"):
    AtomicReceipt.__post_init__ = _receipt_validation_with_mutation


class _CommitPhaseProxy(RepositoryPort):
    def __init__(self, *, target: RepositoryPort, boundary: Any, final_prepare: bool) -> None:
        self.target = target
        self.boundary = boundary
        self.final_prepare = final_prepare

    def prepare(self, *, command: Any, working_state: Any, receipt: Any) -> None:
        self.target.prepare(
            command=command,
            working_state=working_state,
            receipt=receipt,
        )
        if self.final_prepare:
            self.boundary._active_attempt = False

    def commit(self) -> None:
        self.target.commit()

    def rollback(self) -> None:
        self.target.rollback()


class InMemoryUnitOfWork(_reference.InMemoryUnitOfWork):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._deferred_nested_state: Any = None
        if MODE == "active_guard_cleared_before_participant_commit":
            original = self._repository_ports
            self._repository_ports = tuple(
                _CommitPhaseProxy(
                    target=port,
                    boundary=self,
                    final_prepare=index == len(original) - 1,
                )
                for index, port in enumerate(original)
            )

    def _allowed_by_scoped_guard(self, command: TransactionCommand) -> bool:
        active_command = getattr(self, "_active_command", None)
        if active_command is None:
            return False
        if MODE == "nested_allowed_different_key":
            return self._scope(command.idempotency_key) != self._scope(
                active_command.idempotency_key
            )
        if MODE == "nested_allowed_different_consistency_unit":
            return (
                command.idempotency_key.consistency_unit_id
                != active_command.idempotency_key.consistency_unit_id
            )
        return False

    def _defer_nested_state_without_receipt(
        self,
        *,
        command: TransactionCommand,
        mutation: Any,
    ) -> AtomicReceipt:
        working_state = deepcopy(self._state)
        result = mutation(working_state)
        self._deferred_nested_state = working_state
        return AtomicReceipt(
            receipt_id=result["receipt_id"],
            result_id=result["result_id"],
            command_id=command.command_id,
            command_type=command.idempotency_key.command_type,
            consistency_unit_id=command.idempotency_key.consistency_unit_id,
            idempotency_key=command.idempotency_key,
            input_fingerprint=command.input_fingerprint,
            policy_version=command.policy_version,
            prior_state_version=self._state_version,
            resulting_state_version=self._state_version + 1,
            sequence=self._committed_sequence + 1,
        )

    def execute(self, *, command: TransactionCommand, mutation: Any) -> AtomicReceipt:
        allow_all_nested = MODE in {
            "nested_receipt_commits_later_loses_state",
            "nested_and_outer_reuse_sequence",
            "nested_and_outer_reuse_resulting_version",
        }
        if self._active_attempt:
            if MODE == "nested_state_commits_without_receipt":
                return self._defer_nested_state_without_receipt(
                    command=command,
                    mutation=mutation,
                )
            if allow_all_nested or self._allowed_by_scoped_guard(command):
                return self._execute_active(command=command, mutation=mutation)
            raise RuntimeError("UnitOfWork.execute attempt is already active")

        if MODE == "active_guard_set_after_mutation_starts":

            def mutation_before_guard(state: Any) -> Any:
                result = mutation(state)
                self._active_attempt = True
                return result

            try:
                return self._execute_active(
                    command=command,
                    mutation=mutation_before_guard,
                )
            finally:
                self._active_attempt = False

        if MODE == "active_guard_not_cleared_after_failure":
            self._active_attempt = True
            result = self._execute_active(command=command, mutation=mutation)
            self._active_attempt = False
            return result

        previous_command = getattr(self, "_active_command", None)
        self._active_command = command
        try:
            result = super().execute(command=command, mutation=mutation)
        finally:
            self._active_command = previous_command

        if (
            MODE == "nested_state_commits_without_receipt"
            and self._deferred_nested_state is not None
        ):
            self._state = self._deferred_nested_state
            self._deferred_nested_state = None
        return result

    def _execute_active(
        self,
        *,
        command: TransactionCommand,
        mutation: Any,
    ) -> AtomicReceipt:
        if MODE == "replay_response_alters_committed_identity":
            scope = self._scope(command.idempotency_key)
            existing = self._bindings.get(scope)
            if existing is not None:
                existing_identity, existing_receipt = existing
                if existing_identity != self._command_identity(command):
                    raise IdempotencyConflictError("conflicting idempotency-key reuse")
                return replace(
                    existing_receipt,
                    receipt_id=f"{existing_receipt.receipt_id}-replay",
                    result_id=f"{existing_receipt.result_id}-replay",
                    duplicate_replay=True,
                )
        return super()._execute_active(command=command, mutation=mutation)
