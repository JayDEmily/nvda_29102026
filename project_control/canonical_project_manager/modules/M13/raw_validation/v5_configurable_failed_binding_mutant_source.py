from __future__ import annotations

import os
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, replace
from typing import Any, Callable, Iterable, Mapping


MUTATION_BOUNDARY = os.environ.get("M13_MUTATION_BOUNDARY", "")
BINDING_COMPARISON = os.environ.get("M13_BINDING_COMPARISON", "")
ADMITTED_BOUNDARIES = {
    "stale_expected_state_version",
    "owner_mutation_exception",
    "invalid_mutation_result_mapping",
    "invalid_or_empty_receipt_id",
    "invalid_or_empty_result_id",
    "repository_participant_prepare_failure",
    "repository_participant_commit_failure",
    "attesting_receipt_writer_failure",
}
ADMITTED_COMPARISONS = {
    "command_id",
    "semantic_input_fingerprint",
    "policy_version",
    "complete_command_identity",
}
if MUTATION_BOUNDARY not in ADMITTED_BOUNDARIES:
    raise ValueError(f"unsupported M13_MUTATION_BOUNDARY: {MUTATION_BOUNDARY!r}")
if BINDING_COMPARISON not in ADMITTED_COMPARISONS:
    raise ValueError(f"unsupported M13_BINDING_COMPARISON: {BINDING_COMPARISON!r}")


class IdempotencyConflictError(ValueError):
    pass


class StateVersionConflictError(ValueError):
    pass


@dataclass(frozen=True)
class IdempotencyKey:
    value: str
    command_type: str
    consistency_unit_id: str

    def __post_init__(self) -> None:
        if not self.value or not self.command_type or not self.consistency_unit_id:
            raise ValueError("idempotency key fields must be non-empty")


@dataclass(frozen=True)
class TransactionCommand:
    command_id: str
    idempotency_key: IdempotencyKey
    input_fingerprint: str
    expected_state_version: int
    policy_version: str

    def __post_init__(self) -> None:
        if not self.command_id or not self.input_fingerprint or not self.policy_version:
            raise ValueError("transaction command identity fields must be non-empty")
        if self.expected_state_version < 0:
            raise ValueError("expected state version must be non-negative")


@dataclass(frozen=True)
class AtomicReceipt:
    receipt_id: str
    result_id: str
    command_id: str
    command_type: str
    consistency_unit_id: str
    idempotency_key: IdempotencyKey
    input_fingerprint: str
    policy_version: str
    prior_state_version: int
    resulting_state_version: int
    sequence: int
    duplicate_replay: bool = False


class RepositoryPort(ABC):
    @abstractmethod
    def prepare(
        self,
        *,
        command: TransactionCommand,
        working_state: Any,
        receipt: AtomicReceipt,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class UnitOfWork(ABC):
    @abstractmethod
    def execute(
        self,
        *,
        command: TransactionCommand,
        mutation: Callable[[Any], Mapping[str, str]],
    ) -> AtomicReceipt:
        raise NotImplementedError


class InMemoryUnitOfWork(UnitOfWork):
    durability = "non_durable_in_memory"

    def __init__(
        self,
        *,
        initial_state: Any,
        repository_ports: Iterable[RepositoryPort] = (),
    ) -> None:
        self._state = deepcopy(initial_state)
        self._state_version = 0
        self._receipts: list[AtomicReceipt] = []
        self._bindings: dict[tuple[str, ...], tuple[tuple[Any, ...], AtomicReceipt]] = {}
        self._failed_bindings: dict[tuple[str, ...], tuple[str, Any]] = {}
        self._repository_ports = tuple(repository_ports)
        if not all(isinstance(port, RepositoryPort) for port in self._repository_ports):
            raise TypeError("repository_ports must implement RepositoryPort")

    @property
    def state_version(self) -> int:
        return self._state_version

    def snapshot_state(self) -> Any:
        return deepcopy(self._state)

    def list_receipts(self) -> tuple[AtomicReceipt, ...]:
        return deepcopy(tuple(self._receipts))

    @staticmethod
    def _scope(key: IdempotencyKey) -> tuple[str, ...]:
        return (key.command_type, key.consistency_unit_id, key.value)

    @staticmethod
    def _command_identity(command: TransactionCommand) -> tuple[Any, ...]:
        return (
            command.command_id,
            command.input_fingerprint,
            command.policy_version,
            command.expected_state_version,
        )

    @staticmethod
    def _failed_binding_signature(command: TransactionCommand) -> Any:
        if BINDING_COMPARISON == "command_id":
            return command.command_id
        if BINDING_COMPARISON == "semantic_input_fingerprint":
            return command.input_fingerprint
        if BINDING_COMPARISON == "policy_version":
            return command.policy_version
        return (
            command.command_id,
            command.input_fingerprint,
            command.policy_version,
            command.expected_state_version,
        )

    def _reserve_failed_binding(
        self,
        *,
        scope: tuple[str, ...],
        command: TransactionCommand,
        boundary: str,
    ) -> None:
        if MUTATION_BOUNDARY == boundary:
            self._failed_bindings[scope] = (
                BINDING_COMPARISON,
                self._failed_binding_signature(command),
            )

    def execute(
        self,
        *,
        command: TransactionCommand,
        mutation: Callable[[Any], Mapping[str, str]],
    ) -> AtomicReceipt:
        scope = self._scope(command.idempotency_key)
        identity = self._command_identity(command)
        existing = self._bindings.get(scope)
        if existing is not None:
            existing_identity, existing_receipt = existing
            if existing_identity != identity:
                raise IdempotencyConflictError("conflicting idempotency-key reuse")
            return replace(existing_receipt, duplicate_replay=True)

        failed_binding = self._failed_bindings.get(scope)
        if failed_binding is not None:
            comparison, failed_signature = failed_binding
            incoming_signature = self._failed_binding_signature(command)
            false_conflict = (
                failed_signature != incoming_signature
                if comparison == "complete_command_identity"
                else failed_signature == incoming_signature
            )
            if false_conflict:
                raise IdempotencyConflictError(
                    "hidden failed-attempt binding falsely conflicts "
                    f"by {comparison} at {MUTATION_BOUNDARY}"
                )

        if command.expected_state_version != self._state_version:
            self._reserve_failed_binding(
                scope=scope,
                command=command,
                boundary="stale_expected_state_version",
            )
            raise StateVersionConflictError("stale expected state version")

        prior_version = self._state_version
        working_state = deepcopy(self._state)
        try:
            result = mutation(working_state)
        except BaseException:
            self._reserve_failed_binding(
                scope=scope,
                command=command,
                boundary="owner_mutation_exception",
            )
            raise

        if not isinstance(result, Mapping):
            self._reserve_failed_binding(
                scope=scope,
                command=command,
                boundary="invalid_mutation_result_mapping",
            )
            raise TypeError("receipt result must be a mapping")
        receipt_id = result.get("receipt_id")
        result_id = result.get("result_id")
        if not isinstance(receipt_id, str) or not receipt_id:
            self._reserve_failed_binding(
                scope=scope,
                command=command,
                boundary="invalid_or_empty_receipt_id",
            )
            raise ValueError("receipt_id must be a non-empty receipt identifier")
        if not isinstance(result_id, str) or not result_id:
            self._reserve_failed_binding(
                scope=scope,
                command=command,
                boundary="invalid_or_empty_result_id",
            )
            raise ValueError("receipt result_id must be non-empty")

        resulting_version = prior_version + 1
        receipt = AtomicReceipt(
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
            sequence=len(self._receipts) + 1,
        )

        internal_before = (
            deepcopy(self._state),
            self._state_version,
            deepcopy(self._receipts),
            deepcopy(self._bindings),
        )
        prepared: list[RepositoryPort] = []
        failure_stage = ""
        try:
            for port in self._repository_ports:
                failure_stage = "repository_participant_prepare_failure"
                prepared.append(port)
                port.prepare(
                    command=command,
                    working_state=deepcopy(working_state),
                    receipt=deepcopy(receipt),
                )
            for index, port in enumerate(self._repository_ports):
                failure_stage = (
                    "attesting_receipt_writer_failure"
                    if index == len(self._repository_ports) - 1
                    else "repository_participant_commit_failure"
                )
                port.commit()

            self._state = working_state
            self._state_version = resulting_version
            self._receipts.append(receipt)
            self._bindings[scope] = (identity, receipt)
            self._failed_bindings.pop(scope, None)
        except BaseException:
            for port in reversed(prepared):
                try:
                    port.rollback()
                except BaseException:
                    pass
            self._state, self._state_version, self._receipts, self._bindings = internal_before
            self._reserve_failed_binding(
                scope=scope,
                command=command,
                boundary=failure_stage,
            )
            raise

        return receipt
