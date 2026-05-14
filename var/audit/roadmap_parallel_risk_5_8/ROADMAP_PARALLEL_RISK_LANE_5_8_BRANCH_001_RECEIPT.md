# ROADMAP_PARALLEL_RISK_LANE_5_8_BRANCH_001 receipt

## Branch

- Branch ID: `ROADMAP_PARALLEL_RISK_LANE_5_8_BRANCH_001`
- Architecture row: `5.8 Parallel risk lane`
- Tranche ID: `roadmap_parallel_risk_lane`
- User authority: `I open it. continue working`
- Completion claim limit: bounded independent risk-envelope authority hardening only.

## Inspected authority/read set

- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
- Parallel-risk source, tests, proof-block manifest, retained-test registry, and Makefile surfaces touched in this branch.

## Boundary

Opened:

- bounded 5.8 independent parallel-risk lane authority hardening.

Closed:

- broker placement;
- order execution;
- opening mechanics;
- capital deployment sizing beyond already recorded 5.11 input consumption;
- candidate formation;
- serial-stage decision mutation;
- coefficient/modifier policy;
- review/explanation authority;
- dependency files;
- live API/network clients;
- original Atlas/Bridge JSON;
- generated Atlas slices;
- historical receipts.

## Files changed

- `src/nvda_desk/contracts/parallel_risk.py`
- `src/nvda_desk/risk/parallel/evaluate.py`
- `src/nvda_desk/persistence/parallel_risk_observations.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_contract_models.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py`
- `tests/tier_a/persistence/test_parallel_risk_observation_store_surface.py`
- `config/proof_blocks.yaml`
- `config/retained_test_registry.yaml`
  - Note: this branch also relocated the prior 5.11 `capital_deployment_traceability_hardening` registry row from an invalid root-level append into the existing `retained_seed_tier_a` list so the retained-test registry parses as YAML.
- `Makefile`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`
- `ROADMAP_LEDGER.md`
- `var/audit/roadmap_parallel_risk_5_8/*`

## Behavioural proof points

- `ParallelRiskInputTrace` records bootstrap input packet, bootstrap source, admitted semantic inputs, parent/dependency packet IDs, and selected serial temporal packet IDs.
- Hidden capital/placement/review/coefficient authority keys in packet extensions are rejected before evaluation.
- Parallel-risk envelope hard blocks require `block` envelope state.
- Extreme VIX produces a `block` risk envelope without becoming capital sizing or placement authority.
- Parallel-risk observation persistence rejects duplicate `observation_id` values and remains write-only to callers.

## Proof log

| Proof | Status | Log path |
|---|---:|---|
| Baseline parallel-risk pytest before mutation | 0 | `logs/baseline_parallel_risk_pytest.stdout` |
| Targeted parallel-risk pytest after mutation | 0 | `logs/targeted_parallel_risk_pytest_after_format.stdout` |
| Broad risk/capital/downstream pytest | 0 | `logs/broad_risk_capital_downstream_pytest.stdout` |
| Proof-block manifest check-all | 0 | `logs/proof_blocks_check_all_after_registry_fix.stdout` |
| YAML parse: proof-block and retained-test registry | 0 | `logs/yaml_parse_surfaces_final.stdout` |
| `make parallel-risk-check` | 0 | `logs/make_parallel_risk_check_post_yaml.stdout` |
| `make proof-block BLOCK=parallel_risk_lane_authority_surface` | 0 | `logs/make_proof_block_parallel_risk_final.stdout` |
| Py compile touched Python | 0 | `logs/py_compile_touched.stdout` |
| Ruff touched Python | 0 | `logs/ruff_touched_python_after_format.stdout` |
| Black check touched Python | 0 | `logs/black_check_touched_python_after_format.stdout` |
| `git diff --check` | 0 | `logs/git_diff_check_after_retained_eof_fix.stdout` |
| Cache cleanup | 0 | `logs/make_clean_caches.stdout` |

Key observed results:

```text
baseline parallel-risk proof: 23 passed
targeted parallel-risk proof after mutation: 30 passed
broad risk/capital/downstream proof: 57 passed
proof_blocks --check-all: PASS count=11
proof block/retained-test YAML parse: ok
proof block parallel_risk_lane_authority_surface: 30 passed
ruff touched Python: All checks passed
black touched Python: 7 files would be left unchanged
git diff --check: 0
cache cleanup: 0 repo-local cache artefacts remaining
```

## Full-suite note

Full pytest was attempted and did not pass:

```text
333 passed, 1 failed
```

The failing test was the pre-existing vocabulary synonym escalation gate:

```text
tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py::test_vocabulary_synonym_candidate_audit_writes_escalation_artefact_when_touched
```

The generated `var/vocabulary/synonym_candidates.json` change was reverted and was not committed.

## Next pointer

`ROADMAP_LEDGER.md` now points to `USER_AUTHORITY_DECISION_REQUIRED`. The recommended next opening is `5.4 Financial and event calendar architecture` only if the user explicitly opens market/calendar runtime authority.
