# ADR — Verbatim Astra NVIDIA V2 methodology and forward-architecture reviews

**Date:** 12 November 2026 (Melbourne)

**Status:** RECORDED EXTERNAL RECOMMENDATIONS — NOT INSTALLED GOVERNING AUTHORITY

**Repository branch:** `work/t01-continuous-execution-20261112` (parent `a3a3e23e58e313328a6bb22ab72d7a706cfa7aab`)

**Purpose:** Owner-directed preservation of both completed Astra Max analyses. The two texts below are copied byte-for-byte from the gateway's saved `response.md` files. They are evidence and recommendations for a subsequent worker, not an ADR approving or commissioning implementation. This record does not alter `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`, test authority or the D145 pause.

**Provenance:**

- **Astra response 1:** `resp_00ea1b6682b028df006af52544bcbc87d190358f9e6e384a57` — Strategic project-methodology review. Source SHA-256: `dbbac5350aefc43636ef2116fdb5f2a430b0cd0ebce50403ba0ce0f87bf546c9`.
- **Astra response 2:** `resp_00ea1b6682b028df006af52d55e4f487d1906fdffd03028ce0` — Supplementary product architecture, IBKR, dependencies and UI review. Source SHA-256: `1d84abcb364320a65de79230e29e8bedbe276d53f7df3fce0c149646284dcda6`.

---

## Astra response 1 — Strategic project-methodology review

<!-- BEGIN ASTRA RESPONSE 1 — VERBATIM ORIGINAL BYTES -->
I’ll review the pinned snapshot as evidence, not as authority to act. I’ll separate governance, Git recovery, runtime qualification and product assurance, and cross-check the planning claims against the supplied code and tests without executing them.# NVIDIA V2 — strategic project-methodology review

**Evidence date: 12 November 2026. Analytical review only.**

## Executive recommendation

**Keep the substantive engineering controls, but simplify the way work moves between them. Do not promote the current work branch wholesale.**

The principal problem is not that there are 39 leaves. Those leaves distinguish real source, policy and dependency obligations. The unnecessary elaboration lies mainly in:

- several competing presentations of “current” authority;
- repeated copies of rules, profiles and status;
- repeating whole-history recovery work at ordinary leaf boundaries;
- confusing technical review or transfer completion with another request for owner permission;
- deferring virtually all product feedback until a large body of dependent implementation has accumulated.

At the same time, the selected code exposes assurance gaps that paperwork has not eliminated: **architecture tests contradict the admitted M03 population; the product runner does not itself enforce the R2 physical-case budget; and the new runtime pin is not automatically enforced by that runner.** These are static findings, not executed test failures. [W:`tests/architecture/test_identifier_taxonomy.py`:32–49; W:`config/architecture/implementation_allocations.yaml`:2–14; W:`tools/product_proof_outcomes.py`:79–88; W:`tools/run_product_proof_gate.py`:24–82.]

My recommended course is:

1. prepare one reconciled, main-based governing amendment;
2. obtain one independent review and one exact owner decision covering adoption, installation and the bounded standing commission;
3. use verified remote checkpoints with a retained recovery baseline, rather than repeated full recovery ceremonies;
4. retain a separate strict Tester, but amend the schedule to permit **dependency-focused testing windows**, with L32 consolidating rather than repeating accepted results;
5. keep additional M00 PostgreSQL work separate from the M02 SQLite critical path.

**D145 remains PAUSED. Nothing in this report authorises implementation, testing, runtime qualification, repository mutation or promotion.**

---

## Evidence basis and citation convention

- **M:** `repository/main/`, pinned to `ded4b98e1e5999d1ddf2f067e660b691917bcd71`.
- **W:** `repository/work/`, pinned to `a3a3e23e58e313328a6bb22ab72d7a706cfa7aab`.
- **P:** W:`handoff/planning/t01_recovered_successor_20261111/`.
- **E:** W:`handoff/m02_completion_28_execution/`.
- **C:** W:`handoff/planning/m02_foundation_completion_20261030/`.
- **Q:** W:`handoff/m02_foundation_prerequisites_20261029/`.

**VERIFIED** below means established from supplied text or bounded documentary calculations. **VERIFIED—RECORDED** identifies an attributed historical review or execution result, not a result reproduced here. **INFERRED** identifies a reasoned consequence; **UNKNOWN** identifies a material evidence limit; **PROPOSED** identifies a recommendation.

I read the packet instructions, final-tree comparison and pinned governing roots before forming conclusions. I used internal tooling only to index supplied text, check selected text identities, analyse the documentary dependency graph and recompute literal CSV arithmetic. **No repository code, product tests, runtime probes or Git operations were executed.** The archive describes a selection from 4,039 work-tree files; index-only bodies and XLSX contents were not inspected. [ `00_READ_ME_FIRST.md`; `02_BRANCH_COMPARE.md`; `03_SOURCE_COVERAGE_INDEX.md`; `04_WORKBOOK_EVIDENCE.md`.]

# 1. Reconstructed actual state

## 1.1 Authority is layered, not determined by branch recency

**VERIFIED:** Both snapshots retain frozen `GUARDRAILS.md`, blob `54a4407609941f63f6b902076688ff102a3d5ba2`. Its rules expressly distinguish current authority from newer files, green tests, commits and historical receipts. It also says the plan cannot create programme or domain law. This supports continuous execution of commissioned work without treating every newer document as an approval. [W:`GUARDRAILS.md`:9–24, 74–98.]

The roots currently present different operational contexts:

| Surface | What the supplied bytes establish | Consequence |
|---|---|---|
| **Main `AGENTS.md`**, blob `ac541c372eef2c491a89bae94ea1c818ed1e1401` | Accumulated October commissions and historical schedules, including L14-only amendments, alongside an older “Current task” heading. It already says continuation within a commissioned plan needs no routine reapproval. | It is not a clean current operating summary. Its dated amendments must be resolved by scope, not by whichever paragraph an agent encounters first. |
| **Main `EXEC_PLAN.md`**, blob `e35f11bf1fcde2be53b0c44f4818889e72509a39` | The 29 October prerequisite-resolution documentary tranche, including subsequent G4 documentary acceptance. | Main has **not** installed the 39-leaf T01 successor as its root plan. |
| **Work `AGENTS.md`**, blob `0157a3e5d628ebd4c4555614543980424a21a0c7` | Continuous-execution wording is already present in this working root, but its checkpoint instruction still says local commit plus Git bundle. | The successor plan is uninstalled, but it would be inaccurate to say that no root governance bytes have changed on work. |
| **Work `EXEC_PLAN.md`**, blob `95aa1090e02585673f81f16e9a72c150353c0120` | Recovered, historically owner-approved local R2 setup: 39 leaves, CHAT_MANUAL, L32-only product testing and local bundle transport. It retains historical passages and outstanding-boundary wording. | This is **not** `P:PROPOSED_EXEC_PLAN.md`. Copying the work root into main would install the local R2 text, not the intended Ubuntu/GitHub successor. |
| **Work test override**, blob `fb502203947d2075d9a6e29f39c4fe6c7e0a66a1` | Local R2 arrangement; Worker authors but does not execute product tests; separate Tester at L32. | The broad continuous-execution message does not release product testing to the Worker. |

Sources: M:`AGENTS.md`, dated commissions and “Current task”; M:`EXEC_PLAN.md` §§0–6; W:`AGENTS.md`:3–31; W:`EXEC_PLAN.md` §§4–9; W:`tests/AGENTS.override.md`:3–13; `02_BRANCH_COMPARE.md`:10–17.

**Assessment:** This is an authority-presentation problem, not evidence that all prior commissions were invalid. Neither “main is accepted” nor “work is newer” resolves the different jurisdictions automatically.

## 1.2 Acceptance and review chronology

### Established historical documentary acceptance

**VERIFIED—RECORDED:**

- The original G2 re-review accepts documentary work at `dbf08e6521bd16dcde593bb050a4c22beafd49d0`. The packet correctly separates the **9,094-byte original report** from its **3,268-byte summary**.
- The delegated G4 review accepts the prerequisite-disposition packet and synthetic proposal scaffold at candidate `9974df6638d920746df8e2bde70a4ff38013462d`, tree `ee1877c9776b7ef7cfe29ccfed7881b8fca82407`.
- That G4 verdict leaves all 28 implementation holds intact. Four versioned synthetic scenario groups cover the six policy-first identities; they are not production-policy approval.
- The 30 October R1 completion plan received fresh proposal review at `c63770bca1737365fd8d4bbfcb113ce7b9620ae9`, followed by the recorded owner statement, “I accept the plan.” Its acceptance-recording turn did not itself start implementation. Subsequent execution records describe the receiving commission and L00 work.

[Q:`G2_INDEPENDENT_ACCEPTANCE_EXTERNAL.md`, heading and §§1–3; Q:`G4_DELEGATED_INDEPENDENT_REVIEW.md`, verdict and requirements table; C:`INDEPENDENT_PLAN_REVIEW.md`; C:`OWNER_ACCEPTANCE_20261030.md`.]

Old `PENDING` and `RETURNED` entries therefore cannot simply be read as the latest documentary disposition. Conversely, later documentary acceptance cannot be used to erase production holds or manufacture product results.

### Recovery and transport acceptance are narrower

The R1 L00 reviewer recorded documentary acceptance and independent restoration, including 66 original refs and, for the final historical candidate, 237 declared current refs. **Download exposure remained a separate unmet condition.** The recorded permission-denied, HTTP 401 and bridge-connection failures were specific failed distribution routes, not evidence that implementation needed fresh owner permission. [E:`L00/REVIEW.md`, “Release boundary”; E:`L00/L00_FINAL_INDEPENDENT_RESTORE_RECEIPT.json`, `candidate`, `verdict`; E:`L00/TRANSFER_BLOCKER.md`.]

Later evidence records recovery of the original baseline archive and exact F02 source at:

- commit `16b7cc67f5d24336d3768e2da006819474a8c792`;
- tree `2b2bd7c1b7342f22909339a99150e2a395039e06`;
- parent `9a4f1e827accdd7cfe3d7a14d5575573589b1acd`.

The 11 November independent reviewer reports its own fresh GitHub receiver verification of the five recovery branches, all 66 mapped original names/tips, 13 unique tip objects and the 4,024-entry F02 inventory. It explicitly excludes complete additional-ref/non-Git-asset closure and runtime qualification. **Do not restart this already evidenced narrow recovery investigation merely because another chat begins.** [P:`T01_RECONCILIATION_AND_DECISION.md` §§1–2; P:`UBUNTU_F02_RESTORATION_RECEIPT.json`; W:`handoff/review/t01_successor_independent_20261111/INDEPENDENT_REVIEW.md` §§2–3.]

The synthetic R2 source-tree bridge and missing original intermediate lineage must nevertheless remain labelled accurately. Missing objects from the recovered local lineage are **not** proof that the original GitHub planning branch is globally unavailable. [W:`handoff/planning/chat_manual_transition_20261030/LOCAL_WORKER_SOURCE_PROVENANCE.md`; P:`BRANCH_CONSOLIDATION_AUDIT_20261112.md`, branch inventory.]

### The November proposal has not become active authority

**VERIFIED:**

- The 11 November report’s `ACCEPT_DOCUMENTARY_PROPOSAL` concerns pinned input `aa8dc23608bb6d655aebd74e390a8b3d341735c7`, not the later continuous-execution amendment.
- Its original proposed AGENTS and test-override blobs are identified in the report. The supplied amended texts contain subsequent wording.
- The 12 November ADR explicitly preserves that distinction.
- PR #2 published 39 documentary/evidence files. Their presence in main does not accept their proposals.
- The unexecuted 12 November review commission pins `0909250ca05cb8b9f19266bdb9cb4f601332172d` and then-main `7e2601a5e050d76202b1b6d3f69fc167a04c91f7`. Those are **not** the current packet’s work/main tips.

[W:`handoff/review/t01_successor_independent_20261111/INDEPENDENT_REVIEW.md`, heading and §§1, 7; P:`ADR_20261112_CONTINUOUS_EXECUTION.md`:25–34; `02_BRANCH_COMPARE.md`:2–6; W:`handoff/review/t01_main_consolidation_20261112/REVIEW_COMMISSION.md`:6–10, blob `b548ee4f090073e889a0df6aa4b25aa8b4389e06`.]

This strategic review **does not execute that commission** or create its requested repository verdict.

## 1.3 Product evidence and implementation frontier

The retained accounting is:

| Category | Established scope |
|---|---|
| 98 historical controlled identities | Historical profile-specific acceptances—not 98 general live capabilities. |
| 11 L14 claims | SOURCE plus ten already-counted D identities—not eleven additional signals. |
| 28 unresolved foundation identities | Eight source-first, six policy-first and fourteen predecessor-first dispositions. |
| R2 target | 27 new controlled acceptances: named core20 plus seven mandatory extensions. |
| D145 | Paused, zero executable allocation and zero contribution to the new-output target. |
| Seven external holds | D061, D064, D065, D070, D084, D114 and D115 remain outside the foundation 126. |

[E:`TEST_EVIDENCE_LEDGER.json`, `proof_obligations`; C:`EVIDENCE_REUSE_INDEX.json`; Q:`FINAL_CENSUS.json`; W:`handoff/m02_remaining_readiness/EXTERNAL_HOLDS.json`; W:`EXEC_PLAN.md` §§0–1, 6.]

The historical evidence is **not homogeneous**. The readiness reviewer expressly distinguishes D011’s final owner acceptance from a later independent repair re-review that was not established, and D016–D020 root acceptance ledgers from separate reviewer records. “All 98 independently passed” would overstate that evidence. [W:`handoff/m02_remaining_readiness/L00_INDEPENDENT_REVIEW.md`, “Documentary observations”.]

**Current frontier:** the packet records no new R2 product runs or released cases. The execution register leaves downstream work unattempted, while the active evidence ledger retains unresolved contracts and an undesignated separate Tester. Historical F02 documentary acceptance should not be reopened without a new discrepancy, but it does not close the successor’s current authority, complete receiver/assets or Ubuntu execution prerequisites. [E:`EXECUTION_REGISTER.json`, L00–L32; E:`TEST_EVIDENCE_LEDGER.json`, `execution_mode` and allocations; P:`PROPOSED_EXEC_PLAN.md` §10.]

The unresolved inputs are substantive:

- aligned public histories and a common fit for D079–D081/D078;
- explicit R112 model/scale and classification binding for D091;
- option calendar, expiry-instant and official-session IV contracts;
- actual compatible CALL/PUT predecessors and units;
- option trade/quote/sign/multiplier contracts;
- complete book reconstruction, matching and replenishment attribution;
- revaluation, surface, density and numerical conventions;
- full basket membership and three-component breadth representation.

These are not all requests for live data. **An explicitly commissioned controlled-synthetic profile can be proved without production feeds**, provided its synthetic source contract is truthful and admitted. Requiring production-policy approval for every controlled implementation would unnecessarily enlarge the commission. [W:`EXEC_PLAN.md` §§0, 3–4, 7; C:`SIGNAL_COVERAGE_MATRIX.csv`; Q:`G4_DELEGATED_INDEPENDENT_REVIEW.md`, acceptance boundary.]

# 2. Audit of the working method

## 2.1 The 39 leaves are defensible; the repeated ceremony is not

**VERIFIED:** The earlier P1 finding was real: grouped prerequisites allowed independent release in prose while machine dependencies referred to the whole group. Splitting L01a–d, L07a–b and L10a–c corrected that mismatch. Collapsing them merely to make the plan shorter would recreate it. [C:`RECONSTRUCTED_PRIOR_REVIEW.md`, P1; C:`INDEPENDENT_PLAN_REVIEW.md`, “Prior returned mechanisms”.]

However, each leaf repeats substantially the same handover rule, and obligations/status appear in several plans, registers, summaries and profile copies. The G4 propagation defect demonstrates the consequence: a canonical profile was corrected while embedded copies retained earlier wording. [Q:`G4_DELEGATED_RETURN_REPAIR_01.md`; Q:`G4_DELEGATED_INDEPENDENT_REVIEW.md`, “Findings, repairs and recurrence”; W:`EXEC_PLAN.md` §3.]

**PROPOSED:** Keep all semantic IDs and dependencies. Put common execution/checkpoint law once in the active plan. Use the existing execution register for leaf status and the evidence ledger for proof status. Reference canonical profile objects instead of manually embedding copies. Keep historical records immutable, but stop using their accumulated status text as the active dashboard.

## 2.2 Final-only L32 testing exchanges transfer convenience for late engineering risk

The R2 schedule deliberately permits provisional child implementation on stable, documented—but untested—parents. It explicitly acknowledges later upstream defect discovery. That is an intelligible response to manual chat-transfer friction, but it is a poor default for high-dependency components such as history producers, joint fits, option timing and surface/density calculations. [W:`EXEC_PLAN.md` §§2, 4, 6 and L32.]

**INFERRED:** If an upstream interface or persisted representation is wrong, final-only execution can return several completed-looking leaves together. The packet contains no measured defect-cost data, so the scale of this cost is unknown.

**PROPOSED:** Retain the separate sole strict Tester, but use dependency-focused testing windows:

- prove necessary history/temporal/direction support before substantial dependent work;
- prove joint fit before accepting residuals;
- prove ATM IV before its term/RV descendants;
- prove density before tails;
- batch genuinely independent terminal calculations where practical.

L32 should perform final reconciliation and execute remaining proofs, **not routinely rerun already accepted unchanged proofs**.

This is a **schedule amendment**, not an interpretation already authorised by “continuous execution”. Until adopted, the current final-only restriction remains.

## 2.3 Case budgets are useful limits, not evidence of adequacy

The arithmetic is coherent:

- 24 ordinary identities × two cases = 48;
- D141/D142/D144 × four cases = 12;
- total signal allocation = **60**;
- seven supporting pairs add **up to 14**;
- 35 ledger obligations include paused D145, leaving 34 potentially executable obligations.

The six-case ceiling is not a target or automatic permission to execute six cases. The current ledger still releases zero. [W:`EXEC_PLAN.md` §4; E:`TEST_EVIDENCE_LEDGER.json`; C:`INDEPENDENT_PLAN_REVIEW.md`, “Allocation, execution and reuse”.]

**Assessment:** Success plus reached refusal is a good starting discipline. It is not a universal adequacy theorem. A classifier, a joint fit and a constrained surface have different failure mechanisms. Require a concise mapping from each material invariant to:

1. a declared new witness;
2. an exact reusable proof; or
3. an explicit unresolved coverage gap.

Do not hide extra scenarios in parameterisation or a large test loop to satisfy the headline count. Equally, do not apply the later two-case rule retrospectively to historical aggregate counts such as D011’s 113 or D014’s 202. [W:`handoff/m02_remaining_readiness/L00_INDEPENDENT_REVIEW.md`, historical aggregate-count discussion.]

## 2.4 Durable Git evidence is necessary; receipt recursion is avoidable

Lost R0 bytes, source-ZIP reconstruction and the missing earlier final G0 candidate are concrete reasons to retain exact commits, trees, source hashes and recovery evidence. This is not merely bureaucracy. [C:`RECOVERY_RECORD.json`; E:`L00/R2_CANDIDATE_PROVENANCE_BINDING.md`.]

The avoidable problem is making every receipt update appear to require a fresh end-to-end acceptance cycle.

**PROPOSED:** Distinguish:

- **C:** product/documentary candidate;
- **R:** external review or execution receipt identifying C;
- **E:** later evidence commit preserving R.

E may attest C without pretending C contains its own receipt or checksum. Review the E–C documentary delta; do not invalidate C’s unchanged product evidence merely because E exists.

## 2.5 Recovery should be proved at meaningful boundaries

The historical packaging route involved a 124,661,535-byte additive, a 165,856,376-byte recovery base, extensive ref unions and custom completion of bundle headers. The later F02 additive was 1,000,499 bytes, but it carried a different candidate/ref scope; these sizes are **not** an apples-to-apples efficiency benchmark. [E:`L00/L00_FINAL_INDEPENDENT_RESTORE_RECEIPT.json`, `assets`; E:`L00/transfer_repair_20261030/README.md`; P:`T01_RECONCILIATION_AND_DECISION.md` §1.]

Git’s own bundle verification checks format and prerequisite closure; successful verification does not establish semantic acceptance. ([git-scm.com](https://git-scm.com/docs/git-bundle))

**PROPOSED checkpoint method:**

- independently establish one complete receiver/recovery baseline and required-ref map;
- at each leaf, verify the exact new commit/tree, changed scope, relevant evidence and retrievability;
- repeat full fresh restoration when transport, required-ref coverage or non-Git prerequisites change, at recovery events and at close-out;
- retain a verified bundle fallback if remote transport fails.

This replaces redundant repeated work, not recovery assurance. It requires an explicit amendment to the existing per-leaf full-restore/download contract.

## 2.6 Independence should concern judgement, not repeated actor setup

Separate Worker/Tester conversations are appropriate where that is the commissioned arrangement. But repeatedly creating a fresh actor does not itself improve an oracle, and a fresh reviewer should not ignore earlier failures. The U03 lineage records show why recurrence synthesis matters: successive equality witnesses required a closed carrier-domain decision, not another local patch. [W:`implementation/authority/VI13R_REVIEW_LINEAGE_AND_U03_BLOCKER_CORRECTION.md` §§1–4; W:`implementation/authority/VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md` §§2–6.]

Use one bounded handover: candidate, applicable authority, changed paths, prior findings/repairs, proof allocation, environment and exact next responsibility. Require the reviewer to report all material findings discovered within that bounded review, rather than treating the G0 request’s “one evidenced discrepancy” as a one-finding-per-cycle limit. [E:`L00/R2_G0_SQLITE_INDEPENDENT_REVIEW_REQUEST.md`, “Scope and sought decision”.]

The arithmetic handover demonstration supports a possible communication route—not repeated unattended operation or completed NVIDIA testing. [W:`handoff/review/t01_successor_independent_20261111/INDEPENDENT_REVIEW.md` §6.]

## 2.7 Root cause of repeated owner stops

**INFERRED from the recorded sequence:** recurring pauses arise from four mechanisms:

1. stale proposal-stage restrictions remain beside later commissions;
2. “authorisation”, “review”, “release” and “installation” are treated as interchangeable;
3. technical transport failure is escalated as though permission were missing;
4. implementation choices are sometimes reopened as owner decisions despite existing bounded delegation.

VI-04 is a useful counterexample: the owner authorised the smallest correctness-only PostgreSQL layout/types once, within explicit exclusions. That is a better delegation pattern than approving every technical choice. It does not automatically extend to new November backend scope. [M:`AGENTS.md`, dated task stack; P:`ADR_20261112_CONTINUOUS_EXECUTION.md`:8–21; E:`L00/TRANSFER_BLOCKER.md`; W:`implementation/authority/VI04_AUTHORITY_CLOSURE.md` §§2–4.]

**Bottom line:** reduce repeated permissions and duplicated records, not independent semantic responsibility.

# 3. Assessment of the continuous-execution proposal

## 3.1 The central distinction is sound

**VERIFIED:** ADR decisions 1–6 correctly separate:

- already commissioned, in-scope and released work;
- independent review and exclusive Tester responsibility;
- dependency-local stopping;
- genuinely reserved policy, budget, external-operation and promotion decisions;
- real session/tool limits.

The proposed plan’s standing-commission paragraph preserves the same conditional structure. **No change to frozen GUARDRAILS is necessary to establish this principle.** [P:`ADR_20261112_CONTINUOUS_EXECUTION.md`:16–25; P:`PROPOSED_EXEC_PLAN.md` §2; W:`GUARDRAILS.md`:131–143.]

However, shortened operating files should not be looser than the detailed plan.

## 3.2 Exact wording requiring correction or clarification

| Location and exact sentence | Assessment and recommended treatment |
|---|---|
| W:`AGENTS.md`:25 and P:`PROPOSED_AGENTS.md`:25: **“Rerun or expand tests only when new changes, failures, or unresolved concerns justify doing so.”** | **Clarify before adoption.** This is a necessary-condition formulation, not explicit permission, but it is materially looser than the plan’s repair/invalidation law. State that execution remains limited to the designated Tester, admitted allocation and accepted schedule; failed reruns require relevant material repair, successful reruns require precise material invalidation, and expansion requires admission. |
| P:`PROPOSED_TESTS_AGENTS.override.md`:8: **“Reuse uninvalidated previously accepted evidence; rerun or expand only when new changes, failures or unresolved concerns justify it, without exceeding accepted proof budgets or masking failed runs.”** | Apply the same correction. Being below a ceiling does not itself release an extra case. An unresolved concern alone should not become permission for speculative execution. |
| P:`PROPOSED_AGENTS.md`:15: **“Preserve the independent Tester role and evidence conditions; reviewer clearance is not product acceptance.”** | Change “reviewer clearance” to **“documentary reviewer clearance”**. The designated Tester does retain responsibility for an execution-backed semantic disposition; the sentence should not obscure that. |
| P:`PROPOSED_EXEC_PLAN.md` §7: **“No account purchase, live provider session, order action, external communication or provider integration is commissioned.”** | “External communication” is overbroad beside expressly proposed GitHub publication and reviewer handovers. Exclude external communications **other than the repository/checkpoint/reviewer handovers expressly commissioned by the plan**. |
| P:`PROPOSED_EXEC_PLAN.md` §0: **“The root accepted prerequisite plan remains unchanged pending actual owner acceptance and implementation commission.”** Followed by the `EXEC_PLAN_NEXT.md` navigation statement. | Replace this inherited current-state description with the actual distinction: main retains the prerequisite root; work retains local R2; T01 is uninstalled. `EXEC_PLAN_NEXT.md` presently points to accepted historical R1, not this T01 successor. Label retained October narrative as history. |
| W:`handoff/review/t01_main_consolidation_20261112/REVIEW_COMMISSION.md`:17: **“exact final-tree diff `main...work/t01-continuous-execution-20261112`”** | Correct in a later scoped commission/addendum. Three-dot comparison is merge-base-to-topic, not endpoint-to-endpoint. Use pinned endpoint comparison separately from ancestry/ahead-behind analysis. Preserve the original commission as historical evidence. |

GitHub explicitly distinguishes three-dot PR comparisons from two-dot endpoint comparisons. ([docs.github.com](https://docs.github.com/en/pull-requests/reference/branches))

I would also make **proof-budget changes, checkpoint-strategy changes and main promotion explicit reserved boundaries in the concise AGENTS text**, rather than relying on the longer ADR to supply them.

### A separate recommended schedule amendment

The sentence in §2—

> “Formal dependency-ordered product acceptance is deferred to L32, where the independent tester must prove parent before dependent.”

—is not a defect in the continuous-execution clarification. It is the existing final-only policy. My recommendation is to amend it deliberately to permit named dependency checkpoints and retain L32 as final census. Corresponding L32 entry conditions, §4, test override and ledger schedules must change together. Do not introduce early execution through a contradictory AGENTS shortcut.

## 3.3 Does the test-local override weaken independence?

**Assessment: not in its central role allocation.** It retains:

- Worker-authored but unexecuted proofs;
- a separate sole strict Tester;
- prerequisite-order execution;
- raw results and semantic disposition;
- recurrence analysis;
- direct sequences where helpers could conceal a negative condition.

The added “no routine owner continue approval” bullet is therefore sensible. [P:`PROPOSED_TESTS_AGENTS.override.md`:5–13.]

The residual risks are the loose rerun sentence and treating independent review as merely running Worker-supplied assertions. The Tester must still judge oracle adequacy, whether refusal reached the intended invariant, and whether the claimed source/lineage proposition was actually exercised. **Removing repeated permission does not remove the Tester’s right and duty to return inadequate proof.**

# 4. Git and branch strategy

## 4.1 Recommended route: selective integration from accepted main

**PROPOSED:** Use a main-based, allowlisted integration candidate—not a wholesale merge or rebase of the recovered work lineage.

The current comparison is **18 ahead / 53 behind, but eight different final-tree paths**. The older branch audit’s 13/51 and 300-plus comparison discussion describes an earlier comparison, not this final snapshot. [ `02_BRANCH_COMPARE.md`:2–17; P:`BRANCH_CONSOLIDATION_AUDIT_20261112.md`, “Verified remote snapshot”.]

There is an additional repository-specific reason not to infer readiness from identical source trees: `tools/product_proof_claims.py::_admission_history` reads retained Git transitions. **History can affect admission checks even when final file contents agree.** A history integration therefore deserves an explicit impact assessment. [W:`tools/product_proof_claims.py`, `_admission_history()` and `_generation()`.]

The practical route is:

1. Preserve the current work tip and all required recovery/evidence refs.
2. When integration work is commissioned, designate one main-derived working branch; the present work branch becomes retained, non-active evidence without rewriting its tip.
3. Apply only the independently reviewed governing changes and separately justified maintenance changes.
4. Promote that exact candidate through an ordinary non-force integration after its actual authority and required checks are satisfied.
5. Continue with one active development branch descended from accepted main.

“One active branch” is an operating classification, **not a requirement to reduce the repository to two refs**. GitHub’s lightweight branch/review model does not override this project’s historical-name dependencies. ([docs.github.com](https://docs.github.com/en/get-started/using-github/github-flow))

## 4.2 Disposition of the eight different paths

| Path | Recommended integration treatment |
|---|---|
| `.github/workflows/m02-l00-transfer-repair.yml` | **DO_NOT_CARRY_FORWARD into active main workflows.** It is executable publication machinery with `contents: write`, downloads and release creation—not harmless documentary evidence. Preserve it on the historical ref. |
| `.python-version` | Retain main’s 3.12.14 until the separately scoped 3.13.5 environment/configuration transition is evidenced and authorised. |
| `AGENTS.md` | Install only the exact reconciled, accepted text—not the work version by default. |
| `EXEC_PLAN.md` | Install the corrected accepted successor, not the recovered local R2 root merely because it is on work. |
| `handoff/review/t01_main_consolidation_20261112/REVIEW_COMMISSION.md` | May be preserved as **unexecuted historical documentary evidence**; it supplies no acceptance. |
| `pyproject.toml` | Hold runtime-target changes with `.python-version`, dependency/lockfile and CI assessment. They are not documentary-only changes. |
| `tests/AGENTS.override.md` | Activate with the accepted root/plan/schedule, including the narrowed rerun wording. |
| `tools/check_sqlite_runtime.py` | Carry with a coherent runtime configuration and invocation contract. On unchanged main, its required `[tool.nvda.runtime]` setting is absent. |

[ `02_BRANCH_COMPARE.md`:10–17; W:`.github/workflows/m02-l00-transfer-repair.yml`; M/W:`pyproject.toml`; W:`tools/check_sqlite_runtime.py`:17–28.]

The 39 PR #2 documentary paths are already in main. They do not need another bulk “consolidation” merge.

## 4.3 Exact refs must remain recoverable under their declared names

Retain all 66 literal entries in `P:ORIGINAL_66_REFS.json`, not merely their 13 unique object IDs. This includes the two original work heads, the original checkpoint tags and every `refs/recovered/...` alias. The five published recovery heads must also remain:

| Literal published ref | Recorded tip |
|---|---|
| `refs/heads/recovery/r2-g0-f02-20261111` | `16b7cc67f5d24336d3768e2da006819474a8c792` |
| `refs/heads/recovery/legacy-d010-20261111` | `77471e5a851ec04e73c6dc63988868064de930f8` |
| `refs/heads/recovery/legacy-d131-20261111` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` |
| `refs/heads/recovery/legacy-m00-brief2-20261111` | `0c86b187a23e750d39ce04f772f7d52c1bd578b0` |
| `refs/heads/recovery/legacy-next20-20261111` | `8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e` |

[P:`ORIGINAL_66_REFS.json`; P:`GITHUB_REMOTE_RECEIVER_RECEIPT.json`; W:`handoff/review/t01_successor_independent_20261111/INDEPENDENT_REVIEW.md` §3.]

Also retain:

- `refs/heads/nvda-imported-g4-20261029`;
- `refs/heads/nvda-m02-g4-imported`;

both recorded at `9bd59acba13ead7252e52e32e1b5d862adecd99a`. Their literal `refs/remotes/origin/...` counterparts occur in both `E:L00/CURRENT_REFS.txt` and `E:L00/L00_MANIFEST.json`. **Their being main ancestors is not deletion permission.**

The 66-ref proof does not cover the entire additional manifest/ref union, including `refs/tags/nvda-union-20261029/...` preservation of otherwise unreachable objects. Keep those records and refs until a complete, independently verified replacement contract is explicitly accepted. [E:`L00/CURRENT_REFS.txt`; E:`L00/L00_MANIFEST.json`, `refs`; P:`BRANCH_CONSOLIDATION_AUDIT_20261112.md`, consolidation steps 4–6.]

Historical ref tips must be interpreted **at their checkpoint**. For example, a historical `refs/remotes/origin/main` value must not overwrite current main during restoration. Use an isolated receiver. The existing `refs/preservation/local-bootstrap-work` mapping resolves the documented `refs/heads/work` versus `refs/heads/work/*` namespace collision; it is not general permission to rename other required refs. [E:`L00/BRIEF.md`, final paragraph.]

**No branch deletion is needed to achieve the recommended operating model now.**

# 5. Technical cross-checks of planning and test claims

These are selected static checks, not a full codebase review or L32 execution.

## 5.1 Current architecture tests contain provably stale expectations

**VERIFIED static inconsistency:** The allocation registry contains M03, admitted on 24 October 2026. Yet:

- `test_identifier_taxonomy.py` expects only M00/M01/M02 allocations;
- it expects the next module to be M03;
- the allocator consumes current registry, retired and allocated IDs before selecting the next identifier;
- `test_registry_schema.py` similarly omits M03 from its expected current object list.

For the supplied registry, the next module candidate should be M04, not M03. [W:`config/architecture/implementation_allocations.yaml`:2–14; W:`src/nvda_desk/architecture/allocation.py`:47–70, blob `1211c0e93c7d5394b9daa0986fb12a467e2b596c`; W:`tests/architecture/test_identifier_taxonomy.py`:32–49, blob `3703e43556c3a04ebf79d9fcaa2564e8b581231c`; W:`tests/architecture/test_registry_schema.py`, first test.]

**INFERRED:** Those assertions would fail if selected against this normal, unpatched configuration. I did not execute them.

This is evidence against an indiscriminate “unchanged tests are unaffected” policy. Configuration admission can materially invalidate a test’s population assumptions without changing that test file.

**Recommended repair principle:** separate immutable allocator fixtures from assertions about current admitted population. Preserve the historical tests/results and the no-ID-reuse proposition. Do not delete M03 or weaken allocation law to obtain green.

The control fixture `_copy_candidate()` also reconstructs an old universe by removing selected items from the evolving live tree. That is a maintenance hazard: it removes M02 while later M03 depends on M02. Review this as a **fixture-universe class**, not another isolated expected-number patch. [W:`tests/architecture/test_proof_control.py`, `_copy_candidate()`; W:`config/architecture/modules.yaml`, M03.]

## 5.2 “Module-local execution” still has global admission coupling

**VERIFIED:** `load_product_proof_claim()` validates fixed extensions, generations, legacy controls and the complete physical test partition before returning a selected claim. Its architecture tests deliberately require corruption in one extension to reject other selected claims. This is intentional integrity coupling, not necessarily a defect. [W:`tools/product_proof_claims.py`, `load_product_proof_claim()`, `_partition()`, `_scalar_extension()`; W:`tests/architecture/test_proof_control.py`, `test_d013_extension_corruption_rejects_every_selected_claim()` and corresponding D014 test.]

Consequences:

- selecting one claim does not mean only that claim’s control metadata matters;
- unadmitted draft test files can obstruct unrelated proof resolution;
- the fixed scalar-extension inventory does not admit the 28 held R2 identities merely because they appear in a plan.

**PROPOSED:** Before the first new R2 implementation, declare the finite necessary proof-control/configuration changes as part of its changed-path scope. The plan’s “only M02 source and necessary M00 projections” wording is insufficient as a complete mutation inventory.

Later, consider one explicit data-driven allowlist instead of repeated identity lists and per-identity table-count code. Do not replace strict admission with arbitrary test discovery.

## 5.3 The strict runner observes outcomes, but does not enforce the R2 budget

The runner usefully rejects dirty starts, unready targets, historical non-runnable claims and governed mutation. Its plugin checks fresh report identity, collection and setup/call/teardown outcomes. [W:`tools/run_product_proof_gate.py`:24–82; W:`tools/product_proof_outcomes.py`:56–107.]

But **VERIFIED by inspection**:

- parameter suffixes are stripped from collected node IDs;
- required test names are checked as a **subset**, not an exact set;
- these files do not consult the R2 allocation ledger or enforce its two/four/six physical-case limits;
- the detailed outcomes report is created inside a temporary directory, so it is not itself retained by this runner after completion.

[W:`tools/product_proof_outcomes.py`:79–88; W:`tools/run_product_proof_gate.py`:47–70.]

Pytest creates separate nodes for parameterised cases, so function-name presence is not a physical-case census. ([docs.pytest.org](https://docs.pytest.org/en/stable/example/markers.html))

**PROPOSED:** Bind admitted case identities—including parameter variants—to the execution manifest; check exact expected collection and retain the raw outcome report. One batch receipt can contain all case outcomes. This need not produce one administrative document or owner permission per assertion.

## 5.4 Runtime targets, actual execution and CI remain different propositions

**VERIFIED:**

- main pins Python 3.12.14; work pins 3.13.5 and records SQLite 3.54.1;
- `check_sqlite_runtime.py` compares actual Python/SQLite versions and reports `sqlite_source_id()`;
- the product runner does not invoke that preflight;
- `export_m00_synthetic.py::run()` still explicitly rejects any interpreter other than 3.12.14;
- the workflow runs `uv sync --locked`, whole-tree Ruff and the architecture promotion gate on pull requests;
- the architecture type-check test invokes mypy over all `src`.

[M/W:`pyproject.toml`; W:`tools/check_sqlite_runtime.py`:17–44; W:`tools/run_product_proof_gate.py`:24–82; W:`tools/export_m00_synthetic.py`, `run()`/`python_pin`; W:`.github/workflows/architecture-kernel.yml`:3–19; W:`tests/architecture/test_static_typecheck.py`, first test.]

Python documents `sqlite3.sqlite_version` as the **runtime library version**, supporting the distinction between a configuration pin and the actual loaded engine. ([docs.python.org](https://docs.python.org/3/library/sqlite3.html))

**Consequences:**

- A copied runtime pin is not qualification.
- The old exporter is not automatically portable to 3.13.5. It may remain a historical tool; it should not be casually “fixed” or rerun.
- The CI workflow is broader than the documentary/narrow-validation prose. Its actual scope and applicable branch rules must be reconciled before promotion—not bypassed.
- Default pytest discovery covers architecture/bootstrap, not the new R2 signal proofs. A default green would not establish L32 completion.

**UNKNOWN:** current `uv.lock` compatibility, complete CPython-3.13 dependency availability, actual Ubuntu linkage and current required GitHub checks.

Historical 3.12/SQLite results remain true about their original environment. They do not become 3.13 qualification by reuse, but neither should all be rerun reflexively.

## 5.5 The history-support requirement is real—and may be larger than four profiles

The shown `_underlying_returns.py` fixes `T` to **20 October 2026 at 12:40 UTC**, a particular prior close and two permitted knowledge cut-offs. D076 and D077 then validate actual predecessors against that controlled implementation. Those profiles cannot simply supply a rolling, multi-date four-vector training history. [W:`src/nvda_desk/market_measurement_truth/_underlying_returns.py`:22–35, 98–144, blob `fe938f52de364d596ef4f9e4c52c9d7132171a88`; `_relative_market_return.py`:65–89; `_relative_sector_return.py`:65–91.]

**Material planning implication:** D076 depends on D072/D071; D077 depends on D073/D074/D072. Generalising the selected history route may require affected **D072–D074** profiles as well as the four named supporting histories. Another admitted route may exist in omitted source, so this is not a universal absence finding.

Before committing to the support allocation, inspect that dependency closure. **Do not silently exceed 74 cases, inject expected returns as raw inputs, or assume the existing four support pairs cover every changed producer.**

## 5.6 The K06 fixture is correct arithmetic but weak discrimination

I independently recomputed the supplied literal 64-row CSV using exact rational arithmetic:

- 64 distinct slot IDs;
- eight distinct numeric rows repeated eight times;
- Gram matrix diagonal  
  `64, 4/625, 64/15625, 36/15625`;
- exact coefficients: intercept `0.0002`, betas `1.50`, `0.40`, `0.70`.

The reconstructed CSV SHA-256 matches the recorded `addb2051a69373bb3a88dfb9a69c115449d52d3fbe393a190b5eaaf654d556fe`. **This was documentary arithmetic, not execution of M02 OLS.** [Q:`SYNTHETIC_K06_64ROW_FIXTURE.csv`:1–65; Q:`RESTART_INDEPENDENT_REVIEW.md`, literal-arithmetic discussion.]

Because the factors are orthogonal, separate univariate regressions can yield the same slopes. A zero-residual example also fails to discriminate an implementation that simply returns zero. The plan’s correlated fixture, informative nonzero residual and per-coefficient mixed-fit refusal are therefore **necessary engineering assurance, not redundant ritual**. [W:`EXEC_PLAN.md`, L01a–L03.]

## 5.7 Native-shaped evidence does not close different source contracts

Two selected implementations support the plan’s distinctions:

- `_native_option.py` assembles four quote roles with specified skew/age constraints. It does not thereby provide option prints, their trade direction or multiplier provenance for D120.
- `_native_book_insert_rate.py` explicitly requires collector-receipt timing, `event_time_utc=None`, receipt-only temporal kind and absent provider timestamp/timezone. That evidence cannot satisfy D145’s retained event-clock requirement.

[W:`src/nvda_desk/market_measurement_truth/_native_option.py`:20–38, 58–114, blob `1861b129f7a2b568433392873a3a2179c48ecc56`; `_native_book_insert_rate.py`:62–92, blob `e56f161e0fbb5dfee6b6ddf2d73d27b3f7cd3963`; W:`EXEC_PLAN.md`, L19–L20 and L31.]

Likewise, D142’s shock at `t=1` and recovery at `t=7` imply six seconds; an inclusive 30-second no-recovery window must reach `t=31`. The older untimed seven-second example is a different example, not evidence to overwrite the timed oracle. [W:`EXEC_PLAN.md`, L01c/L05.]

**D145 stays paused.** The missing primary source bodies prevent any broader conclusion about all possible provider capabilities.

## 5.8 Workbook derivatives are research/navigation evidence, not current ownership law

PASS06 assigns “M02” to data-quality scoring and places D151 in a working M03 group. The current registry instead uses M02 for neutral measurement and M03 for configured conditions. The CSVs label these earlier allocations `WORKBOOK_DESIGN_ONLY` or `REVIEW_ONLY`. They must not be used to reallocate current runtime owners. [W:`handoff/workbook_v2/pass06_modules/PASS06_30_MODULE_REGISTER.csv`:2–3; W:`handoff/workbook_v2/reviews/excluded_95_provenance_20261014/NVDA_EXCLUDED_95_PROPOSED_GROUPS.csv`, P01/P02; W:`config/architecture/modules.yaml`.]

The historical G01 D025 finding is also not automatically a current defect: the selected M02 `_session_range.py` maps R039 to high, R040 to low and calculates `(last-low)/(high-low)`. For the recorded 120/80/90 witness, that expression is 0.25. This is a static cross-check, not a fresh runtime pass. [W:`handoff/workbook_v2/g01/G01_L3_FINDINGS.csv`:2; W:`src/nvda_desk/market_measurement_truth/_session_range.py`, `MAPPINGS` and `produce()`.]

For D151, the preserved cross-check already reports a percent-output rule against fractional example arithmetic. Verify the original K02 clause before treating representation as a fresh policy choice: an explicit fraction-to-percent encoding may be an implementation consequence of settled law. Basket membership and weighting remain separate substantive questions. [W:`handoff/m02_remaining_readiness/L05_D151_UNIT_CROSSCHECK.md`; Q:`L02_FINDINGS.md`, “D151 numeric boundary”.]

No full workbook audit or new appraisal of the cited research papers is claimed.

# 6. Dependency-ordered recommendation

## 6.1 One course of action

All operational steps below are **proposed follow-on work**, not actions authorised or performed by this report.

### Step 1 — Prepare one reconciled transition candidate

**Worker:** prepare a main-based candidate containing:

- one concise active AGENTS;
- one successor ExecPlan;
- matching test-local instructions and ledger scheduling;
- a current-state summary separating accepted history, present holds and proposed work;
- explicit treatment of all eight differing paths;
- the unchanged 39 semantic leaves, 35 obligation identities and D145 pause;
- the finite control-maintenance scope exposed in §5.

Use the current pinned main/work snapshots, not the old commission’s moving branch names. Preserve the old commission and prior reports; do not relabel them as reviews of this candidate.

**Independent reviewer:** inspect changed meaning, dependency/schedule changes, proof controls and source provenance. Reuse earlier exact documentary results where still applicable. Report all material findings within the bounded scope.

**Acceptance evidence:** exact candidate/base/tree, allowlisted diff, governing file identities, obligation comparison, preserved historical evidence and a disposition of each finding.

### Step 2 — Obtain one exact owner transition decision

The owner should make **one decision on the reviewed package**, expressly covering:

- exact governing-text adoption and installation;
- designated work branch and checkpoint strategy;
- bounded Worker/reviewer/Tester roles;
- the recommended testing-window amendment;
- authorised environment preparation;
- continued execution of eligible work and bounded repairs;
- whether that exact governance candidate may be promoted to main once stated checks succeed.

This can combine acceptance, installation commissioning and standing execution authority. It need not require three separate conversations.

Do **not** bundle in undefined source policies, extra case allocations, PostgreSQL product admission, live operations or D145 reactivation.

### Step 3 — Close receiver and environment prerequisites separately

**Independent receiver:** verify the new pinned candidate, complete required-ref contract and relevant non-Git assets. Reuse the 11 November 66-ref result for its exact original proposition; add the missing current/additional coverage rather than repeating it without reason.

**Environment worker and independent verifier:** establish the authorised Python/SQLite environment and execution evidence contract. Resolve lockfile/dependency and historical-export-tool treatment. Bind actual execution identity to retained test outcomes.

**Parallel work:** documentary source-contract preparation can proceed where authorised and independent of these runtime checks. Additional M00 PostgreSQL contract analysis can also proceed separately.

**Stop:** missing required Git objects/assets block the affected handover; an unsuitable environment blocks dependent execution. Neither automatically blocks unrelated documentary investigation.

### Step 4 — Complete one narrow controlled slice before expanding untested work

**PROPOSED first candidate:** L01b → L04, D091. This is a prioritisation judgement, **not a finding that its contract is already ready**.

Require an admitted R112 variant/scale/identity contract, exact bin version, finite oracle/case allocation, ordinary public ingress, reached refusal and durable readback. The Worker implements; the separate Tester executes at the newly accepted boundary.

This first slice should demonstrate the entire streamlined route once: contract → implementation → independent proof → durable receipt, without repeated owner “continue” requests.

If D091’s substantive contract cannot be released, retain its blocker and select another genuinely eligible unit; do not fabricate readiness to preserve the preferred order.

### Step 5 — Advance by actual dependency, not gate number

Retain these principal chains:

| Chain | Release order |
|---|---|
| Shared fit | L01a support closure → L02 D079–D081 → L03 D078 |
| Option dates and ATM IV | L07a → L08; L10b + L08 → L12 → L13/L14/L15/L16 |
| Option instants and density | L07b → L09; L09 + L10b/L10c → L24 → L25 → L26 → L27/L28 |
| Straddle | L01b/L04 + L10c → L17 → L18 |
| Option flow | L19 → L20; L20 + L04 → L21; L20 + L08 → L22 |
| Microstructure | L01c → L05; L01d → L06; L19 + required attribution contract → L29 |
| Other independent obligations | L23 event contract/output; L30 basket contract/output; L31 paused-D145 disposition only |

[W:`EXEC_PLAN.md` §§2–3; E:`EXECUTION_REGISTER.json`, `depends_on`.]

Under the current graph, **L00 is the sole root and all other 38 leaves depend on it**. There is no already-ready downstream escape while its applicable release conditions remain unmet. After release, a blocker in one chain must not idle unrelated ready chains.

**Tester:** owns independent proof adequacy, execution and disposition.  
**Worker:** owns repairs.  
**Owner:** receives only genuine reserved decisions, consolidated with concrete options and consequences.

### Step 6 — Close L32 and promote only what is actually accepted

L32 should reconcile:

- exact new accepted identities and required instrument variants;
- supporting-profile evidence;
- reused historical evidence with its original scope;
- all 28 dispositions and seven external holds;
- unresolved production/source qualifications;
- final recoverability.

Any mandatory unaccepted output means **PARTIAL/BLOCKED**, even if core20 is achieved. Maximum controlled accounting remains 98 + 27 = 125 while D145 is paused. Main promotion remains an explicit authority boundary, not an automatic consequence of a push, a green control check or continuous execution. [W:`EXEC_PLAN.md` §6; P:`ADR_20261112_CONTINUOUS_EXECUTION.md`:19.]

## 6.2 Precise stop conditions

| Condition | Stop what? | What may continue? |
|---|---|---|
| Candidate/hash or governing revision differs from the reviewed target | Acceptance/promotion of that changed target | Bounded delta assessment |
| Required source meaning, units, clock or selection policy is unresolved | That implementation and dependent descendants | Independent contract investigations |
| Proof allocation is unreleased or inadequate | Affected product execution/acceptance | Finite proof design and unrelated admitted cases |
| Required runtime/backend is unsuitable | Dependent execution | Unrelated documentary work; independently qualified backend work |
| Required ref/asset cannot be recovered | Affected checkpoint/release | Work with a separate valid checkpoint and no dependency on the missing material |
| Product proof fails | Dependent acceptance; preserve first failure | Independent cases; bounded Worker repair |
| Required CI/protection conflicts with authorised scope | Main promotion | Scope reconciliation and independently authorised work |
| Live effects, purchases, new external operations or D145 reactivation are requested without authority | Those actions | Existing authorised work |
| Tool/session/context limit is reached | Current execution turn | A truthful checkpoint and precise resumption instruction—not a background-work promise |

## 6.3 Minimal suggested governance wording — report only

The following is a proposed common clause, not an installed amendment:

> **Standing commission.** Once the owner accepts and commissions the exact plan and governing amendment, continue all eligible actions within its named scope, roles, branches and checkpoint strategy through close-out without routine owner reapproval. Evidence gates remain mandatory; they do not create a new permission gate.
>
> **Independent proof.** Only the designated independent Tester may execute admitted product cases at the boundary specified by the accepted plan. Documentary clearance is not product acceptance. A failed case may rerun after documented relevant material repair; a successful proof may rerun only after documented material invalidation. Additional cases require a finite admitted allocation before execution.
>
> **Reserved decisions.** The standing commission does not supply missing source facts, new domain/source policy, an expanded proof budget, a changed checkpoint strategy, frozen-governance amendment, main-promotion authority, unapproved external operations or D145 reactivation. Use existing authority where it already settles the question.
>
> **Local stopping.** Preserve the first unmet invariant and stop dependent actions. Continue independently authorised work; if none is eligible, report the exact blocker. At a session limit, record the verified checkpoint and next step without claiming background continuation.

The separate testing-window amendment would still need explicit, consistent changes to the plan, L32 entry conditions, override and ledger.

## 6.4 Missing sources that could materially change the next action

These absences do not prevent the methodology recommendation. They prevent stronger readiness or implementation conclusions.

| Exact source needed | Why it matters |
|---|---|
| `handoff/planning/m02_foundation_completion_20261030/PROOF_ALLOCATION_PROPOSED.json` and `LEAF_REGISTER.json` | Exact physical case IDs, proof paths and canonical dependency bindings are referenced but not supplied in full. |
| `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`; its catalogue CSV; `D138_D145_L2_OWNER_APPROVED_DEPENDENCY_AMENDMENT_20261016.md` | Primary K-law, unit and overlay reconciliation before changing a source/profile contract. |
| `handoff/m02_remaining_readiness/COMPLETION_REGISTER.json`, `UNRESOLVED_REGISTER.json`, `EVIDENCE_REUSE.json`, `L05_PROOF_REUSE_AUDIT.json` and linked original logs | Complete per-profile evidence and material-invalidation assessment; summaries do not replace these bodies. |
| `src/nvda_desk/market_measurement_truth/api.py`, `_window.py`, `_native_source.py`, `_native_profiles.py`; M00 `api.py`, `_sqlite.py`, `_postgres.py` | Public dispatch, history, native-source and backend reachability; these are index-only in the supplied coverage. |
| `handoff/planning/ubuntu_postgresql_transition_20261110/ADR_20261110_POSTGRESQL_ADDITIONAL_BACKEND.md`, its `EXEC_PLAN.md` and `T00_F02_INDEPENDENT_BOUNDED_REVIEW_20261110.md` at `465de451d9c0bcd055d6385c0fc5d10cb9c49013` | The supplied November review reports reading them, but their primary bodies are absent here. Needed before deciding new PG scope or reusing the exact F02 disposition beyond its reported limits. |
| `uv.lock`, applicable `vendor/wheels` inventory, external CPython-3.13 wheelhouse manifest and actual SQLite assets | Whether the proposed runtime is reproducible on the actual receiving host. |
| `config/proof/test_families.yaml`, `proof_blocks.yaml`, `promotion_sets.yaml`, plus current GitHub branch-protection/ruleset and required-check readback | Exact mandatory validation and promotion requirements. |
| Earlier proposal blobs at `aa8dc236…`, and the exact later candidate delta from `0909250ca…` to the packet tip | Required for a formal byte-bound amendment review; the earlier report cannot certify changed bytes. |
| `docs/automation/CHATGPT_GITHUB_HANDOVER_UIA_20261110.md` | Primary operational limits before relying on that handover method; this review has only its attributed assessment. |

**Final judgement:** NVIDIA V2 needs less repeated administration and earlier focused engineering feedback—not fewer truthful boundaries. Preserve the semantic obligations, independent Tester and recoverable evidence; replace repeated permission requests, duplicate current-state narratives and whole-history transfer rituals with one bounded standing commission and explicit dependency-based release.
<!-- END ASTRA RESPONSE 1 — VERBATIM ORIGINAL BYTES -->

---

## Astra response 2 — Supplementary product architecture, IBKR, dependencies and UI review

<!-- BEGIN ASTRA RESPONSE 2 — VERBATIM ORIGINAL BYTES -->
I’ll focus this supplement on the first useful product slice and the integration work it needs, rather than repeating the repository clean-up recommendations. I’ll check current primary documentation for IBKR, Streamlit and the relevant Python tooling, and distinguish documented capabilities from account-dependent access and unmade product decisions.# NVIDIA V2 — Supplementary Independent Product-Engineering Assessment

**Assessment date: 12 November 2026**  
**Scope: architecture, integration and delivery recommendations—not implementation or acceptance.**

Repository references retain the original pins:

- **W:** `repository/work/` at `a3a3e23e58e313328a6bb22ab72d7a706cfa7aab`.
- **M:** `repository/main/` at `ded4b98e1e5999d1ddf2f067e660b691917bcd71`.

**VERIFIED** denotes supplied repository evidence or current primary documentation. **INFERRED** denotes an engineering assessment. **PROPOSED** denotes a future decision or action. No GitHub changes, product tests, installations or broker sessions were performed.

## 1. Executive conclusion

**Build an owner-usable measurement and replay workbench before expanding the indicator catalogue further. Then connect one narrowly qualified, read-only IBKR data source to that same path.**

My previous D091-first suggestion concerned advancing the existing R2 implementation backlog. For the broader product objective now commissioned for assessment, I would prioritise **a small application using existing D011/D012 midpoint/spread semantics**, with visible provenance, refusal handling and durable readback.

### Direct answers to the owner’s questions

| Question | Independent assessment |
|---|---|
| **Are we building the right thing?** | A trustworthy measurement foundation is useful. A completed numbered signal catalogue is not, by itself, a usable research or trading product. The next objective should be an observable workflow that answers an owner’s question reliably. |
| **Are we building it in the right order?** | **Not if another large calculation tranche or database transition precedes a useful application path and broker-source feasibility check.** Source suitability, operational behaviour and usability now deserve priority alongside—not after—mathematical correctness. |
| **What are we overengineering?** | Repeated profile-specific plumbing, broad proof machinery around small changes, and potentially expanding numerical machinery before demonstrating demand. Avoid adding microservices, plugin systems, a universal indicator engine or simultaneous backend migrations. |
| **What is under-planned?** | Actual capture identities, account entitlements, session recovery, data freshness and gaps, diagnostic explanations, installed-package operation, storage growth, operator interaction and eventual order reconciliation. These were often intentionally excluded from the current kernel; they must now become explicit product work. |
| **What should we build first?** | An **offline NVDA Measurement & Replay Workbench**: select an approved dataset, calculate a small accepted measurement set through public interfaces, inspect results and provenance, explain unavailable results, close/reopen storage and reproduce the run. No broker orders. |

The current registry expressly excludes provider/network integration and live external effects from M00/M02, and A00’s declared dependency is M00—not M02. Therefore this application slice needs a **bounded composition/admission extension**, not an assumption that a UI may bypass those boundaries. [W:`config/architecture/modules.yaml`, M00/M02 exclusions; W:`config/architecture/application_shells.yaml`; W:`config/architecture/dependency_rules.yaml`:24–41.]

### The dominant new risk

**IBKR may not supply every source proposition that the eventual options/microstructure product needs.** Its documentation distinguishes aggregated watchlist updates from tick-by-tick feeds, states that real-time tick-by-tick data is unavailable for options, and lists important historical-data exclusions, including expired options. Completing more mathematics cannot resolve those limitations. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/md/streaming-data))

**Recommendation:** investigate those source requirements early, while building the offline product independently. Do not make all future usefulness depend on the hardest option-flow or depth feature.

**D145 remains PAUSED.**

---

## 2. Proposed minimal architecture and interfaces

### 2.1 One modular application, not a distributed platform

**PROPOSED initial deployment assumption:** one owner, one Ubuntu execution environment, local storage and a local browser interface. This is not a low-latency execution platform or a multi-user hosted service.

Use **one Python distribution and two project processes**:

1. **Engine/application process:** finite replay jobs initially; a long-running capture service when broker integration arrives.
2. **Streamlit process:** presentation, queries and submission of explicitly permitted application commands.

TWS or IB Gateway is an additional vendor application, not part of the Python engine.

| Responsibility | Recommended boundary |
|---|---|
| **Broker/source adapters** | Manage transport, requests, subscriptions and decoded callback envelopes. Preserve provider facts; do not calculate indicators or reinterpret absent timestamps. |
| **M00 raw occurrence truth** | Continue owning raw occurrences, source/receipt distinctions and lawful public projections. Adapter convenience must not redefine raw truth. |
| **M02 temporal and neutral measurement truth** | Own admitted temporal interpretation, selection, book reconstruction and neutral indicators under versioned definitions. “Derived indicator” does not automatically mean legacy M01. |
| **M03 configured conditions** | Retain its admitted configured-composite responsibility. Do not turn it into a universal strategy framework. |
| **Research/experimentation** | Consume immutable public facts and versioned extracts. Experimental features, models and parameter searches remain separate from accepted production definitions. |
| **Persistence adapters** | Implement owner-local storage contracts. SQL, schema and drivers remain mechanisms—not semantic owners. |
| **Proof/validation** | Keep release/admission machinery outside the market-data processing loop. Runtime contract validation remains where required. |
| **Execution control and broker orders** | A later, separately admitted responsibility for approved intents, limits, submission and reconciliation. Neither a measurement nor a research score may directly place an order. |
| **UI/application composition** | Non-owning orchestration and presentation through declared public interfaces. No private imports or direct cross-owner SQL. |

This direction reuses the current public-seam and non-owning-composition model. It does **not** require allocating a new architecture ID for every adapter, screen or calculation. M01 remains bootstrap unless separately changed. [W:`config/architecture/modules.yaml`; W:`src/nvda_desk/composition/__init__.py`, `Application` and `create_application()`; W:`config/architecture/governance_planes.yaml`.]

### 2.2 Keep the interface set small

Introduce only the interfaces needed by the first use case:

- **Source input:** decoded messages plus explicit connection/gap/control events.
- **Raw reads:** existing M00 projection/history interfaces.
- **Measurement request:** existing owner-specific calculation requests and read facets.
- **Workbench query:** result, lineage, run metadata and operational status.
- **Execution port:** absent from the first release; introduced only with paper-execution authority.

Use typed dataclasses, enums and small `Protocol` interfaces. Do not expose broker SDK objects, database connections or mutable DataFrames across semantic owner boundaries.

Three distinctions are especially important:

1. **Broker instrument identity is not occurrence identity.** An IBKR `conId`, an R/D catalogue ID and a raw occurrence ID are different things.
2. **A new application run is not necessarily new measurement truth.** Identical logical inputs may legitimately resolve to an existing immutable occurrence.
3. **A retransmitted provider observation is not automatically an idempotent command retry.** Do not deduplicate raw observations merely because prices or timestamps match.

The existing typed identity and retry rules provide useful foundations for these distinctions. [W:`implementation/authority/VI10R6_SIGNAL_CATALOGUE_CARRIAGE.md`, “Identity separation”; W:`implementation/authority/VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md` §§2–4; W:`src/nvda_desk/market_measurement_truth/_record_store.py`, `_existing()`.]

### 2.3 Generalise profiles incrementally—not the entire engine

**VERIFIED:** selected implementations bind particular providers, instruments, timestamps and cut-offs. For example, `_underlying_returns.py` fixes a particular October observation frame. That is controlled-profile implementation, not a general rolling-history service. [W:`src/nvda_desk/market_measurement_truth/_underlying_returns.py`:22–35, 98–128.]

**PROPOSED:** when a real use case requires generalisation:

- separate the calculation from its versioned input-selection/configuration profile;
- retain the old controlled profile unchanged;
- introduce a distinct new profile with its own source and numerical obligations;
- reuse owner-local plumbing where genuinely identical.

The nearly repeated native depth read/store wrappers are candidates for later internal consolidation, but not justification for a wholesale rewrite. [W:`src/nvda_desk/market_measurement_truth/_native_smart_depth.py`, `_Reads`; `_native_smart_ask.py`, `_Reads`.]

Similarly, preserve accepted exact-ratio and rounding contracts. Do not make fifty-digit certified arithmetic a universal requirement for every future research computation merely because existing profiles use it. New numerical requirements should follow the calculation’s error budget and accepted meaning. [W:`src/nvda_desk/market_measurement_truth/_log_return.py`, `_logarithm()`; `_numeric_bounds.py`, `sqrt_ratio_50()`.]

### 2.4 Storage: local first, explicit transition later

**Recommended direction:** retain SQLite for the single-owner prototype; treat PostgreSQL as the intended server-store option when demonstrated concurrency, access-control or operational requirements justify it.

SQLite’s own guidance supports local application storage and distinguishes that use from networked, multi-writer workloads. That is a fit argument—not production qualification of these implementations. ([sqlite.org](https://www.sqlite.org/whentouse.html))

Apply the following design:

- **Owner-local truth stores:** retain current M00/M02/M03 ownership and files/namespaces.
- **Operational journal:** keep session state, jobs, reconnect attempts and diagnostics separate from market truth.
- **Immutable run artefacts:** preserve dataset references, profiles, source/configuration versions, code commit, environment fingerprint and result hashes.
- **Research extracts:** publish versioned, read-only datasets. Add columnar storage only when actual analysis size warrants it.
- **Git:** retain code, contracts and small manifests. Store growing captures and logs in managed artefact storage with backups, not an ever-expanding source tree.

Do not claim atomicity across all owner stores. A raw observation may be committed while its measurement remains pending. Publish a completed run manifest only after its referenced outputs are durable; expose partial progress honestly.

**VERIFIED scaling concern:** `RecordState.all()` loads and validates the whole record population; append paths also reload records. **INFERRED:** this can become expensive under sustained capture and frequent UI queries. Measure the selected path before deciding that PostgreSQL, caching or another database is the answer. [W:`src/nvda_desk/market_measurement_truth/_record_store.py`, `_load()`, `all()`, `append()`.]

#### Migration policy

The current stores bind exact schema, application ID and connection policy, including rollback-journal expectations. A generic migration or WAL switch could invalidate those assumptions. [W:`src/nvda_desk/market_measurement_truth/_record_store.py`, `_schema()` and `_transaction()`; `_rational_sqlite.py`, `_schema()` and `_connect()`.]

Therefore:

1. Do not mutate accepted historical databases in place for the prototype.
2. Prefer a new versioned store and an explicit, verified conversion when required.
3. For newly admitted evolving stores, use ordered, checksummed migrations with recorded schema versions.
4. Test restoration and conversion through public reads, including identity, units, timestamps and provenance—not row counts alone.
5. Distinguish schema version from calculation-definition version.
6. Use a consistent database backup mechanism, rather than assuming copying a live file is sufficient. SQLite supplies an online backup API for this purpose. ([sqlite.org](https://www.sqlite.org/backup.html))

Existing PostgreSQL evidence remains valuable, but neither the historical proof environment nor the proposed additional M00 backend is a production storage decision. The actual M00 adapter body and new deployment configuration still require inspection and qualification. [W:`implementation/authority/VI03_POSTGRES_EXECUTION_CAPABILITY.md`, scope; W:`handoff/planning/t01_recovered_successor_20261111/PROPOSED_EXEC_PLAN.md` §10.]

---

## 3. Concise dependency and package policy

### 3.1 Select a small stack, then lock a tested combination

**PROPOSED stack:**

- existing standard-library calculation/types/storage mechanisms;
- PyYAML where already required;
- Streamlit as a **UI extra**;
- official IBKR Python API as a **broker extra**;
- Psycopg 3 only for the separately admitted PostgreSQL deployment;
- existing pytest, Ruff and mypy development tools;
- a full JSON Schema validator in validation tooling where full Draft 2020-12 behaviour is required.

Do not add an ORM, message broker, distributed task queue, web API framework, technical-analysis library or machine-learning platform merely to establish “architecture”.

NumPy/SciPy may become justified for a specific admitted numerical requirement. Avoiding all dependencies is not a good reason to hand-build a constrained optimiser. Conversely, installing them does not establish that their algorithms satisfy the accepted K-law or precision contract.

### 3.2 Current upstream observations—not an approved compatibility matrix

| Component | Verified current documentation | Recommendation |
|---|---|---|
| **Python** | Python.org lists **3.13.18**, released 25 October 2026; the 3.13 series is in security maintenance. The current feature series is 3.15. | Keep the already-selected 3.13 minor line for the first product slice, but qualify the current security patch rather than perpetuating 3.13.5. Do not introduce another minor-version migration just to follow “latest”. ([python.org](https://www.python.org/downloads/)) |
| **Streamlit** | Opened release notes identify **1.67.0**, released 5 November 2026. Installation documentation supports Python **3.11–3.15**. | A suitable candidate for the UI extra, subject to the actual locked environment and application tests. ([docs.streamlit.io](https://docs.streamlit.io/develop/quick-reference/release-notes)) |
| **IBKR API** | The official download page lists **1052.01 Latest**, dated 30 October 2026, and identifies Python in that package. IBKR documents Python **3.11.0 minimum**. | Obtain the official Python-containing distribution; verify its actual contents and record the paired TWS/Gateway build. Do not invent a corresponding PyPI version pin. ([download2.interactivebrokers.com](https://download2.interactivebrokers.com/installers/tws-api/index.html)) |
| **Psycopg** | Current Psycopg 3 documentation lists Python **3.10–3.15** and PostgreSQL **10–18** support. | Retain this driver family; choose and qualify the exact package/client-library combination when the PG increment is reached. Documentation support is not proof for the repository’s existing 3.3.4 environment. ([psycopg.org](https://www.psycopg.org/psycopg3/docs/basic/install.html)) |

The repository presently pins different main/work Python versions and retains an offline wheelhouse configuration. Those are existing facts, not permission to update them here. [M/W:`pyproject.toml`:10, 18–24; W:`pyproject.toml`:75–84; `06_TOOLCHAIN_VERSION.md`.]

### 3.3 Reproducibility without permanent dependency stagnation

Use the existing `pyproject.toml`/uv direction:

- commit the application lockfile;
- use locked installation in CI and releases;
- separate core, UI, broker and test dependency groups;
- bind external SDK artefacts and offline wheels by provenance and digest;
- record Python, linked SQLite, OS/architecture and relevant native client libraries;
- review security advisories and perform bounded upgrades.

uv distinguishes ordinary resolution from `--locked` operation, which refuses a stale lock instead of changing it. Preserve that distinction in release procedures. ([docs.astral.sh](https://docs.astral.sh/uv/concepts/projects/sync/))

IBKR explicitly says third-party package repositories—including pip-hosted distributions—are not its supported API distribution route. The official SDK must therefore be treated as an identified external build input, not replaced by an arbitrary package named `ibapi`. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/download-the-tws-api))

For Psycopg, record which implementation and `libpq` are actually loaded. Binary and system-linked installations have different dependency-update behaviour; the pure Python package still needs a usable client library. ([psycopg.org](https://www.psycopg.org/psycopg3/docs/basic/install.html?trk=article-ssr-frontend-pulse_little-text-block))

### Packaging acceptance should be practical

Build a wheel and prove the selected application works **outside the source checkout**. Required runtime catalogues/configuration must be packaged resources or explicit deployment assets—not accidental dependencies on the current working directory or an entire `handoff/` tree.

The current package uses a `src` layout, while some code loads adjacent catalogue data and repository-relative configuration. This warrants a deployment test, not an assumption that source-tree execution proves packaging. [W:`pyproject.toml`:27–53; W:`src/nvda_desk/derived_signal_calculation_truth/_catalogue.py`, `catalogue_rows()`; W:`src/nvda_desk/architecture/registry.py`, `from_repository()`.]

Keep the existing build backend unless a concrete problem requires change. Standard Python packaging supports building wheels through the declared backend; a new packaging framework is unnecessary. ([packaging.python.org](https://packaging.python.org/en/latest/guides/tool-recommendations/))

---

## 4. IBKR integration approach

### 4.1 Choose the official TWS Python API

**PROPOSED:** use the official Python API with a small callback adapter. Begin against TWS so the owner and tester can inspect corresponding platform information. Move the same adapter to IB Gateway when longer-running paper/shadow operation is justified.

TWS and IB Gateway expose the same socket API interface after authentication. Gateway is the lighter host, but it does not eliminate login, restart or reauthentication requirements. IBKR recommends becoming familiar with TWS first. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/download-tws))

Do not start a new integration on `ib_insync`. IBKR identifies it as no longer updated; it also distinguishes `ib_async` from its directly supported implementation. The official API now has a Python synchronous wrapper, but its availability does not require adopting a second application abstraction. For this event/provenance-oriented system, explicit callback handling is a reasonable first choice. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/third-party-api-platforms))

Do not simultaneously implement TWS API and Web API authentication paths. One qualified route is enough initially.

### 4.2 Authentication belongs to the broker host—not Streamlit

**VERIFIED:** TWS/Gateway authentication requires the user’s broker login, with supported 2FA; IBKR does not support treating the host as a permanently headless authenticated service. Daily restart and periodic manual reauthentication must be accommodated. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/download-tws))

**PROPOSED controls:**

- keep broker credentials and 2FA out of source, prompts, CI and the UI;
- use a named, non-conflicting API client ID—not as an authentication credential;
- keep the first broker host/API configuration **read-only**;
- prefer local connectivity; verify Windows/WSL address behaviour explicitly if they are split across environments;
- require handshake completion and expected account identity before declaring API readiness.

IBKR documents the handshake and `nextValidId` readiness boundary; sending requests too early can lose them. Receiving an order ID does not authorise submitting orders. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/connectivity/establishing-an-api-connection))

The owner’s unavoidable operational work is broker authentication and genuine account decisions—not repeated software-leaf approval.

### 4.3 Establish an account capability inventory before requesting data

**UNKNOWN for this project:** actual account type, broker entity, subscriptions, API acknowledgements, paper-user sharing, trading permissions and available line quotas.

Before a live-data increment, establish:

| Capability | Evidence required |
|---|---|
| API account access | Actual eligible account/user, supported authentication and enabled socket/API access |
| Stock quotes | Off-platform entitlement for the selected instrument and required venue/consolidated coverage |
| Options/Greeks | Relevant option and underlying subscriptions; exact computation variant |
| Market depth | Required exchange/SMART-depth permissions and capacity |
| Paper data | Actual paper-user entitlement/sharing arrangement and concurrent-session constraints |
| Data use | Applicable API acknowledgement, storage/display/sharing permissions and approved cost envelope |

Seeing a quote in TWS does **not** establish API entitlement. IBKR distinguishes on-platform from off-platform data and requires a Market Data API Acknowledgement. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/general/market-data-subscriptions/tws-data-vs-api-data))

Option Greeks require subscriptions for both the option and underlying; paper-market-data access is user/sharing dependent. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/md/option-greeks))

### 4.4 Start with one NVDA stock quote stream—not an option-chain collector

**PROPOSED first live source:** one qualified NVDA stock contract and one `BidAsk` tick-by-tick subscription, conditional on actual entitlement and capacity.

That callback supplies bid, ask, sizes and a provider-reported tick timestamp together. It is a better first source candidate for a midpoint/spread slice than pretending independently delivered watchlist fields are an atomic quote. Preserve the timestamp’s documented meaning; do not rename it “exchange event time” without evidence. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/md/live-ticks))

This still needs a **new live-source profile**: instrument resolution, mapping, native numeric conversion, temporal interpretation and admissibility. Do not feed it into a synthetic profile under the old provider label.

Keep three feed concepts separate:

- `reqMktData` streaming watchlist updates are aggregated snapshots, not a complete tick tape;
- a one-shot snapshot can return fields over an approximately eleven-second collection window and is not guaranteed to return every field;
- regulatory snapshots are a separately paid request mode, not a harmless fallback. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/md/streaming-data))

No UI refresh should create another broker subscription. Maintain one desired-subscription registry and cancel subscriptions explicitly when no longer needed.

### 4.5 Pacing and history are application constraints

Implement a small request scheduler with separate limits for general requests, historical retrieval and specialised subscriptions.

IBKR currently documents general pacing as market-data lines divided by two per second: the default 100 lines corresponds to 50 requests/second. That is not an invariant entitlement for every future configuration. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/pacing-limitations))

For historical bars of 30 seconds or less, documented restrictions include identical-request spacing, same-contract bursts and a ten-minute request limit; `BID_ASK` requests count twice. Encode the applicable rules by request category, with caching, cancellation and bounded retry—not one generic sleep. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/md/market-data-limitations))

More importantly:

- do not assume historical retrieval reconstructs the live callback stream;
- preserve request parameters, retrieval time, regular-hours setting, timezone and adjustment context;
- retain revised historical values as new vintages rather than overwriting what research previously knew;
- distinguish incomplete updating bars from finalised inputs.

Historical data may be filtered or revised, and updating-bar callbacks can repeatedly revise the same timestamp. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/md/market-data-limitations))

**Critical feasibility gate:** real-time options tick-by-tick data is unavailable through the documented interface. That does not prove no useful option trade data can be obtained by any route, but it defeats an assumption that D120’s required trade/quote history follows automatically from buying an option subscription. Resolve the exact source route before building dependent live claims. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/md/live-ticks))

### 4.6 Model reconnection, time and failure explicitly

Use a small connection state machine: disconnected, connecting, API-ready, data-ready and degraded. A connected socket is not evidence of fresh, complete market data.

| Event | Required treatment |
|---|---|
| IBKR 1100 | Mark broker connectivity degraded; stop dependent freshness-sensitive actions. |
| IBKR 1101 | Reconcile and resubmit lost market-data requests. |
| IBKR 1102 | Data requests were maintained; avoid blindly duplicating subscriptions. |
| Depth reset 317 | Clear the reconstructed book and re-establish required warm-up before dependent measurements. |

These distinctions come directly from IBKR’s error/depth documentation. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/error/codes))

**PROPOSED implementation discipline:**

- callbacks perform minimal capture/enqueue work;
- queues are bounded;
- overflow or persistence failure creates an explicit gap/degraded state;
- derived results never silently continue across an invalidated capture interval;
- displayed updates may be coalesced, but required underlying evidence must not be silently discarded;
- source timestamps, UTC receipt time and monotonic process timing remain separate.

Record the broker’s historical-time formatting configuration and contract timezone. Monitor host clock synchronisation; server-time checks do not manufacture missing event timestamps. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/tws-settings/historical-date-format))

The current native receipt-clock implementation explicitly preserves absent event time. Retain that discipline; a new L1 timestamp does not repair D145’s L2 event-clock hold. [W:`src/nvda_desk/market_measurement_truth/_native_book_insert_rate.py`:62–92; W:`EXEC_PLAN.md`, L31.]

### 4.7 Resolve instruments; never trade by display symbol alone

Use contract qualification to retain the broker instrument key and the relevant security type, currency, exchange/primary exchange, local symbol and—when options are introduced—expiry, right, strike, trading class and multiplier.

`reqContractDetails` may return multiple matching contracts, so ambiguity must be rejected rather than choosing the first result. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/contracts/details))

Keep provider instrument identity separate from the M00 schema/contract identity. Do not infer a multiplier of 100 or an expiry instant from an expiry date.

### 4.8 Paper execution is a separate product increment

Use separate launch profiles, account allowlists, stores and broker sessions for:

- offline simulation;
- paper execution;
- live execution.

Show **data mode** and **execution mode** separately. Live quotes may support paper execution; delayed quotes must never be presented as live merely because an account is connected.

Before paper submission, require persisted intent identity, validation, acknowledgement tracking and reconciliation against open orders/executions. An uncertain submission must not be blindly retried. Cancellation requested is not cancellation confirmed; IBKR also documents duplicate order-status notifications. ([interactivebrokers.com](https://www.interactivebrokers.com/docs/tws-api/doc/order-management/order-status))

A stop control should initially mean **stop new submissions**. Cancelling outstanding orders or flattening positions are separate behaviours requiring explicit policy.

Paper results demonstrate integration behaviour, not realistic liquidity or profitability. IBKR documents simulated top-of-book fills and other differences from live execution. ([interactivebrokers.com](https://www.interactivebrokers.com/campus/trading-lessons/paper-trading-vs-live-trading-whats-the-difference/))

---

## 5. Minimal UI: choose Streamlit, but keep it thin

**Recommendation: Streamlit is appropriate for the first owner-operated workbench.** Its required role is data inspection and controlled job interaction—not a trading terminal or the owner of a broker connection.

Start with three pages:

| Page | Initial functionality |
|---|---|
| **Status & measurements** | Dataset/source identity, execution disabled, timestamps, data mode, capture health, selected measurement values, units and explicit unavailable states |
| **Replay & research** | Select an approved dataset/profile; launch one bounded replay job; compare runs; inspect a small chart/table; export a reproducible run summary |
| **Provenance & diagnostics** | Result → definition/profile → source occurrences → input versions; refusals, gaps, runtime/build information and relevant logs |

Add a fourth **Simulation/Paper** page only after its execution service and authority exist. Do not build a live-order button now and rely on a warning label to make it safe.

“Replay” here means **isolated experimental reprocessing of retained inputs**, not activation of M00’s excluded authoritative replay/re-identification capability. [W:`config/architecture/modules.yaml`, M00 exclusions and replay obligations.]

### Two operational requirements matter more than visual polish

**1. Explain non-results honestly.**  
Several selected owners collapse bounded validation failures into `None`. The UI cannot infer the reason from that alone. Add a small, read-only diagnostic channel for the selected application path, keyed to its request/run, while preserving the existing result/absence contract. If no reason was observed, display `UNKNOWN`, not an invented explanation. [W:`src/nvda_desk/market_measurement_truth/_underlying_returns.py`, `_Owner.materialise()`; `_native_option.py`, `_Owner.materialise()`.]

**2. Never make browser behaviour cause financial or data-session side effects.**  
Streamlit’s rerun and cache model requires deliberate handling. Cache immutable read results by dataset/profile/run identity; treat Session State as UI state, not a durable job or order ledger. Keep broker sessions in the engine process. ([docs.streamlit.io](https://docs.streamlit.io/develop/concepts/architecture/caching))

For the first offline release, a fixed, allowlisted CLI job can be launched by the application layer. There is no need for FastAPI, Celery or a general command bus. Introduce a durable local command queue only when long-running capture/paper operation needs it.

Deploy locally first. Remote sharing introduces authentication, account-data separation and market-data distribution questions. Do not enable experimental agent-access endpoints for the initial UI.

**Acceptance criterion:** the owner can select a run, understand whether its data is usable, trace a displayed number, diagnose a refusal and reproduce the result without reading repository history.

---

## 6. Ordered delivery increments and independent acceptance

These are proposed product increments, not replacements silently imposed on the 27 mandatory R2 outputs.

| Increment | Deliverable | Acceptance evidence and separate Tester responsibility |
|---|---|---|
| **0 — Establish the product boundary** | One owner/use case, one deployment profile, exact D011/D012 input/profile scope, bounded A00 composition extension and reproducible package candidate | Reviewer checks actual public APIs, profile/admission compatibility, installed-package assets and the necessary test-control repairs identified previously. No broker access needed. |
| **1 — Offline measurement workbench** | Approved inputs → public M00 reads → D011/D012 calculation → durable storage/readback → Streamlit display and provenance | Tester exercises the actual application entry point with an independently derived result, a reached refusal, restart/readback and duplicate-job handling. It must not rely solely on Worker convenience fixtures. |
| **2 — Offline IBKR adapter contract** | Official SDK boundary, instrument mapping, bounded queues, request scheduler, session/gap events and diagnostic read model | Tester uses versioned callback/control specimens: wrong instrument, missing/sentinel field, disconnect, duplicate subscription request, overflow and persistence failure. No real broker connection is implied. |
| **3 — Authorised read-only capture** | One qualified NVDA stock contract and the selected quote subscription; a distinct live-source measurement profile | Tester verifies actual entitlement/data mode, observed callback fields, timestamp interpretation, persistence, reconnect behaviour and absence of order capability. An account blocker does not stop increments 1–2. |
| **4 — Reproducible research** | Retained real observations, explicit historical vintages and one owner-chosen research question | Tester verifies knowledge cut-offs, deterministic preprocessing, dataset separation and reproducibility. Research assessment compares against a declared baseline; engineering correctness is not predictive validation. Add only indicators needed by this question. |
| **5 — Bounded paper execution** | Approved paper intents, account/mode isolation, submission journal, acknowledgements, cancellation and restart reconciliation; Gateway operation where appropriate | Independent Tester proves wrong-account refusal, duplicate-action resistance, uncertain-outcome recovery and audit completeness before any paper session is commissioned. Broker-observed tests then remain separately identified. |
| **6 — Operational hardening** | Service supervision, backup/restore, retention, measured capacity and—if justified—additional M00 PostgreSQL | Tester verifies realistic workload bounds, recovery from committed state, migration/conversion fidelity and actual database privileges. Live execution remains a later explicit decision, not an automatic graduation. |

### Work that should proceed independently

- Offline UI and adapter development can proceed while account entitlement is unresolved.
- Lawfully authorised raw capture can proceed while a research model or derived profile remains held.
- M02 SQLite work should not wait for additional M00 PostgreSQL unless a real dependency is established.
- Options source-feasibility work can proceed before implementing surface/order-flow consumers.
- D145’s pause should not block unrelated product value.

### Testing and workflow changes needed for these increments

Use three distinct evidence classes:

1. **Deterministic application/contract tests:** offline, repeatable and suitable for CI.
2. **Storage and broker integration evidence:** exact environment/source scope; isolated from ordinary PR execution.
3. **Research validation:** empirical performance and sensitivity, never labelled as software conformance merely because a test passed.

Streamlit’s `AppTest` can exercise input and rendered-state behaviour through pytest without a full browser-automation programme. A small real-browser smoke check still has a separate purpose. ([docs.streamlit.io](https://docs.streamlit.io/develop/concepts/app-testing))

**PROPOSED delivery rhythm:**

- Worker supplies a small candidate, changed-path/impact declaration and finite case inventory.
- Separate Tester checks the proposition and oracle, then executes only the admitted scope.
- CI may provide controlled execution machinery once expressly commissioned; it does not replace independent judgement.
- One run manifest retains candidate, environment, dataset/profile identities, raw results and disposition.
- Owner receives a short demonstration and a concrete decision only when substantive choice or external authority is required.

Do not create one permission ceremony per UI assertion. Equally, do not hide an unbounded integration campaign inside the historical “two cases per D” rule: application and adapter obligations need their own finite admission.

The existing R2 Worker/L32 restrictions remain operative until properly amended. This supplement does not itself change them. [W:`EXEC_PLAN.md` §4; W:`tests/AGENTS.override.md`:5–13.]

---

## 7. Decisions to make only when genuinely needed

| Trigger | Genuine decision | What should not wait for it |
|---|---|---|
| **Before the first application build** | Accept the narrow workbench objective and bounded composition/new-proof scope | No need to decide every future strategy, database or frontend feature |
| **Before real broker capture** | Authorise account/session access, costs, data use and the exact source contract; delegate bounded technical identity/restart implementation choices | Offline workbench and adapter tests |
| **Before a new measurement/profile** | Set genuinely missing clock, unit, selection, completeness or numerical policy | Existing unchanged profiles; raw capture that does not depend on the decision |
| **Before research conclusions are operationalised** | Choose the research question, evaluation criterion and any production promotion policy | Exploratory work inside an explicitly non-production research commission |
| **Before paper orders** | Account, instrument/order permissions, limits and permitted stop/recovery actions | Read-only data collection and analysis |
| **Before shared/unattended production** | Availability/loss tolerance, recovery objectives, retention, security and hosting requirements | The single-user local prototype |
| **Only if D145 is reconsidered** | Explicit reactivation and a valid source/clock contract with separately admitted proof | All unrelated work |

Several previously deferred unknowns become real requirements at live capture: occurrence-ID generation, ingestion-sequence scope across restarts, pre-commit loss visibility and recovery behaviour. The historical tranche explicitly avoided claiming these operational guarantees. They should now be resolved proportionately—not assumed from successful local persistence tests. [W:`implementation/authority/VI03_REMAINING_UNKNOWN_IMPACT.md`, exact impact map; W:`config/architecture/modules.yaml`, M00 exclusions.]

**Material evidence still needed before implementation:** the full M00/M02 public API bodies, M00 SQLite/PostgreSQL adapters, native-source/profile bodies, actual D011/D012 contracts/fixtures, `uv.lock`, deployment assets and the authorised account capability inventory. The original curated sample does not establish all of these. Their absence limits execution readiness, not the recommendation to deliver an offline-first product.

### Copy-forward recommendation register

**PROPOSED ADR sentences—verbatim candidates, not accepted authority:**

| ID | Recommendation |
|---|---|
| **P01** | “The first usable product will be a local NVDA measurement and replay workbench, not a live trading system.” |
| **P02** | “The application will remain a modular Python system with explicit owner APIs and separate engine and UI processes.” |
| **P03** | “Streamlit will present results and submit permitted application commands, but will not own broker sessions, calculation truth or order state.” |
| **P04** | “The first broker integration will use the official IBKR Python TWS API and will initially be read-only.” |
| **P05** | “Live-source profiles will be admitted separately from controlled synthetic profiles, without relabelling historical evidence.” |
| **P06** | “Every reproducible run will identify its inputs, temporal cut-offs, profiles, code, environment and outputs, and missing event time will not be inferred from receipt time.” |
| **P07** | “Existing SQLite evidence will remain unchanged, and PostgreSQL will be introduced only for an explicitly admitted storage requirement.” |
| **P08** | “Paper and live execution will be operationally separated, and uncertain submissions will be reconciled rather than blindly retried.” |
| **P09** | “Each delivery increment will demonstrate operator-visible value and independently verified boundary behaviour without routine reruns of unaffected historical proofs.” |
| **P10** | “D145 remains paused unless separately reactivated under explicit authority and a valid source-time contract.” |

**Overall recommendation:** move from proving isolated capabilities to demonstrating one trustworthy owner workflow. Make source feasibility and operational truth visible early, retain the existing semantic safeguards, and let observed product needs—not catalogue size or framework ambition—determine the next engineering investment.
<!-- END ASTRA RESPONSE 2 — VERBATIM ORIGINAL BYTES -->
