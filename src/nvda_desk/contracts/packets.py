"""Canonical DMPV3 packet-carriage contracts for the live native repo."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


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

    if emitted_at is None:
        emitted_at = datetime.now(UTC)

    violations = list(validation_violations or [])
    resolved_traceid = traceid
    if resolved_traceid is None:
        resolved_traceid = f"trace::{packet_id}"
        violations.append("traceid_defaulted_from_packet_id")

    resolved_runid = runid
    if resolved_runid is None:
        resolved_runid = f"run::{packet_id}"
        violations.append("runid_defaulted_from_packet_id")

    resolved_scenarioid = scenarioid or "live"
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

    validation = DmpV3Validation(violations=violations)
    if violations:
        validation.status = "degraded"
        validation.checks = [DmpV3ValidationCheck(name="carriage_context", passed=False)]

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
        for violation in violations:
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
            module_instance_id=module_instance_id or f"{module_id}::default",
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
