"""D116 controlled exact-contract option volume/open-interest ratio."""

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
from ._option_scalars import C1, C2, CONTEXT, T
from ._option_skew import source_event
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "4aff69cb6d28b19bb9d0490bae077036c59eda5923e8bd305cfa4e7549b447df"
PROVIDER, VARIANT = "foundation-controlled-option-activity", "volume_oi_v1"
BASE_META = (
    ("contract.id", ("contract", "id")), ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")), ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")), ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("value.role", ("value", "role")), ("source.mode", ("source", "mode")),
)
VOLUME_META = (*BASE_META,
    ("session.id", ("session", "id")),
    ("counter.generation", ("counter", "generation")),
    ("counter.basis", ("counter", "basis")),
)
OI_META = (*BASE_META, ("official.period_id", ("official", "period_id")))
MAPS = (
    r.RawSignalProjectionMappingV1("mmt-r041-option-volume", 1, r.RawSignalCatalogueId("R041"),
                                   PROVIDER, VARIANT, ("activity", "cumulative_volume"),
                                   "contracts", VOLUME_META),
    r.RawSignalProjectionMappingV1("mmt-r047-option-oi", 1, r.RawSignalCatalogueId("R047"),
                                   PROVIDER, VARIANT, ("oi", "call"), "contracts", OI_META),
    r.RawSignalProjectionMappingV1("mmt-r048-option-oi", 1, r.RawSignalCatalogueId("R048"),
                                   PROVIDER, VARIANT, ("oi", "put"), "contracts", OI_META),
)
UNIT = f.UnitConventionVersionV1("mmt-option-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d116-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "source.mode"),
    timedelta(seconds=60), timedelta(seconds=1), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D116", "D116-OPTION-VOLUME-OI-1", "K02_ALGEBRA", "volume/applicable_open_interest",
    ("R041", "R047", "R048"), (), "P_BASIC", "ratio", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)


def parameter(contract: str) -> f.CalculationParameterSetV1:
    if contract not in (C1, C2):
        raise ValueError("unsupported exact option contract")
    return f.CalculationParameterSetV1(
        "mmt-d116-c1-controlled" if contract == C1 else "mmt-d116-c2-controlled",
        1, "P_BASIC", contract, (contract,),
    )


def mappings(contract: str) -> tuple[r.RawSignalProjectionMappingV1, ...]:
    parameter(contract)
    return MAPS[:2] if contract == C1 else (MAPS[0], MAPS[2])


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    selected = mappings(c.subject_instrument)
    param = parameter(c.subject_instrument)
    expected = f.CalculationRequestV1(
        "D116", c.subject_instrument, T, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version, f.VersionRefV1(param.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1), (CONTEXT.ref,),
        tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), c.subject_instrument,
        ) for mapping in selected),
    )
    if (canonical(c) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids or now < c.knowledge_cutoff_utc):
        raise ValueError("incompatible D116 exact contract request")


def expected_identity(contract: str, role: int) -> r.RawSelectionIdentityV1:
    base = (
        ("contract.id", contract), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", "110"),
        ("option.right", "C" if contract == C1 else "P"),
        ("currency.code", "USD"), ("contract.multiplier", "100"),
        ("instrument.kind", "option"),
        ("value.role", "reported_session_volume" if role == 0 else
         "call_open_interest" if role == 1 else "put_open_interest"),
        ("source.mode", "controlled_real_time" if role == 0 else
         "controlled_official_snapshot"),
    )
    return r.RawSelectionIdentityV1(base + (
        (("session.id", "controlled-option-20oct12-13Z"),
         ("counter.generation", "controlled-counter-20261020/1"),
         ("counter.basis", "cumulative_contracts")) if role == 0 else
        (("official.period_id", "controlled-OI-20261020/1"),)
    ))


def candidate(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
              mapping: r.RawSignalProjectionMappingV1, role: int) -> bool:
    return (item.selection_identity == expected_identity(c.subject_instrument, role)
            and eligible(replace(item, selection_identity=None), mapping, POLICY, c)
            is not None)


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
         role: int) -> f.RawInputLineageV1:
    mapping = MAPS[role]
    if (not candidate(item, c, mapping, role) or source_event(item) != T
        or item.received_ts_utc != T or type(item.native_value) is not Decimal
        or item.native_value < 0):
        raise ValueError("exact current compatible volume/OI role required")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), T,
    )


def produce(request: f.WindowCalculationRequestV1,
            lines: tuple[f.RawInputLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    contract = request.calculation.subject_instrument
    roles = (0, 1) if contract == C1 else (0, 2)
    if len(lines) != 2:
        raise ValueError("applicable volume and OI both required")
    for actual, role in zip(lines, roles, strict=True):
        if canonical(actual) != canonical(line(actual.projection, request.calculation, role)):
            raise ValueError("selected D116 source lineage mismatch")
    numerator, denominator = (Fraction(x.canonical_value) for x in lines)
    if denominator <= 0:
        raise ValueError("positive selected OI denominator required")
    ratio = numerator / denominator
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D116", "pending", request, DEFINITION,
        parameter(contract), POLICY, (UNIT,), mappings(contract), lines, (), 0,
        f.ExactRatioV1(ratio.numerator, ratio.denominator), "ratio", "exact_ratio",
        T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact D116 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                             value.calculated_at_utc)):
        raise ValueError("D116 source/result/identity mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact D116 request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            selected = []
            for mapping in mappings(request.calculation.subject_instrument):
                role = MAPS.index(mapping)
                candidates = tuple(item for item in history(self.raw, request.calculation,
                                                              mapping, POLICY)
                                   if candidate(item, request.calculation, mapping, role))
                if not candidates:
                    raise ValueError("missing applicable option source")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
                    return source_event(item), item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous current option source")
                selected.append(line(chosen, request.calculation, role))
            value = produce(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D116 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)

# D118 owns a distinct per-contract-grain basket source and immutable admission.
BRIEF_D118 = "64e2717a7065a043ef65d3130b12cedd78733083eaf83bacb3e48be6d95434d1"
SUBJECT_D118 = "NVDA_ACTIVITY_E1"
TAGS_D118 = ("C25", "C10", "P25", "P10")
MEMBERS_D118 = tuple(f"controlled-skew-2026-10-23-{tag}" for tag in TAGS_D118)
STRIKES_D118 = ("120", "130", "100", "90")
PROVIDER_D118, VARIANT_D118 = "foundation-controlled-option-activity", "member_volume_v1"
META_D118 = (
    ("contract.id", ("contract", "id")), ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")), ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")), ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("source.mode", ("source", "mode")),
    ("session.id", ("session", "id")),
    ("counter.generation", ("counter", "generation")),
    ("counter.basis", ("counter", "basis")),
    ("value.role", ("value", "role")),
)
MAPS_D118 = (
    r.RawSignalProjectionMappingV1(
        "mmt-r049-member-call-volume", 1, r.RawSignalCatalogueId("R049"),
        PROVIDER_D118, VARIANT_D118, ("activity", "call_volume"), "contracts", META_D118,
    ),
    r.RawSignalProjectionMappingV1(
        "mmt-r050-member-put-volume", 1, r.RawSignalCatalogueId("R050"),
        PROVIDER_D118, VARIANT_D118, ("activity", "put_volume"), "contracts", META_D118,
    ),
)
POLICY_D118 = f.InputSelectionPolicyVersionV1(
    "mmt-d118-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "source.mode",
     "session.id", "counter.generation", "counter.basis"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), MEMBERS_D118,
    PROVIDER_D118, VARIANT_D118, PROVIDER_D118 + "/" + VARIANT_D118, 100, 1000,
)
DEFINITION_D118 = f.CalculationDefinitionV1(
    "D118", "D118-CALL-PUT-VOLUME-BASKET-1", "K02_ALGEBRA",
    "sum(call_member_volume)/sum(put_member_volume)", ("R049", "R050"), (),
    "P_BASIC", "ratio", "exact_ratio", tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER_D118 = f.CalculationParameterSetV1(
    "mmt-d118-controlled", 1, "P_BASIC", SUBJECT_D118, MEMBERS_D118,
)


def request_check_d118(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D118", SUBJECT_D118, T, T + timedelta(seconds=1),
        DEFINITION_D118.calculation_definition_version,
        f.VersionRefV1(PARAMETER_D118.context_id, 1),
        f.VersionRefV1(POLICY_D118.context_id, 1), (CONTEXT.ref,),
        tuple(f.RawInputBindingV1(
            MAPS_D118[index // 2].raw_signal_catalogue_id.value,
            f.VersionRefV1(MAPS_D118[index // 2].mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), member,
        ) for index, member in enumerate(MEMBERS_D118)),
    )
    if (canonical(request.calculation) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible complete D118 E1 basket request")


def expected_identity_d118(index: int) -> r.RawSelectionIdentityV1:
    if index not in range(4):
        raise ValueError("unadmitted member")
    call = index < 2
    return r.RawSelectionIdentityV1((
        ("contract.id", MEMBERS_D118[index]), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", STRIKES_D118[index]),
        ("option.right", "C" if call else "P"),
        ("currency.code", "USD"), ("contract.multiplier", "100"),
        ("instrument.kind", "option"), ("source.mode", "controlled_real_time"),
        ("session.id", "controlled-option-20oct12-13Z"),
        ("counter.generation", "controlled-counter-20261020/1"),
        ("counter.basis", "per_contract_cumulative_session"),
        ("value.role", "call_volume" if call else "put_volume"),
    ))


def candidate_d118(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
                   index: int) -> bool:
    member = MEMBERS_D118[index]
    mapping = MAPS_D118[index // 2]
    own = replace(c, subject_instrument=member)
    return (item.selection_identity == expected_identity_d118(index)
            and eligible(replace(item, selection_identity=None), mapping, POLICY_D118, own)
            == T)


def line_d118(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
              index: int) -> f.RawInputLineageV1:
    mapping = MAPS_D118[index // 2]
    if (not candidate_d118(item, c, index) or item.received_ts_utc != T
        or type(item.native_value) is not Decimal or item.native_value < 0):
        raise ValueError("missing exact nonnegative per-contract member volume")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), T,
    )


def produce_d118(request: f.WindowCalculationRequestV1,
                 lines: tuple[f.RawInputLineageV1, ...], now: datetime
                 ) -> f.WindowMeasurementOccurrenceV1:
    request_check_d118(request, now)
    if len(lines) != 4:
        raise ValueError("all four configured contract members required")
    for index, actual in enumerate(lines):
        if (type(actual) is not f.RawInputLineageV1
            or canonical(actual) != canonical(line_d118(actual.projection,
                                                         request.calculation, index))):
            raise ValueError("D118 exact member/source/order mismatch")
    numerator = sum((Fraction(x.canonical_value) for x in lines[:2]), Fraction())
    denominator = sum((Fraction(x.canonical_value) for x in lines[2:]), Fraction())
    if denominator <= 0:
        raise ValueError("positive full put volume denominator required")
    ratio = numerator / denominator
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF_D118, "D118", "pending", request, DEFINITION_D118,
        PARAMETER_D118, POLICY_D118, (UNIT,), MAPS_D118, lines, (), 0,
        f.ExactRatioV1(ratio.numerator, ratio.denominator), "ratio", "exact_ratio",
        T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate_d118(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact D118 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce_d118(value.request, value.raw_input_lineage,
                                                  value.calculated_at_utc)):
        raise ValueError("D118 source/result/identity mismatch")


class _OwnerD118:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact D118 request required")
        now = self.now()
        f._utc(now)
        try:
            request_check_d118(request, now)
            selected = []
            for index, member in enumerate(MEMBERS_D118):
                mapping = MAPS_D118[index // 2]
                own_request = replace(request.calculation, subject_instrument=member)
                candidates = tuple(item for item in history(self.raw, own_request,
                                                              mapping, POLICY_D118)
                                   if candidate_d118(item, request.calculation, index))
                if not candidates:
                    raise ValueError("missing configured basket member")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
                    return source_event(item), item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous per-contract volume")
                selected.append(line_d118(chosen, request.calculation, index))
            result = produce_d118(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(result))


def build_owner_d118(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF_D118):
        raise ValueError("exact D118 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _OwnerD118(RecordState(storage, _decode, validate_d118), raw, now)
