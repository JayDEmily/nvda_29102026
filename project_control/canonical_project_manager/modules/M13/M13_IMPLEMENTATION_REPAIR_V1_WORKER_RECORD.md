# M13 Implementation Repair V1 — Worker Record

## Status

`PROPOSED_M13_IMPLEMENTATION_REPAIR_V1_AWAITING_INDEPENDENT_PROJECT_MANAGER_REVIEW`

- Authoritative base branch: `review/m13-proof-v8`
- Authoritative base commit: `df17277247e4d68c260318e6306d4788de410a4c`
- Worker branch: `work/m13-state-kernel-implementation-repair-v1`
- Governing brief: `M13_IMPLEMENT_REPAIR_V1_WORKER_BRIEF.md`
- Frozen proof SHA-256:
  `a3ad3e8b51e2dd73119ecbec2e546f8d4e594346efaa8bf588c90b67798b8843`
- Final commit and archive identities are reported externally after their bytes exist;
  embedding either identifier in its own checkpoint would recursively change it.

This is a bounded worker proposal. It does not accept M13, merge to `main`, open a
pull request, start M01, authorise a later module, or claim production durability.

## Pre-mutation Git and integrity gate

| Gate | Result |
|---|---|
| Authenticated remote base | PASS — `refs/heads/review/m13-proof-v8` resolved exactly to `df17277247e4d68c260318e6306d4788de410a4c` |
| Required ancestry | PASS — `cccf120a28419d5b337e47296bcd5ee7357f57cd` and `aded5edc1ad567a1f7d3a4231b918b3af1abd7bd` are ancestors |
| Worker branch absence | PASS — absent locally and remotely before creation |
| Source checkout | PASS — clean at the authoritative base |
| Git object integrity | PASS — `git fsck --full`, no output |
| Frozen proof bytes | PASS — exact required SHA-256 |

The Windows checkout initially exposed CRLF bytes for the frozen proof while the Git
blob itself matched the required LF-byte hash. Repository-local checkout conversion was
disabled and the committed blob bytes were restored before mutation. The checkout was
then clean and the six gates were rerun successfully.

## Bounded source repair

Only two production files changed.

### Instance-owned active-attempt exclusion

`src/nvda_desk/m13_state_kernel/in_memory.py` now owns one `_active_attempt` flag on
each `InMemoryUnitOfWork` instance.

The public `execute()` seam:

1. retains its existing command and callable validation;
2. rejects an already-active attempt with `RuntimeError`;
3. acquires the instance flag before scope calculation, duplicate resolution,
   optimistic-version resolution or any caller/participant callback;
4. delegates the preserved transaction body to `_execute_active()`;
5. keeps the flag active throughout owner mutation, receipt construction, prepare,
   commit, rollback and internal publication; and
6. clears it in an outer `finally` after every success, replay, validation rejection,
   mutation failure, participant failure, rollback path and nested rejection.

No module, class, process registry, command-scope or consistency-unit-scope guard was
introduced. Distinct `InMemoryUnitOfWork` instances remain independent.

### Coherent exact `AtomicReceipt` truth

`src/nvda_desk/m13_state_kernel/contracts.py` now requires:

- receipt `command_type` equals its embedded `IdempotencyKey.command_type`;
- receipt `consistency_unit_id` equals its embedded
  `IdempotencyKey.consistency_unit_id`;
- prior state version is an exact non-negative `int`;
- resulting state version is an exact positive `int` and exactly prior plus one;
- sequence is an exact positive `int`; and
- duplicate replay remains an exact `bool`.

All required identity strings remain non-empty. Replay still changes only
`duplicate_replay`.

## Preserved transaction law

The repair does not change:

- scoped committed idempotency identity;
- duplicate replay ordering;
- stale-version rejection;
- detached state and receipt copies;
- mutation/result validation;
- participant registration before prepare;
- prepare and commit ordering;
- reverse rollback responsibility;
- preservation of the primary failure when rollback also fails;
- publication only after every participant commits;
- failed-attempt non-binding;
- sequence/version allocation only on successful publication; or
- the explicit `non_durable_in_memory` boundary.

No thread-safety, process-safety, crash recovery, distributed transaction,
external-effect completion or trading-domain ownership claim is made.

## Proof-to-source mapping

| Proof obligation | Production owner |
|---|---|
| Same-instance nested execute rejected before nested callback truth | `InMemoryUnitOfWork.execute()` instance guard |
| Guard active through prepare, commit and rollback | outer `try/finally` around `_execute_active()` |
| Guard cleared after every terminal outcome | unconditional instance-field clear in `finally` |
| Distinct instances execute independently | guard stored only on `self` |
| Receipt scope matches embedded key | `AtomicReceipt.__post_init__()` scope comparisons |
| Version and sequence are exact integer truth | exact-type/domain checks in `AtomicReceipt.__post_init__()` |
| Replay preserves committed truth | existing detached `replace(..., duplicate_replay=True)` path |

## Validation and falsification

| Campaign | Result |
|---|---|
| Source baseline | EXPECTED RED — 44 failed / 108 passed |
| Frozen production proof | PASS — 152/152 |
| Persistence Tier A | PASS |
| V7 retained guard mutants | PASS — 8/8 full and designated rejection |
| V6 retained mutants | PASS — 16/16 full and designated rejection |
| Earlier retained mutants | PASS — 11/11 |
| PM V5 retained mutants | PASS — 2/2 |
| V5 configurable failed-binding mutants | PASS — 32/32 |
| Prior implementation-derived mutants | PASS — 8/8 full and designated rejection |
| New production-derived repair mutants | PASS — 6/6 full and designated rejection |
| Proof blocks / proof executor / checkpoint shadow | PASS |
| Architecture / vocabulary exact parity | PASS |
| YAML / compile / Ruff / Black / diff check | PASS |
| Complete repository shadow | PASS — baseline 107 failures, current 63, exactly 44 M13 failures resolved, zero new or changed failures |

The six new production-derived mutants cover: no guard, module-global guard, guard
installed after owner mutation starts, guard cleared before participant commit,
receipt scope checking only one dimension, and resulting-version validation accepting
float/bool impostors.

Commands, exit codes, unedited outputs, summaries and intended-defect adjudications are
retained under `raw_validation/implementation_repair_v1/`.

## Mutation boundary

Allowed production changes are limited to:

- `src/nvda_desk/m13_state_kernel/contracts.py`;
- `src/nvda_desk/m13_state_kernel/in_memory.py`.

The remaining changes are this worker record and worker-owned raw evidence. The frozen
proof, normative sources, proof/retained configuration, unrelated production code,
M01 and later-module surfaces are unchanged.

## Return gate

M13 remains unaccepted pending independent Project Manager implementation review.
