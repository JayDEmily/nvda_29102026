"""Sequence 7 tests-first proof for the independent parallel-risk envelope output."""

from __future__ import annotations

from datetime import UTC, datetime

from tests.support.dmpv3_current_builder import parallel_risk_compatibility_authority

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import ParallelRiskLanePacket
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput, TemporalEventWindow
from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService


def _sequence7_stage_input_bundle() -> StageInputBundle:
    """Return inputs that should yield a caution envelope but not a trade decision."""

    return StageInputBundle(
        temporal=TemporalContextInput(
            source_time_utc=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
            next_event_time_utc=datetime(2026, 4, 21, 10, 0, tzinfo=UTC),
            windows=[
                TemporalEventWindow(
                    event_id="earnings_window",
                    window_start_utc=datetime(2026, 4, 21, 9, 55, tzinfo=UTC),
                    window_end_utc=datetime(2026, 4, 21, 10, 5, tzinfo=UTC),
                    tags=["earnings", "scheduled_event_window_active"],
                )
            ],
        ),
        regime=MarketRegimeContextInput(
            nvda_return_pct=-1.2,
            nq_return_pct=-0.8,
            vix_level=31.0,
        ),
        options_flow=OptionsFlowContextInput(
            spot_price=101.0,
            front_dte=5,
            next_dte=1,
        ),
    )


def test_sequence7_parallel_risk_output_contains_independent_risk_envelope() -> None:
    """Require a risk-envelope payload with tight/broad/caution/block semantics."""

    packets = ParallelRiskLaneService().run_bootstrap(
        stage_input_bundle=_sequence7_stage_input_bundle(),
        input_packet_id="dmp::parallel_risk::bootstrap_input::sequence7-output",
        output_packet_id="dmp::parallel_risk::output::sequence7-output",
        **parallel_risk_compatibility_authority("sequence7-output"),
    )
    lane_packet = packets["lane_packet"]
    payload = ParallelRiskLanePacket.model_validate(lane_packet.data)
    payload_map = payload.model_dump(mode="json")

    envelope = payload_map["risk_envelope"]
    assert envelope["envelope_state"] == "caution"
    assert envelope["state_ladder"] == ["tight", "broad", "caution", "block"]
    assert envelope["decision_authority"] == "independent_risk_envelope_only"
    assert {item["source_family"] for item in envelope["contributions"]} == {
        "temporal_event_context",
        "options_repricing_context",
        "market_volatility_context",
    }
    assert envelope["hard_blocks"] == []
    assert set(envelope["caution_flags"]) >= {
        "scheduled_event_window_active",
        "front_term_structure_backwardation",
        "vix_elevated",
    }


def test_sequence7_parallel_risk_output_is_not_capital_or_execution_authority() -> None:
    """Assert the envelope cannot silently become sizing, brokerage, or candidate selection."""

    packets = ParallelRiskLaneService().run_bootstrap(
        stage_input_bundle=_sequence7_stage_input_bundle(),
        input_packet_id="dmp::parallel_risk::bootstrap_input::sequence7-forbidden",
        output_packet_id="dmp::parallel_risk::output::sequence7-forbidden",
        **parallel_risk_compatibility_authority("sequence7-forbidden"),
    )
    payload_text = str(
        ParallelRiskLanePacket.model_validate(packets["lane_packet"].data).model_dump(mode="json")
    )

    forbidden_tokens = (
        "authorised_deployable_pct",
        "authorised_notional_usd",
        "position_size",
        "brokerage_order",
        "lead_playbook_id",
        "review_explanation",
        "coefficient_modifier",
    )
    for token in forbidden_tokens:
        assert token not in payload_text
