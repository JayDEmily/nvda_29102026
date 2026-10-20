# F18 — Betas/residual/correlation: documentary E1.1–E1.5 assessment

**Scope:** 5 individual IDs: D078, D079, D080, D081, D082. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** D078–D081 are one coherent factor model with intercept and immutable fit identity; one result coefficient is not enough evidence of fit identity. D082 is an aligned return-correlation matrix, not price correlation.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D078 — NVDA residual/idiosyncratic return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K06_REGRESSION_DEPENDENCE`; catalogue `D078` row; parameter profile `P_REGRESSION`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D075;D071;D076;D077;D079;D080;D081`; catalogue window `NONE_DECLARED`; catalogue result units `return`.
- **Independent controlled inputs:** Previously fitted alpha=1; betas=(1,2,3); current factor vector=(1,1,1); current D075=10.
- **Expected result or documented hold:** residual=10-(1+1+2+3)=3. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** At least five full time-aligned model-training vectors, then current vector; D079/D080/D081 must be from exact same immutable fit ID; training excludes current. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Combine coefficients from separate fits; fit on current dependent return; rank-deficient factors; post-cutoff row.
- **M01 reuse:** `REUSE_EXISTING_COMMON_OLS_WITH_MODEL_IDENTITY_GUARDS`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2605,2615,2618,2625.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** P_REGRESSION sample/conditioning profile and common fit provenance. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D079 — Conditional NVDA market beta
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K06_REGRESSION_DEPENDENCE`; catalogue `D079` row; parameter profile `P_REGRESSION`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D075;D071;D076;D077`; catalogue window `Regime and horizon specific`; catalogue result units `beta`.
- **Independent controlled inputs:** Historical factors (0,0,0),(1,0,0),(0,1,0),(0,0,1),(1,1,1); D075 y=(1,2,3,4,7).
- **Expected result or documented hold:** OLS with intercept: beta_market=1, alpha=1, beta_tech=2, beta_semi=3. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Five aligned return rows full rank; same D071,D076,D077 basis and D075 dependent, immutable P_REGRESSION window. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Singular factor columns; misaligned y row; regression without intercept; wrong dependent series.
- **M01 reuse:** `REUSE_ALIGNED_OLS_NOT_THREE_SEPARATE_FITS`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2605,2628,2629,2640.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** P_REGRESSION conditioning/state/windowning; factor timestamp availability. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D080 — Conditional NVDA technology beta
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K06_REGRESSION_DEPENDENCE`; catalogue `D080` row; parameter profile `P_REGRESSION`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D075;D071;D076;D077`; catalogue window `Regime and horizon specific`; catalogue result units `beta`.
- **Independent controlled inputs:** Same full-rank five-row training set as D079.
- **Expected result or documented hold:** OLS beta_tech=2, shared fit (alpha=1,betas=1/2/3). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Five complete aligned predecessor time rows; preserve fit identity and all four source series. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Fit only D075 and D076, dropping correlated-factor regressors; interpolate missing tech return.
- **M01 reuse:** `REUSE_ALIGNED_OLS_NOT_THREE_SEPARATE_FITS`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2605,2629,2640.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** P_REGRESSION sample and state selection. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D081 — Conditional NVDA semiconductor beta
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K06_REGRESSION_DEPENDENCE`; catalogue `D081` row; parameter profile `P_REGRESSION`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D075;D071;D076;D077`; catalogue window `Regime and horizon specific`; catalogue result units `beta`.
- **Independent controlled inputs:** Same full-rank five-row training set as D079.
- **Expected result or documented hold:** OLS beta_semi=3, shared fit (alpha=1,betas=1/2/3). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Five complete aligned predecessor time rows; one immutable shared model fit identity. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Use separate semiconductor-only beta fit or single observation; singular 4-column design.
- **M01 reuse:** `REUSE_ALIGNED_OLS_NOT_THREE_SEPARATE_FITS`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2605,2628,2629,2640.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** P_REGRESSION sample/fit version. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D082 — Rolling NVDA-market/sector correlations
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K06_REGRESSION_DEPENDENCE`; catalogue `D082` row; parameter profile `P_REGRESSION`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R151`, predecessor `NONE_DECLARED`; catalogue window `5d/20d/intraday`; catalogue result units `correlation`.
- **Independent controlled inputs:** Two subject aligned return arrays A=(1,2,3), B=(3,2,1) with nonzero variance.
- **Expected result or documented hold:** Pearson correlation matrix [[1,-1],[-1,1]]. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Three aligned *returns* require at least four strictly ordered positive close observations per subject (R151); exact same timestamps for every member. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Use price levels as returns; intersection silently skips missing time; duplicate native subject/time; constant return series.
- **M01 reuse:** `REUSE_RETURN_CORRELATION_MATRIX_TYPED_OUTPUT`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2641.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc05_correlations_public.py`; `tests/product/derived_signal/test_m01_f4_cross_stage_remaining_own_kernel.py`; `tests/product/derived_signal/test_m01_stage1_leaf3_catalogue_kernels.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** R151 close mapping, common bar/calendar and P_REGRESSION window. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** Previously fitted alpha=1; betas=(1,2,3); current factor vector=(1,1,1); current D075=10 ⇒ residual=10-(1+1+2+3)=3. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D082 first, then Use price levels as returns; intersection silently skips missing time; duplicate native subject/time; constant return series. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** D078–D081 are one coherent factor model with intercept and immutable fit identity; one result coefficient is not enough evidence of fit identity. D082 is an aligned return-correlation matrix, not price correlation.
- **Status:** all 5 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Source-specific reuse challenge

**Observed M01 fit-identity limitation (potential):** `_stage1.py:2618–2631` computes a training fit and compares each supplied D079/D080/D081 numeric coefficient against it, but the direct kernel check shown there does not compare an immutable shared `model_fit_id`. Existing `test_m01_f4_reconstruction_regression_history_public.py:300–323` proves predecessor IDs enter the public occurrence; it does not by itself prove a shared fit identity across arbitrary equal-valued fits. Future M02 proof needs an independent same-coefficients/different-fit identity discriminator, or explicit evidence that existing owner contracts enforce this condition. This is not a proved public exploit.

## Exactness / result-shape qualification

**Model/representation hold:** an exact rational design-matrix training example does not establish rounding, singular tolerance, coefficient representation, immutable fit identity or matrix shape for general market returns. The future proof must distinguish all these.
