"""D005 versioned nonoverlapping phase selection under a complete calendar."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, datetime, timedelta
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _temporal, _temporal_date, _temporal_local
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState
from ._selection import _same_content

BRIEF = "07c01c3e34a1f93f4f004d67d01a05efe353eeeb9b26e6bb4165b1a8702383bb"
NAMESPACE = "neutral_market_measurement_truth/temporal-phase/v1"
T = _temporal.T
MAPS, UNITS = _temporal_date.MAPS, _temporal_date.UNITS
PROVIDER, VARIANT = _temporal.PROVIDER, _temporal.VARIANT
DEFINITION = f.CalculationDefinitionV1(
    "D005", "D005-ORDERED-SESSION-PHASE-1", "K01_TIME",
    "configured half-open ordered nonoverlapping local session phase",
    ("R023", "R024"), ("D003",), "P_TIME", "category", "session_phase",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-d005-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d005-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def _phases(refused: bool) -> f.PhasePolicyV1:
    bounds = tuple(datetime.fromisoformat(s).astimezone(UTC) for s in (
        "2026-10-10T00:00:00+11:00", "2026-10-10T06:00:00+11:00",
        "2026-10-10T16:00:00+11:00",
    ))
    intervals: tuple[f.PhaseIntervalV1, ...] = (f.PhaseIntervalV1(bounds[1], bounds[2], "day"),)
    if not refused:
        intervals = (f.PhaseIntervalV1(bounds[0], bounds[1], "overnight"), *intervals)
    return f.PhasePolicyV1(
        f.VersionRefV1("controlled-phases", 2 if refused else 1),
        f.VersionRefV1("controlled-overnight", 1), "Australia/Melbourne", intervals,
    )


def _request(request: f.TemporalPhaseRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D005", "NVDA", T, T, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (request.calendar_policy.ref, request.phase_policy.ref),
        tuple(f.RawInputBindingV1(
            m.raw_signal_catalogue_id.value, f.VersionRefV1(m.mapping_id, 1),
            f.VersionRefV1(u.context_id, 1), "NVDA",
        ) for m, u in zip(MAPS, UNITS, strict=True)),
    )
    f._utc(now)
    if (
        type(request) is not f.TemporalPhaseRequestV1
        or canonical(c) != canonical(expected)
        or type(request.predecessor_occurrence_id) is not str
        or not request.predecessor_occurrence_id or now < T
        or request.calendar_policy != _temporal_date._calendar(False)
        or request.phase_policy not in (_phases(False), _phases(True))
        or request.phase_policy.calendar_ref != request.calendar_policy.ref
        or request.phase_policy.iana_zone != request.calendar_policy.iana_zone
    ):
        raise ValueError("unadmitted D005 calendar/phase request")
    _temporal_local._zone(request.phase_policy.iana_zone)


def _produce(
    request: f.TemporalPhaseRequestV1,
    lines: tuple[f.TemporalCalendarRawLineageV1, ...],
    predecessor: f.TemporalLocalOccurrenceV1, now: datetime,
) -> f.TemporalPhaseOccurrenceV1:
    _request(request, now)
    c = request.calculation
    if len(lines) != 2 or any(canonical(line) != canonical(
        _temporal_date._line(line.projection, role, c)
    ) for role, line in enumerate(lines)):
        raise ValueError("both actual calendar fields required")
    _temporal_local._validate(predecessor)
    parent_identity = predecessor.raw_input_lineage.projection.selection_identity
    if (
        predecessor.derived_occurrence_id != request.predecessor_occurrence_id
        or predecessor.implementation_brief_sha256 != _temporal_local.BRIEF
        or predecessor.request.calculation.subject_instrument != c.subject_instrument
        or predecessor.request.calculation.as_of_utc != c.as_of_utc
        or predecessor.knowledge_cutoff_utc != c.knowledge_cutoff_utc
        or predecessor.calculated_at_utc > now
        or parent_identity is None
        or any(line.projection.selection_identity is None
               or line.projection.selection_identity.value_for("sample.id")
               != parent_identity.value_for("sample.id") for line in lines)
        or any(line.event_time_utc != predecessor.result.astimezone(UTC)
               or line.projection.received_ts_utc
               != predecessor.raw_input_lineage.projection.received_ts_utc for line in lines)
        or lines[1].canonical_value != "controlled-overnight/1"
        or lines[0].canonical_value != "overnight/1"
    ):
        raise ValueError("actual D003 and exact calendar source mismatch")
    moment = predecessor.result.astimezone(UTC)
    calendar = request.calendar_policy
    if not calendar.coverage_start_utc <= moment < calendar.coverage_end_utc:
        raise ValueError("outside complete calendar coverage")
    sessions = tuple(i for i in calendar.intervals if i.start_utc <= moment < i.end_utc)
    if len(sessions) != 1 or sessions[0].session_id != lines[0].canonical_value:
        raise ValueError("not inside the projected named open session")
    matches = tuple(i for i in request.phase_policy.intervals if i.start_utc <= moment < i.end_utc)
    if len(matches) != 1:
        raise ValueError("configured phase absent")
    result = matches[0].phase
    value = f.TemporalPhaseOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D005", "pending", request, DEFINITION,
        PARAMETER, POLICY, UNITS, MAPS, lines, predecessor, calendar,
        request.phase_policy, result, "category", "session_phase",
        c.as_of_utc, c.knowledge_cutoff_utc, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in {"derived_occurrence_id", "calculated_at_utc"}}
    return replace(value, derived_occurrence_id="mmtphase1:" + hashlib.sha256(
        canonical(payload)
    ).hexdigest())


def _validate(value: f.TemporalPhaseOccurrenceV1) -> None:
    if type(value) is not f.TemporalPhaseOccurrenceV1:
        raise TypeError("exact D005 phase record required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.predecessor, value.calculated_at_utc,
    )):
        raise ValueError("D005 phase/source/predecessor mismatch")


def _decode(payload: bytes) -> f.TemporalPhaseOccurrenceV1:
    value = cast(f.TemporalPhaseOccurrenceV1, decode(payload, f.TemporalPhaseOccurrenceV1))
    parent = value.predecessor
    zone = _temporal_local._zone(parent.raw_input_lineage.canonical_value)
    return replace(value, predecessor=replace(parent, result=parent.result.astimezone(zone)))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.TemporalPhaseOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty derived identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.TemporalPhaseOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid D005 history query")
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

    def materialise(self, request: f.TemporalPhaseRequestV1
                    ) -> f.TemporalPhaseOccurrenceV1 | None:
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
                    if (type(page) is not r.ProjectedRawHistoryPageV1
                        or type(page.items) is not tuple):
                        raise ValueError("invalid D005 source page")
                    for item in page.items:
                        key = item.observation_occurrence_id.value
                        if key in items and not _same_content(items[key], item):
                            raise ValueError("conflicting D005 source identity")
                        items[key] = item
                    cursor = page.next_cursor
                    if cursor is None:
                        break
                    if type(cursor) is not str or cursor in cursors or not page.items:
                        raise ValueError("invalid D005 source cursor")
                    cursors.add(cursor)
                else:
                    raise ValueError("incomplete D005 source history")
                identity = r.RawSelectionIdentityV1((
                    ("sample.id", "controlled-temporal-sample/1"),
                    ("value.role", ("session_identity", "calendar_identity")[role]),
                ))
                candidates = tuple(i for i in items.values() if i.selection_identity == identity)
                if not candidates:
                    raise ValueError("missing calendar source role")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, int]:
                    return item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(i) == rank(chosen) for i in candidates) != 1:
                    raise ValueError("ambiguous calendar role")
                lines.append(_temporal_date._line(chosen, role, request.calculation))
            predecessor = self.predecessor.get_derived_occurrence(request.predecessor_occurrence_id)
            if type(predecessor) is not f.TemporalLocalOccurrenceV1:
                raise ValueError("actual D003 missing")
            value = _produce(request, tuple(lines), predecessor, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.TemporalPhaseOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTemporalLocalReadsV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementTemporalPhaseOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D005 owner")
    if (type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or any(not callable(getattr(predecessor, method, None))
               for method in ("get_derived_occurrence", "list_derived_history"))):
        raise TypeError("actual D003 reader and exact storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, predecessor, now)


def build_reader(admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
                 ) -> f.MeasurementTemporalPhaseReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D005 reader")
    return _Reads(RecordState(storage, _decode, _validate))
