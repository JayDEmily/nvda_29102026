"""D101 complete exact 25D/50D two-sided smile curvature."""

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
from ._option_scalars import CONTEXT, PROVIDER, VARIANT, T
from ._option_skew import MAPS as SKEW_MAPS
from ._option_skew import UNITS as SKEW_UNITS
from ._option_skew import source_event
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "e2ce7083301088d963c64d427811aa0938c141d7805e7aee18359ae7b5ee4ba8"
TAGS = ("C25", "P25", "C50", "P50")
STRIKES = {"C25": "120", "P25": "100", "C50": "110", "P50": "110"}
DELTAS = {"C25": Decimal(".25"), "P25": Decimal("-.25"),
          "C50": Decimal(".50"), "P50": Decimal("-.50")}
E1 = "2026-10-23"
MEMBERS = tuple(f"controlled-skew-{E1}-{tag}" for tag in TAGS)
MAPS, UNITS = SKEW_MAPS[:2], SKEW_UNITS[:2]
PARAMETER = f.CalculationParameterSetV1("mmt-d101-controlled", 1, "P_BASIC",
                                         "NVDA_SMILE_E1", MEMBERS)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d101-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), MEMBERS,
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D101", "D101-SMILE-CURVATURE-1", "K02_ALGEBRA",
    "100*(put25_iv+call25_iv-2*(call50_iv+put50_iv)/2)",
    ("R111", "R112"), (), "P_BASIC", "volatility_points", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D101", "NVDA_SMILE_E1", T, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(UNITS[role].context_id, 1), member,
        ) for member in MEMBERS for role, mapping in enumerate(MAPS)),
    )
    if (canonical(request.calculation) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible exact smile request")


def identity(tag: str, member: str, role: int) -> r.RawSelectionIdentityV1:
    return r.RawSelectionIdentityV1((
        ("contract.id", member), ("underlying.id", "NVDA"),
        ("expiry.date", E1), ("strike.key", STRIKES[tag]),
        ("option.right", tag[0]), ("currency.code", "USD"),
        ("contract.multiplier", "100"), ("instrument.kind", "option"),
        ("model.convention", "controlled-model/1"),
        ("value.role", "model_iv" if role == 0 else "model_delta"),
    ))


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
         tag: str, member: str, role: int) -> f.RawInputLineageV1:
    mapping = MAPS[role]
    event = eligible(replace(item, selection_identity=None), mapping, POLICY,
                     replace(c, subject_instrument=member))
    if (event != T or source_event(item) != T or item.received_ts_utc != T
        or item.selection_identity != identity(tag, member, role)
        or type(item.native_value) is not Decimal):
        raise ValueError("matched exact smile IV/delta source required")
    number = cast(Decimal, item.native_value)
    if (role == 0 and number < 0) or (role == 1 and number != DELTAS[tag]):
        raise ValueError("nonnegative IV and exact signed native delta required")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNITS[role].context_id, 1),
        item, number, event,
    )


def choose(items: tuple[r.ProjectedRawValueV1, ...]) -> r.ProjectedRawValueV1:
    if not items:
        raise ValueError("missing exact smile source role")
    def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
        return source_event(item), item.received_ts_utc, item.ingestion_sequence
    selected = max(items, key=rank)
    if sum(rank(item) == rank(selected) for item in items) != 1:
        raise ValueError("ambiguous smile source rank")
    return selected


def produce(request: f.WindowCalculationRequestV1,
            lines: tuple[f.RawInputLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 8:
        raise ValueError("complete two-sided 25D and 50D grid required")
    for i, (tag, member) in enumerate(zip(TAGS, MEMBERS, strict=True)):
        for role in range(2):
            actual = lines[i * 2 + role]
            if type(actual) is not f.RawInputLineageV1 or canonical(actual) != canonical(
                line(actual.projection, request.calculation, tag, member, role)
            ):
                raise ValueError("smile role/lineage mismatch")
    c25, p25, c50, p50 = (Fraction(lines[i].canonical_value) for i in (0, 2, 4, 6))
    atm = (c50 + p50) / 2
    curvature = 100 * (p25 + c25 - 2 * atm)
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D101", "pending", request, DEFINITION,
        PARAMETER, POLICY, UNITS, MAPS, lines, (), 0,
        f.ExactRatioV1(curvature.numerator, curvature.denominator),
        "volatility_points", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact smile occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                             value.calculated_at_utc)):
        raise ValueError("smile result/source/identity mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact smile request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            lines = []
            for tag, member in zip(TAGS, MEMBERS, strict=True):
                for role, mapping in enumerate(MAPS):
                    member_request = replace(request.calculation, subject_instrument=member)
                    candidates = tuple(history(self.raw, member_request, mapping, POLICY))
                    selected = choose(tuple(item for item in candidates
                        if item.selection_identity == identity(tag, member, role)
                        and source_event(item) == T
                    ))
                    lines.append(line(selected, request.calculation, tag, member, role))
            result = produce(request, tuple(lines), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(result))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D101 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
