# F28 — Risk-neutral density and tails: documentary E1.1–E1.5 assessment

**Scope:** 3 individual IDs: D111, D112, D113. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** D111 requires an actual decreasing/convex call-price spline and D102 quality gate; D112/113 conditional trapezoids are not substitutes for a valid D111 model.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D111 — Risk-neutral terminal density
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K09_SURFACE_DENSITY`; catalogue `D111` row; parameter profile `P_SURFACE`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R014;R015;R034;R035`, predecessor `D086;D087;D102`; catalogue window `NONE_DECLARED`; catalogue result units `probability density`.
- **Independent controlled inputs:** Versioned admissible call-price/strike spline and arbitrage-safe D102 prerequisite not supplied; NO SOURCE-FIT FIGURES.
- **Expected result or documented hold:** NO_NUMERICAL_D111_ORACLE_AUTHORISED; must refuse absent D102 acceptance or valid decreasing convex call-price fit. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Across-strike same-expiry call mids (D087), strike/source and exact D102 surface-quality relation; decreasing-convex spline, second derivative and mass normalisation on versioned grid. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Use IV curve as call-price curve; fit concave/non-monotone calls; negative density, fit without accepted revaluation/grid.
- **M01 reuse:** `NO_DIRECT_M01_D111_KERNEL; MODEL_BLOCK_HONEST`. Source locator: No direct ID branch found in `_stage1.py`; indirect/generic handling unproved.
- **Existing public test navigation:** No exact literal reference in inspected `tests/product/derived_signal/*.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** No M01 D111 kernel; spline/grid/exercise/discount/model/convention and D102 quality tolerance not supplied. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D112 — Risk-neutral downside-tail probability
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K09_SURFACE_DENSITY`; catalogue `D112` row; parameter profile `P_SURFACE`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D111`; catalogue window `Expiry-specific`; catalogue result units `probability`.
- **Independent controlled inputs:** Assuming already ADMITTED D111 triangular density on S={90,100,110} with f={0,.1,0}, selected downside threshold=100.
- **Expected result or documented hold:** trapezoid cumulative mass below 100 = 1/2 (illustrative conditional D111 only). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One complete normalised immutable D111 density grid, threshold and exact grid version; includes left endpoint/threshold under specified integration convention. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Assume density from raw IV points; missing grid segment; threshold outside coverage silently clipped without policy.
- **M01 reuse:** `REUSE_K09_TRAPEZOID_CONDITIONAL_ON_ACCEPTED_D111`. Source locator: No direct ID branch found in `_stage1.py`; indirect/generic handling unproved.
- **Existing public test navigation:** No exact literal reference in inspected `tests/product/derived_signal/*.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** D111 production/fit convention and integration edge/threshold policy. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D113 — Risk-neutral upside-tail probability
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K09_SURFACE_DENSITY`; catalogue `D113` row; parameter profile `P_SURFACE`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D111`; catalogue window `Expiry-specific`; catalogue result units `probability`.
- **Independent controlled inputs:** Assuming same ALREADY ADMITTED D111 triangular density S={90,100,110}, f={0,.1,0}, upside threshold=100.
- **Expected result or documented hold:** trapezoid mass above 100 = 1/2 (illustrative conditional D111 only). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One complete normalised immutable D111 density grid, upside threshold and same grid/integration policy. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Swap downside tail, infer probability from unvalidated raw premiums, silently extrapolate beyond strike grid.
- **M01 reuse:** `REUSE_K09_TRAPEZOID_CONDITIONAL_ON_ACCEPTED_D111`. Source locator: No direct ID branch found in `_stage1.py`; indirect/generic handling unproved.
- **Existing public test navigation:** No exact literal reference in inspected `tests/product/derived_signal/*.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** D111 production/fit, tail-boundary and quantisation policy. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** Versioned admissible call-price/strike spline and arbitrage-safe D102 prerequisite not supplied; NO SOURCE-FIT FIGURES ⇒ NO_NUMERICAL_D111_ORACLE_AUTHORISED; must refuse absent D102 acceptance or valid decreasing convex call-price fit. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D113 first, then Swap downside tail, infer probability from unvalidated raw premiums, silently extrapolate beyond strike grid. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** D111 requires an actual decreasing/convex call-price spline and D102 quality gate; D112/113 conditional trapezoids are not substitutes for a valid D111 model.
- **Status:** all 3 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Source-specific reuse challenge

**Model barrier preserved:** D102 and D111–D113 are mathematical obligations but have no direct `_stage1.py` ID branch and no literal specialised public test in the inspected M01 product-test directory. The absence finding is bounded to these surfaces only. A D112/D113 conditional triangle does not authorise choosing the D111 spline, pricing/exercise convention, regularisation, grid or stopping rule.
