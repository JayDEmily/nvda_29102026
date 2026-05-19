from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pytest

from nvda_desk.contracts.temporal import (
    SourceTemporalStandard,
    TemporalContextInput,
    TemporalEventWindow,
    build_source_temporal_payload,
)
from nvda_desk.contracts.upstream_signal import RawUpstreamSignalInput
from nvda_desk.ingress.raw_bundle_loader import RawBundleLoader
from nvda_desk.upstream.raw_signal_ingress import ingest_raw_upstream_signal


REPO_ROOT = Path(__file__).resolve().parents[3]
RAW_CAPTURE_SOURCE_PATHS = (
    Path("src/nvda_desk/contracts/temporal.py"),
    Path("src/nvda_desk/ingress/raw_bundle_loader.py"),
    Path("src/nvda_desk/contracts/upstream_signal.py"),
    Path("src/nvda_desk/upstream/raw_signal_ingress.py"),
)
DONOR_RUNTIME_TOKENS = (
    "sqlalchemy",
    "create_engine",
    "SessionLocal",
    "DatabaseManager",
    "seed_database",
    "backfill",
    "broker_order",
)
PROHIBITED_OWNER_IMPORTS = (
    "nvda_desk.cognition",
    "nvda_desk.downstream",
    "nvda_desk.risk",
    "nvda_desk.services",
    "nvda_desk.runtime",
)

REOPENED_ROW_CASES = (
    ("FWD006-AUDIT-001", "atlas_donor_module_006", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-002", "atlas_donor_module_009", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-003", "atlas_donor_options_004", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-004", "atlas_donor_replay_002", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-005", "atlas_donor_replay_003", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-006", "atlas_donor_research_003", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-007", "atlas_donor_session_clock_001", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-008", "atlas_donor_session_clock_002", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-009", "atlas_donor_session_clock_003", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-010", "atlas_donor_session_clock_004", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-011", "atlas_donor_session_clock_005", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-012", "atlas_donor_session_clock_006", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-013", "atlas_donor_session_clock_007", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-014", "atlas_donor_session_clock_008", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-015", "atlas_donor_session_clock_009", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-016", "atlas_donor_session_clock_010", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-017", "atlas_donor_risk_009", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-018", "atlas_donor_risk_011", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-019", "atlas_donor_options_flow_history_005", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-020", "atlas_donor_options_flow_history_006", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-021", "atlas_donor_options_flow_history_007", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-022", "atlas_donor_temporal_surface_001", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-023", "atlas_donor_temporal_surface_002", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-024", "atlas_donor_temporal_surface_003", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-025", "atlas_donor_temporal_surface_004", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-026", "atlas_donor_temporal_surface_005", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-027", "atlas_donor_temporal_surface_006", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-028", "atlas_donor_temporal_surface_007", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-029", "atlas_donor_temporal_surface_008", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-030", "atlas_donor_temporal_surface_011", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-031", "atlas_donor_overnight_008", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-032", "atlas_donor_overnight_009", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-033", "atlas_donor_overnight_012", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-034", "atlas_donor_overnight_013", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-035", "atlas_donor_eval_006", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-036", "atlas_donor_eval_009", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-037", "atlas_donor_eval_011", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-038", "atlas_donor_eval_018", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-039", "atlas_donor_eval_021", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-040", "atlas_donor_execution_records_005", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-041", "atlas_donor_execution_records_008", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-042", "atlas_donor_execution_records_011", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-043", "atlas_donor_execution_records_016", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-044", "atlas_donor_execution_records_018", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-045", "atlas_donor_execution_records_020", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-046", "atlas_donor_market_010", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-047", "atlas_donor_market_013", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-048", "atlas_donor_market_015", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-049", "atlas_donor_market_017", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-050", "atlas_donor_market_019", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-051", "atlas_donor_slv_016", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-052", "atlas_donor_slv_017", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-053", "atlas_donor_review_008", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-054", "atlas_donor_parallel_risk_004", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-055", "atlas_donor_dataset_003", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-056", "atlas_donor_dataset_004", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-057", "atlas_donor_dataset_006", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-058", "atlas_donor_dataset_010", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-059", "atlas_donor_dataset_012", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-060", "atlas_donor_dataset_016", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-061", "atlas_donor_dataset_019", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-062", "atlas_donor_events_015", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-063", "atlas_donor_events_039", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-064", "atlas_donor_calibration_009", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-065", "atlas_donor_domain_session_clock_001", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-066", "atlas_donor_domain_session_clock_002", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-067", "atlas_donor_domain_session_clock_005", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-068", "atlas_donor_domain_temporal_state_001", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-069", "atlas_donor_domain_temporal_state_003", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-070", "atlas_donor_domain_temporal_state_005", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-071", "atlas_donor_domain_temporal_state_006", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-072", "atlas_donor_domain_temporal_state_007", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-073", "atlas_donor_domain_temporal_state_009", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-074", "atlas_donor_domain_temporal_state_010", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-075", "atlas_donor_domain_temporal_state_011", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-076", "atlas_donor_domain_temporal_state_012", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-077", "atlas_donor_domain_temporal_state_013", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-078", "atlas_donor_domain_temporal_state_014", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-079", "atlas_donor_domain_temporal_state_015", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-080", "atlas_donor_domain_temporal_state_016", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-081", "atlas_donor_domain_temporal_state_017", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-082", "atlas_donor_db_models_003", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-083", "atlas_donor_db_models_005", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-084", "atlas_donor_db_models_007", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-085", "atlas_donor_db_models_009", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-086", "atlas_donor_db_models_012", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-087", "atlas_donor_db_models_013", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-088", "atlas_donor_db_models_018", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-089", "atlas_donor_db_models_019", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-090", "atlas_donor_db_models_020", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-091", "atlas_donor_db_models_021", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-092", "atlas_donor_db_seed_012", "transform_boundary_no_donor_runtime"),
    ("FWD006-AUDIT-093", "atlas_donor_service_carry_handoff_002", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-094", "atlas_donor_service_carry_replay_006", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-095", "atlas_donor_service_carry_replay_009", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-096", "atlas_donor_service_options_flow_history_006", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-097", "atlas_donor_service_market_state_003", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-098", "atlas_donor_service_market_state_004", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-099", "atlas_donor_service_market_state_006", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-100", "atlas_donor_service_market_state_012", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-101", "atlas_donor_service_market_state_016", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-102", "atlas_donor_options_flow_context_016", "raw_bundle_provenance_preservation"),
    ("FWD006-AUDIT-103", "atlas_donor_temporal_context_006", "temporal_event_window_and_source_standard"),
    ("FWD006-AUDIT-104", "atlas_donor_slv_experiments_002", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-105", "atlas_donor_slv_experiments_005", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-106", "atlas_donor_slv_experiments_011", "replay_date_level_source_truth"),
    ("FWD006-AUDIT-107", "atlas_donor_cognition_runtime_service_012", "upstream_trace_only_non_interference"),
    ("FWD006-AUDIT-108", "atlas_donor_cognition_runtime_service_014", "upstream_trace_only_non_interference")
)


@pytest.mark.parametrize(("audit_row_id", "atlas_record_id", "behaviour"), REOPENED_ROW_CASES)
def test_fwd006_reopened_rows_have_real_raw_capture_source_temporal_behaviour(
    audit_row_id: str, atlas_record_id: str, behaviour: str
) -> None:
    assert atlas_record_id
    source_time = datetime(2026, 5, 19, 9, 31, 45)
    source_day = date(2026, 5, 19)

    if behaviour == "raw_bundle_provenance_preservation":
        bundle = RawBundleLoader().load_api_payload(
            {
                "snapshot_id": audit_row_id,
                "source_provider": "fwd006_source",
                "source_channel": "api_payload",
                "market_snapshot": {
                    "source_time_utc": source_time,
                    "spot_price": 100.0,
                    "atlas_record_id": atlas_record_id,
                },
                "options_surface": {"spot_price": 101.0, "front_dte": 1, "next_dte": 5},
            }
        )
        assert bundle.snapshot_id == audit_row_id
        assert bundle.provenance.source_kind == "api_payload"
        assert bundle.provenance.transport == "mapping"
        assert bundle.provenance.source_time_utc == source_time
        assert bundle.provenance.source_provider == "fwd006_source"
        assert bundle.provenance.source_channel == "api_payload"
        assert bundle.market_snapshot["atlas_record_id"] == atlas_record_id
        assert bundle.options_surface == {"spot_price": 101.0, "front_dte": 1, "next_dte": 5}
        return

    if behaviour == "replay_date_level_source_truth":
        bundle = RawBundleLoader().load_json_bundle(
            {
                "snapshot_id": audit_row_id,
                "source_date": source_day,
                "source_time_kind": "date",
                "source_provider": "replay_fixture",
                "market_snapshot": {"atlas_record_id": atlas_record_id, "close": 100.0},
            }
        )
        assert bundle.provenance.source_kind == "json_bundle"
        assert bundle.provenance.source_date == source_day
        assert bundle.provenance.source_time_utc is None
        assert bundle.provenance.source_time_kind == "date"
        assert bundle.provenance.source_provider == "replay_fixture"
        assert bundle.market_snapshot["atlas_record_id"] == atlas_record_id
        return

    if behaviour == "temporal_event_window_and_source_standard":
        carrier = SourceTemporalStandard(
            source_time_raw="2026-05-19T09:31:45-04:00",
            source_time_kind="timestamp",
            source_timezone_raw="America/New_York",
            source_time_utc=source_time,
            captured_at_utc=datetime(2026, 5, 19, 9, 32),
            persisted_at_utc=datetime(2026, 5, 19, 9, 33),
            source_provider="calendar_fixture",
            source_channel="source_temporal_law",
            time_granularity="timestamp",
        )
        window = TemporalEventWindow(
            event_id=audit_row_id,
            window_start_utc=source_time,
            window_end_utc=datetime(2026, 5, 19, 10, 0),
            tags=[atlas_record_id],
        )
        context = TemporalContextInput.model_validate(
            {**carrier.model_dump(), "windows": [window.model_dump()]}
        )
        assert context.source_time_utc == source_time
        assert context.source_date is None
        assert context.windows[0].event_id == audit_row_id
        assert context.windows[0].tags == [atlas_record_id]
        assert build_source_temporal_payload(source_date=source_day)["time_granularity"] == "date"
        with pytest.raises(ValueError, match="source temporal standard requires"):
            SourceTemporalStandard(captured_at_utc=source_time, persisted_at_utc=source_time)
        return

    if behaviour == "upstream_trace_only_non_interference":
        dataset_packet_payload = {"existing": {"retained": True}}
        source_id = "source::" + audit_row_id
        raw_signal = RawUpstreamSignalInput(
            source_id=source_id,
            signal_family_id="admitted_fwd006_family",
            scope_id="raw_capture",
            payload={
                "atlas_record_id": atlas_record_id,
                "nested": {"position_size": 10, "safe_feature": "retained"},
                "trade_allowed": True,
            },
        )
        result = ingest_raw_upstream_signal(
            raw_signal=raw_signal,
            dataset_packet_payload=dataset_packet_payload,
            admitted_signal_families={"admitted_fwd006_family"},
        )
        dataset_packet_payload["existing"]["retained"] = False
        assert result.dataset_packet_payload == {"existing": {"retained": True}}
        assert result.sanity_trace.disposition == "admitted_trace_only"
        assert result.trace_envelope["source_id"] == source_id
        assert result.trace_envelope["payload"] == {
            "atlas_record_id": atlas_record_id,
            "nested": {"safe_feature": "retained"},
        }
        assert result.trade_decision_side_effects == []

        rejected = ingest_raw_upstream_signal(
            raw_signal=RawUpstreamSignalInput(
                source_id=source_id + "::rejected",
                signal_family_id="unadmitted_family",
                scope_id="raw_capture",
                payload={"atlas_record_id": atlas_record_id},
            ),
            dataset_packet_payload={"existing": True},
            admitted_signal_families={"admitted_fwd006_family"},
        )
        assert rejected.quarantined is True
        assert rejected.sanity_trace.disposition == "rejected_quarantined"
        assert rejected.sanity_trace.rejection_reason == "signal_family_not_admitted"
        assert rejected.trace_envelope == {}
        return

    if behaviour == "transform_boundary_no_donor_runtime":
        for path in RAW_CAPTURE_SOURCE_PATHS:
            text = (REPO_ROOT / path).read_text(encoding="utf-8")
            for token in DONOR_RUNTIME_TOKENS:
                assert token not in text, f"{path} leaks donor/runtime token {token!r}"
            for owner_import in PROHIBITED_OWNER_IMPORTS:
                assert owner_import not in text, f"{path} imports prohibited owner {owner_import!r}"
        with pytest.raises(ValueError, match="source temporal standard requires"):
            RawBundleLoader().load_api_payload(
                {
                    "snapshot_id": audit_row_id,
                    "captured_at_utc": source_time,
                    "persisted_at_utc": source_time,
                    "market_snapshot": {"atlas_record_id": atlas_record_id},
                }
            )
        return

    raise AssertionError(f"Unhandled FWD-006 reopened row behaviour: {behaviour}")
