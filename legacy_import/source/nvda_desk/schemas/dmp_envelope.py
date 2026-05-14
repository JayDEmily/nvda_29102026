"""Dependency-light DMPV3 envelope primitives.

This module holds the generic DMPV3 shell without importing repo payload unions.
Schema modules that need canonical DMPV3 carriage without pulling the full desk
payload registry should depend on this leaf module.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DmpV3Producer(BaseModel):
    """Structured producer identity for one DMPV3 packet."""

    model_config = ConfigDict(extra="forbid")

    module_id: str = Field(min_length=1)
    module_version: str = Field(min_length=1)
    module_instance_id: str = Field(min_length=1)
    grammar_role: str = Field(min_length=1)
    stage_name: str | None = None
    behaviour_class: str = Field(min_length=1)


class DmpV3Lineage(BaseModel):
    """DMPV3 lineage surface plus bounded repo compatibility metadata."""

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
    """One named DMPV3 validation check result."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    passed: bool


class DmpV3Validation(BaseModel):
    """DMPV3 validation record."""

    model_config = ConfigDict(extra="forbid")

    status: str = Field(default="valid", min_length=1)
    checks: list[DmpV3ValidationCheck] = Field(
        default_factory=lambda: [DmpV3ValidationCheck(name="schema_validation", passed=True)]
    )
    violations: list[str] = Field(default_factory=list)


class DmpV3Summary(BaseModel):
    """Human-facing summary block carried by every DMPV3 packet."""

    model_config = ConfigDict(extra="forbid")

    headline: str = Field(min_length=1)
    keyflags: list[str] = Field(default_factory=list)
    humanstate: str = Field(min_length=1)


def _deep_merge_dicts(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge extension dictionaries without dropping canonical leaves."""

    merged = deepcopy(base)
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge_dicts(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged

class DmpV3Envelope[PayloadT: BaseModel](BaseModel):
    """Canonical dependency-light DMPV3 packet envelope."""

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
    data: PayloadT
    dmpextensions: dict[str, Any] = Field(default_factory=dict)

    @property
    def protocol_version(self) -> str:
        return "dmp.v3"

    @property
    def packet_id(self) -> str:
        return self.id

    @property
    def payload(self) -> PayloadT:
        return self.data

    @property
    def trader_summary(self) -> str:
        return self.summary.headline

    @property
    def stack_id(self) -> str | None:
        return (
            self.dmpextensions.get("nvda", {})
            .get("execution_context", {})
            .get("stack_id")
        )

    @property
    def coefficient_set_id(self) -> str | None:
        return (
            self.dmpextensions.get("nvda", {})
            .get("execution_context", {})
            .get("coefficient_set_id")
        )

    @property
    def dependencies(self) -> list[str]:
        raw = self.dmpextensions.get("nvda", {}).get("semantic_dependencies", [])
        if isinstance(raw, list):
            return [str(item) for item in raw]
        return []


def build_dmp_v3_envelope_kwargs(
    *,
    packet_id: str,
    emitted_at: datetime,
    grammar_role: str,
    behaviour_class: str,
    payload: BaseModel,
    trader_summary: str,
    stack_id: str | None = None,
    coefficient_set_id: str | None = None,
    dependencies: list[str] | None = None,
    input_model_name: str | None = None,
    output_model_name: str | None = None,
    parent_packet_ids: list[str] | None = None,
    dependency_packet_ids: list[str] | None = None,
    source_artifact_ids: list[str] | None = None,
    review_trace_id: str | None = None,
    replay_trace_id: str | None = None,
    decision_trace_id: str | None = None,
    trace_id: str | None = None,
    run_id: str | None = None,
    scenario_id: str | None = None,
    module_id: str | None = None,
    module_version: str = "1.0.0",
    module_instance_id: str | None = None,
    stage_name: str | None = None,
    registry_version: str | None = None,
    environment_tag: str | None = None,
    dmpextensions: dict[str, Any] | None = None,
    dataschema: str | None = None,
    source: str | None = None,
    packet_type: str | None = None,
    packetrole: str | None = None,
    validation_violations: list[str] | None = None,
    summary_keyflags: list[str] | None = None,
) -> dict[str, Any]:
    """Return canonical DMPV3 envelope kwargs for one typed payload."""

    payload_model = payload.__class__
    resolved_output_model = output_model_name or payload_model.__name__
    resolved_module_id = module_id or grammar_role
    resolved_source = source or f"urn:nvda:producer:{resolved_module_id}"
    resolved_type = packet_type or f"urn:nvda:packet:{grammar_role}.{behaviour_class}"
    resolved_dataschema = dataschema or f"urn:nvda:schema:{grammar_role}.output:1.0.0"
    resolved_packetrole = packetrole or behaviour_class
    extensions_payload: dict[str, Any] = {
        "nvda": {
            "execution_context": {
                "stack_id": stack_id,
                "coefficient_set_id": coefficient_set_id,
                "registry_version": registry_version,
                "environment_tag": environment_tag,
            },
            "schema_identifiers": {
                "payload_model_name": payload_model.__name__,
                "payload_module_path": payload_model.__module__,
                "input_model_name": input_model_name,
                "output_model_name": resolved_output_model,
            },
            "semantic_dependencies": list(dependencies or []),
        }
    }
    if dmpextensions:
        extensions_payload = _deep_merge_dicts(extensions_payload, dict(dmpextensions))

    violations = list(validation_violations or [])
    validation = DmpV3Validation(violations=violations)
    if violations:
        validation.status = "degraded"
        validation.checks = [DmpV3ValidationCheck(name="schema_validation", passed=False)]

    return {
        "id": packet_id,
        "source": resolved_source,
        "type": resolved_type,
        "time": emitted_at,
        "dataschema": resolved_dataschema,
        "traceid": trace_id or f"trace::{packet_id}",
        "runid": run_id or f"run::{packet_id}",
        "scenarioid": scenario_id or "live",
        "packetrole": resolved_packetrole,
        "producer": DmpV3Producer(
            module_id=resolved_module_id,
            module_version=module_version,
            module_instance_id=module_instance_id or f"{resolved_module_id}::default",
            grammar_role=grammar_role,
            stage_name=stage_name or grammar_role,
            behaviour_class=behaviour_class,
        ),
        "lineage": DmpV3Lineage(
            parentids=list(parent_packet_ids or []),
            dependencyids=list(dependency_packet_ids or []),
            derivedfrom=(f"{grammar_role}_from_declared_dependencies" if dependency_packet_ids else None),
            replayref=replay_trace_id,
            sourceartifactids=list(source_artifact_ids or []),
            reviewtraceid=review_trace_id,
            replaytraceid=replay_trace_id,
            decisiontraceid=decision_trace_id,
        ),
        "validation": validation,
        "summary": DmpV3Summary(
            headline=trader_summary,
            keyflags=list(summary_keyflags or []),
            humanstate=trader_summary,
        ),
        "data": payload,
        "dmpextensions": extensions_payload,
    }
