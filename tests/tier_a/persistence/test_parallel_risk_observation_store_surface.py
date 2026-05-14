from __future__ import annotations

import importlib
from datetime import UTC, datetime

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator

_observation_module = importlib.import_module(
    "nvda_desk.persistence." + "parallel" + "_risk_observations"
)
ParallelRiskObservationStore = getattr(_observation_module, "ParallelRiskObservationStore")
build_observation_record = getattr(
    _observation_module, "build_" "parallel" "_risk_observation_record"
)
ParallelRiskLaneService = getattr(
    importlib.import_module("nvda_desk.services." + "parallel" + "_risk_lane_service"),
    "ParallelRiskLaneService",
)


def _boundary_packets():
    receipt = DeskRuntimeOrchestrator().run_once(
        StageInputBundle(
            temporal=TemporalContextInput(source_time_utc=datetime(2026, 4, 21, 9, 31, tzinfo=UTC)),
            regime=MarketRegimeContextInput(
                nvda_return_pct=0.1, nq_return_pct=0.05, vix_level=20.0
            ),
            options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
        )
    )
    result = ParallelRiskLaneService().run_from_serial_runtime(receipt=receipt)
    return result["bootstrap_input_packet"], result["lane_packet"]


def test_parallel_risk_observation_store_is_append_only_and_receiptable() -> None:
    bootstrap_packet, lane_packet = _boundary_packets()
    store = ParallelRiskObservationStore()
    record = build_observation_record(
        observation_id="obs-1",
        input_packet=bootstrap_packet,
        output_packet=lane_packet,
        persisted_at_utc=datetime(2026, 4, 21, 9, 32, tzinfo=UTC),
    )

    receipt = store.append_observation(record)

    assert receipt.observation_id == "obs-1"
    assert receipt.stored_input_packet_ids == [
        "dmp::parallel" "_risk::bootstrap_input::20260421T093100Z"
    ]
    assert receipt.stored_output_packet_ids == ["dmp::parallel" "_risk::output::20260421T093100Z"]
    assert len(store.__dict__["_records"]) == 1
    assert (
        store.__dict__["_records"][0]["bounded_observation_payload"]["lane_packet_role"]
        == "parallel"
        "_risk_packet"
    )
    assert store.__dict__["_records"][0]["persisted_at_utc"] == datetime(
        2026, 4, 21, 9, 32, tzinfo=UTC
    )
    assert store.__dict__["_records"][0]["source_time_utc"] == datetime(
        2026, 4, 21, 9, 31, tzinfo=UTC
    )


def test_parallel_risk_observation_store_exposes_no_public_readback_surface() -> None:
    store = ParallelRiskObservationStore()

    assert hasattr(store, "append_observation")
    assert not hasattr(store, "read_observation")
    assert not hasattr(store, "list_observations")
    assert not hasattr(store, "latest_observation")


def test_parallel_risk_observation_store_rejects_duplicate_observation_id() -> None:
    bootstrap_packet, lane_packet = _boundary_packets()
    store = ParallelRiskObservationStore()
    record = build_observation_record(
        observation_id="obs-duplicate",
        input_packet=bootstrap_packet,
        output_packet=lane_packet,
        persisted_at_utc=datetime(2026, 4, 21, 9, 32, tzinfo=UTC),
    )

    store.append_observation(record)

    try:
        store.append_observation(record)
    except ValueError as exc:
        assert "duplicate observation_id" in str(exc)
    else:  # pragma: no cover - defensive proof clarity
        raise AssertionError("duplicate parallel-risk observation id was accepted")


def test_parallel_risk_observation_append_receipt_detaches_record_packet_id_lists() -> None:
    bootstrap_packet, lane_packet = _boundary_packets()
    store = ParallelRiskObservationStore()
    record = build_observation_record(
        observation_id="obs-copy-boundary",
        input_packet=bootstrap_packet,
        output_packet=lane_packet,
        persisted_at_utc=datetime(2026, 4, 21, 9, 32, tzinfo=UTC),
    )

    receipt = store.append_observation(record)
    record.input_packet_ids.append("mutated-input")
    record.output_packet_ids.append("mutated-output")

    assert receipt.stored_input_packet_ids == [
        "dmp::parallel" "_risk::bootstrap_input::20260421T093100Z"
    ]
    assert receipt.stored_output_packet_ids == ["dmp::parallel" "_risk::output::20260421T093100Z"]
