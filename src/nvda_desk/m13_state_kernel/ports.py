"""Public transaction and participant protocols owned by M13."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from typing import Any

from pydantic import BaseModel

from .contracts import AtomicReceipt, DurableEvidenceRecord, TransactionCommand


class RepositoryPort(ABC):
    """Storage participant protocol without ownership of stored domain meaning."""

    @abstractmethod
    def prepare(
        self,
        *,
        command: TransactionCommand,
        working_state: Any,
        receipt: AtomicReceipt,
    ) -> None:
        """Stage transaction-local truth without claiming a successful commit."""
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        """Publish the participant's prepared truth for the current attempt."""
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        """Restore participant-visible and pending truth to its pre-attempt state."""
        raise NotImplementedError


class UnitOfWork(ABC):
    """One owner-declared transaction execution boundary."""

    @abstractmethod
    def execute(
        self,
        *,
        command: TransactionCommand,
        mutation: Callable[[Any], Mapping[str, str]],
    ) -> AtomicReceipt:
        """Commit state and receipt truth together or publish neither."""
        raise NotImplementedError


class StateReadPort(ABC):
    """Read-only detached state view; it owns no domain interpretation."""

    @property
    @abstractmethod
    def state_version(self) -> int:
        """Return the current committed state version."""
        raise NotImplementedError

    @abstractmethod
    def snapshot_state(self) -> Any:
        """Return a detached snapshot of current committed state."""
        raise NotImplementedError


class TransactionalStatePort(UnitOfWork, StateReadPort):
    """Combined transaction and detached-read port for owner repositories."""


class EvidenceRepositoryPort(ABC):
    """Typed durable evidence store without ownership of domain meaning."""

    @abstractmethod
    def store(
        self,
        *,
        owner_module: str,
        occurrence_id: str,
        content: BaseModel,
    ) -> DurableEvidenceRecord:
        """Persist one typed occurrence or return its exact idempotent record."""
        raise NotImplementedError

    @abstractmethod
    def load(self, occurrence_id: str) -> BaseModel:
        """Reload one typed occurrence and validate its retained contract."""
        raise NotImplementedError

    @abstractmethod
    def list_records(self) -> tuple[DurableEvidenceRecord, ...]:
        """Return durable occurrence identities in committed sequence order."""
        raise NotImplementedError
