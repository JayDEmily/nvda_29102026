"""Pure temporal event-window tagging helpers."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from nvda_desk.contracts.temporal import TemporalEventWindow


def active_window_tags(
    source_time_utc: datetime, windows: Iterable[TemporalEventWindow]
) -> list[str]:
    """Return sorted unique tags for windows active at the source observation time."""

    tags: set[str] = set()
    for window in windows:
        if window.window_start_utc <= source_time_utc <= window.window_end_utc:
            tags.update(window.tags)
    return sorted(tags)


def next_event_time_utc(
    source_time_utc: datetime, windows: Iterable[TemporalEventWindow]
) -> datetime | None:
    """Return the earliest future window start after the source observation time."""

    future_starts = [
        window.window_start_utc for window in windows if window.window_start_utc > source_time_utc
    ]
    return min(future_starts) if future_starts else None
