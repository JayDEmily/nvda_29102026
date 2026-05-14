"""Posture, permission, and deployable-capital governance service.

This service converts temporal, regime, options, and inventory context into the
binding permission and deployable-capital state that downstream layers must obey.
"""

from __future__ import annotations

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.cognition import (
    BreadthState,
    PermissionState,
    PostureHardInvariantsSurface,
    PostureLocalEnvelopeSurface,
    PostureRiskInput,
    PostureRiskOutput,
    VolatilityRegime,
)


class PostureRiskService:
    """Derive binding posture and deployable-capital state.

    Purpose:
        Convert desk context plus inventory state into a typed permission gate.
    Inputs:
        `PostureRiskInput` carrying temporal, regime, options, inventory, and
        risk-budget state, including thesis lifecycle and time-stop controls.
    Outputs:
        `PostureRiskOutput` with explicit posture labels, permission,
        fresh-vs-inventory state, and deployable-capital controls.
    Determinism:
        Applies fixed thresholds in a stable order with no hidden persistence.
    """

    def evaluate(self, payload: PostureRiskInput) -> PostureRiskOutput:
        """Build posture, permission, and deployable-capital output."""

        inventory_posture_state = self._inventory_posture_state(payload)
        thesis_state = self._thesis_state(payload)
        capital_lockup_state = self._capital_lockup_state(payload.inventory.capital_lockup_pct)
        adverse_excursion_state = self._adverse_excursion_state(
            payload.inventory.adverse_excursion_pct
        )
        time_stop_state = self._time_stop_state(payload.inventory.time_stop_minutes_remaining)
        fresh_vs_inventory_state = self._fresh_vs_inventory_state(payload, inventory_posture_state)
        signal_conflict_state = self._signal_conflict_state(payload, inventory_posture_state)
        reasons: list[str] = [
            f"inventory_posture_state:{inventory_posture_state}",
            f"thesis_state:{thesis_state}",
            f"fresh_vs_inventory_state:{fresh_vs_inventory_state}",
            f"signal_conflict_state:{signal_conflict_state}",
            f"capital_lockup_state:{capital_lockup_state}",
            f"adverse_excursion_state:{adverse_excursion_state}",
            f"time_stop_state:{time_stop_state}",
        ]
        hard_block_reasons: list[str] = []
        derisk_reasons: list[str] = []
        permission_state = PermissionState.ALLOW
        posture_label = inventory_posture_state
        inventory_action_bias = "hold"
        fresh_deployable = min(payload.inventory.fresh_cash_pct, payload.risk_budget_remaining_pct)
        overnight_deployable = max(
            0.0, fresh_deployable - payload.inventory.overnight_inventory_pct
        )

        if payload.temporal.session_phase in {
            SessionClockPhase.CLOSED,
            SessionClockPhase.AFTER_HOURS,
        }:
            permission_state = PermissionState.BLOCK
            posture_label = "closed_window"
            hard_block_reasons.append("temporal_no_trade_window")
            reasons.append("temporal_no_trade_window")
        if thesis_state == "broken":
            permission_state = PermissionState.BLOCK
            posture_label = "thesis_invalidated"
            hard_block_reasons.append("thesis_invalidated")
            reasons.append("thesis_invalidated")
        if adverse_excursion_state == "excursion_breached":
            permission_state = PermissionState.BLOCK
            posture_label = "adverse_excursion_stop"
            hard_block_reasons.append("adverse_excursion_breached")
            reasons.append("adverse_excursion_breached")
        if time_stop_state == "time_stop_elapsed":
            permission_state = PermissionState.BLOCK
            posture_label = "time_stop_elapsed"
            hard_block_reasons.append("time_stop_elapsed")
            reasons.append("time_stop_elapsed")
        if inventory_posture_state == "capital_locked":
            permission_state = PermissionState.BLOCK
            posture_label = "capital_locked"
            hard_block_reasons.append("capital_locked")
            reasons.append("capital_locked")

        if permission_state is not PermissionState.BLOCK:
            if payload.regime.volatility_regime is VolatilityRegime.STRESSED:
                permission_state = PermissionState.DERISK
                posture_label = "stress_derisk"
                derisk_reasons.append("stressed_volatility_regime")
                reasons.append("stressed_volatility_regime")
            if payload.regime.breadth_state is BreadthState.WEAK:
                permission_state = PermissionState.DERISK
                posture_label = "weak_breadth_derisk"
                derisk_reasons.append("weak_breadth")
                reasons.append("weak_breadth")
            if (
                payload.options_flow.options_behavior_cluster == "negative_gamma_flush"
                and payload.regime.breadth_state is BreadthState.WEAK
            ):
                permission_state = PermissionState.DERISK
                posture_label = "negative_gamma_flush"
                derisk_reasons.append("negative_gamma_flush")
                reasons.append("negative_gamma_flush")
            if signal_conflict_state != "aligned_signals":
                permission_state = PermissionState.DERISK
                posture_label = "signal_conflict_derisk"
                derisk_reasons.append("signal_conflict_detected")
                reasons.append("signal_conflict_detected")
            if inventory_posture_state in {"trapped", "full"}:
                permission_state = PermissionState.DERISK
                posture_label = inventory_posture_state
                derisk_reasons.append(f"inventory_posture:{inventory_posture_state}")
                reasons.append(f"inventory_posture:{inventory_posture_state}")
            if fresh_vs_inventory_state in {"inventory_locked", "inventory_only"}:
                permission_state = PermissionState.DERISK
                posture_label = fresh_vs_inventory_state
                derisk_reasons.append(f"fresh_vs_inventory:{fresh_vs_inventory_state}")
                reasons.append(f"fresh_vs_inventory:{fresh_vs_inventory_state}")
            if time_stop_state == "time_stop_near":
                permission_state = PermissionState.DERISK
                posture_label = "time_stop_near"
                derisk_reasons.append("time_stop_near")
                reasons.append("time_stop_near")

        if permission_state is PermissionState.BLOCK:
            fresh_deployable = 0.0
            overnight_deployable = 0.0
            inventory_action_bias = "reduce"
        elif permission_state is PermissionState.DERISK:
            fresh_deployable = round(
                min(
                    fresh_deployable,
                    (
                        15.0
                        if payload.options_flow.options_behavior_cluster == "negative_gamma_flush"
                        else 30.0
                    ),
                ),
                4,
            )
            overnight_deployable = round(min(overnight_deployable, 10.0), 4)
            if inventory_posture_state in {"trapped", "full"}:
                inventory_action_bias = "trim"
            elif payload.options_flow.gamma_state.value == "destabilising":
                inventory_action_bias = "hedge"
            else:
                inventory_action_bias = "hold"
        else:
            fresh_deployable = round(min(fresh_deployable, 55.0), 4)
            overnight_deployable = round(min(overnight_deployable, 20.0), 4)
            inventory_action_bias = (
                "add" if fresh_vs_inventory_state == "fresh_capital_available" else "hold"
            )

        thesis_pressure_score = round(
            min(
                1.0,
                max(
                    0.0,
                    (payload.inventory.capital_lockup_pct / 100.0 * 0.25)
                    + (min(abs(payload.inventory.adverse_excursion_pct), 15.0) / 15.0 * 0.25)
                    + (0.20 if thesis_state == "fragile" else 0.0)
                    + (0.15 if signal_conflict_state != "aligned_signals" else 0.0)
                    + (0.25 if time_stop_state == "time_stop_near" else 0.0)
                    + (0.35 if time_stop_state == "time_stop_elapsed" else 0.0),
                ),
            ),
            4,
        )

        return PostureRiskOutput(
            permission_state=permission_state,
            posture_label=posture_label,
            inventory_posture_state=inventory_posture_state,
            fresh_deployable_capital_pct=fresh_deployable,
            overnight_deployable_capital_pct=overnight_deployable,
            inventory_action_bias=inventory_action_bias,
            fresh_vs_inventory_state=fresh_vs_inventory_state,
            thesis_state=thesis_state,
            capital_lockup_state=capital_lockup_state,
            adverse_excursion_state=adverse_excursion_state,
            time_stop_state=time_stop_state,
            signal_conflict_state=signal_conflict_state,
            time_stop_minutes_remaining=payload.inventory.time_stop_minutes_remaining,
            thesis_pressure_score=thesis_pressure_score,
            hard_invariants=PostureHardInvariantsSurface(
                block_active=permission_state is PermissionState.BLOCK,
                hard_block_reasons=hard_block_reasons,
                zero_deployable_required=permission_state is PermissionState.BLOCK,
            ),
            local_envelope=PostureLocalEnvelopeSurface(
                base_permission_state=permission_state,
                base_posture_label=posture_label,
                inventory_posture_state=inventory_posture_state,
                fresh_vs_inventory_state=fresh_vs_inventory_state,
                thesis_state=thesis_state,
                capital_lockup_state=capital_lockup_state,
                adverse_excursion_state=adverse_excursion_state,
                time_stop_state=time_stop_state,
                signal_conflict_state=signal_conflict_state,
                base_fresh_deployable_capital_pct=fresh_deployable,
                base_overnight_deployable_capital_pct=overnight_deployable,
                base_inventory_action_bias=inventory_action_bias,
                time_stop_minutes_remaining=payload.inventory.time_stop_minutes_remaining,
                thesis_pressure_score=thesis_pressure_score,
                derisk_reasons=derisk_reasons,
            ),
            downstream_annotations=[],
            reasons=reasons,
        )

    def _inventory_posture_state(self, payload: PostureRiskInput) -> str:
        inventory = payload.inventory
        if inventory.existing_inventory_pct <= 0.0 and inventory.open_orders_count == 0:
            return "flat"
        if inventory.capital_lockup_pct >= 75.0 or (
            inventory.existing_inventory_pct >= 70.0 and inventory.fresh_cash_pct <= 15.0
        ):
            return "capital_locked"
        if inventory.cost_basis_gap_pct <= -6.0 and inventory.existing_inventory_pct >= 20.0:
            return "trapped"
        if inventory.existing_inventory_pct <= 10.0:
            return "probe"
        if inventory.existing_inventory_pct >= 50.0:
            return "full"
        return "normal"

    def _thesis_state(self, payload: PostureRiskInput) -> str:
        raw_state = payload.inventory.thesis_state_input.lower()
        if raw_state in {"broken", "invalid"}:
            return "broken"
        if raw_state in {"fragile", "stress_tested"}:
            return "fragile"
        if payload.inventory.cost_basis_gap_pct <= -8.0:
            return "fragile"
        return "valid"

    def _fresh_vs_inventory_state(
        self, payload: PostureRiskInput, inventory_posture_state: str
    ) -> str:
        inventory = payload.inventory
        if inventory_posture_state in {"capital_locked", "trapped"}:
            return "inventory_locked"
        if inventory.fresh_cash_pct <= 10.0 and inventory.existing_inventory_pct >= 25.0:
            return "inventory_only"
        if inventory.fresh_cash_pct >= 30.0 and inventory.existing_inventory_pct <= 20.0:
            return "fresh_capital_available"
        return "balanced_capital_mix"

    def _signal_conflict_state(
        self, payload: PostureRiskInput, inventory_posture_state: str
    ) -> str:
        conflict_tags: list[str] = []
        if payload.regime.signal_conflict_state != "aligned_regime":
            conflict_tags.append(payload.regime.signal_conflict_state)
        if (
            payload.regime.sector_leadership_state == "semis_leading"
            and payload.regime.breadth_state is BreadthState.SUPPORTIVE
            and payload.options_flow.options_behavior_cluster == "negative_gamma_flush"
        ):
            conflict_tags.append("leadership_vs_hostile_options")
        if (
            inventory_posture_state in {"trapped", "capital_locked"}
            and payload.options_flow.gamma_state.value == "destabilising"
        ):
            conflict_tags.append("inventory_stress_with_destabilising_gamma")
        if payload.options_flow.options_behavior_cluster == "event_suppressed":
            conflict_tags.append("event_suppressed")
        return "aligned_signals" if not conflict_tags else "conflicted_signals"

    def _capital_lockup_state(self, capital_lockup_pct: float) -> str:
        if capital_lockup_pct >= 70.0:
            return "lockup_high"
        if capital_lockup_pct >= 40.0:
            return "lockup_moderate"
        return "lockup_low"

    def _adverse_excursion_state(self, adverse_excursion_pct: float) -> str:
        if adverse_excursion_pct <= -10.0:
            return "excursion_breached"
        if adverse_excursion_pct <= -5.0:
            return "excursion_elevated"
        return "excursion_tolerable"

    def _time_stop_state(self, time_stop_minutes_remaining: int | None) -> str:
        if time_stop_minutes_remaining is None:
            return "time_stop_unset"
        if time_stop_minutes_remaining == 0:
            return "time_stop_elapsed"
        if time_stop_minutes_remaining <= 15:
            return "time_stop_near"
        return "time_stop_buffered"
