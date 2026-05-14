"""Read bounded downstream state snapshots."""

from __future__ import annotations

from nvda_desk.contracts.downstream import DownstreamStateReadResult, DownstreamStateSnapshot


class DownstreamStateService:
    """Return truthful downstream state reads without inventing policy."""

    def read_state(
        self, position_ids: list[str] | None = None, receipt_id: str | None = None
    ) -> DownstreamStateReadResult:
        return DownstreamStateReadResult(
            snapshot=DownstreamStateSnapshot(position_ids=list(position_ids or [])),
            receipt_id=receipt_id,
        )
