from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PermissionState(StrEnum):
    ALLOW = "allow"
    DERISK = "derisk"
    BLOCK = "block"


class PosturePermissionEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    permission_state: PermissionState
    local_envelope: dict = Field(default_factory=dict)
    hard_invariants: list[str] = Field(default_factory=list)


class PostureRiskOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    permission_state: PermissionState
    local_envelope: dict = Field(default_factory=dict)
    hard_invariants: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
