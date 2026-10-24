# D087 — commissioned controlled exact option midpoint

ACCEPTED_FOR_IMPLEMENTATION under owner accepted root EXEC_PLAN.md §§4.4–4.5 and §§6–9. Independent final semantic and strict acceptance required. D085/D086 temporal producers remain deferred.

## 1. Owning source and exactly two cases

C1=controlled-nvda-c110-20261023 and C2=controlled-nvda-p110-20261023 supported for their own requests. Exact option contract key, expiry/right/strike/underlying/currency/multiplier/kind/model/source/role metadata and same-snapshot T govern R034 quote.bid and R035 quote.ask. Two immutable parameter IDs mmt-d087-c1-controlled/1 and mmt-d087-c2-controlled/1 prevent conflicting subject/member alias. Own D087-OPTION-SCALAR-1/K02/P_BASIC; mmt-d087-selection/1; USD_per_share native identity; midpoint ExactRatioV1; option_premium/exact_ratio, window0. Require finite nonnegative bid<=ask after selecting complete bounded source history by exact contract/role; no older quote fallback.

Success admits and projects actual C1 bid2/ask4, yields ExactRatioV1(3,1), asserts both full raw lineages and ordinary public SQLite read-only reopen. Refusal admits and projects actual C1 bid4/ask2 under otherwise lawful exact source/contract, reaches crossed-quote eligibility, emits no result/history. C2 remains supported for later actual D088 predecessor setup without amending this profile. No live IBKR/native certification or D085 prerequisite inference.

Exactly two physical cases authored before production. New _option_scalars.py only D087 owner and bounded _window.py public routes. Reuse unchanged projection/codec/storage/identity; no shared runner, M00 or old test changes.

## 2. Incorporated bytes

D087-PROOF-CONTRACT-SHA256: 5c66d3d8c197209048c1a45b4f723a14bbc417df26fc2c4061f1f2add9dea456

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F22_EXTENDED_E11_E15.md | 890ec8f4747f7eebdfa65e14395bdc538e4d4c49970e58a720cba60b6d9a180c |
| handoff/foundation_implementation/authority/D087_PROFILE.json | 4f3cb210540a04ad24730f1d28d1cb9cd0482dcfc7fd627069d18b6b2a686023 |
| handoff/foundation_implementation/authority/D087_PROOF_CONTRACT.json | 5c66d3d8c197209048c1a45b4f723a14bbc417df26fc2c4061f1f2add9dea456 |
