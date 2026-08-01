"""Supported risk atom construction for currently available PRL inputs.

Risk atoms describe the market state-of-play. They can carry constructive, defensive,
ambiguous, mixed, uncertainty, and consequence semantics without issuing trade advice.
"""

from __future__ import annotations

from datetime import datetime

from nvda_desk.contracts.parallel_risk import (
    EventProximityRegisterEntry,
    FreshnessRegisterEntry,
    MissingSignalRegisterEntry,
    ParallelRiskAtomStateValue,
    ParallelRiskEnvelope,
    RiskAtomState,
)


def build_supported_risk_atoms(
    *,
    freshness_entries: list[FreshnessRegisterEntry],
    missing_signal_entries: list[MissingSignalRegisterEntry],
    event_proximity_entries: list[EventProximityRegisterEntry],
    envelope: ParallelRiskEnvelope,
    generated_at_utc: datetime | None = None,
) -> list[RiskAtomState]:
    """Build risk atoms from the currently lawful PRL signal surface."""

    atoms: list[RiskAtomState] = []
    atoms.extend(_freshness_atom(entry) for entry in freshness_entries)
    atoms.extend(_missing_signal_atom(entry) for entry in missing_signal_entries)
    atoms.extend(_event_atom(entry) for entry in event_proximity_entries)
    atoms.extend(_envelope_atoms(envelope))
    return atoms


def _freshness_atom(entry: FreshnessRegisterEntry) -> RiskAtomState:
    state: ParallelRiskAtomStateValue = "observe" if entry.freshness_state != "stale" else "caution"
    risk_side = "constructive" if entry.freshness_state == "fresh" else "uncertainty"
    confidence = (
        0.9
        if entry.freshness_state == "fresh"
        else 0.45 if entry.freshness_state == "unknown" else 0.6
    )
    return RiskAtomState(
        risk_atom_id=f"freshness:{entry.signal_id}",
        name="source_freshness_state",
        family="operational_tooling",
        state=state,
        intensity=0.2 if entry.freshness_state == "fresh" else 0.6,
        confidence=confidence,
        trigger_condition=f"freshness_state={entry.freshness_state}",
        observable_cues=[entry.model_dump(mode="json")],
        calculation_basis={"method_id": "freshness_register_v1", "risk_side": risk_side},
        source_refs=list(entry.source_refs),
        time_sensitivity={"session_phase_sensitive": False},
        trader_cognition_update={
            "uncertainty_side": [entry.impact_on_profile or "freshness_state"]
        },
        why_this_is_risk_not_play="Freshness describes reliability of the state read, not a trade action.",
    )


def _missing_signal_atom(entry: MissingSignalRegisterEntry) -> RiskAtomState:
    return RiskAtomState(
        risk_atom_id=f"signal_availability:{entry.signal_id}",
        name="signal_availability_state",
        family=entry.signal_family,
        state="observe",
        intensity=0.45 if entry.impact_on_profile == "lowers_confidence" else 0.2,
        confidence=0.7,
        trigger_condition=entry.missing_reason,
        observable_cues=[entry.model_dump(mode="json")],
        calculation_basis={"method_id": "missing_signal_register_v1", "risk_side": "uncertainty"},
        source_refs=list(entry.source_refs),
        time_sensitivity={"session_phase_sensitive": False},
        trader_cognition_update={"uncertainty_side": [entry.missing_reason]},
        why_this_is_risk_not_play="Signal availability changes confidence and uncertainty only; it does not choose a response.",
    )


def _event_atom(entry: EventProximityRegisterEntry) -> RiskAtomState:
    active_tag = "scheduled_event_window_active" in set(entry.runtime_tags)
    return RiskAtomState(
        risk_atom_id=f"event_proximity:{entry.event_id}",
        name="event_proximity_state",
        family="calendar_event",
        state="caution" if active_tag else "observe",
        intensity=0.7 if active_tag else 0.35,
        confidence=0.8,
        trigger_condition=entry.risk_interpretation,
        observable_cues=[entry.model_dump(mode="json")],
        calculation_basis={"method_id": "event_proximity_register_v1", "risk_side": "mixed"},
        source_refs=list(entry.source_refs),
        time_sensitivity={"event_window_sensitive": True},
        trader_cognition_update={
            "consequence_side": [entry.event_type],
            "uncertainty_side": entry.runtime_tags,
        },
        why_this_is_risk_not_play="Event proximity describes timing and consequence context, not a trading instruction.",
    )


def _envelope_atoms(envelope: ParallelRiskEnvelope) -> list[RiskAtomState]:
    atoms: list[RiskAtomState] = []
    for contribution in envelope.contributions:
        atoms.append(
            RiskAtomState(
                risk_atom_id=f"envelope:{contribution.source_family}:{contribution.reason}",
                name="legacy_envelope_contribution_state",
                family=contribution.source_family,
                state=_coerce_atom_state(contribution.state),
                intensity=0.75 if contribution.state in {"caution", "block"} else 0.35,
                confidence=0.75,
                trigger_condition=contribution.reason,
                observable_cues=[contribution.model_dump(mode="json")],
                calculation_basis={
                    "method_id": "legacy_envelope_contribution_v1",
                    "risk_side": "mixed",
                },
                source_refs=[],
                time_sensitivity={"session_phase_sensitive": False},
                trader_cognition_update={"state_of_play": [contribution.reason]},
                why_this_is_risk_not_play="Envelope contribution describes current environmental state and carries no execution authority.",
            )
        )
    return atoms


def _coerce_atom_state(state: str) -> ParallelRiskAtomStateValue:
    if state in {"inactive", "observe", "caution", "block"}:
        return state  # type: ignore[return-value]
    return "observe"
