"""Typed coefficient-authority contracts for workbook-derived runtime promotion."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SurfaceClass(StrEnum):
    """Lawful coefficient classes for promoted runtime authority."""

    MUTABLE_RUNTIME_SURFACE = "mutable_runtime_surface"
    BASELINE_ONLY_SURFACE = "baseline_only_surface"
    PROHIBITED_FIXED_SURFACE = "prohibited_fixed_surface"
    WORKBOOK_RESEARCH_BAND_SURFACE = "workbook_research_band_surface"


class WorkbookLineageRef(BaseModel):
    """Explicit lineage back to one governed workbook concept or row."""

    model_config = ConfigDict(extra="forbid")
    workbook_path: str
    sheet_name: str
    cell_range: str
    lineage_note: str | None = None


class ModifierEffectRecord(BaseModel):
    """One bounded modifier effect over one admitted coefficient surface."""

    model_config = ConfigDict(extra="forbid")
    coefficient_id: str
    transform_family: str
    effective_value: float | bool
    rationale: str | None = None


class ModifierPolicyRecord(BaseModel):
    """One admitted runtime modifier policy and its bounded surface effects."""

    model_config = ConfigDict(extra="forbid")
    policy_id: str
    owner_stage: str
    admitted_surfaces: list[str] = Field(default_factory=list)
    effects: list[ModifierEffectRecord] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_effects(self) -> "ModifierPolicyRecord":
        """Validate each policy declares a unique, admitted effect surface."""

        effect_ids = [effect.coefficient_id for effect in self.effects]
        if len(effect_ids) != len(set(effect_ids)):
            raise ValueError(
                f"duplicate modifier effect coefficients are not allowed for {self.policy_id}"
            )
        undeclared = sorted(set(effect_ids) - set(self.admitted_surfaces))
        if undeclared:
            raise ValueError(
                f"modifier policy {self.policy_id} includes effects outside admitted_surfaces: {undeclared}"
            )
        return self


class CoefficientAuthorityRecord(BaseModel):
    """One promoted coefficient or threshold with bounded runtime authority."""

    model_config = ConfigDict(extra="forbid")
    coefficient_id: str
    owner_stage: str
    surface_class: SurfaceClass
    baseline_value: float | bool
    hard_floor: float | str | None = None
    hard_cap: float | str | None = None
    transform_family: str
    runtime_mutable: bool = False
    workbook_ref: WorkbookLineageRef
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_bounds(self) -> "CoefficientAuthorityRecord":
        """Validate coefficient baselines and declared hard bounds."""

        if isinstance(self.baseline_value, bool):
            if self.runtime_mutable and self.transform_family.startswith("baseline_only"):
                raise ValueError(
                    f"boolean baseline-only surface cannot be marked runtime_mutable: {self.coefficient_id}"
                )
            valid_floor = self.hard_floor in {None, False, "FALSE_ONLY"}
            valid_cap = self.hard_cap in {None, True, "TRUE_ONLY"}
            if not valid_floor or not valid_cap:
                raise ValueError(
                    f"boolean coefficient {self.coefficient_id} must use FALSE_ONLY / TRUE_ONLY style bounds"
                )
            return self

        if not isinstance(self.baseline_value, (int, float)):
            raise ValueError(f"baseline_value must be numeric or boolean for {self.coefficient_id}")
        if not isinstance(self.hard_floor, (int, float)) or not isinstance(
            self.hard_cap, (int, float)
        ):
            raise ValueError(
                f"numeric coefficient {self.coefficient_id} must declare numeric hard_floor and hard_cap"
            )
        if float(self.hard_floor) > float(self.baseline_value):
            raise ValueError(f"hard_floor cannot exceed baseline_value for {self.coefficient_id}")
        if float(self.hard_cap) < float(self.baseline_value):
            raise ValueError(f"hard_cap cannot be below baseline_value for {self.coefficient_id}")
        if float(self.hard_floor) > float(self.hard_cap):
            raise ValueError(f"hard_floor cannot exceed hard_cap for {self.coefficient_id}")
        if self.surface_class == SurfaceClass.BASELINE_ONLY_SURFACE and self.runtime_mutable:
            raise ValueError(
                f"baseline-only surfaces cannot be runtime_mutable: {self.coefficient_id}"
            )
        return self


class CoefficientAuthorityDocument(BaseModel):
    """Whole governed coefficient-authority document promoted from workbook concepts."""

    model_config = ConfigDict(extra="forbid")
    authority_id: str
    schema_version: str
    workbook_source_path: str
    notes: list[str] = Field(default_factory=list)
    records: list[CoefficientAuthorityRecord] = Field(default_factory=list)
    modifier_policies: list[ModifierPolicyRecord] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_document(self) -> "CoefficientAuthorityDocument":
        """Validate document-level uniqueness, ownership, and bounded policy effects."""

        records_by_id = self.record_map()
        record_ids = list(records_by_id)
        if len(record_ids) != len(self.records):
            raise ValueError("coefficient_id values must be unique within coefficient authority")
        known_records = set(record_ids)
        for policy in self.modifier_policies:
            unknown = sorted(set(policy.admitted_surfaces) - known_records)
            if unknown:
                raise ValueError(
                    f"modifier policy {policy.policy_id} declares unknown admitted surfaces: {unknown}"
                )
            for effect in policy.effects:
                record = records_by_id[effect.coefficient_id]
                self._validate_policy_effect(policy=policy, record=record, effect=effect)
        return self

    @staticmethod
    def _validate_policy_effect(
        *,
        policy: ModifierPolicyRecord,
        record: CoefficientAuthorityRecord,
        effect: ModifierEffectRecord,
    ) -> None:
        """Validate one effect cannot widen or cross ownership/runtime authority."""

        if record.owner_stage != policy.owner_stage:
            raise ValueError(
                f"modifier policy {policy.policy_id} crosses owner_stage for {record.coefficient_id}"
            )
        if not record.runtime_mutable:
            raise ValueError(
                f"modifier policy {policy.policy_id} targets surface_class="
                f"{record.surface_class.value} for {record.coefficient_id}"
            )
        if effect.transform_family != record.transform_family:
            raise ValueError(
                f"modifier policy {policy.policy_id} transform_family mismatch for "
                f"{record.coefficient_id}"
            )
        if isinstance(record.baseline_value, bool):
            if not isinstance(effect.effective_value, bool):
                raise ValueError(
                    f"boolean coefficient {record.coefficient_id} requires boolean effective_value"
                )
            return
        if isinstance(effect.effective_value, bool) or not isinstance(
            effect.effective_value, (int, float)
        ):
            raise ValueError(
                f"numeric coefficient {record.coefficient_id} requires numeric effective_value"
            )
        if not isinstance(record.hard_floor, (int, float)) or not isinstance(
            record.hard_cap, (int, float)
        ):
            raise ValueError(f"numeric coefficient {record.coefficient_id} requires numeric bounds")
        if float(effect.effective_value) < float(record.hard_floor) or float(
            effect.effective_value
        ) > float(record.hard_cap):
            raise ValueError(
                f"modifier policy {policy.policy_id} effective_value for {record.coefficient_id} "
                "is outside hard bounds"
            )

    def record_map(
        self, *, owner_stage: str | None = None
    ) -> dict[str, CoefficientAuthorityRecord]:
        """Return coefficient records keyed by id, optionally filtered by owner stage."""

        records = self.records
        if owner_stage is not None:
            records = [record for record in records if record.owner_stage == owner_stage]
        return {record.coefficient_id: record for record in records}


def coefficient_authority_document_from_dict(
    payload: dict[str, Any],
) -> CoefficientAuthorityDocument:
    """Build and validate one coefficient-authority document from a plain dict."""

    return CoefficientAuthorityDocument(**payload)
