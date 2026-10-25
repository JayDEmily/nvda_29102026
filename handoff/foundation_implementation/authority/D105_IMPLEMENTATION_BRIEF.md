# D105 — controlled complete prior-year comparable-IV rank

ACCEPTED_FOR_IMPLEMENTATION under owner-accepted root EXEC_PLAN.md §4.9,6–9. Independent final semantic/strict acceptance required.

## 1. Source and two-case contract

D105-PRIOR-YEAR-IV-RANK-1/K04/P_BASELINE on synthetic R183 one controlled constant-maturity series NVDA_30D_ATM_CONTROLLED. Actual M00 public true-instant R183 at iv.close, provider foundation-controlled-iv-history/variant daily_constant_maturity_iv_v1, exact series/underlying/30D/ATM/model/period.close_utc metadata, native annualised decimal volatility. Current at T, cutoffT+1s, nowT+2s. Require every365 prior daily UTC anchors T−365d..T−1d including weekends; no calendar inference or current-in-baseline. History page100/1000 must enumerate all, select each exact source role, persist366 lineages current then chronological prior and public read-only SQLite reopen. First100 prior .20,next65 .40,last200 .60,current .70 =>100*(.70−.20)/(.60−.20)=125 rank points with no clamp. Refusal all365 prior .40 while current .70, refusing zero prior range without result/history. Exactly two cases, no live native data certification.

## 2. Incorporated bytes

D105-PROOF-CONTRACT-SHA256: 619621224eff6a2df5c9717a63005ffcf96688b79d6c203f030960d3b5cf0246

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F25_EXTENDED_E11_E15.md | e48b30513881f772410a769c93c8d59f46c7daebc62c34b9a4e879626fac7853 |
| handoff/foundation_implementation/authority/D105_PROFILE.json | 7f0c9b322e0a1156a0dea76b1af7c7e7c5c08f2cd525a32854e969c3d4f3e3f2 |
| handoff/foundation_implementation/authority/D105_PROOF_CONTRACT.json | 619621224eff6a2df5c9717a63005ffcf96688b79d6c203f030960d3b5cf0246 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
