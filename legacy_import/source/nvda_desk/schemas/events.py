from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ImpactLevel = Literal["low", "medium", "high"]


class DeskEventClass(StrEnum):
    """Bounded top-level event classes recognised by the desk."""

    COMPANY = "company"
    PEER_COMPANY = "peer_company"
    MACRO = "macro"
    POLICY = "policy"
    EXPIRY = "expiry"
    VENUE_SESSION = "venue_session"


class EventSemanticPhase(StrEnum):
    """Trader-grade distinction between existence, pricing, and realised path."""

    KNOWN_RISK = "known_risk"
    PRICED_RISK = "priced_risk"
    REALISED_REACTION = "realised_reaction"


class EventMaterialityTier(StrEnum):
    """Bounded impact ladder used before later posture matrices exist."""

    BACKGROUND = "background"
    MONITOR = "monitor"
    POSTURE_RELEVANT = "posture_relevant"
    DESK_CRITICAL = "desk_critical"


class CompanyEventSubclass(StrEnum):
    """NVDA-specific company events that are desk-relevant."""

    NVDA_EARNINGS = "nvda_earnings"
    NVDA_GUIDANCE = "nvda_guidance"
    NVDA_PRODUCT_EVENT = "nvda_product_event"
    NVDA_SHAREHOLDER_EVENT = "nvda_shareholder_event"
    NVDA_SUPPLY_CHAIN_UPDATE = "nvda_supply_chain_update"
    NVDA_REGULATORY_FILING = "nvda_regulatory_filing"


class PeerEventSubclass(StrEnum):
    """Bounded peer events used as contextual, not identity-defining, inputs."""

    MEGA_CAP_AI_EARNINGS = "mega_cap_ai_earnings"
    SEMICONDUCTOR_PEER_EARNINGS = "semiconductor_peer_earnings"
    PEER_GUIDANCE_RESET = "peer_guidance_reset"
    PEER_PRODUCT_EVENT = "peer_product_event"
    PEER_SUPPLY_CHAIN_WARNING = "peer_supply_chain_warning"


class MacroEventSubclass(StrEnum):
    """Bounded macro and data-release classes relevant to the NVDA desk."""

    CPI = "cpi"
    PPI = "ppi"
    NONFARM_PAYROLLS = "nonfarm_payrolls"
    RETAIL_SALES = "retail_sales"
    GDP = "gdp"
    ISM = "ism"
    JOBLESS_CLAIMS = "jobless_claims"
    TREASURY_AUCTION = "treasury_auction"


class PolicyEventSubclass(StrEnum):
    """Policy-significant events kept distinct from ordinary macro releases."""

    FOMC_RATE_DECISION = "fomc_rate_decision"
    FOMC_MINUTES = "fomc_minutes"
    FED_CHAIR_SPEECH = "fed_chair_speech"
    FED_SPEAKER_CLUSTER = "fed_speaker_cluster"
    BOJ_RATE_DECISION = "boj_rate_decision"
    PBOC_POLICY_SIGNAL = "pboc_policy_signal"
    US_EXPORT_CONTROL_ACTION = "us_export_control_action"


class ExpiryEventSubclass(StrEnum):
    """Expiry and maturity events that can distort posture lawfully."""

    WEEKLY_OPTIONS_EXPIRY = "weekly_options_expiry"
    MONTHLY_OPTIONS_EXPIRY = "monthly_options_expiry"
    QUARTERLY_EXPIRY = "quarterly_expiry"
    INDEX_OPTION_EXPIRY = "index_option_expiry"
    FUTURES_ROLL = "futures_roll"


class VenueSessionEventSubclass(StrEnum):
    """Venue and session-linked event classes required by later calendar gates."""

    MARKET_HOLIDAY = "market_holiday"
    HALF_DAY = "half_day"
    HOLIDAY_EVE = "holiday_eve"
    SESSION_DISLOCATION = "session_dislocation"
    CLOSING_AUCTION_DISTORTION = "closing_auction_distortion"


class EventTaxonomyRecord(BaseModel):
    """One governed event taxonomy record."""

    model_config = ConfigDict(extra="forbid")

    event_class: DeskEventClass
    subclass: str = Field(min_length=1)
    semantic_phase: EventSemanticPhase
    materiality_tier: EventMaterialityTier
    review_visible: bool = True
    notes: list[str] = Field(default_factory=list)


class EventTaxonomyAuthorityPacket(BaseModel):
    """Frozen Gate 65 authority packet for bounded event identity."""

    model_config = ConfigDict(extra="forbid")

    top_level_classes: list[DeskEventClass] = Field(default_factory=list)
    semantic_phases: list[EventSemanticPhase] = Field(default_factory=list)
    materiality_tiers: list[EventMaterialityTier] = Field(default_factory=list)
    company_subclasses: list[CompanyEventSubclass] = Field(default_factory=list)
    peer_subclasses: list[PeerEventSubclass] = Field(default_factory=list)
    macro_subclasses: list[MacroEventSubclass] = Field(default_factory=list)
    policy_subclasses: list[PolicyEventSubclass] = Field(default_factory=list)
    expiry_subclasses: list[ExpiryEventSubclass] = Field(default_factory=list)
    venue_session_subclasses: list[VenueSessionEventSubclass] = Field(default_factory=list)


class ExpiryCalendarInteraction(StrEnum):
    """How expiry semantics collide with calendar structure."""

    NORMAL_SESSION = "normal_session"
    EARLY_CLOSE_EXPIRY = "early_close_expiry"
    PRE_HOLIDAY_EXPIRY = "pre_holiday_expiry"
    POST_HOLIDAY_RESET = "post_holiday_reset"


class CalendarAwareEventContract(BaseModel):
    """One calendar-sensitive event interaction frozen by Gate 66."""

    model_config = ConfigDict(extra="forbid")

    venue_event_subclass: VenueSessionEventSubclass | None = None
    expiry_subclass: ExpiryEventSubclass | None = None
    expiry_calendar_interaction: ExpiryCalendarInteraction
    notes: list[str] = Field(default_factory=list)


class SessionCalendarCreate(BaseModel):
    session_date: date
    venue: str = Field(default="NASDAQ", min_length=1)
    market_open_utc: datetime
    market_close_utc: datetime
    session_label: str = Field(default="regular", min_length=1)
    is_half_day: bool = False


class SessionCalendarPayload(SessionCalendarCreate):
    calendar_id: int


class SessionCalendarListResponse(BaseModel):
    sessions: list[SessionCalendarPayload]


class MarketEventCreate(BaseModel):
    event_ts: datetime
    event_type: str = Field(min_length=1)
    title: str = Field(min_length=1)
    impact_level: ImpactLevel = "medium"
    symbol: str | None = Field(default=None, min_length=1)
    source_document: str = Field(default="manual", min_length=1)
    notes_md: str = ""


class MarketEventPayload(MarketEventCreate):
    event_id: int
    created_at: datetime


class MarketEventListResponse(BaseModel):
    events: list[MarketEventPayload]


class EventProximityResponse(BaseModel):
    requested_at: datetime
    symbol: str | None = None
    event_risk_window_open: bool
    upcoming_events: list[MarketEventPayload]
    recent_events: list[MarketEventPayload]


class EventSourceClass(StrEnum):
    """Bounded event-source classes supported by Gate 72."""

    EXCHANGE_CALENDAR = "exchange_calendar"
    ISSUER_IR = "issuer_ir"
    MACRO_CALENDAR = "macro_calendar"
    POLICY_CALENDAR = "policy_calendar"
    INTERNAL_CURATED = "internal_curated"
    OPTIONS_EXPIRY_CALENDAR = "options_expiry_calendar"


class SupportedEventSource(StrEnum):
    """Supported upstream event sources before shared store/query wiring."""

    NASDAQ_TRADER = "nasdaq_trader"
    ISSUER_INVESTOR_RELATIONS = "issuer_investor_relations"
    MACRO_RELEASE_CALENDAR = "macro_release_calendar"
    POLICY_RELEASE_CALENDAR = "policy_release_calendar"
    INTERNAL_EVENT_LEDGER = "internal_event_ledger"
    OPTIONS_EXPIRY_LEDGER = "options_expiry_ledger"


class EventFreshnessState(StrEnum):
    """Freshness states visible after provenance normalisation."""

    CURRENT = "current"
    STALE = "stale"
    DEFERRED = "deferred"


class EventConfidenceTier(StrEnum):
    """Confidence tiers visible after provenance normalisation."""

    AUTHORITATIVE = "authoritative"
    CORROBORATED = "corroborated"
    PROVISIONAL = "provisional"
    DEGRADED = "degraded"


class SourceConflictDisposition(StrEnum):
    """How source conflicts are surfaced rather than hidden."""

    AUTHORITATIVE_SOURCE_WINS = "authoritative_source_wins"
    LATEST_CORROBORATED_WINS = "latest_corroborated_wins"
    KEEP_CONFLICT_VISIBLE = "keep_conflict_visible"


class SourceOutagePolicy(StrEnum):
    """Fallback posture when one supported event source is degraded or absent."""

    USE_LAST_VERIFIED_WITH_FLAG = "use_last_verified_with_flag"
    DEGRADE_TO_UNKNOWN = "degrade_to_unknown"
    DROP_SOURCE_AND_BLOCK_UNSUPPORTED = "drop_source_and_block_unsupported"


class EventSourceInventoryRecord(BaseModel):
    """One supported source in the Gate 72 source inventory."""

    model_config = ConfigDict(extra="forbid")

    source: SupportedEventSource
    source_class: EventSourceClass
    notes: list[str] = Field(default_factory=list)


class EventSourceProvenance(BaseModel):
    """Normalised provenance contract carried by one event record."""

    model_config = ConfigDict(extra="forbid")

    source: SupportedEventSource
    source_class: EventSourceClass
    source_document: str = Field(min_length=1)
    observed_at: datetime
    freshness_state: EventFreshnessState
    confidence_tier: EventConfidenceTier
    conflict_disposition: SourceConflictDisposition = (
        SourceConflictDisposition.KEEP_CONFLICT_VISIBLE
    )
    outage_policy: SourceOutagePolicy | None = None
    lineage_key: str = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)


class RawEventSourceObservation(BaseModel):
    """One upstream event observation before provenance normalisation."""

    model_config = ConfigDict(extra="forbid")

    source: SupportedEventSource
    source_class: EventSourceClass
    symbol: str | None = None
    event_id: str = Field(min_length=1)
    event_at: datetime
    event_type: str = Field(min_length=1)
    label: str = Field(min_length=1)
    event_class: DeskEventClass | None = None
    event_subclass: str | None = Field(default=None, exclude_if=lambda value: value is None)
    semantic_phase: EventSemanticPhase = EventSemanticPhase.KNOWN_RISK
    materiality_tier: EventMaterialityTier = EventMaterialityTier.MONITOR
    layer_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    jurisdiction: str | None = Field(default=None, exclude_if=lambda value: value is None)
    venues: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    entities: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    runtime_tags: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    evaluation_tags: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    source_status: str | None = Field(default=None, exclude_if=lambda value: value is None)
    source_document: str = Field(min_length=1)
    repo_artifact_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    repo_artifact_path: str | None = Field(default=None, exclude_if=lambda value: value is None)
    import_lineage_key: str | None = Field(default=None, exclude_if=lambda value: value is None)
    window_start_at: datetime | None = Field(default=None, exclude_if=lambda value: value is None)
    window_end_at: datetime | None = Field(default=None, exclude_if=lambda value: value is None)
    observed_at: datetime
    freshness_state: EventFreshnessState
    confidence_tier: EventConfidenceTier
    lineage_key: str = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)
    outage_policy: SourceOutagePolicy | None = None


class NormalisedEventRecord(BaseModel):
    """Shared event truth after source normalisation and provenance freezing."""

    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(min_length=1)
    symbol: str | None = None
    event_id: str = Field(min_length=1)
    event_at: datetime
    event_type: str = Field(min_length=1)
    label: str = Field(min_length=1)
    event_class: DeskEventClass | None = None
    event_subclass: str | None = Field(default=None, exclude_if=lambda value: value is None)
    semantic_phase: EventSemanticPhase = EventSemanticPhase.KNOWN_RISK
    materiality_tier: EventMaterialityTier = EventMaterialityTier.MONITOR
    layer_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    jurisdiction: str | None = Field(default=None, exclude_if=lambda value: value is None)
    venues: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    entities: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    runtime_tags: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    evaluation_tags: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    source_status: str | None = Field(default=None, exclude_if=lambda value: value is None)
    source_document: str | None = Field(default=None, exclude_if=lambda value: value is None)
    repo_artifact_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    repo_artifact_path: str | None = Field(default=None, exclude_if=lambda value: value is None)
    import_lineage_key: str | None = Field(default=None, exclude_if=lambda value: value is None)
    window_start_at: datetime | None = Field(default=None, exclude_if=lambda value: value is None)
    window_end_at: datetime | None = Field(default=None, exclude_if=lambda value: value is None)
    provenance: list[EventSourceProvenance] = Field(default_factory=list)
    lineage_keys: list[str] = Field(default_factory=list)
    conflict_notes: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class EventIngestionAuthorityPacket(BaseModel):
    """Frozen Gate 72 authority for event-source ingestion and provenance."""

    model_config = ConfigDict(extra="forbid")

    source_inventory: list[EventSourceInventoryRecord] = Field(default_factory=list)
    source_classes: list[EventSourceClass] = Field(default_factory=list)
    supported_sources: list[SupportedEventSource] = Field(default_factory=list)
    freshness_states: list[EventFreshnessState] = Field(default_factory=list)
    confidence_tiers: list[EventConfidenceTier] = Field(default_factory=list)
    conflict_dispositions: list[SourceConflictDisposition] = Field(default_factory=list)
    outage_policies: list[SourceOutagePolicy] = Field(default_factory=list)


class ReplayEventConsumerMode(StrEnum):
    """Shared consumer modes allowed to read the bounded event store."""

    RUNTIME_NEARBY = "runtime_nearby"
    REVIEW_LINEAGE = "review_lineage"
    REPLAY_SESSION = "replay_session"


class EventQueryWindow(BaseModel):
    """Bounded nearby-event query window used by shared consumers."""

    model_config = ConfigDict(extra="forbid")

    lookback_minutes: int = Field(ge=0)
    lookahead_minutes: int = Field(ge=0)


class EventStoreQueryResult(BaseModel):
    """Shared event truth returned to runtime, review, or replay consumers."""

    model_config = ConfigDict(extra="forbid")

    requested_at: datetime
    symbol: str | None = None
    query_window: EventQueryWindow
    nearby_events: list[NormalisedEventRecord] = Field(default_factory=list)
    material_events: list[NormalisedEventRecord] = Field(default_factory=list)
    lineage_map: dict[str, list[str]] = Field(default_factory=dict)
    replay_mode: ReplayEventConsumerMode = ReplayEventConsumerMode.RUNTIME_NEARBY


class EventStoreAuthorityPacket(BaseModel):
    """Frozen Gate 73 authority for shared event-store and query surfaces."""

    model_config = ConfigDict(extra="forbid")

    default_query_window: EventQueryWindow
    default_materiality_floor: EventMaterialityTier = EventMaterialityTier.POSTURE_RELEVANT
    replay_modes: list[ReplayEventConsumerMode] = Field(default_factory=list)
    lineage_required: bool = True


class LiveEventReference(BaseModel):
    """Compact event identity packet preserved into live cognition input."""

    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(min_length=1)
    event_id: str = Field(min_length=1)
    event_at: datetime
    event_type: str = Field(min_length=1)
    label: str = Field(min_length=1)
    event_class: DeskEventClass | None = None
    event_subclass: str | None = Field(default=None, exclude_if=lambda value: value is None)
    semantic_phase: EventSemanticPhase = EventSemanticPhase.KNOWN_RISK
    materiality_tier: EventMaterialityTier = EventMaterialityTier.MONITOR
    layer_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    jurisdiction: str | None = Field(default=None, exclude_if=lambda value: value is None)
    venues: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    entities: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    runtime_tags: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    evaluation_tags: list[str] = Field(default_factory=list, exclude_if=lambda value: value == [])
    source_status: str | None = Field(default=None, exclude_if=lambda value: value is None)
    source_document: str | None = Field(default=None, exclude_if=lambda value: value is None)
    repo_artifact_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    import_lineage_key: str | None = Field(default=None, exclude_if=lambda value: value is None)
    window_start_at: datetime | None = Field(default=None, exclude_if=lambda value: value is None)
    window_end_at: datetime | None = Field(default=None, exclude_if=lambda value: value is None)
    provenance_count: int = Field(ge=0, default=0)
    lineage_keys: list[str] = Field(default_factory=list)


class LiveEventSnapshot(BaseModel):
    """Event-rich nearby-event packet preserved for live cognition and review."""

    model_config = ConfigDict(extra="forbid")

    requested_at: datetime
    symbol: str | None = None
    query_window: EventQueryWindow
    next_event: LiveEventReference | None = None
    nearby_events: list[LiveEventReference] = Field(default_factory=list)
    material_events: list[LiveEventReference] = Field(default_factory=list)
    lineage_keys: list[str] = Field(default_factory=list)


class LiveEventRichnessAuthorityPacket(BaseModel):
    """Frozen Gate 74 authority for preserving event richness into live packets."""

    model_config = ConfigDict(extra="forbid")

    identity_required: bool = True
    impact_required: bool = True
    provenance_required: bool = True
    nearby_summary_required: bool = True
    lineage_retention_required: bool = True
    timestamp_backcompat_required: bool = True
