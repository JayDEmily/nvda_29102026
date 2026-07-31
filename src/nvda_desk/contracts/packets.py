"""Canonical DMPV3 packet-carriage contracts for the live native repo."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Callable, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")

K07_ADMITTED_PACKET_ROLES = frozenset(
    {
        "reference_packet",
        "prepared_context_packet",
        "stage_packet",
        "parallel_risk_packet",
        "review_explanation_packet",
        "replay_request_packet",
        "replay_result_packet",
        "replay_comparison_packet",
        "diagnostic_packet",
        "rejection_packet",
    }
)

K07_LINEAGE_FIELDS = (
    "parentids",
    "dependencyids",
    "derivedfrom",
    "replayref",
    "sourceartifactids",
    "inputfingerprint",
    "reviewtraceid",
    "replaytraceid",
    "decisiontraceid",
)

K07_LINEAGE_MATRIX = {
    "reference_packet": ("C", "C", "R", "C", "R", "R", "C", "C", "N"),
    "prepared_context_packet": ("C", "C", "R", "C", "R", "R", "C", "C", "N"),
    "stage_packet": ("R", "C", "R", "C", "R", "R", "C", "C", "C"),
    "parallel_risk_packet": ("R", "C", "R", "C", "R", "R", "C", "C", "C"),
    "review_explanation_packet": ("R", "C", "R", "C", "C", "R", "R", "C", "C"),
    "replay_request_packet": ("C", "C", "N", "R", "R", "R", "C", "R", "C"),
    "replay_result_packet": ("R", "C", "R", "R", "R", "R", "C", "R", "C"),
    "replay_comparison_packet": ("R", "C", "R", "R", "R", "R", "C", "R", "C"),
    "diagnostic_packet": ("C", "C", "C", "C", "C", "C", "C", "C", "C"),
    "rejection_packet": ("C", "C", "C", "C", "C", "C", "C", "C", "C"),
}

K07_COMMON_CHECKS = (
    "canonical_envelope",
    "producer_identity",
    "role_schema_consistency",
    "execution_context_ownership",
    "typed_payload",
    "lineage_profile",
    "authority_boundary",
    "extension_bounds",
    "summary_consistency",
    "validation_completeness",
)

K07_ROLE_CHECKS = {
    "reference_packet": (
        "reference_identity_and_version",
        "source_artifact_retrievability",
        "source_temporal_precision",
        "reference_material_fingerprint",
        "no_runtime_decision_authority",
    ),
    "prepared_context_packet": (
        "prepared_identity_and_contract_version",
        "source_and_capture_lineage",
        "source_temporal_preservation",
        "prepared_fingerprint",
        "completeness_and_limitation_state",
        "no_domain_decision_authority",
    ),
    "stage_packet": (
        "stage_identity_and_order",
        "prepared_or_prior_stage_parentage",
        "material_dependency_closure",
        "stage_input_fingerprint",
        "domain_output_identity",
        "serial_parallel_capital_boundary",
    ),
    "parallel_risk_packet": (
        "parallel_lane_identity",
        "lawful_input_boundary",
        "material_dependency_closure",
        "risk_input_fingerprint",
        "risk_output_identity",
        "serial_candidate_and_capital_separation",
    ),
    "review_explanation_packet": (
        "review_trace_identity",
        "reviewed_evidence_closure",
        "review_input_fingerprint",
        "deterministic_explanation",
        "contradiction_visibility",
        "no_runtime_decision_authority",
    ),
    "replay_request_packet": (
        "replay_trace_identity",
        "replay_target_retrievability",
        "requested_evidence_and_version_completeness",
        "requested_input_fingerprint",
        "no_live_side_effect_request",
    ),
    "replay_result_packet": (
        "replay_trace_identity",
        "original_occurrence_separation",
        "consumed_evidence_and_version_verification",
        "isolated_state_and_controlled_time",
        "semantic_result_fingerprint",
        "no_live_side_effects",
        "authoritative_or_incomplete_status",
    ),
    "replay_comparison_packet": (
        "replay_trace_identity",
        "original_and_result_identity",
        "comparison_evidence_closure",
        "comparison_fingerprint",
        "mismatch_visibility",
        "no_reconstruction_overclaim",
    ),
    "diagnostic_packet": (
        "diagnostic_contract_and_version",
        "target_or_rejected_input_identity",
        "failure_fact_completeness",
        "non_binding_status",
        "no_binding_role_substitution",
        "no_authority_promotion",
    ),
    "rejection_packet": (
        "diagnostic_contract_and_version",
        "target_or_rejected_input_identity",
        "failure_fact_completeness",
        "non_binding_status",
        "no_binding_role_substitution",
        "no_authority_promotion",
    ),
}

K07_DIAGNOSTIC_TARGET_FIELDS = (
    "parentids",
    "dependencyids",
    "derivedfrom",
    "replayref",
    "sourceartifactids",
    "reviewtraceid",
    "replaytraceid",
    "decisiontraceid",
)

class DmpV3Producer(BaseModel):
    """Bounded producer identity carried by one DMPV3 packet."""

    model_config = ConfigDict(extra="forbid")

    module_id: str = Field(min_length=1)
    module_version: str = Field(min_length=1)
    module_instance_id: str = Field(min_length=1)
    grammar_role: str = Field(min_length=1)
    behaviour_class: str = Field(min_length=1)
    stage_name: str | None = None


class DmpV3Lineage(BaseModel):
    """Bounded lineage surface for one DMPV3 packet."""

    model_config = ConfigDict(extra="forbid")

    parentids: list[str] = Field(default_factory=list)
    dependencyids: list[str] = Field(default_factory=list)
    derivedfrom: str | None = None
    replayref: str | None = None
    sourceartifactids: list[str] = Field(default_factory=list)
    inputfingerprint: str | None = None
    reviewtraceid: str | None = None
    replaytraceid: str | None = None
    decisiontraceid: str | None = None


class DmpV3ValidationCheck(BaseModel):
    """One named validation check outcome."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    passed: bool


class DmpV3Validation(BaseModel):
    """Validation carriage for one DMPV3 packet."""

    model_config = ConfigDict(extra="forbid")

    status: str = Field(default="valid", min_length=1)
    checks: list[DmpV3ValidationCheck] = Field(
        default_factory=lambda: [DmpV3ValidationCheck(name="schema_validation", passed=True)]
    )
    violations: list[str] = Field(default_factory=list)


class DmpV3Summary(BaseModel):
    """Human-facing summary block carried by one DMPV3 packet."""

    model_config = ConfigDict(extra="forbid")

    headline: str = Field(min_length=1)
    keyflags: list[str] = Field(default_factory=list)
    humanstate: str = Field(min_length=1)


def _deep_merge_dicts(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge bounded extension dictionaries without erasing canonical leaves."""

    merged = deepcopy(base)
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge_dicts(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def _has_value(value: Any) -> bool:
    if isinstance(value, (list, tuple, dict, str)):
        return bool(value)
    return value is not None


def _require_owned_identifier(value: str | None, field_name: str) -> str:
    if (
        value is None
        or not value
        or value.strip() != value
        or any(character.isspace() for character in value)
        or value == "live"
    ):
        raise ValueError(f"{field_name} must be a caller-owned governed identity")
    return value


def _validate_k07_lineage(
    packetrole: str,
    lineage: DmpV3Lineage,
    conditional_lineage_fields: set[str],
) -> None:
    values = lineage.model_dump()
    matrix = dict(zip(K07_LINEAGE_FIELDS, K07_LINEAGE_MATRIX[packetrole], strict=True))
    unknown_conditions = conditional_lineage_fields.difference(K07_LINEAGE_FIELDS)
    if unknown_conditions:
        raise ValueError(
            "conditional_lineage_fields contains unknown fields: "
            + ", ".join(sorted(unknown_conditions))
        )
    invalid_conditions = {
        field_name
        for field_name in conditional_lineage_fields
        if matrix[field_name] != "C"
    }
    if invalid_conditions:
        raise ValueError(
            "conditional_lineage_fields may activate only C fields: "
            + ", ".join(sorted(invalid_conditions))
        )

    for field_name, state in matrix.items():
        present = _has_value(values[field_name])
        if state == "R" and not present:
            raise ValueError(f"lineage.{field_name} is required for {packetrole}")
        if state == "C" and ((field_name in conditional_lineage_fields) != present):
            requirement = (
                "required" if field_name in conditional_lineage_fields else "not applicable"
            )
            raise ValueError(f"lineage.{field_name} is {requirement} for {packetrole}")
        if state == "N" and present:
            raise ValueError(f"lineage.{field_name} is not applicable to {packetrole}")
    if packetrole in {"diagnostic_packet", "rejection_packet"} and not any(
        _has_value(values[field_name]) for field_name in K07_DIAGNOSTIC_TARGET_FIELDS
    ):
        raise ValueError(
            f"lineage.truthful_target_reference is required for {packetrole}"
        )


def _validate_role_schema(*, packetrole: str, dataschema: str, data: Any) -> None:
    if not dataschema.strip():
        raise ValueError("dataschema must identify the typed payload contract")
    if data is None:
        raise ValueError("typed_payload must be present")
    if isinstance(data, dict):
        declared_role = data.get("role")
        if declared_role is not None and declared_role != packetrole:
            raise ValueError("packetrole and typed payload role must agree")


def _k07_validation(
    *,
    packetrole: str,
    canonical_envelope_valid: bool,
    owner_check_validator: Callable[[str, dict[str, Any]], bool] | None,
    owner_check_context: dict[str, Any],
    optional_limitations: list[str],
) -> DmpV3Validation:
    expected_names = (*K07_COMMON_CHECKS, *K07_ROLE_CHECKS[packetrole])
    completed: dict[str, DmpV3ValidationCheck] = {}
    for name in expected_names:
        if name == "validation_completeness":
            continue
        if name == "canonical_envelope":
            passed = canonical_envelope_valid
        else:
            if owner_check_validator is None:
                raise ValueError(
                    f"validation.{name} requires an owner-supplied check validator"
                )
            passed = bool(owner_check_validator(name, owner_check_context))
        if not passed:
            raise ValueError(f"validation.{name} failed")
        completed[name] = DmpV3ValidationCheck(name=name, passed=True)

    executed_names = set(expected_names).difference({"validation_completeness"})
    completeness_passed = set(completed) == executed_names
    if not completeness_passed:
        raise ValueError("validation.validation_completeness failed")
    completed["validation_completeness"] = DmpV3ValidationCheck(
        name="validation_completeness",
        passed=True,
    )
    checks = [completed[name] for name in expected_names]
    checks.extend(
        DmpV3ValidationCheck(name=f"optional_quality:{limitation}", passed=False)
        for limitation in optional_limitations
    )
    return DmpV3Validation(
        status="degraded" if optional_limitations else "valid",
        checks=checks,
        violations=list(optional_limitations),
    )


class DmpV3Envelope(BaseModel, Generic[T]):
    """Canonical DMPV3 outer envelope for live inter-module packet carriage."""

    model_config = ConfigDict(extra="forbid")

    specversion: str = "1.0"
    dmpversion: str = "3.0.0"
    id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    type: str = Field(min_length=1)
    time: datetime
    datacontenttype: str = "application/json"
    dataschema: str = Field(min_length=1)
    traceid: str = Field(min_length=1)
    runid: str = Field(min_length=1)
    scenarioid: str = Field(min_length=1)
    packetrole: str = Field(min_length=1)
    producer: DmpV3Producer
    lineage: DmpV3Lineage = Field(default_factory=DmpV3Lineage)
    validation: DmpV3Validation = Field(default_factory=DmpV3Validation)
    summary: DmpV3Summary
    data: T
    dmpextensions: dict[str, Any] = Field(default_factory=dict)

    @property
    def packet_id(self) -> str:
        return self.id

    @property
    def emitted_at(self) -> datetime:
        return self.time


class DmpV3Packet(DmpV3Envelope[T], Generic[T]):
    """Repo-facing typed helper surface layered on the canonical DMPV3 envelope."""


class DeskModulePacketV3(DmpV3Packet[Any]):
    """Typed repo helper for bounded live module payload carriage."""


def _canonical_envelope_is_valid(envelope_without_validation: dict[str, Any]) -> bool:
    expected_fields = set(DmpV3Envelope.model_fields).difference({"validation"})
    emitted_at = envelope_without_validation.get("time")
    return (
        set(envelope_without_validation) == expected_fields
        and envelope_without_validation.get("specversion") == "1.0"
        and envelope_without_validation.get("dmpversion") == "3.0.0"
        and _has_value(envelope_without_validation.get("id"))
        and isinstance(emitted_at, datetime)
        and emitted_at.tzinfo is not None
        and emitted_at.utcoffset() is not None
    )


def build_dmp_v3_envelope_kwargs(
    *,
    packet_id: str,
    dataschema: str,
    data: Any,
    packetrole: str,
    module_id: str,
    module_version: str | None = None,
    module_instance_id: str | None = None,
    grammar_role: str,
    behaviour_class: str,
    stage_name: str | None = None,
    emitted_at: datetime | None = None,
    source: str | None = None,
    packet_type: str | None = None,
    datacontenttype: str = "application/json",
    traceid: str | None = None,
    runid: str | None = None,
    scenarioid: str | None = None,
    parentids: list[str] | None = None,
    dependencyids: list[str] | None = None,
    derivedfrom: str | None = None,
    replayref: str | None = None,
    sourceartifactids: list[str] | None = None,
    inputfingerprint: str | None = None,
    source_artifact_validator: Callable[[str], bool] | None = None,
    input_fingerprint_validator: Callable[[str], bool] | None = None,
    conditional_lineage_fields: set[str] | None = None,
    owner_check_validator: Callable[[str, dict[str, Any]], bool] | None = None,
    optional_limitation_validator: Callable[[str], bool] | None = None,
    degraded_consumer_restriction: str | None = None,
    reviewtraceid: str | None = None,
    replaytraceid: str | None = None,
    decisiontraceid: str | None = None,
    validation_violations: list[str] | None = None,
    summary_headline: str | None = None,
    summary_keyflags: list[str] | None = None,
    summary_humanstate: str | None = None,
    dmpextensions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return canonical DMPV3 envelope kwargs for one repo-owned payload."""

    _require_owned_identifier(packet_id, "packet_id")
    if packetrole not in K07_ADMITTED_PACKET_ROLES:
        raise ValueError(f"packetrole is not admitted by K07: {packetrole}")
    resolved_traceid = _require_owned_identifier(traceid, "traceid")
    resolved_runid = _require_owned_identifier(runid, "runid")
    resolved_scenarioid = _require_owned_identifier(scenarioid, "scenarioid")
    _require_owned_identifier(module_id, "module_id")
    resolved_module_version = _require_owned_identifier(module_version, "module_version")
    resolved_module_instance_id = _require_owned_identifier(
        module_instance_id, "module_instance_id"
    )
    _require_owned_identifier(grammar_role, "grammar_role")
    _require_owned_identifier(behaviour_class, "behaviour_class")
    if emitted_at is None:
        raise ValueError("emitted_at must be supplied by the emitting boundary")
    _validate_role_schema(
        packetrole=packetrole,
        dataschema=dataschema,
        data=data,
    )

    limitations = list(validation_violations or [])
    resolved_source = source or f"urn:nvda:producer:{module_id}"
    resolved_type = packet_type or f"urn:nvda:packet:{packetrole}"

    lineage = DmpV3Lineage(
        parentids=list(parentids or []),
        dependencyids=list(dependencyids or []),
        derivedfrom=derivedfrom,
        replayref=replayref,
        sourceartifactids=list(sourceartifactids or []),
        inputfingerprint=inputfingerprint,
        reviewtraceid=reviewtraceid,
        replaytraceid=replaytraceid,
        decisiontraceid=decisiontraceid,
    )
    active_conditionals = set(conditional_lineage_fields or set())
    _validate_k07_lineage(packetrole, lineage, active_conditionals)
    if packetrole in {"diagnostic_packet", "rejection_packet"}:
        target_values: list[str] = []
        for field_name in K07_DIAGNOSTIC_TARGET_FIELDS:
            value = getattr(lineage, field_name)
            if isinstance(value, list):
                target_values.extend(value)
            elif isinstance(value, str):
                target_values.append(value)
        if packet_id in target_values:
            raise ValueError(
                "diagnostic/rejection occurrence identity must differ from its target"
            )
    if packetrole.startswith("replay_") and lineage.replayref == packet_id:
        raise ValueError("replay occurrence identity must differ from replayref")
    if lineage.sourceartifactids:
        if source_artifact_validator is None:
            raise ValueError(
                "sourceartifactids require an owner-supplied retrievability validator"
            )
        unresolved_artifacts = [
            artefact_id
            for artefact_id in lineage.sourceartifactids
            if not source_artifact_validator(artefact_id)
        ]
        if unresolved_artifacts:
            raise ValueError(
                "sourceartifactids are not retrievable: "
                + ", ".join(unresolved_artifacts)
            )
    if lineage.inputfingerprint is not None:
        if input_fingerprint_validator is None:
            raise ValueError(
                "inputfingerprint requires an owner-supplied fingerprint validator"
            )
        if not input_fingerprint_validator(lineage.inputfingerprint):
            raise ValueError("inputfingerprint failed owner validation")

    if emitted_at.tzinfo is None or emitted_at.utcoffset() is None:
        raise ValueError("emitted_at must be timezone-aware")

    if limitations:
        if optional_limitation_validator is None:
            raise ValueError(
                "degraded carriage requires an owner-supplied optional limitation validator"
            )
        if not degraded_consumer_restriction or not degraded_consumer_restriction.strip():
            raise ValueError(
                "degraded carriage requires an explicit consumer restriction"
            )
        for limitation in limitations:
            if not optional_limitation_validator(limitation):
                raise ValueError(f"optional limitation is not admitted: {limitation}")

    payload_type = data.__class__
    canonical_schema_identifiers = {
        "payload_model_name": payload_type.__name__,
        "payload_module_path": payload_type.__module__,
        "output_model_name": payload_type.__name__,
    }
    extensions_payload: dict[str, Any] = {
        "nvda": {
            "schema_identifiers": canonical_schema_identifiers,
            "semantic_dependencies": list(lineage.dependencyids),
        }
    }
    if dmpextensions:
        extensions_payload = _deep_merge_dicts(extensions_payload, dict(dmpextensions))
        canonical_nvda_extensions = extensions_payload.setdefault("nvda", {})
        canonical_nvda_extensions["schema_identifiers"] = canonical_schema_identifiers
        canonical_nvda_extensions["semantic_dependencies"] = list(lineage.dependencyids)

    validation_status = "degraded" if limitations else "valid"
    keyflags = list(summary_keyflags or [])
    if validation_status == "degraded":
        for violation in limitations:
            if violation not in keyflags:
                keyflags.append(violation)
        restriction_flag = f"consumer_restriction:{degraded_consumer_restriction}"
        if restriction_flag not in keyflags:
            keyflags.append(restriction_flag)

    producer = DmpV3Producer(
        module_id=module_id,
        module_version=resolved_module_version,
        module_instance_id=resolved_module_instance_id,
        grammar_role=grammar_role,
        behaviour_class=behaviour_class,
        stage_name=stage_name,
    )
    summary = DmpV3Summary(
        headline=summary_headline or f"{module_id} emitted {packetrole}",
        keyflags=keyflags,
        humanstate=summary_humanstate or validation_status,
    )
    envelope_without_validation = {
        "specversion": "1.0",
        "dmpversion": "3.0.0",
        "id": packet_id,
        "source": resolved_source,
        "type": resolved_type,
        "time": emitted_at,
        "datacontenttype": datacontenttype,
        "dataschema": dataschema,
        "traceid": resolved_traceid,
        "runid": resolved_runid,
        "scenarioid": resolved_scenarioid,
        "packetrole": packetrole,
        "producer": producer,
        "lineage": lineage,
        "summary": summary,
        "data": data,
        "dmpextensions": extensions_payload,
    }
    owner_check_context = {
        "packet_id": packet_id,
        "emitted_at": emitted_at,
        "source": resolved_source,
        "packet_type": resolved_type,
        "datacontenttype": datacontenttype,
        "packetrole": packetrole,
        "dataschema": dataschema,
        "data": data,
        "producer": producer,
        "execution_context": {
            "traceid": resolved_traceid,
            "runid": resolved_runid,
            "scenarioid": resolved_scenarioid,
        },
        "lineage": lineage,
        "dmpextensions": extensions_payload,
        "summary": summary,
        "optional_limitations": tuple(limitations),
        "degraded_consumer_restriction": degraded_consumer_restriction,
    }
    validation = _k07_validation(
        packetrole=packetrole,
        canonical_envelope_valid=_canonical_envelope_is_valid(
            envelope_without_validation
        ),
        owner_check_validator=owner_check_validator,
        owner_check_context=owner_check_context,
        optional_limitations=limitations,
    )
    return {
        **envelope_without_validation,
        "validation": validation,
    }
