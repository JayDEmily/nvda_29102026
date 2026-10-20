# F27 — ATM straddle and implied move: documentary E1.1–E1.5 assessment

**Scope:** 2 individual IDs: D109, D110. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** ATM selection comes from D091, pricing from D087, and underlier from aligned R118. A midpoint price alone cannot certify that a contract is ATM.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D109 — ATM straddle midpoint premium
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D109` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D087;D091`; catalogue window `NONE_DECLARED`; catalogue result units `currency/share`.
- **Independent controlled inputs:** D087 same-expiry near-ATM call mid2 and put mid3, both independently classified by compatible D091.
- **Expected result or documented hold:** ATM straddle midpoint premium=5 option-price currency units. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Exactly one eligible ATM call and put, same underlying/expiry/strike and source/cutoff; D091 family/contract selection and D087 occurrences complete. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Pair call/put different strikes/expiries; duplicate side; select nearest without admitted ATM policy; after-cutoff quote.
- **M01 reuse:** `REUSE_K02_MATCHED_CALL_PUT_MIDS`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1592,1640.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_d110_spot_expected_move_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`; `tests/product/derived_signal/test_m01_f3_contract_graph.py`; `tests/product/derived_signal/test_m01_stage1_predecessor_scope.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR option pair/ATM selection rule and contract multiplier output scale. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D110 — ATM straddle implied move percentage
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K02_ALGEBRA`; catalogue `D110` row; parameter profile `P_BASIC`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R118`, predecessor `D109`; catalogue window `NONE_DECLARED`; catalogue result units `percent`.
- **Independent controlled inputs:** D109 paired straddle premium5; aligned R118 spot100.
- **Expected result or documented hold:** 100*(5/100)=5%. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Matched underlying/currency/timestamp for D109 and positive R118; D109 itself must have lawful D087/D091 lineage. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Spot zero; mix contracts/multipliers or different underlying spot; mistakenly sqrt(DTE)-scale without authority.
- **M01 reuse:** `REUSE_K02_SPOT_SCALED_STRADDLE`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1638.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_d110_spot_expected_move_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR spot source, premium units/multiplier convention. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** D087 same-expiry near-ATM call mid2 and put mid3, both independently classified by compatible D091 ⇒ ATM straddle midpoint premium=5 option-price currency units. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D110 first, then Spot zero; mix contracts/multipliers or different underlying spot; mistakenly sqrt(DTE)-scale without authority. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** ATM selection comes from D091, pricing from D087, and underlier from aligned R118. A midpoint price alone cannot certify that a contract is ATM.
- **Status:** all 2 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Source-specific reuse challenge

**Observed fallback to check before reuse:** `_stage1.py:1592–1636` contains a fallback to `metadata.delta` when no D091 occurrences are present. The current catalogue gives D109 an explicit D091 predecessor. Existing `test_m01_f4_d110_spot_expected_move_public.py` provisions actual bucket classifications for its positive public witness; it does not turn the fallback into accepted M02 authority. Future proof must insist on the declared D091 selection or obtain a separately admitted alternative.
