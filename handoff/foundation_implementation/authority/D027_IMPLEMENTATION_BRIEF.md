# D027 — exact controlled implementation

ACCEPTED_FOR_IMPLEMENTATION under owner instruction23October2026 to complete D026–D036 and checkpoint each signal. Standing delegated concrete profile/proof admission; one independent final source/case review and sole final strict GREEN required. No provider/API/native certification.

## 1. Exact meaning/profile

VWAP change per exact elapsed minute, absolute and percentage; current120 atT and latest lawful reference100 atT−360s yield both10/3. Reference must be latest at/before T−300s within inclusive60s, same native session/basis; post-anchor observations cannot substitute. Missing eligible reference refuses.

Definition D027-VWAP-RATE-1; parameter mmt-vwap-rate-300s/1. ### 4.1 Common raw/temporal law and D026/D027

Use NVDA; synthetic provider `foundation-pilot-fixture`, variant `cash_quote_v1`, sequence scope `foundation-pilot-fixture/cash_quote_v1`; exact finite native Decimal numeric values; true_instant UTC ISO-Z time; event<=receipt<=knowledge cutoff. Set cutoff=T+1s and captured now=T+2s unless the named negative changes only receipt visibility. Quiescent bounded public M00 histories must be fully enumerated, with duplicate/rank/cursor protection reused where applicable. Do not strip native identities in stored projections; validate them before temporary numeric-eligibility checks.

D026/D027: S=`controlled-price-session/1`, bounds20Oct2026 12:00–13:00Z, complete from12:00; T=12:40Z. Use unchanged WindowContextV1 and existing price unit `mmt-pilot-price/1`. Current freshness60s. Add `mmt-session-provider-vwap/1`: R137→vwap.value, native price, identity fields session→vwap.session, as_of→vwap.as_of, basis→vwap.basis. Require session=S, native as_of equal selected event, basis=`cumulative_session`. It is distinct from the accepted D018 mapping; do not amend D018 bytes. D026 also reuses `mmt-current-last/1` R037→trade.last with session→session.id. Both D026 inputs must be same subject/session/event/source basis.

D027 current event=T; reference latest eligible event<=T−300s, at most60s before that anchor, same S/basis and receipt visibility. Reference gap60s is inclusive, admitting T−360s. Divide by exact positive (T−reference_event)/60 minutes. No log and no inferred five-minute divisor. A small role-aware selector may be added in the new VWAP module where the existing exact-event helper cannot express latest-at-before-anchor; reuse its paging/ranking law without changing accepted selectors.



## 2. Exact proof and budget

D027-PROOF-CONTRACT-SHA256: 57a5f628461b84d5f2f7e18df3e0f9707dec3b88a83b29bfa330893a37874731

Exactly two cases, sole named parameterised function in tests/product/market_measurement_d027/test_vwap_rate.py. Root manifest fixed for this ID; expectations independently authored from literal source operands and exact admitted numerical convention, not production helpers. Worker inspected public M00 setup, refusal reachability, full result/configuration/lineage assertions and durable reopen before sealing. This records worker adequacy under standing delegation, not a fabricated independent review. One admitted semantic RED then minimal source delta, scoped mypy/changed-path Ruff once, one final independent reviewer/sole strict GREEN. No broad/old claims/probes/extra cases or duplicate successful checks. Command python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d027. Preserve raw failures and linked generations after material proof repair.

## 3. Shared boundaries

Reuse existing public window owner/request/occurrence/read seam and RecordState/typed canonical codec/identity. Only commissioned root§5 delta: D026 fixed loader declarations D026–D036 once (D028eight incorporated rows, other new IDsseven); D026/D027 exact named result carriers; D028 separate baseline context; D029 exact rational square-root helper; D032 separate risk context. Old WindowContextV1/dataclass fields, accepted source/proof/generations and canonical bytes stay intact. No new factory/store/schema/codec framework or M00/M01/global CSV mutation. New contexts use existing request.context union. New shaped results qualified inside this ID's existing positive/reopen case.

## 4. Incorporated bytes

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |
| handoff/foundation_implementation/authority/D027_PROOF_CONTRACT.json | 57a5f628461b84d5f2f7e18df3e0f9707dec3b88a83b29bfa330893a37874731 |
