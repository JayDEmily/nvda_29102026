from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ModuleClass(StrEnum):
    SIGNAL = "signal"
    VETO = "veto"
    SIZING = "sizing"
    EXECUTION = "execution"


class ModuleStatus(StrEnum):
    PLANNED = "planned"
    DRAFT = "draft"
    CODED = "coded"
    BACKTESTED = "backtested"
    PAPER_CANDIDATE = "paper_candidate"
    APPROVED = "approved"
    RETIRED = "retired"


class ModuleDescriptor(BaseModel):
    module_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    module_class: ModuleClass
    status: ModuleStatus = ModuleStatus.PLANNED
    thesis: str = Field(min_length=1)


class ModuleSpecCreate(BaseModel):
    descriptor: ModuleDescriptor
    required_inputs: list[str] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)
    notes_md: str = Field(default="", min_length=0)
    source_refs: list[str] = Field(default_factory=list)


class ModuleSpecPayload(BaseModel):
    spec_id: int
    created_at: datetime
    descriptor: ModuleDescriptor
    required_inputs: list[str]
    parameters: dict[str, Any]
    notes_md: str
    source_refs: list[str]


class ModuleSpecListResponse(BaseModel):
    specs: list[ModuleSpecPayload]


class PromotionDecisionCreate(BaseModel):
    module_id: str = Field(min_length=1)
    from_status: ModuleStatus
    to_status: ModuleStatus
    decision_reason: str = Field(min_length=1)
    evaluation_ids: list[int] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    approved_by: str = Field(default="operator", min_length=1)


class PromotionDecisionPayload(BaseModel):
    decision_id: int
    created_at: datetime
    module_id: str
    from_status: ModuleStatus
    to_status: ModuleStatus
    decision_reason: str
    evaluation_ids: list[int]
    evidence_refs: list[str]
    approved_by: str


class PromotionDecisionListResponse(BaseModel):
    decisions: list[PromotionDecisionPayload]
