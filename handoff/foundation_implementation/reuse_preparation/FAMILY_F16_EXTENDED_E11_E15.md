# F16 — US/sector/NVDA underlying returns: documentary E1.1–E1.5 assessment

**Scope:** 5 individual IDs: D071, D072, D073, D074, D075. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** Shared generic R037/R042 names do not make SPY/QQQ/SMH/SOXX/NVDA interchangeable. Preserve subject-specific prior official close and cutoff.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D071 — SPY/S&P proxy intraday return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D071` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R037;R042`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `return`.
- **Independent controlled inputs:** SPY/S&P proxy R042 prior close100; R037 current110.
- **Expected result or documented hold:** ln(11/10). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One exact selected broad-market proxy, same subject/variant prior official close and current session state; two eligible observations. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Mix SPY and index symbol or denominator zero; compare foreign timezones.
- **M01 reuse:** `REUSE_K03_RETURN_NOT_GENERIC_CROSS_SUBJECT`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1455,2181,2606.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py`; `tests/product/derived_signal/test_m01_f4_rc13_relative_sector_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d084_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR proxy choice, entitlement, market-state and prior-close authority. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D072 — QQQ/Nasdaq-100 proxy intraday return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D072` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R037;R042`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `return`.
- **Independent controlled inputs:** QQQ/Nasdaq proxy prior close100; current90.
- **Expected result or documented hold:** ln(9/10). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Same QQQ or exact selected NDX proxy, aligned current session plus prior official close. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Mix ETF and index, split adjustment, future close.
- **M01 reuse:** `REUSE_K03_RETURN_NOT_GENERIC_CROSS_SUBJECT`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1455,1457,2181.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py`; `tests/product/derived_signal/test_m01_f4_rc13_relative_sector_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d084_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR QQQ/NDX native series and adjustment. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D073 — SMH semiconductor ETF intraday return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D073` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R037;R042`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `return`.
- **Independent controlled inputs:** SMH R042=50; R037=55.
- **Expected result or documented hold:** ln(11/10). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Two complete same-SMH subject snapshots, official prior close and eligible current last. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Substitute SOXX prior close; stale ETF price, prior close not official.
- **M01 reuse:** `REUSE_K03_RETURN_NOT_GENERIC_CROSS_SUBJECT`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1458,1463,2181.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py`; `tests/product/derived_signal/test_m01_f4_rc13_relative_sector_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d084_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR SMH quote/close fields and calendars. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D074 — SOXX semiconductor ETF intraday return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D074` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R037;R042`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `return`.
- **Independent controlled inputs:** SOXX prior close40; current40.
- **Expected result or documented hold:** ln(1)=0. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Two distinct eligible SOXX observations of equal prices under one calendar and source mapping. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Treat zero as missing; SMH/SOXX cross-subject mixed pair.
- **M01 reuse:** `REUSE_K03_RETURN_NOT_GENERIC_CROSS_SUBJECT`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1459,1463,2181.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py`; `tests/product/derived_signal/test_m01_f4_rc13_relative_sector_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d084_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR SOXX quote and official close. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D075 — NVDA intraday return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D075` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R037;R042`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `return`.
- **Independent controlled inputs:** NVDA prior close100; current125.
- **Expected result or documented hold:** ln(5/4). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** NVDA same canonical subject prior official close and current live/last observation with cutoff/market phase. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Mix premarket reference and RTH without selection; adjusted versus unadjusted close; nonpositive price.
- **M01 reuse:** `REUSE_K03_RETURN_NOT_GENERIC_CROSS_SUBJECT`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2181,2606.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc13_sector_returns_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR NVDA close/last adjustment state and source timing. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** SPY/S&P proxy R042 prior close100; R037 current110 ⇒ ln(11/10). A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D075 first, then Mix premarket reference and RTH without selection; adjusted versus unadjusted close; nonpositive price. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** Shared generic R037/R042 names do not make SPY/QQQ/SMH/SOXX/NVDA interchangeable. Preserve subject-specific prior official close and cutoff.
- **Status:** all 5 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Exactness / result-shape qualification

**Real-number precision hold:** logarithmic returns must not be assumed to have finite Decimal expansions; the accepted mathematical value and any M02 representation/rounding rule are distinct.
