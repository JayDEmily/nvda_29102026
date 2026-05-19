# FWD-009 baseline reopened row set

Created UTC: 2026-05-19T09:32:02.862560+00:00

Source CSV path: `var/audit/non310_completion_claim_audit_20260519/FWD009_ROW_AUDIT.csv`

Total rows in FWD009_ROW_AUDIT.csv: `51`

Rows already accepted as existing satisfaction: `2`

- FWD009-AUDIT-004: atlas_donor_dataset_007
- FWD009-AUDIT-027: atlas_donor_options_flow_context_006

Rows reopened as unsupported_worker_claim: `49`

- FWD009-AUDIT-001: atlas_donor_trace_review_003
- FWD009-AUDIT-002: atlas_donor_dataset_002
- FWD009-AUDIT-003: atlas_donor_dataset_005
- FWD009-AUDIT-005: atlas_donor_dataset_008
- FWD009-AUDIT-006: atlas_donor_dataset_009
- FWD009-AUDIT-007: atlas_donor_dataset_011
- FWD009-AUDIT-008: atlas_donor_dataset_015
- FWD009-AUDIT-009: atlas_donor_dataset_018
- FWD009-AUDIT-010: atlas_donor_dataset_020
- FWD009-AUDIT-011: atlas_donor_dataset_022
- FWD009-AUDIT-012: atlas_donor_service_chain_to_cognition_002
- FWD009-AUDIT-013: atlas_donor_service_chain_to_cognition_005
- FWD009-AUDIT-014: atlas_donor_service_chain_to_cognition_007
- FWD009-AUDIT-015: atlas_donor_service_market_regime_context_001
- FWD009-AUDIT-016: atlas_donor_service_market_regime_context_005
- FWD009-AUDIT-017: atlas_donor_service_market_regime_context_006
- FWD009-AUDIT-018: atlas_donor_service_market_regime_context_007
- FWD009-AUDIT-019: atlas_donor_service_market_regime_context_008
- FWD009-AUDIT-020: atlas_donor_service_market_regime_context_009
- FWD009-AUDIT-021: atlas_donor_service_market_regime_context_010
- FWD009-AUDIT-022: atlas_donor_options_flow_context_001
- FWD009-AUDIT-023: atlas_donor_options_flow_context_002
- FWD009-AUDIT-024: atlas_donor_options_flow_context_003
- FWD009-AUDIT-025: atlas_donor_options_flow_context_004
- FWD009-AUDIT-026: atlas_donor_options_flow_context_005
- FWD009-AUDIT-028: atlas_donor_options_flow_context_008
- FWD009-AUDIT-029: atlas_donor_options_flow_context_009
- FWD009-AUDIT-030: atlas_donor_options_flow_context_010
- FWD009-AUDIT-031: atlas_donor_options_flow_context_011
- FWD009-AUDIT-032: atlas_donor_options_flow_context_012
- FWD009-AUDIT-033: atlas_donor_options_flow_context_013
- FWD009-AUDIT-034: atlas_donor_options_flow_context_014
- FWD009-AUDIT-035: atlas_donor_options_flow_context_015
- FWD009-AUDIT-036: atlas_donor_options_flow_context_017
- FWD009-AUDIT-037: atlas_donor_options_flow_context_018
- FWD009-AUDIT-038: atlas_donor_temporal_context_001
- FWD009-AUDIT-039: atlas_donor_temporal_context_002
- FWD009-AUDIT-040: atlas_donor_temporal_context_003
- FWD009-AUDIT-041: atlas_donor_temporal_context_004
- FWD009-AUDIT-042: atlas_donor_temporal_context_005
- FWD009-AUDIT-043: atlas_donor_temporal_context_009
- FWD009-AUDIT-044: atlas_donor_temporal_context_010
- FWD009-AUDIT-045: atlas_donor_temporal_context_011
- FWD009-AUDIT-046: atlas_donor_temporal_context_013
- FWD009-AUDIT-047: atlas_donor_temporal_context_014
- FWD009-AUDIT-048: atlas_donor_temporal_context_015
- FWD009-AUDIT-049: atlas_donor_temporal_context_016
- FWD009-AUDIT-050: atlas_donor_temporal_context_017
- FWD009-AUDIT-051: atlas_donor_temporal_context_019

Only the 49 reopened `unsupported_worker_claim` rows are in scope for this repair pass.
The two rows already marked `already_satisfied_by_existing_tests_and_code` are not reimplemented.
