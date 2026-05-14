"""Persist execution records in one bounded append-only in-memory store."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class ExecutionRecordsRepository:
    """Deterministic append-only repository for execution records."""

    def __init__(self):
        self._records: list[dict[str, Any]] = []

    def append_record(self, record: Mapping[str, Any]) -> None:
        """Append one execution record to the bounded store."""
        self._records.append(deepcopy(dict(record)))

    def list_records(self) -> list[dict[str, Any]]:
        """Return all stored execution records in insertion order."""
        return deepcopy(self._records)
