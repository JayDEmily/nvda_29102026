"""Compatibility wrapper over the benchmark-owned calendar reference projection home."""

from __future__ import annotations

from nvda_desk.calendar.reference.projection import (
    FinancialCalendarCrosswalkRecord,
    FinancialCalendarProjectionService,
    MarketStateService,
    financial_calendar_crosswalk,
    project_runtime_context,
    stitch_precursor_context,
)

__all__ = [
    "FinancialCalendarCrosswalkRecord",
    "FinancialCalendarProjectionService",
    "MarketStateService",
    "financial_calendar_crosswalk",
    "project_runtime_context",
    "stitch_precursor_context",
]
