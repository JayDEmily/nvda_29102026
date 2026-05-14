# ROADMAP_LIVE_POSITION_INVENTORY_5_13_BRANCH_001_RECEIPT

Date: 2026-05-09
Branch: `work/roadmap-ledger-tranche-control-20260509`
Target: `5.13 Live position and inventory architecture`
Authority: user instruction `proceed` after `NEXT_AUTHORITY_OPENING_BRIEF_001` recommended opening row 5.13.

## Scope opened

Bounded read/write state and repository invariant hardening only:

- live-inventory contract models;
- repo-native position/capital state readbacks;
- declared-exposure-only inventory summary;
- explicit inventory receipt write through `ReceiptLedger` only when a receipt id is supplied;
- Tier A downstream/persistence tests;
- proof block, Makefile check, retained-test registry notes, working-doc overlays, and roadmap ledger update.

## Scope closed

- broker placement;
- order execution;
- new candidate formation;
- raw signal preparation;
- capital deployment sizing;
- ungoverned capital mutation;
- dependency files;
- original Atlas/Bridge JSON;
- generated Atlas slices;
- historical receipts.

## Files materially changed

- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`
- `src/nvda_desk/contracts/downstream.py`
- `src/nvda_desk/downstream/live_inventory.py`
- `src/nvda_desk/domain/downstream/live_inventory.py`
- `src/nvda_desk/repositories/position_repository.py`
- `src/nvda_desk/repositories/capital_state_repository.py`
- `tests/tier_a/downstream_runtime/test_downstream_contract_models.py`
- `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py`
- `tests/tier_a/persistence/test_position_repository_surface.py`
- `tests/tier_a/persistence/test_capital_state_repository_surface.py`
- `config/proof_blocks.yaml`
- `config/retained_test_registry.yaml`
- `Makefile`
- `ROADMAP_LEDGER.md`

## Proof log

| Proof | Status | Evidence path | Result |
|---|---:|---|---|
| Baseline I1 targeted pytest | 0 | `var/audit/roadmap_live_inventory_5_13/logs/baseline_i1_pytest.*` | `7 passed` |
| Targeted I1 pytest after mutation | 0 | `var/audit/roadmap_live_inventory_5_13/logs/targeted_i1_pytest_final.*` | `15 passed` |
| Broad downstream/persistence/capital pytest | 0 | `var/audit/roadmap_live_inventory_5_13/logs/broad_downstream_persistence_capital_pytest.*` | `44 passed` |
| Proof-block manifest check-all | 0 | `var/audit/roadmap_live_inventory_5_13/logs/proof_check_all_final.*`; `var/audit/roadmap_live_inventory_5_13/proof_blocks_check_all_receipt.json` | `PASS count=9` |
| Proof-block manifest check-all after ledger update | 0 | `var/audit/roadmap_live_inventory_5_13/logs/proof_check_all_post_ledger.*`; `var/audit/roadmap_live_inventory_5_13/proof_blocks_check_all_receipt_post_ledger.json` | `PASS count=9` |
| Makefile static gate | 0 | `var/audit/roadmap_live_inventory_5_13/logs/make_live_inventory_check_final.*` | `live position/inventory architecture surfaces present` |
| Named proof block | 0 | `var/audit/roadmap_live_inventory_5_13/logs/proof_block_live_inventory_final.*` | `15 passed` |
| Ruff touched Python | 0 | `var/audit/roadmap_live_inventory_5_13/logs/ruff_touched_final.*` | `All checks passed!` |
| Black check touched Python | 0 | `var/audit/roadmap_live_inventory_5_13/logs/black_check_touched_final.*` | `9 files would be left unchanged` |
| Git diff whitespace check | 0 | `var/audit/roadmap_live_inventory_5_13/logs/git_diff_check.*` | no output |
| Full pytest attempt | 1 | `var/audit/roadmap_live_inventory_5_13/logs/full_pytest.*` | `322 passed`, `1 failed`: vocabulary synonym escalation from planning docs |
| Cache cleanup | 0 | `var/audit/roadmap_live_inventory_5_13/logs/clean_caches.*`; `post_clean_cache_inventory.txt` | 0 repo-local cache artefacts after cleanup |

## Full-suite caveat

The full pytest attempt was not green. The failure was `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py::test_vocabulary_synonym_candidate_audit_writes_escalation_artefact_when_touched`, which generated unresolved synonym candidates from planning documents created before this 5.13 branch. This branch did not mutate canonical vocabulary files and restored `var/vocabulary/synonym_candidates.json` after the diagnostic run so no generated vocabulary artefact is committed.

## Boundary conclusion

The branch proves a bounded live-inventory/state readback surface only. It does not prove capital deployment, opening placement, broker execution, exit/close, or full runtime trading behaviour.
