"""Unavailable-signal helpers for future PRL signal inventory integration.

Unavailable signals are explicit state-of-play metadata. They prevent hallucinated market
context until a lawful typed source exists.
"""

from __future__ import annotations

from nvda_desk.contracts.parallel_risk import MissingSignalRegisterEntry, SignalSnapshotEntry


def build_unavailable_signal_snapshot_entry(
    *,
    signal_id: str,
    signal_family: str,
    reason: str,
    expected_signal_inventory_ref: str | None = None,
    workbook_lineage_refs: list[str] | None = None,
    source_refs: list[str] | None = None,
) -> SignalSnapshotEntry:
    """Return a snapshot entry for a known-but-unavailable signal without a value."""

    return SignalSnapshotEntry(
        signal_id=signal_id,
        signal_family=signal_family,
        raw_or_derived="metadata",
        value=None,
        freshness_state="unknown",
        freshness_reason=reason,
        lineage_refs=list(source_refs or []),
        workbook_lineage_refs=list(workbook_lineage_refs or []),
        missing_or_quarantined="missing",
        lawful_prl_use_allowed=False,
        lawful_prl_use_reason="typed_runtime_signal_unavailable",
    )


def build_unavailable_signal_watch_entry(
    *,
    signal_id: str,
    signal_family: str,
    reason: str,
    expected_signal_inventory_ref: str | None = None,
    workbook_lineage_refs: list[str] | None = None,
    source_refs: list[str] | None = None,
) -> MissingSignalRegisterEntry:
    """Return a register entry for a known unavailable signal family."""

    return MissingSignalRegisterEntry(
        signal_id=signal_id,
        signal_family=signal_family,
        expected_reason="expected_by_future_parallel_risk_lane_signal_inventory",
        missing_reason=reason,
        impact_on_profile="lowers_confidence",
        source_refs=list(source_refs or []),
        expected_signal_inventory_ref=expected_signal_inventory_ref,
        workbook_lineage_refs=list(workbook_lineage_refs or []),
    )
