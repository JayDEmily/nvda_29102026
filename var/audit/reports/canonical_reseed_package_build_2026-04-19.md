# Canonical re-seed package build — 2026-04-19

## Purpose

Create one authoritative carry-forward package from the last safe rebuild baseline and restore the missing canonical workbook-authority bundle.

## Source baseline

- baseline branch: `work/post-wave1-contract-truth-pass-20260419`
- baseline commit: `3540521e3c0e35c2270e01daf77b91f97ea2ffa9`
- baseline package source: `nvda_continue_progress_extended_2026-04-19.zip`

## Restored authority surfaces

The following were restored from `Final.zip` into the repo state:

- `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`
- `data/reference/financial_calendar/`
- `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
- workbook lineage and workbook-law documents under `docs/planning/`

## New governance surfaces added

- `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
- updated `migration_prebuild/AGENTS.override.md`
- `var/audit/README.md`
- `var/audit/nvda_running_audit_log.xlsx`
- brief and audit history under `var/audit/`

## Package intent

This package is the new authoritative carry-forward starting point.
All later continuation zips created before this re-seed should be treated as historical evidence only.

## Resulting repo state

- re-seed work branch: `work/canonical-reseed-authority-20260419`
- re-seed repo state: current `HEAD` of `work/canonical-reseed-authority-20260419`
- canonical package archive name: `nvda_canonical_reseed_authority_2026-04-19.zip`
