"""Minimal composition boundary with no domain objects admitted."""

from __future__ import annotations

from dataclasses import dataclass

from nvda_desk.architecture.registry import ArchitectureRegistry


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
