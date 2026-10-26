# D131 — controlled positional option depth near actual midpoint

ACCEPTED_FOR_IMPLEMENTATION under owner accepted root EXEC_PLAN.md §§2.2,3,5; independent final semantic and strict proof remain required.

## 1. Exact two cases

Actual same-option public D087 yields midpoint100 from separately projected bid99 and ask101. Three complete M00 native SMART event groups separately project five typed fields R185 integer position, R187 integer operation, R188 integer side, R189 Decimal price and R190 Decimal size, co-referenced by native occurrence, source generation and event/receipt order. Controlled synthetic operation codes 0 insert/shift, 1 update, 2 delete/shift and reset/error317 invalidate old state; side codes0 bid,1 ask. The complete warm-up inserts bid99.8 size5 and ask100.2 size3 at position0 and far bid99 size7 at position1. Inclusive price band0.5 from actual midpoint selects two standing rows, sum8 contracts; far bid is excluded. Persist exact typed raw event groups, reconstructed state and actual predecessor with SQLite read-only reopen.

The refusal retains complete warm-up and actual D087, then records reset/error317 before selection without new warm-up. No stale row or result/history. No native SMART operation mapping or exchange completeness is claimed.

D131-PROOF-CONTRACT-SHA256: 409dda80b31238bd06321797035ec7aee36929ca3e8bfd5429aec5a51e06b467

## 2. Incorporated bytes

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/reuse_preparation/FAMILY_F32_EXTENDED_E11_E15.md | 9e0f32dd13b90d3da0f4fa69cd6edf1168e6b11fdfc8aa5ad4d19f753d48d501 |
| handoff/foundation_implementation/authority/D131_PROFILE.json | e37ddcbafa1a135881d6a3ca2ba4ce3b243b5d7162dab7903531c06b27e16398 |
| handoff/foundation_implementation/authority/D131_PROOF_CONTRACT.json | 409dda80b31238bd06321797035ec7aee36929ca3e8bfd5429aec5a51e06b467 |
