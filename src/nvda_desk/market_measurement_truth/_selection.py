"""Controlled raw projection eligibility through the declared M00 public seam."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from decimal import Decimal

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from . import api as f
from ._evaluation import canonical


def eligible(
    item: raw_api.ProjectedRawValueV1,
    mapping: raw_api.RawSignalProjectionMappingV1,
    policy: f.InputSelectionPolicyVersionV1,
    request: f.CalculationRequestV1,
) -> datetime | None:
    if type(item) is not raw_api.ProjectedRawValueV1:
        return None
    if (
        type(item.raw_signal_catalogue_id) is not raw_api.RawSignalCatalogueId
        or item.raw_signal_catalogue_id != mapping.raw_signal_catalogue_id
        or type(item.observation_occurrence_id) is not type(raw_api.observation_occurrence_id("id"))
        or item.projection_mapping_id != mapping.mapping_id
        or type(item.projection_mapping_version) is not int
        or item.projection_mapping_version != mapping.version
        or item.source_provider != policy.source_provider
        or item.source_variant != policy.source_variant
        or type(item.ingestion_sequence_scope) is not type(raw_api.ingestion_sequence_scope("id"))
        or item.ingestion_sequence_scope.value != policy.ingestion_sequence_scope
        or type(item.ingestion_sequence) is not int
        or item.native_field_path != mapping.native_field_path
        or item.native_units != mapping.native_units
        or item.subject_instrument != request.subject_instrument
        or item.selection_identity is not None
        or item.revision_vintage_native is not None
        or type(item.native_value) is not Decimal
        or not item.native_value.is_finite()
        or item.source_temporal_kind != "true_instant"
        or item.source_timezone_native != "UTC"
        or type(item.source_timestamp_raw) is not str
        or not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z",
            item.source_timestamp_raw,
        )
    ):
        return None
    try:
        event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
        f._utc(item.received_ts_utc)
        if (
            event > request.as_of_utc
            or item.received_ts_utc > request.knowledge_cutoff_utc
            or event > item.received_ts_utc
            or not timedelta(0) <= request.as_of_utc - event <= policy.maximum_staleness
        ):
            return None
    except (TypeError, ValueError):
        return None
    return event


def select(
    reader: f.RawProjectionReaderV1,
    mapping: raw_api.RawSignalProjectionMappingV1,
    policy: f.InputSelectionPolicyVersionV1,
    request: f.CalculationRequestV1,
) -> tuple[raw_api.ProjectedRawValueV1, datetime] | None:
    cursor: str | None = None
    cursors: set[str] = set()
    seen: dict[str, bytes] = {}
    candidates: list[tuple[raw_api.ProjectedRawValueV1, datetime]] = []
    for _ in range(policy.history_page_limit):
        try:
            page = reader.list_projected_raw_history(
                mapping.raw_signal_catalogue_id,
                mappings=(mapping,),
                subject_instrument=request.subject_instrument,
                received_at_or_before_utc=request.knowledge_cutoff_utc,
                event_at_or_before_utc=request.as_of_utc,
                limit=policy.history_page_size,
                cursor=cursor,
            )
        except (TypeError, ValueError):
            return None
        if (
            type(page) is not raw_api.ProjectedRawHistoryPageV1
            or type(page.items) is not tuple
            or len(page.items) > policy.history_page_size
        ):
            return None
        for item in page.items:
            if type(item) is not raw_api.ProjectedRawValueV1:
                return None
            when = eligible(item, mapping, policy, request)
            if when is None:
                continue
            content = canonical(item)
            identity = item.observation_occurrence_id.value
            if identity in seen:
                if seen[identity] != content:
                    return None
                continue
            seen[identity] = content
            candidates.append((item, when))
        cursor = page.next_cursor
        if cursor is None:
            break
        if (
            type(cursor) is not str
            or not re.fullmatch(r"[1-9][0-9]*", cursor)
            or cursor in cursors
            or not page.items
        ):
            return None
        cursors.add(cursor)
    else:
        return None
    if not candidates:
        return None

    def rank(pair: tuple[raw_api.ProjectedRawValueV1, datetime]) -> tuple[datetime, datetime, int]:
        return pair[1], pair[0].received_ts_utc, pair[0].ingestion_sequence

    selected = max(candidates, key=rank)
    if sum(rank(pair) == rank(selected) for pair in candidates) != 1:
        return None
    return selected
