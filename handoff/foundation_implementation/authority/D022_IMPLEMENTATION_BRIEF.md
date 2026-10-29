# D022 — bounded controlled implementation

Status: ACCEPTED_FOR_IMPLEMENTATION under owner instruction of 23 October 2026 to complete D021–D025 and checkpoint each. Concrete source/calculation profiles below and root plan are commissioned. Standing delegation binds worker proof adequacy and admission; one independent final review remains required.

## 1. Meaning and configuration

K03 D022: ln(R037 current / R043 same-session open), catalogue dependency order R043,R037.

Definition D022-SESSION-RETURN-1; parameter mmt-session-return-50d-half-even/1 P_WINDOW, policy mmt-session-return-selection/1 with48h role enumeration and60s current freshness. Same session/contextS, exact open event=sessionstart, current event=asof; selection identities from native session.id. Reuse admitted50digit log kernel.

### 3.1 Concrete controlled profiles

Use NVDA and the existing synthetic provider `foundation-pilot-fixture`, variant `cash_quote_v1`, scope `foundation-pilot-fixture/cash_quote_v1`, exact Decimal native prices, existing `mmt-pilot-price/1` identity conversion, true-instant UTC ISO-Z source time and event<=receipt<=cutoff. Public M00 mappings must expose exact native field and any session/phase/kind identity; R tags alone are insufficient. Bounded complete quiescent fixtures are declared, not inferred to be live-feed/calendar certification.

Controlled S is `controlled-price-session/1`; S_prev is `controlled-price-session-prev/1`. D022/D025 use a WindowContextV1 with S's ref/bounds/completeness; D023 uses `controlled-preopen-pair/1` with its measurement interval below and explicit S/S_prev relationship in the immutable profile. Raw mapping versions are 1: `mmt-current-last` (R037, trade.last), `mmt-session-open` (R043, session.open), `mmt-prior-official-close` (R042, session.close), `mmt-session-high` (R039, session.high), `mmt-session-low` (R040, session.low). Each exposes session identity from `session.id`; D023 uses a distinct `mmt-preopen-last/1` mapping for the same R037 field additionally exposing `session.phase`, and its R042 mapping additionally exposes `session.kind`. Preserve actual native selection identities in lineage, using the accepted D018 validation pattern without changing stored projections. Dependency/binding order follows the catalogue: D022 R043,R037; D023 R042,R037; D025 R039,R040,R037.

- **D021:** reuse `controlled-close-session/1` [2026-10-20T12:00Z,13:00Z), complete from12:00Z; T=12:40Z, cutoff=T+1s, captured now=T+2s. Reuse current-at-as-of/minute-grid, latest-at-or-before anchor, maximum60s reference gap, no-session-bridging and source/paging policy from D019/D020. Add fixed1800s identity only; do not edit the accepted60/300s identities.
- **D022:** controlled current session S=[2026-10-20T12:00Z,13:00Z); T=12:40Z, cutoff/now offsets as above. R043 at S start; R037 at T. Each exposes native session=S. Wrong-session negative open belongs to declared S_prev=[2026-10-19T12:00Z,13:00Z), and must be returned by public history. Define role-specific selection: current freshness60s; session-open identity/event-at-open, with a48h enumeration/visibility allowance so the negative is not rejected merely as an old tick. Never apply the current-price60s bound to a legitimate session open.
- **D023:** controlled target S opens2026-10-20T12:00Z; pre-open measurement interval [11:00Z,12:01Z), T=11:50Z; explicitly linked S_prev is the controlled interval above, official close at2026-10-19T13:00Z. Current fact exposes target S and phase=pre_market; reference exposes S_prev and kind=official_close. Negative exposes kind=intraday at12:59Z on the previous date with the same80 value. Reference allowance48h, current freshness60s, same receipt cutoff. This declared pair is a synthetic profile, not a guessed exchange trading calendar or midnight rule.
- **D024:** use the same T/cutoff/session/profile as D021 for all three producers. Validate exact accepted D019/D020/D021 definitions, immutable parameter/horizon identities60/300/1800s, source subject and context; preserve all three complete predecessor snapshots and their ultimate raw lineage, in D019,D020,D021 order. A thin typed composition of actual public read facets may delegate lookups to those producers; it must not manufacture or modify returned facts. No new predecessor API family is needed.
- **D025:** same S/T as D022. Map High/Low/Last explicitly to distinct native fields (`session.high`, `session.low`, `trade.last`) of one source observation carrying R039/R040/R037. Preserve that observation ID for all three field projections, session=S and snapshot event=T. Require exact matching source/session/time and finite values with High>=Low; no silent high/low swapping. Do not clip an inconsistent out-of-range Last into [0,1]; refuse incompatible source content. In the named negative Last=High=Low avoids a competing range-membership failure.

These are proposed concrete execution profiles, bound into the corresponding immutable brief on commissioning. Any unresolved source/calendar meaning outside them remains a native-readiness hold, not a reason to research/connect a provider during this tranche.

### 3.2 D024's five fields and numerical representation

The law is `q1=D019/1`, `q5=D020/5`, `q30=D021/30`, `accel_1v5=q1-q5`, `accel_5v30=q5-q30`, units return/minute. Treat each already-rounded canonical predecessor Decimal as its exact stored finite value; divide/subtract using exact rational arithmetic. Preserve upstream rounding provenance; do not claim the result is an unrounded irrational logarithm or apply a second hidden rounding policy.

Proposed public carrier: frozen `ReturnAccelerationV1(q1:ExactRatioV1, q5:ExactRatioV1, q30:ExactRatioV1, accel_1v5:ExactRatioV1, accel_5v30:ExactRatioV1)`, added once to the existing window-result union. No positional unnamed vector or reuse of D018's two-field comparison carrier.

Independent expected numerator/denominator pairs, prepared from the declared literals rather than runtime predecessor results:

| Field | Numerator | Denominator |
| --- | --- | --- |
| q1 | 87011376989629766167765901873749540976783972605843 | 1000000000000000000000000000000000000000000000000000 |
| q5 | 18232155679395462621171802515451463319738933791449 | 500000000000000000000000000000000000000000000000000 |
| q30 | 40546510810816438197801311546434913657199042346249 | 3000000000000000000000000000000000000000000000000000 |
| accel_1v5 | 10109413126167768185084459368569322867461221004589 | 200000000000000000000000000000000000000000000000000 |
| accel_5v30 | 13769284653111267505845900709254773252246912080489 | 600000000000000000000000000000000000000000000000000 |


## 2. Exact bounded proof and change

D022-PROOF-CONTRACT-SHA256: 1fb204b145963317eb13b7a5bb525f2354effc1c3972890e8a6acde4d8b3e12e

Positive current120 at12:40 and open100 at12:00 in S -> literal L5. Negative returns actual otherwise valid open100 from previous controlled session S_prev at19Oct12:00; current remains valid.

Refusal: Wrong-session open must refuse specifically at session/role compatibility rather than empty history or60s staleness.

Exactly two cases, one named parameterised function. Worker inspected literal inputs, independent expected values, public fixture sequencing and refusal prerequisites against the incorporated authority before sealing. This records worker judgement under standing delegation, not an invented independent review. One admitted strict RED, one independent final strict GREEN, one scoped mypy and changed-path Ruff per signal. No old claims, extra probes, broad suites or duplicate successful results. Full logs in d022_execution; checkpoint after acceptance.

Reuse unchanged public owner/request/read protocols, RecordState, typed codec and hash identity; preserve prior authority, tests and immutable generations. The D021 scope includes the single declaration-only loader extension for fixed D021–D025 identities and seven-row counts, without changing validator/generation algorithms or old catalogue bytes. D024 alone adds the proposed five-field carrier to the window union. Other IDs reuse existing carriers. No new factory/store/schema/API family. Native feed/calendar certification remains held.

## 3. Incorporated exact bytes

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |
| handoff/foundation_implementation/authority/D022_PROOF_CONTRACT.json | 1fb204b145963317eb13b7a5bb525f2354effc1c3972890e8a6acde4d8b3e12e |
