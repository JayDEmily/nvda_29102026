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
