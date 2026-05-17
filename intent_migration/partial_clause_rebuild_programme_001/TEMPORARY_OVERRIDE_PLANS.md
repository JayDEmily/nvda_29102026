# Temporary override PLANS — partial-clause rebuild programme 001

Status: `active_interstitial_plan_planning_only`

Scope: `intent_migration/partial_clause_rebuild_programme_001`

This file is a temporary override plan for the missing-behaviour rebuild programme. It does **not** replace or mutate repo-root `PLANS.md`. Repo-root `AGENTS.md` and `PLANS.md` remain frozen standing control surfaces. Mutable current state remains in `ROADMAP_LEDGER.md`.

## 1. Controlling premise

All missing ideas isolated by the Atlas-intent adjudication are required inputs to the rebuild programme. The programme must reintroduce the ideas natively, not transplant donor-era code shape.

A missing clause may close only as one of:

1. `already_native_equivalent_found` — full read finds the behaviour already alive in another native form, with evidence;
2. `native_delta_required` — the missing behaviour must be added or exposed natively;
3. `native_delta_required_with_vocabulary_admission` — behaviour is required and introduces durable terms that must pass vocabulary admission before tests/code persist those terms;
4. `blocked_by_authority_conflict` — required but cannot proceed until the conflict is recorded and resolved.

`optional_reject` is not an allowed final state for the 310-clause backlog.

## 2. Frozen-surface rule

Do not edit:

- repo-root `PLANS.md`;
- repo-root `AGENTS.md`;
- route `AGENTS.override.md` files except by an explicit bounded governance-control leaf.

Allowed mutable planning surfaces for this interstitial pass:

- `ROADMAP_LEDGER.md`;
- files under `intent_migration/partial_clause_rebuild_programme_001/`.

No runtime/source/test/config/fixture/vocabulary-data mutation is opened by this temporary plan.

## 3. Mandatory read gate before each owner-service leaf

Before a service leaf may write or amend tests, the worker must create a current leaf read manifest and read in full:

1. `AGENTS.md`;
2. repo-root `PLANS.md` as frozen input;
3. `ROADMAP_LEDGER.md` current pointer;
4. applicable `AGENTS.override.md` route files;
5. numbered control/normative stack routed by `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
6. vocabulary governance docs and registry;
7. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` for owner-service placement;
8. `tests/AGENTS.override.md` before touching tests;
9. `docs/08_TESTING_AND_PROMOTION_CORE.md` and `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`;
10. `config/retained_test_registry.yaml`;
11. `config/proof_blocks.yaml`;
12. relevant existing tests for the owner surface;
13. directly impacted source files after tests are planned, before source mutation;
14. docstrings on impacted owned runtime surfaces, only as lowest-authority explanatory surfaces.

The read manifest recorded for this interstitial plan is:

- `INTERSTITIAL_READ_MANIFEST_GOVERNANCE_TEST_VOCABULARY.csv`
- `INTERSTITIAL_READ_MANIFEST_GOVERNANCE_TEST_VOCABULARY.md`
- `INTERSTITIAL_TEST_TREE_STRUCTURE.txt`

## 4. Vocabulary/admission gate

Before any new durable term enters tests, fixtures, proof labels, manifests, receipts, docs, schemas, or code:

1. compare the candidate term against `data/vocabulary/canonical_vocabulary.json` and `docs/vocabulary/vocabulary_registry.md`;
2. classify it exactly as `enrich_existing`, `add_new`, `alias_only`, or `quarantine`;
3. if admitted, update the generator-backed canonical path in the same bounded gate;
4. run the vocabulary proof obligations named by `config/proof_blocks.yaml`;
5. do not use a proof artefact as a back door for unadmitted vocabulary.

Proof blocks identified during this read gate. The first three are vocabulary/admission proof blocks; later rows are owner-surface proof blocks that future leaves must select only when their owned paths are touched:

| Proof block | Tier | Lifecycle | Owned paths |
|---|---|---|---:|
| `vocabulary_governance_conformance_candidate` | Tier A | admitted_for_vocab_repair_gate | 14 |
| `vocabulary_synonym_audit_clean_check` | Tier A | admitted_for_atlas_feature_admission_014 | 5 |
| `vocabulary_candidate_review_clean_check` | Tier A | admitted_for_atlas_feature_admission_025 | 4 |
| `proof_executor_contract` | Tier B | admitted_for_roadmap_5_17_proof_checkpoint_hardening | 6 |
| `checkpoint_receipt_contract` | Tier B | admitted_for_active_code_atlas_testing_proof_checkpoint_surface | 6 |
| `persistence_ledgers_receipts_surface` | Tier A | admitted_for_roadmap_5_16_persistence_ledger_receipt_hardening | 23 |
| `persistence_session_boundary_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_005 | 7 |
| `module_registry_repository_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_006 | 6 |
| `support_spine_prepared_packet_review_surface` | Tier A | admitted_for_roadmap_support_spine_5h_branch_001 | 20 |
| `raw_signal_contract_copy_boundary_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_017 | 7 |
| `raw_signal_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_018 | 10 |
| `raw_capture_source_temporal_law_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_013 | 8 |
| `raw_capture_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_015 | 10 |
| `source_temporal_standard_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_014 | 7 |
| `dmpv3_extension_canonical_leaf_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_008 | 8 |
| `dmpv3_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_009 | 10 |
| `serial_desk_cognition_spine_surface` | Tier A | admitted_for_roadmap_serial_spine_5h_branch_001 | 14 |
| `serial_desk_cognition_spine_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_row032_serial_transform_boundary | 13 |
| `roadmap_external_source_api_ingress_authority_surface` | Tier A | admitted_for_roadmap_external_ingress_authority_readiness_5h_branch_001 | 12 |
| `external_source_contract_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_011 | 8 |
| `external_source_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_012 | 11 |
| `live_position_inventory_architecture_surface` | Tier A | admitted_for_roadmap_live_position_inventory_5_13_branch_001 | 15 |
| `live_position_inventory_authority_boundary_surface` | Tier A | admitted_for_active_code_atlas_row036_live_inventory_authority_boundary | 10 |
| `live_position_inventory_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_row037_live_inventory_transform_boundary | 10 |
| `downstream_capital_deployment_authority_surface` | Tier A | admitted_for_roadmap_downstream_capital_deployment_5_11_branch_001 | 14 |
| `downstream_capital_deployment_transform_boundary_surface` | Tier B | admitted_for_active_code_atlas_row039_downstream_capital_transform_boundary | 9 |
| `parallel_risk_lane_authority_surface` | Tier A | admitted_for_roadmap_parallel_risk_lane_5_8_branch_001 | 12 |
| `parallel_risk_lane_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_row034_parallel_risk_transform_boundary | 9 |
| `financial_event_calendar_authority_surface` | Tier A | admitted_for_roadmap_next_three_gates_5_4_5_9_5_12_branch_001 | 10 |
| `financial_event_calendar_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_020 | 10 |
| `dynamic_coefficient_modifier_authority_surface` | Tier A | admitted_for_roadmap_next_three_gates_5_4_5_9_5_12_branch_001 | 11 |
| `modifier_contract_authority_boundaries_surface` | Tier A | admitted_for_active_code_atlas_row_028_dynamic_coefficient_modifier_authority_new_test_family | 6 |
| `dynamic_modifier_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_row_029_dynamic_coefficient_modifier_authority_transform_required | 12 |
| `opening_placement_readiness_surface` | Tier A | admitted_for_roadmap_next_three_gates_5_4_5_9_5_12_branch_001 | 12 |
| `opening_authority_boundary_surface` | Tier A | admitted_for_active_code_atlas_row041_opening_authority_boundary | 8 |
| `opening_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_row042_opening_transform_boundary | 9 |
| `playbook_library_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_row044_playbook_transform_boundary | 6 |
| `playbook_library_architecture_surface` | Tier A | admitted_for_roadmap_playbook_library_5_10_branch_001 | 14 |
| `exit_close_architecture_surface` | Tier A | admitted_for_roadmap_exit_close_5_14_branch_001 | 11 |
| `exit_close_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_row043_exit_close_transform_boundary | 8 |
| `tier_a_remaining_coverage_inventory` | Tier A | admitted_for_test_false_positive_resistance_tier_a_coverage_reconciliation | 30 |
| `tier_b_retained_coverage_reconciliation` | Tier B | admitted_for_test_false_positive_resistance_final_closeout_amendment | 14 |
| `prepared_runtime_snapshot_contract_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_022 | 5 |
| `prepared_runtime_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_023 | 7 |
| `review_contract_authority_boundaries_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_025 | 5 |
| `review_transform_boundary_surface` | Tier A | admitted_for_active_code_atlas_test_first_execution_026 | 7 |

## 5. Tier A/B/C test interpretation

Tier status is not determined by folder name alone.

- Tier A is blocking only when admitted by current live doctrine, proof block, retained-test registry, or active bounded-pack receipt.
- Tier B is bounded shadow proof and non-blocking unless promoted by live doctrine.
- Tier C is historical/observational/non-blocking unless promoted by live doctrine.

A future leaf that touches tests must update the required receipt surfaces and, where tier status changes, reconcile `config/retained_test_registry.yaml` and `config/proof_blocks.yaml`.

## 6. Owner-service queue

The owner-service allocation from Phase 2 remains the execution queue. Each row is a leaf family, not permission to batch source changes.

| Forward ID | Row | Owner surface | Total clauses | Partial deltas | Confirmed deleted | Primary review groups |
|---|---|---|---:|---:|---:|---|
| `FWD-001` | 5.18 | Vocabulary governance interface | 1 | 1 | 0 | Vocabulary document strict-extra-field enforcement |
| `FWD-002` | 5.17 | Testing, proof, and checkpoint surfaces | 68 | 12 | 56 | Legacy fixture corpus loaders and row parsers; Research notes, promotion decisions, and evaluation sidecar APIs; SLV replay, walk-forward, fragility, horizon, and experiment harness |
| `FWD-003` | 5.16 | Persistence, ledgers, and receipts | 54 | 3 | 51 | Canonical import registry schema, service, reports, and backlog views; Durable SQL/ORM persistence, DB factory, and seed data |
| `FWD-005` | 5.1 | External source interfaces and API ingress | 30 | 27 | 3 | API exposure for live internal mechanisms; Authority/veto and block-event API surfaces |
| `FWD-007` | 5.3 | Raw signal families | 56 | 24 | 32 | Rich raw market substrate and signal service surfaces; Strategic ladder signal family and SLV market scoring |
| `FWD-008` | 5.4 | Financial and event calendar architecture | 11 | 11 | 0 | Runtime financial/event calendar authority and proximity queries |
| `FWD-010` | 5.9 | Dynamic coefficient and modifier authority | 12 | 12 | 0 | Dynamic coefficient calibration, audit packets, and active replay harness |
| `FWD-013` | 5.8 | Parallel risk lane | 8 | 5 | 3 | Parallel risk candidate enrichment, consequence/fragility classes, and risk event APIs |
| `FWD-015` | 5.12 | Opening architecture and placement readiness | 13 | 11 | 2 | Broker execution lifecycle, account state, and typed order domain |
| `FWD-016` | 5.13 | Live position and inventory architecture | 2 | 0 | 2 | Daily PnL reporting surface |
| `FWD-017` | 5.14 | Exit and close architecture | 25 | 5 | 20 | Overnight carry market/replay and exit-continuation machinery |
| `FWD-018` | 5.15 | Review and explanation layer | 30 | 9 | 21 | Review packet daily health, module health, rendering, and reporting; SLV replay, walk-forward, fragility, horizon, and experiment harness |

## 7. Per-clause execution rule

For each clause in the selected owner-service leaf:

1. restate the Atlas-origin idea in plain English;
2. identify the survived native part, if any, and mark it as a duplication guard;
3. perform vocabulary/admission check for durable wording;
4. read normative owner documents and existing tests;
5. decide whether a native equivalent already exists under different wording;
6. if equivalent exists, close as `already_native_equivalent_found` with file/line evidence and no code mutation;
7. if a native delta is required, write or amend tests first;
8. prove the test fails for the right reason where feasible;
9. only then amend or add native code;
10. run targeted tests, relevant proof block(s), registry/proof validation, `git diff --check`, and `git status --short`;
11. update receipt and ledger before moving to the next clause or leaf.

## 8. Anti-duplication rule

Never rebuild a legacy row directly. Rebuild only the missing native behaviour delta.

Each implementation packet must state:

- existing native behaviour to preserve;
- missing behaviour to add;
- owning surface;
- dependency surfaces;
- terms admitted/reused/quarantined;
- test files added/amended;
- source files added/amended;
- proof blocks and retained-registry entries affected;
- evidence that the change did not duplicate an existing live mechanism.

## 9. Implementation boundary

This temporary plan does not implement the backlog. It sets the rules for the next implementation leaves.

Implementation may start only after an owner-service leaf has completed its read gate, vocabulary gate, and test-first design gate.

## 10. Next executable gate

Next gate: `INTERSTITIAL_OWNER_SERVICE_LEAF_001`.

Default first owner-service leaf: `FWD-001 — Vocabulary governance interface`, because all later durable naming, test labels, proof labels, and receipts depend on vocabulary/admission discipline.

If current live authority selects another owner surface, that selection must be recorded in `ROADMAP_LEDGER.md` before test/source mutation.
