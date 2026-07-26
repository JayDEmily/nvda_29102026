# M13 State Kernel — Independent Proof Review V7

## Disposition

`IMPLEMENTATION_REPAIR_OPEN`

The V7 worker proposal is independently accepted as sufficient proof of the bounded N-06 instance-owned active-attempt exclusion requirement. It preserves the complete V6 family, adds positive two-instance independence proof, and rejects process-, module-, class- and scope-global guard false positives without introducing thread-safety, durability, distributed-transaction or external-effect authority.

Only `M13-IMPLEMENT-REPAIR-V1` is open. M13 completion, merge, M01 and every later module remain closed pending independent review of the repaired production implementation.

## Source verification

- Supplied archive: `NVDA_M13_PROOF_REPAIR_V7_aded5ed_20260726.tar(3).gz`.
- Archive SHA-256: `1eb29baac7b0e3253c499957d50b85fce1e1440ec43da26b1dc2a6a335bd4d72`.
- Worker branch/commit/worktree: `proof/m13-state-kernel-repair-v7` / `aded5edc1ad567a1f7d3a4231b918b3af1abd7bd` / clean.
- Accepted parent: `cf44a74385536672237de4747d084faaa7971b47`.
- Changed semantic paths: one M13 proof test and the M13 proof record only; all remaining additions are worker-owned M13 evidence.
- `src/**`, normative documents, proof configuration, retained-test configuration and later modules: unchanged.

## Independent proof validation

| Check | Result |
|---|---|
| Frozen V6 functions | PASS — 24/24 function ASTs unchanged |
| Frozen V6 cases | PASS — 131/131 retained exactly once |
| V7 additions | PASS — two functions and 21 separately collected cases |
| Proof-only conforming reference | PASS — 152/152 |
| Frozen rejected implementation | EXPECTED RED — 44 failed, 108 passed |
| V7-specific rejected-implementation effect | PASS — one additional intentional failure; 20 positive distinct-instance cases pass |
| PM module-global guard | Frozen V6 false positive reproduced; V7 rejects it |
| V7 guard mutants | PASS — 8/8 independently rejected by designated semantic cases |
| V6 retained mutants | Worker evidence integrity verified; prior PM acceptance remains controlling |
| All prior M13 mutants | Worker evidence integrity verified; no regression recorded |
| Proof blocks | PASS — 52 |
| Proof executor | PASS — 21 |
| Non-M13 persistence Tier A | PASS — 36 |
| Checkpoint shadow | PASS — 2 |
| Worker evidence integrity | PASS — 484 tracked evidence hashes verified |

## Semantic judgement

The 20-case matrix exercises two distinct `InMemoryUnitOfWork` instances across owner mutation, participant prepare, participant commit, receipt-writer-equivalent participation and observable rollback. It covers the four required command/consistency-unit relationships and all required success/failure combinations at programme level. Each instance's state, version, sequence, receipt, participant state, idempotency truth, correction and replay are observed independently.

The integration case simultaneously establishes that a nested call on active instance A is rejected while an unrelated call on instance B commits. This closes the measured V6 false positive without weakening same-instance exclusion.

The eight V7 mutants are materially distinct and truthful:

1. module-global flag;
2. class-global/static flag;
3. one universal process marker;
4. guard keyed only by command type;
5. guard keyed only by consistency-unit ID;
6. guard keyed only by command type plus consistency-unit ID;
7. guard shared by every instance of one concrete class; and
8. early guard release before participant commit with global coupling.

The first seven pass the frozen V6 family and fail the V7 proof because a separate instance is falsely blocked. The eighth remains rejected by V6 and by the V7 simultaneous integration case. No rejection relies on interface mismatch or an unrelated broken success path.

## Bounded tooling caveat

The worker preservation helper hardcodes `.venv/bin/python`; the supplied Git archive does not contain that virtual environment. The helper therefore is not self-contained in an arbitrary fresh environment. This is not a proof defect because the underlying AST and collected-case preservation was independently recomputed with the available interpreter and passed. Future checkpoint tooling should use the invoking interpreter or an explicitly provisioned environment.

## Gate result

`M13-PROOF-REPAIR-V7` is accepted.

Open only `M13-IMPLEMENT-REPAIR-V1` under the frozen 152-case family. The implementation repair must:

- install one active-attempt guard per `InMemoryUnitOfWork` instance before any callback or duplicate/version resolution capable of re-entry;
- reject same-instance nested `execute()` calls throughout the entire attempt;
- clear the guard in a `finally` path after every success or failure while never releasing it before participant commit/rollback completion;
- keep distinct `UnitOfWork` instances independently executable;
- make `AtomicReceipt` command type and consistency-unit identity agree with its embedded `IdempotencyKey`;
- require exact integer prior/resulting versions and sequence, excluding booleans, floats, strings and coercible numerics;
- preserve all previously accepted transaction, rollback, idempotency, replay, detached-copy and non-durable behaviour.

The worker may modify only the bounded M13 production package and worker-owned implementation evidence. Tests, normative authority, proof/retained configuration, unrelated source and later modules remain frozen. Final M13 acceptance remains an independent Project Manager decision.
