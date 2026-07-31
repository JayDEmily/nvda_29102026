"""Build prepared-context payloads and DMPV3 packets without trading side effects."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime
from typing import Any

from nvda_desk.contracts.packets import DeskModulePacketV3
from nvda_desk.contracts.prepared_context import (
    PreparedContextPayload,
)
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
    emitted_at: datetime | None = None,
    traceid: str | None = None,
    runid: str | None = None,
    scenarioid: str | None = None,
    parentids: list[str] | None = None,
    dependencyids: list[str] | None = None,
    reviewtraceid: str | None = None,
) -> DeskModulePacketV3:
    """Build the canonical prepared-context DMPV3 handoff packet."""

    payload = build_prepared_context_payload(snapshot)
    violations = list(payload.failed_enrichments)
    source_artifact_ids = list(payload.source_artifact_ids)
    if not source_artifact_ids and payload.source_snapshot_id:
        source_artifact_ids = [payload.source_snapshot_id]
    return DmpPacketBuilder.build_prepared_context_packet(
        packet_id=packet_id,
        data=payload,
        emitted_at=emitted_at,
        traceid=traceid,
        runid=runid,
        scenarioid=scenarioid,
        parentids=parentids,
        dependencyids=dependencyids,
        sourceartifactids=source_artifact_ids,
        inputfingerprint=(
            payload.input_fingerprint or fingerprint_prepared_context_payload(payload)
        ),
        reviewtraceid=reviewtraceid,
        validation_violations=violations,
        summary_keyflags=["prepared_context"],
        dmpextensions={
            "nvda": {
                "source_temporal_standard": {
                    "source_time_utc": (
                        payload.source_time_utc.isoformat()
                        if payload.source_time_utc is not None
                        else None
                    ),
                    "source_date": (
                        payload.source_date.isoformat() if payload.source_date is not None else None
                    ),
                    "alignment_policy": payload.alignment_policy,
                }
            }
        },
    )


def build_context_payload_mapping(snapshot: PreparedRuntimeSnapshot) -> dict[str, Any]:
    """Return a JSON-shaped detached mapping for checkpoint and receipt writers."""

    return build_prepared_context_payload(snapshot).model_dump(mode="json")
