"""D131 controlled positional SMART book and exact same-contract midpoint band."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _option_scalars
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState

BRIEF = "c095187484e295c35e1c27906480a0793d81d76091fac21fc9002ac6c521302c"
NAMESPACE = "neutral_market_measurement_truth/book-depth/v1"
PROVIDER, VARIANT = "foundation-controlled-smart-book", "positional_v1"
SUBJECT = _option_scalars.C1
T = _option_scalars.T
CUTOFF = T + timedelta(seconds=1)
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d131-smart-positional", 1), PROVIDER, VARIANT,
    "controlled-smart-book-generation/1", T - timedelta(seconds=10), 100,
)
ROLES = (
    ("R185", "position", "book_position", "position"),
    ("R187", "operation", "book_operation", "operation"),
    ("R188", "side", "book_side", "side"),
    ("R189", "price", "USD_per_share", "price"),
    ("R190", "size", "contracts", "size"),
)
IDENTITY = (("generation.id", ("generation", "id")),
            ("event.id", ("event", "id")), ("contract.id", ("contract", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d131-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), PROVIDER, VARIANT,
    ("book", field), units, IDENTITY,
) for raw, field, units, _ in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d131-" + raw.lower() + "-unit", 1, units, units, Decimal(1), Decimal(0),
) for raw, _, units, _ in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D131", "D131-POSITIONAL-OPTION-DEPTH-BAND-1", "K02_ALGEBRA",
    "sum(standing size where abs(price - actual D087 midpoint) <= band)",
    tuple(raw for raw, *_ in ROLES), ("D087",), "P_BASIC", "contracts",
    "scalar_decimal", tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d131-half-dollar", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)


def request(predecessor_occurrence_id: str) -> f.BookDepthRequestV1:
    return f.BookDepthRequestV1(
        f.CalculationRequestV1(
            "D131", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
            tuple(f.RawInputBindingV1(
                raw, f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(unit.context_id, 1), SUBJECT,
            ) for (raw, *_), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
        ), SELECTION, predecessor_occurrence_id, Decimal("0.5"),
    )


def _request(value: f.BookDepthRequestV1, now: datetime) -> None:
    f._utc(now)
    if (type(value) is not f.BookDepthRequestV1 or not value.predecessor_occurrence_id
        or canonical(value) != canonical(request(value.predecessor_occurrence_id))
        or now < CUTOFF):
        raise ValueError("incompatible controlled D131 request")


def _line(item: r.ProjectedRawValueV1, role: int
          ) -> f.BookRawLineageV1:
    raw, _, _, _ = ROLES[role]
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
        or item.selection_identity.value_for("generation.id") != SELECTION.generation
        or item.selection_identity.value_for("contract.id") != SUBJECT
        or not item.selection_identity.value_for("event.id")
        or type(item.native_value) is not (int if role < 3 else Decimal)
        or item.received_ts_utc > CUTOFF
        or type(item.source_timestamp_raw) is not str):
        raise ValueError("unmatched or ineligible typed book field")
    f._utc(item.received_ts_utc)
    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
    f._utc(event)
    if (not SELECTION.history_complete_from_utc <= event <= T
        or event > item.received_ts_utc):
        raise ValueError("ineligible book event time")
    if role == 0 and item.native_value < 0:
        raise ValueError("negative book position")
    if role == 1 and item.native_value not in (0, 1, 2, 317):
        raise ValueError("unknown book operation")
    if role == 2 and item.native_value not in (0, 1):
        raise ValueError("unknown book side")
    if role >= 3 and (not cast(Decimal, item.native_value).is_finite()
                      or item.native_value < 0):
        raise ValueError("invalid book price or size")
    return f.BookRawLineageV1(
        raw, item.observation_occurrence_id.value, f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(unit.context_id, 1), item, item.native_value, event,
    )


def _replay(lines: tuple[f.BookRawLineageV1, ...]
            ) -> tuple[f.BookRowV1, ...]:
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
        raise ValueError("incomplete or unbounded book history")
    ordered = sorted(groups.values(), key=lambda group: (
        next(iter(group.values())).event_time_utc,
        next(iter(group.values())).projection.received_ts_utc,
        next(iter(group.values())).projection.ingestion_sequence,
    ))
    sides: dict[int, list[f.BookRowV1]] = {0: [], 1: []}
    saw_bid = saw_ask = False
    previous_key: tuple[datetime, datetime, int] | None = None
    for group in ordered:
        if "R187" not in group:
            raise ValueError("missing operation")
        first = group["R187"]
        key = (first.event_time_utc, first.projection.received_ts_utc,
               first.projection.ingestion_sequence)
        if previous_key is not None and key <= previous_key:
            raise ValueError("ambiguous event order")
        previous_key = key
        identity = first.projection.selection_identity
        if any((line.projection.selection_identity != identity
                or line.event_time_utc != first.event_time_utc
                or line.projection.received_ts_utc != first.projection.received_ts_utc
                or line.projection.ingestion_sequence != first.projection.ingestion_sequence)
               for line in group.values()):
            raise ValueError("mixed native occurrence")
        operation = cast(int, first.canonical_value)
        if operation == 317:
            if set(group) != {"R187"}:
                raise ValueError("reset carries only operation")
            sides = {0: [], 1: []}
            saw_bid = saw_ask = False
            continue
        if set(group) != {"R185", "R187", "R188", "R189", "R190"}:
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
        saw_bid |= side == 0
        saw_ask |= side == 1
    if not (saw_bid and saw_ask and sides[0] and sides[1]):
        raise ValueError("book reset without complete fresh two-side warm-up")
    return tuple((*sides[0], *sides[1]))


def _produce(req: f.BookDepthRequestV1, lines: tuple[f.BookRawLineageV1, ...],
             parent: f.WindowMeasurementOccurrenceV1, now: datetime
             ) -> f.BookDepthOccurrenceV1:
    _request(req, now)
    _option_scalars.validate(parent)
    if (parent.derived_occurrence_id != req.predecessor_occurrence_id
        or parent.derived_signal_id != "D087"
        or parent.request.calculation.subject_instrument != SUBJECT
        or parent.effective_as_of_utc != T or parent.knowledge_cutoff_utc != CUTOFF
        or parent.calculated_at_utc > now or type(parent.result) is not f.ExactRatioV1):
        raise ValueError("actual same-contract midpoint required")
    midpoint = Fraction(parent.result.numerator, parent.result.denominator)
    if midpoint != 100:
        raise ValueError("incompatible controlled option midpoint")
    rows = _replay(lines)
    selected = tuple(row for row in rows if abs(Fraction(row.price) - midpoint)
                     <= Fraction(req.band))
    depth = sum((row.size for row in selected), Decimal(0))
    value = f.BookDepthOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D131", "pending", req, DEFINITION, PARAMETER,
        UNITS, MAPS, lines, parent, rows, depth, "contracts", "scalar_decimal", T,
        CUTOFF, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return replace(value, derived_occurrence_id="mmtbook1:" +
                   hashlib.sha256(canonical(payload)).hexdigest())


def _validate(value: f.BookDepthOccurrenceV1) -> None:
    if type(value) is not f.BookDepthOccurrenceV1:
        raise TypeError("exact D131 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.predecessor, value.calculated_at_utc
    )):
        raise ValueError("D131 book/parent/result/identity mismatch")


def _decode(payload: bytes) -> f.BookDepthOccurrenceV1:
    return cast(f.BookDepthOccurrenceV1, decode(payload, f.BookDepthOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.BookDepthOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty book occurrence identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(self, *, derived_signal_id: str, subject_instrument: str,
                             effective_at_or_before_utc: datetime,
                             knowledge_at_or_before_utc: datetime, limit: int
                             ) -> tuple[f.BookDepthOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid book history query")
        return tuple(sorted((v for v in self.state.all()
                             if v.derived_signal_id == derived_signal_id
                             and v.request.calculation.subject_instrument == subject_instrument
                             and v.effective_as_of_utc <= effective_at_or_before_utc
                             and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc),
                            key=lambda v: (v.effective_as_of_utc, v.knowledge_cutoff_utc,
                                           v.derived_occurrence_id), reverse=True)[:limit])


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 predecessor: f.MeasurementWindowReadsV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.predecessor, self.now = state, raw, predecessor, now
        self.reads = _Reads(state)

    def materialise(self, req: f.BookDepthRequestV1) -> f.BookDepthOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            _request(req, now)
            parent = self.predecessor.get_derived_occurrence(req.predecessor_occurrence_id)
            if type(parent) is not f.WindowMeasurementOccurrenceV1:
                return None
            lines: list[f.BookRawLineageV1] = []
            for role, mapping in enumerate(MAPS):
                cursor: str | None = None
                while True:
                    page = self.raw.list_projected_raw_history(
                        mapping.raw_signal_catalogue_id, mappings=(mapping,),
                        subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
                        event_at_or_before_utc=T, limit=100, cursor=cursor,
                    )
                    lines.extend(_line(item, role) for item in page.items)
                    if len(lines) > SELECTION.maximum_events * len(MAPS):
                        raise ValueError("unbounded book history")
                    if page.next_cursor is None:
                        break
                    if page.next_cursor == cursor:
                        raise ValueError("nonprogressing book cursor")
                    cursor = page.next_cursor
            lines.sort(key=lambda line: (line.event_time_utc, line.projection.received_ts_utc,
                                         line.projection.ingestion_sequence,
                                         next(i for i, role in enumerate(ROLES)
                                              if role[0] == line.raw_signal_id)))
            value = _produce(req, tuple(lines), parent, now)
        except (ValueError, TypeError, ArithmeticError):
            return None
        return cast(f.BookDepthOccurrenceV1, self.state.append(value))


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                predecessor: f.MeasurementWindowReadsV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementBookDepthOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D131 owner")
    if (type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now)
        or not callable(getattr(predecessor, "get_derived_occurrence", None))):
        raise TypeError("actual predecessor reader and storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, predecessor, now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.MeasurementBookDepthReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D131 reader")
    return _Reads(RecordState(storage, _decode, _validate))
