# NVDA M01 → Workbook V2 M01-1: source-and-authority audit

**Review date:** 14 October 2026 (Australia/Melbourne)  
**Repository HEAD:** `514040e0d32cf2efd0629c08cdf056b4c8b3f766`  
**Branch:** `work/workbook-v2-pass01-guardrails-method-20261014`  
**Scope:** Original M01 vs proposed V2 M01-1, existing engineering reuse, semantic and architecture blockers. **Read-only; no tests executed, no code or workbook changed.**  
**Disposition:** **M01-1 NOT COMPLETE / NOT ACCEPTED.** The implementation is substantial and reusable, but a completion percentage based on tests or dispatch bindings would be misleading.

## 1. What the user is engineering

The original `M01 derived_signal_calculation_truth` was one canonical **209-D calculation graph**, not solely a market-derived signal layer. The original acceptance test in its brief is deterministic computability from M00 raw truth, versioned parameters and optional D predecessors (§1): that admits strategy-weighted scores, candidate utility, risk limits, trade-action recommendations, realised portfolio measurements and forecast evaluation. It deliberately means **more than 'derived market data'**.

Workbook V2 changes the *proposed ownership architecture*: M00 owns native raw truth; **M01-1 only descriptive strategy-independent market/time/statistical transformations**; 95 other D identities are working allocations to **M02–M31 independent peers**, including local reimplementation of strategy-dependent intermediate arithmetic rather than peer runtime calls. The original D identities and mathematics remain preserved. Therefore Stage 1 vs Stage 2 in the old plan is **an implementation-scheduling cut**, not the market/strategy cut. An original Stage-1 row can be downstream in V2; an original Stage-2 row can belong in V2 M01-1.

Sources: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §§1–9,13,18; `handoff/workbook_v2/decisions/ADR_WBV2_001_MODULE_RESPONSIBILITY_CLASSIFICATION.md`; `.../ADR_WBV2_002_DOWNSTREAM_MODULES_LOCAL_DUPLICATION.md`; `handoff/workbook_v2/pass08_independence_clarification/PASS08_CLARIFICATION.md`.

**Authority:** V2 is programme-owner-approved as *workbook design direction*, not yet accepted as normative ownership, a production M01-1 module or a replacement ExecPlan. Existing `EXEC_PLAN.md` remains governing for changes; user instruction explicitly restricts this audit to understanding and excludes running tests.

## 2. Source evidence inspected (not merely test receipts)

- `GUARDRAILS.md` and root `AGENTS.md` in full; `EXEC_PLAN.md`, Stage 1 / F1–F4 and Stage 2/3 obligations.
- Accepted M01 brief (674 lines), effective 209-row catalogue, `AUTHORITY_INDEX.md`, owner-approved D104/D116/D123/F4 addenda; prior F4 source-contract discrepancy register, F4 owner policy implementation pause and independent review return.
- Actual V2 Pass08 workbook: 41 worksheets; `M01-1 Derived Raw` expressly states 114 proposed candidates; individual `M21` sheet and `00_Guardrails & Method` read back from the workbook. V2 Pass04 209-row eligibility register, Pass06 30-module allocation and Pass08 peer-self-sufficiency clarification.
- Production owner source: `_stage1.py` (3,712 lines; all Stage-1 kernel families), `api.py` (3,162 lines; graph resolution, M00 field-value ingress, versioning, lineage, calculation/persistence), `_catalogue.py`, `_financial_policy.py`; related product-test **source** for D009, D117, D138, D123 (read, not run).
- Static crosswalk of all 209 effective `Dxxx` catalogue bindings against V2 allocations, kernel-stage ownership, directly declared D inputs and the 30-module register. The accompanying CSV identifies actual source functions, original-stage classification, V2 proposed owner, special deficiencies and existing test-file *mentions* (not test coverage or passage).

## 3. Exact reuse accounting, with no false completion claim

| Population | Original Stage 1: code kernel family available | Original Stage 2: production kernel absent | Total |
|---|---:|---:|---:|
| V2 M01-1 proposed | **113** | **1: D096** | **114** |
| V2 M02–M31 proposed | **61** | **34** | **95** |
| **Original 209** | **174** | **35** | **209** |

The original Stage-1 code contains kernel branches/family paths for all 174 accepted Stage-1 identities. It is **not** a proof that each is mathematically correct or independently review-accepted. No K09–K15 kernel is accepted by the current public `_materialise` dispatcher (`src/nvda_desk/derived_signal_calculation_truth/api.py:2316–2330`); deferred Stage-2 occurrence reuse can read stored history, but does **not** substitute for a production kernel.

Among proposed M01-1:

- **109** belong to original Stage 1 with an original Stage-1-closed dependency graph. An implementation path exists; neither complete row-specific semantic correctness nor separate M01-1 acceptance follows from this count.
- **4** have an original Stage-1 own-kernel path but depend on missing D096: **D097, D098, D107, D108**. Their arithmetic is present in `_stage1.py:1406–1428,1505–1510`; the ordinary public graph cannot presently build them from M00 alone.
- **1: D096** belongs to original K09 Stage 2. It has **no production calculation branch**, despite being a fixed descriptive measurement and an eligible M01-1 candidate (brief §5 K09, line 298).

Thus '113/114 code paths' is **not 99.1% completion**. It excludes the unresolved data contracts, mathematically inadequate branches, 65 convention-freeze flags, public proof, and physical architecture split.

## 4. What can actually be reused

### A. The shared calculation infrastructure: meaningful existing engineering

`api.py:1245` and supporting methods project R signals from the M00 typed public seam; `api.py:2316–3047` resolves declared predecessors, temporal/selection constraints, lineage, parameter/context/convention versions, raw and derived result identities, and persistable occurrences. `_stage1.py:3622–3712` dispatches pure deterministic kernel families; `_postgres.py` implements M01 persistence. These are real foundations to **adapt** for an M01-1 owner rather than rebuild wholesale. Existing `K01–K06`, parts of `K08`, and `K17` are naturally aligned to a descriptive-market layer. But the owner and dispatcher currently accept all original Stage-1 rows, including risk/strategy/policy: they do **not** implement the proposed M01-1 admission boundary.

### B. Exact existing family distribution for the proposed 114

| Original kernel | Candidate count | Reuse assessment |
|---|---:|---|
| K01 time/session | 9 | Core reusable; D009 has a source-semantic issue (below). |
| K02 arithmetic | 40 | Mostly reusable; D123 source contract incomplete; four dependent rows require D096. |
| K03 returns/changes | 33 | Reusable in principle; D104 has a specific owner-authorised skew-rotation equation. |
| K04 baselines/percentiles | 9 | Reusable in principle; D117 R075 role unresolved. |
| K05 realised volatility/risk/ATR | 8 | Reusable exact historical estimators; fixed window/sampling profiles essential. |
| K06 regression/dependence | 6 | Reusable OLS/statistics; fitted *measurements*, not configurable trading-model weights; D138 book-source contract unresolved. |
| K08 objective classifications/flow aggregations | 7 | May be reusable **only with fixed non-strategy P_RULE conventions**: D015, D016, D120, D122, D124, D139, D140. |
| K17 order-flow imbalance | 1 | D145 objective L2 market statistic; event order, snapshots and exact windows matter. |
| K09 ATM-IV interpolation | 1 | D096 **not implemented**. |

**65 of 114** proposed rows have `Requires_NonStrategy_Convention_Freeze=YES` in V2. This is an eligibility/acceptance work item, **not proof that 65 runtime configurations are presently absent**. The implementation's ability to accept an immutable versioned parameter object does not by itself prove that the admissible profile represents a fixed market-measurement definition rather than caller-chosen playbook tuning.

## 5. Specific semantic gaps and source risks, separately classified

### F1 — D009: source-level mismatch between accepted result space and implemented branch (**VERIFIED static discrepancy**)

Brief §5 K01: D009 must classify visible macro vintages `initial`, `latest_known_at_cutoff` **or `revised`**. `_stage1.py:1187–1225` constructs a single latest vintage and returns only `initial` (single visible vintage) or `latest_known_at_cutoff` (multiple). There is no `revised` branch. The existing `test_m01_f4_macro_vintage_public.py` covers initial, latest, future exclusion and incomplete source record, **but no revised-vintage category**. The branch cannot express the entire accepted classification as written. An authority-aligned output/selection correction and proof are needed; this is not merely missing test execution.

### F2 — D096 and its dependent four rows (**VERIFIED missing production graph**)

Accepted §5 K09 defines a bounded 50-absolute-delta **linear interpolation**, selecting exact 0.50 when present, nearest valid bracketing points otherwise, call/put mean when both exist, and single-side-only if expressly admitted. This is not the whole fitted surface/density machinery in K09. The original plan deferred all K09, so production lacks D096 and consequently cannot complete D097, D098, D107 or D108. **Recommendation:** under a newly authorised M01-1 plan, implement precisely the D096 interpolation requirement as foundational market arithmetic; do not activate the rest of Stage 2 simply to obtain it.

### F3 — D123: provider-independent kernel exists; real official-period identity not established (**VERIFIED integration gap, not an allegation of bad controlled arithmetic**)

The owner-authorised D123 correction selects the two latest **distinct official reporting periods** and their highest eligible revision per contract. `_stage1.py:142–245,3641–3650`, `api.py:2338–2350`, and the D123 addendum support *controlled*, M00-projected `official_reporting_period_id`, ordinal, revision ID and revision precedence. The addendum expressly does **not** establish such fields' authoritative mapping from live IBKR/OCC OI streams; ticks/receipt order may not be substituted. Controlled source calculation ≠ live-source end-to-end calculation. A live native mapping and its authority are unknown/unresolved.

### F4 — D117: declared R075 role unresolved (**UNKNOWN until source-contract decision**)

The effective D117 CSV declares `R041;R075`. `_stage1.py:2275–2400` uses `R041` for the numerical historical z-score; the product source `test_m01_f4_rc14_option_volume_z_public.py` requires an R075 observation and checks its lineage/missing-input refusal. That confirms R075 is retained as a **prerequisite** but does not establish its numerical or qualification role. F4 PF-03 expressly directs investigation rather than deletion of that dependency. A versioned source meaning is needed before claiming full semantic closure.

### F5 — D138: depth-snapshot versus event-stream source meaning unresolved (**UNKNOWN whether production defect; material live-data risk**)

Effective D138 uses `R188;R189;R190` + `D011`, while real L2 update streams include operation `R187`. `_stage1.py:2603–2660` computes OLS from co-selected price/size/side raw rows without replaying inserts, updates or deletes. `test_m01_f4_book_slope_public.py` supplies a synthetic **complete `depth_snapshot`**. This proves neither that an admitted provider supplies coherent complete depth snapshots, nor that the event stream alone is reconstructed before D138. F4 PF-04 marks this source-contract question unresolved. Do **not** blindly copy D138 as production-ready.

### F6 — architecture/acceptance is absent for the entire proposed 114 (**VERIFIED**)

- Existing public `api.py` exposes original `D001–D209` semantics through one M01 owner and **rejects K09–K15 kernel work**, rather than exposing an independent `M01-1` service containing precisely market measurement responsibility.
- V2 ADR-WBV2-001 §6 requires independently executable, individually identifiable/testable, durably reproducible and versioned market computations. The Pass04 eligibility audit explicitly records **`NOT_INDIVIDUALLY_VERIFIED_IN_THIS_PASS` for every D**; no separate accepted 114-row V2 contract, independent M01-1 module test/proof register or new architecture admission exists.
- Original Stage-1 F4 review is **unaccepted**, even for the 174 current kernel paths. Earlier full-suite pass counts, where available, are not evidence of independent per-calculation semantic acceptance. No fresh tests were run in this audit.

### F7 — current source preflight and F4 review remain relevant but do not all attach to M01-1

F4 PF-01 (D104) is historically repaired under exact owner equation; PF-02–PF-04 above concern M01-1; PF-05 concerns the 30 old cross-stage rows. PF-08–PF-11 (D186, D178, D189, D192) concern **downstream V2 owners**, not M01-1; later programme-owner approval and financial-policy repair work must not be lost, but should not keep a market-only M01-1 gated by policy calculations. The **13 October independent review return** found four earlier financial-policy integration/rounding/carrier defects and the worker made further repairs without final independent re-review; that is original M01 Stage-1 unfinished work, **not evidence that market calculations are incomplete for those same reasons**.

## 6. Important V2 boundary issue: 114 is provisional, not a magic fixed truth

The 114 represent a row-by-row **proposed eligibility judgement** against fixed measurement meaning, not automatically approved module responsibility. Some of the 95 NO rows have market-facing arithmetic but were excluded because their inputs/parameter conventions are not proven to be strategy-independent:

- **D091** delta bucket: no immutable non-strategy bucket definition established. Consequently **D109, D110 and D121** are ineligible through predecessor closure in the current V2 proposal (M05/M06). Freezing a lawful measurement meaning could justify reassessment, **not immediate admission**.
- **D141/D142** L2 replenishment/resilience: configurable shock, recovery and timing thresholds; they could be measurements only if the thresholds and event definitions are fixed as measurement conventions (M10).
- **D151** breadth: the authorised canonical definition admits a configurable weighted basket; a fixed measurement rule would have to be specified to reclassify the entire canonical identity (M03).
- **D062** next event: even though seconds-to-future-event is fixed arithmetic, the 'earliest *relevant* scheduled event' selection and event universe must be demonstrably non-strategy to qualify (M04).

These are **reconsideration questions**, not defects established by this pass or a mandate to shift rows. Conversely, **D079–D081** conditional beta and **D096** interpolation can legitimately be descriptive despite original labels `REGRESSION` / `SURFACE`, provided the state subset/measurement convention is fixed and not a strategy-trained predictive model. Classifying a whole family or original stage together would be wrong.

## 7. What remains relative to the original M01 brief and relative to V2

**Original accepted M01 (209):** Stage-1 kernel source covers 174, with 144 originally Stage-1-closed graph identities and 30 dependent on the missing Stage 2 graph; 35 Stage-2 own kernels are not present in production; Stage-1 F4 has unresolved acceptance and review. The three-stage original M01 plan is **not completed**. It is not correct to say 'M01 done except a few blockers' or to equate broad passing tests with this claim.

**V2 M01-1 (114 candidates):** 113 have original Stage-1 code routes, one (D096) is missing, four otherwise coded routes require D096, D009 has a definite classification-coverage discrepancy, D117 and D138 require explicit source-contract decisions, D123 has an unresolved **real provider** mapping, 65 have a marked convention-freeze obligation, and **all** require new independent M01-1 owner/interface/proof acceptance. Neither 'fully written' nor 'fully tested' is established.

**V2 M02–M31 (95 proposed):** 61 have own-kernel routes in original Stage 1; 34 belong to original Stage 2 and have no current production kernel. **None of the 30 peer modules is implemented as an independent runtime owner**. The 107 original across-group D-to-D references (67 ordered pairs) are **historical lineage**, not V2 runtime interfaces. Future peer implementations must reproduce any strategy-dependent intermediate chain locally and consume only shared M00/M01-1 ingress; simply moving 61 old Stage-1 functions into 30 packages would leave those peers coupled or with missing prerequisites.

## 8. Recommended engineering sequence (future work, not performed here)

1. **Freeze the market/nonmarket boundary as a governed scope decision** following focused challenges to D009, the convention-dependent 65 and the handful of borderline excluded market operations. Do not assume V2 allocation equals implementation acceptance.
2. **Authorise a new M01-1 execution/acceptance plan** explicitly superseding the original monolithic M01 allocation where required; reconcile authority-index, architecture ownership/public API and versioning without losing canonical D mathematics. Preserve historical M01 work and its review evidence.
3. **Extract/reuse the existing 113 paths and shared infrastructure as a starting implementation**, decoupled from portfolio/candidate/policy contexts; correct the proven D009 gap and resolve D117/D138 source meanings and D123 official-period mapping as distinct obligations. Freeze non-strategy measurement profiles and prove their source selection/units/lineage.
4. **Implement bounded D096 interpolation** as an M01-1 foundational calculation using its exact §5 K09 definition, not the remaining K09 fitted surface/density or other original Stage-2 mathematics. Integrate the other four currently blocked M01-1 predecessor paths.
5. **Then** produce authoritative 114-row (or revised approved population) independent positive, boundary, refusal, temporal, version, provenance, persistence, retry and public-interface proofs; independent review and architecture admission establish M01-1 completion. Only after that should downstream peers be migrated under their separately approved contracts. No tests are being run or bypassed in the present audit.

## 9. What this audit does and does not establish

- **VERIFIED from current source/catalogue:** 209 row mapping, proposed 114/95 split, 113/61 Stage-1 and 1/34 Stage-2 distribution, K09 production absence, D096 four dependent market rows, D009 inability to emit revised status, source calls for D117 and D138, 65 V2 convention flags, lack of a V2 M01-1 production owner.
- **VERIFIED from current authority and records:** D123 controlled official-period contract but no established live native mapping; F4 and Stage-1 not independently accepted; no V2 production admission.
- **UNKNOWN / unproved here:** exhaustive arithmetic and semantic correctness of each 113 existing kernel routes, actual live availability of compatible native feeds, production parameter versions, independent per-row coverage, code performance and complete eventual V2 self-sufficiency.
- **No action authorised/attempted:** no Python/unit/DB tests executed in this pass, no runtime module migration, no implementation corrections, no workbook/catalogue amendments, no acceptance or Git commits.

The companion CSV is an **evidence and location inventory**, not an individual 209-calculation correctness certificate. An existing test file mentioning a D identity is counted as a *text reference only*, never as an executed or semantically discriminating proof.
