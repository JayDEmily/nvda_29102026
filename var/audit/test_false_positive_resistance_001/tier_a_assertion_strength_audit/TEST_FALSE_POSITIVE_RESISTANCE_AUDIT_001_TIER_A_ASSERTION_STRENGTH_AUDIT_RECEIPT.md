# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 Tier A assertion-strength audit
## Scope
- Physical Tier A pytest files under `tests/tier_a/`.
- Gate: `TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001_TIER_A_REMAINING_ASSERTION_STRENGTH_AUDIT`.
- This report classifies assertion shape only. It does not prove runtime correctness or full false-positive resistance.

## Summary
- Tier A pytest files: `95`
- Tier A test functions: `381`
- `smoke-only`: `38`
- `strong behavioural assertion`: `337`
- `weak assertion`: `6`
- Files needing follow-up: `41`
- Files provisionally assertion-strong by this audit: `54`

## Classification rule
- `strong behavioural assertion`: explicit comparison/boundary assertion and/or `pytest.raises` path exists. Still requires known-bad and mutation/fault evidence before trust promotion.
- `weak assertion`: assertion appears limited to truthiness, presence, type, or file existence.
- `smoke-only`: no direct `assert`/`pytest.raises`; relies on import/attribute helper failures or non-crash.
- `dangerous false-positive risk`: no observable assertion path found.

## Follow-up required
Every `smoke-only`, `weak assertion`, `harness-only`, or `dangerous false-positive risk` row must be treated as not trusted until a later gate adds known-bad specimens and, where needed, amends the test.

### Weak/smoke rows
| File | Line | Test | Classification | Reason |
|---|---:|---|---|---|
| `tests/tier_a/adapters_egress/test_broker_boundary_surface.py` | 34 | `test_broker_boundary_remains_protocol_only_without_concrete_adapters` | `weak assertion` | Assertion path appears limited to truthiness/presence/type/file existence. |
| `tests/tier_a/adapters_ingress/test_external_source_interface_boundary.py` | 101 | `test_current_ingress_adapters_do_not_import_concrete_network_clients` | `weak assertion` | Assertion path appears limited to truthiness/presence/type/file existence. |
| `tests/tier_a/analysis/test_replay_evaluation_surface.py` | 43 | `test_replay_evaluation_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/api/test_api_dto_boundary_surface.py` | 21 | `test_api_dto_boundary_surface_is_present` | `weak assertion` | Assertion path appears limited to truthiness/presence/type/file existence. |
| `tests/tier_a/calendar_operational/test_calendar_operational_surface.py` | 22 | `test_calendar_operational_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py` | 21 | `test_calendar_reference_import_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py` | 29 | `test_calendar_reference_projection_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py` | 38 | `test_calendar_reference_crosswalk_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/capital_deployment/test_capital_authority_service_surface.py` | 39 | `test_capital_authority_service_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/capital_deployment/test_capital_deployment_fresh_capital_correction.py` | 21 | `test_capital_authority_depends_on_final_join_surfaces` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/capital_deployment/test_capital_downstream_placement_boundary.py` | 15 | `test_capital_authority_is_downstream_not_a_serial_stage_module` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/config/test_config_authority_surface.py` | 21 | `test_config_home_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/downstream_runtime/test_downstream_contract_models.py` | 30 | `test_downstream_contract_models_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py` | 28 | `test_downstream_live_inventory_service_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/downstream_runtime/test_downstream_opening_service_surface.py` | 21 | `test_downstream_opening_service_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/downstream_runtime/test_downstream_review_stage_service_surface.py` | 21 | `test_downstream_review_stage_service_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/downstream_runtime/test_downstream_state_reader_service_surface.py` | 21 | `test_downstream_state_reader_service_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/entry/test_entry_boundary_surface.py` | 21 | `test_entry_boundary_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/ingress/test_raw_bundle_loader_surface.py` | 22 | `test_raw_bundle_loader_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/migrations/test_migration_lifecycle_surface.py` | 22 | `test_migration_lifecycle_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/modifiers/test_state_conditioned_modifier_surface.py` | 47 | `test_modifier_home_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/options_flow_history/test_options_flow_contract_models.py` | 21 | `test_options_flow_contract_models_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/options_flow_history/test_options_flow_history_persistence_surface.py` | 22 | `test_options_flow_history_persistence_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/options_flow_history/test_options_flow_history_replay_live_state_separation.py` | 15 | `test_options_flow_history_replay_stays_separate_from_live_trade_state` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/options_flow_history/test_options_flow_history_replay_surface.py` | 22 | `test_options_flow_history_replay_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/options_flow_history/test_options_flow_history_runtime_authority_separation.py` | 15 | `test_options_flow_history_repository_is_separate_from_runtime_authority` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/options_flow_history/test_options_flow_history_trade_state_separation.py` | 15 | `test_options_flow_history_repository_is_separate_from_trade_state_repositories` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/parallel_risk/test_parallel_risk_dmp_fixture_root.py` | 8 | `test_dmp_v3_fixture_root_is_present_for_parallel_risk_shell_proofs` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/persistence/test_execution_records_repository_surface.py` | 22 | `test_execution_records_repository_exposes_no_keyed_overwrite_method` | `weak assertion` | Assertion path appears limited to truthiness/presence/type/file existence. |
| `tests/tier_a/persistence/test_parallel_risk_observation_store_surface.py` | 70 | `test_parallel_risk_observation_store_exposes_no_public_readback_surface` | `weak assertion` | Assertion path appears limited to truthiness/presence/type/file existence. |
| `tests/tier_a/reference_data/test_reference_data_contract.py` | 22 | `test_reference_data_contract_exports_required_models` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/reference_data/test_reference_data_contract.py` | 36 | `test_reference_data_contract_models_are_dataclasses` | `weak assertion` | Assertion path appears limited to truthiness/presence/type/file existence. |
| `tests/tier_a/review_runtime/test_review_explanation_service_surface.py` | 29 | `test_review_explanation_service_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/review_runtime/test_review_stage_surface.py` | 21 | `test_review_stage_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/runtime/test_runtime_orchestrator_surface.py` | 27 | `test_runtime_orchestrator_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/seam_boundaries/test_prepared_ingress_checkpoint_surface.py` | 21 | `test_checkpoint_helper_surface_is_present_for_prepared_ingress_boundaries` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/serial_recommendation/test_execution_contract_models.py` | 22 | `test_execution_contract_models_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/serial_recommendation/test_execution_service_surface.py` | 21 | `test_execution_service_and_domain_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py` | 22 | `test_canonical_runtime_specimen_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py` | 24 | `test_cognition_ingress_mapping_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py` | 26 | `test_cognition_ingress_translation_coordinator_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py` | 24 | `test_preparation_runtime_substrate_surface_is_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/upstream_cognition/test_regime_contract_models.py` | 21 | `test_regime_contract_models_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |
| `tests/tier_a/upstream_cognition/test_regime_ingress_surface.py` | 21 | `test_regime_ingress_mapper_and_service_surfaces_are_present` | `smoke-only` | No direct assert/pytest.raises path; relies on helper import/attribute failure or non-crash. |

## Artefacts
- `tier_a_assertion_strength_summary.json`
- `tier_a_assertion_strength_rows.json`
- `tier_a_assertion_strength_rows.tsv`
- `tier_a_assertion_strength_file_summary.json`
- `tier_a_assertion_strength_file_summary.tsv`
