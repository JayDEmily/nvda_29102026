Status: Gate 115 complete on `main`; Gate 116 is the next active gate in the historical-evaluation readiness pack

# 2026-03-30 Gate 115 Normalised Prepared Runtime Features

## Purpose

Freeze the bounded Gate 115 uplift that adds one explicit normalised prepared-runtime feature packet with deterministic derivation and provenance.

## Gate 115 result

- Verdict: `complete_normalised_prepared_runtime_features`
- Downstream permission: Gate 116 may begin

## What is now frozen

- `PreparedNormalisedFeatureSet` is the canonical bounded feature-carriage packet for Gate 115.
- `PreparedRuntimeSnapshot.normalised_features` preserves the feature packet through raw-to-prepared conversion.
- `RealDataCognitionInputs.normalised_features` preserves the same packet into cognition ingress.
- the prepared-runtime sanity report now exposes `normalised_feature_snapshot_coverage_pct` so coverage stays review-visible rather than assumed.

## Canonical carried features

- `intraday_move_vs_rolling_range_5m`
- `distance_to_vwap_vs_rolling_range_5m`
- `intraday_move_vs_price_realised_vol_15m`
- `front_iv_vs_front_realised_vol_ratio`
- `next_iv_vs_next_realised_vol_ratio`
- `atm_straddle_vs_spot_pct`
- `near_spot_front_volume_share`

## Deterministic freeze

From the checked-in canonical raw bundle and rebuilt prepared fixture pack:

- first snapshot `intraday_move_vs_rolling_range_5m` = `0.2504`
- first snapshot `atm_straddle_vs_spot_pct` = `7.069`
- third snapshot `intraday_move_vs_price_realised_vol_15m` = `4.644`
- third snapshot `front_iv_vs_front_realised_vol_ratio` = `1.8438`
- sanity report `normalised_feature_snapshot_coverage_pct` = `100.0`

## What Gate 115 does not claim

- It does not claim the runtime already consumes these fields for decision law.
- It does not claim the later historical-evaluation thresholds are tuned.
- It only freezes the bounded feature-carriage substrate required before those later gates make stronger use of the richer inputs.
