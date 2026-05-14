"""Downstream capital-deployment authority service.

Purpose:
    Decide whether an already-formed opening candidate deserves fresh capital
    now, and if so how much notional is authorised.
Inputs:
    `CapitalDeploymentAuthorityInput` carrying posture, eligibility,
    execution, preserved handoff/risk carriage, and the current capital
    snapshot.
Outputs:
    `CapitalDeploymentAuthorityDecision` with a bounded deploy-or-stand-down
    action, authorised percentage, authorised notional, and rationale codes.
Determinism:
    Uses fixed precedence rules over existing runtime surfaces; it does not
    recalculate upstream cognition or introduce recommendation memory.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentAuthorityDecision,
    CapitalDeploymentAuthorityInput,
)
from nvda_desk.schemas.risk import RiskAction
from nvda_desk.services.downstream_seam_checkpointing import (
    CHECKPOINT_CDA_DECISION_OBSERVED,
    checkpoint_observation,
)


class CapitalDeploymentAuthorityService:
    """Authorise bounded fresh-capital deployment from existing runtime truth."""

    def evaluate(
        self,
        payload: CapitalDeploymentAuthorityInput,
    ) -> CapitalDeploymentAuthorityDecision:
        """Return the bounded fresh-capital authority decision for one runtime pass."""

        buying_power = round(max(0.0, payload.capital_state.buying_power), 4)
        opportunity_target_pct = self._opportunity_target_pct(payload)
        posture_cap_pct = self._posture_cap_pct(payload)
        terminal_risk_action, terminal_risk_scalar, notes = self._terminal_risk_surface(payload)
        weather_state = payload.parallel_risk_lane_packet.required_market_translation_surface().environmental_weather_state.value
        consequence_class = payload.parallel_risk_lane_packet.required_candidate_audit_surface().consequence_class.value

        rationale_codes = [
            f"lead_playbook:{payload.execution.lead_playbook_id or 'none'}",
            f"posture_permission:{payload.posture.permission_state.value}",
            f"terminal_risk:{terminal_risk_action.value}",
            f"terminal_risk_scalar:{terminal_risk_scalar:.4f}",
            f"buying_power:{buying_power:.4f}",
            f"opportunity_target_pct:{opportunity_target_pct:.4f}",
            f"posture_cap_pct:{posture_cap_pct:.4f}",
            f"posture_cap_source:permission_state:{payload.posture.permission_state.value}",
            f"opportunity_source:{self._opportunity_target_source(payload)}",
        ]
        rationale_codes.append(f"weather_state:{weather_state}")
        rationale_codes.append(f"consequence_class:{consequence_class}")

        if payload.execution.lead_playbook_id is None:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:no_lead_playbook"],
                notes=notes,
            )

        if opportunity_target_pct <= 0.0:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:no_opening_capacity_from_recommendation"],
                notes=notes,
            )

        if terminal_risk_action is RiskAction.BLOCK:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:terminal_block"],
                notes=notes,
            )

        if buying_power <= 0.0:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:no_buying_power"],
                notes=notes,
            )

        terminal_risk_cap_pct = round(opportunity_target_pct * terminal_risk_scalar, 4)
        authorised_pct = round(min(terminal_risk_cap_pct, posture_cap_pct), 4)
        authorised_notional_usd = round(buying_power * (authorised_pct / 100.0), 4)
        if authorised_pct <= 0.0 or authorised_notional_usd <= 0.0:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:no_authorised_capacity"],
                notes=notes,
            )

        return self._decision(
            payload=payload,
            deployment_action=CapitalDeploymentAuthorityAction.DEPLOY,
            buying_power=buying_power,
            opportunity_target_pct=opportunity_target_pct,
            posture_cap_pct=posture_cap_pct,
            authorised_deployable_pct=authorised_pct,
            authorised_notional_usd=authorised_notional_usd,
            terminal_risk_action=terminal_risk_action,
            weather_state=weather_state,
            consequence_class=consequence_class,
            rationale_codes=[*rationale_codes, "deploy:bounded_fresh_capital_authorised"],
            notes=notes,
        )

    def _stand_down(
        self,
        *,
        payload: CapitalDeploymentAuthorityInput,
        buying_power: float,
        opportunity_target_pct: float,
        posture_cap_pct: float,
        terminal_risk_action: RiskAction,
        weather_state: str,
        consequence_class: str,
        rationale_codes: list[str],
        notes: list[str],
    ) -> CapitalDeploymentAuthorityDecision:
        return self._decision(
            payload=payload,
            deployment_action=CapitalDeploymentAuthorityAction.STAND_DOWN,
            buying_power=buying_power,
            opportunity_target_pct=opportunity_target_pct,
            posture_cap_pct=posture_cap_pct,
            authorised_deployable_pct=0.0,
            authorised_notional_usd=0.0,
            terminal_risk_action=terminal_risk_action,
            weather_state=weather_state,
            consequence_class=consequence_class,
            rationale_codes=rationale_codes,
            notes=notes,
        )

    def _decision(
        self,
        *,
        payload: CapitalDeploymentAuthorityInput,
        deployment_action: CapitalDeploymentAuthorityAction,
        buying_power: float,
        opportunity_target_pct: float,
        posture_cap_pct: float,
        authorised_deployable_pct: float,
        authorised_notional_usd: float,
        terminal_risk_action: RiskAction,
        weather_state: str,
        consequence_class: str,
        rationale_codes: list[str],
        notes: list[str],
    ) -> CapitalDeploymentAuthorityDecision:
        decision = CapitalDeploymentAuthorityDecision(
            deployment_action=deployment_action,
            lead_playbook_id=payload.execution.lead_playbook_id,
            opportunity_target_pct=opportunity_target_pct,
            posture_cap_pct=posture_cap_pct,
            authorised_deployable_pct=authorised_deployable_pct,
            authorised_notional_usd=authorised_notional_usd,
            available_buying_power_usd=buying_power,
            capital_source=payload.capital_state.source,
            terminal_risk_action=terminal_risk_action,
            environmental_weather_state=weather_state,
            consequence_class=consequence_class,
            rationale_codes=rationale_codes,
            notes=notes,
        )
        decision.checkpoint_observations.append(
            checkpoint_observation(
                checkpoint_name=CHECKPOINT_CDA_DECISION_OBSERVED,
                input_snapshot={
                    "lead_playbook_id": payload.execution.lead_playbook_id,
                    "permission_state": payload.posture.permission_state.value,
                    "terminal_risk_action": terminal_risk_action.value,
                    "weather_state": weather_state,
                    "consequence_class": consequence_class,
                    "buying_power": buying_power,
                    "opportunity_target_pct": opportunity_target_pct,
                    "posture_cap_pct": posture_cap_pct,
                },
                output_snapshot={
                    "deployment_action": decision.deployment_action.value,
                    "authorised_deployable_pct": decision.authorised_deployable_pct,
                    "authorised_notional_usd": decision.authorised_notional_usd,
                    "rationale_codes": list(decision.rationale_codes),
                },
            )
        )
        return decision

    def _terminal_risk_surface(
        self,
        payload: CapitalDeploymentAuthorityInput,
    ) -> tuple[RiskAction, float, list[str]]:
        decision = payload.stage_local_handoff.terminal_risk_application.final_decision
        return decision.action, self._terminal_risk_scalar(decision.action, decision.confidence_scalar), []

    def _posture_cap_pct(self, payload: CapitalDeploymentAuthorityInput) -> float:
        permission_state = payload.posture.permission_state.value
        if permission_state == "block":
            return 0.0
        if permission_state == "derisk":
            return 30.0
        return 55.0

    def _opportunity_target_pct(self, payload: CapitalDeploymentAuthorityInput) -> float:
        """Return the downstream deployable-total answer from posture and lawful serial shape."""

        shape_sum = round(sum(payload.execution.scaling_plan), 4) if payload.execution.scaling_plan else 0.0
        if shape_sum <= 0.0 or shape_sum > 1.0:
            return 0.0
        posture_total = round(max(0.0, min(100.0, payload.posture.fresh_deployable_capital_pct)), 4)
        return round(max(0.0, min(100.0, posture_total * shape_sum)), 4)

    def _opportunity_target_source(self, payload: CapitalDeploymentAuthorityInput) -> str:
        """Describe which bounded surface supplied the deployable-total answer."""

        shape_sum = round(sum(payload.execution.scaling_plan), 4) if payload.execution.scaling_plan else 0.0
        if shape_sum <= 0.0:
            return "no_opening_capacity"
        if shape_sum > 1.0:
            return "invalid_execution_scaling_plan_shape_sum_gt_1_0"
        return "posture_fresh_deployable_capital_pct_times_serial_shape"

    def _terminal_risk_scalar(self, action: RiskAction | None, confidence_scalar: float) -> float:
        """Return the bounded terminal-risk scalar used by CDA sizing only."""

        if action is RiskAction.BLOCK:
            return 0.0
        if action is RiskAction.DERISK:
            return round(max(0.0, min(1.0, confidence_scalar)), 4)
        return 1.0

