"""M08-owned contracts for immutable playbook catalogue and eligibility authority."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from hashlib import sha256
from math import isfinite
from typing import Any, Literal

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
    "stand_down_posture_blocked",
    "stand_down_no_candidate_families",
    "stand_down_no_eligible_candidates",
    "eligible",
]
JsonScalar = str | int | float | bool | None

CLOSED_AUTHORITY_CLASSES: tuple[str, ...] = (
    "candidate_expression",
    "capital",
    "broker_order",
    "position_inventory",
    "exit_close",
    "coefficient",
    "source_ingress",
    "replay",
    "transaction",
)


class FrozenDict(dict):
    """Small deeply non-mutable mapping that retains normal dict equality."""

    @staticmethod
    def _blocked(*_args, **_kwargs):
        raise TypeError("frozen_mapping")

    __setitem__ = _blocked
    __delitem__ = _blocked
    clear = _blocked
    pop = _blocked
    popitem = _blocked
    setdefault = _blocked
    update = _blocked
    __ior__ = _blocked


def _is_utc(value: datetime) -> bool:
    return (
        value.tzinfo is not None
        and value.utcoffset() is not None
        and value.utcoffset() == UTC.utcoffset(value)
    )


def _validate_scalar(value: Any, *, field_name: str) -> JsonScalar:
    if not isinstance(value, (str, int, float, bool)) and value is not None:
        raise ValueError(f"{field_name}_must_be_json_scalar")
    if isinstance(value, float) and not isfinite(value):
        raise ValueError(f"{field_name}_must_be_finite")
    return value


def _canonical_json(material: Any) -> str:
    return json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


class EligibilityConstraint(BaseModel):
    """One typed fact comparison declared by a playbook definition."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    fact_ref: str = Field(min_length=1)
    operator: Literal["eq"]
    expected: JsonScalar
    required: StrictBool = True

    @field_validator("expected")
    @classmethod
    def _validate_expected(cls, value: JsonScalar) -> JsonScalar:
        return _validate_scalar(value, field_name="constraint_expected")


class PlaybookDefinition(BaseModel):
    """One immutable, versioned M08 playbook and candidate-family definition."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    playbook_id: str = Field(min_length=1)
    playbook_version: str = Field(min_length=1)
    candidate_family_id: str = Field(min_length=1)
    candidate_family_version: str = Field(min_length=1)
    setup_variant_id: str = ""
    setup_variant_version: str = ""
    selection_priority: StrictInt
    constraints: tuple[EligibilityConstraint, ...] = Field(min_length=1)
    enabled: StrictBool = True
    lifecycle_intent: dict[str, str] = Field(min_length=1)
    lifecycle_schema_version: str = Field(min_length=1)
    promotion_lineage: str = Field(min_length=1)

    @field_validator("lifecycle_intent")
    @classmethod
    def _validate_lifecycle_intent(cls, value: dict[str, str]) -> dict[str, str]:
        if any(not key or not item for key, item in value.items()):
            raise ValueError("lifecycle_intent_contains_empty_value")
        return dict(value)

    @model_validator(mode="after")
    def _validate_variant_identity(self) -> "PlaybookDefinition":
        if bool(self.setup_variant_id) != bool(self.setup_variant_version):
            raise ValueError("setup_variant_identity_version_mismatch")
        return self

    @model_validator(mode="after")
    def _freeze_nested_mapping(self) -> "PlaybookDefinition":
        object.__setattr__(self, "lifecycle_intent", FrozenDict(self.lifecycle_intent))
        return self

    @property
    def identity_tuple(self) -> tuple[str, ...]:
        return (
            self.candidate_family_id,
            self.candidate_family_version,
            self.playbook_id,
            self.playbook_version,
            self.setup_variant_id,
            self.setup_variant_version,
        )


def definition_material(definition: PlaybookDefinition) -> dict[str, Any]:
    return {
        "playbook_id": definition.playbook_id,
        "playbook_version": definition.playbook_version,
        "candidate_family_id": definition.candidate_family_id,
        "candidate_family_version": definition.candidate_family_version,
        "setup_variant_id": definition.setup_variant_id,
        "setup_variant_version": definition.setup_variant_version,
        "selection_priority": definition.selection_priority,
        "constraints": [
            {
                "fact_ref": constraint.fact_ref,
                "operator": constraint.operator,
                "expected": constraint.expected,
                "required": constraint.required,
            }
            for constraint in definition.constraints
        ],
        "enabled": definition.enabled,
        "lifecycle_intent": dict(definition.lifecycle_intent),
        "lifecycle_schema_version": definition.lifecycle_schema_version,
        "promotion_lineage": definition.promotion_lineage,
    }


def catalogue_fingerprint(
    *,
    catalogue_id: str,
    catalogue_version: str,
    schema_version: str,
    authority_id: str,
    authority_version: str,
    effective_version_selector: str,
    eligibility_law_version: str,
    promotion_lineage: str,
    definitions: tuple[PlaybookDefinition, ...],
) -> str:
    material = {
        "catalogue_id": catalogue_id,
        "catalogue_version": catalogue_version,
        "schema_version": schema_version,
        "authority_id": authority_id,
        "authority_version": authority_version,
        "effective_version_selector": effective_version_selector,
        "eligibility_law_version": eligibility_law_version,
        "promotion_lineage": promotion_lineage,
        "definitions": [
            definition_material(definition)
            for definition in sorted(definitions, key=lambda item: item.identity_tuple)
        ],
    }
    return sha256(_canonical_json(material).encode("utf-8")).hexdigest()


class PlaybookCatalogue(BaseModel):
    """Immutable, versioned M08 authority snapshot for K13 resolution."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    catalogue_id: str = Field(min_length=1)
    catalogue_version: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    authority_id: str = Field(min_length=1)
    authority_version: str = Field(min_length=1)
    effective_version_selector: str = Field(min_length=1)
    eligibility_law_version: str = Field(min_length=1)
    promotion_lineage: str = Field(min_length=1)
    definitions: tuple[PlaybookDefinition, ...] = Field(min_length=1)
    catalogue_fingerprint: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_catalogue_law(self) -> "PlaybookCatalogue":
        identity_sets = {
            "duplicate_playbook_identity": [
                (item.playbook_id, item.playbook_version) for item in self.definitions
            ],
            "duplicate_candidate_family_identity": [
                (item.candidate_family_id, item.candidate_family_version)
                for item in self.definitions
            ],
            "duplicate_setup_variant_identity": [
                (item.setup_variant_id, item.setup_variant_version)
                for item in self.definitions
                if item.setup_variant_id
            ],
        }
        for reason, values in identity_sets.items():
            if len(values) != len(set(values)):
                raise ValueError(reason)
        expected = catalogue_fingerprint(
            catalogue_id=self.catalogue_id,
            catalogue_version=self.catalogue_version,
            schema_version=self.schema_version,
            authority_id=self.authority_id,
            authority_version=self.authority_version,
            effective_version_selector=self.effective_version_selector,
            eligibility_law_version=self.eligibility_law_version,
            promotion_lineage=self.promotion_lineage,
            definitions=self.definitions,
        )
        if self.catalogue_fingerprint != expected:
            raise ValueError("catalogue_fingerprint_mismatch")
        return self


class PosturePermission(BaseModel):
    """Identified owner-issued posture permission consumed by M08."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    posture_id: str
    posture_version: str
    status: Literal["permitted", "blocked"]
    effective_at_utc: datetime
    semantic_fingerprint: str


class FactAuthority(BaseModel):
    """One owner-issued material eligibility fact and its lineage."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    fact_ref: str
    owner_id: str
    contract_version: str
    effective_at_utc: datetime
    semantic_fingerprint: str
    value: JsonScalar

    @field_validator("value")
    @classmethod
    def _validate_value(cls, value: JsonScalar) -> JsonScalar:
        return _validate_scalar(value, field_name="fact_value")


class EligibilityContext(BaseModel):
    """Identified owner-issued eligibility context consumed by M08."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    context_id: str
    context_version: str
    effective_at_utc: datetime
    semantic_fingerprint: str
    facts: dict[str, FactAuthority]

    @model_validator(mode="after")
    def _freeze_facts(self) -> "EligibilityContext":
        object.__setattr__(self, "facts", FrozenDict(self.facts))
        return self


class DefinitionDisposition(BaseModel):
    """One deterministic skipped or ineligible definition disposition."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    playbook_id: str = Field(min_length=1)
    playbook_version: str = Field(min_length=1)
    candidate_family_id: str = Field(min_length=1)
    candidate_family_version: str = Field(min_length=1)
    setup_variant_id: str = ""
    setup_variant_version: str = ""
    reason: str = Field(min_length=1)


class EligibleCandidate(BaseModel):
    """One ordered M08 eligibility candidate carrying bounded handoff metadata."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    playbook_id: str = Field(min_length=1)
    playbook_version: str = Field(min_length=1)
    candidate_family_id: str = Field(min_length=1)
    candidate_family_version: str = Field(min_length=1)
    setup_variant_id: str = ""
    setup_variant_version: str = ""
    selection_priority: StrictInt
    lifecycle_intent: dict[str, str]
    lifecycle_schema_version: str = Field(min_length=1)
    promotion_lineage: str = Field(min_length=1)

    @model_validator(mode="after")
    def _freeze_nested_mapping(self) -> "EligibleCandidate":
        object.__setattr__(self, "lifecycle_intent", FrozenDict(self.lifecycle_intent))
        return self

    @property
    def identity_tuple(self) -> tuple[str, ...]:
        return (
            self.candidate_family_id,
            self.candidate_family_version,
            self.playbook_id,
            self.playbook_version,
            self.setup_variant_id,
            self.setup_variant_version,
        )


class EligibilityDecision(BaseModel):
    """Deterministic, side-effect-free M08 K13 eligibility result."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    decision_id: str = Field(min_length=1)
    decision_schema_version: str = "1.0.0"
    semantic_fingerprint: str | None = None
    status: DecisionStatus
    reason: str | None = None
    catalogue_id: str | None = None
    catalogue_version: str | None = None
    catalogue_schema_version: str | None = None
    authority_id: str | None = None
    authority_version: str | None = None
    eligibility_law_version: str | None = None
    catalogue_fingerprint: str | None = None
    catalogue_promotion_lineage: str | None = None
    posture_id: str | None = None
    posture_version: str | None = None
    posture_status: str | None = None
    posture_effective_at_utc: datetime | None = None
    posture_fingerprint: str | None = None
    context_id: str | None = None
    context_version: str | None = None
    context_effective_at_utc: datetime | None = None
    context_fingerprint: str | None = None
    material_fact_lineage: tuple[FactAuthority, ...] = ()
    skipped_definitions: tuple[DefinitionDisposition, ...] = ()
    ineligible_definitions: tuple[DefinitionDisposition, ...] = ()
    eligible_candidates: tuple[EligibleCandidate, ...] = ()
    eligibility_lead: EligibleCandidate | None = None
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES
    foreign_authority_claimed: Literal[False] = False

    @model_validator(mode="after")
    def _validate_decision_law(self) -> "EligibilityDecision":
        if self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES:
            raise ValueError("closed_authority_classes_mismatch")
        if self.status == "rejected":
            if self.semantic_fingerprint is not None:
                raise ValueError("rejected_decision_must_not_bind_semantic_fingerprint")
            if self.eligible_candidates or self.eligibility_lead is not None:
                raise ValueError("rejected_decision_must_not_bind_eligibility")
            return self
        required_lineage = (
            self.semantic_fingerprint,
            self.catalogue_id,
            self.catalogue_version,
            self.catalogue_schema_version,
            self.authority_id,
            self.authority_version,
            self.eligibility_law_version,
            self.catalogue_fingerprint,
            self.catalogue_promotion_lineage,
            self.posture_id,
            self.posture_version,
            self.posture_status,
            self.posture_effective_at_utc,
            self.posture_fingerprint,
            self.context_id,
            self.context_version,
            self.context_effective_at_utc,
            self.context_fingerprint,
        )
        if any(value is None or value == "" for value in required_lineage):
            raise ValueError("non_rejected_decision_lineage_incomplete")
        if self.status == "eligible":
            if not self.eligible_candidates or self.eligibility_lead is None:
                raise ValueError("eligible_decision_requires_candidates_and_lead")
            if self.eligibility_lead != self.eligible_candidates[0]:
                raise ValueError("eligibility_lead_must_be_first_ordered_candidate")
        elif self.eligible_candidates or self.eligibility_lead is not None:
            raise ValueError("stand_down_decision_must_not_bind_eligibility")
        return self


__all__ = [
    "CLOSED_AUTHORITY_CLASSES",
    "EligibilityContext",
    "EligibilityDecision",
    "EligibleCandidate",
    "FactAuthority",
    "PlaybookCatalogue",
    "PlaybookDefinition",
    "PosturePermission",
    "catalogue_fingerprint",
]
