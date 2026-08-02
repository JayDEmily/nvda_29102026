from __future__ import annotations

from datetime import UTC, datetime

import pytest
from tests.support.dmpv3_current_builder import parallel_risk_compatibility_authority

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import ParallelRiskLanePacket
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput, TemporalEventWindow
from nvda_desk.risk.parallel.evaluate import (
    ParallelRiskService,
    enrich_candidate_semantics,
    enrich_market_translation,
    evaluate_parallel_risk,
)


def _bundle() -> StageInputBundle:
    return StageInputBundle(
        temporal=TemporalContextInput(
            source_time_utc=datetime(2026, 4, 21, 9, 31),
            next_event_time_utc=datetime(2026, 4, 21, 10, 0),
            windows=[
                TemporalEventWindow(
                    event_id="earnings",
                    window_start_utc=datetime(2026, 4, 21, 9, 55),
                    window_end_utc=datetime(2026, 4, 21, 10, 5),
                    tags=["earnings", "high-vol"],
                )
            ],
        ),
        regime=MarketRegimeContextInput(vix_level=19.0),
        options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
    )


def test_parallel_risk_evaluation_surface_emits_lawful_bootstrap_output_packet() -> None:
    service = ParallelRiskService()
    bootstrap_packet = service.build_bootstrap_input_packet(
        stage_input_bundle=_bundle(),
        packet_id="bootstrap-1",
        **parallel_risk_compatibility_authority(
            "evaluation-1",
            emitted_at=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
        ),
    )

    lane_packet = evaluate_parallel_risk(
        preparation_packet=bootstrap_packet,
        output_packet_id="parallel-risk-1",
    )

    payload = ParallelRiskLanePacket.model_validate(lane_packet.data)
    assert lane_packet.packetrole == "parallel_risk_packet"
    assert lane_packet.lineage.parentids == ["bootstrap-1"]
    assert lane_packet.lineage.dependencyids == ["bootstrap-1"]
    assert payload.environment_assessment.window_ids == ["earnings"]
    assert payload.environment_assessment.window_tags == ["earnings", "high-vol"]
    assert payload.environment_assessment.source_time_utc == datetime(2026, 4, 21, 9, 31)
    assert payload.environment_assessment.next_event_time_utc == datetime(2026, 4, 21, 10, 0)
    assert payload.stage_read_state[0].state == "bootstrap_input_used"
    assert payload.notes[-2:] == [
        "stage_b_reserved_without_lawful_upstream_packets",
        "stage_c_reserved_without_lawful_upstream_packets",
    ]


def test_parallel_risk_stage_b_reserved_and_stage_c_candidate_semantics_is_audit_only() -> None:
    service = ParallelRiskService()
    bootstrap_packet = service.build_bootstrap_input_packet(
        stage_input_bundle=_bundle(),
        packet_id="bootstrap-2",
        **parallel_risk_compatibility_authority(
            "evaluation-2",
            emitted_at=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
        ),
    )

    with pytest.raises(NotImplementedError, match="Stage B market translation remains reserved"):
        enrich_market_translation(preparation_packet=bootstrap_packet)

    audit = enrich_candidate_semantics(candidate_id="candidate-1", semantic_tags=["swing"])
    assert audit.candidate_id == "candidate-1"
    assert audit.audit_state == "candidate_present"
    assert audit.decision_authority == "parallel_risk_candidate_audit_only"
    assert audit.capital_sizing_allowed is False


def test_parallel_risk_output_records_lawful_input_trace() -> None:
    service = ParallelRiskService()
    bootstrap_packet = service.build_bootstrap_input_packet(
        stage_input_bundle=_bundle(),
        packet_id="bootstrap-trace-1",
        **parallel_risk_compatibility_authority(
            "input-trace",
            emitted_at=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
        ),
    )

    lane_packet = evaluate_parallel_risk(
        preparation_packet=bootstrap_packet,
        output_packet_id="parallel-risk-trace-1",
    )

    payload = ParallelRiskLanePacket.model_validate(lane_packet.data)
    assert payload.input_trace.bootstrap_input_packet_id == "bootstrap-trace-1"
    assert payload.input_trace.bootstrap_source == "stage_input_bundle.parallel_risk_primitives"
    assert payload.input_trace.admitted_semantic_inputs == [
        "temporal_input",
        "regime_input",
        "options_flow_input",
    ]
    assert payload.input_trace.forbidden_authority_keys_consumed == []
    assert payload.input_trace.decision_authority == "parallel_risk_input_trace_only"


def test_parallel_risk_hidden_capital_authority_is_rejected_from_extensions() -> None:
    service = ParallelRiskService()
    bootstrap_packet = service.build_bootstrap_input_packet(
        stage_input_bundle=_bundle(),
        packet_id="bootstrap-hidden-authority",
        **parallel_risk_compatibility_authority(
            "hidden-authority",
            emitted_at=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
        ),
        dmpextensions={
            "nvda": {
                "capital": {
                    "authorised_notional_usd": 1000.0,
                }
            }
        },
    )

    with pytest.raises(ValueError, match="parallel_risk_hidden_authority_key_rejected"):
        evaluate_parallel_risk(
            preparation_packet=bootstrap_packet,
            output_packet_id="parallel-risk-hidden-authority",
        )


def test_parallel_risk_extreme_volatility_emits_block_without_capital_authority() -> None:
    service = ParallelRiskService()
    bundle = _bundle()
    bundle.regime.vix_level = 51.0
    bootstrap_packet = service.build_bootstrap_input_packet(
        stage_input_bundle=bundle,
        packet_id="bootstrap-block-1",
        **parallel_risk_compatibility_authority(
            "block-1",
            emitted_at=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
        ),
    )

    lane_packet = evaluate_parallel_risk(
        preparation_packet=bootstrap_packet,
        output_packet_id="parallel-risk-block-1",
    )

    payload = ParallelRiskLanePacket.model_validate(lane_packet.data)
    assert payload.risk_envelope.envelope_state == "block"
    assert payload.risk_envelope.hard_blocks == ["vix_extreme"]
    assert payload.risk_envelope.decision_authority == "independent_risk_envelope_only"
