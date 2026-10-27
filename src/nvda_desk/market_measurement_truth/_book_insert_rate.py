"""D139 bounded receipt-clock positional SMART insertion rate."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState

BRIEF = "77e84fa49327cebe561167b7086b2db3acc71ae1bdeee3054656885c271a2f89"
NAMESPACE = "neutral_market_measurement_truth/book-rate/v1"
SUBJECT = "NVDA"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
PROVIDER, VARIANT = "foundation-controlled-smart-book", "receipt_rate_v1"
GENERATION = "controlled-smart-rate-generation/1"
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d139-receipt-positional", 1), PROVIDER, VARIANT,
    GENERATION, T - timedelta(seconds=10), 100,
)
ROLES = (
    ("R001", ("time", "receipt"), "UTC_datetime"),
    ("R185", ("book", "position"), "book_position"),
    ("R187", ("book", "operation"), "book_operation"),
    ("R188", ("book", "side"), "book_side"),
    ("R190", ("book", "size"), "shares"),
)
IDENTITY = (("generation.id", ("generation", "id")),
            ("event.id", ("event", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d139-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), PROVIDER,
    VARIANT, path, unit, IDENTITY,
) for raw, path, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d139-" + raw.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for raw, _, unit in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D139", "D139-RECEIPT-CLOCK-INSERT-RATE-1", "K08_RULE_BUCKET_POLICY",
    "count and inserted standing size of bid positions1-2 in four-second R001 receipt bucket",
    tuple(raw for raw, _, _ in ROLES), (), "P_RULE", "events or size/time",
    "book_rate_pair", tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d139-bid-positions1-2-4s", 1, "P_RULE", SUBJECT, (SUBJECT,),
)


def _request() -> f.BookRateRequestV1:
    return f.BookRateRequestV1(f.CalculationRequestV1(
        "D139", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
        tuple(f.RawInputBindingV1(
            rid, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (rid, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION, 4, 0, (1, 2))


def _line(item: r.ProjectedRawValueV1, role: int) -> f.BookRateRawLineageV1:
    rid, _, _ = ROLES[role]
    mapping, unit = MAPS[role], UNITS[role]
    expected = (datetime if role == 0 else int if role < 4 else Decimal)
    if (type(item) is not r.ProjectedRawValueV1
        or item.raw_signal_catalogue_id != mapping.raw_signal_catalogue_id
        or item.projection_mapping_id != mapping.mapping_id
        or item.projection_mapping_version != 1
        or item.native_field_path != mapping.native_field_path
        or item.native_units != mapping.native_units
        or item.source_provider != PROVIDER or item.source_variant != VARIANT
        or item.subject_instrument != SUBJECT
        or item.ingestion_sequence_scope.value != PROVIDER + "/" + VARIANT
        or type(item.ingestion_sequence) is not int or item.ingestion_sequence <= 0
        or item.revision_vintage_native is not None
        or item.source_temporal_kind != "true_instant"
        or item.source_timezone_native != "UTC"
        or item.selection_identity is None
        or item.selection_identity.value_for("generation.id") != GENERATION
        or item.selection_identity.value_for("subject.id") != SUBJECT
        or not item.selection_identity.value_for("event.id")
        or type(item.native_value) is not expected
        or item.received_ts_utc > CUTOFF
        or type(item.source_timestamp_raw) is not str):
        raise ValueError("ineligible typed receipt-book projection")
    f._utc(item.received_ts_utc)
    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
    f._utc(event)
    if (not SELECTION.history_complete_from_utc <= event <= T
        or event > item.received_ts_utc
        or not SELECTION.history_complete_from_utc <= item.received_ts_utc <= T):
        raise ValueError("source event or collector receipt outside admitted history")
    if role == 0:
        f._utc(cast(datetime, item.native_value))
        if item.native_value != item.received_ts_utc:
            raise ValueError("R001 must be actual collector receipt")
    elif role == 1 and cast(int, item.native_value) < 0:
        raise ValueError("negative book position")
    elif role == 2 and item.native_value not in (0, 1, 2, 317):
        raise ValueError("unknown native operation")
    elif role == 3 and item.native_value not in (0, 1):
        raise ValueError("unknown native side")
    elif role == 4 and (not cast(Decimal, item.native_value).is_finite()
                        or cast(Decimal, item.native_value) < 0):
        raise ValueError("invalid native size")
    return f.BookRateRawLineageV1(
        rid, item.observation_occurrence_id.value, f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(unit.context_id, 1), item, item.native_value, event,
    )


def _replay(lines: tuple[f.BookRateRawLineageV1, ...]
            ) -> tuple[tuple[f.SmartSizeRowV1, ...], tuple[str, ...], Decimal]:
    groups: dict[str, dict[str, f.BookRateRawLineageV1]] = {}
    for line in lines:
        role = next((i for i, row in enumerate(ROLES) if row[0] == line.raw_signal_id), -1)
        if role < 0 or canonical(line) != canonical(_line(line.projection, role)):
            raise ValueError("typed book lineage differs from actual projection")
        group = groups.setdefault(line.observation_occurrence_id, {})
        if line.raw_signal_id in group:
            raise ValueError("duplicate book role")
        group[line.raw_signal_id] = line
    if not groups or len(groups) > SELECTION.maximum_events:
        raise ValueError("incomplete or unbounded book")
    ordered = sorted(groups.values(), key=lambda group: (
        next(iter(group.values())).projection.received_ts_utc,
        next(iter(group.values())).projection.ingestion_sequence,
    ))
    sides: dict[int, list[f.SmartSizeRowV1]] = {0: [], 1: []}
    seen_warmup = False
    selected: list[str] = []
    size_total = Decimal(0)
    previous_key: tuple[datetime, int] | None = None
    for group in ordered:
        if "R001" not in group:
            raise ValueError("actual collector receipt required")
        first = group["R001"]
        receipt = cast(datetime, first.canonical_value)
        key = (receipt, first.projection.ingestion_sequence)
        if previous_key is not None and key <= previous_key:
            raise ValueError("ambiguous collector order")
        previous_key = key
        identity = first.projection.selection_identity
        if any((line.projection.selection_identity != identity
                or line.event_time_utc != first.event_time_utc
                or line.projection.received_ts_utc != receipt
                or line.projection.ingestion_sequence != first.projection.ingestion_sequence)
               for line in group.values()):
            raise ValueError("mixed native occurrence")
        if set(group) != {x[0] for x in ROLES}:
            raise ValueError("missing mandatory book role")
        operation = cast(int, group["R187"].canonical_value)
        side = cast(int, group["R188"].canonical_value)
        pos = cast(int, group["R185"].canonical_value)
        size = cast(Decimal, group["R190"].canonical_value)
        if operation == 317:
            sides = {0: [], 1: []}
            seen_warmup = False
            continue
        rows = sides[side]
        in_window = T - timedelta(seconds=4) < receipt <= T
        if in_window and not seen_warmup:
            raise ValueError("missing complete pre-window top book")
        if operation == 0:
            if pos > len(rows) or size <= 0:
                raise ValueError("invalid positional insert")
            rows.insert(pos, f.SmartSizeRowV1(side, pos, size))
        elif operation == 1:
            if pos >= len(rows) or size <= 0:
                raise ValueError("update without standing row")
            rows[pos] = f.SmartSizeRowV1(side, pos, size)
        else:
            if pos >= len(rows) or size != 0:
                raise ValueError("delete without standing position")
            del rows[pos]
        rows[:] = [replace(row, position=i) for i, row in enumerate(rows)]
        if not in_window:
            seen_warmup = bool(sides[0] and sides[1])
        elif side == 0 and pos in (1, 2) and operation == 0:
            selected.append(first.observation_occurrence_id)
            size_total += size
        elif side == 0 and pos in (1, 2):
            raise ValueError("selected bid mutation is not an insert")
    if not seen_warmup or len(selected) != 2:
        raise ValueError("incomplete warm-up or selected bid insert set")
    return tuple((*sides[0], *sides[1])), tuple(selected), size_total


def _produce(req: f.BookRateRequestV1, lines: tuple[f.BookRateRawLineageV1, ...],
             now: datetime) -> f.BookRateOccurrenceV1:
    f._utc(now)
    if (type(req) is not f.BookRateRequestV1
        or canonical(req) != canonical(_request()) or now < CUTOFF):
        raise ValueError("incompatible exact D139 receipt-rate request")
    standing, ids, size = _replay(lines)
    count_rate = Fraction(len(ids), req.window_seconds)
    size_rate = Fraction(size) / req.window_seconds
    result = f.BookRatePairV1(
        f.ExactRatioV1(count_rate.numerator, count_rate.denominator),
        f.ExactRatioV1(size_rate.numerator, size_rate.denominator),
    )
    value = f.BookRateOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D139", "pending", req, DEFINITION, PARAMETER,
        SELECTION, UNITS, MAPS, lines, standing, ids, result, "events or size/time",
        "book_rate_pair", T, CUTOFF, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return replace(value, derived_occurrence_id="mmtrate1:" +
                   hashlib.sha256(canonical(payload)).hexdigest())


def _validate(value: f.BookRateOccurrenceV1) -> None:
    if type(value) is not f.BookRateOccurrenceV1:
        raise TypeError("exact D139 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.calculated_at_utc)):
        raise ValueError("D139 receipt/source/rate identity mismatch")


def _decode(payload: bytes) -> f.BookRateOccurrenceV1:
    return cast(f.BookRateOccurrenceV1, decode(payload, f.BookRateOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.BookRateOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty rate identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(self, *, derived_signal_id: str, subject_instrument: str,
                             effective_at_or_before_utc: datetime,
                             knowledge_at_or_before_utc: datetime, limit: int
                             ) -> tuple[f.BookRateOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid rate history query")
        return tuple(sorted((v for v in self.state.all()
                             if v.derived_signal_id == derived_signal_id
                             and v.request.calculation.subject_instrument == subject_instrument
                             and v.effective_as_of_utc <= effective_at_or_before_utc
                             and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc),
                            key=lambda v: (v.effective_as_of_utc, v.knowledge_cutoff_utc,
                                           v.derived_occurrence_id), reverse=True)[:limit])


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, req: f.BookRateRequestV1) -> f.BookRateOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            if type(req) is not f.BookRateRequestV1:
                raise TypeError("exact receipt-rate request required")
            lines: list[f.BookRateRawLineageV1] = []
            for role, mapping in enumerate(MAPS):
                cursor: str | None = None
                cursors: set[str] = set()
                while True:
                    page = self.raw.list_projected_raw_history(
                        mapping.raw_signal_catalogue_id, mappings=(mapping,),
                        subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
                        event_at_or_before_utc=T, limit=100, cursor=cursor,
                    )
                    if type(page) is not r.ProjectedRawHistoryPageV1:
                        raise ValueError("invalid typed receipt-book page")
                    lines.extend(_line(item, role) for item in page.items)
                    if len(lines) > SELECTION.maximum_events * len(MAPS):
                        raise ValueError("unbounded receipt-book history")
                    if page.next_cursor is None:
                        break
                    if page.next_cursor in cursors or not page.items:
                        raise ValueError("nonprogressing receipt-book cursor")
                    cursor = page.next_cursor
                    cursors.add(cursor)
            lines.sort(key=lambda line: (line.projection.received_ts_utc,
                                         line.projection.ingestion_sequence,
                                         next(i for i, role in enumerate(ROLES)
                                              if role[0] == line.raw_signal_id)))
            value = _produce(req, tuple(lines), now)
        except (ValueError, TypeError, ArithmeticError):
            return None
        return cast(f.BookRateOccurrenceV1, self.state.append(value))


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementBookRateOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D139 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact receipt-book storage and clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.MeasurementBookRateReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("exact D139 reader required")
    return _Reads(RecordState(storage, _decode, _validate))
