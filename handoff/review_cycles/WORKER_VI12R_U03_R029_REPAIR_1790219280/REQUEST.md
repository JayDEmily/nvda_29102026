# Review-cycle request

## Cycle identity

- **Cycle:** `WORKER_VI12R_U03_R029_REPAIR_1790219280`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U03_R029_1790214675`
- **Reviewer-029 disposition:** `FAIL / RETURN_TO_WORKER`
- **Reviewer-029 disposition commit:** `9b2ff603517c7fa5e063a4ad08790bb9fddd28c3`
- **Rejected repaired U03 candidate:** `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`
- **Rejected repaired U03 candidate tree:** `21eb6bd2ba53b29ea6d80f90c01af40668f56955`
- **Accepted/promoted U02 main:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **Reviewer-028 finding status:** `R028-U03-F001` — `CLOSED`
- **Open Reviewer-029 finding:** `R029-U03-F001`

## Authorised task

Programme Owner direction on 2026-09-24 supersedes the earlier witness-only repair instruction.
Treat `R029-U03-F001` as the trigger for **class-level U03 native-retry root-cause closure**, not as
an isolated `datetime` special case. The governing direction is
`implementation/authority/VI13R_U03_NATIVE_RETRY_ROOT_CAUSE_DIRECTION.md`; read it in full before
changing code. Do not begin or assess U04.

Reviewer 029 independently established that `R028-U03-F001` is closed: both required `array.array`
and `range` same-ID conflicts reject, the first admitted record remains intact, and the complete U03
proof is 47/47 green including all earlier numeric/NaN/complex/bytes/mapping exactness cases.

`R029-U03-F001` demonstrates another manifestation of the remaining class problem: ordinary Python
equality can erase fidelity-bearing representation for values that the realised `native_record`
surface currently admits. The verified witness is aware `datetime` instant normalisation
(`2026-09-20T12:00:00+00:00` versus `2026-09-20T13:00:00+01:00`), but closing that witness alone is
not completion.

Before mutation, establish from current authority plus the realised API whether the admitted native
value domain is closed enough to support one principled exact-content comparison strategy. Then
produce exactly one of the two outcomes defined by the Programme Owner direction:

1. **CLASS_LEVEL_REPAIR_READY_FOR_REVIEW** — implement and prove a bounded U03 strategy that closes
   the established admitted domain as a class, preserves every Reviewer-025..029 closed behaviour,
   preserves genuinely identical reconstructed-content idempotency, and has no unproved generic
   equality escape; or
2. **BLOCKED — U03 NATIVE VALUE DOMAIN / EXACT-CONTENT AUTHORITY GAP** — if current authority leaves
   an open value universe that cannot be compared exactly without inventing provider validity or
   representation law. Identify the minimum Programme Owner decision required and stop.

Do **not** return a candidate to Reviewer 030 merely by adding a `datetime` branch. Do **not** invent
a provider-value whitelist, narrow `native_record`, or broaden the work into U04/persistence/replay.
Use compact strategy-level regressions rather than an open-ended one-test-per-type catalogue.

Relevant semantic authority remains IRB BC-005, BC-006, BC-009 and BC-010 plus IWO-U03 and
IA17-PROD-003/004/005 and the observation/identity portion of IA17-PROD-008. Existing U01/U02/U03
public semantics, non-native observation equality, owner boundaries and all existing valid proof must
be preserved.

## Branch / history law

Preserve Git ancestry. Create a fresh repair branch from the current received handoff HEAD so the
Reviewer-029 disposition and this Programme Owner correction remain in ancestry; do not squash,
rebase or rewrite history. Until the Worker mutates U03, the production source remains the rejected
candidate `d25aedeed5de65d0a241bdce6eae22671ef2ddf8` carried forward unchanged. Keep physical repair
bounded to U03 owner/proof paths required for the class-level native-retry closure.

## Required validation and handoff

For **CLASS_LEVEL_REPAIR_READY_FOR_REVIEW**, run the proposition-bearing U01+U02+U03 proof plus
current architecture/static controls on the frozen repaired candidate. Preserve exact
commit/tree/changed paths, the comparator-domain analysis and compact strategy-level regression
results. Only then create a fresh `TESTER_...` cycle for Reviewer 030 to review the class-level
closure claim.

For **BLOCKED — U03 NATIVE VALUE DOMAIN / EXACT-CONTENT AUTHORITY GAP**, record the blocker and the
minimum Programme Owner decision required in this Worker cycle and stop; do not create Reviewer 030.

U04 remains prohibited until U03 receives PASS and is lawfully promoted to forward `main`.
