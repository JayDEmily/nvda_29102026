"""Immutable M12 K19 review and replay contracts."""

from __future__ import annotations

from datetime import UTC, datetime
from importlib import import_module
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .fingerprint import semantic_fingerprint

ReplayClass = Literal[
    "preserved_occurrence_replay",
    "governed_semantic_reexecution",
    "comparison_only",
]
ReplayAuthorityStatus = Literal[
    "authoritative_match",
    "semantic_mismatch",
    "non_authoritative_incomplete",
    "comparison_only",
]


def _hash(value: str, reason: str) -> str:
    if len(value) != 64:
        raise ValueError(reason)
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(reason) from exc
    return value


def _nonempty(value: str, reason: str) -> str:
    token = str(value).strip()
    if not token:
        raise ValueError(reason)
    return token


def _unique_nonblank(values: tuple[str, ...], reason: str) -> tuple[str, ...]:
    normalised = tuple(_nonempty(value, reason) for value in values)
    if len(set(normalised)) != len(normalised):
        raise ValueError(reason)
    return normalised


def _material(model: BaseModel, *, exclude: set[str]) -> dict[str, Any]:
    return model.model_dump(mode="python", exclude=exclude)


class ReplayMaterial(BaseModel):
    """One verified retained evidence item in deterministic replay order."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    material_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    owner_module: str = Field(min_length=3, max_length=3)
    contract_path: str = Field(min_length=1)
    contract_name: str = Field(min_length=1)
    owner_contract_version: str = Field(min_length=1)
    occurrence_id: str = Field(min_length=1)
    content_snapshot: dict[str, Any]
    content_fingerprint: str
    sequence: int = Field(ge=0)
    material_time_utc: datetime | None = None
    material_label: str = Field(min_length=1)
    verified: Literal[True] = True
    retrievable: Literal[True] = True
    semantic_fingerprint: str

    @field_validator("owner_module")
    @classmethod
    def _owner(cls, value: str) -> str:
        token = _nonempty(value, "owner_module_invalid")
        if len(token) != 3 or token[0] != "M" or not token[1:].isdigit():
            raise ValueError("owner_module_invalid")
        number = int(token[1:])
        if number < 0 or number > 15:
            raise ValueError("owner_module_invalid")
        return f"M{number:02d}"

    @field_validator("material_time_utc")
    @classmethod
    def _time(cls, value: datetime | None) -> datetime | None:
        if value is not None and (
            value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value)
        ):
            raise ValueError("material_time_must_be_utc")
        return value

    @model_validator(mode="after")
    def _law(self) -> "ReplayMaterial":
        contract_path = _nonempty(self.contract_path, "contract_path_must_be_nonempty")
        _nonempty(self.contract_name, "contract_name_must_be_nonempty")
        _nonempty(self.owner_contract_version, "owner_contract_version_must_be_nonempty")
        _nonempty(self.occurrence_id, "occurrence_id_must_be_nonempty")
        _nonempty(self.material_label, "material_label_must_be_nonempty")
        _hash(self.content_fingerprint, "material_content_fingerprint_invalid")
        if ":" not in contract_path:
            raise ValueError("replay_material_contract_path_invalid")
        module_name, qualname = contract_path.split(":", 1)
        if not module_name.startswith("nvda_desk.") or not qualname or "<locals>" in qualname:
            raise ValueError("replay_material_contract_path_invalid")
        try:
            contract_type: Any = import_module(module_name)
            for token in qualname.split("."):
                contract_type = getattr(contract_type, token)
        except (ImportError, AttributeError) as exc:
            raise ValueError("replay_material_contract_unavailable") from exc
        if not isinstance(contract_type, type) or not issubclass(contract_type, BaseModel):
            raise ValueError("replay_material_contract_not_pydantic")
        if contract_type.__name__ != self.contract_name:
            raise ValueError("replay_material_contract_name_mismatch")
        try:
            validated_content = contract_type.model_validate(self.content_snapshot)
        except Exception as exc:
            raise ValueError("replay_material_content_not_type_valid") from exc
        canonical_content = validated_content.model_dump(mode="python")
        if semantic_fingerprint(canonical_content) != self.content_fingerprint:
            raise ValueError("replay_material_content_fingerprint_mismatch")
        expected = semantic_fingerprint(
            _material(self, exclude={"material_id", "semantic_fingerprint"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("replay_material_fingerprint_mismatch")
        if self.material_id != f"replay-material:{expected[:24]}":
            raise ValueError("replay_material_id_mismatch")
        return self


class ReplayEnvelope(BaseModel):
    """K19 immutable envelope for one declared replay target and class."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    envelope_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    replay_run_id: str = Field(min_length=1)
    replay_class: ReplayClass
    target_id: str = Field(min_length=1)
    original_output_id: str = Field(min_length=1)
    original_output_occurrence_id: str = Field(min_length=1)
    original_output_fingerprint: str
    original_reasons: tuple[str, ...]
    materials: tuple[ReplayMaterial, ...]
    material_ids: tuple[str, ...]
    executable_versions: tuple[str, ...]
    missing_material: tuple[str, ...] = ()
    unverifiable_material: tuple[str, ...] = ()
    contradictions: tuple[str, ...] = ()
    live_side_effects_allowed: Literal[False] = False
    runtime_promotion_allowed: Literal[False] = False
    semantic_domain_fingerprint: str
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _law(self) -> "ReplayEnvelope":
        for field_name in (
            "replay_run_id",
            "target_id",
            "original_output_id",
            "original_output_occurrence_id",
        ):
            _nonempty(getattr(self, field_name), f"{field_name}_must_be_nonempty")
        _hash(self.original_output_fingerprint, "original_output_fingerprint_invalid")
        reasons = _unique_nonblank(
            self.original_reasons, "original_reasons_must_be_unique_nonblank"
        )
        materials = tuple(
            ReplayMaterial.model_validate(item.model_dump(mode="python")) for item in self.materials
        )
        if not materials:
            raise ValueError("replay_materials_must_be_nonempty")
        ids = tuple(item.material_id for item in materials)
        if ids != self.material_ids:
            raise ValueError("replay_material_ids_mismatch")
        if len(set(ids)) != len(ids):
            raise ValueError("replay_material_ids_must_be_unique")
        occurrences = tuple(item.occurrence_id for item in materials)
        if len(set(occurrences)) != len(occurrences):
            raise ValueError("replay_occurrence_ids_must_be_unique")
        sequences = tuple(item.sequence for item in materials)
        if any(later <= earlier for earlier, later in zip(sequences, sequences[1:])):
            raise ValueError("replay_material_sequence_must_be_strictly_increasing")
        executable = _unique_nonblank(
            self.executable_versions, "executable_versions_must_be_unique_nonblank"
        )
        if self.replay_class == "governed_semantic_reexecution" and not executable:
            raise ValueError("executable_versions_required_for_governed_reexecution")
        missing = _unique_nonblank(
            self.missing_material, "missing_material_must_be_unique_nonblank"
        )
        unverifiable = _unique_nonblank(
            self.unverifiable_material, "unverifiable_material_must_be_unique_nonblank"
        )
        contradictions = _unique_nonblank(
            self.contradictions, "contradictions_must_be_unique_nonblank"
        )
        domain_payload = {
            "contract_version": self.contract_version,
            "replay_class": self.replay_class,
            "target_id": self.target_id,
            "original_output_id": self.original_output_id,
            "original_output_occurrence_id": self.original_output_occurrence_id,
            "original_output_fingerprint": self.original_output_fingerprint,
            "original_reasons": reasons,
            "material_fingerprints": tuple(item.semantic_fingerprint for item in materials),
            "executable_versions": executable,
            "missing_material": missing,
            "unverifiable_material": unverifiable,
            "contradictions": contradictions,
            "live_side_effects_allowed": False,
            "runtime_promotion_allowed": False,
        }
        expected_domain = semantic_fingerprint(domain_payload)
        if self.semantic_domain_fingerprint != expected_domain:
            raise ValueError("replay_envelope_domain_fingerprint_mismatch")
        expected = semantic_fingerprint(
            {"replay_run_id": self.replay_run_id, "semantic_domain_fingerprint": expected_domain}
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("replay_envelope_fingerprint_mismatch")
        if self.envelope_id != f"replay-envelope:{expected[:24]}":
            raise ValueError("replay_envelope_id_mismatch")
        return self


class ReplayAssessment(BaseModel):
    """Immutable completeness and semantic-match classification for one envelope."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    assessment_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    envelope_id: str = Field(min_length=1)
    envelope_fingerprint: str
    replay_run_id: str = Field(min_length=1)
    replay_class: ReplayClass
    target_id: str = Field(min_length=1)
    authority_status: ReplayAuthorityStatus
    verified_material_ids: tuple[str, ...]
    missing_material: tuple[str, ...]
    unverifiable_material: tuple[str, ...]
    contradictions: tuple[str, ...]
    exact_matches: tuple[str, ...]
    mismatches: tuple[str, ...]
    reproduced_output_id: str | None = None
    reproduced_output_fingerprint: str | None = None
    live_side_effects_performed: Literal[False] = False
    runtime_authority_promoted: Literal[False] = False
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _law(self) -> "ReplayAssessment":
        _hash(self.envelope_fingerprint, "assessment_envelope_fingerprint_invalid")
        _unique_nonblank(
            self.verified_material_ids, "verified_material_ids_must_be_unique_nonblank"
        )
        missing = _unique_nonblank(
            self.missing_material, "missing_material_must_be_unique_nonblank"
        )
        unverifiable = _unique_nonblank(
            self.unverifiable_material, "unverifiable_material_must_be_unique_nonblank"
        )
        contradictions = _unique_nonblank(
            self.contradictions, "contradictions_must_be_unique_nonblank"
        )
        exact = _unique_nonblank(self.exact_matches, "exact_matches_must_be_unique_nonblank")
        mismatches = _unique_nonblank(self.mismatches, "mismatches_must_be_unique_nonblank")
        if self.reproduced_output_fingerprint is not None:
            _hash(self.reproduced_output_fingerprint, "reproduced_output_fingerprint_invalid")
        incomplete = bool(missing or unverifiable or contradictions)
        if self.authority_status == "comparison_only":
            if self.replay_class != "comparison_only":
                raise ValueError("comparison_status_requires_comparison_class")
            if (
                self.reproduced_output_id is not None
                or self.reproduced_output_fingerprint is not None
            ):
                raise ValueError("comparison_only_cannot_carry_reexecution_result")
        elif self.authority_status == "non_authoritative_incomplete":
            if not incomplete:
                raise ValueError("incomplete_status_requires_incomplete_material")
            if mismatches:
                raise ValueError("incomplete_status_cannot_carry_semantic_mismatch")
        elif self.authority_status == "semantic_mismatch":
            if incomplete or not mismatches:
                raise ValueError("semantic_mismatch_status_inconsistent")
            if self.reproduced_output_id is None or self.reproduced_output_fingerprint is None:
                raise ValueError("semantic_mismatch_requires_reproduced_output")
        elif self.authority_status == "authoritative_match":
            if incomplete or mismatches or not exact:
                raise ValueError("authoritative_match_status_inconsistent")
            if self.reproduced_output_id is None or self.reproduced_output_fingerprint is None:
                raise ValueError("authoritative_match_requires_reproduced_output")
        expected = semantic_fingerprint(
            _material(self, exclude={"assessment_id", "semantic_fingerprint"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("replay_assessment_fingerprint_mismatch")
        if self.assessment_id != f"replay-assessment:{expected[:24]}":
            raise ValueError("replay_assessment_id_mismatch")
        return self


class ReviewProjection(BaseModel):
    """Detached read-only explanation projection over one exact replay assessment."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    projection_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    envelope_id: str = Field(min_length=1)
    envelope_fingerprint: str
    assessment_id: str = Field(min_length=1)
    assessment_fingerprint: str
    target_id: str = Field(min_length=1)
    replay_class: ReplayClass
    authority_status: ReplayAuthorityStatus
    verified_material_ids: tuple[str, ...]
    missing_material: tuple[str, ...]
    unverifiable_material: tuple[str, ...]
    contradictions: tuple[str, ...]
    exact_matches: tuple[str, ...]
    mismatches: tuple[str, ...]
    explanation: str = Field(min_length=1)
    live_side_effects_performed: Literal[False] = False
    runtime_authority_promoted: Literal[False] = False
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _law(self) -> "ReviewProjection":
        _hash(self.envelope_fingerprint, "projection_envelope_fingerprint_invalid")
        _hash(self.assessment_fingerprint, "projection_assessment_fingerprint_invalid")
        validated: dict[str, tuple[str, ...]] = {}
        for field_name, values, reason in (
            ("verified", self.verified_material_ids, "projection_verified_material_invalid"),
            ("missing", self.missing_material, "projection_missing_material_invalid"),
            (
                "unverifiable",
                self.unverifiable_material,
                "projection_unverifiable_material_invalid",
            ),
            ("contradictions", self.contradictions, "projection_contradictions_invalid"),
            ("exact", self.exact_matches, "projection_exact_matches_invalid"),
            ("mismatches", self.mismatches, "projection_mismatches_invalid"),
        ):
            validated[field_name] = _unique_nonblank(values, reason)
        incomplete = bool(
            validated["missing"] or validated["unverifiable"] or validated["contradictions"]
        )
        if self.authority_status == "comparison_only":
            if (
                self.replay_class != "comparison_only"
                or validated["exact"]
                or validated["mismatches"]
            ):
                raise ValueError("projection_status_comparison_only_inconsistent")
        elif self.authority_status == "non_authoritative_incomplete":
            if not incomplete or validated["mismatches"]:
                raise ValueError("projection_status_incomplete_inconsistent")
        elif self.authority_status == "semantic_mismatch":
            if incomplete or not validated["mismatches"]:
                raise ValueError("projection_status_mismatch_inconsistent")
        elif self.authority_status == "authoritative_match":
            if incomplete or validated["mismatches"] or not validated["exact"]:
                raise ValueError("projection_status_authoritative_inconsistent")
        expected = semantic_fingerprint(
            _material(self, exclude={"projection_id", "semantic_fingerprint"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("review_projection_fingerprint_mismatch")
        if self.projection_id != f"review-projection:{expected[:24]}":
            raise ValueError("review_projection_id_mismatch")
        return self
