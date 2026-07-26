# M13 State Kernel — Independent Proof Review V6

## Disposition

`CLOSED:M13_PROOF_REPAIR_V7_REQUIRED_FOR_INSTANCE_SCOPED_ACTIVE_ATTEMPT_EXCLUSION`

The worker's V6 proof repair is substantial and valid for the behaviours it exercises. It preserves the prior 46 cases, adds 85 auditable cases, passes the proof-only conforming reference 131/131, rejects the 16 declared V6 mutants and truthfully leaves the rejected implementation expected-red at 43 failures / 88 passes.

It is not sufficient for independent acceptance because it proves only that nested execution is rejected on the same active `UnitOfWork`. It does not prove that active-attempt exclusion is owned by that instance rather than by a process-global or class-global guard.

## Source verification

- Supplied archive: `NVDA_M13_PROOF_REPAIR_V6_d01f758_20260726.tar(1).gz`.
- Archive SHA-256: `37f54c1d4581b2a30bc7770b4a55cc9acde81832bb98ba2935ad6e8bade5f93a`.
- Worker branch/commit/worktree: `proof/m13-state-kernel-repair-v6` / `d01f75813260cae46597ed9d258ee68efb4b6508` / clean.
- Accepted parent: `92c30ef0f1894e8265242b8a0f229daea7ebb603`.
- Worker changed paths: one M13 proof test, the M13 proof record and worker-owned M13 evidence only.
- `src/**`, normative documents, proof configuration, retained-test configuration and later modules: unchanged.

## Positive validation independently reproduced

| Check | Result |
|---|---|
| Frozen pre-V6 functions | PASS — 15/15 function ASTs unchanged; nine V6 functions added |
| Collection | PASS — 131 cases |
| Rejected implementation | EXPECTED RED — 43 failed, 88 passed; original 46 remain green |
| Proof-only conforming reference | PASS — 131/131 |
| Declared V6 mutants | PASS — 16/16 full and targeted intended rejections independently rerun |
| Proof blocks | PASS — 52 |
| Proof executor | PASS — 21 |
| Non-M13 persistence Tier A | PASS — 36 |
| Checkpoint shadow | PASS — 2 |
| YAML and worker diff check | PASS |

These results preserve the V6 work as lawful partial proof. They do not override the independent false positive below.

## Blocking false positive — global active guard

A proof-only mutant was created from the conforming reference with one module-global active-attempt flag rather than one flag per `UnitOfWork` instance.

Observed results:

```text
V6 repaired proof against global-guard mutant: 131 passed
```

The mutant therefore satisfies every V6 case while implementing the wrong ownership boundary.

A direct public-seam probe creates two distinct non-durable `UnitOfWork` instances with different command types, consistency-unit IDs and idempotency keys. While instance A is active, its owner callback executes an unrelated transaction through instance B.

- The conforming per-instance reference permits B to commit its own state, version `1`, sequence `1` and receipt, then permits A to commit its independent state, version `1`, sequence `1` and receipt.
- The global-guard mutant raises `RuntimeError("UnitOfWork.execute attempt is already active")` from B solely because A is active.

This contradicts:

1. the accepted V6 proof requirement that exclusion is **per active `UnitOfWork` instance**;
2. N-06.5, which preserves independent owner-specific transactions rather than inventing one process-wide transaction/lock; and
3. M13 ownership, which provides transaction mechanics without coupling unrelated consistency units through hidden global state.

The 131-case family contains no positive two-instance independence case, so this false implementation is invisible.

## Exact return gate

The next lawful unit is test-only `M13-PROOF-REPAIR-V7`.

Preserve all 131 V6 cases and add the minimum public-seam proof establishing:

1. active-attempt exclusion is scoped to the active `UnitOfWork` instance;
2. a second distinct instance with a different command type and consistency unit remains independently executable while the first instance is active;
3. both instances publish only their own state, version, sequence, receipt and idempotency truth;
4. same-instance nested execution remains rejected;
5. success or failure in one instance does not poison the active-attempt state of another; and
6. process-global, module-global and class-global active-guard mutants pass the frozen V6 family but are rejected by the V7 addition for the intended over-broad coupling reason.

Production source remains frozen. The worker must not repair implementation, alter normative authority or configuration, issue `IMPLEMENTATION_OPEN`, merge, or begin M01. After independent acceptance of V7 proof, a separate `M13-IMPLEMENT-REPAIR-V1` may repair the four-file implementation.

## Evidence

Independent evidence is retained under:

`project_control/canonical_project_manager/modules/M13/raw_validation/pm_v7_review/`

Key files:

- `pm_v6_mutant_global_active_guard.py`
- `global_guard_full_family.txt`
- `pm_v6_two_instance_guard_probe.py`
- `two_instance_reference.txt`
- `two_instance_global_mutant.txt`
- `independent_frozen_proof_check.txt`
- `new_mutants_summary.tsv`
