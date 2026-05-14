"""Benchmark-owned state-conditioned modifier evaluation and application surfaces."""

from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy

from nvda_desk.config.coefficient_authority import CoefficientAuthorityService
from nvda_desk.contracts.execution import ExecutionExpressionOutput
from nvda_desk.contracts.modifiers import ModifierReplayReceipt, ModifierRuntimePacket
from nvda_desk.contracts.posture import PostureRiskOutput


class StateConditionedModifierService:
    """Coordinate bounded modifier packet construction and application."""

    def __init__(
        self, coefficient_authority_service: CoefficientAuthorityService | None = None
    ) -> None:
        self.coefficient_authority_service = (
            coefficient_authority_service or CoefficientAuthorityService()
        )

    def build_packet(
        self, *, active_modifier_ids: Iterable[str] = (), owner_stage: str = "posture"
    ) -> ModifierRuntimePacket:
        """Build one bounded modifier packet from the governed authority surface."""

        return self.coefficient_authority_service.build_modifier_packet(
            active_modifier_ids=active_modifier_ids,
            owner_stage=owner_stage,
        )

    def build_replay_receipt(
        self, *, active_modifier_ids: Iterable[str] = (), owner_stage: str = "posture"
    ) -> ModifierReplayReceipt:
        """Build a deterministic replay receipt from governed coefficient authority."""

        return self.coefficient_authority_service.build_replay_receipt(
            active_modifier_ids=active_modifier_ids,
            owner_stage=owner_stage,
        )

    def apply_posture_modifiers(
        self,
        *,
        posture: PostureRiskOutput,
        modifier_packet: ModifierRuntimePacket | None = None,
    ) -> PostureRiskOutput:
        """Apply modifier lineage to one posture envelope."""

        return apply_posture_modifiers(posture=posture, modifier_packet=modifier_packet)

    def apply_execution_modifiers(
        self,
        *,
        execution: ExecutionExpressionOutput,
        modifier_packet: ModifierRuntimePacket | None = None,
    ) -> ExecutionExpressionOutput:
        """Return the bounded execution output for the current admitted modifier scope."""

        return apply_execution_modifiers(execution=execution, modifier_packet=modifier_packet)


def build_modifier_packet(
    *,
    active_modifier_ids: Iterable[str] = (),
    owner_stage: str = "posture",
    coefficient_authority_service: CoefficientAuthorityService | None = None,
) -> ModifierRuntimePacket:
    """Build one modifier packet without exposing config-home internals to callers."""

    service = StateConditionedModifierService(coefficient_authority_service)
    return service.build_packet(active_modifier_ids=active_modifier_ids, owner_stage=owner_stage)


def apply_posture_modifiers(
    *,
    posture: PostureRiskOutput,
    modifier_packet: ModifierRuntimePacket | None = None,
) -> PostureRiskOutput:
    """Attach resolved coefficient lineage to one posture envelope."""

    envelope = deepcopy(dict(posture.local_envelope))
    if modifier_packet is not None:
        envelope["active_modifier_ids"] = list(modifier_packet.active_modifier_ids)
        envelope["resolved_surfaces"] = list(modifier_packet.resolved_surfaces)
        envelope["effective_coefficients"] = {
            coefficient.coefficient_id: coefficient.model_dump()
            for coefficient in modifier_packet.resolved_coefficients
        }
        for coefficient in modifier_packet.resolved_coefficients:
            envelope[coefficient.coefficient_id] = coefficient.effective_value
    return PostureRiskOutput(
        permission_state=posture.permission_state,
        local_envelope=envelope,
        hard_invariants=list(posture.hard_invariants),
        reasons=list(posture.reasons),
    )


def apply_execution_modifiers(
    *,
    execution: ExecutionExpressionOutput,
    modifier_packet: ModifierRuntimePacket | None = None,
) -> ExecutionExpressionOutput:
    """Preserve the current execution surface until execution-side modifiers are admitted."""

    del modifier_packet
    return ExecutionExpressionOutput.model_validate(execution.model_dump())
