"""M05-owned immutable contracts for bounded serial cognition."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from hashlib import sha256
from math import isfinite
from typing import Any, Final, Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

StageName = Literal[
    "temporal",
    "regime",
    "options_flow",
    "posture",
    "eligibility",
    "execution",
]
StageStatus = Literal["complete", "stand_down", "withheld", "rejected"]
SerialStatus = Literal["formed", "stand_down", "withheld", "rejected"]
AuthorityRef = tuple[str, str, str, str]
Pair = tuple[str, str]
CarrierValue = str | int | float | bool | datetime | tuple[str, ...] | None

SERIAL_STAGE_ORDER: Final[tuple[str, ...]] = (
    "temporal",
    "regime",
    "options_flow",
    "posture",
    "eligibility",
    "execution",
)
SERIAL_STAGE_DEPENDENCIES: Final[dict[str, tuple[str, ...]]] = {
    "temporal": (),
    "regime": (),
    "options_flow": (),
    "posture": ("regime",),
    "eligibility": ("posture",),
    "execution": (
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
    ),
}
STAGE_OWNER_IDS: Final[dict[str, str]] = {
    "temporal": "temporal_context",
    "regime": "market_regime_context",
    "options_flow": "options_flow",
    "posture": "posture_permission",
    "eligibility": "playbook_eligibility",
    "execution": "candidate_expression",
}
CLOSED_AUTHORITY_CLASSES: Final[tuple[str, ...]] = (
    "prepared_truth",
    "packet_identity",
    "coefficient_modifier",
    "playbook_eligibility",
    "parallel_risk",
    "capital",
    "broker_order",
    "position_inventory",
    "lifecycle",
    "transaction",
    "replay",
)
ALLOWED_STAGE_AUTHORITY_OWNERS: Final[dict[str, frozenset[str]]] = {
    "temporal": frozenset({"m03"}),
    "regime": frozenset({"m03"}),
    "options_flow": frozenset({"m03"}),
    "posture": frozenset({"m07"}),
    "eligibility": frozenset({"m08"}),
    "execution": frozenset({"m08"}),
}
ALLOWED_STAGE_FACT_IDS: Final[dict[str, frozenset[str]]] = {
    "temporal": frozenset(
        {"effective_at_utc", "session_state", "next_event_time_utc"}
    ),
    "regime": frozenset({"nvda_return_pct", "nq_return_pct", "vix_level"}),
    "options_flow": frozenset({"spot_price", "front_dte", "next_dte"}),
    "posture": frozenset({"modifier_decision_status", "posture_policy_ref"}),
    "eligibility": frozenset(
        {"eligibility_status", "eligibility_lead_id", "ordered_eligible_candidate_ids"}
    ),
    "execution": frozenset({"eligibility_lead_id", "expression_policy_ref"}),
}


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def semantic_fingerprint(value: Any) -> str:
    """Return the deterministic SHA-256 fingerprint for semantic material."""

    payload = json.dumps(
        _canonical(value),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(payload).hexdigest()


def _require_text(value: str, reason: str) -> str:
    if not value:
        raise ValueError(reason)
    return value


def _require_hash(value: str, reason: str) -> str:
    if len(value) != 64:
        raise ValueError(reason)
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(reason) from exc
    return value


def _unique_pairs(items: tuple[Pair, ...], reason: str) -> tuple[Pair, ...]:
    keys = tuple(key for key, _ in items)
    if len(keys) != len(set(keys)) or any(not key or not value for key, value in items):
        raise ValueError(reason)
    return items


def _validate_authority_refs(items: tuple[AuthorityRef, ...]) -> tuple[AuthorityRef, ...]:
    if len(items) != len(set(items)):
        raise ValueError("authority_refs_must_be_unique")
    for owner, identity, version, fingerprint in items:
        if not owner or not identity or not version:
            raise ValueError("authority_ref_lineage_incomplete")
        _require_hash(fingerprint, "authority_ref_fingerprint_invalid")
    return items


class CarrierFact(BaseModel):
    """One owner-issued primitive or bounded tuple admitted to one stage carrier."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    fact_id: str
    owner_id: str
    contract_version: str
    value: CarrierValue
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _validate_law(self) -> "CarrierFact":
        for value, reason in (
            (self.fact_id, "carrier_fact_id_required"),
            (self.owner_id, "carrier_fact_owner_required"),
            (self.contract_version, "carrier_fact_contract_version_required"),
        ):
            _require_text(value, reason)
        if isinstance(self.value, float) and not isfinite(self.value):
            raise ValueError("carrier_fact_float_must_be_finite")
        if isinstance(self.value, tuple) and any(not item for item in self.value):
            raise ValueError("carrier_fact_tuple_contains_empty_identity")
        material = self.model_dump(mode="python")
        material.pop("semantic_fingerprint")
        if self.semantic_fingerprint != semantic_fingerprint(material):
            raise ValueError("carrier_fact_fingerprint_mismatch")
        return self


class StageContext(BaseModel):
    """Immutable K08 context shared by exactly one six-stage serial run."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    context_id: str
    contract_version: str
    prepared_id: str
    prepared_schema_version: str
    prepared_fingerprint: str
    prepared_input_fingerprint: str
    source_capture_refs: tuple[tuple[str, str], ...]
    preparation_policy_version: str
    alignment_policy_version: str
    fingerprint_policy_version: str
    canonicalisation_version: str
    derivation_versions: tuple[Pair, ...]
    effective_at_utc: datetime
    prepared_validation_state: str
    prepared_completeness_state: str
    serial_order_version: str
    runner_version: str
    mapping_policy_versions: tuple[Pair, ...]
    limitations: tuple[str, ...] = ()
    unavailable_owner_facts: tuple[str, ...] = ()
    closed_authority_classes: tuple[str, ...]
    foreign_authority_claimed: bool = False
    semantic_fingerprint: str

    @field_validator("effective_at_utc")
    @classmethod
    def _effective_at_is_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("context_effective_at_must_be_timezone_aware")
        return value

    @model_validator(mode="after")
    def _validate_law(self) -> "StageContext":
        if (
            self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES
            or self.foreign_authority_claimed
        ):
            raise ValueError("context_foreign_authority_claimed")
        required = (
            self.context_id,
            self.contract_version,
            self.prepared_id,
            self.prepared_schema_version,
            self.prepared_fingerprint,
            self.prepared_input_fingerprint,
            self.preparation_policy_version,
            self.alignment_policy_version,
            self.fingerprint_policy_version,
            self.canonicalisation_version,
            self.prepared_validation_state,
            self.prepared_completeness_state,
            self.serial_order_version,
            self.runner_version,
        )
        if any(not item for item in required) or not self.source_capture_refs:
            raise ValueError("context_lineage_incomplete")
        _require_hash(self.prepared_fingerprint, "prepared_fingerprint_invalid")
        _require_hash(
            self.prepared_input_fingerprint,
            "prepared_input_fingerprint_invalid",
        )
        for source_id, capture_id in self.source_capture_refs:
            if not source_id or not capture_id:
                raise ValueError("source_capture_ref_incomplete")
        if (
            self.source_capture_refs != tuple(sorted(self.source_capture_refs))
            or len(self.source_capture_refs) != len(set(self.source_capture_refs))
        ):
            raise ValueError("source_capture_refs_not_canonical")
        _unique_pairs(self.derivation_versions, "derivation_versions_invalid")
        if self.derivation_versions != tuple(sorted(self.derivation_versions)):
            raise ValueError("derivation_versions_not_canonical")
        _unique_pairs(self.mapping_policy_versions, "mapping_policy_versions_invalid")
        if tuple(name for name, _ in self.mapping_policy_versions) != SERIAL_STAGE_ORDER:
            raise ValueError("mapping_policy_versions_must_cover_exact_stage_order")
        if any(not item for item in self.limitations + self.unavailable_owner_facts):
            raise ValueError("context_explicit_state_must_be_nonempty")
        material = self.model_dump(mode="python")
        material.pop("semantic_fingerprint")
        expected = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected:
            raise ValueError("context_fingerprint_mismatch")
        return self


class StageInput(BaseModel):
    """One narrow tagged carrier for exactly one governed M05 stage."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    stage: StageName
    context_id: str
    context_fingerprint: str
    contract_version: str
    carrier_stage: StageName
    carrier_id: str
    carrier_contract_version: str
    carrier_schema_version: str
    carrier_facts: tuple[CarrierFact, ...]
    carrier_fingerprint: str
    authority_refs: tuple[AuthorityRef, ...] = ()
    missing_state: str | None = None

    @model_validator(mode="after")
    def _validate_law(self) -> "StageInput":
        if self.carrier_stage != self.stage:
            raise ValueError("carrier_stage_mismatch")
        for value, reason in (
            (self.context_id, "stage_input_context_id_required"),
            (self.contract_version, "stage_input_contract_version_required"),
            (self.carrier_id, "stage_input_carrier_id_required"),
            (self.carrier_contract_version, "carrier_contract_version_required"),
            (self.carrier_schema_version, "carrier_schema_version_required"),
        ):
            _require_text(value, reason)
        _require_hash(self.context_fingerprint, "stage_input_context_fingerprint_invalid")
        _validate_authority_refs(self.authority_refs)
        if self.missing_state is not None and not self.missing_state:
            raise ValueError("missing_state_must_be_nonempty")
        fact_ids = tuple(item.fact_id for item in self.carrier_facts)
        if len(fact_ids) != len(set(fact_ids)):
            raise ValueError("carrier_fact_identity_duplicate")
        if not set(fact_ids) <= ALLOWED_STAGE_FACT_IDS[self.stage]:
            raise ValueError("carrier_fact_not_admitted_for_stage")
        if not self.carrier_facts and self.missing_state is None:
            raise ValueError("carrier_facts_or_missing_state_required")
        allowed_owners = ALLOWED_STAGE_AUTHORITY_OWNERS[self.stage]
        if any(item.owner_id not in allowed_owners for item in self.carrier_facts):
            raise ValueError("carrier_fact_foreign_owner")
        material = {
            "stage": self.stage,
            "context_id": self.context_id,
            "context_fingerprint": self.context_fingerprint,
            "contract_version": self.contract_version,
            "carrier_stage": self.carrier_stage,
            "carrier_id": self.carrier_id,
            "carrier_contract_version": self.carrier_contract_version,
            "carrier_schema_version": self.carrier_schema_version,
            "carrier_facts": self.carrier_facts,
            "authority_refs": self.authority_refs,
            "missing_state": self.missing_state,
        }
        expected = semantic_fingerprint(material)
        if self.carrier_fingerprint != expected:
            raise ValueError("stage_input_carrier_fingerprint_mismatch")
        return self


class StageOutput(BaseModel):
    """One immutable stage result with exact dependency and authority lineage."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    output_id: str
    stage: StageName
    owner_id: str
    contract_version: str
    schema_version: str
    context_id: str
    context_fingerprint: str
    input_carrier_id: str
    input_carrier_fingerprint: str
    dependency_output_ids: tuple[str, ...] = ()
    dependency_fingerprints: tuple[str, ...] = ()
    status: StageStatus
    result_refs: tuple[Pair, ...] = ()
    reasons: tuple[str, ...] = ()
    consumed_authority_refs: tuple[AuthorityRef, ...] = ()
    packet_refs: tuple[tuple[str, str], ...] = ()
    closed_authority_classes: tuple[str, ...]
    foreign_authority_claimed: bool = False
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _validate_law(self) -> "StageOutput":
        if self.owner_id != STAGE_OWNER_IDS[self.stage]:
            raise ValueError("stage_output_owner_mismatch")
        if (
            self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES
            or self.foreign_authority_claimed
        ):
            raise ValueError("stage_output_foreign_authority_claimed")
        for value, reason in (
            (self.contract_version, "stage_output_contract_version_required"),
            (self.schema_version, "stage_output_schema_version_required"),
            (self.context_id, "stage_output_context_id_required"),
            (self.input_carrier_id, "stage_output_input_carrier_id_required"),
        ):
            _require_text(value, reason)
        _require_hash(self.context_fingerprint, "stage_output_context_fingerprint_invalid")
        _require_hash(
            self.input_carrier_fingerprint,
            "stage_output_input_carrier_fingerprint_invalid",
        )
        if len(self.dependency_output_ids) != len(self.dependency_fingerprints):
            raise ValueError("stage_output_dependency_lineage_mismatch")
        if any(not item for item in self.dependency_output_ids):
            raise ValueError("stage_output_dependency_id_required")
        for value in self.dependency_fingerprints:
            _require_hash(value, "stage_output_dependency_fingerprint_invalid")
        _unique_pairs(self.result_refs, "stage_output_result_refs_invalid")
        _validate_authority_refs(self.consumed_authority_refs)
        for packet_id, packet_fingerprint in self.packet_refs:
            if not packet_id:
                raise ValueError("packet_ref_identity_required")
            _require_hash(packet_fingerprint, "packet_ref_fingerprint_invalid")
        if any(not reason for reason in self.reasons):
            raise ValueError("stage_output_reason_must_be_nonempty")
        if self.status != "complete" and not self.reasons:
            raise ValueError("terminal_stage_output_reason_required")
        material = self.model_dump(mode="python")
        material.pop("output_id")
        material.pop("semantic_fingerprint")
        expected = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected:
            raise ValueError("stage_output_fingerprint_mismatch")
        if self.output_id != f"stage.{self.stage}.{expected[:16]}":
            raise ValueError("stage_output_identity_not_deterministic")
        return self


class SerialCandidate(BaseModel):
    """Immutable K09 formed or explicit terminal serial result."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    status: SerialStatus
    reasons: tuple[str, ...] = ()
    failed_stage: StageName | None = None
    candidate_id: str | None = None
    candidate_contract_version: str
    candidate_schema_version: str
    context_id: str
    context_fingerprint: str
    prepared_id: str
    prepared_fingerprint: str
    stage_order_version: str
    stage_outputs: tuple[StageOutput, ...]
    posture_status: str | None = None
    posture_reasons: tuple[str, ...] = ()
    m07_authority_refs: tuple[AuthorityRef, ...] = ()
    m08_authority_refs: tuple[AuthorityRef, ...] = ()
    ordered_eligible_candidate_ids: tuple[str, ...] = ()
    eligibility_lead_id: str | None = None
    selected_playbook_family_id: str | None = None
    selected_playbook_family_version: str | None = None
    selected_playbook_id: str | None = None
    selected_playbook_version: str | None = None
    selected_setup_variant_id: str | None = None
    selected_setup_variant_version: str | None = None
    expression_id: str | None = None
    expression_version: str | None = None
    expression_fingerprint: str | None = None
    lifecycle_intent: tuple[Pair, ...] = ()
    limitations: tuple[str, ...] = ()
    closed_authority_classes: tuple[str, ...]
    foreign_authority_claimed: bool = False
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _validate_law(self) -> "SerialCandidate":
        material = self.model_dump(mode="python")
        material.pop("candidate_id")
        material.pop("semantic_fingerprint")
        expected = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected:
            raise ValueError("candidate_fingerprint_mismatch")
        if (
            self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES
            or self.foreign_authority_claimed
        ):
            raise ValueError("candidate_foreign_authority_claimed")
        for value, reason in (
            (self.candidate_contract_version, "candidate_contract_version_required"),
            (self.candidate_schema_version, "candidate_schema_version_required"),
            (self.context_id, "candidate_context_id_required"),
            (self.prepared_id, "candidate_prepared_id_required"),
            (self.stage_order_version, "candidate_stage_order_version_required"),
        ):
            _require_text(value, reason)
        _require_hash(self.context_fingerprint, "candidate_context_fingerprint_invalid")
        _require_hash(self.prepared_fingerprint, "candidate_prepared_fingerprint_invalid")
        _validate_authority_refs(self.m07_authority_refs)
        _validate_authority_refs(self.m08_authority_refs)
        _unique_pairs(self.lifecycle_intent, "candidate_lifecycle_intent_invalid")
        observed = tuple(item.stage for item in self.stage_outputs)
        if observed != SERIAL_STAGE_ORDER[: len(observed)]:
            raise ValueError("candidate_stage_order_invalid")
        by_stage = {item.stage: item for item in self.stage_outputs}
        for output in self.stage_outputs:
            if (
                output.context_id != self.context_id
                or output.context_fingerprint != self.context_fingerprint
            ):
                raise ValueError("candidate_stage_context_lineage_mismatch")
            if not output.input_carrier_id or not output.input_carrier_fingerprint:
                raise ValueError("candidate_stage_input_lineage_incomplete")
            dependencies = tuple(
                by_stage[name] for name in SERIAL_STAGE_DEPENDENCIES[output.stage]
            )
            if (
                output.dependency_output_ids
                != tuple(item.output_id for item in dependencies)
                or output.dependency_fingerprints
                != tuple(item.semantic_fingerprint for item in dependencies)
            ):
                raise ValueError("candidate_stage_dependency_lineage_mismatch")
        if self.stage_outputs:
            if any(item.status != "complete" for item in self.stage_outputs[:-1]):
                raise ValueError("candidate_preterminal_stage_status_invalid")
            last = self.stage_outputs[-1]
            expected_terminal = "complete" if self.status == "formed" else self.status
            if last.status != expected_terminal:
                raise ValueError("candidate_terminal_status_mismatch")
            if self.status != "formed" and self.failed_stage != last.stage:
                raise ValueError("candidate_failed_stage_mismatch")
            if self.status != "formed" and self.reasons != last.reasons:
                raise ValueError("candidate_terminal_reasons_mismatch")
        posture = by_stage.get("posture")
        eligibility = by_stage.get("eligibility")
        execution = by_stage.get("execution")
        posture_refs = dict(posture.result_refs) if posture else {}
        if self.posture_status != posture_refs.get("posture_status"):
            raise ValueError("candidate_posture_lineage_mismatch")
        if self.posture_reasons != (posture.reasons if posture else ()):
            raise ValueError("candidate_posture_lineage_mismatch")
        expected_m07 = tuple(
            dict.fromkeys(
                ref
                for ref in (posture.consumed_authority_refs if posture else ())
                if ref[0] == "m07"
            )
        )
        expected_m08 = tuple(
            dict.fromkeys(
                ref
                for output in (eligibility, execution)
                if output is not None
                for ref in output.consumed_authority_refs
                if ref[0] == "m08"
            )
        )
        if self.m07_authority_refs != expected_m07 or self.m08_authority_refs != expected_m08:
            raise ValueError("candidate_authority_lineage_mismatch")
        eligibility_refs = dict(eligibility.result_refs) if eligibility else {}
        expected_candidates = tuple(
            value
            for key, value in sorted(eligibility_refs.items())
            if key.startswith("eligible_candidate.")
        )
        expected_lead = eligibility_refs.get("eligibility_lead_id")
        if (
            self.ordered_eligible_candidate_ids != expected_candidates
            or self.eligibility_lead_id != expected_lead
        ):
            raise ValueError("candidate_eligibility_lineage_mismatch")
        if self.status == "formed":
            if observed != SERIAL_STAGE_ORDER or self.failed_stage is not None:
                raise ValueError("formed_candidate_incomplete")
            if (
                not self.ordered_eligible_candidate_ids
                or self.eligibility_lead_id != self.ordered_eligible_candidate_ids[0]
                or self.selected_playbook_id != self.eligibility_lead_id
            ):
                raise ValueError("formed_candidate_eligibility_lineage_incomplete")
            if self.candidate_id != f"serial.{expected[:16]}":
                raise ValueError("formed_candidate_identity_invalid")
            if self.posture_status != "permitted":
                raise ValueError("formed_candidate_requires_permitted_posture")
            if not self.m07_authority_refs or not self.m08_authority_refs:
                raise ValueError("formed_candidate_authority_lineage_incomplete")
            required_expression = (
                self.selected_playbook_family_id,
                self.selected_playbook_family_version,
                self.selected_playbook_id,
                self.selected_playbook_version,
                self.selected_setup_variant_id,
                self.selected_setup_variant_version,
                self.expression_id,
                self.expression_version,
                self.expression_fingerprint,
            )
            if any(item is None or item == "" for item in required_expression):
                raise ValueError("formed_candidate_expression_lineage_incomplete")
            _require_hash(
                self.expression_fingerprint or "",
                "formed_candidate_expression_fingerprint_invalid",
            )
            execution_refs = dict(execution.result_refs) if execution else {}
            expected_expression = (
                execution_refs.get("playbook_family_id"),
                execution_refs.get("playbook_family_version"),
                execution_refs.get("playbook_id"),
                execution_refs.get("playbook_version"),
                execution_refs.get("setup_variant_id"),
                execution_refs.get("setup_variant_version"),
                execution_refs.get("expression_id"),
                execution_refs.get("expression_version"),
                execution_refs.get("expression_fingerprint"),
            )
            if required_expression != expected_expression:
                raise ValueError("candidate_expression_lineage_mismatch")
            expected_lifecycle = tuple(
                (key.removeprefix("lifecycle."), value)
                for key, value in execution_refs.items()
                if key.startswith("lifecycle.")
            )
            if self.lifecycle_intent != expected_lifecycle:
                raise ValueError("candidate_lifecycle_intent_mismatch")
        elif self.status == "stand_down":
            if self.candidate_id is not None or self.failed_stage not in {
                "posture",
                "eligibility",
            }:
                raise ValueError("stand_down_candidate_or_stage_invalid")
        else:
            if self.candidate_id is not None or self.failed_stage not in SERIAL_STAGE_ORDER:
                raise ValueError("terminal_candidate_or_stage_invalid")
        if self.status != "formed":
            formed_payload = (
                self.selected_playbook_family_id,
                self.selected_playbook_family_version,
                self.selected_playbook_id,
                self.selected_playbook_version,
                self.selected_setup_variant_id,
                self.selected_setup_variant_version,
                self.expression_id,
                self.expression_version,
                self.expression_fingerprint,
            )
            if any(item is not None for item in formed_payload) or self.lifecycle_intent:
                raise ValueError("terminal_candidate_contains_formed_payload")
        return self


__all__ = [
    "CLOSED_AUTHORITY_CLASSES",
    "SERIAL_STAGE_DEPENDENCIES",
    "SERIAL_STAGE_ORDER",
    "STAGE_OWNER_IDS",
    "SerialCandidate",
    "StageContext",
    "StageInput",
    "StageOutput",
    "semantic_fingerprint",
]
