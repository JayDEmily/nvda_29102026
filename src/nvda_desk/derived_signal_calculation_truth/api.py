"""Typed public foundation seam for Derived Signal Calculation Truth."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Protocol


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
        _require_utc(value, field_name)
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
class CalculationParameterSetV1(_VersionedContextV1):
    profile: str
    parameters: tuple[tuple[str, ImmutableContextValueV1], ...]

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_non_empty_string(self.profile, "profile")
        _require_named_context_values(self.parameters, "parameters", non_empty=True)


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


type DerivedResultV1 = bool | int | Decimal | str | datetime | tuple["DerivedResultV1", ...]


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


class RawProjectionReaderV1(Protocol):
    def project_raw_value(self, *args: object, **kwargs: object) -> object | None: ...

    def list_projected_raw_history(self, *args: object, **kwargs: object) -> object: ...


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
    __slots__ = ("_persistence", "_raw_projection_reader", "reads")

    def __init__(
        self,
        *,
        raw_projection_reader: RawProjectionReaderV1,
        persistence: _PersistenceV1,
    ) -> None:
        self._raw_projection_reader = raw_projection_reader
        self._persistence = persistence
        self.reads = _ReadsV1(persistence)

    def materialise(self, request: CalculationRequestV1) -> DerivedSignalOccurrenceV1 | None:
        if type(request) is not CalculationRequestV1:
            raise TypeError("request must be CalculationRequestV1")
        # DS-I01 establishes the calculation/read foundation only. No D-kernel is admitted in
        # this leaf, so the sole lawful result until a later kernel leaf supplies all required
        # inputs and calculation meaning is absence.
        return None


def create_owner(
    *,
    raw_projection_reader: RawProjectionReaderV1,
    persistence: _PersistenceV1 | None = None,
) -> _OwnerV1:
    if persistence is None:
        persistence = _MemoryPersistenceV1()
    return _OwnerV1(raw_projection_reader=raw_projection_reader, persistence=persistence)


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
    "PnLConventionVersionV1",
    "RawInputLineageV1",
    "RawProjectionReaderV1",
    "RecalculationScheduleV1",
    "RequiredFieldPolicyV1",
    "UnitConventionVersionV1",
    "VersionRefV1",
    "create_owner",
]
