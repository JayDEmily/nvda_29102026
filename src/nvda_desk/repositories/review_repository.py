"""Persist review packets and lineage records in one bounded in-memory store."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class ReviewRepository:
    """Deterministic in-memory repository for review outputs."""

    def __init__(self):
        self._packets: dict[str, dict[str, Any]] = {}

    def write_packet(self, packet_id: str, packet: Mapping[str, Any]) -> None:
        """Store one review packet by identifier."""

        normalised_id = str(packet_id).strip()
        if not normalised_id:
            raise ValueError("packet_id must be non-empty")
        if normalised_id in self._packets:
            raise ValueError(f"duplicate packet_id: {normalised_id}")
        self._packets[normalised_id] = deepcopy(dict(packet))

    def read_packet(self, packet_id: str) -> dict[str, Any] | None:
        """Return one stored review packet, if present."""

        packet = self._packets.get(str(packet_id).strip())
        return deepcopy(packet) if packet is not None else None

    def list_packets(self) -> list[dict[str, Any]]:
        """Return stored review packets in insertion order."""

        return deepcopy(list(self._packets.values()))
