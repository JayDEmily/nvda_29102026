from __future__ import annotations

import importlib
from datetime import UTC, datetime

import pytest

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput, TemporalEventWindow
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator

ParallelRiskLaneService = getattr(
    importlib.import_module("nvda_desk.services." + "parallel" + "_risk_lane_service"),
    "ParallelRiskLaneService",
)


def _serial_runtime_receipt() -> dict[str, object]:
    return DeskRuntimeOrchestrator().run_once(
        StageInputBundle(
            temporal=TemporalContextInput(
                source_time_utc=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
                windows=[
                    TemporalEventWindow(
                        event_id="serial_boundary_window",
                        window_start_utc=datetime(2026, 4, 21, 9, 30, tzinfo=UTC),
                        window_end_utc=datetime(2026, 4, 21, 9, 45, tzinfo=UTC),
                        tags=["scheduled_event_window_active"],
                    )
                ],
            ),
            regime=MarketRegimeContextInput(
                nvda_return_pct=0.1, nq_return_pct=0.05, vix_level=20.0
            ),
            options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
        )
    )


def test_parallel_risk_lane_service_runs_serial_runtime_boundary_path_without_hidden_state() -> (
    None
):
    service = ParallelRiskLaneService()
    receipt = _serial_runtime_receipt()

    result = service.run_from_serial_runtime(receipt=receipt)

    temporal_packet_id = receipt["stage_packets"]["temporal"]["id"]
    assert set(result) == {"selected_stage_packets", "bootstrap_input_packet", "lane_packet"}
    assert set(result["selected_stage_packets"]) == {"temporal"}
    assert result["selected_stage_packets"]["temporal"].packet_id == temporal_packet_id
    assert (
        result["bootstrap_input_packet"].packet_id == "dmp::parallel"
        "_risk::bootstrap_input::20260421T093100Z"
    )
    assert result["bootstrap_input_packet"].lineage.parentids == [temporal_packet_id]
    assert result["bootstrap_input_packet"].lineage.dependencyids == [temporal_packet_id]
    assert result["bootstrap_input_packet"].lineage.derivedfrom == (
        "parallel" "_risk_bootstrap_from_serial_runtime_temporal_packet"
    )
    assert (
        result["bootstrap_input_packet"].data.bootstrap_source
        == "serial_runtime.stage_packets.temporal"
    )
    assert [
        window.event_id for window in result["bootstrap_input_packet"].data.temporal_input.windows
    ] == ["serial_boundary_window"]
    assert result["lane_packet"].data.environment_assessment.window_ids == [
        "serial_boundary_window"
    ]
    assert result["lane_packet"].packet_id == "dmp::parallel" "_risk::output::20260421T093100Z"
    assert result["lane_packet"].lineage.parentids == [
        "dmp::parallel" "_risk::bootstrap_input::20260421T093100Z"
    ]
    assert result["lane_packet"].lineage.dependencyids == [
        "dmp::parallel" "_risk::bootstrap_input::20260421T093100Z"
    ]
    assert service.__dict__.keys() == {"_service"}


def test_parallel_risk_lane_service_fails_closed_on_temporal_packet_id_contract_mismatch() -> None:
    service = ParallelRiskLaneService()
    receipt = _serial_runtime_receipt()
    receipt["stage_packets"]["temporal"]["id"] = "dmp::serial::regime::20260421T093100Z"

    with pytest.raises(ValueError, match="serial_runtime_temporal_packet_id_contract_mismatch"):
        service.run_from_serial_runtime(receipt=receipt)


def test_parallel_risk_lane_service_records_serial_temporal_input_trace() -> None:
    service = ParallelRiskLaneService()
    receipt = _serial_runtime_receipt()

    result = service.run_from_serial_runtime(receipt=receipt)

    temporal_packet_id = receipt["stage_packets"]["temporal"]["id"]
    payload = result["lane_packet"].data
    assert payload.input_trace.bootstrap_source == "serial_runtime.stage_packets.temporal"
    assert payload.input_trace.admitted_semantic_inputs == ["temporal_input"]
    assert payload.input_trace.selected_stage_packet_ids == [temporal_packet_id]
    assert (
        payload.input_trace.bootstrap_input_packet_id == result["bootstrap_input_packet"].packet_id
    )
    assert payload.input_trace.parent_packet_ids == [temporal_packet_id]
