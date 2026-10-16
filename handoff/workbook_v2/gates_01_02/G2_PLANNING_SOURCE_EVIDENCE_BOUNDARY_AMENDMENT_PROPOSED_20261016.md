# Gate 2 — proposed planning/source-evidence boundary amendment

**Proposal ID:** `G2-PLANNING-BOUNDARY-20261016-01`  
**Date:** 16 October 2026 — Australia/Melbourne  
**Status:** `PROPOSED / PREPARATION AUTHORISED / EXACT TEXT NOT YET ACCEPTED`  
**Gate 2:** remains unaccepted and blocked on unresolved material classifications.  
**Purpose:** establish the distinction between an accepted future input contract and proof that an operational source implements it, without accepting an unknown contract or manufacturing source evidence.

## 1. Current instruction, baseline and authority boundary

The programme owner has reiterated that this is planning: the IBKR API acquisition module is upstream of M00; no connection or integration is to be performed now. In this thread the assistant asked whether to **prepare a proposed Gate 2 amendment** separating future source-contract specification from later operational certification, with required semantics still resolved. On 16 October 2026 the owner replied: **“Yes, do the... do that so we don't break the rules. So I'm giving you authorisation, and, um, that's fine. Continue.”**

That reply authorises preparation of this concrete proposal. It is not recorded as acceptance of exact clauses that had not yet been written, acceptance of Gate 2, or permission to implement. The existing frozen root `EXEC_PLAN.md` remains the active plan. This document is a proposed bounded amendment to it, not a second active ExecPlan. No proposal clause below governs execution until the owner accepts this exact proposal by ID and candidate commit.

Inspected entry state:

- Supplied archive: `NVDA_V2_GATE_2_IBKR_L2_ACQUISITION_SCOPE_FULL_GIT_20261016.tar(1).gz`; SHA-256 `ab0e6d40cfe7c67a7a897f7c3fe5355f35adb258417b44e8ff1cb7adcf9e21aa`.
- Parent branch: `work/v2-g2-l2-acquisition-scope-reconciliation-20261016`.
- Parent commit: `5845623caa5b4d7fc078df5415c12acc4c0e739b`; tree `b0a7a11193db0454393b4913ad121546d24eb854`.
- Proposal branch: `work/v2-g2-planning-boundary-proposal-20261016`.
- Accepted local `main`: `77d82bd8ee4268673715fe7e5653b6a65a299b54`.
- Frozen root plan: Revision 4; SHA-256 `8abed334586aea28b22db7ec6fd0614f41cdb47a02b08cb4e839eb61b96e8b0e`.
- Master brief: `handoff/workbook_v2/decisions/ADR_WBV2_003_V2_INVESTIGATION_COMMISSIONING_BRIEF_VERBATIM.md`; SHA-256 `7a05874fbd4971d03bcef47d5cdaf8020f533a10a6a73cf0ef276b8cb446f771`.

Gate 1's accepted evidence and decision remain as recorded in `GATE_1_OWNER_ACCEPTANCE_20261016.md`. The root plan's activation-era status lines do not reopen Gate 1; that decision explicitly explains the frozen snapshot. None of the historical source-contract findings is erased by this proposal.

## 2. Reason for the proposed clarification

The active plan already distinguishes semantic eligibility from later implementation proof: G2.4 expressly places absent implemented tests, durability and public reachability in C–E. ADR-WBV2-001 makes the same distinction. The master brief §8 Phase 4 distinguishes controlled-input proof, native-source evidence and observed live behaviour and does not impose live execution universally.

The later L2 investigations correctly preserve real semantic unknowns, but their receiving-evidence lists also include selected operational requests, captured callbacks and projection readback. Those are not all the same proposition. A complete, authority-backed contract can describe required future inputs without claiming that a deployed acquisition source already supplies them. Conversely, a list of requirements is not proof of source feasibility or a complete contract.

The proposed change therefore does not turn every source gap into later engineering. It requires each gap to be split by the proposition it actually prevents establishing. The current nine L2 source propositions, the two approved dependency amendments and all other issue records remain traceable.

## 3. Exact proposed governing clauses

The following clauses are proposed as a bounded interpretation/amendment of `EXEC_PLAN.md` §1 G2.3–G2.6, its Gate 2 exit rules and §5.3. They apply to the Gate 2 planning assessment only. The root plan bytes remain frozen; an owner acceptance record would explicitly identify this overlay and its limited precedence. If the owner does not accept the proposal, the existing rules and blockers remain unchanged.

### A1 — Two independently evidenced propositions

For each affected D, distinguish:

1. **Planning contract and classification:** the authoritative intended mathematical meaning, exact R/D identities and complete input chain, required source variant/selection, units and categorical interpretations, temporal/ordering/history/readiness/reset/refusal law, neutral-versus-strategy meaning, and proposed responsibility. A new or amended semantic choice requires competent authority. Primary source evidence must support the proposed source's ability to express the required facts; a hypothetical schema alone is insufficient.
2. **Operational source conformity:** whether an identified acquisition deployment, subscription, request, callback stream, mapping and M00 public ingress actually conform to that contract, including runtime ordering, completeness, reset and warm-up proof.

Evidence for one proposition does not establish the other. A planning classification is not a source-admission certificate. Observed field presence is not by itself proof of the required calculation semantics or complete book state.

### A2 — Gate 2 closure and permitted deferral

Gate 2 must resolve proposition 1 for every identity whose classification depends on it. It may defer proposition 2 only when its unknown answer cannot change the planning classification, dependency meaning or lawful proposed responsibility and when no applicable accepted domain rule requires that evidence to establish proposition 1.

Every permitted deferral must name the exact obligation, affected D/issue links and propagation, receiving responsibility, evidence required, consequence of failure and the future acceptance hold point. The future plan must assign an executable unit before any dependent production admission. Until that unit exists and is accepted, no runtime work or source admission is authorised.

Where provider documentation is inconsistent or cannot establish required callback applicability, source identity, state completeness, time or history, that **semantic feasibility question remains UNKNOWN/BLOCKED in Gate 2**. It must be resolved by stronger primary evidence or an expressly authorised semantic alternative. Do not invent a snapshot marker, callback route, readiness heuristic, field mapping, coefficient or missing history. Merely saying that a future adapter will solve the problem does not close it.

### A3 — Required future inputs versus actual selected deployment

Planning may specify an exact versioned required source/input contract before an operational deployment exists, provided A1/A2 are satisfied. Contract variables may remain deployment-bound only when their allowable values and effect on meaning are explicit and selection within that domain cannot change classification. Otherwise their selection remains a Gate 2 decision.

No hypothetical request ID, conId, subscription product, entitlement, session, mapping instance or callback capture may be recorded as actual. In a future contract such fields are required bindings, not observed values. The owner's intent to subscribe to IBKR depth is scope direction only.

### A4 — Independent architecture responsibilities

Plan provider connectivity/acquisition upstream of M00. Retain M00's registered raw-observation, provenance and typed public-projection responsibility and its provider/network-integration exclusion. M00 does not become the IBKR network client, and a downstream calculation does not acquire provider data directly. Do not assign a new runtime ID, package, registry entry or admitted state owner through this amendment.

Specify the required semantics of reconstructed book state and identify a proposed responsible boundary before finalising the affected classification. The exact admitted placement and engineering of reconstruction, categorical interpretation and persistence require subsequent architecture/implementation authority. No provider-native value may be silently replaced and represented as unchanged raw truth; derived mathematics is not moved into M00 for convenience.

### A5 — L2 mathematics and source refusal remain separate

Preserve `D138-L2-CONTRACT-20261016-01` and `D145-L2-CONTRACT-20261016-01`, each with authoritative direct R inputs `R185;R187;R188;R189;R190`. Preserve D138's D011 predecessor and K06 mathematics and D145's K17 mathematics and accepted temporal obligations. This amendment neither changes the catalogue nor reopens those approvals.

Evaluate D138 standing-depth/cutoff sufficiency separately from D145 consecutive-best-state/warm-up sufficiency. Preserve source-generation/reset refusal and exact native R meanings. A planning decision must not certify an operational book. Missing or ambiguous source state remains a refusal condition in later implementation; it must not produce fabricated valid outputs.

### A6 — Register treatment and remaining decisions

Keep the existing cumulative `D001_D209_TRACEABILITY.csv`, `ISSUES.csv` and `ISSUE_D_LINKS.csv`; preserve historical values and issue IDs. When this amendment is accepted, append distinct planning-contract/classification and operational-source-evidence fields or equally explicit linked dispositions. Each changed row must cite its separate evidence and authority. Do not overwrite prior unknowns as though a live source had been verified.

No D classification changes solely because this amendment is accepted. The 35 currently disputed identities, conditional convention obligations and future group-boundary decision require their own evidence-based dispositions. Established downstream disqualifiers are not removed by resolving upstream input supply. Do not accept an unresolved classification as merely conditional to obtain Gate 2 closure.

### A7 — Gate exit and the next ExecPlan

Gate 2's five mandatory exit propositions (a)–(e) remain required. For (b) and (d), apply the explicit planning-contract/operational-conformity distinction above; all classification-critical unknowns remain blocking. The exit record must list accepted planning contracts separately from deferred operational proof, with no claim of live source availability, M02 readiness or peer admission.

After all required Gate 2 findings and decisions are supported, submit the exact candidate for the programme owner's separate Gate 2 acceptance. This amendment is not that acceptance. After owner acceptance closes the current two-gate tranche, draft the successor ExecPlan from ADR-WBV2-003 C–E and §8, incorporating retained Gate 1/2 obligations and every operational hold point. A successor draft is not active until expressly accepted. No implementation or integration is authorised by drafting or accepting a planning assessment.

## 4. Nine L2 propositions: required split under the proposal

This table specifies the future reassessment method. It does not newly certify provider behaviour, a complete source contract or any SC-L2 proposition. Source references and unresolved witnesses remain in `G2_L2_SOURCE_CUSTODIAN_INVESTIGATION_20261016.md` and `G2_L2_ACQUISITION_SCOPE_RECONCILIATION_20261016.md`.

| Existing proposition | Planning requirement still to settle from authority/evidence | Operational evidence to receive later if A2 permits |
|---|---|---|
| SC-L2-01 — request/selection | Exact permitted provider variant, subject/venue/depth scope and selection semantics; distinguish meaning-changing selections from deployment bindings | Actual entitlement, contract/conId, request ID, selected request values, API/session/generation evidence |
| SC-L2-02 — callback | Resolve supported callback applicability for the chosen contract; documented routing inconsistency remains a semantic blocker until resolved | Captured callback identity and fields correlated with the selected request |
| SC-L2-03 — R mapping/enum/units | Exact required five-R field correspondence and native categorical meanings; lawful versioned interpretation and occurrence identity preservation | Instantiated mapping versions, native record, public projection readback and conformity evidence |
| SC-L2-04 — chronology | Receipt-only temporal basis where required; deterministic per-stream/generation order, duplicate/gap/omission and cutoff law | Recorded atomic occurrences, timestamps/sequences and gap/recovery witnesses |
| SC-L2-05 — initial readiness | Authority-backed, feasible initial book/readiness and visible-depth sufficiency law; not a requested-row-count assumption or undocumented heuristic | Observed or otherwise admissibly demonstrated initialisation and invalid/partial-state refusals |
| SC-L2-06 — reset | Required scoped invalidation, generation separation, reinitialisation and refusal semantics | Conforming reset/reconnect trace and reset-to-readiness evidence |
| SC-L2-07 — D138 | Coherent standing bid/ask scope at D011 cutoff; accepted OLS/history/selection sufficiency | Source-to-selected-state lineage, reconstruction and D138 conformity proof |
| SC-L2-08 — D145 | Consecutive best-book transitions, predecessor before the first included transition, accepted windows/history and generation constraints | Conforming ordered state history, warm-up and D145 conformity proof |
| SC-L2-09 — selection metadata | Determine whether R186/R191 are sufficient provenance/selection fields or require a separately approved definition change; preserve existing R families | Actual metadata presence and source-selection conformity |

In particular SC-L2-02 and SC-L2-05 cannot be declared deferred merely because they also need runtime evidence later. Their unresolved planning questions remain material. If a future contract proves infeasible or incompatible, return the affected semantic decision to authority rather than substituting another source silently.

## 5. Traceable receiving work and exact continuation

No new gate numbering is created here. Receiving C–E responsibilities below are master-brief work packages, not currently open execution gates.

| Work reference | Proposed receiver | Hold point/evidence required |
|---|---|---|
| PB-L2-01 | Future upstream acquisition commissioning and C–E source-readiness assessment | Actual lawful request/entitlement/callback binding and admissible trace; no source admission without evidence |
| PB-L2-02 | C–E M00-ingress and calculation-boundary design/proof | Required versioned projection, native enums/units, occurrence/subject/stream identity and public-seam conformity; no direct M00-table bypass |
| PB-L2-03 | C–E book-state responsibility and source-conformity proof | Initialisation, position mutations, ordering, omissions, generation/reset/recovery and refusal; D138 and D145 evaluated independently |
| PB-L2-04 | C–E per-calculation acceptance and dependent reuse assessment | D138 cutoff/standing-depth and D145 predecessor/window/warm-up proof, with affected dependency links retained |
| PB-PLAN-01 | Successor ExecPlan drafting after Gate 2 acceptance | Convert each permitted deferral into an assigned unit and acceptance hold point; preserve original-M01 obligations, ownership/compatibility and later retirement requirements |

These are proposed receiving obligations, not claims that a competent implementer, module ID, live source or future gate has already been appointed/admitted. The programme owner commissions those roles and accepts the future plan.

**Next unit after acceptance of this exact amendment:** reassess `G2I-015` and `G2I-018` under A1–A6, recording which precise questions remain semantic blockers and which are genuinely operational. Begin from SC-L2-02 callback applicability and SC-L2-05 initial-readiness feasibility; inspect primary evidence needed for the question being decided. If they remain blocked, retain that result and continue only independent documentary decisions whose required evidence is available. Do not make unrelated classification investigations depend on a deployed L2 collector. Do not change classifications without their own primary evidence and authority.

Until acceptance, the next decision is the owner's acceptance/return of this proposal, not Gate 2 acceptance. There is no authorised live connection, implementation or integration step in this continuation.

## 6. Change and evidence limits

This preparation adds this proposal only. It does not change root governance, the active plan, accepted Gate 1, any D/R definition, the two L2 approvals, historical findings, the three cumulative registers, architecture configuration, source, tests, workbook or `main`. No application tests or application execution are part of this assignment.

Primary project sources inspected for the proposed boundary: full root guardrails/agent map/active plan and master brief; ADR-WBV2-001/002; registered M00/M01 responsibility records; Gate 1 owner acceptance; G2.6 findings and subsequent L2 notes; the L2 source-custodian investigation, acquisition-scope reconciliation and owner-approved D138/D145 amendment. Current CSV headers and issue examples were inspected for extension compatibility. This pass does not claim a fresh exhaustive 209-row semantic review, provider-document revalidation, live-data inspection or runtime source conformity. Existing reported totals and source gaps are inherited assessment states, not newly proven full-population findings here.

The failed attachment `NVDA_IMPLEMENTATION_ADMISSION_PM_HANDOVER_FULL_GIT_20260913.tar(1).gz` was not inspected. This proposal relies on the current supplied repository's governing files; it does not certify that missing archive or original historical archive-byte equivalence.

**Owner decision requested:** ACCEPT or RETURN `G2-PLANNING-BOUNDARY-20261016-01` against the delivered candidate commit. Acceptance would activate only clauses A1–A7 as the bounded planning overlay described above; it would not accept Gate 2, any source contract, any particular classification or any later ExecPlan.
