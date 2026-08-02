"""Explicitly non-durable in-memory implementation of the M13 transaction seam."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from copy import deepcopy
from dataclasses import dataclass, replace
from typing import Any

from .contracts import (
    AtomicReceipt,
    IdempotencyConflictError,
    IdempotencyKey,
    StateVersionConflictError,
    TransactionCommand,
)
from .ports import RepositoryPort, TransactionalStatePort

_Scope = tuple[str, str, str]
_CommandIdentity = tuple[str, str, str]


@dataclass(frozen=True, slots=True)
class _CommittedBinding:
    command_identity: _CommandIdentity
    receipt: AtomicReceipt


class InMemoryUnitOfWork(TransactionalStatePort):
    """Detached alpha adapter proving only in-process, non-durable behaviour."""

    durability = "non_durable_in_memory"

    def __init__(
        self,
        *,
        initial_state: Any,
        repository_ports: Iterable[RepositoryPort] = (),
    ) -> None:
        ports = tuple(repository_ports)
        if not all(isinstance(port, RepositoryPort) for port in ports):
            raise TypeError("repository_ports must implement RepositoryPort")

        self._state = deepcopy(initial_state)
        self._state_version = 0
        self._committed_sequence = 0
        self._receipts: list[AtomicReceipt] = []
        self._bindings: dict[_Scope, _CommittedBinding] = {}
        self._repository_ports = ports
        self._active_attempt = False

    @property
    def state_version(self) -> int:
        """Return the current committed state version."""

        return self._state_version

    @property
    def committed_sequence(self) -> int:
        """Return the latest successfully committed receipt sequence."""

        return self._committed_sequence

    def snapshot_state(self) -> Any:
        """Return a detached snapshot of current committed state."""

        return deepcopy(self._state)

    def list_receipts(self) -> tuple[AtomicReceipt, ...]:
        """Return detached committed receipts in deterministic sequence order."""

        return deepcopy(tuple(self._receipts))

    def execute(
        self,
        *,
        command: TransactionCommand,
        mutation: Callable[[Any], Mapping[str, str]],
    ) -> AtomicReceipt:
        if not isinstance(command, TransactionCommand):
            raise TypeError("command must be a TransactionCommand")
        if not callable(mutation):
            raise TypeError("mutation must be callable")
        if self._active_attempt:
            raise RuntimeError("UnitOfWork.execute attempt is already active")

        self._active_attempt = True
        try:
            return self._execute_active(command=command, mutation=mutation)
        finally:
            self._active_attempt = False

    def _execute_active(
        self,
        *,
        command: TransactionCommand,
        mutation: Callable[[Any], Mapping[str, str]],
    ) -> AtomicReceipt:
        scope = self._scope(command.idempotency_key)
        command_identity = self._command_identity(command)
        committed = self._bindings.get(scope)

        # A committed duplicate is resolved before optimistic-version rejection:
        # its original expected version is necessarily stale after commit.
        if committed is not None:
            if committed.command_identity != command_identity:
                raise IdempotencyConflictError("conflicting idempotency-key reuse")
            return replace(deepcopy(committed.receipt), duplicate_replay=True)

        if command.expected_state_version != self._state_version:
            raise StateVersionConflictError("stale expected state version")

        prior_version = self._state_version
        resulting_version = prior_version + 1
        proposed_sequence = self._committed_sequence + 1
        working_state = deepcopy(self._state)
        mutation_result = mutation(working_state)
        receipt = self._build_receipt(
            command=command,
            mutation_result=mutation_result,
            prior_version=prior_version,
            resulting_version=resulting_version,
            sequence=proposed_sequence,
        )

        self._coordinate_participants(
            command=command,
            working_state=working_state,
            receipt=receipt,
        )

        # Internal truth is published only after every external participant
        # reports a successful commit. Failed attempts create no binding.
        self._state = working_state
        self._state_version = resulting_version
        self._committed_sequence = proposed_sequence
        self._receipts.append(receipt)
        self._bindings[scope] = _CommittedBinding(command_identity, receipt)
        return deepcopy(receipt)

    @staticmethod
    def _scope(key: IdempotencyKey) -> _Scope:
        return (key.value, key.command_type, key.consistency_unit_id)

    @staticmethod
    def _command_identity(command: TransactionCommand) -> _CommandIdentity:
        return (
            command.command_id,
            command.input_fingerprint,
            command.policy_version,
        )

    @staticmethod
    def _build_receipt(
        *,
        command: TransactionCommand,
        mutation_result: Mapping[str, str],
        prior_version: int,
        resulting_version: int,
        sequence: int,
    ) -> AtomicReceipt:
        if not isinstance(mutation_result, Mapping):
            raise TypeError("receipt result must be a mapping")

        receipt_id = mutation_result.get("receipt_id")
        result_id = mutation_result.get("result_id")
        if not isinstance(receipt_id, str) or not receipt_id.strip():
            raise ValueError("receipt_id must be a non-empty receipt identifier")
        if not isinstance(result_id, str) or not result_id.strip():
            raise ValueError("receipt result_id must be non-empty")

        return AtomicReceipt(
            receipt_id=receipt_id,
            result_id=result_id,
            command_id=command.command_id,
            command_type=command.idempotency_key.command_type,
            consistency_unit_id=command.idempotency_key.consistency_unit_id,
            idempotency_key=command.idempotency_key,
            input_fingerprint=command.input_fingerprint,
            policy_version=command.policy_version,
            prior_state_version=prior_version,
            resulting_state_version=resulting_version,
            sequence=sequence,
        )

    def _coordinate_participants(
        self,
        *,
        command: TransactionCommand,
        working_state: Any,
        receipt: AtomicReceipt,
    ) -> None:
        rollback_responsibility: list[RepositoryPort] = []
        try:
            for participant in self._repository_ports:
                # Registration precedes prepare because prepare itself may create
                # pending participant truth before raising.
                rollback_responsibility.append(participant)
                participant.prepare(
                    command=command,
                    working_state=deepcopy(working_state),
                    receipt=deepcopy(receipt),
                )

            for participant in self._repository_ports:
                participant.commit()
        except BaseException as primary_failure:
            rollback_failures: list[Exception] = []
            for participant in reversed(rollback_responsibility):
                try:
                    participant.rollback()
                except Exception as rollback_failure:
                    rollback_failures.append(rollback_failure)
            for rollback_failure in rollback_failures:
                primary_failure.add_note(
                    "participant rollback also failed: "
                    f"{type(rollback_failure).__name__}: {rollback_failure}"
                )
            raise
