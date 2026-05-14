# Sequence 10.1 temporal truth contract gap report

## Classification

Defect classification: **A. non-conforming code against existing temporal law**.

The repair uses existing admitted temporal terms only: `source_time_utc`, `source_timezone_raw`, `source_time_kind`, `source_date`, `captured_at_utc`, `persisted_at_utc`, `time_granularity`, `window_start_utc`, and `window_end_utc`. No new durable vocabulary terms are introduced.

## Findings

1. `source_time_utc` remains the canonical UTC source-observation timestamp.
2. The prior session classifier compared the UTC wall-clock value directly against 09:30/10:30/15:30/16:00 thresholds.
3. Runtime tests previously encoded `2026-04-21T09:31:00Z` as opening-session evidence. For an NVDA/US-market context, that is not 09:31 in `America/New_York`.
4. `TemporalContextOutput` did not carry the `windows` set from `TemporalContextInput`; the serial-runtime-to-parallel-risk adapter rebuilt `TemporalContextInput` with `windows=[]`.

## Corrective contract

- Session classification now converts `source_time_utc` into the explicit `source_timezone_raw` zone before threshold comparison.
- Missing `source_timezone_raw` is treated as explicit UTC, not as an exchange/session timezone.
- Invalid `source_timezone_raw` fails closed with `unknown_source_timezone_raw:<value>`.
- Temporal output now carries `windows`; the serial temporal stage packet to parallel-risk bootstrap path preserves those windows.

## Vocabulary decision

Existing admitted fields are sufficient. `var/vocabulary/synonym_candidates.json` was not mutated.
