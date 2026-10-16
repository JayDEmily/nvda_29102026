# NVDA V2 — Gate 2 review addendum: G2.1–G2.5 against the commissioning brief

**Date:** 16 October 2026 — Australia/Melbourne  
**Role:** Independent documentary review and bounded return, not a Gate 2 owner-acceptance record, a new mathematical decision or execution of G2.6.  
**Recommendation:** **BLOCK Gate 2 acceptance on identified material semantic/source and allocation decisions; RETURN the G2.6 decision-record deliverable for completion once the necessary evidence/authority is available.** Do not restart Gate 1, redo the already-reconciled historical inventories, merge to `main`, run application tests or begin work packages C–E under this review.

## 1. Exact baseline, governing question and review method

- **Supplied G2.5 commit:** `37d9ce2050d8371ab2f4f7f5223bbb8c0750ae39` (tree `12cc774e7f676808b24562d3a95b84dfd615ec61`; parent `3406ed90ccacb0558b6c304012d20f75ff35d5a3`).
- **Accepted Gate 1 main:** `77d82bd8ee4268673715fe7e5653b6a65a299b54`, preserved and not reopened. `handoff/workbook_v2/gates_01_02/GATE_1_OWNER_ACCEPTANCE_20261016.md` is the controlling owner decision despite the frozen ExecPlan's earlier status text.
- **Governance:** `GUARDRAILS.md`, root `AGENTS.md`, frozen root `EXEC_PLAN.md` (SHA-256 `8abed334586aea28b22db7ec6fd0614f41cdb47a02b08cb4e839eb61b96e8b0e`), and `handoff/workbook_v2/decisions/ADR_WBV2_003_V2_INVESTIGATION_COMMISSIONING_BRIEF_VERBATIM.md` (14 October 2026, §§1–6.B, 9–11). G2.6 and the five mandatory Gate 2 exit propositions are in `EXEC_PLAN.md` §1. ADR-WBV2-001/002 define semantic eligibility and no-peer-runtime/local-duplication policy.
- **Inspected:** G2.1–G2.5 findings; all 209 rows and 99 columns of `D001_D209_TRACEABILITY.csv`; G1.5 crosswalk and owner acceptance; the effective `NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, relevant accepted contract clauses and D138/D145 source facts described below; historical Pass06 95-group membership and 107-reference CSVs; the 14 October brief, architecture role constraints and reviewer precedent `GATE_1_REVIEW_ADDENDUM_20261015.md` from its historical review branch.
- **Independent readback:** Parsed the committed traceability, normative catalogue and Pass06 CSVs. Confirmed 209 distinct `D001`–`D209` identities; historical 114/95 split; one historical group per 95; 107 unique direct cross-group references exactly equal the corresponding effective-catalogue D edges; 67 ordered old-module pairs; 30 historical groups; D192 has 117 unique transitive D ancestors; and **no** conditionally proposed M02 identity has an unknown/downstream D ancestor in the declared graph. Reconfirmed the actual catalogue input lists for D138 and D145. These are **documentary graph/identity checks**, not proof of source-contract sufficiency, every accepted equation or full runtime behaviour.
- **Not performed or claimed:** New exhaustive independent row-by-row mathematical derivation, every workbook-cell reread, native provider instance validation, executable source correctness review, application/database/unit/integration tests, lint/typecheck, implementation/peer proof, production admission or Gate 2 owner acceptance. The previous workers' broader readback claims remain precisely their claims; the independent checks above only confirm their stated scope.

## 2. Leaf-by-leaf judgement against the brief

| Leaf | Reviewed proposition | Disposition and scope |
|---|---|---|
| **G2.1** | Single D001–D209 population, original/effective/historical source provenance | **SUPPORTED within independently checked identity/history scope**: 209 unique IDs, historical 114/95 and 95/30/107 reconciled. Does not establish mathematical or source sufficiency. Original reference-archive byte equivalence remains the documented, Gate 1-bounded unknown, not a reason to reopen accepted Gate 1. |
| **G2.2** | Accepted mathematical meaning and amendments distinct from historical workbook claims | **DOCUMENTED, with bounded substantive source corroboration**: effective source and owner amendments are distinguished; D104/D116/D120/D123/D134–D135/F4 contracts are not silently replaced by historical descriptions. This review does not independently certify each of 209 equations or resolved native-source meaning. Specific remaining source issues flow into G2.3, not a new mathematics amendment. |
| **G2.3** | Full semantic source/dependency closure for all D | **NOT SATISFIED** as an exit-strength claim. Static R/D closure is supported; provider-native mappings, full history/parameter instances and, importantly, D138/D145 input sufficiency remain materially unresolved. The leaf report itself explicitly records `BLOCKED_ON_NAMED_SEMANTIC_SOURCE_CONTRACTS`, not `PASS`. |
| **G2.4** | Defensible complete M02-versus-downstream semantic classification | **NOT SATISFIED** as a final allocation/classification claim. Exactly 100 **conditional** M02 candidates, 74 positive downstream disqualifiers, **35 materially UNKNOWN**; 53 of the 100 conditional candidates have historical convention-freeze flags. None is a future admitted owner. These distinctions are correctly preserved in the current register. |
| **G2.5** | Historical downstream responsibility and local-frontier reconciliation | **SUPPORTED for the bounded historical/static proposition**: 95/30 memberships, 107 references and distinct static group frontiers reconcile; five old groups contain no presently established downstream member. **NOT** proof of the ultimate group count, independently executable peers or admitted module allocations, as the leaf itself recognises. |
| **G2.6** | Linked material disagreements, decision owners, actions and gate-exit disposition | **NOT PERFORMED at the reviewed baseline.** This review addendum identifies the required docket and acceptance blockers; it is **not** a substitute for complete issue-specific decisions or a programme-owner `ACCEPT`. |

The first unmet **Gate 2** mandatory invariant is `EXEC_PLAN.md` §1 Gate 2 exit (b)/(d): classification-relevant semantic/source closure and authoritative disposition of materially disputed allocations. The brief's work package 6.B does not permit documenting an unknown to count as resolving it. The separately supported identity/reconciliation findings must not be discredited merely because downstream semantic closure is blocked.

## 3. B1 — Two distinct L2 input-contract insufficiencies remain material

### B1a — D138 cumulative standing-depth regression

**Verified source discrepancy:** Effective catalogue `derived_id=D138` declares `R189;R190;R188` plus `D011`, but not book-row position `R185` or book operation `R187`. Original native R188–R190 source descriptions concern incremental `updateMktDepthL2` callback fields, not an inherently complete standing-book snapshot. The accepted K06 cumulative-depth-versus-distance slope requires the **actual standing state**. G2.3 §4 DEP-L2-138 records why the inspected current `_stage1.py` branch cannot by itself prove the missing state reconstruction.

**Disposition:** `BLOCKED` on source/definition sufficiency, not permission to rewrite the catalogue. The mathematical/source-contract authority must establish a genuinely admitted standing snapshot variant or approve the exact required dependency/selection correction, with source-custodian evidence. Later C–E may implement and prove the resulting approved path. Do not replace an accepted R identity with a new value meaning or declare a source defect corrected from documentary graph inspection.

### B1b — D145 position-addressed book updates

**Verified source discrepancy:** Effective D145 declares `R187;R188;R189;R190`, with no native book-row `R185` position. The original L2 provider event is position/operation-sensitive. Current price-key `(side, price)` reconstruction is not demonstrated equivalent for all position-addressed replace/delete events. G2.3 §4 DEP-L2-145 identifies **32** transitive downstream D descendants exposed to the same source-contract question (graph exposure, not proof that each executed occurrence fails).

**Disposition:** Separately `BLOCKED`: demonstrate an accepted price-addressed source variant and exact field mapping, or obtain the narrow source/mathematical authority change and corresponding selection contract. Do not treat B1a and B1b as one generic book defect or presume a permitted repair.

## 4. B2 — All 35 disputed classifications need their own evidential dispositions

**Independently checked register status:** Historical `YES=114` divides into **100 conditional proposed M02 / 14 UNKNOWN**. Historical `NO=95` divides into **74 established downstream disqualifiers / 21 UNKNOWN**. These 35 are genuinely unallocated in the *new* proposal. `M01` remains the registered current semantic responsibility for all D001–D209.

The following **exhaustively covers the 35 distinct currently UNKNOWN D identities**. D064 intentionally appears in **two** issue classes because provider identity and score/model fixedness are separate questions; it must get separately linkable issue dispositions.

| Separate issue mechanism | Affected D identities | Required closure evidence/authority |
|---|---|---|
| K07 score/feature/weight neutrality | D006, D008, D040, D041, D061, **D064**, D070, D084, D132 | Admit or evidence the relevant immutable feature extractor, transforms, weights and baseline; establish whether its meaning is a non-strategy measurement or tuned policy/model. No invented coefficients. Other K07 identities with independently established downstream disqualifiers need not be reclassified merely because their concrete runtime instance is absent. |
| Event-provider/native time and consensus | D062, D063, **D064** | Native `R284/R285/R286/R289` variants, temporal kind, release identity/vintage, event/sensitivity and prior-sample sufficiency; source custodian plus mathematical owner where meaning/eligibility changes. |
| Regression state/comparator fixedness | D078, D079, D080, D081, D082 | Exact non-strategy state/peer-basket selection and sample/history identities, or record an evidenced model-conditioned downstream disqualifier. |
| Objective bucket/book thresholds and basket | D091, D122, D124, D139, D140, D141, D142, D151 | Exact approved band/threshold, membership, observation window, event or basket policy; determine non-strategy fixedness rather than assuming that all versioned parameters are neutral. |
| Surface fit/risk-neutral model definition | D102, D111, D112, D113 | Approved pricing/surface/fit convention and its dependent meaning, including admissible fixed-versus-model-dependent context; propagate only after D102 resolution. |
| Inherited D091-dependent grouping | D109, D110, D121 | Reconcile D091's exact semantic classification and inherited source/configuration before choosing a new owner. |
| Other native source/input sufficiency | D117, D123, D138, D145 | R075 comparator source; two distinct official-OI reporting periods/revision precedence; D138 full standing L2; D145 positional updates, respectively. Controlled calculation authority is not live provider evidence. |

**Material dependency propagation:** The event-source gap reaches 38 D identities in the static R closure, and D145 reaches 32 transitive D descendants. The present reports distinguish these from 38/32 additional independent owner changes. Reassessment of downstream *input sufficiency* after resolution is necessary; positive strategy-dependent disqualifiers are not erased by repairing a source.

**53 conditional historical convention flags:** G2.4 correctly treats the 53 historical flags within its 100 conditional M02 candidates as needing non-strategy fixed conventions. They are **not** 53 independently proved errors or 53 automatically rejected measurements. An exact authority-backed convention/profile schedule and per-row effect must precede **unqualified** M02 eligibility; the other 12 flagged candidates are among the 35 UNKNOWN. Missing tests, code migration and durability alone belong to later C–E and are not semantic disqualifiers.

## 5. B3 — Downstream group count and canonical future responsibility not yet decidable

**Verified static impact:** Historical P02, P04, P05, P06 and P09 have respectively `0/7`, `0/2`, `0/2`, `0/4` and `0/2` established-downstream/UNKNOWN membership. Those **17** D rows may change the necessity or nature of those five groups. P01/P03 also mix established downstream and unknown classifications. The **14 historical YES now UNKNOWN** have no historical P01–P30 membership at all:

`D063, D078, D079, D080, D081, D082, D117, D122, D123, D124, D138, D139, D140, D145`.

**Disposition:** The programme owner cannot approve a definitive 30-module/M03–M32 successor allocation from current evidence. Resolve the material classifications and propose boundaries for *every* D; then obtain the proper owner decision, respecting new-object ingress/ID allocation law. Do not treat the original 107 D edges as peer runtime APIs or reuse a canonical D owner for copied peer-private arithmetic. Actual independent peer design, re-use, code locality, tests and public ingress belong to work package E and subsequent authorised implementation.

## 6. R1 — Complete the G2.6 issue/decision record; do not substitute narrative for decisions

**Observed documentary gap:** `D001_D209_TRACEABILITY.csv` has 99 fields and per-row issue narratives, but no linked `ISSUES.csv` or equivalent one-record-per-distinct-issue decision docket at the reviewed commit. G2.3's issue labels and G2.4's receiving-action prose are useful **leads**, not recorded decisions or owner acceptance. For example, D064's unresolved provider source and P_SCORE semantic fixedness require independently traceable dispositions. G2.6 is expressly **not started**, so this is receiving work, **not a retroactive defect in the G2.1–G2.5 leaves**.

**Required bounded G2.6 output:** Use the same cumulative 209-row register, with one linked material-issue record per genuinely distinct matter (the permitted `handoff/workbook_v2/gates_01_02/ISSUES.csv` is appropriate). Each record must identify canonical affected IDs, currently accepted definition/current M01 owner, historical eligibility/group, new conditional proposal, precise authority/source evidence, impact and recursive exposure, classification/status, source custodian versus actual decision authority, what fact or authority decision is required, whether it changes mathematics/source selection/module boundary, receiving work and final disposition. Where several D identities share one upstream root cause, link the rows to that root issue rather than fabricating 35 unrelated decisions; where one D has two material issues, retain two records. Preserve `UNKNOWN/BLOCKED` until the particular evidence or decision exists. No favourable status may be backfilled merely to meet a count.

A G2.6 gate-exit candidate must then state, separately for each mandatory Gate 2 claim (a)–(e), what is supported, what remains blocked, what is genuinely deferrable to C–E, and the exact owner `ACCEPT`/`RETURN`/`BLOCK` decision. This review cannot supply an absent source mapping or make that owner decision itself. The frozen `EXEC_PLAN.md` remains unchanged; the later owner acceptance record, as in Gate 1, supersedes historical status lines rather than silently editing planning authority.

## 7. Acceptance boundary, next work and recurrence

**Recommendation: `BLOCK` Gate 2 exit.** G2.1/G2.2 documentary meaning and G2.5 historical/static reconciliation are usable, with their evidence limitations. G2.3's *semantic* closure and G2.4's *full* classification claim are **not met**, and G2.6 has not yet completed issue-by-issue documentary decisions. The owner may consider each prior leaf's documented findings without accepting Gate 2 or promoting unknown allocations.

**Next authorised type of work:** (i) present the specifically identified D138 and D145 source/authority questions to their competent owners, alongside event/official-OI/score/convention evidence requests; (ii) complete the G2.6 linked material-issue docket and propagation in a bounded work branch **without inventing** those answers; (iii) when necessary evidence/decisions have actually arrived, reassess affected rows and the surviving group boundaries; (iv) separately request the programme-owner Gate 2 exit decision only when the plan's mandatory propositions are supported. A *blocked* Gate 2 is not permission to begin C–E production work or change M00/M01, and a failed missing-input classification cannot be accepted by administrative waiver.

**Review lineage:** This is the first Gate 2 reviewer addendum in the inspected G2.1→G2.5 commit sequence. No earlier successive Gate 2 return/repair episode is established; therefore the new documentary-docket finding is `ISOLATED`, while the D138/D145 issues are **already recorded unresolved mechanisms**, not new repeat defects. Historical Gate 1 R1/R2 were incorporated and owner-accepted; do not reopen them.

**Change boundary of this review:** Addendum only on a separate review branch; no change to root governance/ExecPlan, source evidence, the 209-row cumulative register, canonical definitions, module registry, production code, workbook, tests or accepted main. Git/readback checks establish artefact integrity, **not Gate 2 correctness**.
