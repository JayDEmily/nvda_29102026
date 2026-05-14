"""Typed bridge from intraday runtime outputs into carry-horizon evaluation."""

from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    InventoryState,
    LifecycleAction,
    OptionsFlowContextOutput,
    PostureRiskOutput,
    TemporalContextOutput,
)
from nvda_desk.schemas.overnight import (
    CarryAction,
    CarryHorizon,
    CloseStateCarryHandoff,
)


class CarryHandoffBuilder:
    """Build the typed close-state packet consumed by carry-horizon services.

    Purpose:
        Keep weekend and event carry logic in a separate branch while still using
        deterministic outputs from the intraday runtime.
    Inputs:
        Symbol, evaluation timestamp, and the upstream stage outputs needed to
        describe the close-state surface, including held-position context.
    Outputs:
        `CloseStateCarryHandoff` with explicit horizon taxonomy and allowed
        carry-action envelope.
    Determinism:
        Uses timestamp and stage outputs only; no live calls or hidden state.
    """

    def __init__(self, settings: Settings | None = None):
        self._settings = settings or Settings()
        self._tz = ZoneInfo(self._settings.market_timezone)

    def build(
        self,
        *,
        symbol: str,
        evaluation_ts: datetime,
        temporal: TemporalContextOutput,
        options_flow: OptionsFlowContextOutput,
        posture: PostureRiskOutput,
        inventory: InventoryState,
        execution: ExecutionExpressionOutput,
    ) -> CloseStateCarryHandoff:
        aware_ts = (
            evaluation_ts.astimezone(self._tz)
            if evaluation_ts.tzinfo
            else evaluation_ts.replace(tzinfo=self._tz)
        )
        next_session_open_ts = temporal.next_session_open_hint or self._next_session_open(aware_ts)
        weekend_window = (
            aware_ts.weekday() >= 5
            or "full_holiday" in temporal.calendar_closure_classes
            or (next_session_open_ts.date() - aware_ts.date()).days >= 2
        )
        event_carry_window = (
            temporal.event_window_state in {
                "event_imminent_window",
                "event_live_window",
                "event_cooling_off_window",
            }
            or temporal.event_carry_sensitivity in {"carry_sensitive", "next_session_memory"}
        )
        horizon = (
            CarryHorizon.WEEKEND
            if weekend_window
            else (CarryHorizon.EVENT_CARRY if event_carry_window else CarryHorizon.OVERNIGHT)
        )
        allowed_actions = self._allowed_actions(
            permission_state=posture.permission_state.value,
            horizon=horizon,
            event_carry_window=event_carry_window,
            thesis_state=posture.thesis_state,
            existing_inventory_pct=inventory.existing_inventory_pct,
            overnight_inventory_pct=inventory.overnight_inventory_pct,
            active_playbook_ids=execution.active_playbook_ids,
        )
        (
            allowed_actions,
            lifecycle_action_ceiling,
            lifecycle_rationale_codes,
        ) = self._apply_lifecycle_envelope(
            execution=execution,
            allowed_actions=allowed_actions,
            existing_inventory_pct=inventory.existing_inventory_pct,
            overnight_inventory_pct=inventory.overnight_inventory_pct,
        )
        recommended_action_ceiling = (
            lifecycle_action_ceiling
            or (allowed_actions[-1] if allowed_actions else CarryAction.BLOCK_CARRY)
        )
        rationale_codes: list[str] = [f"horizon:{horizon.value}"]
        if weekend_window:
            rationale_codes.append("weekend_window")
        if temporal.calendar_closure_classes:
            rationale_codes.append(f"calendar_closure:{','.join(temporal.calendar_closure_classes)}")
        if event_carry_window:
            rationale_codes.append("event_carry_window")
            rationale_codes.append(f"event_carry_sensitivity:{temporal.event_carry_sensitivity}")
        if posture.permission_state.value != "allow":
            rationale_codes.append(f"permission:{posture.permission_state.value}")
        if inventory.existing_inventory_pct > 0 or inventory.overnight_inventory_pct > 0:
            rationale_codes.append("existing_inventory_present")
        else:
            rationale_codes.append("no_existing_inventory")
        if execution.active_playbook_ids:
            rationale_codes.append("active_intraday_playbook_present")
        if posture.thesis_state != "valid":
            rationale_codes.append(f"thesis_state:{posture.thesis_state}")
        rationale_codes.extend(lifecycle_rationale_codes)
        lifecycle_plan = execution.lifecycle_plan
        return CloseStateCarryHandoff(
            symbol=symbol,
            evaluation_ts=aware_ts,
            horizon=horizon,
            next_session_open_ts=next_session_open_ts,
            weekend_window=weekend_window,
            event_carry_window=event_carry_window,
            close_phase=temporal.session_phase,
            desk_window=temporal.desk_window,
            event_window_state=temporal.event_window_state,
            expiry_cycle_state=temporal.expiry_cycle_state,
            permission_state=posture.permission_state.value,
            fresh_deployable_capital_pct=posture.fresh_deployable_capital_pct,
            overnight_deployable_capital_pct=posture.overnight_deployable_capital_pct,
            existing_inventory_pct=inventory.existing_inventory_pct,
            overnight_inventory_pct=inventory.overnight_inventory_pct,
            open_orders_count=inventory.open_orders_count,
            inventory_action_bias=posture.inventory_action_bias,
            thesis_state=posture.thesis_state,
            dealer_pressure_state=options_flow.dealer_pressure_state,
            pin_risk_state=options_flow.pin_risk_state,
            options_behavior_cluster=options_flow.options_behavior_cluster,
            active_family_ids=list(execution.active_family_ids),
            active_setup_variant_ids=list(execution.active_setup_variant_ids),
            active_playbook_ids=list(execution.active_playbook_ids),
            lifecycle_setup_variant_id=(lifecycle_plan.setup_variant_id if lifecycle_plan is not None else None),
            lifecycle_execution_expression_id=(
                lifecycle_plan.execution_expression_id if lifecycle_plan is not None else None
            ),
            lifecycle_state=(lifecycle_plan.lifecycle_state if lifecycle_plan is not None else None),
            lifecycle_next_action=(lifecycle_plan.next_action if lifecycle_plan is not None else None),
            lifecycle_carry_candidate=(
                lifecycle_plan.carry_candidate if lifecycle_plan is not None else False
            ),
            lifecycle_action_ceiling=lifecycle_action_ceiling,
            lifecycle_fired_rules=(list(lifecycle_plan.fired_rules) if lifecycle_plan is not None else []),
            lifecycle_blocked_rules=(list(lifecycle_plan.blocked_rules) if lifecycle_plan is not None else []),
            lifecycle_rationale_codes=(list(lifecycle_plan.rationale_codes) if lifecycle_plan is not None else []),
            recommended_action_ceiling=recommended_action_ceiling,
            allowed_actions=allowed_actions,
            rationale_codes=rationale_codes,
        )

    def _apply_lifecycle_envelope(
        self,
        *,
        execution: ExecutionExpressionOutput,
        allowed_actions: list[CarryAction],
        existing_inventory_pct: float,
        overnight_inventory_pct: float,
    ) -> tuple[list[CarryAction], CarryAction | None, list[str]]:
        lifecycle = execution.lifecycle_plan
        if lifecycle is None:
            return allowed_actions, None, []

        action_ceiling: CarryAction | None = None
        lifecycle_rationale_codes = [
            f"lifecycle_state:{lifecycle.lifecycle_state}",
            f"lifecycle_carry_candidate:{str(lifecycle.carry_candidate).lower()}",
        ]
        has_position = existing_inventory_pct > 0 or overnight_inventory_pct > 0

        if lifecycle.next_action is not None:
            lifecycle_rationale_codes.append(
                f"lifecycle_next_action:{lifecycle.next_action.value}"
            )

        if lifecycle.next_action is LifecycleAction.FLATTEN or lifecycle.must_flatten_by_close:
            return [CarryAction.FLATTEN], CarryAction.FLATTEN, [
                *lifecycle_rationale_codes,
                "lifecycle_ceiling:flatten",
            ]
        if lifecycle.next_action is LifecycleAction.BLOCK_CARRY:
            return [CarryAction.BLOCK_CARRY], CarryAction.BLOCK_CARRY, [
                *lifecycle_rationale_codes,
                "lifecycle_ceiling:block_carry",
            ]
        if lifecycle.carry_candidate and lifecycle.next_action is LifecycleAction.HOLD_SMALL_OVERNIGHT:
            bounded = [
                action
                for action in allowed_actions
                if action in {CarryAction.FLATTEN, CarryAction.HOLD_SMALL}
            ]
            return bounded or [CarryAction.FLATTEN], CarryAction.HOLD_SMALL, [
                *lifecycle_rationale_codes,
                "lifecycle_ceiling:hold_small",
            ]

        bounded = [
            action
            for action in allowed_actions
            if action in {CarryAction.FLATTEN, CarryAction.HOLD_SMALL}
        ]
        if not has_position:
            bounded = [action for action in bounded if action is CarryAction.FLATTEN]
            action_ceiling = CarryAction.FLATTEN
        elif CarryAction.HOLD_SMALL in bounded:
            action_ceiling = CarryAction.HOLD_SMALL
        elif CarryAction.FLATTEN in bounded:
            action_ceiling = CarryAction.FLATTEN
        return bounded or [CarryAction.FLATTEN], action_ceiling, [
            *lifecycle_rationale_codes,
            f"lifecycle_ceiling:{(action_ceiling or CarryAction.FLATTEN).value}",
        ]

    def _allowed_actions(
        self,
        *,
        permission_state: str,
        horizon: CarryHorizon,
        event_carry_window: bool,
        thesis_state: str,
        existing_inventory_pct: float,
        overnight_inventory_pct: float,
        active_playbook_ids: list[str],
    ) -> list[CarryAction]:
        if permission_state == "block":
            return [CarryAction.BLOCK_CARRY]
        if permission_state == "derisk":
            allowed = [CarryAction.FLATTEN, CarryAction.HOLD_SMALL]
        else:
            allowed = [
                CarryAction.FLATTEN,
                CarryAction.HOLD_SMALL,
                CarryAction.HOLD_BASELINE,
                CarryAction.ADD_CARRY,
            ]
        has_position = existing_inventory_pct > 0 or overnight_inventory_pct > 0
        has_active_intraday_thesis = bool(active_playbook_ids)
        if thesis_state != "valid":
            allowed = [
                action
                for action in allowed
                if action in {CarryAction.FLATTEN, CarryAction.HOLD_SMALL}
            ]
        if not has_position:
            allowed = [action for action in allowed if action is not CarryAction.HOLD_BASELINE]
            if not has_active_intraday_thesis:
                allowed = [action for action in allowed if action is CarryAction.FLATTEN]
        if horizon is CarryHorizon.WEEKEND and CarryAction.ADD_CARRY in allowed:
            allowed.remove(CarryAction.ADD_CARRY)
        if event_carry_window and CarryAction.ADD_CARRY in allowed:
            allowed.remove(CarryAction.ADD_CARRY)
        if not allowed:
            return [CarryAction.BLOCK_CARRY]
        return allowed

    def _next_session_open(self, aware_ts: datetime) -> datetime:
        candidate = aware_ts.replace(
            hour=self._settings.regular_open_hour,
            minute=self._settings.regular_open_minute,
            second=0,
            microsecond=0,
        )
        if aware_ts.weekday() < 5 and aware_ts < candidate:
            return candidate
        next_day = aware_ts + timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        return next_day.replace(
            hour=self._settings.regular_open_hour,
            minute=self._settings.regular_open_minute,
            second=0,
            microsecond=0,
        )
