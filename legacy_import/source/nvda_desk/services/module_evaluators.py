from __future__ import annotations

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.overnight import (
    CarryAction,
    CarryRecommendation,
    OvernightCarryEvaluatorInput,
    OvernightCarryEvaluatorOutput,
)
from nvda_desk.schemas.slv import (
    LadderConfidence,
    LadderOverallDecision,
    LadderRungDecision,
    LadderRungResult,
    StrategicLadderValidatorInput,
    StrategicLadderValidatorOutput,
)


class StrategicLadderValidatorService:
    def evaluate(self, payload: StrategicLadderValidatorInput) -> StrategicLadderValidatorOutput:
        rung_results: list[LadderRungResult] = []
        score_components: list[float] = []
        overall_reasons: list[str] = []

        for rung in payload.rungs:
            reasons: list[str] = []
            score = (rung.strike_pressure_score * 0.55) + (rung.fill_plausibility_score * 0.45)
            distance_pct = abs((payload.spot_price - rung.price) / payload.spot_price) * 100
            if distance_pct > 5:
                score -= 0.25
                reasons.append("rung_too_far_from_spot")
            if rung.fill_plausibility_score < 0.35:
                score -= 0.3
                reasons.append("low_fill_plausibility")
            if rung.strike_pressure_score < 0.30:
                score -= 0.2
                reasons.append("weak_strike_pressure")
            if payload.session_phase in {
                SessionClockPhase.CLOSED,
                SessionClockPhase.AFTER_HOURS,
            }:
                score -= 0.15
                reasons.append("phase_not_actionable")

            if score >= 0.7:
                decision = LadderRungDecision.KEEP
            elif score >= 0.45:
                decision = LadderRungDecision.ADJUST
            else:
                decision = LadderRungDecision.DROP

            rung_results.append(
                LadderRungResult(
                    price=rung.price,
                    size_units=rung.size_units,
                    decision=decision,
                    reasons=reasons,
                )
            )
            score_components.append(max(0.0, min(1.0, score)))

        ladder_score = sum(score_components) / len(score_components)
        drop_count = sum(1 for item in rung_results if item.decision is LadderRungDecision.DROP)
        adjust_count = sum(1 for item in rung_results if item.decision is LadderRungDecision.ADJUST)

        if payload.iv_hv_divergence_pct > 25:
            overall_reasons.append("iv_hv_divergence_elevated")
            ladder_score -= 0.1
        if abs(payload.distance_to_vwap_pct) > 2.5:
            overall_reasons.append("distance_to_vwap_elevated")
            ladder_score -= 0.1

        ladder_score = max(0.0, min(1.0, ladder_score))
        if drop_count > 0 or ladder_score < 0.45:
            overall = LadderOverallDecision.REJECT
            confidence = LadderConfidence.MEDIUM
        elif adjust_count > 0 or ladder_score < 0.7:
            overall = LadderOverallDecision.ADJUST
            confidence = LadderConfidence.MEDIUM
        else:
            overall = LadderOverallDecision.ACCEPT
            confidence = LadderConfidence.HIGH

        if not overall_reasons:
            overall_reasons.append("structure_within_v1_tolerances")

        return StrategicLadderValidatorOutput(
            ladder_validity_score=ladder_score,
            overall_decision=overall,
            rung_decisions=rung_results,
            reasons=overall_reasons,
            confidence=confidence,
        )


class OvernightCarryEvaluatorService:
    def evaluate(self, payload: OvernightCarryEvaluatorInput) -> OvernightCarryEvaluatorOutput:
        rationale_codes: list[str] = []
        risk_hot = payload.vix_level >= 30 or payload.vvix_level >= 110
        precursor_supportive = payload.asia_precursor_composite > 0.2
        close_extended = abs(payload.close_distance_to_vwap_pct) >= 2.5
        low_risk_budget = payload.risk_budget_remaining_pct < 20

        if risk_hot:
            rationale_codes.append("macro_volatility_hot")
        if close_extended:
            rationale_codes.append("close_extended_vs_vwap")
        if low_risk_budget:
            rationale_codes.append("low_risk_budget")
        if payload.open_orders_count > 0:
            rationale_codes.append("open_orders_present")
        if precursor_supportive:
            rationale_codes.append("asia_precursor_supportive")

        if risk_hot or low_risk_budget:
            recommendation = CarryRecommendation.BLOCK
            exposure = 0.0
            keep_orders_active = False
            review_required = True
        elif payload.close_phase is SessionClockPhase.DEALER_UNWIND_CLOSE and precursor_supportive:
            recommendation = CarryRecommendation.INCREASE
            exposure = min(25.0, payload.risk_budget_remaining_pct)
            keep_orders_active = False
            review_required = False
        elif close_extended or payload.realised_vol_pct > 6:
            recommendation = CarryRecommendation.FLATTEN
            exposure = 0.0
            keep_orders_active = False
            review_required = False
        else:
            recommendation = CarryRecommendation.HOLD_SMALL
            exposure = min(10.0, payload.risk_budget_remaining_pct)
            keep_orders_active = payload.open_orders_count == 0
            review_required = False

        if not rationale_codes:
            rationale_codes.append("baseline_overnight_profile")

        action = {
            CarryRecommendation.INCREASE: CarryAction.ADD_CARRY,
            CarryRecommendation.HOLD_SMALL: CarryAction.HOLD_SMALL,
            CarryRecommendation.FLATTEN: CarryAction.FLATTEN,
            CarryRecommendation.BLOCK: CarryAction.BLOCK_CARRY,
        }[recommendation]
        return OvernightCarryEvaluatorOutput(
            carry_recommendation=recommendation,
            carry_action=action,
            overnight_exposure_pct=exposure,
            keep_orders_active=keep_orders_active,
            rationale_codes=rationale_codes,
            review_required=review_required,
        )
