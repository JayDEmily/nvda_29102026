# D041 — controlled mean-reversion conditions score

Status: ACCEPTED_FOR_IMPLEMENTATION under owner's24October2026 full completion delegation. Depends on D040 accepted checkpoint 171a9149dea53f44a1bd1fec6a1d7971c3c1a9f3; no reacceptance/retesting of D040. New signal, same admitted P02 responsibility/M03 runtime owner.

## 1. Exact canonical profile and meaning

D041_PROFILE.json owns the four ordered feature declarations and three exact predecessor contracts. Raw P_SCORE = (2 + |d|/(1+|d|) - t - v/(1+v))/3, where d is D026.percent_difference in percentage points, t is the accepted controlled D040 unsigned trend intensity, and v is nonnegative D033 annualised decimal volatility. K07 component extraction, bounded_ratio(scale1), paired signed clipping/orientation for d, identity for t, intercept2/3 and nonnegative weights1/3 implement that equation exactly. Generic score returns raw, no sigmoid. Clip follows transform and precedes orientation; no missing-feature renormalisation or implicit scalarisation.

This unsigned conditions index rewards price stretch against VWAP and penalises directional movement intensity and high volatility. Low volatility is an explicit level proxy, not a measured volatility-stability statistic. It gives no buy/sell direction, reversal probability, calibration, prediction or profitability guarantee. All values in [0,1]; fixed profile changes require new version.

## 2. Boundary and provenance

Use existing public frozen ScoreRequestV1/ScoreOccurrenceV1/ScoreProfileV1/FeatureEvidenceV1 and exact rational carrier from the D040 owning brief. Add public create_reversion_owner(admission,foundation_reader,score_reader,storage,utc_now) and create_reversion_reader(admission,storage). Separate typed foundation and same-owner score read facets ensure D040 is actually read from its owner, not handed in as an answer. Materialise, lookup and bounded history have the same contracts; read-only reader has no writer operation.

Only new _reversion.py implements this profile/selection/evidence/recomputation and its factories. api.py appends those two factory declarations; existing D040 factories/calculation/profile/test/generation/codec/store remain unchanged. Private imports within M03 are owner-local reuse, not peer calls. No M01/provider/API work. Existing fixed D041 proof declaration was added with D040; no loader/runner change now.

Request is NVDA/as-of20Oct2026 12:40Z. D041 allows cutoff T+1s or T+2s and calculation time >=cutoff. All selected actual direct predecessors must have exactly the request subject/as-of/cutoff and calculated_at <=now. This two-value controlled cutoff domain admits a meaningful future-compatible request while testing rejection of an older D040 knowledge snapshot. It does not alter D040's fixed T+1s profile.

D026 matches exact public price context12–13Z, window2400s from session start; D033 matches exact risk grid12:10–12:40Z/31minute closes with declared context/calendar and window1800s. Distinct close/price/risk context IDs and sample grids are explicitly compatible at the same subject/instant; do not fabricate a shared context ID. Full definition/brief/parameter/selection/version/window/units/result carriers and actual requested IDs/order are checked. Same-owner D040 must match its exact accepted profile/definition/brief hash and 1800s maximum component horizon; validate its own nested evidence with unchanged D040 validator and preserve exact instance. No foreign private import or predecessor requalification.

ScoreOccurrenceV1 retains complete actual D026/D040/D033 snapshots and four per-feature extraction/transform/orientation/weight records, own immutable profile bytes/hash, request, owner/admission, exact rational result and time/identity. Owner namespace/identity algorithm and technical SQLite profile are reused unchanged. Own admission binds this exact D041 brief. File validator restricts records to D041 while nested D040 remains a genuine predecessor; no old file migration. Separate file, own immutable append transaction/canonical hash/readback, ordinary public read-only durable reopen. Hostile-code/database-role security remains outside controlled trusted-application scope.

## 3. Exactly two cases and independent oracle

tests/product/configured_conditions_d041/test_signal.py: sole test_d041_signal, success/refusal. Common source setup may reuse unchanged D040 fixture construction code, but must not import/run its test or assert its acceptance suite.

Success: actual public M00->M02 close/VWAP inputs from D040's frozen witness; create real D040 using its accepted public factory and retain reader. This is predecessor materialisation, not a historical test rerun. Public D026 uses actual current last110 and cumulative session VWAP105 at T, giving percent_difference100/21 and bounded magnitude100/121. Public D033 uses actual31minute R151 closes100 except final110, giving the previously accepted exact Decimal 2.1397082297976278396691909270830504534270372226234. Use declared accepted controlled-risk calendar (11sessions10–20Oct12–13Z, minute intervals1/15120tradingyear).

The independent oracle reuses accepted D040's frozen rational from its owning §6, and D033's accepted literal from tests/product/market_measurement_d033/test_thirty_minute_realised_volatility.py. Apply (2+100/121-t-v/(1+v))/3 with standard-library Fraction, no product imports. Exact result numerator 467314847346827567997098903571949270113434695041186542272384088946224091736527877301805269524643233163672055237449516829689584217848364371480216014351600975360500026694492390610103370902206892963522677 and denominator 1118334641222872879090856194617732223528491901424553643707563560473702612201092412011248168844163188272351142399580166916130650797241778460099055375116915708572861408176162898213795850486628731345583764. Proof fixes those literal integers and separately asserts all four feature contributions against the independent frozen inputs, full typed metadata/actual lineage/profile/hash/times/units and public durable read-only reopen. These source rows are setup, not hidden extra scenarios.

Refusal: create actual D040 with its approved cutoffT+1s; create actual lawful D026/D033 with cutoffT+2s and request D041 cutoffT+2s, nowT+3s. Assert all three selected actual occurrences exist, same subject/as-of, correct identities/versions/shapes; D026/D033 match the new request and D040 alone differs in cutoff. It must reach D040's incompatible knowledge snapshot, emit None, leave D041 history empty. No extra missing fields, mutated frozen result or fabricated predecessor.

## 4. Proof discipline and limits

One independent final acceptance reviewer/sole strict executor; two cases only. No runtime RED, implementer GREEN, old product tests, probe or final sweep. Omission of RED deliberately reduces test-first evidence. Scoped mypy/Ruff only new _reversion.py/appended api.py/new proof; successful unchanged codec/store/D040 source evidence reused. No architecture requalification for unchanged owner/edges. Exact D041 binding/profile/contract/physical bytes inspected before immutable generation0001. Root bounded material-repair recovery applies without new approval.

Other P02 identities, native/provider/calendar certification, broader integration/E2E, application composition, empirical strategy quality, main integration and M01 historical-state retirement remain separate. Runtime pair does not individually certify every guard/fault/retry or adversarial store branch; independent review reports material gaps.

D041-PROOF-CONTRACT-SHA256: 9ff0224ec54801a90032ebaa451107f0f9029bb908b4e78300d107f5ce083086

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/configured_market_conditions/authority/D041_PROFILE.json | 6951cc43dc03045ca0f0ee4de12c3ccfb889bc56310ca3cbd5d4d16374095b6a |
| handoff/configured_market_conditions/authority/D041_PROOF_CONTRACT.json | 9ff0224ec54801a90032ebaa451107f0f9029bb908b4e78300d107f5ce083086 |
