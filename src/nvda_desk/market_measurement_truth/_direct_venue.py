"""D143 two-venue direct positional book concentration."""

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

BRIEF = "a6008036bb46d81996ac5bc9d9054db8544349d90477b806b0184def034fff9d"
NAMESPACE = "neutral_market_measurement_truth/direct-venue/v1"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
SUBJECT = "NVDA"
PROVIDER, VARIANT = "foundation-controlled-direct-book", "direct_venue_v1"
GENERATION = "controlled-direct-generation/1"
ROLES = (
    ("R192", "position", "book_position"), ("R193", "marketMaker", "venue_id"),
    ("R194", "operation", "book_operation"), ("R195", "side", "book_side"),
    ("R196", "price", "USD_per_share"), ("R197", "size", "shares"),
)
IDENTITY = (("generation.id", ("generation", "id")),
            ("event.id", ("event", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d143-" + rid.lower(), 1, r.RawSignalCatalogueId(rid), PROVIDER,
    VARIANT, ("book", field), unit, IDENTITY,
) for rid, field, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d143-" + rid.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for rid, _, unit in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D143", "D143-DIRECT-VENUE-CONCENTRATION-1", "K02_ALGEBRA",
    "per-venue complete standing top-one bid+ask depth shares and sum squared shares",
    tuple(rid for rid, _, _ in ROLES), (), "P_BASIC", "concentration index",
    "venue_concentration", tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d143-two-venues-top-one", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d143-direct-positional", 1), PROVIDER, VARIANT,
    GENERATION, T - timedelta(seconds=10), 100,
)
VENUES = ("ALPHA", "BETA")


def _request() -> f.DirectVenueRequestV1:
    return f.DirectVenueRequestV1(f.CalculationRequestV1(
        "D143", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
        tuple(f.RawInputBindingV1(
            rid, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (rid, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION, VENUES, 1)


def _line(item: r.ProjectedRawValueV1, role: int) -> f.DirectBookRawLineageV1:
    rid, _, _ = ROLES[role]
    mapping, unit = MAPS[role], UNITS[role]
    expected = str if role == 1 else int if role in (0, 2, 3) else Decimal
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
        raise ValueError("ineligible typed direct-book projection")
    f._utc(item.received_ts_utc)
    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
    f._utc(event)
    if not SELECTION.history_complete_from_utc <= event <= T or event > item.received_ts_utc:
        raise ValueError("ineligible direct event timestamp")
    if role == 0 and cast(int, item.native_value) < 0:
        raise ValueError("negative position")
    if role == 1 and item.native_value not in VENUES:
        raise ValueError("unknown direct marketMaker/venue")
    if role == 2 and item.native_value not in (0, 1, 2, 317):
        raise ValueError("unknown direct operation")
    if role == 3 and item.native_value not in (0, 1):
        raise ValueError("unknown direct side")
    if role >= 4 and (not cast(Decimal, item.native_value).is_finite()
                      or cast(Decimal, item.native_value) < 0):
        raise ValueError("invalid direct price/size")
    return f.DirectBookRawLineageV1(
        rid, item.observation_occurrence_id.value, f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(unit.context_id, 1), item, item.native_value, event,
    )


def _replay(lines: tuple[f.DirectBookRawLineageV1, ...]
            ) -> tuple[f.DirectVenueRowV1, ...]:
    groups: dict[str, dict[str, f.DirectBookRawLineageV1]] = {}
    for line in lines:
        role = next((i for i, row in enumerate(ROLES) if row[0] == line.raw_signal_id), -1)
        if role < 0 or canonical(line) != canonical(_line(line.projection, role)):
            raise ValueError("direct lineage differs from actual projection")
        group = groups.setdefault(line.observation_occurrence_id, {})
        if line.raw_signal_id in group:
            raise ValueError("duplicate direct role")
        group[line.raw_signal_id] = line
    if not groups or len(groups) > SELECTION.maximum_events:
        raise ValueError("incomplete or unbounded direct book")
    ordered = sorted(groups.values(), key=lambda group: (
        next(iter(group.values())).projection.received_ts_utc,
        next(iter(group.values())).projection.ingestion_sequence,
    ))
    books: dict[tuple[str, int], list[f.DirectVenueRowV1]] = {
        (venue, side): [] for venue in VENUES for side in (0, 1)
    }
    previous_key: tuple[datetime, int] | None = None
    for group in ordered:
        if set(group) != {x[0] for x in ROLES}:
            raise ValueError("incomplete six-field direct event")
        first = group["R193"]
        key = (first.projection.received_ts_utc, first.projection.ingestion_sequence)
        if previous_key is not None and key <= previous_key:
            raise ValueError("ambiguous direct event ordering")
        previous_key = key
        identity = first.projection.selection_identity
        if any((line.projection.selection_identity != identity
                or line.event_time_utc != first.event_time_utc
                or line.projection.received_ts_utc != first.projection.received_ts_utc
                or line.projection.ingestion_sequence != first.projection.ingestion_sequence)
               for line in group.values()):
            raise ValueError("mixed native direct event")
        venue = cast(str, first.canonical_value)
        side = cast(int, group["R195"].canonical_value)
        operation = cast(int, group["R194"].canonical_value)
        pos = cast(int, group["R192"].canonical_value)
        price = cast(Decimal, group["R196"].canonical_value)
        size = cast(Decimal, group["R197"].canonical_value)
        if operation == 317:
            books = {(v, s): [] for v in VENUES for s in (0, 1)}
            continue
        rows = books[(venue, side)]
        if operation == 0:
            if pos > len(rows) or price <= 0 or size <= 0:
                raise ValueError("invalid direct insert")
            rows.insert(pos, f.DirectVenueRowV1(venue, side, pos, price, size))
        elif operation == 1:
            if pos >= len(rows) or price <= 0 or size <= 0:
                raise ValueError("direct update without row")
            rows[pos] = f.DirectVenueRowV1(venue, side, pos, price, size)
        else:
            if pos >= len(rows) or price != rows[pos].price or size != 0:
                raise ValueError("direct delete without matching standing row")
            del rows[pos]
        rows[:] = [replace(row, position=i) for i, row in enumerate(rows)]
    if any(len(rows) != 1 for rows in books.values()):
        raise ValueError("complete bid and ask top one for each venue required")
    if any(books[(v, 0)][0].price > books[(v, 1)][0].price for v in VENUES):
        raise ValueError("crossed direct venue book")
    return tuple(row for venue in VENUES for side in (0, 1) for row in books[(venue, side)])


def _produce(req: f.DirectVenueRequestV1,
             lines: tuple[f.DirectBookRawLineageV1, ...], now: datetime
             ) -> f.DirectVenueOccurrenceV1:
    f._utc(now)
    if (type(req) is not f.DirectVenueRequestV1
        or canonical(req) != canonical(_request()) or now < CUTOFF):
        raise ValueError("incompatible D143 direct selection")
    rows = _replay(lines)
    depths = tuple(sum((Fraction(row.size) for row in rows if row.venue == venue),
                       Fraction()) for venue in VENUES)
    total = sum(depths, Fraction())
    if total <= 0:
        raise ValueError("zero direct venue depth")
    shares = tuple(d / total for d in depths)
    hhi = sum((x*x for x in shares), Fraction())
    result = f.VenueConcentrationV1(
        VENUES, tuple(f.ExactRatioV1(x.numerator, x.denominator) for x in shares),
        f.ExactRatioV1(hhi.numerator, hhi.denominator),
    )
    value = f.DirectVenueOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D143", "pending", req, DEFINITION, PARAMETER,
        SELECTION, UNITS, MAPS, lines, rows, result, "concentration index",
        "venue_concentration", T, CUTOFF, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return replace(value, derived_occurrence_id="mmtvenue1:" +
                   hashlib.sha256(canonical(payload)).hexdigest())


def _validate(value: f.DirectVenueOccurrenceV1) -> None:
    if type(value) is not f.DirectVenueOccurrenceV1:
        raise TypeError("exact D143 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.calculated_at_utc)):
        raise ValueError("D143 venue/source/result mismatch")


def _decode(payload: bytes) -> f.DirectVenueOccurrenceV1:
    return cast(f.DirectVenueOccurrenceV1, decode(payload, f.DirectVenueOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.DirectVenueOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty direct venue identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(self, *, derived_signal_id: str, subject_instrument: str,
                             effective_at_or_before_utc: datetime,
                             knowledge_at_or_before_utc: datetime, limit: int
                             ) -> tuple[f.DirectVenueOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid venue history query")
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

    def materialise(self, req: f.DirectVenueRequestV1) -> f.DirectVenueOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            if type(req) is not f.DirectVenueRequestV1:
                raise TypeError("exact direct request required")
            lines: list[f.DirectBookRawLineageV1] = []
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
                        raise ValueError("invalid direct source page")
                    lines.extend(_line(item, role) for item in page.items)
                    if len(lines) > SELECTION.maximum_events * len(MAPS):
                        raise ValueError("unbounded direct history")
                    if page.next_cursor is None:
                        break
                    if page.next_cursor in cursors or not page.items:
                        raise ValueError("nonprogressing direct cursor")
                    cursor = page.next_cursor
                    cursors.add(cursor)
            lines.sort(key=lambda line: (line.projection.received_ts_utc,
                                         line.projection.ingestion_sequence,
                                         next(i for i, role in enumerate(ROLES)
                                              if role[0] == line.raw_signal_id)))
            value = _produce(req, tuple(lines), now)
        except (ValueError, TypeError, ArithmeticError):
            return None
        return cast(f.DirectVenueOccurrenceV1, self.state.append(value))


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementDirectVenueOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D143 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact direct storage and clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.MeasurementDirectVenueReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("exact D143 reader required")
    return _Reads(RecordState(storage, _decode, _validate))
