# D101 — controlled exact native-delta smile curvature

ACCEPTED_FOR_IMPLEMENTATION under owner-accepted root EXEC_PLAN.md §4.7,6–9. Independent final semantic/strict acceptance required.

## 1. Source and two-case contract

Own D101-SMILE-CURVATURE-1/K02/P_BASIC on only E1/T, subject NVDA_SMILE_E1 and exact members C25,P25,C50,P50 with strikes120,100,110,110 and signed deltas+.25,−.25,+.50,−.50. For each member select actual separately projected public R111 IV and R112 signed native delta, at exact T/receipt T, provider/variant/model/expiry/right/full ten-field metadata and matching units. No R015 or D096 predecessor is declared. Two complete exact 50D sides yield ATM=(.22+.26)/2=.24; exact curvature100*(.30+.20−2*.24)=2 volatility points. Persist all eight numeric projections and full lineage, read through public SQLite read-only reader. Refusal omits only P50 R112 while P50 IV and six other roles are separately projected; no single-sided ATM or missing-role inference, no history. Exactly two cases, no native certification.

## 2. Incorporated bytes

D101-PROOF-CONTRACT-SHA256: ef948751afb8b3c20f7876fc2f9d269ecc8ac16921945a2042aaebacea814654

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F24_EXTENDED_E11_E15.md | 7891ac42b1609ad5cb186e0c8a554140907cf46e995cc79fdb9c570327606383 |
| handoff/foundation_implementation/authority/D101_PROFILE.json | fc2974baa8d20fd502f82194dd914dd681b00423005a47fb769c66be5214c07b |
| handoff/foundation_implementation/authority/D101_PROOF_CONTRACT.json | ef948751afb8b3c20f7876fc2f9d269ecc8ac16921945a2042aaebacea814654 |
