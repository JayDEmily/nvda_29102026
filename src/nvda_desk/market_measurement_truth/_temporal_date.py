"""D004 controlled complete overnight trading-date assignment."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _temporal, _temporal_local
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState
from ._selection import _same_content

BRIEF = "94ac73562afcbb34af75cd9cd72c7b94783ecb4c4d857beecc7690340d61b495"
NAMESPACE = "neutral_market_measurement_truth/temporal-date/v1"
T = _temporal.T
PROVIDER, VARIANT = _temporal.PROVIDER, _temporal.VARIANT
MAPS = (
    r.RawSignalProjectionMappingV1(
        "mmt-d004-r023", 1, r.RawSignalCatalogueId("R023"), PROVIDER,
        VARIANT, ("calendar", "session"), "session_identity", _temporal.META,
    ),
    r.RawSignalProjectionMappingV1(
        "mmt-d004-r024", 1, r.RawSignalCatalogueId("R024"), PROVIDER,
        VARIANT, ("calendar", "identity"), "calendar_identity", _temporal.META,
    ),
)
UNITS = (
    f.UnitConventionVersionV1(
        "mmt-d004-session", 1, "session_identity", "session_identity", Decimal(1), Decimal(0),
    ),
    f.UnitConventionVersionV1(
        "mmt-d004-calendar", 1, "calendar_identity", "calendar_identity",
        Decimal(1), Decimal(0),
    ),
)
DEFINITION = f.CalculationDefinitionV1(
    "D004", "D004-OVERNIGHT-TRADING-DATE-1", "K01_TIME",
    "configured session trading date, including overnight attribution",
    ("R023", "R024"), ("D003",), "P_TIME", "date", "exchange_trading_date",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-d004-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d004-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def _calendar(refused: bool) -> f.CalendarPolicyV1:
    boundaries = tuple(datetime.fromisoformat(s).astimezone(UTC) for s in (
        "2026-10-09T00:00:00+11:00", "2026-10-09T16:00:00+11:00",
        "2026-10-10T06:00:00+11:00", "2026-10-10T16:00:00+11:00",
        "2026-10-11T00:00:00+11:00",
    ))
    return f.CalendarPolicyV1(
        f.VersionRefV1("controlled-overnight", 2 if refused else 1),
        "Australia/Melbourne", boundaries[0], boundaries[-1],
        (f.CalendarIntervalV1(boundaries[0], boundaries[1], "closed", None),
         f.CalendarIntervalV1(boundaries[1], boundaries[2],
                              "closed" if refused else "overnight/1",
                              None if refused else date(2026, 10, 9)),
         f.CalendarIntervalV1(boundaries[2], boundaries[3], "day/1", date(2026, 10, 10)),
         f.CalendarIntervalV1(boundaries[3], boundaries[4], "closed", None)),
    )


def _request(request: f.TemporalDateRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D004", "NVDA", T, T, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (request.calendar_policy.ref,),
        tuple(f.RawInputBindingV1(
            m.raw_signal_catalogue_id.value, f.VersionRefV1(m.mapping_id, 1),
            f.VersionRefV1(u.context_id, 1), "NVDA",
        ) for m, u in zip(MAPS, UNITS, strict=True)),
    )
    f._utc(now)
    if (
        type(request) is not f.TemporalDateRequestV1
        or canonical(c) != canonical(expected)
        or type(request.predecessor_occurrence_id) is not str
        or not request.predecessor_occurrence_id or now < T
        or request.calendar_policy not in (_calendar(False), _calendar(True))
    ):
        raise ValueError("unadmitted complete D004 calendar/request")
    _temporal_local._zone(request.calendar_policy.iana_zone)


def _line(item: r.ProjectedRawValueV1, role: int, c: f.CalculationRequestV1
          ) -> f.TemporalCalendarRawLineageV1:
    m, u = MAPS[role], UNITS[role]
    identity = r.RawSelectionIdentityV1((
        ("sample.id", "controlled-temporal-sample/1"),
        ("value.role", ("session_identity", "calendar_identity")[role]),
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
        or item.source_temporal_kind != "true_instant"
        or item.source_timezone_native != "UTC"
        or item.received_ts_utc > c.knowledge_cutoff_utc
        or item.native_value != ("overnight/1", "controlled-overnight/1")[role]
    ):
        raise ValueError("unadmitted R023/R024 native source")
    f._utc(item.received_ts_utc)
    event = _temporal._stamp(str(item.source_timestamp_raw)).astimezone(UTC)
    if (event > c.as_of_utc or event > item.received_ts_utc
        or c.as_of_utc - event > POLICY.maximum_staleness):
        raise ValueError("future or stale calendar source event")
    return f.TemporalCalendarRawLineageV1(
        m.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(m.mapping_id, 1), f.VersionRefV1(u.context_id, 1),
        item, item.native_value, event,
    )


def _produce(
    request: f.TemporalDateRequestV1, lines: tuple[f.TemporalCalendarRawLineageV1, ...],
    predecessor: f.TemporalLocalOccurrenceV1, now: datetime,
) -> f.TemporalDateOccurrenceV1:
    _request(request, now)
    c = request.calculation
    if len(lines) != 2 or any(canonical(line) != canonical(_line(line.projection, n, c))
                                  for n, line in enumerate(lines)):
        raise ValueError("both exact native calendar fields required")
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
    ):
        raise ValueError("actual D003/calendar occurrence mismatch")
    moment = predecessor.result.astimezone(UTC)
    policy = request.calendar_policy
    if not policy.coverage_start_utc <= moment < policy.coverage_end_utc:
        raise ValueError("instant outside complete calendar coverage")
    selected = tuple(i for i in policy.intervals if i.start_utc <= moment < i.end_utc)
    if len(selected) != 1 or selected[0].session_id != lines[0].canonical_value:
        raise ValueError("no applicable named trading session")
    trading_date = selected[0].trading_date
    if type(trading_date) is not date:
        raise ValueError("closed session cannot assign trading date")
    value = f.TemporalDateOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D004", "pending", request, DEFINITION,
        PARAMETER, POLICY, UNITS, MAPS, lines, predecessor, policy, trading_date,
        "date", "exchange_trading_date", c.as_of_utc, c.knowledge_cutoff_utc, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in {"derived_occurrence_id", "calculated_at_utc"}}
    return replace(value, derived_occurrence_id="mmtdate1:" + hashlib.sha256(
        canonical(payload)
    ).hexdigest())


def _validate(value: f.TemporalDateOccurrenceV1) -> None:
    if type(value) is not f.TemporalDateOccurrenceV1:
        raise TypeError("exact D004 date record required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.predecessor, value.calculated_at_utc,
    )):
        raise ValueError("D004 date/source/session mismatch")


def _decode(payload: bytes) -> f.TemporalDateOccurrenceV1:
    value = cast(f.TemporalDateOccurrenceV1, decode(payload, f.TemporalDateOccurrenceV1))
    parent = value.predecessor
    zone = _temporal_local._zone(parent.raw_input_lineage.canonical_value)
    return replace(value, predecessor=replace(parent, result=parent.result.astimezone(zone)))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.TemporalDateOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty derived identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.TemporalDateOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid D004 history query")
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

    def materialise(self, request: f.TemporalDateRequestV1
                    ) -> f.TemporalDateOccurrenceV1 | None:
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
                        raise ValueError("invalid D004 source page")
                    for item in page.items:
                        key = item.observation_occurrence_id.value
                        if key in items and not _same_content(items[key], item):
                            raise ValueError("conflicting D004 source identity")
                        items[key] = item
                    cursor = page.next_cursor
                    if cursor is None:
                        break
                    if type(cursor) is not str or cursor in cursors or not page.items:
                        raise ValueError("invalid D004 source cursor")
                    cursors.add(cursor)
                else:
                    raise ValueError("incomplete D004 source history")
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
                lines.append(_line(chosen, role, request.calculation))
            predecessor = self.predecessor.get_derived_occurrence(request.predecessor_occurrence_id)
            if type(predecessor) is not f.TemporalLocalOccurrenceV1:
                raise ValueError("actual D003 missing")
            value = _produce(request, tuple(lines), predecessor, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.TemporalDateOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTemporalLocalReadsV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementTemporalDateOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D004 owner")
    if (type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or any(not callable(getattr(predecessor, method, None))
               for method in ("get_derived_occurrence", "list_derived_history"))):
        raise TypeError("actual D003 reader and exact storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, predecessor, now)


def build_reader(admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
                 ) -> f.MeasurementTemporalDateReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D004 reader")
    return _Reads(RecordState(storage, _decode, _validate))
