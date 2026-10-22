"""Exact named VWAP deviation/rate over public source-role history."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._log_return import UNIT
from ._record_store import RecordState
from ._selection import _same_content, eligible
from ._session_returns import CONTEXT, S
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEFS = {
    "D027": "6c4a8b6a4451ddfa6b555e9f1b02d659af269ec0788e8ebc15b8ddf9528796bf",
    "D026": "a2f3fc76cd2cc846fd4885d4f3d3df7a1a3e5c7370700a613ecb0706c853412f",
}
VWAP = r.RawSignalProjectionMappingV1(
    "mmt-session-provider-vwap",
    1,
    r.RawSignalCatalogueId("R137"),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    ("vwap", "value"),
    "price",
    (("session", ("vwap", "session")), ("as_of", ("vwap", "as_of")), ("basis", ("vwap", "basis"))),
)
LAST = r.RawSignalProjectionMappingV1(
    "mmt-current-last",
    1,
    r.RawSignalCatalogueId("R037"),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    ("trade", "last"),
    "price",
    (("session", ("session", "id")),),
)


def configuration(
    identity: str,
) -> tuple[
    f.CalculationDefinitionV1,
    f.CalculationParameterSetV1,
    f.InputSelectionPolicyVersionV1,
    tuple[r.RawSignalProjectionMappingV1, ...],
]:
    if identity not in BRIEFS:
        raise ValueError("unadmitted VWAP calculation")
    definition = f.CalculationDefinitionV1(
        identity,
        "D027-VWAP-RATE-1" if identity == "D027" else "D026-VWAP-DEVIATION-1",
        "K03_CHANGE_RETURN",
        "(vwap_t-vwap_ref)/elapsed_minutes; 100*(vwap_t/vwap_ref-1)/elapsed_minutes"
        if identity == "D027"
        else "last-vwap; 100*(last/vwap-1)",
        ("R137",) if identity == "D027" else ("R037", "R137"),
        (),
        "P_WINDOW",
        "price/minute / percent/minute" if identity == "D027" else "price / percent",
        "named_exact_vwap_rate" if identity == "D027" else "named_exact_vwap_deviation",
        tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
    )
    name = "mmt-vwap-rate-300s" if identity == "D027" else "mmt-vwap-deviation"
    param = f.CalculationParameterSetV1(name, 1, "P_WINDOW", "NVDA", ("NVDA",))
    policy = f.InputSelectionPolicyVersionV1(
        name + "-selection",
        1,
        ("subject_instrument", "session"),
        timedelta(seconds=60),
        timedelta(0),
        ("true_instant",),
        (),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        "foundation-pilot-fixture/cash_quote_v1",
        100,
        1000,
    )
    return definition, param, policy, (VWAP,) if identity == "D027" else (LAST, VWAP)


def history(
    raw: f.RawProjectionReaderV1,
    c: f.CalculationRequestV1,
    mapping: r.RawSignalProjectionMappingV1,
    policy: f.InputSelectionPolicyVersionV1,
) -> tuple[r.ProjectedRawValueV1, ...]:
    cursor: str | None = None
    cursors: set[str] = set()
    seen: dict[str, r.ProjectedRawValueV1] = {}
    for _ in range(policy.history_page_limit):
        page = raw.list_projected_raw_history(
            mapping.raw_signal_catalogue_id,
            mappings=(mapping,),
            subject_instrument=c.subject_instrument,
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
            raise ValueError("incomplete history")
        for item in page.items:
            if type(item) is not r.ProjectedRawValueV1 or type(
                item.observation_occurrence_id
            ) is not type(r.observation_occurrence_id("id")):
                raise ValueError("malformed history identity")
            identity = item.observation_occurrence_id.value
            if identity in seen and not _same_content(seen[identity], item):
                raise ValueError("conflicting duplicate")
            seen[identity] = item
        cursor = page.next_cursor
        if cursor is None:
            return tuple(seen.values())
        if (
            type(cursor) is not str
            or not re.fullmatch(r"[1-9][0-9]*", cursor)
            or cursor in cursors
            or not page.items
        ):
            raise ValueError("incomplete paging")
        cursors.add(cursor)
    raise ValueError("history bound exhausted")


def chosen(lines: tuple[f.RawInputLineageV1, ...]) -> f.RawInputLineageV1:
    if not lines:
        raise ValueError("missing eligible role")

    def rank(line: f.RawInputLineageV1) -> tuple[datetime, datetime, int]:
        return (
            line.event_time_utc,
            line.projection.received_ts_utc,
            line.projection.ingestion_sequence,
        )

    value = max(lines, key=rank)
    if sum(rank(v) == rank(value) for v in lines) != 1:
        raise ValueError("ambiguous source rank")
    return value


def line(
    item: r.ProjectedRawValueV1,
    c: f.CalculationRequestV1,
    mapping: r.RawSignalProjectionMappingV1,
    policy: f.InputSelectionPolicyVersionV1,
) -> f.RawInputLineageV1:
    if type(item.source_timestamp_raw) is not str:
        raise ValueError("native UTC source time required")
    event = eligible(replace(item, selection_identity=None), mapping, policy, c)
    expected = (
        (("session", S),)
        if mapping == LAST
        else (("session", S), ("as_of", item.source_timestamp_raw), ("basis", "cumulative_session"))
    )
    if (
        event is None
        or item.selection_identity != r.RawSelectionIdentityV1(expected)
        or type(item.native_value) is not Decimal
        or item.native_value < 0
        or event < CONTEXT.session_start_utc
    ):
        raise ValueError("incompatible native VWAP role")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(UNIT.context_id, 1),
        item,
        item.native_value,
        event,
    )


def select(
    raw: f.RawProjectionReaderV1,
    c: f.CalculationRequestV1,
    mapping: r.RawSignalProjectionMappingV1,
    policy: f.InputSelectionPolicyVersionV1,
) -> f.RawInputLineageV1:
    lines = []
    for item in history(raw, c, mapping, policy):
        try:
            lines.append(line(item, c, mapping, policy))
        except (TypeError, ValueError):
            continue
    return chosen(tuple(lines))


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    definition, param, policy, maps = configuration(c.derived_signal_id)
    expected = f.CalculationRequestV1(
        c.derived_signal_id,
        "NVDA",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        definition.calculation_definition_version,
        f.VersionRefV1(param.context_id, 1),
        f.VersionRefV1(policy.context_id, 1),
        (CONTEXT.ref,),
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
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or not CONTEXT.session_start_utc <= c.as_of_utc < CONTEXT.session_end_utc
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
    ):
        raise ValueError("incompatible VWAP request")


def produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    c = request.calculation
    definition, param, policy, maps = configuration(c.derived_signal_id)
    if len(lines) != 2:
        raise ValueError("complete VWAP source pair required")

    rate = c.derived_signal_id == "D027"
    checks = (
        (
            (lines[0], VWAP, c),
            (lines[1], VWAP, replace(c, as_of_utc=c.as_of_utc - timedelta(seconds=300))),
        )
        if rate
        else tuple((v, m, c) for v, m in zip(lines, maps, strict=True))
    )
    for selected, mapping, anchor in checks:
        if canonical(selected) != canonical(line(selected.projection, anchor, mapping, policy)):
            raise ValueError("incompatible source snapshot")
    if lines[0].event_time_utc != c.as_of_utc or (
        not rate and lines[1].event_time_utc != c.as_of_utc
    ):
        raise ValueError("exact current snapshot required")
    last, vwap = (Fraction(v.canonical_value) for v in lines)
    if vwap <= 0:
        raise ValueError("zero VWAP denominator")
    seconds = (
        int((lines[0].event_time_utc - lines[1].event_time_utc).total_seconds())
        if rate
        else int((c.as_of_utc - CONTEXT.session_start_utc).total_seconds())
    )
    if seconds <= 0:
        raise ValueError("positive elapsed time required")
    divisor = Fraction(seconds, 60) if rate else Fraction(1)
    diff, pct = (last - vwap) / divisor, 100 * (last / vwap - 1) / divisor
    carrier = f.VwapRateV1 if rate else f.VwapDeviationV1
    result = carrier(
        f.ExactRatioV1(diff.numerator, diff.denominator),
        f.ExactRatioV1(pct.numerator, pct.denominator),
    )
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEFS[c.derived_signal_id],
        c.derived_signal_id,
        "pending",
        request,
        definition,
        param,
        policy,
        (UNIT,),
        maps,
        lines,
        (),
        seconds,
        result,
        definition.units,
        definition.result_shape,
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact window occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(
        produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
    ):
        raise ValueError("VWAP result/metadata/identity mismatch")


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        validate(value)
        if value.implementation_brief_sha256 != admission.implementation_brief_sha256:
            raise ValueError("wrong owner admission")

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
            raise TypeError("exact request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            if BRIEFS[c.derived_signal_id] != self.admission.implementation_brief_sha256:
                return None
            _, _, policy, maps = configuration(c.derived_signal_id)
            lines = (
                (
                    select(self.raw, c, VWAP, policy),
                    select(
                        self.raw,
                        replace(c, as_of_utc=c.as_of_utc - timedelta(seconds=300)),
                        VWAP,
                        policy,
                    ),
                )
                if c.derived_signal_id == "D027"
                else tuple(select(self.raw, c, m, policy) for m in maps)
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
        raise ValueError("exact VWAP owner admission required")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("declared raw-only dependencies required")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
