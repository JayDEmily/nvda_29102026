# D106 — controlled complete prior-year comparable-IV midrank percentile

ACCEPTED_FOR_IMPLEMENTATION under owner-accepted root EXEC_PLAN.md §4.9,6–9. Independent final semantic/strict acceptance required.

## 1. Source and two-case contract

D106-PRIOR-YEAR-IV-MIDRANK-1/K04/P_BASELINE uses the same declared synthetic R183 constant-maturity series/source identity as D105 but its own profile/authority and full current plus365 prior daily UTC anchors. Current .40, chronological prior first100 .20,next65 .40,last200 .60: strict-less100,equal65, exact100*(100+65/2)/365=2650/73 percentile, no current in prior and no tie rounding. Actual public M00 raw history must cross page100 boundaries, persist366 ordered lineages current then chronological prior and public SQLite read-only reopen. Refusal omits only required T−1day prior observation while all364 other prior anchors and current exist; no count shrink/fill/history. Exactly two cases, no live native calendar/history certification.

## 2. Incorporated bytes

D106-PROOF-CONTRACT-SHA256: ed7f69d5d4f9beb0df8edc3bcae8d506e2768fc8f17f68ba8a43eae3274331e9

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F25_EXTENDED_E11_E15.md | e48b30513881f772410a769c93c8d59f46c7daebc62c34b9a4e879626fac7853 |
| handoff/foundation_implementation/authority/D106_PROFILE.json | 80b80a012b2c62abc09e68c73214c08a55613c276472ea2c8ca90cc2eff19b1a |
| handoff/foundation_implementation/authority/D106_PROOF_CONTRACT.json | ed7f69d5d4f9beb0df8edc3bcae8d506e2768fc8f17f68ba8a43eae3274331e9 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
