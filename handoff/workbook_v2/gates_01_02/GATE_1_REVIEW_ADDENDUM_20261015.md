# Gate 1 review — bounded return and follow-up

Date: 15 October 2026. Reviewer: Codex, reviewing the supplied findings rather than implementing Gates 1 or 2.

## Decision

**Recommendation: RETURN for a bounded documentary correction. Gate 1 is not accepted; Gate 2 remains NOT_OPEN.** The first failed exit invariant is reliable effective authority for Gate 2 (ExecPlan Gate 1 claim (a)); the outstanding-obligation inventory also needs reconciliation (claim (c)). This is not a request to redo the whole investigation, finish M01, run tests, or seek approval again for already-approved mathematics.

The user authorised review and a supplement for remaining investigation. This addendum records that review; it does not amend the frozen plan or accepted domain definitions. The six original findings are preserved unchanged. Their READY_FOR_DECISION labels are submissions, not acceptance.

## Exact reviewed baseline and method

- Supplied archive: `NVDA_V2_GATE_1_COMPLETE_FINDINGS_SINGLE_FULL_GIT_20261015.tar(1).gz`, SHA-256 `ce89804957a9bdc24cf873bc5802b48a107d955ae740edcc6ececf10d649401f`.
- Supplied local `main`: `e9cde877b4c9ca61f71ac3eeefde9d7684d4a73e`; tree `3da4c00c5d5a0227b21a01149745814298c635f6`; worktree initially clean.
- Frozen plan: Revision 4, SHA-256 `8abed334586aea28b22db7ec6fd0614f41cdb47a02b08cb4e839eb61b96e8b0e`.
- Compared the six submitted findings and index against the guardrails, agents, plan and master commissioning brief, especially 6.A, 8 Phase 1 and 10. Followed the identified F4 authority references, their approval Git object and later review/repair/pause records. Inspected G1.2/G1.6 recording lineage and relevant F4 ancestry.
- Read-only document/Git examination only. No application execution, tests, lint, typecheck or repository validation suites. Historical execution results below are reports of earlier work, not fresh verification.

This review stops positive gate certification at the proved failures below. It is not a fresh exhaustive 209-row semantic audit, workbook-cell revalidation, implementation census, or independent acceptance of repaired F4 production. No separate acceptance of G1.1/G1.3/G1.4/G1.5 is asserted by the absence of an additional finding here.

## R1 — Correct the effective F4 authority (G1.2; material before Gate 2)

**VERIFIED discrepancy.** G1.2's 13 October amendment row says that the earlier proposal's “unapproved D178 economics” are not accepted by the D175 approval. The very authority it cites, `handoff/m01_completion/authority/F4_OWNER_APPROVED_CLARIFICATION_20261013.md`, expressly incorporates:

1. `proof/f4_20261013_three_blockers/AUTHORITY_RESOLUTION_RECORD.md`, sections **4, 5 and 7**; and
2. `proof/f4_20261013_d175_policy/D175_POLICY_RESOLUTION_PROPOSAL.md`, sections **3–6**.

It also expressly says the proposal-only labels are historical, before approval. Approval record commit `2bfac720bede231207eaf07eed5ec6c993246c3d` is an ancestor of the reviewed baseline. The later `proof/f4_20261013_implementation/PAUSE_HANDOFF.md` corroborates the scope, but the approval record itself is the controlling source, not the pause summary.

The first incorporated section 4 is the D178 execution-reference/currency and multi-leg allocation contract; section 5 is the D189/D192 risk convention/carrier, qualified by the later D175 policy; section 7 is D192 precedence/refusal. The later record supplies the reference-calibrated D175 policy, its validity restrictions, exact monetary carriers, D176 consumption and related scope/provenance contracts. The restriction to two changed **catalogue context fields** does not restrict the entire approved **mathematical clarification** to those fields. Unchanged CSV bytes are not evidence that a separately approved definition is absent.

**Required correction:** Replace the conflicting interpretation in the effective-authority handoff, preserving the original finding as historical evidence if using a supplement. Carry both incorporated scopes and their exact section references into the Gate 2 source map. Distinguish accepted mathematics, approved implementation contracts, historical implementation/proof and still-unaccepted Stage 1. Do not invent risk defaults or declare production correct.

**Closure evidence:** One reconciled amendment entry explicitly covers D178, D189 and D192 as well as D175 and affected carrier consumers; it identifies which later policy provisions qualify the earlier risk proposal. No surviving current-facing instruction calls the incorporated D178 contract unapproved. No new owner approval is needed to restate the existing record; if contrary later authority is found, identify and resolve that exact conflict.

## R2 — Reconcile the latest F4 obligations, not only the early snapshot (G1.6)

**VERIFIED coverage gap.** G1.6 identifies F4 using `proof/f4_20261009/F4_WORKER_PROGRESS_AND_UNRESOLVED.md`, and uses broad M-10/M-11 carry-forward rows. A-03 narrows the financial change to D175/D189 contexts/policy. The ledger does not separately identify the later financial review's four findings and subsequent repair/re-review boundary. Its claim to inventory separately material known defects/decisions therefore exceeds the demonstrated reconciliation.

Primary later sources:

- `proof/f4_20261013_implementation/INDEPENDENT_REVIEW_RETURN.md`: reviewed production `95ae8c3f8078fdf492db7831a53efe749f424a5d`, four Important findings, no Stage-1 acceptance.
- `proof/f4_20261013_implementation/PAUSE_HANDOFF.md`: repair proofs `1e7d125`, production repair `4ed7586`, further snapshot-correspondence proof `a4aa6ba`, preserved final edits at `585fccc95521fb22e17348e77bd665198a8ec675`; no independent re-review of the repaired final tree in that checkpoint.
- `proof/f4_20261013_d186_authorised/D186_RECOVERY_CHECKPOINT.md`: bounded authorised D186 extractor/entry-identity work and evidence limitations; its earlier unresolved D178/D189/D192 statements must be read through the later approval rather than carried forward unchanged.

**Required follow-up inventory (documentary, not a repair task):**

| Obligation to reconcile | Exact question and required carry-forward |
|---|---|
| Approved D178/D164 and D175/D176/D189/D192 contracts | Carry the complete approved semantics and carrier/provenance consequences, not only the two CSV changes. Meaning belongs in Gate 2; implementation/reuse proof belongs in later C–E. |
| Actual live exposure units and scoped quantities | Reconcile the review finding, subsequent repair evidence and remaining acceptance. Preserve the invariant that actual sources establish exact contracts, signed quantities, multipliers, currency and scaling. |
| Joint clipping representation | Reconcile the common-lambda/component-rounding finding and repair boundary. Preserve exact inequality and representation proof; do not assert the old defect still exists without source evidence. |
| Actual producer/reference correspondence | Reconcile D175 retained metadata and later snapshot-correspondence repairs; carry the class-wide correspondence obligation, not only a list of matching labels. |
| Canonical D187-to-D192 score carrier | Reconcile the canonical numeric score/domain incompatibility and repair evidence; retain explicit thresholds and boolean refusal. |
| D186 approved extraction and exact entry anchor | Record bounded authority, current evidence and remaining independent acceptance; preserve exact entry/current identity, canonical units, feature configuration and fail-closed lineage. |
| Latest-tree review and evidence debt | Name the absent re-review and verification after the last edits, database proof limits, and remaining 174/144/30 reconciliation. These are future proof obligations, not tasks to execute during Gate 1. |

For each, record source/commit, inherited claim, later repair or authority, current established status, proposed destination (conditional on Gate 2), compatibility/proof consequence, responsible future worker/decision owner and receiving work package. A general “all F4 work carries” does not establish whether a specific old blocker is resolved, repaired-but-unaccepted, or still unknown. Conversely, a historical review failure must not be labelled a current production defect merely because it once occurred.

**Closure evidence:** An updated supplementary G1.6 ledger resolves the sequence through the latest relevant checkpoint and links each still-open obligation to its receiving scope. Preserve the distinction between documentary reconciliation now and implementation acceptance later. No tests or code changes are required for this follow-up.

## Lineage and recurrence classification

G1.2's incorrect exclusion entered at `3a711281be9c8c4d25a21f352ebb5e3a36246965` and was preserved when the findings moved out of the plan at `40f12de`. G1.6 entered at `c8e5838468f4aee31e36dda1e5f7ec5e69824f9a`. This is the first identified review return of these Gate 1 findings in the inspected lineage: **ISOLATED Gate 1 review episode**, with a shared authority/status-reconciliation mechanism across R1/R2, not a claimed second successive failed Gate 1 repair.

The inherited F4 reviewer separately classified its source-scope, retained-provenance and carrier findings as RECURRENT_CLASS and rounding as ISOLATED. Preserve those classifications when carrying that work forward. Their existence is not evidence that the repaired current code repeats the failures.

## What does not need to hold up this documentary correction

Do not require completion of M01, live provider proof, a running database, new module registration, migration, or test execution to close Gate 1. The Gate 1 findings already distinguish those future activities from architecture/authority investigation. Original archive-byte uncertainty is not the reason for this return; no newly identified archive-only question is raised here.

The full 209-row meaning/dependency classification remains Gate 2, and the implementation census/reuse/self-sufficiency work remains C–E. This addendum adds no gate and changes no leaf count: six leaves in each gate.

## Next action and acceptance boundary

Complete R1 and R2 as a single bounded findings supplement, retaining the frozen ExecPlan and original sources. Then review the resulting exact evidence baseline against all five Gate 1 exit claims and record the owner/delegate decision. The present submission is **not approved for closure**. Gate 2 must not begin on the strength of this return, a commit, or a READY_FOR_DECISION label.
