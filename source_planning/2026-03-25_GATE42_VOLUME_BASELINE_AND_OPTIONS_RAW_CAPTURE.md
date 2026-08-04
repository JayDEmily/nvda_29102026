# Gate 42 — Volume Baseline and Raw Options Capture Policy

Status: complete on `main`

## Purpose

Define the missing raw capture policy that the runtime needs for honest options-first and participation-aware behaviour.

## Closed scope

- Added `Volume_Baseline_Raw_Spec` to the workbook for same-bucket historical volume, trade-count, and spread baselines.
- Froze the dense-versus-coarse options capture policy:
  - dense front-two-expiry capture every 30 seconds during RTH;
  - dense near-spot strike band;
  - coarser farther-tenor capture for curve context only.
- Marked quote-level options fields as raw capture targets:
  - `expiry`, `dte`, `strike`, `side`, `bid`, `ask`, `last`, `iv`, `delta`, `gamma`, `oi`, `volume` where vendor-supplied.

## Why this gate exists

The old workbook carried too many options proxy fields as if they were raw, and the runtime still lacked a truthful same-minute participation baseline. Gate 42 closes that doctrine gap even where loader wiring is still future work.

## Result

Gate 42 is closed. The project now has an explicit raw-capture policy for options rows and a truthful baseline policy for volume and liquidity context.
