"""Persist replay, evaluation, and research artefacts outside live trading state."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class ResearchLogsRepository:
    """Append-only repository for bounded research and evaluation artefacts."""

    def __init__(self):
        self._logs: list[dict[str, Any]] = []

    def append_log(self, log: Mapping[str, Any]) -> None:
        self._logs.append(deepcopy(dict(log)))

    def list_logs(self) -> list[dict[str, Any]]:
        return deepcopy(self._logs)
