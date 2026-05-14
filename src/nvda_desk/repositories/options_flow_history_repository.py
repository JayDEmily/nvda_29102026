"""Persist options-flow history observations in one bounded append-only store."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class OptionsFlowHistoryRepository:
    """Deterministic append-only repository for options-flow history records."""

    def __init__(self):
        self._records: list[dict[str, Any]] = []

    def append_record(self, record: Mapping[str, Any]) -> None:
        """Append one options-flow history record."""
        self._records.append(deepcopy(dict(record)))

    def list_records(self) -> list[dict[str, Any]]:
        """Return all stored options-flow history records in insertion order."""
        return deepcopy(self._records)
