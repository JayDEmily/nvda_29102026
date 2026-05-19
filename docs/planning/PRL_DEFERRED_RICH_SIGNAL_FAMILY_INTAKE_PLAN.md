# PRL deferred rich signal-family intake plan

Status: planning artefact for `PRL-MRP-027`.

The following families remain deferred until a lawful typed upstream source and PRL contract/promotion path exists. They must not be fabricated by the Parallel Risk Lane.

| Signal family | Required upstream source | Required contract | Future PRL atom |
|---|---|---|---|
| VWAP | intraday market-data/VWAP service | `MarketMicrostructureContext` or promoted signal snapshot | VWAP reliability / gravity state |
| spread/depth | NBBO/L2 quote feed with size/depth | `LiquidityContext` | liquidity/depth state |
| tape speed / relative volume | trades and volume-curve baseline | `TapeSpeedContext` / `VolumeContext` | tape-speed / activity-legibility state |
| realised volatility / ATR | bar series/high-low/returns | `RealizedVolatilityContext` | realised-volatility/range state |
| dense options chain | options chain quote/IV/volume/OI/Greeks | `OptionsChainSnapshot` | options-surface availability/state |
| IV rank / implied move | IV history and ATM straddle/term surface | `OptionsVolatilityContext` | implied-vol premium / event-vol state |
| skew | IV by strike/expiry | `OptionsSkewContext` | skew-asymmetry state |
| real gamma exposure / gamma flip | options greeks + OI/volume + spot model | `DealerConvexityContext` | dealer-convexity / gamma-flip state |
| OI concentration / strike pin | OI by strike/expiry and spot distance | `StrikeConcentrationContext` | strike-concentration / pin state |
| MOC / close auction imbalance | exchange auction/MOC imbalance feed | `AuctionContext` | close-auction state |
| headline risk | governed news/headline feed with source time/reliability/conflict metadata | `HeadlineRiskContext` | headline reliability / information-lag state |
| crowding / real-money flow | ETF flow, fund flow, prime/positioning proxy | `FlowPositioningContext` | crowded/forced-flow state |
| cognitive load / attention pressure | alert density, signal conflict count, event density, admitted operator/context input | `CognitiveLoadContext` | attention-load / cognitive-friction state |

## Intake gates for every deferred family

1. Identify lawful upstream source.
2. Add or promote typed contract/config carrier.
3. Add source freshness and missing/unavailable handling.
4. Add risk atom tests before implementation.
5. Preserve authority boundary: no candidate, play, capital, order, serial mutation, review judgement, or direct workbook runtime read.
6. Preserve neutral risk semantics: constructive, defensive, ambiguous, mixed, consequence, and confidence dimensions may coexist.
