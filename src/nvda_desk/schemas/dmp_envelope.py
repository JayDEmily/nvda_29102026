"""Compatibility wrapper over the canonical DMPV3 envelope contracts."""

from __future__ import annotations

from nvda_desk.contracts.packets import (
    DmpV3Envelope,
    DmpV3Lineage,
    DmpV3Producer,
    DmpV3Summary,
    DmpV3Validation,
    DmpV3ValidationCheck,
    build_dmp_v3_envelope_kwargs,
)

__all__ = [
    "DmpV3Envelope",
    "DmpV3Lineage",
    "DmpV3Producer",
    "DmpV3Summary",
    "DmpV3Validation",
    "DmpV3ValidationCheck",
    "build_dmp_v3_envelope_kwargs",
]
