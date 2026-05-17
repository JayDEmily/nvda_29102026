from __future__ import annotations

from decimal import Decimal

from nvda_desk.contracts.strategic_ladder import (
    LadderConfidence,
    LadderDecision,
    LadderMarketEvidence,
    LadderRungResult,
    StrategicLadderMarketValidationOutput,
    StrategicLadderValidationOutput,
    StrategicLadderValidationRequest,
    StrikeZoneSignal,
    SupervisoryOverlay,
)


class StrategicLadderMarketService:
    def validate_baseline_ladder(
        self, request: StrategicLadderValidationRequest
    ) -> StrategicLadderValidationOutput:
        return validate_baseline_ladder(request)

    def validate_market_ladder(
        self, request: StrategicLadderValidationRequest
    ) -> StrategicLadderMarketValidationOutput:
        return validate_market_ladder(request)


def validate_baseline_ladder(
    request: StrategicLadderValidationRequest,
) -> StrategicLadderValidationOutput:
    results = [
        LadderRungResult(
            rung_id=rung.rung_id,
            rung_decision=LadderDecision.ACCEPT,
            confidence=LadderConfidence.MEDIUM,
            market_evidence=LadderMarketEvidence(reasons=["baseline_shape_valid"]),
        )
        for rung in request.rungs
    ]
    return StrategicLadderValidationOutput(
        request_id=request.request_id,
        overall_decision=_overall_decision(results),
        rung_results=results,
    )


def validate_market_ladder(
    request: StrategicLadderValidationRequest,
) -> StrategicLadderMarketValidationOutput:
    if request.observation_context is None:
        baseline = validate_baseline_ladder(request)
        return StrategicLadderMarketValidationOutput(
            request_id=baseline.request_id,
            overall_decision=baseline.overall_decision,
            rung_results=baseline.rung_results,
            strike_zone_signals=[],
            supervisory_overlay=SupervisoryOverlay(overlay_state="clear"),
        )

    context = request.observation_context
    overlay_reasons: list[str] = []
    if context.negative_gamma_active:
        overlay_reasons.append("negative_gamma_active")
    if context.event_risk_active:
        overlay_reasons.append("event_risk_active")
    if context.liquidity_state not in {"normal", "liquid"}:
        overlay_reasons.append(f"liquidity_state::{context.liquidity_state}")

    rung_results: list[LadderRungResult] = []
    strike_zone_signals: list[StrikeZoneSignal] = []
    for rung in request.rungs:
        distance = abs(context.spot_price - rung.limit_price)
        evidence_reasons: list[str] = []
        if distance <= Decimal("2"):
            state = "near_spot"
            decision = LadderDecision.REVISE if overlay_reasons else LadderDecision.ACCEPT
            confidence = LadderConfidence.HIGH
            evidence_reasons.append("rung_near_spot")
        elif distance <= Decimal("5"):
            state = "outside_near_spot"
            decision = LadderDecision.REVISE if overlay_reasons else LadderDecision.ACCEPT
            confidence = LadderConfidence.MEDIUM
            evidence_reasons.append("rung_outside_near_spot")
        else:
            state = "far_from_spot"
            decision = LadderDecision.REJECT
            confidence = LadderConfidence.LOW
            evidence_reasons.append("rung_far_from_spot")

        evidence_reasons.extend(overlay_reasons)
        rung_results.append(
            LadderRungResult(
                rung_id=rung.rung_id,
                rung_decision=decision,
                confidence=confidence,
                market_evidence=LadderMarketEvidence(
                    symbol=context.symbol,
                    spot_price=context.spot_price,
                    distance_from_spot=distance,
                    market_state=state,
                    reasons=evidence_reasons,
                ),
            )
        )
        strike_zone_signals.append(
            StrikeZoneSignal(
                signal_id="spot_distance",
                score=max(Decimal("0"), Decimal("10") - distance),
                reasons=evidence_reasons,
            )
        )

    overlay_state = (
        "block"
        if any(result.rung_decision == LadderDecision.REJECT for result in rung_results)
        else "caution" if overlay_reasons else "clear"
    )
    return StrategicLadderMarketValidationOutput(
        request_id=request.request_id,
        overall_decision=_overall_decision(rung_results),
        rung_results=rung_results,
        strike_zone_signals=strike_zone_signals,
        supervisory_overlay=SupervisoryOverlay(
            overlay_state=overlay_state, reasons=overlay_reasons
        ),
    )


def _overall_decision(results: list[LadderRungResult]) -> LadderDecision:
    if any(result.rung_decision == LadderDecision.REJECT for result in results):
        return LadderDecision.REJECT
    if any(result.rung_decision == LadderDecision.REVISE for result in results):
        return LadderDecision.REVISE
    return LadderDecision.ACCEPT
