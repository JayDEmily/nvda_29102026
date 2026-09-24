# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `TESTER_VI13R_U04_R032_1790251908`
- **Current actor:** `TESTER`
- **Predecessor Worker cycle:** `WORKER_VI12R_U04_R031_REPAIR_1790248980`
- **Reviewer-031 finding under repair:** `R031-U04-F001`
- **Reviewer-031 recurrence classification:** `ISOLATED`
- **Rejected U04 candidate:** `e7eb44119bdf7fb22abacae8291788619792c96a`
- **Repaired U04 candidate:** `dc3b448191a2b2d3528ffb576b1ebc2c56839991`
- **Candidate tree:** `3c7a42eb215d708a0f8d8db37727133ecc234275`
- **Worker branch:** `work/vi12r-u04-r031-repair`
- **Promoted U03 forward main:** `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec`
- **U05 and later:** prohibited

## Mandatory readback

Before substantive review, read in full root `README.md`, `GUARDRAILS.md`, applicable `AGENTS.md` /
overrides and complete current `EXEC_PLAN.md`; then `handoff/control/CURRENT_STATE.md`, this request,
Reviewer-031 response/evidence/result and disposition, the predecessor Worker repair response/evidence,
accepted IRB BC-007/BC-008/BC-009/BC-010, IWO-U04, admitted U04 proof family and physical U04 proof,
`implementation/proof/VI13R_U04_REVIEWER_031_DISPOSITION.md`,
`implementation/proof/VI12R_U04_REVIEWER031_REPAIR_EVIDENCE.md`, and the exact repaired candidate
diff. Apply ExecPlan section 6.11 to the relevant U04 failure/repair lineage before any further
return-to-worker routing.

## Authorised task

Independently re-review only **IWO-U04 — Receipt evidence and append-only assessment state** on the
exact repaired candidate above. Do not begin or assess U05.

First determine whether `R031-U04-F001` is closed as a mechanism:

- assessment presence must derive from capture-local eligible admitted/committed observation evidence
  visible to the assessment's own transaction, not from optional relation materialisation;
- omitting `CaptureReceiptEvidenceRelation.v1` materialisation must not change otherwise eligible
  visible evidence into zero;
- in-slot evidence whose eligibility requires unavailable authority must fail closed rather than
  become semantic zero;
- `received_ts_utc` must remain receipt time and must not be used as a surrogate for BC-008
  system-knowledge time or transaction/commit visibility;
- lawful no-evidence, ineligible and out-of-slot cases must retain accepted zero/no-positive-evidence
  semantics where authority establishes zero; and
- same-ID retry must remain idempotent while later evidence is represented by a new immediate-
  predecessor-superseding assessment rather than mutation of the earlier assessment.

Then re-review the preserved U04 contract: exact relation role/nonclaims, capture locality, exact
three outcomes, M00-owned outcome derivation, append-only assessment chain, immediate-predecessor
supersession, persistence-port non-ownership, accepted U01-U03 behaviour and absence of U05/provider-
mapping/finality/SLA invention.

Primary obligations remain `IA17-PROD-006`, `IA17-PROD-007` and the state/identity portions of
`IA17-PROD-008`.

## Required disposition

Return exactly one U04 disposition: `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`.

If PASS, state that exact repaired U04 candidate may be lawfully promoted; U05 becomes authorised
only after that promotion and fresh routing. If FAIL, identify the exact authorised proposition
defeated, owning layer and smallest bounded repair, and first perform the lineage-aware recurrence
classification required by ExecPlan 6.11. If the same/substantially same U04 implementation failure
repeats, do not automatically route another local patch; apply the section 6.11 stop/escalation law.
If authority is insufficient or contradictory, return `BLOCKED` rather than inventing law.

Record response/evidence/commands/result in this cycle, preserve exact candidate identity, create the
next opposite-role cycle required by the disposition, update `CURRENT_STATE.md`, and return a
full-Git TAR.
