"""Missing/quarantined signal helpers for the Parallel Risk Lane.

These helpers describe input availability and confidence, not a trading posture.
"""

from __future__ import annotations

from typing import Literal

from nvda_desk.contracts.parallel_risk import MissingSignalRegisterEntry, SignalSnapshotEntry
from nvda_desk.contracts.upstream_signal import UpstreamIngressResult


def build_missing_signal_register_entry(
    *,
    signal_id: str,
    signal_family: str,
    expected_reason: str,
    missing_reason: str,
    impact_on_profile: Literal[
        "none", "lowers_confidence", "disables_atom", "forces_caution", "forces_block"
    ] = "lowers_confidence",
    source_refs: list[str] | None = None,
    expected_signal_inventory_ref: str | None = None,
    workbook_lineage_refs: list[str] | None = None,
) -> MissingSignalRegisterEntry:
    """Return one metadata-only missing-signal register entry."""

    return MissingSignalRegisterEntry(
        signal_id=signal_id,
        signal_family=signal_family,
        expected_reason=expected_reason,
        missing_reason=missing_reason,
        impact_on_profile=impact_on_profile,
        source_refs=list(source_refs or []),
        expected_signal_inventory_ref=expected_signal_inventory_ref,
        workbook_lineage_refs=list(workbook_lineage_refs or []),
    )


def signal_snapshot_from_upstream_ingress_result(
    result: UpstreamIngressResult, *, raw_or_derived: Literal["raw", "derived", "metadata", "config", "trace"]
) -> SignalSnapshotEntry:
    """Project one upstream ingress result into a PRL signal snapshot entry.

    Rejected/quarantined values remain unavailable to the PRL; admitted trace-only payloads
    keep trace value and lineage without opening decision authority.
    """

    trace = result.sanity_trace
    if result.quarantined:
        return SignalSnapshotEntry(
            signal_id=trace.signal_family_id,
            signal_family=trace.signal_family_id,
            raw_or_derived=raw_or_derived,
            value=None,
            missing_or_quarantined="quarantined",
            rejection_reason=trace.rejection_reason,
            source_ids=[trace.source_id],
            lawful_prl_use_allowed=False,
            lawful_prl_use_reason="upstream_signal_quarantined_not_available_to_prl",
        )

    return SignalSnapshotEntry(
        signal_id=trace.signal_family_id,
        signal_family=trace.signal_family_id,
        raw_or_derived=raw_or_derived,
        value=result.trace_envelope.get("payload", {}),
        missing_or_quarantined="present",
        source_ids=[trace.source_id],
        lineage_refs=[trace.scope_id],
        lawful_prl_use_allowed=True,
        lawful_prl_use_reason="admitted_trace_only_signal_snapshot",
    )
