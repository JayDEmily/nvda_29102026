"""Expression and execution service for the Desk Cognition Grammar.

This service turns the admitted candidate pool into a concrete execution
recommendation, geometry packet, and invalidation scaffolding.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    CandidateAdjudicationRecord,
    ExecutionCandidateOwnershipSurface,
    ExecutionExpressionInput,
    ExecutionExpressionOutput,
    LifecycleAction,
    LifecyclePlanOutput,
    PlaybookCandidate,
    PlaybookDecision,
    PositionContextInput,
    TradableExpressionFamily,
)
from nvda_desk.schemas.playbook_registry import ExecutionTemplateSpec
from nvda_desk.schemas.state_policy import ModifierRuntimePacket, MutableRuntimeSurface
from nvda_desk.services.playbook_registry import PlaybookRegistryService


class ExecutionExpressionService:
    """Derive deterministic expression and execution outputs.

    Purpose:
        Turn the admitted candidate pool into a concrete execution recommendation
        and geometry packet.
    Inputs:
        `ExecutionExpressionInput` with posture, playbook eligibility, and options context.
        Posture is read for permission, lifecycle, and invalidation context only.
    Outputs:
        `ExecutionExpressionOutput` describing entry style, family/setup lineage,
        laddering, invalidation reasons, exits, and hedge need.
    Determinism:
        Uses checked-in registry order and execution templates with no hidden fallbacks.
    """

    _SPECIMEN_SETUP_VARIANT_ID = "opening_drive_continuation"
    _SPECIMEN_EXECUTION_EXPRESSION_ID = "continuation_ladder_exec"
    _SPECIMEN_LEGACY_PLAYBOOK_ID = "continuation_ladder"
    _SPECIMEN_TRADABLE_EXPRESSION_FAMILY = TradableExpressionFamily.SINGLE_LEG_CALL_DEBIT
    _SPECIMEN_LEGAL_LIFECYCLE_ACTIONS = [
        LifecycleAction.ADD,
        LifecycleAction.TRIM,
        LifecycleAction.FLATTEN,
        LifecycleAction.HOLD_SMALL_OVERNIGHT,
        LifecycleAction.BLOCK_CARRY,
    ]

    def __init__(self, registry_service: PlaybookRegistryService | None = None):
        self._registry = registry_service or PlaybookRegistryService()

    _SURFACE_DEFAULTS: dict[MutableRuntimeSurface, float | bool] = {
        MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR: 0.65,
        MutableRuntimeSurface.ZONE_SCORE_THRESHOLD: 0.50,
        MutableRuntimeSurface.DISTANCE_TO_VWAP_SOFT_LIMIT_PCT: 1.50,
        MutableRuntimeSurface.RISK_VIX_CAUTION_THRESHOLD: 24.0,
        MutableRuntimeSurface.RISK_VIX_HOT_THRESHOLD: 32.0,
        MutableRuntimeSurface.MAX_RISK_PER_TRADE: 0.35,
        MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT: 55.0,
        MutableRuntimeSurface.HEDGE_REQUIRED: False,
    }

    def evaluate(self, payload: ExecutionExpressionInput) -> ExecutionExpressionOutput:
        """Create deterministic expression and execution state for one snapshot."""

        candidate_index = {
            candidate.playbook_id: candidate for candidate in payload.eligibility.candidates
        }
        operative_surfaces = self._operative_surfaces(payload.modifier_runtime_packet)
        ordered_playbook_ids = self._registry.active_playbook_ids()
        registry_priority = {playbook_id: index + 1 for index, playbook_id in enumerate(ordered_playbook_ids)}
        eligible_candidates = [
            candidate_index[playbook_id]
            for playbook_id in ordered_playbook_ids
            if playbook_id in candidate_index
            and candidate_index[playbook_id].decision is PlaybookDecision.ELIGIBLE
        ]
        watch_playbook_ids = [
            playbook_id
            for playbook_id in ordered_playbook_ids
            if playbook_id in candidate_index
            and candidate_index[playbook_id].decision is PlaybookDecision.WATCH_ONLY
        ]
        adjudication = self._adjudicate_candidates(
            eligible_candidates=eligible_candidates,
            registry_priority=registry_priority,
            payload=payload,
        )
        active_playbook_ids = [entry.playbook_id for entry in adjudication]
        active_setup_variant_ids = self._ordered_unique(
            [entry.setup_variant_id for entry in adjudication if entry.setup_variant_id]
            + list(payload.eligibility.active_setup_variant_ids)
        )
        active_family_ids = self._ordered_unique(
            [entry.family_id for entry in adjudication if entry.family_id]
            + list(payload.eligibility.active_family_ids)
        )
        lead_playbook_id = active_playbook_ids[0] if active_playbook_ids else None
        lead_candidate = next(
            (candidate for candidate in eligible_candidates if candidate.playbook_id == lead_playbook_id),
            None,
        )
        lead_setup_variant_id = (
            lead_candidate.setup_variant_id if lead_candidate and lead_candidate.setup_variant_id else None
        ) or (active_setup_variant_ids[0] if active_setup_variant_ids else None)
        lead_family_id = (
            lead_candidate.family_id if lead_candidate and lead_candidate.family_id else None
        ) or (active_family_ids[0] if active_family_ids else None)
        contradiction_resolution = self._contradiction_resolution(adjudication)
        lead_selection_score = adjudication[0].score if adjudication else None
        lead_selection_reasons = list(adjudication[0].reasons) if adjudication else []
        reasons: list[str] = []
        invalidation_reasons: list[str] = []
        exit_reasons: list[str] = []
        playbook_execution_styles: dict[str, str] = {}
        setup_variant_execution_styles: dict[str, str] = {}
        passive_aggressive_bias = "balanced"
        ladder_spacing_bps = 0.0
        max_chase_distance_bps = 0.0
        stop_distance_bps = 0.0
        take_profit_distance_bps = 0.0
        hedge_ratio = 0.0
        per_slice_risk_pct = 0.0
        geometry_notes: list[str] = []

        if payload.posture.permission_state.value == "block":
            reasons.append("execution_blocked_by_permission")
            candidate_ownership = self._candidate_ownership_surface(
                payload=payload,
                adjudication=[],
                watch_playbook_ids=watch_playbook_ids,
                lead_playbook_id=None,
                contradiction_resolution=None,
                note="execution_skipped_after_posture_block",
            )
            position_context = self._normalise_position_context(
                payload=payload,
                lead_setup_variant_id=None,
                lead_playbook_id=None,
            )
            lifecycle_plan = self._build_lifecycle_plan(
                payload=payload,
                position_context=position_context,
                lead_setup_variant_id=None,
                lead_playbook_id=None,
                entry_style="no_trade",
                inventory_action="reduce",
                exit_reasons=["stand_aside_until_permission_clears"],
                target=0.0,
                scaling_plan=[],
            )
            return ExecutionExpressionOutput(
                active_playbook_ids=[],
                active_setup_variant_ids=[],
                active_family_ids=[],
                lead_playbook_id=None,
                lead_setup_variant_id=None,
                lead_family_id=None,
                adjudication_method="candidate_score_v1",
                contradiction_resolution=None,
                lead_selection_score=None,
                lead_selection_reasons=[],
                candidate_adjudication=[],
                entry_style="no_trade",
                playbook_execution_styles={},
                setup_variant_execution_styles={},
                entry_gate_score_floor=operative_surfaces["entry_gate_score_floor"],
                zone_score_threshold=operative_surfaces["zone_score_threshold"],
                distance_to_vwap_soft_limit_pct=operative_surfaces["distance_to_vwap_soft_limit_pct"],
                risk_vix_caution_threshold=operative_surfaces["risk_vix_caution_threshold"],
                risk_vix_hot_threshold=operative_surfaces["risk_vix_hot_threshold"],
                max_risk_per_trade=operative_surfaces["max_risk_per_trade"],
                passive_aggressive_bias="passive",
                ladder_spacing_bps=0.0,
                max_chase_distance_bps=0.0,
                stop_distance_bps=0.0,
                take_profit_distance_bps=0.0,
                hedge_ratio=0.0,
                per_slice_risk_pct=0.0,
                geometry_notes=["blocked_before_execution_geometry"],
                hedge_required=bool(operative_surfaces["hedge_required"]),
                inventory_action="reduce",
                fresh_capital_action="reduce",
                thesis_invalidation_state="defer_to_risk_gate",
                scaling_plan=[],
                invalidation_reasons=["risk_gate_blocked_execution"],
                exit_reasons=["stand_aside_until_permission_clears"],
                exit_plan=["stand_aside_until_permission_clears"],
                lifecycle_plan=lifecycle_plan,
                candidate_ownership=candidate_ownership,
                reasons=reasons,
            )

        hedge_required = bool(operative_surfaces["hedge_required"]) or (
            bool(payload.eligibility.hedge_candidates)
            or payload.options_flow.gamma_state.value == "destabilising"
        )

        if active_setup_variant_ids:
            assert lead_setup_variant_id is not None
            template = self._registry.template(
                self._registry.setup_variant(lead_setup_variant_id).execution_expression_id
            )
            entry_style = template.entry_style
            playbook_execution_styles = {
                playbook_id: self._registry.template_for_playbook(playbook_id).entry_style
                for playbook_id in active_playbook_ids
            }
            setup_variant_execution_styles = {
                setup_variant_id: self._registry.template(
                    self._registry.setup_variant(setup_variant_id).execution_expression_id
                ).entry_style
                for setup_variant_id in active_setup_variant_ids
            }
            target = 1.0 if lead_candidate is not None and template.scaling_step_factors else 0.0
            scaling_plan = [round(float(factor), 4) for factor in template.scaling_step_factors] if target > 0.0 else []
            thesis_invalidation_state = template.thesis_invalidation_state
            invalidation_reasons = self._invalidation_reasons(template, payload)
            exit_reasons = self._exit_reasons(template, payload)
            exit_plan = list(exit_reasons)
            inventory_action = self._inventory_action(payload, template)
            fresh_capital_action = template.default_fresh_capital_action
            (
                passive_aggressive_bias,
                ladder_spacing_bps,
                max_chase_distance_bps,
                stop_distance_bps,
                take_profit_distance_bps,
                hedge_ratio,
                per_slice_risk_pct,
                geometry_notes,
            ) = self._execution_geometry(
                template=template,
                payload=payload,
                target=target,
                scaling_plan=scaling_plan,
                operative_surfaces=operative_surfaces,
                hedge_required=hedge_required,
            )
            reasons.extend(f"active_family:{family_id}" for family_id in active_family_ids)
            reasons.extend(
                f"active_setup_variant:{setup_variant_id}"
                for setup_variant_id in active_setup_variant_ids
            )
            if lead_playbook_id is not None:
                reasons.append(f"lead_playbook:{lead_playbook_id}")
            if contradiction_resolution is not None:
                reasons.append(f"adjudication:{contradiction_resolution}")
            if lead_selection_score is not None:
                reasons.append(f"lead_score:{lead_selection_score}")
        elif watch_playbook_ids:
            lead_watch = watch_playbook_ids[0]
            template = self._registry.template_for_playbook(lead_watch)
            entry_style = "watch_only"
            playbook_execution_styles = {
                playbook_id: self._registry.template_for_playbook(playbook_id).watch_execution_style
                for playbook_id in watch_playbook_ids
            }
            setup_variant_execution_styles = {
                setup_variant_id: self._registry.template(
                    self._registry.setup_variant(setup_variant_id).execution_expression_id
                ).watch_execution_style
                for setup_variant_id in payload.eligibility.watch_setup_variant_ids
            }
            target = 0.0
            scaling_plan = []
            thesis_invalidation_state = "not_confirmed"
            invalidation_reasons = ["setup_needs_confirmation"]
            exit_reasons = ["remain_observational"]
            exit_plan = list(exit_reasons)
            inventory_action = "hold"
            fresh_capital_action = "hold"
            passive_aggressive_bias = "passive"
            geometry_notes = ["watch_only_no_execution_geometry"]
            reasons.append(f"watch_only_playbook:{lead_watch}")
        else:
            entry_style = "stand_aside"
            template = None
            target = 0.0
            scaling_plan = []
            thesis_invalidation_state = "no_valid_playbook"
            invalidation_reasons = payload.eligibility.no_trade_reasons or ["no_playbook_qualified"]
            exit_reasons = ["stand_aside"]
            exit_plan = list(exit_reasons)
            inventory_action = "hold"
            fresh_capital_action = "hold"
            passive_aggressive_bias = "passive"
            geometry_notes = ["no_active_setup_variant"]
            reasons.append("no_active_setup_variant")

        if hedge_required:
            reasons.append("hedge_required")
            hedge_exit_reason = (
                template.hedge_exit_reason
                if template is not None
                else "overlay_hedge_if_gamma_reaccelerates"
            )
            if hedge_exit_reason not in exit_reasons:
                exit_reasons.append(hedge_exit_reason)

        position_context = self._normalise_position_context(
            payload=payload,
            lead_setup_variant_id=lead_setup_variant_id,
            lead_playbook_id=lead_playbook_id,
        )
        lifecycle_plan = self._build_lifecycle_plan(
            payload=payload,
            position_context=position_context,
            lead_setup_variant_id=lead_setup_variant_id,
            lead_playbook_id=lead_playbook_id,
            entry_style=entry_style,
            inventory_action=inventory_action,
            exit_reasons=exit_reasons,
            target=target,
            scaling_plan=scaling_plan,
        )
        if lifecycle_plan is not None and self._is_specimen_position_context(position_context):
            inventory_action = self._lifecycle_inventory_action(
                lifecycle_plan=lifecycle_plan,
                fallback=inventory_action,
            )
            if lifecycle_plan.next_action in {
                LifecycleAction.TRIM,
                LifecycleAction.FLATTEN,
                LifecycleAction.HOLD_SMALL_OVERNIGHT,
                LifecycleAction.BLOCK_CARRY,
            }:
                fresh_capital_action = "hold"
            exit_reasons = self._merge_exit_reasons(exit_reasons, lifecycle_plan)
            exit_plan = self._merge_exit_plan(exit_plan, lifecycle_plan)

        candidate_ownership = self._candidate_ownership_surface(
            payload=payload,
            adjudication=adjudication,
            watch_playbook_ids=watch_playbook_ids,
            lead_playbook_id=lead_playbook_id,
            contradiction_resolution=contradiction_resolution,
            note=(
                "lead_selected_from_admitted_candidate_pool"
                if lead_playbook_id is not None
                else (
                    "watch_only_candidates_not_promoted_to_execution"
                    if watch_playbook_ids
                    else "no_admitted_candidate_promoted"
                )
            ),
        )

        return ExecutionExpressionOutput(
            active_playbook_ids=active_playbook_ids,
            active_setup_variant_ids=active_setup_variant_ids,
            active_family_ids=active_family_ids,
            lead_playbook_id=lead_playbook_id,
            lead_setup_variant_id=lead_setup_variant_id,
            lead_family_id=lead_family_id,
            adjudication_method="candidate_score_v1",
            contradiction_resolution=contradiction_resolution,
            lead_selection_score=lead_selection_score,
            lead_selection_reasons=lead_selection_reasons,
            candidate_adjudication=adjudication,
            entry_style=entry_style,
            playbook_execution_styles=playbook_execution_styles,
            setup_variant_execution_styles=setup_variant_execution_styles,
            entry_gate_score_floor=operative_surfaces["entry_gate_score_floor"],
            zone_score_threshold=operative_surfaces["zone_score_threshold"],
            distance_to_vwap_soft_limit_pct=operative_surfaces["distance_to_vwap_soft_limit_pct"],
            risk_vix_caution_threshold=operative_surfaces["risk_vix_caution_threshold"],
            risk_vix_hot_threshold=operative_surfaces["risk_vix_hot_threshold"],
            max_risk_per_trade=operative_surfaces["max_risk_per_trade"],
            passive_aggressive_bias=passive_aggressive_bias,
            ladder_spacing_bps=ladder_spacing_bps,
            max_chase_distance_bps=max_chase_distance_bps,
            stop_distance_bps=stop_distance_bps,
            take_profit_distance_bps=take_profit_distance_bps,
            hedge_ratio=hedge_ratio,
            per_slice_risk_pct=per_slice_risk_pct,
            geometry_notes=geometry_notes,
            hedge_required=hedge_required,
            inventory_action=inventory_action,
            fresh_capital_action=fresh_capital_action,
            thesis_invalidation_state=thesis_invalidation_state,
            scaling_plan=scaling_plan,
            invalidation_reasons=invalidation_reasons,
            exit_reasons=exit_reasons,
            exit_plan=exit_plan,
            lifecycle_plan=lifecycle_plan,
            candidate_ownership=candidate_ownership,
            reasons=reasons,
        )

    def _candidate_ownership_surface(
        self,
        *,
        payload: ExecutionExpressionInput,
        adjudication: list[CandidateAdjudicationRecord],
        watch_playbook_ids: list[str],
        lead_playbook_id: str | None,
        contradiction_resolution: str | None,
        note: str,
    ) -> ExecutionCandidateOwnershipSurface:
        admissibility_surface = payload.eligibility.admissibility_surface
        admitted_playbook_ids = list(admissibility_surface.admissible_playbook_ids)
        watch_only_ids = list(admissibility_surface.watch_only_playbook_ids)
        return ExecutionCandidateOwnershipSurface(
            admitted_playbook_ids=admitted_playbook_ids,
            watch_only_playbook_ids=watch_only_ids,
            adjudicated_playbook_ids=[entry.playbook_id for entry in adjudication],
            lead_playbook_id=lead_playbook_id,
            contradiction_resolution=contradiction_resolution,
            notes=[
                "stage5_limited_to_admissibility_and_watch_status",
                "stage6_owns_candidate_ranking_and_lead_selection",
                note,
            ],
        )

    def _normalise_position_context(
        self,
        *,
        payload: ExecutionExpressionInput,
        lead_setup_variant_id: str | None,
        lead_playbook_id: str | None,
    ) -> PositionContextInput | None:
        if payload.position_context is not None:
            return payload.position_context
        if not self._is_specimen_context(
            payload=payload,
            lead_setup_variant_id=lead_setup_variant_id,
            lead_playbook_id=lead_playbook_id,
        ):
            return None
        return PositionContextInput(
            setup_variant_id=self._SPECIMEN_SETUP_VARIANT_ID,
            execution_expression_id=self._SPECIMEN_EXECUTION_EXPRESSION_ID,
            tradable_expression_family=self._SPECIMEN_TRADABLE_EXPRESSION_FAMILY,
            legal_lifecycle_actions=list(self._SPECIMEN_LEGAL_LIFECYCLE_ACTIONS),
        )

    def _is_specimen_context(
        self,
        *,
        payload: ExecutionExpressionInput,
        lead_setup_variant_id: str | None,
        lead_playbook_id: str | None,
    ) -> bool:
        if lead_setup_variant_id == self._SPECIMEN_SETUP_VARIANT_ID:
            return True
        if lead_playbook_id == self._SPECIMEN_LEGACY_PLAYBOOK_ID:
            return True
        if self._SPECIMEN_SETUP_VARIANT_ID in payload.eligibility.active_setup_variant_ids:
            return True
        return self._SPECIMEN_SETUP_VARIANT_ID in payload.eligibility.watch_setup_variant_ids

    def _inventory_action_to_lifecycle_action(self, inventory_action: str) -> LifecycleAction:
        mapping = {
            "add": LifecycleAction.ADD,
            "trim": LifecycleAction.TRIM,
            "reduce": LifecycleAction.FLATTEN,
            "hold": LifecycleAction.HOLD_SMALL_OVERNIGHT,
            "hedge": LifecycleAction.BLOCK_CARRY,
        }
        return mapping.get(inventory_action, LifecycleAction.BLOCK_CARRY)

    def _build_lifecycle_plan(
        self,
        *,
        payload: ExecutionExpressionInput,
        position_context: PositionContextInput | None,
        lead_setup_variant_id: str | None,
        lead_playbook_id: str | None,
        entry_style: str,
        inventory_action: str,
        exit_reasons: list[str],
        target: float,
        scaling_plan: list[float],
    ) -> LifecyclePlanOutput | None:
        if position_context is None:
            return None
        if self._is_specimen_position_context(position_context):
            return self._compile_specimen_lifecycle_plan(
                payload=payload,
                position_context=position_context,
                lead_playbook_id=lead_playbook_id,
                entry_style=entry_style,
                inventory_action=inventory_action,
                exit_reasons=exit_reasons,
                target=target,
                scaling_plan=scaling_plan,
            )

        allowed_actions = list(position_context.legal_lifecycle_actions)
        next_action = self._inventory_action_to_lifecycle_action(inventory_action)
        if next_action not in allowed_actions and allowed_actions:
            next_action = allowed_actions[0]

        if entry_style == "watch_only":
            lifecycle_state = "watch_only_scaffold"
        elif entry_style in {"no_trade", "stand_aside"}:
            lifecycle_state = "inactive_scaffold"
        else:
            lifecycle_state = "entry_authorised_scaffold"

        carry_candidate = bool(
            lead_setup_variant_id == self._SPECIMEN_SETUP_VARIANT_ID
            and entry_style not in {"no_trade", "stand_aside"}
            and payload.temporal.desk_window == "late_session"
            and self._is_clear_event_window(payload.temporal.event_window_state)
        )
        blocked_rules = []
        if not self._is_clear_event_window(payload.temporal.event_window_state):
            blocked_rules.append("event_window_blocks_carry")
        rationale_codes = [
            f"setup_variant:{position_context.setup_variant_id or 'unbound'}",
            f"execution_expression:{position_context.execution_expression_id or 'unbound'}",
            f"lifecycle_state:{lifecycle_state}",
            "gate_136_additive_lifecycle_scaffold",
        ]
        if lead_playbook_id is not None:
            rationale_codes.append(f"lead_playbook:{lead_playbook_id}")
        rationale_codes.append(
            f"tradable_expression_family:{position_context.tradable_expression_family.value if position_context.tradable_expression_family else 'unbound'}"
        )
        return LifecyclePlanOutput(
            setup_variant_id=position_context.setup_variant_id,
            execution_expression_id=position_context.execution_expression_id,
            tradable_expression_family=position_context.tradable_expression_family,
            legal_lifecycle_actions=allowed_actions,
            lifecycle_state=lifecycle_state,
            next_action=next_action,
            allowed_actions=allowed_actions,
            carry_candidate=carry_candidate,
            must_flatten_by_close=bool(position_context.hard_flat_required),
            fired_rules=list(exit_reasons),
            blocked_rules=blocked_rules,
            rationale_codes=rationale_codes,
        )

    def _compile_specimen_lifecycle_plan(
        self,
        *,
        payload: ExecutionExpressionInput,
        position_context: PositionContextInput,
        lead_playbook_id: str | None,
        entry_style: str,
        inventory_action: str,
        exit_reasons: list[str],
        target: float,
        scaling_plan: list[float],
    ) -> LifecyclePlanOutput:
        allowed_actions = list(position_context.legal_lifecycle_actions)
        current_position_size_pct = round(position_context.current_position_size_pct or 0.0, 4)
        position_active = (
            position_context.position_active
            if position_context.position_active is not None
            else current_position_size_pct > 0.0
        )
        remaining_ladder_steps = self._remaining_ladder_steps(
            current_position_size_pct=current_position_size_pct,
            scaling_plan=scaling_plan,
        )
        carry_state_eligible = (
            position_context.carry_state_eligible
            if position_context.carry_state_eligible is not None
            else False
        )
        hard_flat_required = bool(position_context.hard_flat_required)
        clear_event_window = self._is_clear_event_window(payload.temporal.event_window_state)
        lifecycle_state = "entry_authorised_scaffold"
        next_action = self._inventory_action_to_lifecycle_action(inventory_action)
        fired_rules: list[str] = []
        blocked_rules: list[str] = []
        rationale_codes = [
            f"setup_variant:{position_context.setup_variant_id or 'unbound'}",
            f"execution_expression:{position_context.execution_expression_id or 'unbound'}",
            f"tradable_expression_family:{position_context.tradable_expression_family.value if position_context.tradable_expression_family else 'unbound'}",
            f"position_active:{str(position_active).lower()}",
            f"current_position_size_pct:{current_position_size_pct}",
            f"remaining_ladder_steps:{remaining_ladder_steps}",
            "gate_136_additive_lifecycle_scaffold",
            "gate_137_continuation_lifecycle_compiler",
        ]
        if lead_playbook_id is not None:
            rationale_codes.append(f"lead_playbook:{lead_playbook_id}")

        invalidation_hits: list[str] = []
        if payload.regime.sector_leadership_state != "semis_leading":
            invalidation_hits.append("leadership_lost")
        if payload.regime.breadth_state.value != "supportive":
            invalidation_hits.append("breadth_rollover")
        if payload.posture.thesis_state != "valid" or payload.posture.permission_state.value == "block":
            invalidation_hits.append("state_break_below_ladder_anchor")

        if not clear_event_window:
            blocked_rules.append("event_window_blocks_carry")
        if remaining_ladder_steps > 0:
            blocked_rules.append("carry_requires_full_ladder")
        if not position_active:
            blocked_rules.append("carry_requires_active_position")

        carry_candidate = False
        if entry_style == "watch_only":
            lifecycle_state = "watch_only_monitor"
            next_action = LifecycleAction.BLOCK_CARRY
            fired_rules = ["remain_observational"]
            blocked_rules.append("watch_only_no_lifecycle_commitment")
        elif entry_style in {"no_trade", "stand_aside"}:
            lifecycle_state = "inactive_no_trade"
            next_action = LifecycleAction.BLOCK_CARRY
            fired_rules = ["stand_aside_until_setup_confirms"]
            blocked_rules.append("no_trade_no_lifecycle_commitment")
        elif invalidation_hits:
            lifecycle_state = "specimen_invalidation_exit"
            next_action = LifecycleAction.FLATTEN
            fired_rules = invalidation_hits
            blocked_rules.append("carry_blocked_by_invalidation")
        elif hard_flat_required:
            lifecycle_state = "hard_flat_required"
            next_action = LifecycleAction.FLATTEN
            fired_rules = ["hard_flat_before_close"]
            blocked_rules.append("carry_blocked_by_hard_flat")
        elif position_active and payload.temporal.desk_window in {"late_session", "close"} and remaining_ladder_steps > 0:
            lifecycle_state = "stale_thesis_flatten"
            next_action = LifecycleAction.FLATTEN
            fired_rules = ["close_window_stale_thesis"]
            blocked_rules.append("carry_blocked_by_incomplete_ladder")
        elif (
            position_active
            and remaining_ladder_steps == 0
            and payload.temporal.desk_window == "late_session"
            and carry_state_eligible
            and clear_event_window
        ):
            lifecycle_state = "carry_nomination_ready"
            next_action = LifecycleAction.HOLD_SMALL_OVERNIGHT
            carry_candidate = True
            fired_rules = ["late_session_carry_nomination"]
        elif position_active and remaining_ladder_steps == 0:
            lifecycle_state = "trim_extension"
            next_action = LifecycleAction.TRIM
            fired_rules = ["trim_into_extension"]
        else:
            lifecycle_state = "ladder_building"
            next_action = LifecycleAction.ADD
            fired_rules = ["continue_ladder_build"]

        if next_action not in allowed_actions and allowed_actions:
            next_action = allowed_actions[0]

        rationale_codes.extend(
            [
                f"lifecycle_state:{lifecycle_state}",
                f"next_action:{next_action.value}",
                f"carry_candidate:{str(carry_candidate).lower()}",
            ]
        )
        rationale_codes.extend(f"rule:{rule}" for rule in fired_rules)
        rationale_codes.extend(f"blocked:{rule}" for rule in blocked_rules)
        if exit_reasons:
            rationale_codes.extend(f"template_exit:{reason}" for reason in exit_reasons)

        return LifecyclePlanOutput(
            setup_variant_id=position_context.setup_variant_id,
            execution_expression_id=position_context.execution_expression_id,
            tradable_expression_family=position_context.tradable_expression_family,
            legal_lifecycle_actions=allowed_actions,
            lifecycle_state=lifecycle_state,
            next_action=next_action,
            allowed_actions=allowed_actions,
            carry_candidate=carry_candidate,
            must_flatten_by_close=hard_flat_required,
            fired_rules=fired_rules,
            blocked_rules=self._ordered_unique(blocked_rules),
            rationale_codes=self._ordered_unique(rationale_codes),
        )

    def _is_specimen_position_context(
        self, position_context: PositionContextInput | None
    ) -> bool:
        return bool(
            position_context is not None
            and position_context.setup_variant_id == self._SPECIMEN_SETUP_VARIANT_ID
            and position_context.execution_expression_id == self._SPECIMEN_EXECUTION_EXPRESSION_ID
        )

    def _remaining_ladder_steps(
        self,
        *,
        current_position_size_pct: float,
        scaling_plan: list[float],
    ) -> int:
        if not scaling_plan:
            return 0
        cumulative = 0.0
        filled_steps = 0
        for step in scaling_plan:
            cumulative = round(cumulative + step, 4)
            if current_position_size_pct + 1e-6 >= cumulative:
                filled_steps += 1
        return max(len(scaling_plan) - filled_steps, 0)

    def _is_clear_event_window(self, event_window_state: str) -> bool:
        return event_window_state in {"clear", "clear_window"}

    def _lifecycle_inventory_action(
        self,
        *,
        lifecycle_plan: LifecyclePlanOutput,
        fallback: str,
    ) -> str:
        mapping = {
            LifecycleAction.ADD: "add",
            LifecycleAction.TRIM: "trim",
            LifecycleAction.FLATTEN: "reduce",
            LifecycleAction.HOLD_SMALL_OVERNIGHT: "hold",
            LifecycleAction.BLOCK_CARRY: "hold",
        }
        if lifecycle_plan.next_action is None:
            return fallback
        return mapping.get(lifecycle_plan.next_action, fallback)

    def _merge_exit_reasons(
        self, exit_reasons: list[str], lifecycle_plan: LifecyclePlanOutput
    ) -> list[str]:
        reasons = list(exit_reasons)
        for reason in lifecycle_plan.fired_rules:
            if reason not in reasons:
                reasons.append(reason)
        return reasons

    def _merge_exit_plan(
        self, exit_plan: list[str], lifecycle_plan: LifecyclePlanOutput
    ) -> list[str]:
        merged = list(lifecycle_plan.fired_rules)
        for blocked_rule in lifecycle_plan.blocked_rules:
            tag = f"blocked:{blocked_rule}"
            if tag not in merged:
                merged.append(tag)
        for existing in exit_plan:
            if existing not in merged:
                merged.append(existing)
        return merged

    def _invalidation_reasons(
        self, template: ExecutionTemplateSpec, payload: ExecutionExpressionInput
    ) -> list[str]:
        reasons = list(template.invalidation_reasons)
        if payload.posture.time_stop_state == "time_stop_near":
            reasons.append("time_stop_near")
        return reasons

    def _exit_reasons(
        self, template: ExecutionTemplateSpec, payload: ExecutionExpressionInput
    ) -> list[str]:
        reasons = list(template.exit_reasons)
        if payload.posture.inventory_posture_state in set(template.inventory_pressure_states):
            reasons.append(template.inventory_pressure_exit_reason)
        return reasons

    def _inventory_action(
        self, payload: ExecutionExpressionInput, template: ExecutionTemplateSpec
    ) -> str:
        if not template.respect_posture_biases:
            return template.default_inventory_action
        if payload.posture.permission_state.value == "block":
            return "reduce"
        if payload.posture.permission_state.value == "derisk" and template.default_inventory_action == "add":
            posture_overrides = set(template.posture_override_actions)
            if "hold" in posture_overrides:
                return "hold"
            if "trim" in posture_overrides:
                return "trim"
            if "hedge" in posture_overrides:
                return "hedge"
        return template.default_inventory_action


    def _ordered_unique(self, values: list[str]) -> list[str]:
        ordered: list[str] = []
        for value in values:
            if value and value not in ordered:
                ordered.append(value)
        return ordered

    def _contradiction_tags(
        self,
        candidate: PlaybookCandidate,
        payload: ExecutionExpressionInput,
    ) -> list[str]:
        tags: list[str] = []
        if candidate.hedge_overlay and candidate.action_bias.value == "add":
            tags.append("add_requires_hedge_overlay")
        if payload.options_flow.gamma_state.value == "destabilising" and candidate.action_bias.value == "add":
            tags.append("destabilising_gamma_add_candidate")
        if payload.temporal.event_window_state != "clear" and candidate.action_bias.value == "add":
            tags.append("event_window_add_candidate")
        if payload.posture.permission_state.value == "derisk" and candidate.action_bias.value == "add":
            tags.append("permission_envelope_derisk_add_candidate")
        return tags

    def _candidate_score(
        self,
        candidate: PlaybookCandidate,
        payload: ExecutionExpressionInput,
    ) -> tuple[float, list[str]]:
        score = 0.0
        reasons = ["serial_shape_only_candidate"]
        action_bonus = {
            "add": 20.0,
            "hold": 10.0,
            "trim": 6.0,
            "reduce": 2.0,
            "hedge": 8.0,
        }[candidate.action_bias.value]
        score += action_bonus
        reasons.append(f"action_bias_bonus:{action_bonus}")
        if candidate.hedge_overlay:
            score -= 5.0
            reasons.append("hedge_overlay_penalty:-5.0")
        if payload.regime.breadth_state.value == "supportive" and candidate.action_bias.value == "add":
            score += 4.0
            reasons.append("supportive_breadth_bonus:4.0")
        if payload.regime.sector_leadership_state == "semis_leading" and candidate.action_bias.value == "add":
            score += 3.0
            reasons.append("sector_leadership_bonus:3.0")
        if payload.options_flow.gamma_state.value == "destabilising" and candidate.action_bias.value == "add":
            score -= 8.0
            reasons.append("gamma_penalty:-8.0")
        if payload.temporal.event_window_state != "clear" and candidate.action_bias.value == "add":
            score -= 6.0
            reasons.append("event_window_penalty:-6.0")
        if payload.options_flow.gamma_state.value == "destabilising" and candidate.action_bias.value == "hedge":
            score += 8.0
            reasons.append("gamma_hedge_bonus:8.0")
        if candidate.setup_variant_id in payload.eligibility.active_setup_variant_ids:
            score += 2.0
            reasons.append("active_variant_bonus:2.0")
        return round(score, 4), reasons

    def _adjudicate_candidates(
        self,
        eligible_candidates: list[PlaybookCandidate],
        registry_priority: dict[str, int],
        payload: ExecutionExpressionInput,
    ) -> list[CandidateAdjudicationRecord]:
        adjudication: list[CandidateAdjudicationRecord] = []
        for candidate in eligible_candidates:
            score, reasons = self._candidate_score(candidate, payload)
            contradiction_tags = self._contradiction_tags(candidate, payload)
            adjudication.append(
                CandidateAdjudicationRecord(
                    playbook_id=candidate.playbook_id,
                    family_id=candidate.family_id,
                    setup_variant_id=candidate.setup_variant_id,
                    action_bias=candidate.action_bias,
                    sizing_fraction=candidate.sizing_fraction,
                    score=score,
                    registry_priority=registry_priority.get(candidate.playbook_id, 999),
                    contradiction_tags=contradiction_tags,
                    reasons=reasons,
                )
            )
        adjudication.sort(key=lambda item: (-item.score, item.registry_priority, item.playbook_id))
        return adjudication

    def _contradiction_resolution(
        self,
        adjudication: list[CandidateAdjudicationRecord],
    ) -> str | None:
        if not adjudication:
            return None
        if len(adjudication) == 1:
            return "single_candidate_clear"
        if len(adjudication) >= 2 and adjudication[0].score == adjudication[1].score:
            return "registry_priority_tiebreak"
        family_count = len({item.family_id for item in adjudication if item.family_id is not None})
        action_count = len({item.action_bias.value for item in adjudication})
        if family_count > 1 or action_count > 1 or any(item.contradiction_tags for item in adjudication):
            return "mixed_context_resolved_by_score"
        return "score_ranked_candidate_pool"

    def _execution_geometry(
        self,
        template: ExecutionTemplateSpec,
        payload: ExecutionExpressionInput,
        target: float,
        scaling_plan: list[float],
        operative_surfaces: dict[str, float | bool],
        hedge_required: bool,
    ) -> tuple[str, float, float, float, float, float, float, list[str]]:
        passive_aggressive_bias = template.passive_aggressive_bias
        ladder_spacing_bps = template.ladder_spacing_bps
        max_chase_distance_bps = template.max_chase_distance_bps
        stop_distance_bps = template.stop_distance_bps
        take_profit_distance_bps = template.take_profit_distance_bps
        hedge_ratio = template.hedge_ratio if hedge_required else 0.0
        notes: list[str] = []

        if payload.options_flow.gamma_state.value == "destabilising":
            ladder_spacing_bps = round(ladder_spacing_bps * 1.25, 4)
            max_chase_distance_bps = round(max_chase_distance_bps * 0.7, 4)
            stop_distance_bps = round(stop_distance_bps * 1.1, 4)
            hedge_ratio = max(hedge_ratio, 0.35 if hedge_required else 0.0)
            notes.append("gamma_stress_geometry_tightened")
            if passive_aggressive_bias == "aggressive":
                passive_aggressive_bias = "balanced"

        if payload.temporal.event_window_state != "clear":
            max_chase_distance_bps = round(max_chase_distance_bps * 0.6, 4)
            if passive_aggressive_bias == "balanced":
                passive_aggressive_bias = "passive"
            elif passive_aggressive_bias == "aggressive":
                passive_aggressive_bias = "balanced"
            notes.append("event_window_geometry_cautious")

        total_slices = len(scaling_plan) if scaling_plan else 1
        per_slice_risk_pct = round(
            min(
                template.base_risk_per_slice_pct,
                float(operative_surfaces["max_risk_per_trade"]) / total_slices,
            ),
            4,
        )
        if per_slice_risk_pct < template.base_risk_per_slice_pct:
            notes.append("max_risk_per_trade_cap_applied")

        if target == 0.0:
            notes.append("zero_target_geometry")

        return (
            passive_aggressive_bias,
            ladder_spacing_bps,
            max_chase_distance_bps,
            stop_distance_bps,
            take_profit_distance_bps,
            hedge_ratio,
            per_slice_risk_pct,
            notes,
        )

    def _operative_surfaces(self, packet: ModifierRuntimePacket | None) -> dict[str, float | bool]:
        if packet is None:
            return {
                "entry_gate_score_floor": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR]),
                "zone_score_threshold": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.ZONE_SCORE_THRESHOLD]),
                "distance_to_vwap_soft_limit_pct": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.DISTANCE_TO_VWAP_SOFT_LIMIT_PCT]),
                "risk_vix_caution_threshold": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.RISK_VIX_CAUTION_THRESHOLD]),
                "risk_vix_hot_threshold": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.RISK_VIX_HOT_THRESHOLD]),
                "max_risk_per_trade": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.MAX_RISK_PER_TRADE]),
                "hedge_required": bool(self._SURFACE_DEFAULTS[MutableRuntimeSurface.HEDGE_REQUIRED]),
            }

        def numeric(surface: MutableRuntimeSurface) -> float:
            for item in packet.resolved_surfaces:
                if item.target_surface is surface and item.effective_numeric_value is not None:
                    return float(item.effective_numeric_value)
            return float(self._SURFACE_DEFAULTS[surface])

        def boolean(surface: MutableRuntimeSurface) -> bool:
            for item in packet.resolved_surfaces:
                if item.target_surface is surface and item.effective_boolean_value is not None:
                    return bool(item.effective_boolean_value)
            return bool(self._SURFACE_DEFAULTS[surface])

        return {
            "entry_gate_score_floor": numeric(MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR),
            "zone_score_threshold": numeric(MutableRuntimeSurface.ZONE_SCORE_THRESHOLD),
            "distance_to_vwap_soft_limit_pct": numeric(MutableRuntimeSurface.DISTANCE_TO_VWAP_SOFT_LIMIT_PCT),
            "risk_vix_caution_threshold": numeric(MutableRuntimeSurface.RISK_VIX_CAUTION_THRESHOLD),
            "risk_vix_hot_threshold": numeric(MutableRuntimeSurface.RISK_VIX_HOT_THRESHOLD),
            "max_risk_per_trade": numeric(MutableRuntimeSurface.MAX_RISK_PER_TRADE),
            "hedge_required": boolean(MutableRuntimeSurface.HEDGE_REQUIRED),
        }
