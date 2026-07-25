from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.api.app import create_app
from nvda_desk.contracts.daily_pnl import DailyPnlReport
from nvda_desk.downstream.daily_pnl import DailyPnlReportService


def test_daily_pnl_report_service_records_and_lists_reports_without_trading_mutation() -> None:
    service = DailyPnlReportService()
    report = service.record_report(
        DailyPnlReport(
            report_id="pnl-1",
            trade_date="2026-05-15",
            symbol="NVDA",
            realised_pnl_usd=120.5,
            unrealised_pnl_usd=-20.0,
            evidence_ids=("fill-1", "position-1"),
        )
    )

    assert report.total_pnl_usd == 100.5
    assert report.trading_decision_mutated is False
    assert service.list_reports().reports == (report,)


def test_daily_pnl_report_rejects_hidden_trading_authority_payloads() -> None:
    with pytest.raises(ValidationError, match="trading authority"):
        DailyPnlReport(
            report_id="pnl-bad",
            trade_date="2026-05-15",
            symbol="NVDA",
            realised_pnl_usd=0.0,
            context={"order_submitted": True},
        )


def test_api_records_and_lists_daily_pnl_reports() -> None:
    app = create_app()
    assert {"record_daily_pnl_report", "list_daily_pnl_reports"}.issubset(app.route_handlers)

    result = app.record_daily_pnl_report(
        {
            "report_id": "api-pnl-1",
            "trade_date": "2026-05-15",
            "symbol": "NVDA",
            "realised_pnl_usd": 10.0,
            "unrealised_pnl_usd": 2.5,
        }
    )

    assert result["total_pnl_usd"] == 12.5
    assert app.list_daily_pnl_reports()[0]["report_id"] == "api-pnl-1"
