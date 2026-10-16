# Gate 2 — classification continuation and concrete decision proposals

Date: 17 October 2026 — Australia/Melbourne.

Status: assessment under the accepted root ExecPlan and A1–A7 overlay. Proposals below are not accepted domain amendments or Gate 2 acceptance. This is not a successor ExecPlan.

## 1. Baseline, scope and evidence limits

The continuation starts at `b002a3915dc8a5fbc54ba5f21e814afd87179e9b`, from the last delivered full-history archive `NVDA_V2_GATE_2_REPAIR_REVIEWED_BLOCKED_FULL_GIT_20261016.tar.gz`, SHA-256 `c4b66a525f6465d01ceca3663345a53d3808763943f6916e8fa6c574d95a0f68` (18,646,124 bytes). The initially available working copy was at `55c7c83`, rather than the last reviewed checkpoint. The exact later archive was recovered and its digest matched before extraction into a separate directory. The earlier working copy was preserved. Git integrity inspection of the recovered repository exited successfully; dangling historical objects were retained. The first metadata-helper invocation rejected a relative path; its absolute-path retry succeeded. Neither failed invocation is represented as a successful check.

Entry assessment is 209 identities: 100 conditional foundation proposals, 74 proposed non-foundation classifications, and 35 unresolved classifications. These are assessment states, not admitted owners. Accepted main remains `77d82bd8ee4268673715fe7e5653b6a65a299b54`.

The owner instructed completion of the planning/classification work. No API acquisition, integration, application execution, test execution, runtime catalogue/profile mutation, registry change or main merge is authorised. The separately uploaded September implementation-admission archive is not required for these questions; the owner explicitly directed continuation without it. It has not been inspected in this continuation.

Inspected primary sources for the units below: root governance and accepted ExecPlan; master ADR-WBV2-003; ADR-WBV2-001/002; full effective mathematical brief; effective catalogue rows; accepted D117/D123 amendments; original workbook Raw Signals entries cited by the affected rows. Existing G2.2/G2.3 row evidence is navigation, not a substitute for the explicit primary rules cited below. Source excerpts and call-path inspection are documentary evidence only. No new full-population implementation review or runtime proof is claimed.

## 2. D091: concrete neutral partition proposal

**Decision ID: G2-DELTA-MEASUREMENT-20261017-01. State: PROPOSED.**

The accepted brief §5 K08 specifies bucketing absolute R112 delta by non-overlapping versioned boundaries and deterministic inclusion. It does not specify numerical boundaries. The catalogue's 10/25/50 labels are examples, not an admitted partition. The original raw workbook identifies R112 as model option-computation delta in dimensionless units; this establishes the intended input vocabulary, not actual acquisition conformity.

Recommend the following first measurement version. The additional 75/90 labels make the partition explicit across the entire permitted delta domain. They are new proposed convention choices, not recovered authority or a claim about an industry standard.

| Label | Absolute-delta interval |
| --- | --- |
| `delta_10` | `[0, 0.175)` |
| `delta_25` | `[0.175, 0.375)` |
| `delta_50` | `[0.375, 0.625)` |
| `delta_75` | `[0.625, 0.825)` |
| `delta_90` | `[0.825, 1]` |

Use exact decimal/rational comparisons. Interior boundaries belong to the upper interval; `1` belongs to the final interval. Refuse non-finite values and absolute delta outside `[0,1]`. Preserve call/put sign and right in input lineage; the bucket operation uses absolute delta only. Do not round delta, interpolate a missing delta, silently substitute bid/ask delta for model R112, or select a contract because it is a trade candidate. Exactly one same-contract R112 observation is selected under the declared cutoff/version policy. Changing the partition or input variant creates a separately identifiable measurement version; a strategy cannot redefine this version.

These thresholds are the midpoints between the declared measurement centres 0.10, 0.25, 0.50, 0.75 and 0.90. This is an explicit reproducible design rationale, not empirical optimisation or proof of market suitability. No score weight, predictive coefficient, candidate, position or action threshold enters the category.

**Approval effect:** if the owner accepts this exact convention, D091 may be reassessed for conditional foundation eligibility under A1/A2; actual R112 selection/mapping/conformity is separate. This proposal does not itself close G2I-007 or certify a source.

### 2.1 D109: matching is a separate obligation

D109's accepted arithmetic is `ATM_call_mid + ATM_put_mid`, with D087 and D091 predecessors. Bucket establishment alone does not select a unique straddle. The common selection must preserve identical underlying, source namespace, expiry, strike, multiplier/deliverable identity and compatible currency/units, with opposite call/put rights and distinct exact contract identities. Both selected D091 categories must be `delta_50` from the same accepted partition version. Their D087 quote midpoints must have matching exact contract identities and satisfy the same cutoff and declared freshness/skew policy. Missing or duplicate authoritative occurrences refuse.

**Recommended bounded first mode:** evaluate one exact expiry over the declared complete eligible contract universe. Emit only if there is exactly one common-strike call/put pair meeting the requirements; otherwise refuse. Do not choose the lowest strike, nearest database row, lexically first contract ID or first returned pair. This deliberately preserves ambiguity as refusal. Selecting a closest-to-50-delta pair among several would require a separately authorised exact selection rule and lawful access to the numerical delta; the D091 category alone cannot establish that ranking. No hidden R112 edge is added to D109.

This restricted matching mode is part of decision `G2-DELTA-MEASUREMENT-20261017-01`. It is not an assertion that a valid pair will usually exist. D109 remains unresolved until the required convention and source treatment are accepted.

### 2.2 D110: a distinct denominator and join

D110 remains `100 * D109 / R118`. Use the same underlying/expiry/source and compatible currency as the selected straddle, with a positive finite aligned model-underlying price and the declared cutoff/skew law. Refuse a mismatched or missing spot occurrence; do not substitute an underlying trade from another source. Resolving D091 alone does not establish this R118 join. No arithmetic or dependency amendment is proposed.

### 2.3 D121: aggregation-time labels must be explicit

D121 retains D120 and D091. Recommend separate fixed 60-second, 300-second and session-to-cutoff measurement versions. Rolling intervals are `(T-W,T]` on the permitted preserved receipt basis; session mode uses the versioned session opening through T. Select one complete D120 window result per exact contract and one D091 category for the same contract at T, under one declared input policy. Aggregate both D120 `signed_contracts` and `signed_premium_notional` by `(expiry, option_right, delta_bucket)`, preserving the complete contract set, units and occurrence identities. Refuse missing/duplicate labels, incompatible windows or conflicting identities. An empty universe is not an observed zero.

This first proposal labels the whole contract-window flow using the **window-end** delta category. It does not claim trade-time delta attribution. A trade-time version would need its own definition and event-level input closure; an implementation must not choose between the two silently. D120's native R016 multiplier amendment remains effective. Decision `G2-DELTA-MEASUREMENT-20261017-01` includes this explicit interpretation; no current definition is changed before acceptance.

## 3. D122: remove an arbitrary horizon selector from the proposed first mode

**Decision ID: G2-EXPIRY-FLOW-MEASUREMENT-20261017-01. State: PROPOSED.**

The accepted K08 law groups D120 by parameter-defined expiry/DTE buckets; D085 is calendar days to expiry, not trading days. Recommend an exact-day partition: for every integer `n >= 0`, label `DTE_n` contains precisely D085=`n`. Preserve exact expiry as a separate group key, rather than pooling different expiries merely because their day count agrees. This defines the entire domain without an arbitrary 0–7/8–30/long-dated trading-horizon choice.

Use the same fixed 60-second, 300-second and session-to-cutoff window variants as §2.3; join D120 and D085 by exact option identity, source/context and the same window endpoint. Require non-negative integer DTE under the accepted exchange-local calendar law. Sum both signed-contract and signed-premium-notional components, preserving the complete universe and no-missing-as-zero rule. Negative/non-integer/missing DTE or incomplete joins refuse. This does not add a dependency, alter D085 day-count mathematics, or make D121's pending delta decision a prerequisite for D122.

If accepted, this resolves the discretionary-band choice for the first D122 mode. The numerical/source/conformity and classification conclusions must still be recorded separately; approval is not Gate 2 acceptance.

## 4. D124: test the claimed blocker against the effective authority

The original catalogue concept says strike/expiry **or** spot-distance concentration. The controlling brief's explicit K08 row requires each strike/expiry share of total relevant OI plus `HHI = sum(share_i^2)` on `[0,1]`; total OI must be positive. Direct inputs are R047/R048. No spot-price input is declared. Thus missing spot-distance bands do not, by themselves, prove that the explicit strike/expiry mode is undefined. A spot-distance implementation cannot silently introduce an undeclared spot path.

The exact-contract/right join, neutral eligible-universe domain, cutoff/vintage selection, non-negative OI and positive total remain distinct obligations; N8 proposes the still-unaccepted universe/vintage contract. For a complete declared universe, aggregate the appropriate call R047 or put R048 facts by `(strike, expiry)`, then divide each grouped OI by the positive universe total. Both-right aggregate membership is explicit; an unavailable right is not silently zero. No official-period *change* is computed, so D123's two-period equation is not inherited merely because both use OI.

**Assessment submitted for independent review:** the explicit strike/expiry mode supports a bounded foundation recommendation, but current D124 remains UNKNOWN because its neutral universe/vintage contract is still proposed; operational source-version conformity is a different hold. Do not claim that arbitrary selected trading baskets or an unproved spot-distance mode qualify. A classification correction will be recorded only after checking this scope against the existing authority; no new concentration mathematics is proposed.

## 5. D132: application scope does not prove numerical candidate dependence

The effective catalogue's `applicable_universe` is **Candidate and neighbouring options**. Its K07/P_SCORE output combines spread, size, depth, frequency and volume. That application scope is positive evidence requiring investigation, but does not independently prove that a candidate or neighbour relation enters the numerical definition. A context-free score could be applied to a consumer-selected contract. K07's explicit candidate/neighbour comparison law governs D173, not D132. D132 has no declared candidate typed context.

**Current finding: retain UNKNOWN.** The independent reviewer identified the narrower-evidence/broader-claim error in the initial draft. The earlier progress statement that candidate scope definitely excludes D132 is withdrawn. No register promotion followed that statement. Exact P_SCORE semantics are still needed to distinguish a neutral liquidity measurement from a tuned/discretionary assessment. A future fixed whole-market measurement is not presumed, and missing weights alone do not prove a downstream disqualifier. Preserve G2I-001 and G2I-021 as open. Other eight score rows require their own evidence.

## 6. Remaining classification units

The following sections are completed unit by unit from their own primary definitions. A new proposal is always identified as such; an unproved source fact is never converted into an approval or a live-data requirement.


### 6.1 Complete 35-row decision coverage

This table accounts for all 35 entry UNKNOWN identities exactly once. It is a review of the outstanding classification questions, not 35 resolved outcomes. Current classifications remain unchanged until their own evidence/authority is sufficient. The named source-feasibility, role and domain changes are proposals. The other 174 rows retain their existing assessment; no fresh exhaustive implementation review is claimed.

| D | Separate primary-rule finding | Concrete proposed decision |
| --- | --- | --- |
| D006 | Age/status/cadence P_SCORE is not supplied by the age equation; propose authored assessment role, not inferred tuning. | S1 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D008 | Structured skew/coverage metrics and bounded score are one canonical output; do not split identity or infer a neutral score schema. | S1 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D040 | Exact trend feature extractors/orientations/weights remain authored model inputs; S1 decides intended role. | S1 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D041 | Retain D040 and volatility/price-deviation closure; no generic score decision deletes the parent. | S1 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D061 | Volatility arithmetic predecessors are neutral candidates; the composite assessment role is a separate proposed decision. | S1 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D062 | Calendar-scope/relevance choice separated from D065 policy gate; exact timestamp/vintage native supply unproved. | N2 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D063 | Same release/series/period/units and pre-release consensus, initially published actual, comparable strictly prior surprise baseline; provider TBD. | N2 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D064 | S1 role plus independent R289/native event/vintage obligation; closing score-role does not establish macro source supply. | S1 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D070 | Market return inputs do not themselves establish neutral composite feature weighting. | S1 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D078 | Residual uses current aligned factors and one exact coherent fit; no independently selected beta versions. | N3 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D079 | OLS market coefficient uses dependent D075 plus all accepted covariates, full common sample and fit identity. | N3 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D080 | OLS technology coefficient is from same multivariate fit; not an independent QQQ-only regression. | N3 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D081 | OLS semiconductor coefficient is from same multivariate fit; no fitted scenario coefficient substituted. | N3 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D082 | Pearson matrix has one complete aligned market-only sample and fixed basket; basket weights are not an implicit alternative estimator. | N4 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D084 | Exact technology/semiconductor/dispersion extraction and weights remain model inputs under proposed S1. | S1 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D091 | Existing K08 family permits exact versioned partitions. Missing production numbers alone is not the issue; current A1 expressibility/source treatment remains explicit. | N5 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D102 | Risk-neutral descriptive fit is distinct from physical forecast. Concrete pricing-convention market-only full input closure remains required, even if B accepted. | N6 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D109 | D091 improvement does not identify a unique ATM common-strike pair; same-expiry/right/contract/source and cutoff joins remain separate. | N5 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D110 | Retains D109 plus positive finite aligned R118 denominator; no source/underlying mismatch. | N5 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D111 | Call-price convex spline/density plus same-snapshot D102 quality; D102 residual is not a price object. Concrete revaluation closure inherited. | N6 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D112 | Tail integration requires exact grid/threshold role and D111; strategy-selected barrier is not the proposed shared measurement. | N6 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D113 | Upper-tail integration independently requires exact grid/threshold role and D111; no blanket inference from D112. | N6 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D117 | R041-only and accepted P1-P5 unchanged; B2 explicitly proposes a different receiving stage for retained P6 source/calendar feasibility. | N7 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D121 | Requires explicit window-end versus trade-time category interpretation; N5 proposes window-end first mode, preserving both D120 components. | N5 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D122 | Exact-day DTE partition proposal is independent of D091; new first-mode choice remains proposed. | N8 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D123 | Controlled official-period/revision fields remain provider-independent; no two-receipt substitute or new official-period fact. | N7 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D124 | K08 explicit strike/expiry share+HHI needs no optional spot bands; neutral universe and OI vintage/completeness contract are still proposed. | N8 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D132 | Candidate application scope alone does not prove candidate-dependent mathematics; retain UNKNOWN pending explicit score-role/schema. | S1 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D138 | Standing cumulative depth, matched D011, per-side OLS and selected visible-depth sufficiency; separate from OFI transition warm-up. | N9 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D139 | Insertion count/size rate by position bucket; retain exact declared R list and stable ordered book state. | N9 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D140 | Deletion size is immediately pre-delete row size, not zero payload; source reset/gap invalidates window. | N9 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D141 | First qualifying same-price restoration, one match per depletion and capped size; no causal hidden-trader assertion. | N9 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D142 | Joint depth-and-spread recovery; explicit measurement trigger/window, no filled result for incomplete recovery. | N9 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D145 | Consecutive best states, valid left-boundary predecessor, all transitions, fixed windows, reset/generation refusal; approved five R retained. | N9 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |
| D151 | Three breadth components and denominators retained; fixed market basket/count-or-weight mode excludes portfolio/candidate selection. | N10 in `G2_CLASSIFICATION_CONTRACT_DECISIONS_PROPOSED_20261017.md` |

## 7. Individual audit of the 53 convention flags

Each flag was compared with its effective catalogue inputs, parameter/window and accepted kernel/row law. `FIXED_LAW` means the flag does not by itself expose a new mathematical choice; actual source/profile binding still needs evidence. `MEASUREMENT_DOMAIN` means a real selection/convention obligation remains, whose exact neutral domain must be settled where classification-relevant. Neither label claims source sufficiency or production instance acceptance. The audit does not erase the flag or close G2I-020 wholesale.

| D | Audit distinction | Exact requirement / remaining binding |
| --- | --- | --- |
| D001 | FIXED_LAW | True-instant-only UTC conversion; offset/timezone and native temporal-kind binding required, never invent event time. |
| D002 | FIXED_LAW | Typed source-event or collector-receipt age; date-only refuses seconds, negative age invalid. |
| D003 | FIXED_LAW | Preserve instant; bind official instrument IANA zone, no strategy parameter. |
| D004 | MEASUREMENT_DOMAIN | Exact source session/trading-date calendar including overnight boundaries; concrete calendar binding still required. |
| D005 | MEASUREMENT_DOMAIN | Ordered nonoverlapping phase schedule, inclusion and uncovered-time refusal; named morning/midday boundaries are not supplied by labels. |
| D009 | FIXED_LAW | Accepted initial/latest-known-at-cutoff/revised mutually exclusive vintage law; native revision history binding remains required. |
| D010 | MEASUREMENT_DOMAIN | Official market-open state and declared RTH/liquid phase; no strategy liquidity/activation threshold. |
| D015 | FIXED_LAW | Quote test then last-different-price tick test then 0/unknown; exact subject/time/quote joins and no guessed sign. |
| D016 | MEASUREMENT_DOMAIN | Separate fixed 1s/5s/60s/300s windows; exact signed-size event set and no duplicated trades. |
| D019 | FIXED_LAW | Exact one-minute log-return aligned anchor; latest eligible at/before anchor, no look-forward. |
| D020 | FIXED_LAW | Exact five-minute log-return aligned anchor; sufficient complete source window required. |
| D021 | FIXED_LAW | Exact thirty-minute log-return aligned anchor; no shortened substitute. |
| D022 | FIXED_LAW | Current versus exact same-session open; declared source/calendar and knowledge cutoff. |
| D023 | FIXED_LAW | Current premarket/open versus prior official close; overnight/session anchor explicit. |
| D024 | FIXED_LAW | Accepted q1/q5/q30 and acceleration differences; all three matched horizons required. |
| D026 | FIXED_LAW | Accepted price and percent difference versus VWAP; legacy optional sigma is not part of current definition. |
| D027 | FIXED_LAW | Five-minute VWAP change, both price/minute and percent/minute; exact elapsed time and anchor. |
| D028 | MEASUREMENT_DOMAIN | Cumulative/session-volume ratio to strictly prior mean at same elapsed session coordinate; N, matching and R044 role require exact baseline domain. |
| D029 | MEASUREMENT_DOMAIN | Bar-volume z-score; immutable 20-60-session same-time baseline, sample SD; do not substitute D117 cumulative volume. |
| D030 | MEASUREMENT_DOMAIN | Trade-rate z-score; immutable 20-60-session same-time baseline and native R062 rate meaning. |
| D031 | MEASUREMENT_DOMAIN | Volume-rate z-score; immutable 20-60-session same-time baseline and native R063 rate meaning. |
| D044 | MEASUREMENT_DOMAIN | 1d/5d source-series anchor variants, decimal-rate to bps conversion; publication/holiday/vintage calendar fixed, no fabricated daily observations. |
| D045 | MEASUREMENT_DOMAIN | 1d/5d source-series anchor variants, decimal-rate to bps conversion; publication/holiday/vintage calendar fixed, no fabricated daily observations. |
| D046 | MEASUREMENT_DOMAIN | 1d/5d source-series anchor variants, decimal-rate to bps conversion; publication/holiday/vintage calendar fixed, no fabricated daily observations. |
| D048 | MEASUREMENT_DOMAIN | 1d/5d/20d source-series percent-change variants; exact source release/calendar anchors, no inferred intraday history. |
| D049 | MEASUREMENT_DOMAIN | 1d/5d percent-change variants; preserve quoted FX orientation, native series calendar/vintage and anchor. |
| D050 | MEASUREMENT_DOMAIN | 1d/5d percent-change variants; preserve quoted FX orientation, native series calendar/vintage and anchor. |
| D051 | MEASUREMENT_DOMAIN | 1d/5d percent-change variants; preserve quoted FX orientation, native series calendar/vintage and anchor. |
| D052 | MEASUREMENT_DOMAIN | Separate 5m/1h/1d point-and-percent changes only where native temporal resolution/history supports horizon; date-only does not supply intraday anchors. |
| D053 | MEASUREMENT_DOMAIN | Separate 5m/1h/1d point-and-percent changes only where native temporal resolution/history supports horizon; date-only does not supply intraday anchors. |
| D054 | MEASUREMENT_DOMAIN | Separate 5m/1h/1d point-and-percent changes only where native temporal resolution/history supports horizon; date-only does not supply intraday anchors. |
| D055 | MEASUREMENT_DOMAIN | Separate 5m/1h/1d point-and-percent changes only where native temporal resolution/history supports horizon; date-only does not supply intraday anchors. |
| D056 | MEASUREMENT_DOMAIN | Separate 5m/1h/1d point-and-percent changes only where native temporal resolution/history supports horizon; date-only does not supply intraday anchors. |
| D066 | MEASUREMENT_DOMAIN | Daily log-return source-index/calendar/proxy identity and exact daily anchor; no discretionary substitute index or timezone day. |
| D067 | MEASUREMENT_DOMAIN | Daily log-return source-index/calendar/proxy identity and exact daily anchor; no discretionary substitute index or timezone day. |
| D068 | MEASUREMENT_DOMAIN | Daily log-return source-index/calendar/proxy identity and exact daily anchor; no discretionary substitute index or timezone day. |
| D069 | MEASUREMENT_DOMAIN | Daily log-return source-index/calendar/proxy identity and exact daily anchor; no discretionary substitute index or timezone day. |
| D071 | MEASUREMENT_DOMAIN | Exact instrument/proxy and current/prior-close anchor in R037/R042, fixed source/calendar; do not silently substitute session-open branch. |
| D072 | MEASUREMENT_DOMAIN | Exact instrument/proxy and current/prior-close anchor in R037/R042, fixed source/calendar; do not silently substitute session-open branch. |
| D073 | MEASUREMENT_DOMAIN | Exact instrument/proxy and current/prior-close anchor in R037/R042, fixed source/calendar; do not silently substitute session-open branch. |
| D074 | MEASUREMENT_DOMAIN | Exact instrument/proxy and current/prior-close anchor in R037/R042, fixed source/calendar; do not silently substitute session-open branch. |
| D075 | MEASUREMENT_DOMAIN | Exact instrument/proxy and current/prior-close anchor in R037/R042, fixed source/calendar; do not silently substitute session-open branch. |
| D083 | MEASUREMENT_DOMAIN | Contemporaneous market-only basket, complete member set, N>=2 and sample SD; no historical P_BASELINE or portfolio universe. |
| D085 | FIXED_LAW | Whole calendar-day expiry minus exchange-local trading date; negative invalid for live contract, not trading-day count. |
| D086 | MEASUREMENT_DOMAIN | Accepted ACT/365F to exact versioned instrument expiry instant; no invented midnight or guessed exercise cutoff. |
| D094 | MEASUREMENT_DOMAIN | Five-minute matched-contract/bucket IV change in vol points; concrete matching, cutoff and source IV variant fixed. |
| D095 | MEASUREMENT_DOMAIN | One-trading-day comparable IV anchor; source calendar/vintage and contract/bucket comparability fixed. |
| D096 | MEASUREMENT_DOMAIN | Accepted nearest bracketing linear absolute-delta interpolation at .50, call/put coverage explicit; no implicit extrapolation or single-side mode. |
| D103 | MEASUREMENT_DOMAIN | Exact grid common to two declared snapshots/horizon, mean IV-point shift; preserve matched members, no unmatched substitution. |
| D104 | MEASUREMENT_DOMAIN | Corresponding D099/D100 skew difference over fixed 5m/1h/1d anchor; no unproved extra spot-control transformation. |
| D105 | FIXED_LAW | Full prior comparable one-year min/max rank, range positive; no shortened year or current-as-own-baseline. |
| D106 | FIXED_LAW | Full prior comparable one-year strict-less plus half-tie percentile divided by N; no arbitrary tie policy. |
| D120 | MEASUREMENT_DOMAIN | Exact signed-contract and premium-notional sums, same-event quote/sign and native R016 multiplier; fixed 60s/300s/session universe and no receipt-ID grouping. |

Flag audit totals: 16 FIXED_LAW, 37 MEASUREMENT_DOMAIN. These are categories of reading findings, not accepted completion counts.

## 8. Responsibility coverage and explicit conditional scenario

The current accepted/current-assessment population is unchanged: **100 conditional foundation proposals, 74 proposed non-foundation, 35 UNKNOWN**. No new runtime owner is assigned. The historical 95 memberships, 30 groups and 107 direct cross-group references remain unchanged.

For reviewing the proposed decisions only, consider the explicit **unaccepted scenario** in which S1 assigns the nine scores downstream and every one of the other 26 disputed rows satisfies its neutral contract and source/authority treatment. That gives 126 hypothetical foundation rows and 83 hypothetical downstream rows. This arithmetic assumes N6 selected-convention closure and every other retained condition; it is not a candidate acceptance result and must not replace current classifications.

| Historical group | Hypothetical canonical downstream members after all named decisions |
| --- | --- |
| P01 | D006, D007, D008, D158 |
| P02 | D040, D041, D061, D070, D084, D132 |
| P03 | D064, D065 |
| P07 | D114, D115 |
| P08 | D125, D126, D127, D128, D129, D130 |
| P10 | D146, D147, D148, D149, D150 |
| P11 | D152, D153, D154 |
| P12 | D155 |
| P13 | D156, D157 |
| P14 | D159 |
| P15 | D160 |
| P16 | D161, D162, D168, D169, D170, D174 |
| P17 | D133, D164 |
| P18 | D163, D165, D166, D167 |
| P19 | D171, D172, D173 |
| P20 | D175, D176 |
| P21 | D177, D178 |
| P22 | D179, D180, D193 |
| P23 | D181, D182, D183, D184, D185 |
| P24 | D186, D187 |
| P25 | D188, D190, D191 |
| P26 | D189, D192 |
| P27 | D194, D195, D196, D197, D198, D199 |
| P28 | D200, D201 |
| P29 | D202, D203, D204, D205, D206, D207, D208 |
| P30 | D209 |

This scenario retains 26 nonempty historical responsibilities. P04/P05/P06/P09 would have no downstream canonical output only under the stated assumptions. P06 in particular cannot be declared empty while N6 remains unproved. Empty proposed groups are not retired runtime modules; they are research labels. No renumbering or admission is authorised.

For every retained peer, all non-foundation intermediate chains remain private/local to that peer, with singular canonical D ownership and lawful M00/admitted-foundation ingress. Historical D-to-D edges do not become peer runtime calls. Actual recursive implementation reuse/namespace/persistence/test design remains C–E; this pass does not claim those implementations exist. The existing full G2.3 closure remains the row-level lineage source, not a runtime coupling map.

## 9. Exact remaining decision boundary

The scope/role/domain package is `G2-CONTRACT-CLASSIFICATION-20261017-01`. B expressly changes the earlier source-feasibility prerequisite; S expressly chooses intended score roles; N defines bounded neutral measurement proposals. None is recorded as accepted. Even accepting the package does not settle N6 selected-revaluation full closure, all concrete ATM/event-profile conditions, final groups or Gate 2 exit. The worker must continue those dependent units after the relevant authority/inputs are available, then seek separate Gate 2 acceptance. No successor ExecPlan is drafted or activated in this pass.

Independent review of this continuation and the exact candidate will be recorded below after it occurs. The entry repair PASS remains limited to its own earlier repair.

## 10. Documentary verification

Read-only parsing compared the three registers with entry `b002a39`: unchanged schemas 111/25/19 columns, populations 209/21/124 and every non-PB cell unchanged. Only the four explicit planning/source/proposal fields changed. The effective 209-D graph resolves and is acyclic; no equation/dependency change was made. Guardrails, agents, frozen ExecPlan and effective catalogue digests matched their pinned values. Accepted main remained `77d82bd8ee4268673715fe7e5653b6a65a299b54`. Markdown/diff whitespace inspection passed before candidate commit.

The first original/Pass08 workbook comparator stopped on an `IndexError` because it indexed a zero-length worksheet row. That attempt did not establish workbook equality. After explicitly admitting empty worksheet rows as non-D rows, the comparator independently required exactly 209 unique D identities in each sheet and equality of all their first 15 cells; that check passed. This is mechanical source-cell readback, not a fresh semantic certification of all 209 rows. No application tests, imports, validators, database or provider operations ran.
