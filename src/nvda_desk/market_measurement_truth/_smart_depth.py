"""Controlled four-field positional SMART depth, initially D134 bid top two."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime, timedelta
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState

BRIEF = "628cddf853ab1c074a8b89264533714d7211a83618704742b2435b02121ac336"
NAMESPACE = "neutral_market_measurement_truth/smart-depth/v1"
SUBJECT = "NVDA"
T = datetime.fromisoformat("2026-10-20T12:40:00+00:00")
CUTOFF = T + timedelta(seconds=1)
PROVIDER, VARIANT = "foundation-controlled-smart-book", "positional_four_field_v1"
GENERATION = "controlled-smart-four-field-generation/1"
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d134-smart-four-field", 1), PROVIDER, VARIANT,
    GENERATION, T - timedelta(seconds=10), 100,
)
ROLES = (
    ("R185", "position", "book_position"), ("R187", "operation", "book_operation"),
    ("R188", "side", "book_side"), ("R190", "size", "shares"),
)
IDENTITY = (("generation.id", ("generation", "id")),
            ("event.id", ("event", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d134-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), PROVIDER, VARIANT,
    ("book", field), unit, IDENTITY,
) for raw, field, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d134-" + raw.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for raw, _, unit in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D134", "D134-SMART-TOP-TWO-BID-1", "K02_ALGEBRA",
    "sum(top two standing SMART bid sizes after positional replay)",
    tuple(raw for raw, _, _ in ROLES), (), "P_BASIC", "shares", "scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*item) for item in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d134-top-two", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)


def request() -> f.SmartDepthRequestV1:
    return f.SmartDepthRequestV1(
        f.CalculationRequestV1(
            "D134", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
            tuple(f.RawInputBindingV1(
                raw, f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(unit.context_id, 1), SUBJECT,
            ) for (raw, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
        ), SELECTION, 2,
    )


def _request(value: f.SmartDepthRequestV1, now: datetime) -> None:
    f._utc(now)
    if type(value) is not f.SmartDepthRequestV1 or canonical(value) != canonical(request()) \
            or now < CUTOFF:
        raise ValueError("unadmitted D134 book selection")


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
        raise ValueError("ineligible typed four-field SMART projection")
    f._utc(item.received_ts_utc)
    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
    f._utc(event)
    if not SELECTION.history_complete_from_utc <= event <= min(T, item.received_ts_utc):
        raise ValueError("ineligible native book instant")
    if role == 0 and item.native_value < 0:
        raise ValueError("negative book position")
    if role == 1 and item.native_value not in (0, 1, 2, 317):
        raise ValueError("unmapped book operation")
    if role == 2 and item.native_value not in (0, 1):
        raise ValueError("unmapped book side")
    if role == 3 and (not cast(Decimal, item.native_value).is_finite()
                      or item.native_value < 0):
        raise ValueError("invalid book size")
    return f.BookRawLineageV1(
        raw, item.observation_occurrence_id.value, f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(unit.context_id, 1), item, item.native_value, event,
    )


def _replay(lines: tuple[f.BookRawLineageV1, ...]
            ) -> tuple[f.SmartSizeRowV1, ...]:
    groups: dict[str, dict[str, f.BookRawLineageV1]] = {}
    for line in lines:
        role = next((i for i, spec in enumerate(ROLES) if spec[0] == line.raw_signal_id), -1)
        if role < 0 or canonical(line) != canonical(_line(line.projection, role)):
            raise ValueError("unmatched native book lineage")
        group = groups.setdefault(line.observation_occurrence_id, {})
        if line.raw_signal_id in group:
            raise ValueError("duplicate native role")
        group[line.raw_signal_id] = line
    if not groups or len(groups) > SELECTION.maximum_events:
        raise ValueError("missing or unbounded book events")
    ordered = sorted(groups.values(), key=lambda group: (
        next(iter(group.values())).projection.received_ts_utc,
        next(iter(group.values())).projection.ingestion_sequence,
    ))
    sides: dict[int, list[f.SmartSizeRowV1]] = {0: [], 1: []}
    warm: set[int] = set()
    prior: tuple[datetime, int] | None = None
    for group in ordered:
        if "R187" not in group:
            raise ValueError("required native operation missing")
        first = group["R187"]
        key = (first.projection.received_ts_utc, first.projection.ingestion_sequence)
        if prior is not None and key <= prior:
            raise ValueError("ambiguous receipt/ingestion ordering")
        prior = key
        if any((line.event_time_utc != first.event_time_utc
                or line.projection.received_ts_utc != key[0]
                or line.projection.ingestion_sequence != key[1]
                or line.projection.selection_identity != first.projection.selection_identity)
               for line in group.values()):
            raise ValueError("mixed native occurrence group")
        operation = cast(int, first.canonical_value)
        if operation == 317:
            if set(group) != {"R187"}:
                raise ValueError("reset must be operation-only")
            sides = {0: [], 1: []}
            warm.clear()
            continue
        if set(group) != {"R185", "R187", "R188", "R190"}:
            raise ValueError("partial positional mutation")
        side = cast(int, group["R188"].canonical_value)
        position = cast(int, group["R185"].canonical_value)
        size = cast(Decimal, group["R190"].canonical_value)
        rows = sides[side]
        if operation == 0:
            if position > len(rows) or size <= 0:
                raise ValueError("invalid insertion")
            rows.insert(position, f.SmartSizeRowV1(side, position, size))
        elif operation == 1:
            if position >= len(rows) or size <= 0:
                raise ValueError("update without standing position")
            rows[position] = f.SmartSizeRowV1(side, position, size)
        else:
            if position >= len(rows) or size != 0:
                raise ValueError("delete without standing position")
            del rows[position]
        rows[:] = [replace(row, position=i) for i, row in enumerate(rows)]
        warm.add(side)
    if warm != {0, 1} or any(len(sides[side]) < 2 for side in (0, 1)):
        raise ValueError("incomplete two-side top-two book warm-up")
    return tuple((*sides[0], *sides[1]))


def _produce(req: f.SmartDepthRequestV1, lines: tuple[f.BookRawLineageV1, ...],
             now: datetime) -> f.SmartDepthOccurrenceV1:
    _request(req, now)
    standing = _replay(lines)
    bid = tuple(row for row in standing if row.side == 0 and row.position < req.depth_levels)
    if len(bid) != 2:
        raise ValueError("incomplete selected bid levels")
    depth = sum((row.size for row in bid), Decimal(0))
    value = f.SmartDepthOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D134", "pending", req, DEFINITION, PARAMETER,
        UNITS, MAPS, lines, standing, depth, "shares", "scalar_decimal", T, CUTOFF, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return replace(value, derived_occurrence_id="mmtsmart1:" +
                   hashlib.sha256(canonical(payload)).hexdigest())


def _validate(value: f.SmartDepthOccurrenceV1) -> None:
    if type(value) is not f.SmartDepthOccurrenceV1:
        raise TypeError("exact SMART depth occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(value.request, value.raw_input_lineage,
                                              value.calculated_at_utc)):
        raise ValueError("SMART source/state/result/identity mismatch")


def _decode(payload: bytes) -> f.SmartDepthOccurrenceV1:
    return cast(f.SmartDepthOccurrenceV1, decode(payload, f.SmartDepthOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.SmartDepthOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty SMART occurrence identity required")
        return next((v for v in self.state.all()
                     if v.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(self, *, derived_signal_id: str, subject_instrument: str,
                             effective_at_or_before_utc: datetime,
                             knowledge_at_or_before_utc: datetime, limit: int
                             ) -> tuple[f.SmartDepthOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid SMART history query")
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

    def materialise(self, req: f.SmartDepthRequestV1) -> f.SmartDepthOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            _request(req, now)
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
                        raise ValueError("unbounded SMART history")
                    if page.next_cursor is None:
                        break
                    if page.next_cursor == cursor:
                        raise ValueError("nonprogressing SMART cursor")
                    cursor = page.next_cursor
            lines.sort(key=lambda line: (line.projection.received_ts_utc,
                                         line.projection.ingestion_sequence,
                                         next(i for i, spec in enumerate(ROLES)
                                              if spec[0] == line.raw_signal_id)))
            value = _produce(req, tuple(lines), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.SmartDepthOccurrenceV1, self.state.append(value))


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementSmartDepthOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D134 owner")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact SMART storage and clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.MeasurementSmartDepthReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D134 reader")
    return _Reads(RecordState(storage, _decode, _validate))
