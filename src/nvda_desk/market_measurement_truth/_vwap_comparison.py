"""D018 named exact comparison against a compatible actual D017 snapshot."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _session_vwap as v
from . import api as f
from ._evaluation import canonical
from ._record_store import RecordState
from ._selection import _same_content, eligible
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "1f65edb4e3050c89604c749accc5fdf39ff03e69e54eca43a50cfa496298e90e"
DEFINITION = replace(
    v.DEFINITION,
    derived_signal_id="D018",
    calculation_definition_version="D018-VWAP-COMPARISON-1",
    equation="provider_vwap - D017; 10000 * difference / D017",
    raw_dependencies=("R137",),
    derived_dependencies=("D017",),
    units="price / bps",
    result_shape="named_exact_comparison",
)
PARAMETER = replace(v.PARAMETER, context_id="mmt-vwap-comparison")
POLICY = replace(v.POLICY, context_id="mmt-comparison-selection")
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-provider-vwap",
    1,
    r.RawSignalCatalogueId("R137"),
    POLICY.source_provider,
    POLICY.source_variant,
    ("vwap", "value"),
    "price",
    (("session", ("vwap", "session")), ("as_of", ("vwap", "as_of"))),
)
UNIT = v.UNITS[0]


def _request(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D018",
        "NVDA",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (v.CONTEXT.ref,),
        (
            f.RawInputBindingV1(
                "R137",
                f.VersionRefV1(MAPPING.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1),
                "NVDA",
            ),
        ),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != v.CONTEXT
        or len(request.predecessor_occurrence_ids) != 1
        or not v.CONTEXT.session_start_utc <= c.as_of_utc < v.CONTEXT.session_end_utc
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
    ):
        raise ValueError("incompatible comparison context")


def _lineage(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1) -> f.RawInputLineageV1:
    expected = r.RawSelectionIdentityV1(
        (
            ("session", "controlled-vwap-session/1"),
            ("as_of", c.as_of_utc.isoformat().replace("+00:00", "Z")),
        )
    )
    if item.selection_identity != expected:
        raise ValueError("provider session/as-of identity mismatch")
    event = eligible(replace(item, selection_identity=None), MAPPING, POLICY, c)
    if event != c.as_of_utc or type(item.native_value) is not Decimal or item.native_value < 0:
        raise ValueError("ineligible provider VWAP")
    return f.RawInputLineageV1(
        "R137",
        item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1),
        f.VersionRefV1(UNIT.context_id, 1),
        item,
        item.native_value,
        event,
    )


def _select(raw: f.RawProjectionReaderV1, c: f.CalculationRequestV1) -> f.RawInputLineageV1:
    cursor: str | None = None
    cursors: set[str] = set()
    seen: dict[str, r.ProjectedRawValueV1] = {}
    candidates = []
    for _ in range(POLICY.history_page_limit):
        page = raw.list_projected_raw_history(
            MAPPING.raw_signal_catalogue_id,
            mappings=(MAPPING,),
            subject_instrument="NVDA",
            received_at_or_before_utc=c.knowledge_cutoff_utc,
            event_at_or_before_utc=c.as_of_utc,
            limit=POLICY.history_page_size,
            cursor=cursor,
        )
        if (
            type(page) is not r.ProjectedRawHistoryPageV1
            or type(page.items) is not tuple
            or len(page.items) > POLICY.history_page_size
        ):
            raise ValueError("incomplete provider history")
        for item in page.items:
            if type(item) is not r.ProjectedRawValueV1 or type(
                item.observation_occurrence_id
            ) is not type(r.observation_occurrence_id("id")):
                raise ValueError("invalid provider identity")
            identity = item.observation_occurrence_id.value
            if identity in seen:
                if not _same_content(seen[identity], item):
                    raise ValueError("conflicting provider record")
                continue
            seen[identity] = item
            try:
                candidates.append(_lineage(item, c))
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


def _produce(
    request: f.WindowCalculationRequestV1,
    line: f.RawInputLineageV1,
    predecessor: f.WindowMeasurementOccurrenceV1,
    now: datetime,
) -> f.WindowMeasurementOccurrenceV1:
    _request(request, now)
    v.validate(predecessor)
    c, pc = request.calculation, predecessor.request.calculation
    if (
        predecessor.derived_occurrence_id != request.predecessor_occurrence_ids[0]
        or predecessor.request.context != request.context
        or pc.as_of_utc != c.as_of_utc
        or pc.knowledge_cutoff_utc != c.knowledge_cutoff_utc
        or predecessor.calculated_at_utc > now
        or type(predecessor.result) is not f.ExactRatioV1
        or not predecessor.result.numerator
        or canonical(line) != canonical(_lineage(line.projection, c))
    ):
        raise ValueError("incompatible or zero actual VWAP predecessor")
    p = Fraction(predecessor.result.numerator, predecessor.result.denominator)
    difference = Fraction(line.canonical_value) - p
    bps = 10000 * difference / p
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D018",
        "pending",
        request,
        DEFINITION,
        PARAMETER,
        POLICY,
        (UNIT,),
        (MAPPING,),
        (line,),
        (predecessor,),
        predecessor.window_seconds,
        f.MeasurementComparisonV1(
            f.ExactRatioV1(difference.numerator, difference.denominator),
            f.ExactRatioV1(bps.numerator, bps.denominator),
        ),
        "price / bps",
        "named_exact_comparison",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact window occurrence required")
    f._Validated.__post_init__(value)
    if (
        len(value.raw_input_lineage) != 1
        or len(value.predecessors) != 1
        or type(value.predecessors[0]) is not f.WindowMeasurementOccurrenceV1
    ):
        raise ValueError("complete comparison inputs required")
    if canonical(value) != canonical(
        _produce(
            value.request,
            value.raw_input_lineage[0],
            value.predecessors[0],
            value.calculated_at_utc,
        )
    ):
        raise ValueError("comparison metadata/equation/identity mismatch")


class _Owner:
    def __init__(
        self,
        state: RecordState,
        raw: f.RawProjectionReaderV1,
        predecessor: f.MeasurementWindowReadsV1,
        now: Callable[[], datetime],
    ) -> None:
        self.state, self.raw, self.predecessor, self.now = state, raw, predecessor, now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.WindowCalculationRequestV1
    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact window request required")
        now = self.now()
        f._utc(now)
        try:
            _request(request, now)
            predecessor = self.predecessor.get_derived_occurrence(
                request.predecessor_occurrence_ids[0]
            )
            if type(predecessor) is not f.WindowMeasurementOccurrenceV1:
                return None
            value = _produce(request, _select(self.raw, request.calculation), predecessor, now)
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
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D018 admission required")
    if (
        type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
        or not callable(getattr(predecessor, "get_derived_occurrence", None))
    ):
        raise TypeError("declared comparison dependencies required")
    return _Owner(
        RecordState(storage, _decode, validate),
        raw,
        cast(f.MeasurementWindowReadsV1, predecessor),
        now,
    )
