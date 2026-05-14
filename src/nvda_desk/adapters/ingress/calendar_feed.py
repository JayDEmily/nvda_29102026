"""Adapt calendar reference payloads into native reference-data contracts."""

from __future__ import annotations

from typing import Any, Mapping

from nvda_desk.calendar.reference.importer import load_manifest


def adapt_calendar_manifest(payload: Mapping[str, Any]):
    """Return one imported reference bundle from a calendar manifest payload."""
    return load_manifest(payload)
