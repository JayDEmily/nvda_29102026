# D032 — controlled 5m exact risk admission

ACCEPTED_FOR_IMPLEMENTATION under the owner's commissioned D026–D036 controlled tranche, with separate human review waived by owner and source certification deferred. No normative permission to synthesize real trading calendars.

## 1. Exact semantic identity

R151 unadjusted bar closes at all 6 exact controlled 5m sample instants 2026-10-20T12:35:00+00:00 through 2026-10-20T12:40:00+00:00, 5 authorised return intervals, log provenance and exact annualisation fraction. Positive result 5.2411933614380407513132873039695738036883343009577 annualised volatility. Negative middle 12:37 minute omitted; 12:37:30 off-grid present must refuse and write no occurrence.

Definition `D032-REALISED-VOL-1`, parameters `mmt-realised-vol-5m-50d/1`, selection `mmt-realised-vol-5m-selection/1`, R151 native `bar.close` price. Controlled year252 explicit hour-long sessions, no overnight elapsed time, every required interval exact Fraction. Positive closes all100 except final110. Log ratio ln(110/100) computed by unchanged `_log_return._logarithm` once and treated as exact rounded Decimal intermediate; squared sum/interval-year Fraction root rounded once using unchanged `sqrt_ratio_50`. No D predecessors or M00 mutations.

### 4.3 Realised-volatility calendar, complete grids and annualisation

Use R151→bar.close under `mmt-risk-close/1`, native price and `mmt-pilot-price/1`. Expose session.id, sample.kind and adjustment.basis. Require adjustment=`unadjusted`; intraday sample kinds=`session_open`, `minute_close`, `official_close` according to the exact grid; daily samples=`official_close`. No synthetic R151-to-R143 dependency or D019/D020/D021 predecessor.

Controlled risk calendar `controlled-risk-calendar/1`: explicit sessions10–20October2026, each12:00–13:00Z, no breaks, type=`controlled_cash`, ref `controlled-risk-YYYYMMDD/1`. The **proposed synthetic trading year is252 such60minute sessions**: 15,120 eligible minutes. This is a declared fixture parameter, not an empirical market-year claim. Persist exact per-interval trading-year fractions, calculated by intersection with the listed eligible session intervals; never charge overnight/closed time.

| ID | Exact required sample grid / as-of T | Return intervals / total year fraction |
| --- | --- | --- |
| D032 | 20Oct12:35,12:36,…,12:40 | 5; each1/15120, total5/15120 |
| D033 | 20Oct12:10,12:11,…,12:40 | 30; each1/15120, total30/15120 |
| D034 | 20Oct12:00,12:01,…,13:00 inclusive | 60; each1/15120, total1/252 |
| D035 | Official closes15–20Oct at13:00 | 5; each1/252, total5/252 |
| D036 | Official closes10–20Oct at13:00 | 10; each1/252, total10/252 |

D035's15Oct close is the price anchor; the five complete measured sessions are16–20Oct. D036's10Oct anchor precedes the ten complete measured sessions11–20Oct. Known exact calendar/sampling completeness must be represented, not inferred from having six/eleven numeric values. Historical visibility allowance30days; every selected grid event matches exactly and is visible at cutoff. Required prices strictly positive. Missing official-close/minute positions refuse even if other older/off-grid prices are present. D032 negative off-grid sample is12:37:30 after omitting12:37; D034 negative after-session close is13:01, receipt13:01, cutoff13:02 and now13:03 so it is genuinely visible but cannot be the official13:00 sample. Other cases use common cutoff/now offsets.



D032–D036: for each adjacent close pair, reuse unchanged `_log_return._logarithm` to obtain its canonical50-digit half-even Decimal log. Treat each such finite log as an exact rational intermediate; square/sum and divide by exact sum of interval year fractions using Fraction. Apply sqrt_ratio_50 once for final annualised volatility. **This explicitly proposed two-stage numerical convention preserves log-rounding provenance; it does not claim an unrounded irrational result.** Do not silently switch to mean-centred sample SD, log-of-price differences, float annualisation, a second intermediate rounding, or a constant dt times count without validating the interval measures.



## 2. Exact two-case proof and gate

Contract SHA256 d088600e510dc3dcc2b840e2d5ed76b1f32efb66b9d7fdd80a4a452e9ecf5eca. Exactly one parameterised function `test_d032_five_minute_realised_volatility`, two cases in `tests/product/market_measurement_d032/test_five_minute_realised_volatility.py`. Positive asserts exact canonical 50-digit Decimal literal, owner/definition/parameter/policy/units/context, ordered public M00 lineage and read-only SQLite reopen. Negative creates otherwise lawful evidence for the specified missing-grid condition and asserts nonmaterialisation. No extra cases, no broad regressions.

## 3. Shared bounded changes

D032 introduces `RealisedRiskWindowContextV1` and `TradingReturnIntervalV1` with exact immutable session/sample/interval identity; later D033–D036 reuse it. The sole new source owner `_realised_volatility.py` reuses native M00 projection and the immutable shared numeric helpers. No existing context layout, accepted proof, M00 or legacy M01 modification.

## 4. Incorporated bytes

D032-PROOF-CONTRACT-SHA256: d088600e510dc3dcc2b840e2d5ed76b1f32efb66b9d7fdd80a4a452e9ecf5eca

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |
| handoff/foundation_implementation/authority/D032_PROOF_CONTRACT.json | d088600e510dc3dcc2b840e2d5ed76b1f32efb66b9d7fdd80a4a452e9ecf5eca |
