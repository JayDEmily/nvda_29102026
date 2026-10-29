# D093 — controlled exact-contract quote-side IV width

ACCEPTED_FOR_IMPLEMENTATION under owner-accepted root EXEC_PLAN.md §§4.4–4.5,6–9. Independent final semantic/strict acceptance required.

## 1. Exact source and two cases

Select public C1 R084 bid_model.iv and R093 ask_model.iv with complete matching contract/model/source role, identity annualised_decimal_volatility units, event/receipt and cutoff. Own D093-OPTION-SCALAR-1/K02/P_BASIC, mmt-d093-controlled/selection. Both selected finite nonnegative native IVs must have identical event time under zero-skew join; do not impose invented upper cap or crossed-IV prohibition. Width is exact reduced Fraction(100)*(ask-bid), volatility_points. Success both atT (.20,.30) yields ExactRatioV1(10,1) and full public SQLite read-only reopen. Refusal bidT, askT-1s both fresh actual C1 sources: reject zero-skew join with no result/history. No native model certification or D094 historical IV change.

## 2. Incorporated bytes

D093-PROOF-CONTRACT-SHA256: a734f31132ba0b3ca3c42153355d4421e986544485308cae91afb0fa16acf6b6

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F22_EXTENDED_E11_E15.md | 890ec8f4747f7eebdfa65e14395bdc538e4d4c49970e58a720cba60b6d9a180c |
| handoff/foundation_implementation/authority/D093_PROFILE.json | 0bc8b15680c2a14982ba9044ae63b1a0495c2cba2b424af672e58690b3315d38 |
| handoff/foundation_implementation/authority/D093_PROOF_CONTRACT.json | a734f31132ba0b3ca3c42153355d4421e986544485308cae91afb0fa16acf6b6 |
