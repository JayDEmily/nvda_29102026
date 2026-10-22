"""Fixed controlled cash-volume baseline profiles through public raw history."""

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

BRIEFS = {"D028": "c0c2788a727681d87f7b971d242f263d0f04657c896cc113bcf8a57126e684a9"}
DATES = tuple(datetime(2026, 9, 29, 12, tzinfo=UTC) + timedelta(days=i) for i in range(22))
OVERLAY = (
    "handoff/m01_completion/authority/D028_OWNER_APPROVED_RAW_VOLUME_BASELINE_AMENDMENT_20261017.md",
    "115edc89241c9973793f2c74bdc2f4f946a42fe38217b2462c2cab932fa1837c",
)


def configuration(
    identity: str,
) -> tuple[
    f.CalculationDefinitionV1,
    f.CalculationParameterSetV1,
    f.InputSelectionPolicyVersionV1,
    r.RawSignalProjectionMappingV1,
    f.UnitConventionVersionV1,
    f.BaselineWindowContextV1,
]:
    if identity not in BRIEFS:
        raise ValueError("unadmitted baseline")
    name = "mmt-relative-volume-2sessions"
    mapping = r.RawSignalProjectionMappingV1(
        "mmt-session-volume",
        1,
        r.RawSignalCatalogueId("R041"),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        ("session", "volume"),
        "shares",
        (
            ("session.id", ("session", "id")),
            ("counter.generation", ("counter", "generation")),
            ("counter.basis", ("counter", "basis")),
            ("counter.complete_from_open", ("counter", "complete_from_open")),
        ),
    )
    unit = f.UnitConventionVersionV1(
        "mmt-shares", 1, "shares", "shares", Decimal("1"), Decimal("0")
    )
    definition = f.CalculationDefinitionV1(
        identity,
        "D028-RELATIVE-VOLUME-1",
        "K04_RELATIVE_ACTIVITY",
        "current / mean(prior_same_fraction)",
        ("R041",),
        (),
        "P_BASELINE",
        "multiple",
        "exact_ratio",
        tuple(f.AuthorityArtifactRefV1(*x) for x in (*_AUTHORITY, OVERLAY)),
    )
    parameter = f.CalculationParameterSetV1(name, 1, "P_BASELINE", "NVDA", ("NVDA",))
    policy = f.InputSelectionPolicyVersionV1(
        name + "-selection",
        1,
        ("subject_instrument", "session"),
        timedelta(days=30),
        timedelta(0),
        ("true_instant",),
        (),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        "foundation-pilot-fixture/cash_quote_v1",
        100,
        1000,
    )
    context = f.BaselineWindowContextV1(
        f.VersionRefV1("controlled-volume-calendar", 1),
        DATES[-1],
        DATES[-1] + timedelta(hours=1),
        DATES[0],
        tuple(
            f.SessionFrameV1(
                f.VersionRefV1("controlled-volume-" + d.strftime("%Y%m%d"), 1),
                "controlled_cash",
                d,
                d + timedelta(hours=1),
            )
            for d in DATES
        ),
        2,
        1800,
    )
    return definition, parameter, policy, mapping, unit, context


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    d, p, policy, m, u, context = configuration(c.derived_signal_id)
    expected = f.CalculationRequestV1(
        c.derived_signal_id,
        "NVDA",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        d.calculation_definition_version,
        f.VersionRefV1(p.context_id, 1),
        f.VersionRefV1(policy.context_id, 1),
        (context.ref,),
        (
            f.RawInputBindingV1(
                m.raw_signal_catalogue_id.value,
                f.VersionRefV1(m.mapping_id, 1),
                f.VersionRefV1(u.context_id, 1),
                "NVDA",
            ),
        ),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != context
        or request.predecessor_occurrence_ids
        or c.as_of_utc
        != context.session_start_utc + timedelta(seconds=context.bucket_offset_seconds)
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
    ):
        raise ValueError("incompatible fixed baseline request")


def line(
    item: r.ProjectedRawValueV1,
    c: f.CalculationRequestV1,
    m: r.RawSignalProjectionMappingV1,
    u: f.UnitConventionVersionV1,
    policy: f.InputSelectionPolicyVersionV1,
    frame: f.SessionFrameV1,
    event: datetime,
) -> f.RawInputLineageV1:
    actual = eligible(replace(item, selection_identity=None), m, policy, c)
    expected = (
        ("session.id", frame.ref.context_id + "/1"),
        ("counter.generation", "counter-" + frame.start_utc.strftime("%Y%m%d") + "/1"),
        ("counter.basis", "cash_shares_unadjusted"),
        ("counter.complete_from_open", True),
    )
    if (
        actual != event
        or item.selection_identity != r.RawSelectionIdentityV1(expected)
        or type(item.native_value) is not Decimal
        or item.native_value < 0
    ):
        raise ValueError("missing compatible exact fraction")
    return f.RawInputLineageV1(
        m.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(m.mapping_id, 1),
        f.VersionRefV1(u.context_id, 1),
        item,
        item.native_value,
        event,
    )


def roles(context: f.BaselineWindowContextV1) -> tuple[tuple[f.SessionFrameV1, datetime], ...]:
    current = context.sessions[-1]
    required = context.sessions[-context.prior_session_count - 1 : -1]
    if (
        len(required) != context.prior_session_count
        or context.history_complete_from_utc > required[0].start_utc
    ):
        raise ValueError("incomplete calendar")
    frames = (current, *required)
    for frame in frames:
        if (
            frame.session_type != current.session_type
            or frame.end_utc - frame.start_utc != current.end_utc - current.start_utc
        ):
            raise ValueError("incompatible mandatory session")
    return tuple(
        (frame, frame.start_utc + timedelta(seconds=context.bucket_offset_seconds))
        for frame in frames
    )


def produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    c = request.calculation
    d, p, policy, m, u, context = configuration(c.derived_signal_id)
    required = roles(context)
    if len(lines) != len(required):
        raise ValueError("incomplete fixed membership")
    for selected, (frame, event) in zip(lines, required, strict=True):
        if canonical(selected) != canonical(
            line(selected.projection, c, m, u, policy, frame, event)
        ):
            raise ValueError("lineage mismatch")
    values = tuple(Fraction(v.canonical_value) for v in lines)
    mean = sum(values[1:], Fraction()) / context.prior_session_count
    if mean <= 0:
        raise ValueError("nonpositive baseline")
    ratio = values[0] / mean
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
        (u,),
        (m,),
        lines,
        (),
        context.bucket_offset_seconds,
        result,
        d.units,
        d.result_shape,
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact window occurrence")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(
        produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
    ):
        raise ValueError("baseline result/configuration mismatch")


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        validate(value)
        if value.implementation_brief_sha256 != admission.implementation_brief_sha256:
            raise ValueError("wrong admission")

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
            raise TypeError("exact request")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            if BRIEFS[c.derived_signal_id] != self.admission.implementation_brief_sha256:
                return None
            _, _, policy, m, u, context = configuration(c.derived_signal_id)
            items = history(self.raw, c, m, policy)
            lines = []
            for frame, event in roles(context):
                candidates = []
                for item in items:
                    try:
                        candidates.append(line(item, c, m, u, policy, frame, event))
                    except (TypeError, ValueError):
                        continue
                lines.append(chosen(tuple(candidates)))
            value = produce(request, tuple(lines), now)
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
        raise ValueError("exact baseline admission")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("declared raw-only dependencies")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
