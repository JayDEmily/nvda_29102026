"""Canonical DMPV3 packet-carriage contracts for the live native repo."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from hashlib import sha256
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

K07_REQUIRED_LINEAGE = {
    "reference_packet": frozenset({"derivedfrom", "sourceartifactids", "inputfingerprint"}),
    "prepared_context_packet": frozenset(
        {"derivedfrom", "sourceartifactids", "inputfingerprint"}
    ),
    "stage_packet": frozenset(
        {"parentids", "derivedfrom", "sourceartifactids", "inputfingerprint"}
    ),
    "parallel_risk_packet": frozenset(
        {"parentids", "derivedfrom", "sourceartifactids", "inputfingerprint"}
    ),
    "review_explanation_packet": frozenset(
        {"parentids", "derivedfrom", "inputfingerprint", "reviewtraceid"}
    ),
    "replay_request_packet": frozenset(
        {"replayref", "sourceartifactids", "inputfingerprint", "replaytraceid"}
    ),
    "replay_result_packet": frozenset(
        {
            "parentids",
            "derivedfrom",
            "replayref",
            "sourceartifactids",
            "inputfingerprint",
            "replaytraceid",
        }
    ),
    "replay_comparison_packet": frozenset(
        {
            "parentids",
            "derivedfrom",
            "replayref",
            "sourceartifactids",
            "inputfingerprint",
            "replaytraceid",
        }
    ),
    "diagnostic_packet": frozenset(),
    "rejection_packet": frozenset(),
}

K07_NOT_APPLICABLE_LINEAGE = {
    "reference_packet": frozenset({"decisiontraceid"}),
    "prepared_context_packet": frozenset({"decisiontraceid"}),
    "replay_request_packet": frozenset({"derivedfrom"}),
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

_FORBIDDEN_AUTHORITY_KEYS = frozenset(
    {"capital_authority", "live_order", "domain_state_mutation"}
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


def _find_forbidden_authority_key(value: Any) -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in _FORBIDDEN_AUTHORITY_KEYS:
                return key
            nested = _find_forbidden_authority_key(item)
            if nested is not None:
                return nested
    elif isinstance(value, (list, tuple)):
        for item in value:
            nested = _find_forbidden_authority_key(item)
            if nested is not None:
                return nested
    return None


def _validate_k07_lineage(packetrole: str, lineage: DmpV3Lineage) -> None:
    values = lineage.model_dump()
    for field_name in K07_REQUIRED_LINEAGE[packetrole]:
        if not _has_value(values[field_name]):
            raise ValueError(f"lineage.{field_name} is required for {packetrole}")
    for field_name in K07_NOT_APPLICABLE_LINEAGE.get(packetrole, frozenset()):
        if _has_value(values[field_name]):
            raise ValueError(f"lineage.{field_name} is not applicable to {packetrole}")
    if packetrole in {"diagnostic_packet", "rejection_packet"} and not any(
        _has_value(values[field_name]) for field_name in K07_LINEAGE_FIELDS
    ):
        raise ValueError(
            f"lineage.truthful_target_reference is required for {packetrole}"
        )


def _validate_role_schema_and_authority(
    *, packetrole: str, dataschema: str, data: Any
) -> None:
    if not dataschema.strip():
        raise ValueError("dataschema must identify the typed payload contract")
    if data is None:
        raise ValueError("typed_payload must be present")
    if isinstance(data, dict):
        declared_role = data.get("role")
        if declared_role is not None and declared_role != packetrole:
            raise ValueError("packetrole and typed payload role must agree")
    forbidden_key = _find_forbidden_authority_key(data)
    if forbidden_key is not None:
        raise ValueError(f"authority_boundary forbids payload key {forbidden_key}")


def _k07_validation(
    *, packetrole: str, optional_limitations: list[str]
) -> DmpV3Validation:
    checks = [
        DmpV3ValidationCheck(name=name, passed=True)
        for name in (*K07_COMMON_CHECKS, *K07_ROLE_CHECKS[packetrole])
    ]
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


def build_dmp_v3_envelope_kwargs(
    *,
    packet_id: str,
    dataschema: str,
    data: Any,
    packetrole: str,
    module_id: str,
    module_version: str = "native",
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
    input_material: bytes | None = None,
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
    _require_owned_identifier(module_id, "module_id")
    _require_owned_identifier(module_version, "module_version")
    resolved_module_instance_id = _require_owned_identifier(
        module_instance_id, "module_instance_id"
    )
    _require_owned_identifier(grammar_role, "grammar_role")
    _require_owned_identifier(behaviour_class, "behaviour_class")
    if emitted_at is None:
        raise ValueError("emitted_at must be supplied by the emitting boundary")
    resolved_traceid = _require_owned_identifier(traceid, "traceid")
    resolved_runid = _require_owned_identifier(runid, "runid")
    resolved_scenarioid = _require_owned_identifier(scenarioid, "scenarioid")
    if packetrole not in K07_ADMITTED_PACKET_ROLES:
        raise ValueError(f"packetrole is not admitted by K07: {packetrole}")
    _validate_role_schema_and_authority(
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
    _validate_k07_lineage(packetrole, lineage)
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
        if input_material is None:
            raise ValueError(
                "inputfingerprint requires owner-supplied input material"
            )
        if sha256(input_material).hexdigest() != lineage.inputfingerprint:
            raise ValueError("inputfingerprint does not match owner-supplied material")

    validation = _k07_validation(
        packetrole=packetrole,
        optional_limitations=limitations,
    )

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

    keyflags = list(summary_keyflags or [])
    if validation.status == "degraded":
        for violation in limitations:
            if violation not in keyflags:
                keyflags.append(violation)

    summary = DmpV3Summary(
        headline=summary_headline or f"{module_id} emitted {packetrole}",
        keyflags=keyflags,
        humanstate=summary_humanstate or validation.status,
    )

    return {
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
        "producer": DmpV3Producer(
            module_id=module_id,
            module_version=module_version,
            module_instance_id=resolved_module_instance_id,
            grammar_role=grammar_role,
            behaviour_class=behaviour_class,
            stage_name=stage_name,
        ),
        "lineage": lineage,
        "validation": validation,
        "summary": summary,
        "data": data,
        "dmpextensions": extensions_payload,
    }
