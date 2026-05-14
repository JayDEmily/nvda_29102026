"""Persist raw market observations without mixing them with trade state."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class MarketObservationRepository:
    """Append-only repository for raw market observations."""

    def __init__(self):
        self._rows: list[dict[str, Any]] = []

    def append_observation(self, row: Mapping[str, Any]) -> None:
        self._rows.append(deepcopy(dict(row)))

    def list_observations(self) -> list[dict[str, Any]]:
        return deepcopy(self._rows)
