"""D094 controlled exact-contract five-minute model-IV history owner."""

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
from ._option_scalars import C1, META, PROVIDER, VARIANT, T
from ._option_scalars import CONTEXT as OPTION_CONTEXT
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "93e7054fd91487f6a8fe2fa1b2118ed82e35b0094c4950841fbb174b1c41b6f5"
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r111-option", 1, r.RawSignalCatalogueId("R111"),
    PROVIDER, VARIANT, ("model", "iv"), "annualised_decimal_volatility", META,
)
UNIT = f.UnitConventionVersionV1(
    "mmt-option-iv", 1, "annualised_decimal_volatility",
    "annualised_decimal_volatility", Decimal("1"), Decimal("0"),
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-iv-window", 1), T - timedelta(seconds=600),
    OPTION_CONTEXT.session_end_utc, T - timedelta(seconds=600),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d094-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=600), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D094", "D094-OPTION-IV-CHANGE-5M-1", "K03_CHANGE_RETURN",
    "100*(current_iv-reference_iv)", ("R111",), (), "P_WINDOW",
    "volatility_points", "exact_ratio", tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-d094-controlled", 1, "P_WINDOW", C1, (C1,))
ANCHOR, EARLIEST = T - timedelta(seconds=300), T - timedelta(seconds=600)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D094", C1, T, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,),
        (f.RawInputBindingV1(
            "R111", f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), C1,
        ),),
    )
    if (canonical(request.calculation) != canonical(expected)
        or request.context != CONTEXT or request.predecessor_occurrence_ids
        or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible controlled five-minute IV request")


def source_identity() -> r.RawSelectionIdentityV1:
    return r.RawSelectionIdentityV1((
        ("contract.id", C1), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", "110"),
        ("option.right", "C"), ("currency.code", "USD"),
        ("contract.multiplier", "100"), ("instrument.kind", "option"),
        ("model.convention", "controlled-model/1"), ("value.role", "model_iv"),
    ))


def candidate(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1) -> bool:
    return (item.subject_instrument == C1
            and item.selection_identity == source_identity()
            and eligible(replace(item, selection_identity=None), MAPPING, POLICY, c) is not None)


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1) -> f.RawInputLineageV1:
    event = eligible(replace(item, selection_identity=None), MAPPING, POLICY, c)
    expected_identity = source_identity()
    if (event is None or not EARLIEST <= event <= T
        or item.received_ts_utc != event
        or item.selection_identity != expected_identity
        or type(item.native_value) is not Decimal or item.native_value < 0):
        raise ValueError("eligible exact-contract model IV source required")
    return f.RawInputLineageV1(
        "R111", item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), event,
    )


def produce(request: f.WindowCalculationRequestV1,
            lines: tuple[f.RawInputLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if (len(lines) != 2 or lines[0].event_time_utc != T
        or not EARLIEST <= lines[1].event_time_utc <= ANCHOR):
        raise ValueError("exact current and bounded five-minute reference required")
    for actual in lines:
        if canonical(actual) != canonical(line(actual.projection, request.calculation)):
            raise ValueError("invalid selected model IV lineage")
    current, reference = (entry.canonical_value for entry in lines)
    difference = Fraction(100) * (Fraction(current) - Fraction(reference))
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D094", "pending", request,
        DEFINITION, PARAMETER, POLICY, (UNIT,), (MAPPING,), lines, (), 300,
        f.ExactRatioV1(difference.numerator, difference.denominator),
        "volatility_points", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact controlled IV change occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(
        value.request, value.raw_input_lineage, value.calculated_at_utc
    )):
        raise ValueError("five-minute IV source/result/identity mismatch")


def choose(items: tuple[r.ProjectedRawValueV1, ...]) -> r.ProjectedRawValueV1:
    if not items:
        raise ValueError("missing eligible IV role")
    def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
        if type(item.source_timestamp_raw) is not str:
            raise ValueError("exact model IV timestamp required")
        event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
        return event, item.received_ts_utc, item.ingestion_sequence
    chosen = max(items, key=rank)
    if sum(rank(item) == rank(chosen) for item in items) != 1:
        raise ValueError("ambiguous model IV source rank")
    return chosen


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact D094 request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            candidates = tuple(history(self.raw, request.calculation, MAPPING, POLICY))
            def event_time(item: r.ProjectedRawValueV1) -> datetime:
                if type(item.source_timestamp_raw) is not str:
                    raise ValueError("exact model IV timestamp required")
                event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
                f._utc(event)
                return event
            current = line(choose(tuple(
                item for item in candidates
                if candidate(item, request.calculation) and event_time(item) == T
            )), request.calculation)
            reference = line(choose(tuple(
                item for item in candidates
                if candidate(item, request.calculation)
                and EARLIEST <= event_time(item) <= ANCHOR
            )), request.calculation)
            value = produce(request, (current, reference), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D094 admission required")
    if (predecessor is not None or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)):
        raise TypeError("declared raw-only storage/clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
