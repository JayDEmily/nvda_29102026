"""D140 receipt-clock delete rate using actual pre-delete standing size."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _book_insert_rate as source
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._record_store import RecordState

BRIEF = "ea4c81074d0f5e774b93f4d34b4d6d1be58d8a8a9bb121521149a9dc00f7bd58"
NAMESPACE = source.NAMESPACE
T, CUTOFF, SUBJECT = source.T, source.CUTOFF, source.SUBJECT
ROLES, MAPS, UNITS = source.ROLES, source.MAPS, source.UNITS
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d140-receipt-positional", 1), source.PROVIDER, source.VARIANT,
    source.GENERATION, T - timedelta(seconds=10), 100,
)
DEFINITION = f.CalculationDefinitionV1(
    "D140", "D140-RECEIPT-CLOCK-DELETE-RATE-1", "K08_RULE_BUCKET_POLICY",
    "count and pre-delete standing size of bid positions1-2 in two-second R001 receipt bucket",
    tuple(raw for raw, _, _ in ROLES), (), "P_RULE", "events or size/time",
    "book_rate_pair", tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d140-bid-positions1-2-2s", 1, "P_RULE", SUBJECT, (SUBJECT,),
)


def _request() -> f.BookRateRequestV1:
    return f.BookRateRequestV1(f.CalculationRequestV1(
        "D140", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
        tuple(f.RawInputBindingV1(
            rid, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (rid, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION, 2, 0, (1, 2))


def _replay(lines: tuple[f.BookRateRawLineageV1, ...]
            ) -> tuple[tuple[f.SmartSizeRowV1, ...], tuple[str, ...], Decimal]:
    groups: dict[str, dict[str, f.BookRateRawLineageV1]] = {}
    for line in lines:
        role = next((i for i, row in enumerate(ROLES) if row[0] == line.raw_signal_id), -1)
        if role < 0 or canonical(line) != canonical(source._line(line.projection, role)):
            raise ValueError("receipt-book lineage differs from public projection")
        group = groups.setdefault(line.observation_occurrence_id, {})
        if line.raw_signal_id in group:
            raise ValueError("duplicate native book role")
        group[line.raw_signal_id] = line
    if not groups or len(groups) > SELECTION.maximum_events:
        raise ValueError("incomplete or unbounded book")
    ordered = sorted(groups.values(), key=lambda group: (
        next(iter(group.values())).projection.received_ts_utc,
        next(iter(group.values())).projection.ingestion_sequence,
    ))
    sides: dict[int, list[f.SmartSizeRowV1]] = {0: [], 1: []}
    warm = False
    selected: list[str] = []
    removed = Decimal(0)
    previous_key: tuple[datetime, int] | None = None
    for group in ordered:
        if set(group) != {x[0] for x in ROLES}:
            raise ValueError("actual R001 and four complete book fields required")
        first = group["R001"]
        receipt = cast(datetime, first.canonical_value)
        key = (receipt, first.projection.ingestion_sequence)
        if previous_key is not None and key <= previous_key:
            raise ValueError("ambiguous receipt/ingestion order")
        previous_key = key
        identity = first.projection.selection_identity
        if any((line.projection.selection_identity != identity
                or line.event_time_utc != first.event_time_utc
                or line.projection.received_ts_utc != receipt
                or line.projection.ingestion_sequence != first.projection.ingestion_sequence)
               for line in group.values()):
            raise ValueError("mixed native event")
        operation = cast(int, group["R187"].canonical_value)
        side = cast(int, group["R188"].canonical_value)
        pos = cast(int, group["R185"].canonical_value)
        native_size = cast(Decimal, group["R190"].canonical_value)
        in_window = T - timedelta(seconds=2) < receipt <= T
        if in_window and not warm:
            raise ValueError("missing complete pre-window standing book")
        if operation == 317:
            sides = {0: [], 1: []}
            warm = False
            continue
        rows = sides[side]
        if operation == 0:
            if pos > len(rows) or native_size <= 0:
                raise ValueError("invalid positional insert")
            rows.insert(pos, f.SmartSizeRowV1(side, pos, native_size))
        elif operation == 1:
            if pos >= len(rows) or native_size <= 0:
                raise ValueError("update without standing row")
            rows[pos] = f.SmartSizeRowV1(side, pos, native_size)
        else:
            if pos >= len(rows) or native_size != 0:
                raise ValueError("delete requires actual standing row and native zero size")
            old_size = rows[pos].size
            del rows[pos]
            if in_window and side == 0 and pos in (1, 2):
                selected.append(first.observation_occurrence_id)
                removed += old_size
        rows[:] = [replace(row, position=i) for i, row in enumerate(rows)]
        if not in_window:
            warm = bool(sides[0] and sides[1])
        elif side == 0 and pos in (1, 2) and operation != 2:
            raise ValueError("selected bid mutation is not a delete")
    if not warm or len(selected) != 1:
        raise ValueError("missing warm-up or selected deletion")
    return tuple((*sides[0], *sides[1])), tuple(selected), removed


def _produce(req: f.BookRateRequestV1, lines: tuple[f.BookRateRawLineageV1, ...],
             now: datetime) -> f.BookRateOccurrenceV1:
    f._utc(now)
    if (type(req) is not f.BookRateRequestV1
        or canonical(req) != canonical(_request()) or now < CUTOFF):
        raise ValueError("incompatible D140 receipt-delete request")
    standing, ids, removed = _replay(lines)
    count_rate = Fraction(len(ids), req.window_seconds)
    size_rate = Fraction(removed) / req.window_seconds
    result = f.BookRatePairV1(
        f.ExactRatioV1(count_rate.numerator, count_rate.denominator),
        f.ExactRatioV1(size_rate.numerator, size_rate.denominator),
    )
    value = f.BookRateOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D140", "pending", req, DEFINITION, PARAMETER,
        SELECTION, UNITS, MAPS, lines, standing, ids, result, "events or size/time",
        "book_rate_pair", T, CUTOFF, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return replace(value, derived_occurrence_id="mmtrate1:" +
                   hashlib.sha256(canonical(payload)).hexdigest())


def _validate(value: f.BookRateOccurrenceV1) -> None:
    if type(value) is not f.BookRateOccurrenceV1:
        raise TypeError("exact D140 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.calculated_at_utc)):
        raise ValueError("D140 standing-size/source/rate mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = source._Reads(state)

    def materialise(self, req: f.BookRateRequestV1) -> f.BookRateOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            if type(req) is not f.BookRateRequestV1:
                raise TypeError("exact deletion-rate request required")
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
                        raise ValueError("invalid receipt-book page")
                    lines.extend(source._line(item, role) for item in page.items)
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
        raise ValueError("exact D140 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact receipt-book storage and clock required")
    return _Owner(RecordState(storage, source._decode, _validate), raw, now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.MeasurementBookRateReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("exact D140 reader required")
    return source._Reads(RecordState(storage, source._decode, _validate))
