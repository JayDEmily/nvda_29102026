# D029 — exact controlled implementation

ACCEPTED_FOR_IMPLEMENTATION under owner instruction23October2026 to complete D026–D036 and checkpoint each signal. Standing delegated concrete profile/proof admission; one independent final source/case review and sole final strict GREEN required. No provider/API/native certification.

## 1. Exact meaning/profile

R144 current16 versus exact twenty immediately prior same-bucket observations8,12 repeated ten times. Mean10/sample variance80/19; signed exact-root result rounded once to50significant digits. Missing mandatory30September matching bucket refuses even with older matching decoy.

Definition D029-VOLUME-ZSCORE-1; parameter mmt-volume-zscore-20sessions-50d/1. ### 4.2 Baseline calendar and mappings

Controlled calendar `controlled-volume-calendar/1` lists daily synthetic sessions for29September–20October2026 inclusive, each12:00–13:00Z, no breaks, type=`controlled_cash`, identities `controlled-volume-YYYYMMDD/1`. This is an explicit synthetic list including weekends; never label it a US exchange calendar or generate a supposedly certified calendar from weekdays. Each listed frame is known at cutoff and immutable;29September is an older compatible decoy, outside the mandatory twenty-session window.

T=20October12:30Z. D028 fixes N=2 (18/19October are immediately prior); D029–D031 fix N=20 (30September–19October), current excluded. Historical role visibility allowance30days, current freshness60s. Session membership comes from the exact calendar order, not observed row count or whichever older sessions have data. Require one unique eligible selected state per mandatory session and exact source/unit/method compatibility. Each historical session/state precedes current.

Mappings version1, same controlled provider/variant:

| R / mapping | Numeric field / native units | Native identity metadata |
| --- | --- | --- |
| R041 / `mmt-session-volume` | session.volume / shares | session.id, counter.generation, counter.basis, counter.complete_from_open |
| R144 / `mmt-bar-volume` | bar.volume / shares | session.id, bucket.id |
| R062 / `mmt-trade-rate` | activity.trades_per_minute / trades/minute | session.id, bucket.id |
| R063 / `mmt-volume-rate` | activity.shares_per_minute / shares/minute | session.id, bucket.id |

For each row identity keys are the listed full dotted names in the listed order, mapped to the corresponding tuple field paths. Unit conventions are identity transforms: `mmt-shares/1`, `mmt-trades-per-minute/1`, `mmt-shares-per-minute/1`. Do not infer rates from totals or share volume from trade counts.

D028 uses exact elapsed eligible trading seconds / total eligible session seconds, calculated from the admitted frame and selected event; desired fraction1/2 is12:30 in each60minute session. Cumulative values are nonnegative, basis=`cash_shares_unadjusted`, generation=`counter-YYYYMMDD/1`, complete_from_open=True. In the negative exactly one required counter reports False. Include a19October12:31 value999 (wrong fraction) and17October12:30 value999 (outside required N) in both cases; neither repairs the negative. Current30; mandatory18October10 and19October20. Require equal session type/duration, correct generation, complete-from-open counters and positive prior mean; no interpolation/scaling/skipping. Zero current is lawful if mean positive.

D029–D031 use native bucket.id=`minute-ending-1230/1`; each value describes the completed [12:29,12:30] minute in its session. Exact event=12:30, source units as above; all volumes/rates are finite and nonnegative. Baseline tuple in chronological calendar order is (8,12) repeated ten times in twenty **distinct sessions/occurrences**. Mean10, sum squared deviations80, sample variance80/19. Current16. Require exactly these twenty immediately prior sessions, not the current value, older replacements or nearest bucket. D029's wrong-bucket decoy is a separate19October12:31 observation999 with bucket `minute-ending-1231/1`; its negative changes the required30September bucket to `minute-ending-1229/1` with matching12:29 event and retains an older29September matching-bucket8 decoy outside the required twenty-session window. D031 negative changes only one required prior receipt to cutoff+1s; public direct projection establishes that future-received source exists.

### 4.4 Fixed arithmetic and independent literals

D026/D027/D028 use exact Fraction arithmetic and reduced ExactRatioV1; no Decimal division or rounding. New public frozen carriers: `VwapDeviationV1(price_difference:ExactRatioV1, percent_difference:ExactRatioV1)`; `VwapRateV1(price_per_minute:ExactRatioV1, percent_per_minute:ExactRatioV1)`. Do not reuse D018's bps-named carrier for percentages.

D029–D031: compute mean/sample variance exactly as rationals; require N=20 and variance>0. Evaluate signed sqrt((current−mean)^2/variance), rounding **only the final z value** to50 significant digits ROUND_HALF_EVEN (exact zero stays Decimal("0")). Proposed shared helper in `_numeric_bounds.py`: `sqrt_ratio_50(value:Fraction)->Decimal`, for nonnegative values, with exact integer/rational lower/upper bounds refined until they round identically; no binary float or ambient Decimal context. Detect exact rational square roots and half-even ties explicitly rather than waiting forever on an interval straddling a midpoint. A negative sign applies exactly after magnitude rounding; unresolved numerical bounds refuse rather than emit a guessed value.

D032–D036: for each adjacent close pair, reuse unchanged `_log_return._logarithm` to obtain its canonical50-digit half-even Decimal log. Treat each such finite log as an exact rational intermediate; square/sum and divide by exact sum of interval year fractions using Fraction. Apply sqrt_ratio_50 once for final annualised volatility. **This explicitly proposed two-stage numerical convention preserves log-rounding provenance; it does not claim an unrounded irrational result.** Do not silently switch to mean-centred sample SD, log-of-price differences, float annualisation, a second intermediate rounding, or a constant dt times count without validating the interval measures.

Independent plan literals were prepared once using Decimal arithmetic at200-digit precision, outside production, followed by the stated50-digit half-even policy. RV literals use the rounded log L below as an exact Fraction before high-precision square root. This was mathematical planning, not execution of a product test.

| Symbol | Canonical Decimal literal |
| --- | --- |
| Z20 = 3 sqrt(19/20) | `2.9240383034426891720515239599698800897757751701012` |
| L = rounded ln(11/10) | `0.095310179804324860043952123280765092220605365308644` |
| V5m = sqrt(15120/5) × L | `5.2411933614380407513132873039695738036883343009577` |
| V30m = sqrt(15120/30) × L | `2.1397082297976278396691909270830504534270372226234` |
| Vsession = sqrt(252) × L | `1.5130021990505661763533261763515839450637636850162` |
| V5d = sqrt(252/5) × L | `0.67663515343674674807858038377343033264846204377132` |
| V10d = sqrt(252/10) × L | `0.47845330538432369294227349314595528724804013793782` |

Assert exact Decimal tuples, zero tolerance. Keep these literals fixed in authored proof; never obtain expectations from production or rerun numerical research per signal. Z units=`z-score`; RV units=`annualised_volatility`, decimal fraction per square-root trading year.



## 2. Exact proof and budget

D029-PROOF-CONTRACT-SHA256: 9a7978da350aece9b13f14c08241e47fa5f2427b5b775c0158bf4160751e6fe8

Exactly two cases, sole named parameterised function in tests/product/market_measurement_d029/test_volume_zscore.py. Root manifest fixed for this ID; expectations independently authored from literal source operands and exact admitted numerical convention, not production helpers. Worker inspected public M00 setup, refusal reachability, full result/configuration/lineage assertions and durable reopen before sealing. This records worker adequacy under standing delegation, not a fabricated independent review. One admitted semantic RED then minimal source delta, scoped mypy/changed-path Ruff once, one final independent reviewer/sole strict GREEN. No broad/old claims/probes/extra cases or duplicate successful checks. Command python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d029. Preserve raw failures and linked generations after material proof repair.

## 3. Shared boundaries

Reuse existing public window owner/request/occurrence/read seam and RecordState/typed canonical codec/identity. Only commissioned root§5 delta: D026 fixed loader declarations D026–D036 once (D028eight incorporated rows, other new IDsseven); D026/D027 exact named result carriers; D028 separate baseline context; D029 exact rational square-root helper; D032 separate risk context. Old WindowContextV1/dataclass fields, accepted source/proof/generations and canonical bytes stay intact. No new factory/store/schema/codec framework or M00/M01/global CSV mutation. New contexts use existing request.context union. New shaped results qualified inside this ID's existing positive/reopen case.

## 4. Incorporated bytes

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |
| handoff/foundation_implementation/authority/D029_PROOF_CONTRACT.json | 9a7978da350aece9b13f14c08241e47fa5f2427b5b775c0158bf4160751e6fe8 |
