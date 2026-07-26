# M13 State Kernel — Independent Implementation Review V1

## Disposition

`CLOSED:M13_PROOF_REPAIR_V6_REQUIRED_FOR_REENTRANT_EXECUTION_AND_RECEIPT_CONTRACT_TRUTH`

The worker implementation at `ddbd7257ab7305b2a3648f9f1d810b07670808aa` is a genuine bounded M13 implementation proposal and passes the frozen 46-case family. It is not accepted because independent Project Manager probes reproduce two target-surface defects that the frozen proof does not cover.

M13 is not complete, must not merge, and M01 remains closed.

## Source verification

- Supplied archive: `NVDA_M13_IMPLEMENTATION_PROPOSED_ddbd725_20260726.tar(1).gz`.
- Archive SHA-256: `f522111ce84bab3b785bb161a71c0bf00e569263d4ba050744d30b19ac933c5e`.
- Worker branch: `implementation/m13-state-kernel`.
- Worker commit: `ddbd7257ab7305b2a3648f9f1d810b07670808aa`.
- Accepted parent: `e8384ada435097d64f46f5fe01d55e8d833bf1f4`.
- Source worktree: clean.
- Frozen proof SHA-256: `7f4fd1e3d9c7f7dc75675146f9e2a38d4fb259a1938986c7cdfc2b006ddfab0a`.
- Worker changed production paths: only the four files under `src/nvda_desk/m13_state_kernel/`.
- Tests, normative documents and proof/retained configuration: unchanged.

## Positive validation independently reproduced

| Surface | Result |
|---|---|
| Frozen M13 family | PASS — 46 passed |
| Complete persistence Tier A | PASS — 82 passed |
| Proof-block structure | PASS — 52 blocks |
| Proof executor | PASS — 21 passed |
| Checkpoint shadow | PASS — 2 passed |
| Architecture boundary | PASS — no outgoing M13 domain dependency or new M13 cycle |
| Integrity and changed-path controls | PASS |
| Implementation-derived mutants | PASS — eight intended full-family and targeted rejections independently observed |
| Complete repository shadow | 61 failed, 1247 passed; count agrees with worker evidence and introduces no claimed unrelated regression |

These results establish that the worker did substantial valid work. They do not override higher-authority defects outside the frozen proof.

## Finding 1 — re-entrant execution corrupts committed sequence and state truth

**Severity:** blocking.

N-06 states that a later owner transaction may begin only from an admitted prior committed result and that receipts/state transitions must carry deterministic committed sequence/version truth.

`InMemoryUnitOfWork.execute()` reads the current version and sequence, creates an isolated working state, then invokes caller-owned mutation without marking the transaction boundary active. A mutation may therefore recursively invoke `execute()` on the same unit of work before the outer transaction has committed. The outer call later publishes its stale precomputed version and sequence over the inner result.

Independent public-seam reproduction produced:

```text
state={'outer': 1, 'inner': 0}
state_version=1
committed_sequence=1
receipt_count=2
receipt_sequences=[1, 1]
receipt_versions=[(0, 1), (0, 1)]
```

The inner transaction returned a success receipt and retained an idempotency binding, but its state mutation was overwritten. Two receipts claim the same committed sequence and version transition. This contradicts:

- `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md` N06.4 deterministic sequence/version law;
- N06.5 later-transaction ordering;
- implementation-brief requirements for expected-version enforcement and atomic publication.

Evidence:

- `src/nvda_desk/m13_state_kernel/in_memory.py:95-123`;
- `raw_validation/pm_implementation_v1_review/pm_v1_reentrant_execute_probe.py`;
- `raw_validation/pm_implementation_v1_review/pm_v1_reentrant_execute_probe.txt`.

## Finding 2 — public `AtomicReceipt` accepts incoherent scope and non-integer version truth

**Severity:** blocking public-contract defect.

The accepted implementation brief requires receipt truth to bind command, idempotency scope, result, prior/resulting versions and sequence. The exported `AtomicReceipt` validates that its duplicated scope fields are non-empty but does not require them to match the embedded `IdempotencyKey`. It also accepts `resulting_state_version=1.0` because equality with `prior_state_version + 1` succeeds without an integer type check.

Independent construction succeeded with:

```text
idempotency key scope = command-a / unit-a
receipt scope         = command-b / unit-b
resulting version     = 1.0 (float)
```

This allows an immutable public value to carry internally contradictory transaction authority even though the production builder currently creates consistent values.

Evidence:

- `src/nvda_desk/m13_state_kernel/contracts.py:76-100`;
- `raw_validation/pm_implementation_v1_review/pm_v1_atomic_receipt_contract_probe.py`;
- `raw_validation/pm_implementation_v1_review/pm_v1_atomic_receipt_contract_probe.txt`.

## Why the frozen 46-case proof is insufficient

The current family tests unsuccessful transaction boundaries, participant rollback, failed idempotency binding, duplicate replay and detached state. It does not attempt a nested call through the same live `UnitOfWork` during owner mutation and does not construct a receipt with mismatched duplicated scope fields or a non-integer resulting version.

A green 46-case result therefore proves the behaviours it exercises, not the absent sequencing and public-contract cases above.

## Exact return gate

The next lawful unit is test-only `M13-PROOF-REPAIR-V6`.

Preserve all 46 existing cases. Add the minimum public-seam proof establishing:

1. a nested `execute()` attempt on the same active unit of work is rejected before nested mutation or participant work;
2. an unhandled nested rejection leaves the outer attempt entirely uncommitted;
3. a caller that catches the bounded nested rejection may complete the outer transaction cleanly as the sole sequence/version `1` commit;
4. active-attempt state is cleared after success and every failure so a later non-nested call is not poisoned;
5. no nested receipt, state, participant truth or idempotency binding survives;
6. `AtomicReceipt` rejects command-type or consistency-unit mismatch against its embedded `IdempotencyKey`;
7. prior and resulting state versions are exact non-negative integers, excluding booleans and floats.

The repaired proof must reject false-positive implementations that:

- permit re-entrant execution;
- block re-entry but fail to clear the active flag after failure;
- retain nested idempotency or receipt truth;
- accept mismatched receipt scope;
- accept non-integer version fields.

The proof-repair worker must not modify production source, normative authority, configuration or later modules and cannot issue final acceptance. After independent PM acceptance, a separate bounded `M13-IMPLEMENT-REPAIR-V1` may amend the four-file implementation.

## Current authority state

- `M13-PROOF-REPAIR-V6`: next lawful unit.
- `M13-IMPLEMENT`: closed pending proof repair and later implementation repair.
- M13 merge/completion: closed.
- M01 and all later modules: closed.
