"""Compatibility wrapper for workbook-owned downstream state service path."""

from __future__ import annotations

from nvda_desk.contracts.downstream import DownstreamStateReadResult
from nvda_desk.downstream.state_reader import DownstreamStateService as _DownstreamStateService


class DownstreamStateService(_DownstreamStateService):
    """Workbook-owned alias of the bounded downstream state reader."""

    def read_state(
        self, position_ids: list[str] | None = None, receipt_id: str | None = None
    ) -> DownstreamStateReadResult:
        return super().read_state(position_ids=position_ids, receipt_id=receipt_id)
