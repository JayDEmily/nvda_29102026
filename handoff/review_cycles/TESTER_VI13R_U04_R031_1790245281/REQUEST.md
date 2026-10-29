# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `TESTER_VI13R_U04_R031_1790245281`
- **Current actor:** `TESTER`
- **Predecessor Worker cycle:** `WORKER_VI12R_U04_1790241325`
- **Promoted U03 forward main:** `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec`
- **U04 candidate:** `e7eb44119bdf7fb22abacae8291788619792c96a`
- **Candidate tree:** `ea104900fcaf8e2db4177df3909956f464d6a918`
- **Worker branch:** `work/vi12r-u04-receipt-assessment`
- **U05 and later:** prohibited

## Mandatory readback

Before substantive review, read in full root `README.md`, `GUARDRAILS.md`, applicable `AGENTS.md` /
overrides and the complete current `EXEC_PLAN.md`; then `handoff/control/CURRENT_STATE.md`, this
request, accepted IRB BC-007/BC-008/BC-009/BC-010, IWO-U04 in the accepted work order, the admitted
U04 proof family and physical U04 proof, `implementation/proof/VI12R_U04_RECEIPT_ASSESSMENT_EVIDENCE.md`,
and the exact candidate implementation/diff. Read the U03 Reviewer-030 disposition only as needed to
confirm preserved predecessor acceptance/lineage. Apply ExecPlan section 6.11 to any return-to-worker
routing.

## Authorised task

Independently review only **IWO-U04 — Receipt evidence and append-only assessment state** on the exact
candidate above. Do not begin or assess U05.

Determine whether the realised candidate conserves the accepted U04 meaning and whether any
implementation-coupled material escape exists, including:

- a relation exists only for an admitted observation and realised capture under the capture's exact
  stored effective policy, with receipt inside `[start,end)` and positive eligibility authority;
- lawful ineligible/out-of-slot/no-scope observation states do not fabricate a relation;
- relation role is exactly `evidences_receipt_presence_only` and adds no membership, count,
  validity, completeness, ownership, health or finality claim;
- relation/assessment evidence is capture-local rather than owner-global;
- assessment outcome is M00-owned and derived only from eligible committed receipt evidence visible
  at `evidence_as_of_ts_utc`; caller or persistence mechanism cannot choose it;
- the contract retains exactly `unknown_not_established`, `zero_received` and
  `one_or_more_received`; U04 does not improperly manufacture restart-unknown or reinterpret zero as
  provider-event absence/exact count;
- `evidence_as_of_ts_utc` remains system-knowledge time and is not treated as event/finality/SLA
  time;
- assessments are append-only, same-ID retry is idempotent only for identical content, later records
  name the exact immediate predecessor, and late eligible evidence can append one-or-more over zero
  without overwriting the earlier assessment;
- the optional technical persistence port receives already-decided facts and does not become the
  semantic decision owner;
- existing U01-U03 semantics and public/architecture boundaries remain intact; and
- no U05/PostgreSQL/restart/provider-mapping or other unauthorised semantics were introduced.

Primary obligations are `IA17-PROD-006`, `IA17-PROD-007` and the state/identity portions of
`IA17-PROD-008`.

## Required disposition

Return exactly one U04 disposition: `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`.

If PASS, state that exact U04 candidate may be lawfully promoted; U05 becomes authorised only after
that promotion and fresh routing. If FAIL, identify the exact authorised proposition defeated,
owning layer and smallest bounded repair, and apply the recurrence classification required by
ExecPlan 6.11 where applicable. If authority itself is insufficient or contradictory, return
`BLOCKED` rather than inventing law.

Record response/evidence/commands/result in this cycle, preserve exact candidate identity, create
the next opposite-role cycle required by the disposition, update `CURRENT_STATE.md`, and return a
full-Git TAR.
