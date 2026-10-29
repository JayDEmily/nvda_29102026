# D090 — controlled exact-contract logarithmic moneyness

ACCEPTED_FOR_IMPLEMENTATION under owner-accepted root EXEC_PLAN.md §§4.4–4.5,6–9. Independent final semantic/strict acceptance required.

## 1. Source, arithmetic and two cases

Use actual public C1 R014 strike110/R118 model underlying spot100 with full contract/role/receipt/event identity, contemporaneous matched selection and no fallback. D090-OPTION-SCALAR-1/K02/P_BASIC, mmt-d090-controlled/selection, no predecessor, window0. Enforce strictly positive strike and spot before natural ln(strike/spot). Reuse unchanged bounded rational log series 32..512 terms and 50 significant-digit ROUND_HALF_EVEN certification, refusing uncertifiable rounding; do not use ambient Decimal division or float. Positive oracle is Decimal("0.095310179804324860043952123280765092220605365308644") with public durable read-only reopen. Refusal keeps valid C1 strike but selected same-time spot-1, refusing the log domain without result/history. No native model spot certification or D091.

## 2. Incorporated bytes

D090-PROOF-CONTRACT-SHA256: 4e5d4918fd7818eeb6b78fd1d82914027da80ec3df1d9beff77620be1bc25e16

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F21_EXTENDED_E11_E15.md | 9755003b09ee3fc17ba1c74c029556bb8d16f00ed9892d21280b7a66684d97e1 |
| handoff/foundation_implementation/authority/D090_PROFILE.json | 678e8962b54e59a48ce6407c6245bc95f9e815c66879ec419bf3607a2116b931 |
| handoff/foundation_implementation/authority/D090_PROOF_CONTRACT.json | 4e5d4918fd7818eeb6b78fd1d82914027da80ec3df1d9beff77620be1bc25e16 |
