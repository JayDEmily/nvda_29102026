from __future__ import annotations

from datetime import datetime

from nvda_desk.contracts.parallel_risk import (
    EventProximityRegisterEntry,
    FreshnessRegisterEntry,
    MissingSignalRegisterEntry,
    ParallelRiskEnvelope,
    ParallelRiskEnvelopeContribution,
)
from nvda_desk.domain.parallel_risk.risk_atoms import build_supported_risk_atoms


def test_supported_risk_atoms_wrap_current_environmental_inputs_without_trade_actions() -> None:
    atoms = build_supported_risk_atoms(
        freshness_entries=[
            FreshnessRegisterEntry(
                signal_id="vix_level",
                freshness_state="fresh",
                impact_on_profile="freshness_supports_current_state_read",
            )
        ],
        missing_signal_entries=[
            MissingSignalRegisterEntry(
                signal_id="vwap_distance",
                signal_family="market_microstructure",
                expected_reason="future inventory expects it",
                missing_reason="not_projected_into_prl",
                impact_on_profile="lowers_confidence",
            )
        ],
        event_proximity_entries=[
            EventProximityRegisterEntry(
                event_id="earnings-nvda",
                event_type="earnings",
                proximity_seconds=1200,
                risk_interpretation="event_proximity_state_of_play_only",
                runtime_tags=["scheduled_event_window_active"],
            )
        ],
        envelope=ParallelRiskEnvelope(
            envelope_state="caution",
            contributions=[
                ParallelRiskEnvelopeContribution(
                    source_family="market_volatility_context",
                    state="caution",
                    reason="vix_elevated",
                ),
                ParallelRiskEnvelopeContribution(
                    source_family="options_repricing_context",
                    state="caution",
                    reason="front_term_structure_backwardation",
                ),
            ],
            caution_flags=["vix_elevated", "front_term_structure_backwardation"],
        ),
        generated_at_utc=datetime(2026, 5, 18, 14, 30),
    )

    ids = {atom.risk_atom_id for atom in atoms}
    assert ids >= {
        "freshness:vix_level",
        "signal_availability:vwap_distance",
        "event_proximity:earnings-nvda",
        "envelope:market_volatility_context:vix_elevated",
        "envelope:options_repricing_context:front_term_structure_backwardation",
    }
    assert all(atom.why_this_is_risk_not_play for atom in atoms)
    serialized = " ".join(atom.model_dump_json() for atom in atoms)
    for forbidden in ("buy", "sell", "fade", "chase", "hedge", "size up", "order"):
        assert forbidden not in serialized


def test_supported_risk_atoms_preserve_constructive_and_uncertainty_semantics() -> None:
    atoms = build_supported_risk_atoms(
        freshness_entries=[
            FreshnessRegisterEntry(
                signal_id="source_time",
                freshness_state="fresh",
                impact_on_profile="freshness_supports_current_state_read",
            )
        ],
        missing_signal_entries=[],
        event_proximity_entries=[],
        envelope=ParallelRiskEnvelope(),
        generated_at_utc=datetime(2026, 5, 18, 14, 30),
    )

    atom = atoms[0]
    assert atom.state == "observe"
    assert atom.calculation_basis["risk_side"] == "constructive"
    assert atom.confidence > 0.0
