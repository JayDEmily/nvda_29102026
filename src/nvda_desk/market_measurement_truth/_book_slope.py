"""D138 exact per-side OLS depth slopes over an actual D011 midpoint."""

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

BRIEF = "c2e78da695a7681cc75ff117282127e0208df0e00ff31a0a5717aeb4dd954647"
NAMESPACE = "neutral_market_measurement_truth/book-slope/v1"
SUBJECT = "NVDA"
T = datetime(2026, 10, 16, 1, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
PROVIDER, VARIANT = "foundation-controlled-smart-book", "positional_slope_v1"
GENERATION = "controlled-smart-slope-generation/1"
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d138-smart-positional", 1), PROVIDER, VARIANT,
    GENERATION, T - timedelta(seconds=10), 100,
)
ROLES = (
    ("R185", "position", "book_position"), ("R187", "operation", "book_operation"),
    ("R188", "side", "book_side"), ("R189", "price", "USD_per_share"),
    ("R190", "size", "shares"),
)
IDENTITY = (("generation.id", ("generation", "id")),
            ("event.id", ("event", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d138-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), PROVIDER, VARIANT,
    ("book", field), unit, IDENTITY,
) for raw, field, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d138-" + raw.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for raw, _, unit in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D138", "D138-L2-CONTRACT-20261016-01", "K06_REGRESSION",
    "OLS(cumulative standing depth, abs(price - actual D011 midpoint)) per side",
    tuple(raw for raw, _, _ in ROLES), ("D011",), "P_BASIC", "shares_per_USD",
    "book_slope_pair", tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d138-three-level", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)


def _request(parent_id: str) -> f.BookSlopeRequestV1:
    return f.BookSlopeRequestV1(f.CalculationRequestV1(
        "D138", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
        tuple(f.RawInputBindingV1(
            raw, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (raw, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION, parent_id, 3)


def _line(item: r.ProjectedRawValueV1, role: int) -> f.BookRawLineageV1:
    raw, _, _ = ROLES[role]
    mapping, unit = MAPS[role], UNITS[role]
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
        or type(item.native_value) is not (int if role < 3 else Decimal)
        or item.received_ts_utc > CUTOFF
        or type(item.source_timestamp_raw) is not str):
        raise ValueError("ineligible exact typed SMART projection")
    f._utc(item.received_ts_utc)
    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
    f._utc(event)
    if not SELECTION.history_complete_from_utc <= event <= T or event > item.received_ts_utc:
        raise ValueError("ineligible SMART event time")
    if role == 0 and cast(int, item.native_value) < 0:
        raise ValueError("negative position")
    if role == 1 and item.native_value not in (0, 1, 2, 317):
        raise ValueError("unknown operation")
    if role == 2 and item.native_value not in (0, 1):
        raise ValueError("unknown side")
    if role >= 3 and (not cast(Decimal, item.native_value).is_finite()
                      or item.native_value < 0):
        raise ValueError("invalid price or size")
    return f.BookRawLineageV1(
        raw, item.observation_occurrence_id.value, f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(unit.context_id, 1), item, item.native_value, event,
    )


def _replay(lines: tuple[f.BookRawLineageV1, ...]) -> tuple[f.BookRowV1, ...]:
    groups: dict[str, dict[str, f.BookRawLineageV1]] = {}
    for line in lines:
        role = next((i for i, item in enumerate(ROLES) if item[0] == line.raw_signal_id), -1)
        if role < 0 or canonical(line) != canonical(_line(line.projection, role)):
            raise ValueError("book lineage differs from actual projection")
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
    sides: dict[int, list[f.BookRowV1]] = {0: [], 1: []}
    previous_key: tuple[datetime, int] | None = None
    for group in ordered:
        if "R187" not in group:
            raise ValueError("missing operation")
        first = group["R187"]
        key = (first.projection.received_ts_utc, first.projection.ingestion_sequence)
        if previous_key is not None and key <= previous_key:
            raise ValueError("ambiguous native event order")
        previous_key = key
        identity = first.projection.selection_identity
        if any((line.projection.selection_identity != identity
                or line.event_time_utc != first.event_time_utc
                or line.projection.received_ts_utc != first.projection.received_ts_utc
                or line.projection.ingestion_sequence != first.projection.ingestion_sequence)
               for line in group.values()):
            raise ValueError("mixed native event group")
        operation = cast(int, first.canonical_value)
        if operation == 317:
            if set(group) != {"R187"}:
                raise ValueError("reset only carries operation")
            sides = {0: [], 1: []}
            continue
        if set(group) != {x[0] for x in ROLES}:
            raise ValueError("incomplete five-field mutation")
        side = cast(int, group["R188"].canonical_value)
        pos = cast(int, group["R185"].canonical_value)
        price = cast(Decimal, group["R189"].canonical_value)
        size = cast(Decimal, group["R190"].canonical_value)
        rows = sides[side]
        if operation == 0:
            if pos > len(rows) or price <= 0 or size <= 0:
                raise ValueError("invalid positional insert")
            rows.insert(pos, f.BookRowV1(side, pos, price, size))
        elif operation == 1:
            if pos >= len(rows) or price <= 0 or size <= 0:
                raise ValueError("update without standing row")
            rows[pos] = f.BookRowV1(side, pos, price, size)
        else:
            if pos >= len(rows) or price != rows[pos].price or size != 0:
                raise ValueError("delete without matching standing row")
            del rows[pos]
        rows[:] = [replace(row, position=i) for i, row in enumerate(rows)]
    if any(len(rows) != 3 for rows in sides.values()):
        raise ValueError("three complete levels per side required after reset")
    for side, rows in sides.items():
        prices = [row.price for row in rows]
        if any((prices[i] <= prices[i + 1]) if side == 0 else
               (prices[i] >= prices[i + 1]) for i in range(2)):
            raise ValueError("invalid side price ladder")
    return tuple((*sides[0], *sides[1]))


def _slope(rows: tuple[f.BookRowV1, ...], midpoint: Fraction, side: int
           ) -> f.ExactRatioV1:
    own = [row for row in rows if row.side == side]
    xs = [abs(Fraction(row.price) - midpoint) for row in own]
    if len(own) != 3 or len(set(xs)) != 3 or any(x <= 0 for x in xs):
        raise ValueError("three distinct positive midpoint distances required")
    cumulative = []
    total = Fraction(0)
    for row in own:
        total += Fraction(row.size)
        cumulative.append(total)
    n = len(xs)
    numerator = (
        n * sum((x * y for x, y in zip(xs, cumulative, strict=True)), Fraction(0))
        - sum(xs) * sum(cumulative)
    )
    denominator = n * sum((x * x for x in xs), Fraction(0)) - sum(xs) ** 2
    if denominator <= 0:
        raise ValueError("degenerate OLS distance")
    answer = numerator / denominator
    return f.ExactRatioV1(answer.numerator, answer.denominator)


def _produce(req: f.BookSlopeRequestV1, lines: tuple[f.BookRawLineageV1, ...],
             parent: f.DerivedSignalOccurrenceV1, now: datetime
             ) -> f.BookSlopeOccurrenceV1:
    f._utc(now)
    if (type(req) is not f.BookSlopeRequestV1
        or canonical(req) != canonical(_request(req.predecessor_occurrence_id))
        or now < CUTOFF):
        raise ValueError("incompatible exact D138 request")
    f._Validated.__post_init__(parent)
    if (type(parent) is not f.DerivedSignalOccurrenceV1
        or parent.derived_occurrence_id != req.predecessor_occurrence_id
        or parent.derived_signal_id != "D011"
        or parent.owner_object_id != "M02"
        or parent.implementation_brief_sha256 != (
            "3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233"
        )
        or parent.calculation_definition_version != "D011-MIDPOINT-1"
        or parent.subject_instrument != SUBJECT or parent.result != Decimal(100)
        or parent.effective_as_of_utc != T or parent.knowledge_cutoff_utc != CUTOFF
        or parent.calculated_at_utc > now
        or tuple(x.raw_signal_id for x in parent.raw_input_lineage) != ("R034", "R035")):
        raise ValueError("actual compatible D011 midpoint required")
    rows = _replay(lines)
    midpoint = Fraction(parent.result)
    result = f.BookSlopePairV1(_slope(rows, midpoint, 0), _slope(rows, midpoint, 1))
    value = f.BookSlopeOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D138", "pending", req, DEFINITION, PARAMETER,
        UNITS, MAPS, lines, parent, rows, result, "shares_per_USD", "book_slope_pair",
        T, CUTOFF, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return replace(value, derived_occurrence_id="mmtslope1:" +
                   hashlib.sha256(canonical(payload)).hexdigest())


def _validate(value: f.BookSlopeOccurrenceV1) -> None:
    if type(value) is not f.BookSlopeOccurrenceV1:
        raise TypeError("exact D138 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.predecessor, value.calculated_at_utc)):
        raise ValueError("D138 source/predecessor/result mismatch")


def _decode(payload: bytes) -> f.BookSlopeOccurrenceV1:
    return cast(f.BookSlopeOccurrenceV1, decode(payload, f.BookSlopeOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.BookSlopeOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty slope identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(self, *, derived_signal_id: str, subject_instrument: str,
                             effective_at_or_before_utc: datetime,
                             knowledge_at_or_before_utc: datetime, limit: int
                             ) -> tuple[f.BookSlopeOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid slope history query")
        return tuple(sorted((v for v in self.state.all()
                             if v.derived_signal_id == derived_signal_id
                             and v.request.calculation.subject_instrument == subject_instrument
                             and v.effective_as_of_utc <= effective_at_or_before_utc
                             and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc),
                            key=lambda v: (v.effective_as_of_utc, v.knowledge_cutoff_utc,
                                           v.derived_occurrence_id), reverse=True)[:limit])


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 predecessor: f.MeasurementReadsV1, now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.predecessor, self.now = state, raw, predecessor, now
        self.reads = _Reads(state)

    def materialise(self, req: f.BookSlopeRequestV1) -> f.BookSlopeOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            if type(req) is not f.BookSlopeRequestV1:
                raise TypeError("exact slope request required")
            parent = self.predecessor.get_derived_occurrence(req.predecessor_occurrence_id)
            if type(parent) is not f.DerivedSignalOccurrenceV1:
                return None
            lines: list[f.BookRawLineageV1] = []
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
                        raise ValueError("invalid book page")
                    lines.extend(_line(item, role) for item in page.items)
                    if len(lines) > SELECTION.maximum_events * len(MAPS):
                        raise ValueError("unbounded book history")
                    if page.next_cursor is None:
                        break
                    if page.next_cursor in cursors or not page.items:
                        raise ValueError("nonprogressing book cursor")
                    cursor = page.next_cursor
                    cursors.add(cursor)
            lines.sort(key=lambda line: (line.projection.received_ts_utc,
                                         line.projection.ingestion_sequence,
                                         next(i for i, role in enumerate(ROLES)
                                              if role[0] == line.raw_signal_id)))
            value = _produce(req, tuple(lines), parent, now)
        except (ValueError, TypeError, ArithmeticError):
            return None
        return cast(f.BookSlopeOccurrenceV1, self.state.append(value))


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                predecessor: f.MeasurementReadsV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementBookSlopeOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D138 admission required")
    if (type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now)
        or not callable(getattr(predecessor, "get_derived_occurrence", None))):
        raise TypeError("actual D011 reader and storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, predecessor, now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.MeasurementBookSlopeReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("exact D138 reader required")
    return _Reads(RecordState(storage, _decode, _validate))
