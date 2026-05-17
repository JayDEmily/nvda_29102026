# FWD-002/FWD-003/FWD-005 implementation receipt

Status: `bounded_closed_current`

Branch: `worker/fwd-002-003-005-implementation`

Scope: implement the next pass requested by the user: FWD-002, FWD-003, and FWD-005 only.

## Clause scope

| Forward leaf | Owner surface | Clauses | Proof block |
|---|---|---:|---|
| FWD-002 | Testing, proof, and checkpoint surfaces | 68 | `fwd002_testing_proof_replay_sidecar_surface` |
| FWD-003 | Persistence, ledgers, and receipts | 54 | `fwd003_import_registry_durable_persistence_surface` |
| FWD-005 | External source interfaces and API ingress | 30 | `fwd005_api_internal_exposure_surface` |
| **Total** |  | **152** |  |

## Native implementation summary

FWD-002 reintroduced the replay/evaluation laboratory ideas as bounded native harnesses and sidecar services, not donor-code transplants.

FWD-003 reintroduced canonical import-registry and durable SQLite persistence ideas as native schema/service/storage seams.

FWD-005 reintroduced API ingress/exposure ideas as bounded `HttpApp` methods and dependency providers for existing live internal mechanisms.

## Evidence files

- Clause closeout: `intent_migration/partial_clause_rebuild_programme_001/fwd_002_003_005_rebuild_pass/FWD_002_003_005_CLAUSE_CLOSEOUT_152.csv`
- Test-first failure receipt: `intent_migration/partial_clause_rebuild_programme_001/fwd_002_003_005_rebuild_pass/FWD_002_003_005_TEST_FIRST_FAILURE_RECEIPT.md`
- Proof summary: `intent_migration/partial_clause_rebuild_programme_001/fwd_002_003_005_rebuild_pass/FWD_002_003_005_PROOF_SUMMARY.md`
- Read/touch manifest: `intent_migration/partial_clause_rebuild_programme_001/fwd_002_003_005_rebuild_pass/FWD_002_003_005_READ_AND_TOUCH_MANIFEST.csv`

## Important limitation

`config/proof_blocks.yaml` was updated for the three new proof blocks. `config/retained_test_registry.yaml` was not mutated in final state; a broad retained-registry rewrite was ruled out in this pass because it created vocabulary-audit noise from pre-existing registry wording.

## Next gate

FWD-007 — Raw signal families. FWD-007 is not opened by this receipt.
