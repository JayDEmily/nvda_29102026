# NVDA Derived Signal families — exhaustive row audit and V2 recommendation

**Status: PROPOSAL FOR PROGRAMME-OWNER REVIEW ONLY. No workbook semantic amendment, accepted M01 catalogue amendment, code change, or module allocation.**

## Decision recommended

Replace the 34 original *descriptive* family groupings with **40 proposed output-responsibility families** in the future `02_Derived Signal Index`, **only after approval**. Add a *separate*, mandatory calculation-responsibility/classification field (market descriptive transformation, statistical/model inference, candidate/portfolio economic measurement, strategy/policy evaluation, retrospective evaluation, or operational control). Do not use Family by itself to assign module ownership or assert that a market calculation is strategy-independent.

The 40 families are proposed for indexing/research navigation, **not** 40 production modules. Every D identifier, authoritative dependency, mathematical definition and M01 responsibility remains unchanged pending separate governance.

## Evidence and procedure

- Repository checkpoint: `eb08239cd99f387ad5c24cf3a67d1133f3ab4c27` on `work/workbook-v2-pass01-guardrails-method-20261014`.
- Original authority reference: `handoff/m01_completion/authority/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`, `Derived Signals!A4:O213`.
- Original workbook SHA-256: `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`.
- Effective current M01 catalogue checked for kernel/context and family DAG: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, SHA-256 `26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803`. The authority index records the supersession of the older accepted companion digest by specifically approved repairs; this hash is not the original digest.
- All 209 source rows were inspected across every original column A:O, not just `Family`; each audit CSV row preserves original ID, worksheet row locator, raw/D dependencies, signal name, calculation concept, window, units, primary purpose and effective kernel/context fields.
- Classification rule: group by what the D output *computes or governs*, not by the input provider alone, bibliography, spreadsheet position or implementation kernel. For ambiguous candidate/model/control outputs, distinguish measurement from decision policy. A signal receives exactly one primary family, but its upstream dependencies are retained separately.
- Each proposed family has a positive definition and exclusion boundary; no new equation is specified in this audit.

## Numerical delta

| Measure | Result |
|---|---:|
| Source D identifiers | 209 |
| Original families | 34 |
| Proposed families | 40 |
| Net family increase | +6 |
| Existing families that must be split | 9 |
| D-IDs presently inside those split families | 76 |
| Minimum D-IDs outside dominant proposed destination of their source family | 29 |
| Proposed destinations combining members from two or more old families | 6 |
| Missing/duplicate D-IDs in proposed classification | 0 |
| Interfamily dependency edges (effective M01 D graph) | 94 |
| Proposed family-level dependency cycles | 0 |

**Interpret the 29 correctly:** for each old family, retain the largest proposed destination as its nominal continuation and count the remaining rows. This is the minimum reassignment measure, **not** the number of changed label strings, and not 29 defects proven in the original research. Most labels are deliberately clarified or renamed. Families and destination groups that merge/split are separately shown below.

## Full proposed family sequence (dependency-consistent)

Sequence satisfies family-level effective D-dependency order. Independently valid branches are ordered deterministically for readability; this list is not the final worksheet/tab plan.

| ID | Family | D count | Positive definition | Excludes |
|---|---|---:|---|---|
| FAM-01 | Time and session semantics | 7 | Canonical/market-local time, trading date, session phase and source vintage state. | Exclude availability/quality scoring and option-expiry arithmetic. |
| FAM-02 | L1 quotes and trade direction | 6 | Best bid/ask prices and size imbalance; trade-sign inference and signed traded volume. | Exclude market-depth reconstruction and order-book event dynamics. |
| FAM-03 | Price path and VWAP | 10 | Underlying price returns, gaps, VWAP, price location and VWAP momentum. | Exclude provider-to-system data-integrity comparison D018. |
| FAM-04 | Volume and trade activity | 4 | Relative volume and standardized trading-volume/trade-rate activity. | Exclude options-chain volume/open-interest analytics. |
| FAM-05 | Realised volatility and range | 8 | Return-based realised volatility, jump variation and bar true range. | Exclude implied volatility surfaces, VIX-family indices and composite regimes. |
| FAM-06 | Trend and reversion features | 2 | Composite trend strength and mean-reversion features of the underlying. | Exclude pure returns, VWAP changes, and volatility estimates. |
| FAM-07 | Rates and funding spreads | 6 | Yield-curve slopes and rate, inflation-expectation and funding-spread changes. | Exclude composite macro latent-factor inference. |
| FAM-08 | Foreign-exchange changes | 4 | Observed broad-dollar and bilateral currency changes over specified windows. | Exclude country equity-index returns and combined international scores. |
| FAM-09 | Volatility indices and regimes | 10 | Cboe volatility-index changes, term slopes and volatility-index-based composite regime score. | Exclude NVDA options IV surface and realised-volatility estimation. |
| FAM-10 | Scheduled-event state | 4 | Time-to-event, release surprise, event importance and active-event-window measures. | Exclude prospective trade gating, candidate utility and strategy decisions. |
| FAM-11 | International equity context | 5 | Non-US index returns and aggregated international overnight risk condition. | Exclude FX-only transformations already assigned to FX. |
| FAM-12 | US market and cross-market breadth | 5 | US market proxy returns, NVDA-market/sector correlations, return dispersion and monitored-basket breadth. | Exclude sector-relative/rotation composite calculations. |
| FAM-13 | Technology and semiconductor sector | 5 | Sector ETF returns, technology/semiconductor relative strength and rotation state. | Exclude NVDA-specific residual return or estimated beta. |
| FAM-14 | NVDA factor-relative state | 5 | NVDA underlying return, conditional market/sector beta and residual stock-specific return. | Exclude sector ETF or broad index return series. |
| FAM-15 | Option expiry and moneyness | 5 | Option time-to-expiry, spot/log moneyness and standard delta-category placement. | Exclude quoted premiums, spreads and implied volatility. |
| FAM-16 | Option quote liquidity | 4 | Option premium midpoint, spread, displayed nearby depth and combined liquidity score. | Exclude full book reconstruction and execution-price action. |
| FAM-17 | Implied-volatility surface and fit | 15 | Quoted implied-volatility measures, changes, term structure, skew, smile, fit error and IV rank/percentile. | Exclude realised-vol comparisons and probability distributions. |
| FAM-18 | Data quality and reconciliation | 5 | Staleness, required-field coverage, cross-source temporal alignment, independent VWAP cross-check and composite data quality. | Exclude market price/return and fitted IV-surface error. |
| FAM-19 | Option-implied move proxy | 2 | ATM straddle mid-premium and premium-to-spot implied movement proxy. | Exclude calibrated probability densities/tail probabilities. |
| FAM-20 | Option probability distributions | 4 | Risk-neutral density and tails; conditional physical return density. | Exclude straddle premium proxies and comparisons between distributions. |
| FAM-21 | IV and probability relative value | 3 | Implied-versus-realised volatility gaps and risk-neutral versus physical distribution disagreement. | Exclude generating the underlying probability distributions. |
| FAM-22 | Option volume and open interest | 6 | Option volume/OI ratios, abnormal activity, call/put mixes, OI change and OI concentration. | Exclude signed aggressive option order flow and dealer-side inference. |
| FAM-23 | Signed option order flow | 3 | Signed option trades and aggregated flow by delta bucket or expiry. | Exclude public-volume/OI measures without signed initiator information. |
| FAM-24 | Inferred dealer exposures | 6 | Dealer-position-assumption-dependent Greek OI proxies, gamma zones/flips and hedge-pressure scenarios. | Exclude directly observed option volume/OI and measured account holdings. |
| FAM-25 | L2 book depth and dynamics | 12 | SMART/direct book depth, imbalance, microprice, dynamics, venue structure and OFI. | Exclude top-of-book best-quote arithmetic and candidate order pricing. |
| FAM-26 | Latent macro risk factors | 5 | Growth, inflation, policy, funding and global latent market-factor synthesis. | Exclude direct rate/FX transformations and probability vectors. |
| FAM-27 | Probabilistic regime inference | 3 | Estimated probabilities of dominant market drivers and NVDA underlying/options regimes. | Exclude deterministic source summaries and decision gate outputs. |
| FAM-28 | State assembly and coherence | 4 | Assembled market-state vector, redundancy and signal conflict measures, and state identifiability/readiness. | Exclude source quality tests and explicit allow/no-trade policy decisions. |
| FAM-29 | Joint scenario generation | 1 | Probability-weighted conditional joint future-market scenario paths. | Exclude candidate valuation and structure-specific scenario stress matrices. |
| FAM-30 | Candidate valuation and risk metrics | 8 | Candidate slippage and total execution-cost estimates, expected P&L, tail risk, aggregate Greeks, payoff loss, breakevens and stress losses. | Exclude utility preferences, ranked selection, allowable risk limits and order placement decisions. |
| FAM-31 | Candidate decision scoring and selection | 7 | Uncertainty/utility penalties, candidate utility, trade/no-trade eligibility and exposure/strike/expiry preference scoring/selection. | Exclude purely measured candidate loss, market-state identifiability and permissible position risk. |
| FAM-32 | Risk limits and position sizing | 2 | Permissible capital/tail/concentration risk bounds and candidate position sizing. | Exclude raw account balance, observed Greeks and action-state logic. |
| FAM-33 | Pretrade execution and order pricing | 2 | Refreshed net entry edge and proposed limit-price target for intended execution. | Exclude predicted transaction costs, observed fills and realised costs. |
| FAM-34 | Execution outcomes and realised costs | 3 | Post-submission fill slippage/completion and measured realised transaction costs. | Exclude proposed limit prices and prospective cost estimates. |
| FAM-35 | Live portfolio exposures and P&L | 5 | Observed live portfolio Greek aggregates and portfolio realised/unrealised P&L state. | Exclude action policy, hedging decisions and retrospective attribution. |
| FAM-36 | Live position assessment and decisions | 7 | Entry-state comparison, invalidation, continuation/modification/exit valuation, hedge needs and hold/modify/exit decision. | Exclude measured live portfolio Greeks and post-trade realised attribution. |
| FAM-37 | Post-trade P&L attribution | 6 | Breakdown of observed position P&L by delta/gamma/vega/theta/skew and residual. | Exclude decision/process quality and alternative-path counterfactuals. |
| FAM-38 | Decision review and counterfactuals | 3 | Decision-process quality, no-trade/alternative counterfactuals and out-of-sample decision performance. | Exclude raw P&L attribution and probabilistic calibration measures. |
| FAM-39 | Forecast and signal validation | 6 | Incremental signal information, probability calibration/proper scores, drift and signal disposition. | Exclude realised position P&L attribution and next-update scheduling. |
| FAM-40 | Observation and recalculation scheduling | 1 | The event or schedule trigger for the next observe/calculate iteration. | Exclude market-data timestamps and financial signal transformations. |

## Exact old-to-proposed crosswalk: all 34 originals

| Original family (count) | Proposed destinations (exact D IDs) |
|---|---|
| Time & data quality (10) | **Time and session semantics** (7): D001, D002, D003, D004, D005, D009, D010; **Data quality and reconciliation** (3): D006, D007, D008 |
| Market microstructure (6) | **L1 quotes and trade direction** (6): D011, D012, D013, D014, D015, D016 |
| Underlying/price path (11) | **Price path and VWAP** (10): D017, D019, D020, D021, D022, D023, D024, D025, D026, D027; **Data quality and reconciliation** (1): D018 |
| Volume/activity (4) | **Volume and trade activity** (4): D028, D029, D030, D031 |
| Volatility (8) | **Realised volatility and range** (8): D032, D033, D034, D035, D036, D037, D038, D039 |
| Regime features (2) | **Trend and reversion features** (2): D040, D041 |
| Macro/rates (6) | **Rates and funding spreads** (6): D042, D043, D044, D045, D046, D047 |
| Macro/FX (4) | **Foreign-exchange changes** (4): D048, D049, D050, D051 |
| Volatility complex (10) | **Volatility indices and regimes** (10): D052, D053, D054, D055, D056, D057, D058, D059, D060, D061 |
| Macro/events (4) | **Scheduled-event state** (4): D062, D063, D064, D065 |
| International (5) | **International equity context** (5): D066, D067, D068, D069, D070 |
| US market (4) | **US market and cross-market breadth** (4): D071, D072, D082, D083 |
| Sector (5) | **Technology and semiconductor sector** (5): D073, D074, D076, D077, D084 |
| NVDA state (5) | **NVDA factor-relative state** (5): D075, D078, D079, D080, D081 |
| Options contract (5) | **Option expiry and moneyness** (5): D085, D086, D089, D090, D091 |
| Options liquidity (4) | **Option quote liquidity** (4): D087, D088, D131, D132 |
| Options surface (15) | **Implied-volatility surface and fit** (15): D092, D093, D094, D095, D096, D097, D098, D099, D100, D101, D102, D103, D104, D105, D106 |
| Options relative value (3) | **IV and probability relative value** (3): D107, D108, D115 |
| Options distribution (6) | **Option-implied move proxy** (2): D109, D110; **Option probability distributions** (4): D111, D112, D113, D114 |
| Options activity (6) | **Option volume and open interest** (6): D116, D117, D118, D119, D123, D124 |
| Options flow (3) | **Signed option order flow** (3): D120, D121, D122 |
| Dealer positioning (6) | **Inferred dealer exposures** (6): D125, D126, D127, D128, D129, D130 |
| Execution (5) | **Candidate valuation and risk metrics** (1): D133; **Pretrade execution and order pricing** (2): D177, D178; **Execution outcomes and realised costs** (2): D179, D180 |
| L2 microstructure (12) | **L2 book depth and dynamics** (12): D134, D135, D136, D137, D138, D139, D140, D141, D142, D143, D144, D145 |
| State synthesis (14) | **US market and cross-market breadth** (1): D151; **Data quality and reconciliation** (1): D158; **Latent macro risk factors** (5): D146, D147, D148, D149, D150; **Probabilistic regime inference** (3): D152, D153, D154; **State assembly and coherence** (4): D155, D156, D157, D159 |
| Decision/scenarios (8) | **Joint scenario generation** (1): D160; **Candidate valuation and risk metrics** (3): D161, D162, D164; **Candidate decision scoring and selection** (4): D163, D165, D166, D167 |
| Structure selection (6) | **Candidate valuation and risk metrics** (3): D168, D169, D170; **Candidate decision scoring and selection** (3): D171, D172, D173 |
| Risk/stress (1) | **Candidate valuation and risk metrics** (1): D174 |
| Risk/sizing (2) | **Risk limits and position sizing** (2): D175, D176 |
| Live risk (5) | **Live portfolio exposures and P&L** (5): D181, D182, D183, D184, D185 |
| Live control (7) | **Live position assessment and decisions** (7): D186, D187, D188, D189, D190, D191, D192 |
| Post-trade (9) | **Execution outcomes and realised costs** (1): D193; **Post-trade P&L attribution** (6): D194, D195, D196, D197, D198, D199; **Decision review and counterfactuals** (2): D200, D201 |
| Learning (7) | **Decision review and counterfactuals** (1): D206; **Forecast and signal validation** (6): D202, D203, D204, D205, D207, D208 |
| Control loop (1) | **Observation and recalculation scheduling** (1): D209 |

## Nine original families requiring structural split

**Time & data quality — 10 D-signals:** Time and session semantics (7: D001, D002, D003, D004, D005, D009, D010); Data quality and reconciliation (3: D006, D007, D008).

**Underlying/price path — 11 D-signals:** Price path and VWAP (10: D017, D019, D020, D021, D022, D023, D024, D025, D026, D027); Data quality and reconciliation (1: D018).

**Options distribution — 6 D-signals:** Option-implied move proxy (2: D109, D110); Option probability distributions (4: D111, D112, D113, D114).

**Execution — 5 D-signals:** Candidate valuation and risk metrics (1: D133); Pretrade execution and order pricing (2: D177, D178); Execution outcomes and realised costs (2: D179, D180).

**State synthesis — 14 D-signals:** US market and cross-market breadth (1: D151); Data quality and reconciliation (1: D158); Latent macro risk factors (5: D146, D147, D148, D149, D150); Probabilistic regime inference (3: D152, D153, D154); State assembly and coherence (4: D155, D156, D157, D159).

**Decision/scenarios — 8 D-signals:** Joint scenario generation (1: D160); Candidate valuation and risk metrics (3: D161, D162, D164); Candidate decision scoring and selection (4: D163, D165, D166, D167).

**Structure selection — 6 D-signals:** Candidate valuation and risk metrics (3: D168, D169, D170); Candidate decision scoring and selection (3: D171, D172, D173).

**Post-trade — 9 D-signals:** Execution outcomes and realised costs (1: D193); Post-trade P&L attribution (6: D194, D195, D196, D197, D198, D199); Decision review and counterfactuals (2: D200, D201).

**Learning — 7 D-signals:** Decision review and counterfactuals (1: D206); Forecast and signal validation (6: D202, D203, D204, D205, D207, D208).

## Why the source grouping is insufficient

- `D018` measures disagreement between vendor VWAP and computed VWAP (quality reconciliation), not underlying price momentum: move from `Underlying/price path` to `Data quality and reconciliation`.
- `D109–D110` produce an ATM straddle premium/scale proxy; `D111–D114` produce estimated probability densities/tail probabilities. Premium and probability density are not the same kind of output: split `Options distribution`.
- `D133` predicts prospective execution slippage; `D179–D180` measure realised fill state; `D177–D178` choose entry/limit parameters. Split `Execution` by measure versus action versus observed result.
- `D146–D150` compute macro latent factors, `D152–D154` infer state probabilities, `D155–D157` assemble/compare state, `D158` checks data quality and `D159` assesses identifiability; `D151` measures breadth. One `State synthesis` label obscures these separate contracts.
- `D160` generates joint conditional market scenarios, `D161–D162/D164` measure candidate outcomes and costs, while `D163/D165–D167` score or select actions. Split `Decision/scenarios` by function.
- `D168–D170` aggregate/measure contractual structure exposures or payoffs; `D171–D173` rank strike/expiry alternatives. Split `Structure selection` into measurement versus decision scoring.
- `D193` measures realised transaction cost; `D194–D199` attribute P&L; `D200–D201` review process quality and counterfactual outcomes. Split `Post-trade`.
- `D206` is out-of-sample performance evaluation of decisions and fits better with `D200–D201` than with forecast probability/signal diagnostics `D202–D205/D207–D208`.
- Retain `D125–D130` as **inferred dealer** exposures; public OI does not directly identify dealer positions. This is a crucial modelling qualifier despite no need to split its source family.

## Important boundary and next approval

The proposed family count is an indexing recommendation, not a proof of market-only calculation status, an independent test for each D-signal or module allocation. In particular a statistical probability density, a dealer-position estimate, a capital limit and a market return cannot be treated as the same responsibility merely because each produces a numerical result. After approval, apply this taxonomy as **new proposed V2 columns**, preserving original V1 family text separately. Audit the classification-role dimension independently; do not collapse this into 40 untested standalone modules.

For full details see the accompanying 209-row audit CSV, 40-family definitions CSV, and verification summary JSON. No V2 workbook or repository production file has been modified by the classification itself.
