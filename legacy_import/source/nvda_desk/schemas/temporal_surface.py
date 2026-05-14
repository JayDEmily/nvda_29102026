from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.domain.temporal_state import ClockEnvelope, TemporalState
from nvda_desk.schemas.session_clock import SessionClockFeaturePayload


class EventProximityState(StrEnum):
    """Bounded proximity states for upcoming or live events."""

    NO_EVENT_CONTEXT = "no_event_context"
    EVENT_SCHEDULED = "event_scheduled"
    EVENT_SAME_DAY = "event_same_day"
    EVENT_SAME_SESSION = "event_same_session"
    EVENT_IMMINENT = "event_imminent"
    EVENT_LIVE_OR_PASSED = "event_live_or_passed"


class EventWindowState(StrEnum):
    """Governed event-window states consumed by posture and review layers."""

    CLEAR_WINDOW = "clear_window"
    SAME_SESSION_EVENT_WINDOW = "same_session_event_window"
    EVENT_IMMINENT_WINDOW = "event_imminent_window"
    EVENT_LIVE_WINDOW = "event_live_window"
    EVENT_COOLING_OFF_WINDOW = "event_cooling_off_window"
    EVENT_MEMORY_WINDOW = "event_memory_window"


class EventOverlapClass(StrEnum):
    """How multiple event windows coexist or supersede each other."""

    SINGLE_EVENT = "single_event"
    STACKED_EVENT_CLUSTER = "stacked_event_cluster"
    OVERLAPPING_WINDOWS = "overlapping_windows"
    HIGHER_PRIORITY_WINDOW_SUPERSEDES = "higher_priority_window_supersedes"


class EventRiskTimingClass(StrEnum):
    """Whether the window reflects priced risk, live release, or memory effects."""

    PRICED_RISK = "priced_risk"
    LIVE_RELEASE = "live_release"
    REALISED_REACTION = "realised_reaction"
    COOLING_OFF = "cooling_off"
    EVENT_MEMORY = "event_memory"


class EventCarrySensitivity(StrEnum):
    """Whether an event window should die intraday or persist into carry decisions."""

    INTRADAY_ONLY = "intraday_only"
    CARRY_SENSITIVE = "carry_sensitive"
    NEXT_SESSION_MEMORY = "next_session_memory"


class EventWindowContract(BaseModel):
    """One governed event-window contract frozen by Gate 67."""

    model_config = ConfigDict(extra="forbid")

    event_family: str = Field(min_length=1)
    proximity_state: EventProximityState
    primary_window_state: EventWindowState
    overlap_class: EventOverlapClass = EventOverlapClass.SINGLE_EVENT
    risk_timing_class: EventRiskTimingClass
    carry_sensitivity: EventCarrySensitivity
    pre_window_minutes: int = Field(ge=0)
    post_window_minutes: int = Field(ge=0)
    cooling_off_minutes: int = Field(ge=0, default=0)
    memory_minutes: int = Field(ge=0, default=0)
    notes: list[str] = Field(default_factory=list)


class EventWindowAuthorityPacket(BaseModel):
    """Frozen Gate 67 authority for event-window semantics."""

    model_config = ConfigDict(extra="forbid")

    proximity_states: list[EventProximityState] = Field(default_factory=list)
    window_states: list[EventWindowState] = Field(default_factory=list)
    overlap_classes: list[EventOverlapClass] = Field(default_factory=list)
    risk_timing_classes: list[EventRiskTimingClass] = Field(default_factory=list)
    carry_sensitivity_classes: list[EventCarrySensitivity] = Field(default_factory=list)
    window_contracts: list[EventWindowContract] = Field(default_factory=list)


class TemporalStateFeaturePayload(BaseModel):
    """Canonical outward Step-1 surface for timestamp-driven temporal lookups."""

    phase: str = Field(description="Compatibility phase label projected from temporal state")
    behavioural_phase: str
    clock_envelope: ClockEnvelope
    market_timezone: str
    ts_market: datetime
    minutes_since_open: int | None = None
    minutes_to_close: int | None = None
    is_pre_market: bool
    is_regular_hours: bool
    is_power_hour: bool
    phase_confidence: float = Field(ge=0.0, le=1.0)
    signal_coverage_ratio: float = Field(ge=0.0, le=1.0)
    evidence_tags: list[str] = Field(default_factory=list)
    compatibility_policy: str = Field(default="session_clock_wrapper_retained")

    @classmethod
    def from_state(cls, state: TemporalState) -> TemporalStateFeaturePayload:
        return cls(
            phase=state.phase.value,
            behavioural_phase=state.behavioural_phase.value,
            clock_envelope=state.clock_envelope,
            market_timezone=state.market_timezone,
            ts_market=state.ts_market,
            minutes_since_open=state.minutes_since_open,
            minutes_to_close=state.minutes_to_close,
            is_pre_market=state.is_pre_market,
            is_regular_hours=state.is_regular_hours,
            is_power_hour=state.is_power_hour,
            phase_confidence=state.phase_confidence,
            signal_coverage_ratio=state.signal_coverage_ratio,
            evidence_tags=list(state.evidence_tags),
        )


class SessionClockCompatibilityPayload(SessionClockFeaturePayload):
    """Explicit compatibility wrapper over the canonical temporal-state surface."""

    compatibility_policy: str = Field(default="legacy_wrapper_over_temporal_state")
