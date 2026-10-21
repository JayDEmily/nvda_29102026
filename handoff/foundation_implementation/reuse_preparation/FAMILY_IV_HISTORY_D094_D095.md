# P3.1 family packet — option-contract IV changes: D094–D095

**State:** Documentary source/fixture/expectation extraction, NOT native IV/source acceptance or M02 implementation. Source and calculation: accepted brief `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md:166–183`; catalogue `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv:95–96`; Annex B `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md:577–578`. D094 declares R111, D095 declares R111 **and R183**; neither has a derived predecessor.

## Legacy M01 code and public tests — P1.1

- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:470–493` `_history_anchor` selects latest eligible current point, then latest point **at or before** the exact comparison anchor. `:247–272` `_same_option_history_selection` requires same subject plus contract ID or (fallback) expiry, delta bucket, right. `:2125–2325` `_eval_k03` computes D094/D095 as `100 × (current_IV − reference_IV)` in volatility points. **REUSE_AS_SPEC** after checking the effective row definitions; M01 private dispatcher and optional carrier are **REEXPRESS** at the authorised M02 seam, not private imports.
- `tests/product/derived_signal/test_m01_f4_rc14_option_iv_history_public.py:1–150` demonstrates raw M00 public native-record projections with typed exact `RawSelectionIdentityV1` (`contract_id`, `underlying_instrument`, `expiry`, `strike`, `option_right`), versioned field-path metadata, bounded `P_WINDOW`, R111 price history and R183 companion context. It covers both calculated expectations, omission, wrong-contract refusal and replay. **REUSE_AS_SPEC** as controlled history evidence; old M01 durability is not M02 SQLite proof.

## Historical fixture selection and negative preconditions — P1.2

`NOW=2026-10-10T03:00:00Z`; `END=NOW−2s`. The original controlled fixture publishes FIVE observations: R111 at END with IV `.53` (`iv-current`); R111 END−5min with `.50` (`iv-anchor-5m`); R111 END−1day with `.48` (`iv-anchor-day`); R111 END−2min with `.90` (`iv-near`, distractor); R183 at END with `.55` (`iv-context`). All records are separate M00 occurrences, same exact native option-selection identity and synthetic source; versioned `RawSignalProjectionMappingV1` points to `metric.R111`/`metric.R183` and selection keys to `identity.*`. Every datum must be visible at cutoff and in the same contract/bucket.

- D094 anchor is **current event time minus 300 seconds**; latest R111 at or before it is `.50`, **not** `.90` from two minutes earlier. Observed controlled expected is `100×(.53−.50)=3` volatility points.
- D095 anchor is **current event time minus one calendar day** in existing `_history_anchor`, choosing `.48`, with the additional declared R183 input. Observed controlled expected `100×(.53−.48)=5` volatility points. The original fixture calls it a one-day comparison; this **does not establish** a production trading-day/official-prior-close anchor. R183's exact mandatory semantic role versus R111-only `_eval_k03` calculation requires future contract review: declared projection/lineage is present in original test, but source-specific time/profile law must not be inferred.
- For D094, original negative case omits both `iv-anchor-5m` and `iv-anchor-day`; that is necessary because otherwise the day-old record remains a lawful fallback `<=` 5-minute anchor. A test that deletes only the five-minute record but expects refusal is **not authority-supported** by the current `latest at or before anchor` law.
- For D095, omission of `iv-anchor-day` or `iv-context` yields original refusal; wrong-contract prior day anchor refuses. For D094, making both anchor candidates belong to a different option contract refuses; preserving a valid older same-contract reference would defeat the intended negative. The fixture `future_current=True` is a constructed option, but the inspected file's tests do **not** exercise it; don't count it as existing D094/D095 proof.
- Original policy `maximum_staleness=3days`, `clock_skew=3days` is synthetic fixture config, not certified native IBKR option subscription/profile. The fixture has no pagination retry/reset, recovery, source revision or SQLite proof.

## Independent arithmetic and refusal witnesses — P2.1

| D | R111 current IV / eligible reference IV | Result | Additional premise |
| --- | --- | --- | --- |
| D094 | .53 / .50 at −5min | +3 volatility points | same exact contract |
| D094 | .50 / .53 at −5min | −3 volatility points | same exact contract |
| D094 | .50 / .50 at −5min | 0 volatility points | same exact contract |
| D095 | .53 / .48 at −1day | +5 volatility points | same contract, required R183 present |
| D095 | .48 / .53 at −1day | −5 volatility points | same contract, required R183 present |
| D095 | .48 / .48 at −1day | 0 volatility points | same contract, required R183 present |

Results are explicit decimal subtraction ×100, not copied as computation from `_eval_k03`. For wrong-contract reference, missing eligible anchor, out-of-cutoff current or missing R183 where required, expected **no occurrence**, not numerical zero. A production IV validity domain cannot be certified from controlled `.53/.48` alone.

## Provider/source and scope holds — P2.2

The original catalogue/workbook name IV raw feeds but do **not** establish current native `R111`/`R183` callback/field conversion, side/model/snapshot semantics, full option contract key, missing/sentinel handling, quote timestamp/receipt eligibility, expiry/calendar roll rules or stable field/scale across the prior reference. These remain `RAW-PROJECTION`, `CALC-PROFILE`, and if one-day anchor is trading-session dependent `SRC-CALENDAR`. Ask the IBKR source-research owner specifically: What accepted provider/mapping/version/source-temporal contract certifies R111 and R183, and how are same-option history and official one-day anchors supplied? Synthetic mathematical success cannot grant native option source certification.

## P3.1 adversarial independent reasoning

Without trusting the M01 `_public()` fixture helper: prescribe four R111 values at explicit instants/IDs as listed above. Verify the set with times ≤END−5min is `{.50, .48}`, hence its max event timestamp is `.50`; `.90` must be excluded. For D095 the ≤END−1day reference set is `{.48}`. Replace both eligible 5m-and-older records' contract with C2 while keeping current C1; resulting reference selection **must refuse**. This isolates ordering and identity from helper composition. No fresh independent reviewer/runtime execution occurred; the future reviewer must challenge the admitted M02 public path separately.
