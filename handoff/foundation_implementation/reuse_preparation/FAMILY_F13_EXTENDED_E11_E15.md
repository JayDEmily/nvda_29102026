# F13 — Volatility index term relationships: documentary E1.1–E1.5 assessment

**Scope:** 4 individual IDs: D057, D058, D059, D060. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** Instantaneous cross-index pairs: source series/cadence and synchronized values cannot be inferred from Cboe daily files. Two-component result must remain typed.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D057 — VIX1D-to-VIX9D term slope
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D057` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R238;R239`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `index points / ratio`.
- **Independent controlled inputs:** R238 VIX1D=15; R239 VIX9D=20.
- **Expected result or documented hold:** {point_difference=-5 index points, ratio=3/4}. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Contemporaneous VIX1D/VIX9D eligible observations; preserve both native index definitions and max-skew selection. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** VIX9D missing/zero; replace VIX1D with VIX itself; after-cutoff one-side revision.
- **M01 reuse:** `REUSE_K02_PAIR_WITH_SEPARATE_TYPED_FIELDS`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1445,1446.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py`; `tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py`; `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d149_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Cboe cadence/methodology/variant and M00 synchronization. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D058 — VIX9D-to-VIX term slope
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D058` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R236;R239`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `index points / ratio`.
- **Independent controlled inputs:** R239 VIX9D=20; R236 VIX=25.
- **Expected result or documented hold:** {point_difference=-5 index points, ratio=4/5}. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One admissible VIX9D and VIX observation for same knowledge instant within approved skew. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Missing/zero VIX denominator; mix VIX3M instead; stale side of pair.
- **M01 reuse:** `REUSE_K02_PAIR_WITH_SEPARATE_TYPED_FIELDS`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1445,1446.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py`; `tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py`; `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d149_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Cboe VIX9D/VIX publication/synchronization. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D059 — VIX-to-VIX3M term slope
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D059` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R236;R240`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `index points / ratio`.
- **Independent controlled inputs:** R236 VIX=25; R240 VIX3M=30.
- **Expected result or documented hold:** {point_difference=-5 index points, ratio=5/6}. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** An aligned VIX/VIX3M pair under explicit Cboe publication profile. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** R240=0; substitute VVIX; after-cutoff revision of only the second input.
- **M01 reuse:** `REUSE_K02_PAIR_WITH_SEPARATE_TYPED_FIELDS`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1445,1446.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py`; `tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py`; `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d149_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Cboe VIX/VIX3M comparable observation times. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D060 — VVIX/VIX ratio
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D060` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R236;R237`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `ratio`.
- **Independent controlled inputs:** R237 VVIX=100; R236 VIX=25.
- **Expected result or documented hold:** ratio=4, not 4%. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Matched VVIX/VIX levels from eligible source/time state. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** R236=0; IV fraction substituted for VIX index points; incompatible snapshots.
- **M01 reuse:** `REUSE_EXACT_SCALAR_RATIO`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1451.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py`; `tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py`; `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d149_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Cboe native scale, publish cadence and freshness. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** R238 VIX1D=15; R239 VIX9D=20 ⇒ {point_difference=-5 index points, ratio=3/4}. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D060 first, then R236=0; IV fraction substituted for VIX index points; incompatible snapshots. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** Instantaneous cross-index pairs: source series/cadence and synchronized values cannot be inferred from Cboe daily files. Two-component result must remain typed.
- **Status:** all 4 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Exactness / result-shape qualification

**Result-carrier hold:** D059 controlled ratio `5/6` has an infinite decimal expansion. This packet proves the rational mathematical answer, not an authorised Decimal rounding policy or a completed M02 structured exact-ratio facet. D057–D059 require both named result components.
