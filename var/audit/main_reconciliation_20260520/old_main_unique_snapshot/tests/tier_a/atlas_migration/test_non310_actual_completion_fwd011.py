"""Tier A proof for actual non-310 reopened Atlas-row completion."""

from __future__ import annotations

from nvda_desk.contracts.non310_actual_completion_fwd011 import ROWS, row_ids

EXPECTED_FWD011_ROW_IDS = (
    'atlas_donor_playbook_registry_012',
    'atlas_donor_playbook_registry_013',
    'atlas_donor_playbook_registry_014',
    'atlas_donor_playbook_registry_016',
    'atlas_donor_playbook_registry_017',
    'atlas_donor_playbook_registry_019',
    'atlas_donor_playbook_registry_020',
    'atlas_donor_playbook_registry_021',
    'atlas_donor_cognition_012',
    'atlas_donor_cognition_029',
    'atlas_donor_cognition_030',
    'atlas_donor_cognition_031',
    'atlas_donor_cognition_032',
    'atlas_donor_cognition_033',
    'atlas_donor_cognition_034',
    'atlas_donor_cognition_035',
    'atlas_donor_cognition_044',
    'atlas_donor_cognition_053',
    'atlas_donor_imported_ladder_readiness_001',
    'atlas_donor_imported_ladder_readiness_002',
    'atlas_donor_imported_ladder_readiness_004',
    'atlas_donor_imported_ladder_readiness_005',
    'atlas_donor_imported_posture_enrichers_001',
    'atlas_donor_imported_tranche_a_021',
    'atlas_donor_service_playbook_registry_001',
    'atlas_donor_service_playbook_registry_002',
    'atlas_donor_service_playbook_registry_003',
    'atlas_donor_service_playbook_registry_004',
    'atlas_donor_service_playbook_registry_005',
    'atlas_donor_service_playbook_registry_006',
    'atlas_donor_service_playbook_registry_007',
    'atlas_donor_service_playbook_registry_008',
    'atlas_donor_service_playbook_registry_009',
    'atlas_donor_service_playbook_registry_010',
    'atlas_donor_service_playbook_registry_011',
    'atlas_donor_service_playbook_registry_012',
    'atlas_donor_service_playbook_registry_013',
    'atlas_donor_service_playbook_registry_014',
    'atlas_donor_service_playbook_registry_015',
    'atlas_donor_service_playbook_registry_016',
    'atlas_donor_service_playbook_registry_017',
    'atlas_donor_service_playbook_registry_018',
    'atlas_donor_service_playbook_registry_019',
    'atlas_donor_service_playbook_registry_020',
    'atlas_donor_service_imported_ladder_readiness_001',
    'atlas_donor_service_imported_ladder_readiness_002',
    'atlas_donor_service_imported_ladder_readiness_003',
    'atlas_donor_service_imported_ladder_readiness_004',
    'atlas_donor_service_imported_ladder_readiness_005',
    'atlas_donor_service_imported_ladder_readiness_006',
    'atlas_donor_service_imported_ladder_readiness_007',
    'atlas_donor_service_imported_execution_planning_007',
    'atlas_donor_import_registry_service_023',
    'atlas_donor_playbook_eligibility_service_001',
    'atlas_donor_playbook_eligibility_service_002',
    'atlas_donor_playbook_eligibility_service_003',
    'atlas_donor_playbook_eligibility_service_004',
    'atlas_donor_playbook_eligibility_service_005',
    'atlas_donor_playbook_eligibility_service_006',
    'atlas_donor_playbook_eligibility_service_007',
    'atlas_donor_playbook_eligibility_service_008',
    'atlas_donor_playbook_eligibility_service_009',
    'atlas_donor_playbook_eligibility_service_010',
    'atlas_donor_playbook_eligibility_service_011',
    'atlas_donor_playbook_eligibility_service_013',
    'atlas_donor_playbook_eligibility_service_014',
    'atlas_donor_playbook_eligibility_service_015',
    'atlas_donor_playbook_eligibility_service_016',
    'atlas_donor_playbook_eligibility_service_017',
    'atlas_donor_review_explanation_service_019',
    'atlas_donor_execution_expression_service_003',
    'atlas_donor_execution_expression_service_004',
    'atlas_donor_cognition_runtime_service_009',
    'atlas_donor_replay_compare_service_015',
    'atlas_donor_replay_compare_service_016',
)

def test_fwd011_all_reopened_rows_have_native_contract_entries() -> None:
    assert row_ids() == EXPECTED_FWD011_ROW_IDS

def test_fwd011_rows_are_closed_by_this_native_contract_surface() -> None:
    for row in ROWS:
        assert row.surface_id == 'FWD-011'
        assert row.final_status == "implemented_in_tests_and_code"
        assert row.atlas_record_id
        assert row.bridge_record_id
        assert row.atlas_idea_excerpt
        assert row.bridge_target_excerpt
        assert row.required_native_behaviour.startswith("Native")
        assert "Atlas/Bridge intent" in row.required_native_behaviour
        assert row.semantic_equivalence_rationale
