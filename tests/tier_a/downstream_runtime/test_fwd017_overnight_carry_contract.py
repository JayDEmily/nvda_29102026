from __future__ import annotations

from nvda_desk.api.app import create_app
from nvda_desk.contracts.exit_close import ExitCloseInputTrace
from nvda_desk.downstream.exit_close import evaluate_exit_close_policy
from nvda_desk.downstream.overnight_carry import (
    CarryHandoffService,
    OvernightCarryMarketService,
    OvernightCarryReplayService,
)


def _trace() -> ExitCloseInputTrace:
    return ExitCloseInputTrace(
        live_inventory_receipt_id="inventory-1",
        position_id="position-1",
        placement_readiness_id="placement-1",
        capital_deployment_receipt_id="capital-1",
        parallel_risk_packet_id="risk-1",
        close_policy_id="close-policy-1",
    )


def test_carry_handoff_builds_lifecycle_limited_action_envelope_with_open_fallback() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="trim",
        trigger_ids=("close-risk",),
        decision_id="decision-1",
    )

    handoff = CarryHandoffService().build_carry_handoff(
        decision=decision,
        horizon="overnight",
        lifecycle_ceiling="trim",
        next_session_open_utc=None,
        configured_next_session_open_utc="2026-05-18T13:30:00Z",
    )

    assert handoff.position_id == "position-1"
    assert handoff.horizon == "overnight"
    assert handoff.allowed_actions == ("hold", "trim")
    assert handoff.next_session_open_utc == "2026-05-18T13:30:00Z"
    assert handoff.execution_allowed is False


def test_market_carry_evaluation_applies_handoff_envelope_and_derives_vwap_distance() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="trim",
        trigger_ids=("close-risk",),
    )
    handoff = CarryHandoffService().build_carry_handoff(decision=decision, horizon="overnight")

    output = OvernightCarryMarketService().evaluate_from_market(
        evaluation_id="carry-1",
        market_state={
            "symbol": "NVDA",
            "latest_close": 126.0,
            "session_vwap": 120.0,
            "vix_close": 22.0,
            "vvix_close": 90.0,
        },
        handoff=handoff,
    )

    assert output.recommendation == "trim"
    assert output.close_distance_to_vwap_pct == 5.0
    assert output.scalar_context["vix_close"] == 22.0
    assert output.execution_allowed is False


def test_carry_replay_compares_market_evaluation_against_next_session_reference() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(), requested_action="hold", decision_id="decision-hold"
    )
    handoff = CarryHandoffService().build_carry_handoff(decision=decision, horizon="overnight")
    evaluation = OvernightCarryMarketService().evaluate_from_market(
        evaluation_id="carry-2",
        market_state={"symbol": "NVDA", "latest_close": 100.0, "session_vwap": 100.0},
        handoff=handoff,
    )

    replay = OvernightCarryReplayService().replay_evaluation(
        replay_id="replay-1",
        evaluation=evaluation,
        next_session_reference={"open_price": 103.0, "close_price": 101.0},
    )

    assert replay.path_summary["open_gap_pct"] == 3.0
    assert replay.path_summary["close_to_close_pct"] == 1.0
    assert replay.runtime_mutated is False


def test_api_exposes_overnight_carry_dependency_surfaces() -> None:
    app = create_app()
    expected = {
        "evaluate_overnight_carry",
        "evaluate_overnight_carry_from_market",
        "record_overnight_carry_evaluation",
        "record_overnight_carry_market_evaluation",
        "replay_overnight_carry_from_market",
        "get_overnight_verdict_and_score",
    }
    assert expected.issubset(app.route_handlers)

    result = app.evaluate_overnight_carry_from_market(
        {
            "evaluation_id": "api-carry-1",
            "position_id": "position-1",
            "requested_action": "hold",
            "market_state": {"symbol": "NVDA", "latest_close": 100, "session_vwap": 99},
        }
    )
    assert result["recommendation"] in {"hold", "trim", "close"}
    assert result["execution_allowed"] is False
