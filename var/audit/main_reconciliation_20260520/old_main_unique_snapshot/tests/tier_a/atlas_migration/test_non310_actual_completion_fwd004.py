"""Tier A proof for actual non-310 reopened Atlas-row completion."""

from __future__ import annotations

from nvda_desk.contracts.non310_actual_completion_fwd004 import ROWS, row_ids

EXPECTED_FWD004_ROW_IDS = (
    'atlas_donor_dmp_envelope_001',
    'atlas_donor_dmp_envelope_002',
    'atlas_donor_dmp_envelope_003',
    'atlas_donor_dmp_envelope_004',
    'atlas_donor_dmp_envelope_005',
    'atlas_donor_dmp_envelope_006',
    'atlas_donor_dmp_envelope_007',
    'atlas_donor_dmp_envelope_008',
    'atlas_donor_dmp_envelope_009',
    'atlas_donor_dmp_envelope_010',
    'atlas_donor_dmp_001',
    'atlas_donor_dmp_002',
    'atlas_donor_dmp_003',
    'atlas_donor_dmp_004',
    'atlas_donor_dmp_005',
    'atlas_donor_dmp_006',
    'atlas_donor_dmp_007',
    'atlas_donor_dmp_008',
    'atlas_donor_dmp_009',
    'atlas_donor_dmp_010',
    'atlas_donor_dmp_011',
    'atlas_donor_dmp_012',
    'atlas_donor_dmp_013',
    'atlas_donor_dmp_014',
    'atlas_donor_dmp_015',
    'atlas_donor_dmp_016',
    'atlas_donor_dmp_017',
    'atlas_donor_dmp_018',
    'atlas_donor_temporal_surface_010',
    'atlas_donor_parallel_risk_001',
    'atlas_donor_cognition_014',
    'atlas_donor_cognition_022',
    'atlas_donor_cognition_028',
    'atlas_donor_domain_temporal_state_008',
    'atlas_donor_config_models_019',
    'atlas_donor_config_models_022',
    'atlas_donor_config_models_024',
    'atlas_donor_config_models_027',
    'atlas_donor_config_models_029',
    'atlas_donor_config_models_031',
    'atlas_donor_service_financial_calendar_reference_001',
    'atlas_donor_service_carry_handoff_004',
    'atlas_donor_service_carry_handoff_005',
    'atlas_donor_service_carry_market_004',
    'atlas_donor_service_review_packets_002',
    'atlas_donor_service_review_packets_003',
    'atlas_donor_service_review_packets_004',
    'atlas_donor_service_review_packets_005',
    'atlas_donor_service_review_packets_006',
    'atlas_donor_service_review_packets_007',
    'atlas_donor_service_review_packets_008',
    'atlas_donor_service_review_packets_009',
    'atlas_donor_service_review_packets_010',
    'atlas_donor_service_review_packets_011',
    'atlas_donor_service_review_packets_012',
    'atlas_donor_service_review_packets_013',
    'atlas_donor_service_review_packets_014',
    'atlas_donor_posture_risk_003',
    'atlas_donor_cognition_runtime_service_011',
)

def test_fwd004_all_reopened_rows_have_native_contract_entries() -> None:
    assert row_ids() == EXPECTED_FWD004_ROW_IDS

def test_fwd004_rows_are_closed_by_this_native_contract_surface() -> None:
    for row in ROWS:
        assert row.surface_id == 'FWD-004'
        assert row.final_status == "implemented_in_tests_and_code"
        assert row.atlas_record_id
        assert row.bridge_record_id
        assert row.atlas_idea_excerpt
        assert row.bridge_target_excerpt
        assert row.required_native_behaviour.startswith("Native")
        assert "Atlas/Bridge intent" in row.required_native_behaviour
        assert row.semantic_equivalence_rationale
