# F25 — IV surface changes/ranks: documentary E1.1–E1.5 assessment

**Scope:** 4 individual IDs: D103, D104, D105, D106. **Disposition:** audited with precise native/profile/model holds; no M02 implementation, independent reviewer verdict, proof admission, or authority change.

**Pinned source checkpoint:** 755ee4d8e5a6ab552b069cba2ba20906a3a3d368 (pre-this-pass preparation branch). Concurrent Gate 6 worker state UNKNOWN. This is a task-local documentary audit only.

## E1.1 — directly inspected authority and reuse boundary

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5, §6–9; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` exact named rows; accepted foundation Annex B and active root `EXEC_PLAN.md` §7.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` direct code locations and relevant existing public tests, enumerated under each ID. Literal search was reconciled with calculation kernels and dispatcher; a zero hit is not a blanket absence finding.
- `src/nvda_desk/market_measurement_truth/api.py` identifies the newer public owner boundary. Existing M01 calculation/fixture behaviours are reuse candidates, never imported tests or already accepted M02 facts.
- **Family-specific semantic discriminator:** Surface-grid equality, D104 coherent skew-pairing, one-year rank and one-year midrank percentile each have separate history and selection. Baselines exclude current.

## E1.2–E1.4 — individual equations/witnesses, full prerequisites, failure cases, exact holds

### D103 — Parallel IV surface shift
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D103` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R111`, predecessor `NONE_DECLARED`; catalogue window `Snapshot-to-snapshot / 5m / 1d`; catalogue result units `vol points`.
- **Independent controlled inputs:** matched 2-point grid prior IVs=(.10,.20), current IVs=(.20,.30).
- **Expected result or documented hold:** parallel shift=100*mean(.10,.10)=+10 vol points. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Exactly identical contract/expiry/strike/right/delta-key grid at two ordered native snapshots; full common matched grid not intersection. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Prior grid lacks one contract; duplicate grid_key; current before prior; wrongly intersection-reduced mean.
- **M01 reuse:** `REUSE_K03_EXACT_SURFACE_GRID_MATCH`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2184.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc14_surface_shift_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** IBKR full options-grid acquisition/snapshot pairing. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D104 — Skew rotation
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K03_CHANGE_RETURN`; catalogue `D104` row; parameter profile `P_WINDOW`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `NONE_DECLARED`, predecessor `D099;D100`; catalogue window `5m/1h/1d`; catalogue result units `vol points`.
- **Independent controlled inputs:** same expiry 25D skew prior8/current10 points; 10D skew prior12/current15 points.
- **Expected result or documented hold:** rotation=(15-12)-(10-8)=+1 vol point. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Four D099/D100 immutable predecessor points; each family paired within its own horizon, same underlying/expiry and coordinated current/prior times. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Mix 25D now with 10D prior; missing prior bucket; different expiry; use absolute skew at current only.
- **M01 reuse:** `REUSE_K03_D104_EXPLICIT_CROSS_FAMILY_PAIRING`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2217,2218,3773.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_d104_owner_rule.py`; `tests/product/derived_signal/test_m01_f4_d104_skew_family_collision_red.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** Source-supported skew history/anchor/profile and shape lineage. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D105 — 1-year IV rank
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K04_STANDARDISE_RANK`; catalogue `D105` row; parameter profile `P_BASELINE`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R183`, predecessor `NONE_DECLARED`; catalogue window `1 year`; catalogue result units `0-100`.
- **Independent controlled inputs:** strictly previous one-year IV min0.20/max0.40; current comparable IV0.30.
- **Expected result or documented hold:** one-year IV rank=100*(.30-.20)/(.40-.20)=50%. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** Complete versioned one-year prior IV reference baseline for matching delta/expiry/model, excluding current; at least distinct bounds. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Current included in baseline; zero min/max range; incomparable tenor or source change.
- **M01 reuse:** `REUSE_K04_1Y_RANGE_EXCLUDING_CURRENT`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2357,2465.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc14_iv_baseline_public.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** R183 collection/history frequency and comparable-IV definition. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

### D106 — 1-year IV percentile
- **Authority:** `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K04_STANDARDISE_RANK`; catalogue `D106` row; parameter profile `P_BASELINE`; typed contexts `NONE_DECLARED`.
- **Exact dependencies:** raw `R183`, predecessor `NONE_DECLARED`; catalogue window `1 year`; catalogue result units `percentile`.
- **Independent controlled inputs:** strictly previous comparable IV sample (0.20,0.30,0.40,0.50); current=0.30.
- **Expected result or documented hold:** percentile=100*(1+0.5*1)/4=37.5%. This is a hypothetical mathematical fixture, not certified native price/IV/model data.
- **Selection/history/fixture preconditions:** All applicable prior one-year comparable observations, matched tenor/IV model; declared handling of missing source days and sample membership. The observed fixture must contain required source observations before injecting refusal/fault conditions, and complete pagination must not exhaust prematurely.
- **Adversarial/refusal discriminators:** Current included; tie counted as all-less or all-greater; incomplete one-year history passed as full.
- **M01 reuse:** `REUSE_K04_MIDRANK_PERCENTILE_EXCLUDING_CURRENT`. Source locator: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` lines 2358,2470.
- **Existing public test navigation:** `tests/product/derived_signal/test_m01_f4_rc14_iv_baseline_public.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py`. Prior tests may encode old convenience/missing-data assumptions and are not proof of this authorised M02 behaviour.
- **Unresolved receiver/hold:** R183 native 1Y history/cadence, comparable IV and calendar policy. M02 output shape, history, immutable identity and separated SQLite read/write must still be specified and proved under the active root authority.

## E1.5 — bounded challenge and authority limits

The following manual construction challenges both calculation arithmetic and fixture sufficiency. Values were selected from the accepted expressions, not copied from M01 test expected-answer helpers. Each per-ID case above is a controlled witness; complex model-dependent outputs deliberately remain unnumbered where the versioned model or fit is missing.

- **Numerical discriminator:** matched 2-point grid prior IVs=(.10,.20), current IVs=(.20,.30) ⇒ parallel shift=100*mean(.10,.10)=+10 vol points. A different ratio unit, sign or current-in-baseline interpretation fails the stated law.
- **Selection/negative discriminator:** supply the positive preconditions for D106 first, then Current included; tie counted as all-less or all-greater; incomplete one-year history passed as full. Observe a *domain* refusal only after the real source/contract selector is exercised; an empty loader or cursor exhaustion is not equivalent.
- **Holds stay open:** Surface-grid equality, D104 coherent skew-pairing, one-year rank and one-year midrank percentile each have separate history and selection. Baselines exclude current.
- **Status:** all 4 signal rows `AUDITED_WITH_PRECISE_HOLDS` as an author documentary classification only. No independent review, real-provider mapping, physical proof admission, M02 implementation, test run, or native test-data certification.

## Source-specific reuse challenge

**Observed source versus native-history distinction:** `_stage1.py:2465–2483` computes D105/D106 from a parameter-counted sample. Its code path alone does not certify an actual complete one-year comparable-IV history or the native R183 cadence. Future tests must establish the exact lookback coverage and equality/strict-prior membership, not merely that `history_count` points exist.
