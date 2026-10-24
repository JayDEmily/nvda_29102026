"""Controlled exact-contract option scalar owners, initially D087 midpoint."""

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
from ._log_return import _logarithm
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF_D087 = "103777a517401fcb08099acb6fe7c915286499819c1f8f71da50c4bf71cc8468"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
C1, C2 = "controlled-nvda-c110-20261023", "controlled-nvda-p110-20261023"
PROVIDER, VARIANT = "foundation-controlled-options", "option_snapshot_v1"
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1), datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC), datetime(2026, 10, 20, 12, tzinfo=UTC),
)
META = (
    ("contract.id", ("contract", "id")),
    ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")),
    ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")),
    ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("model.convention", ("model", "convention")),
    ("value.role", ("value", "role")),
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw),
        PROVIDER, VARIANT, path, "USD_per_share", META,
    ) for raw, path in (("R034", ("quote", "bid")), ("R035", ("quote", "ask")))
)
UNIT = f.UnitConventionVersionV1(
    "mmt-option-price", 1, "USD_per_share", "USD_per_share", Decimal("1"), Decimal("0")
)
DEFINITION = f.CalculationDefinitionV1(
    "D087", "D087-OPTION-SCALAR-1", "K02_ALGEBRA", "(bid+ask)/2",
    ("R034", "R035"), (), "P_BASIC", "option_premium", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d087-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def parameter(contract: str) -> f.CalculationParameterSetV1:
    if contract not in (C1, C2):
        raise ValueError("unsupported exact controlled option contract")
    return f.CalculationParameterSetV1(
        "mmt-d087-c1-controlled" if contract == C1 else "mmt-d087-c2-controlled",
        1, "P_BASIC", contract, (contract,),
    )


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    subject = request.calculation.subject_instrument
    own_parameter = parameter(subject)
    expected = f.CalculationRequestV1(
        "D087", subject, T, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(own_parameter.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                mapping.raw_signal_catalogue_id.value, f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1), subject,
            ) for mapping in MAPS
        ),
    )
    if (
        canonical(request.calculation) != canonical(expected)
        or request.context != CONTEXT or request.predecessor_occurrence_ids
        or now < expected.knowledge_cutoff_utc
    ):
        raise ValueError("incompatible exact controlled midpoint request")


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
         role: int) -> f.RawInputLineageV1:
    mapping = MAPS[role]
    event = eligible(replace(item, selection_identity=None), mapping, POLICY, c)
    expected_identity = r.RawSelectionIdentityV1((
        ("contract.id", c.subject_instrument), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", "110"),
        ("option.right", "C" if c.subject_instrument == C1 else "P"),
        ("currency.code", "USD"), ("contract.multiplier", "100"),
        ("instrument.kind", "option"), ("model.convention", "controlled-model/1"),
        ("value.role", "option_bid" if role == 0 else "option_ask"),
    ))
    if (
        event != T or item.received_ts_utc != T
        or item.selection_identity != expected_identity
        or type(item.native_value) is not Decimal
    ):
        raise ValueError("matched exact-contract option quote role required")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), T,
    )


def produce(request: f.WindowCalculationRequestV1,
            lines: tuple[f.RawInputLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 2:
        raise ValueError("bid and ask both required")
    for role, actual in enumerate(lines):
        if canonical(actual) != canonical(line(actual.projection, request.calculation, role)):
            raise ValueError("option source lineage mismatch")
    bid, ask = (item.canonical_value for item in lines)
    if bid < 0 or ask < 0 or bid > ask:
        raise ValueError("nonnegative uncrossed option quote required")
    midpoint = (Fraction(bid) + Fraction(ask)) / 2
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF_D087, "D087", "pending", request, DEFINITION,
        parameter(request.calculation.subject_instrument), POLICY, (UNIT,), MAPS,
        lines, (), 0, f.ExactRatioV1(midpoint.numerator, midpoint.denominator),
        "option_premium", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact option midpoint occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                             value.calculated_at_utc)):
        raise ValueError("option midpoint/source/identity mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact midpoint request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            selected: list[f.RawInputLineageV1] = []
            for mapping in MAPS:
                candidates = tuple(history(self.raw, request.calculation, mapping, POLICY))
                if not candidates:
                    raise ValueError("missing option quote side")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
                    if type(item.source_timestamp_raw) is not str:
                        raise ValueError("exact option source instant required")
                    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
                    return event, item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous option quote rank")
                selected.append(line(chosen, request.calculation, len(selected)))
            value = produce(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF_D087):
        raise ValueError("exact D087 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage and clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)


# D088 is a separate admitted occurrence with an actual D087 public predecessor.
BRIEF_D088 = "23129ece93db232f4258187a6aef130f74652814512d49cd4db2127fd4a23cfb"
DEFINITION_D088 = f.CalculationDefinitionV1(
    "D088", "D088-OPTION-SCALAR-1", "K02_ALGEBRA", "100*(ask-bid)/mid",
    ("R034", "R035"), ("D087",), "P_BASIC", "percent", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER_D088 = f.CalculationParameterSetV1("mmt-d088-controlled", 1, "P_BASIC", C1, (C1,))
POLICY_D088 = replace(POLICY, context_id="mmt-d088-selection")


def request_check_d088(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D088", C1, T, T + timedelta(seconds=1),
        DEFINITION_D088.calculation_definition_version,
        f.VersionRefV1(PARAMETER_D088.context_id, 1),
        f.VersionRefV1(POLICY_D088.context_id, 1), (CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                mapping.raw_signal_catalogue_id.value,
                f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1), C1,
            ) for mapping in MAPS
        ),
    )
    if (
        canonical(request.calculation) != canonical(expected)
        or request.context != CONTEXT
        or len(request.predecessor_occurrence_ids) != 1
        or now < expected.knowledge_cutoff_utc
    ):
        raise ValueError("incompatible exact option spread request")


def produce_d088(
    request: f.WindowCalculationRequestV1,
    lines: tuple[f.RawInputLineageV1, ...],
    predecessors: tuple[f.WindowMeasurementOccurrenceV1, ...], now: datetime,
) -> f.WindowMeasurementOccurrenceV1:
    request_check_d088(request, now)
    if len(lines) != 2 or len(predecessors) != 1:
        raise ValueError("direct quote and actual midpoint required")
    parent = predecessors[0]
    validate(parent)
    if (
        parent.derived_occurrence_id != request.predecessor_occurrence_ids[0]
        or parent.derived_signal_id != "D087"
        or parent.implementation_brief_sha256 != BRIEF_D087
        or parent.request.calculation.subject_instrument != C1
        or parent.effective_as_of_utc != T
        or parent.knowledge_cutoff_utc != request.calculation.knowledge_cutoff_utc
        or parent.calculated_at_utc > now
        or parent.request.context != request.context
        or parent.unit_conventions != (UNIT,)
        or parent.projection_mappings != MAPS
        or parent.window_seconds != 0
        or type(parent.result) is not f.ExactRatioV1
    ):
        raise ValueError("incompatible actual exact-contract midpoint")
    for role, actual in enumerate(lines):
        event = eligible(replace(actual.projection, selection_identity=None),
                         MAPS[role], POLICY_D088, request.calculation)
        if event != T or canonical(actual) != canonical(line(
            actual.projection, request.calculation, role
        )):
            raise ValueError("direct quote source or own selection mismatch")
    if parent.raw_input_lineage != lines:
        raise ValueError("actual midpoint must retain same selected source observations")
    bid, ask = (item.canonical_value for item in lines)
    midpoint = cast(f.ExactRatioV1, parent.result)
    if bid < 0 or ask < bid or midpoint.numerator <= 0:
        raise ValueError("positive same-contract midpoint and uncrossed quote required")
    spread = Fraction(100) * (Fraction(ask) - Fraction(bid)) / Fraction(
        midpoint.numerator, midpoint.denominator
    )
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF_D088, "D088", "pending", request,
        DEFINITION_D088, PARAMETER_D088, POLICY_D088, (UNIT,), MAPS,
        lines, predecessors, 0, f.ExactRatioV1(spread.numerator, spread.denominator),
        "percent", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate_d088(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact option spread occurrence required")
    f._Validated.__post_init__(value)
    if any(type(p) is not f.WindowMeasurementOccurrenceV1 for p in value.predecessors):
        raise ValueError("actual window predecessor required")
    parents = cast(tuple[f.WindowMeasurementOccurrenceV1, ...], value.predecessors)
    if canonical(value) != canonical(produce_d088(
        value.request, value.raw_input_lineage, parents, value.calculated_at_utc
    )):
        raise ValueError("option spread/source/parent/identity mismatch")


class _SpreadOwner:
    def __init__(
        self, state: RecordState, raw: f.RawProjectionReaderV1,
        predecessor: f.MeasurementWindowReadsV1, now: Callable[[], datetime],
    ) -> None:
        self.state, self.raw, self.predecessor, self.now = state, raw, predecessor, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact option spread request required")
        now = self.now()
        f._utc(now)
        try:
            request_check_d088(request, now)
            parent = self.predecessor.get_derived_occurrence(request.predecessor_occurrence_ids[0])
            if type(parent) is not f.WindowMeasurementOccurrenceV1:
                return None
            selected: list[f.RawInputLineageV1] = []
            for role, mapping in enumerate(MAPS):
                candidates = tuple(history(self.raw, request.calculation, mapping, POLICY_D088))
                if not candidates:
                    raise ValueError("missing direct option quote side")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
                    if type(item.source_timestamp_raw) is not str:
                        raise ValueError("exact option source instant required")
                    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
                    return event, item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous direct quote rank")
                selected.append(line(chosen, request.calculation, role))
            value = produce_d088(request, tuple(selected), (parent,), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner_d088(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF_D088):
        raise ValueError("exact D088 admission required")
    if (
        type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now) or predecessor is None
        or any(not callable(getattr(predecessor, name, None))
               for name in ("get_derived_occurrence", "list_derived_history"))
    ):
        raise TypeError("actual public window parent read facet required")
    return _SpreadOwner(
        RecordState(storage, _decode, validate_d088), raw,
        cast(f.MeasurementWindowReadsV1, predecessor), now,
    )


# D089 is separately admitted for the controlled C1 strike/model-spot pair.
BRIEF_D089 = "88e83eb89daf658d0e8f00115fa1262e331ba89d8e75dc98062a6f9fb4885d71"
MAPS_D089 = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw),
        PROVIDER, VARIANT, path, "USD_per_share", META,
    ) for raw, path in (("R014", ("contract", "strike")),
                        ("R118", ("model", "underlying_price")))
)
DEFINITION_D089 = f.CalculationDefinitionV1(
    "D089", "D089-OPTION-SCALAR-1", "K02_ALGEBRA", "strike/spot",
    ("R014", "R118"), (), "P_BASIC", "ratio", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER_D089 = f.CalculationParameterSetV1("mmt-d089-controlled", 1, "P_BASIC", C1, (C1,))
POLICY_D089 = replace(POLICY, context_id="mmt-d089-selection")


def request_check_d089(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D089", C1, T, T + timedelta(seconds=1),
        DEFINITION_D089.calculation_definition_version,
        f.VersionRefV1(PARAMETER_D089.context_id, 1),
        f.VersionRefV1(POLICY_D089.context_id, 1), (CONTEXT.ref,),
        tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1), C1,
        ) for mapping in MAPS_D089),
    )
    if (canonical(request.calculation) != canonical(expected)
        or request.context != CONTEXT or request.predecessor_occurrence_ids
        or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible controlled strike/spot request")


def line_d089(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
              role: int) -> f.RawInputLineageV1:
    mapping = MAPS_D089[role]
    event = eligible(replace(item, selection_identity=None), mapping, POLICY_D089, c)
    expected_identity = r.RawSelectionIdentityV1((
        ("contract.id", C1), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", "110"),
        ("option.right", "C"), ("currency.code", "USD"),
        ("contract.multiplier", "100"), ("instrument.kind", "option"),
        ("model.convention", "controlled-model/1"),
        ("value.role", "option_strike" if role == 0 else "model_underlying_price"),
    ))
    if (event != T or item.received_ts_utc != T
        or item.selection_identity != expected_identity
        or type(item.native_value) is not Decimal
        or (role == 0 and item.native_value != Decimal("110"))):
        raise ValueError("matched exact-contract strike/model spot role required")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), T,
    )


def produce_d089(request: f.WindowCalculationRequestV1,
                 lines: tuple[f.RawInputLineageV1, ...], now: datetime
                 ) -> f.WindowMeasurementOccurrenceV1:
    request_check_d089(request, now)
    if len(lines) != 2:
        raise ValueError("strike and spot both required")
    for role, actual in enumerate(lines):
        if canonical(actual) != canonical(line_d089(actual.projection, request.calculation, role)):
            raise ValueError("option strike/spot lineage mismatch")
    strike, spot = (item.canonical_value for item in lines)
    if spot == 0:
        raise ValueError("nonzero selected spot denominator required")
    ratio = Fraction(strike) / Fraction(spot)
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF_D089, "D089", "pending", request,
        DEFINITION_D089, PARAMETER_D089, POLICY_D089, (UNIT,), MAPS_D089,
        lines, (), 0, f.ExactRatioV1(ratio.numerator, ratio.denominator),
        "ratio", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate_d089(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact strike/spot occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce_d089(
        value.request, value.raw_input_lineage, value.calculated_at_utc
    )):
        raise ValueError("strike/spot source or identity mismatch")


class _MoneynessOwner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact strike/spot request required")
        now = self.now()
        f._utc(now)
        try:
            request_check_d089(request, now)
            selected: list[f.RawInputLineageV1] = []
            for role, mapping in enumerate(MAPS_D089):
                candidates = tuple(history(self.raw, request.calculation, mapping, POLICY_D089))
                if not candidates:
                    raise ValueError("missing option strike/model spot")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
                    if type(item.source_timestamp_raw) is not str:
                        raise ValueError("exact option source instant required")
                    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
                    return event, item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous strike/model spot rank")
                selected.append(line_d089(chosen, request.calculation, role))
            value = produce_d089(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner_d089(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF_D089):
        raise ValueError("exact D089 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage and clock required")
    return _MoneynessOwner(RecordState(storage, _decode, validate_d089), raw, now)


# D090 is separately admitted for the controlled C1 strike/model-spot natural logarithm.
BRIEF_D090 = "5f3f5938be58e677cd56e1a733f7a1959d6f1c64ef70d7fca5ac53af7f0514a6"
MAPS_D090 = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw),
        PROVIDER, VARIANT, path, "USD_per_share", META,
    ) for raw, path in (("R014", ("contract", "strike")),
                        ("R118", ("model", "underlying_price")))
)
DEFINITION_D090 = f.CalculationDefinitionV1(
    "D090", "D090-OPTION-SCALAR-1", "K02_ALGEBRA", "ln(strike/spot)",
    ("R014", "R118"), (), "P_BASIC", "dimensionless", "scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER_D090 = f.CalculationParameterSetV1("mmt-d090-controlled", 1, "P_BASIC", C1, (C1,))
POLICY_D090 = replace(POLICY, context_id="mmt-d090-selection")


def request_check_d090(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D090", C1, T, T + timedelta(seconds=1),
        DEFINITION_D090.calculation_definition_version,
        f.VersionRefV1(PARAMETER_D090.context_id, 1),
        f.VersionRefV1(POLICY_D090.context_id, 1), (CONTEXT.ref,),
        tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1), C1,
        ) for mapping in MAPS_D090),
    )
    if (canonical(request.calculation) != canonical(expected)
        or request.context != CONTEXT or request.predecessor_occurrence_ids
        or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible controlled strike/spot request")


def line_d090(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
              role: int) -> f.RawInputLineageV1:
    mapping = MAPS_D090[role]
    event = eligible(replace(item, selection_identity=None), mapping, POLICY_D090, c)
    expected_identity = r.RawSelectionIdentityV1((
        ("contract.id", C1), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", "110"),
        ("option.right", "C"), ("currency.code", "USD"),
        ("contract.multiplier", "100"), ("instrument.kind", "option"),
        ("model.convention", "controlled-model/1"),
        ("value.role", "option_strike" if role == 0 else "model_underlying_price"),
    ))
    if (event != T or item.received_ts_utc != T
        or item.selection_identity != expected_identity
        or type(item.native_value) is not Decimal
        or (role == 0 and item.native_value != Decimal("110"))):
        raise ValueError("matched exact-contract strike/model spot role required")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), T,
    )


def produce_d090(request: f.WindowCalculationRequestV1,
                 lines: tuple[f.RawInputLineageV1, ...], now: datetime
                 ) -> f.WindowMeasurementOccurrenceV1:
    request_check_d090(request, now)
    if len(lines) != 2:
        raise ValueError("strike and spot both required")
    for role, actual in enumerate(lines):
        if canonical(actual) != canonical(line_d090(actual.projection, request.calculation, role)):
            raise ValueError("option strike/spot lineage mismatch")
    strike, spot = (item.canonical_value for item in lines)
    if strike <= 0 or spot <= 0:
        raise ValueError("positive selected strike and spot required for logarithm")
    logarithm = _logarithm(strike, spot)
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF_D090, "D090", "pending", request,
        DEFINITION_D090, PARAMETER_D090, POLICY_D090, (UNIT,), MAPS_D090,
        lines, (), 0, logarithm,
        "dimensionless", "scalar_decimal", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate_d090(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact log-moneyness occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce_d090(
        value.request, value.raw_input_lineage, value.calculated_at_utc
    )):
        raise ValueError("log-moneyness source or identity mismatch")


class _LogMoneynessOwner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact strike/spot request required")
        now = self.now()
        f._utc(now)
        try:
            request_check_d090(request, now)
            selected: list[f.RawInputLineageV1] = []
            for role, mapping in enumerate(MAPS_D090):
                candidates = tuple(history(self.raw, request.calculation, mapping, POLICY_D090))
                if not candidates:
                    raise ValueError("missing option strike/model spot")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
                    if type(item.source_timestamp_raw) is not str:
                        raise ValueError("exact option source instant required")
                    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
                    return event, item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous strike/model spot rank")
                selected.append(line_d090(chosen, request.calculation, role))
            value = produce_d090(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner_d090(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF_D090):
        raise ValueError("exact D090 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage and clock required")
    return _LogMoneynessOwner(RecordState(storage, _decode, validate_d090), raw, now)


# D092 is separately admitted for the controlled C1 quote-side IV pair.
BRIEF_D092 = "2814b991a8c2b4c07e573716cc81d0684b65e69dc2bdc264539d895db4692642"
UNIT_D092 = f.UnitConventionVersionV1(
    "mmt-option-iv", 1, "annualised_decimal_volatility",
    "annualised_decimal_volatility", Decimal("1"), Decimal("0"),
)
MAPS_D092 = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + raw.lower() + "-option", 1, r.RawSignalCatalogueId(raw),
        PROVIDER, VARIANT, path, "annualised_decimal_volatility", META,
    ) for raw, path in (("R084", ("bid_model", "iv")),
                        ("R093", ("ask_model", "iv")))
)
DEFINITION_D092 = f.CalculationDefinitionV1(
    "D092", "D092-OPTION-SCALAR-1", "K02_ALGEBRA", "(bid_iv+ask_iv)/2",
    ("R084", "R093"), (), "P_BASIC", "volatility", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER_D092 = f.CalculationParameterSetV1("mmt-d092-controlled", 1, "P_BASIC", C1, (C1,))
POLICY_D092 = replace(POLICY, context_id="mmt-d092-selection")


def request_check_d092(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D092", C1, T, T + timedelta(seconds=1),
        DEFINITION_D092.calculation_definition_version,
        f.VersionRefV1(PARAMETER_D092.context_id, 1),
        f.VersionRefV1(POLICY_D092.context_id, 1), (CONTEXT.ref,),
        tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT_D092.context_id, 1), C1,
        ) for mapping in MAPS_D092),
    )
    if (canonical(request.calculation) != canonical(expected)
        or request.context != CONTEXT or request.predecessor_occurrence_ids
        or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible controlled IV midpoint request")


def line_d092(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
              role: int) -> f.RawInputLineageV1:
    mapping = MAPS_D092[role]
    event = eligible(replace(item, selection_identity=None), mapping, POLICY_D092, c)
    expected_identity = r.RawSelectionIdentityV1((
        ("contract.id", C1), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", "110"),
        ("option.right", "C"), ("currency.code", "USD"),
        ("contract.multiplier", "100"), ("instrument.kind", "option"),
        ("model.convention", "controlled-model/1"),
        ("value.role", "bid_iv" if role == 0 else "ask_iv"),
    ))
    if (event != T or item.received_ts_utc != T
        or item.selection_identity != expected_identity
        or type(item.native_value) is not Decimal
        or item.native_value < 0):
        raise ValueError("matched exact-contract bid/ask IV role required")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT_D092.context_id, 1),
        item, cast(Decimal, item.native_value), T,
    )


def produce_d092(request: f.WindowCalculationRequestV1,
                 lines: tuple[f.RawInputLineageV1, ...], now: datetime
                 ) -> f.WindowMeasurementOccurrenceV1:
    request_check_d092(request, now)
    if len(lines) != 2:
        raise ValueError("bid and ask IV both required")
    for role, actual in enumerate(lines):
        if canonical(actual) != canonical(line_d092(actual.projection, request.calculation, role)):
            raise ValueError("option IV lineage mismatch")
    bid_iv, ask_iv = (item.canonical_value for item in lines)
    ratio = (Fraction(bid_iv) + Fraction(ask_iv)) / 2
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF_D092, "D092", "pending", request,
        DEFINITION_D092, PARAMETER_D092, POLICY_D092, (UNIT_D092,), MAPS_D092,
        lines, (), 0, f.ExactRatioV1(ratio.numerator, ratio.denominator),
        "volatility", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate_d092(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact IV midpoint occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce_d092(
        value.request, value.raw_input_lineage, value.calculated_at_utc
    )):
        raise ValueError("IV midpoint source or identity mismatch")


class _IvMidpointOwner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact IV midpoint request required")
        now = self.now()
        f._utc(now)
        try:
            request_check_d092(request, now)
            selected: list[f.RawInputLineageV1] = []
            for role, mapping in enumerate(MAPS_D092):
                candidates = tuple(history(self.raw, request.calculation, mapping, POLICY_D092))
                if not candidates:
                    raise ValueError("missing option bid/ask IV")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
                    if type(item.source_timestamp_raw) is not str:
                        raise ValueError("exact option source instant required")
                    event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
                    return event, item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous bid/ask IV rank")
                selected.append(line_d092(chosen, request.calculation, role))
            value = produce_d092(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner_d092(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF_D092):
        raise ValueError("exact D092 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage and clock required")
    return _IvMidpointOwner(RecordState(storage, _decode, validate_d092), raw, now)
