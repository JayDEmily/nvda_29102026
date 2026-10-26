"""D003 controlled IANA local time from an actual D001 occurrence."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _temporal
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState
from ._selection import _same_content

BRIEF = "278623c1f97b5faacef1a95304672c92631a14010d5fde71efad4ff817207e1d"
NAMESPACE = "neutral_market_measurement_truth/temporal-local/v1"
T = _temporal.T
PROVIDER, VARIANT = _temporal.PROVIDER, _temporal.VARIANT
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-d003-r004", 1, r.RawSignalCatalogueId("R004"), PROVIDER,
    VARIANT, ("time", "iana"), "IANA_timezone", _temporal.META,
)
UNIT = f.UnitConventionVersionV1(
    "mmt-d003-iana", 1, "IANA_timezone", "IANA_timezone", Decimal(1), Decimal(0),
)
ZONE_POLICY = f.VersionRefV1("controlled-IANA-Melbourne", 1)
DEFINITION = f.CalculationDefinitionV1(
    "D003", "D003-IANA-LOCAL-1", "K01_TIME",
    "same D001 instant in configured IANA exchange zone", ("R004",), ("D001",),
    "P_TIME", "local_datetime", "aware_iana_datetime",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-d003-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d003-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def _zone(value: str) -> ZoneInfo:
    if value != "Australia/Melbourne":
        raise ValueError("unconfigured IANA zone")
    try:
        zone = ZoneInfo(value)
    except ZoneInfoNotFoundError as exc:
        raise ValueError("configured IANA zone unavailable") from exc
    if T.astimezone(zone).utcoffset() != timedelta(hours=11):
        raise ValueError("controlled timezone policy mismatch")
    return zone


def _request(request: f.TemporalLocalRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D003", "NVDA", T, T, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1), (),
        (f.RawInputBindingV1("R004", f.VersionRefV1(MAPPING.mapping_id, 1),
                             f.VersionRefV1(UNIT.context_id, 1), "NVDA"),),
    )
    f._utc(now)
    if (type(request) is not f.TemporalLocalRequestV1
        or canonical(c) != canonical(expected)
        or type(request.predecessor_occurrence_id) is not str
        or not request.predecessor_occurrence_id or now < T):
        raise ValueError("unadmitted D003 request")


def _line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1
          ) -> f.TemporalLocalRawLineageV1:
    identity = r.RawSelectionIdentityV1((
        ("sample.id", "controlled-temporal-sample/1"), ("value.role", "exchange_iana"),
    ))
    if (
        type(item) is not r.ProjectedRawValueV1
        or item.raw_signal_catalogue_id != MAPPING.raw_signal_catalogue_id
        or item.projection_mapping_id != MAPPING.mapping_id
        or item.projection_mapping_version != MAPPING.version
        or item.native_field_path != MAPPING.native_field_path
        or item.native_units != MAPPING.native_units
        or item.source_provider != PROVIDER or item.source_variant != VARIANT
        or item.subject_instrument != "NVDA" or item.selection_identity != identity
        or item.ingestion_sequence_scope.value != POLICY.ingestion_sequence_scope
        or type(item.ingestion_sequence) is not int or item.ingestion_sequence <= 0
        or item.revision_vintage_native is not None or type(item.native_value) is not str
        or item.source_temporal_kind != "true_instant"
        or item.source_timezone_native != "UTC"
        or item.received_ts_utc > c.knowledge_cutoff_utc
    ):
        raise ValueError("unadmitted actual R004 projection")
    f._utc(item.received_ts_utc)
    event = _temporal._stamp(str(item.source_timestamp_raw)).astimezone(UTC)
    if (event > c.as_of_utc or event > item.received_ts_utc
        or c.as_of_utc - event > POLICY.maximum_staleness):
        raise ValueError("future or stale R004 event")
    _zone(item.native_value)
    return f.TemporalLocalRawLineageV1(
        "R004", item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, item.native_value, event,
    )


def _produce(
    request: f.TemporalLocalRequestV1, line: f.TemporalLocalRawLineageV1,
    predecessor: f.TemporalOccurrenceV1, now: datetime,
) -> f.TemporalLocalOccurrenceV1:
    _request(request, now)
    if canonical(line) != canonical(_line(line.projection, request.calculation)):
        raise ValueError("R004 lineage mismatch")
    _temporal._validate(predecessor)
    c = request.calculation
    parent_identity = predecessor.raw_input_lineage[0].projection.selection_identity
    line_identity = line.projection.selection_identity
    if (
        predecessor.derived_occurrence_id != request.predecessor_occurrence_id
        or predecessor.implementation_brief_sha256 != _temporal.BRIEF
        or predecessor.request.subject_instrument != c.subject_instrument
        or predecessor.request.as_of_utc != c.as_of_utc
        or predecessor.knowledge_cutoff_utc != c.knowledge_cutoff_utc
        or predecessor.calculated_at_utc > now
        or predecessor.result != line.event_time_utc
        or parent_identity is None or line_identity is None
        or parent_identity.value_for("sample.id") != line_identity.value_for("sample.id")
        or predecessor.raw_input_lineage[0].projection.received_ts_utc
        != line.projection.received_ts_utc
    ):
        raise ValueError("actual D001 and R004 source mismatch")
    local = predecessor.result.astimezone(_zone(line.canonical_value))
    if local.astimezone(UTC) != predecessor.result:
        raise ValueError("conversion changed instant")
    value = f.TemporalLocalOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D003", "pending", request, DEFINITION,
        PARAMETER, POLICY, UNIT, MAPPING, line, predecessor, ZONE_POLICY,
        local, "local_datetime", "aware_iana_datetime",
        c.as_of_utc, c.knowledge_cutoff_utc, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in {"derived_occurrence_id", "calculated_at_utc"}}
    return replace(value, derived_occurrence_id="mmtlocal1:" + hashlib.sha256(
        canonical(payload)
    ).hexdigest())


def _validate(value: f.TemporalLocalOccurrenceV1) -> None:
    if type(value) is not f.TemporalLocalOccurrenceV1:
        raise TypeError("exact D003 record required")
    f._Validated.__post_init__(value)
    if (
        not isinstance(value.result.tzinfo, ZoneInfo)
        or value.result.tzinfo.key != value.raw_input_lineage.canonical_value
    ):
        raise ValueError("D003 result must retain the selected IANA zone")
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.predecessor, value.calculated_at_utc,
    )):
        raise ValueError("D003 local result/lineage mismatch")


def _decode(payload: bytes) -> f.TemporalLocalOccurrenceV1:
    value = cast(f.TemporalLocalOccurrenceV1, decode(payload, f.TemporalLocalOccurrenceV1))
    zone = _zone(value.raw_input_lineage.canonical_value)
    return replace(value, result=value.result.astimezone(zone))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.TemporalLocalOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty derived identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.TemporalLocalOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid D003 history query")
        return tuple(sorted(
            (v for v in self.state.all() if v.derived_signal_id == derived_signal_id
             and v.request.calculation.subject_instrument == subject_instrument
             and v.effective_as_of_utc <= effective_at_or_before_utc
             and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc),
            key=lambda v: (v.effective_as_of_utc, v.knowledge_cutoff_utc, v.derived_occurrence_id),
            reverse=True,
        )[:limit])


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 predecessor: f.MeasurementTemporalReadsV1, now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.predecessor, self.now = state, raw, predecessor, now
        self.reads = _Reads(state)

    def materialise(self, request: f.TemporalLocalRequestV1
                    ) -> f.TemporalLocalOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            _request(request, now)
            cursor: str | None = None
            cursors: set[str] = set()
            items: dict[str, r.ProjectedRawValueV1] = {}
            for _ in range(POLICY.history_page_limit):
                page = self.raw.list_projected_raw_history(
                    MAPPING.raw_signal_catalogue_id, mappings=(MAPPING,),
                    subject_instrument="NVDA", received_at_or_before_utc=T,
                    event_at_or_before_utc=None, limit=POLICY.history_page_size, cursor=cursor,
                )
                if (type(page) is not r.ProjectedRawHistoryPageV1
                    or type(page.items) is not tuple):
                    raise ValueError("invalid D003 source page")
                for item in page.items:
                    key = item.observation_occurrence_id.value
                    if key in items and not _same_content(items[key], item):
                        raise ValueError("conflicting D003 source identity")
                    items[key] = item
                cursor = page.next_cursor
                if cursor is None:
                    break
                if type(cursor) is not str or cursor in cursors or not page.items:
                    raise ValueError("invalid D003 source cursor")
                cursors.add(cursor)
            else:
                raise ValueError("incomplete D003 source history")
            identity = r.RawSelectionIdentityV1((
                ("sample.id", "controlled-temporal-sample/1"), ("value.role", "exchange_iana"),
            ))
            candidates = tuple(i for i in items.values() if i.selection_identity == identity)
            if not candidates:
                raise ValueError("missing actual R004")
            def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, int]:
                return item.received_ts_utc, item.ingestion_sequence
            chosen = max(candidates, key=rank)
            if sum(rank(i) == rank(chosen) for i in candidates) != 1:
                raise ValueError("ambiguous R004")
            line = _line(chosen, request.calculation)
            predecessor = self.predecessor.get_derived_occurrence(request.predecessor_occurrence_id)
            if type(predecessor) is not f.TemporalOccurrenceV1:
                raise ValueError("actual D001 missing")
            value = _produce(request, line, predecessor, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.TemporalLocalOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTemporalReadsV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementTemporalLocalOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D003 owner")
    if (type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or any(not callable(getattr(predecessor, method, None))
               for method in ("get_derived_occurrence", "list_derived_history"))):
        raise TypeError("actual D001 reader and exact storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, predecessor, now)


def build_reader(admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
                 ) -> f.MeasurementTemporalLocalReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D003 reader")
    return _Reads(RecordState(storage, _decode, _validate))
