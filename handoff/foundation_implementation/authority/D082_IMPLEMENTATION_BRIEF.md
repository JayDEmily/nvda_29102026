# D082 — commissioned controlled aligned return correlation matrix

ACCEPTED_FOR_IMPLEMENTATION under owner accepted root EXEC_PLAN.md §4.2, §§6–9; independent final semantic and strict acceptance required. D078–D081 remain held.

## 1. Owning profile and exactly two cases

Three ordered NVDA/SPY/QQQ R151 positive closes at each of four exact one-minute UTC anchors T−3,T−2,T−1,T under one synthetic provider and bar/session mapping. Compute each three interval log returns with the accepted bounded 50-digit half-even log operation; interpret retained Decimal return representations as exact Fractions for centring, sums and signed Pearson coefficients. Use sqrt_ratio_50 only on the exact squared rational coefficient. Refuse zero variance, missing anchor, ambiguous selection or uncertifiable arithmetic. No price-level correlation, pairwise intersection, interpolation or beta prerequisite. Own D082-ALIGNED-RETURN-CORRELATION-1/K06/P_REGRESSION; subject US_CORRELATION_BASKET; mmt-d082-controlled/1 and mmt-d082-selection/1; result CorrelationMatrixV1 in member order, correlation/correlation_matrix, window180seconds. Exact source contract and pagination are in root§4.2 and incorporated profile.

Success: 12 actual public R151 projections for NVDA(1,2,4,12), SPY(1,2,6,12), QQQ(1,3,9,18), yielding ((1,-0.5,-1),(-0.5,1,0.5),(-1,0.5,1)) in the frozen matrix carrier. Assert full selected lineage and ordinary read-only SQLite reopen. Refusal: omit only SPY T−1m, assert the eleven other genuine positive exact-anchor facts, and require no result or history.

Proof contract and two-case manifest authored before production. New matrix public type must use local row validation to permit identical numeric rows, leaving common tuple distinctness unchanged. New _correlation_matrix.py and bounded _window.py public routes; reuse exact log/root, raw projection, storage, codec and immutable identity. No runner, M00, old acceptance or provider-native change.

## 2. Incorporated bytes

D082-PROOF-CONTRACT-SHA256: d35872c3d1ce9f90ff55b64638b29cc8b38be79e98065c5429ff82e71f1193eb

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F18_EXTENDED_E11_E15.md | bcf4e438395c01c2f673aa37e1b1b5de3d294a9f15d90153b9a6abf7c367138d |
| handoff/foundation_implementation/authority/D082_PROFILE.json | de492dfdb3f6305d71753fd3e3e2f8c8c331f8b529439e9cac7f19fc85d50935 |
| handoff/foundation_implementation/authority/D082_PROOF_CONTRACT.json | d35872c3d1ce9f90ff55b64638b29cc8b38be79e98065c5429ff82e71f1193eb |
