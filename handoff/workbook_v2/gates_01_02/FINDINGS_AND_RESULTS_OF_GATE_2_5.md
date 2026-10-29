# Findings and Results of Gate 2.5 — downstream proposal reconciliation

**Leaf:** G2.5 — Reconcile downstream proposals without prematurely canonicalising owners. **Execution boundary:** investigation only, on a new branch from G2.4 HEAD `3406ed90ccacb0558b6c304012d20f75ff35d5a3`; accepted Gate 1 main `77d82bd8ee4268673715fe7e5653b6a65a299b54` remains unchanged.

**Acceptance proposition (root frozen `EXEC_PLAN.md` §1 G2.5):** show each historical 95 D once in its original proposed group; verify 30 historical memberships and historical 107 cross-group D-lineage occurrences, map their *nominal* new labels using accepted G1.5 without implying registry allocation; investigate grouping meaning and conditional local-chain requirements; preserve G2.3/G2.4 unresolved input and eligibility constraints. Recursive *implementation* self-sufficiency, code migration, independent tests, and actual owner admission are later E/implementation obligations.

**Disposition:** `READY_FOR_OWNER_CONSIDERATION_AS_HISTORICAL_AND_CONDITIONAL_GROUP_ANALYSIS`; **not** proof of 30 viable future modules, no approved new D owner and no peer self-sufficiency. Five original groups have zero currently demonstrated downstream D members; 21 original downstream-proposed identities remain materially classification-unknown. Gate 2 cannot be accepted on these facts alone.

## 1. Authority and source identity

- Current instructions: complete `GUARDRAILS.md`, `AGENTS.md`, frozen `EXEC_PLAN.md` G2.5 and cumulative-register law; Gate 1 owner acceptance `GATE_1_OWNER_ACCEPTANCE_20261016.md` (16 October 2026). G1.5 §§A–E is the **accepted** provisional P01–P30 → new-label crosswalk. Current registered `M01` retains D001–D209; `M00` owns R. No M02/M03+ successor is registered or admitted.
- Domain/architectural intent: original `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 kernel families and §§7–17, effective per-D catalogue (including accepted amendments), ADR-WBV2-001, ADR-WBV2-002, Pass08 clarification, master commissioning brief §§1–6.B, §6.E (future fuller scope), architecture `AK-OWN-001`, `AK-DEP-001`, `AK-SEAM-001`, `AK-INGRESS-001–005` and `AK-EXT-001`. Stage scheduling, legacy model labels and workbook `NO` do not establish future peers.
- Historical source roles: Pass06 module register (30 group concepts), Pass06 allocation CSV (95 historical membership assertions), Pass06 107 references (M01 D graph, not interfaces), Pass08 workbook module register, allocation tab and all 30 module sheets (reader-facing same proposals). G2.3 provides verified static closure and explicitly unproved source sufficiency; G2.4 provides current classification evidence. The CSV/workbook are cross-checked against effective catalogue, not elevated to mathematical authority.

**Inspected bytes — SHA-256 (exact current tracked files):**

| Source | SHA-256 |
|---|---|
| `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` | `67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549` |
| `handoff/workbook_v2/pass06_modules/PASS06_30_MODULE_REGISTER.csv` | `26bdac8cbf3676f003479084844d782ca7d94104fae8dc71d200d17e0a2a5fb8` |
| `handoff/workbook_v2/pass06_modules/PASS06_95_D_MODULE_ALLOCATIONS.csv` | `e1c276ca51a64204e9dd7538ea8fe1ce11e897fffc1412240552cec9fcfd0175` |
| `handoff/workbook_v2/pass06_modules/PASS06_107_CROSS_MODULE_D_REFERENCES.csv` | `b027372460c82031b700dcd9fffbd0fb44684fb4effed569e354152d72487dd1` |
| `handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS08.xlsx` | `c4421d85b356ec3bf2749db381fba67d059a2d89ecd54efcf398e3e880f62742` |
| `handoff/workbook_v2/gates_01_02/FINDINGS_AND_RESULTS_OF_GATE_2_4.md` | `d1165041c6f11fb91cd86841a53a76daf18e3480c525ef90b1d82ceb7a8e2c66` |
| `config/architecture/modules.yaml` | `4ee4a0b1d4bb20a687e900ca4c3f78cc3a3d971dcfb4c785772ed7d4110859ee` |
| `handoff/workbook_v2/gates_01_02/FINDINGS_AND_RESULTS_OF_GATE_1_5.md` | `845e1f81bd79db6803b6e31ec57dc0ea1d007f993eb5ab5b1dd9a2b35cc85c81` |
| `handoff/workbook_v2/decisions/ADR_WBV2_003_V2_INVESTIGATION_COMMISSIONING_BRIEF_VERBATIM.md` | `7a05874fbd4971d03bcef47d5cdaf8020f533a10a6a73cf0ef276b8cb446f771` |

## 2. Population, joins, and independent cross-source readback

**VERIFIED via static document/CSV/worksheet inspection:** 209 distinct D keys and an effective 276-edge direct D graph; 95 historical NO rows occur once each in the 95-row allocation CSV and exactly once among the 30 historical group membership lists; the Pass08 allocation tab, Pass08 module-register rows and all 30 module worksheet identity/source rows agree with those CSVs. The 209 historical eligibility review agrees with the 95-row NO population. Each of the 107 distinct historical direct *cross-group* references equals an effective-catalogue D→D edge between two of the historical 95 identities, in the correct consumer/input directions; exactly 67 distinct ordered historical old-module pairs. The sheet annotations reproduce those external predecessors. Zero missing, extra, duplicated, inverted or unaccounted edges were detected under these checks.

**Qualification:** the historical `Resolution=FUTURE_LOCAL_DUPLICATION_AND_DEPENDENCY_MIGRATION_NOT_IMPLEMENTED` value in Pass06 is *obsolete as a future-interface instruction*. ADR-WBV2-002 and Pass08 explicitly supersede its migration wording. The 107 edges are NOT 107 new calls/APIs, not 107 distinct private functions and not 67 approved runtime module dependencies. The original current M01 D graph remains authoritative lineage until separately changed by accepted implementation authority.

**G2.4 semantic divergence:** Historical 95 downstream-proposed D rows comprise **74 established downstream disqualifiers** and **21 unresolved M02-versus-downstream classifications**; they do NOT constitute 95 verified future downstream owners. Separately, **14 original historical `YES` D rows** are now classification-unknown and have **no P01–P30 group membership**; there is no authority to attach them to one or invent another group. The remaining **100** historical YES rows are only conditionally proposed for shared M02. The 100/74/35 G2.4 assessment is preserved unchanged.

## 3. Distinct responsibilities and non-canonical labels

| Layer | What is established | What must not be inferred |
|---|---|---|
| Original D | One D001–D209 identity/meaning each; effective amended D graph | Copies of arithmetic yield new canonical D identities |
| Current software responsibility | Registered M01 still retains D001–D209; M00 owns raw typed R records | Workbook allocation has moved current M01 ownership |
| Historical research grouping | P01–P30, old working labels M02–M31, original 95 D rows | Old labels are software registry IDs or eligible semantic groups |
| Nominal successor *proposal* | Owner G1.5 working translation `P01/M02→M03`, ... `P30/M31→M32`; proposed shared M02 replaces historical M01-1 *role* | Any numeric successor is reserved/allocated/admitted, or 30-group cardinality is correct |
| Future admitted owner | NONE established for any successor D in this gate | Later E local copies can publish duplicate D identities or use peer-private data |

## 4. Thirty historical group purposes and current classification consequences

The group names and precise D sets below are **original Workbook V2 membership**, not a final accepted future module manifest. `D/U` means established downstream disqualifier / materially unknown among historical assigned outputs; `L` is the number of *historical direct* cross-group consumer→input references; `local external` counts distinct **transitive** D ancestors classified downstream and **outside** this group (would need private noncanonical arithmetic if the peer survives, never peer import); `unknown ext.` counts distinct inherited materially-unknown D ancestors (not presumed executable); `conditional shared` counts unique conditional-M02 ancestor D IDs, not admitted service outputs. A group with `0` downstream has no established reason to remain a distinct downstream module.

| Hist. group / old → nominal new | Historical purpose | Canonical historical outputs | D/U | L | Local external | Unknown ext. | Conditional shared |
|---|---|---|---:|---:|---:|---:|---:|
| P01 `M02` → `M03` | Data-quality scoring and completeness | D006;D007;D008;D158 | 2/2 | 1 | 0 | 1 | 3 |
| P02 `M03` → `M04` | Configured market-condition composites | D040;D041;D061;D070;D084;D132;D151 | 0/7 | 0 | 0 | 0 | 30 |
| P03 `M04` → `M05` | Scheduled event relevance and gating | D062;D064;D065 | 1/2 | 0 | 0 | 0 | 1 |
| P04 `M05` → `M06` | Delta bucket and market-flow grouping | D091;D121 | 0/2 | 0 | 0 | 0 | 3 |
| P05 `M06` → `M07` | ATM straddle implied-move proxy | D109;D110 | 0/2 | 1 | 0 | 1 | 1 |
| P06 `M07` → `M08` | Volatility-surface fit and risk-neutral tails | D102;D111;D112;D113 | 0/4 | 0 | 0 | 0 | 3 |
| P07 `M08` → `M09` | Physical-return forecast and probability comparison | D114;D115 | 2/0 | 3 | 0 | 7 | 25 |
| P08 `M09` → `M10` | Dealer positioning and hedge-pressure inference | D125;D126;D127;D128;D129;D130 | 6/0 | 0 | 0 | 0 | 4 |
| P09 `M10` → `M11` | Limit-order-book resilience assumptions | D141;D142 | 0/2 | 0 | 0 | 0 | 0 |
| P10 `M11` → `M12` | Macro latent factor construction | D146;D147;D148;D149;D150 | 5/0 | 2 | 0 | 3 | 18 |
| P11 `M12` → `M13` | Market and options regime probabilities | D152;D153;D154 | 3/0 | 11 | 12 | 16 | 50 |
| P12 `M13` → `M14` | State-vector assembly | D155 | 1/0 | 8 | 15 | 17 | 51 |
| P13 `M14` → `M15` | Cross-signal dependence and disagreement | D156;D157 | 2/0 | 2 | 16 | 18 | 51 |
| P14 `M15` → `M16` | State identifiability/tradeability scoring | D159 | 1/0 | 5 | 20 | 20 | 52 |
| P15 `M16` → `M17` | Conditional scenario generation | D160 | 1/0 | 4 | 17 | 19 | 54 |
| P16 `M17` → `M18` | Candidate payoff, exposure and stress measurement | D161;D162;D168;D169;D170;D174 | 6/0 | 3 | 18 | 19 | 54 |
| P17 `M18` → `M19` | Prospective execution costs | D133;D164 | 2/0 | 1 | 0 | 1 | 3 |
| P18 `M19` → `M20` | Candidate utility and exposure decisions | D163;D165;D166;D167 | 4/0 | 7 | 29 | 21 | 54 |
| P19 `M20` → `M21` | Expiry, strike and neighbour suitability | D171;D172;D173 | 3/0 | 9 | 31 | 21 | 55 |
| P20 `M21` → `M22` | Risk limits and position sizing | D175;D176 | 2/0 | 5 | 31 | 21 | 54 |
| P21 `M22` → `M23` | Pre-submission entry edge and order-pricing policy | D177;D178 | 2/0 | 4 | 31 | 21 | 54 |
| P22 `M23` → `M24` | Fill and realised transaction measurement | D179;D180;D193 | 3/0 | 0 | 0 | 0 | 1 |
| P23 `M24` → `M25` | Live portfolio Greeks and P&L state | D181;D182;D183;D184;D185 | 5/0 | 0 | 0 | 0 | 0 |
| P24 `M25` → `M26` | Live thesis continuity and invalidation | D186;D187 | 2/0 | 5 | 16 | 17 | 51 |
| P25 `M26` → `M27` | Live continuation, modification and exit valuation | D188;D190;D191 | 3/0 | 9 | 35 | 21 | 54 |
| P26 `M27` → `M28` | Hedge adjustment and live action policy | D189;D192 | 2/0 | 10 | 41 | 21 | 54 |
| P27 `M28` → `M29` | Realised Greek/path P&L attribution | D194;D195;D196;D197;D198;D199 | 6/0 | 6 | 7 | 0 | 5 |
| P28 `M29` → `M30` | Decision process and counterfactual review | D200;D201 | 2/0 | 4 | 32 | 21 | 54 |
| P29 `M30` → `M31` | Forecast/model/signal evaluation and disposition | D202;D203;D204;D205;D206;D207;D208 | 7/0 | 7 | 35 | 21 | 54 |
| P30 `M31` → `M32` | Observation/recalculation scheduling | D209 | 1/0 | 0 | 0 | 0 | 0 |

**Meaningful design disagreement — VERIFIED:** P02, P04, P05, P06 and P09 have **zero established downstream members** (respectively 7, 2, 2, 4 and 2 unknown). They are historical research responsibilities, **not proven future modules**. P01/P03 combine unresolved candidate measurements with independently disqualified downstream gates/scores. Final peer count, contents and numeric labels require classification evidence plus owner decision; the nominal one-place numbering translation may not remain applicable. The other 23 historical groups have at least one downstream-disqualified member, but no output, boundary or independent implementation is admitted here.

## 5. Per-group semantics, full static recursive classification frontier and local-chain consequence

**Method:** For each group, start with its exact canonical output D set and recursively follow the *effective* catalogue D→D dependencies to all reachable D ancestors; reconcile this closure with G2.3. Distinguish (a) own original output D identities, (b) external **established downstream** ancestors that may require local private mathematical copies (never canonical D outputs), (c) external **UNKNOWN** ancestors that cannot yet be assigned to shared M02 or private local strategy arithmetic, and (d) external **conditionally proposed M02** ancestors (possible shared ingress only after admission). Every chain must ultimately respect accepted R/typed context, time, history, model/parameter profiles and refusal; graph closure alone does not establish source adequacy. This is a *static transitive design frontier*, not an E-phase private kernel design or performance/proof of a peer.

### P01 — Data-quality scoring and completeness (`M02` historical; `M03` nominal proposed)

**Boundary assessment:** The required-field policy and composite tradeability/quality score are downstream; D006/D008 and incoming D102 remain unproved as neutral. A putative quality owner cannot turn missing weights or surface semantics into factual completeness.

**Historical canonical members:** D006;D007;D008;D158. **G2.4:** established downstream 2; UNKNOWN 2 (D006;D008). Historical direct cross-group references consumed: 1; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D102. **Conditionally shared M02 D frontier:** 3 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 12 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P02 — Configured market-condition composites (`M03` historical; `M04` nominal proposed)

**Boundary assessment:** All seven configured trend/regime/liquidity/breadth measures still lack admitted non-strategy score or basket versions. Their historic exclusion does not establish a downstream software responsibility.

**Historical canonical members:** D040;D041;D061;D070;D084;D132;D151. **G2.4:** established downstream 0; UNKNOWN 7 (D040;D041;D061;D070;D084;D132;D151). Historical direct cross-group references consumed: 0; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 30 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 29 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P03 — Scheduled event relevance and gating (`M04` historical; `M05` nominal proposed)

**Boundary assessment:** D065 is a configured event applicability gate. D062 event selection/provider and D064 event score/provider are separately unknown; event timing cannot be invented or replaced by receipt-time approximations.

**Historical canonical members:** D062;D064;D065. **G2.4:** established downstream 1; UNKNOWN 2 (D062;D064). Historical direct cross-group references consumed: 0; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 1 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 4 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P04 — Delta bucket and market-flow grouping (`M05` historical; `M06` nominal proposed)

**Boundary assessment:** D091 needs exact delta-bucket policy; D121 inherits it. Neither is established as strategy-dependent merely because the legacy review excluded it.

**Historical canonical members:** D091;D121. **G2.4:** established downstream 0; UNKNOWN 2 (D091;D121). Historical direct cross-group references consumed: 0; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 3 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 9 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P05 — ATM straddle implied-move proxy (`M06` historical; `M07` nominal proposed)

**Boundary assessment:** D109 and D110 inherit D091 bucket identity. Historical P05 consumes P04 lineage, not a legitimate peer API.

**Historical canonical members:** D109;D110. **G2.4:** established downstream 0; UNKNOWN 2 (D109;D110). Historical direct cross-group references consumed: 1; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D091. **Conditionally shared M02 D frontier:** 1 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 4 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P06 — Volatility-surface fit and risk-neutral tails (`M07` historical; `M08` nominal proposed)

**Boundary assessment:** D102 and D111–D113 depend on a fixed option surface/valuation convention; risk-neutral density must not be labelled a physical-return predictive model.

**Historical canonical members:** D102;D111;D112;D113. **G2.4:** established downstream 0; UNKNOWN 4 (D102;D111;D112;D113). Historical direct cross-group references consumed: 0; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 3 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 11 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P07 — Physical-return forecast and probability comparison (`M08` historical; `M09` nominal proposed)

**Boundary assessment:** D114 is a physical-return model and D115 compares physical with risk-neutral outputs; both downstream. The D111 surface predecessor and D061/D070/D079–D081 model-context inputs remain unresolved.

**Historical canonical members:** D114;D115. **G2.4:** established downstream 2; UNKNOWN 0 (none). Historical direct cross-group references consumed: 3; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D061;D070;D079;D080;D081;D102;D111. **Conditionally shared M02 D frontier:** 25 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 26 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P08 — Dealer positioning and hedge-pressure inference (`M09` historical; `M10` nominal proposed)

**Boundary assessment:** D125–D130 encode assumed dealer positioning, OI sign and hedge-response scenarios; arithmetic over public OI does not remove these assumptions.

**Historical canonical members:** D125;D126;D127;D128;D129;D130. **G2.4:** established downstream 6; UNKNOWN 0 (none). Historical direct cross-group references consumed: 0; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 4 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 10 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P09 — Limit-order-book resilience assumptions (`M10` historical; `M11` nominal proposed)

**Boundary assessment:** D141/D142 require approved event/cancellation/replenishment thresholds, native L2 semantics and history. Both remain unknown, not automatically downstream.

**Historical canonical members:** D141;D142. **G2.4:** established downstream 0; UNKNOWN 2 (D141;D142). Historical direct cross-group references consumed: 0; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 0 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 10 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P10 — Macro latent factor construction (`M11` historical; `M12` nominal proposed)

**Boundary assessment:** D146–D150 are weighted latent shocks/factors; local-chain operation depends on event-surprise D063 and D061/D070 profiles not yet fixed.

**Historical canonical members:** D146;D147;D148;D149;D150. **G2.4:** established downstream 5; UNKNOWN 0 (none). Historical direct cross-group references consumed: 2; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D061;D063;D070. **Conditionally shared M02 D frontier:** 18 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 33 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P11 — Market and options regime probabilities (`M12` historical; `M13` nominal proposed)

**Boundary assessment:** D152–D154 are fitted regime probabilities and hence downstream, with event D065, book D145 and scoring/frontier input dependencies separately unresolved.

**Historical canonical members:** D152;D153;D154. **G2.4:** established downstream 3; UNKNOWN 0 (none). Historical direct cross-group references consumed: 11; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D065;D125;D126;D127;D128;D129;D130;D146;D147;D148;D149;D150. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D084;D091;D121;D132;D145. **Conditionally shared M02 D frontier:** 50 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 74 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P12 — State-vector assembly (`M13` historical; `M14` nominal proposed)

**Boundary assessment:** D155 has a defined ordered state-vector meaning rather than an arbitrary dictionary; reproducing its inputs requires a large mixed model/state chain and exact freshness/version congruence.

**Historical canonical members:** D155. **G2.4:** established downstream 1; UNKNOWN 0 (none). Historical direct cross-group references consumed: 8; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D065;D125;D126;D127;D128;D129;D130;D146;D147;D148;D149;D150;D152;D153;D154. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D084;D091;D121;D132;D145. **Conditionally shared M02 D frontier:** 51 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 74 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P13 — Cross-signal dependence and disagreement (`M14` historical; `M15` nominal proposed)

**Boundary assessment:** D156/D157 evaluate dependence and disagreement over the non-neutral assembled state; K07 P_SCORE configuration remains a separate instance obligation.

**Historical canonical members:** D156;D157. **G2.4:** established downstream 2; UNKNOWN 0 (none). Historical direct cross-group references consumed: 2; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D065;D125;D126;D127;D128;D129;D130;D146;D147;D148;D149;D150;D152;D153;D154;D155. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D121;D132;D145. **Conditionally shared M02 D frontier:** 51 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 74 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P14 — State identifiability/tradeability scoring (`M15` historical; `M16` nominal proposed)

**Boundary assessment:** D159 is a decision-oriented tradeability/identifiability score inheriting model and data-quality outputs; private evaluation may not read another peer result.

**Historical canonical members:** D159. **G2.4:** established downstream 1; UNKNOWN 0 (none). Historical direct cross-group references consumed: 5; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D007;D065;D125;D126;D127;D128;D129;D130;D146;D147;D148;D149;D150;D152;D153;D154;D155;D156;D157;D158. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D006;D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D102;D121;D132;D145. **Conditionally shared M02 D frontier:** 52 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 78 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P15 — Conditional scenario generation (`M16` historical; `M17` nominal proposed)

**Boundary assessment:** D160 builds conditional joint scenarios, requiring an aligned model/vector/dealer assumption chain, not a universally shared neutral scenario service.

**Historical canonical members:** D160. **G2.4:** established downstream 1; UNKNOWN 0 (none). Historical direct cross-group references consumed: 4; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D065;D114;D125;D126;D127;D128;D129;D130;D146;D147;D148;D149;D150;D152;D153;D154;D155. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 54 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 76 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P16 — Candidate payoff, exposure and stress measurement (`M17` historical; `M18` nominal proposed)

**Boundary assessment:** D161/D162/D168–D170/D174 require candidate structure, scenario, Greek, loss/currency and revaluation context; local chain must preserve each context and F4 risk-domain consistency.

**Historical canonical members:** D161;D162;D168;D169;D170;D174. **G2.4:** established downstream 6; UNKNOWN 0 (none). Historical direct cross-group references consumed: 3; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D065;D114;D125;D126;D127;D128;D129;D130;D146;D147;D148;D149;D150;D152;D153;D154;D155;D160. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 54 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 77 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P17 — Prospective execution costs (`M18` historical; `M19` nominal proposed)

**Boundary assessment:** D133/D164 depend on intended order, fills/cost schedule and market book; they cannot be admitted as strategy-independent market slippage data.

**Historical canonical members:** D133;D164. **G2.4:** established downstream 2; UNKNOWN 0 (none). Historical direct cross-group references consumed: 1; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D132. **Conditionally shared M02 D frontier:** 3 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 11 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P18 — Candidate utility and exposure decisions (`M19` historical; `M20` nominal proposed)

**Boundary assessment:** D163/D165–D167 are candidate-utility and exposure-selection decisions; a local copy of expected cost/scenario arithmetic does not create a second canonical output.

**Historical canonical members:** D163;D165;D166;D167. **G2.4:** established downstream 4; UNKNOWN 0 (none). Historical direct cross-group references consumed: 7; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D007;D065;D114;D125;D126;D127;D128;D129;D130;D133;D146;D147;D148;D149;D150;D152;D153;D154;D155;D156;D157;D158;D159;D160;D161;D162;D164;D168;D174. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D006;D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 54 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 79 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P19 — Expiry, strike and neighbour suitability (`M20` historical; `M21` nominal proposed)

**Boundary assessment:** D171–D173 are expiry/strike/neighbour candidate-ranking scores; exact candidate universe and weights are policy inputs and source D091/D102/D111 are still unknown.

**Historical canonical members:** D171;D172;D173. **G2.4:** established downstream 3; UNKNOWN 0 (none). Historical direct cross-group references consumed: 9; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D007;D065;D114;D125;D126;D127;D128;D129;D130;D133;D146;D147;D148;D149;D150;D152;D153;D154;D155;D156;D157;D158;D159;D160;D161;D162;D163;D164;D165;D168;D174. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D006;D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 55 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 79 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P20 — Risk limits and position sizing (`M21` historical; `M22` nominal proposed)

**Boundary assessment:** D175/D176 control authorised risk ceiling and position sizing; approved F4 common risk/capital domains prevail over raw risk-proxy substitution.

**Historical canonical members:** D175;D176. **G2.4:** established downstream 2; UNKNOWN 0 (none). Historical direct cross-group references consumed: 5; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D007;D065;D114;D125;D126;D127;D128;D129;D130;D133;D146;D147;D148;D149;D150;D152;D153;D154;D155;D156;D157;D158;D159;D160;D161;D162;D163;D164;D165;D168;D174. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D006;D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 54 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 83 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P21 — Pre-submission entry edge and order-pricing policy (`M22` historical; `M23` nominal proposed)

**Boundary assessment:** D177/D178 calculate executable entry economics and order pricing; D178 must preserve once-only costs and admissible expected-fill/utility domains.

**Historical canonical members:** D177;D178. **G2.4:** established downstream 2; UNKNOWN 0 (none). Historical direct cross-group references consumed: 4; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D007;D065;D114;D125;D126;D127;D128;D129;D130;D133;D146;D147;D148;D149;D150;D152;D153;D154;D155;D156;D157;D158;D159;D160;D161;D162;D163;D164;D165;D168;D174. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D006;D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 54 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 79 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P22 — Fill and realised transaction measurement (`M23` historical; `M24` nominal proposed)

**Boundary assessment:** D179/D180/D193 use actual orders/fills/transactions. Their mostly small D graph does not make broker history a market-only foundation.

**Historical canonical members:** D179;D180;D193. **G2.4:** established downstream 3; UNKNOWN 0 (none). Historical direct cross-group references consumed: 0; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 1 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 9 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P23 — Live portfolio Greeks and P&L state (`M24` historical; `M25` nominal proposed)

**Boundary assessment:** D181–D185 use live quantities/account P&L plus contract Greeks. The absence of D predecessors is not absence of typed/live external state.

**Historical canonical members:** D181;D182;D183;D184;D185. **G2.4:** established downstream 5; UNKNOWN 0 (none). Historical direct cross-group references consumed: 0; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 0 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 9 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P24 — Live thesis continuity and invalidation (`M25` historical; `M26` nominal proposed)

**Boundary assessment:** D186/D187 are entry-state similarity and live thesis invalidation; exact entry/context and model/event provenance required.

**Historical canonical members:** D186;D187. **G2.4:** established downstream 2; UNKNOWN 0 (none). Historical direct cross-group references consumed: 5; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D065;D125;D126;D127;D128;D129;D130;D146;D147;D148;D149;D150;D152;D153;D154;D155. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D084;D091;D121;D132;D145. **Conditionally shared M02 D frontier:** 51 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 74 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P25 — Live continuation, modification and exit valuation (`M26` historical; `M27` nominal proposed)

**Boundary assessment:** D188/D190/D191 combine live continuation, modification-set and exit economics; matched state, costs and version must stay local to future peer.

**Historical canonical members:** D188;D190;D191. **G2.4:** established downstream 3; UNKNOWN 0 (none). Historical direct cross-group references consumed: 9; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D007;D065;D114;D125;D126;D127;D128;D129;D130;D133;D146;D147;D148;D149;D150;D152;D153;D154;D155;D156;D157;D158;D159;D160;D161;D162;D163;D164;D165;D168;D174;D181;D182;D183;D184. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D006;D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 54 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 80 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P26 — Hedge adjustment and live action policy (`M27` historical; `M28` nominal proposed)

**Boundary assessment:** D189/D192 are hedge/action policies, including approved F4 clipping/precedence. D192 has 117 distinct D ancestors; no direct 107-reference inventory establishes independent execution.

**Historical canonical members:** D189;D192. **G2.4:** established downstream 2; UNKNOWN 0 (none). Historical direct cross-group references consumed: 10; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D007;D065;D114;D125;D126;D127;D128;D129;D130;D133;D146;D147;D148;D149;D150;D152;D153;D154;D155;D156;D157;D158;D159;D160;D161;D162;D163;D164;D165;D168;D174;D175;D181;D182;D183;D184;D186;D187;D188;D190;D191. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D006;D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 54 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 84 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P27 — Realised Greek/path P&L attribution (`M28` historical; `M29` nominal proposed)

**Boundary assessment:** D194–D199 are realised Greek/path attribution over actual live/fill history, with interval alignment and residual reconciliation.

**Historical canonical members:** D194;D195;D196;D197;D198;D199. **G2.4:** established downstream 6; UNKNOWN 0 (none). Historical direct cross-group references consumed: 6; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D168;D179;D181;D182;D183;D184;D193. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 5 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 16 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P28 — Decision process and counterfactual review (`M29` historical; `M30` nominal proposed)

**Boundary assessment:** D200/D201 use decision-quality/counterfactual EvaluationSet, not a market measurement despite deterministic scoring.

**Historical canonical members:** D200;D201. **G2.4:** established downstream 2; UNKNOWN 0 (none). Historical direct cross-group references consumed: 4; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D007;D065;D114;D125;D126;D127;D128;D129;D130;D133;D146;D147;D148;D149;D150;D152;D153;D154;D155;D156;D157;D158;D159;D160;D161;D162;D163;D164;D165;D166;D168;D174. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D006;D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 54 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 79 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P29 — Forecast/model/signal evaluation and disposition (`M30` historical; `M31` nominal proposed)

**Boundary assessment:** D202–D208 evaluate forecast/model/outcome quality; D204/D205 have zero R/D graph predecessors but mandatory matched EvaluationSet, which cannot be supplied by market history alone.

**Historical canonical members:** D202;D203;D204;D205;D206;D207;D208. **G2.4:** established downstream 7; UNKNOWN 0 (none). Historical direct cross-group references consumed: 7; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** D007;D065;D114;D125;D126;D127;D128;D129;D130;D133;D146;D147;D148;D149;D150;D152;D153;D154;D155;D156;D157;D158;D159;D160;D161;D162;D163;D164;D165;D166;D168;D174;D179;D193;D200. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** D006;D008;D040;D041;D061;D062;D063;D064;D070;D078;D079;D080;D081;D082;D084;D091;D102;D111;D121;D132;D145. **Conditionally shared M02 D frontier:** 54 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 84 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

### P30 — Observation/recalculation scheduling (`M31` historical; `M32` nominal proposed)

**Boundary assessment:** D209 governs observation/recalculation scheduling rather than market data; its RecalculationSchedule authority and event consumption do not imply a trading orchestrator.

**Historical canonical members:** D209. **G2.4:** established downstream 1; UNKNOWN 0 (none). Historical direct cross-group references consumed: 0; exact occurrences remain in the 107-reference source and per-D register, not new interfaces.

**Recursive local arithmetic frontier (external established downstream ancestors):** NONE. These are **potentially required private implementations** *only if* the group is ultimately admitted with its currently proposed outputs. Own established downstream D outputs remain canonical once, but cannot be supplied by a different peer.

**Unresolved external D frontier:** NONE. **Conditionally shared M02 D frontier:** 0 D identifiers; exact identities recoverable from per-row `G2_3_Transitive_D_Closure` and G2.4 classifications. **Raw terminal R frontier:** 1 distinct R identities (full per-row R sets and types in G2.3).

**Receiving work:** source/domain owner must resolve each implicated unknown source or classification in G2.6/later accepted authority; programme owner must decide whether this group and its D output set remain a lawful distinct responsibility; later E must design named local private intermediates, source/context/parameter/version/lineage/persistence, public M00/admitted M02 ingress and independent/no-peer-runtime tests before implementation admission. No private copies or external API interfaces are authorised here.

## 6. Material blockers and future decisions without hidden transfer

1. **Five wholly unresolved old groups (P02/P04/P05/P06/P09).** Resolve the seven K07/basket, delta bucket and descendants, fitted risk-neutral surface/density, and L2 resilience threshold fixedness issues before treating their historic grouping as future downstream modules. A future neutral outcome could reduce or eliminate those peer proposals; a downstream outcome requires independent, versioned owner scope. Neither outcome is chosen here.
2. **P01/P03 mixed populations.** Preserve D007/D158 and D065 downstream disqualifiers separately from D006/D008 and D062/D064 uncertainties. P01 depends on D102 whose approved pricing convention/model remains unresolved; P03 requires selected event-source fields and importance semantics. Determine what stays shared versus local and whether the original grouped responsibilities should split or consolidate.
3. **14 historical `YES` rows with no downstream group.** `D063,D078,D079,D080,D081,D082,D117,D122,D123,D124,D138,D139,D140,D145` remain materially unknown and **unallocated** as future M02 or downstream peers; their possible dependency impact across historical groups is captured in §5. Never silently assign them to a P group merely because a successor needs an input.
4. **Recursive source and score insufficiency.** D063 event-provider selection; D123 official-OI period; D138 standing L2 book, D145 position-indexed provider operations; the 24 K07 score-profile instances and other G2.4 unknown conventions remain unknown or blocked at their respective contracts. Rows already independently downstream remain downstream but their executable chains still need these repairs. Distinguish proof of *mathematical classification* from later evidence of a runnable source instance.
5. **Local chain and peer independence.** The 107 original direct references are just a subset of reachable upstream calculations. Some later groups (P11–P29) expose dozens of strategy-dependent transitive ancestors (§5); a non-peer-dependent successor must implement needed non-neutral mathematics locally, with new **private** intermediate names/versions and lineage, without changing the single canonical D identity or silently changing accepted equations. The actual source reuse, private namespaces, persistence isolation, independent execution and tests are future E, not verified by this investigation.
6. **Lawful identity and admitted M02 readiness.** The nominal new labels depend on G1.5 and current registered allocation, and are **not reservations**. New `create` ingress resolves the next available number only after exact accepted implementation authority; a changed count/order requires programme-owner reconciliation, not manual ID edits. The 100 conditional M02 candidates are not a currently available public module. No authorised peer may consume private old-M01 outputs under the future architecture merely because an M01 edge exists today.

**Incorrect claims expressly rejected:** (a) 95 historical exclusion labels mean 95 future downstream owners; (b) the historical 30-group count or shift M02→M03 is final; (c) Pass06 “dependency migration” creates runtime calls; (d) 107 cross-group edges alone are a complete local implementation plan; (e) local private arithmetic creates duplicate canonical D outputs; (f) a missing D ancestry proves no context/source dependencies; (g) a graph path to an anticipated M02 candidate proves a working shared seam. No such proposition is established.

## 7. Cumulative register mutation and exact stop

`D001_D209_TRACEABILITY.csv` has **209 rows and 99 columns** (previously 89; 10 appended G2.5 evidence fields). All original 89 fields are preserved **byte-equivalent at parsed cell level**, including 209 identities, current M01 owner, historical 95 memberships and all G2.1–G2.4 observations and classifications. The new G2.5 fields carry independent historical group readback, G1.5 nominal new label, current membership disqualifier/unknown mix, exact original cross-group consumer/input edges, static recursive-chain report pointer, zero-runtime-edge requirement and required receiving decision. For the 114 historical YES rows (including 14 now UNKNOWN), no P group or nominal downstream label is invented. `Future_Admitted_Owner` remains unchanged for every row.

Only this findings document and the cumulative CSV were changed. Existing source workbooks, Pass06 registers, normative mathematics, source/architecture registries, `EXEC_PLAN.md`, `GUARDRAILS.md`, `AGENTS.md`, code, tests and runtime configuration were not changed. **Validation performed:** document/CSV/Pass08 worksheet semantic identity and edge checks, graph recursion integrity, controlled CSV parse/schema/source/hash checks, Git ancestry and archive extraction/readback. **Not performed:** app tests, database work, lint/typecheck, executable peer design/proof, production code changes, main merge, owner acceptance, G2.6 or future E.

**G2.5 conclusion:** historically exact group identities and references are **VERIFIED**; the private-computation frontier is **INFERRED/CONDITIONAL FROM VERIFIED STATIC GRAPH**; runtime sufficiency, unresolved score/source inputs, final 30 groups, prospective numeric identities and future admitted owners are **UNKNOWN/UNASSESSED** as appropriate. G2.5 is ready for owner consideration at its bounded documentary reconciliation proposition; Gate 2 still has material blockers for classification, decision and admission. Stop after G2.5.
