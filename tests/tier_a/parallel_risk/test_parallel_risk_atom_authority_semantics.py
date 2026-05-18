from __future__ import annotations

from nvda_desk.contracts.parallel_risk import ParallelRiskMinuteProfile, RiskAtomState

FORBIDDEN_ACTION_TERMS = {
    "buy",
    "sell",
    "fade",
    "chase",
    "hedge",
    "size up",
    "stand down",
    "take the trade",
    "avoid the trade",
    "order_instruction",
    "trade_recommendation",
    "capital_size",
    "playbook_selection",
}


def test_risk_atom_schema_does_not_expose_trade_action_authority_fields() -> None:
    fields = set(RiskAtomState.model_fields)
    for forbidden in FORBIDDEN_ACTION_TERMS:
        assert forbidden not in fields


def test_risk_atom_can_describe_mixed_state_of_play_without_action_terms() -> None:
    atom = RiskAtomState(
        risk_atom_id="event_proximity:earnings",
        family="calendar_event",
        state="observe",
        intensity=0.5,
        confidence=0.7,
        trigger_condition="earnings event near current market minute",
        calculation_basis={"risk_side": "mixed"},
        trader_cognition_update={
            "opportunity_side": ["event risk may be more explicitly priced"],
            "fragility_side": ["environment can reprice quickly"],
            "uncertainty_side": ["path remains unresolved"],
            "consequence_side": ["being wrong can become expensive faster"],
        },
        why_this_is_risk_not_play="Describes the terrain only; downstream systems own action decisions.",
    )

    payload = atom.model_dump_json()
    for forbidden in FORBIDDEN_ACTION_TERMS:
        assert forbidden not in payload


def test_minute_profile_authority_flags_remain_default_deny_with_atoms_present() -> None:
    profile = ParallelRiskMinuteProfile(
        packet_id="profile-with-atom",
        symbol="NVDA",
        source_time_utc="2026-05-18T14:30:00Z",
        generated_at_utc="2026-05-18T14:30:01Z",
        active_risk_atoms=[
            RiskAtomState(
                risk_atom_id="freshness:vix_level",
                family="operational_tooling",
                state="observe",
                trigger_condition="freshness_state=fresh",
                why_this_is_risk_not_play="Freshness supports confidence only; it is not action authority.",
            )
        ],
    )

    assert profile.authority_flags.candidate_formation_allowed is False
    assert profile.authority_flags.playbook_selection_allowed is False
    assert profile.authority_flags.capital_sizing_allowed is False
    assert profile.authority_flags.broker_execution_allowed is False
    assert profile.authority_flags.direct_workbook_runtime_read_allowed is False
