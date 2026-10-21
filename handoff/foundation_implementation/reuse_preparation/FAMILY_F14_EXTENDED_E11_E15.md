# F14 — Macro event/time/surprise: documentary E1.1–E1.5 assessment

**Scope:** 2 individual IDs: D062, D063. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** Event calendar release metadata is not observed native truth merely because R284/R285/R286 are catalogued. Current surprise must be excluded from historical baseline.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D062 — Time to next scheduled event
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K01_TIME`; catalogue `D062` row; parameter profile `P_TIME`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R284`, predecessor `D001`; catalogue window `NONE_DECLARED`; catalogue result units `seconds/minutes`.
- **Independent controlled inputs:** as_of=12:00:00Z; relevant future R284 events at 12:01:30Z and 12:03:00Z.
- **Expected result or documented hold:** {seconds=90,minutes=3/2}. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Minimum future relevant event strictly after as_of; event timestamp must have been disclosed/known by cutoff; D001 true instant. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Earlier-but-closer event; exactly-now event; future event published only after cutoff; no eligible event.
- **M01 reuse:** `REUSE_K01_FUTURE_EVENT_SELECTOR`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 1329.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_next_event_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Economic-calendar source/event identity and reliable publication/vintage timestamp. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D063 — Standardised macro surprise
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K04_STANDARDISE_RANK`; catalogue `D063` row; parameter profile `P_BASELINE`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R285;R286`, predecessor `NONE_DECLARED`; catalogue window `Release-specific historical window`; catalogue result units `z-score`.
- **Independent controlled inputs:** historical surprises [-1,0,+1] from strictly prior releases; current actual-consensus=2.
- **Expected result or documented hold:** z=(2-0)/sample_sd([-1,0,+1])=2. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** At least two *historical release-specific* actual-minus-consensus observations, all published before current release, plus current actual and prior-known consensus, with release/vintage mapping. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Include current surprise in baseline; N<2; constant historical surprises; post-release consensus revision.
- **M01 reuse:** `REUSE_K04_STANDARDISE_EXCLUDING_CURRENT`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2361.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc21_macro_surprise_public.py`; `tests/product/derived_signal/test_m01_f4_rc21_macro_growth_factor_public.py`; `tests/product/derived_signal/test_m01_f4_rc21_macro_inflation_factor_public.py`; `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Economic-calendar actual/consensus source and revision policy; P_BASELINE N. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** as_of=12:00:00Z; relevant future R284 events at 12:01:30Z and 12:03:00Z ⇒ {seconds=90,minutes=3/2}. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D063 first, then Include current surprise in baseline; N<2; constant historical surprises; post-release consensus revision. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** Event calendar release metadata is not observed native truth merely because R284/R285/R286 are catalogued. Current surprise must be excluded from historical baseline.
- **Status:** all 2 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Controlled fixture supplement — R284/R285/R286 (21 October 2026)

**Scope/status:** supplemental synthetic specification to avoid repeated fixture design. `F14_R284_R285_R286_CONTROLLED_SYNTHETIC_V1.json` is the exact fixture-value manifest. The fields/keys in that file are **fixture-local invented labels**, not a provider schema, admitted raw projection mapping, source guarantee, executable test, or immutable M02 proof. The accepted equations and native-source holds above remain unchanged.

- **R284 / D062:** controlled UTC as-of and knowledge cutoff `2026-10-21T12:00:00Z`; earlier `11:59:00Z` and exactly-now `12:00:00Z` events are ineligible. Events at `12:01:30Z` and `12:03:00Z` were disclosed/received before cutoff, hence select the first: **`seconds=90`, `minutes=1.5`**. An earlier-future `12:00:30Z` event is deliberately received **after** cutoff and must not displace the result. The manifest also provides past-only, unseen, missing, wrong-family and late-receipt discriminators. D001 must be a genuine `true_instant`, not a date-only invention. The semantics of a real provider's event identifier, relevance and revision/availability remain unadmitted.
- **R285/R286 / D063:** controlled **synthetic** US-CPI headline YoY percent-valued release family, paired by release ID. The prior three `(consensus,actual)` pairs are `(2.5,2.4)`, `(2.5,2.5)`, `(2.5,2.6)`; current pair is `(2.5,2.7)`. All values share a declared fixture unit; historical surprise differences in percentage points are `[-0.1,0,+0.1]`, current `+0.2`; sample mean `0`, `N-1` sample SD `0.1`, so **`z=2`**. The manifest fixes prior consensus-known and actual-received timestamps separately, `history_count=3` *for this synthetic scenario only*, and release IDs/family. Negative cases cover incomplete current/history pairs, insufficient N, zero variance, wrong release family, current-in-own-baseline and late consensus revision. No percent-to-fraction conversion policy for a real source is inferred: consistent units cancel from the z-score, but traceable unit normalisation remains a distinct source contract.
- **Fixture construction rule:** create records with explicit individual release/event IDs, non-overlapping publication/receipt/order metadata, and enough qualifying baseline records **before** removing/injecting any negative member. Do not use a convenience helper that substitutes prior releases, inserts a new forecast, computes the expected oracle, advances the cutoff or pre-performs the operation under test. Preserve separate D062 temporal scheduling/knowledge roles and D063 paired release/forecast/actual roles.
- **Evidence/authority boundary:** controlled synthetic arithmetic is supported by the accepted §5 K01/K04 rules and the pre-existing F14 witnesses; selected synthetic values/timestamps are **proposed fixture inputs**, not observed economic releases. Real economic-calendar publisher, fields, timezone, native units, entitlements, release/forecast revisions, baseline N, source-to-M00 mappings and M02 profile/typed result/SQLite proof remain exact admission/implementation holds. A test using these examples cannot be counted as native-source certification or already-admitted M02 proof.
