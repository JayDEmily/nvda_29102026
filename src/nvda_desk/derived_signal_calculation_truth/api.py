"""Typed public foundation seam for Derived Signal Calculation Truth."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, Protocol, cast

if TYPE_CHECKING:
    from ._stage1 import KernelValueV1


def _require_non_empty_string(value: str, field_name: str) -> None:
    if type(value) is not str or not value:
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_positive_version(value: int, field_name: str = "version") -> None:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")


def _require_utc(value: datetime, field_name: str) -> None:
    if type(value) is not datetime:
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError(f"{field_name} must be UTC-aware")


def _require_derived_signal_id(value: str) -> None:
    if type(value) is not str or len(value) != 4 or value[0] != "D" or not value[1:].isdigit():
        raise ValueError("derived_signal_id must be canonical DNNN form")
    if not 1 <= int(value[1:]) <= 209:
        raise ValueError("derived_signal_id must be in D001-D209")


def _require_raw_signal_id(value: str) -> None:
    if type(value) is not str or len(value) != 4 or value[0] != "R" or not value[1:].isdigit():
        raise ValueError("raw_signal_id must be canonical RNNN form")
    if not 1 <= int(value[1:]) <= 323:
        raise ValueError("raw_signal_id must be in R001-R323")


def _require_version_refs(value: tuple[VersionRefV1, ...], field_name: str) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{field_name} must be a tuple")
    keys: list[tuple[str, int]] = []
    for item in value:
        if type(item) is not VersionRefV1:
            raise TypeError(f"{field_name} must contain exact VersionRefV1 values")
        keys.append((item.context_id, item.version))
    if len(keys) != len(set(keys)):
        raise ValueError(f"{field_name} must not contain duplicate identity/version references")


def _require_raw_lineage(value: tuple[RawInputLineageV1, ...], field_name: str) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{field_name} must be a tuple")
    for item in value:
        if type(item) is not RawInputLineageV1:
            raise TypeError(f"{field_name} must contain exact RawInputLineageV1 values")


def _require_non_empty_distinct_strings(value: tuple[str, ...], field_name: str) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{field_name} must be a tuple")
    for item in value:
        _require_non_empty_string(item, field_name)
    if len(value) != len(set(value)):
        raise ValueError(f"{field_name} must contain distinct values")


def _require_derived_result(value: DerivedResultV1, field_name: str = "result") -> None:
    if value is None:
        raise ValueError(f"{field_name} must contain a persisted value; absence is not a result")
    if type(value) in {bool, int, Decimal, str}:
        if type(value) is str and not value:
            raise ValueError(f"{field_name} string values must be non-empty")
        return
    if type(value) is datetime:
        if value.tzinfo is None:
            raise ValueError(f"{field_name} datetime values must be timezone-aware")
        return
    if type(value) is date:
        return
    if type(value) is tuple:
        for item in value:
            _require_derived_result(item, field_name)  # type: ignore[arg-type]
        return
    raise TypeError(f"{field_name} contains a value outside DerivedResultV1")


@dataclass(frozen=True, slots=True)
class _VersionedContextV1:
    context_id: str
    version: int

    def __post_init__(self) -> None:
        _require_non_empty_string(self.context_id, "context_id")
        _require_positive_version(self.version)


type ImmutableContextScalarV1 = bool | int | Decimal | str | datetime | timedelta
type ImmutableContextValueV1 = ImmutableContextScalarV1 | tuple[ImmutableContextScalarV1, ...]


def _require_tuple(value: object, field_name: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{field_name} must be a tuple")
    return value


def _require_string_tuple(
    value: tuple[str, ...], field_name: str, *, non_empty: bool = False, distinct: bool = False
) -> None:
    _require_tuple(value, field_name)
    if non_empty and not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _require_non_empty_string(item, field_name)
    if distinct and len(set(value)) != len(value):
        raise ValueError(f"{field_name} must contain distinct values")


def _require_decimal(value: Decimal, field_name: str, *, positive: bool = False) -> None:
    if type(value) is not Decimal:
        raise TypeError(f"{field_name} must be a Decimal")
    if positive and value <= 0:
        raise ValueError(f"{field_name} must be positive")


def _require_decimal_tuple(
    value: tuple[Decimal, ...],
    field_name: str,
    *,
    non_empty: bool = False,
    non_zero: bool = False,
    positive: bool = False,
) -> None:
    _require_tuple(value, field_name)
    if non_empty and not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _require_decimal(item, field_name)
        if non_zero and item == 0:
            raise ValueError(f"{field_name} values must be non-zero")
        if positive and item <= 0:
            raise ValueError(f"{field_name} values must be positive")


def _require_immutable_context_value(value: ImmutableContextValueV1, field_name: str) -> None:
    if type(value) in {bool, int, Decimal, str, timedelta}:
        if type(value) is str and not value:
            raise ValueError(f"{field_name} string values must be non-empty")
        return
    if type(value) is datetime:
        _require_utc(value, field_name)
        return
    if type(value) is tuple:
        for item in value:
            if type(item) not in {bool, int, Decimal, str, datetime, timedelta}:
                raise TypeError(f"{field_name} tuple values must contain immutable scalar values")
            _require_immutable_context_value(item, field_name)
        return
    raise TypeError(f"{field_name} must contain only admitted immutable context values")


def _require_named_context_values(
    value: tuple[tuple[str, ImmutableContextValueV1], ...],
    field_name: str,
    *,
    non_empty: bool = False,
) -> None:
    _require_tuple(value, field_name)
    if non_empty and not value:
        raise ValueError(f"{field_name} must not be empty")
    names: list[str] = []
    for item in value:
        if type(item) is not tuple or len(item) != 2:
            raise TypeError(f"{field_name} entries must be (name, value) tuples")
        name, configured = item
        _require_non_empty_string(name, field_name)
        _require_immutable_context_value(configured, field_name)
        names.append(name)
    if len(set(names)) != len(names):
        raise ValueError(f"{field_name} names must be distinct")


def _require_named_decimal_values(
    value: tuple[tuple[str, Decimal], ...], field_name: str, *, non_negative: bool = False
) -> None:
    _require_tuple(value, field_name)
    names: list[str] = []
    for item in value:
        if type(item) is not tuple or len(item) != 2:
            raise TypeError(f"{field_name} entries must be (name, Decimal) tuples")
        name, amount = item
        _require_non_empty_string(name, field_name)
        _require_decimal(amount, field_name)
        if non_negative and amount < 0:
            raise ValueError(f"{field_name} amounts must be non-negative")
        names.append(name)
    if len(set(names)) != len(names):
        raise ValueError(f"{field_name} names must be distinct")


def _require_non_negative_timedelta(value: timedelta, field_name: str) -> None:
    if type(value) is not timedelta:
        raise TypeError(f"{field_name} must be a timedelta")
    if value < timedelta(0):
        raise ValueError(f"{field_name} must be non-negative")


@dataclass(frozen=True, slots=True)
class ScoreFeatureV1:
    signal_id: str
    extractor: str
    extractor_arguments: tuple[ImmutableContextScalarV1, ...]
    transform: str
    transform_scale: Decimal | None
    orientation: int
    weight: Decimal
    clip_min: Decimal | None
    clip_max: Decimal | None
    baseline_values: tuple[Decimal, ...]

    def __post_init__(self) -> None:
        _require_derived_signal_id(self.signal_id)
        _require_non_empty_string(self.extractor, "extractor")
        _require_tuple(self.extractor_arguments, "extractor_arguments")
        for item in self.extractor_arguments:
            _require_immutable_context_value(item, "extractor_arguments")
        _require_non_empty_string(self.transform, "transform")
        if self.transform_scale is not None:
            _require_decimal(self.transform_scale, "transform_scale")
        if type(self.orientation) is not int or self.orientation not in {-1, 1}:
            raise ValueError("orientation must be -1 or +1")
        _require_decimal(self.weight, "weight")
        if self.weight < 0:
            raise ValueError("weight must be non-negative")
        if self.clip_min is not None:
            _require_decimal(self.clip_min, "clip_min")
        if self.clip_max is not None:
            _require_decimal(self.clip_max, "clip_max")
        if (
            self.clip_min is not None
            and self.clip_max is not None
            and self.clip_min > self.clip_max
        ):
            raise ValueError("clip_min must not exceed clip_max")
        _require_decimal_tuple(self.baseline_values, "baseline_values")


@dataclass(frozen=True, slots=True)
class CalculationParameterSetV1(_VersionedContextV1):
    profile: str
    parameters: tuple[tuple[str, ImmutableContextValueV1], ...]
    score_features: tuple[ScoreFeatureV1, ...] = ()

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_non_empty_string(self.profile, "profile")
        _require_named_context_values(self.parameters, "parameters", non_empty=True)
        _require_tuple(self.score_features, "score_features")
        for feature in self.score_features:
            if type(feature) is not ScoreFeatureV1:
                raise TypeError("score_features must contain exact ScoreFeatureV1 values")
        ids = tuple(feature.signal_id for feature in self.score_features)
        if len(ids) != len(set(ids)):
            raise ValueError("score_features must contain distinct signal identities")


@dataclass(frozen=True, slots=True)
class RequiredFieldPolicyV1(_VersionedContextV1):
    requirements: tuple[str, ...]

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_string_tuple(self.requirements, "requirements", non_empty=True, distinct=True)


@dataclass(frozen=True, slots=True)
class CandidateStructureContextV1(_VersionedContextV1):
    candidate_identity: str
    leg_contract_identities: tuple[str, ...]
    leg_sides: tuple[str, ...]
    leg_quantities: tuple[Decimal, ...]
    quantity: Decimal
    premium_assumptions: tuple[tuple[str, Decimal], ...]
    entry_assumptions: tuple[tuple[str, ImmutableContextValueV1], ...]
    risk_capital_currency: Decimal

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_non_empty_string(self.candidate_identity, "candidate_identity")
        _require_string_tuple(
            self.leg_contract_identities, "leg_contract_identities", non_empty=True, distinct=True
        )
        _require_string_tuple(self.leg_sides, "leg_sides", non_empty=True)
        _require_decimal_tuple(self.leg_quantities, "leg_quantities", non_empty=True, non_zero=True)
        if not (
            len(self.leg_contract_identities) == len(self.leg_sides) == len(self.leg_quantities)
        ):
            raise ValueError("candidate leg contract, side and quantity tuples must align")
        _require_decimal(self.quantity, "quantity", positive=True)
        _require_named_decimal_values(self.premium_assumptions, "premium_assumptions")
        _require_named_context_values(self.entry_assumptions, "entry_assumptions")
        _require_decimal(self.risk_capital_currency, "risk_capital_currency", positive=True)


@dataclass(frozen=True, slots=True)
class CandidateSetContextV1(_VersionedContextV1):
    candidate_identities: tuple[str, ...]
    eligibility_classes: tuple[tuple[str, str], ...]
    neighbour_relations: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_string_tuple(
            self.candidate_identities, "candidate_identities", non_empty=True, distinct=True
        )
        _require_tuple(self.eligibility_classes, "eligibility_classes")
        eligibility: dict[str, str] = {}
        for item in self.eligibility_classes:
            if type(item) is not tuple or len(item) != 2:
                raise TypeError(
                    "eligibility_classes entries must be (candidate_identity, class) tuples"
                )
            candidate_identity, eligibility_class = item
            _require_non_empty_string(candidate_identity, "eligibility candidate_identity")
            _require_non_empty_string(eligibility_class, "eligibility_class")
            if candidate_identity in eligibility:
                raise ValueError("eligibility_classes must map each candidate at most once")
            eligibility[candidate_identity] = eligibility_class
        if tuple(eligibility) != self.candidate_identities:
            raise ValueError(
                "eligibility_classes must cover candidate_identities in exact candidate order"
            )
        _require_tuple(self.neighbour_relations, "neighbour_relations")
        seen_relations: set[tuple[str, str]] = set()
        admitted = set(self.candidate_identities)
        for item in self.neighbour_relations:
            if type(item) is not tuple or len(item) != 2:
                raise TypeError("neighbour_relations entries must be directed identity pairs")
            left, right = item
            _require_non_empty_string(left, "neighbour relation identity")
            _require_non_empty_string(right, "neighbour relation identity")
            if left == right:
                raise ValueError("neighbour relation may not be self-referential")
            if left not in admitted or right not in admitted:
                raise ValueError(
                    "neighbour relation identities must belong to candidate_identities"
                )
            if item in seen_relations:
                raise ValueError("neighbour_relations must be distinct")
            seen_relations.add(item)


@dataclass(frozen=True, slots=True)
class LivePositionContextV1(_VersionedContextV1):
    position_identity: str
    leg_contract_identities: tuple[str, ...]
    signed_quantities: tuple[Decimal, ...]
    multipliers: tuple[Decimal, ...]
    m00_occurrence_refs: tuple[str, ...]
    current_state_occurrence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_non_empty_string(self.position_identity, "position_identity")
        _require_string_tuple(
            self.leg_contract_identities, "leg_contract_identities", non_empty=True
        )
        _require_decimal_tuple(
            self.signed_quantities, "signed_quantities", non_empty=True, non_zero=True
        )
        _require_decimal_tuple(self.multipliers, "multipliers", non_empty=True, positive=True)
        if not (
            len(self.leg_contract_identities)
            == len(self.signed_quantities)
            == len(self.multipliers)
        ):
            raise ValueError(
                "live-position leg contract, quantity and multiplier tuples must align"
            )
        _require_string_tuple(
            self.m00_occurrence_refs, "m00_occurrence_refs", non_empty=True, distinct=True
        )
        _require_string_tuple(
            self.current_state_occurrence_refs,
            "current_state_occurrence_refs",
            non_empty=True,
            distinct=True,
        )


@dataclass(frozen=True, slots=True)
class OrderIntentContextV1(_VersionedContextV1):
    side: str
    intended_size: Decimal
    urgency: str

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_non_empty_string(self.side, "side")
        _require_decimal(self.intended_size, "intended_size", positive=True)
        _require_non_empty_string(self.urgency, "urgency")


@dataclass(frozen=True, slots=True)
class EntryStateContextV1(_VersionedContextV1):
    d155_occurrence_id: str

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_non_empty_string(self.d155_occurrence_id, "d155_occurrence_id")


@dataclass(frozen=True, slots=True)
class EvaluationSetV1(_VersionedContextV1):
    forecast_occurrence_ids: tuple[str, ...]
    realised_outcome_definition: str
    evaluation_window_start_utc: datetime
    evaluation_window_end_utc: datetime
    comparator_baseline: str
    locked_model_id: str
    locked_model_version: str

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_string_tuple(
            self.forecast_occurrence_ids, "forecast_occurrence_ids", non_empty=True, distinct=True
        )
        _require_non_empty_string(self.realised_outcome_definition, "realised_outcome_definition")
        _require_utc(self.evaluation_window_start_utc, "evaluation_window_start_utc")
        _require_utc(self.evaluation_window_end_utc, "evaluation_window_end_utc")
        if self.evaluation_window_end_utc <= self.evaluation_window_start_utc:
            raise ValueError("evaluation window end must be after its start")
        _require_non_empty_string(self.comparator_baseline, "comparator_baseline")
        _require_non_empty_string(self.locked_model_id, "locked_model_id")
        _require_non_empty_string(self.locked_model_version, "locked_model_version")


@dataclass(frozen=True, slots=True)
class RecalculationScheduleV1(_VersionedContextV1):
    trigger_rules: tuple[str, ...]

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_string_tuple(self.trigger_rules, "trigger_rules", non_empty=True, distinct=True)


@dataclass(frozen=True, slots=True)
class UnitConventionVersionV1(_VersionedContextV1):
    native_units: str
    canonical_units: str
    scale: Decimal
    offset: Decimal

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_non_empty_string(self.native_units, "native_units")
        _require_non_empty_string(self.canonical_units, "canonical_units")
        if type(self.scale) is not Decimal or type(self.offset) is not Decimal:
            raise TypeError("scale and offset must be Decimal values")

    def convert(self, value: Decimal, *, native_units: str) -> Decimal:
        if native_units != self.native_units:
            raise ValueError("native_units does not match this unit convention")
        if type(value) is not Decimal:
            raise TypeError("value must be Decimal")
        return value * self.scale + self.offset


@dataclass(frozen=True, slots=True)
class PnLConventionVersionV1(_VersionedContextV1):
    provider_pnl_components_included: tuple[str, ...]
    provider_pnl_components_excluded: tuple[str, ...]
    observed_total_pnl_is_gross_of_execution_costs: bool
    attribution_units: str

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_string_tuple(
            self.provider_pnl_components_included,
            "provider_pnl_components_included",
            distinct=True,
        )
        _require_string_tuple(
            self.provider_pnl_components_excluded,
            "provider_pnl_components_excluded",
            distinct=True,
        )
        if not self.provider_pnl_components_included and not self.provider_pnl_components_excluded:
            raise ValueError(
                "PnL convention must state at least one inclusion or exclusion component"
            )
        overlap = set(self.provider_pnl_components_included) & set(
            self.provider_pnl_components_excluded
        )
        if overlap:
            raise ValueError("PnL inclusion and exclusion components must be disjoint")
        if type(self.observed_total_pnl_is_gross_of_execution_costs) is not bool:
            raise TypeError("observed_total_pnl_is_gross_of_execution_costs must be bool")
        _require_non_empty_string(self.attribution_units, "attribution_units")


@dataclass(frozen=True, slots=True)
class OptionRevaluationConventionVersionV1(_VersionedContextV1):
    model_family: str
    exercise_style_treatment: str
    discount_rate_input_refs: tuple[str, ...]
    dividend_borrow_carry_input_refs: tuple[str, ...]
    time_day_count_convention: str
    iv_skew_interpretation: str
    numerical_method: str
    numerical_tolerance: Decimal
    greek_scaling: str

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_non_empty_string(self.model_family, "model_family")
        _require_non_empty_string(self.exercise_style_treatment, "exercise_style_treatment")
        _require_string_tuple(
            self.discount_rate_input_refs, "discount_rate_input_refs", distinct=True
        )
        _require_string_tuple(
            self.dividend_borrow_carry_input_refs,
            "dividend_borrow_carry_input_refs",
            distinct=True,
        )
        if not self.discount_rate_input_refs and not self.dividend_borrow_carry_input_refs:
            raise ValueError(
                "option revaluation convention requires carry/rate inputs or references"
            )
        _require_non_empty_string(self.time_day_count_convention, "time_day_count_convention")
        _require_non_empty_string(self.iv_skew_interpretation, "iv_skew_interpretation")
        _require_non_empty_string(self.numerical_method, "numerical_method")
        _require_decimal(self.numerical_tolerance, "numerical_tolerance", positive=True)
        _require_non_empty_string(self.greek_scaling, "greek_scaling")


@dataclass(frozen=True, slots=True)
class ExecutionCostScheduleVersionV1(_VersionedContextV1):
    commission_rules: tuple[tuple[str, Decimal], ...]
    fee_rules: tuple[tuple[str, Decimal], ...]
    multi_leg_incremental_cost_rules: tuple[tuple[str, Decimal], ...]
    cost_units: str

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_named_decimal_values(self.commission_rules, "commission_rules", non_negative=True)
        _require_named_decimal_values(self.fee_rules, "fee_rules", non_negative=True)
        _require_named_decimal_values(
            self.multi_leg_incremental_cost_rules,
            "multi_leg_incremental_cost_rules",
            non_negative=True,
        )
        if not (self.commission_rules or self.fee_rules or self.multi_leg_incremental_cost_rules):
            raise ValueError("execution cost schedule must contain at least one explicit cost rule")
        _require_non_empty_string(self.cost_units, "cost_units")


@dataclass(frozen=True, slots=True)
class AttributionPathContextV1(_VersionedContextV1):
    underlying_path_occurrence_refs: tuple[str, ...]
    iv_path_occurrence_refs: tuple[str, ...]
    position_path_occurrence_refs: tuple[str, ...]
    quantity_path_occurrence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        paths = (
            (self.underlying_path_occurrence_refs, "underlying_path_occurrence_refs"),
            (self.iv_path_occurrence_refs, "iv_path_occurrence_refs"),
            (self.position_path_occurrence_refs, "position_path_occurrence_refs"),
            (self.quantity_path_occurrence_refs, "quantity_path_occurrence_refs"),
        )
        for refs, name in paths:
            _require_string_tuple(refs, name, non_empty=True)
        lengths = {len(refs) for refs, _ in paths}
        if len(lengths) != 1:
            raise ValueError("attribution path occurrence reference tuples must be exactly aligned")


@dataclass(frozen=True, slots=True)
class InputSelectionPolicyVersionV1(_VersionedContextV1):
    join_keys: tuple[str, ...]
    maximum_staleness: timedelta
    maximum_skew: timedelta
    temporal_basis_permissions: tuple[str, ...]
    basket_membership: tuple[str, ...]

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_string_tuple(self.join_keys, "join_keys", non_empty=True, distinct=True)
        _require_non_negative_timedelta(self.maximum_staleness, "maximum_staleness")
        _require_non_negative_timedelta(self.maximum_skew, "maximum_skew")
        _require_string_tuple(
            self.temporal_basis_permissions,
            "temporal_basis_permissions",
            non_empty=True,
            distinct=True,
        )
        allowed_temporal_bases = {"true_instant", "receipt_only", "date_only"}
        if not set(self.temporal_basis_permissions) <= allowed_temporal_bases:
            raise ValueError("temporal_basis_permissions contain an unadmitted temporal basis")
        _require_string_tuple(self.basket_membership, "basket_membership", distinct=True)


@dataclass(frozen=True, slots=True)
class VersionRefV1:
    context_id: str
    version: int

    def __post_init__(self) -> None:
        _require_non_empty_string(self.context_id, "context_id")
        _require_positive_version(self.version)


@dataclass(frozen=True, slots=True)
class RawInputLineageV1:
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_id: str
    projection_mapping_version: int
    unit_convention_id: str
    unit_convention_version: int
    native_units: str
    canonical_units: str

    def __post_init__(self) -> None:
        _require_raw_signal_id(self.raw_signal_id)
        _require_non_empty_string(self.observation_occurrence_id, "observation_occurrence_id")
        _require_non_empty_string(self.projection_mapping_id, "projection_mapping_id")
        _require_positive_version(self.projection_mapping_version, "projection_mapping_version")
        _require_non_empty_string(self.unit_convention_id, "unit_convention_id")
        _require_positive_version(self.unit_convention_version, "unit_convention_version")
        _require_non_empty_string(self.native_units, "native_units")
        _require_non_empty_string(self.canonical_units, "canonical_units")


type DerivedResultV1 = bool | int | Decimal | str | date | datetime | tuple["DerivedResultV1", ...]


@dataclass(frozen=True, slots=True)
class DerivedSignalOccurrenceV1:
    derived_signal_id: str
    derived_occurrence_id: str
    calculation_definition_version: str
    parameter_context_refs: tuple[VersionRefV1, ...]
    subject_instrument: str
    universe: tuple[str, ...] | None
    effective_as_of_utc: datetime
    window: str | None
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime
    result: DerivedResultV1
    units: str
    result_shape: str
    raw_input_lineage: tuple[RawInputLineageV1, ...]
    predecessor_occurrence_ids: tuple[str, ...]
    convention_refs: tuple[VersionRefV1, ...]
    supersedes_derived_occurrence_id: str | None = None

    def __post_init__(self) -> None:
        _require_derived_signal_id(self.derived_signal_id)
        _require_non_empty_string(self.derived_occurrence_id, "derived_occurrence_id")
        _require_non_empty_string(
            self.calculation_definition_version, "calculation_definition_version"
        )
        _require_non_empty_string(self.subject_instrument, "subject_instrument")
        _require_utc(self.effective_as_of_utc, "effective_as_of_utc")
        _require_utc(self.knowledge_cutoff_utc, "knowledge_cutoff_utc")
        _require_utc(self.calculated_at_utc, "calculated_at_utc")
        _require_non_empty_string(self.units, "units")
        _require_non_empty_string(self.result_shape, "result_shape")
        if self.window is not None and (type(self.window) is not str or not self.window):
            raise ValueError("window must be a non-empty string or absent")
        if self.universe is not None:
            _require_non_empty_distinct_strings(self.universe, "universe")
        _require_version_refs(self.parameter_context_refs, "parameter_context_refs")
        _require_raw_lineage(self.raw_input_lineage, "raw_input_lineage")
        _require_non_empty_distinct_strings(
            self.predecessor_occurrence_ids, "predecessor_occurrence_ids"
        )
        _require_version_refs(self.convention_refs, "convention_refs")
        _require_derived_result(self.result)


@dataclass(frozen=True, slots=True)
class ParameterProfileRefV1:
    profile: str
    context_id: str
    version: int

    def __post_init__(self) -> None:
        _require_non_empty_string(self.profile, "profile")
        _require_non_empty_string(self.context_id, "context_id")
        _require_positive_version(self.version)


@dataclass(frozen=True, slots=True)
class RawInputBindingV1:
    raw_signal_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    subject_instrument: str

    def __post_init__(self) -> None:
        _require_raw_signal_id(self.raw_signal_id)
        if type(self.projection_mapping_ref) is not VersionRefV1:
            raise TypeError("projection_mapping_ref must be VersionRefV1")
        if type(self.unit_convention_ref) is not VersionRefV1:
            raise TypeError("unit_convention_ref must be VersionRefV1")
        _require_non_empty_string(self.subject_instrument, "subject_instrument")


@dataclass(frozen=True, slots=True)
class CalculationRequestV1:
    derived_signal_id: str
    subject_instrument: str
    as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculation_definition_version: str
    parameter_set_id: str
    parameter_set_version: int
    input_selection_policy_id: str
    input_selection_policy_version: int
    context_refs: tuple[VersionRefV1, ...]
    parameter_profile_refs: tuple[ParameterProfileRefV1, ...] = ()
    raw_input_bindings: tuple[RawInputBindingV1, ...] = ()

    def __post_init__(self) -> None:
        _require_derived_signal_id(self.derived_signal_id)
        _require_non_empty_string(self.subject_instrument, "subject_instrument")
        _require_utc(self.as_of_utc, "as_of_utc")
        _require_utc(self.knowledge_cutoff_utc, "knowledge_cutoff_utc")
        _require_non_empty_string(
            self.calculation_definition_version, "calculation_definition_version"
        )
        _require_non_empty_string(self.parameter_set_id, "parameter_set_id")
        _require_positive_version(self.parameter_set_version, "parameter_set_version")
        _require_non_empty_string(self.input_selection_policy_id, "input_selection_policy_id")
        _require_positive_version(
            self.input_selection_policy_version, "input_selection_policy_version"
        )
        _require_version_refs(self.context_refs, "context_refs")
        _require_tuple(self.parameter_profile_refs, "parameter_profile_refs")
        for item in self.parameter_profile_refs:
            if type(item) is not ParameterProfileRefV1:
                raise TypeError(
                    "parameter_profile_refs must contain exact ParameterProfileRefV1 values"
                )
        profiles = tuple(item.profile for item in self.parameter_profile_refs)
        if len(profiles) != len(set(profiles)):
            raise ValueError("parameter_profile_refs must contain distinct profiles")
        _require_tuple(self.raw_input_bindings, "raw_input_bindings")
        for binding_item in self.raw_input_bindings:
            if type(binding_item) is not RawInputBindingV1:
                raise TypeError("raw_input_bindings must contain exact RawInputBindingV1 values")
        binding_keys = tuple(
            (item.raw_signal_id, item.subject_instrument) for item in self.raw_input_bindings
        )
        if len(binding_keys) != len(set(binding_keys)):
            raise ValueError(
                "raw_input_bindings must contain distinct raw-signal/subject identities"
            )


class RawProjectionReaderV1(Protocol):
    def project_raw_value(self, *args: object, **kwargs: object) -> object | None: ...

    def list_projected_raw_history(self, *args: object, **kwargs: object) -> object: ...


class _VersionedContextLikeV1(Protocol):
    context_id: str
    version: int


class _RawProjectionMappingLikeV1(Protocol):
    mapping_id: str
    version: int


class _ProjectedRawValueLikeV1(Protocol):
    observation_occurrence_id: object


def _context_key(value: object) -> tuple[str, int]:
    typed = cast(_VersionedContextLikeV1, value)
    return typed.context_id, typed.version


def _mapping_key(value: object) -> tuple[str, int]:
    typed = cast(_RawProjectionMappingLikeV1, value)
    return typed.mapping_id, typed.version


class _PersistenceV1(Protocol):
    def append_occurrence(self, value: DerivedSignalOccurrenceV1) -> DerivedSignalOccurrenceV1: ...

    def get_occurrence(self, derived_occurrence_id: str) -> DerivedSignalOccurrenceV1 | None: ...

    def list_occurrences(
        self, *, derived_signal_id: str, subject_instrument: str, limit: int
    ) -> tuple[DerivedSignalOccurrenceV1, ...]: ...


class _MemoryPersistenceV1:
    def __init__(self) -> None:
        self._by_id: dict[str, DerivedSignalOccurrenceV1] = {}

    def append_occurrence(self, value: DerivedSignalOccurrenceV1) -> DerivedSignalOccurrenceV1:
        existing = self._by_id.get(value.derived_occurrence_id)
        if existing is not None:
            if existing != value:
                raise ValueError("derived occurrence identity already has different content")
            return existing
        self._by_id[value.derived_occurrence_id] = value
        return value

    def get_occurrence(self, derived_occurrence_id: str) -> DerivedSignalOccurrenceV1 | None:
        return self._by_id.get(derived_occurrence_id)

    def list_occurrences(
        self, *, derived_signal_id: str, subject_instrument: str, limit: int
    ) -> tuple[DerivedSignalOccurrenceV1, ...]:
        if type(limit) is not int or limit <= 0:
            raise ValueError("limit must be a positive integer")
        values = [
            value
            for value in self._by_id.values()
            if value.derived_signal_id == derived_signal_id
            and value.subject_instrument == subject_instrument
        ]
        values.sort(key=lambda value: (value.effective_as_of_utc, value.derived_occurrence_id))
        return tuple(values[:limit])


class _ReadsV1:
    __slots__ = ("_persistence",)

    def __init__(self, persistence: _PersistenceV1) -> None:
        self._persistence = persistence

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> DerivedSignalOccurrenceV1 | None:
        _require_non_empty_string(derived_occurrence_id, "derived_occurrence_id")
        return self._persistence.get_occurrence(derived_occurrence_id)

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str, limit: int
    ) -> tuple[DerivedSignalOccurrenceV1, ...]:
        _require_derived_signal_id(derived_signal_id)
        _require_non_empty_string(subject_instrument, "subject_instrument")
        return self._persistence.list_occurrences(
            derived_signal_id=derived_signal_id,
            subject_instrument=subject_instrument,
            limit=limit,
        )


class _OwnerV1:
    __slots__ = (
        "_contexts",
        "_input_selection_policies",
        "_parameter_sets",
        "_persistence",
        "_raw_projection_mappings",
        "_raw_projection_reader",
        "_unit_conventions",
        "_utc_now",
        "reads",
    )

    def __init__(
        self,
        *,
        raw_projection_reader: RawProjectionReaderV1,
        persistence: _PersistenceV1,
        raw_projection_mappings: tuple[object, ...],
        parameter_sets: tuple[CalculationParameterSetV1, ...],
        input_selection_policies: tuple[InputSelectionPolicyVersionV1, ...],
        unit_conventions: tuple[UnitConventionVersionV1, ...],
        contexts: tuple[object, ...],
        utc_now: Callable[[], datetime],
    ) -> None:
        self._raw_projection_reader = raw_projection_reader
        self._persistence = persistence
        self._raw_projection_mappings = raw_projection_mappings
        self._parameter_sets = {(v.context_id, v.version): v for v in parameter_sets}
        self._input_selection_policies = {
            (v.context_id, v.version): v for v in input_selection_policies
        }
        self._unit_conventions = {(v.context_id, v.version): v for v in unit_conventions}
        self._contexts = {_context_key(v): v for v in contexts}
        self._utc_now = utc_now
        self.reads = _ReadsV1(persistence)

    @staticmethod
    def _event_instant(projected: object) -> datetime | None:
        if getattr(projected, "source_temporal_kind", None) != "true_instant":
            return None
        raw = getattr(projected, "source_timestamp_raw", None)
        if type(raw) is not str or not raw:
            return None
        try:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            timezone_name = getattr(projected, "source_timezone_native", None)
            if type(timezone_name) is not str or not timezone_name:
                return None
            try:
                from zoneinfo import ZoneInfo

                parsed = parsed.replace(tzinfo=ZoneInfo(timezone_name))
            except Exception:
                return None
        return parsed.astimezone(UTC)

    def _parameter_set_for_profile(
        self, request: CalculationRequestV1, profile: str
    ) -> CalculationParameterSetV1 | None:
        refs = {item.profile: item for item in request.parameter_profile_refs}
        ref = refs.get(profile)
        if ref is None:
            candidate = self._parameter_sets.get(
                (request.parameter_set_id, request.parameter_set_version)
            )
            if candidate is None or candidate.profile != profile:
                return None
            return candidate
        candidate = self._parameter_sets.get((ref.context_id, ref.version))
        if candidate is None or candidate.profile != profile:
            return None
        return candidate

    def _selection_policy(
        self, request: CalculationRequestV1
    ) -> InputSelectionPolicyVersionV1 | None:
        return self._input_selection_policies.get(
            (request.input_selection_policy_id, request.input_selection_policy_version)
        )

    def _mapping(self, ref: VersionRefV1, raw_signal_id: str) -> object | None:
        candidates = tuple(
            mapping
            for mapping in self._raw_projection_mappings
            if getattr(mapping, "mapping_id", None) == ref.context_id
            and getattr(mapping, "version", None) == ref.version
            and getattr(getattr(mapping, "raw_signal_catalogue_id", None), "value", None)
            == raw_signal_id
        )
        return candidates[0] if len(candidates) == 1 else None

    def _contexts_for_row(
        self, request: CalculationRequestV1, typed_contexts: tuple[str, ...]
    ) -> tuple[object, ...] | None:
        supplied = tuple(
            self._contexts.get((ref.context_id, ref.version)) for ref in request.context_refs
        )
        if any(item is None for item in supplied):
            return None
        contexts = tuple(item for item in supplied if item is not None)
        for requirement in typed_contexts:
            context_type = requirement.split(":", 1)[0]
            if context_type == "CalculationParameterSet":
                continue
            expected_name = f"{context_type}V1"
            matches = tuple(item for item in contexts if type(item).__name__ == expected_name)
            if len(matches) != 1:
                return None
        return contexts

    def _raw_values(
        self,
        request: CalculationRequestV1,
        raw_signal_id: str,
        selection: InputSelectionPolicyVersionV1,
    ) -> (
        tuple[tuple[KernelValueV1, ...], tuple[RawInputLineageV1, ...], tuple[VersionRefV1, ...]]
        | None
    ):
        from nvda_desk.raw_signal_occurrence_truth import api as raw_api

        from ._stage1 import KernelValueV1, select_eligible_values

        bindings = tuple(
            item for item in request.raw_input_bindings if item.raw_signal_id == raw_signal_id
        )
        if not bindings:
            return None
        kernel_values: list[KernelValueV1] = []
        lineage: list[RawInputLineageV1] = []
        convention_refs: list[VersionRefV1] = []
        for binding in bindings:
            mapping = self._mapping(binding.projection_mapping_ref, raw_signal_id)
            unit = self._unit_conventions.get(
                (binding.unit_convention_ref.context_id, binding.unit_convention_ref.version)
            )
            if mapping is None or unit is None:
                return None
            if getattr(mapping, "native_units", None) != unit.native_units:
                return None
            cursor: str | None = None
            projected: list[object] = []
            while True:
                page = self._raw_projection_reader.list_projected_raw_history(
                    raw_api.RawSignalCatalogueId(raw_signal_id),
                    mappings=(mapping,),
                    subject_instrument=binding.subject_instrument,
                    received_at_or_before_utc=request.knowledge_cutoff_utc,
                    event_at_or_before_utc=None,
                    limit=1000,
                    cursor=cursor,
                )
                items = getattr(page, "items", None)
                if type(items) is not tuple:
                    return None
                projected.extend(items)
                cursor = getattr(page, "next_cursor", None)
                if cursor is None:
                    break
                if type(cursor) is not str or not cursor:
                    return None
            for item in projected:
                typed_item = cast(_ProjectedRawValueLikeV1, item)
                if (
                    getattr(getattr(item, "raw_signal_catalogue_id", None), "value", None)
                    != raw_signal_id
                ):
                    return None
                if (
                    getattr(item, "projection_mapping_id", None)
                    != binding.projection_mapping_ref.context_id
                ):
                    return None
                if (
                    getattr(item, "projection_mapping_version", None)
                    != binding.projection_mapping_ref.version
                ):
                    return None
                if getattr(item, "native_units", None) != unit.native_units:
                    return None
                native = getattr(item, "native_value", None)
                if type(native) is Decimal:
                    canonical: object = unit.convert(native, native_units=unit.native_units)
                elif type(native) is int and type(native) is not bool:
                    canonical = unit.convert(Decimal(native), native_units=unit.native_units)
                else:
                    if unit.scale != Decimal(1) or unit.offset != Decimal(0):
                        return None
                    canonical = native
                temporal_kind = str(getattr(item, "source_temporal_kind", ""))
                received = getattr(item, "received_ts_utc", None)
                if type(received) is not datetime:
                    return None
                event = self._event_instant(item)
                if temporal_kind == "true_instant":
                    if event is None:
                        return None
                    effective = event
                else:
                    effective = received
                metadata: tuple[tuple[str, object], ...] = (
                    ("source_provider", str(getattr(item, "source_provider", ""))),
                    ("source_variant", str(getattr(item, "source_variant", "") or "")),
                    (
                        "source_timezone_native",
                        str(getattr(item, "source_timezone_native", "") or ""),
                    ),
                    (
                        "revision_vintage_native",
                        str(getattr(item, "revision_vintage_native", "") or ""),
                    ),
                    ("ingestion_sequence", int(getattr(item, "ingestion_sequence", 0))),
                )
                kernel_values.append(
                    KernelValueV1(
                        value=canonical,
                        occurrence_id=str(typed_item.observation_occurrence_id),
                        effective_at_utc=effective,
                        received_ts_utc=received,
                        subject_instrument=str(
                            getattr(item, "subject_instrument", "") or binding.subject_instrument
                        ),
                        source_temporal_kind=temporal_kind,
                        source_timestamp_raw=getattr(item, "source_timestamp_raw", None),
                        metadata=metadata,
                    )
                )
                lineage.append(
                    RawInputLineageV1(
                        raw_signal_id=raw_signal_id,
                        observation_occurrence_id=str(typed_item.observation_occurrence_id),
                        projection_mapping_id=binding.projection_mapping_ref.context_id,
                        projection_mapping_version=binding.projection_mapping_ref.version,
                        unit_convention_id=binding.unit_convention_ref.context_id,
                        unit_convention_version=binding.unit_convention_ref.version,
                        native_units=unit.native_units,
                        canonical_units=unit.canonical_units,
                    )
                )
            convention_refs.append(binding.unit_convention_ref)
        eligible = select_eligible_values(
            tuple(kernel_values),
            as_of_utc=request.as_of_utc,
            knowledge_cutoff_utc=request.knowledge_cutoff_utc,
            # Historical kernels apply their own exact window.  Freshness is enforced below
            # on each subject's latest point; applying it to history would erase the window.
            maximum_staleness=None,
            temporal_basis_permissions=selection.temporal_basis_permissions,
        )
        if not eligible:
            return None
        for subject in {item.subject_instrument for item in eligible}:
            latest = max(
                (item for item in eligible if item.subject_instrument == subject),
                key=lambda item: (item.effective_at_utc, item.received_ts_utc, item.occurrence_id),
            )
            basis = (
                latest.effective_at_utc
                if latest.source_temporal_kind == "true_instant"
                else latest.received_ts_utc
            )
            if request.as_of_utc - basis > selection.maximum_staleness:
                return None
        eligible_ids = {item.occurrence_id for item in eligible}
        selected_lineage = tuple(
            item for item in lineage if item.observation_occurrence_id in eligible_ids
        )
        return eligible, selected_lineage, tuple(convention_refs)

    @staticmethod
    def _occurrence_kernel_value(value: DerivedSignalOccurrenceV1) -> KernelValueV1:
        from ._stage1 import KernelValueV1

        return KernelValueV1(
            value=value.result,
            occurrence_id=value.derived_occurrence_id,
            effective_at_utc=value.effective_as_of_utc,
            received_ts_utc=value.calculated_at_utc,
            subject_instrument=value.subject_instrument,
            source_temporal_kind="derived",
            metadata=(("units", value.units), ("result_shape", value.result_shape)),
        )

    def _compatible_history(
        self,
        *,
        derived_signal_id: str,
        request: CalculationRequestV1,
        parameter_ref: VersionRefV1,
        selection_ref: VersionRefV1,
    ) -> tuple[DerivedSignalOccurrenceV1, ...]:
        candidates = self._persistence.list_occurrences(
            derived_signal_id=derived_signal_id,
            subject_instrument=request.subject_instrument,
            limit=100000,
        )
        required = {parameter_ref, selection_ref}
        return tuple(
            value
            for value in candidates
            if value.calculation_definition_version == request.calculation_definition_version
            and value.effective_as_of_utc <= request.as_of_utc
            and value.knowledge_cutoff_utc <= request.knowledge_cutoff_utc
            and required <= set(value.parameter_context_refs)
        )

    def _materialise(
        self, request: CalculationRequestV1, derived_signal_id: str, stack: tuple[str, ...]
    ) -> DerivedSignalOccurrenceV1 | None:
        from ._catalogue import catalogue_row
        from ._stage1 import STAGE1_KERNEL_IDS, evaluate_stage1_kernel, occurrence_identity

        if derived_signal_id in stack:
            return None
        row = catalogue_row(derived_signal_id)
        if row.kernel_id not in STAGE1_KERNEL_IDS:
            return None
        if len(row.parameter_profiles) != 1:
            return None
        parameter_set = self._parameter_set_for_profile(request, row.parameter_profiles[0])
        selection = self._selection_policy(request)
        contexts = self._contexts_for_row(request, row.typed_contexts)
        if parameter_set is None or selection is None or contexts is None:
            return None
        parameter_ref = VersionRefV1(parameter_set.context_id, parameter_set.version)
        selection_ref = VersionRefV1(selection.context_id, selection.version)

        raw_inputs: dict[str, tuple[KernelValueV1, ...]] = {}
        direct_lineage: list[RawInputLineageV1] = []
        convention_refs: list[VersionRefV1] = []
        for raw_signal_id in row.raw_dependencies:
            loaded = self._raw_values(request, raw_signal_id, selection)
            if loaded is None:
                return None
            values, lineage, conventions = loaded
            raw_inputs[raw_signal_id] = values
            direct_lineage.extend(lineage)
            convention_refs.extend(conventions)

        if len(raw_inputs) > 1:
            latest = [
                max(values, key=lambda item: item.effective_at_utc).effective_at_utc
                for values in raw_inputs.values()
                if values
            ]
            if latest and max(latest) - min(latest) > selection.maximum_skew:
                return None

        derived_inputs: dict[str, tuple[KernelValueV1, ...]] = {}
        immediate_predecessors: list[DerivedSignalOccurrenceV1] = []
        inherited_lineage: list[RawInputLineageV1] = []
        for predecessor_id in row.derived_dependencies:
            predecessor_row = catalogue_row(predecessor_id)
            if len(predecessor_row.parameter_profiles) != 1:
                return None
            predecessor_parameters = self._parameter_set_for_profile(
                request, predecessor_row.parameter_profiles[0]
            )
            if predecessor_parameters is None:
                return None
            predecessor_parameter_ref = VersionRefV1(
                predecessor_parameters.context_id, predecessor_parameters.version
            )
            history = self._compatible_history(
                derived_signal_id=predecessor_id,
                request=request,
                parameter_ref=predecessor_parameter_ref,
                selection_ref=selection_ref,
            )
            if predecessor_row.kernel_id in STAGE1_KERNEL_IDS:
                current = self._materialise(request, predecessor_id, (*stack, derived_signal_id))
                if current is None:
                    return None
                history_by_id = {value.derived_occurrence_id: value for value in history}
                history_by_id[current.derived_occurrence_id] = current
                history = tuple(
                    sorted(
                        history_by_id.values(),
                        key=lambda value: (
                            value.effective_as_of_utc,
                            value.knowledge_cutoff_utc,
                            value.derived_occurrence_id,
                        ),
                    )
                )
            elif not history:
                return None
            if not history:
                return None
            current = max(
                history,
                key=lambda value: (
                    value.effective_as_of_utc,
                    value.knowledge_cutoff_utc,
                    value.derived_occurrence_id,
                ),
            )
            immediate_predecessors.append(current)
            inherited_lineage.extend(current.raw_input_lineage)
            derived_inputs[predecessor_id] = tuple(
                self._occurrence_kernel_value(value) for value in history
            )

        evaluated = evaluate_stage1_kernel(
            derived_signal_id,
            raw_inputs=raw_inputs,
            derived_inputs=derived_inputs,
            parameter_set=parameter_set,
            contexts=contexts,
            as_of_utc=request.as_of_utc,
            knowledge_cutoff_utc=request.knowledge_cutoff_utc,
        )
        if evaluated is None:
            return None

        lineage_by_key: dict[tuple[str, str, str, int, str, int], RawInputLineageV1] = {}
        for item in (*direct_lineage, *inherited_lineage):
            key = (
                item.raw_signal_id,
                item.observation_occurrence_id,
                item.projection_mapping_id,
                item.projection_mapping_version,
                item.unit_convention_id,
                item.unit_convention_version,
            )
            lineage_by_key[key] = item
        exact_lineage = tuple(lineage_by_key[key] for key in sorted(lineage_by_key))
        predecessor_ids = tuple(
            sorted({value.derived_occurrence_id for value in immediate_predecessors})
        )
        context_refs = tuple(dict.fromkeys((parameter_ref, selection_ref, *request.context_refs)))
        convention_refs_exact = tuple(dict.fromkeys(convention_refs))
        version_keys = tuple(
            (ref.context_id, ref.version) for ref in (*context_refs, *convention_refs_exact)
        ) + tuple(
            (item.projection_mapping_id, item.projection_mapping_version) for item in exact_lineage
        )
        identity = occurrence_identity(
            derived_signal_id,
            calculation_definition_version=request.calculation_definition_version,
            subject_instrument=request.subject_instrument,
            effective_as_of_utc=request.as_of_utc,
            knowledge_cutoff_utc=request.knowledge_cutoff_utc,
            input_occurrence_ids=tuple(
                sorted(
                    {item.observation_occurrence_id for item in exact_lineage}
                    | set(predecessor_ids)
                )
            ),
            version_keys=version_keys,
        )
        existing = self._persistence.get_occurrence(identity)
        if existing is not None:
            return existing
        previous = self._persistence.list_occurrences(
            derived_signal_id=derived_signal_id,
            subject_instrument=request.subject_instrument,
            limit=100000,
        )
        supersedes = (
            max(
                previous, key=lambda value: (value.effective_as_of_utc, value.derived_occurrence_id)
            ).derived_occurrence_id
            if previous
            else None
        )
        calculated_at = self._utc_now()
        if type(calculated_at) is not datetime:
            raise TypeError("utc_now must return datetime")
        _require_utc(calculated_at, "utc_now result")
        occurrence = DerivedSignalOccurrenceV1(
            derived_signal_id=derived_signal_id,
            derived_occurrence_id=identity,
            calculation_definition_version=request.calculation_definition_version,
            parameter_context_refs=context_refs,
            subject_instrument=request.subject_instrument,
            universe=selection.basket_membership or None,
            effective_as_of_utc=request.as_of_utc,
            window=row.parameter_window or None,
            knowledge_cutoff_utc=request.knowledge_cutoff_utc,
            calculated_at_utc=calculated_at,
            result=evaluated.value,  # type: ignore[arg-type]
            units=row.units,
            result_shape=evaluated.result_shape,
            raw_input_lineage=exact_lineage,
            predecessor_occurrence_ids=predecessor_ids,
            convention_refs=convention_refs_exact,
            supersedes_derived_occurrence_id=supersedes,
        )
        return self._persistence.append_occurrence(occurrence)

    def materialise(self, request: CalculationRequestV1) -> DerivedSignalOccurrenceV1 | None:
        if type(request) is not CalculationRequestV1:
            raise TypeError("request must be CalculationRequestV1")
        return self._materialise(request, request.derived_signal_id, ())


def _require_distinct_context_versions(values: tuple[object, ...], field_name: str) -> None:
    keys: list[tuple[str, int]] = []
    for value in values:
        context_id = getattr(value, "context_id", None)
        version = getattr(value, "version", None)
        if (
            type(context_id) is not str
            or not context_id
            or type(version) is not int
            or version <= 0
        ):
            raise TypeError(f"{field_name} entries must expose a valid immutable identity/version")
        keys.append((context_id, version))
    if len(keys) != len(set(keys)):
        raise ValueError(f"{field_name} contains duplicate identity/version values")


def create_owner(
    *,
    raw_projection_reader: RawProjectionReaderV1,
    persistence: _PersistenceV1 | None = None,
    raw_projection_mappings: tuple[object, ...] = (),
    parameter_sets: tuple[CalculationParameterSetV1, ...] = (),
    input_selection_policies: tuple[InputSelectionPolicyVersionV1, ...] = (),
    unit_conventions: tuple[UnitConventionVersionV1, ...] = (),
    contexts: tuple[object, ...] = (),
    utc_now: Callable[[], datetime] | None = None,
) -> _OwnerV1:
    from nvda_desk.raw_signal_occurrence_truth import api as raw_api

    if type(raw_projection_mappings) is not tuple or any(
        type(item) is not raw_api.RawSignalProjectionMappingV1 for item in raw_projection_mappings
    ):
        raise TypeError(
            "raw_projection_mappings must contain exact M00 RawSignalProjectionMappingV1 values"
        )
    if type(parameter_sets) is not tuple or any(
        type(item) is not CalculationParameterSetV1 for item in parameter_sets
    ):
        raise TypeError("parameter_sets must contain exact CalculationParameterSetV1 values")
    if type(input_selection_policies) is not tuple or any(
        type(item) is not InputSelectionPolicyVersionV1 for item in input_selection_policies
    ):
        raise TypeError(
            "input_selection_policies must contain exact InputSelectionPolicyVersionV1 values"
        )
    if type(unit_conventions) is not tuple or any(
        type(item) is not UnitConventionVersionV1 for item in unit_conventions
    ):
        raise TypeError("unit_conventions must contain exact UnitConventionVersionV1 values")
    if type(contexts) is not tuple:
        raise TypeError("contexts must be a tuple")
    _require_distinct_context_versions(parameter_sets, "parameter_sets")
    _require_distinct_context_versions(input_selection_policies, "input_selection_policies")
    _require_distinct_context_versions(unit_conventions, "unit_conventions")
    _require_distinct_context_versions(contexts, "contexts")
    mapping_keys = tuple(_mapping_key(item) for item in raw_projection_mappings)
    if len(mapping_keys) != len(set(mapping_keys)):
        raise ValueError("raw_projection_mappings contains duplicate identity/version values")
    if persistence is None:
        persistence = _MemoryPersistenceV1()
    if utc_now is None:

        def default_utc_now() -> datetime:
            return datetime.now(UTC)

        utc_now = default_utc_now
    if not callable(utc_now):
        raise TypeError("utc_now must be callable")
    return _OwnerV1(
        raw_projection_reader=raw_projection_reader,
        persistence=persistence,
        raw_projection_mappings=raw_projection_mappings,
        parameter_sets=parameter_sets,
        input_selection_policies=input_selection_policies,
        unit_conventions=unit_conventions,
        contexts=contexts,
        utc_now=utc_now,
    )


__all__ = [
    "AttributionPathContextV1",
    "CalculationParameterSetV1",
    "CalculationRequestV1",
    "CandidateSetContextV1",
    "CandidateStructureContextV1",
    "DerivedResultV1",
    "DerivedSignalOccurrenceV1",
    "EntryStateContextV1",
    "EvaluationSetV1",
    "ExecutionCostScheduleVersionV1",
    "InputSelectionPolicyVersionV1",
    "LivePositionContextV1",
    "OptionRevaluationConventionVersionV1",
    "OrderIntentContextV1",
    "ParameterProfileRefV1",
    "PnLConventionVersionV1",
    "RawInputBindingV1",
    "RawInputLineageV1",
    "RawProjectionReaderV1",
    "RecalculationScheduleV1",
    "RequiredFieldPolicyV1",
    "ScoreFeatureV1",
    "UnitConventionVersionV1",
    "VersionRefV1",
    "create_owner",
]
