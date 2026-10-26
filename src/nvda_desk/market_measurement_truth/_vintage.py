"""D009 atomic typed statuses for an exact visible macro vintage history."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _temporal
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState
from ._selection import _same_content

BRIEF = "d548557226dcb7dfaac12aa12f4287adb37b6c897e481e50e980ac4a1bfd92bc"
NAMESPACE = "neutral_market_measurement_truth/vintage-status/v1"
T = _temporal.T
EARLY = datetime(2026, 10, 9, 11, 10, tzinfo=UTC)
PROVIDER, VARIANT = "foundation-controlled-macro", "vintage_v1"
SERIES, PERIOD = "controlled-macro-series/1", "2026-09"
ROLES = ("realtime_start", "realtime_end", "last_updated")
META = (
    ("series.id", ("series", "id")), ("reference.period", ("series", "period")),
    ("vintage.id", ("vintage", "id")), ("field.role", ("field", "role")),
    ("publication.ordinal", ("publication", "ordinal")),
    ("publication.timestamp", ("publication", "timestamp")),
)
MAPS = tuple(r.RawSignalProjectionMappingV1(
    f"mmt-d009-r{raw}", 1, r.RawSignalCatalogueId(f"R{raw}"), PROVIDER,
    VARIANT, ("macro", field), unit, META,
) for raw, field, unit in (
    ("280", "realtime_start", "native_date"),
    ("281", "realtime_end", "native_date"),
    ("282", "last_updated", "native_offset_datetime"),
))
UNITS = tuple(f.UnitConventionVersionV1(
    f"mmt-d009-{raw}", 1, native, canonical_unit, Decimal(1), Decimal(0),
) for raw, native, canonical_unit in (
    ("r280", "native_date", "date"), ("r281", "native_date", "date"),
    ("r282", "native_offset_datetime", "UTC_datetime"),
))
DEFINITION = f.CalculationDefinitionV1(
    "D009", "D009-VINTAGE-STATUS-1", "K01_TIME",
    "each visible immutable macro vintage classified at cutoff by separate publication order",
    ("R280", "R281", "R282"), (), "P_TIME", "category", "vintage_status",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-d009-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d009-selection", 1, ("series.id", "reference.period", "vintage.id"),
    timedelta(hours=4), timedelta(0), ("date_only", "true_instant"), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
# Publication time/ordinal are independently projected native selection metadata,
# not R282 last-updated time or receipt order.
VINTAGES = (
    ("v1", 1, "2026-10-09T11:00:00Z", "2026-10-09T11:05:00Z",
     "2026-10-01", "2026-10-31", "2026-10-09T10:50:00+00:00"),
    ("v2", 2, "2026-10-09T12:00:00Z", "2026-10-09T12:05:00Z",
     "2026-10-02", "2026-11-01", "2026-10-09T11:50:00+00:00"),
    ("v3", 3, "2026-10-09T13:00:00Z", "2026-10-09T13:05:00Z",
     "2026-10-03", "2026-11-02", "2026-10-09T12:50:00+00:00"),
)


def _instant(raw: str) -> datetime:
    return _temporal._stamp(raw).astimezone(UTC)


def _day(raw: str) -> date:
    if type(raw) is not str:
        raise TypeError("native realtime date string required")
    result = date.fromisoformat(raw)
    if result.isoformat() != raw:
        raise ValueError("canonical native date required")
    return result


def _request(request: f.VintageStatusRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D009", "NVDA", T, c.knowledge_cutoff_utc, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1), (),
        tuple(f.RawInputBindingV1(
            m.raw_signal_catalogue_id.value, f.VersionRefV1(m.mapping_id, 1),
            f.VersionRefV1(u.context_id, 1), "NVDA",
        ) for m, u in zip(MAPS, UNITS, strict=True)),
    )
    f._utc(now)
    if (type(request) is not f.VintageStatusRequestV1
        or canonical(c) != canonical(expected)
        or c.knowledge_cutoff_utc not in (T, EARLY)
        or request.series_id != SERIES or request.reference_period != PERIOD
        or now < c.knowledge_cutoff_utc):
        raise ValueError("unadmitted D009 request")


def _line(item: r.ProjectedRawValueV1, vintage_index: int, role: int,
          c: f.CalculationRequestV1) -> f.VintageRawLineageV1:
    vid, ordinal, publication, receipt, start, end, updated = VINTAGES[vintage_index]
    m, u = MAPS[role], UNITS[role]
    identity = r.RawSelectionIdentityV1((
        ("series.id", SERIES), ("reference.period", PERIOD),
        ("vintage.id", vid), ("field.role", ROLES[role]),
        ("publication.ordinal", ordinal), ("publication.timestamp", publication),
    ))
    if (
        type(item) is not r.ProjectedRawValueV1
        or item.raw_signal_catalogue_id != m.raw_signal_catalogue_id
        or item.projection_mapping_id != m.mapping_id
        or item.projection_mapping_version != m.version
        or item.native_field_path != m.native_field_path
        or item.native_units != m.native_units
        or item.source_provider != PROVIDER or item.source_variant != VARIANT
        or item.subject_instrument != "NVDA" or item.selection_identity != identity
        or item.ingestion_sequence_scope.value != POLICY.ingestion_sequence_scope
        or type(item.ingestion_sequence) is not int or item.ingestion_sequence <= 0
        or item.revision_vintage_native is not None or type(item.native_value) is not str
        or item.native_value != (start, end, updated)[role]
        or item.received_ts_utc != _instant(receipt)
        or item.received_ts_utc > c.knowledge_cutoff_utc
    ):
        raise ValueError("unadmitted actual macro vintage field")
    f._utc(item.received_ts_utc)
    published = _instant(publication)
    if published > item.received_ts_utc or published > c.knowledge_cutoff_utc:
        raise ValueError("future publication not visible")
    if role < 2:
        if (item.source_temporal_kind != "date_only"
            or item.source_timestamp_raw != item.native_value
            or item.source_timezone_native is not None):
            raise ValueError("R280/R281 must remain native date-only")
        canonical_value: date | datetime = _day(item.native_value)
    else:
        if (item.source_temporal_kind != "true_instant"
            or item.source_timestamp_raw != item.native_value
            or item.source_timezone_native != "UTC"):
            raise ValueError("R282 must remain its separate offset-aware last-updated")
        canonical_value = _instant(item.native_value)
        if canonical_value > item.received_ts_utc:
            raise ValueError("future last-updated timestamp")
    return f.VintageRawLineageV1(
        m.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(m.mapping_id, 1), f.VersionRefV1(u.context_id, 1),
        item, canonical_value, ordinal, published,
    )


def _produce(
    request: f.VintageStatusRequestV1,
    lines: tuple[f.VintageRawLineageV1, ...], visible: tuple[str, ...],
    now: datetime,
) -> f.VintageStatusOccurrenceV1:
    _request(request, now)
    identity = lines[0].projection.selection_identity if lines else None
    vid = identity.value_for("vintage.id") if identity is not None else None
    if type(vid) is not str or vid not in ("v1", "v2", "v3"):
        raise ValueError("exact vintage required")
    index = int(vid[1:]) - 1
    if (len(lines) != 3 or visible not in (("v1",), ("v1", "v2"), ("v1", "v2", "v3"))
        or vid not in visible or any(canonical(line) != canonical(
            _line(line.projection, index, role, request.calculation)
        ) for role, line in enumerate(lines))):
        raise ValueError("complete selected vintage triple and visible set required")
    start, end, last = (line.canonical_value for line in lines)
    if type(start) is not date or type(end) is not date or type(last) is not datetime:
        raise ValueError("native macro temporal types not preserved")
    if start > end:
        raise ValueError("invalid realtime period")
    status = "initial" if vid == "v1" else (
        "latest_known_at_cutoff" if vid == visible[-1] else "revised"
    )
    publication = lines[0].publication_timestamp_utc
    ordinal = lines[0].publication_ordinal
    if any(line.publication_ordinal != ordinal
           or line.publication_timestamp_utc != publication for line in lines):
        raise ValueError("co-referenced publication identity mismatch")
    c = request.calculation
    value = f.VintageStatusOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D009", "pending", request, DEFINITION,
        PARAMETER, POLICY, UNITS, MAPS, lines, visible, vid, ordinal, publication,
        start, end, last, status, "category", "vintage_status",
        c.as_of_utc, c.knowledge_cutoff_utc, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in {"derived_occurrence_id", "calculated_at_utc"}}
    return replace(value, derived_occurrence_id="mmtvintage1:" + hashlib.sha256(
        canonical(payload)
    ).hexdigest())


def _validate(value: f.VintageStatusOccurrenceV1) -> None:
    if type(value) is not f.VintageStatusOccurrenceV1:
        raise TypeError("exact D009 status record required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.visible_vintage_ids,
        value.calculated_at_utc,
    )):
        raise ValueError("D009 vintage/source/status mismatch")


def _decode(payload: bytes) -> f.VintageStatusOccurrenceV1:
    return cast(f.VintageStatusOccurrenceV1, decode(payload, f.VintageStatusOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.VintageStatusOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty derived identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.VintageStatusOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid D009 history query")
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
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise_vintage_statuses(self, request: f.VintageStatusRequestV1
                                    ) -> tuple[f.VintageStatusOccurrenceV1, ...] | None:
        now = self.now()
        f._utc(now)
        try:
            _request(request, now)
            by_role: list[dict[str, r.ProjectedRawValueV1]] = []
            for mapping in MAPS:
                cursor: str | None = None
                cursors: set[str] = set()
                items: dict[str, r.ProjectedRawValueV1] = {}
                for _ in range(POLICY.history_page_limit):
                    page = self.raw.list_projected_raw_history(
                        mapping.raw_signal_catalogue_id, mappings=(mapping,),
                        subject_instrument="NVDA",
                        received_at_or_before_utc=request.calculation.knowledge_cutoff_utc,
                        event_at_or_before_utc=None, limit=POLICY.history_page_size,
                        cursor=cursor,
                    )
                    if (type(page) is not r.ProjectedRawHistoryPageV1
                        or type(page.items) is not tuple):
                        raise ValueError("invalid D009 source page")
                    for item in page.items:
                        key = item.observation_occurrence_id.value
                        if key in items and not _same_content(items[key], item):
                            raise ValueError("conflicting D009 observation identity")
                        items[key] = item
                    cursor = page.next_cursor
                    if cursor is None:
                        break
                    if type(cursor) is not str or cursor in cursors or not page.items:
                        raise ValueError("invalid D009 cursor")
                    cursors.add(cursor)
                else:
                    raise ValueError("incomplete D009 source history")
                selected: dict[str, r.ProjectedRawValueV1] = {}
                for item in items.values():
                    identity = item.selection_identity
                    if identity is None or identity.value_for("series.id") != SERIES:
                        continue
                    if identity.value_for("reference.period") != PERIOD:
                        continue
                    vid = identity.value_for("vintage.id")
                    if type(vid) is not str or vid not in ("v1", "v2", "v3"):
                        raise ValueError("unadmitted visible vintage")
                    if vid in selected:
                        raise ValueError("ambiguous vintage/role")
                    selected[vid] = item
                by_role.append(selected)
            visible = tuple(row[0] for row in VINTAGES
                            if any(row[0] in role for role in by_role))
            expected = ("v1",) if request.calculation.knowledge_cutoff_utc == EARLY else (
                "v1", "v2", "v3"
            )
            if visible != expected:
                raise ValueError("missing mandatory visible publication history")
            triples = []
            for index, vid in enumerate(visible):
                if any(vid not in role for role in by_role):
                    raise ValueError("partial newest or earlier vintage triple")
                triples.append(tuple(_line(by_role[role][vid], index, role,
                                           request.calculation) for role in range(3)))
            values = tuple(_produce(request, triple, visible, now) for triple in triples)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(tuple[f.VintageStatusOccurrenceV1, ...], self.state.append_many(values))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementVintageOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D009 owner")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact D009 storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, now)


def build_reader(admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
                 ) -> f.MeasurementVintageReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D009 reader")
    return _Reads(RecordState(storage, _decode, _validate))
