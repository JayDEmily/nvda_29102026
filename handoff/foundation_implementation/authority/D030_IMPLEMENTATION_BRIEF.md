# D030 — exact controlled trade-rate baseline implementation

ACCEPTED_FOR_IMPLEMENTATION under owner commission 23 October 2026. This authored bounded contract applies only to the controlled M02 synthetic trade-rate profile, not live-provider certification.

## 1. Meaning and case boundaries

R062 current16 trades/minute and twenty consecutive prior rate observations 8,12 repeated ten times; exact sample SD 80/19 gives Z20. All twenty prior R062 rates8 yields zero sample SD and must refuse.

Definition `D030-TRADE-RATE-ZSCORE-1`, parameter `mmt-trade-rate-zscore-20sessions-50d/1`, selection `mmt-trade-rate-zscore-20sessions-selection/1`, R062 native `activity.trades_per_minute`, units trades/minute, exact bucket and ordered twenty sessions. Scalar Decimal z-score 50 digits. No D predecessors.

### 4.2 Baseline calendar and mappings

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



D029–D031: compute mean/sample variance exactly as rationals; require N=20 and variance>0. Evaluate signed sqrt((current−mean)^2/variance), rounding **only the final z value** to50 significant digits ROUND_HALF_EVEN (exact zero stays Decimal("0")). Proposed shared helper in `_numeric_bounds.py`: `sqrt_ratio_50(value:Fraction)->Decimal`, for nonnegative values, with exact integer/rational lower/upper bounds refined until they round identically; no binary float or ambient Decimal context. Detect exact rational square roots and half-even ties explicitly rather than waiting forever on an interval straddling a midpoint. A negative sign applies exactly after magnitude rounding; unresolved numerical bounds refuse rather than emit a guessed value.



## 2. Two-case admission

Contract SHA256: `33f6465477bd41ff7feb5508e4964cf5094279a3c7a38f0d93b576f6e7a3d7ef`. Exactly one named parameterised two-case function in `tests/product/market_measurement_d030/test_trade_rate_zscore.py`. Case one asserts the fixed Z20 Decimal literal, full M00 lineage, identity and durable SQLite reopen. Case two proves refusal on zero sample SD with all twenty baseline entries otherwise lawful. No extra proof cases. Independent final review required by the active ExecPlan.

## 3. In-scope change

Extend `_volume_baseline.BRIEFS` for this identity, reuse preapproved mapping/configuration/sample-SD/root paths without modifying earlier accepted IDs; add exactly the public test and immutable product proof admission. Native `SRC-VOLUME`/projection certification stays held.

## 4. Incorporated bytes

D030-PROOF-CONTRACT-SHA256: cd5c8bff830e96e7da8bc67329bd1af3bcebd15e1e1005865be3d71f80c39170

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |
| handoff/foundation_implementation/authority/D030_PROOF_CONTRACT.json | cd5c8bff830e96e7da8bc67329bd1af3bcebd15e1e1005865be3d71f80c39170 |
