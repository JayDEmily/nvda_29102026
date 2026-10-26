"""D119 complete official-period call/put open interest basket."""
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
from ._option_scalars import CONTEXT, T
from ._option_skew import source_event
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

# D119 owns a distinct official-period OI basket and immutable admission.
BRIEF_D119 = "ac1fbe2e28df01b10946fa66e81983cfcc1da620a804c5564ff6ad7a4f378dcf"
SUBJECT_D119 = "NVDA_ACTIVITY_E1"
TAGS_D119 = ("C25", "C10", "P25", "P10")
MEMBERS_D119 = tuple(f"controlled-skew-2026-10-23-{tag}" for tag in TAGS_D119)
STRIKES_D119 = ("120", "130", "100", "90")
PROVIDER_D119, VARIANT_D119 = "foundation-controlled-option-activity", "member_oi_v1"
META_D119 = (
    ("contract.id", ("contract", "id")), ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")), ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")), ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("source.mode", ("source", "mode")),
    ("session.id", ("session", "id")),
    ("official.period_id", ("official", "period_id")),
    ("official.revision_id", ("official", "revision_id")),
    ("value.role", ("value", "role")),
)
MAPS_D119 = (
    r.RawSignalProjectionMappingV1(
        "mmt-r047-member-call-oi", 1, r.RawSignalCatalogueId("R047"),
        PROVIDER_D119, VARIANT_D119, ("oi", "call"), "contracts", META_D119,
    ),
    r.RawSignalProjectionMappingV1(
        "mmt-r048-member-put-oi", 1, r.RawSignalCatalogueId("R048"),
        PROVIDER_D119, VARIANT_D119, ("oi", "put"), "contracts", META_D119,
    ),
)
UNIT = f.UnitConventionVersionV1("mmt-option-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
POLICY_D119 = f.InputSelectionPolicyVersionV1(
    "mmt-d119-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "source.mode",
     "official.period_id", "official.revision_id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), MEMBERS_D119,
    PROVIDER_D119, VARIANT_D119, PROVIDER_D119 + "/" + VARIANT_D119, 100, 1000,
)
DEFINITION_D119 = f.CalculationDefinitionV1(
    "D119", "D119-CALL-PUT-OI-BASKET-1", "K02_ALGEBRA",
    "sum(call_member_open_interest)/sum(put_member_open_interest)", ("R047", "R048"), (),
    "P_BASIC", "ratio", "exact_ratio", tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER_D119 = f.CalculationParameterSetV1(
    "mmt-d119-controlled", 1, "P_BASIC", SUBJECT_D119, MEMBERS_D119,
)


def request_check_d119(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D119", SUBJECT_D119, T, T + timedelta(seconds=1),
        DEFINITION_D119.calculation_definition_version,
        f.VersionRefV1(PARAMETER_D119.context_id, 1),
        f.VersionRefV1(POLICY_D119.context_id, 1), (CONTEXT.ref,),
        tuple(f.RawInputBindingV1(
            MAPS_D119[index // 2].raw_signal_catalogue_id.value,
            f.VersionRefV1(MAPS_D119[index // 2].mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), member,
        ) for index, member in enumerate(MEMBERS_D119)),
    )
    if (canonical(request.calculation) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible complete D119 E1 basket request")


def expected_identity_d119(index: int, period: str) -> r.RawSelectionIdentityV1:
    if index not in range(4):
        raise ValueError("unadmitted member")
    call = index < 2
    return r.RawSelectionIdentityV1((
        ("contract.id", MEMBERS_D119[index]), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", STRIKES_D119[index]),
        ("option.right", "C" if call else "P"),
        ("currency.code", "USD"), ("contract.multiplier", "100"),
        ("instrument.kind", "option"), ("source.mode", "controlled_real_time"),
        ("session.id", "controlled-option-20oct12-13Z"),
        ("official.period_id", period),
        ("official.revision_id", "controlled-oi-revision/1"),
        ("value.role", "call_oi" if call else "put_oi"),
    ))


def candidate_d119(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
                   index: int) -> bool:
    member = MEMBERS_D119[index]
    mapping = MAPS_D119[index // 2]
    own = replace(c, subject_instrument=member)
    identity = item.selection_identity
    if identity is None:
        return False
    try:
        period = identity.value_for("official.period_id")
    except (ValueError, KeyError):
        return False
    return (type(period) is str and period in ("controlled-oi-period-20261020/1",
                       "controlled-oi-period-20261019/1")
            and item.selection_identity == expected_identity_d119(index, period)
            and eligible(replace(item, selection_identity=None), mapping, POLICY_D119, own)
            == T)


def line_d119(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
              index: int) -> f.RawInputLineageV1:
    mapping = MAPS_D119[index // 2]
    if (not candidate_d119(item, c, index) or item.received_ts_utc != T
        or type(item.native_value) is not Decimal or item.native_value < 0):
        raise ValueError("missing exact nonnegative per-contract official OI")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), T,
    )


def produce_d119(request: f.WindowCalculationRequestV1,
                 lines: tuple[f.RawInputLineageV1, ...], now: datetime
                 ) -> f.WindowMeasurementOccurrenceV1:
    request_check_d119(request, now)
    if len(lines) != 4:
        raise ValueError("all four configured contract members required")
    for index, actual in enumerate(lines):
        if (type(actual) is not f.RawInputLineageV1
            or canonical(actual) != canonical(line_d119(actual.projection,
                                                         request.calculation, index))):
            raise ValueError("D119 exact member/source/order mismatch")
    periods = tuple(line.projection.selection_identity.value_for("official.period_id")
                    for line in lines if line.projection.selection_identity is not None)
    if periods != ("controlled-oi-period-20261020/1",) * 4:
        raise ValueError("mixed official OI reporting periods")
    numerator = sum((Fraction(x.canonical_value) for x in lines[:2]), Fraction())
    denominator = sum((Fraction(x.canonical_value) for x in lines[2:]), Fraction())
    if denominator <= 0:
        raise ValueError("positive full put OI denominator required")
    ratio = numerator / denominator
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF_D119, "D119", "pending", request, DEFINITION_D119,
        PARAMETER_D119, POLICY_D119, (UNIT,), MAPS_D119, lines, (), 0,
        f.ExactRatioV1(ratio.numerator, ratio.denominator), "ratio", "exact_ratio",
        T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate_d119(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact D119 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce_d119(value.request, value.raw_input_lineage,
                                                  value.calculated_at_utc)):
        raise ValueError("D119 source/result/identity mismatch")


class _OwnerD119:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact D119 request required")
        now = self.now()
        f._utc(now)
        try:
            request_check_d119(request, now)
            selected = []
            for index, member in enumerate(MEMBERS_D119):
                mapping = MAPS_D119[index // 2]
                own_request = replace(request.calculation, subject_instrument=member)
                candidates = tuple(item for item in history(self.raw, own_request,
                                                              mapping, POLICY_D119)
                                   if candidate_d119(item, request.calculation, index))
                if not candidates:
                    raise ValueError("missing configured basket member")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
                    return source_event(item), item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous official per-contract OI")
                selected.append(line_d119(chosen, request.calculation, index))
            result = produce_d119(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(result))


def build_owner_d119(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF_D119):
        raise ValueError("exact D119 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _OwnerD119(RecordState(storage, _decode, validate_d119), raw, now)
