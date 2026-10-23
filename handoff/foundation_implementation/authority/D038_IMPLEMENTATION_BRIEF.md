# D038 — proposed controlled implementation profile

Status: PROPOSED — owner approval required under root EXEC_PLAN.md §3.5. No implementation/admission/runtime acceptance.
Baseline: caf01260f9299fa8bf075528baab48b34db48b5c. Owner instruction: “execute that plan for38,40and41”, 24 October2026.

## 1. Established meaning and proposed choices

Canonical catalogue: D038, Jump-variation estimate, R151/R149/R150, K05_REALIZED_RISK/P_VOL_WINDOW, variance. Accepted calculation law: r_i=ln(P_i/P_(i-1)); RV=sum r_i²; BV=(pi/2)*sum_(i=2..N)|r_i||r_(i-1)|; JV=max(RV−BV,0). No annualisation, sample correction or substituted estimator.

Primary evidence: K05 in handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md; exact catalogue D038 row; AnnexB D038 in FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md; FAMILY_F07_EXTENDED_E11_E15.md D038 card; G1_82_RAW_NATIVE_SOURCE_RESEARCH.csv R149/R150/R151 rows. The latter identify historical TRADES high/low/close candidates and retain native mapping/calendar/adjustment holds. They do not settle the choices below.

**Recommended proposal:** one controlled three-minute profile with four one-minute closes; use high/low as mandatory co-occurring bar-completeness/envelope evidence. Evaluate mathematical log and pi using rational interval bounds and round only the final JV to50 significant digits, ROUND_HALF_EVEN. This preserves the declared dependencies without inserting highs/lows into the return equation.

These source roles, grid and output precision are proposed domain choices, not facts already established by generic K05 or legacy code. No native IBKR bar/clock/adjustment certification is claimed.

## 2. Exact controlled source, time and identity contract

Owner target M02, existing public market_measurement_truth.api WindowCalculationRequestV1/WindowMeasurementOccurrenceV1 seams. Subject NVDA; no D predecessors. Definition D038-JUMP-VARIATION-1, kernel K05_REALIZED_RISK, profile P_VOL_WINDOW, units variance, result_shape scalar_decimal. Parameter mmt-d038-jump-3m-50d-half-even/1; selection mmt-d038-selection/1; context controlled-jump-3m-grid/1.

Controlled session20October2026 12:00–13:00Z, type controlled_cash, no breaks. Required sample instants12:37,12:38,12:39,12:40Z; start anchor12:37, as-of12:40, window_seconds180, history_complete_from12:37. Cutoff12:40:01Z; calculation time12:40:02Z. Four contiguous explicitly listed60second bars end at those instants. No required sample replacement, interpolation or horizon shortening.

Synthetic provider foundation-controlled-jump; variant trades_history_1m_v1; ingestion scope foundation-controlled-jump/trades_history_1m_v1. Source temporal kind true_instant represents the explicitly declared bar end in this synthetic profile. Native values finite Decimal price, identity unit scale1/offset0. No native provider timestamp conversion is inferred.

Each raw observation declares catalogue IDs R151,R149,R150 and native record:

- bar.close -> R151; mapping mmt-d038-close/1.
- bar.high -> R149; mapping mmt-d038-high/1.
- bar.low -> R150; mapping mmt-d038-low/1.
- bar.end_utc: exact ISO UTC end; bar.id: same ISO end string; bar.duration_seconds:60; session.id:controlled_cash_20261020; bar.series:TRADES; bar.adjustment_basis:controlled_unadjusted/1.

All three mappings preserve those six native identities; common unit convention mmt-d038-price/1.

Select the latest eligible R151 occurrence at each exact sample instant using event/receipt/ingestion provenance within the declared provider/variant/scope, visible at the cutoff. Then require R149/R150 projections from that SAME occurrence, matching identity, and low<=close<=high. Close must be positive; no extra arbitrary high/low sign cap. Missing/invalid co-fields in the selected latest occurrence refuse; an older complete occurrence cannot replace it. Ties unresolved by declared lawful provenance refuse. All sample events and receipts must be eligible; native revision_vintage remains absent in this controlled profile.

Lineage order: ascending sample instant; within each sample R151,R149,R150, preserving actual observation IDs and projections. Thus12 exact raw lineage entries represent four observations. No synthetic derived facts or hidden alternative scenarios.

## 3. Numerical contract and independent oracle

Use mathematical natural log and pi. Do NOT replace pi with a fixed truncated literal or round the log returns before RV/BV. Propagate exact rational intervals through log absolute values, squares/products, pi multiplication and the final max with0. Round both resulting interval endpoints to50 significant Decimal digits with ROUND_HALF_EVEN; emit only when they agree. Otherwise refine; if512 terms per bounded series do not certify a unique result, refuse. The proposed refinement schedule is32,64,...,512 terms. No floating-point arithmetic, ambient Decimal context or arbitrary tolerance.

Reuse the unchanged M02 rational log-series reasoning where applicable; _logarithm's already rounded50digit return alone is insufficient for this whole-expression contract. New D038-local interval/range-reduction code can reuse the existing positive-series bound without altering accepted log behaviour.

Independent documentary oracle used100 terms, Fraction arithmetic and explicit50digit rounding; it imported no product code:

- log(q): z=(q−1)/(q+1); S_n=2*sum_(k=0..n−1) z^(2k+1)/(2k+1), tail upper bound2*z^(2n+1)/((2n+1)*(1−z²)) for the positive q in this fixture.
- pi=16*atan(1/5)−4*atan(1/239); alternating atan partial sum and next partial sum bound each arctangent. The tangent identity and first-quadrant signs establish the Machin identity, not a sampled decimal assumption.
- With L=ln(11/10), M=ln(101/100): RV=2L²+M², BV=pi*L*M; propagate lower/upper rational endpoints conservatively into RV−BV. Its lower bound is strictly positive.

Both endpoints independently round to the following50digit values (RV/BV are explanatory diagnostics, not additional output fields):

- RV:0.018267069832752977501143002946891526536995557407530
- BV:0.0029793853847831415565163094998542451106293411820210
- JV:0.015287684447969835944626693447037281426366216225509

Required result Decimal tuple: sign0; digit string15287684447969835944626693447037281426366216225509; exponent−51. Freeze this literal in the future proof; the production evaluator is not an oracle. Nonzero BV and positive JV discriminate omission/wrong scaling of bipower subtraction. Two runtime cases do not independently exercise every numerical/floor branch; independent source review must assess those obligations, with any mandatory uncovered proposition recorded as a scope gap.

## 4. Exact proposed two-case manifest

Future physical proof: tests/product/market_measurement_d038/test_signal.py; sole test_d038_signal, parameter IDs success/refusal. No test file exists under this proposal and no cases ran.

Success: four actual M00 public observations, with event times as §2 and receipt=event+0.5seconds. Ingestion sequences1,2,3,4 in common scope. Ordered close/high/low:

| End UTC | Close | High | Low |
| --- | --- | --- | --- |
| 12:37 | 100 | 101 | 99 |
| 12:38 | 110 | 111 | 109 |
| 12:39 | 111.1 | 112.1 | 110.1 |
| 12:40 | 122.21 | 123.21 | 121.21 |

These yield returns L,M,L. Assert exact JV literal/type/tuple; complete definition/parameter/context/units/mappings; selected12entry actual lineage; owning admission/identity/times/window; ordinary public SQLite write and read-only reopen inside this same case.

Refusal: retain all four required latest closes/lows and the same request. For12:39, include an older complete observation received at12:39:00Z; the latest observation received at12:39:00.5Z lacks only bar.high. Public projection must establish the latest close/low and older complete high actually exist. Latest selection precedes co-field completeness: refuse and persist no D038 occurrence/history rather than combine occurrences or fall back to the older complete bar. Use distinct IDs and unambiguous monotonic ingestion sequence in this fixture; the later two base records' sequence numbers advance accordingly. This is the only negative scenario.

## 5. Proposed minimal implementation boundary after approval

- New src/nvda_desk/market_measurement_truth/_jump_variation.py owns this fixed profile, interval arithmetic, selection/co-occurrence checks and recomputation validator. build_owner(admission, raw, predecessor, storage, now) follows the existing window-owner factory contract.
- src/nvda_desk/market_measurement_truth/_window.py adds only D038 admission/reader routing. Reuse api.py's existing scalar Decimal/window result and generic durable codec/store; no new public carrier or storage framework is proposed.
- tools/product_proof_claims.py: one bounded fixed D038 declaration extension for the owning brief, contract, binding, claim and immutable generation, preserving loader algorithms/validators and every prior claim. Do not extend blocked D040/D041 targets yet.
- Owning brief/contract/binding/claim/admission/generation paths follow the existing market_measurement_d038 pattern; seal only after accepted authority, consistent hashes and actual physical proof bytes.
- New/changed-source mypy and Ruff only; no previous successful check or old test suite. Sole independent strict pair: PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d038, after runtime parameter/pins are actually verified.
- One independent final reviewer, substantive source/case judgement, strict pair and downloadable cumulative accepted Git checkpoint. Retain root bounded failed-check recovery. No shared runner changes to implement recovery.

## 6. Approval boundary and next action

Owner decision requested: accept the §2 source roles/grid/co-occurrence/envelope contract, §3 mathematical interval evaluation/final50digit rounding, and §4 two witnesses as this controlled D038 profile, and authorise its implementation under the already requested three-signal sequence.

Until accepted: D038 remains BLOCKED; zero runnable new cases and no admitted proof generation. D040/D041 remain at their existing profile/jurisdiction holds. Root plan requires stopping at the unresolved D038 choice; no downstream implementation or score coefficients were invented.
