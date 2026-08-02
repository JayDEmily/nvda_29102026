"""Public M13 state-kernel surface for bounded non-durable transactions."""

from .contracts import (
    AtomicReceipt,
    DurableEvidenceRecord,
    IdempotencyConflictError,
    IdempotencyKey,
    StateVersionConflictError,
    TransactionCommand,
)
from .in_memory import InMemoryUnitOfWork
from .ports import (
    EvidenceRepositoryPort,
    RepositoryPort,
    StateReadPort,
    TransactionalStatePort,
    UnitOfWork,
)
from .sqlite import SqliteEvidenceRepository, SqliteUnitOfWork

__all__ = [
    "SqliteUnitOfWork",
    "SqliteEvidenceRepository",
    "DurableEvidenceRecord",
    "EvidenceRepositoryPort",
    "AtomicReceipt",
    "IdempotencyConflictError",
    "IdempotencyKey",
    "InMemoryUnitOfWork",
    "RepositoryPort",
    "StateVersionConflictError",
    "TransactionalStatePort",
    "StateReadPort",
    "TransactionCommand",
    "UnitOfWork",
]
