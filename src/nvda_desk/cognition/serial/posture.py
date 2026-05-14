"""Evaluate bounded posture outputs."""

from __future__ import annotations

from collections.abc import Mapping

from nvda_desk.cognition.modifiers.state_conditioned import apply_posture_modifiers
from nvda_desk.contracts.modifiers import ModifierRuntimePacket
from nvda_desk.contracts.posture import PostureRiskOutput
from nvda_desk.contracts.regime import MarketRegimeContextOutput
from nvda_desk.domain.posture.permission import evaluate_permission


def evaluate_posture(
    *,
    regime: MarketRegimeContextOutput,
    coefficient_values: Mapping[str, float | bool] | None = None,
    modifier_packet: ModifierRuntimePacket | None = None,
) -> PostureRiskOutput:
    """Return one bounded posture evaluation."""

    base = evaluate_permission(regime=regime, coefficient_values=coefficient_values)
    return apply_posture_modifiers(posture=base, modifier_packet=modifier_packet)
