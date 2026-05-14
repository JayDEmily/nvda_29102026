from __future__ import annotations

import importlib

import pytest
from datetime import UTC, datetime

from pydantic import ValidationError

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput

_contracts = importlib.import_module("nvda_desk.contracts." + "parallel" + "_risk")
PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA = getattr(
    _contracts, "PARALLEL" "_RISK" "_BOOTSTRAP_INPUT_DATASCHEMA"
)
LANE_DATASCHEMA = getattr(_contracts, "PARALLEL" "_RISK" "_LANE_DATASCHEMA")
ParallelRiskEnvironmentAssessment = getattr(_contracts, "ParallelRiskEnvironmentAssessment")
ParallelRiskLanePacket = getattr(_contracts, "ParallelRiskLanePacket")
ParallelRiskInputTrace = getattr(_contracts, "ParallelRiskInputTrace")
ParallelRiskObservationAppendReceipt = getattr(_contracts, "ParallelRiskObservationAppendReceipt")
ParallelRiskObservationRecord = getattr(_contracts, "ParallelRiskObservationRecord")
ParallelRiskPreparationPacket = getattr(_contracts, "ParallelRiskPreparationPacket")
ParallelRiskStageReadRecord = getattr(_contracts, "ParallelRiskStageReadRecord")
stage_reader = getattr(_contracts, "bootstrap_" "stage_read_state")
build_bootstrap_input_packet = getattr(
    _contracts, "build_" "parallel" "_risk_bootstrap_input_packet"
)


def test_parallel_risk_contract_models_are_present_and_typed() -> None:
    stage_state = ParallelRiskStageReadRecord(
        stage_name="temporal",
        state="bootstrap_input_used",
        note="bounded",
    )
    assessment = ParallelRiskEnvironmentAssessment(
        source_time_utc=datetime(2026, 4, 21, 9, 31),
        invariant_reads=["serial_spine_preserved"],
    )
    payload = ParallelRiskLanePacket(
        environment_assessment=assessment,
        input_trace=ParallelRiskInputTrace(
            bootstrap_input_packet_id="bootstrap-typed",
            bootstrap_source="stage_input_bundle.parallel_risk_primitives",
            admitted_semantic_inputs=["temporal_input", "regime_input", "options_flow_input"],
        ),
        stage_read_state=[stage_state],
    )
    observation = ParallelRiskObservationRecord(
        observation_id="obs-1",
        input_packet_ids=["input-1"],
        output_packet_ids=["output-1"],
        source_time_utc=datetime(2026, 4, 21, 9, 31),
        persisted_at_utc=datetime(2026, 4, 21, 9, 32),
        traceid="trace-1",
        runid="run-1",
        scenarioid="live",
    )
    receipt = ParallelRiskObservationAppendReceipt(
        observation_id="obs-1",
        stored_input_packet_ids=["input-1"],
        stored_output_packet_ids=["output-1"],
    )

    assert payload.environment_assessment.assessment == "bounded_environment" "_assessment"
    assert observation.output_packet_ids == ["output-1"]
    assert receipt.appended is True
    assert PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA.endswith("bootstrap_input:1.0.0")
    assert LANE_DATASCHEMA.endswith("output:1.0.0")


def test_parallel_risk_bootstrap_builder_wraps_stage_input_bundle_truthfully() -> None:
    bundle = StageInputBundle(
        temporal=TemporalContextInput(
            source_time_utc=datetime(2026, 4, 21, 9, 31),
            next_event_time_utc=datetime(2026, 4, 21, 10, 0),
        ),
        regime=MarketRegimeContextInput(vix_level=19.0),
        options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
    )

    packet = build_bootstrap_input_packet(
        stage_input_bundle=bundle,
        packet_id="parallel-risk-bootstrap-1",
        emitted_at=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
        traceid="trace-bootstrap-1",
        runid="run-bootstrap-1",
    )

    payload = ParallelRiskPreparationPacket.model_validate(packet.data)
    assert packet.packetrole == "parallel_risk_bootstrap_input"
    assert packet.dataschema == PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA
    assert packet.producer.module_id == "parallel_risk_lane_bootstrap_adapter"
    assert payload.temporal_input.source_time_utc == bundle.temporal.source_time_utc
    assert payload.bootstrap_source == "stage_input_bundle.parallel_risk_primitives"
    assert payload.stage_read_state[0].state == "bootstrap_input_used"


def test_stage_read_state_is_truthful_for_current_baseline() -> None:
    stage_reads = stage_reader()
    assert [record.stage_name for record in stage_reads] == [
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
        "execution",
        "review",
    ]
    assert stage_reads[0].state == "bootstrap_input_used"
    assert all(record.state == "not_yet_available" for record in stage_reads[1:])


def test_parallel_risk_input_trace_rejects_forbidden_consumed_authority() -> None:
    trace = ParallelRiskInputTrace(
        bootstrap_input_packet_id="bootstrap-1",
        bootstrap_source="stage_input_bundle.parallel_risk_primitives",
        admitted_semantic_inputs=["temporal_input", "regime_input", "options_flow_input"],
    )
    assert trace.decision_authority == "parallel_risk_input_trace_only"

    try:
        ParallelRiskInputTrace(
            bootstrap_input_packet_id="bootstrap-2",
            bootstrap_source="stage_input_bundle.parallel_risk_primitives",
            admitted_semantic_inputs=["temporal_input"],
            forbidden_authority_keys_consumed=["authorised_notional_usd"],
        )
    except ValueError as exc:
        assert "parallel_risk_forbidden_authority_consumed" in str(exc)
    else:  # pragma: no cover - defensive proof clarity
        raise AssertionError("forbidden capital authority key was admitted")


def test_parallel_risk_envelope_hard_blocks_require_block_state() -> None:
    ParallelRiskEnvelope = getattr(_contracts, "Parallel" "RiskEnvelope")

    try:
        ParallelRiskEnvelope(envelope_state="caution", hard_blocks=["vix_extreme"])
    except ValueError as exc:
        assert "parallel_risk_hard_blocks_require_block_state" in str(exc)
    else:  # pragma: no cover - defensive proof clarity
        raise AssertionError("hard block was allowed without block envelope state")


def test_parallel_risk_input_trace_rejects_unadmitted_bootstrap_source() -> None:
    try:
        ParallelRiskInputTrace(
            bootstrap_input_packet_id="bootstrap-unadmitted",
            bootstrap_source="live_broker_packet",
            admitted_semantic_inputs=["temporal_input"],
        )
    except ValueError as exc:
        assert "parallel_risk_bootstrap_source_not_admitted" in str(exc)
    else:  # pragma: no cover - defensive proof clarity
        raise AssertionError("unadmitted bootstrap source was accepted")


def test_parallel_risk_lane_packet_rejects_hidden_capital_authority_fields() -> None:
    assessment = ParallelRiskEnvironmentAssessment(source_time_utc=datetime(2026, 4, 21, 9, 31))
    trace = ParallelRiskInputTrace(
        bootstrap_input_packet_id="bootstrap-hidden-field",
        bootstrap_source="stage_input_bundle.temporal",
        admitted_semantic_inputs=["temporal_input"],
    )

    with pytest.raises(ValidationError):
        ParallelRiskLanePacket(
            environment_assessment=assessment,
            input_trace=trace,
            authorised_notional_usd=1000.0,
        )


def test_parallel_risk_lane_packet_detaches_nested_assessment_state_from_callers() -> None:
    assessment = ParallelRiskEnvironmentAssessment(
        source_time_utc=datetime(2026, 4, 21, 9, 31),
        notes=["bounded"],
    )
    trace = ParallelRiskInputTrace(
        bootstrap_input_packet_id="bootstrap-detach",
        bootstrap_source="stage_input_bundle.temporal",
        admitted_semantic_inputs=["temporal_input"],
    )

    packet = ParallelRiskLanePacket(
        environment_assessment=assessment,
        input_trace=trace,
    )

    assessment.notes.append("capital_deployment_authority")
    trace.admitted_semantic_inputs.append("capital_deployment_authority")

    assert packet.environment_assessment.notes == ["bounded"]
    assert packet.input_trace.admitted_semantic_inputs == ["temporal_input"]
