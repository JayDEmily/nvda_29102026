from __future__ import annotations

from copy import deepcopy
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class _DetachedMutableModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def _detach_mutable_inputs(cls, value: Any) -> Any:
        return deepcopy(value)


class ExecutionExpressionInput(_DetachedMutableModel):
    model_config = ConfigDict(extra="forbid")
    temporal: dict = Field(default_factory=dict)
    regime: dict = Field(default_factory=dict)
    options_flow: dict = Field(default_factory=dict)
    posture: dict = Field(default_factory=dict)
    eligibility: dict = Field(default_factory=dict)


class ExecutionExpressionOutput(_DetachedMutableModel):
    model_config = ConfigDict(extra="forbid")
    candidate_id: str | None = None
    lead_playbook_id: str | None = None
    scaling_plan: list[str] = Field(default_factory=list)
    final_risk_join: dict | None = None
    active_playbook_ids: list[str] = Field(default_factory=list)


class StageLocalHandoffSurface(_DetachedMutableModel):
    model_config = ConfigDict(extra="forbid")
    execution_post_modifier_pre_final_risk: dict = Field(default_factory=dict)
    lineage_tags: list[str] = Field(default_factory=list)
