from __future__ import annotations

import ast
import dataclasses
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import get_type_hints

import pytest

from nvda_desk.contracts.packets import DmpV3ExecutionContext
from nvda_desk.ingress.raw_bundle_loader import load_api_payload
from nvda_desk.preparation.context_packet import (
    build_context_payload_mapping,
    build_prepared_context_packet,
    build_prepared_context_payload,
    fingerprint_prepared_context_payload,
)
from nvda_desk.preparation.runtime_preparer import (
    PreparedRuntimeDataset,
    PreparedRuntimeSnapshot,
    RuntimePreparationService,
    prepare_runtime_dataset,
    prepare_runtime_snapshot,
)

ROOT = Path(__file__).resolve().parents[3]
SELECTED_NATIVE_FILES = (
    ROOT / "src/nvda_desk/preparation/runtime_preparer.py",
    ROOT / "src/nvda_desk/preparation/context_packet.py",
    ROOT / "src/nvda_desk/contracts/prepared_context.py",
)
PROHIBITED_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.schemas.dataset",
    "nvda_desk.services.options_flow_context",
)
PROHIBITED_DONOR_SYMBOLS = {
    "EventRecord",
    "PreparedRuntimeFixturePack",
    "RealDataCognitionInputs",
    "RuntimeSnapshotSanityReport",
}
PROHIBITED_DONOR_DATASET_FIELDS = {
    "dataset_id",
    "symbol",
    "provenance",
    "events",
    "bars",
    "option_chain_snapshots",
}

REOPENED_ROW_CASES = (
    ("FWD009-AUDIT-001", "atlas_donor_trace_review_003", "prepared_context_packet_trace_review"),
    ("FWD009-AUDIT-002", "atlas_donor_dataset_002", "provenance_lineage"),
    ("FWD009-AUDIT-003", "atlas_donor_dataset_005", "repeated_snapshot_copy_safe"),
    ("FWD009-AUDIT-005", "atlas_donor_dataset_008", "real_data_bundle_preparation"),
    ("FWD009-AUDIT-006", "atlas_donor_dataset_009", "options_flow_input_carriage"),
    ("FWD009-AUDIT-007", "atlas_donor_dataset_011", "options_flow_input_carriage"),
    ("FWD009-AUDIT-008", "atlas_donor_dataset_015", "normalised_feature_derivation"),
    ("FWD009-AUDIT-009", "atlas_donor_dataset_018", "prepared_runtime_dataset_contract"),
    ("FWD009-AUDIT-010", "atlas_donor_dataset_020", "prepared_fixture_payload_copy_safe"),
    ("FWD009-AUDIT-011", "atlas_donor_dataset_022", "native_lean_transform_boundary"),
    ("FWD009-AUDIT-012", "atlas_donor_service_chain_to_cognition_002", "service_identity"),
    (
        "FWD009-AUDIT-013",
        "atlas_donor_service_chain_to_cognition_005",
        "service_snapshot_conversion",
    ),
    (
        "FWD009-AUDIT-014",
        "atlas_donor_service_chain_to_cognition_007",
        "service_dataset_conversion",
    ),
    (
        "FWD009-AUDIT-015",
        "atlas_donor_service_market_regime_context_001",
        "market_regime_input_carriage",
    ),
    (
        "FWD009-AUDIT-016",
        "atlas_donor_service_market_regime_context_005",
        "market_regime_input_carriage",
    ),
    (
        "FWD009-AUDIT-017",
        "atlas_donor_service_market_regime_context_006",
        "market_regime_input_carriage",
    ),
    (
        "FWD009-AUDIT-018",
        "atlas_donor_service_market_regime_context_007",
        "market_regime_input_carriage",
    ),
    (
        "FWD009-AUDIT-019",
        "atlas_donor_service_market_regime_context_008",
        "market_regime_input_carriage",
    ),
    (
        "FWD009-AUDIT-020",
        "atlas_donor_service_market_regime_context_009",
        "market_regime_input_carriage",
    ),
    (
        "FWD009-AUDIT-021",
        "atlas_donor_service_market_regime_context_010",
        "market_regime_input_carriage",
    ),
    ("FWD009-AUDIT-022", "atlas_donor_options_flow_context_001", "native_lean_transform_boundary"),
    ("FWD009-AUDIT-023", "atlas_donor_options_flow_context_002", "service_identity"),
    ("FWD009-AUDIT-024", "atlas_donor_options_flow_context_003", "options_flow_input_carriage"),
    ("FWD009-AUDIT-025", "atlas_donor_options_flow_context_004", "options_flow_input_carriage"),
    ("FWD009-AUDIT-026", "atlas_donor_options_flow_context_005", "options_flow_input_carriage"),
    ("FWD009-AUDIT-028", "atlas_donor_options_flow_context_008", "options_flow_input_carriage"),
    ("FWD009-AUDIT-029", "atlas_donor_options_flow_context_009", "options_flow_input_carriage"),
    ("FWD009-AUDIT-030", "atlas_donor_options_flow_context_010", "options_flow_input_carriage"),
    ("FWD009-AUDIT-031", "atlas_donor_options_flow_context_011", "options_flow_input_carriage"),
    ("FWD009-AUDIT-032", "atlas_donor_options_flow_context_012", "options_flow_input_carriage"),
    ("FWD009-AUDIT-033", "atlas_donor_options_flow_context_013", "options_flow_input_carriage"),
    ("FWD009-AUDIT-034", "atlas_donor_options_flow_context_014", "options_flow_input_carriage"),
    ("FWD009-AUDIT-035", "atlas_donor_options_flow_context_015", "options_flow_input_carriage"),
    ("FWD009-AUDIT-036", "atlas_donor_options_flow_context_017", "options_flow_input_carriage"),
    ("FWD009-AUDIT-037", "atlas_donor_options_flow_context_018", "options_flow_input_carriage"),
    ("FWD009-AUDIT-038", "atlas_donor_temporal_context_001", "native_lean_transform_boundary"),
    ("FWD009-AUDIT-039", "atlas_donor_temporal_context_002", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-040", "atlas_donor_temporal_context_003", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-041", "atlas_donor_temporal_context_004", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-042", "atlas_donor_temporal_context_005", "service_identity"),
    ("FWD009-AUDIT-043", "atlas_donor_temporal_context_009", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-044", "atlas_donor_temporal_context_010", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-045", "atlas_donor_temporal_context_011", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-046", "atlas_donor_temporal_context_013", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-047", "atlas_donor_temporal_context_014", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-048", "atlas_donor_temporal_context_015", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-049", "atlas_donor_temporal_context_016", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-050", "atlas_donor_temporal_context_017", "temporal_event_context_preparation"),
    ("FWD009-AUDIT-051", "atlas_donor_temporal_context_019", "temporal_event_context_preparation"),
)


def _base_time() -> datetime:
    return datetime(2026, 5, 19, 9, 31, 45, tzinfo=UTC)


def _bundle_payload(audit_row_id: str, atlas_record_id: str) -> dict[str, object]:
    source_time_utc = _base_time()
    return {
        "snapshot_id": audit_row_id,
        "source_provider": "fwd009_source",
        "source_channel": "prepared_ingress",
        "source_time_utc": source_time_utc,
        "market_snapshot": {
            "spot_price": 100.0,
            "prior_close": 90.0,
            "nq_return_pct": 0.02,
            "vix_level": 22.5,
            "next_event_time_utc": source_time_utc + timedelta(minutes=45),
            "windows": [
                {
                    "event_id": "earnings",
                    "window_start_utc": source_time_utc + timedelta(minutes=10),
                    "window_end_utc": source_time_utc + timedelta(minutes=20),
                    "tags": [atlas_record_id],
                }
            ],
        },
        "options_surface": {
            "spot_price": 101.0,
            "front_dte": 1,
            "next_dte": 5,
        },
    }


def _prepared_snapshot(audit_row_id: str, atlas_record_id: str) -> PreparedRuntimeSnapshot:
    return prepare_runtime_dataset(
        load_api_payload(_bundle_payload(audit_row_id, atlas_record_id))
    ).primary_snapshot


def _snapshot_payload_for_row(audit_row_id: str, atlas_record_id: str) -> dict[str, object]:
    source_time_utc = _base_time()
    return {
        "atlas_record_id": atlas_record_id,
        "source_time_utc": source_time_utc,
        "runtime_feature_key": f"feature::{audit_row_id}",
        "front_dte": 2,
        "next_dte": 9,
        "market_spot_price": 100.0,
        "reference_close": 95.0,
        "windows": [
            {
                "event_id": audit_row_id,
                "window_start_utc": source_time_utc + timedelta(minutes=15),
                "window_end_utc": source_time_utc + timedelta(minutes=30),
                "tags": [atlas_record_id],
            }
        ],
        "next_event_time_utc": source_time_utc + timedelta(minutes=60),
        "row_specific_context": {
            "term_structure_spread": "front_premium",
            "skew_state": "balanced",
            "gamma_state": "neutral",
            "pin_state": "pin_risk_present",
            "dealer_pressure_state": "mixed",
            "temporal_state": "event_proximity_present",
        },
    }


def _imports_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def _defined_symbols(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.name for node in ast.walk(tree) if isinstance(node, (ast.ClassDef, ast.FunctionDef))
    }


@pytest.mark.parametrize(("audit_row_id", "atlas_record_id", "behaviour"), REOPENED_ROW_CASES)
def test_fwd009_reopened_rows_have_real_prepared_ingress_runtime_context_behaviour(
    audit_row_id: str, atlas_record_id: str, behaviour: str
) -> None:
    assert atlas_record_id

    if behaviour == "prepared_context_packet_trace_review":
        snapshot = _prepared_snapshot(audit_row_id, atlas_record_id)
        payload = build_prepared_context_payload(snapshot)
        fingerprint = fingerprint_prepared_context_payload(payload)
        assert len(fingerprint) == 64
        with pytest.raises(ValueError, match="canonical_prepared_envelope_required"):
            build_prepared_context_packet(
                packet_id=audit_row_id,
                snapshot=snapshot,
                emitted_at=datetime(2026, 5, 19, 10, 0, tzinfo=UTC),
                execution_context=DmpV3ExecutionContext(
                    traceid=f"trace::{audit_row_id}",
                    runid=f"run::{audit_row_id}",
                    scenarioid=f"scenario::{atlas_record_id}",
                ),
                module_version="fwd009-compatibility.1",
                module_instance_id="fwd009-compatibility-instance-1",
                parentids=[snapshot.snapshot_id or "snapshot:none"],
                reviewtraceid=f"review::{audit_row_id}",
            )
        return

    if behaviour == "provenance_lineage":
        snapshot = _prepared_snapshot(audit_row_id, atlas_record_id)
        assert snapshot.snapshot_id == audit_row_id
        assert snapshot.lineage.source_kind == "api_payload"
        assert snapshot.lineage.transport == "mapping"
        assert snapshot.lineage.source_snapshot_id == audit_row_id
        assert snapshot.lineage.source_sections == ("market_snapshot", "options_surface")
        assert snapshot.payload["source_provider"] == "fwd009_source"
        assert snapshot.payload["source_channel"] == "prepared_ingress"
        assert snapshot.payload["source_time_utc"] == _base_time()
        assert snapshot.payload["runtime_bar_time_utc"] == _base_time().replace(
            second=0, microsecond=0
        )
        return

    if behaviour == "repeated_snapshot_copy_safe":
        first = load_api_payload(_bundle_payload(audit_row_id + "::a", atlas_record_id))
        second = load_api_payload(_bundle_payload(audit_row_id + "::b", atlas_record_id))
        dataset = prepare_runtime_dataset([first, second])
        exported = dataset.snapshots[0].as_mapping()
        exported["windows"][0]["event_id"] = "mutated"
        assert [snapshot.snapshot_id for snapshot in dataset.snapshots] == [
            audit_row_id + "::a",
            audit_row_id + "::b",
        ]
        assert len(dataset.dataset_lineage) == 2
        assert dataset.snapshots[0].payload["windows"][0]["event_id"] == "earnings"
        return

    if behaviour == "real_data_bundle_preparation":
        dataset = prepare_runtime_dataset(_bundle_payload(audit_row_id, atlas_record_id))
        snapshot = dataset.primary_snapshot
        assert isinstance(dataset, PreparedRuntimeDataset)
        assert snapshot.payload["market_spot_price"] == 100.0
        assert snapshot.payload["options_spot_price"] == 101.0
        assert snapshot.payload["spot_price"] == 101.0
        assert snapshot.lineage.source_sections == ("market_snapshot", "options_surface")
        assert dataset.failed_enrichments == []
        assert dataset.missing_optional_enrichments == []
        return

    if behaviour == "normalised_feature_derivation":
        snapshot = _prepared_snapshot(audit_row_id, atlas_record_id)
        assert snapshot.derived_fields == {
            "front_to_next_dte_spread": 4,
            "has_windows": True,
            "minutes_to_next_event": 45,
            "nvda_return_pct": pytest.approx((100.0 - 90.0) / 90.0),
            "window_count": 1,
        }
        assert set(snapshot.lineage.derived_field_names) == set(snapshot.derived_fields)
        assert snapshot.failed_enrichments == []
        assert snapshot.missing_optional_enrichments == []
        return

    if behaviour == "prepared_runtime_dataset_contract":
        dataset = prepare_runtime_dataset(
            load_api_payload(_bundle_payload(audit_row_id, atlas_record_id))
        )
        assert dataclasses.is_dataclass(dataset)
        assert isinstance(dataset.primary_snapshot, PreparedRuntimeSnapshot)
        assert dataset.dataset_lineage == [dataset.primary_snapshot.lineage]
        assert dataset.primary_snapshot.runtime_bar_time_utc == _base_time().replace(
            second=0, microsecond=0
        )
        return

    if behaviour == "prepared_fixture_payload_copy_safe":
        source_payload = _snapshot_payload_for_row(audit_row_id, atlas_record_id)
        snapshot = prepare_runtime_snapshot(snapshot_id=audit_row_id, payload=source_payload)
        mapping = build_context_payload_mapping(snapshot)
        source_payload["row_specific_context"]["term_structure_spread"] = "mutated"  # type: ignore[index]
        mapping["payload"]["row_specific_context"]["term_structure_spread"] = "mutated-again"
        assert snapshot.payload["row_specific_context"]["term_structure_spread"] == "front_premium"
        assert (
            build_context_payload_mapping(snapshot)["payload"]["row_specific_context"][
                "term_structure_spread"
            ]
            == "front_premium"
        )
        return

    if behaviour == "native_lean_transform_boundary":
        for path in SELECTED_NATIVE_FILES:
            imports = _imports_for(path)
            assert not {
                module for module in imports if module.startswith(PROHIBITED_IMPORT_PREFIXES)
            }, path
        assert dataclasses.is_dataclass(PreparedRuntimeDataset)
        fields = set(get_type_hints(PreparedRuntimeDataset).keys())
        assert fields == {
            "snapshots",
            "dataset_lineage",
            "missing_optional_enrichments",
            "failed_enrichments",
        }
        assert fields.isdisjoint(PROHIBITED_DONOR_DATASET_FIELDS)
        defined_symbols: set[str] = set()
        for path in SELECTED_NATIVE_FILES:
            defined_symbols.update(_defined_symbols(path))
        assert defined_symbols.isdisjoint(PROHIBITED_DONOR_SYMBOLS)
        return

    if behaviour == "service_identity":
        service = RuntimePreparationService()
        snapshot = service.prepare(
            snapshot_id=audit_row_id,
            payload=_snapshot_payload_for_row(audit_row_id, atlas_record_id),
        )
        assert isinstance(snapshot, PreparedRuntimeSnapshot)
        assert snapshot.snapshot_id == audit_row_id
        assert snapshot.lineage.source_kind == "legacy_payload"
        assert snapshot.lineage.transport == "mapping"
        assert snapshot.lineage.source_sections == ("payload",)
        assert snapshot.payload["atlas_record_id"] == atlas_record_id
        return

    if behaviour == "service_snapshot_conversion":
        service = RuntimePreparationService()
        snapshot = service.prepare(
            raw_bundle=load_api_payload(_bundle_payload(audit_row_id, atlas_record_id))
        )
        assert snapshot.snapshot_id == audit_row_id
        assert snapshot.payload["front_to_next_dte_spread"] == 4
        assert snapshot.payload["window_count"] == 1
        assert snapshot.lineage.alignment_policy == "floor_minute_from_source_time_utc"
        return

    if behaviour == "service_dataset_conversion":
        service = RuntimePreparationService()
        dataset = service.prepare_dataset(
            [
                load_api_payload(_bundle_payload(audit_row_id + "::a", atlas_record_id)),
                _bundle_payload(audit_row_id + "::b", atlas_record_id),
            ]
        )
        assert [snapshot.snapshot_id for snapshot in dataset.snapshots] == [
            audit_row_id + "::a",
            audit_row_id + "::b",
        ]
        assert len(dataset.dataset_lineage) == 2
        assert dataset.failed_enrichments == []
        return

    if behaviour in {"options_flow_input_carriage", "market_regime_input_carriage"}:
        payload = _snapshot_payload_for_row(audit_row_id, atlas_record_id)
        if behaviour == "market_regime_input_carriage":
            payload["market_regime_context"] = {
                "breadth_state": "concentrated",
                "vol_of_vol_state": "elevated",
                "sector_leadership_state": "semis_led",
                "rates_regime_state": "restrictive",
                "fx_stress_state": "moderate",
            }
        else:
            payload["options_flow_context"] = {
                "term_structure_spread": "front_premium",
                "iv_vs_rv_curve_state": "front_rich",
                "pin_state": "pin_risk_present",
                "dealer_pressure_state": "mixed",
                "dominant_strike": 100,
            }
        snapshot = prepare_runtime_snapshot(snapshot_id=audit_row_id, payload=payload)
        assert snapshot.payload["atlas_record_id"] == atlas_record_id
        assert snapshot.payload["runtime_feature_key"] == f"feature::{audit_row_id}"
        assert snapshot.payload["front_to_next_dte_spread"] == 7
        assert snapshot.payload["minutes_to_next_event"] == 60
        assert snapshot.payload["window_count"] == 1
        assert snapshot.payload["has_windows"] is True
        assert snapshot.payload["nvda_return_pct"] == pytest.approx((100.0 - 95.0) / 95.0)
        assert (
            snapshot.as_mapping()["row_specific_context"]["temporal_state"]
            == "event_proximity_present"
        )
        return

    if behaviour == "temporal_event_context_preparation":
        payload = _snapshot_payload_for_row(audit_row_id, atlas_record_id)
        snapshot = prepare_runtime_snapshot(snapshot_id=audit_row_id, payload=payload)
        packet_payload = build_prepared_context_payload(snapshot)
        assert snapshot.payload["windows"][0]["event_id"] == audit_row_id
        assert snapshot.payload["windows"][0]["tags"] == [atlas_record_id]
        assert snapshot.payload["minutes_to_next_event"] == 60
        assert snapshot.payload["runtime_bar_time_utc"] == _base_time().replace(
            second=0, microsecond=0
        )
        assert packet_payload.source_time_utc == _base_time()
        assert packet_payload.runtime_bar_time_utc == _base_time().replace(second=0, microsecond=0)
        return

    raise AssertionError(f"Unhandled FWD-009 row behaviour: {behaviour}")
