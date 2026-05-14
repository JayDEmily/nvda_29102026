"""Compatibility wrapper for workbook-owned downstream live-inventory service path."""

from __future__ import annotations

from nvda_desk.contracts.downstream import DownstreamLiveInventorySnapshot
from nvda_desk.downstream.live_inventory import (
    DownstreamLiveInventoryService as _DownstreamLiveInventoryService,
)


class DownstreamLiveInventoryService(_DownstreamLiveInventoryService):
    """Workbook-owned alias of the bounded downstream live-inventory service."""

    def build_live_snapshot(
        self,
        live_ids: list[str] | None = None,
        *,
        inventory_id: str = "live-inventory",
        capital_snapshot_id: str | None = None,
        receipt_id: str | None = None,
    ) -> DownstreamLiveInventorySnapshot:
        return super().build_live_snapshot(
            live_ids=live_ids,
            inventory_id=inventory_id,
            capital_snapshot_id=capital_snapshot_id,
            receipt_id=receipt_id,
        )
