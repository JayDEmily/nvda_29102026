from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import asc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import Bar1m, Instrument, MarketEvent, SessionCalendar
from nvda_desk.schemas.overnight import (
    CarryAction,
    CarryHorizon,
    CarryReplayPathSummary,
    OvernightCarryMarketInput,
    OvernightCarryReplayFromMarketInput,
    OvernightCarryReplayFromMarketOutput,
)
from nvda_desk.services.carry_market import OvernightCarryMarketService


class OvernightCarryReplayService:
    def __init__(
        self,
        session_factory: sessionmaker[Session],
        carry_market_service: OvernightCarryMarketService,
    ):
        self._session_factory = session_factory
        self._carry_market_service = carry_market_service

    def replay_from_market(
        self, payload: OvernightCarryReplayFromMarketInput
    ) -> OvernightCarryReplayFromMarketOutput:
        market_input = OvernightCarryMarketInput(
            descriptor=payload.descriptor,
            symbol=payload.symbol,
            evaluation_ts=payload.evaluation_ts,
            asia_precursor_composite=payload.asia_precursor_composite,
            risk_budget_remaining_pct=payload.risk_budget_remaining_pct,
            gross_exposure_pct=payload.gross_exposure_pct,
            open_orders_count=payload.open_orders_count,
            close_state_handoff=payload.close_state_handoff,
        )
        carry_eval = self._carry_market_service.evaluate_from_market(market_input)
        close_price = self._latest_price(symbol=payload.symbol, ts=payload.evaluation_ts)
        if close_price is None:
            raise ValueError(f"no market bars available for symbol: {payload.symbol}")
        if (
            payload.close_state_handoff is not None
            and payload.close_state_handoff.next_session_open_ts is not None
        ):
            next_open_ts = payload.close_state_handoff.next_session_open_ts
            weekend_window = payload.close_state_handoff.weekend_window
        else:
            next_open_ts, weekend_window = self._next_session_open(payload.evaluation_ts)
        event_window_open = (
            payload.close_state_handoff.event_carry_window
            if payload.close_state_handoff is not None
            else self._event_window_open(symbol=payload.symbol, requested_at=payload.evaluation_ts)
        )
        next_open_price_reference, reference_source = self._project_next_open_price(
            symbol=payload.symbol,
            next_open_ts=next_open_ts,
            close_price=close_price,
            weekend_window=weekend_window,
            event_window_open=event_window_open,
            carry_eval=carry_eval,
        )
        gap_pct = ((next_open_price_reference - close_price) / close_price) * 100.0
        carry_horizon = (
            payload.close_state_handoff.horizon
            if payload.close_state_handoff is not None
            else (
                CarryHorizon.WEEKEND
                if weekend_window
                else (CarryHorizon.EVENT_CARRY if event_window_open else CarryHorizon.OVERNIGHT)
            )
        )
        paths = [
            self._path_summary(
                path_name="flatten",
                carry_action=CarryAction.FLATTEN,
                exposure_pct=0.0,
                keep_orders_active=False,
                projected_open_price=next_open_price_reference,
                projected_gap_pct=gap_pct,
                rationale_codes=["capital_preservation"],
            ),
            self._path_summary(
                path_name="hold_baseline",
                carry_action=CarryAction.HOLD_BASELINE,
                exposure_pct=payload.baseline_hold_exposure_pct,
                keep_orders_active=payload.open_orders_count == 0,
                projected_open_price=next_open_price_reference,
                projected_gap_pct=gap_pct,
                rationale_codes=["baseline_hold_comparator"],
            ),
            self._path_summary(
                path_name="follow_recommendation",
                carry_action=carry_eval.carry_action,
                exposure_pct=carry_eval.overnight_exposure_pct,
                keep_orders_active=carry_eval.keep_orders_active,
                projected_open_price=next_open_price_reference,
                projected_gap_pct=gap_pct,
                rationale_codes=carry_eval.rationale_codes,
            ),
        ]
        best_path = max(paths, key=lambda item: item.projected_pnl_pct)
        return OvernightCarryReplayFromMarketOutput(
            module_id=payload.descriptor.module_id,
            evaluation_ts=self._aware(payload.evaluation_ts),
            next_session_open_ts=next_open_ts,
            next_session_reference_source=reference_source,
            weekend_window=weekend_window,
            event_window_open=event_window_open,
            carry_horizon=carry_horizon,
            best_path_name=best_path.path_name,
            carry_recommendation=carry_eval.carry_recommendation,
            carry_action=carry_eval.carry_action,
            close_price=round(close_price, 4),
            next_open_price_reference=round(next_open_price_reference, 4),
            path_summaries=paths,
            applied_handoff=payload.close_state_handoff,
        )

    def _project_next_open_price(
        self,
        *,
        symbol: str,
        next_open_ts: datetime,
        close_price: float,
        weekend_window: bool,
        event_window_open: bool,
        carry_eval: object,
    ) -> tuple[float, str]:
        market_open_price = self._latest_price(symbol=symbol, ts=next_open_ts, exact_or_after=True)
        if market_open_price is not None:
            return market_open_price, "market_bar"
        modifier = 0.0
        if weekend_window:
            modifier -= 0.35
        if event_window_open:
            modifier -= 0.55
        rationale_codes = getattr(carry_eval, "rationale_codes", [])
        if "asia_precursor_supportive" in rationale_codes:
            modifier += 0.25
        if "macro_volatility_hot" in rationale_codes:
            modifier -= 0.4
        if "close_extended_vs_vwap" in rationale_codes:
            modifier -= 0.2
        projected = max(0.01, close_price * (1 + modifier / 100.0))
        return projected, "derived_from_last_close"

    def _path_summary(
        self,
        *,
        path_name: str,
        carry_action: CarryAction,
        exposure_pct: float,
        keep_orders_active: bool,
        projected_open_price: float,
        projected_gap_pct: float,
        rationale_codes: list[str],
    ) -> CarryReplayPathSummary:
        projected_pnl_pct = (projected_gap_pct * exposure_pct) / 100.0
        return CarryReplayPathSummary(
            path_name=path_name,
            carry_action=carry_action,
            exposure_pct=exposure_pct,
            keep_orders_active=keep_orders_active,
            projected_open_price=round(projected_open_price, 4),
            projected_gap_pct=round(projected_gap_pct, 4),
            projected_pnl_pct=round(projected_pnl_pct, 4),
            rationale_codes=rationale_codes,
        )

    def _next_session_open(self, ts: datetime) -> tuple[datetime, bool]:
        aware_ts = self._aware(ts)
        requested_date = aware_ts.date()
        with self._session_factory() as session:
            current = session.scalar(
                select(SessionCalendar).where(SessionCalendar.session_date == requested_date)
            )
            if current is None:
                return aware_ts + timedelta(days=1), requested_date.weekday() == 4
            next_session = session.scalar(
                select(SessionCalendar)
                .where(SessionCalendar.market_open_utc > aware_ts)
                .order_by(asc(SessionCalendar.market_open_utc))
                .limit(1)
            )
        if next_session is None:
            fallback_open = datetime.combine(
                requested_date + timedelta(days=1), datetime.min.time(), tzinfo=UTC
            ).replace(hour=13, minute=30)
            return fallback_open, requested_date.weekday() == 4
        weekend_window = (next_session.session_date - requested_date).days > 1
        return self._aware(next_session.market_open_utc), weekend_window

    def _event_window_open(self, *, symbol: str, requested_at: datetime) -> bool:
        aware_ts = self._aware(requested_at)
        window_start = aware_ts - timedelta(hours=12)
        window_end = aware_ts + timedelta(hours=24)
        with self._session_factory() as session:
            stmt = (
                select(MarketEvent)
                .where((MarketEvent.symbol == symbol) | (MarketEvent.symbol.is_(None)))
                .where(MarketEvent.event_ts >= window_start)
                .where(MarketEvent.event_ts <= window_end)
            )
            event = session.scalar(stmt.limit(1))
        return event is not None

    def _latest_price(
        self, *, symbol: str, ts: datetime, exact_or_after: bool = False
    ) -> float | None:
        aware_ts = self._aware(ts)
        with self._session_factory() as session:
            instrument = session.scalar(select(Instrument).where(Instrument.symbol == symbol))
            if instrument is None:
                return None
            stmt = select(Bar1m).where(Bar1m.instrument_id == instrument.id)
            if exact_or_after:
                stmt = stmt.where(Bar1m.ts_utc >= aware_ts).order_by(asc(Bar1m.ts_utc))
            else:
                stmt = stmt.where(Bar1m.ts_utc <= aware_ts).order_by(Bar1m.ts_utc.desc())
            row = session.scalar(stmt.limit(1))
        return None if row is None else float(Decimal(row.close))

    def _aware(self, ts: datetime) -> datetime:
        return ts.astimezone(UTC) if ts.tzinfo is not None else ts.replace(tzinfo=UTC)
