from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from sqlalchemy import asc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import Instrument, OptionSnapshot
from nvda_desk.schemas.options import OptionSnapshotPayload, OptionType
from nvda_desk.schemas.slv import (
    LadderConfidence,
    LadderOverallDecision,
    LadderRungDecision,
    LadderRungMarketContext,
    LadderRungMarketResult,
    StrategicLadderValidatorMarketInput,
    StrategicLadderValidatorMarketOutput,
    StrikeZoneSignal,
)


@dataclass(frozen=True)
class _ScoredSnapshot:
    snapshot: OptionSnapshotPayload
    strike_pressure_score: float
    fill_plausibility_score: float
    proximity_pct: float


class StrategicLadderMarketService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def get_option_surface(
        self,
        *,
        symbol: str,
        as_of_date: date,
        expiry: date | None = None,
        option_type: OptionType | None = None,
    ) -> list[OptionSnapshotPayload]:
        with self._session_factory() as session:
            instrument = session.scalar(select(Instrument).where(Instrument.symbol == symbol))
            if instrument is None:
                return []
            chosen_expiry = expiry or self._infer_expiry(session, instrument.id, as_of_date)
            if chosen_expiry is None:
                return []
            stmt = (
                select(OptionSnapshot)
                .where(OptionSnapshot.instrument_id == instrument.id)
                .where(OptionSnapshot.as_of_date == as_of_date)
                .where(OptionSnapshot.expiry == chosen_expiry)
            )
            if option_type is not None:
                stmt = stmt.where(OptionSnapshot.option_type == option_type.value)
            rows = list(session.scalars(stmt.order_by(asc(OptionSnapshot.strike))))
        return [self._to_payload(row) for row in rows]

    def evaluate_from_market(
        self, payload: StrategicLadderValidatorMarketInput
    ) -> StrategicLadderValidatorMarketOutput:
        surface = self.get_option_surface(
            symbol=payload.symbol,
            as_of_date=payload.as_of_date,
            expiry=payload.expiry,
            option_type=payload.option_type,
        )
        if not surface:
            return StrategicLadderValidatorMarketOutput(
                ladder_validity_score=0.0,
                overall_decision=LadderOverallDecision.REJECT,
                rung_decisions=[
                    LadderRungMarketResult(
                        price=rung.price,
                        size_units=rung.size_units,
                        decision=LadderRungDecision.DROP,
                        reasons=["no_option_surface_available"],
                        market_context=None,
                        suggested_price=None,
                    )
                    for rung in payload.rungs
                ],
                reasons=["no_option_surface_available"],
                confidence=LadderConfidence.LOW,
                as_of_date=payload.as_of_date,
                expiry_used=payload.expiry,
                option_type=payload.option_type,
                snapshots_considered=0,
                strike_zone_signals=[],
            )

        scored_surface = self._score_surface(surface=surface, spot_price=payload.spot_price)
        strike_zone_signals = self._top_signals(scored_surface)
        rung_results: list[LadderRungMarketResult] = []
        rung_scores: list[float] = []
        overall_reasons: list[str] = []

        for rung in payload.rungs:
            matched = min(
                scored_surface,
                key=lambda item: abs(float(item.snapshot.strike) - rung.price),
            )
            matched_proximity_pct = (
                abs(float(matched.snapshot.strike) - rung.price) / payload.spot_price * 100
            )
            raw_score = (matched.strike_pressure_score * 0.6) + (
                matched.fill_plausibility_score * 0.4
            )
            reasons: list[str] = []
            if matched_proximity_pct > 1.5:
                raw_score -= 0.2
                reasons.append("nearest_strike_too_far")
            if payload.iv_hv_divergence_pct > 20:
                raw_score -= 0.1
                reasons.append("iv_hv_divergence_elevated")
            if abs(payload.distance_to_vwap_pct) > payload.distance_to_vwap_soft_limit_pct:
                raw_score -= 0.1
                reasons.append("distance_to_vwap_elevated")
            if matched.fill_plausibility_score < 0.35:
                raw_score -= 0.2
                reasons.append("fill_plausibility_weak")
            if matched.strike_pressure_score < 0.35:
                raw_score -= 0.2
                reasons.append("strike_pressure_weak")

            score = max(0.0, min(1.0, raw_score))
            keep_threshold = min(payload.zone_score_threshold + 0.22, 0.95)
            if score >= keep_threshold:
                decision = LadderRungDecision.KEEP
            elif score >= payload.zone_score_threshold:
                decision = LadderRungDecision.ADJUST
            else:
                decision = LadderRungDecision.DROP

            suggested_price = None
            if decision is LadderRungDecision.ADJUST:
                suggested_price = float(matched.snapshot.strike)
                if suggested_price != rung.price:
                    reasons.append("snap_to_supportive_strike")

            if not reasons:
                reasons.append("matched_surface_within_tolerance")

            rung_results.append(
                LadderRungMarketResult(
                    price=rung.price,
                    size_units=rung.size_units,
                    decision=decision,
                    reasons=reasons,
                    market_context=LadderRungMarketContext(
                        matched_strike=float(matched.snapshot.strike),
                        strike_pressure_score=matched.strike_pressure_score,
                        fill_plausibility_score=matched.fill_plausibility_score,
                        proximity_pct=round(matched_proximity_pct, 4),
                        spread_pct_of_mid=self._spread_pct_of_mid(matched.snapshot),
                        open_interest=matched.snapshot.open_interest,
                        volume=matched.snapshot.volume,
                        confidence=matched.snapshot.confidence,
                    ),
                    suggested_price=suggested_price,
                )
            )
            rung_scores.append(score)

        ladder_score = sum(rung_scores) / len(rung_scores)
        drop_count = sum(1 for item in rung_results if item.decision is LadderRungDecision.DROP)
        adjust_count = sum(1 for item in rung_results if item.decision is LadderRungDecision.ADJUST)

        ladder_accept_threshold = min(
            max(payload.entry_gate_score_floor + 0.07, keep_threshold), 0.95
        )
        ladder_reject_threshold = max(payload.entry_gate_score_floor - 0.30, 0.15)

        if drop_count == len(rung_results) or ladder_score < ladder_reject_threshold:
            overall = LadderOverallDecision.REJECT
            confidence = LadderConfidence.LOW
        elif drop_count > 0 or adjust_count > 0 or ladder_score < ladder_accept_threshold:
            overall = LadderOverallDecision.ADJUST
            confidence = LadderConfidence.MEDIUM
        else:
            overall = LadderOverallDecision.ACCEPT
            confidence = LadderConfidence.HIGH

        if payload.expiry is None:
            overall_reasons.append("expiry_auto_selected")
        if not overall_reasons:
            overall_reasons.append("surface_backed_validation_complete")

        expiry_used = scored_surface[0].snapshot.expiry if scored_surface else payload.expiry
        return StrategicLadderValidatorMarketOutput(
            ladder_validity_score=max(0.0, min(1.0, ladder_score)),
            overall_decision=overall,
            rung_decisions=rung_results,
            reasons=overall_reasons,
            confidence=confidence,
            as_of_date=payload.as_of_date,
            expiry_used=expiry_used,
            option_type=payload.option_type,
            snapshots_considered=len(scored_surface),
            strike_zone_signals=strike_zone_signals,
        )

    def _score_surface(
        self, *, surface: Iterable[OptionSnapshotPayload], spot_price: float
    ) -> list[_ScoredSnapshot]:
        rows = list(surface)
        max_oi = max((row.open_interest or 0) for row in rows) or 1
        max_volume = max((row.volume or 0) for row in rows) or 1
        scored: list[_ScoredSnapshot] = []
        for row in rows:
            proximity_pct = abs(float(row.strike) - spot_price) / spot_price * 100
            oi_norm = (
                0.5 if row.open_interest is None else min((row.open_interest or 0) / max_oi, 1.0)
            )
            volume_norm = 0.5 if row.volume is None else min((row.volume or 0) / max_volume, 1.0)
            proximity_norm = max(0.0, 1.0 - min(proximity_pct / 3.0, 1.0))
            strike_pressure_score = (
                (oi_norm * 0.45) + (volume_norm * 0.25) + (proximity_norm * 0.30)
            )
            spread_pct = self._spread_pct_of_mid(row)
            spread_quality = (
                0.5 if spread_pct is None else max(0.0, 1.0 - min(spread_pct / 25.0, 1.0))
            )
            fill_plausibility_score = min(
                1.0,
                (volume_norm * 0.35) + (spread_quality * 0.45) + (proximity_norm * 0.20),
            )
            scored.append(
                _ScoredSnapshot(
                    snapshot=row,
                    strike_pressure_score=round(strike_pressure_score, 4),
                    fill_plausibility_score=round(fill_plausibility_score, 4),
                    proximity_pct=round(proximity_pct, 4),
                )
            )
        return scored

    def _top_signals(self, scored_surface: list[_ScoredSnapshot]) -> list[StrikeZoneSignal]:
        ranked = sorted(
            scored_surface,
            key=lambda item: (item.strike_pressure_score, item.fill_plausibility_score),
            reverse=True,
        )[:3]
        return [
            StrikeZoneSignal(
                strike=float(item.snapshot.strike),
                normalized_pressure=item.strike_pressure_score,
                fill_plausibility_score=item.fill_plausibility_score,
                spread_pct_of_mid=self._spread_pct_of_mid(item.snapshot),
                open_interest=item.snapshot.open_interest,
                volume=item.snapshot.volume,
                confidence=item.snapshot.confidence,
            )
            for item in ranked
        ]

    def _infer_expiry(self, session: Session, instrument_id: int, as_of_date: date) -> date | None:
        stmt = (
            select(OptionSnapshot.expiry)
            .where(OptionSnapshot.instrument_id == instrument_id)
            .where(OptionSnapshot.as_of_date == as_of_date)
            .where(OptionSnapshot.expiry.is_not(None))
            .order_by(asc(OptionSnapshot.expiry))
            .limit(1)
        )
        return session.scalar(stmt)

    def _to_payload(self, row: OptionSnapshot) -> OptionSnapshotPayload:
        return OptionSnapshotPayload(
            as_of_date=row.as_of_date,
            expiry=row.expiry,
            option_type=OptionType(row.option_type),
            strike=row.strike,
            bid=row.bid,
            ask=row.ask,
            last=row.last,
            volume=row.volume,
            open_interest=row.open_interest,
            iv=row.iv,
            delta=row.delta,
            gamma=row.gamma,
            delta_change=row.delta_change,
            provenance=row.provenance,
            confidence=row.confidence,
            source_document=row.source_document,
            source_pages=row.source_pages,
        )

    def _spread_pct_of_mid(self, row: OptionSnapshotPayload) -> float | None:
        if row.bid is None or row.ask is None:
            return None
        mid = (float(row.bid) + float(row.ask)) / 2.0
        if mid <= 0:
            return None
        return round(((float(row.ask) - float(row.bid)) / mid) * 100, 4)
