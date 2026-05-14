"""Translate prepared runtime snapshots into temporal contracts."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Mapping

from nvda_desk.contracts.temporal import (
    TemporalContextInput,
    TemporalEventWindow,
    build_source_temporal_payload,
)


def build_temporal_input(snapshot: Mapping[str, Any]) -> TemporalContextInput:
    """Return one typed temporal input from a prepared runtime snapshot mapping."""

    source_time_utc = _optional_datetime(snapshot, "source_time_utc")
    source_date = _optional_date(snapshot, "source_date")
    if source_time_utc is None and source_date is None:
        raise ValueError(
            "Prepared snapshot is missing required source temporal truth: source_time_utc or source_date."
        )
    next_event_time_utc = _optional_datetime(snapshot, "next_event_time_utc")
    raw_windows = snapshot.get("windows")
    if raw_windows is None:
        raw_windows = []
    if not isinstance(raw_windows, list):
        raise TypeError("Prepared snapshot field 'windows' must be a list when present.")
    windows = [
        TemporalEventWindow(
            event_id=str(item["event_id"]),
            window_start_utc=item["window_start_utc"],
            window_end_utc=item["window_end_utc"],
            tags=list(item.get("tags", [])),
        )
        for item in raw_windows
    ]
    temporal_payload = build_source_temporal_payload(
        source_time_utc=source_time_utc,
        source_date=source_date,
        source_time_raw=_optional_str(snapshot, "source_time_raw"),
        source_time_kind=_optional_str(snapshot, "source_time_kind"),
        source_timezone_raw=_optional_str(snapshot, "source_timezone_raw"),
        captured_at_utc=_optional_datetime(snapshot, "captured_at_utc"),
        persisted_at_utc=_optional_datetime(snapshot, "persisted_at_utc"),
        source_provider=_optional_str(snapshot, "source_provider"),
        source_channel=_optional_str(snapshot, "source_channel"),
        time_granularity=_optional_str(snapshot, "time_granularity"),
    )
    return TemporalContextInput(
        **temporal_payload,
        next_event_time_utc=next_event_time_utc,
        windows=windows,
    )


def _optional_datetime(snapshot: Mapping[str, Any], key: str) -> datetime | None:
    value = snapshot.get(key)
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    raise TypeError(f"Prepared snapshot field '{key}' must be a datetime when present.")


def _optional_date(snapshot: Mapping[str, Any], key: str) -> date | None:
    value = snapshot.get(key)
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    raise TypeError(f"Prepared snapshot field '{key}' must be a date when present.")


def _optional_str(snapshot: Mapping[str, Any], key: str) -> str | None:
    value = snapshot.get(key)
    if value is None:
        return None
    if isinstance(value, str):
        return value
    raise TypeError(f"Prepared snapshot field '{key}' must be a string when present.")
