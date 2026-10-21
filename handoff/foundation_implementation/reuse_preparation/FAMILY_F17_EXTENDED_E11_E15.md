# F17 — Relative sector strength: documentary E1.1–E1.5 assessment

**Scope:** 2 individual IDs: D076, D077. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** Predecessor-derived returns must have identical return conventions/windows. Optional single semiconductor proxy requires an *explicit* versioned mode.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D076 — Technology relative strength versus broad market
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D076` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D072;D071`; catalogue window `NONE_DECLARED`; catalogue result units `return spread`.
- **Independent controlled inputs:** D072 QQQ log return=1/20; D071 broad-market log return=1/50.
- **Expected result or documented hold:** 3/100 log-return units. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One current compatible D072 and D071 pair with matching comparison horizon, timestamp/cutoff and subject basket. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Mix 1-day QQQ and intraday broad market, incompatible versions or missing predecessor.
- **M01 reuse:** `REUSE_K02_PREDECESSOR_DIFFERENCE`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1454,2606.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc13_relative_sector_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d084_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Proxy selection and synchronized return horizons. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D077 — Semiconductor relative strength versus technology
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D077` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D073;D074;D072`; catalogue window `NONE_DECLARED`; catalogue result units `return spread`.
- **Independent controlled inputs:** D073 SMH return=1/10; D074 SOXX return=-1/50; D072 QQQ return=3/100.
- **Expected result or documented hold:** ((1/10-1/50)/2)-3/100 = 1/100. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Three horizon-aligned predecessor occurrences; explicit two-proxy mode. Optional named single-proxy profile is a different controlled fixture. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Absent SOXX with no single-proxy declaration; silently select one based on availability; mixed return definitions.
- **M01 reuse:** `REUSE_K02_EXPLICIT_BASKET_OR_NAMED_SINGLE_PROXY`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1456,2606.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc13_relative_sector_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_regression_history_public.py`; `tests/product/derived_signal/test_m01_f4_reconstruction_d084_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Accepted single-proxy policy/profile and aligned venue sessions. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** D072 QQQ log return=1/20; D071 broad-market log return=1/50 ⇒ 3/100 log-return units. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D077 first, then Absent SOXX with no single-proxy declaration; silently select one based on availability; mixed return definitions. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** Predecessor-derived returns must have identical return conventions/windows. Optional single semiconductor proxy requires an *explicit* versioned mode.
- **Status:** all 2 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.
