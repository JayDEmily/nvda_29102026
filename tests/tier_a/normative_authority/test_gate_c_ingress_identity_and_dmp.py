from __future__ import annotations

from dataclasses import fields
from datetime import datetime, timezone

import pytest

from nvda_desk.adapters.ingress.market_snapshot_feed import adapt_market_snapshot
from nvda_desk.adapters.ingress.options_surface_feed import adapt_options_surface
from nvda_desk.contracts.packets import build_dmp_v3_envelope_kwargs
from nvda_desk.contracts.stage_inputs import CommonStageContext, StageInputBundle
from nvda_desk.ingress.raw_bundle_loader import RawBundleLoader
from nvda_desk.preparation.runtime_preparer import PreparedRuntimeLineage

_SOURCE_TIME = datetime(2026, 4, 21, 13, 31, tzinfo=timezone.utc)


def test_c001_c003_market_adapter_enforces_external_source_authority_recursively() -> None:
    payload = {
        "snapshot_id": "snap-1",
        "source_time_utc": _SOURCE_TIME,
        "market_snapshot": {"spot_price": 100.0, "nested": {"trade_allowed": True}},
    }

    with pytest.raises(ValueError, match="forbidden_external_payload_keys"):
        adapt_market_snapshot(payload)


def test_c001_c003_options_adapter_enforces_external_source_authority_recursively() -> None:
    payload = {
        "source_time_utc": _SOURCE_TIME,
        "market_snapshot": {"spot_price": 100.0},
        "options_surface": {
            "spot_price": 100.0,
            "front_dte": 1,
            "next_dte": 5,
            "nested": {"authorised_notional_usd": 1_000_000},
        },
    }

    with pytest.raises(ValueError, match="forbidden_external_payload_keys"):
        adapt_options_surface(payload)


def test_c002_raw_bundle_rejects_untyped_fallback_shape_instead_of_reclassifying_it() -> None:
    with pytest.raises(ValueError, match="unsupported|typed|section|family"):
        RawBundleLoader().load_api_payload(
            {"source_time_utc": _SOURCE_TIME, "unrelated_provider_payload": {"x": 1}}
        )


def test_c009_stage_bundle_carries_common_identity_and_version_metadata_without_widening_payloads() -> (
    None
):
    required = {
        "context_id",
        "prepared_id",
        "prepared_fingerprint",
        "input_schema_versions",
        "preparation_policy_version",
    }
    assert "common_context" in StageInputBundle.model_fields
    assert required.issubset(CommonStageContext.model_fields)


def test_c012_prepared_lineage_names_material_derivation_versions_and_input_provenance() -> None:
    names = {field.name for field in fields(PreparedRuntimeLineage)}
    required = {
        "source_artifact_ids",
        "input_fingerprint",
        "input_schema_version",
        "preparation_policy_version",
        "derivation_versions",
    }
    assert required.issubset(names)


def test_c010_c016_dmp_builder_rejects_missing_caller_owned_execution_context_and_lineage() -> None:
    with pytest.raises(
        ValueError, match="traceid|runid|scenarioid|sourceartifactids|inputfingerprint"
    ):
        build_dmp_v3_envelope_kwargs(
            packet_id="packet-1",
            dataschema="Fixture",
            data={"value": 1},
            packetrole="stage_packet",
            module_id="fixture",
            grammar_role="fixture",
            behaviour_class="stage_output",
        )


def test_c016_dmp_domain_content_is_reproducible_when_process_metadata_is_explicit() -> None:
    emitted_at = datetime(2026, 4, 21, 13, 31, 1, tzinfo=timezone.utc)
    kwargs = dict(
        packet_id="packet-1",
        dataschema="Fixture",
        data={"value": 1},
        packetrole="stage_packet",
        module_id="fixture",
        grammar_role="fixture",
        behaviour_class="stage_output",
        emitted_at=emitted_at,
        traceid="trace-1",
        runid="run-1",
        scenarioid="scenario-1",
        parentids=["upstream-packet-1"],
        derivedfrom="fixture-derived-from",
        sourceartifactids=["capture-1"],
        inputfingerprint="f" * 64,
        module_version="1.0.0",
        module_instance_id="fixture-instance-1",
        source_artifact_validator=lambda value: value == "capture-1",
        input_fingerprint_validator=lambda value: value == "f" * 64,
        owner_check_validator=lambda _name, _context: True,
    )
    first = build_dmp_v3_envelope_kwargs(**kwargs)
    second = build_dmp_v3_envelope_kwargs(**kwargs)

    assert first == second
    assert first["time"] == emitted_at
    assert first["lineage"].sourceartifactids == ["capture-1"]
