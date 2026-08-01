from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.parallel_risk import (
    AuthorityFlags,
    ContributionBreakdownEntry,
    EventProximityRegisterEntry,
    FreshnessRegisterEntry,
    MissingSignalRegisterEntry,
    ParallelRiskMinuteProfile,
    RiskAtomState,
    RiskFamilyState,
    SignalSnapshotEntry,
)

FORBIDDEN_AUTHORITY_FIELD_NAMES = {
    "trade_recommendation",
    "order_instruction",
    "capital_size",
    "capital_sizing",
    "authorised_deployable_pct",
    "authorised_notional_usd",
    "position_size",
    "brokerage_order",
    "playbook_selection",
    "lead_playbook_id",
    "candidate_formation",
}


def test_parallel_risk_minute_profile_minimal_instantiates_and_serialises() -> None:
    profile = ParallelRiskMinuteProfile(
        packet_id="prl-minute-1",
        symbol="NVDA",
        source_time_utc=datetime(2026, 5, 18, 14, 30),
        generated_at_utc=datetime(2026, 5, 18, 14, 30, 1),
        session_state="opening",
        risk_envelope_state="observe",
        expected_signal_inventory_ref="workbook:Parallel Risk Lane Signal Inventory",
        vocabulary_dictionary_refs=["data/vocabulary/canonical_vocabulary.json"],
        description_template_id="prl.minute_profile.summary.v1",
        description_vocabulary_refs=["docs/vocabulary/vocabulary_registry.md#Parallel-Risk-Lane"],
    )

    payload = profile.model_dump()

    assert payload["lane_id"] == "parallel_risk_lane"
    assert payload["risk_envelope_state"] == "observe"
    assert payload["authority_flags"]["candidate_formation_allowed"] is False
    assert (
        payload["expected_signal_inventory_ref"] == "workbook:Parallel Risk Lane Signal Inventory"
    )
    assert payload["description_template_id"] == "prl.minute_profile.summary.v1"


@pytest.mark.parametrize(
    "field_name",
    [
        "candidate_formation_allowed",
        "playbook_selection_allowed",
        "capital_sizing_allowed",
        "broker_execution_allowed",
        "serial_stage_mutation_allowed",
        "review_judgement_authority",
        "direct_workbook_runtime_read_allowed",
    ],
)
def test_authority_flags_default_all_forbidden_capabilities_false(field_name: str) -> None:
    flags = AuthorityFlags()
    assert getattr(flags, field_name) is False


def test_authority_flags_reject_forbidden_capability_override() -> None:
    with pytest.raises(ValidationError, match="parallel_risk_authority_flags_must_remain_false"):
        AuthorityFlags(capital_sizing_allowed=True)


def test_risk_atom_state_supports_observe_caution_block_without_trade_action_fields() -> None:
    atoms = [
        RiskAtomState(
            risk_atom_id=f"atom-{state}",
            family="calendar_event",
            state=state,
            intensity=0.5,
            confidence=0.8,
            trigger_condition="scheduled event window active",
            calculation_basis={"method_id": "contract-only-fixture"},
            why_this_is_risk_not_play="Describes event sensitivity only; it does not select a trade.",
        )
        for state in ("observe", "caution", "block")
    ]

    assert [atom.state for atom in atoms] == ["observe", "caution", "block"]
    for forbidden_field in FORBIDDEN_AUTHORITY_FIELD_NAMES:
        assert forbidden_field not in RiskAtomState.model_fields


def test_signal_snapshot_entry_represents_present_missing_quarantined_and_stale_states() -> None:
    entries = [
        SignalSnapshotEntry(
            signal_id="vix_level",
            signal_family="macro_regime",
            raw_or_derived="raw",
            value=28.0,
            units="index_level",
            source_time_utc=datetime(2026, 5, 18, 14, 30),
            freshness_state="fresh",
            missing_or_quarantined="present",
        ),
        SignalSnapshotEntry(
            signal_id="vwap_distance",
            signal_family="market_microstructure",
            raw_or_derived="derived",
            value=None,
            units="bps",
            source_time_utc=None,
            freshness_state="unknown",
            missing_or_quarantined="missing",
        ),
        SignalSnapshotEntry(
            signal_id="headline_feed",
            signal_family="information_headline",
            raw_or_derived="raw",
            value=None,
            units=None,
            source_time_utc=None,
            freshness_state="unknown",
            missing_or_quarantined="quarantined",
            rejection_reason="source_not_typed_for_prl",
        ),
        SignalSnapshotEntry(
            signal_id="options_chain_snapshot",
            signal_family="options_convexity",
            raw_or_derived="raw",
            value=None,
            units="chain",
            source_time_utc=datetime(2026, 5, 18, 14, 0),
            freshness_state="stale",
            missing_or_quarantined="present",
        ),
    ]

    assert [entry.missing_or_quarantined for entry in entries] == [
        "present",
        "missing",
        "quarantined",
        "present",
    ]
    assert entries[-1].freshness_state == "stale"


def test_expected_signal_inventory_refs_are_metadata_only() -> None:
    profile = ParallelRiskMinuteProfile(
        packet_id="prl-minute-inventory-ref",
        symbol="NVDA",
        source_time_utc=datetime(2026, 5, 18, 14, 30),
        generated_at_utc=datetime(2026, 5, 18, 14, 30, 1),
        expected_signal_inventory_ref="workbook:data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx#Parallel Risk Lane Signal Inventory",
        workbook_lineage_refs=["Raw_Primitives_Catalog!A1:H49"],
    )

    payload = profile.model_dump()

    assert payload["expected_signal_inventory_ref"].endswith("#Parallel Risk Lane Signal Inventory")
    assert payload["workbook_lineage_refs"] == ["Raw_Primitives_Catalog!A1:H49"]
    assert profile.authority_flags.direct_workbook_runtime_read_allowed is False


def test_description_fields_are_template_and_vocabulary_references_only() -> None:
    profile = ParallelRiskMinuteProfile(
        packet_id="prl-minute-template-ref",
        symbol="NVDA",
        source_time_utc=datetime(2026, 5, 18, 14, 30),
        generated_at_utc=datetime(2026, 5, 18, 14, 30, 1),
        description_template_id="prl.minute_profile.summary.v1",
        description_vocabulary_refs=["data/vocabulary/canonical_vocabulary.json"],
    )

    assert profile.description_template_id == "prl.minute_profile.summary.v1"
    assert profile.description_vocabulary_refs == ["data/vocabulary/canonical_vocabulary.json"]
    for forbidden_field in FORBIDDEN_AUTHORITY_FIELD_NAMES | {"plain_english", "freeform_text"}:
        assert forbidden_field not in ParallelRiskMinuteProfile.model_fields


def test_register_and_contribution_contracts_remain_descriptive() -> None:
    missing = MissingSignalRegisterEntry(
        signal_id="vwap_distance",
        signal_family="market_microstructure",
        expected_reason="future inventory expects this after typed promotion",
        missing_reason="not_projected_into_prl",
        impact_on_profile="lowers_confidence",
    )
    freshness = FreshnessRegisterEntry(
        signal_id="vix_level",
        freshness_state="fresh",
        source_time_utc=datetime(2026, 5, 18, 14, 30),
        generated_at_utc=datetime(2026, 5, 18, 14, 30, 1),
    )
    event = EventProximityRegisterEntry(
        event_id="nvda_earnings_placeholder",
        event_type="earnings",
        proximity_seconds=900,
        risk_interpretation="event proximity context only",
    )
    family = RiskFamilyState(
        family="calendar_event",
        state="observe",
        intensity=0.2,
        confidence=0.7,
    )
    contribution = ContributionBreakdownEntry(
        contribution_id="event-window-contribution",
        family="calendar_event",
        state="observe",
        reason="scheduled event context present",
    )

    assert missing.impact_on_profile == "lowers_confidence"
    assert freshness.freshness_state == "fresh"
    assert event.risk_interpretation == "event proximity context only"
    assert family.state == "observe"
    assert contribution.reason == "scheduled event context present"
