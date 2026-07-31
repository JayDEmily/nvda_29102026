# M02 K04 Gate D Validation Summary

## Disposition

`PASS:GATE_D_ACCEPTED:M02_K04_FINANCIAL_CALENDAR_AUTHORITY`

## Accepted surface

- canonical package: `src/nvda_desk/m02_financial_calendar/`
- public contracts: `CalendarFactCandidate`, `FinancialCalendarSnapshot`, `CalendarProjection`
- bounded compatibility adapters:
  - `src/nvda_desk/contracts/reference_data.py`
  - `src/nvda_desk/calendar/reference/projection.py`
  - `src/nvda_desk/calendar/operational/events.py`

The implementation is immutable, deterministic and side-effect-free. It preserves exact four-layer identity, source and candidate lineage, explicit applied supersession decisions, supplied observation/capture facts, lawful absence/conflict states and declared canonicalisation-version identity. It grants no candidate, risk, capital, execution, position, lifecycle, replay or transaction authority.

## Results

| Validation | Result |
|---|---|
| Focused M02 K04 proof | PASS — 33 / 33 |
| Named false-positive mutants | PASS — 6 / 6 killed |
| Former expected-red production cases | PASS — 7 / 7 |
| Direct integrity regressions added | PASS — 13 / 13 |
| Affected surface | 61 passed / 20 unchanged unrelated failures |
| Proof-block registration | PASS — named block |
| All proof-block manifests | PASS — 57 / 57 |
| Proof-executor contract | PASS — 21 / 21 |
| Tier A baseline | 1,390 passed / 274 failed |
| Tier A final | 1,414 passed / 263 failed |
| Tier A node delta | zero new failures; 11 resolved; 13 added passing nodes |
| Tier B | PASS — 49 / 49 |
| Vocabulary canonical-builder parity | PASS — 4 / 4 |
| M02 scoped vocabulary audit/stamp | PASS — 0 unresolved candidates / 23 files; stamp current |
| Python compilation | PASS |
| `git diff --check` | PASS |
| Ruff 0.15.11 | UNAVAILABLE — locked module not installed |
| Black 26.3.1 | UNAVAILABLE — locked module not installed |

The 263 remaining Tier A failures and 20 affected-surface failures remain visible shadow evidence. The exact node comparison records no new failures attributable to M02.

## Evidence-format correction

Staged-range validation found pytest-generated trailing spaces/tabs in raw text and JUnit transcripts. Only trailing spaces/tabs were removed; test names, failure text, counts and outcomes were unchanged.
