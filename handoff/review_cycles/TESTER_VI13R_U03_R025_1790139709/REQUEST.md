# Review-cycle request

## Cycle identity

- **Cycle:** `TESTER_VI13R_U03_R025_1790139709`
- **Current actor:** `TESTER`
- **Predecessor Worker cycle:** `WORKER_VI12R_U03_1790138454`
- **Accepted forward `main`:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **U03 production candidate:** `7cf8936f854fbed952a468ce06c2f2a0320d9291`
- **U03 production tree:** `b63aac7fb538ea6a38ce3dea5aab719fc7be0ee0`
- **Worker branch:** `work/vi12r-u03-observation-fidelity`

## Authorised task

Follow root governance and the current `EXEC_PLAN.md` exactly. Independently review only the
realised **IWO-U03 — Raw observation admission, native fidelity and temporal-kind truth** candidate.
Do not begin or assess U04.

Bind the review to the exact candidate above. Inspect the actual implementation as well as the
bounded proof and accepted semantic authority. In particular, determine whether the realised U03
implementation preserves:

- one observation occurrence per actually supplied provider logical record, without field splitting;
- distinct observations for separable/newly received records even when delivery/native identifiers
  or values match;
- same-occurrence retry idempotency only for identical content and conflicting reuse rejection;
- exact native record/provider-null/numeric runtime-type and optional provenance fidelity;
- required UTC receipt, genuine optional nanosecond evidence only, and typed local ingestion order;
- ingestion sequence non-decrease scoped locally rather than globally;
- exact `true_instant|date_only|receipt_only` law without inferred provider timezone/event UTC;
- independent no-scope observation validity and referential readback;
- preservation of accepted U01/U02 behaviour and the public owner boundary.

Apply the current bounded-review method: challenge concrete defects in this realised implementation
and proof, including ordinary reachable mutable-state bypass if one actually exists, but do not
reopen an unlimited search over arbitrary Python introspection/metaprogramming or hypothetical
future implementation topologies.

Primary obligations are `IA17-PROD-003`, `IA17-PROD-004`, `IA17-PROD-005` and the observation/
identity portions of `IA17-PROD-008`. Relevant accepted IRB clauses are BC-005, BC-006, BC-009 and
BC-010.

## Required disposition

Return exactly one U03 disposition: `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`.

If `PASS`, state explicitly that U03 may be lawfully promoted and that U04 becomes authorised only
after that promotion. If `FAIL`, identify the exact accepted proposition defeated, the owning
layer and the smallest bounded repair; U04 remains prohibited.

Record response/evidence/commands/result in this cycle, preserve exact candidate identity, create
the next opposite-role `WORKER_...` cycle, update `CURRENT_STATE.md`, and return a full-Git TAR.
