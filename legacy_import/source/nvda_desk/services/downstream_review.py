"""Architecture-only downstream review receipt builder."""
from __future__ import annotations

from nvda_desk.schemas.downstream import (
    DownstreamArchitectureReceipt,
    DownstreamLiveInventorySnapshot,
    DownstreamOpeningSnapshot,
)


class DownstreamReviewService:
    """Build review-safe receipts for the downstream bootstrap."""

    service_id = "downstream_review_service"

    def build_receipt(
        self,
        *,
        opening_snapshot: DownstreamOpeningSnapshot,
        live_inventory_snapshot: DownstreamLiveInventorySnapshot,
    ) -> DownstreamArchitectureReceipt:
        """Return the downstream architecture receipt without policy claims."""

        return DownstreamArchitectureReceipt(
            opening_snapshot=opening_snapshot,
            live_inventory_snapshot=live_inventory_snapshot,
            deferred_domains=[
                "opening_policy",
                "placement_readiness_policy",
                "placement_handoff_policy",
                "live_inventory_health_policy",
                "position_management_policy",
                "capital_rotation_policy",
                "exit_policy",
                "close_execution_policy",
            ],
            notes=[
                "downstream_review_receipt_architecture_only",
                "receipt_must_not_be_read_as_behavioural_policy",
            ],
        )
