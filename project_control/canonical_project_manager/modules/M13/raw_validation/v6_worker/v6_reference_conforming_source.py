"""Proof-only conforming reference for the admitted non-durable M13 V6 contract.

This file is external falsification evidence.  It is not production code and
makes no durability, process-safety, crash-recovery or production-readiness claim.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, replace
from typing import Any, Callable, Iterable, Mapping


def _non_empty(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty string")


def _exact_int(value: Any, field: str) -> None:
    if type(value) is not int:
        raise TypeError(f"{field} must be an exact integer")


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
        _non_empty(self.value, "idempotency key value")
        _non_empty(self.command_type, "idempotency key command_type")
        _non_empty(self.consistency_unit_id, "idempotency key consistency_unit_id")


@dataclass(frozen=True)
class TransactionCommand:
    command_id: str
    idempotency_key: IdempotencyKey
    input_fingerprint: str
    expected_state_version: int
    policy_version: str

    def __post_init__(self) -> None:
        _non_empty(self.command_id, "command_id")
        if not isinstance(self.idempotency_key, IdempotencyKey):
            raise TypeError("idempotency_key must be an IdempotencyKey")
        _non_empty(self.input_fingerprint, "input_fingerprint")
        _non_empty(self.policy_version, "policy_version")
        _exact_int(self.expected_state_version, "expected_state_version")
        if self.expected_state_version < 0:
            raise ValueError("expected_state_version must be non-negative")


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

    def __post_init__(self) -> None:
        for field in (
            "receipt_id",
            "result_id",
            "command_id",
            "command_type",
            "consistency_unit_id",
            "input_fingerprint",
            "policy_version",
        ):
            _non_empty(getattr(self, field), field)
        if not isinstance(self.idempotency_key, IdempotencyKey):
            raise TypeError("idempotency_key must be an IdempotencyKey")
        if self.command_type != self.idempotency_key.command_type:
            raise ValueError("receipt command_type must match idempotency key scope")
        if self.consistency_unit_id != self.idempotency_key.consistency_unit_id:
            raise ValueError("receipt consistency_unit_id must match idempotency key scope")
        _exact_int(self.prior_state_version, "prior_state_version")
        _exact_int(self.resulting_state_version, "resulting_state_version")
        _exact_int(self.sequence, "sequence")
        if self.prior_state_version < 0:
            raise ValueError("prior_state_version must be non-negative")
        if self.resulting_state_version != self.prior_state_version + 1:
            raise ValueError("resulting_state_version must be the exact next version")
        if self.sequence <= 0:
            raise ValueError("sequence must be positive")
        if type(self.duplicate_replay) is not bool:
            raise TypeError("duplicate_replay must be a bool")


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
        self._committed_sequence = 0
        self._receipts: list[AtomicReceipt] = []
        self._bindings: dict[tuple[str, ...], tuple[tuple[Any, ...], AtomicReceipt]] = {}
        self._repository_ports = tuple(repository_ports)
        if not all(isinstance(port, RepositoryPort) for port in self._repository_ports):
            raise TypeError("repository_ports must implement RepositoryPort")
        self._active_attempt = False

    @property
    def state_version(self) -> int:
        return self._state_version

    @property
    def committed_sequence(self) -> int:
        return self._committed_sequence

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
        identity = self._command_identity(command)
        existing = self._bindings.get(scope)
        if existing is not None:
            existing_identity, existing_receipt = existing
            if existing_identity != identity:
                raise IdempotencyConflictError("conflicting idempotency-key reuse")
            return replace(existing_receipt, duplicate_replay=True)

        if command.expected_state_version != self._state_version:
            raise StateVersionConflictError("stale expected state version")

        prior_version = self._state_version
        working_state = deepcopy(self._state)
        result = mutation(working_state)
        if not isinstance(result, Mapping):
            raise TypeError("receipt result must be a mapping")
        receipt_id = result.get("receipt_id")
        result_id = result.get("result_id")
        if not isinstance(receipt_id, str) or not receipt_id:
            raise ValueError("receipt_id must be a non-empty receipt identifier")
        if not isinstance(result_id, str) or not result_id:
            raise ValueError("receipt result_id must be non-empty")

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
            resulting_state_version=prior_version + 1,
            sequence=self._committed_sequence + 1,
        )
        internal_before = (
            deepcopy(self._state),
            self._state_version,
            self._committed_sequence,
            deepcopy(self._receipts),
            deepcopy(self._bindings),
        )
        rollback_responsibility: list[RepositoryPort] = []
        try:
            for port in self._repository_ports:
                rollback_responsibility.append(port)
                port.prepare(
                    command=command,
                    working_state=deepcopy(working_state),
                    receipt=deepcopy(receipt),
                )
            for port in self._repository_ports:
                port.commit()

            self._state = working_state
            self._state_version = receipt.resulting_state_version
            self._committed_sequence = receipt.sequence
            self._receipts.append(receipt)
            self._bindings[scope] = (identity, receipt)
        except BaseException:
            for port in reversed(rollback_responsibility):
                try:
                    port.rollback()
                except BaseException:
                    pass
            (
                self._state,
                self._state_version,
                self._committed_sequence,
                self._receipts,
                self._bindings,
            ) = internal_before
            raise

        return receipt
