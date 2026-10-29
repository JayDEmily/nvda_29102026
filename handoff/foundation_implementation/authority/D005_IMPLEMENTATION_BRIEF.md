# D005 — controlled versioned session phase

ACCEPTED_FOR_IMPLEMENTATION under accepted root EXEC_PLAN.md §§2.1,3,5; independently reviewed final proof remains mandatory.

## 1. Source, calendar, phase and exact pair

Actual D001/D003 yield aware local Saturday 2026-10-10T00:59:50+11:00. Actual projected M00 R023 session `overnight/1` and R024 calendar `controlled-overnight/1` share exact provider, variant, subject, sample, source event and receipt. The separately versioned complete `controlled-overnight/1` calendar covers Friday00–Sunday00 Melbourne local, with the overnight Friday16–Saturday06 session and Saturday06–16 day session open, other intervals explicitly closed; Saturday is declared open. The phase policy is a separate immutable context, not R024's version: v1 ordered half-open overnight [Saturday00,06) and day [06,16) phases; v2 has only day [06,16). Both schedules are nonoverlapping, versioned and anchored to the calendar's IANA identity. Neither policy asserts native exchange truth.

Success policy v1 returns typed `overnight`, retaining selected R023/R024, actual nested D003/D001 and both policy versions through public SQLite read-only reopen. Refusal changes only the phase policy to valid v2; all source projections, actual predecessors and complete open calendar stay the same, but no configured phase contains local00:59:50 and no result/history is emitted. Overlap is invalid at policy admission, not the reached refusal. Exactly two physical cases. No D010 acceptance.

## 2. Incorporated bytes

D005-PROOF-CONTRACT-SHA256: 1e38e9c96c005aa2211a033a395f6e6c882454c70b0a64595d3056cc8e50fdf5

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F01_TEMPORAL_E11_SOURCE_EXTRACTION.md | 5cf80f45f10841303d01f992e81b39f0affb335cb6c652ab12bedc17e14a01c7 |
| handoff/foundation_implementation/authority/D005_PROFILE.json | d099260ad0b2508264a89f897c0655f4e7d967149896a4ca37f4aa29fdc3172c |
| handoff/foundation_implementation/authority/D005_PROOF_CONTRACT.json | 1e38e9c96c005aa2211a033a395f6e6c882454c70b0a64595d3056cc8e50fdf5 |
