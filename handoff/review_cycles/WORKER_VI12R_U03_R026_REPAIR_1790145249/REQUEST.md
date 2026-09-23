# Review-cycle request

## Cycle identity

- **Cycle:** `WORKER_VI12R_U03_R026_REPAIR_1790145249`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U03_R026_1790143078`
- **Reviewer-026 disposition:** `FAIL / RETURN_TO_WORKER`
- **Reviewer-026 disposition commit:** `f58aa8b9cd21f1ebd9b01b80a71213bd5d16c63b`
- **Rejected repaired U03 candidate:** `6316735eb22bdbe243b02637f09376bf1200e43d`
- **Rejected repaired U03 candidate tree:** `a9cc881f50b7a6adf021ce80fce52a330e9d203d`
- **Accepted/promoted U02 main:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **Predecessor finding not fully closed:** `R025-U03-F001`
- **Open Reviewer-026 findings:** `R026-U03-F001`, `R026-U03-F002`

## Authorised task

Execute the smallest bounded IWO-U03 repair required to close **only the remaining retry-comparator
failures established by Reviewer 026**. Do not begin or assess U04.

Reviewer 026 verified that the two original Reviewer-025 examples are repaired, but the comparator
still fails exact same-occurrence semantics for admitted native numeric values:

1. `R026-U03-F001`: a separately reconstructed same-ID payload containing `float("nan")` is rejected
   as conflicting even when the reconstructed native value is identical; `Decimal("NaN")` exhibits
   the same false-conflict behaviour. The current full-observation ordinary equality gate prevents
   the native comparator from establishing identical content.
2. `R026-U03-F002`: a same-ID retry changing `complex(-0.0, 0.0)` to `complex(0.0, 0.0)` is accepted
   as idempotent because the complex branch uses ordinary `==` and collapses the signed-zero
   distinction.

Required repair outcome:

1. preserve accepted U01/U02/U03 public semantics and the bounded owner boundary;
2. keep the already-correct int/float and Decimal-scale conflict rejection plus unchanged readback;
3. make separately reconstructed genuinely identical admitted native numeric content idempotent,
   including the concrete NaN canaries established by Reviewer 026;
4. reject the concrete complex signed-zero native conflict without replacing the original record;
5. remove the ordinary-native-equality failure mode from full-observation retry comparison while
   preserving accepted non-native field semantics;
6. add the smallest implementation-coupled U03 regressions that close the two concrete
   Reviewer-026 escapes;
7. do not invent provider validity, duplicate or retransmission equivalence, broaden U04 behaviour,
   add persistence/replay, or activate downstream capability.

The current public `native_record` contract admits these challenge values; do not close the findings
by adding an unauthorised provider-validity restriction. Relevant authority remains IRB BC-005,
BC-006, BC-009 and BC-010 plus IWO-U03.

## Branch / history law

Preserve Git ancestry. Create a fresh repair branch from the Reviewer-026 FAIL continuity state; do
not squash, rebase or rewrite history. Keep the repair bounded to the U03 owner/proof paths required
by `R026-U03-F001` and `R026-U03-F002`.

## Required validation and handoff

Run the proposition-bearing U01+U02+U03 proof plus current architecture/static controls on the
frozen repaired candidate. Preserve exact commit/tree/changed paths and focused regression result.
Then create a fresh `TESTER_...` cycle for independent U03 re-review. U04 remains prohibited until
repaired U03 receives PASS and is lawfully promoted.
