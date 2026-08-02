from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.api.app import create_app
from nvda_desk.api.deps import (
    get_events_service,
    get_execution_records_service,
    get_market_state_service,
    get_module_registry_service,
    get_session_clock_classifier,
    get_settings_cached,
)


def test_api_dependency_graph_exposes_cached_internal_services_without_owning_domain_logic() -> (
    None
):
    assert get_settings_cached() is get_settings_cached()
    assert get_session_clock_classifier()(datetime(2026, 5, 15, 14, 0, tzinfo=UTC)) in {
        "pre_open",
        "opening",
        "mid_session",
        "closing",
        "post_close",
    }
    assert get_market_state_service() is get_market_state_service()
    assert get_module_registry_service() is get_module_registry_service()
    assert get_events_service() is get_events_service()
    assert get_execution_records_service() is get_execution_records_service()


def test_api_app_registers_internal_exposure_routes_and_stateful_crud_surfaces() -> None:
    app = create_app()
    expected_routes = {
        "create_market_event",
        "create_module_spec",
        "create_session_calendar",
        "get_coefficient_group",
        "get_runtime_settings",
        "get_strategy_variant",
        "list_coefficients",
        "list_market_events",
        "list_module_specs",
        "list_session_calendars",
        "list_strategy_variants",
        "market_intraday",
        "market_option_surface",
        "market_session_clock",
        "market_snapshot",
        "market_temporal_state",
        "record_strategic_ladder_evaluation",
        "replay_session_phases",
        "replay_strategic_ladder_from_market",
    }
    assert expected_routes.issubset(app.route_handlers)

    session = app.create_session_calendar(
        {"session_id": "s1", "trade_date": "2026-05-15", "session_state": "regular"}
    )
    event = app.create_market_event({"event_id": "e1", "event_type": "earnings"})
    module = app.create_module_spec("module-a", {"status": "candidate"})

    assert session["session_id"] == "s1"
    assert event["event_id"] == "e1"
    assert module["module_id"] == "module-a"
    assert app.list_session_calendars()[0]["session_id"] == "s1"
    assert app.list_market_events()[0]["event_id"] == "e1"
    assert app.list_module_specs()[0]["module_id"] == "module-a"


def test_api_app_exposes_replay_evaluation_without_untyped_authority_event_state() -> None:
    app = create_app()

    assert "paths" in app.get_runtime_settings()
    assert isinstance(app.list_coefficients(), list)
    assert app.get_coefficient_group("posture")["owner_stage"] == "posture"
    assert isinstance(app.list_strategy_variants(), list)
    assert app.get_strategy_variant(app.list_strategy_variants()[0]["playbook_id"])["playbook_id"]

    removed_authority_methods = {
        "record_veto_event",
        "list_veto_events",
        "record_risk_block_event",
        "list_risk_block_events",
    }
    assert removed_authority_methods.isdisjoint(app.route_handlers)
    assert all(not hasattr(app, method_name) for method_name in removed_authority_methods)
    assert not hasattr(app, "_veto_events")
    assert not hasattr(app, "_risk_block_events")

    replay = app.replay_strategic_ladder_from_market([{"candidate_id": "a", "score": "0.25"}])
    assert replay["best_stack_id"] == "a"
    assert app.record_strategic_ladder_evaluation("eval-1", {"score": 1})["run_id"] == "eval-1"
    assert app.replay_session_phases(["pre_open", "opening"])["phases"] == ["pre_open", "opening"]
