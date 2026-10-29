# F15 — International market returns: documentary E1.1–E1.5 assessment

**Scope:** 4 individual IDs: D066, D067, D068, D069. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** Each international index requires its own exact daily/overnight calendar, close type and publication window; no market-calendar equivalence across countries.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D066 — Nikkei 225 return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D066` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R270`, predecessor `NONE_DECLARED`; catalogue window `1d`; catalogue result units `return`.
- **Independent controlled inputs:** Nikkei aligned reference close100 and comparison close110.
- **Expected result or documented hold:** ln(11/10). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** At least two strictly ordered R270 Nikkei closes at the row-selected day/overnight anchor; exact Japanese session/calendar boundary. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Cross-day holiday gap disguised as daily, wrong Nikkei series or nonpositive close, later-known close.
- **M01 reuse:** `REUSE_LOG_RETURN_HISTORY_ONLY`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2126,2144.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc03_history_public.py`; `tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py`; `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Nikkei source subscription, JP timezone and session close semantics. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D067 — Hong Kong index return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D067` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R271`, predecessor `NONE_DECLARED`; catalogue window `1d`; catalogue result units `return`.
- **Independent controlled inputs:** HK index aligned reference close200 and comparison close180.
- **Expected result or documented hold:** ln(9/10). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** At least two R271 same named Hong Kong index closes at the exact daily eligible anchor; configured exchange trading calendar. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Use mainland close/other HK index; forward fill holiday; denominator zero.
- **M01 reuse:** `REUSE_LOG_RETURN_HISTORY_ONLY`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2126,2145.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc03_history_public.py`; `tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py`; `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** HK index native series, market holidays/source availability. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D068 — China index return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D068` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R272`, predecessor `NONE_DECLARED`; catalogue window `1d`; catalogue result units `return`.
- **Independent controlled inputs:** China index aligned reference close50 and comparison close50.
- **Expected result or documented hold:** ln(1)=0. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Two distinct equal-valued R272 observations at genuine eligible daily anchors, with selected China instrument identity. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Treat zero return as absent; combine exchanges; use unsupported prior trading day.
- **M01 reuse:** `REUSE_LOG_RETURN_HISTORY_ONLY`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2126,2146.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc03_history_public.py`; `tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py`; `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** China series/index identity and admitted market calendar. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D069 — China technology index return
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D069` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R273`, predecessor `NONE_DECLARED`; catalogue window `1d`; catalogue result units `return`.
- **Independent controlled inputs:** Nasdaq China technology index reference80, comparison100.
- **Expected result or documented hold:** ln(5/4). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Two R273 closes at selected source-supported daily anchor with exact index identity/official close semantics. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Substitute QQQ proxy; arbitrary weekend bars; after-cutoff correction.
- **M01 reuse:** `REUSE_LOG_RETURN_HISTORY_ONLY`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2126,2147.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc03_history_public.py`; `tests/product/derived_signal/test_m01_f4_rc06_market_regime_scores_public.py`; `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Index vendor/source, native time and units. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** Nikkei aligned reference close100 and comparison close110 ⇒ ln(11/10). A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D069 first, then Substitute QQQ proxy; arbitrary weekend bars; after-cutoff correction. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** Each international index requires its own exact daily/overnight calendar, close type and publication window; no market-calendar equivalence across countries.
- **Status:** all 4 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Exactness / result-shape qualification

**Real-number precision hold:** logarithmic returns such as `ln(11/10)` are exact *symbolic* witnesses; M01 Decimal logarithm does not by itself authorise a unique M02 finite-precision representation. The output arithmetic and canonicalisation contract needs an independently specified treatment.
