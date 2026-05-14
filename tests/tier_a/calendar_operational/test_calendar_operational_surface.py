from __future__ import annotations

import importlib
from dataclasses import is_dataclass

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_calendar_operational_surfaces_are_present() -> None:
    operational = _require_module("nvda_desk.calendar.operational.events")
    assert operational.__name__ == "nvda_desk.calendar.operational.events"

    for attr_name in (
        "MarketEventDTO",
        "SessionCalendarDTO",
        "OperationalEventRepository",
        "OperationalSessionRepository",
    ):
        assert _require_attr(operational, attr_name) is getattr(operational, attr_name)


def test_calendar_operational_repositories_preserve_crud_separation() -> None:
    operational = _require_module("nvda_desk.calendar.operational.events")
    assert operational.__name__ == "nvda_desk.calendar.operational.events"

    market_event = _require_attr(operational, "MarketEventDTO")
    assert market_event is getattr(operational, "MarketEventDTO")
    session_dto = _require_attr(operational, "SessionCalendarDTO")
    assert session_dto is getattr(operational, "SessionCalendarDTO")
    event_repo = _require_attr(operational, "OperationalEventRepository")()
    session_repo = _require_attr(operational, "OperationalSessionRepository")()

    assert is_dataclass(market_event)
    assert is_dataclass(session_dto)

    event = event_repo.create_event(
        market_event(event_id="evt-1", event_type="market_holiday", tags=["venue_holiday"])
    )
    session = session_repo.create_session(
        session_dto(session_id="sess-1", trade_date="2026-04-20", session_state="holiday")
    )

    assert [item.event_id for item in event_repo.list_events()] == [event.event_id]
    assert [item.session_id for item in session_repo.list_sessions()] == [session.session_id]
