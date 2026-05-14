from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.schemas.market import Bar1mPayload
from nvda_desk.schemas.risk import RiskPolicyInput
from nvda_desk.schemas.slv import (
    LadderConfidence,
    LadderOverallDecision,
    LadderReplayRungOutcome,
    StrategicLadderReplayInput,
    StrategicLadderReplayOutput,
    StrategicLadderValidatorMarketInput,
    SupervisoryOverlay,
)
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.services.risk_gateway import RiskGatewayService
from nvda_desk.services.slv_market import StrategicLadderMarketService


class StrategicLadderReplayService:
    def __init__(
        self,
        session_factory: sessionmaker[Session],
        classifier: SessionClockClassifier,
        market_state_service: MarketStateService,
        market_validator: StrategicLadderMarketService,
        risk_gateway: RiskGatewayService,
    ):
        self._session_factory = session_factory
        self._classifier = classifier
        self._market_state_service = market_state_service
        self._market_validator = market_validator
        self._risk_gateway = risk_gateway

    def replay_from_market(
        self, payload: StrategicLadderReplayInput
    ) -> StrategicLadderReplayOutput:
        market_validation = self._market_validator.evaluate_from_market(
            StrategicLadderValidatorMarketInput(
                descriptor=payload.descriptor,
                symbol=payload.symbol,
                as_of_date=payload.as_of_date,
                expiry=payload.expiry,
                option_type=payload.option_type,
                spot_price=payload.spot_price,
                distance_to_vwap_pct=payload.distance_to_vwap_pct,
                iv_hv_divergence_pct=payload.iv_hv_divergence_pct,
                session_phase=payload.session_phase,
                entry_gate_score_floor=payload.entry_gate_score_floor,
                zone_score_threshold=payload.zone_score_threshold,
                distance_to_vwap_soft_limit_pct=payload.distance_to_vwap_soft_limit_pct,
                rungs=payload.rungs,
            )
        )
        overlay = self._build_overlay(payload)
        end_ts = payload.entry_ts + timedelta(minutes=payload.lookahead_minutes)
        bars = self._market_state_service.get_intraday_bars(
            symbol=payload.symbol, ts=end_ts, limit=payload.lookahead_minutes + 1
        ).bars
        bars = [bar for bar in bars if payload.entry_ts <= bar.ts_utc <= end_ts]
        rung_outcomes = [
            self._replay_rung(rung.price, rung.size_units, bars) for rung in payload.rungs
        ]

        positive_hits = sum(1 for outcome in rung_outcomes if outcome.outcome_label == "bounce")
        fill_count = sum(1 for outcome in rung_outcomes if outcome.filled)
        replay_score = 0.0
        if rung_outcomes:
            replay_score = (positive_hits / len(rung_outcomes)) * max(
                overlay.confidence_scalar, 0.0
            )
            if fill_count == 0:
                replay_score *= 0.3
        reasons = list(market_validation.reasons)
        if overlay.action.value != "allow":
            reasons.extend(overlay.reasons)

        confidence = market_validation.confidence
        overall = market_validation.overall_decision
        if overlay.action.value == "block":
            overall = LadderOverallDecision.REJECT
            confidence = LadderConfidence.LOW
            replay_score = 0.0
        elif overlay.action.value == "derisk" and overall is LadderOverallDecision.ACCEPT:
            overall = LadderOverallDecision.ADJUST
            confidence = LadderConfidence.MEDIUM
            replay_score *= 0.7

        return StrategicLadderReplayOutput(
            entry_ts=payload.entry_ts,
            entry_phase=self._classifier.classify(payload.entry_ts).phase,
            lookahead_minutes=payload.lookahead_minutes,
            ladder_validity_score=market_validation.ladder_validity_score,
            replay_score=round(max(0.0, min(1.0, replay_score)), 4),
            overall_decision=overall,
            confidence=confidence,
            reasons=reasons,
            market_validation=market_validation,
            supervisory_overlay=overlay,
            rung_outcomes=rung_outcomes,
            evaluated_bar_count=len(bars),
        )

    def _build_overlay(self, payload: StrategicLadderReplayInput) -> SupervisoryOverlay:
        vix_snapshot = self._market_state_service.get_market_snapshot(
            symbol="VIX", ts=payload.entry_ts
        )
        vvix_snapshot = self._market_state_service.get_market_snapshot(
            symbol="VVIX", ts=payload.entry_ts
        )
        vix_level = (
            float(vix_snapshot.latest_bar.close) if vix_snapshot.latest_bar is not None else 0.0
        )
        vvix_level = (
            float(vvix_snapshot.latest_bar.close) if vvix_snapshot.latest_bar is not None else 0.0
        )
        vix_change = self._symbol_change_pct(
            symbol="VIX", entry_ts=payload.entry_ts, lookback_minutes=15
        )
        vvix_change = self._symbol_change_pct(
            symbol="VVIX", entry_ts=payload.entry_ts, lookback_minutes=15
        )
        decision = self._risk_gateway.evaluate(
            RiskPolicyInput(
                symbol=payload.symbol,
                module_id=payload.descriptor.module_id,
                requested_at=payload.entry_ts,
                session_phase=payload.session_phase,
                vix_level=vix_level,
                vvix_level=vvix_level,
                vix_change_pct_15m=vix_change,
                vvix_change_pct_15m=vvix_change,
                data_age_seconds=0,
                gross_exposure_pct=payload.gross_exposure_pct,
                risk_budget_remaining_pct=payload.risk_budget_remaining_pct,
                open_orders_count=0,
                conflict_tags=payload.conflict_tags,
                vix_caution_threshold=payload.risk_vix_caution_threshold,
                vix_hot_threshold=payload.risk_vix_hot_threshold,
            )
        )
        return SupervisoryOverlay(
            action=decision.action,
            reasons=decision.reasons,
            confidence_scalar=decision.confidence_scalar,
            vix_level=decision.vix_level,
            vvix_level=decision.vvix_level,
        )

    def _symbol_change_pct(
        self, *, symbol: str, entry_ts: datetime, lookback_minutes: int
    ) -> float:
        bars = self._market_state_service.get_intraday_bars(
            symbol=symbol, ts=entry_ts, limit=lookback_minutes + 1
        ).bars
        if len(bars) < 2:
            return 0.0
        first = float(bars[0].close)
        last = float(bars[-1].close)
        if first == 0:
            return 0.0
        return ((last - first) / first) * 100.0

    def _replay_rung(
        self, price: float, size_units: float, bars: list[Bar1mPayload]
    ) -> LadderReplayRungOutcome:
        fill_bar = next((bar for bar in bars if float(bar.low) <= price <= float(bar.high)), None)
        if fill_bar is None:
            return LadderReplayRungOutcome(
                price=price,
                size_units=size_units,
                filled=False,
                outcome_label="missed",
            )
        relevant_bars = [bar for bar in bars if bar.ts_utc >= fill_bar.ts_utc]
        max_high = max(float(bar.high) for bar in relevant_bars)
        min_low = min(float(bar.low) for bar in relevant_bars)
        closing_return = ((float(relevant_bars[-1].close) - price) / price) * 100.0
        mfe = ((max_high - price) / price) * 100.0
        mae = ((price - min_low) / price) * 100.0
        if closing_return >= 0.5:
            outcome_label = "bounce"
        elif closing_return <= -0.5:
            outcome_label = "drawdown"
        else:
            outcome_label = "flat"
        return LadderReplayRungOutcome(
            price=price,
            size_units=size_units,
            filled=True,
            fill_ts=fill_bar.ts_utc.astimezone(UTC),
            phase_at_fill=self._classifier.classify(fill_bar.ts_utc).phase,
            max_favorable_excursion_pct=round(mfe, 4),
            max_adverse_excursion_pct=round(mae, 4),
            closing_return_pct=round(closing_return, 4),
            outcome_label=outcome_label,
        )
