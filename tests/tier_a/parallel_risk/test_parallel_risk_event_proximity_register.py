from __future__ import annotations

from datetime import datetime, timedelta, timezone

from nvda_desk.calendar.operational.events import (
    MarketEventDTO,
    OperationalEventRepository,
    RuntimeCalendarQuery,
)
from nvda_desk.domain.parallel_risk.event_proximity import (
    event_proximity_entries_from_calendar_snapshot,
)


def test_event_proximity_register_projects_calendar_matches_without_trade_authority() -> None:
    repo = OperationalEventRepository()
    now = datetime(2026, 5, 17, 14, 0, tzinfo=timezone.utc)
    repo.create_event(
        MarketEventDTO(
            event_id="earnings-nvda",
            event_type="earnings",
            starts_at=now + timedelta(minutes=20),
            ends_at=now + timedelta(minutes=40),
            symbol="NVDA",
            materiality="high",
            tags=["earnings", "scheduled_event_window_active"],
            lineage_ids=["calendar-ref-1"],
        )
    )
    snapshot = repo.build_runtime_calendar_snapshot(
        RuntimeCalendarQuery(
            symbol="NVDA",
            window_start_utc=now,
            window_end_utc=now + timedelta(hours=1),
            minimum_materiality="medium",
            observed_at=now,
        )
    )

    entries = event_proximity_entries_from_calendar_snapshot(snapshot)

    assert len(entries) == 1
    entry = entries[0]
    assert entry.event_id == "earnings-nvda"
    assert entry.proximity_seconds == 1200
    assert entry.materiality == "high"
    assert entry.materiality_rank == 3
    assert entry.runtime_tags == ["earnings", "scheduled_event_window_active"]
    assert entry.evaluation_tags == ["earnings", "scheduled_event_window_active"]
    assert entry.source_refs == ["calendar-ref-1"]
    assert entry.risk_interpretation == "event_proximity_state_of_play_only"
    payload = entry.model_dump_json()
    assert "buy" not in payload
    assert "sell" not in payload
    assert "order" not in payload


def test_event_proximity_register_returns_empty_entries_when_no_calendar_matches() -> None:
    repo = OperationalEventRepository()
    now = datetime(2026, 5, 17, 14, 0, tzinfo=timezone.utc)
    snapshot = repo.build_runtime_calendar_snapshot(
        RuntimeCalendarQuery(
            symbol="NVDA",
            window_start_utc=now,
            window_end_utc=now + timedelta(hours=1),
            minimum_materiality="medium",
            observed_at=now,
        )
    )

    assert event_proximity_entries_from_calendar_snapshot(snapshot) == []
