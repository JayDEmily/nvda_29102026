"""Assembly helper for minute-level Parallel Risk Lane profiles."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from nvda_desk.contracts.parallel_risk import (
    EventProximityRegisterEntry,
    FreshnessRegisterEntry,
    MissingSignalRegisterEntry,
    ParallelRiskMinuteProfile,
    ParallelRiskPreparationPacket,
    SignalSnapshotEntry,
)
from nvda_desk.domain.parallel_risk.environment_assessment import assess_environment, assess_risk_envelope
from nvda_desk.domain.parallel_risk.family_aggregation import aggregate_risk_family_states
from nvda_desk.domain.parallel_risk.risk_atoms import build_supported_risk_atoms


def assemble_parallel_risk_minute_profile(
    *,
    packet: ParallelRiskPreparationPacket,
    packet_id: str,
    symbol: str,
    generated_at_utc: datetime,
    freshness_entries: list[FreshnessRegisterEntry] | None = None,
    missing_signal_entries: list[MissingSignalRegisterEntry] | None = None,
    event_proximity_entries: list[EventProximityRegisterEntry] | None = None,
    parent_packet_ids: list[str] | None = None,
    dependency_packet_ids: list[str] | None = None,
    source_artifact_ids: list[str] | None = None,
    input_fingerprint: str | None = None,
) -> ParallelRiskMinuteProfile:
    """Assemble a descriptive minute profile from current lawful PRL primitives."""

    environment = assess_environment(packet)
    envelope = assess_risk_envelope(packet)
    freshness = list(freshness_entries or [])
    missing = list(missing_signal_entries or [])
    events = list(event_proximity_entries or [])
    atoms = build_supported_risk_atoms(
        freshness_entries=freshness,
        missing_signal_entries=missing,
        event_proximity_entries=events,
        envelope=envelope,
        generated_at_utc=generated_at_utc,
    )
    families = aggregate_risk_family_states(atoms)
    signal_snapshot = _signal_snapshot(packet)
    return ParallelRiskMinuteProfile(
        packet_id=packet_id,
        symbol=symbol,
        source_time_utc=packet.temporal_input.source_time_utc or generated_at_utc,
        generated_at_utc=generated_at_utc,
        session_state="unknown",
        risk_envelope_state=envelope.envelope_state,
        active_risk_atoms=[atom for atom in atoms if atom.state != "inactive"],
        watched_risk_atoms=[atom for atom in atoms if atom.state == "inactive"],
        risk_family_states=families,
        signal_snapshot=signal_snapshot,
        missing_signal_register=missing,
        freshness_register=freshness,
        event_proximity_register=events,
        contribution_breakdown=[],
        hard_blocks=list(envelope.hard_blocks),
        caution_flags=list(envelope.caution_flags),
        uncertainty_summary=_uncertainty_summary(freshness=freshness, missing=missing),
        mechanical_summary={
            "environment_assessment_basis": environment.assessment_basis,
            "risk_envelope_state": envelope.envelope_state,
            "atom_count": len(atoms),
            "family_count": len(families),
        },
        lineage={
            "bootstrap_source": packet.bootstrap_source,
            "parent_packet_ids": list(parent_packet_ids or []),
            "dependency_packet_ids": list(dependency_packet_ids or []),
            "source_artifact_ids": list(source_artifact_ids or []),
            "input_fingerprint": input_fingerprint,
            "forbidden_authority_keys_consumed": [],
        },
        notes=["parallel_risk_minute_profile_state_of_play_only"],
    )


def _signal_snapshot(packet: ParallelRiskPreparationPacket) -> list[SignalSnapshotEntry]:
    entries: list[SignalSnapshotEntry] = []
    temporal = packet.temporal_input
    if temporal.source_time_utc is not None:
        entries.append(
            SignalSnapshotEntry(
                signal_id="source_time_utc",
                signal_family="source_temporal",
                raw_or_derived="metadata",
                value=temporal.source_time_utc.isoformat(),
                units="datetime_utc",
                source_time_utc=temporal.source_time_utc,
                freshness_state="unknown",
            )
        )
    if packet.regime_input.vix_level is not None:
        entries.append(
            SignalSnapshotEntry(
                signal_id="vix_level",
                signal_family="macro_regime",
                raw_or_derived="raw",
                value=packet.regime_input.vix_level,
                units="index_level",
                source_time_utc=temporal.source_time_utc,
                freshness_state="unknown",
            )
        )
    for signal_id, value in (
        ("spot_price", packet.options_flow_input.spot_price),
        ("front_dte", packet.options_flow_input.front_dte),
        ("next_dte", packet.options_flow_input.next_dte),
    ):
        if value is not None:
            entries.append(
                SignalSnapshotEntry(
                    signal_id=signal_id,
                    signal_family="options_flow",
                    raw_or_derived="raw",
                    value=value,
                    units="price" if signal_id == "spot_price" else "days",
                    source_time_utc=temporal.source_time_utc,
                    freshness_state="unknown",
                )
            )
    return entries


def _uncertainty_summary(
    *, freshness: list[FreshnessRegisterEntry], missing: list[MissingSignalRegisterEntry]
) -> dict[str, Any]:
    return {
        "freshness_unknown_or_stale_count": sum(
            1 for entry in freshness if entry.freshness_state in {"unknown", "stale"}
        ),
        "missing_signal_count": len(missing),
        "summary_basis": "deterministic_register_counts_only",
    }
