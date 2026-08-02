from __future__ import annotations

from datetime import UTC, datetime, timedelta

from tests.support.m03_k05_k06_contract_harness import (
    production_api,
    production_capture_payload,
    valid_capture_reference,
)

from nvda_desk.contracts.packets import DmpV3ExecutionContext, PreparedContextIdentity
from nvda_desk.downstream.checkpoints import PreparedIngressCheckpoint
from nvda_desk.ingress.raw_bundle_loader import load_api_payload
from nvda_desk.preparation.context_packet import (
    build_context_payload_mapping,
    build_prepared_context_packet,
    build_prepared_context_payload,
    fingerprint_prepared_context_payload,
)
from nvda_desk.preparation.runtime_preparer import (
    prepare_runtime_dataset,
    prepare_runtime_snapshot_from_envelope,
)


def _prepared_snapshot():
    source_time_utc = datetime(2026, 4, 21, 9, 31, 45, tzinfo=UTC)
    return prepare_runtime_dataset(
        load_api_payload(
            {
                "snapshot_id": "snap-context-1",
                "source_time_utc": source_time_utc,
                "market_snapshot": {
                    "spot_price": 100.0,
                    "prior_close": 90.0,
                    "windows": [
                        {
                            "event_id": "earnings",
                            "window_start_utc": source_time_utc + timedelta(minutes=10),
                            "window_end_utc": source_time_utc + timedelta(minutes=20),
                        }
                    ],
                },
                "options_surface": {"front_dte": 1, "next_dte": 5},
            }
        )
    ).primary_snapshot


def _governed_snapshot(*, degraded: bool = False):
    api = production_api()
    reference = valid_capture_reference()
    capture = api["SourceCaptureReference"].model_validate(production_capture_payload(reference))
    limitation = "calendar_reference_projection_missing"
    envelope = api["PreparedDataBuilder"]().build(
        source_capture_refs=(capture,),
        input_schema_versions={"market.snapshot": "1.0.0"},
        schema_version="1.0.0",
        preparation_policy_version="prepare.1.0.0",
        alignment_policy_version="alignment.1.0.0",
        fingerprint_policy_version="sha256.1.0.0",
        canonicalisation_version="json.1.0.0",
        derivation_versions={},
        effective_at_utc=reference.effective_at_utc,
        payload=api["PreparedRuntimePayloadV1"](spot_price=100.0, prior_close=90.0),
        payload_schema_version="1.0.0",
        validation_state="degraded" if degraded else "valid",
        completeness_state="degraded" if degraded else "complete",
        limitations=(limitation,) if degraded else (),
    )
    return prepare_runtime_snapshot_from_envelope(envelope), envelope


def test_prepared_context_payload_is_detached_and_fingerprinted() -> None:
    snapshot = _prepared_snapshot()
    payload = build_prepared_context_payload(snapshot)
    first_fingerprint = fingerprint_prepared_context_payload(payload)

    snapshot.payload["spot_price"] = 999.0
    payload.payload["spot_price"] = 777.0
    rebuilt = build_prepared_context_payload(_prepared_snapshot())

    assert payload.snapshot_id == "snap-context-1"
    assert payload.source_snapshot_id == "snap-context-1"
    assert payload.source_sections == ["market_snapshot", "options_surface"]
    assert payload.alignment_policy == "floor_minute_from_source_time_utc"
    assert first_fingerprint == fingerprint_prepared_context_payload(rebuilt)
    assert rebuilt.payload["spot_price"] == 100.0


def test_prepared_context_packet_uses_canonical_dmp_shell_and_lineage() -> None:
    snapshot, envelope = _governed_snapshot()
    packet = build_prepared_context_packet(
        packet_id="prepared-context-1",
        snapshot=snapshot,
        emitted_at=datetime(2026, 4, 21, 10, 0, tzinfo=UTC),
        execution_context=DmpV3ExecutionContext(
            traceid="trace-1", runid="run-1", scenarioid="scenario-1"
        ),
        module_version="prepared-context.1",
        module_instance_id="prepared-context-instance-1",
        parentids=["raw-bundle-1"],
    )

    assert packet.specversion == "1.0"
    assert packet.dmpversion == "3.0.0"
    assert packet.packetrole == "prepared_context_packet"
    assert packet.dataschema == "nvda.preparation.PreparedRuntimeContext.v1"
    assert packet.producer.module_id == "prepared_ingress"
    assert packet.producer.grammar_role == "prepared_runtime_context"
    assert packet.producer.behaviour_class == "preparation_output"
    assert packet.producer.stage_name == "runtime_context_preparation"
    assert packet.lineage.sourceartifactids == ["source.market.1"]
    assert packet.lineage.parentids == ["raw-bundle-1"]
    assert packet.lineage.derivedfrom == envelope.prepared_id
    assert packet.lineage.inputfingerprint == envelope.prepared_fingerprint
    assert packet.validation.status == "valid"
    assert packet.data == PreparedContextIdentity(
        prepared_id=envelope.prepared_id,
        prepared_fingerprint=envelope.prepared_fingerprint,
        schema_version=envelope.schema_version,
        preparation_policy_version=envelope.preparation_policy_version,
    )
    assert packet.dmpextensions["nvda"]["source_temporal_standard"]["alignment_policy_version"] == (
        "alignment.1.0.0"
    )


def test_prepared_ingress_checkpoint_receipt_is_copy_safe() -> None:
    snapshot = _prepared_snapshot()
    checkpoint = PreparedIngressCheckpoint.from_snapshot("checkpoint-1", snapshot)
    receipt = checkpoint.as_receipt_payload(snapshot)
    receipt["prepared_context"]["payload"]["spot_price"] = 0.0

    assert checkpoint.status == "valid"
    assert receipt["checkpoint_id"] == "checkpoint-1"
    assert build_context_payload_mapping(snapshot)["payload"]["spot_price"] == 100.0


def test_prepared_context_packet_carries_failed_enrichment_as_degraded_validation() -> None:
    snapshot, envelope = _governed_snapshot(degraded=True)

    packet = build_prepared_context_packet(
        packet_id="prepared-context-degraded",
        snapshot=snapshot,
        emitted_at=datetime(2026, 4, 21, 10, 0, tzinfo=UTC),
        execution_context=DmpV3ExecutionContext(
            traceid="trace-degraded",
            runid="run-degraded",
            scenarioid="scenario-degraded",
        ),
        module_version="prepared-context.1",
        module_instance_id="prepared-context-instance-1",
    )

    assert packet.validation.status == "degraded"
    assert packet.validation.violations == ["calendar_reference_projection_missing"]
    assert packet.summary.humanstate == "degraded"
    assert "calendar_reference_projection_missing" in packet.summary.keyflags
    assert packet.data.prepared_id == envelope.prepared_id
    assert "consumer_restriction:non_binding_prepared_context" in packet.summary.keyflags
