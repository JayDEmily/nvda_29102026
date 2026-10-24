# D092 — controlled exact-contract quote-side IV midpoint

ACCEPTED_FOR_IMPLEMENTATION under owner-accepted root EXEC_PLAN.md §§4.4–4.5,6–9. Independent final semantic/strict acceptance required.

## 1. Exact source and two cases

Select public C1 R084 bid_model.iv and R093 ask_model.iv from the same exact contract/model/time snapshot, with full ordered metadata, source role, unit and observation lineage. Own D092-OPTION-SCALAR-1/K02/P_BASIC, mmt-d092-controlled/selection. Identity scale1 annualised_decimal_volatility, both finite nonnegative; midpoint is exact reduced Fraction(bid+ask)/2, no upper cap or artificial crossed-IV prohibition. Success C1 .20/.30 yields ExactRatioV1(1,4), full public SQLite read-only reopen. Refusal has actual C1 bid and lawful C2 ask independently projected, no C1 ask: reject cross-contract substitution, no result/history. No native model source or D093 width certification.

## 2. Incorporated bytes

D092-PROOF-CONTRACT-SHA256: a26910f366f039053a4bd3f27b3820766a9c7e6509f77c95d83026049f67ae35

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F22_EXTENDED_E11_E15.md | 890ec8f4747f7eebdfa65e14395bdc538e4d4c49970e58a720cba60b6d9a180c |
| handoff/foundation_implementation/authority/D092_PROFILE.json | 8f93ce9681d4c2b9e79ac3a4e0c5b4207bc1bc8caaeacf67fd3b51d7aa5950b5 |
| handoff/foundation_implementation/authority/D092_PROOF_CONTRACT.json | a26910f366f039053a4bd3f27b3820766a9c7e6509f77c95d83026049f67ae35 |
