"""Test-only contract instruments for the M04 K07 packet-role proof family."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any, Callable, Final

ROLES: Final = (
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
)

LINEAGE_FIELDS: Final = (
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

COMMON_CHECKS: Final = (
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

ROLE_CHECKS: Final = {
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

# Explicit transcription of section 9.10.3. Conditional cells are activated by
# ``activated_lineage`` in a case; otherwise they must remain empty.
LINEAGE_MATRIX: Final = {
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

FIXED_TIME: Final = datetime(2026, 7, 30, 9, 30, tzinfo=UTC)


class EmissionRejected(ValueError):
    """Exact stand-down result for a proposed binding packet emission."""

    def __init__(self, fact: str) -> None:
        super().__init__(f"stand_down:{fact}")
        self.fact = fact


@dataclass
class OwnerPorts:
    """Owner-provided validators and evidence ports with observable calls."""

    artefacts: set[str]
    calls: list[str] = field(default_factory=list)

    def artefact_retrievable(self, artefact_id: str) -> bool:
        self.calls.append(f"artefact:{artefact_id}")
        return artefact_id in self.artefacts

    def fingerprint_valid(self, material: bytes, fingerprint: str) -> bool:
        self.calls.append("fingerprint")
        return sha256(material).hexdigest() == fingerprint

    def typed_payload_valid(self, payload: dict[str, Any]) -> bool:
        self.calls.append("typed_payload")
        return payload.get("contract_version") == "v1"

    def authority_boundary_valid(self, payload: dict[str, Any]) -> bool:
        self.calls.append("authority_boundary")
        return not any(
            key in payload
            for key in ("capital_authority", "live_order", "domain_state_mutation")
        )


@dataclass(frozen=True)
class K07Case:
    role: str
    packet_id: str
    emitted_at: datetime
    traceid: str
    runid: str
    scenarioid: str
    module_id: str
    module_version: str
    module_instance_id: str
    grammar_role: str
    behaviour_class: str
    stage_name: str | None
    dataschema: str
    payload: dict[str, Any]
    material: bytes
    lineage: dict[str, Any]
    activated_lineage: frozenset[str]
    ports: OwnerPorts
    optional_limitation: str | None = None
    authoritative_evidence_available: bool = True
    preserved_original_id: str | None = None
    preserved_original_time: datetime | None = None


@dataclass(frozen=True)
class ValidationResult:
    name: str
    passed: bool
    evidence: str


@dataclass(frozen=True)
class K07Packet:
    role: str
    packet_id: str
    emitted_at: datetime
    source: str
    context: tuple[str, str, str]
    producer: tuple[str, str, str, str, str, str | None]
    dataschema: str
    payload: dict[str, Any]
    lineage: dict[str, Any]
    validation_status: str
    validation_results: tuple[ValidationResult, ...]
    outcome: str
    summary_flags: tuple[str, ...]
    extensions: dict[str, Any]
    side_effects: tuple[str, ...] = ()


def _has_value(value: Any) -> bool:
    if isinstance(value, (list, tuple, dict, str)):
        return bool(value)
    return value is not None


def _syntactically_valid_identity(value: str) -> bool:
    return bool(value) and value.strip() == value and " " not in value and value != "live"


def _required_lineage(case: K07Case, *, allow_not_applicable: bool = False) -> None:
    states = dict(zip(LINEAGE_FIELDS, LINEAGE_MATRIX[case.role], strict=True))
    for name, state in states.items():
        present = _has_value(case.lineage.get(name))
        if state == "R" and not present:
            raise EmissionRejected(f"lineage.{name}")
        if state == "C" and ((name in case.activated_lineage) != present):
            raise EmissionRejected(f"lineage.{name}")
        if state == "N" and present and not allow_not_applicable:
            raise EmissionRejected(f"lineage.{name}:not_applicable")
    if case.role in {"diagnostic_packet", "rejection_packet"} and not any(
        _has_value(case.lineage.get(name)) for name in LINEAGE_FIELDS
    ):
        raise EmissionRejected("lineage.truthful_target_reference")


def _checks(case: K07Case, *, hardcoded: bool = False) -> tuple[ValidationResult, ...]:
    if hardcoded:
        return tuple(
            ValidationResult(name, True, "hardcoded")
            for name in (*COMMON_CHECKS, *ROLE_CHECKS[case.role])
        )
    if not case.ports.typed_payload_valid(case.payload):
        raise EmissionRejected("typed_payload")
    if not case.ports.authority_boundary_valid(case.payload):
        raise EmissionRejected("authority_boundary")
    for artefact_id in case.lineage.get("sourceartifactids", []):
        if not case.ports.artefact_retrievable(artefact_id):
            raise EmissionRejected(f"sourceartifactids:{artefact_id}")
    fingerprint = case.lineage.get("inputfingerprint")
    if fingerprint and not case.ports.fingerprint_valid(case.material, fingerprint):
        raise EmissionRejected("inputfingerprint")
    return tuple(
        ValidationResult(name, True, f"owner_fact:{name}")
        for name in (*COMMON_CHECKS, *ROLE_CHECKS[case.role])
    )


class ReferenceSubject:
    """A conforming test-only subject used to verify proof-family sensitivity."""

    mutant: str | None = None

    def __init__(self, mutant: str | None = None) -> None:
        self.mutant = mutant

    def emit(self, case: K07Case) -> K07Packet:
        if case.role not in ROLES:
            raise EmissionRejected("packetrole")
        for name in ("traceid", "runid", "scenarioid"):
            value = getattr(case, name)
            if not _syntactically_valid_identity(value):
                if self.mutant == "MUT-CONTEXT-DEFAULT":
                    case = replace(case, **{name: f"default::{case.packet_id}"})
                elif self.mutant == "MUT-WRONG-REASON":
                    raise EmissionRejected("generic_invalid_packet")
                else:
                    raise EmissionRejected(name)

        if self.mutant != "MUT-DROP-LINEAGE":
            _required_lineage(
                case,
                allow_not_applicable=self.mutant == "MUT-N-FIELD",
            )

        results = _checks(case, hardcoded=self.mutant == "MUT-HARDCODE-CHECKS")
        status = "degraded" if case.optional_limitation else "valid"
        if self.mutant == "MUT-DEGRADED-BYPASS" and not case.authoritative_evidence_available:
            status = "degraded"

        outcome = "authoritative"
        if case.role == "replay_result_packet" and not case.authoritative_evidence_available:
            outcome = (
                "authoritative"
                if self.mutant == "MUT-REPLAY-OVERCLAIM"
                else "non_authoritative_incomplete"
            )

        packet_id = case.packet_id
        emitted_at = case.emitted_at
        if self.mutant == "MUT-REPLAY-IDENTITY-REUSE" and case.preserved_original_id:
            packet_id = case.preserved_original_id
            emitted_at = case.preserved_original_time or case.emitted_at

        role = case.role
        if self.mutant == "MUT-DIAGNOSTIC-SUBSTITUTE" and role in {
            "diagnostic_packet",
            "rejection_packet",
        }:
            role = "stage_packet"

        lineage = dict(case.lineage)
        if self.mutant == "MUT-DROP-LINEAGE":
            lineage["sourceartifactids"] = []
        if self.mutant == "MUT-ARTIFACT-HASH-SUBSTITUTE":
            case.ports.calls[:] = [
                call for call in case.ports.calls if not call.startswith("artefact:")
            ]

        return K07Packet(
            role=role,
            packet_id=packet_id,
            emitted_at=emitted_at,
            source=f"urn:nvda:producer:{case.module_id}",
            context=(case.traceid, case.runid, case.scenarioid),
            producer=(
                case.module_id,
                case.module_version,
                case.module_instance_id,
                case.grammar_role,
                case.behaviour_class,
                case.stage_name,
            ),
            dataschema=case.dataschema,
            payload=dict(case.payload),
            lineage=lineage,
            validation_status=status,
            validation_results=results,
            outcome=outcome,
            summary_flags=(case.optional_limitation,) if case.optional_limitation else (),
            extensions={"nvda": {"contract": "m04.k07.v1"}},
        )


class ProductionSubject:
    """Adapter over the current repo-owned public packet builder."""

    def emit(self, case: K07Case) -> Any:
        # Load the canonical contract package before the builder. This mirrors
        # the public import order used by the existing packet family and avoids
        # treating a package-initialisation cycle as K07 behavioural evidence.
        from nvda_desk.contracts import packets as canonical_packets
        from nvda_desk.packets.dmp_packets import build_dmp_v3_packet

        assert canonical_packets.DeskModulePacketV3 is not None
        return build_dmp_v3_packet(
            packet_id=case.packet_id,
            emitted_at=case.emitted_at,
            traceid=case.traceid,
            runid=case.runid,
            scenarioid=case.scenarioid,
            dataschema=case.dataschema,
            data=case.payload,
            packetrole=case.role,
            module_id=case.module_id,
            module_version=case.module_version,
            module_instance_id=case.module_instance_id,
            grammar_role=case.grammar_role,
            behaviour_class=case.behaviour_class,
            stage_name=case.stage_name,
            source_artifact_validator=case.ports.artefact_retrievable,
            input_material=case.material,
            **case.lineage,
        )


def positive_case(role: str, *, activate_conditionals: bool = False) -> K07Case:
    material = f"material::{role}".encode()
    states = dict(zip(LINEAGE_FIELDS, LINEAGE_MATRIX[role], strict=True))
    activated = frozenset(name for name, state in states.items() if state == "C")
    if not activate_conditionals:
        activated = frozenset()
    lineage: dict[str, Any] = {}
    for name, state in states.items():
        if state == "R" or name in activated:
            if name in {"parentids", "dependencyids", "sourceartifactids"}:
                lineage[name] = [f"{name}::{role}"]
            elif name == "inputfingerprint":
                lineage[name] = sha256(material).hexdigest()
            else:
                lineage[name] = f"{name}::{role}"
        else:
            lineage[name] = [] if name in {"parentids", "dependencyids", "sourceartifactids"} else None
    if role in {"diagnostic_packet", "rejection_packet"} and not activate_conditionals:
        activated = frozenset({"dependencyids"})
        lineage["dependencyids"] = [f"rejected-input::{role}"]
    artefacts = set(lineage.get("sourceartifactids", []))
    return K07Case(
        role=role,
        packet_id=f"occurrence::{role}",
        emitted_at=FIXED_TIME,
        traceid=f"trace::{role}",
        runid=f"run::{role}",
        scenarioid=f"scenario::{role}",
        module_id=f"owner_{role}",
        module_version="v1",
        module_instance_id=f"owner_{role}::instance",
        grammar_role=f"grammar_{role}",
        behaviour_class="module_output",
        stage_name="stage" if role == "stage_packet" else None,
        dataschema=f"nvda.m04.{role}.v1",
        payload={"contract_version": "v1", "role": role},
        material=material,
        lineage=lineage,
        activated_lineage=activated,
        ports=OwnerPorts(artefacts=artefacts),
        preserved_original_id=f"original::{role}" if role.startswith("replay_") else None,
        preserved_original_time=(
            datetime(2026, 7, 29, 9, 30, tzinfo=UTC) if role.startswith("replay_") else None
        ),
    )


def with_lineage(case: K07Case, field_name: str, value: Any) -> K07Case:
    lineage = dict(case.lineage)
    lineage[field_name] = value
    return replace(case, lineage=lineage)


def assert_complete_packet(case: K07Case, packet: K07Packet) -> None:
    assert packet.role == case.role
    assert packet.packet_id == case.packet_id
    assert packet.emitted_at == case.emitted_at
    assert packet.context == (case.traceid, case.runid, case.scenarioid)
    assert packet.packet_id not in packet.context
    assert packet.producer[:5] == (
        case.module_id,
        case.module_version,
        case.module_instance_id,
        case.grammar_role,
        case.behaviour_class,
    )
    assert packet.dataschema == case.dataschema
    assert packet.payload == case.payload
    assert packet.lineage == case.lineage
    assert packet.validation_status == ("degraded" if case.optional_limitation else "valid")
    names = tuple(result.name for result in packet.validation_results)
    assert names == (*COMMON_CHECKS, *ROLE_CHECKS[case.role])
    assert all(result.passed and result.evidence.startswith("owner_fact:") for result in packet.validation_results)
    assert packet.side_effects == ()
    assert packet.extensions["nvda"]["contract"] == "m04.k07.v1"


MUTANTS: Final = (
    "MUT-CONTEXT-DEFAULT",
    "MUT-DROP-LINEAGE",
    "MUT-N-FIELD",
    "MUT-HARDCODE-CHECKS",
    "MUT-WRONG-REASON",
    "MUT-DEGRADED-BYPASS",
    "MUT-DIAGNOSTIC-SUBSTITUTE",
    "MUT-ARTIFACT-HASH-SUBSTITUTE",
    "MUT-REPLAY-OVERCLAIM",
    "MUT-REPLAY-IDENTITY-REUSE",
)


ContractAssertion = Callable[[ReferenceSubject], None]
