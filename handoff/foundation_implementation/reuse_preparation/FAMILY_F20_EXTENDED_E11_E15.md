# F20 — Option contract calendar: documentary E1.1–E1.5 assessment

**Scope:** 2 individual IDs: D085, D086. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** Calendar days and ACT/365F differ; market-local expiry clock must be versioned, not inferred from option last trading day or hard-coded midnight.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D085 — Calendar days to expiry
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K01_TIME`; catalogue `D085` row; parameter profile `P_TIME`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R001;R013`, predecessor `D004`; catalogue window `NONE_DECLARED`; catalogue result units `days`.
- **Independent controlled inputs:** D004 exchange-local trading date 2026-10-20; R013 expiry date 2026-10-23.
- **Expected result or documented hold:** whole calendar days = 3. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Same contract R013 and D004 exchange-calendar occurrence, including overnight date boundary. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Expired contract negative interval; interpret 3 trading sessions rather than calendar days; wrong timezone.
- **M01 reuse:** `REUSE_K01_EXPIRY_DATE_DIFFERENCE`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1343,3142,3146.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_temporal_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`; `tests/product/derived_signal/test_m01_f3_grouped_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR option contract expiry date and exchange-session timezone. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D086 — Time to expiry in years
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K01_TIME`; catalogue `D086` row; parameter profile `P_TIME`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R013`, predecessor `D001`; catalogue window `NONE_DECLARED`; catalogue result units `years`.
- **Independent controlled inputs:** D001 2026-10-20 00:00Z; configured expiry instant 2026-10-21 00:00Z.
- **Expected result or documented hold:** ACT/365F = 1/365 years. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Source R013 date plus explicit configured expiry time/IANA zone, true D001 timestamp; no implicit midnight. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Expire in past; date-only treated as instant; use 365 trading days or unapproved early expiry.
- **M01 reuse:** `REUSE_K01_ACT365F_WITH_VERSIONED_CLOCK`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1361.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_temporal_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Option expiry clock/exercise/market holiday mapping. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** D004 exchange-local trading date 2026-10-20; R013 expiry date 2026-10-23 ⇒ whole calendar days = 3. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D086 first, then Expire in past; date-only treated as instant; use 365 trading days or unapproved early expiry. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** Calendar days and ACT/365F differ; market-local expiry clock must be versioned, not inferred from option last trading day or hard-coded midnight.
- **Status:** all 2 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Exactness / result-shape qualification

**Result-carrier hold:** D086 returns mathematical ACT/365F `1/365` in the controlled example; this is non-terminating in base 10. A Decimal quotient with ambient precision is not automatically the accepted exact carrier. Define versioned exact fraction/precision before M02 acceptance.
