from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.contracts.modifiers import ResolvedCoefficientValue


class ReviewFailureClass(StrEnum):
    """Bounded review failure classes for decision-basis reconstruction."""

    DIAGNOSIS_FAILURE = "diagnosis_failure"
    POSTURE_POLICY_FAILURE = "posture_policy_failure"
    ELIGIBILITY_FAILURE = "eligibility_failure"
    EXECUTION_EXPRESSION_FAILURE = "execution_expression_failure"
    SIZING_FAILURE = "sizing_failure"
    DATA_PROVENANCE_FAILURE = "data_provenance_failure"
    ONTOLOGY_FAILURE = "ontology_failure"


class ReviewResolutionClass(StrEnum):
    """Bounded review outcomes for action, non-action, ambiguity, and luck."""

    ACTION_TAKEN = "action_taken"
    NON_ACTION = "non_action"
    BLOCKED_TRADE = "blocked_trade"
    UNKNOWN = "unknown"
    UNRESOLVED = "unresolved"
    BAD_LUCK = "bad_luck"
    ONTOLOGY_FAILURE = "ontology_failure"


class EconomicContributionTag(StrEnum):
    """Bounded economic-accountability labels for review-only attribution."""

    VALUE_ADD = "value_add"
    CAPITAL_PRESERVATION = "capital_preservation"
    NEUTRAL = "neutral"
    VALUE_LEAK = "value_leak"
    UNKNOWN = "unknown"


class ReviewPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    packet_id: str | None = None
    summary: str | None = None
    sections: list[str] = Field(default_factory=list)


class ReviewLineage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_ids: list[str] = Field(default_factory=list)
    resolved_surfaces: list[str] = Field(default_factory=list)
    resolved_coefficients: list[ResolvedCoefficientValue] = Field(default_factory=list)


class PromotionEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ready_for_candidate_review: bool = False
    required_sections: list[str] = Field(default_factory=list)
    missing_sections: list[str] = Field(default_factory=list)


class FailureTaxonomyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)
    primary_failure_class: ReviewFailureClass | None = None
    resolution: ReviewResolutionClass = ReviewResolutionClass.UNKNOWN
    blocked_trade: bool = False
    non_action: bool = False
    evidence_floor: dict[str, Any] | None = None
    rationale: list[str] = Field(default_factory=list)


class EconomicAccountabilityRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)
    diagnosis: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    posture: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    timing: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    execution: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    sizing: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    non_action: EconomicContributionTag = EconomicContributionTag.NEUTRAL


class EffectivePolicySnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")
    policy_ids: list[str] = Field(default_factory=list)
    resolved_surfaces: list[str] = Field(default_factory=list)
    resolved_coefficients: list[ResolvedCoefficientValue] = Field(default_factory=list)


class ReviewLineagePacket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_lineage_keys: list[str] = Field(default_factory=list)
    resolved_surfaces: list[str] = Field(default_factory=list)
    modifier_policy_ids: list[str] = Field(default_factory=list)
    resolved_coefficients: list[ResolvedCoefficientValue] = Field(default_factory=list)


class PacketLineageSurface(BaseModel):
    model_config = ConfigDict(extra="forbid")
    packet_ids: list[str] = Field(default_factory=list)
    source_packet_ids: list[str] = Field(default_factory=list)
