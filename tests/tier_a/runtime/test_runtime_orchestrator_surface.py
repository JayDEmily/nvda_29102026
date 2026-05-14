from __future__ import annotations

import importlib
from datetime import UTC, datetime

import pytest

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_runtime_orchestrator_surface_is_present() -> None:
    runtime = _require_module("nvda_desk.runtime.orchestrator")
    assert runtime.__name__ == "nvda_desk.runtime.orchestrator"
    assert _require_attr(runtime, "DeskRuntimeOrchestrator") is getattr(runtime, "DeskRuntimeOrchestrator")


def test_runtime_orchestrator_executes_the_admitted_six_stage_serial_path_from_stage_input_bundle() -> (
    None
):
    runtime = _require_module("nvda_desk.runtime.orchestrator")
    assert runtime.__name__ == "nvda_desk.runtime.orchestrator"
    orchestrator = _require_attr(runtime, "DeskRuntimeOrchestrator")()

    receipt = orchestrator.run_once(
        StageInputBundle(
            temporal=TemporalContextInput(
                source_time_utc=datetime(2026, 4, 21, 13, 31, tzinfo=UTC),
                source_timezone_raw="America/New_York",
            ),
            regime=MarketRegimeContextInput(
                nvda_return_pct=0.1,
                nq_return_pct=0.05,
                vix_level=20.0,
            ),
            options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
        )
    )

    assert receipt["stage_order"] == [
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
        "execution",
    ]
    assert receipt["executed_stages"] == receipt["stage_order"]
    assert receipt["missing_stages"] == []
    assert list(receipt["stage_outputs"]) == receipt["stage_order"]
    assert list(receipt["stage_packet_ids"]) == receipt["stage_order"]
    assert list(receipt["stage_packets"]) == receipt["stage_order"]
    assert receipt["stage_dependencies"] == {
        "temporal": [],
        "regime": [],
        "options_flow": [],
        "posture": ["regime"],
        "eligibility": ["posture"],
        "execution": ["temporal", "regime", "options_flow", "posture", "eligibility"],
    }
    assert receipt["stage_outputs"]["temporal"]["source_time_utc"] == "2026-04-21T13:31:00Z"
    assert receipt["stage_outputs"]["temporal"]["source_timezone_raw"] == "America/New_York"
    assert receipt["stage_outputs"]["temporal"]["session_state"] == "opening"
    assert receipt["stage_outputs"]["posture"]["permission_state"] == "allow"
    assert receipt["stage_outputs"]["eligibility"]["active_family_ids"] == []
    assert receipt["stage_outputs"]["execution"]["scaling_plan"] == ["stand_down"]
    assert (
        receipt["stage_local_handoff"]["execution_post_modifier_pre_final_risk"]
        == receipt["stage_outputs"]["execution"]
    )


def test_runtime_orchestrator_remains_stateless_and_keeps_partial_mapping_fallback() -> None:
    runtime = _require_module("nvda_desk.runtime.orchestrator")
    assert runtime.__name__ == "nvda_desk.runtime.orchestrator"
    orchestrator = _require_attr(runtime, "DeskRuntimeOrchestrator")()

    assert orchestrator.__dict__ == {}
    receipt = orchestrator.run_once({"temporal": {"source_time_utc": "2026-04-21T09:31:00"}})
    assert orchestrator.__dict__ == {}
    assert receipt["executed_stages"] == ["temporal"]
    assert receipt["missing_stages"] == [
        "regime",
        "options_flow",
        "posture",
        "eligibility",
        "execution",
    ]


def test_runtime_orchestrator_does_not_treat_utc_wall_clock_as_us_market_opening() -> None:
    runtime = _require_module("nvda_desk.runtime.orchestrator")
    assert runtime.__name__ == "nvda_desk.runtime.orchestrator"
    orchestrator = _require_attr(runtime, "DeskRuntimeOrchestrator")()

    receipt = orchestrator.run_once(
        StageInputBundle(
            temporal=TemporalContextInput(
                source_time_utc=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
                source_timezone_raw="America/New_York",
            ),
            regime=MarketRegimeContextInput(
                nvda_return_pct=0.1,
                nq_return_pct=0.05,
                vix_level=20.0,
            ),
            options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
        )
    )

    assert receipt["stage_outputs"]["temporal"]["source_time_utc"] == "2026-04-21T09:31:00Z"
    assert receipt["stage_outputs"]["temporal"]["source_timezone_raw"] == "America/New_York"
    assert receipt["stage_outputs"]["temporal"]["session_state"] == "pre_open"


def test_runtime_orchestrator_can_attach_live_inventory_snapshot_without_changing_serial_decision() -> None:
    from nvda_desk.downstream.live_inventory import DownstreamLiveInventoryService
    from nvda_desk.repositories.position_repository import PositionRepository

    runtime = _require_module("nvda_desk.runtime.orchestrator")
    orchestrator = _require_attr(runtime, "DeskRuntimeOrchestrator")()
    positions = PositionRepository()
    positions.write_position("pos-1", {"symbol": "NVDA", "declared_exposure": 10.0})

    receipt = orchestrator.run_once(
        StageInputBundle(
            temporal=TemporalContextInput(
                source_time_utc=datetime(2026, 4, 21, 13, 31, tzinfo=UTC),
                source_timezone_raw="America/New_York",
            ),
            regime=MarketRegimeContextInput(
                nvda_return_pct=0.1,
                nq_return_pct=0.05,
                vix_level=20.0,
            ),
            options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
        ),
        live_inventory_service=DownstreamLiveInventoryService(position_repository=positions),
        live_inventory_request={"inventory_id": "runtime-inv", "live_ids": [" pos-1 "]},
    )

    assert receipt["stage_order"] == [
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
        "execution",
    ]
    assert receipt["stage_outputs"]["execution"]["scaling_plan"] == ["stand_down"]
    assert receipt["runtime_live_inventory"]["inventory_id"] == "runtime-inv"
    assert receipt["runtime_live_inventory"]["live_ids"] == ["pos-1"]
    assert receipt["runtime_live_inventory"]["exposure_state"] == {
        "position_count": 1,
        "open_position_ids": ["pos-1"],
        "declared_exposure_by_symbol": {"NVDA": 10.0},
    }
    assert receipt["runtime_live_inventory_policy_effect"] == "read_only_no_serial_decision_change"
    assert orchestrator.__dict__ == {}


def test_runtime_live_inventory_attachment_rejects_unsupported_request_keys() -> None:
    from nvda_desk.downstream.live_inventory import DownstreamLiveInventoryService

    runtime = _require_module("nvda_desk.runtime.orchestrator")
    orchestrator = _require_attr(runtime, "DeskRuntimeOrchestrator")()

    with pytest.raises(ValueError, match="unsupported keys: broker_order_id"):
        orchestrator.run_once(
            {"temporal": {"source_time_utc": "2026-04-21T09:31:00"}},
            live_inventory_service=DownstreamLiveInventoryService(),
            live_inventory_request={"broker_order_id": "broker-1"},
        )

def test_runtime_orchestrator_can_attach_reconciled_inventory_snapshot_without_service_read() -> None:
    from nvda_desk.downstream.live_inventory import DownstreamLiveInventoryService
    from nvda_desk.repositories.position_repository import PositionRepository

    runtime = _require_module("nvda_desk.runtime.orchestrator")
    orchestrator = _require_attr(runtime, "DeskRuntimeOrchestrator")()
    positions = PositionRepository()
    snapshot = DownstreamLiveInventoryService(position_repository=positions).reconcile_fill_evidence(
        [
            {
                "fill_evidence_id": "fill-1",
                "position_id": "pos-1",
                "symbol": "NVDA",
                "declared_exposure_delta": 7.5,
            }
        ],
        reconciliation_id="recon-runtime-1",
        inventory_id="runtime-reconciled",
        receipt_id="runtime-inv-receipt-1",
    )

    receipt = orchestrator.run_once(
        StageInputBundle(
            temporal=TemporalContextInput(
                source_time_utc=datetime(2026, 4, 21, 13, 31, tzinfo=UTC),
                source_timezone_raw="America/New_York",
            ),
            regime=MarketRegimeContextInput(
                nvda_return_pct=0.1,
                nq_return_pct=0.05,
                vix_level=20.0,
            ),
            options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
        ),
        live_inventory_snapshot=snapshot,
    )

    assert receipt["stage_outputs"]["execution"]["scaling_plan"] == ["stand_down"]
    assert receipt["runtime_live_inventory"]["inventory_id"] == "runtime-reconciled"
    assert receipt["runtime_live_inventory"]["live_ids"] == ["pos-1"]
    assert receipt["runtime_live_inventory"]["inventory_receipt"] == {
        "receipt_id": "runtime-inv-receipt-1",
        "inventory_id": "runtime-reconciled",
        "position_ids": ["pos-1"],
        "capital_snapshot_id": None,
        "policy_freeze_state": "architecture_only_no_policy",
    }
    assert receipt["runtime_live_inventory_policy_effect"] == "read_only_no_serial_decision_change"
    assert orchestrator.__dict__ == {}


def test_runtime_live_inventory_attachment_rejects_ambiguous_or_orphaned_inputs() -> None:
    from nvda_desk.downstream.live_inventory import DownstreamLiveInventoryService
    from nvda_desk.contracts.downstream import DownstreamLiveInventorySnapshot

    runtime = _require_module("nvda_desk.runtime.orchestrator")
    orchestrator = _require_attr(runtime, "DeskRuntimeOrchestrator")()

    with pytest.raises(ValueError, match="live_inventory_request requires live_inventory_service"):
        orchestrator.run_once(
            {"temporal": {"source_time_utc": "2026-04-21T09:31:00"}},
            live_inventory_request={"inventory_id": "orphan"},
        )

    with pytest.raises(ValueError, match="cannot both be supplied"):
        orchestrator.run_once(
            {"temporal": {"source_time_utc": "2026-04-21T09:31:00"}},
            live_inventory_service=DownstreamLiveInventoryService(),
            live_inventory_snapshot=DownstreamLiveInventorySnapshot(inventory_id="snapshot"),
        )
