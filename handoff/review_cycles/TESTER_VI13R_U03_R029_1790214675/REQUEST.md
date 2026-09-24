# Review-cycle request

## Cycle identity

- **Cycle:** `TESTER_VI13R_U03_R029_1790214675`
- **Current actor:** `TESTER`
- **Predecessor Worker cycle:** `WORKER_VI12R_U03_R028_REPAIR_1790207424`
- **Accepted forward `main`:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **Rejected repaired U03 candidate:** `06735b3682d79387ebaa4da70002e6685d52740a`
- **Reviewer-028 disposition commit:** `d6d58c0a45b439c262cc135b961e9c67b98ac0a8`
- **Open Reviewer-028 finding under repair:** `R028-U03-F001`
- **Repaired U03 candidate:** `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`
- **Repaired U03 tree:** `21eb6bd2ba53b29ea6d80f90c01af40668f56955`
- **Worker branch:** `work/vi12r-u03-r028-repair`

## Authorised task

Follow root governance and the current `EXEC_PLAN.md` exactly. Independently review only the
repaired **IWO-U03 — Raw observation admission, native fidelity and temporal-kind truth** candidate.
Do not begin or assess U04.

Bind the review to the exact repaired candidate above. First determine whether `R028-U03-F001` is
closed:

- same-ID native `array('b', [1])` -> `array('B', [1])` must reject as conflicting content;
- same-ID native `range(0, 3, 2)` -> `range(0, 4, 2)` must reject as conflicting content;
- rejected conflicting retry must not mutate or replace the first admitted record;
- native retry equality must preserve representation-bearing state for these admitted same-type
  standard sequence values rather than ordinary Python equality collapsing it;
- all earlier int/float, Decimal-scale, reconstructed NaN-idempotency, complex signed-zero,
  bytes/bytearray and nested mapping-key int/float behaviours must remain closed;
- non-native observation fields must retain their accepted existing retry equality semantics.

Then challenge this realised repair for concrete remaining U03 defects under the bounded-review
method. Preserve accepted U01/U02/U03 semantics. Do not reopen unlimited hypothetical proof-harness
search, invent provider duplicate/retransmission equivalence or provider validity semantics,
implement U04, add persistence/replay or activate downstream capability.

Primary obligations remain `IA17-PROD-003`, `IA17-PROD-004`, `IA17-PROD-005` and the
observation/identity portions of `IA17-PROD-008`; relevant accepted IRB clauses are BC-005,
BC-006, BC-009 and BC-010.

## Required disposition

Return exactly one U03 disposition: `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`.

If `PASS`, state explicitly that repaired U03 may be lawfully promoted and that U04 becomes
authorised only after that promotion. If `FAIL`, identify the exact accepted proposition defeated,
ownership layer and smallest bounded repair; U04 remains prohibited.

Record response/evidence/commands/result in this cycle, preserve exact candidate identity, create
the next opposite-role `WORKER_...` cycle, update `CURRENT_STATE.md`, and return a full-Git TAR.
