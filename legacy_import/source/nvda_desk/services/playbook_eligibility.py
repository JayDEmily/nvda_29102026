"""Playbook-eligibility service for the Desk Cognition Grammar.

This service decides which playbook families, setup variants, and legacy-
compatible playbooks are eligible, watch-only, or ineligible once temporal,
regime, options, and posture layers are known.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Literal

from nvda_desk.schemas.cognition import (
    EligibilityAdmissibilitySurface,
    PlaybookAction,
    PlaybookCandidate,
    PlaybookDecision,
    PlaybookEligibilityInput,
    PlaybookEligibilityOutput,
    PlaybookFamilyCandidate,
    SetupVariantCandidate,
)
from nvda_desk.schemas.playbook_registry import (
    PlaybookDecisionProfile,
    PlaybookSpec,
    SetupVariantSpec,
)
from nvda_desk.services.playbook_registry import PlaybookRegistryService


class PlaybookEligibilityService:
    """Determine deterministic playbook eligibility for one snapshot.

    Purpose:
        Translate desk state into explicit playbook-family decisions, setup
        variants, and legacy-compatible playbook action biases.
    Inputs:
        `PlaybookEligibilityInput` carrying temporal, regime, options, and
        posture outputs from upstream runtime layers.
    Outputs:
        `PlaybookEligibilityOutput` with native family/setup-variant decisions
        plus a legacy-compatible playbook bridge.
    Determinism:
        Uses checked-in registry order plus fixed rule evaluation with no live calls.
    """

    def __init__(self, registry_service: PlaybookRegistryService | None = None):
        self._registry = registry_service or PlaybookRegistryService()
        self._variant_evaluators: dict[
            str,
            Callable[
                [PlaybookEligibilityInput, list[str], SetupVariantSpec],
                SetupVariantCandidate,
            ],
        ] = {
            "opening_drive_continuation": self._continuation_ladder,
            "midday_compression_release": self._compression_breakout,
            "late_session_pin_reversion": self._pin_reversion,
            "negative_gamma_flush_probe": self._negative_gamma_flush,
            "front_expiry_pin_build": self._front_expiry_pin_pressure,
            "front_next_curve_dislocation": self._term_structure_dislocation,
            "skew_relaxation_reversal": self._skew_pressure_reversal,
        }

    def evaluate(self, payload: PlaybookEligibilityInput) -> PlaybookEligibilityOutput:
        """Return eligible, watch-only, probe-only, and ineligible playbooks."""

        no_trade_reasons = self._no_trade_reasons(payload)
        setup_variant_candidates = [
            self._evaluate_variant(variant, payload, no_trade_reasons)
            for variant in self._registry.ordered_setup_variants()
        ]
        family_candidates = self._family_candidates(setup_variant_candidates)
        candidates = self._playbook_candidates(setup_variant_candidates)
        add_candidates = [
            candidate.playbook_id
            for candidate in candidates
            if candidate.action_bias.value == "add"
        ]
        hold_candidates = [
            candidate.playbook_id
            for candidate in candidates
            if candidate.action_bias.value == "hold"
        ]
        trim_candidates = [
            candidate.playbook_id
            for candidate in candidates
            if candidate.action_bias.value == "trim"
        ]
        reduce_candidates = [
            candidate.playbook_id
            for candidate in candidates
            if candidate.action_bias.value == "reduce"
        ]
        hedge_candidates = [
            candidate.playbook_id
            for candidate in candidates
            if candidate.action_bias.value == "hedge"
        ]
        probe_candidates = [
            candidate.playbook_id
            for candidate in candidates
            if candidate.decision is PlaybookDecision.ELIGIBLE and candidate.sizing_fraction <= 0.15
        ]
        watch_only_candidates = [
            candidate.playbook_id
            for candidate in candidates
            if candidate.decision is PlaybookDecision.WATCH_ONLY
        ]
        rejected_playbook_reasons = {
            candidate.playbook_id: candidate.reasons
            for candidate in candidates
            if candidate.decision is not PlaybookDecision.ELIGIBLE
        }
        active_family_ids = [
            candidate.family_id
            for candidate in family_candidates
            if candidate.decision is PlaybookDecision.ELIGIBLE
        ]
        watch_family_ids = [
            candidate.family_id
            for candidate in family_candidates
            if candidate.decision is PlaybookDecision.WATCH_ONLY
        ]
        active_setup_variant_ids = [
            candidate.setup_variant_id
            for candidate in setup_variant_candidates
            if candidate.decision is PlaybookDecision.ELIGIBLE
        ]
        watch_setup_variant_ids = [
            candidate.setup_variant_id
            for candidate in setup_variant_candidates
            if candidate.decision is PlaybookDecision.WATCH_ONLY
        ]
        admissible_playbook_ids = [
            candidate.playbook_id
            for candidate in candidates
            if candidate.decision is PlaybookDecision.ELIGIBLE
        ]
        reasons = [f"permission_state:{payload.posture.permission_state.value}"]
        reasons.extend(f"no_trade:{reason}" for reason in no_trade_reasons)
        reasons.extend(f"active_family:{family_id}" for family_id in active_family_ids)
        reasons.extend(
            f"active_setup_variant:{setup_variant_id}"
            for setup_variant_id in active_setup_variant_ids
        )
        admissibility_surface = EligibilityAdmissibilitySurface(
            permission_state=payload.posture.permission_state,
            no_trade_reasons=list(no_trade_reasons),
            admissible_family_ids=active_family_ids,
            watch_family_ids=watch_family_ids,
            admissible_setup_variant_ids=active_setup_variant_ids,
            watch_setup_variant_ids=watch_setup_variant_ids,
            admissible_playbook_ids=admissible_playbook_ids,
            watch_only_playbook_ids=watch_only_candidates,
            notes=[
                "stage5_limited_to_admissibility_and_watch_status",
                "stage6_owns_candidate_ranking_and_lead_selection",
            ],
        )
        return PlaybookEligibilityOutput(
            family_candidates=family_candidates,
            setup_variant_candidates=setup_variant_candidates,
            candidates=candidates,
            active_family_ids=active_family_ids,
            watch_family_ids=watch_family_ids,
            active_setup_variant_ids=active_setup_variant_ids,
            watch_setup_variant_ids=watch_setup_variant_ids,
            add_candidates=add_candidates,
            hold_candidates=hold_candidates,
            trim_candidates=trim_candidates,
            reduce_candidates=reduce_candidates,
            hedge_candidates=hedge_candidates,
            probe_candidates=probe_candidates,
            watch_only_candidates=watch_only_candidates,
            no_trade_reasons=no_trade_reasons,
            rejected_playbook_reasons=rejected_playbook_reasons,
            admissibility_surface=admissibility_surface,
            reasons=reasons,
        )

    def _evaluate_variant(
        self,
        variant: SetupVariantSpec,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
    ) -> SetupVariantCandidate:
        evaluator = self._variant_evaluators.get(variant.setup_variant_id)
        if evaluator is None and variant.legacy_playbook_id is not None:
            evaluator = self._variant_evaluators.get(variant.legacy_playbook_id)
        if evaluator is None:
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=[f"no_variant_evaluator:{variant.setup_variant_id}"],
            )
        return evaluator(payload, no_trade_reasons, variant)

    def _variant_candidate(
        self,
        variant: SetupVariantSpec,
        *,
        decision: PlaybookDecision,
        action_bias: PlaybookAction,
        sizing_fraction: float,
        hedge_overlay: bool,
        reasons: list[str],
    ) -> SetupVariantCandidate:
        return SetupVariantCandidate(
            setup_variant_id=variant.setup_variant_id,
            family_id=variant.family_id,
            execution_expression_id=variant.execution_expression_id,
            horizon=variant.horizon.value,
            legacy_playbook_id=variant.legacy_playbook_id,
            decision=decision,
            action_bias=action_bias,
            sizing_fraction=sizing_fraction,
            hedge_overlay=hedge_overlay,
            reasons=list(reasons),
        )

    def _candidate_from_profile(
        self,
        spec: PlaybookSpec,
        profile_name: Literal["eligible", "watch_only", "ineligible"],
        reasons: list[str],
    ) -> PlaybookCandidate:
        profile: PlaybookDecisionProfile = getattr(spec, profile_name)
        return PlaybookCandidate(
            playbook_id=spec.playbook_id,
            family_id=spec.family_id,
            setup_variant_id=spec.setup_variant_id,
            execution_expression_id=spec.execution_expression_id,
            horizon=spec.horizon.value,
            decision=profile.decision,
            action_bias=profile.action_bias,
            sizing_fraction=profile.sizing_fraction,
            hedge_overlay=profile.hedge_overlay,
            reasons=list(reasons),
        )

    def _family_candidates(
        self, setup_variant_candidates: list[SetupVariantCandidate]
    ) -> list[PlaybookFamilyCandidate]:
        grouped: dict[str, list[SetupVariantCandidate]] = defaultdict(list)
        for candidate in setup_variant_candidates:
            grouped[candidate.family_id].append(candidate)
        family_candidates: list[PlaybookFamilyCandidate] = []
        for family in self._registry.document().families:
            variants = grouped.get(family.family_id, [])
            active_variants = [
                item.setup_variant_id
                for item in variants
                if item.decision is PlaybookDecision.ELIGIBLE
            ]
            watch_variants = [
                item.setup_variant_id
                for item in variants
                if item.decision is PlaybookDecision.WATCH_ONLY
            ]
            active_playbook_ids: list[str] = []
            watch_playbook_ids: list[str] = []
            for variant_id in active_variants:
                active_playbook_ids.extend(
                    self._registry.active_playbook_ids_for_setup_variant(variant_id)
                )
            for variant_id in watch_variants:
                watch_playbook_ids.extend(
                    self._registry.active_playbook_ids_for_setup_variant(variant_id)
                )
            if active_variants:
                decision = PlaybookDecision.ELIGIBLE
                reasons = [f"eligible_variants:{active_variants}"]
            elif watch_variants:
                decision = PlaybookDecision.WATCH_ONLY
                reasons = [f"watch_variants:{watch_variants}"]
            else:
                decision = PlaybookDecision.INELIGIBLE
                reasons = ["no_active_variants"]
            family_candidates.append(
                PlaybookFamilyCandidate(
                    family_id=family.family_id,
                    decision=decision,
                    active_setup_variant_ids=active_variants,
                    watch_setup_variant_ids=watch_variants,
                    active_playbook_ids=active_playbook_ids,
                    watch_playbook_ids=watch_playbook_ids,
                    reasons=reasons,
                )
            )
        return family_candidates

    def _playbook_candidates(
        self, setup_variant_candidates: list[SetupVariantCandidate]
    ) -> list[PlaybookCandidate]:
        candidates: list[PlaybookCandidate] = []
        for variant_candidate in setup_variant_candidates:
            for spec in self._registry.playbooks_for_setup_variant(
                variant_candidate.setup_variant_id
            ):
                profile_name = self._profile_name_for_decision(variant_candidate.decision)
                reasons = [f"derived_from_setup_variant:{variant_candidate.setup_variant_id}"]
                reasons.extend(variant_candidate.reasons)
                candidates.append(self._candidate_from_profile(spec, profile_name, reasons))
        return candidates

    def _profile_name_for_decision(
        self, decision: PlaybookDecision
    ) -> Literal["eligible", "watch_only", "ineligible"]:
        if decision is PlaybookDecision.ELIGIBLE:
            return "eligible"
        if decision is PlaybookDecision.WATCH_ONLY:
            return "watch_only"
        return "ineligible"

    def _no_trade_reasons(self, payload: PlaybookEligibilityInput) -> list[str]:
        reasons: list[str] = []
        if payload.posture.permission_state.value == "block":
            reasons.append("permission_blocked")
        if payload.temporal.event_window_state in {
            "event_live_window",
            "event_imminent_window",
        }:
            reasons.append("event_window_veto")
            event_family = payload.temporal.active_event_family or ""
            if self._is_macro_or_policy_family(event_family):
                reasons.append("macro_event_window_veto")
            elif self._is_company_family(event_family):
                reasons.append("company_event_window_veto")
            elif self._is_expiry_family(event_family) or payload.temporal.expiry_cycle_state == "expiry_day":
                reasons.append("expiry_event_window_veto")
        if self._has_venue_session_distortion(payload):
            reasons.append("venue_session_distortion")
        if payload.options_flow.options_behavior_cluster == "event_suppressed":
            reasons.append("options_surface_event_suppressed")
        return reasons

    def _has_venue_session_distortion(self, payload: PlaybookEligibilityInput) -> bool:
        if not payload.temporal.calendar_closure_classes:
            return False
        return payload.temporal.desk_window in {"late_session", "close", "closed"}

    def _is_macro_or_policy_family(self, event_family: str) -> bool:
        family = event_family.lower()
        return any(token in family for token in {"fomc", "cpi", "ppi", "pce", "nfp", "gdp", "macro", "policy"})

    def _is_company_family(self, event_family: str) -> bool:
        family = event_family.lower()
        return "earnings" in family or family.startswith("nvda_") or family.startswith("mega_cap_ai_")

    def _is_expiry_family(self, event_family: str) -> bool:
        return "expiry" in event_family.lower() or "opex" in event_family.lower()

    def _continuation_ladder(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        variant: SetupVariantSpec,
    ) -> SetupVariantCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=reasons,
            )
        if (
            payload.regime.sector_leadership_state == "semis_leading"
            and payload.regime.breadth_state.value == "supportive"
            and payload.temporal.desk_window
            in {"early_anchor", "mid_morning", "trend_window", "late_session"}
            and payload.options_flow.options_behavior_cluster
            not in {"negative_gamma_flush", "event_suppressed"}
        ):
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.ELIGIBLE,
                action_bias=PlaybookAction.ADD,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["leadership_and_breadth_supportive"],
            )
        if payload.regime.sector_leadership_state in {
            "nvda_only_leadership",
            "leadership_mixed",
        }:
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.WATCH_ONLY,
                action_bias=PlaybookAction.HOLD,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["leadership_not_clean_enough"],
            )
        return self._variant_candidate(
            variant,
            decision=PlaybookDecision.INELIGIBLE,
            action_bias=PlaybookAction.REDUCE,
            sizing_fraction=0.0,
            hedge_overlay=False,
            reasons=["continuation_not_supported"],
        )

    def _negative_gamma_flush(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        variant: SetupVariantSpec,
    ) -> SetupVariantCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=reasons,
            )
        if (
            payload.temporal.recent_path_tag == "intraday_flush"
            and payload.options_flow.options_behavior_cluster == "negative_gamma_flush"
        ):
            if payload.posture.permission_state.value == "derisk":
                return self._variant_candidate(
                    variant,
                    decision=PlaybookDecision.WATCH_ONLY,
                    action_bias=PlaybookAction.HOLD,
                    sizing_fraction=0.0,
                    hedge_overlay=True,
                    reasons=["hostile_flush_context"],
                )
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.ELIGIBLE,
                action_bias=PlaybookAction.ADD,
                sizing_fraction=0.0,
                hedge_overlay=True,
                reasons=["buyable_flush_probe"],
            )
        return self._variant_candidate(
            variant,
            decision=PlaybookDecision.INELIGIBLE,
            action_bias=PlaybookAction.REDUCE,
            sizing_fraction=0.0,
            hedge_overlay=False,
            reasons=["no_negative_gamma_flush_context"],
        )

    def _pin_reversion(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        variant: SetupVariantSpec,
    ) -> SetupVariantCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=reasons,
            )
        if (
            payload.options_flow.pin_risk_state in {"pin_risk_high", "pin_risk_present"}
            and payload.options_flow.strike_cluster_state
            in {"live_pin_cluster", "inferred_pin_cluster"}
            and payload.options_flow.pin_progression_state in {"pinning_in", "pin_stable"}
            and payload.temporal.desk_window in {"lunch", "trend_window", "late_session", "close"}
        ):
            if payload.options_flow.dealer_pressure_state == "dealer_destabilising":
                return self._variant_candidate(
                    variant,
                    decision=PlaybookDecision.WATCH_ONLY,
                    action_bias=PlaybookAction.HOLD,
                    sizing_fraction=0.0,
                    hedge_overlay=False,
                    reasons=["pin_active_but_flow_destabilising"],
                )
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.ELIGIBLE,
                action_bias=PlaybookAction.TRIM,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["pin_reversion_supported"],
            )
        return self._variant_candidate(
            variant,
            decision=PlaybookDecision.INELIGIBLE,
            action_bias=PlaybookAction.REDUCE,
            sizing_fraction=0.0,
            hedge_overlay=False,
            reasons=["no_pin_reversion_context"],
        )

    def _compression_breakout(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        variant: SetupVariantSpec,
    ) -> SetupVariantCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=reasons,
            )
        if (
            payload.options_flow.options_behavior_cluster == "compression_breakout_ready"
            and payload.temporal.desk_window in {"lunch", "trend_window", "late_session"}
        ):
            if payload.posture.permission_state.value == "derisk":
                return self._variant_candidate(
                    variant,
                    decision=PlaybookDecision.WATCH_ONLY,
                    action_bias=PlaybookAction.HOLD,
                    sizing_fraction=0.0,
                    hedge_overlay=False,
                    reasons=["compression_ready_but_posture_derisk"],
                )
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.ELIGIBLE,
                action_bias=PlaybookAction.ADD,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["compression_breakout_supported"],
            )
        if payload.options_flow.gamma_state.value == "supportive":
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.WATCH_ONLY,
                action_bias=PlaybookAction.HOLD,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["supportive_options_need_more_confirmation"],
            )
        return self._variant_candidate(
            variant,
            decision=PlaybookDecision.INELIGIBLE,
            action_bias=PlaybookAction.REDUCE,
            sizing_fraction=0.0,
            hedge_overlay=False,
            reasons=["compression_not_supported"],
        )

    def _front_expiry_pin_pressure(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        variant: SetupVariantSpec,
    ) -> SetupVariantCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=reasons,
            )
        if payload.temporal.expiry_cycle_state not in {"expiry_day", "front_week"}:
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["not_front_expiry_window"],
            )
        if payload.temporal.desk_window not in {"early_anchor", "mid_morning"}:
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["pin_pressure_window_not_open"],
            )
        if (
            payload.options_flow.pin_risk_state in {"pin_risk_high", "pin_risk_present"}
            and payload.options_flow.strike_cluster_state
            in {"live_pin_cluster", "inferred_pin_cluster"}
            and payload.options_flow.pin_progression_state in {"pinning_in", "pin_stable"}
        ):
            if payload.options_flow.dealer_pressure_state == "dealer_destabilising":
                return self._variant_candidate(
                    variant,
                    decision=PlaybookDecision.WATCH_ONLY,
                    action_bias=PlaybookAction.HOLD,
                    sizing_fraction=0.0,
                    hedge_overlay=False,
                    reasons=["pin_build_visible_but_flow_destabilising"],
                )
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.ELIGIBLE,
                action_bias=PlaybookAction.TRIM,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["front_expiry_pin_pressure_supported"],
            )
        return self._variant_candidate(
            variant,
            decision=PlaybookDecision.INELIGIBLE,
            action_bias=PlaybookAction.REDUCE,
            sizing_fraction=0.0,
            hedge_overlay=False,
            reasons=["no_front_expiry_pin_pressure_context"],
        )

    def _term_structure_dislocation(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        variant: SetupVariantSpec,
    ) -> SetupVariantCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=reasons,
            )
        if payload.temporal.expiry_cycle_state == "far_cycle":
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["term_dislocation_not_relevant_far_cycle"],
            )
        if payload.options_flow.term_structure_state.value == "flat":
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["term_structure_flat"],
            )
        if (
            payload.options_flow.tenor_curve_state
            in {
                "backwardated_curve",
                "hump_curve",
                "front_loaded_curve",
                "back_loaded_curve",
            }
            and payload.options_flow.iv_rv_curve_state
            in {"front_expiry_rich", "next_expiry_rich", "both_expiries_rich"}
            and payload.options_flow.repeated_snapshot_state
            in {"stable_recheck", "escalating_pressure"}
            and payload.temporal.desk_window in {"early_anchor", "mid_morning", "trend_window"}
        ):
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.ELIGIBLE,
                action_bias=PlaybookAction.ADD,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["term_structure_dislocation_supported"],
            )
        if payload.options_flow.tenor_curve_state in {
            "backwardated_curve",
            "hump_curve",
            "front_loaded_curve",
            "back_loaded_curve",
        }:
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.WATCH_ONLY,
                action_bias=PlaybookAction.HOLD,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["term_structure_dislocation_needs_iv_confirmation"],
            )
        return self._variant_candidate(
            variant,
            decision=PlaybookDecision.INELIGIBLE,
            action_bias=PlaybookAction.REDUCE,
            sizing_fraction=0.0,
            hedge_overlay=False,
            reasons=["no_term_structure_dislocation_context"],
        )

    def _skew_pressure_reversal(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        variant: SetupVariantSpec,
    ) -> SetupVariantCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=reasons,
            )
        if payload.options_flow.options_behavior_cluster == "negative_gamma_flush":
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.INELIGIBLE,
                action_bias=PlaybookAction.REDUCE,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["full_flush_already_has_priority"],
            )
        if (
            payload.options_flow.dealer_pressure_state == "dealer_destabilising"
            and payload.options_flow.skew_evolution_state
            in {"downside_skew_expanding", "upside_skew_expanding"}
            and payload.options_flow.repeated_snapshot_state
            in {"stable_recheck", "cooling_pressure"}
            and payload.options_flow.options_behavior_cluster
            in {"dealer_flow_tension", "balanced_options_state"}
            and payload.temporal.desk_window in {"early_anchor", "mid_morning", "trend_window"}
        ):
            if payload.posture.permission_state.value == "derisk":
                return self._variant_candidate(
                    variant,
                    decision=PlaybookDecision.WATCH_ONLY,
                    action_bias=PlaybookAction.HOLD,
                    sizing_fraction=0.0,
                    hedge_overlay=True,
                    reasons=["skew_reversal_visible_but_posture_derisk"],
                )
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.ELIGIBLE,
                action_bias=PlaybookAction.ADD,
                sizing_fraction=0.0,
                hedge_overlay=True,
                reasons=["skew_pressure_reversal_supported"],
            )
        if payload.options_flow.skew_evolution_state in {
            "downside_skew_expanding",
            "upside_skew_expanding",
        }:
            return self._variant_candidate(
                variant,
                decision=PlaybookDecision.WATCH_ONLY,
                action_bias=PlaybookAction.HOLD,
                sizing_fraction=0.0,
                hedge_overlay=False,
                reasons=["skew_pressure_visible_needs_reversal_confirmation"],
            )
        return self._variant_candidate(
            variant,
            decision=PlaybookDecision.INELIGIBLE,
            action_bias=PlaybookAction.REDUCE,
            sizing_fraction=0.0,
            hedge_overlay=False,
            reasons=["no_skew_pressure_reversal_context"],
        )
