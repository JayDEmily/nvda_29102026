"""Per-index controlled exact daily anchors; no inferred exchange calendar."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._log_return import _logarithm
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import chosen, history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEFS = {
    "D069": "3c8796ec7b767ed1471b01ecd170c69cc4974f801aeff1c0a7343726b9e008fc",
    "D068": "e53dd3327bf582276edd55b26f1bb3464ab9f437e995b5d121042d07f9cdf7c8",
    "D067": "41261784bfdcc5c4e94fa8f49d5b14b6dd0e01b60b1e122dd6c1240c78056a2f",
    "D066": "39e06e96fd6bc3c8415296995896710ec91964c7c7c5d9e8e49e77e59c866308",
}
PROFILES = {
    "D069": ("R273", "NASDAQNQCN10"),
    "D068": ("R272", "NASDAQNQCN"),
    "D067": ("R271", "NASDAQNQHK"),
    "D066": ("R270", "NIKKEI225"),
}
T = datetime(2026, 10, 20, 13, tzinfo=UTC)
REFERENCE = T - timedelta(days=1)
PROVIDER, VARIANT = "foundation-controlled-international", "daily_close_v1"
META = tuple(
    ("index." + key, ("index", key))
    for key in ("series", "close_utc", "adjustment_basis", "close_kind")
)


def configuration(
    identity: str,
) -> tuple[
    f.CalculationDefinitionV1,
    f.CalculationParameterSetV1,
    f.InputSelectionPolicyVersionV1,
    r.RawSignalProjectionMappingV1,
    f.UnitConventionVersionV1,
    f.WindowContextV1,
]:
    if identity not in BRIEFS:
        raise ValueError("unadmitted international return")
    rid, _ = PROFILES[identity]
    definition = f.CalculationDefinitionV1(
        identity,
        identity + "-LOG-RETURN-1",
        "K03_CHANGE_RETURN",
        "ln(current/reference)",
        (rid,),
        (),
        "P_WINDOW",
        "return",
        "scalar_decimal",
        tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
    )
    param = f.CalculationParameterSetV1(
        "mmt-" + identity.lower() + "-controlled", 1, "P_WINDOW", "NVDA", ("NVDA",)
    )
    policy = f.InputSelectionPolicyVersionV1(
        "mmt-" + identity.lower() + "-selection",
        1,
        ("subject_instrument", "index.series"),
        timedelta(days=1),
        timedelta(0),
        ("true_instant",),
        (),
        PROVIDER,
        VARIANT,
        PROVIDER + "/" + VARIANT,
        100,
        1000,
    )
    mapping = r.RawSignalProjectionMappingV1(
        "mmt-" + rid.lower() + "-international",
        1,
        r.RawSignalCatalogueId(rid),
        PROVIDER,
        VARIANT,
        ("index", "value"),
        "index_points",
        META,
    )
    unit = f.UnitConventionVersionV1(
        "mmt-" + rid.lower() + "-index-units",
        1,
        "index_points",
        "index_points",
        Decimal("1"),
        Decimal("0"),
    )
    context = f.WindowContextV1(
        f.VersionRefV1("controlled-international-" + rid.lower(), 1),
        REFERENCE,
        T + timedelta(seconds=1),
        REFERENCE,
    )
    return definition, param, policy, mapping, unit, context


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    d, p, policy, mapping, unit, context = configuration(c.derived_signal_id)
    expected = f.CalculationRequestV1(
        c.derived_signal_id,
        "NVDA",
        T,
        T + timedelta(seconds=1),
        d.calculation_definition_version,
        f.VersionRefV1(p.context_id, 1),
        f.VersionRefV1(policy.context_id, 1),
        (context.ref,),
        (
            f.RawInputBindingV1(
                mapping.raw_signal_catalogue_id.value,
                f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(unit.context_id, 1),
                "NVDA",
            ),
        ),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != context
        or request.predecessor_occurrence_ids
        or now < c.knowledge_cutoff_utc
    ):
        raise ValueError("incompatible exact international frame")


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1) -> f.RawInputLineageV1:
    _, _, policy, mapping, unit, _ = configuration(c.derived_signal_id)
    event = eligible(replace(item, selection_identity=None), mapping, policy, c)
    if event is None or item.selection_identity != r.RawSelectionIdentityV1(
        (
            ("index.series", PROFILES[c.derived_signal_id][1]),
            ("index.close_utc", event.isoformat().replace("+00:00", "Z")),
            ("index.adjustment_basis", "controlled_unadjusted/1"),
            ("index.close_kind", "controlled_official"),
        )
    ):
        raise ValueError("wrong exact index series/close/basis/time")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(unit.context_id, 1),
        item,
        cast(Decimal, item.native_value),
        event,
    )


def produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    c = request.calculation
    d, p, policy, mapping, unit, _ = configuration(c.derived_signal_id)
    if len(lines) != 2:
        raise ValueError("exact current and prior closes required")
    for actual, anchor in zip(lines, (T, REFERENCE), strict=True):
        if actual.event_time_utc != anchor or canonical(actual) != canonical(
            line(actual.projection, c)
        ):
            raise ValueError("required exact international anchor absent")
    if any(x.canonical_value <= 0 for x in lines):
        raise ValueError("positive log prices required")
    result = _logarithm(lines[0].canonical_value, lines[1].canonical_value)
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
        (unit,),
        (mapping,),
        lines,
        (),
        86400,
        result,
        "return",
        "scalar_decimal",
        T,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        if type(value) is not f.WindowMeasurementOccurrenceV1:
            raise TypeError("exact international occurrence required")
        f._Validated.__post_init__(value)
        if admission.implementation_brief_sha256 != BRIEFS.get(
            value.derived_signal_id
        ) or canonical(value) != canonical(
            produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
        ):
            raise ValueError("immutable international calculation mismatch")

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
            raise TypeError("exact international request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            if self.admission.implementation_brief_sha256 != BRIEFS[c.derived_signal_id]:
                return None
            _, _, policy, mapping, _, _ = configuration(c.derived_signal_id)
            items = history(self.raw, c, mapping, policy)
            selected = []
            for anchor in (T, REFERENCE):
                candidates = []
                for item in items:
                    try:
                        value = line(item, c)
                        if value.event_time_utc == anchor:
                            candidates.append(value)
                    except (TypeError, ValueError):
                        continue
                selected.append(chosen(tuple(candidates)))
            result = produce(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(result))


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
        raise ValueError("exact admitted international owner required")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("international return requires public M00 only")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
