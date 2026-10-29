"""Exact subject-specific current-last versus prior official-close returns."""

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
    "D071": "83e3871a48ec3f9be3f019aeaa8e149bb0658930ca08b4f0158a7a3205c42710",
    "D072": "6a9ff0f10b2d1e507f75dd7d82456272b55eb02fe3a90f8911d0fe14f1ec7184",
    "D073": "8ca4fc8976069b14962cd6c1706c38472749b807c50be81792325178d5c34f64",
    "D074": "c9b03ed51bbe4c64cb8a9f60a3a77a77c95a8961ecad21d3d15940ac8d6c9c1d",
    "D075": "5cbb863087a2393218818f2e85c0182ad44060509ec1901200f6f670e8d1e377",
}
PROFILES = {"D071": "SPY", "D072": "QQQ", "D073": "SMH", "D074": "SOXX", "D075": "NVDA"}
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
REFERENCE = datetime(2026, 10, 19, 13, tzinfo=UTC)
START = datetime(2026, 10, 19, 12, tzinfo=UTC)
END = datetime(2026, 10, 20, 13, tzinfo=UTC)
CONTEXT = f.WindowContextV1(f.VersionRefV1("controlled-underlying-session", 1), START, END, START)
PROVIDER, VARIANT = "foundation-controlled-underlying", "last_prior_close_v1"
META = (
    ("instrument.id", ("instrument", "id")),
    ("session.id", ("session", "id")),
    ("adjustment.basis", ("adjustment", "basis")),
    ("price.kind", ("price", "kind")),
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + rid.lower() + "-underlying",
        1,
        r.RawSignalCatalogueId(rid),
        PROVIDER,
        VARIANT,
        path,
        "price",
        META,
    )
    for rid, path in (("R037", ("trade", "last")), ("R042", ("official_close", "value")))
)
UNIT = f.UnitConventionVersionV1(
    "mmt-underlying-price", 1, "price", "price", Decimal("1"), Decimal("0")
)


def configuration(
    identity: str,
) -> tuple[f.CalculationDefinitionV1, f.CalculationParameterSetV1, f.InputSelectionPolicyVersionV1]:
    if identity not in BRIEFS:
        raise ValueError("unadmitted underlying return")
    subject = PROFILES[identity]
    definition = f.CalculationDefinitionV1(
        identity,
        identity + "-LOG-RETURN-1",
        "K03_CHANGE_RETURN",
        "ln(current/reference)",
        ("R037", "R042"),
        (),
        "P_WINDOW",
        "return",
        "scalar_decimal",
        tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
    )
    param = f.CalculationParameterSetV1(
        "mmt-" + identity.lower() + "-controlled", 1, "P_WINDOW", subject, (subject,)
    )
    policy = f.InputSelectionPolicyVersionV1(
        "mmt-" + identity.lower() + "-selection",
        1,
        ("subject_instrument", "instrument.id", "session.id"),
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
    return definition, param, policy


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    d, p, policy = configuration(c.derived_signal_id)
    subject = PROFILES[c.derived_signal_id]
    expected = f.CalculationRequestV1(
        c.derived_signal_id,
        subject,
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
                f.VersionRefV1(UNIT.context_id, 1),
                subject,
            )
            for m in MAPS
        ),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or c.knowledge_cutoff_utc not in (T + timedelta(seconds=1), T + timedelta(seconds=2))
        or now < c.knowledge_cutoff_utc
    ):
        raise ValueError("incompatible exact underlying frame/cutoff")


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1, role: int) -> f.RawInputLineageV1:
    _, _, policy = configuration(c.derived_signal_id)
    mapping = MAPS[role]
    event = eligible(replace(item, selection_identity=None), mapping, policy, c)
    expected = r.RawSelectionIdentityV1(
        (
            ("instrument.id", PROFILES[c.derived_signal_id]),
            ("session.id", "controlled-20oct12-13Z" if role == 0 else "controlled-19oct12-13Z"),
            ("adjustment.basis", "controlled_unadjusted/1"),
            ("price.kind", "current_last" if role == 0 else "official_close"),
        )
    )
    if event != (T if role == 0 else REFERENCE) or item.selection_identity != expected:
        raise ValueError("wrong exact subject/session/basis/price role")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(UNIT.context_id, 1),
        item,
        cast(Decimal, item.native_value),
        event,
    )


def produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    c = request.calculation
    d, p, policy = configuration(c.derived_signal_id)
    if len(lines) != 2:
        raise ValueError("two subject-specific price roles required")
    for role, actual in enumerate(lines):
        if canonical(actual) != canonical(line(actual.projection, c, role)):
            raise ValueError("underlying lineage mismatch")
    if any(item.canonical_value <= 0 for item in lines):
        raise ValueError("positive ln prices required")
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
        (UNIT,),
        MAPS,
        lines,
        (),
        85200,
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
            raise TypeError("exact underlying occurrence required")
        f._Validated.__post_init__(value)
        if admission.implementation_brief_sha256 != BRIEFS.get(
            value.derived_signal_id
        ) or canonical(value) != canonical(
            produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
        ):
            raise ValueError("immutable underlying return mismatch")

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
            raise TypeError("exact underlying request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            if self.admission.implementation_brief_sha256 != BRIEFS[c.derived_signal_id]:
                return None
            _, _, policy = configuration(c.derived_signal_id)
            selected = []
            for role, mapping in enumerate(MAPS):
                candidates = []
                for item in history(self.raw, c, mapping, policy):
                    try:
                        candidates.append(line(item, c, role))
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
        raise ValueError("exact admitted underlying owner required")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("underlying return requires public M00 only")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
