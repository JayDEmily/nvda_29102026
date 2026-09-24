# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `WORKER_VI12R_U04_R031_REPAIR_1790248980`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U04_R031_1790245281`
- **Reviewer-031 disposition:** `FAIL / RETURN_TO_WORKER`
- **Reviewer-031 disposition commit:** `6c33e51ab436b8f19dd1799ddf60cc0b3d87ebaa`
- **Rejected U04 candidate:** `e7eb44119bdf7fb22abacae8291788619792c96a`
- **Rejected U04 candidate tree:** `ea104900fcaf8e2db4177df3909956f464d6a918`
- **Accepted/promoted U03 forward main:** `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec`
- **Open Reviewer-031 finding:** `R031-U04-F001`
- **Recurrence classification:** `ISOLATED`
- **U05 and later:** prohibited

## Mandatory readback

Before mutation, read in full root `README.md`, `GUARDRAILS.md`, applicable `AGENTS.md` / overrides,
the complete current `EXEC_PLAN.md`, `handoff/control/CURRENT_STATE.md`, this request, Reviewer-031
response/evidence/disposition, accepted IRB BC-007/BC-008/BC-009/BC-010, IWO-U04, the admitted U04
proof family and physical U04 proof, and the exact rejected candidate implementation/diff. Preserve
U03 accepted ancestry and apply the smallest complete repair discipline.

## Authorised task

Execute one bounded IWO-U04 repair that closes **`R031-U04-F001` as a mechanism**, not merely the two
Reviewer-031 canary witnesses. Do not begin or assess U05.

Reviewer 031 established that the rejected candidate computes assessment presence only from
`state.relations_by_capture`, even though BC-007 makes receipt-evidence relation materialisation
optional. Consequently an admitted in-slot observation under positive eligibility authority can be
reported as `zero_received` when the optional relation command was not first invoked, and an in-slot
observation whose eligibility cannot be adjudicated can likewise be collapsed to zero. The candidate
also uses observation `received_ts_utc` as a surrogate for the BC-008 system-knowledge / committed-
visibility boundary.

The repaired candidate must establish all of the following authorised propositions:

1. assessment outcome is derived from capture-local eligible admitted/committed observation evidence
   visible to the assessment's own transaction, independently of whether a
   `CaptureReceiptEvidenceRelation.v1` object was separately materialised;
2. omitting optional relation materialisation cannot turn otherwise eligible visible evidence into
   `zero_received`;
3. when admitted in-slot evidence requires eligibility adjudication, unavailable required eligibility
   authority fails closed rather than manufacturing semantic zero;
4. observation `received_ts_utc` remains the receipt-time fact and is not used as a substitute for
   system-knowledge time or transaction/commit visibility;
5. lawful no-evidence, ineligible, out-of-slot and no-scope cases continue to avoid fabricated
   positive receipt evidence and retain the accepted U04 zero semantics where authority establishes
   zero;
6. relation role/nonclaims, capture locality, append-only assessment history, immediate-predecessor
   supersession, same-ID retry semantics, late-evidence supersession and accepted U01-U03 behaviour
   remain intact; and
7. add bounded implementation-coupled U04 regressions that prove the repaired mechanism rather than
   accumulating unrelated witness-specific tests.

Do not solve this by making optional relation materialisation mandatory. Do not move semantic
outcome choice into the persistence port. Do not invent provider validity, PostgreSQL/restart
semantics, provider mapping semantics, finality/SLA meaning or any U05 capability.

If current accepted authority is genuinely insufficient to represent or determine item 4 without
inventing a new system-knowledge/commit fact, stop `BLOCKED` on that exact authority gap. Do not
silently substitute receipt time, event time, wall-clock time or relation-materialisation time.

## Branch / history law

Preserve Git ancestry from this routed handoff. Create a fresh bounded repair branch; do not squash,
rebase or rewrite history. Keep production/proof changes confined to the U04 owner and the smallest
U04 implementation-coupled proof needed for `R031-U04-F001`. U05 remains prohibited.

## Required validation and handoff

Freeze one repaired U04 candidate and record its exact commit/tree/changed paths. Run the
proposition-bearing U04 proof, preserved U01-U04 proof and current static/architecture/product-
control checks available in the execution environment. Distinguish independently executed evidence
from preserved predecessor evidence.

If the repair proposition is satisfied, create a fresh `TESTER_...` cycle for independent U04
re-review. The next Tester must apply ExecPlan section 6.11 to the relevant U04 lineage before any
further return-to-worker routing. U05 becomes eligible only after a fresh U04 `PASS` and lawful
promotion.
