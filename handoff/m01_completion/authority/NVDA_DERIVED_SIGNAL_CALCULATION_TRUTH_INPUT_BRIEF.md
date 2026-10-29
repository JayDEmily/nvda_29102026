# Derived Signal Calculation Truth — implementation-ready input brief

Status: **FINAL REPAIRED CANDIDATE FOR INDEPENDENT REVIEW — NOT ACCEPTED IMPLEMENTATION AUTHORITY**.

This is an external successor-brief draft only. It does not modify the terminal repository, allocate a current architecture identifier, create a successor execution cycle or authorise product code. If accepted, the exact accepted bytes enter the existing Implementation Admission process. Numeric `M` allocation remains an architecture-admission result rather than a choice made by this brief.

## 1. Own one bounded meaning: deterministic Derived Signal calculation truth

Create one runtime semantic owner for **Derived Signal Calculation Truth**.

Its responsibility is: given lawfully available M00 Raw Signal facts exposed through an exact typed raw-value projection, prior Derived Signal facts, and exact immutable calculation/configuration/context versions, calculate and durably preserve the corresponding canonical `Dxxx` result with complete lineage.

The ownership test is:

> **Can this `Dxxx` value be deterministically calculated from M00 Raw Signal facts, optionally through other `Dxxx` calculations, once the required history and explicit versioned calculation/configuration/context inputs exist?**

If yes, it belongs to this capability. Legacy `Family`, `Required steps` and `Primary purpose/output` labels do not allocate ownership.

The capability calculates facts. It does not ingest providers, redefine raw truth, place orders, mutate accounts or perform external effects.

## 2. Authority package and workbook reference

Implementation Authority Ingress still accepts **one exact brief byte object**. For this capability, that object is:

- `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` — the single implementation-ready brief supplied to ingress and hash-bound there by SHA-256.

This brief normatively incorporates one exact companion catalogue by content digest:

- `NVDA_DERIVED_SIGNAL_CATALOGUE.csv` — SHA-256 `63bc1b776fc8fa8ba82eb3c9b16916f295c9ec3d480a5a068937c2f25146f5f5` — the complete `D001`–`D209` row catalogue, including each row's canonical vocabulary, authoritative raw/derived dependencies, kernel binding, parameter profile, explicit typed contexts and workbook locator.

A different CSV byte sequence is **not** the companion catalogue incorporated by this brief, even if it has the same filename or sits in the same Git tree. Git history/commit/tree provide provenance but do not substitute for the exact companion-content binding above. Before architecture projection or implementation work, the worker must verify that the supplied companion CSV bytes match the digest above; missing or mismatched companion bytes are a fail-closed authority defect.

Reference workbook:

`NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx` — SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`.

The `Derived Signals` worksheet supplies the canonical `D001`–`D209` identifiers and the source row-level human name, symbolic label, calculation concept, parameter/window, units, cadence and applicable universe. The workbook's `Raw Signals` worksheet is source evidence for provider/native-field provenance.

The workbook is **reference evidence, not implementation authority**. The exact hash-bound companion CSV is the single authoritative per-signal binding surface incorporated by this brief. Where that CSV or this Markdown brief defines, clarifies or supersedes a workbook dependency, equation, convention, parameter rule, output shape or sufficiency rule, this brief plus its exact incorporated CSV governs. `Family`, `Required steps` and `Primary purpose/output` remain descriptive legacy metadata only and do not allocate architecture ownership.

Any calculation-owner consumption of an `Rxxx` value still requires the typed projection/mapping law in clause 9; a catalogue ID attached to an M00 observation is not, by itself, a field-level value binding.

## 3. Admit D001–D209 as the calculation namespace, subject to sufficiency

Mechanical inspection of the exact workbook establishes:

- 209 D rows;
- all workbook `Rxxx` references resolve within `R001`–`R323`;
- all workbook `Dxxx` references resolve within `D001`–`D209`;
- the workbook-derived D dependency graph is acyclic;
- 206 rows have at least one direct or transitive raw-signal path before the brief resolves the three explicit dependency gaps;
- D007, D204 and D205 have no explicit workbook R/D dependencies.

A D identity being admitted does not mean a result always exists. The result exists only when its full inputs, history, definition and parameter/context versions exist and satisfy the row's law.

## 4. Resolve D007, D204 and D205 explicitly

### D007 — Required-field completeness

For immutable `RequiredFieldPolicy` containing `N > 0` distinct requirements:

`D007 = satisfied_required_count / N`.

Each requirement contributes at most once; duplicate observations do not inflate the numerator. Empty policy is invalid.

### D204 — Brier score

For resolved binary forecast/outcome pairs `(p_i, y_i)`:

`D204 = (1/N) * Σ(p_i - y_i)^2`, with `0 <= p_i <= 1`, `y_i ∈ {0,1}`, `N >= 1`.

### D205 — log score / negative log likelihood

Discrete/categorical: `-ln p(realised_outcome)`.

Continuous density: `-ln f(realised_outcome)` under the exact declared density convention.

Batch score is arithmetic mean. Zero realised probability/density is infinite loss; no silent epsilon clipping.

## 5. Fix the calculation kernels so implementation does not choose the mathematics

Every admitted `Dxxx` is bound to exactly one primary calculation kernel by `NVDA_DERIVED_SIGNAL_CATALOGUE.csv`. The workbook description remains useful reference context, but the kernel rules below plus any row-specific clarification in this brief govern.

A versioned parameter set may supply numbers, thresholds, weights, baskets, windows, grids, coefficients and calendars. It may not change the kernel's mathematical meaning. A change of kernel, estimator family, sign convention, return convention, annualisation convention or result interpretation is a calculation-definition version change.

### K01_TIME — temporal conversion, session and expiry calculations

Use timezone-aware temporal arithmetic only.

- `D001`: emit UTC only when the M00 temporal kind is `true_instant`; parse the provider-native timestamp with its supplied offset/timezone and convert the same instant to UTC. `date_only` and `receipt_only` do not produce D001.
- `D002`: emit one typed age result at the calculation knowledge cutoff. For `true_instant`, `basis=source_event` and `age_seconds = knowledge_cutoff_utc - D001`; for `receipt_only`, `basis=collector_receipt` and `age_seconds = knowledge_cutoff_utc - received_ts_utc`. `date_only` does not produce a seconds-valued D002 because an instant must not be invented from a date. Negative age under the chosen basis is invalid rather than clipped to zero.
- `D003`: convert D001 to the configured exchange IANA timezone without changing the instant.
- `D004`: obtain exchange-local trading date from the configured session calendar, including overnight/session boundary rules.
- `D005`: classify the local instant into an ordered, non-overlapping versioned session-phase schedule. A phase is absent if no configured phase contains the instant.
- `D009`: classify each visible macro vintage into one mutually exclusive category at the calculation knowledge cutoff: `initial` when it is the first published vintage; `latest_known_at_cutoff` when it is the newest visible non-initial vintage; otherwise `revised`. If only the initial vintage is visible, it remains `initial`. The occurrence also preserves the applicable vintage/realtime period and cutoff; `latest` is never a timeless claim.
- `D010`: true only when the configured market calendar says the instrument is open and the observation lies in the configured liquid/RTH phase; otherwise false when the state is knowable.
- `D062`: for the earliest relevant scheduled event strictly after the calculation as-of instant, return `{seconds=next_event_ts-as_of_ts, minutes=seconds/60}`; seconds is the canonical stored duration and minutes is an exact representation derived from it.
- `D085`: whole calendar-day difference between option expiry date and exchange-local trading date; negative values are invalid for a live contract calculation.
- `D086`: ACT/365F year fraction from D001 to the configured expiry instant. Expiry instant/session convention is versioned by instrument/calendar policy.

### K02_ALGEBRA — exact algebra, aggregation and deterministic transforms

Use the algebra stated by the row description, with these universal conventions:

- all numeric inputs first pass the explicit raw-value/unit projection law in clause 9; no kernel infers scale from magnitude;
- canonical rates/yields and volatilities are decimal fractions for arithmetic (for example `0.0525` means 5.25% and `0.30` means 30-vol);
- addition/subtraction preserves compatible units;
- ratios require a strictly non-zero denominator; otherwise no occurrence;
- percentage outputs are multiplied by `100`; basis-point outputs by `10,000`; volatility-point outputs are decimal-volatility differences multiplied by `100`;
- weighted sums retain the exact member set and weights in lineage;
- when a row's legacy units list more than one representation, the canonical output is a typed structure containing each named representation rather than an implementation-selected one;
- concentration shares are decimal fractions in `[0,1]` that sum to 1 before HHI is calculated; `HHI = Σ share_i²` is therefore on a canonical `0–1` scale;
- an expected/pre-trade cost calculation may consume an immutable fee schedule and intended order/candidate context, but it must not consume a post-trade execution-cost fact that does not yet exist at the decision cutoff.

Fixed examples that remove material ambiguity:

- `D011 = (bid + ask) / 2`.
- `D012 = ask - bid`.
- `D013 = 100 * D012 / D011`.
- `D014 = (bid_size - ask_size) / (bid_size + ask_size)`.
- `D017 = Σ(price_i * size_i) / Σ(size_i)` over the admitted session/anchor window.
- `D018` returns `{price_difference = provider_vwap - D017, bps_difference = 10000 * price_difference / D017}`.
- `D025 = (last - session_low) / (session_high - session_low)`.
- `D042 = 100 * (yield_10y - yield_2y)` and `D043 = 100 * (yield_10y - yield_3m)`, returning percentage-point slopes from canonical decimal-yield inputs.
- `D047 = 10000 * (SOFR - effective_fed_funds)`, returning basis points from canonical decimal-rate inputs.
- `D057` returns `{point_difference=VIX1D-VIX9D, ratio=VIX1D/VIX9D}`; `D058` returns `{point_difference=VIX9D-VIX, ratio=VIX9D/VIX}`; `D059` returns `{point_difference=VIX-VIX3M, ratio=VIX/VIX3M}`. The second value in each pair must be non-zero.
- `D060 = VVIX / VIX`.
- `D076 = QQQ_return - broad_market_return`.
- `D077 = mean(SMH_return, SOXX_return) - QQQ_return` when both semiconductor proxies are present; a parameterised single-proxy mode must name the proxy.
- `D087 = (option_bid + option_ask) / 2`.
- `D088 = 100 * (option_ask - option_bid) / D087`; this brief adds direct `R034/R035` option bid/ask dependency because midpoint alone is insufficient to reconstruct spread.
- `D089 = strike / spot`.
- `D090 = ln(strike / spot)`.
- `D092 = (bid_iv + ask_iv) / 2` in canonical decimal-volatility units.
- `D093 = 100 * (ask_iv - bid_iv)` in volatility points.
- `D097 = 100 * (ATM_IV_2 - ATM_IV_1) / (expiry_day_2 - expiry_day_1)` using two parameter-selected expiries and returning volatility points per calendar day; equal expiry days are invalid.
- `D098` uses three ordered expiries `(d1,iv1)`, `(d2,iv2)`, `(d3,iv3)` and returns the non-uniform-grid second divided difference in volatility points/day²: `2 * (100*(iv3-iv2)/(d3-d2) - 100*(iv2-iv1)/(d2-d1)) / (d3-d1)`.
- `D099 = 100 * (put_IV_25delta - call_IV_25delta)`.
- `D100 = 100 * (put_IV_10delta - call_IV_10delta)`.
- `D101 = 100 * (put_IV_25delta + call_IV_25delta - 2 * ATM_IV)` at one expiry.
- `D107 = 100 * (D096 - D035)` and `D108 = 100 * (D096 - D036)` after both inputs are aligned to canonical decimal annualised-volatility units.
- `D109 = ATM_call_mid + ATM_put_mid`.
- `D110 = 100 * D109 / spot`.
- `D116 = option_volume / open_interest`.
- `D118 = aggregate_call_volume / aggregate_put_volume`.
- `D119 = aggregate_call_OI / aggregate_put_OI`.
- `D123 = current_OI - prior_official_OI`.
- `D131`, `D134`, `D135` are exact sums of displayed size inside the configured depth selection after deterministic book reconstruction. For event-driven L2 books, state is reconstructed by subject/source and side in stable receipt/ingestion order using the provider operation and row-position semantics; insert/update/delete events are applied before the selected depth sum is taken.
- `D136 = (bid_depth - ask_depth) / (bid_depth + ask_depth)`.
- `D137 = (ask_price * bid_size + bid_price * ask_size) / (bid_size + ask_size)`.
- `D143` is Herfindahl concentration `Σ share_i²` of displayed direct depth by venue/market maker using **absolute displayed-size shares** on the canonical `0–1` HHI scale. The direct book is reconstructed from position, operation, side, price, size and venue/market-maker fields before concentration is calculated.
- `D144` is a structured matched-book difference containing SMART-minus-direct price and depth differences at the admitted matched levels. Both books are reconstructed from their full position/operation/side/price/size event streams; matching uses the versioned subject, side, price/level and maximum-skew rules rather than query order.
- `D151` returns three separately preserved breadth fractions over the exact monitored basket: `positive_return_fraction` uses current/last versus the current session open, `above_vwap_fraction` uses current/last versus current session VWAP, and `above_prior_close_fraction` uses current/last versus prior official close. Each denominator is the count (or configured weight sum) of members with all inputs required for that component; missing members are not silently treated as false.
- `D164` is the **pre-trade** sum of D133 expected spread/slippage cost plus deterministic commissions/fees and declared multi-leg incremental costs from the exact immutable `ExecutionCostScheduleVersion` and intended order/candidate context. Realised post-trade commission R233 is not an input to D164. Each expected-cost component is retained.
- `D168` is the quantity- and multiplier-weighted sum of leg delta, gamma, vega and theta, returned as a Greek vector.
- `D170` returns every real terminal underlying-price root where total structure payoff net of premium equals zero.
- `D179 = side_sign * (fill_price - benchmark_price)` with buy `+1`, sell `-1`; bps form is `10000 * price_slippage / benchmark_price`.
- `D180 = filled_quantity / (filled_quantity + remaining_quantity)` from the matched order-status state; denominator must be positive.
- `D181`–`D184` are quantity × multiplier × current per-contract Greek sums across the admitted live position set.
- `D185` is a structured P&L state preserving realised, unrealised and total components separately; it must not collapse them.
- `D190 = best_modify_value - hold_value`, where `hold_value` is the D188 hold-utility value and `best_modify_value` is the greatest lawful D165 value among modification-eligible candidate identities enumerated by the exact `CandidateSetContext`. D165 already includes that candidate's D164 execution cost, so D190 does not subtract D164 again. Equal candidate values use the immutable candidate order from `CandidateSetContext`; if no lawful modification candidate exists, no D190 occurrence is emitted.
- `D191` is executable liquidation value for the exact position context using the D133 expected executable fill price for the liquidation side/size/multiplier, less only the non-slippage commissions/fees component retained in D164. D133 slippage is already embedded in the expected fill price and must not be subtracted a second time.
- `D193` is realised execution cost equal to commissions/fees plus signed slippage × the matched executed quantity × multiplier; per-fill quantity is taken from the exact execution record, not inferred from cumulative order state.
- `D199 = observed_total_PnL - (D194 + D195 + D196 + D197 + D198) - cost_term`, where `cost_term = D193` only when the exact `PnLConventionVersion` states that `observed_total_PnL` is gross of those execution costs; otherwise `cost_term = 0`. `observed_total_PnL` is the convention-consistent realised+unrealised provider P&L state.

### K03_CHANGE_RETURN — returns, rates of change and matched changes

For price-return rows use log return `ln(x_t / x_ref)` unless the row explicitly says `percent change`. For `percent change`, use `100 * (x_t / x_ref - 1)`. For point/basis-point changes use simple difference.

The reference observation must be the latest eligible observation at or before the exact comparison anchor; never look forward to fill a missing anchor.

- `D019`, `D020`, `D021` use one-, five- and thirty-minute aligned close anchors.
- `D022` uses session open to current/last; `D023` uses prior close to current pre-market/open.
- `D024` converts D019/D020/D021 to return-per-minute rates `q1=D019/1`, `q5=D020/5`, `q30=D021/30` and returns `{q1,q5,q30,accel_1v5=q1-q5,accel_5v30=q5-q30}`.
- `D026` is canonicalised by this brief to `{price_difference = current - VWAP, percent_difference = 100*(current/VWAP - 1)}`. The legacy optional `sigma` representation is not part of D026 because no realised-volatility dependency is declared; a volatility-standardised deviation requires a separately declared derived dependency/version.
- `D027` returns both `{price_per_minute=(VWAP_t-VWAP_ref)/elapsed_minutes, percent_per_minute=100*(VWAP_t/VWAP_ref-1)/elapsed_minutes}` over the five-minute anchor.
- `D044`–`D046` are `10000 * (rate_t - rate_ref)` basis-point changes from canonical decimal-rate inputs over the selected 1d/5d anchor.
- `D048`–`D051` are percent changes over the selected 1d/5d/20d anchor.
- `D052`–`D056` return `{point_change, percent_change}` over the selected horizon.
- `D066`–`D075` use log return over the row's stated daily/overnight/session anchor.
- `D094`, `D095` are `100 * (IV_t - IV_ref)` matched-contract/matched-bucket changes in volatility points.
- `D103 = 100 * mean(IV_current_i - IV_prior_i)` across the exact matched surface grid common to both snapshots; the matched member set is preserved and no unmatched point is silently substituted.
- `D104` is current skew measure minus the corresponding prior skew measure, using D099/D100 and the selected horizon.

### K04_STANDARDISE_RANK — baselines, z-scores, rank and percentile

For baseline sample `x_1…x_N`, use sample standard deviation `s` with `N-1` denominator.

`z = (x_current - mean(x_1…x_N)) / s`.

Require `N >= 2` and `s > 0`; otherwise no z-score occurrence. For historical-baseline rows (`D028`–`D031`, `D063`, `D105`, `D106`, `D117`), every baseline observation must be strictly prior to the current observation/forecast origin and visible by the knowledge cutoff; the current observation is never part of its own baseline. `D083` is the separate contemporaneous cross-sectional case and uses only the exact current basket admitted by `P_CROSS_SECTION`. Accordingly, the companion CSV binds `P_BASELINE` only to D028–D031/D063/D105/D106/D117 and binds `P_CROSS_SECTION` only to D083; the two profiles are not jointly required by K04 rows.

- `D028` is current cumulative/session volume divided by the historical mean volume at the same elapsed session fraction.
- `D029`–`D031` and `D117` use the z-score law above with the parameter-selected historical window and matching time-of-day/contract bucket.
- For `D063`, let `s_t = actual_t - consensus_t`. Over the release-specific historical surprise sample `s_1…s_N`, `D063 = (s_current - mean(s_1…s_N)) / sample_sd(s_1…s_N)`. Require `N >= 2` and non-zero sample standard deviation.
- `D105 = 100 * (current - min_1y) / (max_1y - min_1y)`; no occurrence when the one-year range is zero.
- `D106 = 100 * (count(x_i < current) + 0.5*count(x_i = current)) / N`.
- `D083` uses sample standard deviation across the parameter-selected contemporaneous basket.

### K05_REALIZED_RISK — realised volatility, jump variation and ATR

Construct ordered log returns `r_i = ln(P_i/P_{i-1})` from admitted closes. Let `Δτ_i` be each interval's trading-time fraction of a year under the applicable market calendar.

For `D032`–`D037`:

`annualised_RV = sqrt( Σ r_i² / Σ Δτ_i )`.

The configured window must be complete enough to satisfy the named horizon; a five-day row does not emit after fewer than five complete admitted trading days.

`D038` uses bipower-variation jump separation on the admitted high-frequency return series:

- realised variation `RV = Σ r_i²`;
- bipower variation `BV = (π/2) * Σ_{i=2..N} |r_i| |r_{i-1}|`;
- jump variation `JV = max(RV - BV, 0)`.

`D039` uses true range `TR_i = max(high_i-low_i, |high_i-prev_close_i|, |low_i-prev_close_i|)` and returns the arithmetic mean over the parameter-selected number of five-minute bars. The bar count is mandatory versioned configuration.

### K06_REGRESSION_DEPENDENCE — beta, residual, slope and dependence matrices

Use ordinary least squares with intercept unless the row-specific parameter set explicitly declares a different accepted calculation-definition version. The default regression definition is not silently switchable to robust, ridge, lasso or machine-learning regression.

- `D078`–`D081` share one coherent aligned factor model rather than coefficients from three incompatible regressions. Over the parameter-selected history/state subset fit `D075 = α + β_market*D071 + β_tech*D076 + β_semi*D077 + ε`, where D075 is the dependent NVDA return, D076 is technology relative to broad market and D077 is semiconductor relative to technology. D079, D080 and D081 therefore each require D075 as well as D071/D076/D077 to identify the same fitted model.
- `D079 = β_market`, `D080 = β_tech`, and `D081 = β_semi`; the common model intercept, sample definition and fit identity are retained in each occurrence lineage.
- `D078 = D075 - (α + D079*D071 + D080*D076 + D081*D077)` using coefficient occurrences from that same fitted-model identity and aligned current factor observations. Mixing coefficients from different model fits is invalid.
- `D082`: Pearson correlation matrix over the aligned parameter-selected return window; pairwise missing data are not silently used—rows must satisfy the common aligned sample.
- `D138`: per-side OLS slope of cumulative displayed depth against absolute price distance from D011, returned as `{bid_slope, ask_slope}`.
- `D156`: return both Pearson correlation and ridge-stabilised partial-correlation matrices over the aligned D155 feature history. The ridge coefficient is a mandatory versioned parameter; partial correlation is derived from the inverse regularised covariance matrix.

### K07_WEIGHTED_SCORE — deterministic composite scores and latent factors

For rows that say combine/score/aggregate without an externally established closed-form equation, `P_SCORE` supplies an **ordered immutable feature schema**. Each feature schema entry names one signal dependency, one deterministic scalar extractor, one transform and its parameters, orientation, weight and any clipping bounds. An implementation never chooses an extractor or transform implicitly.

Allowed scalar extractors are fixed mathematical operations:

- `component(path) =` the named scalar field/component;
- `weighted_component_sum = Σ a_i x_i` with all coefficients `a_i` declared;
- `class_probability(label) = p_label`;
- `probability_margin = p_(1) - p_(2)`, the largest minus second-largest class probability;
- `normalised_entropy = -Σ p_i ln(p_i) / ln(K)` for `K >= 2`, with `0 ln 0 := 0`;
- `distribution_cdf(x) = P(X <= x)`, `upper_tail(x) = 1-CDF(x)`, and named mean/variance moments under the stored distribution;
- `matrix_entry(i,j)`, `row_l2(i) = sqrt(Σ_j a_ij²)`, and `frobenius = sqrt(Σ_iΣ_j a_ij²)`.

A structured/vector/matrix/distribution input therefore cannot be fed to a score until its exact extractor and arguments are present in the feature schema.

For extracted scalar `x`:

1. `identity(x) = x`;
2. `signed_log(x;s) = sign(x) * ln(1 + |x|/s)`, with mandatory `s > 0`;
3. `bounded_ratio(x;s) = x / (s + |x|)`, with mandatory `s > 0`;
4. `z_score(x) = (x-μ)/σ` using the strictly-prior baseline admitted by the feature schema, with `σ > 0`;
5. optional clipping is applied **after** the transform and **before** orientation;
6. orientation is multiplication by the declared `+1` or `-1`;
7. `raw = intercept + Σ w_j z_j`;
8. a row whose canonical scalar output is `0-1` returns `sigmoid(raw)`; a generic/factor score returns `raw` unless its row rule explicitly declares another fixed bounded carrier.

Weights are non-negative after orientation has been separated from sign. Weights, intercept, transform scales, extraction arguments, feature orientation, baseline identity and clipping bounds are immutable parameter-set content and are retained in lineage. Missing required features produce no occurrence; weights are never silently renormalised around missing inputs.

For `D157`, the row-specific disagreement rule additionally uses the aligned D156 partial-correlation matrix to discount duplicate information: after oriented/standardised D155 scalar features `z_j` are formed, set `u_j = w_j / (1 + Σ_{k≠j}|ρ_jk|)`, require `Σu_j > 0`, normalise `v_j = u_j/Σu_j`, set `μ_w = Σv_j z_j`, and return `sqrt(Σv_j*(z_j-μ_w)^2)`. No alternative sample/unbiased weighted-variance correction is used.

For `D173`, the subject candidate is the exact `CandidateStructureContext` and its comparison universe is **only** the neighbour identities declared for that subject in the immutable `CandidateSetContext`. The neighbour relation is explicit, symmetric or directed exactly as stored, and may encode adjacent strikes/expiries or approximately equivalent exposures; implementation code may not infer neighbours from database proximity. Apply the row's `P_SCORE` schema to those named comparisons and preserve each compared candidate identity and score difference in lineage.

For K07 rows consuming probability vectors or distributions (`D159`, `D172`, `D187`, `D207`), the companion CSV binds the dependency and `P_SCORE` feature schema must name the exact class probability, entropy/margin, tail probability, moment or other allowed scalar extractor. No implementation-selected scalarisation is permitted.

`D008` is a structured quality result rather than a scalar with hidden meaning. It preserves `max_true_instant_skew_seconds`, `event_time_coverage_fraction`, `missing_event_time_count` and the parameterised bounded `alignment_score`; receipt-only/date-only observations may contribute to coverage/missingness but never receive fabricated event instants.

This kernel governs D006, D008, D040, D041, D061, D064, D070, D084, D132, D146–D150, D157–D159, D163, D171–D173, D187, D200 and D207.

### K08_RULE_BUCKET_POLICY — deterministic rule sets, grouping and constrained selection

Rules, thresholds, bands and tie-break order are immutable versioned parameter-set content.

- `D007 = satisfied_required_count / required_count`, `required_count > 0`; each policy requirement contributes at most one.
- `D015`: quote test first (`trade > midpoint` buyer, `< midpoint` seller); at exact midpoint apply signed tick test against the last different trade price; if still ambiguous emit `0/unknown`, never guess.
- `D016 = Σ trade_sign_i * trade_size_i` over the selected window.
- `D065`: for an event-centred window `[event_ts-pre_window, event_ts+post_window]`, select the relevant scheduled event from visible R284 events whose timestamp lies in the equivalent as-of interval `[as_of-post_window, as_of+pre_window]`. If more than one qualifies, choose the smallest absolute time distance from `as_of`, breaking an exact tie toward the earlier event. Return true only when that selected event's D064 meets the configured applicability threshold. D062 may supply the pre-event countdown but is never the sole source for post-event activity.
- `D091`: bucket by absolute delta using non-overlapping versioned bucket boundaries and deterministic boundary inclusion.
- `D120`: return both `signed_contracts = Σ sign*size` and `signed_premium_notional = Σ sign*size*trade_price*multiplier`.
- `D121`, `D122`: exact grouped sums of D120 by parameter-defined delta and expiry/DTE buckets.
- `D124`: return each strike/expiry share of total relevant OI as a decimal fraction plus HHI `Σ share_i²` on the canonical `0–1` scale. Total relevant OI must be positive.
- `D128`: use **absolute** gamma-exposure magnitude for concentration. For configured spot-distance bands, `share_b = Σ|gamma_exposure_i|_b / Σ|gamma_exposure_i|`; return the shares plus HHI `Σ share_b²` on the canonical `0–1` scale. Signed net gamma remains available from D125/D130 but is not used as a concentration weight.
- `D139`: after deterministic SMART-book reconstruction, return insert-event count rate and inserted-size rate by side and configured level bucket over the exact window. Inserted size is the event's admitted displayed size.
- `D140`: after the same reconstruction, return delete/cancel-event count rate and removed-size rate by side and configured level bucket. Removed size is the immediately pre-delete displayed size at that book row, not an assumed value from a delete event whose native size may be zero.
- `D141`: a replenishment candidate is a depletion/execution at one subject/side/price followed within `Δt_max` by restored displayed size at that same subject/side/price. Each depletion is matched once to the first qualifying restoration. Per event, credited replenishment is capped at the depleted size. The window score is `Σ credited_replenished_size / Σ depleted_size` across matched/eligible depletion events; denominator must be positive.
- `D142`: capture the pre-shock selected-depth total and spread, then after the configured depletion/spread-shock event identify the first reconstructed-book state at which **both** depth is at least the configured fraction of pre-shock depth and spread is no greater than the configured multiple/fraction of pre-shock spread. Report elapsed seconds plus recovered depth/spread state. If the joint condition is not met within the observation window, no completed-resilience occurrence is emitted.
- `D166`: true only when D159 and D165 satisfy both configured minimum thresholds.
- `D167`: evaluate only the candidate identities enumerated by the exact `CandidateSetContext`. If no candidate has a lawful D165/D166 occurrence, no D167 occurrence exists. If every eligible candidate has D166=false emit category `no_trade`; otherwise choose the eligible D166=true candidate with greatest D165. Equal D165 values are resolved by the immutable candidate order in `CandidateSetContext`, followed by any row-specific tie-break explicitly declared in `P_RULE`; no candidate outside the set may be introduced at runtime.
- `D175`: maximum permissible risk is the minimum of every active capital, CVaR, stress-loss, concentration and liquidity limit expressed in common currency.
- `D176`: recommended quantity is the greatest non-negative whole contract/share count satisfying every D175 constraint after the explicit model-uncertainty and liquidity multipliers; fractional-share support requires an explicit parameter mode.
- `D178`: for a buy, target price is no higher than `min(best_ask, midpoint + allowed_execution_cost_per_unit)`; for a sell, no lower than `max(best_bid, midpoint - allowed_execution_cost_per_unit)`. The allowed cost is bounded by fresh D133 and the minimum edge reserve from D177. Order side, size and urgency are typed calculation-context inputs.
- `D186`: compare current and stored entry D155 vectors using `d² = Σ_j w_j * ((x_j-entry_j)/s_j)²`, where each `w_j >= 0`, `Σw_j=1`, and each scale `s_j > 0` is an explicit immutable `P_RULE` similarity scale for that feature. Return `similarity = exp(-0.5*d²)` plus raw and standardised per-feature deltas. Entry-state occurrence identity is mandatory.
- `D189`: target hedge vector equals clipped target-band midpoint minus the current D181, D182, D183 **and D184** exposures for each exposure outside its configured band; exposures already inside band return zero adjustment. D175 supplies the active risk limits used to clip the target adjustment.
- `D192`: apply the versioned `P_RULE` action precedence without comparing unlike value types or a hedge vector with a monetary value. The fixed decision order is: (1) mandatory-exit rule if D187 invalidation/risk policy requires exit; (2) mandatory-hedge rule when D175 is breached and D189 contains a non-zero permitted hedge adjustment; (3) modify when D190 utility gain exceeds the configured minimum in D190's declared utility domain; (4) exit when D191 immediate-exit currency value exceeds D188 `expected_currency_PnL` by the configured currency exit margin; otherwise `hold`. Any ties inside a rule use the explicit fixed tie order from `P_RULE`.
- `D208`: classify each signal by versioned thresholds over D202 information value and D207 decay into the listed categories; no free-text classification.
- `D209`: materialise one trigger occurrence for the next admitted M00 receipt event or configured recalculation schedule event. It is a calculation/control fact only and performs no external action.

### K09_SURFACE_DENSITY — interpolation, arbitrage-aware surface fitting and risk-neutral density

- `D096`: for each expiry and option side separately, linearly interpolate IV in absolute delta around `0.50` using the nearest valid observations bracketing 0.50. If an exact 0.50 observation exists use it. When both call and put 50-delta estimates exist, the canonical ATM IV is their arithmetic mean; when only one side is valid, that side may be used only if the parameter profile explicitly admits single-side coverage and the coverage state is preserved. If 0.50 is not bracketed, no interpolation occurs unless a separately versioned extrapolation mode exists.
- `D102`: for each admitted IV point use `k = ln(strike / spot_ref)` with strike from R014, `spot_ref` from the aligned R118 model-underlying observation, and `T` from aligned D086. Fit total implied variance `w = IV²*T` on `(k,T)` with a constrained cubic B-spline weighted least-squares surface. Weights are inverse squared IV bid/ask width where positive, otherwise equal weight. Enforce non-negative total variance, non-decreasing calendar total variance at matched `k`, and strike-slice call-price convexity using the exact `OptionRevaluationConventionVersion`; the implementation may not choose a pricing convention. Return weighted RMS IV residual plus per-point residuals. If the coordinate inputs, revaluation convention or constraints are unavailable/infeasible, no fitted-surface occurrence is emitted.
- `D111`: for one expiry, take the valid call-option D087 mid-price observations across strike and fit a decreasing convex cubic spline directly in call price versus strike; D102 must satisfy its accepted surface-quality tolerance for the same snapshot but is not treated as a call-price object. Compute non-negative state-price density from the fitted call-price curve using the Breeden–Litzenberger second strike derivative on the versioned strike grid, then normalise numerical mass to 1 to obtain the risk-neutral terminal probability density. Grid/interpolation identities are lineage.
- `D112`, `D113`: numerical trapezoidal integration of D111 below/above the parameter-selected terminal-price thresholds.
- `D115`: use one aligned R118 `spot_ref > 0` and convert each D111 terminal-price grid point `S_T` to log return `r = ln(S_T/spot_ref)`. Evaluate D111 and D114 on the same versioned log-return grid and return CDF difference by grid point plus differences in mean, variance and configured tail probabilities. The exact `spot_ref` occurrence and return grid are lineage; no implicit price-to-return anchor is allowed.
- `D129`: this brief adds D130 as the spot-scenario exposure dependency. Use the D130 net-gamma values over its ordered spot grid, linearly interpolate between adjacent points, and find sign-changing roots. Choose the root nearest current spot; equal-distance ties choose the lower price. If no sign change exists in the admitted search band, no gamma-flip occurrence is emitted.

### K10_DISTRIBUTION_SCENARIO — conditional distributions, probability vectors and scenario sets

- `D114`: construct historical training tuples `(c_t, r_{t→t+H})`, where conditioning vector `c_t={D035,D036,D079,D080,D081,D070,D061}` is evaluated **at forecast origin `t` using only facts visible at that origin**, and `r_{t→t+H}` is the subsequently realised horizon-matched NVDA log return. Weight historical returns by Gaussian-kernel similarity of `c_t` to the current conditioning vector. Bandwidths and minimum effective sample size are mandatory parameters. The canonical distribution is a weighted empirical atomic measure/CDF; when a continuous density is required, use a Gaussian KDE over return outcomes with a separate mandatory versioned outcome bandwidth. Return both representations and never use endpoint/future conditioning values to weight the historical sample.
- `D152`–`D154`: probability vectors use multinomial logistic/softmax models over the exact listed input vector. Coefficient matrix, intercepts, feature standardisation and class labels are immutable versioned model parameters. Probabilities sum to 1.
- `D160`: construct a finite deterministic joint scenario set from versioned quantiles of D114, D111 and D130 plus configured state-conditioned rate/sector/liquidity shocks. Each scenario records every shock component and a non-negative weight; weights are normalised to 1. Scenario grids, conditional mappings and combination rules are parameter-set content, never random runtime draws.
- `D201`: counterfactuals replay the versioned alternative candidate definitions against the realised subsequent M00/Derived Signal path, using only the information set that existed at the original decision time for candidate formation. The realised future path may be used only for outcome valuation, not to change the historical decision inputs.

### K11_EXPOSURE_STRESS — option-position exposure, dealer proxies and stress revaluation

The parameter set supplies dealer-side sign assumptions where required and candidate-structure leg quantities where the calculation is hypothetical rather than a live position.

Any row that revalues option prices or recomputes Greeks (`D102`, `D130`, `D174`, `D188`, `D198`) additionally requires an immutable `OptionRevaluationConventionVersion`. That convention names the pricing/Greek model family, exercise-style treatment, discount/rate and dividend/borrow/carry inputs or references, time/day-count convention, IV/skew interpretation, numerical scheme/tolerances and Greek scaling. A concrete convention is an explicit calculation input and is retained in lineage; implementation code may not silently choose or substitute one.

- `D125`: per contract/strike preserve both `delta_change_per_currency_unit = dealer_sign * OI * gamma * multiplier` and `currency_scaled_gamma_per_1pct = dealer_sign * OI * gamma * multiplier * spot² * 0.01`; aggregate each measure separately and retain the dealer-sign assumption.
- `D126 = Σ dealer_sign * OI * vega * multiplier`.
- `D127 = Σ dealer_sign * OI * delta * multiplier`.
- `D130`: recompute the D125/D126/D127 exposure vector over the versioned spot/IV/skew scenario grid using the exact `OptionRevaluationConventionVersion` and return required hedge-share changes plus net gamma exposure per scenario. When D129 is requested, the scenario grid must cover the independently configured `gamma_flip_search_band`; D130 does not depend on a D129 result.
- `D169`: evaluate total expiry payoff net of premium over every strike breakpoint plus both tails. Return `{bounded, contractual_max_loss}` when bounded. If a tail is unbounded, return `bounded=false` and the parameter-set stress loss instead of falsely calling it contractual maximum loss.
- `D174`: full structure **gross** P&L revaluation over each D160 scenario using the exact candidate legs and `OptionRevaluationConventionVersion`, returned as a candidate × scenario P&L matrix aligned to the D160 scenario weights. D164 is excluded here and is deducted exactly once by D165; D168 exposures are preserved as diagnostics but do not replace full revaluation when the convention is available.

### K12_VALUE_UTILITY — execution-aware value estimates

- `D133`: estimate executable slippage by deterministic book walking through displayed depth for the exact intended size and side, relative to the matched decision midpoint `(R034 + R035) / 2` at the same knowledge cutoff. D011/D087 may expose equivalent midpoint conveniences elsewhere, but they are not D133 dependencies. Preserve `{expected_fill_price, signed_slippage_per_unit, slippage_bps, expected_slippage_currency}` with the exact intended size/multiplier. If displayed depth is insufficient, no full-size estimate is emitted unless the parameter set explicitly supplies a named extrapolation model.
- `D177`: recompute the same D165 utility definition at the immediate pre-order knowledge cutoff using fresh D164 execution cost and D159 identifiability. It does not subtract D164 a second time.
- `D188`: revalue the exact current position enumerated by the immutable `LivePositionContext` under D160 scenarios using the `OptionRevaluationConventionVersion`; aggregate Greeks D181–D184 are diagnostics/constraints and are not a substitute for leg-level nonlinear revaluation. Return both `expected_currency_PnL` and the corresponding `P_UTILITY` hold-utility value under the exact D164 cost treatment declared for the live-position context. Immediate close/restructure alternatives are not silently folded into the hold value; D190/D191 represent those alternatives.
- `D178` uses the constrained-price rule in K08 because it also depends on order-side policy.

### K13_EXPECTATION_RISK_UTILITY — expected P&L, CVaR and net utility

- `D161 = Σ_s p_s * PnL_{candidate,s}` for each candidate, where scenario weights `p_s` come from D160 and candidate scenario P&L comes from the aligned D174 candidate × scenario matrix. Candidate identity must match the exact `CandidateStructureContext`; D160 alone is insufficient.
- `D162`: for each candidate use D174 scenario P&L and D160 weights. For loss `L_s=-PnL_{candidate,s}`, sort scenarios by loss and calculate weighted VaR and expected shortfall/CVaR over exactly the worst probability mass `1-α`, using fractional weight at the boundary when necessary. Return `{VaR_currency, CVaR_currency, VaR_percent_risk_capital, CVaR_percent_risk_capital}` where each percent is `100 * currency_value / CandidateStructureContext.risk_capital_currency`; that denominator must be positive. `α` is mandatory versioned configuration.
- `D165 = D161 - λ_tail*D162_CVaR_currency - λ_model*D163 - D164` after unit conversion into one declared utility/currency convention. `λ_tail >= 0`; `λ_model` carries the currency/utility scale required to convert D163 into the same domain. Coefficients and any additional monotone utility transform are immutable parameters.

### K14_PNL_ATTRIBUTION — deterministic Greek/path attribution

Use left-endpoint contemporaneous Greeks over each aligned path interval and retain interval-level contributions.

- `D194 = Σ quantity * multiplier * delta_t * ΔS_t`.
- `D195 = Σ quantity * multiplier * 0.5 * gamma_t * (ΔS_t)²`.
- `D196 = Σ quantity * multiplier * vega_t * ΔIV_parallel_t`, respecting the provider's vega unit convention.
- `D197 = Σ quantity * multiplier * theta_t * elapsed_days_t`.
- `D198`: revalue the exact position/structure under the D104 skew change with parallel IV held fixed using the `OptionRevaluationConventionVersion`, then subtract the already-attributed D196 parallel-vega contribution. This residual is the skew P&L component; D196 is therefore an explicit derived dependency.

The attribution context must include the exact M00 underlying/IV path and position/quantity history required for these equations even where the legacy workbook dependency list omitted those path references.
The immutable attribution convention must also state whether the observed provider P&L fields used by D199 are gross or net of commissions/fees. D193 is subtracted in D199 only when the observed-P&L basis is gross of those costs; double-counting provider-included costs is prohibited.

### K15_EVALUATION — forecast, calibration and out-of-sample evaluation

Evaluation rows consume immutable `EvaluationSet` definitions identifying forecast occurrences, realised outcome definition, evaluation window and baseline/comparator.

- `D202`: return a structured incremental-value record containing (a) out-of-sample Pearson/Spearman information coefficient where the target is numeric, (b) reduction in the accepted forecast loss relative to the baseline without the signal, and (c) decision-performance delta where applicable. Each component must name its target and comparator.
- `D203`: expected calibration error using versioned probability bins: `Σ_b (n_b/N) * |mean_p_b - observed_rate_b|`; return the bin table with the scalar error.
- `D204 = mean((p_i - y_i)²)` over resolved binary forecast/outcome pairs.
- `D205`: discrete/categorical loss `-ln p(realised)`; continuous-density loss `-ln f(realised)` under the declared density convention. Batch score is arithmetic mean. Zero realised probability/density is infinite loss; no silent epsilon clipping.
- `D206`: return an out-of-sample performance vector containing gross P&L, D193 transaction cost, net P&L, hit rate, maximum drawdown and annualised Sharpe ratio of net period returns (`sqrt(periods_per_year) * mean(return) / sample_sd(return)`) under the versioned evaluation window/regime segmentation. Sharpe is absent when sample standard deviation is zero.
- `D207` then uses K07 over deterioration of D203, D206 and D202 versus immutable validation baselines.

### K16_STRUCTURED_ASSEMBLY — canonical state vector assembly

`D155` is not a statistical model. It is an ordered, schema-versioned assembly of the exact admitted component occurrences named by its calculation definition, with each component value, units, freshness/quality metadata and occurrence identity preserved. It performs no hidden weighting or inference.

### K17_ORDER_FLOW_IMBALANCE — top-of-book OFI

For consecutive best-book states `n-1` and `n`:

`e_n = I(Pb_n >= Pb_{n-1})*Qb_n - I(Pb_n <= Pb_{n-1})*Qb_{n-1} - I(Pa_n <= Pa_{n-1})*Qa_n + I(Pa_n >= Pa_{n-1})*Qa_{n-1}`.

`D145` is `Σ e_n` over the selected 1s/5s/1m window. Preserve event sequence and window boundaries in lineage.

## 6. Make every non-signal input explicit and versioned

The calculation owner may require configuration/context in addition to R/D facts. Those inputs are not Raw Signals and must not be disguised as observations.

The following immutable typed inputs are admitted:

- `CalculationParameterSet` — windows, thresholds, weights, coefficients, calendars, baskets, grids, confidence levels, model bandwidths and other numeric/configured parameters;
- `RequiredFieldPolicy` — D007 mandatory-field requirements;
- `CandidateStructureContext` — one candidate identity, hypothetical leg side/contract, quantity, premium/entry assumptions and positive `risk_capital_currency`; required for per-candidate calculations before an actual position exists;
- `CandidateSetContext` — an immutable ordered set of distinct `CandidateStructureContext` identities plus explicit candidate eligibility classes and the exact neighbour relation used by D173. It supplies the complete comparison/selection universe for D167 and D190. It contains identities/relations only, never precomputed D165/D173/D190 answers;
- `LivePositionContext` — immutable identity of the exact current open-position state used for nonlinear live-position calculations: leg contract identities, signed quantities, multipliers and exact M00/current-state occurrence references required to establish the repricing baseline. It may reference raw/current facts but may not contain a precomputed D188 continuation value;
- `OrderIntentContext` — order side, intended size and urgency used by D133/D178;
- `EntryStateContext` — exact stored D155 occurrence representing the entry-state comparison anchor for D186;
- `EvaluationSet` — forecast identities, realised-outcome definition, evaluation window, comparator/baseline and locked model/version for D202–D207;
- `RecalculationSchedule` — admitted scheduled trigger rules for D209;
- `RawSignalProjectionMapping` — immutable field-level mapping from a canonical `Rxxx` identity to one exact provider/native-record field path and native unit semantics for a named source variant; it may select/expose a native value but may not derive a `Dxxx` value.
- `UnitConventionVersion` — immutable conversion law from admitted native units/scale into canonical calculation units, including explicit fraction/percent/basis-point/volatility-point conventions; conversion is never inferred from numeric magnitude.
- `PnLConventionVersion` — immutable statement of provider P&L inclusion/exclusion semantics and attribution unit conventions used by D194–D199.
- `OptionRevaluationConventionVersion` — immutable option price/Greek revaluation law required by D102/D130/D174/D188/D198, including model family, exercise handling, carry/rate inputs or references, time convention, numerical method/tolerances and Greek scaling.
- `ExecutionCostScheduleVersion` — immutable pre-trade commissions/fees and multi-leg incremental-cost schedule used by D164; it is distinct from realised R233 execution cost.
- `AttributionPathContext` — exact aligned underlying/IV/position/quantity path occurrence references used by D194–D198; it contains references, not precomputed attribution answers.
- `InputSelectionPolicyVersion` — immutable subject/contract join keys, maximum staleness/skew tolerances, temporal-basis permissions and basket membership needed to select compatible M00/D inputs without look-ahead.

Every context object has an opaque identity and immutable version. A derived occurrence preserves the exact context identities it used. Changing a context value creates a new version and, where material, a new derived occurrence; it never rewrites old calculated truth.

In `NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, `typed_contexts` is a semicolon-delimited **conjunction**: every listed context is required for that row. No `|`/OR syntax is admitted. A token of the form `CalculationParameterSet:P_PROFILE` means one `CalculationParameterSet` instance constrained to that named parameter profile; the colon is a type/profile qualifier, not an alternative operator. Alternative applicability must be represented by an explicit context type/version or a separate calculation-definition version, never punctuation interpreted by implementation code.

A parameter/context object may contain fixed coefficients or thresholds. It may not contain a precomputed `Dxxx` answer and thereby bypass the calculation.

## 7. The companion CSV is the single per-signal dependency authority

`NVDA_DERIVED_SIGNAL_CATALOGUE.csv` is the only normative list of direct `Rxxx` dependencies, predecessor `Dxxx` dependencies, kernel binding and row-specific typed contexts. The workbook dependency columns are reference evidence only.

The CSV incorporates all V8 dependency corrections and the independent-review repairs, including:

- coherent D078–D081 factor-model dependencies, including D075 as the dependent return for D079–D081;
- D088 bid/ask inputs and D129 scenario-gamma dependency;
- the spot/strike/time inputs required by D102 and the common-return anchor required by D115;
- R284 support for D065 pre/post event selection;
- complete SMART/direct L2 reconstruction fields for D131/D133/D139–D144, with D133 decision midpoint computed locally from its matched R034/R035 inputs rather than an undeclared D011/D087 edge;
- R062 for D132 and session-open/VWAP inputs for D151;
- D174 candidate scenario P&L for D161/D162;
- pre-trade D164 cost inputs through `ExecutionCostScheduleVersion` rather than realised R233;
- D184 for D189 and D196 for D198;
- matched execution quantity/multiplier support for D193;
- explicit `CandidateSetContext` bindings for D167/D173/D190, `LivePositionContext` for D188, unambiguous conjunctive typed-context grammar for D164, corrected K04 historical-vs-cross-sectional parameter bindings, and typed attribution/evaluation contexts for D194–D207.

An implementer must not merge the workbook and CSV dependency sets, nor resurrect a workbook-only dependency that the CSV supersedes. A dependency change requires a brief/calculation-definition version change.

## 8. Treat history sufficiency as part of meaning

A required history/window is a semantic precondition. Before the full required history exists, there is no canonical occurrence for that calculation.

Examples include five-/ten-/twenty-day realised volatility, z-score baselines, regression windows, one-year IV rank/percentile, calibration/evaluation sets and any state-conditioned historical model.

Do not fabricate zero, semantic `NULL`, shortened windows, duplicated observations, forward-filled future knowledge, silent interpolation/extrapolation or a different estimator under the same `Dxxx` identity.

### 8.1 Match subjects, contracts and time before calculating

Input selection is part of calculation meaning, not a database convenience.

For every calculation, the exact `InputSelectionPolicyVersion` determines the join keys and admissible temporal basis. At minimum:

- single-instrument calculations require the same canonical subject/instrument identity across all required inputs;
- option-contract calculations require matching underlying, expiry, strike, option right and contract identity wherever those dimensions are material;
- cross-sectional calculations use the exact versioned basket/member set rather than whatever members happen to be present;
- a point-in-time input is the latest eligible fact at or before the knowledge cutoff under the row's permitted time basis and freshness limit;
- an input after the knowledge cutoff is never eligible;
- a `true_instant` may be aligned on D001/event time; `receipt_only` and `date_only` values must not be given fabricated event instants and may participate only where the row/policy explicitly permits their temporal basis;
- calculations requiring a synchronous snapshot must satisfy the configured maximum skew across the selected inputs; otherwise no occurrence;
- contract/expiry/delta/strike matching must be exact unless the row explicitly defines interpolation/bucketing;
- a missing exact match is not repaired by nearest-neighbour substitution unless the accepted kernel explicitly defines that interpolation.

The resulting derived occurrence retains the exact selected input occurrence identities, so the join can be reconstructed independently of query order.

## 9. Preserve the M00 boundary and expose a typed raw-value/history projection

The calculation owner consumes M00 truth only through M00's public seam. It must not read or write M00-owned PostgreSQL tables directly.

The existing v1.0.0 M00 public read facet is referential: it can retrieve a raw observation by its opaque occurrence identity. M00 observations preserve provider-native logical records and may carry one or more `RawSignalCatalogueId` values as provenance. That provenance is **not** sufficient to identify a calculable field value when one provider record contains multiple fields or multiple `Rxxx` IDs.

The successor authority therefore requires an additive read-only M00 projection for the named Derived Signal consumer. This is a compatibility extension of M00's read surface only: it does not change the stored `RawObservationOccurrenceV1` payload, observation identity or existing raw-truth meaning.

For each projected raw value it exposes at minimum:

- canonical `Rxxx`;
- source M00 `observation_occurrence_id`;
- exact `RawSignalProjectionMapping` identity/version;
- provider/source variant and exact native field path selected from the immutable `native_record`;
- exact native value and native units before conversion;
- subject/instrument identity available from the observation/mapping;
- source temporal kind and preserved source timestamp/timezone metadata;
- `received_ts_utc`, ingestion-sequence value and scope;
- any revision/vintage metadata required to distinguish observations.

A projection exists only when an explicit mapping resolves one exact native field/value for that `Rxxx`. If the mapping is absent, ambiguous, points to a missing field, or cannot establish units required by the calculation, no projected value exists. A record-level `raw_signal_catalogue_ids` tag alone must never cause the calculation owner to guess which native field is the value.
Provider-specific field names, callbacks and native extraction rules remain on the raw-side translation/read-projection boundary. The Derived Signal calculation implementation must not embed provider-specific parsing as a fallback when the projection is absent.

The read projection must support bounded enumeration by `Rxxx`, subject/context and receipt/event criteria with stable ordering and pagination. It may expose exact native facts and mapping metadata, but it does not aggregate, rescale, interpolate, calculate windows or emit any `Dxxx`.

Before a raw numeric value enters a calculation kernel, the exact `UnitConventionVersion` converts it into the kernel's canonical unit. Linear/affine unit conversion and explicit scale conversion are permitted; magnitude-based heuristics are prohibited. In particular, the implementation must never guess whether `5`, `0.05` or `5%` represents the same percentage, yield or volatility.

Every derived occurrence lineage retains the source observation identity, projection-mapping version and unit-convention version so the calculation can be reproduced without direct access to M00 tables.

## 10. Keep calculation ownership separate from the PostgreSQL persistence mechanism

The Derived Signal capability owns the calculation meaning and must expose one canonical production calculation path for each admitted calculation-definition version.

PostgreSQL is the durable-state and transaction mechanism for this capability; it does not become semantic owner merely because calculation inputs/results are stored there. The implementation may perform an admitted kernel in owner service code, in calculation-owner-owned SQL/functions/procedures, or in a combination selected during implementation, provided:

- one exact calculation-definition version has one authoritative production result path;
- no second implementation may silently compete with or override that result;
- any optimisation/cached/materialised SQL path is proved equivalent to the authoritative calculation version before it can supply canonical results;
- calculation code receives M00 facts only through the typed public projection in clause 9;
- the calculation owner never obtains direct read/write privilege over M00-owned relations merely for convenience.

Durable persistence must use:

- a PostgreSQL schema separate from M00's schema;
- a database role/write boundary separate from M00's writer;
- no calculation-owner database-role privilege to read or write M00-owned tables;
- transactionally durable derived occurrences, parameter/context identities and lineage;
- where calculation-run input projections are staged in PostgreSQL, rows that retain source M00 occurrence IDs, `Rxxx`, projection-mapping version, native value/unit, canonical converted value/unit and unit-convention version and are immutable for that calculation run.

The same PostgreSQL deployment may host both schemas. A separate PostgreSQL server instance is not required by this brief.

## 11. Keep time, knowledge cutoff and no-look-ahead distinct

Every derived occurrence preserves calculation time, effective/as-of time, window, knowledge cutoff and direct input occurrence identities.

Only M00/Derived Signal facts visible under the calculation's knowledge cutoff may be used, except that explicitly post-hoc evaluation/counterfactual calculations may use later realised facts solely as outcomes while preserving the original decision information set.

Date-only, receipt-only and true-instant distinctions remain intact; no derived calculation may invent an event instant from absent source-time authority.

## 12. Persist a typed derived occurrence with exact lineage

At minimum preserve:

- canonical `Dxxx`;
- opaque derived-occurrence ID;
- calculation-definition version;
- parameter/context version IDs;
- subject/instrument/universe;
- effective/as-of time and exact window;
- knowledge cutoff and calculation time;
- typed result;
- units/result shape;
- direct M00 occurrence refs plus the exact raw-value projection-mapping and unit-convention versions used for those inputs;
- direct predecessor D occurrence refs;
- applicable P&L/attribution convention version where the result depends on provider P&L inclusion semantics;
- supersession/recalculation lineage where applicable.

The value carrier must support scalar numeric, boolean, category, temporal, vector, matrix, density/distribution, scenario-set and event-like results.

## 13. Evaluate D dependencies as one version-consistent acyclic graph

A request for a `Dxxx` may recursively resolve predecessor `Dxxx` calculations, but only through the dependency graph admitted by this brief.

- Evaluate predecessors in topological order.
- Every predecessor used by one result must be compatible with the same subject/context, knowledge cutoff and calculation-definition/parameter universe required by the requesting row.
- A stored predecessor may be reused only when its exact lineage and versions satisfy the request; otherwise calculate a new predecessor occurrence or fail closed.
- Never mix predecessor occurrences from different parameter/model versions merely because their `Dxxx` identifiers match.
- If any required predecessor has no lawful occurrence, the requesting calculation has no occurrence.
- Runtime recursion may not add dependency edges or bypass an admitted edge to obtain a convenient value.

The 209-row graph plus the explicit dependency overrides in clause 7 is required to remain acyclic.

## 14. Make retries idempotent and recalculation append-only

Same logical occurrence identity + same inputs + same calculation/parameter/context versions + same temporal context must be idempotent.

Conflicting content under one derived-occurrence ID is rejected.

A changed material input, knowledge cutoff, formula version, parameter/context version or provider revision produces a separately identifiable occurrence. Historical derived truth is not overwritten.

## 15. Expose one typed public calculation/read seam

The public seam must support:

- calculate/materialise a named `Dxxx` for exact context/as-of/calculation/parameter versions;
- retrieve by derived-occurrence ID;
- retrieve bounded derived history;
- expose exact lineage and versions;
- distinguish absent occurrence from a persisted value.

Downstream readers do not gain calculation-owner write authority.

## 16. Calculated action-like outputs do not perform external effects

A calculated `position_size`, `limit_price`, `action`, `signal_disposition`, `next_tick` or similar D value remains a persisted calculation only.

This brief does not authorise order placement/cancellation/modification, brokerage-account mutation, provider/network actions, or autonomous external effects.

## 17. Fail closed on any missing prerequisite

No derived occurrence is emitted when a material prerequisite is absent, including required M00/Derived Signal facts, required window, accepted calculation definition, parameter/context version, subject matching, temporal alignment, units, successful execution of the one authoritative calculation path, or durable write.

No worker/SQL/helper/test may invent a default to make the row calculable.

## 18. Required proof before implementation acceptance

Proof must cover at least:

1. all 209 D identities bind to exactly one row in `NVDA_DERIVED_SIGNAL_CATALOGUE.csv` and one admitted kernel;
2. all R/D references plus brief dependency overrides resolve and remain acyclic;
3. one M00 observation carrying multiple `Rxxx` provenance IDs cannot yield a raw value until an exact field-level projection mapping resolves the requested `Rxxx`;
4. native percentage/rate/volatility representations convert only under explicit unit-convention versions, including adversarial `5` versus `0.05` cases;
5. subject/contract/time selection refuses mismatched contracts, future observations and over-skewed snapshot inputs;
6. direct arithmetic example D011;
7. five-day history sufficiency D035;
8. derived-from-derived D107 with ultimate raw lineage;
9. recursive D evaluation is topologically ordered and refuses predecessor occurrences from incompatible model/parameter versions;
10. coherent shared-model regression/residual D078–D081, including proof that D079–D081 cannot fit without D075;
11. surface/density D102/D111, including explicit spot/strike/time coordinates and option-revaluation convention;
12. parameterised score/probability rows with immutable parameter versions, exact scalar extractors and fixed transform mathematics;
13. D007 completeness;
14. D180 uses filled/(filled+remaining), and D193 uses matched executed quantity rather than cumulative-state inference;
15. D204 Brier and D205 log score;
16. no-look-ahead;
17. deterministic re-execution;
18. append-only recalculation;
19. M00 seam isolation, bounded history enumeration and raw-value projection without direct table access or provider-specific parsing fallback in the calculation owner;
20. D199 attribution proves the configured provider-P&L gross/net convention and conditionally subtracts D193 exactly once;
21. L2 book reconstruction proves deterministic position/side/operation ordering and D139–D144 event/recovery semantics;
22. D161/D162 consume aligned D174 candidate scenario P&L and D160 weights, with D162 percentage risk tied to explicit risk capital; D167/D173/D190 use only the immutable candidate/neighbour universe declared by `CandidateSetContext`;
23. D188 revalues the exact leg-level state referenced by `LivePositionContext` and cannot substitute aggregate D181–D184 Greeks for nonlinear repricing;
24. PostgreSQL schema/role isolation, durable derived-state persistence and one authoritative calculation path without a competing semantic implementation;
25. structured/vector/matrix/distribution result persistence;
26. external-effect exclusion;
27. architecture admission through the normal process rather than numeric module ID embedded in this brief.

Passing these proofs establishes only Derived Signal Calculation Truth. It does not establish predictive quality, profitability, production SLA or external-action authority.

## Appendix A — parameter-profile meanings

- `P_TIME`: market calendar, session/expiry convention and timezone mapping.
- `P_BASIC`: exact subject/member selection only; no mathematical free parameter.
- `P_WINDOW`: comparison horizon/anchor and required minimum coverage.
- `P_BASELINE`: strictly-prior historical baseline length, matching rule and minimum sample; it never denotes a contemporaneous basket.
- `P_CROSS_SECTION`: monitored contemporaneous basket/member rule; it never supplies a historical baseline.
- `P_VOL_WINDOW`: return sampling interval, calendar/trading-time convention and required coverage.
- `P_REGRESSION`: regression window/state subset and D156 ridge coefficient.
- `P_SCORE`: ordered feature schema, exact scalar extractors, fixed transform family/scale, orientation, immutable weights/intercept, baseline identity and any output clipping.
- `P_RULE`: bucket boundaries, thresholds, bands, action precedence/tie-breaks, D186 feature scales/weights and typed policy contexts.
- `P_SURFACE`: strike/expiry grid, spline knots/penalty, fit tolerances and integration/search grid.
- `P_MODEL`: model coefficients/bandwidths/class labels and deterministic scenario grid/mapping.
- `P_EXPOSURE`: dealer-side assumptions, candidate leg quantities and stress grid; option revaluation itself is separately bound by `OptionRevaluationConventionVersion`.
- `P_UTILITY`: tail confidence, risk/utility coefficients and edge reserves.
- `P_ATTRIBUTION`: aligned path sampling convention, P&L gross/net-of-cost basis and attribution unit conversions.
- `P_EVALUATION`: evaluation window, target/outcome definition, bins, comparator/baseline and locked model version.
- `P_STATE_VECTOR`: ordered component schema only.
- `P_OFI`: OFI aggregation window and book-event matching tolerance.

## Appendix B — verified workbook dependency census

The exact reference workbook contains:

- 105 rows with direct raw dependencies and no workbook-derived dependency;
- 35 rows with both raw and derived dependencies;
- 66 rows with derived dependencies only;
- 3 rows with no explicit workbook signal dependency: D007, D204, D205;
- 111 distinct raw `Rxxx` identities in the transitive support of the 206 workbook-connected rows;
- 0 unresolved R references;
- 0 unresolved D references;
- 0 D dependency cycles.

These are evidence about the source workbook, not authority over this brief.

## Appendix C — companion D001–D209 catalogue

The complete row-level normative binding is `NVDA_DERIVED_SIGNAL_CATALOGUE.csv`.

Mechanical validation of that CSV must establish:

- exactly 209 data rows;
- exactly one occurrence of every identifier D001 through D209;
- exactly one admitted kernel binding per row;
- every `Rxxx` dependency resolves within R001–R323 in the reference workbook;
- every predecessor `Dxxx` dependency resolves within D001–D209;
- the resulting D graph is acyclic;
- each row retains its source workbook locator so reference provenance can be checked without making the workbook authoritative.

A new D identity, dependency edge, kernel move or row-specific context change is a brief/calculation-definition change, not an implementation convenience.

## Appendix D — Remaining Unknowns deliberately outside this draft

This draft does not choose:

- the numeric architecture module identifier;
- package/distribution name/version;
- Python public API spelling;
- whether a particular calculation kernel executes in owner service code, PostgreSQL functions/procedures or another implementation mechanism that preserves the accepted semantics;
- PostgreSQL schema/role names;
- table/index/partition layout;
- opaque occurrence-ID generation algorithm;
- provider/network implementations;
- performance/SLA/RTO/RPO targets; or
- concrete provider/native-field projection mappings and production parameter/context instances (including fee schedules and option-revaluation conventions), except for their required typed/versioned form and calculation constraints established above;
- downstream authority to act on any calculated value.

Those are later authority/mechanism questions. They may not change the accepted calculation semantics above without an explicit compatibility/version disposition.
