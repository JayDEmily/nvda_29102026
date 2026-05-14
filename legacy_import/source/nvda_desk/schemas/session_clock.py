from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.domain.session_clock import SessionClockPhase, SessionClockState


class TradingVenue(StrEnum):
    """Bounded venues used by desk-calendar governance."""

    NASDAQ_US = "nasdaq_us"
    JPX_CASH = "jpx_cash"
    HKEX_CASH = "hkex_cash"
    SSE_CASH = "sse_cash"
    SZSE_CASH = "szse_cash"
    CFFEX_INDEX_FUTURES = "cffex_index_futures"


class VenueTimezone(StrEnum):
    """IANA timezone authority for supported desk venues."""

    AMERICA_NEW_YORK = "America/New_York"
    ASIA_TOKYO = "Asia/Tokyo"
    ASIA_HONG_KONG = "Asia/Hong_Kong"
    ASIA_SHANGHAI = "Asia/Shanghai"


class SessionTemplate(StrEnum):
    """Canonical session templates used before runtime calendar wiring."""

    US_EQUITY_CONTINUOUS = "us_equity_continuous"
    JPX_SPLIT_SESSION = "jpx_split_session"
    HKEX_SPLIT_SESSION_WITH_CAS = "hkex_split_session_with_cas"
    MAINLAND_CHINA_SPLIT_SESSION = "mainland_china_split_session"
    INDEX_FUTURES_SPLIT_SESSION = "index_futures_split_session"


class CalendarClosureClass(StrEnum):
    """Closure and abbreviation types that later carry and event gates may read."""

    WEEKEND = "weekend"
    FULL_HOLIDAY = "full_holiday"
    HALF_DAY = "half_day"
    HOLIDAY_EVE_HALF_DAY = "holiday_eve_half_day"
    BRIDGE_HOLIDAY = "bridge_holiday"
    MAKEUP_WORKING_DAY = "makeup_working_day"
    OBSERVED_HOLIDAY = "observed_holiday"


class SessionBridgeRule(StrEnum):
    """Bounded bridge rules for precursor and carry interpretation."""

    NO_SPECIAL_BRIDGE = "no_special_bridge"
    US_EARLY_CLOSE = "us_early_close"
    HK_HOLIDAY_EVE_HALF_DAY = "hk_holiday_eve_half_day"
    CHINA_WEEKEND_MAKEUP_WORKDAY = "china_weekend_makeup_workday"
    PRECURSOR_NEXT_US_SESSION_ONLY = "precursor_next_us_session_only"
    EXPIRY_COLLIDES_WITH_SHORTENED_SESSION = "expiry_collides_with_shortened_session"


class VenueSessionContract(BaseModel):
    """One venue/session contract frozen by Gate 66."""

    model_config = ConfigDict(extra="forbid")

    venue: TradingVenue
    timezone: VenueTimezone
    template: SessionTemplate
    trading_days: list[str] = Field(default_factory=list)
    order_acceptance_notes: list[str] = Field(default_factory=list)
    session_segments: list[str] = Field(default_factory=list)
    closure_classes: list[CalendarClosureClass] = Field(default_factory=list)
    bridge_rules: list[SessionBridgeRule] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class DeskCalendarAuthorityPacket(BaseModel):
    """Frozen Gate 66 calendar authority across US and precursor venues."""

    model_config = ConfigDict(extra="forbid")

    venues: list[VenueSessionContract] = Field(default_factory=list)
    closure_classes: list[CalendarClosureClass] = Field(default_factory=list)
    bridge_rules: list[SessionBridgeRule] = Field(default_factory=list)
    expiry_interaction_notes: list[str] = Field(default_factory=list)


class SessionClockFeaturePayload(BaseModel):
    phase: SessionClockPhase = Field(description="Deterministic v1 session phase")
    market_timezone: str
    ts_market: datetime
    minutes_since_open: int | None = None
    minutes_to_close: int | None = None
    is_pre_market: bool
    is_regular_hours: bool
    is_power_hour: bool
    phase_confidence: float = Field(ge=0.0, le=1.0)
    compatibility_policy: str = Field(default="legacy_wrapper_over_temporal_state")

    @classmethod
    def from_state(cls, state: SessionClockState) -> SessionClockFeaturePayload:
        return cls(
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
