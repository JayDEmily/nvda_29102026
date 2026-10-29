# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `WORKER_VI12R_U04_1790241325`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U03_R030_1790239551`
- **Reviewer-030 disposition commit:** `dc40971d24ee773ee133d07622f92d709a7cec11`
- **Reviewer-030 disposition:** `PASS`
- **U03 authority clarification commit:** `c4caa78a2d13c5dc115c83fedcdf44648efe6d78`
- **Accepted U03 candidate:** `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf`
- **Accepted U03 tree:** `81ef8edc93c9b322b29cdec6b9ab76b731d8e9a5`
- **Current forward `main` before U03 promotion:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **U05 and later:** prohibited

## Mandatory readback

Before mutation, read root `README.md`, `GUARDRAILS.md`, applicable `AGENTS.md` / overrides, complete current `EXEC_PLAN.md`, `CURRENT_STATE.md`, this request, the accepted U03 NativeValueV1 authority plus static-typing clarification, Reviewer-030 disposition/evidence, IRB BC-007/BC-008/BC-009/BC-010, and IWO-U04 in the accepted work order. Inspect the existing U04 product proof before implementation.

## Authorised task

Follow current governance and execute the next lawful Worker sequence without widening scope:

1. **Promote accepted U03 first.** Preserve ancestry; do not squash, rebase or rewrite history. Fast-forward forward `main` through the routed accepted U03 lineage, then verify that candidate `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf`, authority clarification `c4caa78a2d13c5dc115c83fedcdf44648efe6d78`, and Reviewer-030 PASS `dc40971d24ee773ee133d07622f92d709a7cec11` are ancestors of the resulting `main`. Verify clean worktree and strict Git integrity before U04 work.
2. **Only after U03 promotion succeeds, begin IWO-U04 on a fresh branch from promoted `main`.** Implement only **IWO-U04 — Receipt evidence and append-only assessment state**, preserving accepted U01-U03 meaning.
3. U04 semantic scope is exactly:
   - derive a receipt-evidence relation only for an established eligible active policy when receipt time lies inside the capture `[start,end)` interval;
   - relation role exactly `evidences_receipt_presence_only`;
   - preserve lawful no-relation state for a no-scope observation;
   - assessment outcomes exactly `unknown_not_established`, `zero_received`, `one_or_more_received`;
   - `evidence_as_of_ts_utc` is system-knowledge time, not event/finality/SLA time;
   - assessments are append-only with immediate-predecessor supersession;
   - later eligible evidence may append `one_or_more_received` superseding prior zero without overwrite; and
   - there is no final-assessment concept.
4. Primary obligations are `IA17-PROD-006`, `IA17-PROD-007` and the state/identity portions of `IA17-PROD-008`. Use the already accepted bounded U04 proof as the contract; add implementation-coupled proof only where the realised implementation exposes a material escape.
5. Do **not** begin U05 or later units, add PostgreSQL persistence/restart behaviour, invent provider eligibility/mapping rules, infer membership/count/finality, weaken accepted U01-U03 proof, choose Remaining Unknowns, or move semantic ownership.
6. Run the proposition-bearing U04 validation required by the governing plan on committed candidate state. Freeze exact commit/tree/changed paths/evidence, then create a fresh opposite-role `TESTER_...` cycle for VI-13R review of U04 only.

## Fail-closed conditions

- If the accepted U03 candidate, authority clarification and Reviewer-030 PASS cannot be promoted with preserved ancestry, stop `BLOCKED`; do not start U04.
- If forward `main` after promotion is not clean/integrity-valid, stop `BLOCKED`; do not start U04.
- If U04 implementation requires provider eligibility/mapping semantics, persistence design or another unresolved authority value not already fixed by the accepted IWO/IRB, stop on that exact authority gap rather than inventing a default.
- If `CURRENT_STATE.md`, this cycle prefix or this request disagree about actor/bound state, stop `BLOCKED` rather than guessing.

## Required cycle output

Record Worker results in this cycle's `RESPONSE.md`, `RESULT.json`, `EVIDENCE.md`, `COMMANDS.txt` and `SOURCE_PACKET.sha256`. Preserve exact U03 promotion identity and U04 candidate identity. Create the next `TESTER_<...timestamp>/` cycle only if a lawful U04 candidate is frozen. Reviewer recurrence control in ExecPlan section 6.11 remains mandatory for the next Tester.
