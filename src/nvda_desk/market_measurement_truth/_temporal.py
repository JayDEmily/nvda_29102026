"""D001 controlled true-instant normalisation, with its own typed source path."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState
from ._selection import _same_content

BRIEF = "bd023e56cbf27f4e2979587fb9e4deb288be329901fd46c7a78897f9b8b4139d"
NAMESPACE = "neutral_market_measurement_truth/temporal/v1"
T = datetime(2026, 10, 9, 14, tzinfo=UTC)
PROVIDER, VARIANT = "foundation-controlled-temporal", "clock_v1"
META = (("sample.id", ("sample", "id")), ("value.role", ("value", "role")))
MAPS = (
    r.RawSignalProjectionMappingV1(
        "mmt-d001-r002", 1, r.RawSignalCatalogueId("R002"),
        PROVIDER, VARIANT, ("time", "value"), "native_time", META,
    ),
    r.RawSignalProjectionMappingV1(
        "mmt-d001-r003", 1, r.RawSignalCatalogueId("R003"),
        PROVIDER, VARIANT, ("time", "timezone"), "native_timezone", META,
    ),
)
UNITS = (
    f.UnitConventionVersionV1(
        "mmt-d001-temporal", 1, "native_time", "UTC_datetime", Decimal(1), Decimal(0),
    ),
    f.UnitConventionVersionV1(
        "mmt-d001-zone", 1, "native_timezone", "offset", Decimal(1), Decimal(0),
    ),
)
DEFINITION = f.CalculationDefinitionV1(
    "D001", "D001-TRUE-INSTANT-UTC-1", "K01_TIME",
    "same true instant converted to aware UTC", ("R002", "R003"), (),
    "P_TIME", "UTC_datetime", "aware_utc_datetime",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d001-controlled", 1, "P_TIME", "NVDA", ("NVDA",),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d001-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
_STAMP = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]{1,6})?(?:Z|[+-](?:0[0-9]|1[0-4]):[0-5][0-9])"
)
_OFFSET = re.compile(r"[+-](?:0[0-9]|1[0-4]):[0-5][0-9]")


def _request(c: f.CalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D001", "NVDA", T, T, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1), (),
        tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value,
            f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), "NVDA",
        ) for mapping, unit in zip(MAPS, UNITS, strict=True)),
    )
    f._utc(now)
    if type(c) is not f.CalculationRequestV1 or canonical(c) != canonical(expected) or now < T:
        raise ValueError("unadmitted controlled D001 request")


def _stamp(raw: str) -> datetime:
    if type(raw) is not str or _STAMP.fullmatch(raw) is None:
        raise ValueError("exact offset-bearing instant required")
    stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError("a true instant needs its native offset")
    return stamp


def _line(item: r.ProjectedRawValueV1, role: int, c: f.CalculationRequestV1
          ) -> f.TemporalRawLineageV1:
    mapping, unit = MAPS[role], UNITS[role]
    identity = r.RawSelectionIdentityV1((
        ("sample.id", "controlled-temporal-sample/1"),
        ("value.role", ("source_timestamp", "source_timezone")[role]),
    ))
    if (
        type(item) is not r.ProjectedRawValueV1
        or item.raw_signal_catalogue_id != mapping.raw_signal_catalogue_id
        or item.projection_mapping_id != mapping.mapping_id
        or item.projection_mapping_version != mapping.version
        or item.native_field_path != mapping.native_field_path
        or item.native_units != mapping.native_units
        or item.source_provider != PROVIDER or item.source_variant != VARIANT
        or item.subject_instrument != "NVDA"
        or item.ingestion_sequence_scope.value != POLICY.ingestion_sequence_scope
        or type(item.ingestion_sequence) is not int or item.ingestion_sequence <= 0
        or item.selection_identity != identity or item.revision_vintage_native is not None
        or type(item.native_value) is not str
        or item.received_ts_utc > c.knowledge_cutoff_utc
    ):
        raise ValueError("unadmitted exact temporal source/role")
    f._utc(item.received_ts_utc)
    if item.source_temporal_kind != "true_instant":
        raise ValueError("D001 cannot manufacture a date-only/receipt-only instant")
    if role == 0:
        if item.source_timestamp_raw != item.native_value:
            raise ValueError("native source timestamp and raw timestamp disagree")
        event = _stamp(item.native_value)
    else:
        if item.source_timezone_native != "UTC":
            raise ValueError("R003 event timestamp must have declared UTC source")
        event = _stamp(str(item.source_timestamp_raw))
    event_utc = event.astimezone(UTC)
    if (
        event_utc > c.as_of_utc or event_utc > item.received_ts_utc
        or c.as_of_utc - event_utc > POLICY.maximum_staleness
    ):
        raise ValueError("future or stale controlled source")
    return f.TemporalRawLineageV1(
        mapping.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(unit.context_id, 1),
        item, item.native_value, event_utc,
    )


def _produce(c: f.CalculationRequestV1, lines: tuple[f.TemporalRawLineageV1, ...],
             now: datetime) -> f.TemporalOccurrenceV1:
    _request(c, now)
    if len(lines) != 2:
        raise ValueError("both exact temporal roles required")
    if any(canonical(line) != canonical(_line(line.projection, role, c))
           for role, line in enumerate(lines)):
        raise ValueError("temporal lineage/source mismatch")
    a, b = lines
    if (
        a.projection.selection_identity is None
        or b.projection.selection_identity is None
        or a.projection.selection_identity.value_for("sample.id")
        != b.projection.selection_identity.value_for("sample.id")
        or a.event_time_utc != b.event_time_utc
        or a.projection.received_ts_utc != b.projection.received_ts_utc
        or _OFFSET.fullmatch(b.canonical_value) is None
        or a.projection.source_timezone_native != b.canonical_value
    ):
        raise ValueError("unmatched supplied offset/source sample")
    offset = _stamp(a.canonical_value).utcoffset()
    sign = 1 if b.canonical_value[0] == "+" else -1
    expected = sign * timedelta(
        hours=int(b.canonical_value[1:3]), minutes=int(b.canonical_value[4:6]),
    )
    if offset != expected:
        raise ValueError("source instant offset disagrees with supplied zone")
    result = a.event_time_utc
    value = f.TemporalOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D001", "pending", c, DEFINITION,
        PARAMETER, POLICY, UNITS, MAPS, lines, (), result,
        "UTC_datetime", "aware_utc_datetime", c.as_of_utc,
        c.knowledge_cutoff_utc, now,
    )
    payload = {
        field.name: getattr(value, field.name) for field in fields(value)
        if field.name not in {"derived_occurrence_id", "calculated_at_utc"}
    }
    return replace(value, derived_occurrence_id="mmttemporal1:" + hashlib.sha256(
        canonical(payload)
    ).hexdigest())


def _validate(value: f.TemporalOccurrenceV1) -> None:
    if type(value) is not f.TemporalOccurrenceV1:
        raise TypeError("exact temporal record required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(
        _produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
    ):
        raise ValueError("temporal result/source/identity mismatch")


def _decode(payload: bytes) -> f.TemporalOccurrenceV1:
    return cast(f.TemporalOccurrenceV1, decode(payload, f.TemporalOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.TemporalOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("exact nonempty derived identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.TemporalOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid temporal history query")
        return tuple(sorted(
            (
                v for v in self.state.all()
                if v.derived_signal_id == derived_signal_id
                and v.request.subject_instrument == subject_instrument
                and v.effective_as_of_utc <= effective_at_or_before_utc
                and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc
            ),
            key=lambda v: (v.effective_as_of_utc, v.knowledge_cutoff_utc, v.derived_occurrence_id),
            reverse=True,
        )[:limit])


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.CalculationRequestV1) -> f.TemporalOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            _request(request, now)
            lines = []
            for role, mapping in enumerate(MAPS):
                cursor: str | None = None
                cursors: set[str] = set()
                items: dict[str, r.ProjectedRawValueV1] = {}
                for _ in range(POLICY.history_page_limit):
                    page = self.raw.list_projected_raw_history(
                        mapping.raw_signal_catalogue_id, mappings=(mapping,),
                        subject_instrument="NVDA", received_at_or_before_utc=T,
                        event_at_or_before_utc=None, limit=POLICY.history_page_size,
                        cursor=cursor,
                    )
                    if (
                        type(page) is not r.ProjectedRawHistoryPageV1
                        or type(page.items) is not tuple
                    ):
                        raise ValueError("invalid temporal source page")
                    for item in page.items:
                        key = item.observation_occurrence_id.value
                        if key in items and not _same_content(items[key], item):
                            raise ValueError("conflicting temporal source identity")
                        items[key] = item
                    cursor = page.next_cursor
                    if cursor is None:
                        break
                    if type(cursor) is not str or cursor in cursors or not page.items:
                        raise ValueError("invalid temporal source cursor")
                    cursors.add(cursor)
                else:
                    raise ValueError("incomplete temporal source history")
                candidates = tuple(item for item in items.values()
                                   if item.selection_identity == r.RawSelectionIdentityV1((
                                       ("sample.id", "controlled-temporal-sample/1"),
                                       ("value.role", ("source_timestamp",
                                                       "source_timezone")[role]),
                                   )))
                if not candidates:
                    raise ValueError("missing temporal source role")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, int]:
                    return item.received_ts_utc, item.ingestion_sequence
                selected = max(candidates, key=rank)
                if sum(rank(item) == rank(selected) for item in candidates) != 1:
                    raise ValueError("ambiguous temporal source")
                lines.append(_line(selected, role, request))
            value = _produce(request, tuple(lines), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.TemporalOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementTemporalOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D001 owner")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, now)


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1,
) -> f.MeasurementTemporalReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D001 reader")
    return _Reads(RecordState(storage, _decode, _validate))
