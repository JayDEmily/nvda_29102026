"""D010 delivered-live eligibility under explicit calendar, state and liquid phase."""
from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _temporal, _temporal_date, _temporal_local, _temporal_phase
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState
from ._selection import _same_content

BRIEF = "8eead9ba80813cd82244ce076af7a18fdef121474c0dd15a346aee814e892a98"
NAMESPACE = "neutral_market_measurement_truth/market-open/v1"
T = _temporal.T
MODE_MAP = r.RawSignalProjectionMappingV1(
    "mmt-d010-r005", 1, r.RawSignalCatalogueId("R005"), _temporal.PROVIDER,
    _temporal.VARIANT, ("market", "delivered_mode"), "marketDataType_enum",
    (*_temporal.META, ("requested.mode", ("requested", "mode")),
     ("generation.id", ("generation", "id"))),
)
MODE_UNIT = f.UnitConventionVersionV1(
    "mmt-d010-mode", 1, "marketDataType_enum", "delivered_mode", Decimal(1), Decimal(0),
)
MAPS = (MODE_MAP, *_temporal_date.MAPS)
UNITS = (MODE_UNIT, *_temporal_date.UNITS)
DEFINITION = f.CalculationDefinitionV1(
    "D010", "D010-LIVE-OPEN-LIQUID-1", "K01_TIME",
    "eligible live source AND known open calendar AND configured liquid phase",
    ("R005", "R023", "R024"), ("D003",), "P_TIME", "boolean", "market_open",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-d010-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d010-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    _temporal.PROVIDER, _temporal.VARIANT,
    _temporal.PROVIDER + "/" + _temporal.VARIANT, 100, 1000,
)
MODE_POLICY = f.DeliveredModePolicyV1(
    f.VersionRefV1("controlled-delivered-mode", 1), "live", 1, "controlled-stream/1",
)
OPEN_STATE = f.MarketStatePolicyV1(
    f.VersionRefV1("controlled-market-state", 1), f.VersionRefV1("controlled-overnight", 1),
    (date(2026, 10, 10),), (),
)
UNKNOWN_STATE = f.MarketStatePolicyV1(
    f.VersionRefV1("controlled-market-state", 2), f.VersionRefV1("controlled-overnight", 1),
    (), (),
)
CLOSED_STATE = f.MarketStatePolicyV1(
    f.VersionRefV1("controlled-market-state", 3), f.VersionRefV1("controlled-overnight", 1),
    (), (date(2026, 10, 10),),
)


def _request(request: f.MarketOpenRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D010", "NVDA", T, T, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (request.mode_policy.ref, request.calendar_policy.ref, request.phase_policy.ref,
         request.market_state_policy.ref),
        tuple(f.RawInputBindingV1(
            m.raw_signal_catalogue_id.value, f.VersionRefV1(m.mapping_id, 1),
            f.VersionRefV1(u.context_id, 1), "NVDA",
        ) for m, u in zip(MAPS, UNITS, strict=True)),
    )
    f._utc(now)
    if (type(request) is not f.MarketOpenRequestV1
        or canonical(c) != canonical(expected) or now < T
        or type(request.predecessor_occurrence_id) is not str
        or not request.predecessor_occurrence_id or request.mode_policy != MODE_POLICY
        or request.calendar_policy != _temporal_date._calendar(False)
        or request.phase_policy != _temporal_phase._phases(False)
        or request.market_state_policy not in (OPEN_STATE, UNKNOWN_STATE, CLOSED_STATE)
        or request.market_state_policy.calendar_ref != request.calendar_policy.ref
        or request.phase_policy.calendar_ref != request.calendar_policy.ref
        or request.liquid_phases != ("overnight",)):
        raise ValueError("unadmitted D010 mode/calendar/phase/state request")


def _mode_line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1
               ) -> f.MarketModeRawLineageV1:
    identity = r.RawSelectionIdentityV1((
        ("generation.id", MODE_POLICY.generation_id), ("requested.mode", "live"),
        ("sample.id", "controlled-temporal-sample/1"),
        ("value.role", "delivered_market_mode"),
    ))
    if (type(item) is not r.ProjectedRawValueV1
        or item.raw_signal_catalogue_id != MODE_MAP.raw_signal_catalogue_id
        or item.projection_mapping_id != MODE_MAP.mapping_id
        or item.projection_mapping_version != 1
        or item.native_field_path != MODE_MAP.native_field_path
        or item.native_units != MODE_MAP.native_units
        or item.source_provider != _temporal.PROVIDER
        or item.source_variant != _temporal.VARIANT
        or item.subject_instrument != "NVDA" or item.selection_identity != identity
        or item.ingestion_sequence_scope.value != POLICY.ingestion_sequence_scope
        or type(item.ingestion_sequence) is not int or item.ingestion_sequence <= 0
        or item.revision_vintage_native is not None
        or type(item.native_value) is not int
        or item.native_value != MODE_POLICY.live_delivered_code
        or item.source_temporal_kind != "true_instant"
        or item.source_timezone_native != "UTC"
        or item.received_ts_utc > c.knowledge_cutoff_utc):
        raise ValueError("R005 does not certify delivered live source")
    f._utc(item.received_ts_utc)
    event = _temporal._stamp(str(item.source_timestamp_raw)).astimezone(UTC)
    if (event > c.as_of_utc or event > item.received_ts_utc
        or c.as_of_utc - event > POLICY.maximum_staleness):
        raise ValueError("ineligible delivered mode event")
    return f.MarketModeRawLineageV1(
        "R005", item.observation_occurrence_id.value,
        f.VersionRefV1(MODE_MAP.mapping_id, 1), f.VersionRefV1(MODE_UNIT.context_id, 1),
        item, item.native_value, event,
    )


def _produce(request: f.MarketOpenRequestV1, mode: f.MarketModeRawLineageV1,
             lines: tuple[f.TemporalCalendarRawLineageV1, ...],
             predecessor: f.TemporalLocalOccurrenceV1, now: datetime
             ) -> f.MarketOpenOccurrenceV1:
    _request(request, now)
    c = request.calculation
    if canonical(mode) != canonical(_mode_line(mode.projection, c)) or len(lines) != 2 or any(
        canonical(line) != canonical(_temporal_date._line(line.projection, n, c))
        for n, line in enumerate(lines)
    ):
        raise ValueError("exact D010 projected lineages required")
    _temporal_local._validate(predecessor)
    parent_identity = predecessor.raw_input_lineage.projection.selection_identity
    all_lines = (mode, *lines)
    if (predecessor.derived_occurrence_id != request.predecessor_occurrence_id
        or predecessor.implementation_brief_sha256 != _temporal_local.BRIEF
        or predecessor.request.calculation.subject_instrument != c.subject_instrument
        or predecessor.request.calculation.as_of_utc != c.as_of_utc
        or predecessor.knowledge_cutoff_utc != c.knowledge_cutoff_utc
        or predecessor.calculated_at_utc > now or parent_identity is None
        or any(line.projection.selection_identity is None
               or line.projection.selection_identity.value_for("sample.id")
               != parent_identity.value_for("sample.id") for line in all_lines)
        or any(line.event_time_utc != predecessor.result.astimezone(UTC)
               or line.projection.received_ts_utc
               != predecessor.raw_input_lineage.projection.received_ts_utc for line in all_lines)
        or lines[0].canonical_value != "overnight/1"
        or lines[1].canonical_value != "controlled-overnight/1"):
        raise ValueError("D010 actual predecessor/raw occurrence mismatch")
    moment = predecessor.result.astimezone(UTC)
    calendar = request.calendar_policy
    if not calendar.coverage_start_utc <= moment < calendar.coverage_end_utc:
        raise ValueError("outside complete calendar")
    sessions = tuple(i for i in calendar.intervals if i.start_utc <= moment < i.end_utc)
    if len(sessions) != 1 or sessions[0].session_id != lines[0].canonical_value:
        raise ValueError("named calendar session absent")
    local_date = predecessor.result.date()
    state = request.market_state_policy
    if local_date not in state.open_dates and local_date not in state.closed_dates:
        raise ValueError("market open state unknown")
    phases = tuple(i for i in request.phase_policy.intervals if i.start_utc <= moment < i.end_utc)
    if len(phases) != 1:
        raise ValueError("phase unknown")
    result = local_date in state.open_dates and phases[0].phase in request.liquid_phases
    value = f.MarketOpenOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D010", "pending", request, DEFINITION,
        PARAMETER, POLICY, UNITS, MAPS, mode, lines, predecessor,
        request.mode_policy, calendar, request.phase_policy, state, request.liquid_phases,
        result, "boolean", "market_open", c.as_of_utc, c.knowledge_cutoff_utc, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in {"derived_occurrence_id", "calculated_at_utc"}}
    return replace(value, derived_occurrence_id="mmtopen1:" + hashlib.sha256(
        canonical(payload)).hexdigest())


def _validate(value: f.MarketOpenOccurrenceV1) -> None:
    if type(value) is not f.MarketOpenOccurrenceV1:
        raise TypeError("exact D010 record required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.delivered_mode_lineage, value.calendar_lineage,
        value.predecessor, value.calculated_at_utc,
    )):
        raise ValueError("D010 stored source/state mismatch")


def _decode(payload: bytes) -> f.MarketOpenOccurrenceV1:
    value = cast(f.MarketOpenOccurrenceV1, decode(payload, f.MarketOpenOccurrenceV1))
    parent = value.predecessor
    zone = _temporal_local._zone(parent.raw_input_lineage.canonical_value)
    return replace(value, predecessor=replace(parent, result=parent.result.astimezone(zone)))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.MarketOpenOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty derived identity required")
        return next((v for v in self.state.all()
                     if v.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.MarketOpenOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid D010 history query")
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
                 predecessor: f.MeasurementTemporalLocalReadsV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.predecessor, self.now = state, raw, predecessor, now
        self.reads = _Reads(state)

    def materialise(self, request: f.MarketOpenRequestV1
                    ) -> f.MarketOpenOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            _request(request, now)
            lines: list[f.MarketModeRawLineageV1 | f.TemporalCalendarRawLineageV1] = []
            for role, mapping in enumerate(MAPS):
                cursor: str | None = None
                cursors: set[str] = set()
                items: dict[str, r.ProjectedRawValueV1] = {}
                for _ in range(POLICY.history_page_limit):
                    page = self.raw.list_projected_raw_history(
                        mapping.raw_signal_catalogue_id, mappings=(mapping,),
                        subject_instrument="NVDA", received_at_or_before_utc=T,
                        event_at_or_before_utc=None, limit=POLICY.history_page_size, cursor=cursor,
                    )
                    if (type(page) is not r.ProjectedRawHistoryPageV1
                        or type(page.items) is not tuple):
                        raise ValueError("invalid D010 source page")
                    for item in page.items:
                        key = item.observation_occurrence_id.value
                        if key in items and not _same_content(items[key], item):
                            raise ValueError("conflicting D010 source identity")
                        items[key] = item
                    cursor = page.next_cursor
                    if cursor is None:
                        break
                    if type(cursor) is not str or cursor in cursors or not page.items:
                        raise ValueError("invalid D010 source cursor")
                    cursors.add(cursor)
                else:
                    raise ValueError("incomplete D010 source history")
                if role == 0:
                    identity = r.RawSelectionIdentityV1((
                        ("generation.id", MODE_POLICY.generation_id), ("requested.mode", "live"),
                        ("sample.id", "controlled-temporal-sample/1"),
                        ("value.role", "delivered_market_mode"),
                    ))
                else:
                    identity = r.RawSelectionIdentityV1((
                        ("sample.id", "controlled-temporal-sample/1"),
                        ("value.role", ("session_identity", "calendar_identity")[role - 1]),
                    ))
                candidates = tuple(i for i in items.values() if i.selection_identity == identity)
                if not candidates:
                    raise ValueError("missing D010 source role")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, int]:
                    return item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(i) == rank(chosen) for i in candidates) != 1:
                    raise ValueError("ambiguous D010 source role")
                lines.append(_mode_line(chosen, request.calculation) if role == 0
                             else _temporal_date._line(chosen, role - 1, request.calculation))
            predecessor = self.predecessor.get_derived_occurrence(request.predecessor_occurrence_id)
            if type(predecessor) is not f.TemporalLocalOccurrenceV1:
                raise ValueError("actual D003 missing")
            mode = cast(f.MarketModeRawLineageV1, lines[0])
            calendar_lines = cast(tuple[f.TemporalCalendarRawLineageV1, ...], tuple(lines[1:]))
            value = _produce(request, mode, calendar_lines, predecessor, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.MarketOpenOccurrenceV1, self.state.append(value))


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                predecessor: f.MeasurementTemporalLocalReadsV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementMarketOpenOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D010 owner")
    if (type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now)
        or any(not callable(getattr(predecessor, method, None))
               for method in ("get_derived_occurrence", "list_derived_history"))):
        raise TypeError("actual D003 reader and exact storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, predecessor, now)


def build_reader(admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
                 ) -> f.MeasurementMarketOpenReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D010 reader")
    return _Reads(RecordState(storage, _decode, _validate))
