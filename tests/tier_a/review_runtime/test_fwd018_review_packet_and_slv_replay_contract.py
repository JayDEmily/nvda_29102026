from __future__ import annotations

from nvda_desk.api.app import create_app
from nvda_desk.contracts.daily_pnl import DailyPnlReport
from nvda_desk.persistence.execution_records import ExecutionRecordsRepository
from nvda_desk.repositories.position_repository import PositionRepository
from nvda_desk.review.packet_service import ReviewPacketService
from nvda_desk.review.strategic_ladder_replay import StrategicLadderReplayService


def test_review_packet_service_builds_module_health_and_daily_packet_with_pnl_fallback() -> None:
    execution_records = ExecutionRecordsRepository()
    execution_records.append_record({"module_id": "module-a", "record_type": "order_event"})
    execution_records.append_record({"module_id": "module-a", "record_type": "fill_event"})
    positions = PositionRepository()
    positions.write_position("pos-1", {"symbol": "NVDA"})
    service = ReviewPacketService(
        execution_records=execution_records,
        position_repository=positions,
        active_module_ids=("module-a", "module-b"),
    )

    health = service.build_module_health_packet(packet_id="health-1")
    daily = service.build_daily_review_packet(
        packet_id="daily-1", symbol="NVDA", trade_date="2026-05-15"
    )

    assert health.module_summaries[0].order_event_count == 1
    assert health.module_summaries[0].fill_event_count == 1
    assert health.position_snapshot_count == 1
    assert daily.daily_pnl.report_id == "daily-1::pnl-fallback"
    assert daily.missing_material_ids == ("daily_pnl_report::NVDA::2026-05-15",)
    assert daily.source_packet_ids == ("daily-1::module-health",)
    assert daily.source_receipt_ids == ()
    assert daily.source_artifact_ids == ()
    assert daily.rendering_authority_mutated is False


def test_review_packet_service_renders_review_safe_payloads_without_runtime_authority() -> None:
    service = ReviewPacketService()
    rendering = service.render_review_safe_packet(
        packet_id="render-1",
        packet_kind="failure_taxonomy",
        payload={"failure": "missing_trigger", "order_submitted": "redacted"},
    )

    assert rendering.packet_kind == "failure_taxonomy"
    assert rendering.review_safe_payload["failure"] == "missing_trigger"
    assert "order_submitted" not in rendering.review_safe_payload
    assert rendering.runtime_authority_mutated is False


def test_strategic_ladder_replay_builds_context_metrics_and_walk_forward_output() -> None:
    service = StrategicLadderReplayService()
    context = service.build_replay_context(
        context_id="ctx-1",
        market_state={
            "symbol": "NVDA",
            "previous_close": 100.0,
            "latest_close": 105.0,
            "vwap": 102.0,
        },
        overlay_state={"risk": "normal"},
    )
    replay = service.run_replay(run_id="run-1", contexts=(context,))
    walk_forward = service.build_walk_forward_output(output_id="wf-1", replay_results=(replay,))

    assert context.percent_change == 5.0
    assert context.distance_to_vwap_pct == 2.9412
    assert replay.runtime_authority_mutated is False
    assert walk_forward.run_count == 1


def test_api_exposes_review_packets_and_strategic_ladder_replay_surfaces() -> None:
    app = create_app()
    assert {"get_module_health_packet", "get_daily_review_packet"}.issubset(app.route_handlers)

    app.record_daily_pnl_report(
        DailyPnlReport(
            report_id="pnl-1",
            trade_date="2026-05-15",
            symbol="NVDA",
            realised_pnl_usd=1.0,
        ).model_dump(mode="json")
    )
    health = app.get_module_health_packet({"packet_id": "health-api"})
    daily = app.get_daily_review_packet(
        {"packet_id": "daily-api", "symbol": "NVDA", "trade_date": "2026-05-15"}
    )

    assert health["packet_id"] == "health-api"
    assert daily["daily_pnl"]["report_id"] == "pnl-1"
    assert daily["missing_material_ids"] == []
    assert daily["source_packet_ids"] == ["daily-api::module-health"]
    assert daily["source_receipt_ids"] == ["pnl-1"]
