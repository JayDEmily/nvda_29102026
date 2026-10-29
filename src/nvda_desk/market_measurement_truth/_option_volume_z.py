"""D117 exact-contract controlled twenty-session receipt-based option volume z-score."""

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
from ._option_scalars import C1, T
from ._option_skew import source_event
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "b1ac74fb86cd171f3d4a431713cadeab9864a98b755a84016809aa8654120b33"
PROVIDER, VARIANT = "foundation-controlled-option-volume", "retained_realtime_counter_v1"
META = (
    ("contract.id", ("contract", "id")), ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")), ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")), ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("calendar.id", ("calendar", "id")),
    ("calendar.version", ("calendar", "version")),
    ("session.id", ("session", "id")),
    ("stream.id", ("stream", "id")),
    ("stream.generation", ("stream", "generation")),
    ("source.mode", ("source", "mode")),
    ("counter.basis", ("counter", "basis")),
    ("counter.complete_from_open", ("counter", "complete_from_open")),
    ("value.role", ("value", "role")),
)
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r041-option-session-volume", 1, r.RawSignalCatalogueId("R041"), PROVIDER,
    VARIANT, ("session", "volume"), "contracts", META,
)
UNIT = f.UnitConventionVersionV1("mmt-option-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
DATES = tuple(datetime(2026, 9, 29, 12, tzinfo=UTC) + timedelta(days=i) for i in range(22))
CONTEXT = f.BaselineWindowContextV1(
    f.VersionRefV1("controlled-option-volume-calendar", 1), DATES[-1],
    DATES[-1] + timedelta(hours=1), DATES[0],
    tuple(f.SessionFrameV1(
        f.VersionRefV1("controlled-option-volume-" + day.strftime("%Y%m%d"), 1),
        "controlled_option_regular", day, day + timedelta(hours=1),
    ) for day in DATES), 20, 2400,
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d117-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "calendar.id",
     "calendar.version", "session.id", "stream.id", "stream.generation",
     "source.mode", "counter.basis", "counter.complete_from_open"),
    timedelta(days=30), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
OVERLAYS = (
    ("handoff/m01_completion/authority/D117_OWNER_APPROVED_RAW_VOLUME_HISTORY_AMENDMENT_20261016.md",
     "7dab0973a7bafcdb284185f492fd37a4ad58d0e9e1246e6f37c3fa893e8023df"),
    ("handoff/m01_completion/authority/D117_OWNER_APPROVED_EXACT_CONTRACT_BASELINE_20261016.md",
     "b5b310413b9f2ded2d87e6b84994f531bb9aba2dd679c463deb48d0e54f7546b"),
)
DEFINITION = f.CalculationDefinitionV1(
    "D117", "D117-EXACT-CONTRACT-20SESSION-RECEIPT-1", "K04_STANDARDISE_RANK",
    "(current-mean(prior20))/sample_sd(prior20)", ("R041",), (), "P_BASELINE",
    "z_score", "scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*x) for x in (*_AUTHORITY, *OVERLAYS)),
)
PARAMETER = f.CalculationParameterSetV1("mmt-d117-controlled", 1, "P_BASELINE", C1, (C1,))


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D117", C1, T, T + timedelta(seconds=1), DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), (f.RawInputBindingV1(
            "R041", f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), C1,
        ),),
    )
    if (canonical(request.calculation) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible D117 twenty-session receipt request")


def roles() -> tuple[tuple[f.SessionFrameV1, datetime], ...]:
    frames = (CONTEXT.sessions[-1], *CONTEXT.sessions[1:-1])
    if (len(CONTEXT.sessions) != 22 or len(frames) != 21
        or CONTEXT.history_complete_from_utc != CONTEXT.sessions[0].start_utc):
        raise ValueError("incomplete exact synthetic session calendar")
    return tuple((frame, frame.start_utc + timedelta(seconds=2400)) for frame in frames)


def expected_identity(frame: f.SessionFrameV1) -> r.RawSelectionIdentityV1:
    date = frame.start_utc.strftime("%Y%m%d")
    return r.RawSelectionIdentityV1((
        ("contract.id", C1), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", "110"),
        ("option.right", "C"), ("currency.code", "USD"),
        ("contract.multiplier", "100"), ("instrument.kind", "option"),
        ("calendar.id", "controlled-option-volume-calendar"),
        ("calendar.version", "1"),
        ("session.id", f"controlled-option-volume-{date}/1"),
        ("stream.id", "controlled-option-stream/1"),
        ("stream.generation", f"controlled-session-{date}/1"),
        ("source.mode", "controlled_real_time"),
        ("counter.basis", "cumulative_contracts_in_named_session"),
        ("counter.complete_from_open", "true"),
        ("value.role", "reported_session_volume"),
    ))


def candidate(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
              frame: f.SessionFrameV1, minute: datetime) -> bool:
    if item.selection_identity != expected_identity(frame):
        return False
    event = eligible(replace(item, selection_identity=None), MAPPING, POLICY, c)
    return (event is not None and frame.start_utc <= event <= minute
            and minute - timedelta(seconds=60) < item.received_ts_utc <= minute
            and item.received_ts_utc <= c.knowledge_cutoff_utc)


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
         frame: f.SessionFrameV1, minute: datetime) -> f.RawInputLineageV1:
    if (not candidate(item, c, frame, minute) or type(item.native_value) is not Decimal
        or item.native_value < 0):
        raise ValueError("valid historical receipt and cumulative contract volume required")
    return f.RawInputLineageV1(
        "R041", item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), source_event(item),
    )


def produce(request: f.WindowCalculationRequestV1,
            lines: tuple[f.RawInputLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 21:
        raise ValueError("current plus twenty immediate prior sessions required")
    for actual, (frame, minute) in zip(lines, roles(), strict=True):
        if (type(actual) is not f.RawInputLineageV1
            or canonical(actual) != canonical(line(actual.projection, request.calculation,
                                                    frame, minute))):
            raise ValueError("D117 exact session receipt source/order mismatch")
    values = tuple(Fraction(x.canonical_value) for x in lines)
    mean = sum(values[1:], Fraction()) / 20
    variance = sum(((v - mean) ** 2 for v in values[1:]), Fraction()) / 19
    if variance <= 0:
        raise ValueError("positive sample variance required")
    difference = values[0] - mean
    magnitude = sqrt_ratio_50(difference * difference / variance)
    result = magnitude.copy_negate() if difference < 0 else magnitude
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D117", "pending", request, DEFINITION,
        PARAMETER, POLICY, (UNIT,), (MAPPING,), lines, (), 2400,
        result, "z_score", "scalar_decimal", T,
        request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact D117 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                             value.calculated_at_utc)):
        raise ValueError("D117 source/result/identity mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact D117 request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            items = tuple(history(self.raw, request.calculation, MAPPING, POLICY))
            lines = []
            for frame, minute in roles():
                candidates = tuple(item for item in items
                                   if candidate(item, request.calculation, frame, minute))
                if not candidates:
                    raise ValueError("missing required session receipt")
                # The declared stream/generation is already fixed by session identity.
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, int]:
                    return item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous receipt/ingestion order")
                lines.append(line(chosen, request.calculation, frame, minute))
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
        raise ValueError("exact D117 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
