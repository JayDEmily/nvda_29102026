"""Declarative architecture registry. It is metadata, not a service locator."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .identifiers import parse_identifier
from .schema import validate_document

_REGISTRY_SPECS = (
    ("modules.yaml", "modules", "module.schema.json", "M"),
    ("protocols.yaml", "protocols", "protocol.schema.json", "P"),
    ("governance_planes.yaml", "governance_planes", "governance_plane.schema.json", "G"),
    ("application_shells.yaml", "application_shells", "application_shell.schema.json", "A"),
    ("kernels.yaml", "kernels", "kernel.schema.json", "K"),
    ("surfaces.yaml", "surfaces", "surface.schema.json", "S"),
)
_EXECUTABLE_CATEGORIES = frozenset({"A", "M", "K"})


@dataclass(frozen=True, slots=True)
class ArchitectureObject:
    id: str
    name: str
    status: str
    description: str
    package: str | None = None
    public_seam: str | None = None
    permitted_dependencies: tuple[str, ...] = ()
    predecessors: tuple[str, ...] = ()
    successors: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False, hash=False)

    @property
    def category(self) -> str:
        return parse_identifier(self.id).prefix

    @property
    def composable(self) -> bool:
        return self.status == "active" and self.category in _EXECUTABLE_CATEGORIES


class ArchitectureRegistry:
    """Validated metadata view over all architecture-object registries."""

    def __init__(
        self, objects: tuple[ArchitectureObject, ...], retired_ids: frozenset[str]
    ) -> None:
        self.objects = objects
        self.retired_ids = retired_ids
        self._by_id = {item.id: item for item in objects}
        self.validate_integrity()

    @classmethod
    def from_repository(cls, repository_root: Path) -> ArchitectureRegistry:
        config_root = repository_root / "config" / "architecture"
        schema_root = repository_root / "schemas"
        objects: list[ArchitectureObject] = []
        retired: set[str] = set()
        for filename, key, schema_filename, prefix in _REGISTRY_SPECS:
            document_path = config_root / filename
            validate_document(document_path, schema_root / schema_filename)
            document = yaml.safe_load(document_path.read_text(encoding="utf-8"))
            for raw in document[key]:
                if parse_identifier(raw["id"]).prefix != prefix:
                    raise ValueError(f"{raw['id']} is in the wrong registry: {filename}")
                known = {
                    "id",
                    "name",
                    "status",
                    "description",
                    "package",
                    "public_seam",
                    "permitted_dependencies",
                    "predecessors",
                    "successors",
                }
                objects.append(
                    ArchitectureObject(
                        id=raw["id"],
                        name=raw["name"],
                        status=raw["status"],
                        description=raw["description"],
                        package=raw.get("package"),
                        public_seam=raw.get("public_seam"),
                        permitted_dependencies=tuple(raw.get("permitted_dependencies", ())),
                        predecessors=tuple(raw.get("predecessors", ())),
                        successors=tuple(raw.get("successors", ())),
                        metadata={name: value for name, value in raw.items() if name not in known},
                    )
                )
            retired.update(document.get("retired_ids", ()))
        return cls(tuple(objects), frozenset(retired))

    def validate_integrity(self) -> None:
        ids = [item.id for item in self.objects]
        if len(ids) != len(set(ids)):
            raise ValueError("active architecture identifiers are not unique")
        overlap = set(ids) & self.retired_ids
        if overlap:
            raise ValueError(f"retired identifiers were reused: {sorted(overlap)}")
        for value in self.retired_ids:
            parse_identifier(value)
        for item in self.objects:
            if (
                item.status == "active"
                and item.category in _EXECUTABLE_CATEGORIES
                and (not item.package or not item.public_seam)
            ):
                raise ValueError(f"active executable object {item.id} lacks package/public_seam")
            if (item.package is None) != (item.public_seam is None):
                raise ValueError(f"{item.id} must declare package and public_seam together")
            if (
                item.public_seam
                and item.package
                and not (
                    item.public_seam == item.package
                    or item.public_seam.startswith(item.package + ".")
                )
            ):
                raise ValueError(f"{item.id} public seam is outside its package")
            for dependency in item.permitted_dependencies:
                parse_identifier(dependency)
                if dependency not in self._by_id:
                    raise ValueError(f"{item.id} declares unknown dependency {dependency}")
            if len(item.predecessors) != len(set(item.predecessors)):
                raise ValueError(f"{item.id} has duplicate predecessor identifiers")
            if len(item.successors) != len(set(item.successors)):
                raise ValueError(f"{item.id} has duplicate successor identifiers")
            for predecessor in item.predecessors:
                parse_identifier(predecessor)
                if predecessor == item.id:
                    raise ValueError(f"{item.id} cannot be its own predecessor")
                current_predecessor = self._by_id.get(predecessor)
                if current_predecessor is None and predecessor not in self.retired_ids:
                    raise ValueError(
                        f"{item.id} names unregistered lifecycle predecessor {predecessor}"
                    )
                if current_predecessor and item.id not in current_predecessor.successors:
                    raise ValueError(
                        f"current predecessor {predecessor} does not name {item.id} as successor"
                    )
            for successor in item.successors:
                parse_identifier(successor)
                if successor == item.id:
                    raise ValueError(f"{item.id} cannot be its own successor")
                current_successor = self._by_id.get(successor)
                if current_successor is None and successor not in self.retired_ids:
                    raise ValueError(
                        f"{item.id} names unregistered lifecycle successor {successor}"
                    )
                if current_successor and item.id not in current_successor.predecessors:
                    raise ValueError(
                        f"current successor {successor} does not name {item.id} as predecessor"
                    )

    def get(self, object_id: str) -> ArchitectureObject:
        try:
            return self._by_id[object_id]
        except KeyError as exc:
            raise KeyError(f"unregistered architecture object: {object_id}") from exc

    def require_composable(self, object_id: str) -> ArchitectureObject:
        item = self.get(object_id)
        if not item.composable:
            raise ValueError(f"{object_id} has status {item.status!r} and is not composable")
        return item

    def active_runtime_modules(self) -> tuple[ArchitectureObject, ...]:
        return tuple(
            item for item in self.objects if item.category == "M" and item.status == "active"
        )

    def package_owners(self) -> tuple[ArchitectureObject, ...]:
        return tuple(item for item in self.objects if item.package is not None)
