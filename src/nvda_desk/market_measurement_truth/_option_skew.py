"""D099 exact native delta and categorical right matched option skew."""

from __future__ import annotations

import re
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
from ._option_scalars import CONTEXT, META, PROVIDER, VARIANT, T
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "ab854fdd6a9a34c431c977fa973e392592be1e0d21854f4c95324852ed4f95a7"
A = T - timedelta(seconds=300)
EXPIRIES = {"E1": "2026-10-23", "E2": "2026-10-30"}
TAGS = ("C25", "P25")
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-" + name.lower() + "-option", 1, r.RawSignalCatalogueId(name),
    PROVIDER, VARIANT, path, unit, META,
) for name, path, unit in (
    ("R111", ("model", "iv"), "annualised_decimal_volatility"),
    ("R112", ("model", "delta"), "delta_fraction"),
    ("R015", ("contract", "right"), "option_right"),
))
UNITS = tuple(f.UnitConventionVersionV1(
    name, 1, unit, unit, Decimal(1), Decimal(0),
) for name, unit in (
    ("mmt-option-iv", "annualised_decimal_volatility"),
    ("mmt-option-delta", "delta_fraction"),
    ("mmt-option-right", "option_right"),
))
DEFINITION = f.CalculationDefinitionV1(
    "D099", "D099-NATIVE-DELTA-SKEW-1", "K02_ALGEBRA", "100*(put_iv-call_iv)",
    ("R111", "R112", "R015"), (), "P_BASIC", "volatility_points", "option_skew",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)


def domain(request: f.WindowCalculationRequestV1, now: datetime
           ) -> tuple[str, f.CalculationParameterSetV1, f.InputSelectionPolicyVersionV1]:
    c = request.calculation
    matches = [key for key, expiry in EXPIRIES.items()
               if c.subject_instrument == f"NVDA_SKEW_{expiry}"]
    if len(matches) != 1 or c.as_of_utc not in (A, T):
        raise ValueError("unsupported exact skew expiry/frame")
    key = matches[0]
    expiry = EXPIRIES[key]
    members = tuple(f"controlled-skew-{expiry}-{tag}" for tag in TAGS)
    parameter = f.CalculationParameterSetV1(
        f"mmt-d099-{key}-controlled", 1, "P_BASIC", c.subject_instrument, members,
    )
    policy = f.InputSelectionPolicyVersionV1(
        f"mmt-d099-{key}-selection", 1,
        ("subject_instrument", "contract.id", "underlying.id", "expiry.date",
         "strike.key", "option.right", "currency.code", "contract.multiplier",
         "model.convention"),
        timedelta(seconds=60), timedelta(0), ("true_instant",), members,
        PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
    )
    expected = f.CalculationRequestV1(
        "D099", c.subject_instrument, c.as_of_utc, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version, f.VersionRefV1(parameter.context_id, 1),
        f.VersionRefV1(policy.context_id, 1), (CONTEXT.ref,),
        tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value,
            f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(UNITS[role].context_id, 1), member,
        ) for member in members for role, mapping in enumerate(MAPS)),
    )
    if (canonical(c) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids or now < c.knowledge_cutoff_utc):
        raise ValueError("incompatible exact skew request")
    return expiry, parameter, policy


def source_identity(member: str, expiry: str, tag: str, role: int
                    ) -> r.RawSelectionIdentityV1:
    return r.RawSelectionIdentityV1((
        ("contract.id", member), ("underlying.id", "NVDA"),
        ("expiry.date", expiry), ("strike.key", "120" if tag == "C25" else "100"),
        ("option.right", "C" if tag == "C25" else "P"),
        ("currency.code", "USD"), ("contract.multiplier", "100"),
        ("instrument.kind", "option"), ("model.convention", "controlled-model/1"),
        ("value.role", ("model_iv", "model_delta", "option_right")[role]),
    ))


def source_event(item: r.ProjectedRawValueV1) -> datetime:
    raw = item.source_timestamp_raw
    if type(raw) is not str or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z", raw
    ):
        raise ValueError("exact UTC source instant required")
    event = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    f._utc(event)
    return event


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
         policy: f.InputSelectionPolicyVersionV1, member: str, expiry: str,
         tag: str, role: int) -> f.RawInputLineageV1 | f.OptionRightLineageV1:
    mapping = MAPS[role]
    own_request = replace(c, subject_instrument=member)
    if (type(item) is not r.ProjectedRawValueV1
        or item.subject_instrument != member
        or item.selection_identity != source_identity(member, expiry, tag, role)
        or item.received_ts_utc != c.as_of_utc
        or source_event(item) != c.as_of_utc):
        raise ValueError("incomplete exact member/source snapshot")
    if role < 2:
        event = eligible(replace(item, selection_identity=None), mapping, policy, own_request)
        if event != c.as_of_utc or type(item.native_value) is not Decimal:
            raise ValueError("invalid numeric option source")
        number = cast(Decimal, item.native_value)
        if ((role == 0 and number < 0)
            or (role == 1 and number != (Decimal(".25") if tag == "C25" else Decimal("-.25")))):
            raise ValueError("invalid IV or exact signed native delta")
        return f.RawInputLineageV1(
            mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(UNITS[role].context_id, 1),
            item, number, event,
        )
    # The categorical source is checked locally: the general eligibility helper is numeric-only.
    if (type(item.raw_signal_catalogue_id) is not r.RawSignalCatalogueId
        or item.raw_signal_catalogue_id != mapping.raw_signal_catalogue_id
        or item.projection_mapping_id != mapping.mapping_id
        or type(item.projection_mapping_version) is not int
        or item.projection_mapping_version != mapping.version
        or item.native_field_path != mapping.native_field_path
        or item.native_units != mapping.native_units
        or item.source_provider != policy.source_provider
        or item.source_variant != policy.source_variant
        or item.ingestion_sequence_scope.value != policy.ingestion_sequence_scope
        or type(item.ingestion_sequence) is not int
        or item.source_temporal_kind != "true_instant"
        or item.source_timezone_native != "UTC"
        or item.revision_vintage_native is not None
        or type(item.native_value) is not str
        or item.native_value != ("C" if tag == "C25" else "P")):
        raise ValueError("actual native R015 side/source mismatch")
    return f.OptionRightLineageV1(
        "R015", item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1), mapping, item,
        cast(str, item.native_value), cast(str, item.native_value), "option_right",
        c.as_of_utc,
    )


def produce(request: f.WindowCalculationRequestV1,
            numeric: tuple[f.RawInputLineageV1, ...],
            rights: tuple[f.OptionRightLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    expiry, parameter, policy = domain(request, now)
    if len(numeric) != 4 or len(rights) != 2:
        raise ValueError("complete call/put IV/delta/right evidence required")
    for index, (tag, member) in enumerate(zip(TAGS, parameter.members, strict=True)):
        for role in range(3):
            actual = numeric[2 * index + role] if role < 2 else rights[index]
            if type(actual) is not (f.RawInputLineageV1 if role < 2 else f.OptionRightLineageV1):
                raise TypeError("incorrect typed source lineage")
            expected = line(actual.projection, request.calculation, policy, member, expiry,
                            tag, role)
            if canonical(actual) != canonical(expected):
                raise ValueError("skew selected source lineage mismatch")
    difference = 100 * (Fraction(numeric[2].canonical_value)
                        - Fraction(numeric[0].canonical_value))
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D099", "pending", request, DEFINITION,
        parameter, policy, UNITS, MAPS, numeric, (), 0,
        f.OptionSkewV1(f.ExactRatioV1(difference.numerator, difference.denominator), rights),
        "volatility_points", "option_skew", request.calculation.as_of_utc,
        request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact skew occurrence required")
    f._Validated.__post_init__(value)
    if type(value.result) is not f.OptionSkewV1 or canonical(value) != canonical(produce(
        value.request, value.raw_input_lineage, value.result.native_right_lineage,
        value.calculated_at_utc,
    )):
        raise ValueError("skew source/result/identity mismatch")


def choose(items: tuple[r.ProjectedRawValueV1, ...]) -> r.ProjectedRawValueV1:
    if not items:
        raise ValueError("missing exact option role")
    def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
        if type(item.source_timestamp_raw) is not str:
            raise ValueError("exact option timestamp required")
        event = source_event(item)
        return event, item.received_ts_utc, item.ingestion_sequence
    selected = max(items, key=rank)
    if sum(rank(item) == rank(selected) for item in items) != 1:
        raise ValueError("ambiguous option source rank")
    return selected


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact skew request required")
        now = self.now()
        f._utc(now)
        try:
            expiry, parameter, policy = domain(request, now)
            numeric: list[f.RawInputLineageV1] = []
            rights: list[f.OptionRightLineageV1] = []
            for tag, member in zip(TAGS, parameter.members, strict=True):
                own_request = replace(request.calculation, subject_instrument=member)
                for role, mapping in enumerate(MAPS):
                    candidates = tuple(history(self.raw, own_request, mapping, policy))
                    selected = choose(tuple(item for item in candidates
                        if item.selection_identity == source_identity(member, expiry, tag, role)
                        and source_event(item) == request.calculation.as_of_utc
                    ))
                    actual = line(selected, request.calculation, policy, member, expiry, tag, role)
                    if role == 2:
                        rights.append(cast(f.OptionRightLineageV1, actual))
                    else:
                        numeric.append(cast(f.RawInputLineageV1, actual))
            result = produce(request, tuple(numeric), tuple(rights), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(result))


def build_owner(admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
                predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D099 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
