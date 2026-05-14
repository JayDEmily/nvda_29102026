# ROADMAP_DOWNSTREAM_CAPITAL_DEPLOYMENT_5_11_BRANCH_001 receipt

## Status

`acted_on_bounded`

## User authority

User instruction: `proceed Next gate: 5.11 Downstream capital deployment authority`.

Opened row: `5.11 Downstream capital deployment authority`.

## Scope

Opened only for bounded fresh-capital decision contract hardening.

## Boundaries held closed

- broker placement
- order execution
- opening placement mechanics
- candidate formation
- serial-stage decisions
- parallel-risk generation
- live external API/network clients
- dependency files
- original Atlas/Bridge JSON
- generated Atlas slices
- historical receipts

## Files changed

- `ROADMAP_LEDGER.md`
- `Makefile`
- `config/proof_blocks.yaml`
- `config/retained_test_registry.yaml`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`
- `src/nvda_desk/contracts/capital.py`
- `src/nvda_desk/capital/authority.py`
- `src/nvda_desk/domain/capital/deployment.py`
- `src/nvda_desk/services/capital_deployment_service.py`
- `tests/tier_a/capital_deployment/test_capital_authority_service_surface.py`
- `tests/tier_a/capital_deployment/test_capital_contract_models.py`
- `tests/tier_a/capital_deployment/test_sequence9_capital_deployment_decision_surface.py`
- `tests/tier_a/capital_deployment/test_sequence9_capital_deployment_dmp_packet.py`
- `var/audit/roadmap_capital_deployment_5_11/*`

## Behaviour hardened

- Capital input model now requires explicit trace tokens for serial candidate material, downstream pre-deployment truth, final-risk receipt, capital-state snapshot, and bounded deployment policy.
- Optional parallel-risk packet identity is preserved when present.
- Downstream pre-deployment block truth dominates deployment sizing.
- Capital decisions carry consumed-input trace metadata and optional capital-deployment receipt ID.
- Capital-deployment receipt construction records the emitted output while keeping placement authority closed.

## Proof log

| Proof | Status | Log |
|---|---:|---|
| baseline capital deployment pytest | `0`; `16 passed` | `logs/baseline_capital_deployment_pytest.stdout` |
| targeted capital deployment pytest | `0`; `21 passed` | `logs/targeted_capital_deployment_pytest.stdout` |
| broad capital/downstream/persistence pytest | `0`; `35 passed` | `logs/broad_capital_downstream_pytest.stdout` |
| proof blocks check-all | `0`; `PASS count=10` | `logs/proof_blocks_check_all.stdout`; receipt `proof_blocks_check_all_receipt.json` |
| make capital-deployment-check | `0` | `logs/make_capital_deployment_check.stdout` |
| proof block `downstream_capital_deployment_authority_surface` | `0`; `21 passed` | `logs/make_proof_block_capital.stdout` |
| py_compile touched Python | `0` | `logs/py_compile.stdout` |
| ruff touched Python | `0` | `logs/ruff_touched.stdout` |
| black --check touched Python | `0` | `logs/black_check_touched.stdout` |
| git diff --check | `0` | `logs/git_diff_check.stdout`; final `logs/final_git_diff_check.stdout` |
| clean-caches | `0`; `0` repo-local cache artefacts remaining outside `.venv` | `logs/clean_caches.stdout`; `logs/post_cleanup_cache_paths.txt` |
| full pytest | `1`; `381 passed`, `1 failed` | `logs/full_pytest.stdout`; failure is vocabulary synonym escalation |

## Full pytest caveat

Full pytest was attempted. It did not pass because `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py::test_vocabulary_synonym_candidate_audit_writes_escalation_artefact_when_touched` failed after generating a vocabulary synonym escalation artefact. The generated `var/vocabulary/synonym_candidates.json` change was reverted and was not committed.

## Ledger result

- `roadmap_downstream_capital_deployment_authority` is now `acted_on_bounded`.
- Current pointer is `USER_AUTHORITY_DECISION_REQUIRED`.
- Recommended next opening is `5.8 Parallel risk lane`, only if explicitly authorised.
