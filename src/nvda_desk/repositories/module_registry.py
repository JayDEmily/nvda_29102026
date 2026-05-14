"""Persist module promotion and registry state."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class ModuleRegistryRepository:
    """Key-value repository for governance module registry records."""

    def __init__(self):
        self._records: dict[str, dict[str, Any]] = {}

    def write_record(self, module_id: str, record: Mapping[str, Any]) -> None:
        module_key = str(module_id).strip()
        if not module_key:
            raise ValueError("module_id must be non-empty")
        if module_key in self._records:
            raise ValueError(f"duplicate module_id {module_key!r}")
        self._records[module_key] = deepcopy(dict(record))

    def read_record(self, module_id: str) -> dict[str, Any] | None:
        record = self._records.get(str(module_id))
        return deepcopy(record) if record is not None else None
