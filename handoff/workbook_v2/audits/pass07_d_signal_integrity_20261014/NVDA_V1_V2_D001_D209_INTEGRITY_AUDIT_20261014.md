# NVDA — D001–D209 original-to-V2 preservation and allocation audit

**Result: PASS** — 209 original signal designations checked against their preserved V2 source and proposed module allocation.

## Scope and authority

- Audit compares the **original V1 Excel `Derived Signals` tab** with the **Pass 06 V2 Excel `Derived Signals` tab** and its M01-1/M02–M31 allocation worksheets.
- The V1 workbook is the original research catalogue; the M01 implementation's normative CSV remains its own authority. This check does not establish mathematical/test correctness or approve new architecture.
- Every row is checked for exact D-ID, source name, original-tab retention, exactly-one proposed-module allocation, and matching names/module index. All populated values and formula text of the original `Derived Signals` sheet are compared against its retained V2 copy.

## Inspected artefacts

- V1: `implementation/authority/source_signal_catalogue/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx` (SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`)
- V2: `handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS06.xlsx` (SHA-256 `2a36468fd83d16379861f330f929994a5a6d0a366c4953dbc03511bc0ad7b64c`)
- Proposed module allocations remain review designations; M01-1 and M02–M31 have not been admitted as production module identities.

## Reconciliation

| Measure | Observed |
|---|---:|
| Unique V1 D-identifiers | 209 |
| Unique retained V2 D-identifiers | 209 |
| M01-1 worksheet entries | 114 |
| M02–M31 worksheet entries | 95 |
| M02–M31 allocation-index entries | 95 |
| Missing module assignments | 0 |
| Extra module assignments | 0 |
| Multiply allocated D-identifiers | 0 |
| V1-to-V2 original sheet cell-content match | YES |
| Individually passing D rows | 209 / 209 |

## Complete row-by-row audit

`V1` confirms presence in the first workbook. `V2 retained` confirms the same ID/name remains in its preserved source worksheet. `Module` and `Module location` identify the proposed allocation (not a new canonical D-ID).

| D-ID | Original V1 signal name | V1 present | V2 retained | Proposed module | Module location | Allocation count | Result |
|---|---|---|---|---|---|---:|---|
| D001 | Canonical event timestamp UTC | YES | YES | M01-1 | `M01-1!A6` | 1 | PASS |
| D002 | Observation/source age | YES | YES | M01-1 | `M01-1!A7` | 1 | PASS |
| D003 | Market-local timestamp | YES | YES | M01-1 | `M01-1!A8` | 1 | PASS |
| D004 | Exchange-local trading date | YES | YES | M01-1 | `M01-1!A9` | 1 | PASS |
| D005 | Market session phase | YES | YES | M01-1 | `M01-1!A10` | 1 | PASS |
| D006 | Quote staleness score | YES | YES | M02 | `M02!A5` | 1 | PASS |
| D007 | Required-field completeness ratio | YES | YES | M02 | `M02!A6` | 1 | PASS |
| D008 | Cross-source temporal alignment quality | YES | YES | M02 | `M02!A7` | 1 | PASS |
| D009 | Macro series revision/vintage status | YES | YES | M01-1 | `M01-1!A11` | 1 | PASS |
| D010 | Market-open/liquid-session flag | YES | YES | M01-1 | `M01-1!A12` | 1 | PASS |
| D011 | Bid-ask midpoint | YES | YES | M01-1 | `M01-1!A13` | 1 | PASS |
| D012 | Absolute bid-ask spread | YES | YES | M01-1 | `M01-1!A14` | 1 | PASS |
| D013 | Relative bid-ask spread | YES | YES | M01-1 | `M01-1!A15` | 1 | PASS |
| D014 | Top-of-book size imbalance | YES | YES | M01-1 | `M01-1!A16` | 1 | PASS |
| D015 | Trade direction proxy | YES | YES | M01-1 | `M01-1!A17` | 1 | PASS |
| D016 | Signed trade volume | YES | YES | M01-1 | `M01-1!A18` | 1 | PASS |
| D017 | System-computed session VWAP | YES | YES | M01-1 | `M01-1!A19` | 1 | PASS |
| D018 | IBKR VWAP versus system VWAP difference | YES | YES | M01-1 | `M01-1!A20` | 1 | PASS |
| D019 | 1-minute log return | YES | YES | M01-1 | `M01-1!A21` | 1 | PASS |
| D020 | 5-minute log return | YES | YES | M01-1 | `M01-1!A22` | 1 | PASS |
| D021 | 30-minute log return | YES | YES | M01-1 | `M01-1!A23` | 1 | PASS |
| D022 | Session-to-date return | YES | YES | M01-1 | `M01-1!A24` | 1 | PASS |
| D023 | Overnight/pre-market gap | YES | YES | M01-1 | `M01-1!A25` | 1 | PASS |
| D024 | Return acceleration/deceleration | YES | YES | M01-1 | `M01-1!A26` | 1 | PASS |
| D025 | Position within session high-low range | YES | YES | M01-1 | `M01-1!A27` | 1 | PASS |
| D026 | Price deviation from VWAP | YES | YES | M01-1 | `M01-1!A28` | 1 | PASS |
| D027 | VWAP rate of change | YES | YES | M01-1 | `M01-1!A29` | 1 | PASS |
| D028 | Relative volume versus normal time-of-day | YES | YES | M01-1 | `M01-1!A30` | 1 | PASS |
| D029 | Volume z-score | YES | YES | M01-1 | `M01-1!A31` | 1 | PASS |
| D030 | Trade-rate z-score | YES | YES | M01-1 | `M01-1!A32` | 1 | PASS |
| D031 | Volume-rate z-score | YES | YES | M01-1 | `M01-1!A33` | 1 | PASS |
| D032 | 5-minute realised volatility | YES | YES | M01-1 | `M01-1!A34` | 1 | PASS |
| D033 | 30-minute realised volatility | YES | YES | M01-1 | `M01-1!A35` | 1 | PASS |
| D034 | Intraday/session realised volatility | YES | YES | M01-1 | `M01-1!A36` | 1 | PASS |
| D035 | 5-day realised volatility | YES | YES | M01-1 | `M01-1!A37` | 1 | PASS |
| D036 | 10-day realised volatility | YES | YES | M01-1 | `M01-1!A38` | 1 | PASS |
| D037 | 20-day realised volatility | YES | YES | M01-1 | `M01-1!A39` | 1 | PASS |
| D038 | Jump-variation estimate | YES | YES | M01-1 | `M01-1!A40` | 1 | PASS |
| D039 | 5-minute average true range | YES | YES | M01-1 | `M01-1!A41` | 1 | PASS |
| D040 | Trend strength score | YES | YES | M03 | `M03!A5` | 1 | PASS |
| D041 | Mean-reversion score | YES | YES | M03 | `M03!A6` | 1 | PASS |
| D042 | 2s10s Treasury slope | YES | YES | M01-1 | `M01-1!A42` | 1 | PASS |
| D043 | 3m10y Treasury slope | YES | YES | M01-1 | `M01-1!A43` | 1 | PASS |
| D044 | 10-year real-yield change | YES | YES | M01-1 | `M01-1!A44` | 1 | PASS |
| D045 | 10-year nominal-yield change | YES | YES | M01-1 | `M01-1!A45` | 1 | PASS |
| D046 | 10-year breakeven-inflation change | YES | YES | M01-1 | `M01-1!A46` | 1 | PASS |
| D047 | SOFR minus effective Fed funds spread | YES | YES | M01-1 | `M01-1!A47` | 1 | PASS |
| D048 | Broad USD rate of change | YES | YES | M01-1 | `M01-1!A48` | 1 | PASS |
| D049 | JPY/USD rate of change | YES | YES | M01-1 | `M01-1!A49` | 1 | PASS |
| D050 | HKD/USD rate of change | YES | YES | M01-1 | `M01-1!A50` | 1 | PASS |
| D051 | CNY/USD rate of change | YES | YES | M01-1 | `M01-1!A51` | 1 | PASS |
| D052 | VIX change | YES | YES | M01-1 | `M01-1!A52` | 1 | PASS |
| D053 | VVIX change | YES | YES | M01-1 | `M01-1!A53` | 1 | PASS |
| D054 | VIX1D change | YES | YES | M01-1 | `M01-1!A54` | 1 | PASS |
| D055 | VIX9D change | YES | YES | M01-1 | `M01-1!A55` | 1 | PASS |
| D056 | VIX3M change | YES | YES | M01-1 | `M01-1!A56` | 1 | PASS |
| D057 | VIX1D-to-VIX9D term slope | YES | YES | M01-1 | `M01-1!A57` | 1 | PASS |
| D058 | VIX9D-to-VIX term slope | YES | YES | M01-1 | `M01-1!A58` | 1 | PASS |
| D059 | VIX-to-VIX3M term slope | YES | YES | M01-1 | `M01-1!A59` | 1 | PASS |
| D060 | VVIX/VIX ratio | YES | YES | M01-1 | `M01-1!A60` | 1 | PASS |
| D061 | Composite US volatility regime score | YES | YES | M03 | `M03!A7` | 1 | PASS |
| D062 | Time to next scheduled event | YES | YES | M04 | `M04!A5` | 1 | PASS |
| D063 | Standardised macro surprise | YES | YES | M01-1 | `M01-1!A61` | 1 | PASS |
| D064 | Event importance score | YES | YES | M04 | `M04!A6` | 1 | PASS |
| D065 | Active event-window flag | YES | YES | M04 | `M04!A7` | 1 | PASS |
| D066 | Nikkei 225 return | YES | YES | M01-1 | `M01-1!A62` | 1 | PASS |
| D067 | Hong Kong index return | YES | YES | M01-1 | `M01-1!A63` | 1 | PASS |
| D068 | China index return | YES | YES | M01-1 | `M01-1!A64` | 1 | PASS |
| D069 | China technology index return | YES | YES | M01-1 | `M01-1!A65` | 1 | PASS |
| D070 | International overnight risk score | YES | YES | M03 | `M03!A8` | 1 | PASS |
| D071 | SPY/S&P proxy intraday return | YES | YES | M01-1 | `M01-1!A66` | 1 | PASS |
| D072 | QQQ/Nasdaq-100 proxy intraday return | YES | YES | M01-1 | `M01-1!A67` | 1 | PASS |
| D073 | SMH semiconductor ETF intraday return | YES | YES | M01-1 | `M01-1!A68` | 1 | PASS |
| D074 | SOXX semiconductor ETF intraday return | YES | YES | M01-1 | `M01-1!A69` | 1 | PASS |
| D075 | NVDA intraday return | YES | YES | M01-1 | `M01-1!A70` | 1 | PASS |
| D076 | Technology relative strength versus broad market | YES | YES | M01-1 | `M01-1!A71` | 1 | PASS |
| D077 | Semiconductor relative strength versus technology | YES | YES | M01-1 | `M01-1!A72` | 1 | PASS |
| D078 | NVDA residual/idiosyncratic return | YES | YES | M01-1 | `M01-1!A73` | 1 | PASS |
| D079 | Conditional NVDA market beta | YES | YES | M01-1 | `M01-1!A74` | 1 | PASS |
| D080 | Conditional NVDA technology beta | YES | YES | M01-1 | `M01-1!A75` | 1 | PASS |
| D081 | Conditional NVDA semiconductor beta | YES | YES | M01-1 | `M01-1!A76` | 1 | PASS |
| D082 | Rolling NVDA-market/sector correlations | YES | YES | M01-1 | `M01-1!A77` | 1 | PASS |
| D083 | Cross-sectional market/sector dispersion proxy | YES | YES | M01-1 | `M01-1!A78` | 1 | PASS |
| D084 | Sector rotation score | YES | YES | M03 | `M03!A9` | 1 | PASS |
| D085 | Calendar days to expiry | YES | YES | M01-1 | `M01-1!A79` | 1 | PASS |
| D086 | Time to expiry in years | YES | YES | M01-1 | `M01-1!A80` | 1 | PASS |
| D087 | Option midpoint | YES | YES | M01-1 | `M01-1!A81` | 1 | PASS |
| D088 | Option relative spread | YES | YES | M01-1 | `M01-1!A82` | 1 | PASS |
| D089 | Spot moneyness | YES | YES | M01-1 | `M01-1!A83` | 1 | PASS |
| D090 | Log-moneyness | YES | YES | M01-1 | `M01-1!A84` | 1 | PASS |
| D091 | Delta bucket | YES | YES | M05 | `M05!A5` | 1 | PASS |
| D092 | Mid-quote implied volatility estimate | YES | YES | M01-1 | `M01-1!A85` | 1 | PASS |
| D093 | Implied-volatility bid/ask width | YES | YES | M01-1 | `M01-1!A86` | 1 | PASS |
| D094 | 5-minute IV change | YES | YES | M01-1 | `M01-1!A87` | 1 | PASS |
| D095 | 1-day IV change | YES | YES | M01-1 | `M01-1!A88` | 1 | PASS |
| D096 | ATM implied volatility by expiry | YES | YES | M01-1 | `M01-1!A89` | 1 | PASS |
| D097 | Near-term IV term-structure slope | YES | YES | M01-1 | `M01-1!A90` | 1 | PASS |
| D098 | IV term-structure curvature | YES | YES | M01-1 | `M01-1!A91` | 1 | PASS |
| D099 | 25-delta put-call skew / risk reversal | YES | YES | M01-1 | `M01-1!A92` | 1 | PASS |
| D100 | 10-delta wing skew | YES | YES | M01-1 | `M01-1!A93` | 1 | PASS |
| D101 | Volatility smile curvature | YES | YES | M01-1 | `M01-1!A94` | 1 | PASS |
| D102 | Volatility-surface fit error | YES | YES | M07 | `M07!A5` | 1 | PASS |
| D103 | Parallel IV surface shift | YES | YES | M01-1 | `M01-1!A95` | 1 | PASS |
| D104 | Skew rotation | YES | YES | M01-1 | `M01-1!A96` | 1 | PASS |
| D105 | 1-year IV rank | YES | YES | M01-1 | `M01-1!A97` | 1 | PASS |
| D106 | 1-year IV percentile | YES | YES | M01-1 | `M01-1!A98` | 1 | PASS |
| D107 | IV minus 5-day realised volatility | YES | YES | M01-1 | `M01-1!A99` | 1 | PASS |
| D108 | IV minus 10-day realised volatility | YES | YES | M01-1 | `M01-1!A100` | 1 | PASS |
| D109 | ATM straddle midpoint premium | YES | YES | M06 | `M06!A5` | 1 | PASS |
| D110 | ATM straddle implied move percentage | YES | YES | M06 | `M06!A6` | 1 | PASS |
| D111 | Risk-neutral terminal density | YES | YES | M07 | `M07!A6` | 1 | PASS |
| D112 | Risk-neutral downside-tail probability | YES | YES | M07 | `M07!A7` | 1 | PASS |
| D113 | Risk-neutral upside-tail probability | YES | YES | M07 | `M07!A8` | 1 | PASS |
| D114 | Estimated physical/real-world return distribution | YES | YES | M08 | `M08!A5` | 1 | PASS |
| D115 | Risk-neutral versus physical distribution gap | YES | YES | M08 | `M08!A6` | 1 | PASS |
| D116 | Option volume/open-interest ratio | YES | YES | M01-1 | `M01-1!A101` | 1 | PASS |
| D117 | Unusual option volume z-score | YES | YES | M01-1 | `M01-1!A102` | 1 | PASS |
| D118 | Call/put volume ratio | YES | YES | M01-1 | `M01-1!A103` | 1 | PASS |
| D119 | Call/put open-interest ratio | YES | YES | M01-1 | `M01-1!A104` | 1 | PASS |
| D120 | Signed option order flow | YES | YES | M01-1 | `M01-1!A105` | 1 | PASS |
| D121 | Signed flow by delta bucket | YES | YES | M05 | `M05!A6` | 1 | PASS |
| D122 | Signed flow by expiry | YES | YES | M01-1 | `M01-1!A106` | 1 | PASS |
| D123 | Open-interest change | YES | YES | M01-1 | `M01-1!A107` | 1 | PASS |
| D124 | Open-interest concentration by strike/expiry | YES | YES | M01-1 | `M01-1!A108` | 1 | PASS |
| D125 | Gamma-weighted open-interest exposure proxy | YES | YES | M09 | `M09!A5` | 1 | PASS |
| D126 | Vega-weighted open-interest exposure proxy | YES | YES | M09 | `M09!A6` | 1 | PASS |
| D127 | Delta-weighted open-interest exposure proxy | YES | YES | M09 | `M09!A7` | 1 | PASS |
| D128 | Gamma concentration around spot | YES | YES | M09 | `M09!A8` | 1 | PASS |
| D129 | Estimated gamma-flip level | YES | YES | M09 | `M09!A9` | 1 | PASS |
| D130 | Dealer hedging-pressure scenarios | YES | YES | M09 | `M09!A10` | 1 | PASS |
| D131 | Cumulative option depth near midpoint | YES | YES | M01-1 | `M01-1!A109` | 1 | PASS |
| D132 | Composite option liquidity score | YES | YES | M03 | `M03!A10` | 1 | PASS |
| D133 | Expected slippage estimate | YES | YES | M18 | `M18!A5` | 1 | PASS |
| D134 | SMART cumulative bid depth | YES | YES | M01-1 | `M01-1!A110` | 1 | PASS |
| D135 | SMART cumulative ask depth | YES | YES | M01-1 | `M01-1!A111` | 1 | PASS |
| D136 | SMART depth imbalance | YES | YES | M01-1 | `M01-1!A112` | 1 | PASS |
| D137 | Order-book microprice | YES | YES | M01-1 | `M01-1!A113` | 1 | PASS |
| D138 | Order-book slope | YES | YES | M01-1 | `M01-1!A114` | 1 | PASS |
| D139 | Depth insertion rate | YES | YES | M01-1 | `M01-1!A115` | 1 | PASS |
| D140 | Depth cancellation/deletion rate | YES | YES | M01-1 | `M01-1!A116` | 1 | PASS |
| D141 | Queue replenishment/reloading proxy | YES | YES | M10 | `M10!A5` | 1 | PASS |
| D142 | Liquidity resilience | YES | YES | M10 | `M10!A6` | 1 | PASS |
| D143 | Direct-exchange depth concentration | YES | YES | M01-1 | `M01-1!A117` | 1 | PASS |
| D144 | SMART versus direct depth divergence | YES | YES | M01-1 | `M01-1!A118` | 1 | PASS |
| D145 | Order-flow imbalance (OFI) | YES | YES | M01-1 | `M01-1!A119` | 1 | PASS |
| D146 | Latent growth-shock factor | YES | YES | M11 | `M11!A5` | 1 | PASS |
| D147 | Latent inflation-shock factor | YES | YES | M11 | `M11!A6` | 1 | PASS |
| D148 | Latent policy/rates factor | YES | YES | M11 | `M11!A7` | 1 | PASS |
| D149 | Latent funding/liquidity factor | YES | YES | M11 | `M11!A8` | 1 | PASS |
| D150 | Composite global risk factor | YES | YES | M11 | `M11!A9` | 1 | PASS |
| D151 | US market breadth proxy | YES | YES | M03 | `M03!A11` | 1 | PASS |
| D152 | Dominant US market-driver probabilities | YES | YES | M12 | `M12!A5` | 1 | PASS |
| D153 | NVDA underlying regime probabilities | YES | YES | M12 | `M12!A6` | 1 | PASS |
| D154 | NVDA options/dealer regime probabilities | YES | YES | M12 | `M12!A7` | 1 | PASS |
| D155 | Canonical market-state vector | YES | YES | M13 | `M13!A5` | 1 | PASS |
| D156 | Signal redundancy/dependence matrix | YES | YES | M14 | `M14!A5` | 1 | PASS |
| D157 | Signal conflict/disagreement score | YES | YES | M14 | `M14!A6` | 1 | PASS |
| D158 | Composite data-quality score | YES | YES | M02 | `M02!A8` | 1 | PASS |
| D159 | State identifiability/tradeability score | YES | YES | M15 | `M15!A5` | 1 | PASS |
| D160 | Conditional joint scenario set | YES | YES | M16 | `M16!A5` | 1 | PASS |
| D161 | Expected P&L by candidate exposure | YES | YES | M17 | `M17!A5` | 1 | PASS |
| D162 | Tail-loss/CVaR by candidate exposure | YES | YES | M17 | `M17!A6` | 1 | PASS |
| D163 | Model-uncertainty penalty | YES | YES | M19 | `M19!A5` | 1 | PASS |
| D164 | Total expected execution cost | YES | YES | M18 | `M18!A6` | 1 | PASS |
| D165 | Net expected utility by candidate | YES | YES | M19 | `M19!A6` | 1 | PASS |
| D166 | Tradeable distribution flag | YES | YES | M19 | `M19!A7` | 1 | PASS |
| D167 | Selected exposure state | YES | YES | M19 | `M19!A8` | 1 | PASS |
| D168 | Aggregate structure Greeks | YES | YES | M17 | `M17!A7` | 1 | PASS |
| D169 | Maximum loss / bounded-loss estimate | YES | YES | M17 | `M17!A8` | 1 | PASS |
| D170 | Structure breakeven points | YES | YES | M17 | `M17!A9` | 1 | PASS |
| D171 | Expiry suitability score | YES | YES | M20 | `M20!A5` | 1 | PASS |
| D172 | Strike suitability score | YES | YES | M20 | `M20!A6` | 1 | PASS |
| D173 | Neighbour-contract relative score | YES | YES | M20 | `M20!A7` | 1 | PASS |
| D174 | Contract/structure stress-loss matrix | YES | YES | M17 | `M17!A10` | 1 | PASS |
| D175 | Maximum permissible position risk | YES | YES | M21 | `M21!A5` | 1 | PASS |
| D176 | Recommended position size | YES | YES | M21 | `M21!A6` | 1 | PASS |
| D177 | Current entry edge after costs | YES | YES | M22 | `M22!A5` | 1 | PASS |
| D178 | Limit-price target | YES | YES | M22 | `M22!A6` | 1 | PASS |
| D179 | Realised fill slippage | YES | YES | M23 | `M23!A5` | 1 | PASS |
| D180 | Fill completion ratio | YES | YES | M23 | `M23!A6` | 1 | PASS |
| D181 | Live portfolio delta | YES | YES | M24 | `M24!A5` | 1 | PASS |
| D182 | Live portfolio gamma | YES | YES | M24 | `M24!A6` | 1 | PASS |
| D183 | Live portfolio vega | YES | YES | M24 | `M24!A7` | 1 | PASS |
| D184 | Live portfolio theta | YES | YES | M24 | `M24!A8` | 1 | PASS |
| D185 | Live position P&L state | YES | YES | M24 | `M24!A9` | 1 | PASS |
| D186 | Current-state similarity to entry state | YES | YES | M25 | `M25!A5` | 1 | PASS |
| D187 | Position invalidation score | YES | YES | M25 | `M25!A6` | 1 | PASS |
| D188 | Expected continuation value | YES | YES | M26 | `M26!A5` | 1 | PASS |
| D189 | Required hedge exposure | YES | YES | M27 | `M27!A5` | 1 | PASS |
| D190 | Expected value gain from modification | YES | YES | M26 | `M26!A6` | 1 | PASS |
| D191 | Immediate exit value after costs | YES | YES | M26 | `M26!A7` | 1 | PASS |
| D192 | Action decision state | YES | YES | M27 | `M27!A6` | 1 | PASS |
| D193 | Realised transaction cost | YES | YES | M23 | `M23!A7` | 1 | PASS |
| D194 | Delta P&L attribution | YES | YES | M28 | `M28!A5` | 1 | PASS |
| D195 | Gamma P&L attribution | YES | YES | M28 | `M28!A6` | 1 | PASS |
| D196 | Vega P&L attribution | YES | YES | M28 | `M28!A7` | 1 | PASS |
| D197 | Theta P&L attribution | YES | YES | M28 | `M28!A8` | 1 | PASS |
| D198 | Skew P&L attribution | YES | YES | M28 | `M28!A9` | 1 | PASS |
| D199 | Unexplained/residual P&L | YES | YES | M28 | `M28!A10` | 1 | PASS |
| D200 | Decision-quality score independent of realised outcome | YES | YES | M29 | `M29!A5` | 1 | PASS |
| D201 | Counterfactual outcome set | YES | YES | M29 | `M29!A6` | 1 | PASS |
| D202 | Signal incremental information value | YES | YES | M30 | `M30!A5` | 1 | PASS |
| D203 | Probability calibration error | YES | YES | M30 | `M30!A6` | 1 | PASS |
| D204 | Brier score for binary probability outputs | YES | YES | M30 | `M30!A7` | 1 | PASS |
| D205 | Log score / negative log likelihood | YES | YES | M30 | `M30!A8` | 1 | PASS |
| D206 | Out-of-sample decision performance | YES | YES | M30 | `M30!A9` | 1 | PASS |
| D207 | Model decay/drift score | YES | YES | M30 | `M30!A10` | 1 | PASS |
| D208 | Signal disposition classification | YES | YES | M30 | `M30!A11` | 1 | PASS |
| D209 | Next observation/update trigger | YES | YES | M31 | `M31!A5` | 1 | PASS |

## Discrepancies

None detected by the stated preservation and allocation checks.

## Limitations

- This proves identifier, name, retained-source-cell and proposed module placement consistency only.
- It does **not** prove independently correct equations, runtime behaviour, module boundaries, or individual test coverage.
- A proposed module may need future dependency migration or private code duplication; neither is implemented by this audit.

## Reproduction

From the repository root:

```sh
python handoff/workbook_v2/audits/pass07_d_signal_integrity_20261014/audit_d_signal_integrity.py
```
