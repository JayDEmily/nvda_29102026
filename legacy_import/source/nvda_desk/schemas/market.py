from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.session_clock import SessionClockFeaturePayload
from nvda_desk.schemas.temporal_surface import TemporalStateFeaturePayload


class PrecursorVenueUniverse(StrEnum):
    """Bounded ex-US precursor venue families allowed by Gate 68."""

    JPX_CASH_INDEX_COMPLEX = "jpx_cash_index_complex"
    HKEX_CASH_INDEX_COMPLEX = "hkex_cash_index_complex"
    MAINLAND_CHINA_CASH_INDEX_COMPLEX = "mainland_china_cash_index_complex"
    CFFEX_INDEX_FUTURES_COMPLEX = "cffex_index_futures_complex"


class PrecursorSourceClass(StrEnum):
    """Permitted precursor source classes."""

    CASH_EQUITY_INDEX = "cash_equity_index"
    INDEX_FUTURES = "index_futures"


class RawPrecursorField(StrEnum):
    """Raw precursor facts allowed to enter later stitching gates."""

    SESSION_RETURN_PCT = "session_return_pct"
    OPENING_GAP_PCT = "opening_gap_pct"
    SESSION_RANGE_PCT = "session_range_pct"
    REALISED_VOL_PCT = "realised_vol_pct"
    CLOSE_LOCATION_IN_RANGE = "close_location_in_range"
    RELATIVE_VOLUME_RATIO = "relative_volume_ratio"
    FUTURES_BASIS_PCT = "futures_basis_pct"
    CLOSE_TIMESTAMP = "close_timestamp"


class DerivedPrecursorField(StrEnum):
    """Derived precursor summaries that later policy gates may consume."""

    DIRECTIONAL_COMPOSITE_SCORE = "directional_composite_score"
    CROSS_VENUE_AGREEMENT_SCORE = "cross_venue_agreement_score"
    FUTURES_CASH_DIVERGENCE_SCORE = "futures_cash_divergence_score"
    IMPULSE_PERSISTENCE_SCORE = "impulse_persistence_score"
    PRECURSOR_PRESSURE_SCORE = "precursor_pressure_score"
    CARRY_RISK_WARNING_SCORE = "carry_risk_warning_score"


class SessionAlignmentExpectation(StrEnum):
    """How precursor sessions align to the next US decision window."""

    USE_LAST_COMPLETE_SESSION = "use_last_complete_session"
    NO_PARTIAL_SESSION_PROJECTION = "no_partial_session_projection"
    MAP_TO_NEXT_US_CASH_OPEN = "map_to_next_us_cash_open"
    WEEKEND_AND_HOLIDAY_GAPS_MUST_STAY_EXPLICIT = "weekend_and_holiday_gaps_must_stay_explicit"


class ExcludedPrecursorSource(StrEnum):
    """Tempting but out-of-scope sources explicitly excluded by Gate 68."""

    EUROPEAN_CASH_INDICES = "european_cash_indices"
    COMMODITIES_COMPLEX = "commodities_complex"
    CRYPTO_24X7 = "crypto_24x7"
    SINGLE_STOCK_CHATTER = "single_stock_chatter"


class PrecursorVenueContract(BaseModel):
    """One bounded precursor venue contract frozen by Gate 68."""

    model_config = ConfigDict(extra="forbid")

    venue: PrecursorVenueUniverse
    source_class: PrecursorSourceClass
    included_in_live_read_set: bool = True
    allowed_raw_fields: list[RawPrecursorField] = Field(default_factory=list)
    allowed_derived_fields: list[DerivedPrecursorField] = Field(default_factory=list)
    session_alignment: list[SessionAlignmentExpectation] = Field(default_factory=list)
    rationale: list[str] = Field(default_factory=list)
    exclusion_notes: list[str] = Field(default_factory=list)


class PrecursorUniverseAuthorityPacket(BaseModel):
    """Frozen Gate 68 authority for precursor markets and allowed fields."""

    model_config = ConfigDict(extra="forbid")

    venues: list[PrecursorVenueContract] = Field(default_factory=list)
    raw_fields: list[RawPrecursorField] = Field(default_factory=list)
    derived_fields: list[DerivedPrecursorField] = Field(default_factory=list)
    session_alignment_expectations: list[SessionAlignmentExpectation] = Field(default_factory=list)
    excluded_sources: list[ExcludedPrecursorSource] = Field(default_factory=list)


class PrecursorTimestampDiscipline(StrEnum):
    """Deterministic timestamp rules frozen by Gate 75 precursor stitching law."""

    LAST_COMPLETE_SESSION_ONLY = "last_complete_session_only"
    VENUE_LOCAL_CLOSE_REQUIRED = "venue_local_close_required"
    REQUEST_TIME_MUST_NOT_PRECEDE_SOURCE_TIME = "request_time_must_not_precede_source_time"
    NO_FORWARD_FILL_ACROSS_US_DECISION_WINDOW = "no_forward_fill_across_us_decision_window"


class PrecursorFreshnessState(StrEnum):
    """Bounded freshness states for one precursor slice before runtime binding."""

    CURRENT = "current"
    DEGRADED = "degraded"
    STALE = "stale"
    MISSING = "missing"


class PrecursorFallbackDisposition(StrEnum):
    """Deterministic fallback choices for missing or degraded precursor truth."""

    CONTINUE_NORMALLY = "continue_normally"
    CONTINUE_WITH_DEGRADED_CONFIDENCE = "continue_with_degraded_confidence"
    CONTINUE_WITHOUT_VENUE = "continue_without_venue"
    REQUIRE_STAND_DOWN_PRESSURE = "require_stand_down_pressure"


class PrecursorContradictionClass(StrEnum):
    """Cross-venue contradiction classes frozen before later posture policy consumes them."""

    NONE = "none"
    DIRECTIONAL_SPLIT = "directional_split"
    FUTURES_CASH_DIVERGENCE = "futures_cash_divergence"
    TIMESTAMP_MISALIGNMENT = "timestamp_misalignment"
    BROAD_CROSS_VENUE_CONFLICT = "broad_cross_venue_conflict"


class PrecursorPostureState(StrEnum):
    """Review-visible precursor posture meaning prepared by Gate 75."""

    NORMAL_CONFIDENCE = "normal_confidence"
    DEGRADED_CONFIDENCE = "degraded_confidence"
    TIGHTENED_POSTURE = "tightened_posture"
    STAND_DOWN_PRESSURE = "stand_down_pressure"
    UNRESOLVED_CONTEXT = "unresolved_context"


class PrecursorVenueSlice(BaseModel):
    """One bounded precursor venue slice before cross-venue stitching."""

    model_config = ConfigDict(extra="forbid")

    venue: PrecursorVenueUniverse
    source_class: PrecursorSourceClass
    session_close_at: datetime
    observed_at: datetime
    freshness_state: PrecursorFreshnessState = PrecursorFreshnessState.CURRENT
    raw_values: dict[RawPrecursorField, float | datetime] = Field(default_factory=dict)
    derived_values: dict[DerivedPrecursorField, float] = Field(default_factory=dict)
    lineage_keys: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PrecursorStitchingResult(BaseModel):
    """Deterministic precursor assembly result produced before runtime binding."""

    model_config = ConfigDict(extra="forbid")

    requested_at: datetime
    stitched_order: list[PrecursorVenueUniverse] = Field(default_factory=list)
    active_slices: list[PrecursorVenueSlice] = Field(default_factory=list)
    missing_venues: list[PrecursorVenueUniverse] = Field(default_factory=list)
    dropped_venues: list[PrecursorVenueUniverse] = Field(default_factory=list)
    fallback_dispositions: list[PrecursorFallbackDisposition] = Field(default_factory=list)
    contradiction_class: PrecursorContradictionClass = PrecursorContradictionClass.NONE
    posture_state: PrecursorPostureState = PrecursorPostureState.NORMAL_CONFIDENCE
    lineage_keys: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PrecursorStitchingAuthorityPacket(BaseModel):
    """Frozen Gate 75 authority for precursor stitching, fallback, and contradiction law."""

    model_config = ConfigDict(extra="forbid")

    venue_order: list[PrecursorVenueUniverse] = Field(default_factory=list)
    timestamp_disciplines: list[PrecursorTimestampDiscipline] = Field(default_factory=list)
    freshness_states: list[PrecursorFreshnessState] = Field(default_factory=list)
    fallback_dispositions: list[PrecursorFallbackDisposition] = Field(default_factory=list)
    contradiction_classes: list[PrecursorContradictionClass] = Field(default_factory=list)
    posture_states: list[PrecursorPostureState] = Field(default_factory=list)


class PrecursorRuntimePacket(BaseModel):
    """Typed precursor packet preserved additively into runtime and review surfaces."""

    model_config = ConfigDict(extra="forbid")

    requested_at: datetime
    stitched_order: list[PrecursorVenueUniverse] = Field(default_factory=list)
    active_venues: list[PrecursorVenueUniverse] = Field(default_factory=list)
    missing_venues: list[PrecursorVenueUniverse] = Field(default_factory=list)
    raw_fields: list[RawPrecursorField] = Field(default_factory=list)
    derived_fields: list[DerivedPrecursorField] = Field(default_factory=list)
    derived_values: dict[DerivedPrecursorField, float] = Field(default_factory=dict)
    contradiction_class: PrecursorContradictionClass = PrecursorContradictionClass.NONE
    posture_state: PrecursorPostureState = PrecursorPostureState.NORMAL_CONFIDENCE
    fallback_dispositions: list[PrecursorFallbackDisposition] = Field(default_factory=list)
    lineage_keys: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class Bar1mPayload(BaseModel):
    ts_utc: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


class MarketSnapshotResponse(BaseModel):
    symbol: str
    requested_at: datetime
    temporal_state: TemporalStateFeaturePayload
    session_clock: SessionClockFeaturePayload
    latest_bar: Bar1mPayload | None = None


class IntradayBarsResponse(BaseModel):
    symbol: str
    requested_at: datetime
    bars: list[Bar1mPayload]
