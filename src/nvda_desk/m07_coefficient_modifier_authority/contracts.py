"""M07-owned contracts for bounded coefficient and modifier authority."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    field_validator,
    model_validator,
)

DecisionStatus = Literal[
    "rejected",
    "applied",
    "no_modifier_members",
    "no_applicable_modifiers",
]
TransformOperator = Literal["add", "multiply", "set"]
BoundDisposition = Literal["within_bounds", "clamped_lower", "clamped_upper"]

CLOSED_AUTHORITY_CLASSES: tuple[str, ...] = (
    "capital",
    "playbook",
    "execution",
    "lifecycle",
    "replay",
    "transaction",
    "downstream_state_mutation",
)


def _finite(value: Decimal, *, field_name: str) -> Decimal:
    if not value.is_finite():
        raise ValueError(f"{field_name}_must_be_finite")
    return value


def _is_utc(value: datetime) -> bool:
    return (
        value.tzinfo is not None
        and value.utcoffset() is not None
        and value.utcoffset() == UTC.utcoffset(value)
    )


class CoefficientMember(BaseModel):
    """One immutable numeric coefficient admitted by an M07 policy bundle."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    coefficient_id: str = Field(min_length=1)
    coefficient_version: str = Field(min_length=1)
    owner_stage: str = Field(min_length=1)
    value_type: Literal["decimal"]
    units: str = Field(min_length=1)
    baseline_value: Decimal
    hard_lower_bound: Decimal
    hard_upper_bound: Decimal
    surface_class: Literal["mutable_runtime_surface"]
    transform_family: Literal["bounded_decimal_algebra"]
    runtime_mutability_class: Literal["runtime_mutable"]
    promotion_lineage: str = Field(min_length=1)

    @field_validator("baseline_value", "hard_lower_bound", "hard_upper_bound")
    @classmethod
    def _validate_finite_decimal(cls, value: Decimal, info) -> Decimal:
        return _finite(value, field_name=info.field_name)

    @model_validator(mode="after")
    def _validate_bounds(self) -> "CoefficientMember":
        if self.hard_lower_bound > self.hard_upper_bound:
            raise ValueError("coefficient_hard_bounds_out_of_order")
        if not self.hard_lower_bound <= self.baseline_value <= self.hard_upper_bound:
            raise ValueError("coefficient_baseline_outside_hard_bounds")
        return self


class ModifierMember(BaseModel):
    """One immutable modifier admitted by an M07 policy bundle."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    modifier_id: str = Field(min_length=1)
    modifier_version: str = Field(min_length=1)
    owner_stage: str = Field(min_length=1)
    target_coefficient_ids: tuple[str, ...] = Field(min_length=1)
    applicability_fact_refs: tuple[str, ...] = Field(min_length=1)
    precedence_rank: StrictInt
    transform_operator: TransformOperator
    operand: Decimal
    combination_law: Literal["authority_ordered"]
    conflict_modifier_ids: tuple[str, ...] = ()
    veto_modifier_ids: tuple[str, ...] = ()
    kill_switch: StrictBool = False
    restrictive_only: StrictBool = False
    promotion_lineage: str = Field(min_length=1)

    @field_validator("operand")
    @classmethod
    def _validate_operand(cls, value: Decimal) -> Decimal:
        return _finite(value, field_name="modifier_operand")

    @model_validator(mode="after")
    def _validate_member_law(self) -> "ModifierMember":
        collections = {
            "target_coefficient_ids": self.target_coefficient_ids,
            "applicability_fact_refs": self.applicability_fact_refs,
            "conflict_modifier_ids": self.conflict_modifier_ids,
            "veto_modifier_ids": self.veto_modifier_ids,
        }
        for field_name, values in collections.items():
            if any(not value for value in values):
                raise ValueError(f"{field_name}_contains_empty_identity")
            if len(values) != len(set(values)):
                raise ValueError(f"{field_name}_contains_duplicate_identity")
        if self.modifier_id in self.conflict_modifier_ids:
            raise ValueError("modifier_cannot_conflict_with_itself")
        if self.modifier_id in self.veto_modifier_ids:
            raise ValueError("modifier_cannot_veto_itself")
        if self.kill_switch:
            if self.transform_operator != "set" or self.operand != Decimal("0"):
                raise ValueError("kill_switch_must_set_zero")
            if not self.restrictive_only:
                raise ValueError("kill_switch_must_be_restrictive_only")
        return self


class PolicyBundle(BaseModel):
    """Immutable, versioned M07 coefficient/modifier authority bundle."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    bundle_id: str = Field(min_length=1)
    bundle_version: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    authority_id: str = Field(min_length=1)
    authority_version: str = Field(min_length=1)
    effective_version_selector: str = Field(min_length=1)
    resolution_law_version: str = Field(min_length=1)
    promotion_lineage: str = Field(min_length=1)
    owner_stage: str = Field(min_length=1)
    coefficients: tuple[CoefficientMember, ...] = Field(min_length=1)
    modifiers: tuple[ModifierMember, ...] = ()

    @model_validator(mode="after")
    def _validate_bundle_law(self) -> "PolicyBundle":
        coefficient_ids = [item.coefficient_id for item in self.coefficients]
        if len(coefficient_ids) != len(set(coefficient_ids)):
            raise ValueError("duplicate_coefficient_identity")
        modifier_ids = [item.modifier_id for item in self.modifiers]
        if len(modifier_ids) != len(set(modifier_ids)):
            raise ValueError("duplicate_modifier_identity")

        coefficients = {item.coefficient_id: item for item in self.coefficients}
        modifiers = set(modifier_ids)
        for coefficient in self.coefficients:
            if coefficient.owner_stage != self.owner_stage:
                raise ValueError("coefficient_owner_stage_mismatch")
        for modifier in self.modifiers:
            if modifier.owner_stage != self.owner_stage:
                raise ValueError("modifier_owner_stage_mismatch")
            for target_id in modifier.target_coefficient_ids:
                target = coefficients.get(target_id)
                if target is None:
                    raise ValueError("modifier_targets_unknown_coefficient")
                if target.owner_stage != modifier.owner_stage:
                    raise ValueError("modifier_target_owner_stage_mismatch")
            unknown_conflicts = set(modifier.conflict_modifier_ids).difference(modifiers)
            if unknown_conflicts:
                raise ValueError("modifier_conflict_reference_unknown")
            unknown_vetoes = set(modifier.veto_modifier_ids).difference(modifiers)
            if unknown_vetoes:
                raise ValueError("modifier_veto_reference_unknown")
            if modifier.kill_switch:
                for target_id in modifier.target_coefficient_ids:
                    target = coefficients[target_id]
                    if not target.hard_lower_bound <= Decimal("0") <= target.hard_upper_bound:
                        raise ValueError("kill_switch_target_bounds_exclude_zero")
        return self


class InputStateFacts(BaseModel):
    """Identified owner facts supplied to the side-effect-free K12 resolver."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    context_id: str = Field(min_length=1)
    context_version: str = Field(min_length=1)
    effective_at_utc: datetime
    fingerprint: str = Field(min_length=1)
    facts: dict[str, StrictBool]

    @field_validator("facts")
    @classmethod
    def _validate_facts(cls, value: dict[str, StrictBool]) -> dict[str, StrictBool]:
        if any(not key for key in value):
            raise ValueError("input_fact_identity_must_not_be_empty")
        return dict(value)


class ModifierDisposition(BaseModel):
    """One ordered evaluated, applied or skipped modifier fact."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    modifier_id: str = Field(min_length=1)
    modifier_version: str = Field(min_length=1)
    precedence_rank: StrictInt
    reason: str = Field(min_length=1)


class CoefficientResolution(BaseModel):
    """Baseline-to-effective lineage for one coefficient."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    coefficient_id: str = Field(min_length=1)
    coefficient_version: str = Field(min_length=1)
    baseline_value: Decimal
    pre_clamp_candidate: Decimal
    hard_lower_bound: Decimal
    hard_upper_bound: Decimal
    effective_value: Decimal
    bound_disposition: BoundDisposition


class ModifierDecision(BaseModel):
    """Deterministic, side-effect-free M07 K12 resolution result."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    decision_id: str = Field(min_length=1)
    semantic_fingerprint: str | None = None
    bundle_id: str | None = None
    bundle_version: str | None = None
    schema_version: str | None = None
    authority_id: str | None = None
    authority_version: str | None = None
    resolution_law_version: str | None = None
    owner_stage: str | None = None
    input_context_id: str | None = None
    input_context_version: str | None = None
    input_effective_at_utc: datetime | None = None
    input_fingerprint: str | None = None
    status: DecisionStatus
    evaluated_modifiers: tuple[ModifierDisposition, ...] = ()
    applied_modifiers: tuple[ModifierDisposition, ...] = ()
    skipped_modifiers: tuple[ModifierDisposition, ...] = ()
    coefficient_results: tuple[CoefficientResolution, ...] = ()
    conflict_dispositions: tuple[str, ...] = ()
    veto_dispositions: tuple[str, ...] = ()
    kill_switch_dispositions: tuple[str, ...] = ()
    rejection_reasons: tuple[str, ...] = ()
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES

    @model_validator(mode="after")
    def _validate_decision_shape(self) -> "ModifierDecision":
        if self.status == "rejected":
            if not self.rejection_reasons:
                raise ValueError("rejected_decision_requires_reason")
            if self.coefficient_results:
                raise ValueError("rejected_decision_must_not_carry_effective_values")
        else:
            if self.rejection_reasons:
                raise ValueError("accepted_decision_must_not_carry_rejection_reason")
            required = (
                self.owner_stage,
                self.semantic_fingerprint,
                self.bundle_id,
                self.bundle_version,
                self.schema_version,
                self.authority_id,
                self.authority_version,
                self.resolution_law_version,
                self.input_context_id,
                self.input_context_version,
                self.input_effective_at_utc,
                self.input_fingerprint,
            )
            if any(value is None for value in required):
                raise ValueError("accepted_decision_requires_complete_lineage")
            if not self.coefficient_results:
                raise ValueError("accepted_decision_requires_coefficient_results")
        if self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES:
            raise ValueError("decision_closed_authority_classes_must_remain_closed")
        return self


class ModifierApplicationReceipt(BaseModel):
    """Immutable M07 evidence for one non-rejected K12 decision context."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str = Field(min_length=1)
    application_id: str = Field(min_length=1)
    source_decision_id: str = Field(min_length=1)
    source_decision_fingerprint: str = Field(min_length=1)
    bundle_id: str = Field(min_length=1)
    bundle_version: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    authority_id: str = Field(min_length=1)
    authority_version: str = Field(min_length=1)
    resolution_law_version: str = Field(min_length=1)
    owner_stage: str = Field(min_length=1)
    input_context_id: str = Field(min_length=1)
    input_context_version: str = Field(min_length=1)
    input_effective_at_utc: datetime
    input_fingerprint: str = Field(min_length=1)
    decision_status: Literal["applied", "no_modifier_members", "no_applicable_modifiers"]
    applied_modifiers: tuple[ModifierDisposition, ...] = ()
    skipped_modifiers: tuple[ModifierDisposition, ...] = ()
    coefficient_results: tuple[CoefficientResolution, ...] = Field(min_length=1)
    conflict_dispositions: tuple[str, ...] = ()
    veto_dispositions: tuple[str, ...] = ()
    kill_switch_dispositions: tuple[str, ...] = ()
    no_op_class: Literal["no_modifier_members", "no_applicable_modifiers"] | None = None
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES
    limitations: tuple[str, ...] = (
        "resolution_only",
        "external_state_mutation_not_proven",
    )
    external_mutation_proven: Literal[False] = False
    emitted_at_utc: datetime

    @model_validator(mode="after")
    def _validate_receipt_law(self) -> "ModifierApplicationReceipt":
        if not _is_utc(self.input_effective_at_utc):
            raise ValueError("receipt_input_state_time_must_be_utc")
        if not _is_utc(self.emitted_at_utc):
            raise ValueError("receipt_emission_time_must_be_utc")
        expected_no_op = (
            self.decision_status
            if self.decision_status in {"no_modifier_members", "no_applicable_modifiers"}
            else None
        )
        if self.no_op_class != expected_no_op:
            raise ValueError("receipt_no_op_class_mismatch")
        if self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES:
            raise ValueError("receipt_closed_authority_classes_must_remain_closed")
        return self
