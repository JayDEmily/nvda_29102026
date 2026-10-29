"""Admitted instantaneous volatility relationships over the public M00 projection."""

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
from ._macro_changes import META, PROVIDER, SERIES, VARIANT, T, line
from ._record_store import RecordState
from ._vwap_returns import chosen, history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEFS = {
    "D060": "a43ea49957202b1401b9ccec0c8a9445894654a8b527976c0f0e7c7e97c4aebc",
    "D059": "1ce887da55b8afa021484defce4f39bf96a2b597573781fb32ba5435b4abcb26",
    "D058": "dd0d4c18be4ee9f88fb884931cd2b0c70b274099e68ba176d93c59b4c4ac4405",
    "D057": "c96b1fda3d4e2a97c839bc5669c441c21e1f9190d50472b20d0e8fd9ee067960",
}
PROFILES = {
    "D060": ("R237", "R236"),
    "D059": ("R236", "R240"),
    "D058": ("R239", "R236"),
    "D057": ("R238", "R239"),
}
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-volatility-terms", 1),
    T - timedelta(seconds=60),
    T + timedelta(seconds=1),
    T - timedelta(seconds=60),
)


def configuration(
    identity: str,
) -> tuple[
    f.CalculationDefinitionV1,
    f.CalculationParameterSetV1,
    f.InputSelectionPolicyVersionV1,
    tuple[r.RawSignalProjectionMappingV1, ...],
    tuple[f.UnitConventionVersionV1, ...],
]:
    if identity not in BRIEFS:
        raise ValueError("unadmitted volatility relationship")
    raw_ids = PROFILES[identity]
    scalar = identity == "D060"
    definition = f.CalculationDefinitionV1(
        identity,
        identity + ("-VOL-RATIO-1" if scalar else "-TERM-PAIR-1"),
        "K02_ALGEBRA",
        "first/second" if scalar else "first-second; first/second",
        raw_ids,
        (),
        "P_BASIC",
        "ratio" if scalar else "index_points / ratio",
        "exact_ratio" if scalar else "named_exact_term_pair",
        tuple(f.AuthorityArtifactRefV1(*item) for item in _AUTHORITY),
    )
    parameters = f.CalculationParameterSetV1(
        "mmt-" + identity.lower() + "-controlled", 1, "P_BASIC", "NVDA", ("NVDA",)
    )
    policy = f.InputSelectionPolicyVersionV1(
        "mmt-" + identity.lower() + "-selection",
        1,
        ("subject_instrument", "metric.series"),
        timedelta(seconds=60),
        timedelta(0),
        ("true_instant",),
        (),
        PROVIDER,
        VARIANT,
        PROVIDER + "/" + VARIANT,
        100,
        1000,
    )
    mappings = tuple(
        r.RawSignalProjectionMappingV1(
            "mmt-macro-" + raw.lower(),
            1,
            r.RawSignalCatalogueId(raw),
            PROVIDER,
            VARIANT,
            ("metric", "value"),
            SERIES[raw][1],
            META,
        )
        for raw in raw_ids
    )
    units = tuple(
        f.UnitConventionVersionV1(
            "mmt-macro-" + raw.lower() + "-units",
            1,
            SERIES[raw][1],
            SERIES[raw][1],
            Decimal("1"),
            Decimal("0"),
        )
        for raw in raw_ids
    )
    return definition, parameters, policy, mappings, units


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    definition, parameter, policy, mappings, units = configuration(c.derived_signal_id)
    expected = f.CalculationRequestV1(
        c.derived_signal_id,
        "NVDA",
        T,
        T + timedelta(seconds=1),
        definition.calculation_definition_version,
        f.VersionRefV1(parameter.context_id, 1),
        f.VersionRefV1(policy.context_id, 1),
        (CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                m.raw_signal_catalogue_id.value,
                f.VersionRefV1(m.mapping_id, 1),
                f.VersionRefV1(u.context_id, 1),
                "NVDA",
            )
            for m, u in zip(mappings, units, strict=True)
        ),
    )
    if (
        type(now) is not datetime
        or canonical(c) != canonical(expected)
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or c.knowledge_cutoff_utc > now
    ):
        raise ValueError("incompatible fixed volatility request")


def produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    if type(now) is not datetime:
        raise TypeError("exact UTC calculation instant required")
    request_check(request, now)
    c = request.calculation
    definition, parameters, policy, mappings, units = configuration(c.derived_signal_id)
    if len(lines) != 2:
        raise ValueError("two selected volatility roles required")
    for actual, mapping, unit in zip(lines, mappings, units, strict=True):
        if canonical(actual) != canonical(line(actual.projection, c, mapping, unit, policy)):
            raise ValueError("volatility lineage mismatch")
    if abs(lines[0].event_time_utc - lines[1].event_time_utc) > policy.maximum_skew:
        raise ValueError("volatility snapshot skew")
    first, second = (Fraction(item.canonical_value) for item in lines)
    if second == 0:
        raise ValueError("selected volatility denominator is zero")
    fraction = first / second
    ratio = f.ExactRatioV1(fraction.numerator, fraction.denominator)
    difference = first - second
    result = (
        ratio
        if c.derived_signal_id == "D060"
        else f.TermPairV1(f.ExactRatioV1(difference.numerator, difference.denominator), ratio)
    )
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEFS[c.derived_signal_id],
        c.derived_signal_id,
        "pending",
        request,
        definition,
        parameters,
        policy,
        units,
        mappings,
        lines,
        (),
        0,
        result,
        definition.units,
        definition.result_shape,
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        if type(value) is not f.WindowMeasurementOccurrenceV1:
            raise TypeError("exact volatility occurrence required")
        f._Validated.__post_init__(value)
        if admission.implementation_brief_sha256 != BRIEFS.get(
            value.derived_signal_id
        ) or canonical(value) != canonical(
            produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
        ):
            raise ValueError("immutable volatility calculation mismatch")

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
            raise TypeError("exact volatility request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            if BRIEFS[c.derived_signal_id] != self.admission.implementation_brief_sha256:
                return None
            _, _, policy, mappings, units = configuration(c.derived_signal_id)
            selected = []
            for mapping, unit in zip(mappings, units, strict=True):
                candidates = []
                for item in history(self.raw, c, mapping, policy):
                    try:
                        candidates.append(line(item, c, mapping, unit, policy))
                    except (TypeError, ValueError):
                        continue
                # Numerical denominator validation follows latest selection; never backfill zero.
                selected.append(chosen(tuple(candidates)))
            value = produce(request, tuple(selected), now)
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
        raise ValueError("exact admitted volatility owner required")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("volatility owner requires public M00 only")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
