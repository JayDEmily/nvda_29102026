"""Tier A proof for actual non-310 reopened Atlas-row completion."""

from __future__ import annotations

from nvda_desk.contracts.non310_actual_completion_fwd009 import ROWS, row_ids

EXPECTED_FWD009_ROW_IDS = (
    'atlas_donor_trace_review_003',
    'atlas_donor_dataset_002',
    'atlas_donor_dataset_005',
    'atlas_donor_dataset_008',
    'atlas_donor_dataset_009',
    'atlas_donor_dataset_011',
    'atlas_donor_dataset_015',
    'atlas_donor_dataset_018',
    'atlas_donor_dataset_020',
    'atlas_donor_dataset_022',
    'atlas_donor_service_chain_to_cognition_002',
    'atlas_donor_service_chain_to_cognition_005',
    'atlas_donor_service_chain_to_cognition_007',
    'atlas_donor_service_market_regime_context_001',
    'atlas_donor_service_market_regime_context_005',
    'atlas_donor_service_market_regime_context_006',
    'atlas_donor_service_market_regime_context_007',
    'atlas_donor_service_market_regime_context_008',
    'atlas_donor_service_market_regime_context_009',
    'atlas_donor_service_market_regime_context_010',
    'atlas_donor_options_flow_context_001',
    'atlas_donor_options_flow_context_002',
    'atlas_donor_options_flow_context_003',
    'atlas_donor_options_flow_context_004',
    'atlas_donor_options_flow_context_005',
    'atlas_donor_options_flow_context_008',
    'atlas_donor_options_flow_context_009',
    'atlas_donor_options_flow_context_010',
    'atlas_donor_options_flow_context_011',
    'atlas_donor_options_flow_context_012',
    'atlas_donor_options_flow_context_013',
    'atlas_donor_options_flow_context_014',
    'atlas_donor_options_flow_context_015',
    'atlas_donor_options_flow_context_017',
    'atlas_donor_options_flow_context_018',
    'atlas_donor_temporal_context_001',
    'atlas_donor_temporal_context_002',
    'atlas_donor_temporal_context_003',
    'atlas_donor_temporal_context_004',
    'atlas_donor_temporal_context_005',
    'atlas_donor_temporal_context_009',
    'atlas_donor_temporal_context_010',
    'atlas_donor_temporal_context_011',
    'atlas_donor_temporal_context_013',
    'atlas_donor_temporal_context_014',
    'atlas_donor_temporal_context_015',
    'atlas_donor_temporal_context_016',
    'atlas_donor_temporal_context_017',
    'atlas_donor_temporal_context_019',
)

def test_fwd009_all_reopened_rows_have_native_contract_entries() -> None:
    assert row_ids() == EXPECTED_FWD009_ROW_IDS

def test_fwd009_rows_are_closed_by_this_native_contract_surface() -> None:
    for row in ROWS:
        assert row.surface_id == 'FWD-009'
        assert row.final_status == "implemented_in_tests_and_code"
        assert row.atlas_record_id
        assert row.bridge_record_id
        assert row.atlas_idea_excerpt
        assert row.bridge_target_excerpt
        assert row.required_native_behaviour.startswith("Native")
        assert "Atlas/Bridge intent" in row.required_native_behaviour
        assert row.semantic_equivalence_rationale
