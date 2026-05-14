"""Persist canonical capital-state snapshots in one bounded in-memory store."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class CapitalStateRepository:
    """Deterministic in-memory capital-state repository for the rebuild phase."""

    def __init__(self):
        self._snapshots: dict[str, dict[str, Any]] = {}

    def write_snapshot(self, snapshot_id: str, snapshot: Mapping[str, Any]) -> None:
        """Store one capital-state snapshot by identifier."""

        normalised_id = str(snapshot_id).strip()
        if not normalised_id:
            raise ValueError("snapshot_id must be non-empty")
        if normalised_id in self._snapshots:
            raise ValueError(f"duplicate snapshot_id: {normalised_id}")
        self._snapshots[normalised_id] = deepcopy(dict(snapshot))

    def read_snapshot(self, snapshot_id: str) -> dict[str, Any] | None:
        """Return one stored capital-state snapshot, if present."""

        record = self.read_snapshot_record(snapshot_id)
        return record["snapshot"] if record is not None else None

    def read_snapshot_record(self, snapshot_id: str) -> dict[str, Any] | None:
        """Return one stored capital-state snapshot with its repository identifier."""

        normalised_id = str(snapshot_id).strip()
        snapshot = self._snapshots.get(normalised_id)
        if snapshot is None:
            return None
        return {"snapshot_id": normalised_id, "snapshot": deepcopy(snapshot)}

    def list_snapshots(self) -> list[dict[str, Any]]:
        """Return stored capital-state snapshots in insertion order."""

        return deepcopy(list(self._snapshots.values()))

    def list_snapshot_records(self) -> list[dict[str, Any]]:
        """Return stored capital-state snapshots with identifiers in insertion order."""

        return [
            {"snapshot_id": snapshot_id, "snapshot": deepcopy(snapshot)}
            for snapshot_id, snapshot in self._snapshots.items()
        ]
