"""D104 exact rotation of four genuine native-right matched skew occurrences."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta
from fractions import Fraction
from typing import cast

from . import _option_skew as skew
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._option_scalars import CONTEXT, PROVIDER, VARIANT, T
from ._record_store import RecordState
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "a4a08441eddcc44ec5def45ccce81f9a1f5e426fa08c43e6691ef67b77658cc9"
A = T - timedelta(seconds=300)
MEMBERS = tuple(f"controlled-skew-2026-10-23-{tag}"
                for tag in ("C25", "P25", "C10", "P10"))
PARAMETER = f.CalculationParameterSetV1("mmt-d104-controlled", 1, "P_WINDOW",
                                         "NVDA_SKEW_E1", MEMBERS)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d104-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=300), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D104", "D104-SKEW-ROTATION-5M-1", "K03_CHANGE_RETURN",
    "(D100_current-D099_current)-(D100_prior-D099_prior)",
    (), ("D099", "D100"), "P_WINDOW", "volatility_points", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D104", "NVDA_SKEW_E1", T, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), (),
    )
    if (canonical(request.calculation) != canonical(expected) or request.context != CONTEXT
        or len(request.predecessor_occurrence_ids) != 4
        or len(set(request.predecessor_occurrence_ids)) != 4
        or now < expected.knowledge_cutoff_utc
        or not CONTEXT.history_complete_from_utc <= A):
        raise ValueError("incompatible exact skew rotation request")


def parent_check(p: f.WindowMeasurementOccurrenceV1, signal: str,
                 anchor: datetime, now: datetime) -> Fraction:
    if signal == "D099":
        skew.validate(p)
    elif signal == "D100":
        skew.validate_d100(p)
    else:
        raise ValueError("unknown skew family")
    c = p.request.calculation
    if (p.derived_signal_id != signal
        or p.implementation_brief_sha256 != (skew.BRIEF if signal == "D099"
                                                 else skew.BRIEF_D100)
        or c.subject_instrument != "NVDA_SKEW_2026-10-23"
        or c.as_of_utc != anchor or p.effective_as_of_utc != anchor
        or c.knowledge_cutoff_utc != T + timedelta(seconds=1)
        or p.knowledge_cutoff_utc != c.knowledge_cutoff_utc
        or p.request.context != CONTEXT or p.calculated_at_utc > now
        or p.units != "volatility_points" or p.result_shape != "option_skew"
        or p.projection_mappings != skew.MAPS or p.unit_conventions != skew.UNITS
        or p.parameter_set.members != tuple(MEMBERS[:2] if signal == "D099"
                                                else MEMBERS[2:])
        or type(p.result) is not f.OptionSkewV1
        or len(p.raw_input_lineage) != 4
        or len(p.result.native_right_lineage) != 2):
        raise ValueError("incompatible actual E1 skew family/expiry/anchor/source")
    return Fraction(p.result.value.numerator, p.result.value.denominator)


def produce(request: f.WindowCalculationRequestV1,
            parents: tuple[f.WindowMeasurementOccurrenceV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if (len(parents) != 4 or tuple(p.derived_occurrence_id for p in parents)
        != request.predecessor_occurrence_ids):
        raise ValueError("four actual ordered predecessor identities required")
    values = tuple(parent_check(p, signal, anchor, now)
                   for p, signal, anchor in zip(
                       parents, ("D099", "D100", "D099", "D100"),
                       (A, A, T, T), strict=True,
                   ))
    p25, p10, c25, c10 = values
    rotation = (c10 - c25) - (p10 - p25)
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D104", "pending", request, DEFINITION,
        PARAMETER, POLICY, skew.UNITS, skew.MAPS,
        tuple(line for parent in parents for line in parent.raw_input_lineage),
        parents, 300, f.ExactRatioV1(rotation.numerator, rotation.denominator),
        "volatility_points", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact rotation occurrence required")
    f._Validated.__post_init__(value)
    if any(type(p) is not f.WindowMeasurementOccurrenceV1 for p in value.predecessors):
        raise ValueError("actual window skew predecessors required")
    parents = cast(tuple[f.WindowMeasurementOccurrenceV1, ...], value.predecessors)
    if canonical(value) != canonical(produce(value.request, parents, value.calculated_at_utc)):
        raise ValueError("rotation source/result/identity mismatch")


def selected(history: tuple[f.WindowMeasurementOccurrenceV1, ...],
             signal: str, anchor: datetime, now: datetime
             ) -> f.WindowMeasurementOccurrenceV1:
    candidates = []
    for p in history:
        if type(p) is not f.WindowMeasurementOccurrenceV1:
            raise TypeError("exact public predecessor history required")
        if p.effective_as_of_utc <= anchor:
            parent_check(p, signal, p.effective_as_of_utc, now)
            candidates.append(p)
    if not candidates:
        raise ValueError("missing comparable skew family history")
    def rank(p: f.WindowMeasurementOccurrenceV1) -> tuple[datetime, datetime]:
        return p.effective_as_of_utc, p.calculated_at_utc
    choice = max(candidates, key=rank)
    if (choice.effective_as_of_utc != anchor
        or sum(rank(p) == rank(choice) for p in candidates) != 1):
        raise ValueError("missing exact anchor or ambiguous latest skew")
    return choice


class _Owner:
    def __init__(self, state: RecordState, predecessor: f.MeasurementWindowReadsV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.predecessor, self.now = state, predecessor, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact rotation request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            facts = tuple(self.predecessor.get_derived_occurrence(i)
                          for i in request.predecessor_occurrence_ids)
            if any(type(p) is not f.WindowMeasurementOccurrenceV1 for p in facts):
                raise ValueError("all four actual requested predecessors required")
            parents = cast(tuple[f.WindowMeasurementOccurrenceV1, ...], facts)
            # Validate each actual producer, including a lawful E2 producer, before own E1 join.
            for p, signal in zip(parents, ("D099", "D100", "D099", "D100"), strict=True):
                if signal == "D099":
                    skew.validate(p)
                else:
                    skew.validate_d100(p)
            for p, signal, anchor in zip(parents, ("D099", "D100", "D099", "D100"),
                                         (A, A, T, T), strict=True):
                parent_check(p, signal, anchor, now)
            selected_parents = []
            for anchor in (A, T):
                for signal in ("D099", "D100"):
                    page = self.predecessor.list_derived_history(
                        derived_signal_id=signal, subject_instrument="NVDA_SKEW_2026-10-23",
                        effective_at_or_before_utc=anchor,
                        knowledge_at_or_before_utc=request.calculation.knowledge_cutoff_utc,
                        limit=100,
                    )
                    if type(page) is not tuple or len(page) > 100:
                        raise ValueError("incomplete public skew history")
                    selected_parents.append(selected(page, signal, anchor, now))
            if (tuple(p.derived_occurrence_id for p in selected_parents)
                != request.predecessor_occurrence_ids):
                raise ValueError("requested skew facts are not latest comparable anchors")
            value = produce(request, parents, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D104 admission required")
    if (type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now)
        or predecessor is None
        or not callable(getattr(predecessor, "get_derived_occurrence", None))
        or not callable(getattr(predecessor, "list_derived_history", None))):
        raise TypeError("actual public skew read facet required")
    return _Owner(RecordState(storage, _decode, validate),
                  cast(f.MeasurementWindowReadsV1, predecessor), now)
