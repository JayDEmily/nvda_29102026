# F26 — IV vs realised volatility: documentary E1.1–E1.5 assessment

**Scope:** 2 individual IDs: D107, D108. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** IV versus realised comparisons are only defined after D096 and complete D035/D036 history share canonical decimal annualised-vol conventions.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D107 — IV minus 5-day realised volatility
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D107` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D096;D035`; catalogue window `NONE_DECLARED`; catalogue result units `vol points`.
- **Independent controlled inputs:** same comparable annualised decimal IV D096=0.30; 5-day realised D035=0.20.
- **Expected result or documented hold:** 100*(.30-.20)=+10 volatility points. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One aligned D096 expiry/delta selection and D035 complete five-day history; annualisation, cutoff and units match. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Subtract percentage points from decimal fractions; stale ATM versus later realised result; select wrong expiry.
- **M01 reuse:** `REUSE_K02_DIFFERENCE_AFTER_CANONICAL_UNIT_CHECK`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1587,1590.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_cross_stage_k02_stage1_kernel.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** D096 unimplemented/modeled source; realised trading calendar and annualisation. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D108 — IV minus 10-day realised volatility
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D108` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D096;D036`; catalogue window `NONE_DECLARED`; catalogue result units `vol points`.
- **Independent controlled inputs:** D096 IV=0.25; complete ten-day realised D036=0.30.
- **Expected result or documented hold:** 100*(.25-.30)=-5 volatility points. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One aligned D096 and D036 complete 10-day annualised-volatility history; matched time/basis and immutable definitions. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Reuse D035 five-day value; missing daily closes; mix provider IV scale.
- **M01 reuse:** `REUSE_K02_DIFFERENCE_AFTER_CANONICAL_UNIT_CHECK`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1587.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_cross_stage_k02_stage1_kernel.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** D096 exact source coverage and D036 calendar/profile. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** same comparable annualised decimal IV D096=0.30; 5-day realised D035=0.20 ⇒ 100*(.30-.20)=+10 volatility points. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D108 first, then Reuse D035 five-day value; missing daily closes; mix provider IV scale. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** IV versus realised comparisons are only defined after D096 and complete D035/D036 history share canonical decimal annualised-vol conventions.
- **Status:** all 2 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Exactness / result-shape qualification

**Result-shape hold:** M01 cross-stage tests (`test_m01_f4_cross_stage_k02_stage1_kernel.py:52–60`) inject a Decimal value labelled D096. Accepted K09 specifies per-expiry/side selection. This is only an arithmetic witness, not proof that public D096 will expose a scalar or that a selected expiry is unambiguous.
