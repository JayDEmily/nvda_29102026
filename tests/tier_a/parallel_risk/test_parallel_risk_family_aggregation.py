from __future__ import annotations

from nvda_desk.contracts.parallel_risk import RiskAtomState
from nvda_desk.domain.parallel_risk.family_aggregation import aggregate_risk_family_states


def _atom(
    atom_id: str, family: str, state: str, intensity: float, confidence: float
) -> RiskAtomState:
    return RiskAtomState(
        risk_atom_id=atom_id,
        family=family,
        state=state,
        intensity=intensity,
        confidence=confidence,
        trigger_condition="fixture",
        why_this_is_risk_not_play="Family aggregation describes terrain only.",
    )


def test_family_aggregation_uses_highest_state_and_max_intensity_without_action_authority() -> None:
    families = aggregate_risk_family_states(
        [
            _atom("a1", "calendar_event", "observe", 0.2, 0.8),
            _atom("a2", "calendar_event", "caution", 0.7, 0.6),
            _atom("a3", "operational_tooling", "observe", 0.3, 0.9),
        ]
    )

    by_family = {item.family: item for item in families}
    assert by_family["calendar_event"].state == "caution"
    assert by_family["calendar_event"].intensity == 0.7
    assert by_family["calendar_event"].confidence == 0.6
    assert by_family["calendar_event"].dominant_atoms == ["a2"]
    assert by_family["operational_tooling"].state == "observe"


def test_family_aggregation_empty_atoms_returns_empty_list() -> None:
    assert aggregate_risk_family_states([]) == []
