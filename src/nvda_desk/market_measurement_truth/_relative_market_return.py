"""Exact technology minus broad return from compatible actual owning facts."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from . import _underlying_returns as underlying
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._record_store import RecordState
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "2a4691f906f558becf06d9993a7bfb48384e6847b89a10ae90c1d3019ba3dd8c"
DEFINITION = f.CalculationDefinitionV1(
    "D076",
    "D076-RELATIVE-RETURN-1",
    "K02_ALGEBRA",
    "D072-D071",
    (),
    ("D072", "D071"),
    "P_BASIC",
    "return_spread",
    "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d076-controlled", 1, "P_BASIC", "US_TECH_VS_BROAD", ("QQQ", "SPY")
)
POLICY = replace(
    underlying.configuration("D072")[2],
    context_id="mmt-d076-selection",
    join_keys=("as_of_utc", "knowledge_cutoff_utc", "context", "return_convention"),
    basket_membership=("QQQ", "SPY"),
)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D076",
        "US_TECH_VS_BROAD",
        underlying.T,
        underlying.T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (underlying.CONTEXT.ref,),
        (),
    )
    if (
        canonical(request.calculation) != canonical(expected)
        or request.context != underlying.CONTEXT
        or len(request.predecessor_occurrence_ids) != 2
        or len(set(request.predecessor_occurrence_ids)) != 2
        or now < expected.knowledge_cutoff_utc
    ):
        raise ValueError("incompatible exact relative-return request")


def produce(
    request: f.WindowCalculationRequestV1,
    predecessors: tuple[f.WindowMeasurementOccurrenceV1, ...],
    now: datetime,
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if (
        len(predecessors) != 2
        or tuple(p.derived_occurrence_id for p in predecessors)
        != request.predecessor_occurrence_ids
    ):
        raise ValueError("actual ordered D072/D071 required")
    for p, identity, subject in zip(predecessors, ("D072", "D071"), PARAMETER.members, strict=True):
        underlying.validator(f.OwnerAdmissionV1("M02", underlying.BRIEFS[identity]))(p)
        if (
            p.derived_signal_id != identity
            or p.request.calculation.subject_instrument != subject
            or p.request.context != request.context
            or p.effective_as_of_utc != request.calculation.as_of_utc
            or p.knowledge_cutoff_utc != request.calculation.knowledge_cutoff_utc
            or p.calculated_at_utc > now
            or p.window_seconds != 85200
            or type(p.result) is not Decimal
        ):
            raise ValueError("incompatible actual return snapshot/convention")
    difference = Fraction(cast(Decimal, predecessors[0].result)) - Fraction(
        cast(Decimal, predecessors[1].result)
    )
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D076",
        "pending",
        request,
        DEFINITION,
        PARAMETER,
        POLICY,
        (),
        (),
        (),
        predecessors,
        85200,
        f.ExactRatioV1(difference.numerator, difference.denominator),
        "return_spread",
        "exact_ratio",
        request.calculation.as_of_utc,
        request.calculation.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact relative-return occurrence required")
    f._Validated.__post_init__(value)
    if any(type(p) is not f.WindowMeasurementOccurrenceV1 for p in value.predecessors):
        raise ValueError("actual window predecessors required")
    predecessors = cast(tuple[f.WindowMeasurementOccurrenceV1, ...], value.predecessors)
    if canonical(value) != canonical(produce(value.request, predecessors, value.calculated_at_utc)):
        raise ValueError("relative result/metadata/lineage/identity mismatch")


class _Owner:
    def __init__(
        self,
        state: RecordState,
        predecessor: f.MeasurementWindowReadsV1,
        now: Callable[[], datetime],
    ) -> None:
        self.state, self.predecessor, self.now = state, predecessor, now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.WindowCalculationRequestV1
    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact relative request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            facts = tuple(
                self.predecessor.get_derived_occurrence(i)
                for i in request.predecessor_occurrence_ids
            )
            if any(type(p) is not f.WindowMeasurementOccurrenceV1 for p in facts):
                return None
            value = produce(request, cast(tuple[f.WindowMeasurementOccurrenceV1, ...], facts), now)
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
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D076 admission required")
    if (
        type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or predecessor is None
        or any(
            not callable(getattr(predecessor, method, None))
            for method in ("get_derived_occurrence", "list_derived_history")
        )
    ):
        raise TypeError("actual public window read facet required")
    return _Owner(
        RecordState(storage, _decode, validate), cast(f.MeasurementWindowReadsV1, predecessor), now
    )
