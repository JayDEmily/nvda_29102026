# F24 — IV term/smile/surface construction: documentary E1.1–E1.5 assessment

**Scope:** 7 individual IDs: D096, D097, D098, D099, D100, D101, D102. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** D096 interpolation, D097/098 term derivatives, D099–101 contract-matched native-delta skew, and D102 arbitrage-aware constrained fit are separate subcontracts. D102 requires actual OptionRevaluationConventionVersion.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D096 — ATM implied volatility by expiry
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K09_SURFACE_DENSITY`; catalogue `D096` row; parameter profile `P_SURFACE`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R111;R112`, predecessor `D085`; catalogue window `NONE_DECLARED`; catalogue result units `volatility`.
- **Independent controlled inputs:** one expiry+side |delta|=0.40 IV0.20 and |delta|=0.60 IV0.30; 50D bracket, no exact; second side absent with explicitly admitted single-side mode.
- **Expected result or documented hold:** linear interpolation IV=1/4; single-side only if mode admitted. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** At least two ordered distinct deltas bracketing 0.50 on same expiry/right for each candidate side; D085 expiry classification; option contract/native deltas bound individually. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Both deltas below0.50 => refuse extrapolation; missing side without single-side policy; mix calls/puts or expiries.
- **M01 reuse:** `NO_DIRECT_M01_D096_KERNEL; ACCEPTED_K09_INTERPOLATION_SPEC_ONLY`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1486,1589.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_cross_stage_k02_stage1_kernel.py`; `tests/product/derived_signal/test_m01_stage1_leaf2_temporal_graph.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Native R111/R112 pair, 50D coverage/profile; model/contract source and M02 structured per-expiry result. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D097 — Near-term IV term-structure slope
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D097` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D096`; catalogue window `e.g. 2D vs 9D / 9D vs 30D`; catalogue result units `vol points per day`.
- **Independent controlled inputs:** selected D096 expiry days10 and30; canonical ATM IVs0.20 and0.26.
- **Expected result or documented hold:** slope=100*(0.26-0.20)/(30-10)=3/10 vol-points/calendar-day. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Exactly two parameter-selected, ordered, distinct expiry nodes with complete D096 derivation and comparable 50D selections. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Equal days, compare different delta basis or invent missing expiry by interpolation.
- **M01 reuse:** `REUSE_K02_NONZERO_EXPIRY_DELTA; BLOCK_ON_D096`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1484,1495.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_cross_stage_k02_stage1_kernel.py`; `tests/product/derived_signal/test_m01_stage1_leaf2_temporal_graph.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** D096 prerequisite not implemented; tenor-selection criteria and source grid. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D098 — IV term-structure curvature
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D098` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D096`; catalogue window `Near/mid/long expiries`; catalogue result units `curvature`.
- **Independent controlled inputs:** D096 (day10,IV0.20),(day20,IV0.25),(day40,IV0.32).
- **Expected result or documented hold:** second divided difference=2*((0.32-0.25)*100/20-(0.25-0.20)*100/10)/(40-10)=-1/100 vol-points/day². This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Three ordered distinct expiry nodes with all D096 predecessor identities and units; nonuniform grid retained. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Equally spaced second difference used on irregular 10/20/40 grid; duplicate expiry; mixed ATM policies.
- **M01 reuse:** `REUSE_K02_NONUNIFORM_SECOND_DIFFERENCE; BLOCK_ON_D096`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1484,1498.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_cross_stage_k02_stage1_kernel.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** D096 predecessor expiry selection and result type. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D099 — 25-delta put-call skew / risk reversal
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D099` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R015;R111;R112`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `vol points`.
- **Independent controlled inputs:** same expiry 25D put IV0.30 and 25D call IV0.20, each matched to its own R112 delta and R015 native side.
- **Expected result or documented hold:** put-call risk reversal=+10 vol points. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Exactly one put and one call at 0.25 absolute native delta, same expiry/underlying/model, each IV/native delta/right from same contract. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Copy delta label from metadata; swap put/call sign; choose nearest 0.25 without approved interpolation.
- **M01 reuse:** `REUSE_K02_NATIVE_CONTRACT_DELTA_JOIN`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1508,1511,1561,1582,2223,3780.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_d104_owner_rule.py`; `tests/product/derived_signal/test_m01_f4_d104_skew_family_collision_red.py`; `tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR native option-right and model-delta quote availability. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D100 — 10-delta wing skew
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D100` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R015;R111;R112`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `vol points`.
- **Independent controlled inputs:** same expiry 10D put IV0.40 and 10D call IV0.25.
- **Expected result or documented hold:** put-call wing difference=+15 vol points. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Exactly one call/put pair at absolute native delta 0.10; matched expiry/contract-native side/delta, one compatible IV model. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Reuse 25D pair; missing wing silently replaced; mix expiry or native IV scale.
- **M01 reuse:** `REUSE_K02_NATIVE_CONTRACT_DELTA_JOIN`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1508,1582,2224,3780.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_d104_owner_rule.py`; `tests/product/derived_signal/test_m01_f4_d104_skew_family_collision_red.py`; `tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR 10D quotes/delta coverage and source eligibility. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D101 — Volatility smile curvature
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D101` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R111;R112`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `curvature`.
- **Independent controlled inputs:** same expiry 25D put0.30, 25D call0.20, ATM IV0.24.
- **Expected result or documented hold:** smile curvature=100*(.30+.20-2*.24)=+2 volatility points. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Complete same-expiry 25D put/call and native 50D ATM value or separately accepted ATM construction; unique complete row set. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Mix expiry, absent ATM or only one wing; choose undefined ATM estimator; wrong volatility multiplier.
- **M01 reuse:** `REUSE_K02_THREE_POINT_CURVATURE`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1508,1515,1545,1561.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR native delta grid and one-expiry ATM choice/coverage. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D102 — Volatility-surface fit error
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K09_SURFACE_DENSITY`; catalogue `D102` row; parameter profile `P_SURFACE`; typed contexts `OptionRevaluationConventionVersion`.
- **Exact dependencies:** raw `R014;R084;R093;R111;R118`, predecessor `D086`; catalogue window `NONE_DECLARED`; catalogue result units `vol points / score`.
- **Independent controlled inputs:** controlled IV points plus (strike,spot,T,IV bid/ask width); no numerical spline coefficient or revaluation convention admitted in this tranche.
- **Expected result or documented hold:** NO_NUMERICAL_ORACLE_AUTHORISED: expected refusal without OptionRevaluationConventionVersion / required constrained fit inputs. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Multiple strike and expiry observations with k=ln(strike/spot), T from D086; constrained spline fit needs quoted widths/weights and every nonnegative-calendar/convexity constraint, versioned grid/model. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Absent model, mismatched spot/time, infeasible static arbitrage constraints, silent equal-width fallback when bid/ask width positive.
- **M01 reuse:** `NO_DIRECT_M01_D102_KERNEL; MODEL_BLOCK_HONEST`. Source locator: No direct ID branch found in `_stage1.py`; indirect/generic handling unproved.
- **Existing public test navigation:** No exact literal reference in inspected `tests/product/derived_signal/*.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Concrete OptionRevaluationConventionVersion, spline knots/tolerances, source grid, no-arbitrage feasibility; model conventions outside tranche. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** one expiry+side |delta|=0.40 IV0.20 and |delta|=0.60 IV0.30; 50D bracket, no exact; second side absent with explicitly admitted single-side mode ⇒ linear interpolation IV=1/4; single-side only if mode admitted. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D102 first, then Absent model, mismatched spot/time, infeasible static arbitrage constraints, silent equal-width fallback when bid/ask width positive. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** D096 interpolation, D097/098 term derivatives, D099–101 contract-matched native-delta skew, and D102 arbitrage-aware constrained fit are separate subcontracts. D102 requires actual OptionRevaluationConventionVersion.
- **Status:** all 7 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Source-specific reuse challenge

**Observed M01 expiry-selection limitation:** `_stage1.py:1484–1507` sorts all available D096 term points and uses the first two/three. Accepted §5 K02 calls for **parameter-selected** near expiries. `test_m01_f4_cross_stage_k02_stage1_kernel.py:28–48` supplies only exactly two/three points, so it cannot distinguish selected maturities from the earliest available prefix. Future M02 witness needs a third/fourth distracting expiry outside the configured selected set, without assuming selection policy values absent authority.

## Exactness / result-shape qualification

**K09 model hold:** D096 cannot be treated as an arbitrary scalar `Decimal` if its admitted result preserves expiry/side/coverage. D097/D098 and D107/D108 must consume an exact selected IV component with proper shape and identity, rather than a fabricated scalar upstream fact.
