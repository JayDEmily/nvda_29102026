# F19 — Market/sector dispersion: documentary E1.1–E1.5 assessment

**Scope:** 1 individual IDs: D083. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** K04 D083 is contemporaneous P_CROSS_SECTION, not the strictly-prior P_BASELINE. A configured missing member must not silently reduce the basket.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D083 — Cross-sectional market/sector dispersion proxy
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K04_STANDARDISE_RANK`; catalogue `D083` row; parameter profile `P_CROSS_SECTION`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R037;R042`, predecessor `NONE_DECLARED`; catalogue window `Intraday/session`; catalogue result units `return dispersion`.
- **Independent controlled inputs:** three contemporaneous exact basket returns (-1,0,+1) in common declared return units.
- **Expected result or documented hold:** sample_sd=1 (N-1 denominator). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Three complete current admissible member returns; exact P_CROSS_SECTION basket/membership and same return horizon. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Two members but third silently omitted; treat sample as population sd sqrt(2/3); cross-market mismatched closes.
- **M01 reuse:** `REUSE_K04_CROSS_SECTION_NOT_HISTORICAL_BASELINE`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2337.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc13_cross_section_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d084_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** P_CROSS_SECTION constituent/weight policy and source matching. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** three contemporaneous exact basket returns (-1,0,+1) in common declared return units ⇒ sample_sd=1 (N-1 denominator). A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D083 first, then Two members but third silently omitted; treat sample as population sd sqrt(2/3); cross-market mismatched closes. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** K04 D083 is contemporaneous P_CROSS_SECTION, not the strictly-prior P_BASELINE. A configured missing member must not silently reduce the basket.
- **Status:** all 1 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.
