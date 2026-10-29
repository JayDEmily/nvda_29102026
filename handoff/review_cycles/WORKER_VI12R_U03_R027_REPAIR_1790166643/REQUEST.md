# Review-cycle request

## Cycle identity

- **Cycle:** `WORKER_VI12R_U03_R027_REPAIR_1790166643`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U03_R027_1790155140`
- **Reviewer-027 disposition:** `FAIL / RETURN_TO_WORKER`
- **Reviewer-027 disposition commit:** `31b76489b1ec32fa38921bd3f5e97e40f544e23e`
- **Rejected repaired U03 candidate:** `758060930b015c23bf63a5de4d71c4d318760393`
- **Rejected repaired U03 candidate tree:** `b819ffa1795e97e40374a59cedd42834233d2225`
- **Accepted/promoted U02 main:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **Closed Reviewer-026 findings:** `R026-U03-F001`, `R026-U03-F002`
- **Open Reviewer-027 finding:** `R027-U03-F001`

## Authorised task

Execute the smallest bounded IWO-U03 repair required to close **only `R027-U03-F001`**. Do not
begin or assess U04.

Reviewer 027 independently verified that the concrete Reviewer-026 NaN-idempotency and
complex-signed-zero failures are closed and that the prior int/float and Decimal-scale conflicts
remain closed. The remaining defect is generic native-content equality:

1. a same-ID retry from native `b"abc"` to `bytearray(b"abc")` is accepted as idempotent rather than
   rejected as conflicting content;
2. a same-ID retry whose nested native mapping changes key `1` to `1.0` is likewise accepted as
   idempotent;
3. the root mechanism is ordinary Python equality in the generic native-value fallback plus ordinary
   set/key equality and lookup in nested mappings, which collapses distinct admitted runtime
   representations.

Required repair outcome:

1. preserve accepted U01/U02/U03 public semantics and the bounded owner boundary;
2. retain all already-closed Reviewer-025 and Reviewer-026 retry behaviours, including separately
   reconstructed NaN idempotency, exact float/complex/Decimal representation handling and unchanged
   original readback after rejected conflicts;
3. reject same-ID `bytes` -> `bytearray` native-content change without replacing the first record;
4. reject same-ID nested mapping-key `int(1)` -> `float(1.0)` change without replacing the first
   record;
5. make native comparison exact/runtime-type-sensitive across values admitted by the current U03
   surface, including nested mapping keys, without changing accepted non-native field equality
   semantics;
6. add the smallest implementation-coupled U03 regressions needed to close the two concrete
   Reviewer-027 witnesses;
7. do not invent provider validity, duplicate or retransmission equivalence, broaden U04 behaviour,
   add persistence/replay, or activate downstream capability.

The current public `native_record` contract admits these challenge values. Do not close the finding
by adding an unauthorised provider-validity restriction. Relevant authority remains IRB BC-005,
BC-006, BC-009 and BC-010 plus IWO-U03.

## Branch / history law

Preserve Git ancestry. Create a fresh repair branch from the Reviewer-027 FAIL continuity state; do
not squash, rebase or rewrite history. Keep the repair bounded to the U03 owner/proof paths required
by `R027-U03-F001`.

## Required validation and handoff

Run the proposition-bearing U01+U02+U03 proof plus current architecture/static controls on the frozen
repaired candidate. Preserve exact commit/tree/changed paths and focused regression result. Then
create a fresh `TESTER_...` cycle for independent U03 re-review. U04 remains prohibited until repaired
U03 receives PASS and is lawfully promoted to forward `main`.
