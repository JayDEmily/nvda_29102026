# Phase 0 — Signal Workbook Viability Audit for One Canonical Real-Data Run

Status: complete on branch `testing`

## Purpose

Decide whether the checked-in signal workbook can support one lawful deterministic runtime path without invented raw inputs.

## Inputs inspected

- `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`
- `src/nvda_desk/schemas/dataset.py`
- `src/nvda_desk/services/real_data_loader.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json`

## Verdict

**Phase 0 result: `fail_missing_raw_truth`**

The workbook is useful as doctrine, signal-catalog authority, and scenario-thinking support. It is **not** currently sufficient to build one canonical real-data runtime bundle for the checked-in Gate E -> Gate 92 real-data path.

## Why it fails

### 1. The workbook is mostly a doctrine and scenario artifact, not a runtime-capture artifact

Observed workbook shape:
- `README`, `Controls`, `Scenario_Packs`, and `Test_Use_Cases` are guidance surfaces;
- `Live_Web_Baseline` is a public-web anchor table;
- `Anchor_Data` is a date-indexed anchor surface;
- `Synthetic_Raw` is formula-driven from anchors plus scenario controls;
- the main derived tabs are also formula-driven from `Synthetic_Raw`;
- `Options_Chain_Raw_Spec` and `Volume_Baseline_Raw_Spec` describe capture policy but do not contain captured runtime rows.

That means the workbook currently explains what should exist far better than it stores one admissible runtime snapshot.

### 2. The checked-in real-data runtime path requires structures the workbook does not carry

The current runtime-preparation code expects a `RealDataBundle` with:
- provenance;
- timestamped OHLCV bars;
- timestamped option-chain snapshots with per-quote fields;
- normalised event records.

The workbook does not contain one authoritative block with those surfaces wired together at a single mid-session timestamp.

### 3. The options-chain surface is specified, not captured

The workbook includes `Options_Chain_Raw_Spec`, which is useful doctrine.

It does **not** include actual quote rows carrying:
- snapshot timestamp;
- expiry;
- strike;
- side;
- bid/ask;
- IV;
- gamma;
- open interest;
- quote volume.

Without that raw surface, the repo cannot lawfully derive front/next-expiry ATM IV, put/call skew, strike clustering, tenor curve, repeated-snapshot pressure, or pin progression for a true real-data snapshot.

### 4. The event surface is too thin for the runtime path

The workbook carries `Event_Flag` on the anchor/synthetic tables and a temporal test harness that can reason about event minutes remaining.

It does **not** carry one normalised event table with event identity, class, impact, scheduled timestamp, and lineage keys. The checked-in real-data path expects that richer event truth.

### 5. The temporal surface is still missing critical intraday raw truth

The current workbook does not provide one timestamped intraday bar sequence with open/high/low/close/volume rows that can support:
- session VWAP;
- distance to VWAP;
- VWAP slope 5m;
- opening-range high/low;
- opening-range break count;
- realised vol 5m / 15m;
- relative volume against historical same-bucket baseline.

The workbook talks about these surfaces and, in places, estimates or proxies them. That is not the same as storing the raw truth required by the runtime-preparation service.

## What is present and still valuable

The workbook remains useful for:
- raw-versus-derived authority separation;
- signal-catalog governance;
- options-chain capture doctrine;
- volume-baseline doctrine;
- temporal Step 1 threshold thinking;
- playbook/module dependency audit;
- public-web anchor sanity checks.

That value should be preserved. It just should not be mislabelled as a canonical runtime bundle.

## Missing raw truth that blocks one canonical workbook-driven run

1. One typed provenance record for a single admitted import.
2. One intraday timestamped OHLCV bar series.
3. One or more timestamped option-chain snapshots with actual quote rows.
4. Per-quote IV, gamma, open interest, and volume for at least the front two expiries.
5. One normalised event table with event identity, impact, timing, and lineage.
6. One authoritative mid-session timestamp linking the bar, chain, and event surfaces together.
7. Repeated snapshot sequence rows if the canonical run is expected to exercise pin-progression or pressure-evolution logic from raw truth.

## Derived surfaces that should be computed later, not captured as fake raw truth

If the missing raw truth is supplied, the following should be built deterministically rather than entered manually:
- session VWAP;
- distance to VWAP;
- VWAP slope 5m;
- opening-range metrics;
- realised-vol metrics;
- relative-volume ratio;
- front and next-expiry ATM IV split;
- skew/imbalance/concentration features;
- pin progression and repeated-snapshot sequence features.

## Safe next step

Do **not** invent the missing raw surfaces inside the workbook.

Safe next action:
- keep the workbook as doctrine and signal-catalog authority;
- keep `fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json` as the current canonical real-data runtime artefact;
- unblock later testing phases only when a true captured raw bundle is added or when a deliberately bounded single-snapshot import artefact is created from real captured rows, not from synthetic workbook expansion.

## Machine-readable companion

See:
- `docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.json`
