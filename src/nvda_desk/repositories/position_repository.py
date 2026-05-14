"""Persist canonical position snapshots in one bounded in-memory store."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class PositionRepository:
    """Deterministic in-memory position repository for the rebuild phase."""

    def __init__(self):
        self._positions: dict[str, dict[str, Any]] = {}

    def write_position(self, position_id: str, position: Mapping[str, Any]) -> None:
        """Store one canonical position snapshot by identifier."""

        normalised_id = str(position_id).strip()
        if not normalised_id:
            raise ValueError("position_id must be non-empty")
        if normalised_id in self._positions:
            raise ValueError(f"duplicate position_id: {normalised_id}")
        self._positions[normalised_id] = deepcopy(dict(position))

    def read_position(self, position_id: str) -> dict[str, Any] | None:
        """Return one stored canonical position snapshot, if present."""

        record = self.read_position_record(position_id)
        return record["position"] if record is not None else None

    def replace_position(self, position_id: str, position: Mapping[str, Any]) -> None:
        """Replace one existing canonical position snapshot by identifier."""

        normalised_id = str(position_id).strip()
        if not normalised_id:
            raise ValueError("position_id must be non-empty")
        if normalised_id not in self._positions:
            raise KeyError(f"unknown position_id: {normalised_id}")
        self._positions[normalised_id] = deepcopy(dict(position))

    def read_position_record(self, position_id: str) -> dict[str, Any] | None:
        """Return one stored position with its repository identifier."""

        normalised_id = str(position_id).strip()
        position = self._positions.get(normalised_id)
        if position is None:
            return None
        return {"position_id": normalised_id, "position": deepcopy(position)}

    def list_positions(self) -> list[dict[str, Any]]:
        """Return stored canonical position snapshots in insertion order."""

        return deepcopy(list(self._positions.values()))

    def list_position_records(self) -> list[dict[str, Any]]:
        """Return stored positions with repository identifiers in insertion order."""

        return [
            {"position_id": position_id, "position": deepcopy(position)}
            for position_id, position in self._positions.items()
        ]
