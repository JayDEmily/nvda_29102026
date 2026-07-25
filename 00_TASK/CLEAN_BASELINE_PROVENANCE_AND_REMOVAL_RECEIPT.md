# Clean Baseline Provenance and Removal Receipt

Date: 22 July 2026  
Purpose: identify exactly what the clean-worker tarball preserves and excludes.

## Source material

| Source | SHA-256 | Use |
|---|---|---|
| Corrected PM-001–PM-010 snapshot | `e18b0643aaec536bd9f22b3eb080efa891c3603f15c1bbd40f218b1bda82b077` | complete repository base |
| Complete fourth-reopen P2 candidate | `1e6ae44439c5249cb04ed10b8abe4773b9bb97e843cc76545cd48b7dc97b6ca3` | PM-011 directory only |
| Newly attached truncated `(3).gz` copy | `0ae8030fdf5179602e24656083336ae36c80dbd43073d04c3d29732db1060699` | rejected as input; gzip integrity failed |

The source archives were not mutated or deleted.

## Preserved

- complete Git repository and history from the corrected P1 snapshot;
- branch `work/NVIDIA_2026_pm001_pm010_restart_20260721`;
- HEAD `21c1e5eccfbb818bdd422afd42117f23b1f74f26`;
- the nine accepted P1 tracked-file changes relative to HEAD;
- complete PM-001–PM-010 evidence;
- complete PM-011 mechanical census and receipt;
- all 166 Tier A and 13 Tier B physical Python tests at their PM-011 baseline bytes; and
- wider repository content unrelated to rejected P2 work.

Every physical test file was recomputed against `PM-011/P2_PHYSICAL_TEST_CENSUS.tsv`: 179 present, 179 hash matches, zero missing and zero mismatches.

## Excluded from the clean worker input

The following material from the rejected fourth-reopen candidate was not copied:

1. all PM-012–PM-020 directories and files;
2. all prior P2 relationship registers, adjudication prose and traceability tables;
3. first, second, third and fourth reopen manifests and self-review artefacts;
4. PM-019 aggregate registers, semantic self-review and count projections;
5. PM-020 validators, probes, raw runs, receipts, “final” metadata and archive manifests;
6. candidate changes to `Makefile`, `config/proof_blocks.yaml`, `config/retained_test_registry.yaml` and the wider canonical programme ExecPlan;
7. candidate changes to these eight tests:
   - `tests/tier_a/adapters_egress/test_broker_boundary_surface.py`;
   - `tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py`;
   - `tests/tier_a/parallel_risk/test_fwd013_parallel_risk_candidate_enrichment_contract.py`;
   - `tests/tier_a/vocabulary/test_parallel_risk_lane_vocabulary_terms.py`;
   - `tests/tier_a/vocabulary/test_vocabulary_candidate_schema_contracts.py`;
   - `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py`;
   - `tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py`;
   - `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py`;
8. `.pytest_cache`, `__pycache__` directories and compiled `.pyc` files; and
9. nested input archives and wrapper snapshot metadata from the P1 transport package.

## Added control material

- `00_TASK/NVDA_P2_CLEAN_WORKER_SEMANTIC_REVIEW_EXEC_PLAN_20260722.md`;
- `00_TASK/PROJECT_EXECUTION_METHOD.md`;
- this receipt;
- `project_control/canonical_project_manager/P2_ABSOLUTE_SEMANTIC_READ_LEDGER.tsv`, initialised with 179 `NO` rows; and
- an updated `ROADMAP_LEDGER_V2.md` activating the bounded clean-worker plan.

## Claim boundary

This cleanup establishes provenance, corpus identity and absence of prior P2 semantic material. It does not establish that P2 is correct, complete or accepted.
