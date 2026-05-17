from __future__ import annotations

from copy import deepcopy

from nvda_desk.contracts.daily_pnl import DailyPnlReport, DailyPnlReportCollection


class DailyPnlReportService:
    def __init__(self) -> None:
        self._reports: dict[str, DailyPnlReport] = {}

    def record_report(self, report: DailyPnlReport) -> DailyPnlReport:
        if report.report_id in self._reports:
            raise ValueError(f"duplicate report_id: {report.report_id}")
        self._reports[report.report_id] = report.model_copy(deep=True)
        return report.model_copy(deep=True)

    def list_reports(self) -> DailyPnlReportCollection:
        return DailyPnlReportCollection(reports=tuple(deepcopy(list(self._reports.values()))))

    def find_report(self, *, symbol: str, trade_date: str) -> DailyPnlReport | None:
        normalised_symbol = symbol.strip().upper()
        for report in self._reports.values():
            if report.symbol == normalised_symbol and report.trade_date == trade_date:
                return report.model_copy(deep=True)
        return None
