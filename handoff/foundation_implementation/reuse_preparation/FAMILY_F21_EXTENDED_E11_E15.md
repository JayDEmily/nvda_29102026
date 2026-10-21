# F21 — Option moneyness and delta bucket: documentary E1.1–E1.5 assessment

**Scope:** 3 individual IDs: D089, D090, D091. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** Strike/spot moneyness and native delta bucketing have distinct semantics. P_BUCKET boundaries and native IBKR model-delta interpretation are separate.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D089 — Spot moneyness
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D089` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R014;R118`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `ratio`.
- **Independent controlled inputs:** R014 strike110; R118 spot100, same contemporaneous underlying.
- **Expected result or documented hold:** strike/spot=11/10. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Exact contract/underlying mapping, contemporaneous spot and strike; both nonzero positive for log downstream. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** R118 zero; substitute different underlying or stale spot; R014 means delta.
- **M01 reuse:** `REUSE_K02_POSITIVE_RATIO`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1471,1475.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_option_scalar_public.py`; `tests/product/derived_signal/test_m01_f4_cross_stage_rule_algebra_own_kernel.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR strike/currency scale, underlying match/time skew. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D090 — Log-moneyness
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D090` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R014;R118`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `dimensionless`.
- **Independent controlled inputs:** R014 strike110; R118 spot100, same contract and source profile.
- **Expected result or documented hold:** ln(11/10). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Same aligned raw strike/spot pair and positive ratio; preserve exact contract lineage. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Nonpositive strike/spot or mixed underlying; use natural log of difference not ratio.
- **M01 reuse:** `REUSE_K02_LOG_RATIO_DOMAIN_GUARD`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1474.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_option_scalar_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR R014/R118 units and contract-to-underlying joining. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D091 — Delta bucket
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K08_RULE_BUCKET_POLICY`; catalogue `D091` row; parameter profile `P_RULE`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R112`, predecessor `NONE_DECLARED`; catalogue window `NONE_DECLARED`; catalogue result units `category`.
- **Independent controlled inputs:** versioned bucket bounds (0,0.2,0.35,0.6) and labels (10D,25D,50D); R112 absolute delta=0.25.
- **Expected result or documented hold:** label=25D (under this stated example profile only). This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** One native R112 delta and a complete ordered disjoint finite P_BUCKET boundary/label configuration, exact contract, side and expiry. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Delta0.35 boundary assigned wrong side; no profile; percentage 25 substituted for fractional 0.25; absent side.
- **M01 reuse:** `REUSE_K08_PARAMETERISED_HALF_OPEN_BUCKETS`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1593,1596,1600,3084,3142,3146.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_d110_spot_expected_move_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`; `tests/product/derived_signal/test_m01_f3_grouped_public.py`; `tests/product/derived_signal/test_m01_stage1_predecessor_scope.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR model delta sign/convention and actual admitted bucket boundaries. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** R014 strike110; R118 spot100, same contemporaneous underlying ⇒ strike/spot=11/10. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D091 first, then Delta0.35 boundary assigned wrong side; no profile; percentage 25 substituted for fractional 0.25; absent side. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** Strike/spot moneyness and native delta bucketing have distinct semantics. P_BUCKET boundaries and native IBKR model-delta interpretation are separate.
- **Status:** all 3 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Exactness / result-shape qualification

**Logarithm precision hold:** D090 exact `ln(11/10)` is symbolic. Its Decimal/log implementation rounding and canonical hash stability need explicit contract, without inventing a tolerance.
