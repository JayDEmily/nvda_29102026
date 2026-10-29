# F1b — authority-derived Stage-1 relationship classes

**Status:** Evidence-only classification, not an alternative dependency authority or acceptance.

- Normative edge source: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, SHA-256 `63bc1b776fc8fa8ba82eb3c9b16916f295c9ec3d480a5a068937c2f25146f5f5`.
- Authoritative meaning: companion brief §5 individual kernel/row rules, §6 immutable contexts, §§7–9 exact edges and field mapping, §§11–14 temporal and R/D lineage, §17 absence.
- `F1_CLASSIFIED_EDGE_MAP.csv` assigns exactly one primary RC class per edge. The `NONE` record for D007 has no dependency edge and is excluded from the 488-edge total.
- A class is an **inventory grouping for proof**, never an invented extra `R`/`D` edge. The row-specific `brief_rule_ref` and `workbook_row` remain decisive. Global mapping/version/cutoff law applies to **every** class, not only the example rows.
- Cardinality describes the accepted relation where determinable (e.g. a window of trades to a signed sum). `UNKNOWN` is intentional where the brief does not give an unambiguous per-edge multiplicity. A broad class can have explicitly overridden per-row cardinality in the CSV.
- `N/A` means the dimension does not exist (for example D007 has no R/D edge); `UNKNOWN` indicates a needed semantic claim is not proved by the cited authority.

## Class definitions and complete membership

### RC01 — Temporal/event/expiry selection (35 census records)
- **Rows:** D001, D002, D003, D004, D005, D006, D008, D010, D062, D065, D085, D086, D209.
- **Authority:** §5 K01; §§8.1,11; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** per-event or as-of selection; D006/D008 require score/time alignment.
- **Material identity:** event/receipt kind; subject where material; exchange calendar/expiry where declared. **Temporal alignment:** event/receipt basis, UTC/local conversion; cutoff; no invented event instant.
- **Cardinality:** UNKNOWN unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `api.py _materialise/_raw_values; _stage1.py _eval_k01/_eval_k07/_eval_k08`; this is a source inventory, not proof of correctness.

### RC02 — Exact same-subject algebraic inputs (29 census records)
- **Rows:** D011, D012, D013, D014, D018, D025, D042, D043, D047, D057, D058, D059, D060, D123.
- **Authority:** §5 K02; §§8.1,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** point/snapshot values not inferred equivalent across different observation IDs.
- **Material identity:** canonical subject; exact contract when option input; versions. **Temporal alignment:** as-of eligible latest; freshness/skew; cutoff.
- **Cardinality:** UNKNOWN unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `api.py _raw_values/_materialise; _stage1.py _eval_k02`; this is a source inventory, not proof of correctness.

### RC03 — Same-subject history and matched time anchor (29 census records)
- **Rows:** D019, D020, D021, D022, D023, D024, D026, D027, D044, D045, D046, D048, D049, D050, D051, D052, D053, D054, D055, D056, D066, D067, D068, D069.
- **Authority:** §5 K03; §§8,8.1; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** history points to one output window; multiple time points mandatory where specified.
- **Material identity:** subject; anchor/window version; ordered observations. **Temporal alignment:** strict historical anchor; no look-ahead or nearest substitution.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _history_anchor/_eval_k03; api.py _materialise`; this is a source inventory, not proof of correctness.

### RC04 — Historical baseline / realised-risk window (17 census records)
- **Rows:** D028, D029, D030, D031, D032, D033, D034, D035, D036, D037, D038, D039.
- **Authority:** §5 K04/K05; §§8,8.1; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** multiple eligible samples -> one result; refuse short/inconsistent sample sets.
- **Material identity:** subject/contract if material; exact versioned baseline/window. **Temporal alignment:** strictly prior baseline or exact sampling window.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k04/_eval_k05; api.py _compatible_history`; this is a source inventory, not proof of correctness.

### RC05 — Regression/dependence aligned input history (20 census records)
- **Rows:** D078, D079, D080, D081, D082.
- **Authority:** §5 K06; §§8,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** aligned feature/response pairs/matrix, exact model input identity.
- **Material identity:** model version; aligned subject basket/factor series; window. **Temporal alignment:** synchronised history and matched returns under cutoff.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _factor_rows/_eval_k06; api.py _materialise`; this is a source inventory, not proof of correctness.

### RC06 — Versioned multi-feature weighted scoring (29 census records)
- **Rows:** D040, D041, D061, D070, D084, D132.
- **Authority:** §5 K07; §§6,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** all required features and extractors; no silent weight renormalisation.
- **Material identity:** exact feature identities/extractors; parameter/context versions. **Temporal alignment:** eligible aligned feature timestamps and required baseline where used.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py extract_scalar/_score/_eval_k07; api.py _materialise`; this is a source inventory, not proof of correctness.

### RC07 — Trade event to eligible quote and tick sign (4 census records)
- **Rows:** D015.
- **Authority:** §5 K08 D015; §§8.1,12,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** one signed classification *of trade* with quote; quote-to-trade matching cardinality not explicitly numbered.
- **Material identity:** same trade subject/contract; R120 source event; R126/R127 and D011 quote temporal match. **Temporal alignment:** quote timestamp/cutoff; prior distinct trade for tick test.
- **Cardinality:** UNKNOWN unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k08 D015; api.py _materialise`; this is a source inventory, not proof of correctness.

### RC08 — Per-trade signed quantity/notional correlation (8 census records)
- **Rows:** D016, D120.
- **Authority:** §5 K08 D015/D016/D120; §§8.1,9,12–14,17; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** many exact signed trade facts -> one sum; missing match cannot silently become zero.
- **Material identity:** same individual R120/R121 trade, contract, multiplier and D015's ultimate M00 observation lineage; never D-raw ID equality. **Temporal alignment:** selected trade window; no forward classification; cutoff.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k08 D016/D120; api.py _occurrence_kernel_value/_materialise`; this is a source inventory, not proof of correctness.

### RC09 — Per-observation trade price/size VWAP aggregation (2 census records)
- **Rows:** D017.
- **Authority:** §5 K02 D017; §§8.1,9,12; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** many price*size pairs -> one VWAP; requires matching source observations.
- **Material identity:** same M00 trade occurrence for R120 and R121; subject; session/window. **Temporal alignment:** session window, cutoff, ordered trade observations.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _align_occurrence_fields/_eval_k02 D017`; this is a source inventory, not proof of correctness.

### RC10 — Exact per-contract predecessor within multi-leg/pair parent (4 census records)
- **Rows:** D109, D170.
- **Authority:** §5 K02 D109/D170; §6 CandidateStructureContext; §§8.1,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** one parent may require several distinct D087/D091 child occurrences.
- **Material identity:** D109 distinct call/put same strike+expiry; D170 candidate leg's exact contract; scoped child policy. **Temporal alignment:** same as-of and cutoff with scoped child policy.
- **Cardinality:** one-to-many unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `api.py _scoped_contract_requests/_materialise; _stage1.py _eval_k02 D109/D170`; this is a source inventory, not proof of correctness.

### RC11 — Versioned bucket/group membership and aggregation (9 census records)
- **Rows:** D091, D121, D122, D124, D128.
- **Authority:** §5 K08 D091/D121/D122/D124/D128; §§6,8.1,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** grouped sums by declared bucket; D091 scalar bucket has single input; class cardinality conditional.
- **Material identity:** exact delta/expiry/strike/member; per-contract D120/D091/D085 membership; P_RULE boundaries. **Temporal alignment:** same qualifying window and cutoff; each source's own contract/time identity.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k08 D091/D121/D122/D124/D128; api.py _materialise`; this is a source inventory, not proof of correctness.

### RC12 — Book-event reconstruction and quote/depth correlation (68 census records)
- **Rows:** D131, D134, D135, D136, D137, D138, D139, D140, D141, D142, D143, D144, D145.
- **Authority:** §5 K02/K08 L2 and K17; §§8.1,9,12; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** event stream -> reconstructed book and aggregate; where quote matching mandatory use compatible book state.
- **Material identity:** subject/option contract, venue, side, level, price, exact L2 events. **Temporal alignment:** sequence/operation/time window, pre/post state and cutoff.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py reconstruct_book/_book_events/_eval_k02/_eval_k08/_eval_k17`; this is a source inventory, not proof of correctness.

### RC13 — Versioned multi-instrument basket and common-return factor alignment (21 census records)
- **Rows:** D071, D072, D073, D074, D075, D076, D077, D083, D151.
- **Authority:** §5 K02/K03/K04/K06; §§6,8.1,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** explicit member set and model response; no opportunistic member substitution.
- **Material identity:** exact subject per member; basket identity; coherent NVDA dependent and market/sector factors. **Temporal alignment:** matched cross-sectional snapshots/history by declared model/window.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _latest_by_subject/_factor_rows/_eval_k06/_eval_k02`; this is a source inventory, not proof of correctness.

### RC14 — Option-contract/delta/strike/expiry and IV geometry (45 census records)
- **Rows:** D087, D088, D089, D090, D092, D093, D094, D095, D097, D098, D099, D100, D101, D103, D104, D105, D106, D107, D108, D110, D116, D117, D118, D119.
- **Authority:** §5 K02/K03/K04; §§8.1,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** multi-strike/delta right comparison where row explicitly demands; otherwise exact contract.
- **Material identity:** exact underlying/contract/strike/right/expiry/delta bucket as applicable. **Temporal alignment:** window, cutoff and matched terms; no nearest strike unless permitted.
- **Cardinality:** UNKNOWN unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k02/_eval_k03/_eval_k04; api.py _selection_policy_satisfies_row_authority`; this is a source inventory, not proof of correctness.

### RC15 — Candidate structure/leg/set/neighbour comparison (42 census records)
- **Rows:** D164, D166, D167, D168, D171, D172, D173, D175, D176, D178, D190.
- **Authority:** §5 K02/K07/K08; §6; §§8.1,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** one candidate or eligible candidate set; explicit ordered membership; neighbour relation never inferred.
- **Material identity:** versioned CandidateStructureContext; CandidateSetContext identity/order/neighbour where bound; exact contract per leg. **Temporal alignment:** same candidate/model and as-of/cutoff.
- **Cardinality:** UNKNOWN unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `api.py _contexts_for_row/_scoped_contract_requests; _stage1.py _eval_k02/_eval_k07/_eval_k08`; this is a source inventory, not proof of correctness.

### RC16 — Live position, fill, execution or attribution state (57 census records)
- **Rows:** D179, D180, D181, D182, D183, D184, D185, D187, D189, D191, D192, D193, D199, D200.
- **Authority:** §5 K02/K08; §6; §§8.1,12,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** matching executed quantity/path/position state; no aggregate Greek proxy for nonlinear repricing.
- **Material identity:** exact position/order/fill M00 occurrence, signed quantities, multiplier and convention where admitted. **Temporal alignment:** same position snapshot or exact path/window and cutoff.
- **Cardinality:** UNKNOWN unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k02/_eval_k08; api.py _contexts_for_row/_materialise`; this is a source inventory, not proof of correctness.

### RC17 — Structured component occurrence/state-vector comparison (26 census records)
- **Rows:** D155, D156, D157, D158, D159, D163, D186.
- **Authority:** §5 K16/K07/K06/K08; §§6,12–13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** ordered named D components into vector; matrices/score consume exactly named component occurrences.
- **Material identity:** D155 component occurrence IDs, units and schema version; D186 entry anchor; relevant model context. **Temporal alignment:** same aligned time/window; entry occurrence explicitly versioned.
- **Cardinality:** many-to-one unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k16/_eval_k06/_eval_k07/_eval_k08`; this is a source inventory, not proof of correctness.

### RC18 — Policy-only D007 (zero R/D dependencies) (1 census records)
- **Rows:** D007.
- **Authority:** §4 D007; §5 K08; §6; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** policy requirement completeness, no R/D edge in catalogue.
- **Material identity:** RequiredFieldPolicy version and requirement identity. **Temporal alignment:** available policy/read eligibility under cutoff.
- **Cardinality:** N/A unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k08 D007; api.py _contexts_for_row`; this is a source inventory, not proof of correctness.

### RC19 — Evaluation/disposition from named model evidence (5 census records)
- **Rows:** D207, D208.
- **Authority:** §5 K07/K08; §§6,13; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** fixed evidence vector and threshold classification; cross-stage dependent D203/D206/D202 deferred.
- **Material identity:** EvaluationSet identity/version and class/feature extractor where required. **Temporal alignment:** evaluation historical window/knowledge cutoff.
- **Cardinality:** UNKNOWN unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k07/_eval_k08; api.py _materialise`; this is a source inventory, not proof of correctness.

### RC20 — Macro observation revision and vintage tracking (3 census records)
- **Rows:** D009.
- **Authority:** §5 K01 D009; §§8.1,11; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** related raw revision fields; latest known vintage not invented.
- **Material identity:** same macro series, release/revision/vintage identity. **Temporal alignment:** as-of visibility and receipt vs release/period distinction.
- **Cardinality:** UNKNOWN unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k01 D009; api.py _raw_values`; this is a source inventory, not proof of correctness.

### RC21 — Versioned macro-event/factor score association (35 census records)
- **Rows:** D063, D064, D146, D147, D148, D149, D150.
- **Authority:** §5 K04/K07; §§6,8,8.1; individual rows and exact edge IDs in the classified CSV.
- **Meaning/correlation:** event series to surprise/factor and versioned extractor.
- **Material identity:** same released series/event or declared score feature/model ID. **Temporal alignment:** release/surprise as-of cutoff; aligned named series as required.
- **Cardinality:** UNKNOWN unless row-specific correction is recorded in CSV; no implicit M00-to-Dxxx ID equality.
- **Observed entry points:** `_stage1.py _eval_k04/_eval_k07; api.py _materialise`; this is a source inventory, not proof of correctness.

## Global edge-carrier obligations

1. For every `Rxxx` edge, source identity is the opaque M00 `observation_occurrence_id`, with exact field-path `RawSignalProjectionMapping`, native units and `UnitConventionVersion`; same `Rxxx` tag alone does **not** establish a value or a relationship (§9).
2. For every `Dxxx` edge, the predecessor's `derived_occurrence_id` is a *different namespace*. The parent preserves direct predecessor occurrence references and ultimate raw lineage. To join a derived *per-raw-observation fact* back to trade data, follow reconstructed predecessor M00 lineage and compatible subject/contract/time/version; never equate the two namespaces (§§8.1,12–13).
3. For every row, `typed_contexts` is a conjunction and the parameter profile/version, selection policy/version, calculation-definition version, mapping and unit versions are part of compatibility (§§6,8.1,13). They are repeated per edge in the classified inventory and row census.
4. Direct Stage 2 predecessors remain normative entries, not executable Stage 1 edges. The 25 direct and five transitive Stage 2 rows are distinguished in each census record and in `F1_COUNTS.json`.
5. The current source is *not* semantically established by assignment to a class. F1c records positive, negative and independently discriminating public-seam obligations and explicitly unmapped/unproved paths.

## Known separate witnesses (not conflated)

- **Confirmed rejected output:** `D015→D016` and `D015→D120` are RC08. The reviewer independently observed D015=+1 while D016=0 and D120=(0,0) instead of (2,1200); see `handoff/m01_completion/review/M01_STAGE1_REVIEW_RESULT_514cf90e4c49.json`. This is a cross-namespace lineage/correlation failure, **not** evidence that all RC08 edges fail.
- **Previously repaired scope:** `D087→D109` / `D091→D109`, `D087→D170` are RC10. Existing `tests/product/derived_signal/test_m01_stage1_predecessor_scope.py` exercises selected cases, but this F1 evidence does not declare whole-class acceptance.
- **Unassessed grouped paths:** `D120/D091→D121` and `D120/D085→D122` are RC11. They were expressly unassessed by the reviewer after the D120 failure; source code's per-ID lookups cannot be taken as independent public proof.

