"""Build prepared-context payloads and DMPV3 packets without trading side effects."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime
from typing import Any

from nvda_desk.contracts.packets import (
    K07_COMMON_CHECKS,
    K07_ROLE_CHECKS,
    DeskModulePacketV3,
    DmpV3ExecutionContext,
    PreparedContextIdentity,
)
from nvda_desk.contracts.prepared_context import (
    PreparedContextPayload,
)
from nvda_desk.contracts.prepared_data import PreparedDataEnvelope
from nvda_desk.packets.dmp_packets import DmpPacketBuilder
from nvda_desk.preparation.runtime_preparer import PreparedRuntimeSnapshot


def build_prepared_context_payload(
    snapshot: PreparedRuntimeSnapshot,
) -> PreparedContextPayload:
    """Return a detached prepared-context payload from one prepared snapshot."""

    return PreparedContextPayload(
        snapshot_id=snapshot.snapshot_id,
        payload=deepcopy(snapshot.payload),
        derived_fields=deepcopy(snapshot.derived_fields),
        missing_optional_enrichments=list(snapshot.missing_optional_enrichments),
        failed_enrichments=list(snapshot.failed_enrichments),
        source_kind=snapshot.lineage.source_kind,
        transport=snapshot.lineage.transport,
        source_snapshot_id=snapshot.lineage.source_snapshot_id,
        source_sections=list(snapshot.lineage.source_sections),
        alignment_policy=snapshot.lineage.alignment_policy,
        runtime_bar_time_utc=snapshot.lineage.runtime_bar_time_utc,
        derived_field_names=list(snapshot.lineage.derived_field_names),
        source_artifact_ids=list(snapshot.lineage.source_artifact_ids),
        capture_ids=list(snapshot.lineage.capture_ids),
        input_fingerprint=snapshot.lineage.input_fingerprint,
        input_schema_version=snapshot.lineage.input_schema_version,
        input_schema_versions=dict(snapshot.lineage.input_schema_versions),
        preparation_policy_version=snapshot.lineage.preparation_policy_version,
        derivation_versions=dict(snapshot.lineage.derivation_versions),
        prepared_id=(
            snapshot.prepared_envelope.prepared_id
            if snapshot.prepared_envelope is not None
            else None
        ),
        prepared_fingerprint=(
            snapshot.prepared_envelope.prepared_fingerprint
            if snapshot.prepared_envelope is not None
            else None
        ),
        payload_kind=(
            snapshot.prepared_envelope.payload_kind
            if snapshot.prepared_envelope is not None
            else None
        ),
        source_time_utc=snapshot.payload.get("source_time_utc"),
        source_date=snapshot.payload.get("source_date"),
    )


def fingerprint_prepared_context_payload(payload: PreparedContextPayload) -> str:
    """Return a deterministic SHA256 fingerprint for a prepared-context payload."""

    encoded = json.dumps(
        payload.model_dump(mode="json"), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_prepared_context_packet(
    *,
    packet_id: str,
    snapshot: PreparedRuntimeSnapshot,
    emitted_at: datetime,
    execution_context: DmpV3ExecutionContext,
    module_version: str,
    module_instance_id: str,
    parentids: list[str] | None = None,
    dependencyids: list[str] | None = None,
    reviewtraceid: str | None = None,
) -> DeskModulePacketV3:
    """Build one governed M03 identity handoff from a canonical envelope."""

    if snapshot.prepared_envelope is None:
        raise ValueError("canonical_prepared_envelope_required")
    try:
        envelope = PreparedDataEnvelope.model_validate(
            snapshot.prepared_envelope.model_dump(mode="python")
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("prepared_envelope_contract_invalid") from exc
    if not isinstance(execution_context, DmpV3ExecutionContext):
        raise TypeError("dmp_v3_execution_context_required")
    try:
        governed_context = DmpV3ExecutionContext.model_validate(
            execution_context.model_dump(mode="python")
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("execution_context_contract_invalid") from exc

    identity = PreparedContextIdentity(
        prepared_id=envelope.prepared_id,
        prepared_fingerprint=envelope.prepared_fingerprint,
        schema_version=envelope.schema_version,
        preparation_policy_version=envelope.preparation_policy_version,
    )
    source_artifact_ids = [
        reference.source_artifact_id for reference in envelope.source_capture_refs
    ]
    admitted_sources = frozenset(source_artifact_ids)
    limitations = list(
        dict.fromkeys((*envelope.limitations, *envelope.missing_optional_enrichments))
    )
    admitted_limitations = frozenset(limitations)
    conditional_lineage_fields = {
        field_name
        for field_name, value in (
            ("parentids", parentids),
            ("dependencyids", dependencyids),
            ("reviewtraceid", reviewtraceid),
        )
        if value
    }
    owner_checks = frozenset((*K07_COMMON_CHECKS, *K07_ROLE_CHECKS["prepared_context_packet"]))

    def _owner_check(name: str, context: dict[str, Any]) -> bool:
        producer = context["producer"]
        lineage = context["lineage"]
        packet_context = context["execution_context"]
        return bool(
            name in owner_checks
            and context["packetrole"] == "prepared_context_packet"
            and context["data"] == identity
            and producer.module_id == "prepared_ingress"
            and producer.module_version == module_version
            and producer.module_instance_id == module_instance_id
            and packet_context == governed_context.model_dump(mode="python")
            and lineage.derivedfrom == envelope.prepared_id
            and lineage.sourceartifactids == source_artifact_ids
            and lineage.inputfingerprint == envelope.prepared_fingerprint
            and tuple(context["optional_limitations"]) == tuple(limitations)
        )

    return DmpPacketBuilder.build_prepared_context_packet(
        packet_id=packet_id,
        data=identity,
        emitted_at=emitted_at,
        traceid=governed_context.traceid,
        runid=governed_context.runid,
        scenarioid=governed_context.scenarioid,
        module_version=module_version,
        module_instance_id=module_instance_id,
        parentids=parentids,
        dependencyids=dependencyids,
        derivedfrom=envelope.prepared_id,
        sourceartifactids=source_artifact_ids,
        inputfingerprint=envelope.prepared_fingerprint,
        reviewtraceid=reviewtraceid,
        source_artifact_validator=lambda source_id: source_id in admitted_sources,
        input_fingerprint_validator=lambda fingerprint: (
            fingerprint == envelope.prepared_fingerprint
        ),
        conditional_lineage_fields=conditional_lineage_fields,
        owner_check_validator=_owner_check,
        validation_violations=limitations,
        optional_limitation_validator=(
            (lambda limitation: limitation in admitted_limitations) if limitations else None
        ),
        degraded_consumer_restriction=("non_binding_prepared_context" if limitations else None),
        summary_keyflags=["prepared_context"],
        dmpextensions={
            "nvda": {
                "source_temporal_standard": {
                    "effective_at_utc": envelope.effective_at_utc.isoformat(),
                    "alignment_policy_version": envelope.alignment_policy_version,
                }
            }
        },
    )


def build_context_payload_mapping(snapshot: PreparedRuntimeSnapshot) -> dict[str, Any]:
    """Return a JSON-shaped detached mapping for checkpoint and receipt writers."""

    return build_prepared_context_payload(snapshot).model_dump(mode="json")
