from __future__ import annotations

from copy import deepcopy
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ResolvedCoefficientValue(BaseModel):
    """One resolved coefficient snapshot with baseline/effective lineage."""

    model_config = ConfigDict(extra="forbid")
    coefficient_id: str
    owner_stage: str
    surface_class: str
    baseline_value: float | bool
    effective_value: float | bool
    transform_family: str
    modifier_inputs: list[str] = Field(default_factory=list)
    workbook_ref: str
    runtime_mutable: bool = False

    @model_validator(mode="after")
    def detach_modifier_inputs(self) -> "ResolvedCoefficientValue":
        """Detach caller-owned modifier lineage lists on model construction."""

        self.modifier_inputs = list(self.modifier_inputs)
        return self


def _detached_coefficient(
    coefficient: ResolvedCoefficientValue | dict[str, Any],
) -> ResolvedCoefficientValue:
    if isinstance(coefficient, ResolvedCoefficientValue):
        return ResolvedCoefficientValue.model_validate(deepcopy(coefficient.model_dump()))
    return ResolvedCoefficientValue.model_validate(deepcopy(dict(coefficient)))


class ModifierRuntimePacket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    packet_id: str | None = None
    active_modifier_ids: list[str] = Field(default_factory=list)
    policy_ids: list[str] = Field(default_factory=list)
    resolved_surfaces: list[str] = Field(default_factory=list)
    resolved_coefficients: list[ResolvedCoefficientValue] = Field(default_factory=list)

    @model_validator(mode="after")
    def detach_lineage_lists(self) -> "ModifierRuntimePacket":
        """Detach caller-owned modifier packet lineage containers."""

        self.active_modifier_ids = list(self.active_modifier_ids)
        self.policy_ids = list(self.policy_ids)
        self.resolved_surfaces = list(self.resolved_surfaces)
        self.resolved_coefficients = [
            _detached_coefficient(coefficient)
            for coefficient in self.resolved_coefficients
        ]
        return self


class ModifierReplayReceipt(BaseModel):
    """Deterministic replay receipt for bounded coefficient/modifier authority."""

    model_config = ConfigDict(extra="forbid")
    authority_id: str
    schema_version: str
    owner_stage: str
    active_modifier_ids: list[str] = Field(default_factory=list)
    resolved_coefficients: list[ResolvedCoefficientValue] = Field(default_factory=list)
    replay_fingerprint: str
    closed_authority_classes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def detach_lineage_lists(self) -> "ModifierReplayReceipt":
        """Detach caller-owned replay lineage containers."""

        self.active_modifier_ids = list(self.active_modifier_ids)
        self.resolved_coefficients = [
            _detached_coefficient(coefficient)
            for coefficient in self.resolved_coefficients
        ]
        self.closed_authority_classes = list(self.closed_authority_classes)
        return self
