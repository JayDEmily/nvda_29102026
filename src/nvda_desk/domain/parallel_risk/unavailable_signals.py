"""Unavailable-signal helpers for PRL signal inventory integration.

Unavailable signals are explicit state-of-play metadata. They prevent hallucinated market
context until a lawful typed source exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from nvda_desk.contracts.parallel_risk import (
    MissingSignalRegisterEntry,
    ParallelRiskExpectedSignalRecord,
    ParallelRiskSignalInventoryDocument,
    SignalSnapshotEntry,
)

InventoryPresenceState = Literal[
    "present",
    "missing",
    "unavailable",
    "deferred",
    "excluded",
    "quarantined",
    "rejected",
]


@dataclass(frozen=True)
class InventoryBackedUnavailableSignals:
    """Unavailable-signal projection derived from the typed PRL inventory."""

    signal_snapshot: list[SignalSnapshotEntry]
    missing_signal_register: list[MissingSignalRegisterEntry]
    presence_by_signal_id: dict[str, InventoryPresenceState]
    open_unresolved_signals: list[dict[str, str]]


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


def build_inventory_backed_unavailable_signals(
    *,
    inventory: ParallelRiskSignalInventoryDocument,
    present_signal_ids: set[str] | frozenset[str],
    quarantined_signal_ids: set[str] | frozenset[str] | None = None,
    rejected_signal_ids: set[str] | frozenset[str] | None = None,
    source_refs: list[str] | None = None,
) -> InventoryBackedUnavailableSignals:
    """Project inventory availability into snapshot/register metadata without fake values."""

    present = set(present_signal_ids)
    quarantined = set(quarantined_signal_ids or set())
    rejected = set(rejected_signal_ids or set())
    refs = list(source_refs or [])
    snapshots: list[SignalSnapshotEntry] = []
    register: list[MissingSignalRegisterEntry] = []
    presence: dict[str, InventoryPresenceState] = {}
    unresolved: list[dict[str, str]] = []

    for record in inventory.records:
        if record.inventory_status == "excluded":
            presence[record.signal_id] = "excluded"
            continue
        if record.signal_id in rejected:
            state: InventoryPresenceState = "rejected"
            reason = "upstream_signal_rejected_not_available_to_prl"
            impact = "lowers_confidence"
        elif record.signal_id in quarantined:
            state = "quarantined"
            reason = "upstream_signal_quarantined_not_available_to_prl"
            impact = "lowers_confidence"
        elif record.signal_id in present:
            presence[record.signal_id] = "present"
            continue
        elif record.inventory_status == "available_now" and record.required_for_current_atom:
            state = "missing"
            reason = record.missing_handling
            impact = _impact_from_policy(record.missing_handling)
        elif record.inventory_status == "deferred":
            state = "deferred"
            reason = record.unavailable_handling
            impact = _impact_from_policy(record.missing_handling)
        else:
            state = "unavailable"
            reason = record.unavailable_handling
            impact = _impact_from_policy(record.missing_handling)

        presence[record.signal_id] = state
        snapshot = _snapshot_from_inventory_record(
            record=record,
            state=state,
            reason=reason,
            source_refs=refs,
        )
        snapshots.append(snapshot)
        register.append(
            MissingSignalRegisterEntry(
                signal_id=record.signal_id,
                signal_family=record.signal_family,
                expected_reason="expected_by_parallel_risk_signal_inventory",
                missing_reason=reason,
                impact_on_profile=impact,
                source_refs=refs,
                expected_signal_inventory_ref=f"{inventory.inventory_id}#{record.promotion_record_key}",
                workbook_lineage_refs=list(record.workbook_lineage_refs),
            )
        )
        unresolved.append(
            {
                "signal_id": record.signal_id,
                "signal_family": record.signal_family,
                "inventory_status": record.inventory_status,
                "presence_state": state,
                "handling_policy": reason,
            }
        )

    return InventoryBackedUnavailableSignals(
        signal_snapshot=snapshots,
        missing_signal_register=register,
        presence_by_signal_id=presence,
        open_unresolved_signals=unresolved,
    )


def _snapshot_from_inventory_record(
    *,
    record: ParallelRiskExpectedSignalRecord,
    state: InventoryPresenceState,
    reason: str,
    source_refs: list[str],
) -> SignalSnapshotEntry:
    return SignalSnapshotEntry(
        signal_id=record.signal_id,
        signal_family=record.signal_family,
        raw_or_derived=_signal_kind(record.raw_derived_config_trace_classification),
        value=None,
        freshness_state="unknown",
        freshness_reason=reason,
        lineage_refs=list(source_refs),
        workbook_lineage_refs=list(record.workbook_lineage_refs),
        missing_or_quarantined=state,
        lawful_prl_use_allowed=False,
        lawful_prl_use_reason="typed_inventory_signal_not_available_to_prl_runtime",
    )


def _impact_from_policy(policy: str) -> Literal[
    "none", "lowers_confidence", "disables_atom", "forces_caution", "forces_block"
]:
    if "forces_block" in policy:
        return "forces_block"
    if "forces_caution" in policy:
        return "forces_caution"
    if "disables_atom" in policy:
        return "disables_atom"
    if "lowers_confidence" in policy or "no_value" in policy:
        return "lowers_confidence"
    return "none"


def _signal_kind(classification: str) -> Literal["raw", "derived", "metadata", "config", "trace"]:
    if "trace" in classification or "upstream_packet" in classification:
        return "trace"
    if "config" in classification:
        return "config"
    if "derived" in classification:
        return "derived"
    if "raw" in classification:
        return "raw"
    return "metadata"
