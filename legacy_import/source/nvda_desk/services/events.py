from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import cast

from sqlalchemy import asc, desc, or_, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import MarketEvent, SessionCalendar
from nvda_desk.schemas.events import (
    EventProximityResponse,
    ImpactLevel,
    MarketEventCreate,
    MarketEventListResponse,
    MarketEventPayload,
    SessionCalendarCreate,
    SessionCalendarListResponse,
    SessionCalendarPayload,
)


class EventsService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def create_session(self, payload: SessionCalendarCreate) -> SessionCalendarPayload:
        with self._session_factory() as session:
            row = SessionCalendar(**payload.model_dump(mode="python"))
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_session_payload(row)

    def list_sessions(self, limit: int = 20) -> SessionCalendarListResponse:
        with self._session_factory() as session:
            rows = list(
                session.scalars(
                    select(SessionCalendar)
                    .order_by(desc(SessionCalendar.session_date))
                    .limit(limit)
                )
            )
        return SessionCalendarListResponse(sessions=[self._to_session_payload(row) for row in rows])

    def create_event(self, payload: MarketEventCreate) -> MarketEventPayload:
        with self._session_factory() as session:
            row = MarketEvent(**payload.model_dump(mode="python"))
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_event_payload(row)

    def list_events(self, symbol: str | None = None, limit: int = 20) -> MarketEventListResponse:
        with self._session_factory() as session:
            stmt = select(MarketEvent)
            if symbol:
                stmt = stmt.where(or_(MarketEvent.symbol == symbol, MarketEvent.symbol.is_(None)))
            rows = list(session.scalars(stmt.order_by(desc(MarketEvent.event_ts)).limit(limit)))
        return MarketEventListResponse(events=[self._to_event_payload(row) for row in rows])

    def get_proximity(
        self, *, requested_at: datetime, symbol: str | None = None
    ) -> EventProximityResponse:
        window_before = requested_at - timedelta(hours=4)
        window_after = requested_at + timedelta(hours=24)
        with self._session_factory() as session:
            stmt = (
                select(MarketEvent)
                .where(MarketEvent.event_ts >= window_before)
                .where(MarketEvent.event_ts <= window_after)
            )
            if symbol:
                stmt = stmt.where(or_(MarketEvent.symbol == symbol, MarketEvent.symbol.is_(None)))
            rows = list(session.scalars(stmt.order_by(asc(MarketEvent.event_ts))))
        aware_requested_at = (
            requested_at.astimezone(UTC)
            if requested_at.tzinfo
            else requested_at.replace(tzinfo=UTC)
        )
        recent = [row for row in rows if self._aware(row.event_ts) <= aware_requested_at]
        upcoming = [row for row in rows if self._aware(row.event_ts) > aware_requested_at]
        risk_window_open = any(row.impact_level in {"medium", "high"} for row in rows)
        return EventProximityResponse(
            requested_at=aware_requested_at,
            symbol=symbol,
            event_risk_window_open=risk_window_open,
            upcoming_events=[self._to_event_payload(row) for row in upcoming],
            recent_events=[self._to_event_payload(row) for row in recent],
        )

    def _to_session_payload(self, row: SessionCalendar) -> SessionCalendarPayload:
        return SessionCalendarPayload(
            calendar_id=row.id,
            session_date=row.session_date,
            venue=row.venue,
            market_open_utc=row.market_open_utc,
            market_close_utc=row.market_close_utc,
            session_label=row.session_label,
            is_half_day=row.is_half_day,
        )

    def _to_event_payload(self, row: MarketEvent) -> MarketEventPayload:
        return MarketEventPayload(
            event_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            event_ts=self._aware(row.event_ts),
            event_type=row.event_type,
            impact_level=cast(ImpactLevel, row.impact_level),
            title=row.title,
            source_document=row.source_document,
            notes_md=row.notes_md,
        )

    def _aware(self, ts: datetime) -> datetime:
        return ts.astimezone(UTC) if ts.tzinfo is not None else ts.replace(tzinfo=UTC)
