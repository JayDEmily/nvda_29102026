"""Build deterministic bounded-trace review reports."""

from __future__ import annotations

from collections.abc import Iterable

from nvda_desk.contracts.trace_review import BoundedTraceReviewReport, BoundedTraceRunResult


class BoundedTraceReviewService:
    """Aggregate bounded-trace run results into one review report."""

    def build_report(
        self,
        *,
        runs: Iterable[BoundedTraceRunResult],
        narrative_summary: str | None = None,
    ) -> BoundedTraceReviewReport:
        return BoundedTraceReviewReport(runs=list(runs), narrative_summary=narrative_summary)


__all__ = ["BoundedTraceReviewService", "BoundedTraceReviewReport", "BoundedTraceRunResult"]
