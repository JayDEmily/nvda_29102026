# F29 — Exact option volume and official open-interest ratios/concentration: individual M01→M02 E1.1–E1.5 documentary audit

**Status:** AUTHOR-ASSESSED_WITH_PRECISE_HOLDS. No native source certification, independent semantic admission or active M02 implementation acceptance.

**Pinned source:** `c16468d1fb64f03a3e77fc8389d3e1797c2478bf` initial exact preparation HEAD; active worker later state UNKNOWN. **IDs:** D116, D118, D119, D123, D124.

**Common accepted mechanism / dependency:** The right-specific D116 and D123 exemptions do not relax both-right D119; D123 needs two different official periods while D116 needs only one latest eligible OI. Controlled values below are constructed from accepted formulae; they are not assertions about live provider data.

## Individual specification, legacy navigation and adversarial refusal

### D116 — Option volume/open-interest ratio

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D116`; effective raw `R041;R047;R048`, predecessors `NONE_DECLARED`. Accepted overlay: `handoff/m01_completion/authority/D116_CALCULATION_DEFINITION_AUTHORISED_CORRECTION_20261011.md`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Selected CALL contract R041 volume=30, same contract R047 OI=20 => exact ratio 3/2. Selected PUT R041=12 and R048=6 => 2. Opposite right absent is lawful.
- **History, identity and fixture prerequisites:** Exactly one chosen option right and matching selected contract; one current eligible non-negative cumulative volume and strictly positive same-contract OI with comparable unit/temporal identity; no D123 two-period requirement. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Zero volume => 0; OI=0/negative, opposite-right OI substitution, wrong contract, ambiguous current source, future value => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1641`. `REUSE_AS_SPEC_WITH_ACCEPTED_D116_RIGHT_FIX; legacy average-volume R075 witness invalid.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_d116_authorised_public.py`; `tests/product/derived_signal/test_m01_f4_rc14_option_volume_oi_public.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** IBKR volume/OI native mapping, right/expiry/contract selection, official OI reporting scale and timestamp not admitted. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D118 — Call/put volume ratio

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D118`; effective raw `R049;R050`, predecessors `NONE_DECLARED`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Within selected expiry/strike basket, aggregated call volume=12 contracts, put volume=4 => 3.
- **History, identity and fixture prerequisites:** Same immutable expiry/DTE, strike region, units, side, source version and eligible cutoff for both R049/R050 aggregate memberships; unique member inclusion. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Put=0; missing matched side, out-of-basket call, duplicate contract/event, stale/future chain => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1652`. `REUSE_K02_SUM_RATIO_AS_SPEC; must re-prove exact basket.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_rc14_option_chain_ratio_public.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Native R049/R050 aggregation scope and selected expiry/DTE/strike-region definition not source-certified. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D119 — Call/put open-interest ratio

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D119`; effective raw `R047;R048`, predecessors `NONE_DECLARED`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** For selected basket aggregate call OI=40, put OI=20 => 2.
- **History, identity and fixture prerequisites:** Matched expiry/DTE, strike region, official OI period/vintage and units across R047/R048 sets; both aggregate sides mandatory unlike D116/D123 right-specific selection. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Put OI zero, mixed official periods, duplicated contract, silent missing-right zero substitution => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1652`. `REUSE_K02_OI_RATIO_AS_SPEC; period/side alignment requires re-expression.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_rc14_option_chain_ratio_public.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Both-right official reporting period and revision fields for native provider unadmitted. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D123 — Open-interest change

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K02_ALGEBRA; Annex B `D123`; effective raw `R047;R048`, predecessors `NONE_DECLARED`. Accepted overlay: `handoff/m01_completion/authority/D123_CALCULATION_DEFINITION_AUTHORISED_CLARIFICATION_20261011.md`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Same exact CALL contract: preceding official period P1 eligible OI=100, latest distinct period P2=125 => +25; correction to P2=130 with higher official revision precedence => +30.
- **History, identity and fixture prerequisites:** Controlled M00 mappings supply official_reporting_period_id/order, official_revision_id/precedence, exact same contract/right/subject/source and two distinct eligible official period ordinals; choose highest unambiguous revision in each period. PUT uses R048 only. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Two ticks from same period are NOT two reporting periods; missing prior period, contradictory ordinal/preference, opposite right or receipt-arrival order substituted as period => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:148`. `REUSE_CORRECTED_OFFICIAL_PERIOD_SELECTOR_AS_SPEC; preserve controlled-only acceptance.`. Existing public navigation: `tests/product/derived_signal/test_m01_f4_d123_controlled_public.py`; `tests/product/derived_signal/test_m01_f4_d123_exact_contract_authority.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Provider-native period identity/revision ordering is not certified; controlled projection keys are not native IBKR guarantees. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D124 — Open-interest concentration by strike/expiry

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K08_RULE_BUCKET_POLICY; Annex B `D124`; effective raw `R047;R048`, predecessors `NONE_DECLARED`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Same strike-expiry OI groups A=30 and B=10 => shares (3/4,1/4); HHI=(3/4)^2+(1/4)^2=5/8.
- **History, identity and fixture prerequisites:** Each call/put R047/R048 contract unique with exact underlying/right/strike/expiry; configured grouping = strike_expiry; sum across rights per (strike,expiry), normalise by positive total; full OI set and lineage. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Total OI zero; duplicate contract; grouping-by-raw-ID instead of strike/expiry, missing right or silent partial basket => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:3245`. `REUSE_K08_EXPLICIT_STRIKE_EXPIRY_HHI_AS_SPEC.`. Existing public navigation: `tests/product/derived_signal/test_m01_f3_open_interest_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Native OI report period, membership and market coverage not certified. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

## E1.5 — bounded independent documentary challenge

- **Numerical:** Selected CALL contract R041 volume=30, same contract R047 OI=20 => exact ratio 3/2. Selected PUT R041=12 and R048=6 => 2. Opposite right absent is lawful. This witness distinguishes the accepted operation, units and output shape from a plausible wrong implementation. Independently derived here; not generated by the M01 evaluator.
- **Selection/fault:** D123 later revision must change +25 to +30 with the SAME official-period ordinal; changing R048 instead of call R047 must not affect selected call D123. First construct the full positive history and independently identify the exact mutation or omitted observation; a cursor exhausted before the condition is reached is not evidence for the intended refusal.
- **Authority boundary:** Family may share replay/identity/provenance engines only with separate acceptance; each D identity above keeps its own equation, prerequisite and refusal. Unresolved provider/model/source mappings remain precisely held; no fabricated native range, output or live capability.
- **Disposition:** D116=AUDITED_WITH_PRECISE_HOLDS, D118=AUDITED_WITH_PRECISE_HOLDS, D119=AUDITED_WITH_PRECISE_HOLDS, D123=AUDITED_WITH_PRECISE_HOLDS, D124=AUDITED_WITH_PRECISE_HOLDS. AUTHOR documentary assessment only.
