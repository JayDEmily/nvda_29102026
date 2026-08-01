from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from nvda_desk.m02_financial_calendar.contracts import FinancialCalendarLayer


class ReferenceArtifactKind(StrEnum):
    CALENDAR_BUNDLE = "calendar_bundle"
    CROSSWALK = "crosswalk"
    REFERENCE_PACKET = "reference_packet"


@dataclass(slots=True)
class ReferenceArtifact:
    artifact_id: str
    kind: ReferenceArtifactKind
    source_path: str
    version: str


@dataclass(slots=True)
class BundleLayerReference:
    layer_id: str
    artifact_ids: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ImportedReferenceBundle:
    bundle_id: str
    version: str
    artifacts: list[ReferenceArtifact] = field(default_factory=list)
    layers: list[BundleLayerReference] = field(default_factory=list)


@dataclass(slots=True)
class LiveEventReference:
    event_id: str
    source_artifact_id: str
    observed_at: datetime


@dataclass(slots=True)
class LiveEventSnapshot:
    event_id: str
    event_type: str
    runtime_tags: list[str] = field(default_factory=list)
    evaluation_tags: list[str] = field(default_factory=list)
    reference: LiveEventReference | None = None


@dataclass(slots=True)
class CalendarAuthorityProjectionTrace:
    """Trace proving calendar runtime context came from checked reference material."""

    context_id: str
    bundle_id: str
    artifact_ids: list[str]
    event_ids: list[str]
    runtime_tags: list[str]
    effective_at: datetime
    projection_mode: str = "checked_reference_projection"
    online_mutation_allowed: bool = False
    candidate_formation_allowed: bool = False
    capital_sizing_allowed: bool = False


@dataclass(slots=True)
class PrecursorRuntimePacket:
    context_id: str
    effective_at: datetime
    events: list[LiveEventSnapshot] = field(default_factory=list)
    bundle: ImportedReferenceBundle | None = None
    projection_trace: CalendarAuthorityProjectionTrace | None = None


# Transitional K04 compatibility adapters. Canonical ownership lives in
# nvda_desk.m02_financial_calendar; these shapes preserve admitted callers only.
@dataclass(frozen=True, slots=True)
class FinancialCalendarAuthorityBundle:
    """Exact four-layer compatibility bundle narrowed toward K04."""

    market_session_reference: tuple[object, ...] = ()
    financial_event_reference: tuple[object, ...] = ()
    operational_calendar_state: tuple[object, ...] = ()
    derived_runtime_calendar_context: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class CalendarFactCandidate:
    """Legacy constructor adapter for one owner-issued K04 candidate fact."""

    candidate_id: str
    layer: FinancialCalendarLayer
    fact_family: str
    semantic_field: str
    value: object
    effective_at_utc: datetime
    source_artifact_id: str
    source_version: str = "compatibility-v1"
    value_type: str = "compatibility_scalar"
    unit: str | None = None
    owner_id: str = "compatibility_calendar_owner"


@dataclass(frozen=True, slots=True)
class CalendarFieldResolutionPolicy:
    """Legacy field-policy adapter with no caller-selected winner authority."""

    policy_id: str
    semantic_field: str
    mandatory: bool
    authoritative_layer: FinancialCalendarLayer


@dataclass(frozen=True, slots=True)
class CalendarFieldResolutionReceipt:
    """Compatibility receipt preserving selected value and all lineage."""

    selected_value: object
    candidate_ids: tuple[str, ...]
    source_refs: tuple[tuple[str, str], ...]
    layers: tuple[FinancialCalendarLayer, ...]


class CalendarFieldConflictError(ValueError):
    """Raised when compatibility candidates cannot be lawfully coalesced."""
