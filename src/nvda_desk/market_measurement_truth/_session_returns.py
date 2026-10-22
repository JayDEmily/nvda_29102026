"""Controlled session roles with exact native identities and canonical log results."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._log_return import UNIT, _logarithm
from ._record_store import RecordState
from ._selection import _same_content, eligible
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEFS = {"D022": "831139cef8d7e18ffdfe970a6cf228d683dcbf98ffc3c3962c4d0e9c070878b8"}
S = "controlled-price-session/1"
PREV = "controlled-price-session-prev/1"
START = datetime(2026, 10, 20, 12, tzinfo=UTC)
END = datetime(2026, 10, 20, 13, tzinfo=UTC)
CONTEXT = f.WindowContextV1(f.VersionRefV1("controlled-price-session", 1), START, END, START)


def mapping(
    rid: str, mid: str, path: tuple[str, ...], extra: tuple[tuple[str, tuple[str, ...]], ...] = ()
) -> r.RawSignalProjectionMappingV1:
    return r.RawSignalProjectionMappingV1(
        mid,
        1,
        r.RawSignalCatalogueId(rid),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        path,
        "price",
        (("session", ("session", "id")), *extra),
    )


def configuration(
    identity: str,
) -> tuple[
    f.CalculationDefinitionV1,
    f.CalculationParameterSetV1,
    f.InputSelectionPolicyVersionV1,
    tuple[r.RawSignalProjectionMappingV1, ...],
    f.WindowContextV1,
]:
    if identity != "D022":
        raise ValueError("unadmitted session calculation")
    maps = (
        mapping("R043", "mmt-session-open", ("session", "open")),
        mapping("R037", "mmt-current-last", ("trade", "last")),
    )
    policy = f.InputSelectionPolicyVersionV1(
        "mmt-session-return-selection",
        1,
        ("subject_instrument", "session"),
        timedelta(hours=48),
        timedelta(0),
        ("true_instant",),
        (),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        "foundation-pilot-fixture/cash_quote_v1",
        100,
        1000,
    )
    definition = f.CalculationDefinitionV1(
        "D022",
        "D022-SESSION-RETURN-1",
        "K03_CHANGE_RETURN",
        "ln(current / session_open)",
        ("R043", "R037"),
        (),
        "P_WINDOW",
        "return",
        "scalar_decimal",
        tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
    )
    parameter = f.CalculationParameterSetV1(
        "mmt-session-return-50d-half-even", 1, "P_WINDOW", "NVDA", ("NVDA",)
    )
    return definition, parameter, policy, maps, CONTEXT


def lineage(
    item: r.ProjectedRawValueV1,
    c: f.CalculationRequestV1,
    mapping: r.RawSignalProjectionMappingV1,
    policy: f.InputSelectionPolicyVersionV1,
    identity: r.RawSelectionIdentityV1,
    event: datetime,
) -> f.RawInputLineageV1:
    if item.selection_identity != identity:
        raise ValueError("native session/phase/kind identity mismatch")
    actual = eligible(replace(item, selection_identity=None), mapping, policy, c)
    if actual != event or type(item.native_value) is not Decimal:
        raise ValueError("ineligible source role/event/value")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(UNIT.context_id, 1),
        item,
        item.native_value,
        actual,
    )


def select_line(
    raw: f.RawProjectionReaderV1,
    c: f.CalculationRequestV1,
    mapping: r.RawSignalProjectionMappingV1,
    policy: f.InputSelectionPolicyVersionV1,
    identity: r.RawSelectionIdentityV1,
    event: datetime,
) -> f.RawInputLineageV1:
    cursor: str | None = None
    cursors: set[str] = set()
    seen: dict[str, r.ProjectedRawValueV1] = {}
    candidates = []
    for _ in range(policy.history_page_limit):
        page = raw.list_projected_raw_history(
            mapping.raw_signal_catalogue_id,
            mappings=(mapping,),
            subject_instrument="NVDA",
            received_at_or_before_utc=c.knowledge_cutoff_utc,
            event_at_or_before_utc=c.as_of_utc,
            limit=policy.history_page_size,
            cursor=cursor,
        )
        if (
            type(page) is not r.ProjectedRawHistoryPageV1
            or type(page.items) is not tuple
            or len(page.items) > policy.history_page_size
        ):
            raise ValueError("incomplete provider history")
        for item in page.items:
            if type(item) is not r.ProjectedRawValueV1 or type(
                item.observation_occurrence_id
            ) is not type(r.observation_occurrence_id("id")):
                raise ValueError("invalid provider identity")
            occurrence_id = item.observation_occurrence_id.value
            if occurrence_id in seen:
                if not _same_content(seen[occurrence_id], item):
                    raise ValueError("conflicting provider record")
                continue
            seen[occurrence_id] = item
            try:
                candidates.append(lineage(item, c, mapping, policy, identity, event))
            except (TypeError, ValueError):
                continue
        cursor = page.next_cursor
        if cursor is None:
            break
        if (
            type(cursor) is not str
            or not re.fullmatch(r"[1-9][0-9]*", cursor)
            or cursor in cursors
            or not page.items
        ):
            raise ValueError("incomplete provider paging")
        cursors.add(cursor)
    else:
        raise ValueError("provider history bound exhausted")
    if not candidates:
        raise ValueError("no compatible provider value")

    def rank(line: f.RawInputLineageV1) -> tuple[datetime, datetime, int]:
        return (
            line.event_time_utc,
            line.projection.received_ts_utc,
            line.projection.ingestion_sequence,
        )

    chosen = max(candidates, key=rank)
    if sum(rank(line) == rank(chosen) for line in candidates) != 1:
        raise ValueError("ambiguous provider rank")
    return chosen


def roles(
    identity: str, c: f.CalculationRequestV1
) -> tuple[tuple[r.RawSelectionIdentityV1, datetime, timedelta], ...]:
    if identity != "D022":
        raise ValueError("unadmitted role profile")
    session = r.RawSelectionIdentityV1((("session", S),))
    return ((session, START, timedelta(hours=48)), (session, c.as_of_utc, timedelta(seconds=60)))


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    definition, parameter, policy, maps, context = configuration(c.derived_signal_id)
    expected = f.CalculationRequestV1(
        c.derived_signal_id,
        "NVDA",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        definition.calculation_definition_version,
        f.VersionRefV1(parameter.context_id, 1),
        f.VersionRefV1(policy.context_id, 1),
        (context.ref,),
        tuple(
            f.RawInputBindingV1(
                m.raw_signal_catalogue_id.value,
                f.VersionRefV1(m.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1),
                "NVDA",
            )
            for m in maps
        ),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != context
        or request.predecessor_occurrence_ids
        or not context.history_complete_from_utc
        <= context.session_start_utc
        <= c.as_of_utc
        < context.session_end_utc
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
    ):
        raise ValueError("incompatible session request/context")


def produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    c = request.calculation
    definition, parameter, policy, maps, _ = configuration(c.derived_signal_id)
    if len(lines) != 2:
        raise ValueError("complete session roles required")
    for line, m, (identity, event, freshness) in zip(
        lines, maps, roles(c.derived_signal_id, c), strict=True
    ):
        if (
            canonical(line)
            != canonical(
                lineage(
                    line.projection,
                    c,
                    m,
                    replace(policy, maximum_staleness=freshness),
                    identity,
                    event,
                )
            )
            or line.canonical_value <= 0
        ):
            raise ValueError("incompatible positive session price")
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEFS[c.derived_signal_id],
        c.derived_signal_id,
        "pending",
        request,
        definition,
        parameter,
        policy,
        (UNIT,),
        maps,
        lines,
        (),
        int((c.as_of_utc - lines[0].event_time_utc).total_seconds()),
        _logarithm(lines[1].canonical_value, lines[0].canonical_value),
        "return",
        "scalar_decimal",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(
        produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
    ):
        raise ValueError("session result/metadata/identity mismatch")


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        validate(value)
        if value.implementation_brief_sha256 != admission.implementation_brief_sha256:
            raise ValueError("different session owner admission")

    return check


class _Owner:
    def __init__(
        self,
        admission: f.OwnerAdmissionV1,
        state: RecordState,
        raw: f.RawProjectionReaderV1,
        now: Callable[[], datetime],
    ) -> None:
        self.admission, self.state, self.raw, self.now = admission, state, raw, now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.WindowCalculationRequestV1
    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact window request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            if BRIEFS[c.derived_signal_id] != self.admission.implementation_brief_sha256:
                return None
            _, _, policy, maps, _ = configuration(c.derived_signal_id)
            lines = tuple(
                select_line(
                    self.raw, c, m, replace(policy, maximum_staleness=freshness), identity, event
                )
                for m, (identity, event, freshness) in zip(
                    maps, roles(c.derived_signal_id, c), strict=True
                )
            )
            value = produce(request, lines, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1,
    raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if (
        type(admission) is not f.OwnerAdmissionV1
        or admission.object_id != "M02"
        or admission.implementation_brief_sha256 not in BRIEFS.values()
    ):
        raise ValueError("exact session admission required")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("declared raw-only session dependencies required")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
