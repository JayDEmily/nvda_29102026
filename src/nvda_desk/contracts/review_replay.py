"""Contracts for deterministic imported-module review replay comparisons."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CitationAdmissionClass = Literal["admitted_partial", "rejected", "superseded", "reserved"]
CitationDecisionStatus = Literal["accepted_for_review_only", "rejected", "superseded", "reserved"]


class ImportedModuleCitation(BaseModel):
    """One imported-module claim cited during review-only replay work."""

    model_config = ConfigDict(extra="forbid")

    source_identifier: str = Field(min_length=1)
    imported_module: str = Field(min_length=1)
    cited_claim: str = Field(min_length=1)


class ReviewReplayDecision(BaseModel):
    """PM or review decision attached to one imported-module citation."""

    model_config = ConfigDict(extra="forbid")

    source_identifier: str = Field(min_length=1)
    decision_id: str = Field(min_length=1)
    admission_class: CitationAdmissionClass
    status: CitationDecisionStatus
    rejection_reason: str | None = None


class ImportedModuleCitationTrace(BaseModel):
    """Traceable citation row joined to its governing review-replay decision."""

    model_config = ConfigDict(extra="forbid")

    source_identifier: str = Field(min_length=1)
    imported_module: str = Field(min_length=1)
    cited_claim: str = Field(min_length=1)
    decision_id: str = Field(min_length=1)
    admission_class: CitationAdmissionClass
    rejection_or_supersession_status: CitationDecisionStatus
    rejection_reason: str | None = None


class ReviewReplayComparisonResult(BaseModel):
    """Deterministic comparison result for imported-module citation replay."""

    model_config = ConfigDict(extra="forbid")

    compared_source_identifiers: list[str] = Field(default_factory=list)
    missing_decision_source_identifiers: list[str] = Field(default_factory=list)
    citation_traces: list[ImportedModuleCitationTrace] = Field(default_factory=list)
    promoted_to_runtime: bool = False
    runtime_side_effects: list[str] = Field(default_factory=list)
