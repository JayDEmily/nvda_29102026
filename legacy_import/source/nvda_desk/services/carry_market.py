from __future__ import annotations

from datetime import UTC, datetime

import numpy as np
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.schemas.market import Bar1mPayload
from nvda_desk.schemas.overnight import (
    CarryAction,
    CarryDerivedContext,
    CarryRecommendation,
    CloseStateCarryHandoff,
    OvernightCarryEvaluatorInput,
    OvernightCarryMarketInput,
    OvernightCarryMarketOutput,
)
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.services.module_evaluators import OvernightCarryEvaluatorService


class OvernightCarryMarketService:
    def __init__(
        self,
        session_factory: sessionmaker[Session],
        classifier: SessionClockClassifier,
        market_state_service: MarketStateService,
    ):
        self._session_factory = session_factory
        self._classifier = classifier
        self._market_state_service = market_state_service
        self._service = OvernightCarryEvaluatorService()

    def evaluate_from_market(
        self, payload: OvernightCarryMarketInput
    ) -> OvernightCarryMarketOutput:
        bars = self._market_state_service.get_intraday_bars(
            symbol=payload.symbol, ts=payload.evaluation_ts, limit=60
        ).bars
        if not bars:
            derived = CarryDerivedContext(
                evaluation_ts=payload.evaluation_ts,
                last_bar_ts=payload.evaluation_ts,
                close_phase=(
                    payload.close_state_handoff.close_phase
                    if payload.close_state_handoff is not None
                    else self._classifier.classify(payload.evaluation_ts).phase
                ),
                close_distance_to_vwap_pct=0.0,
                realised_vol_pct=0.0,
                vix_level=0.0,
                vvix_level=0.0,
            )
        else:
            last_bar = bars[-1]
            vwap = self._session_vwap(bars)
            close_distance = 0.0 if vwap == 0 else ((float(last_bar.close) - vwap) / vwap) * 100
            realised_vol = self._realised_vol_pct(bars)
            vix_level = self._latest_close_or_zero("VIX", payload.evaluation_ts)
            vvix_level = self._latest_close_or_zero("VVIX", payload.evaluation_ts)
            close_phase = (
                payload.close_state_handoff.close_phase
                if payload.close_state_handoff is not None
                else self._classifier.classify(last_bar.ts_utc.astimezone(UTC)).phase
            )
            derived = CarryDerivedContext(
                evaluation_ts=payload.evaluation_ts,
                last_bar_ts=last_bar.ts_utc,
                close_phase=close_phase,
                close_distance_to_vwap_pct=round(close_distance, 4),
                realised_vol_pct=round(realised_vol, 4),
                vix_level=round(vix_level, 4),
                vvix_level=round(vvix_level, 4),
            )
        output = self._service.evaluate(
            OvernightCarryEvaluatorInput(
                descriptor=payload.descriptor,
                symbol=payload.symbol,
                close_distance_to_vwap_pct=derived.close_distance_to_vwap_pct,
                close_phase=derived.close_phase,
                realised_vol_pct=derived.realised_vol_pct,
                vix_level=derived.vix_level,
                vvix_level=derived.vvix_level,
                asia_precursor_composite=payload.asia_precursor_composite,
                risk_budget_remaining_pct=payload.risk_budget_remaining_pct,
                gross_exposure_pct=payload.gross_exposure_pct,
                open_orders_count=payload.open_orders_count,
            )
        )
        adjusted_action, adjusted_exposure, adjustment_reasons = self._apply_handoff_constraints(
            handoff=payload.close_state_handoff,
            recommendation=output.carry_recommendation,
            action=output.carry_action,
            exposure=output.overnight_exposure_pct,
        )
        adjusted_recommendation = self._recommendation_for_action(adjusted_action)
        rationale_codes = list(output.rationale_codes)
        rationale_codes.extend(adjustment_reasons)
        return OvernightCarryMarketOutput(
            carry_recommendation=adjusted_recommendation,
            carry_action=adjusted_action,
            overnight_exposure_pct=adjusted_exposure,
            keep_orders_active=output.keep_orders_active,
            rationale_codes=rationale_codes,
            review_required=output.review_required,
            derived_context=derived,
            applied_handoff=payload.close_state_handoff,
        )

    def _apply_handoff_constraints(
        self,
        *,
        handoff: CloseStateCarryHandoff | None,
        recommendation: CarryRecommendation,
        action: CarryAction,
        exposure: float,
    ) -> tuple[CarryAction, float, list[str]]:
        if handoff is None:
            return action, exposure, []
        if action in handoff.allowed_actions:
            return action, exposure, []
        if handoff.recommended_action_ceiling is CarryAction.BLOCK_CARRY:
            reasons = ["handoff:block_carry"]
            if handoff.lifecycle_action_ceiling is not None:
                reasons.append(f"handoff:lifecycle_ceiling:{handoff.lifecycle_action_ceiling.value}")
            return CarryAction.BLOCK_CARRY, 0.0, reasons
        for fallback in (
            CarryAction.HOLD_SMALL,
            CarryAction.HOLD_BASELINE,
            CarryAction.FLATTEN,
        ):
            if fallback in handoff.allowed_actions:
                if fallback is CarryAction.HOLD_SMALL:
                    reasons = [f"handoff:downgraded_from:{action.value}"]
                    if handoff.lifecycle_action_ceiling is not None:
                        reasons.append(f"handoff:lifecycle_ceiling:{handoff.lifecycle_action_ceiling.value}")
                    return (
                        fallback,
                        min(exposure, handoff.overnight_deployable_capital_pct, 10.0),
                        reasons,
                    )
                if fallback is CarryAction.HOLD_BASELINE:
                    reasons = [f"handoff:downgraded_from:{action.value}"]
                    if handoff.lifecycle_action_ceiling is not None:
                        reasons.append(f"handoff:lifecycle_ceiling:{handoff.lifecycle_action_ceiling.value}")
                    return (
                        fallback,
                        min(exposure, handoff.overnight_deployable_capital_pct),
                        reasons,
                    )
                reasons = [f"handoff:downgraded_from:{action.value}"]
                if handoff.lifecycle_action_ceiling is not None:
                    reasons.append(f"handoff:lifecycle_ceiling:{handoff.lifecycle_action_ceiling.value}")
                return fallback, 0.0, reasons
        # defensive fallback
        if recommendation is CarryRecommendation.BLOCK:
            reasons = ["handoff:block_carry"]
            if handoff.lifecycle_action_ceiling is not None:
                reasons.append(f"handoff:lifecycle_ceiling:{handoff.lifecycle_action_ceiling.value}")
            return CarryAction.BLOCK_CARRY, 0.0, reasons
        reasons = [f"handoff:downgraded_from:{action.value}"]
        if handoff.lifecycle_action_ceiling is not None:
            reasons.append(f"handoff:lifecycle_ceiling:{handoff.lifecycle_action_ceiling.value}")
        return CarryAction.FLATTEN, 0.0, reasons

    def _recommendation_for_action(self, action: CarryAction) -> CarryRecommendation:
        return {
            CarryAction.ADD_CARRY: CarryRecommendation.INCREASE,
            CarryAction.HOLD_SMALL: CarryRecommendation.HOLD_SMALL,
            CarryAction.HOLD_BASELINE: CarryRecommendation.HOLD_SMALL,
            CarryAction.FLATTEN: CarryRecommendation.FLATTEN,
            CarryAction.BLOCK_CARRY: CarryRecommendation.BLOCK,
        }[action]

    def _latest_close_or_zero(self, symbol: str, ts: datetime) -> float:
        snapshot = self._market_state_service.get_market_snapshot(symbol=symbol, ts=ts)
        return float(snapshot.latest_bar.close) if snapshot.latest_bar is not None else 0.0

    def _session_vwap(self, bars: list[Bar1mPayload]) -> float:
        pv_total = 0.0
        volume_total = 0.0
        for bar in bars:
            typical = (float(bar.high) + float(bar.low) + float(bar.close)) / 3.0
            pv_total += typical * bar.volume
            volume_total += bar.volume
        return pv_total / volume_total if volume_total else 0.0

    def _realised_vol_pct(self, bars: list[Bar1mPayload]) -> float:
        closes = np.array([float(bar.close) for bar in bars], dtype=float)
        if closes.size < 2:
            return 0.0
        returns = np.diff(np.log(closes))
        if returns.size == 0:
            return 0.0
        return float(np.std(returns) * np.sqrt(390) * 100.0)
