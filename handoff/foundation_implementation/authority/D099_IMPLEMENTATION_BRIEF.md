# D099 — controlled native 25-delta put-call skew

ACCEPTED_FOR_IMPLEMENTATION under owner-accepted root EXEC_PLAN.md §4.7,6–9. Independent final semantic/strict acceptance required.

## 1. Source, typed categorical result and two cases

Own D099-NATIVE-DELTA-SKEW-1/K02/P_BASIC with exact C25/P25 per-expiry E1/E2 contract/model/strike/right keys and both A=T−300s,T permitted requests before admission. At each request, separately select actual public R111 model IV, R112 signed model delta and R015 native option-right C/P from each exact contract, same selected snapshot, full ten-field metadata, provider/variant/unit/receipt and source observation IDs. Require exact +.25 C25/−.25 P25 and native C/P matching metadata and contract; IV nonnegative. A categorical OptionRightLineageV1 carries complete R015 projection/string/value/unit; OptionSkewV1 carries reduced ExactRatioV1 100*(putIV−callIV) and ordered call/put categorical lines. Four numeric source lines carry R111/R112. Success at T/E1 .20/.30, ±.25 and C/P yields10 volatility points with full categorical-preserving public SQLite read-only reopen. Refusal changes only actual P25 R015 native string to C while its metadata/right/delta remain lawful P/−.25; independently project all six facts, refuse without result/history. Never infer right from metadata alone. E2 and A request support is frozen for genuine later D104, but not extra D099 test cases. No native provider certification.

## 2. Incorporated bytes

D099-PROOF-CONTRACT-SHA256: fd11175b0117bb27bfce8e7d1ac4c0c1eaa39d3cbea5dad0c84c8524b679fbb4

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F24_EXTENDED_E11_E15.md | 7891ac42b1609ad5cb186e0c8a554140907cf46e995cc79fdb9c570327606383 |
| handoff/foundation_implementation/authority/D099_PROFILE.json | 5ccd3b42c09915161ee739e9ef52587a8514c18640259f1a55a61c9167bf9e9a |
| handoff/foundation_implementation/authority/D099_PROOF_CONTRACT.json | fd11175b0117bb27bfce8e7d1ac4c0c1eaa39d3cbea5dad0c84c8524b679fbb4 |
