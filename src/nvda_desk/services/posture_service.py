"""Coordinate bounded posture evaluation."""

from __future__ import annotations

from collections.abc import Iterable

from nvda_desk.cognition.modifiers.state_conditioned import StateConditionedModifierService
from nvda_desk.cognition.serial.posture import evaluate_posture
from nvda_desk.contracts.modifiers import ModifierRuntimePacket
from nvda_desk.contracts.posture import PostureRiskOutput
from nvda_desk.contracts.regime import MarketRegimeContextOutput


class PostureService:
    """Coordinate posture evaluation without absorbing domain logic."""

    def __init__(self, modifier_service: StateConditionedModifierService | None = None) -> None:
        self.modifier_service = modifier_service or StateConditionedModifierService()

    def evaluate(
        self,
        *,
        regime: MarketRegimeContextOutput,
        active_modifier_ids: Iterable[str] = (),
        modifier_packet: ModifierRuntimePacket | None = None,
    ) -> PostureRiskOutput:
        coefficient_values = self.modifier_service.coefficient_authority_service.baseline_value_map(
            owner_stage="posture"
        )
        resolved_packet = modifier_packet or self.modifier_service.build_packet(
            active_modifier_ids=active_modifier_ids,
            owner_stage="posture",
        )
        return evaluate_posture(
            regime=regime,
            coefficient_values=coefficient_values,
            modifier_packet=resolved_packet,
        )
