from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import TypedDict

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.checkpoints import CheckpointObservation

from nvda_desk.schemas.events import (
    DeskEventClass,
    EventMaterialityTier,
    EventSemanticPhase,
    EventSourceClass,
    ExpiryEventSubclass,
    MacroEventSubclass,
    PeerEventSubclass,
    PolicyEventSubclass,
    SupportedEventSource,
    VenueSessionEventSubclass,
)


class FinancialCalendarLayerId(StrEnum):
    """Bounded layer identifiers supplied by the 2026 calendar bundle."""

    US_MARKET_STRUCTURE = "layer_01_us_market_structure"
    US_MACRO_POLICY = "layer_02_us_macro_policy"
    NVDA_SECTOR_CATALYSTS = "layer_03_nvda_sector_catalysts"
    ASIA_PRECURSOR_VENUE_CONTEXT = "layer_04_asia_precursor_venue_context"


class FinancialCalendarEventType(StrEnum):
    """Bounded bundle event types frozen before import code lands."""

    MARKET_HOLIDAY = "market_holiday"
    MARKET_HALF_DAY = "market_half_day"
    OPTIONS_HALF_DAY = "options_half_day"
    MONTHLY_OPTIONS_EXPIRY = "monthly_options_expiry"
    MONTH_END_MARKER = "month_end_marker"
    FOMC_WINDOW = "fomc_window"
    CPI_RELEASE = "cpi_release"
    EMPLOYMENT_SITUATION_RELEASE = "employment_situation_release"
    PPI_RELEASE = "ppi_release"
    PCE_RELEASE = "pce_release"
    GDP_RELEASE = "gdp_release"
    EARNINGS_RELEASE = "earnings_release"
    JPX_CASH_HOLIDAY = "jpx_cash_holiday"
    JPX_DERIVATIVES_HOLIDAY_OPEN = "jpx_derivatives_holiday_open"
    JPX_DERIVATIVES_HOLIDAY_CLOSED = "jpx_derivatives_holiday_closed"
    HKEX_CASH_HOLIDAY = "hkex_cash_holiday"
    HKEX_HALF_DAY = "hkex_half_day"
    STOCK_CONNECT_CLOSED = "stock_connect_closed"
    STOCK_CONNECT_HALF_DAY = "stock_connect_half_day"
    MAINLAND_CASH_HOLIDAY = "mainland_cash_holiday"


class FinancialCalendarProjectionTarget(StrEnum):
    """Canonical target surfaces that later gates may project into."""

    DESK_CALENDAR_AUTHORITY = "desk_calendar_authority"
    RAW_EVENT_INGESTION = "raw_event_ingestion"
    EVENT_STORE = "event_store"
    PRECURSOR_RUNTIME_PACKET = "precursor_runtime_packet"
    TEMPORAL_CONTEXT = "temporal_context"


class FinancialCalendarEntityScope(StrEnum):
    """Entity-family selectors required by the bundle crosswalk."""

    ANY = "any"
    NVDA_ONLY = "nvda_only"
    DIRECT_READTHROUGH_MEGA_CAP = "direct_readthrough_mega_cap"


class FinancialCalendarRetainedField(StrEnum):
    """Fields that must survive import and canonical projection."""

    EVENT_ID = "event_id"
    LAYER_ID = "layer_id"
    EVENT_TYPE = "event_type"
    TITLE = "title"
    START_DATE = "start_date"
    END_DATE = "end_date"
    START_TIME_LOCAL = "start_time_local"
    END_TIME_LOCAL = "end_time_local"
    TIMEZONE = "timezone"
    JURISDICTION = "jurisdiction"
    VENUES = "venues"
    ENTITIES = "entities"
    IMPACT_LEVEL = "impact_level"
    RUNTIME_TAGS = "runtime_tags"
    EVALUATION_TAGS = "evaluation_tags"
    SOURCE_STATUS = "source_status"
    SOURCE_DOCUMENT = "source_document"
    NOTES_MD = "notes_md"
    REPO_ARTIFACT_PATH = "repo_artifact_path"
    REPO_ARTIFACT_ID = "repo_artifact_id"
    IMPORT_LINEAGE_KEY = "import_lineage_key"


class FinancialCalendarReferenceArtifactKind(StrEnum):
    """Repo-controlled artefact kinds for the reference-bundle lane."""

    MASTER_MANIFEST = "master_manifest"
    SOURCE_MANIFEST = "source_manifest"
    LAYER_JSON = "layer_json"
    BUNDLE_README = "bundle_readme"
    BINDING_PLAN = "binding_plan"
    CHECKSUM_MANIFEST = "checksum_manifest"
    EXTERNAL_EXAMPLE_PACKET = "external_example_packet"
    EXTERNAL_VALIDATION_RESULT = "external_validation_result"


class FinancialCalendarReferenceArtifact(BaseModel):
    """One repo-controlled reference artefact used by the bundle lane."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1)
    artifact_kind: FinancialCalendarReferenceArtifactKind
    repo_path: str = Field(min_length=1)
    media_type: str = Field(min_length=1)
    schema_id: str = Field(min_length=1)
    checksum: str | None = None
    byte_count: int | None = Field(default=None, ge=0)


class FinancialCalendarBundleLayerReference(BaseModel):
    """Layer pointer stored in the bundle master manifest."""

    model_config = ConfigDict(extra="forbid")

    layer_id: FinancialCalendarLayerId
    title: str = Field(min_length=1)
    file: str = Field(min_length=1)
    event_count: int = Field(ge=0)


class FinancialCalendarRepoFit(BaseModel):
    """Repo-fit metadata preserved from the supplied bundle master."""

    model_config = ConfigDict(extra="forbid")

    intended_root: str = Field(min_length=1)
    paired_runtime_consumers: list[str] = Field(default_factory=list)
    paired_schemas: list[str] = Field(default_factory=list)
    import_style: str = Field(min_length=1)


class FinancialCalendarBundleMetadata(BaseModel):
    """Compact metadata object preserved from the checked-in reference bundle."""

    model_config = ConfigDict(extra="forbid")

    bundle_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    calendar_year: int = Field(ge=2000)
    authority: str = Field(min_length=1)
    design_goal: str = Field(min_length=1)
    repo_fit: FinancialCalendarRepoFit
    layers: list[FinancialCalendarBundleLayerReference] = Field(default_factory=list)
    source_manifest_file: str = Field(min_length=1)
    coverage_notes: list[str] = Field(default_factory=list)


class FinancialCalendarReferenceBundlePayload(BaseModel):
    """DMPV3 payload carrying bundle metadata plus authoritative artefact references."""

    model_config = ConfigDict(extra="forbid")

    metadata: FinancialCalendarBundleMetadata
    artifacts: list[FinancialCalendarReferenceArtifact] = Field(default_factory=list)
    active_reference_packet_shell: str = Field(min_length=1)
    checkpoint_observations: list[CheckpointObservation] = Field(default_factory=list)


class FinancialCalendarReferenceEvent(BaseModel):
    """Raw reference event as supplied by one checked-in layer artefact."""

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=1)
    layer_id: FinancialCalendarLayerId
    event_type: FinancialCalendarEventType
    title: str = Field(min_length=1)
    start_date: date
    end_date: date
    start_time_local: str | None = None
    end_time_local: str | None = None
    timezone: str = Field(min_length=1)
    jurisdiction: str = Field(min_length=1)
    venues: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    impact_level: str = Field(min_length=1)
    runtime_tags: list[str] = Field(default_factory=list)
    evaluation_tags: list[str] = Field(default_factory=list)
    source_status: str = Field(min_length=1)
    source_document: str = Field(min_length=1)
    notes_md: str = ""


class FinancialCalendarLayerArtifact(BaseModel):
    """One layer JSON file after repo-controlled import."""

    model_config = ConfigDict(extra="forbid")

    layer_id: FinancialCalendarLayerId
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    calendar_year: int = Field(ge=2000)
    events: list[FinancialCalendarReferenceEvent] = Field(default_factory=list)


class FinancialCalendarImportedRecord(BaseModel):
    """Provenance-bearing import-stage record frozen before canonical projection."""

    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(min_length=1)
    repo_artifact_id: str = Field(min_length=1)
    repo_artifact_path: str = Field(min_length=1)
    import_lineage_key: str = Field(min_length=1)
    event_id: str = Field(min_length=1)
    layer_id: FinancialCalendarLayerId
    event_type: FinancialCalendarEventType
    title: str = Field(min_length=1)
    start_date: date
    end_date: date
    start_time_local: str | None = None
    end_time_local: str | None = None
    timezone: str = Field(min_length=1)
    jurisdiction: str = Field(min_length=1)
    venues: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    impact_level: str = Field(min_length=1)
    runtime_tags: list[str] = Field(default_factory=list)
    evaluation_tags: list[str] = Field(default_factory=list)
    source_status: str = Field(min_length=1)
    source_document: str = Field(min_length=1)
    notes_md: str = ""


class FinancialCalendarRepoManifest(BaseModel):
    """Repo-controlled manifest for the checked-in reference bundle."""

    model_config = ConfigDict(extra="forbid")

    bundle_root: str = Field(min_length=1)
    bundle_metadata_file: str = Field(min_length=1)
    layer_files: list[str] = Field(default_factory=list)
    source_manifest_file: str = Field(min_length=1)
    checksum_manifest_file: str = Field(min_length=1)
    supporting_files: list[str] = Field(default_factory=list)
    active_reference_packet_shell: str | None = None
    import_status: str = Field(min_length=1)


class FinancialCalendarImportedBundle(BaseModel):
    """Repo-controlled view over the checked-in bundle plus imported records."""

    model_config = ConfigDict(extra="forbid")

    metadata: FinancialCalendarBundleMetadata
    repo_manifest: FinancialCalendarRepoManifest
    artifacts: list[FinancialCalendarReferenceArtifact] = Field(default_factory=list)
    imported_records: list[FinancialCalendarImportedRecord] = Field(default_factory=list)
    checkpoint_observations: list[CheckpointObservation] = Field(default_factory=list)


class FinancialCalendarCrosswalkRecord(BaseModel):
    """Deterministic mapping from bundle fact family into repo-native surfaces."""

    model_config = ConfigDict(extra="forbid")

    bundle_event_type: FinancialCalendarEventType
    layer_id: FinancialCalendarLayerId
    entity_scope: FinancialCalendarEntityScope = FinancialCalendarEntityScope.ANY
    projection_targets: list[FinancialCalendarProjectionTarget] = Field(default_factory=list)
    supported_source: SupportedEventSource
    source_class: EventSourceClass
    event_class: DeskEventClass | None = None
    event_subclass: str | None = None
    semantic_phase: EventSemanticPhase
    materiality_tier: EventMaterialityTier
    retained_fields: list[FinancialCalendarRetainedField] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class FinancialCalendarRetainedFieldMatrix(BaseModel):
    """Named retained-field families required by the tranche."""

    model_config = ConfigDict(extra="forbid")

    import_stage: list[FinancialCalendarRetainedField] = Field(default_factory=list)
    canonical_projection: list[FinancialCalendarRetainedField] = Field(default_factory=list)
    review_runtime_explanation: list[FinancialCalendarRetainedField] = Field(default_factory=list)


DEFAULT_RETAINED_FIELD_MATRIX = FinancialCalendarRetainedFieldMatrix(
    import_stage=list(FinancialCalendarRetainedField),
    canonical_projection=[
        FinancialCalendarRetainedField.EVENT_ID,
        FinancialCalendarRetainedField.LAYER_ID,
        FinancialCalendarRetainedField.EVENT_TYPE,
        FinancialCalendarRetainedField.TITLE,
        FinancialCalendarRetainedField.START_DATE,
        FinancialCalendarRetainedField.END_DATE,
        FinancialCalendarRetainedField.TIMEZONE,
        FinancialCalendarRetainedField.JURISDICTION,
        FinancialCalendarRetainedField.VENUES,
        FinancialCalendarRetainedField.ENTITIES,
        FinancialCalendarRetainedField.IMPACT_LEVEL,
        FinancialCalendarRetainedField.RUNTIME_TAGS,
        FinancialCalendarRetainedField.EVALUATION_TAGS,
        FinancialCalendarRetainedField.SOURCE_STATUS,
        FinancialCalendarRetainedField.SOURCE_DOCUMENT,
        FinancialCalendarRetainedField.NOTES_MD,
        FinancialCalendarRetainedField.REPO_ARTIFACT_ID,
        FinancialCalendarRetainedField.REPO_ARTIFACT_PATH,
        FinancialCalendarRetainedField.IMPORT_LINEAGE_KEY,
    ],
    review_runtime_explanation=[
        FinancialCalendarRetainedField.EVENT_ID,
        FinancialCalendarRetainedField.LAYER_ID,
        FinancialCalendarRetainedField.EVENT_TYPE,
        FinancialCalendarRetainedField.TITLE,
        FinancialCalendarRetainedField.JURISDICTION,
        FinancialCalendarRetainedField.VENUES,
        FinancialCalendarRetainedField.ENTITIES,
        FinancialCalendarRetainedField.RUNTIME_TAGS,
        FinancialCalendarRetainedField.EVALUATION_TAGS,
        FinancialCalendarRetainedField.SOURCE_STATUS,
        FinancialCalendarRetainedField.SOURCE_DOCUMENT,
        FinancialCalendarRetainedField.REPO_ARTIFACT_ID,
        FinancialCalendarRetainedField.IMPORT_LINEAGE_KEY,
    ],
)


class _FinancialCalendarCrosswalkCommon(TypedDict):
    retained_fields: list[FinancialCalendarRetainedField]
    semantic_phase: EventSemanticPhase


def default_financial_calendar_crosswalk() -> list[FinancialCalendarCrosswalkRecord]:
    """Return the deterministic Gate 89 crosswalk for the 2026 bundle."""

    common: _FinancialCalendarCrosswalkCommon = {
        "retained_fields": list(DEFAULT_RETAINED_FIELD_MATRIX.canonical_projection),
        "semantic_phase": EventSemanticPhase.KNOWN_RISK,
    }
    return [
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.MARKET_HOLIDAY,
            layer_id=FinancialCalendarLayerId.US_MARKET_STRUCTURE,
            projection_targets=[
                FinancialCalendarProjectionTarget.DESK_CALENDAR_AUTHORITY,
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.NASDAQ_TRADER,
            source_class=EventSourceClass.EXCHANGE_CALENDAR,
            event_class=DeskEventClass.VENUE_SESSION,
            event_subclass=VenueSessionEventSubclass.MARKET_HOLIDAY.value,
            materiality_tier=EventMaterialityTier.DESK_CRITICAL,
            notes=["US cash and options closure facts become desk-calendar truth before any behavioural routing."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.MARKET_HALF_DAY,
            layer_id=FinancialCalendarLayerId.US_MARKET_STRUCTURE,
            projection_targets=[
                FinancialCalendarProjectionTarget.DESK_CALENDAR_AUTHORITY,
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.NASDAQ_TRADER,
            source_class=EventSourceClass.EXCHANGE_CALENDAR,
            event_class=DeskEventClass.VENUE_SESSION,
            event_subclass=VenueSessionEventSubclass.HALF_DAY.value,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            notes=["US half-day semantics must survive into carry/session routing."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.OPTIONS_HALF_DAY,
            layer_id=FinancialCalendarLayerId.US_MARKET_STRUCTURE,
            projection_targets=[
                FinancialCalendarProjectionTarget.DESK_CALENDAR_AUTHORITY,
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.OPTIONS_EXPIRY_LEDGER,
            source_class=EventSourceClass.OPTIONS_EXPIRY_CALENDAR,
            event_class=DeskEventClass.VENUE_SESSION,
            event_subclass=VenueSessionEventSubclass.HALF_DAY.value,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            notes=["US options half-day state remains explicit alongside cash-session structure."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.MONTHLY_OPTIONS_EXPIRY,
            layer_id=FinancialCalendarLayerId.US_MARKET_STRUCTURE,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.OPTIONS_EXPIRY_LEDGER,
            source_class=EventSourceClass.OPTIONS_EXPIRY_CALENDAR,
            event_class=DeskEventClass.EXPIRY,
            event_subclass=ExpiryEventSubclass.MONTHLY_OPTIONS_EXPIRY.value,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            notes=["Monthly expiry anchors may inform posture later but are not direct alpha by themselves."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.MONTH_END_MARKER,
            layer_id=FinancialCalendarLayerId.US_MARKET_STRUCTURE,
            projection_targets=[FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT],
            supported_source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            event_class=None,
            event_subclass=None,
            materiality_tier=EventMaterialityTier.MONITOR,
            notes=["Month-end markers stay bounded temporal context, not free-form event-taxonomy expansion."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.FOMC_WINDOW,
            layer_id=FinancialCalendarLayerId.US_MACRO_POLICY,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.POLICY_RELEASE_CALENDAR,
            source_class=EventSourceClass.POLICY_CALENDAR,
            event_class=DeskEventClass.POLICY,
            event_subclass=PolicyEventSubclass.FOMC_RATE_DECISION.value,
            materiality_tier=EventMaterialityTier.DESK_CRITICAL,
            notes=["The bundle stores a decision window; canonical taxonomy remains policy-led rather than inventing a new window subclass."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.CPI_RELEASE,
            layer_id=FinancialCalendarLayerId.US_MACRO_POLICY,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.MACRO_RELEASE_CALENDAR,
            source_class=EventSourceClass.MACRO_CALENDAR,
            event_class=DeskEventClass.MACRO,
            event_subclass=MacroEventSubclass.CPI.value,
            materiality_tier=EventMaterialityTier.DESK_CRITICAL,
            notes=["CPI is already canonical macro taxonomy; no new macro subclass is created here."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.EMPLOYMENT_SITUATION_RELEASE,
            layer_id=FinancialCalendarLayerId.US_MACRO_POLICY,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.MACRO_RELEASE_CALENDAR,
            source_class=EventSourceClass.MACRO_CALENDAR,
            event_class=DeskEventClass.MACRO,
            event_subclass=MacroEventSubclass.NONFARM_PAYROLLS.value,
            materiality_tier=EventMaterialityTier.DESK_CRITICAL,
            notes=["Employment Situation releases map to the existing nonfarm-payrolls taxonomy surface."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.PPI_RELEASE,
            layer_id=FinancialCalendarLayerId.US_MACRO_POLICY,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.MACRO_RELEASE_CALENDAR,
            source_class=EventSourceClass.MACRO_CALENDAR,
            event_class=DeskEventClass.MACRO,
            event_subclass=MacroEventSubclass.PPI.value,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.PCE_RELEASE,
            layer_id=FinancialCalendarLayerId.US_MACRO_POLICY,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.MACRO_RELEASE_CALENDAR,
            source_class=EventSourceClass.MACRO_CALENDAR,
            event_class=DeskEventClass.MACRO,
            event_subclass=None,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            notes=["PCE does not yet have a dedicated canonical subclass; it remains macro without creating a free-text taxonomy expansion in Gate 89."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.GDP_RELEASE,
            layer_id=FinancialCalendarLayerId.US_MACRO_POLICY,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.MACRO_RELEASE_CALENDAR,
            source_class=EventSourceClass.MACRO_CALENDAR,
            event_class=DeskEventClass.MACRO,
            event_subclass=MacroEventSubclass.GDP.value,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.EARNINGS_RELEASE,
            layer_id=FinancialCalendarLayerId.NVDA_SECTOR_CATALYSTS,
            entity_scope=FinancialCalendarEntityScope.NVDA_ONLY,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.ISSUER_INVESTOR_RELATIONS,
            source_class=EventSourceClass.ISSUER_IR,
            event_class=DeskEventClass.COMPANY,
            event_subclass="nvda_earnings",
            materiality_tier=EventMaterialityTier.DESK_CRITICAL,
            notes=["NVDA-confirmed earnings remain company identity, not peer context."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.EARNINGS_RELEASE,
            layer_id=FinancialCalendarLayerId.NVDA_SECTOR_CATALYSTS,
            entity_scope=FinancialCalendarEntityScope.DIRECT_READTHROUGH_MEGA_CAP,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.TEMPORAL_CONTEXT,
            ],
            supported_source=SupportedEventSource.ISSUER_INVESTOR_RELATIONS,
            source_class=EventSourceClass.ISSUER_IR,
            event_class=DeskEventClass.PEER_COMPANY,
            event_subclass=PeerEventSubclass.MEGA_CAP_AI_EARNINGS.value,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            notes=["Direct-readthrough mega-cap earnings remain contextual peer-company events."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.JPX_CASH_HOLIDAY,
            layer_id=FinancialCalendarLayerId.ASIA_PRECURSOR_VENUE_CONTEXT,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.PRECURSOR_RUNTIME_PACKET,
            ],
            supported_source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            event_class=DeskEventClass.VENUE_SESSION,
            event_subclass=VenueSessionEventSubclass.MARKET_HOLIDAY.value,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            notes=["JPX cash holidays are precursor venue-state truth and may remain visible in nearby-event review."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.JPX_DERIVATIVES_HOLIDAY_OPEN,
            layer_id=FinancialCalendarLayerId.ASIA_PRECURSOR_VENUE_CONTEXT,
            projection_targets=[FinancialCalendarProjectionTarget.PRECURSOR_RUNTIME_PACKET],
            supported_source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            event_class=None,
            event_subclass=None,
            materiality_tier=EventMaterialityTier.MONITOR,
            notes=["Holiday-trading exceptions belong to precursor runtime truth, not the canonical event taxonomy."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.JPX_DERIVATIVES_HOLIDAY_CLOSED,
            layer_id=FinancialCalendarLayerId.ASIA_PRECURSOR_VENUE_CONTEXT,
            projection_targets=[FinancialCalendarProjectionTarget.PRECURSOR_RUNTIME_PACKET],
            supported_source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            event_class=None,
            event_subclass=None,
            materiality_tier=EventMaterialityTier.MONITOR,
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.HKEX_CASH_HOLIDAY,
            layer_id=FinancialCalendarLayerId.ASIA_PRECURSOR_VENUE_CONTEXT,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.PRECURSOR_RUNTIME_PACKET,
            ],
            supported_source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            event_class=DeskEventClass.VENUE_SESSION,
            event_subclass=VenueSessionEventSubclass.MARKET_HOLIDAY.value,
            materiality_tier=EventMaterialityTier.POSTURE_RELEVANT,
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.HKEX_HALF_DAY,
            layer_id=FinancialCalendarLayerId.ASIA_PRECURSOR_VENUE_CONTEXT,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.PRECURSOR_RUNTIME_PACKET,
            ],
            supported_source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            event_class=DeskEventClass.VENUE_SESSION,
            event_subclass=VenueSessionEventSubclass.HALF_DAY.value,
            materiality_tier=EventMaterialityTier.MONITOR,
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.STOCK_CONNECT_CLOSED,
            layer_id=FinancialCalendarLayerId.ASIA_PRECURSOR_VENUE_CONTEXT,
            projection_targets=[FinancialCalendarProjectionTarget.PRECURSOR_RUNTIME_PACKET],
            supported_source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            event_class=None,
            event_subclass=None,
            materiality_tier=EventMaterialityTier.MONITOR,
            notes=["Stock Connect closure state is preserved for precursor alignment, not expanded into free-text event taxonomy."],
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.STOCK_CONNECT_HALF_DAY,
            layer_id=FinancialCalendarLayerId.ASIA_PRECURSOR_VENUE_CONTEXT,
            projection_targets=[FinancialCalendarProjectionTarget.PRECURSOR_RUNTIME_PACKET],
            supported_source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            event_class=None,
            event_subclass=None,
            materiality_tier=EventMaterialityTier.MONITOR,
            **common,
        ),
        FinancialCalendarCrosswalkRecord(
            bundle_event_type=FinancialCalendarEventType.MAINLAND_CASH_HOLIDAY,
            layer_id=FinancialCalendarLayerId.ASIA_PRECURSOR_VENUE_CONTEXT,
            projection_targets=[
                FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION,
                FinancialCalendarProjectionTarget.EVENT_STORE,
                FinancialCalendarProjectionTarget.PRECURSOR_RUNTIME_PACKET,
            ],
            supported_source=SupportedEventSource.INTERNAL_EVENT_LEDGER,
            source_class=EventSourceClass.INTERNAL_CURATED,
            event_class=DeskEventClass.VENUE_SESSION,
            event_subclass=VenueSessionEventSubclass.MARKET_HOLIDAY.value,
            materiality_tier=EventMaterialityTier.MONITOR,
            **common,
        ),
    ]
