Status: Gate 116 complete on `main`; Gate 117 is the next active gate in the historical-evaluation readiness pack

# 2026-03-30 Gate 116 Event-Class Temporal Windows

## Purpose

Freeze the bounded Gate 116 uplift that replaces hidden generic event countdown handling with explicit event-class timing profiles and calendar-aware next-session hints.

## Gate 116 result

- Verdict: `complete_event_class_temporal_windows`
- Downstream permission: Gate 117 may begin

## What is now frozen

- `TemporalContextService` uses event-class timing profiles for macro-like, policy, company-like, expiry, and venue-session events.
- `TemporalContextOutput.event_timing_profile` exposes which timing law was applied instead of hiding it behind a generic countdown.
- `TemporalEventWindowSurface.timing_profile` preserves the same law into review-visible governance.
- calendar authority projection now carries a bounded list of future trading days so `next_session_open_hint` can use declared trading days instead of weekend-only shortcuts.

## Deterministic freeze

- macro-like events now keep a tighter imminent window than company-like events
- company-like events preserve longer same-session and cooling-off windows than macro releases
- projected desk-calendar authority for the 2026-11-27 half-day session carries future NASDAQ trading days beginning `2026-11-27`, `2026-11-30`
- manual calendar authority with trading days `2026-12-24` and `2026-12-29` yields `next_session_open_hint=2026-12-29T09:30:00-05:00` after the 2026-12-24 close

## What Gate 116 does not claim

- It does not claim broader historical evaluation, execution geometry, or candidate adjudication.
- It only freezes the upstream timing law and the calendar-aware session-open hint required before precursor, adjudication, and final-risk gates lean harder on temporal state.
