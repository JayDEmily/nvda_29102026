"""Risk-family aggregation for supported Parallel Risk Lane atoms."""

from __future__ import annotations

from collections import defaultdict

from nvda_desk.contracts.parallel_risk import (
    ParallelRiskAtomStateValue,
    RiskAtomState,
    RiskFamilyState,
)

_STATE_RANK: dict[ParallelRiskAtomStateValue, int] = {
    "inactive": 0,
    "observe": 1,
    "caution": 2,
    "block": 3,
}


def aggregate_risk_family_states(atoms: list[RiskAtomState]) -> list[RiskFamilyState]:
    """Aggregate atom states into family-level descriptive state.

    The output is a state-of-play summary only; it carries no capital, playbook, or order
    authority.
    """

    grouped: dict[str, list[RiskAtomState]] = defaultdict(list)
    for atom in atoms:
        grouped[atom.family].append(atom)

    families: list[RiskFamilyState] = []
    for family, family_atoms in sorted(grouped.items()):
        highest_rank = max(_STATE_RANK[atom.state] for atom in family_atoms)
        state = next(key for key, rank in _STATE_RANK.items() if rank == highest_rank)
        max_intensity = max(atom.intensity for atom in family_atoms)
        confidence = min(atom.confidence for atom in family_atoms)
        dominant_atoms = sorted(
            atom.risk_atom_id
            for atom in family_atoms
            if _STATE_RANK[atom.state] == highest_rank and atom.intensity == max_intensity
        )
        if not dominant_atoms:
            dominant_atoms = sorted(
                atom.risk_atom_id
                for atom in family_atoms
                if _STATE_RANK[atom.state] == highest_rank
            )
        families.append(
            RiskFamilyState(
                family=family,
                state=state,
                intensity=max_intensity,
                confidence=confidence,
                dominant_atoms=dominant_atoms,
                notes=["state_of_play_aggregation_only"],
            )
        )
    return families
