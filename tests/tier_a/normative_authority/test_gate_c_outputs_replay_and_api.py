from __future__ import annotations

from nvda_desk.api.app import create_app
from nvda_desk.contracts.daily_pnl import DailyPnlReport
from nvda_desk.downstream.daily_pnl import DailyPnlReportService


def test_c021_c048_api_does_not_own_untyped_veto_or_risk_block_state() -> None:
    app = create_app()
    assert not hasattr(app, "_veto_events")
    assert not hasattr(app, "_risk_block_events")
    assert "record_veto_event" not in app.route_handlers
    assert "record_risk_block_event" not in app.route_handlers


def test_c041_c048_api_exit_close_path_rejects_missing_upstream_authority_instead_of_fabricating_ids() -> (
    None
):
    app = create_app()
    try:
        app.evaluate_overnight_carry({"requested_action": "hold"})
    except (ValueError, TypeError):
        return
    raise AssertionError("API fabricated exit/close input authority instead of failing closed")


def test_c043_daily_pnl_reporting_is_idempotent_by_report_identity_and_preserves_evidence_ids() -> (
    None
):
    service = DailyPnlReportService()
    report = DailyPnlReport(
        report_id="pnl-1",
        trade_date="2026-05-15",
        symbol="NVDA",
        realised_pnl_usd=10.0,
        unrealised_pnl_usd=2.5,
        evidence_ids=("fill-1", "position-1"),
    )
    first = service.record_report(report)
    try:
        service.record_report(report)
    except ValueError as exc:
        assert "duplicate report_id" in str(exc)
    else:
        raise AssertionError("duplicate report identity was silently accepted")

    assert [item.report_id for item in service.list_reports().reports] == ["pnl-1"]
    assert first.evidence_ids == ("fill-1", "position-1")
    assert first.trading_decision_mutated is False


def test_c047_replay_evaluation_requires_dataset_and_window_identity_and_cannot_promote_runtime_authority() -> (
    None
):
    from dataclasses import fields

    from nvda_desk.analysis.replay.walk_forward import WalkForwardHarnessAuthorityPacket

    names = {field.name for field in fields(WalkForwardHarnessAuthorityPacket)}
    assert {"dataset_id", "dataset_fingerprint"}.issubset(names)
    assert "windows" in names
    assert WalkForwardHarnessAuthorityPacket.__dataclass_fields__[
        "consumer_mode"
    ].default.value in {
        "review_only",
        "research_only",
    }
