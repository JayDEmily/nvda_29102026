"""Sequence 7 tests-first proof for parallel-risk input packet alignment."""

from __future__ import annotations

from datetime import UTC, datetime

from tests.support.dmpv3_current_builder import parallel_risk_compatibility_authority

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import ParallelRiskPreparationPacket
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput, TemporalEventWindow
from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService


def _sequence7_stage_input_bundle() -> StageInputBundle:
    """Return a bounded input bundle with temporal, options, and volatility context."""

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


def test_sequence7_bootstrap_input_carries_all_allowed_parallel_risk_primitives() -> None:
    """Require temporal, options-flow, and volatility/regime primitives at the risk lane seam."""

    bootstrap_packet = ParallelRiskLaneService().build_bootstrap_input_packet(
        stage_input_bundle=_sequence7_stage_input_bundle(),
        packet_id="dmp::parallel_risk::bootstrap_input::sequence7",
        **parallel_risk_compatibility_authority("sequence7-input"),
    )

    payload = ParallelRiskPreparationPacket.model_validate(bootstrap_packet.data)
    payload_map = payload.model_dump(mode="json")

    assert payload_map["temporal_input"]["next_event_time_utc"] is not None
    assert payload_map["regime_input"]["vix_level"] == 31.0
    assert payload_map["options_flow_input"]["front_dte"] == 5
    assert payload_map["options_flow_input"]["next_dte"] == 1
    assert payload_map["bootstrap_source"] == "stage_input_bundle.parallel_risk_primitives"


def test_sequence7_bootstrap_input_excludes_downstream_decision_authority() -> None:
    """Keep capital, sizing, brokerage, candidate-selection, and review authority out of input."""

    bootstrap_packet = ParallelRiskLaneService().build_bootstrap_input_packet(
        stage_input_bundle=_sequence7_stage_input_bundle(),
        packet_id="dmp::parallel_risk::bootstrap_input::sequence7-boundary",
        **parallel_risk_compatibility_authority("sequence7-boundary"),
    )
    payload_text = str(
        ParallelRiskPreparationPacket.model_validate(bootstrap_packet.data).model_dump()
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
