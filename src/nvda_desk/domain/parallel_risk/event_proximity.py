"""Calendar event-proximity projection for Parallel Risk Lane profiles."""

from __future__ import annotations

from nvda_desk.calendar.operational.events import RuntimeCalendarSnapshot
from nvda_desk.contracts.parallel_risk import EventProximityRegisterEntry


def event_proximity_entries_from_calendar_snapshot(
    snapshot: RuntimeCalendarSnapshot,
) -> list[EventProximityRegisterEntry]:
    """Return descriptive event proximity entries from a context-only calendar snapshot."""

    entries: list[EventProximityRegisterEntry] = []
    for match in snapshot.matches:
        event = match.event
        tags = sorted(event.tags)
        entries.append(
            EventProximityRegisterEntry(
                event_id=event.event_id,
                event_type=event.event_type,
                starts_at_utc=event.starts_at,
                ends_at_utc=event.ends_at,
                proximity_seconds=match.proximity_seconds,
                materiality=event.materiality,
                materiality_rank=match.materiality_rank,
                runtime_tags=tags,
                evaluation_tags=tags,
                risk_interpretation="event_proximity_state_of_play_only",
                source_refs=list(event.lineage_ids),
            )
        )
    return entries
