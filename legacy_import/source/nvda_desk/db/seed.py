from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from nvda_desk.db.base import Base
from nvda_desk.db.models import (
    Bar1m,
    Instrument,
    MarketEvent,
    OptionSnapshot,
    SessionCalendar,
)
from nvda_desk.db.session import create_engine_from_url
from nvda_desk.fixtures import load_legacy_option_fixture_rows


@dataclass(frozen=True)
class DevSeedSummary:
    instrument_count: int
    bar_count: int
    option_snapshot_count: int


def create_schema(database_url: str) -> None:
    engine = create_engine_from_url(database_url)
    Base.metadata.create_all(bind=engine)


def seed_dev_data(session: Session) -> DevSeedSummary:
    instruments = [
        ("NVDA", "equity"),
        ("QQQ", "etf"),
        ("SOXX", "etf"),
        ("VIX", "index"),
        ("VVIX", "index"),
    ]
    for symbol, asset_class in instruments:
        existing = session.scalar(select(Instrument).where(Instrument.symbol == symbol))
        if existing is None:
            session.add(Instrument(symbol=symbol, asset_class=asset_class))
    session.flush()

    instrument_map = {
        instrument.symbol: instrument for instrument in session.scalars(select(Instrument)).all()
    }
    _seed_intraday_bars(
        session,
        instrument=instrument_map["NVDA"],
        base_price=Decimal("118.00"),
        profile="nvda",
    )
    _seed_intraday_bars(
        session,
        instrument=instrument_map["VIX"],
        base_price=Decimal("18.50"),
        profile="vix",
    )
    _seed_intraday_bars(
        session,
        instrument=instrument_map["VVIX"],
        base_price=Decimal("88.00"),
        profile="vvix",
    )
    _seed_option_snapshots(session, instrument=instrument_map["NVDA"])
    _seed_session_calendars(session)
    _seed_market_events(session)
    session.commit()

    total_instruments = session.query(Instrument).count()
    total_bars = session.query(Bar1m).count()
    total_option_snapshots = session.query(OptionSnapshot).count()
    return DevSeedSummary(
        instrument_count=total_instruments,
        bar_count=total_bars,
        option_snapshot_count=total_option_snapshots,
    )


def _seed_intraday_bars(
    session: Session,
    *,
    instrument: Instrument,
    base_price: Decimal,
    profile: str,
) -> None:
    start = datetime(2026, 3, 18, 13, 30, tzinfo=UTC)
    existing_bars = list(
        session.scalars(
            select(Bar1m).where(Bar1m.instrument_id == instrument.id).order_by(Bar1m.ts_utc)
        )
    )
    target_bar_count = 240
    next_index = len(existing_bars)
    price = existing_bars[-1].close if existing_bars else base_price
    for i in range(next_index, target_bar_count):
        ts = start + timedelta(minutes=i)
        drift = _drift_for(profile=profile, index=i)
        open_px = price
        close_px = max(Decimal("0.01"), price + drift)
        high_px = max(open_px, close_px) + _high_pad_for(profile)
        low_px = max(Decimal("0.01"), min(open_px, close_px) - _low_pad_for(profile))
        volume = _volume_for(profile=profile, index=i)
        session.add(
            Bar1m(
                instrument_id=instrument.id,
                ts_utc=ts,
                open=open_px,
                high=high_px,
                low=low_px,
                close=close_px,
                volume=volume,
            )
        )
        price = close_px


def _drift_for(*, profile: str, index: int) -> Decimal:
    if profile == "nvda":
        return (
            Decimal("0.15")
            if index < 30
            else (
                Decimal("0.04")
                if index < 90
                else Decimal("-0.03") if index < 150 else Decimal("0.01")
            )
        )
    if profile == "vix":
        return (
            Decimal("0.05")
            if index < 30
            else (
                Decimal("0.02")
                if index < 90
                else Decimal("-0.01") if index < 150 else Decimal("0.00")
            )
        )
    if profile == "vvix":
        return (
            Decimal("0.08")
            if index < 30
            else (
                Decimal("0.03")
                if index < 90
                else Decimal("-0.02") if index < 150 else Decimal("0.00")
            )
        )
    return Decimal("0.00")


def _high_pad_for(profile: str) -> Decimal:
    return Decimal("0.12") if profile in {"vix", "vvix"} else Decimal("0.08")


def _low_pad_for(profile: str) -> Decimal:
    return Decimal("0.10") if profile in {"vix", "vvix"} else Decimal("0.06")


def _volume_for(*, profile: str, index: int) -> int:
    if profile == "nvda":
        return 1_100_000 + (index * 35_000)
    if profile == "vix":
        return 250_000 + (index * 8_000)
    if profile == "vvix":
        return 125_000 + (index * 4_000)
    return 10_000 + index


def _seed_option_snapshots(session: Session, *, instrument: Instrument) -> None:
    for row in load_legacy_option_fixture_rows():
        exists = session.scalar(
            select(OptionSnapshot)
            .where(OptionSnapshot.instrument_id == instrument.id)
            .where(OptionSnapshot.as_of_date == row.date)
            .where(OptionSnapshot.expiry == row.expiry)
            .where(OptionSnapshot.option_type == row.option_type)
            .where(OptionSnapshot.strike == row.strike)
        )
        if exists is not None:
            continue
        session.add(
            OptionSnapshot(
                instrument_id=instrument.id,
                as_of_date=row.date,
                expiry=row.expiry,
                option_type=row.option_type,
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
        )


def _seed_session_calendars(session: Session) -> None:
    sessions = [
        (
            date(2026, 3, 18),
            datetime(2026, 3, 18, 13, 30, tzinfo=UTC),
            datetime(2026, 3, 18, 20, 0, tzinfo=UTC),
            "regular",
            False,
        ),
        (
            date(2026, 3, 19),
            datetime(2026, 3, 19, 13, 30, tzinfo=UTC),
            datetime(2026, 3, 19, 20, 0, tzinfo=UTC),
            "regular",
            False,
        ),
    ]
    for session_date, market_open, market_close, session_label, is_half_day in sessions:
        existing = session.scalar(
            select(SessionCalendar)
            .where(SessionCalendar.session_date == session_date)
            .where(SessionCalendar.venue == "NASDAQ")
        )
        if existing is None:
            session.add(
                SessionCalendar(
                    session_date=session_date,
                    venue="NASDAQ",
                    market_open_utc=market_open,
                    market_close_utc=market_close,
                    session_label=session_label,
                    is_half_day=is_half_day,
                )
            )


def _seed_market_events(session: Session) -> None:
    events = [
        (
            "NVDA",
            datetime(2026, 3, 18, 18, 0, tzinfo=UTC),
            "earnings_window",
            "high",
            "NVDA earnings window opens",
        ),
        (
            None,
            datetime(2026, 3, 18, 14, 15, tzinfo=UTC),
            "macro_release",
            "medium",
            "US macro release cluster",
        ),
    ]
    for symbol, event_ts, event_type, impact_level, title in events:
        existing = session.scalar(
            select(MarketEvent)
            .where(MarketEvent.symbol == symbol)
            .where(MarketEvent.event_ts == event_ts)
            .where(MarketEvent.title == title)
        )
        if existing is None:
            session.add(
                MarketEvent(
                    symbol=symbol,
                    event_ts=event_ts,
                    event_type=event_type,
                    impact_level=impact_level,
                    title=title,
                    source_document="dev_seed",
                    notes_md="Seeded for sandbox-safe event proximity checks.",
                )
            )
