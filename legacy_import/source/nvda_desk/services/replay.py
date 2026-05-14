from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import asc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import Bar1m, Instrument
from nvda_desk.domain.session_clock import SessionClockClassifier, SessionClockPhase
from nvda_desk.schemas.replay import (
    ReplayHorizonDiscoveryResponse,
    ReplayPhaseSummary,
    ReplaySessionResponse,
)


class ReplayService:
    def __init__(self, classifier: SessionClockClassifier, session_factory: sessionmaker[Session]):
        self._classifier = classifier
        self._session_factory = session_factory

    def replay_session_phases(
        self, symbol: str, start_ts: datetime, end_ts: datetime
    ) -> ReplaySessionResponse:
        with self._session_factory() as session:
            stmt = (
                select(Bar1m)
                .join(Instrument)
                .where(Instrument.symbol == symbol)
                .where(Bar1m.ts_utc >= start_ts)
                .where(Bar1m.ts_utc <= end_ts)
                .order_by(asc(Bar1m.ts_utc))
            )
            bars = list(session.scalars(stmt))

        grouped: dict[SessionClockPhase, list[Bar1m]] = defaultdict(list)
        for bar in bars:
            effective_ts = (
                bar.ts_utc if bar.ts_utc.tzinfo is not None else bar.ts_utc.replace(tzinfo=UTC)
            )
            phase = self._classifier.classify(effective_ts).phase
            grouped[phase].append(bar)

        phase_summaries: list[ReplayPhaseSummary] = []
        for phase in sorted(grouped.keys(), key=lambda item: item.value):
            phase_bars = grouped[phase]
            first = phase_bars[0]
            last = phase_bars[-1]
            open_price = first.open
            close_price = last.close
            return_pct = None
            if float(open_price) != 0:
                return_pct = float(((close_price - open_price) / open_price) * 100)
            phase_summaries.append(
                ReplayPhaseSummary(
                    phase=phase,
                    bar_count=len(phase_bars),
                    first_ts=first.ts_utc,
                    last_ts=last.ts_utc,
                    open_price=open_price,
                    close_price=close_price,
                    volume_total=sum(bar.volume for bar in phase_bars),
                    return_pct=return_pct,
                )
            )

        return ReplaySessionResponse(
            symbol=symbol,
            requested_at=datetime.now(tz=UTC),
            start_ts=start_ts,
            end_ts=end_ts,
            total_bars=len(bars),
            phase_summaries=phase_summaries,
        )


def serialize_horizon_discovery_response(
    response: ReplayHorizonDiscoveryResponse,
    output_path: str | Path,
) -> str:
    """Serialise a Gate 79 harness response to stable JSON."""

    serialised = json.dumps(response.model_dump(mode="json"), indent=2, sort_keys=True) + "\n"
    Path(output_path).write_text(serialised)
    return serialised
