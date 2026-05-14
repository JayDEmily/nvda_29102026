"""Coordinate bounded downstream review receipts only."""

from __future__ import annotations

from nvda_desk.contracts.downstream import (
    DownstreamArchitectureReceipt,
    DownstreamLiveInventorySnapshot,
    DownstreamOpeningSnapshot,
)


class DownstreamReviewService:
    """Build downstream architecture receipts without behavioural policy."""

    def build_receipt(
        self,
        *,
        opening_snapshot: DownstreamOpeningSnapshot,
        live_inventory_snapshot: DownstreamLiveInventorySnapshot,
    ) -> DownstreamArchitectureReceipt:
        return DownstreamArchitectureReceipt(
            opening_snapshot=opening_snapshot,
            live_inventory_snapshot=live_inventory_snapshot,
        )
