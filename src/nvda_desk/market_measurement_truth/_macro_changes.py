"""Fixed controlled macro rate and change profiles over public M00."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import chosen, history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEFS: dict[str, str] = {
    "D046": "61a6320423ee32323d3cf375f484c7a345c678a9f190105b8cc372cf207f4544",
    "D045": "405914f63d83e66c109bd4f7a9bf03ef560ddef4b5becb66c5a111f00914254e",
    "D044": "eaab891044f59e22586039ca458b1fa33caac33df149f78e0aa656486b1f2de8",
    "D043": "2662f4e41370209a8c3fbe6b92116bd679d12a907716337080cfd2ffcf6666b7",
    "D042": "fd69f8a6f1c9f015ac2c01351c93fe9ea91d94730e1c0a43b47865a616e14bd3",
}
# raw dependencies, exact horizon days, arithmetic mode, definition label
PROFILES: dict[str, tuple[tuple[str, ...], int, str, str]] = {
    "D046": (("R255",), 5, "rate", "RATE-CHANGE"),
    "D045": (("R249",), 1, "rate", "RATE-CHANGE"),
    "D044": (("R252",), 1, "rate", "RATE-CHANGE"),
    "D043": (("R246", "R249"), 0, "slope", "RATE-SLOPE"),
    "D042": (("R247", "R249"), 0, "slope", "RATE-SLOPE"),
}
SERIES: dict[str, tuple[str, str, str]] = {
    "R255": ("T10YIE", "rate_fraction", "not_applicable"),
    "R252": ("DFII10", "rate_fraction", "not_applicable"),
    "R246": ("DGS3MO", "rate_fraction", "not_applicable"),
    "R247": ("DGS2", "rate_fraction", "not_applicable"),
    "R249": ("DGS10", "rate_fraction", "not_applicable"),
}
T = datetime(2026, 10, 20, 13, tzinfo=UTC)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-macro-history", 1),
    T - timedelta(days=30),
    T + timedelta(seconds=1),
    T - timedelta(days=30),
)
PROVIDER, VARIANT = "foundation-controlled-macro", "macro_snapshot_v1"
META = (
    ("metric.series", ("metric", "series")),
    ("metric.measurement_date", ("metric", "measurement_date")),
    ("metric.method", ("metric", "method")),
    ("metric.quote_orientation", ("metric", "quote_orientation")),
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
        raise ValueError("unadmitted macro profile")
    raw_ids, _days, mode, label = PROFILES[identity]
    basic = mode in ("slope", "spread")
    profile = "P_BASIC" if basic else "P_WINDOW"
    units = (
        "percentage_points"
        if mode == "slope"
        else "basis_points"
        if mode in ("spread", "rate")
        else "percent"
    )
    shape = "scalar_decimal" if mode in ("slope", "spread", "rate") else "exact_ratio"
    equations = {
        "slope": "100*(second-first)",
        "spread": "10000*(first-second)",
        "rate": "10000*(current-reference)",
        "percent": "100*(current/reference-1)",
    }
    definition = f.CalculationDefinitionV1(
        identity,
        identity + "-" + label + "-1",
        "K02_ALGEBRA" if basic else "K03_CHANGE_RETURN",
        equations[mode],
        raw_ids,
        (),
        profile,
        units,
        shape,
        tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
    )
    param = f.CalculationParameterSetV1(
        "mmt-" + identity.lower() + "-controlled", 1, profile, "NVDA", ("NVDA",)
    )
    policy = f.InputSelectionPolicyVersionV1(
        "mmt-" + identity.lower() + "-selection",
        1,
        ("subject_instrument", "metric.series"),
        timedelta(days=30),
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
            "mmt-macro-" + rid.lower(),
            1,
            r.RawSignalCatalogueId(rid),
            PROVIDER,
            VARIANT,
            ("metric", "value"),
            SERIES[rid][1],
            META,
        )
        for rid in raw_ids
    )
    units_tuple = tuple(
        f.UnitConventionVersionV1(
            "mmt-macro-" + rid.lower() + "-units",
            1,
            SERIES[rid][1],
            SERIES[rid][1],
            Decimal("1"),
            Decimal("0"),
        )
        for rid in raw_ids
    )
    return definition, param, policy, mappings, units_tuple


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    d, p, policy, maps, units = configuration(c.derived_signal_id)
    expected = f.CalculationRequestV1(
        c.derived_signal_id,
        "NVDA",
        T,
        c.knowledge_cutoff_utc,
        d.calculation_definition_version,
        f.VersionRefV1(p.context_id, 1),
        f.VersionRefV1(policy.context_id, 1),
        (CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                m.raw_signal_catalogue_id.value,
                f.VersionRefV1(m.mapping_id, 1),
                f.VersionRefV1(u.context_id, 1),
                "NVDA",
            )
            for m, u in zip(maps, units, strict=True)
        ),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or not T <= c.knowledge_cutoff_utc <= now
    ):
        raise ValueError("incompatible fixed macro request")


def line(
    item: r.ProjectedRawValueV1,
    c: f.CalculationRequestV1,
    mapping: r.RawSignalProjectionMappingV1,
    unit: f.UnitConventionVersionV1,
    policy: f.InputSelectionPolicyVersionV1,
) -> f.RawInputLineageV1:
    event = eligible(replace(item, selection_identity=None), mapping, policy, c)
    if event is None or type(item.native_value) is not Decimal:
        raise ValueError("lawful native macro instant/value required")
    series, _, orientation = SERIES[mapping.raw_signal_catalogue_id.value]
    expected = r.RawSelectionIdentityV1(
        (
            ("metric.series", series),
            ("metric.measurement_date", event.date().isoformat()),
            ("metric.method", "controlled_snapshot/1"),
            ("metric.quote_orientation", orientation),
        )
    )
    if item.selection_identity != expected:
        raise ValueError("incompatible native macro identity/date/method/orientation")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(unit.context_id, 1),
        item,
        item.native_value,
        event,
    )


def exact_decimal(value: Fraction) -> Decimal:
    denominator = value.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        twos += 1
        denominator //= 2
    while denominator % 5 == 0:
        fives += 1
        denominator //= 5
    if denominator != 1:
        raise ValueError("nonterminating difference")
    scale = max(twos, fives)
    coefficient = abs(value.numerator) * 2 ** (scale - twos) * 5 ** (scale - fives)
    return Decimal((int(value < 0), tuple(int(digit) for digit in str(coefficient)), -scale))


def produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    c = request.calculation
    d, p, policy, maps, units = configuration(c.derived_signal_id)
    _, days, mode, _ = PROFILES[c.derived_signal_id]
    roles = (
        tuple((m, u, T) for m, u in zip(maps, units, strict=True))
        if days == 0
        else ((maps[0], units[0], T), (maps[0], units[0], T - timedelta(days=days)))
    )
    if len(lines) != len(roles):
        raise ValueError("incomplete macro roles")
    for actual, (mapping, unit, anchor) in zip(lines, roles, strict=True):
        expected = line(actual.projection, c, mapping, unit, policy)
        if (
            canonical(actual) != canonical(expected)
            or not anchor - timedelta(seconds=60) <= actual.event_time_utc <= anchor
        ):
            raise ValueError("macro selected lineage/anchor mismatch")
    values = tuple(Fraction(x.canonical_value) for x in lines)
    if mode == "slope":
        result: Decimal | f.ExactRatioV1 = exact_decimal(100 * (values[1] - values[0]))
    elif mode in ("spread", "rate"):
        result = exact_decimal(10000 * (values[0] - values[1]))
    else:
        if values[1] == 0:
            raise ValueError("zero macro reference")
        ratio = 100 * (values[0] / values[1] - 1)
        result = f.ExactRatioV1(ratio.numerator, ratio.denominator)
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEFS[c.derived_signal_id],
        c.derived_signal_id,
        "pending",
        request,
        d,
        p,
        policy,
        units,
        maps,
        lines,
        (),
        days * 86400,
        result,
        d.units,
        d.result_shape,
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        if type(value) is not f.WindowMeasurementOccurrenceV1:
            raise TypeError("exact macro occurrence")
        f._Validated.__post_init__(value)
        if admission.implementation_brief_sha256 != BRIEFS.get(
            value.derived_signal_id
        ) or canonical(value) != canonical(
            produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
        ):
            raise ValueError("macro immutable calculation mismatch")

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
            raise TypeError("exact macro request")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            if BRIEFS[c.derived_signal_id] != self.admission.implementation_brief_sha256:
                return None
            _, _, policy, maps, units = configuration(c.derived_signal_id)
            days = PROFILES[c.derived_signal_id][1]
            roles = (
                tuple((m, u, T) for m, u in zip(maps, units, strict=True))
                if days == 0
                else ((maps[0], units[0], T), (maps[0], units[0], T - timedelta(days=days)))
            )
            selected = []
            for mapping, unit, anchor in roles:
                candidates = []
                for item in history(self.raw, c, mapping, policy):
                    try:
                        candidate = line(item, c, mapping, unit, policy)
                        if anchor - timedelta(seconds=60) <= candidate.event_time_utc <= anchor:
                            candidates.append(candidate)
                    except (TypeError, ValueError):
                        continue
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
        raise ValueError("exact macro admission")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("macro requires public M00 only")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
