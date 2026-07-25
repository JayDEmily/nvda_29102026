from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, replace
from typing import Any, Callable, Iterable, Mapping


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
        """Stage one transaction participant without publishing committed truth."""
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        """Publish the prepared participant state for the current transaction."""
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        """Restore the participant to its pre-transaction visible state."""
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
        try:
            self._state = working_state
            self._state_version = resulting_version
            self._receipts.append(receipt)
            self._bindings[scope] = (identity, receipt)
            for port in self._repository_ports:
                prepared.append(port)
                port.prepare(
                    command=command,
                    working_state=deepcopy(working_state),
                    receipt=deepcopy(receipt),
                )
            for port in self._repository_ports:
                port.commit()
        except BaseException:
            for port in reversed(prepared):
                try:
                    port.rollback()
                except BaseException:
                    pass
            raise

        return receipt
