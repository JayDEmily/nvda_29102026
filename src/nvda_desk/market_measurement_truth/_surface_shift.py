"""D103 exact complete two-contract five-minute model-IV surface shift."""

from __future__ import annotations

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
from ._option_scalars import CONTEXT, META, PROVIDER, VARIANT, T
from ._option_skew import source_event
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "8fe8a0081907ca543c7bb94765cedac48cfcc2335d724384c3d9dfe77bbef45d"
A = T - timedelta(seconds=300)
MEMBERS = ("controlled-skew-2026-10-23-C25", "controlled-skew-2026-10-23-P25")
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r111-option", 1, r.RawSignalCatalogueId("R111"), PROVIDER, VARIANT,
    ("model", "iv"), "annualised_decimal_volatility", META,
)
UNIT = f.UnitConventionVersionV1(
    "mmt-option-iv", 1, "annualised_decimal_volatility",
    "annualised_decimal_volatility", Decimal(1), Decimal(0),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d103-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=300), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d103-controlled", 1, "P_WINDOW",
                                         "NVDA_SURFACE_E1", MEMBERS)
DEFINITION = f.CalculationDefinitionV1(
    "D103", "D103-MATCHED-SURFACE-SHIFT-5M-1", "K03_CHANGE_RETURN",
    "100*mean(member_iv_current-member_iv_reference)", ("R111",), (),
    "P_WINDOW", "volatility_points", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D103", "NVDA_SURFACE_E1", T, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), tuple(f.RawInputBindingV1(
            "R111", f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), member,
        ) for member in MEMBERS),
    )
    if (canonical(request.calculation) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids or now < expected.knowledge_cutoff_utc
        or not CONTEXT.history_complete_from_utc <= A):
        raise ValueError("incompatible complete surface request")


def identity(tag: str, member: str) -> r.RawSelectionIdentityV1:
    return r.RawSelectionIdentityV1((
        ("contract.id", member), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"),
        ("strike.key", "120" if tag == "C25" else "100"),
        ("option.right", tag[0]), ("currency.code", "USD"),
        ("contract.multiplier", "100"), ("instrument.kind", "option"),
        ("model.convention", "controlled-model/1"), ("value.role", "model_iv"),
    ))


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
         tag: str, member: str, anchor: datetime) -> f.RawInputLineageV1:
    own = replace(c, subject_instrument=member)
    event = eligible(replace(item, selection_identity=None), MAPPING, POLICY, own)
    if (event != anchor or source_event(item) != anchor
        or item.received_ts_utc != anchor
        or item.selection_identity != identity(tag, member)
        or type(item.native_value) is not Decimal or item.native_value < 0):
        raise ValueError("exact selected surface snapshot source required")
    return f.RawInputLineageV1(
        "R111", item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), anchor,
    )


def choose(items: tuple[r.ProjectedRawValueV1, ...]) -> r.ProjectedRawValueV1:
    if not items:
        raise ValueError("missing member of complete surface grid")
    def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
        return source_event(item), item.received_ts_utc, item.ingestion_sequence
    selected = max(items, key=rank)
    if sum(rank(item) == rank(selected) for item in items) != 1:
        raise ValueError("ambiguous surface source rank")
    return selected


def produce(request: f.WindowCalculationRequestV1,
            lines: tuple[f.RawInputLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 4:
        raise ValueError("two members at both exact anchors required")
    for i, anchor in enumerate((T, A)):
        for j, (tag, member) in enumerate(zip(("C25", "P25"), MEMBERS, strict=True)):
            actual = lines[2 * i + j]
            if (type(actual) is not f.RawInputLineageV1
                or canonical(actual) != canonical(line(
                    actual.projection, request.calculation, tag, member, anchor
                ))):
                raise ValueError("surface member/anchor/source lineage mismatch")
    changes = (Fraction(lines[i].canonical_value) - Fraction(lines[i + 2].canonical_value)
               for i in range(2))
    shift = 100 * sum(changes, Fraction(0)) / 2
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D103", "pending", request, DEFINITION,
        PARAMETER, POLICY, (UNIT,), (MAPPING,), lines, (), 300,
        f.ExactRatioV1(shift.numerator, shift.denominator),
        "volatility_points", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact surface shift occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                             value.calculated_at_utc)):
        raise ValueError("surface shift/source/identity mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact surface request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            selected = []
            for anchor in (T, A):
                for tag, member in zip(("C25", "P25"), MEMBERS, strict=True):
                    own = replace(request.calculation, subject_instrument=member)
                    candidates = tuple(history(self.raw, own, MAPPING, POLICY))
                    eligible_candidates = tuple(item for item in candidates
                        if item.selection_identity == identity(tag, member)
                        and source_event(item) == anchor
                        and eligible(replace(item, selection_identity=None), MAPPING,
                                     POLICY, own) == anchor)
                    actual = choose(eligible_candidates)
                    selected.append(line(actual, request.calculation, tag, member, anchor))
            result = produce(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(result))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D103 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
