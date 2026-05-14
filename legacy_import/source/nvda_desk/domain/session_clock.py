from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from nvda_desk.config import Settings


class SessionClockPhase(StrEnum):
    PRE_MARKET = "pre_market"
    OPEN_DISORDER = "open_disorder"
    EARLY_ANCHOR = "early_anchor"
    INSTITUTIONAL_REPRICING = "institutional_repricing"
    MIDDAY_COMPRESSION = "midday_compression"
    POST_LUNCH_DRIFT = "post_lunch_drift"
    POWER_HOUR = "power_hour"
    DEALER_UNWIND_CLOSE = "dealer_unwind_close"
    AFTER_HOURS = "after_hours"
    CLOSED = "closed"


@dataclass(frozen=True)
class SessionClockState:
    phase: SessionClockPhase
    market_timezone: str
    ts_market: datetime
    minutes_since_open: int | None
    minutes_to_close: int | None
    is_pre_market: bool
    is_regular_hours: bool
    is_power_hour: bool
    phase_confidence: float


class SessionClockClassifier:
    """Compatibility wrapper projecting the Step-1 temporal-state engine.

    This class remains available for legacy API and replay surfaces that only
    provide timestamps. The canonical Step-1 logic now lives in
    `TemporalStateClassifier`; timestamp-only callers receive its clock-prior
    projection with no extra primitive observables.
    """

    def __init__(self, settings: Settings):
        self._settings = settings

    def classify(self, ts: datetime) -> SessionClockState:
        from nvda_desk.domain.temporal_state import (
            TemporalSignalInput,
            TemporalStateClassifier,
        )

        state = TemporalStateClassifier(self._settings).classify(TemporalSignalInput(ts=ts))
        return SessionClockState(
            phase=state.phase,
            market_timezone=state.market_timezone,
            ts_market=state.ts_market,
            minutes_since_open=state.minutes_since_open,
            minutes_to_close=state.minutes_to_close,
            is_pre_market=state.is_pre_market,
            is_regular_hours=state.is_regular_hours,
            is_power_hour=state.is_power_hour,
            phase_confidence=state.phase_confidence,
        )
