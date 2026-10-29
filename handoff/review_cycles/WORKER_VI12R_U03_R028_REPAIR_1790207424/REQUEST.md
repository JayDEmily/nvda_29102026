# Review-cycle request

## Cycle identity

- **Cycle:** `WORKER_VI12R_U03_R028_REPAIR_1790207424`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U03_R028_1790205913`
- **Reviewer-028 disposition:** `FAIL / RETURN_TO_WORKER`
- **Reviewer-028 disposition commit:** `d6d58c0a45b439c262cc135b961e9c67b98ac0a8`
- **Rejected repaired U03 candidate:** `06735b3682d79387ebaa4da70002e6685d52740a`
- **Rejected repaired U03 candidate tree:** `b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`
- **Accepted/promoted U02 main:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **Reviewer-027 finding status:** `R027-U03-F001` — concrete bytes/bytearray and nested mapping-key witnesses closed, overall finding not fully closed
- **Open Reviewer-028 finding:** `R028-U03-F001`

## Authorised task

Execute the smallest bounded IWO-U03 repair required to close **only `R028-U03-F001`**. Do not
begin or assess U04.

Reviewer 028 independently verified that the two concrete Reviewer-027 regressions are closed and
that all earlier numeric/NaN/complex retry behaviours remain closed. Exact pinned U01+U02+U03 is
373/373 and current static/product/architecture controls are green. The remaining defect is the
same native-content equality root at the generic fallback, now demonstrated for admitted same-type
standard sequences:

1. a same-ID retry from native `array('b', [1])` to `array('B', [1])` is accepted as idempotent
   rather than rejected even though the `array.array` typecode changes;
2. a same-ID retry from native `range(0, 3, 2)` to `range(0, 4, 2)` is accepted as idempotent rather
   than rejected even though the range bound changes;
3. both pairs preserve exact runtime type and ordinary Python equality returns true, so the current
   generic `left == right` fallback collapses the changed native representation.

Required repair outcome:

1. preserve accepted U01/U02/U03 public semantics and the bounded owner boundary;
2. retain all already-closed retry behaviours: int/float conflict, Decimal-scale conflict,
   reconstructed NaN idempotency, complex signed-zero conflict, bytes/bytearray conflict and nested
   mapping-key int/float conflict;
3. reject same-ID `array.array` typecode/content change without replacing the first admitted record;
4. reject same-ID `range` start/stop/step representation change without replacing the first admitted
   record;
5. eliminate the demonstrated ordinary-equality collapse for admitted standard sequence values while
   preserving existing non-native observation-field equality semantics;
6. add the smallest implementation-coupled U03 regressions needed to close the two concrete
   Reviewer-028 witnesses;
7. do not invent provider validity, duplicate or retransmission equivalence, broaden U04 behaviour,
   add persistence/replay, or activate downstream capability.

The current public `native_record` contract admits these challenge values. Do not close the finding
by adding an unauthorised provider-validity restriction. Relevant authority remains IRB BC-005,
BC-006, BC-009 and BC-010 plus IWO-U03 and the active standard-sequence exactness requirement.

Do not broaden the repair into arbitrary object-identity policy beyond what this finding and accepted
authority establish.

## Branch / history law

Preserve Git ancestry. Create a fresh repair branch from the Reviewer-028 FAIL continuity state; do
not squash, rebase or rewrite history. Keep the repair bounded to the U03 owner/proof paths required
by `R028-U03-F001`.

## Required validation and handoff

Run the proposition-bearing U01+U02+U03 proof plus current architecture/static controls on the frozen
repaired candidate. Preserve exact commit/tree/changed paths and focused regression result. Then
create a fresh `TESTER_...` cycle for independent U03 re-review. U04 remains prohibited until repaired
U03 receives PASS and is lawfully promoted to forward `main`.
