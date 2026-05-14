from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, cast

from pydantic import BaseModel

if TYPE_CHECKING:
    from sqlalchemy.orm import Session, sessionmaker
else:
    Session = Any
    sessionmaker = Any

from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    FinalRiskJoinSurface,
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    PermissionState,
    PostureRiskOutput,
    TemporalContextInput,
    TemporalContextOutput,
    TerminalRiskApplicationSurface,
    TerminalRiskOverlapClass,
)
from nvda_desk.schemas.risk import (
    RiskAction,
    RiskDecision,
    RiskDecisionListResponse,
    RiskDecisionPayload,
    RiskPolicyInput,
)


class RiskGatewayService:
    def __init__(self, session_factory: sessionmaker[Session] | None = None):
        self._session_factory = session_factory

    def evaluate(self, payload: RiskPolicyInput) -> RiskDecision:
        reasons: list[str] = []
        action = RiskAction.ALLOW
        confidence_scalar = 1.0

        if payload.session_phase.value in {"closed", "after_hours"}:
            reasons.append("phase_no_trade_window")
            action = RiskAction.BLOCK
        if payload.data_age_seconds > 300:
            reasons.append("stale_market_state")
            action = RiskAction.BLOCK
        if payload.gross_exposure_pct >= 95 or payload.risk_budget_remaining_pct <= 5:
            reasons.append("exposure_or_budget_breached")
            action = RiskAction.BLOCK

        hard_conflicts = [tag for tag in payload.conflict_tags if tag.startswith("hard_veto:")]
        soft_conflicts = [tag for tag in payload.conflict_tags if not tag.startswith("hard_veto:")]
        if hard_conflicts:
            reasons.append("hard_conflict_block")
            action = RiskAction.BLOCK
        elif soft_conflicts and action is RiskAction.ALLOW:
            reasons.append("module_conflict_derisk")
            action = RiskAction.DERISK

        volatility_hot = (
            payload.vix_level >= payload.vix_hot_threshold
            or payload.vvix_level >= 115
            or payload.vix_change_pct_15m >= 18
            or payload.vvix_change_pct_15m >= 22
        )
        volatility_caution = (
            payload.vix_level >= payload.vix_caution_threshold
            or payload.vvix_level >= 95
            or payload.vix_change_pct_15m >= 8
            or payload.vvix_change_pct_15m >= 12
        )

        if volatility_hot:
            reasons.append("volatility_shock_block")
            action = RiskAction.BLOCK
        elif volatility_caution and action is RiskAction.ALLOW:
            reasons.append("volatility_caution_derisk")
            action = RiskAction.DERISK

        if payload.open_orders_count > 12 and action is RiskAction.ALLOW:
            reasons.append("order_pressure_derisk")
            action = RiskAction.DERISK

        if action is RiskAction.BLOCK:
            confidence_scalar = 0.0
        elif action is RiskAction.DERISK:
            confidence_scalar = 0.65
        if not reasons:
            reasons.append("risk_gateway_clear")

        return RiskDecision(
            action=action,
            reasons=reasons,
            confidence_scalar=confidence_scalar,
            vix_level=payload.vix_level,
            vvix_level=payload.vvix_level,
            vix_change_pct_15m=payload.vix_change_pct_15m,
            vvix_change_pct_15m=payload.vvix_change_pct_15m,
        )

    def evaluate_runtime_join(
        self,
        *,
        requested_at: datetime,
        temporal_input: TemporalContextInput,
        temporal: TemporalContextOutput,
        regime_input: MarketRegimeContextInput,
        options_flow_input: OptionsFlowContextInput,
        posture: PostureRiskOutput,
        execution: ExecutionExpressionOutput,
        inventory_state: InventoryState,
        risk_budget_remaining_pct: float,
        symbol: str = "NVDA",
    ) -> RiskDecision:
        overlay_decision = self.evaluate_overlay(
            requested_at=requested_at,
            temporal_input=temporal_input,
            temporal=temporal,
            regime_input=regime_input,
            options_flow_input=options_flow_input,
            posture=posture,
            execution=execution,
            inventory_state=inventory_state,
            risk_budget_remaining_pct=risk_budget_remaining_pct,
            symbol=symbol,
        )
        terminal_application = self.build_terminal_risk_application(
            overlay_decision=overlay_decision,
            posture=posture,
        )
        return terminal_application.final_decision

    def evaluate_overlay(
        self,
        *,
        requested_at: datetime,
        temporal_input: TemporalContextInput,
        temporal: TemporalContextOutput,
        regime_input: MarketRegimeContextInput,
        options_flow_input: OptionsFlowContextInput,
        posture: PostureRiskOutput,
        execution: ExecutionExpressionOutput,
        inventory_state: InventoryState,
        risk_budget_remaining_pct: float,
        symbol: str = "NVDA",
    ) -> RiskDecision:
        return self.evaluate(
            self._runtime_policy_input(
                requested_at=requested_at,
                temporal_input=temporal_input,
                temporal=temporal,
                regime_input=regime_input,
                options_flow_input=options_flow_input,
                posture=posture,
                execution=execution,
                inventory_state=inventory_state,
                risk_budget_remaining_pct=risk_budget_remaining_pct,
                symbol=symbol,
            )
        )

    def build_terminal_risk_application(
        self,
        *,
        overlay_decision: RiskDecision,
        posture: PostureRiskOutput,
    ) -> TerminalRiskApplicationSurface:
        action = overlay_decision.action
        reasons = list(overlay_decision.reasons)
        confidence_scalar = overlay_decision.confidence_scalar
        overlap_classes: list[TerminalRiskOverlapClass] = []
        notes = ["overlay_evaluation_preserved_before_terminal_application"]

        if posture.permission_state is PermissionState.BLOCK:
            action = RiskAction.BLOCK
            confidence_scalar = 0.0
            reasons = ["posture_block_join", *reasons]
            if overlay_decision.action is RiskAction.ALLOW:
                overlap_classes.append(
                    TerminalRiskOverlapClass.POSTURE_BLOCK_SUPERSEDES_OVERLAY_ALLOW
                )
            elif overlay_decision.action is RiskAction.DERISK:
                overlap_classes.append(
                    TerminalRiskOverlapClass.POSTURE_BLOCK_SUPERSEDES_OVERLAY_DERISK
                )
            else:
                overlap_classes.append(
                    TerminalRiskOverlapClass.POSTURE_BLOCK_ALIGNS_WITH_OVERLAY_BLOCK
                )
        elif posture.permission_state is PermissionState.DERISK and action is RiskAction.ALLOW:
            action = RiskAction.DERISK
            confidence_scalar = min(confidence_scalar, 0.65)
            reasons = ["posture_derisk_join", *reasons]
            overlap_classes.append(
                TerminalRiskOverlapClass.POSTURE_DERISK_SUPERSEDES_OVERLAY_ALLOW
            )
        elif action is RiskAction.DERISK:
            overlap_classes.append(TerminalRiskOverlapClass.OVERLAY_DERISK_NO_TERMINAL_OVERRIDE)
        elif action is RiskAction.BLOCK:
            overlap_classes.append(TerminalRiskOverlapClass.OVERLAY_BLOCK_NO_TERMINAL_OVERRIDE)
        else:
            overlap_classes.append(TerminalRiskOverlapClass.OVERLAY_ALLOW_NO_TERMINAL_OVERRIDE)

        if not reasons:
            reasons = ["risk_gateway_clear"]

        final_decision = RiskDecision(
            action=action,
            reasons=reasons,
            confidence_scalar=confidence_scalar,
            vix_level=overlay_decision.vix_level,
            vvix_level=overlay_decision.vvix_level,
            vix_change_pct_15m=overlay_decision.vix_change_pct_15m,
            vvix_change_pct_15m=overlay_decision.vvix_change_pct_15m,
        )
        return TerminalRiskApplicationSurface(
            posture_permission_state=posture.permission_state,
            overlay_decision=overlay_decision,
            final_decision=final_decision,
            overlap_classes=overlap_classes,
            notes=notes,
        )

    def _runtime_policy_input(
        self,
        *,
        requested_at: datetime,
        temporal_input: TemporalContextInput,
        temporal: TemporalContextOutput,
        regime_input: MarketRegimeContextInput,
        options_flow_input: OptionsFlowContextInput,
        posture: PostureRiskOutput,
        execution: ExecutionExpressionOutput,
        inventory_state: InventoryState,
        risk_budget_remaining_pct: float,
        symbol: str,
    ) -> RiskPolicyInput:
        return RiskPolicyInput(
            symbol=symbol,
            module_id=execution.lead_playbook_id or execution.lead_family_id or "desk_cognition_runtime",
            requested_at=requested_at,
            session_phase=temporal.session_phase,
            vix_level=regime_input.vix_level,
            vvix_level=regime_input.vvix_level,
            vix_change_pct_15m=self._vix_change_proxy(temporal_input, options_flow_input),
            vvix_change_pct_15m=self._vvix_change_proxy(temporal, regime_input, options_flow_input),
            data_age_seconds=0,
            gross_exposure_pct=inventory_state.existing_inventory_pct,
            risk_budget_remaining_pct=risk_budget_remaining_pct,
            open_orders_count=inventory_state.open_orders_count,
            conflict_tags=self._runtime_conflict_tags(posture, execution),
            vix_caution_threshold=execution.risk_vix_caution_threshold,
            vix_hot_threshold=execution.risk_vix_hot_threshold,
        )

    def apply_final_join(
        self,
        execution: ExecutionExpressionOutput,
        decision: RiskDecision,
    ) -> ExecutionExpressionOutput:
        pre_active = list(execution.active_playbook_ids)
        pre_lead = execution.lead_playbook_id
        pre_entry_style = execution.entry_style
        base_reasons = list(execution.reasons)
        geometry_notes = list(execution.geometry_notes)
        lineage_tags = [
            "joined_after:execution_synthesis",
            f"risk_action:{decision.action.value}",
            f"lead_before_join:{pre_lead or 'none'}",
        ]
        if any(reason.startswith("posture_") for reason in decision.reasons):
            lineage_tags.append("authority_source:posture")
        if any(
            "volatility" in reason or "order_pressure" in reason for reason in decision.reasons
        ):
            lineage_tags.append("authority_source:market_risk")

        if decision.action is RiskAction.BLOCK:
            geometry_notes.append("final_risk_block_execution")
            entry_style = (
                pre_entry_style
                if pre_lead is None and pre_entry_style in {"no_trade", "blocked"}
                else "final_risk_blocked"
            )
            return execution.model_copy(
                update={
                    "pre_final_risk_active_playbook_ids": pre_active,
                    "pre_final_risk_lead_playbook_id": pre_lead,
                    "pre_final_risk_entry_style": pre_entry_style,
                    "active_playbook_ids": [],
                    "active_setup_variant_ids": [],
                    "active_family_ids": [],
                    "lead_playbook_id": None,
                    "lead_setup_variant_id": None,
                    "lead_family_id": None,
                    "entry_style": entry_style,
                    "max_risk_per_trade": 0.0,
                    "ladder_spacing_bps": 0.0,
                    "max_chase_distance_bps": 0.0,
                    "stop_distance_bps": 0.0,
                    "take_profit_distance_bps": 0.0,
                    "hedge_ratio": 0.0,
                    "per_slice_risk_pct": 0.0,
                    "geometry_notes": geometry_notes,
                    "hedge_required": False,
                    "inventory_action": "reduce",
                    "fresh_capital_action": "block",
                    "scaling_plan": [],
                    "final_risk_join": FinalRiskJoinSurface(
                        action=decision.action,
                        confidence_scalar=decision.confidence_scalar,
                        reasons=list(decision.reasons),
                        lineage_tags=lineage_tags,
                        execution_effect="block_execution",
                    ),
                    "reasons": [*base_reasons, f"final_risk_join:{decision.action.value}"],
                }
            )

        if decision.action is RiskAction.DERISK:
            scalar = round(max(0.0, min(1.0, decision.confidence_scalar)), 4)
            geometry_notes.append("final_risk_derisk_execution")
            return execution.model_copy(
                update={
                    "pre_final_risk_active_playbook_ids": pre_active,
                    "pre_final_risk_lead_playbook_id": pre_lead,
                    "pre_final_risk_entry_style": pre_entry_style,
                    "scaling_plan": [round(value * scalar, 4) for value in execution.scaling_plan],
                    "max_risk_per_trade": round(execution.max_risk_per_trade * scalar, 4),
                    "max_chase_distance_bps": round(
                        execution.max_chase_distance_bps * scalar, 4
                    ),
                    "per_slice_risk_pct": round(execution.per_slice_risk_pct * scalar, 4),
                    "hedge_required": True,
                    "hedge_ratio": round(max(execution.hedge_ratio, 1.0 - scalar), 4),
                    "fresh_capital_action": "derisk",
                    "geometry_notes": geometry_notes,
                    "final_risk_join": FinalRiskJoinSurface(
                        action=decision.action,
                        confidence_scalar=decision.confidence_scalar,
                        reasons=list(decision.reasons),
                        lineage_tags=lineage_tags,
                        execution_effect="derisk_execution",
                    ),
                    "reasons": [*base_reasons, f"final_risk_join:{decision.action.value}"],
                }
            )

        return execution.model_copy(
            update={
                "pre_final_risk_active_playbook_ids": pre_active,
                "pre_final_risk_lead_playbook_id": pre_lead,
                "pre_final_risk_entry_style": pre_entry_style,
                "final_risk_join": FinalRiskJoinSurface(
                    action=decision.action,
                    confidence_scalar=decision.confidence_scalar,
                    reasons=list(decision.reasons),
                    lineage_tags=lineage_tags,
                    execution_effect="allow_as_computed",
                ),
                "reasons": [*base_reasons, f"final_risk_join:{decision.action.value}"],
            }
        )

    def _runtime_conflict_tags(
        self,
        posture: PostureRiskOutput,
        execution: ExecutionExpressionOutput,
    ) -> list[str]:
        conflict_tags: list[str] = []
        if posture.signal_conflict_state != "aligned_signals":
            conflict_tags.append(posture.signal_conflict_state)
        return conflict_tags

    def _vix_change_proxy(
        self,
        temporal_input: TemporalContextInput,
        options_flow_input: OptionsFlowContextInput,
    ) -> float:
        move_component = max(0.0, abs(temporal_input.intraday_move_pct) * 4.0)
        gamma_component = max(0.0, options_flow_input.gamma_pressure_score - 0.6) * 20.0
        return round(move_component + gamma_component, 4)

    def _vvix_change_proxy(
        self,
        temporal: TemporalContextOutput,
        regime_input: MarketRegimeContextInput,
        options_flow_input: OptionsFlowContextInput,
    ) -> float:
        skew_component = max(0.0, options_flow_input.put_call_skew - 0.35) * 30.0
        vol_of_vol_component = max(0.0, regime_input.vvix_level - 95.0) / 2.0
        time_component = 6.0 if temporal.event_window_state == "event_imminent_window" else 0.0
        return round(skew_component + vol_of_vol_component + time_component, 4)

    def record(self, payload: RiskPolicyInput) -> RiskDecisionPayload:
        if self._session_factory is None:
            raise RuntimeError("RiskGatewayService.record requires a session factory")
        from nvda_desk.db.models import RiskDecisionLog

        decision = self.evaluate(payload)
        with self._session_factory() as session:
            row = RiskDecisionLog(
                symbol=payload.symbol,
                module_id=payload.module_id,
                action=decision.action.value,
                requested_at=(
                    payload.requested_at.astimezone(UTC)
                    if payload.requested_at.tzinfo
                    else payload.requested_at.replace(tzinfo=UTC)
                ),
                input_json=self._dump_model(payload),
                output_json=self._dump_model(decision),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_payload(row)

    def list_decisions(
        self, module_id: str | None = None, limit: int = 20
    ) -> RiskDecisionListResponse:
        if self._session_factory is None:
            raise RuntimeError("RiskGatewayService.list_decisions requires a session factory")
        from sqlalchemy import desc, select

        from nvda_desk.db.models import RiskDecisionLog

        with self._session_factory() as session:
            stmt = select(RiskDecisionLog)
            if module_id:
                stmt = stmt.where(RiskDecisionLog.module_id == module_id)
            stmt = stmt.order_by(desc(RiskDecisionLog.created_at)).limit(limit)
            rows = list(session.scalars(stmt))
        return RiskDecisionListResponse(decisions=[self._to_payload(row) for row in rows])

    def _dump_model(self, model: BaseModel) -> str:
        return json.dumps(model.model_dump(mode="json"))

    def _to_payload(self, row: Any) -> RiskDecisionPayload:
        output_payload = dict(json.loads(row.output_json))
        return RiskDecisionPayload(
            decision_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            module_id=row.module_id,
            requested_at=row.requested_at,
            action=cast(RiskAction, row.action),
            reasons=list(output_payload.get("reasons", [])),
            confidence_scalar=float(output_payload.get("confidence_scalar", 0.0)),
            input_payload=dict(json.loads(row.input_json)),
            output_payload=output_payload,
        )
