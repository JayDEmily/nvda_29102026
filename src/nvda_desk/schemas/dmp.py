"""Compatibility wrapper over the canonical DMPV3 packet helpers."""

from __future__ import annotations

from nvda_desk.contracts.packets import DeskModulePacketV3, DmpV3Packet
from nvda_desk.packets.dmp_packets import build_dmp_v3_packet

__all__ = [
    "DeskModulePacketV3",
    "DmpV3Packet",
    "build_dmp_v3_packet",
]
