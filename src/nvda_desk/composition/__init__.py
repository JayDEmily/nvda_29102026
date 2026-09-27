"""A00 composition boundary for admitted runtime owners and technical mechanisms."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from nvda_desk.architecture.registry import ArchitectureRegistry
from nvda_desk.raw_signal_occurrence_truth._postgres import create_postgres_persistence
from nvda_desk.raw_signal_occurrence_truth.api import create_owner


@dataclass(frozen=True, slots=True)
class CompositionPlan:
    """Explicit list of active executable identities; never a service locator."""

    object_ids: tuple[str, ...]

    @classmethod
    def from_registry(cls, registry: ArchitectureRegistry) -> CompositionPlan:
        return cls(tuple(sorted(item.id for item in registry.objects if item.composable)))

    def require(self, registry: ArchitectureRegistry, object_id: str) -> None:
        registry.require_composable(object_id)
        if object_id not in self.object_ids:
            raise ValueError(f"{object_id} is not present in this composition plan")


_RawSignalOwnerFactory = Callable[..., Any]


@dataclass(frozen=True, slots=True)
class Application:
    """Top-level A00 application composition without Raw Signal semantic ownership."""

    __raw_signal_owner: Any


def create_application(
    *,
    postgres_dsn: str | None = None,
    raw_signal_owner_factory: _RawSignalOwnerFactory | None = None,
) -> Application:
    """Construct the admitted A00 -> M00 production composition.

    The production path requires a PostgreSQL DSN and constructs the accepted technical
    persistence mechanism before injecting it into M00. A bounded owner-factory-only path
    exists for proof of A00 delegation without fabricating a production database dependency.
    """

    owner_factory = create_owner if raw_signal_owner_factory is None else raw_signal_owner_factory

    if postgres_dsn is None:
        if raw_signal_owner_factory is None:
            raise ValueError("postgres_dsn is required for production application construction")
        return Application(owner_factory())

    if type(postgres_dsn) is not str or not postgres_dsn.strip():
        raise ValueError("postgres_dsn must be a non-empty string")

    durability_port = create_postgres_persistence(postgres_dsn)
    owner = owner_factory(durability_port=durability_port)
    return Application(owner)
