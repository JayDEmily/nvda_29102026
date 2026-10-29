# Review-cycle request

## Cycle identity

- **Cycle:** `TESTER_VI13R_U03_R028_1790205913`
- **Current actor:** `TESTER`
- **Predecessor Worker cycle:** `WORKER_VI12R_U03_R027_REPAIR_1790166643`
- **Accepted forward `main`:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **Rejected repaired U03 candidate:** `758060930b015c23bf63a5de4d71c4d318760393`
- **Reviewer-027 disposition commit:** `31b76489b1ec32fa38921bd3f5e97e40f544e23e`
- **Open Reviewer-027 finding under repair:** `R027-U03-F001`
- **Repaired U03 candidate:** `06735b3682d79387ebaa4da70002e6685d52740a`
- **Repaired U03 tree:** `b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`
- **Worker branch:** `work/vi12r-u03-r027-repair`

## Authorised task

Follow root governance and the current `EXEC_PLAN.md` exactly. Independently review only the
repaired **IWO-U03 — Raw observation admission, native fidelity and temporal-kind truth** candidate.
Do not begin or assess U04.

Bind the review to the exact repaired candidate above. First determine whether `R027-U03-F001` is
closed:

- same-ID native `bytes` -> `bytearray` content change must reject as conflicting content;
- same-ID nested mapping-key `int(1)` -> `float(1.0)` change must reject as conflicting content;
- rejected conflicting retry must not mutate or replace the first admitted record;
- native retry equality must remain exact/runtime-type-sensitive through admitted nested mapping
  keys/values and standard nested sequence/set values rather than falling back to Python equality
  where it collapses representation;
- already-closed int/float, Decimal-scale, reconstructed NaN-idempotency and complex signed-zero
  behaviours must remain closed;
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
