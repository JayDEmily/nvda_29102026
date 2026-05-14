"""Compatibility wrapper over the benchmark-owned calendar reference importer."""

from __future__ import annotations

from nvda_desk.calendar.reference.importer import (
    FinancialCalendarImporter,
    load_layers,
    load_manifest,
)
from nvda_desk.packets.dmp_packets import build_reference_packet

__all__ = ["FinancialCalendarImporter", "build_reference_packet", "load_layers", "load_manifest"]
