"""Five exact return-rate fields from three actual compatible fixed-horizon facts."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from typing import cast

from . import _log_return as log
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._record_store import RecordState
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "7776047c140ed8e6fa76af66a772b4a8ffbf1088ce4681377243ec666ddc9885"
DEFINITION = f.CalculationDefinitionV1(
    "D024",
    "D024-RETURN-ACCELERATION-1",
    "K03_CHANGE_RETURN",
    "q1=D019/1; q5=D020/5; q30=D021/30; accel_1v5=q1-q5; accel_5v30=q5-q30",
    (),
    ("D019", "D020", "D021"),
    "P_WINDOW",
    "return/minute",
    "named_exact_acceleration",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-return-acceleration", 1, "P_WINDOW", "NVDA", ("NVDA",))
POLICY = replace(log.POLICY, context_id="mmt-return-acceleration-selection")


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D024",
        "NVDA",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (log.CONTEXT.ref,),
        (),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != log.CONTEXT
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
        or not log.CONTEXT.session_start_utc <= c.as_of_utc < log.CONTEXT.session_end_utc
        or len(set(request.predecessor_occurrence_ids)) != len(request.predecessor_occurrence_ids)
    ):
        raise ValueError("incompatible acceleration request")


def produce(
    request: f.WindowCalculationRequestV1,
    predecessors: tuple[f.WindowMeasurementOccurrenceV1, ...],
    now: datetime,
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if (
        len(predecessors) != 3
        or tuple(p.derived_occurrence_id for p in predecessors)
        != request.predecessor_occurrence_ids
    ):
        raise ValueError("three actual ordered horizons required")
    c = request.calculation
    rates = []
    for p, identity, minutes in zip(
        predecessors, ("D019", "D020", "D021"), (1, 5, 30), strict=True
    ):
        log.validate(p)
        pc = p.request.calculation
        if (
            p.derived_signal_id != identity
            or p.request.context != request.context
            or pc.subject_instrument != c.subject_instrument
            or pc.as_of_utc != c.as_of_utc
            or pc.knowledge_cutoff_utc != c.knowledge_cutoff_utc
            or p.calculated_at_utc > now
            or type(p.result) is not Decimal
            or canonical(p.raw_input_lineage[0]) != canonical(predecessors[0].raw_input_lineage[0])
        ):
            raise ValueError("incompatible actual fixed-horizon predecessor")
        rates.append(Fraction(p.result) / minutes)
    q1, q5, q30 = rates
    values = (q1, q5, q30, q1 - q5, q5 - q30)
    result = f.ReturnAccelerationV1(*(f.ExactRatioV1(x.numerator, x.denominator) for x in values))
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D024",
        "pending",
        request,
        DEFINITION,
        PARAMETER,
        POLICY,
        (log.UNIT,),
        (log.MAPPING,),
        tuple(
            {
                line.observation_occurrence_id: line
                for p in predecessors
                for line in p.raw_input_lineage
            }.values()
        ),
        predecessors,
        1800,
        result,
        "return/minute",
        "named_exact_acceleration",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact occurrence required")
    f._Validated.__post_init__(value)
    if any(type(p) is not f.WindowMeasurementOccurrenceV1 for p in value.predecessors):
        raise ValueError("actual window predecessors required")
    predecessors = cast(tuple[f.WindowMeasurementOccurrenceV1, ...], value.predecessors)
    if canonical(value) != canonical(produce(value.request, predecessors, value.calculated_at_utc)):
        raise ValueError("acceleration result/metadata/lineage/identity mismatch")


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
            raise TypeError("exact window request required")
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
        raise ValueError("exact D024 admission required")
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
