"""Fixed release-specific surprise over matched public actual/forecast observations."""

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
from ._numeric_bounds import sqrt_ratio_50
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import chosen, history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEFS = {"D063": "09d32004835d2cd8ac9b8aa3911a97f4b1f1f62b418564c9a0280ce65983185e"}
T = datetime(2026, 10, 15, 12, 30, tzinfo=UTC)
CUTOFF = datetime(2026, 10, 15, 13, tzinfo=UTC)
START = datetime(2026, 7, 14, 12, tzinfo=UTC)
CONTEXT = f.WindowContextV1(f.VersionRefV1("controlled-release-history", 1), START, CUTOFF, START)
RELEASES = (
    ("syn-release-jul", "2026-07-15T12:30:00Z"),
    ("syn-release-aug", "2026-08-14T12:30:00Z"),
    ("syn-release-sep", "2026-09-15T12:30:00Z"),
    ("syn-release-oct", "2026-10-15T12:30:00Z"),
)
FAMILY = "US-CPI-HEADLINE-YOY-SYNTHETIC"
META = tuple(
    ("release." + key, ("release", key))
    for key in ("id", "family", "scheduled_utc", "kind", "known_utc", "revision")
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + rid.lower() + "-release",
        1,
        r.RawSignalCatalogueId(rid),
        "foundation-controlled-events",
        "release_snapshot_v1",
        ("release", kind),
        "synthetic_pct_yoy",
        META,
    )
    for rid, kind in (("R286", "actual"), ("R285", "consensus"))
)
UNIT = f.UnitConventionVersionV1(
    "mmt-release-units", 1, "synthetic_pct_yoy", "synthetic_pct_yoy", Decimal("1"), Decimal("0")
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d063-selection",
    1,
    ("subject_instrument", "release.id", "release.family", "release.kind"),
    timedelta(days=100),
    timedelta(0),
    ("true_instant",),
    (),
    "foundation-controlled-events",
    "release_snapshot_v1",
    "foundation-controlled-events/release_snapshot_v1",
    100,
    1000,
)
PARAM = f.CalculationParameterSetV1("mmt-d063-controlled", 1, "P_BASELINE", "NVDA", ("NVDA",))
DEFINITION = f.CalculationDefinitionV1(
    "D063",
    "D063-MACRO-SURPRISE-1",
    "K04_STANDARDISE_RANK",
    "(current_surprise-mean(prior_surprises))/sample_sd(prior_surprises)",
    ("R286", "R285"),
    (),
    "P_BASELINE",
    "z-score",
    "scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D063",
        "NVDA",
        T,
        CUTOFF,
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAM.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                m.raw_signal_catalogue_id.value,
                f.VersionRefV1(m.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1),
                "NVDA",
            )
            for m in MAPS
        ),
    )
    if (
        canonical(request.calculation) != canonical(expected)
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or now < CUTOFF
    ):
        raise ValueError("incompatible release request")


def line(
    item: r.ProjectedRawValueV1,
    c: f.CalculationRequestV1,
    mapping: r.RawSignalProjectionMappingV1,
    release_id: str,
    scheduled: str,
) -> f.RawInputLineageV1:
    event = eligible(replace(item, selection_identity=None), mapping, POLICY, c)
    if event is None or item.selection_identity is None:
        raise ValueError("lawful numeric release projection required")
    metadata = {key: cast(str, value) for key, value in item.selection_identity.values}
    if any(type(value) is not str for _, value in item.selection_identity.values):
        raise ValueError("exact string release metadata required")
    kind = mapping.native_field_path[-1]
    if tuple(metadata) != tuple(key for key, _ in META):
        raise ValueError("exact release identity fields required")
    if (
        metadata["release.id"],
        metadata["release.family"],
        metadata["release.scheduled_utc"],
        metadata["release.kind"],
    ) != (release_id, FAMILY, scheduled, kind):
        raise ValueError("wrong selected release/family/kind")
    known_text = metadata["release.known_utc"]
    known = datetime.fromisoformat(known_text.replace("Z", "+00:00"))
    scheduled_at = datetime.fromisoformat(scheduled.replace("Z", "+00:00"))
    f._utc(known)
    if (
        known.isoformat().replace("+00:00", "Z") != known_text
        or not metadata["release.revision"]
        or item.received_ts_utc != known
        or known > CUTOFF
    ):
        raise ValueError("release disclosure/receipt mismatch")
    if kind == "consensus":
        if event != known or known >= scheduled_at:
            raise ValueError("forecast must be known strictly before own release")
    elif event != scheduled_at or known < scheduled_at or (scheduled_at < T and known >= T):
        raise ValueError("actual release/strict historical visibility mismatch")
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
    if len(lines) != 8:
        raise ValueError("four complete selected release pairs required")
    for index, (release_id, scheduled) in enumerate(RELEASES):
        for role, mapping in enumerate(MAPS):
            actual = lines[2 * index + role]
            if canonical(actual) != canonical(
                line(actual.projection, request.calculation, mapping, release_id, scheduled)
            ):
                raise ValueError("release lineage mismatch")
            metadata = (
                dict(actual.projection.selection_identity.values)
                if actual.projection.selection_identity
                else {}
            )
            if metadata.get("release.revision") != ("a1" if role == 0 else "c1"):
                raise ValueError("unsupported selected release revision")
    surprises = tuple(
        Fraction(lines[i].canonical_value) - Fraction(lines[i + 1].canonical_value)
        for i in range(0, 8, 2)
    )
    baseline = surprises[:3]
    mean = sum(baseline, Fraction()) / 3
    variance = sum(((value - mean) ** 2 for value in baseline), Fraction()) / 2
    if variance <= 0:
        raise ValueError("positive sample variance required")
    difference = surprises[3] - mean
    magnitude = sqrt_ratio_50(difference * difference / variance)
    result = magnitude.copy_negate() if difference < 0 else magnitude
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEFS["D063"],
        "D063",
        "pending",
        request,
        DEFINITION,
        PARAM,
        POLICY,
        (UNIT,),
        MAPS,
        lines,
        (),
        int((T - datetime(2026, 7, 15, 12, 30, tzinfo=UTC)).total_seconds()),
        result,
        "z-score",
        "scalar_decimal",
        T,
        CUTOFF,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        if type(value) is not f.WindowMeasurementOccurrenceV1:
            raise TypeError("exact release occurrence required")
        f._Validated.__post_init__(value)
        if admission != f.OwnerAdmissionV1("M02", BRIEFS["D063"]) or canonical(value) != canonical(
            produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
        ):
            raise ValueError("immutable release calculation mismatch")

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
            raise TypeError("exact release request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            histories = tuple(history(self.raw, request.calculation, m, POLICY) for m in MAPS)
            selected = []
            for release_id, scheduled in RELEASES:
                for mapping, items in zip(MAPS, histories, strict=True):
                    candidates = []
                    for item in items:
                        try:
                            candidates.append(
                                line(item, request.calculation, mapping, release_id, scheduled)
                            )
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
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1(
        "M02", BRIEFS["D063"]
    ):
        raise ValueError("exact D063 admission required")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("D063 needs public M00 only")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
