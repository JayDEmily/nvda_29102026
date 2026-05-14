"""Persist execution event records separately from review and state reads."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class ExecutionEventRepository:
    """Append-only repository for execution event artefacts."""

    def __init__(self):
        self._events: list[dict[str, Any]] = []

    def append_event(self, event: Mapping[str, Any]) -> None:
        self._events.append(deepcopy(dict(event)))

    def list_events(self) -> list[dict[str, Any]]:
        return deepcopy(self._events)
