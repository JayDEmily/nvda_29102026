"""Project imported calendar reference facts into runtime precursor contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable, Mapping

from nvda_desk.contracts.reference_data import (
    CalendarAuthorityProjectionTrace,
    ImportedReferenceBundle,
    LiveEventReference,
    LiveEventSnapshot,
    PrecursorRuntimePacket,
)

_FORBIDDEN_EVENT_ROW_KEYS = frozenset(
    {
        "candidate_id",
        "candidate_formation",
        "trading_instruction",
        "capital_sizing",
        "order_id",
        "broker_submit",
    }
)


@dataclass(slots=True)
class FinancialCalendarCrosswalkRecord:
    """One deterministic mapping from a source event type into runtime tags."""

    source_event_type: str
    runtime_tags: list[str] = field(default_factory=list)
    evaluation_tags: list[str] = field(default_factory=list)
    projection_targets: list[str] = field(default_factory=lambda: ["precursor_runtime_packet"])


_DEFAULT_CROSSWALK: tuple[FinancialCalendarCrosswalkRecord, ...] = (
    FinancialCalendarCrosswalkRecord(
        source_event_type="market_holiday",
        runtime_tags=["venue_holiday", "calendar_authority"],
        evaluation_tags=["session_structure"],
    ),
    FinancialCalendarCrosswalkRecord(
        source_event_type="market_half_day",
        runtime_tags=["venue_half_day", "calendar_authority"],
        evaluation_tags=["session_structure"],
    ),
    FinancialCalendarCrosswalkRecord(
        source_event_type="monthly_options_expiry",
        runtime_tags=["options_expiry", "calendar_authority"],
        evaluation_tags=["expiry_context"],
    ),
    FinancialCalendarCrosswalkRecord(
        source_event_type="fomc_window",
        runtime_tags=["macro_policy", "calendar_authority"],
        evaluation_tags=["event_risk"],
    ),
)


class FinancialCalendarProjectionService:
    """Project imported reference bundles into precursor runtime packets."""

    def project_runtime_context(
        self,
        *,
        bundle: ImportedReferenceBundle,
        event_rows: Iterable[Mapping[str, Any]],
        context_id: str,
        effective_at: datetime,
    ) -> PrecursorRuntimePacket:
        return project_runtime_context(
            bundle=bundle,
            event_rows=event_rows,
            context_id=context_id,
            effective_at=effective_at,
        )


class MarketStateService:
    """Small deterministic market-state bridge for calendar projection."""

    def stitch_precursor_context(
        self,
        *,
        bundle: ImportedReferenceBundle,
        events: Iterable[LiveEventSnapshot],
        context_id: str,
        effective_at: datetime,
    ) -> PrecursorRuntimePacket:
        return stitch_precursor_context(
            bundle=bundle,
            events=events,
            context_id=context_id,
            effective_at=effective_at,
        )


def _crosswalk_for(source_event_type: str) -> FinancialCalendarCrosswalkRecord:
    for record in _DEFAULT_CROSSWALK:
        if record.source_event_type == source_event_type:
            return record
    return FinancialCalendarCrosswalkRecord(source_event_type=source_event_type)


def _artifact_ids(bundle: ImportedReferenceBundle) -> set[str]:
    return {artifact.artifact_id for artifact in bundle.artifacts}


def _projection_trace(
    *,
    bundle: ImportedReferenceBundle,
    context_id: str,
    effective_at: datetime,
    events: list[LiveEventSnapshot],
) -> CalendarAuthorityProjectionTrace:
    runtime_tags = sorted({tag for event in events for tag in event.runtime_tags})
    return CalendarAuthorityProjectionTrace(
        context_id=context_id,
        bundle_id=bundle.bundle_id,
        artifact_ids=sorted(_artifact_ids(bundle)),
        event_ids=[event.event_id for event in events],
        runtime_tags=runtime_tags,
        effective_at=effective_at,
    )


def _validate_row(
    *,
    row: Mapping[str, Any],
    artifact_ids: set[str],
    effective_at: datetime,
) -> tuple[str, str, datetime]:
    forbidden = sorted(_FORBIDDEN_EVENT_ROW_KEYS & set(row))
    if forbidden:
        raise ValueError(
            f"calendar event row contains forbidden runtime authority keys: {forbidden}"
        )
    event_id = str(row["event_id"]).strip()
    if not event_id:
        raise ValueError("calendar event_id must be non-empty")
    source_artifact_id = str(row.get("source_artifact_id", "")).strip()
    if not source_artifact_id:
        if len(artifact_ids) == 1:
            source_artifact_id = next(iter(artifact_ids))
        else:
            raise ValueError(
                "calendar event rows must name source_artifact_id for multi-artifact bundles"
            )
    if source_artifact_id not in artifact_ids:
        raise ValueError(
            f"calendar event references unknown source_artifact_id: {source_artifact_id}"
        )
    observed_at = row.get("observed_at", effective_at)
    if not isinstance(observed_at, datetime):
        raise ValueError("calendar observed_at must be a datetime when supplied")
    return event_id, source_artifact_id, observed_at


def project_runtime_context(
    *,
    bundle: ImportedReferenceBundle,
    event_rows: Iterable[Mapping[str, Any]],
    context_id: str,
    effective_at: datetime,
) -> PrecursorRuntimePacket:
    """Build one precursor runtime packet from imported event rows."""

    artifact_ids = _artifact_ids(bundle)
    if not artifact_ids:
        raise ValueError("calendar projection requires at least one checked reference artifact")
    snapshots: list[LiveEventSnapshot] = []
    seen_event_ids: set[str] = set()
    for row in event_rows:
        event_id, source_artifact_id, observed_at = _validate_row(
            row=row,
            artifact_ids=artifact_ids,
            effective_at=effective_at,
        )
        if event_id in seen_event_ids:
            raise ValueError(f"duplicate calendar event_id values are not allowed: {event_id}")
        seen_event_ids.add(event_id)
        event_type = str(row["event_type"])
        crosswalk = _crosswalk_for(event_type)
        snapshots.append(
            LiveEventSnapshot(
                event_id=event_id,
                event_type=event_type,
                runtime_tags=list(crosswalk.runtime_tags),
                evaluation_tags=list(crosswalk.evaluation_tags),
                reference=LiveEventReference(
                    event_id=event_id,
                    source_artifact_id=source_artifact_id,
                    observed_at=observed_at,
                ),
            )
        )
    return PrecursorRuntimePacket(
        context_id=context_id,
        effective_at=effective_at,
        events=snapshots,
        bundle=bundle,
        projection_trace=_projection_trace(
            bundle=bundle,
            context_id=context_id,
            effective_at=effective_at,
            events=snapshots,
        ),
    )


def stitch_precursor_context(
    *,
    bundle: ImportedReferenceBundle,
    events: Iterable[LiveEventSnapshot],
    context_id: str,
    effective_at: datetime,
) -> PrecursorRuntimePacket:
    """Wrap already-projected snapshots into one precursor runtime packet."""

    event_list = list(events)
    seen = [event.event_id for event in event_list]
    duplicates = sorted({event_id for event_id in seen if seen.count(event_id) > 1})
    if duplicates:
        raise ValueError(f"duplicate calendar event_id values are not allowed: {duplicates}")
    return PrecursorRuntimePacket(
        context_id=context_id,
        effective_at=effective_at,
        events=event_list,
        bundle=bundle,
        projection_trace=_projection_trace(
            bundle=bundle,
            context_id=context_id,
            effective_at=effective_at,
            events=event_list,
        ),
    )


def financial_calendar_crosswalk() -> list[FinancialCalendarCrosswalkRecord]:
    """Return the deterministic runtime crosswalk records for calendar projection."""

    return [
        FinancialCalendarCrosswalkRecord(
            source_event_type=record.source_event_type,
            runtime_tags=list(record.runtime_tags),
            evaluation_tags=list(record.evaluation_tags),
            projection_targets=list(record.projection_targets),
        )
        for record in _DEFAULT_CROSSWALK
    ]


def resolve_calendar_field(*, candidates, policy):
    """Compatibility-only K04 coalescence over the canonical four-layer law."""

    from nvda_desk.contracts.reference_data import (
        CalendarFieldConflictError,
        CalendarFieldResolutionReceipt,
        FinancialCalendarLayer,
    )

    governed = tuple(
        sorted(
            (
                candidate
                for candidate in candidates
                if candidate.semantic_field == policy.semantic_field
            ),
            key=lambda item: item.candidate_id,
        )
    )
    if not governed:
        if policy.mandatory:
            raise CalendarFieldConflictError("mandatory_calendar_field_missing")
        return None
    if (
        any(
            item.layer == FinancialCalendarLayer.DERIVED_RUNTIME_CALENDAR_CONTEXT
            for item in governed
        )
        and len({item.value for item in governed}) > 1
    ):
        raise CalendarFieldConflictError("derived_calendar_override_forbidden")
    comparison_keys = {
        (
            item.fact_family,
            item.semantic_field,
            item.value_type,
            item.unit,
            item.value,
            item.effective_at_utc,
        )
        for item in governed
    }
    if len(comparison_keys) != 1:
        raise CalendarFieldConflictError("unresolved_calendar_field_conflict")
    return CalendarFieldResolutionReceipt(
        selected_value=governed[0].value,
        candidate_ids=tuple(item.candidate_id for item in governed),
        source_refs=tuple(
            sorted({(item.source_artifact_id, item.source_version) for item in governed})
        ),
        layers=tuple(sorted({item.layer for item in governed}, key=str)),
    )
