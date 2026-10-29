# F22 — Option quote liquidity and IV bid/ask: documentary E1.1–E1.5 assessment

**Scope:** 4 individual IDs: D087, D088, D092, D093. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** Option quotes must be keyed to exact option contract, not confused with underlying equity quote names R034/R035. The IV bid/ask fields use canonical decimal vol fractions.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D087 — Option midpoint
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D087` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R034;R035`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `option premium`.
- **Independent controlled inputs:** same-option-contract R034 option bid2, R035 option ask4.
- **Expected result or documented hold:** option midpoint=3 currency/option-price units. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One compatible option bid/ask native snapshot for exact contract, right, expiry, strike, currency/contract multiplier and cutoff. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Use underlying stock quote with same R IDs; crossed or stale pair without approved eligibility; missing bid.
- **M01 reuse:** `REUSE_K02_MIDPOINT_WITH_CONTRACT_BOUNDARY`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1395,1467,1594,1606,1677,1881,2091,2093.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_option_scalar_public.py`; `tests/product/derived_signal/test_m01_f4_rc16_fill_cost_public.py`; `tests/product/derived_signal/test_m01_f4_d110_spot_expected_move_public.py`; `tests/product/derived_signal/test_m01_f4_option_depth_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR price quote variant, entitlement, market state and unit interpretation. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D088 — Option relative spread
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D088` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R034;R035`, predecessor `D087`; catalogue window `NONE_DECLARED`; catalogue result units `percent`.
- **Independent controlled inputs:** R034 bid2,R035 ask4 and same-contract D087 midpoint3.
- **Expected result or documented hold:** relative spread=100*(4-2)/3 = 200/3 %. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Complete D087 occurrence and native bid/ask matching its selection identity/contract; no asynchronous substitute. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** D087 zero; mismatched D087 from another contract; wrong percent/bps multiplier.
- **M01 reuse:** `REUSE_K02_PERCENT_SPREAD_AND_PREDECESSOR_LINEAGE`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1466.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_option_scalar_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d132_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR synchronized bid/ask + D087 identity/version. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D092 — Mid-quote implied volatility estimate
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D092` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R084;R093`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `volatility`.
- **Independent controlled inputs:** option bid IV R084=0.20, ask IV R093=0.30.
- **Expected result or documented hold:** decimal annualised IV midpoint=1/4 (25 vol). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One exact option contract with two eligible IV quote-side observations and same model/time convention. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Mix contract expiries; treat 20 as fraction 0.20; one missing IV side silently copied.
- **M01 reuse:** `REUSE_K02_IV_MIDPOINT_CANONICAL_DECIMAL`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1480.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc14_option_iv_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR bid/ask model IV numeric scale/model versions. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D093 — Implied-volatility bid/ask width
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D093` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R084;R093`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `vol points`.
- **Independent controlled inputs:** R084 bid IV0.20,R093 ask IV0.30.
- **Expected result or documented hold:** volatility-point difference=100*(0.30-0.20)=10. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Same eligible matched option and model/unit state for IV bid and ask. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Mix call and put or expiration; compute 0.10 as 0.10 vol points; crossed scale.
- **M01 reuse:** `REUSE_K02_IV_POINT_DIFFERENCE`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1482.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc14_option_iv_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR source field semantics/IV-side pairing. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** same-option-contract R034 option bid2, R035 option ask4 ⇒ option midpoint=3 currency/option-price units. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D093 first, then Mix call and put or expiration; compute 0.10 as 0.10 vol points; crossed scale. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** Option quotes must be keyed to exact option contract, not confused with underlying equity quote names R034/R035. The IV bid/ask fields use canonical decimal vol fractions.
- **Status:** all 4 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Exactness / result-shape qualification

**Result-carrier hold:** D088 expected `200/3%` is mathematically non-terminating. Reusing the M01 Decimal division unchanged would choose a finite representation; new M02 typed exact ratio and/or an explicitly authorised representation policy is required.
