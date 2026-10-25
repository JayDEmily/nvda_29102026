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
