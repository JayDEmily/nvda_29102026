# NVDA V2 — Evidence-grounded understanding and assessment

**Date:** 14 October 2026 (Australia/Melbourne)  
**Status:** **PARTIAL SOURCE ASSESSMENT / IMPLEMENTATION NOT AUTHORISED / NOT A REVIEW ACCEPTANCE**  
**Authority:** current user commissioning brief; root `GUARDRAILS.md`; root `AGENTS.md`; accepted original `EXEC_PLAN.md`; effective M01 catalogue and specific approved addenda; V2 workbook/ADRs as **design direction**.

## Executive answer to the two questions

**1. Against original M01:** the repository retains the original M01 as a `bootstrap`, **not active**, owner of D001–D209 (`config/architecture/modules.yaml`). The public owner (`api.py:2316–2330`) accepts the ten original Stage-1 kernel families but refuses the seven Stage-2 families. The accepted catalogue reconciles **174 Stage-1 / 35 Stage-2** rows. Exactly **144 Stage-1** rows have Stage-1-only transitive predecessors; **30** have one or more Stage-2 predecessors. Stage-1 F4 remained **unaccepted**, and the latest preserved worker checkpoint expressly stops before final whole-stage proof and independent review. Stage 2 and whole-M01 acceptance remain outstanding. Dispatch presence is neither row correctness nor runtime acceptance.

**2. Against V2:** the current proposed 114/95 classification reconciles all 209 D identities once. **113/114 proposed M01-1 rows** are attached to an existing Stage-1 family; D096 is not implemented. Four further rows (D097, D098, D107, D108) are dependent on the missing D096. Existing numerical, M00 ingress, selection, lineage and persistence facilities merit reuse **with isolation and repairs**, not a wholesale copy of the original module. The source currently does **not** implement or admit a separately bounded V2 M01-1 owner, and none of the downstream M02–M31 identities is an independent runtime peer. Important mathematical/source discrepancies were independently identified below. **No claim of M01-1 readiness or 209-row semantic certification is supported.**

## 1. Baseline and exact evidence identity

- Primary uploaded archive: `NVDA_WORKBOOK_V2_PASS08_SELF_SUFFICIENCY_CLARIFIED_FULL_GIT_20261014.tar(4).gz`, SHA-256 `0b5a459e6620d617c539bd8aa3f4830fcc176c9ecd7440484adc983d85b29429`.
- Supporting uploaded audit archive: `NVDA_M01_M011_SEMANTIC_AUDIT_20261014.tar(3).gz`, SHA-256 `488e9462f9189b97ab4609bda9d2164e15c09ae980b8eb6296b7b8b089523afc`.
- Primary extracted Git branch `work/workbook-v2-pass01-guardrails-method-20261014`, HEAD `514040e0d32cf2efd0629c08cdf056b4c8b3f766`, tree `a316a20b4245fd11b61d71d8bd7ed1778236f7ea`. Clean `git status --porcelain=v1` on inspection; `git fsck --full --no-reflogs` exit 0, dangling/unreachable objects reported. This verifies the checked archive's Git integrity to the command's scope, **not** semantic acceptance.
- Effective authoritative catalogue in `handoff/m01_completion/authority/` and runtime catalogue both SHA-256 `26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803` (D134/135, D116, D175/D189 amendments per `AUTHORITY_INDEX.md`). Earlier digests are historical.
- Original reference workbook SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`. V2 Pass08 workbook SHA-256 `c4421d85b356ec3bf2749db381fba67d059a2d89ecd54efcf398e3e880f62742`; **41 actual worksheets**, seven original reference tabs retained.
- No tests, application runtime, database server, formatting suites, type checking or code modifications were performed in this assessment. Static parsing, repository/Git inspection and hash checks only.

## 2. Correct architectural interpretation

The former M01 contract (`authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §§1–18) was **all deterministic derived calculation truth**, covering descriptive market signals as well as tuned scores, model outputs, portfolio and position economics, risk limits, candidate/action policies and evaluation. Determinism is not the same as strategy independence. Old Stage 1 versus Stage 2 is a **kernel scheduling division**, not an architectural domain boundary.

The V2 decision (`ADR_WBV2_001`, `ADR_WBV2_002`, Pass08) separates M00 raw observation truth; a shared descriptive, strategy-independent M01-1 foundation; and thirty independently executable downstream peers. Raw data include account, contract, operational and other records, not just market quotes. M01-1 can own complex regressions and fixed measurement conventions where all their meanings/inputs remain descriptive and strategy-independent. Every downstream peer may read M00 and eligible M01-1 public results; it cannot call or privately read another peer. Equivalent strategy-dependent intermediate arithmetic is duplicated **locally** with distinct private identity, version, lineage and proof. Canonical D identities remain singular.

The current architecture (`docs/architecture/ARCHITECTURAL_OBJECT_TAXONOMY.md`) requires `M` plus a decimal suffix: **`M01-1` is not a valid current registered runtime identity**. Current `M01` is already consumed, `M02–M31` are **working** labels only. The proposed minimum-disruption path is a separately approved semantic narrowing of registered **M01**, preserving `M01-1` as the V2 capability/design label, and later admission of M02–M31 through authorised ingress. Neither renaming nor automatic splitting is permissible. This precise identity decision is required before production transition.

## 3. Census: distinct completion propositions

| Proposition | Identified population | What it proves / does not prove |
|---|---:|---|
| Effective normative D catalogue | 209 | Every original D001–D209 exists once in the current CSV |
| Old Stage-1 kernel-family assignment | 174 | Dispatcher path *may* be selected; individual branch correctness unproved |
| Old Stage-1 graph with Stage-1-only predecessors | 144 | Structural eligibility for public calculation, not runtime pass |
| Old Stage-1 graph requiring Stage-2 predecessor | 30 | Own-family calculation may exist but public graph fails closed until predecessors exist |
| Original Stage-2 kernel-family assignment | 35 | Not implemented in current public materialiser |
| V2 proposed M01-1 | 114 | Proposed semantic eligibility, not production allocation |
| V2 proposed M02–M31 | 95 | Exactly one canonical proposed downstream allocation for every excluded identity |
| M01-1 existing Stage-1 family | 113 | Reuse candidate only, not completion percentage |
| M01-1 missing original Stage-2 family | 1 (D096) | Bounded new foundation mathematics required |
| Explicit measurement-convention freeze flags | 65 of 114 | Each flag requires accepted fixed measurement semantics; not itself proof of defect |
| Historical direct peer-group D references | 107, 67 ordered pairs | Lineage crosswalk, **not** runtime peer interface |

The 209-row traceability register and the 95-row recursive root graph are supplied separately. They record source meanings, original/V2 ownership, declared and transitive D/R inputs, typed contexts, profiles, implementation navigation and actual *limits* of verification. They intentionally mark uninspected individual semantic propositions as **UNASSESSED**, not favourable conclusions.

## 4. Production engineering actually present

**VERIFIED source existence, not runtime acceptance:** `src/nvda_desk/derived_signal_calculation_truth/api.py` implements typed request/context/occurrence models; `_OwnerV1._raw_values()` (approximately 1245–1457) projects source-native observations through an M00 public read boundary. `_materialise()` (2316–3046) checks kernel family, profile, selection, required contexts, recursive D predecessors, compatibility, history, versioned calculation identity, exact raw/predecessor lineage and idempotent or append-only persistence. `_stage1.py` contains numeric and temporal kernel families plus event and book helpers. `_catalogue.py` supplies hash-bound current catalogue loading/acyclic graph order. `_postgres.py` supplies a separate owner storage mechanism including `dsct_derived_signal_occurrence_v1`; it does not own market meanings. `_financial_policy.py` currently embeds broader original-M01 financial/risk calculations **not eligible for blanket relocation into M01-1**.

**REUSE_WITH_SEPARATION:** typed ingress contract, occurrence identity, history selection, lineage/version carriers and PostgreSQL mechanism are valuable starting implementations. They presently share the original M01 owner and a broad Stage-1 dispatch. The new boundary needs an explicit allowlist, independently owned measurement profiles, public seam/read contract, persistence/write isolation and transition/version behaviour. No existing old-owner occurrence may be silently relabelled as new-owner truth.

**Historical evidence:** `handoff/m01_completion/proof/f4_20261013_implementation/PAUSE_HANDOFF.md` records proof-first source changes in D178/D175/D189/D192 and associated consumers; a fresh reviewer returned `RETURN_TO_WORKER / RECURRENT_CLASS` at earlier tree `95ae8c3f8078d...`; subsequent repair commits had **not** undergone final independent re-review. The handoff reports 773 derived-signal cases and 74 architecture/bootstrap cases before the last snapshot edits, latest 15 focused cases after them, and 55 PostgreSQL fixture errors in its wider run due the historical non-root host constraint. These are **historical, time/tree-specific test reports**. They do not establish current results or entire Stage-1 acceptance. A foundation-only DS-R01 acceptance was historically recorded; it is not D001–D209 calculation acceptance.

## 5. Material source findings requiring separate remedies

### F-01 — D025 high/low inversion: VERIFIED STATIC DISCREPANCY

The original `Raw Signals` tab defines **R039 = High**, **R040 = Low**. The accepted M01 brief line 123 defines `(last − session_low)/(session_high − session_low)`. Production `_stage1.py:1354–1361` instead assigns `low=R039`, `high=R040` and computes `(last-low)/(high-low)`. This reverses the canonical source meanings. The existing `tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py:29–30` provides inverted source-labelled values (R039=90, R040=110), so its midpoint fixture can mask the error. **REPAIR_REQUIRED** for a V2 market calculation. First establish proper semantic public proof from original raw identities, then correct exact field use and source-labelled test evidence.

### F-02 — D099/D100 R015 meaning mismatch: VERIFIED STATIC DISCREPANCY

The original raw workbook defines **R015 = `Contract.right`, option right C/P**, not strike. Effective D099 and D100 declare `R111;R112;R015`. In `_stage1.py:1430–1501`, D099/D100 build `R015` as a per-contract 'strike' input and require `_d(strike_point.value) == _d(iv_meta["strike"])` (1466–1475). An ordinary correct R015 C/P value is not that numeric strike. `tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py:33–39` supplies **synthetic R015=strike**, so it cannot prove compatibility with the accepted native R015 meaning. The IV and delta contracts require unambiguous C/P co-reference and exact real-strike identity from accepted sources/metadata. **REPAIR_REQUIRED**, preserving D099/D100 accepted numeric skew equations and source identity; do not silently reinterpret R015 as strike.

### F-03 — D009 vintage classification: VERIFIED STATIC DISCREPANCY

The accepted brief §5 K01 line 95 requires three mutually exclusive outputs: `initial`, `latest_known_at_cutoff`, and `revised`. `_stage1.py:1188–1225` selects the latest co-referenced visible vintage and emits only `initial` or `latest_known_at_cutoff`. There is no reachable `revised` output branch. `test_m01_f4_macro_vintage_public.py` has no independent test of the revised-class output. **REPAIR_REQUIRED** with source-vintage selection and independently expected classification cases. The precise treatment of a requested historical vintage must follow the accepted law, not a convenience selection.

### F-04 — D096 and four successors: VERIFIED MISSING FOUNDATION CAPABILITY

The accepted brief §5 K09 line 298 specifies **per expiry, per option side** 0.50 absolute-delta linear interpolation; exact 0.50 when present; nearest bracketing values otherwise; arithmetic call/put mean if both valid; single-side value only when a versioned profile permits and preserves coverage; no unapproved extrapolation. D096 is assigned original K09 and is refused by current `_materialise` Stage-1-only dispatch. D097, D098, D107 and D108 already have K02 arithmetic in `_stage1.py:1406–1428,1505–1510` but require D096 as a predecessor. **NEW_IMPLEMENTATION_REQUIRED** only for accepted bounded D096 mathematics and exact source/selection/version integration. Do not import unrelated fitted-surface D102 or all historical Stage 2.

### F-05 — D117 R075: SOURCE MEANING BLOCKED, NOT A PROVED NUMERICAL DEFECT

Effective D117 declares R041 (current volume) and R075 (Average Option Volume). `_stage1.py:2270–2278,2359–2401` selects R041 historical series for the z-score; R075 appears as an admitted prerequisite rather than visibly participating in the numerical operation. The accepted D116 correction explicitly preserves D117/R075. The precise numerical/bucket/qualification purpose of R075 remains **UNKNOWN**. Requires bounded authority/source-contract resolution; deleting R075 to simplify code is forbidden.

### F-06 — D123 official OI period: CONTROLLED SEMANTICS PRESENT, LIVE CONTRACT UNKNOWN

The approved `D123_CALCULATION_DEFINITION_AUTHORISED_CLARIFICATION_20261011.md` admits provider-independent, explicitly mapped official period IDs, chronological order and within-period revision precedence. `_stage1.py:142–243` selects latest two distinct eligible periods; `api.py:2485–2502` retains only the selected raw lineage. The addendum explicitly **does not** establish how live IBKR/OCC ticks 27/28 map to official reporting periods/revisions. Controlled arithmetic can be independently proven without asserting real-source support. Production live mapping is **BLOCKED pending primary provider evidence**, not proof that the controlled calculator is defective.

### F-07 — D138 order-book source meaning: UNRESOLVED SOURCE CONTRACT

Accepted D138 computes per-side OLS slope of cumulative depth against distance to D011 midpoint. `_stage1.py:2603–2660` assembles co-referenced R188/R189/R190 price/size/side rows and fits their slopes. Source workbook describes L2 update events with R187 operation semantics. `test_m01_f4_book_slope_public.py` uses a controlled complete `depth_snapshot`. Whether an admitted live M00 projection guarantees a consistent full book state, or whether event reconstruction is required before D138, is **UNKNOWN**. Do not call it a defect solely because the fixture uses snapshots.

### F-08 — wider original-M01 financial/policy repairs: DOWNSTREAM PRESERVE

The latest 13 October F4 repair/handoff concerns accepted risk-scope, D175 limits, D178 execution cost, D189 four-Greek clipping, D192 breach and associated producer evidence. Their production status and historical proof must remain traceable, including the unaccepted reviewer-return candidate. The V2 design moves their **semantic responsibility** downstream, but does not authorise changing their accepted equations, discarding repairs or building new shared downstream strategy functions.

### F-09 — 65 convention flags: INDIVIDUAL DECISIONS PENDING

A measurement-convention flag is not an error. For each flagged candidate, review the actual numeric range, unit, selection window/history, comparator/basket/source coverage, parameter admissibility, versioning and dependency context. A fixed non-strategy convention may legitimately be part of M01-1. Caller-chosen strategy coefficients, candidate/portfolio/order-intent choices and silent redefinition may not. A per-row authority version or bounded owner decision must precede acceptance wherever not already established.

## 6. Downstream self-sufficiency baseline and workload distribution

Each downstream module must implement its owned canonical outputs and any required **private chain** of strategy-dependent calculations belonging historically to other modules. The counts below are derived recursively from the current accepted D graph, and count **distinct historical D-equivalent nodes**, not code files, tests or implementation effort. They are *not* runtime peer dependencies.

| Module | Responsibility | D | Private | S2 | Direct |
|---|---|---|---|---|---|
| M02 | Data-quality scoring and completeness | 4 | 1 | 1 | 1 |
| M03 | Configured market-condition composites | 7 | 0 | 0 | 0 |
| M04 | Scheduled event relevance and gating | 3 | 0 | 0 | 0 |
| M05 | Delta bucket and market-flow grouping | 2 | 0 | 0 | 0 |
| M06 | ATM straddle implied-move proxy | 2 | 1 | 0 | 1 |
| M07 | Volatility-surface fit and risk-neutral tails | 4 | 0 | 4 | 0 |
| M08 | Physical-return forecast and probability comparison | 2 | 4 | 4 | 3 |
| M09 | Dealer positioning and hedge-pressure inference | 6 | 0 | 5 | 0 |
| M10 | Limit-order-book resilience assumptions | 2 | 0 | 0 | 0 |
| M11 | Macro latent factor construction | 5 | 2 | 0 | 2 |
| M12 | Market and options regime probabilities | 3 | 22 | 9 | 11 |
| M13 | State-vector assembly | 1 | 26 | 9 | 8 |
| M14 | Cross-signal dependence and disagreement | 2 | 27 | 9 | 2 |
| M15 | State identifiability/tradeability scoring | 1 | 33 | 10 | 5 |
| M16 | Conditional scenario generation | 1 | 30 | 13 | 4 |
| M17 | Candidate payoff, exposure and stress measurement | 6 | 31 | 17 | 3 |
| M18 | Prospective execution costs | 2 | 1 | 1 | 1 |
| M19 | Candidate utility and exposure decisions | 4 | 43 | 18 | 7 |
| M20 | Expiry, strike and neighbour suitability | 3 | 45 | 18 | 9 |
| M21 | Risk limits and position sizing | 2 | 45 | 18 | 5 |
| M22 | Pre-submission entry edge and order-pricing policy | 2 | 45 | 19 | 4 |
| M23 | Fill and realised transaction measurement | 3 | 0 | 0 | 0 |
| M24 | Live portfolio Greeks and P&L state | 5 | 0 | 0 | 0 |
| M25 | Live thesis continuity and invalidation | 2 | 27 | 9 | 5 |
| M26 | Live continuation, modification and exit valuation | 3 | 49 | 19 | 9 |
| M27 | Hedge adjustment and live action policy | 2 | 55 | 19 | 10 |
| M28 | Realised Greek/path P&L attribution | 6 | 7 | 5 | 6 |
| M29 | Decision process and counterfactual review | 2 | 46 | 19 | 4 |
| M30 | Forecast/model/signal evaluation and disposition | 7 | 49 | 23 | 7 |
| M31 | Observation/recalculation scheduling | 1 | 0 | 0 | 0 |

`Private` counts the distinct recursive predecessor D identities **assigned to different downstream groups** which this peer cannot call and must locally reproduce if genuinely required for its calculations. `S2` counts distinct K09–K15 nodes required anywhere in that module's transitive output closure, including its own canonical outputs. `Direct` counts historical direct cross-group edges emanating from its canonical D outputs. Full exact sets, edges, ultimate R inputs, eligible M01-1 inputs, external typed contexts and missing Stage-2 source kernels are enumerated in `04A_DOWNSTREAM_95_ROOT_CLOSURES.csv` and `04B_DOWNSTREAM_30_PEER_SUMMARY.csv`.

**Limits:** This graph closure is a verified static dependency inventory; it does **not** establish that every local chain is strategy-dependent, correctly sourced, compatible with each peer's context, or already implemented. The algorithm retains the original D meanings as labels but does not create a second canonical D occurrence or allow peer imports. The per-peer recursive **mathematical and source-contract semantic review remains pending**. No M02–M31 independently admitted runtime module is present in `config/architecture/modules.yaml`.

## 7. Assessment completion boundary

**VERIFIED here:** archive hashes, Git branch/clean condition/object-check exit; effective catalogue digest; 209 identity crosswalk; V2 114/95 split; original 174/35 and 144/30 boundaries; 107 cross-group direct edges; 65 convention flags; architectural identifier conflict; source/test discrepancies F-01/F-02/F-03; D096 absence and four successors; D117/D123/D138 contract limits; historical F4 acceptance status as recorded.

**Not established:** independent full semantic proof for all 209 calculations; correctness or complete test coverage of the 113 nominal market Stage-1 code routes; a native-source proof for D123/D138; full correctness of per-peer private intermediate chains; clean database/production runtime behaviour under an authorised V2 boundary; numerical completion percentage; a newly accepted ExecPlan or independently admitted V2 architecture.

The 209-row register therefore contains `STATIC_ACCOUNTING_VERIFIED;SEMANTIC_UNASSESSED` for the unsampled individual meanings. A prior audit/test mention is navigation, not a proof. This is a **recoverable partial investigation handoff**, not a complete source-certified commissioning study. The remaining in-scope deep review is explicitly queued in the proposed execution plan and unresolved register.

## 8. Source references

See `07_EVIDENCE_INDEX.md` for precise file names, source semantics, authorities, reviewed history and forbidden overclaims. The deliverable files were written outside the Git repository. No active plan, registry, code, test or workbook was modified.
