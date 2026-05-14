"""Pure downstream live-inventory calculations."""

from __future__ import annotations

from nvda_desk.contracts.downstream import DownstreamLiveInventorySnapshot
from nvda_desk.downstream.live_inventory import DownstreamLiveInventoryService


def build_live_inventory_snapshot(
    live_ids: list[str] | None = None,
) -> DownstreamLiveInventorySnapshot:
    """Return one bounded live-inventory snapshot without injecting policy."""
    return DownstreamLiveInventoryService().build_live_snapshot(live_ids=live_ids)
