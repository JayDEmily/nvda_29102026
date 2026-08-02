"""Current-law DMPV3 owner facts for retained packet-surface tests."""

from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from typing import Any

from nvda_desk.contracts.packets import (
    K07_COMMON_CHECKS,
    K07_LINEAGE_FIELDS,
    K07_LINEAGE_MATRIX,
    K07_ROLE_CHECKS,
    DmpV3ExecutionContext,
)

_LIST_LINEAGE_FIELDS = {"parentids", "dependencyids", "sourceartifactids"}


def current_packet_kwargs(
    *,
    role: str,
    packet_id: str,
    emitted_at: datetime,
    parentids: list[str] | None = None,
    dependencyids: list[str] | None = None,
    derivedfrom: str | None = None,
    sourceartifactids: list[str] | None = None,
    reviewtraceid: str | None = None,
) -> dict[str, Any]:
    """Return explicit owner-supplied occurrence, lineage and validation facts."""

    states = dict(zip(K07_LINEAGE_FIELDS, K07_LINEAGE_MATRIX[role], strict=True))
    caller_values: dict[str, Any] = {
        "parentids": parentids,
        "dependencyids": dependencyids,
        "derivedfrom": derivedfrom,
        "reviewtraceid": reviewtraceid,
    }
    lineage: dict[str, Any] = {}
    conditionals: set[str] = set()
    for field_name, state in states.items():
        supplied = caller_values.get(field_name)
        if state == "R":
            if supplied:
                value = supplied
            elif field_name in _LIST_LINEAGE_FIELDS:
                value = [f"{field_name}::{packet_id}"]
            elif field_name == "inputfingerprint":
                value = sha256(f"input::{packet_id}".encode()).hexdigest()
            else:
                value = f"{field_name}::{packet_id}"
        elif state == "C" and supplied:
            value = supplied
            conditionals.add(field_name)
        else:
            value = [] if field_name in _LIST_LINEAGE_FIELDS else None
        lineage[field_name] = value

    if sourceartifactids is not None:
        lineage["sourceartifactids"] = list(sourceartifactids)
    execution = {
        "traceid": f"trace::{packet_id}",
        "runid": f"run::{packet_id}",
        "scenarioid": f"scenario::{packet_id}",
    }
    module_version = "current-test-owner.1"
    module_instance_id = f"current-test-owner::{packet_id}"
    admitted_sources = frozenset(lineage["sourceartifactids"])
    expected_checks = frozenset((*K07_COMMON_CHECKS, *K07_ROLE_CHECKS[role]))

    def owner_check(name: str, context: dict[str, Any]) -> bool:
        return bool(
            name in expected_checks
            and context["packetrole"] == role
            and context["execution_context"] == execution
            and context["producer"].module_version == module_version
            and context["producer"].module_instance_id == module_instance_id
            and context["lineage"].model_dump(mode="python") == lineage
        )

    lineage_kwargs = {
        field_name: value
        for field_name, value in lineage.items()
        if states[field_name] == "R" or field_name in conditionals
    }
    return {
        "emitted_at": emitted_at,
        **execution,
        "module_version": module_version,
        "module_instance_id": module_instance_id,
        **lineage_kwargs,
        "source_artifact_validator": lambda source_id: source_id in admitted_sources,
        "input_fingerprint_validator": lambda fingerprint: (
            fingerprint == lineage["inputfingerprint"]
        ),
        "conditional_lineage_fields": conditionals,
        "owner_check_validator": owner_check,
    }


def serial_runtime_packet_authority(scope_id: str) -> dict[str, Any]:
    """Return explicit caller facts for one legacy serial-runtime test occurrence."""

    source_artifact_ids = (f"source::{scope_id}",)
    return {
        "execution_context": DmpV3ExecutionContext(
            traceid=f"trace::{scope_id}",
            runid=f"run::{scope_id}",
            scenarioid=f"scenario::{scope_id}",
        ),
        "packet_emitted_at": datetime(2026, 8, 2, 10, 0, tzinfo=UTC),
        "module_version": "legacy-serial-runtime.1",
        "runtime_instance_id": f"legacy-serial-runtime::{scope_id}",
        "upstream_packet_id": f"prepared-context::{scope_id}",
        "source_artifact_ids": source_artifact_ids,
        "source_artifact_validator": lambda source_id: source_id in source_artifact_ids,
    }


def parallel_risk_compatibility_authority(
    scope_id: str,
    *,
    emitted_at: datetime | None = None,
    sourceartifactids: list[str] | None = None,
    inputfingerprint: str | None = None,
) -> dict[str, Any]:
    """Return explicit facts for one non-binding legacy parallel-risk specimen."""

    resolved_sources = list(sourceartifactids or [f"source::parallel-risk::{scope_id}"])
    resolved_fingerprint = (
        inputfingerprint or sha256(f"parallel-risk-input::{scope_id}".encode()).hexdigest()
    )
    return {
        "emitted_at": emitted_at or datetime(2026, 8, 2, 11, 0, tzinfo=UTC),
        "traceid": f"trace::parallel-risk::{scope_id}",
        "runid": f"run::parallel-risk::{scope_id}",
        "scenarioid": f"scenario::parallel-risk::{scope_id}",
        "derivedfrom": f"test-specimen::parallel-risk::{scope_id}",
        "sourceartifactids": resolved_sources,
        "inputfingerprint": resolved_fingerprint,
    }
