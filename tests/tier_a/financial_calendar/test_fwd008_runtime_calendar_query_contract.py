from __future__ import annotations

from datetime import datetime, timedelta, timezone

from nvda_desk.calendar.operational.events import (
    MarketEventDTO,
    OperationalEventRepository,
    RuntimeCalendarQuery,
)


def test_runtime_calendar_query_filters_symbol_window_and_materiality_without_trade_authority() -> (
    None
):
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
            tags=["earnings"],
            lineage_ids=["calendar-ref-1"],
        )
    )
    repo.create_event(
        MarketEventDTO(
            event_id="macro-spx",
            event_type="macro",
            starts_at=now + timedelta(hours=5),
            symbol="SPX",
            materiality="medium",
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

    assert snapshot.query.symbol == "NVDA"
    assert [match.event.event_id for match in snapshot.matches] == ["earnings-nvda"]
    assert snapshot.matches[0].proximity_seconds == 1200
    assert snapshot.matches[0].materiality_rank == 3
    assert snapshot.lineage_for("earnings-nvda") == ["calendar-ref-1"]
    assert snapshot.decision_authority == "calendar_context_only"
    assert snapshot.candidate_formation_allowed is False
    assert snapshot.capital_sizing_allowed is False
