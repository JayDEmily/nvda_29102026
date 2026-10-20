# F33 — SMART/direct snapshot, slopes and divergence: individual M01→M02 E1.1–E1.5 documentary audit

**Status:** AUTHOR-ASSESSED_WITH_PRECISE_HOLDS. No native source certification, independent semantic admission or active M02 implementation acceptance.

**Pinned source:** `c16468d1fb64f03a3e77fc8389d3e1797c2478bf` initial exact preparation HEAD; active worker later state UNKNOWN. **IDs:** D134, D135, D136, D137, D138, D143, D144.

**Common accepted mechanism / dependency:** D138 accepts only corrected five-field native mutation data; D144 requires same-book and timestamp/skew control, not generic positional pairing. Controlled values below are constructed from accepted formulae; they are not assertions about live provider data.

## Individual specification, legacy navigation and adversarial refusal

### D134 — SMART cumulative bid depth

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D134`; effective raw `R185;R187;R188;R190`, predecessors `NONE_DECLARED`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Reconstructed SMART bid levels positions1/2 sizes5 and3, depth_levels=2 => cumulative bid depth 8.
- **History, identity and fixture prerequisites:** Ordered state built from exact position, operation, side, price, size; all relevant eligible mutations and warm-up; select top two standing bid positions in one subject/source. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Summing inserts instead of final standing state, missing native op, shift after insertion without reindex, error317 reset => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1665`. `REEXPRESS_POSITIONAL_BOOK_PROOF_WITH_NATIVE_DEPENDENCIES.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_depth_snapshot_authority.py`; `tests/product/derived_signal/test_m01_f4_positional_book_class.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Native SMART book row position and reset/source completeness unadmitted. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D135 — SMART cumulative ask depth

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D135`; effective raw `R185;R187;R188;R190`, predecessors `NONE_DECLARED`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Reconstructed SMART ask levels positions1/2 sizes2 and4, depth_levels=2 => cumulative ask depth 6.
- **History, identity and fixture prerequisites:** Same selected book/window as D134, with ask-side native state and deterministic update/delete/reindex rules. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Bid/ask side conflation, depth_levels<=0, missing history or state reset => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1665`. `REEXPRESS_POSITIONAL_BOOK_PROOF_WITH_NATIVE_DEPENDENCIES.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_depth_snapshot_authority.py`; `tests/product/derived_signal/test_m01_f4_positional_book_class.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Native SMART ask side/position event projection and completeness unadmitted. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D136 — SMART depth imbalance

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D136`; effective raw `NONE_DECLARED`, predecessors `D134;D135`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** D134=8 and D135=6 same versioned depth profile => (8-6)/(8+6)=1/7 exact rational.
- **History, identity and fixture prerequisites:** D134 and D135 predecessor occurrences must refer to same book/subject/window/levels/source-selection state; nonzero depth sum; preserve both refs. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Mixed depth-level configurations, absent side, denominator0, stale unrelated predecessor => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1692`. `REUSE_K02_EXACT_RATIO_AS_SPEC_WITH_PREDECESSOR_ALIGNMENT.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_depth_snapshot_authority.py`; `tests/product/derived_signal/test_m01_f4_positional_book_class.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** M02 exact-ratio carrier and typed cross-predecessor book context/proof to be admitted. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D137 — Order-book microprice

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D137`; effective raw `R033;R034;R035;R036`, predecessors `NONE_DECLARED`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Best bid99, best ask101, bid size3, ask size1 => (101*3+99*1)/(3+1)=201/2=100.5.
- **History, identity and fixture prerequisites:** Matched top-of-book R034/R035 prices and R033/R036 sizes from one source/current state, subject, quote-time and unit versions; nonzero total size. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Mixed quote timestamps, zero denominator, crossed book or omitted price/size pairing => refuse when profile forbids.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1696`. `REUSE_K02_CROSS_WEIGHTED_MICROPRICE_AS_SPEC.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_microprice_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Native coherent quote state/crossed-book policy and Decimal/exact-ratio representation hold. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D138 — Order-book slope

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K06_REGRESSION_DEPENDENCE; Annex B `D138`; effective raw `R185;R187;R188;R189;R190`, predecessors `D011`. Accepted overlay: `handoff/m01_completion/authority/D138_D145_L2_OWNER_APPROVED_DEPENDENCY_AMENDMENT_20261016.md`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Mid D011=100; BID cumulative depth at absolute distances (1,2,3)=(2,5,9) => OLS slope 7/2; ASK cumulative (1,3,6) => slope 5/2; result {bid_slope=3.5,ask_slope=2.5}.
- **History, identity and fixture prerequisites:** Accepted five R185/R187/R188/R189/R190 fields reconstruct complete positional SMART book before per-side OLS with intercept; D011 matched midpoint; >=2 distinct distances each side. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Unordered row triple, wrong positional shift, equal x distances, missing R185/R187, reset before warm-up => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:2685`. `REEXPRESS_REQUIRED: legacy M01 slope reads only R188/R189/R190 despite accepted five-R dependency correction.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_book_slope_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Provider row-position/operation semantics, ordering and complete snapshot/clear-reset support not admitted. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D143 — Direct-exchange depth concentration

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D143`; effective raw `R192;R193;R194;R195;R196;R197`, predecessors `NONE_DECLARED`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Direct standing depth by venue A=3, venue B=1 => shares3/4,1/4; direct depth HHI=5/8.
- **History, identity and fixture prerequisites:** Six matching R192-R197 fields per native direct event; reconstruct direct positions by venue, side and native op; preserve venue/market-maker identity; use absolute standing size. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Missing venue/market maker, duplicate partial event, summing mutated rows rather than standing venue size, total=0 => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1700`. `REEXPRESS_EXACT_DIRECT_BOOK_HHI_AS_SPEC.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_direct_book_public.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Native direct-depth venue attribution, market-maker identity, source side and completeness not certified. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D144 — SMART versus direct depth divergence

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D144`; effective raw `R185;R187;R188;R189;R190;R192;R193;R194;R195;R196;R197`, predecessors `NONE_DECLARED`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Matched admitted SMART bid row (price100,size8), direct bid row (price99.5,size5) => structured {price_difference=+0.5,depth_difference=+3} for that matched row, conditional on explicit matched-level/skew policy.
- **History, identity and fixture prerequisites:** Reconstruct complete SMART and direct books separately with all native position/op/side/price/size (+ direct venue) fields; match versioned same subject, side, price/level, max skew. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Matching solely same numeric position despite incompatible venues or timestamps, dropping unmatched required row, mixing update streams => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1719`. `REEXPRESS_MATCHING: legacy M01 positional pairing alone does not prove accepted same-price/level/skew selection.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_direct_book_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Book matching tolerances/source identity and native venue/time coverage hold. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

## E1.5 — bounded independent documentary challenge

- **Numerical:** Reconstructed SMART bid levels positions1/2 sizes5 and3, depth_levels=2 => cumulative bid depth 8. This witness distinguishes the accepted operation, units and output shape from a plausible wrong implementation. Independently derived here; not generated by the M01 evaluator.
- **Selection/fault:** Run insert-shift then deletion and error317 reset; D134/135/138 cannot use old standing quantities until reinitialised. Independently challenge D144 same-level but beyond-skew match. First construct the full positive history and independently identify the exact mutation or omitted observation; a cursor exhausted before the condition is reached is not evidence for the intended refusal.
- **Authority boundary:** Family may share replay/identity/provenance engines only with separate acceptance; each D identity above keeps its own equation, prerequisite and refusal. Unresolved provider/model/source mappings remain precisely held; no fabricated native range, output or live capability.
- **Disposition:** D134=AUDITED_WITH_PRECISE_HOLDS, D135=AUDITED_WITH_PRECISE_HOLDS, D136=AUDITED_WITH_PRECISE_HOLDS, D137=AUDITED_WITH_PRECISE_HOLDS, D138=AUDITED_WITH_PRECISE_HOLDS, D143=AUDITED_WITH_PRECISE_HOLDS, D144=AUDITED_WITH_PRECISE_HOLDS. AUTHOR documentary assessment only.
