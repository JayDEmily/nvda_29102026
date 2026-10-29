"""D124 complete strike/expiry open-interest concentration."""
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

# D124 owns an exact grouped OI basket and typed concentration result.
BRIEF_D124 = "de019a62f030ebe9380a53072ec20dad64493531f43d0b7c8910ae1d8bd719a1"
SUBJECT_D124 = "NVDA_OI_CONCENTRATION_E1"
TAGS_D124 = ("100-C", "105-C", "100-P", "105-P")
MEMBERS_D124 = tuple(f"controlled-oi-E1-{tag}" for tag in TAGS_D124)
STRIKES_D124 = ("100", "105", "100", "105")
PROVIDER_D124, VARIANT_D124 = "foundation-controlled-option-activity", "member_oi_concentration_v1"
META_D124 = (
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
MAPS_D124 = (
    r.RawSignalProjectionMappingV1(
        "mmt-r047-member-call-oi", 1, r.RawSignalCatalogueId("R047"),
        PROVIDER_D124, VARIANT_D124, ("oi", "call"), "contracts", META_D124,
    ),
    r.RawSignalProjectionMappingV1(
        "mmt-r048-member-put-oi", 1, r.RawSignalCatalogueId("R048"),
        PROVIDER_D124, VARIANT_D124, ("oi", "put"), "contracts", META_D124,
    ),
)
UNIT = f.UnitConventionVersionV1("mmt-option-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
POLICY_D124 = f.InputSelectionPolicyVersionV1(
    "mmt-d124-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "source.mode",
     "official.period_id", "official.revision_id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), MEMBERS_D124,
    PROVIDER_D124, VARIANT_D124, PROVIDER_D124 + "/" + VARIANT_D124, 100, 1000,
)
DEFINITION_D124 = f.CalculationDefinitionV1(
    "D124", "D124-STRIKE-EXPIRY-OI-HHI-1", "K08_RULE_BUCKET_POLICY",
    "strike_expiry shares and sum of squared shares", ("R047", "R048"), (),
    "P_BASIC", "concentration", "strike_expiry_hhi",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER_D124 = f.CalculationParameterSetV1(
    "mmt-d124-controlled", 1, "P_BASIC", SUBJECT_D124, MEMBERS_D124,
)


def request_check_d124(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D124", SUBJECT_D124, T, T + timedelta(seconds=1),
        DEFINITION_D124.calculation_definition_version,
        f.VersionRefV1(PARAMETER_D124.context_id, 1),
        f.VersionRefV1(POLICY_D124.context_id, 1), (CONTEXT.ref,),
        tuple(f.RawInputBindingV1(
            MAPS_D124[index // 2].raw_signal_catalogue_id.value,
            f.VersionRefV1(MAPS_D124[index // 2].mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), member,
        ) for index, member in enumerate(MEMBERS_D124)),
    )
    if (canonical(request.calculation) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible complete D124 E1 basket request")


def expected_identity_d124(index: int, period: str) -> r.RawSelectionIdentityV1:
    if index not in range(4):
        raise ValueError("unadmitted member")
    call = index < 2
    return r.RawSelectionIdentityV1((
        ("contract.id", MEMBERS_D124[index]), ("underlying.id", "NVDA"),
        ("expiry.date", "2026-10-23"), ("strike.key", STRIKES_D124[index]),
        ("option.right", "C" if call else "P"),
        ("currency.code", "USD"), ("contract.multiplier", "100"),
        ("instrument.kind", "option"), ("source.mode", "controlled_real_time"),
        ("session.id", "controlled-option-20oct12-13Z"),
        ("official.period_id", period),
        ("official.revision_id", "controlled-oi-revision/1"),
        ("value.role", "call_oi" if call else "put_oi"),
    ))


def candidate_d124(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
                   index: int) -> bool:
    member = MEMBERS_D124[index]
    mapping = MAPS_D124[index // 2]
    own = replace(c, subject_instrument=member)
    identity = item.selection_identity
    if identity is None:
        return False
    try:
        period = identity.value_for("official.period_id")
    except (ValueError, KeyError):
        return False
    return (type(period) is str and period == "controlled-oi-period-20261020/1"
            and item.selection_identity == expected_identity_d124(index, period)
            and eligible(replace(item, selection_identity=None), mapping, POLICY_D124, own)
            == T)


def line_d124(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
              index: int) -> f.RawInputLineageV1:
    mapping = MAPS_D124[index // 2]
    if (not candidate_d124(item, c, index) or item.received_ts_utc != T
        or type(item.native_value) is not Decimal or item.native_value < 0):
        raise ValueError("missing exact nonnegative per-contract official OI")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), T,
    )


def produce_d124(request: f.WindowCalculationRequestV1,
                 lines: tuple[f.RawInputLineageV1, ...], now: datetime
                 ) -> f.WindowMeasurementOccurrenceV1:
    request_check_d124(request, now)
    if len(lines) != 4:
        raise ValueError("all four configured contract members required")
    for index, actual in enumerate(lines):
        if (type(actual) is not f.RawInputLineageV1
            or canonical(actual) != canonical(line_d124(actual.projection,
                                                         request.calculation, index))):
            raise ValueError("D124 exact member/source/order mismatch")
    periods = tuple(line.projection.selection_identity.value_for("official.period_id")
                    for line in lines if line.projection.selection_identity is not None)
    if periods != ("controlled-oi-period-20261020/1",) * 4:
        raise ValueError("mixed official OI reporting periods")
    groups = (sum((Fraction(lines[i].canonical_value) for i in (0, 2)), Fraction()),
              sum((Fraction(lines[i].canonical_value) for i in (1, 3)), Fraction()))
    total = sum(groups, Fraction())
    if total <= 0:
        raise ValueError("positive complete OI denominator required")
    shares = tuple(group / total for group in groups)
    concentration = f.OIConcentrationV1(
        (("2026-10-23", "100"), ("2026-10-23", "105")),
        tuple(f.ExactRatioV1(share.numerator, share.denominator) for share in shares),
        f.ExactRatioV1((sum((share * share for share in shares), Fraction())).numerator,
                       (sum((share * share for share in shares), Fraction())).denominator),
    )
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF_D124, "D124", "pending", request, DEFINITION_D124,
        PARAMETER_D124, POLICY_D124, (UNIT,), MAPS_D124, lines, (), 0,
        concentration, "concentration", "strike_expiry_hhi",
        T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate_d124(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact D124 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce_d124(value.request, value.raw_input_lineage,
                                                  value.calculated_at_utc)):
        raise ValueError("D124 source/result/identity mismatch")


class _OwnerD124:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact D124 request required")
        now = self.now()
        f._utc(now)
        try:
            request_check_d124(request, now)
            selected = []
            for index, member in enumerate(MEMBERS_D124):
                mapping = MAPS_D124[index // 2]
                own_request = replace(request.calculation, subject_instrument=member)
                candidates = tuple(item for item in history(self.raw, own_request,
                                                              mapping, POLICY_D124)
                                   if candidate_d124(item, request.calculation, index))
                if not candidates:
                    raise ValueError("missing configured basket member")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
                    return source_event(item), item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous official per-contract OI")
                selected.append(line_d124(chosen, request.calculation, index))
            result = produce_d124(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(result))


def build_owner_d124(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF_D124):
        raise ValueError("exact D124 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _OwnerD124(RecordState(storage, _decode, validate_d124), raw, now)
