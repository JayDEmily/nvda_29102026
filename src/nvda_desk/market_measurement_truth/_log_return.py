"""Fixed close anchors and independently bounded, correctly rounded logarithms."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._record_store import RecordState
from ._selection import eligible, select
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEFS = {
    "D019": "6affd5b55eb03007a23ae80a79bbd3d5665105d70b2e7e65c4050d29cf60c085",
    "D020": "811906fdfb073da9b5a7ba137563953d6ff977d50bfe99b8f43adb068f20e839",
}
HORIZONS = {"D019": 60, "D020": 300}
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-close-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-close-selection",
    1,
    ("subject_instrument",),
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
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-bar-close",
    1,
    r.RawSignalCatalogueId("R143"),
    POLICY.source_provider,
    POLICY.source_variant,
    ("bar", "close"),
    "price",
    (),
)
UNIT = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0"))


def _series(z: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    """For 0<=z<=1/3, bound 2*atanh(z) by partial sum and geometric tail."""
    partial = Fraction(0)
    power = z
    square = z * z
    for index in range(terms):
        partial += 2 * power / (2 * index + 1)
        power *= square
    remainder = 2 * power / ((2 * terms + 1) * (1 - square))
    return partial, partial + remainder


def _logarithm(current: Decimal, reference: Decimal) -> Decimal:
    ratio = Fraction(current) / Fraction(reference)
    if ratio == 1:
        return Decimal("0")
    power = ratio.numerator.bit_length() - ratio.denominator.bit_length()
    reduced = ratio / (Fraction(2) ** power)
    if reduced < 1:
        reduced *= 2
        power -= 1
    elif reduced >= 2:
        reduced /= 2
        power += 1
    z = (reduced - 1) / (reduced + 1)
    for terms in range(32, 513, 32):
        low, high = _series(z, terms)
        two_low, two_high = _series(Fraction(1, 3), terms)
        low += power * (two_low if power >= 0 else two_high)
        high += power * (two_high if power >= 0 else two_low)
        with localcontext(Context(prec=50, rounding=ROUND_HALF_EVEN)) as context:
            a = context.divide(Decimal(low.numerator), Decimal(low.denominator))
            b = context.divide(Decimal(high.numerator), Decimal(high.denominator))
        if a == b:
            return a
    raise ValueError("rational log bounds do not establish the admitted rounding")


def _configuration(identity: str) -> tuple[f.CalculationDefinitionV1, f.CalculationParameterSetV1]:
    seconds = HORIZONS[identity]
    return (
        f.CalculationDefinitionV1(
            identity,
            identity + "-LOG-RETURN-1",
            "K03_CHANGE_RETURN",
            "ln(close_t / close_reference)",
            ("R143",),
            (),
            "P_WINDOW",
            "return",
            "scalar_decimal",
            tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
        ),
        f.CalculationParameterSetV1(
            f"mmt-log-{seconds}s-50d-half-even", 1, "P_WINDOW", "NVDA", ("NVDA",)
        ),
    )


def _request(request: f.WindowCalculationRequestV1, now: datetime) -> int:
    c = request.calculation
    if c.derived_signal_id not in HORIZONS:
        raise ValueError("unadmitted log identity")
    definition, parameter = _configuration(c.derived_signal_id)
    seconds = HORIZONS[c.derived_signal_id]
    expected = f.CalculationRequestV1(
        c.derived_signal_id,
        "NVDA",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        definition.calculation_definition_version,
        f.VersionRefV1(parameter.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,),
        (
            f.RawInputBindingV1(
                "R143",
                f.VersionRefV1(MAPPING.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1),
                "NVDA",
            ),
        ),
    )
    anchor = c.as_of_utc - timedelta(seconds=seconds)
    if (
        canonical(c) != canonical(expected)
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or c.as_of_utc.second
        or c.as_of_utc.microsecond
        or not CONTEXT.history_complete_from_utc <= CONTEXT.session_start_utc <= anchor
        or not c.as_of_utc < CONTEXT.session_end_utc
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
    ):
        raise ValueError("unsupported close/anchor/session context")
    return seconds


def _lineage(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1) -> f.RawInputLineageV1:
    event = eligible(item, MAPPING, POLICY, c)
    if (
        event is None
        or event.second
        or event.microsecond
        or event < CONTEXT.session_start_utc
        or type(item.native_value) is not Decimal
        or item.native_value <= 0
    ):
        raise ValueError("ineligible positive aligned close")
    return f.RawInputLineageV1(
        "R143",
        item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1),
        f.VersionRefV1(UNIT.context_id, 1),
        item,
        item.native_value,
        event,
    )


def _produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    seconds = _request(request, now)
    if len(lines) != 2:
        raise ValueError("current/reference pair required")
    c = request.calculation
    if lines[0].event_time_utc != c.as_of_utc:
        raise ValueError("current close must equal as-of")
    for line, scoped in zip(
        lines, (c, replace(c, as_of_utc=c.as_of_utc - timedelta(seconds=seconds))), strict=True
    ):
        if canonical(line) != canonical(_lineage(line.projection, scoped)):
            raise ValueError("invalid anchored lineage")
    definition, parameter = _configuration(c.derived_signal_id)
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEFS[c.derived_signal_id],
        c.derived_signal_id,
        "pending",
        request,
        definition,
        parameter,
        POLICY,
        (UNIT,),
        (MAPPING,),
        lines,
        (),
        seconds,
        _logarithm(lines[0].canonical_value, lines[1].canonical_value),
        "return",
        "scalar_decimal",
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
        _produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
    ):
        raise ValueError("log metadata/equation/identity mismatch")


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        validate(value)
        if value.implementation_brief_sha256 != admission.implementation_brief_sha256:
            raise ValueError("different log owner admission")

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
            seconds = _request(request, now)
            if (
                BRIEFS[request.calculation.derived_signal_id]
                != self.admission.implementation_brief_sha256
            ):
                return None
            c = request.calculation
            lines = []
            for scoped in (c, replace(c, as_of_utc=c.as_of_utc - timedelta(seconds=seconds))):
                pair = select(self.raw, MAPPING, POLICY, scoped)
                if pair is None:
                    return None
                lines.append(_lineage(pair[0], scoped))
            value = _produce(request, tuple(lines), now)
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
        raise ValueError("exact fixed log admission required")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("declared raw-only log dependencies required")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
