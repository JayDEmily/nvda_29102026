# NVDA V2 — D037–D056 bounded implementation plan

## 1. Authority, baseline and planning boundary

Owner commissioned this plan on 23 October 2026, explicitly retaining narrowly scoped, never-previously-run tests and a single independent acceptance executor per signal. **Planning only: no signal implementation or runtime test is commissioned by creation of this document.** Subsequent execution instruction must commission its controlled profiles and resolve the blocked entries below.

Base: `5fabf1c936cd46a0ccdfe0200a8a775092b07225`, the D036 accepted cumulative checkpoint. New branch: `work/v2-d037-d056-plan-20261023`. No merge to main or push is part of this task. Preserve all accepted M00/D011–D036 source, proof, immutable generations and raw evidence. Previous root plan and its complete acceptance ledger remain available with `git show 5fabf1c:EXEC_PLAN.md`; D036 independent review and pinned runtime log remain in `handoff/foundation_implementation/d036_execution/`.

Root EXEC_PLAN.md is the sole current plan once accepted. GUARDRAILS.md stays frozen. DO_NOT_CARRY_FORWARD the completed D026–D036 schedule into active execution; retain its history. The retired D042/D043/D047 pilot and gate programme stay retired. Those IDs appear here only as ordinary members of the newly requested numeric range, not as a revival of the pilot.

Scope is exactly D037 through D056, twenty IDs. No D057+, API/provider/TWS collection, M00 repair, M01 import/migration, source certification, broad requalification or opportunistic refactor. Controlled examples do not certify native market sources/calendars.

## 2. Reuse and exact authority boundaries

Read the affected semantic sections in full, once per owning unit; reuse unchanged prior inspection rather than repeating a census:

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`: K02, K03, K05, K07 and applicable projection/time/identity clauses; adjacent catalogue rows D037–D056.
- `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md`: Annex B relevant foundation entries and Annex C P02. D040/D041 are preserved downstream allocations, not foundation admissions. See also `handoff/workbook_v2/gates_03_04/DOWNSTREAM_SELF_SUFFICIENCY.md` D040/D041 cards: common K07 law is not a chosen parameter instance; existing generic M01 engineering is not an admitted M02 score profile.
- Under `handoff/foundation_implementation/reuse_preparation/`: D037 in `FAMILY_REALIZED_VOL_D035_D037.md`; D038/D039 in `FAMILY_F07_EXTENDED_E11_E15.md`; `FAMILY_RATE_SPREADS_P12_P22.md`; F10, F11 and F12 packets; corresponding per-ID G2/G3 records. Preparation mathematics/fixture knowledge is reusable specification, not executable M02 acceptance. Its exhaustive falsifiers are not another test manifest.
- Reuse current public M00 projections, M02 request/lineage/configuration/typed codec/SQLite readback mechanisms and immutable admission. No legacy PostgreSQL fixtures or M01 private runtime imports.

Retain CPython3.12.14, SQLite3.53.1, pytest9.0.3, mypy1.20.1, Ruff0.15.11, PyYAML6.0.3 and existing hashed offline locks. Reuse the already qualified environment and logs. Do not switch to the attached Python3.13 wheelhouse or requalify merely because a new turn/branch/reviewer starts. If the actual environment is lost or changes, record the exact gap; do not rerun product tests to diagnose it.

## 3. Non-negotiable execution budget

1. **No previously executed test is run again.** This supersedes the former automatic semantic RED→GREEN cycle and failed-check retry allowance. Write and inspect new proof before implementation, but do not execute it as RED. Implement first; the independent reviewer performs its sole runtime execution.
2. Only new cases proving new/changed signal behaviour are eligible. Before execution, record each exact node ID, owning delta and proposition, and check existing execution evidence. Existing tests remain intact and unexecuted. Renaming, copying, wrapping or reparameterising an old case solely to evade this rule is prohibited. A new D registration is new behaviour when its actual definition/source/selection/lineage is exercised; its oracle and setup patterns may reuse prior research.
3. Two declared cases per unblocked signal: one discriminating success and one named refusal. Six remains an absolute ceiling, not a quota or permission to add cases. The current bounded manifest is **34 new cases for 17 unblocked IDs**; D038/D040/D041 have no runnable manifest until authority is settled. Do not claim forty accepted cases or twenty runnable signals.
4. One independent sub-agent judgement per signal, after source/proof preparation. That reviewer is the **sole runtime executor**. No implementer GREEN, reviewer duplicate, focused then strict run, extra probe, hidden scenario loop, mutation grid or final aggregate sweep. Independent fixture scrutiny occurs inside source/case review, not in extra executions.
5. No default pytest, Makefile broad checks, architecture/bootstrap, promotion/control suites, old M00/M01/M02 claims, integration/network/provider checks, benchmarks or speculative adversarial matrices. A new acceptance run may exercise unchanged shared code through the new signal; it does not rerun the shared code's old tests.
6. Static validation is not a licence to rerun broad checks. One narrowly scoped mypy invocation for changed production Python and one Ruff invocation for changed Python paths, only when new code warrants them. Keep their exact file list/command/output. No full-package/repository sweep, reviewer repeat or static check for prose/hash-only changes. Reuse previously successful evidence for unchanged bytes. If mandatory tooling cannot isolate the new delta, stop with that exact conflict instead of broadening scope.
7. On any failed required check: preserve its first output, stop dependent execution, diagnose only the reached invariant and report the bounded repair. **No automatic rerun**, including after repair. An owner-approved exception must name the affected case/check, material repair and exact rerun scope. Never weaken assertions, suppress a valid case or change an oracle to get green. The ledger must expose any stale result after code changes.
8. A later source/proof change invalidating evidence does not authorise another execution. Record the affected claim and request the exact exception. Documentary acceptance entries, commits, bundles, new reviewers and downloads never trigger tests.

The limit constrains execution duplication, not mathematical correctness, case assertions or source review. A missing mandatory proposition is an explicit scope gap; do not silently omit it or add a test.

## 4. Per-ID manifest and sequence

All paths below: `tests/product/market_measurement_dnnn/test_signal.py`; sole parameterised function `test_dnnn_signal`, with node suffixes `[success]` and `[refusal]`. Spell D numbers lower-case in physical function names (`test_d037_signal`). Each row is an independent acceptance unit. Listed raw dependencies have no D predecessors unless explicitly stated. Exact expected rationals use reduced ExactRatioV1; decimal fields use exact tuple assertions, zero tolerance.

| ID / meaning | Inputs and success oracle | Refusal inside the second case |
| --- | --- | --- |
| D037 / 20-session realised volatility | R151; 21 successive official closes, twenty100 then110; sqrt(252/20) × L under §5.1. | Only the last11 required closes remain inside unchanged21-point context; no ten-session substitute. |
| D038 / jump variation | R149/R150/R151; BLOCKED under §6. | No proof authored or run until the source-role and numeric profile decision. |
| D039 / five-minute ATR | R141 high/R142 low/R143 close; previous100; bars(110,90,105),(112,99,108); mean(TR20,TR13)=ExactRatioV1(33,2) price. | Latest required bar lacks high; older complete bar exists but must not replace it. |
| D040 / trend strength | D020,D021,D027,D024; BLOCKED under §6. | No invented weights, extractors or transforms. |
| D041 / mean reversion | D026,D040,D033; BLOCKED under §6, also depends on D040. | No substitution for the absent score. |
| D042 / 2s10s slope | R249=.0390,R247=.0425; 100×difference=−0.35 percentage points; negative rates/slopes are not generically forbidden. | Correct R247 exists but receipt=cutoff+1s; no future knowledge. |
| D043 / 3m10y slope | R249=.0430,R246=.0410; +0.20 percentage points. | R246 has incompatible series identity despite lawful projection. |
| D044 / real-yield change | R252 .0410→.0425 at1d anchor; +15 basis points. | Only post-anchor reference available; no five-minute proxy or forward fill. |
| D045 / nominal-yield change | R249 .0490→.0500 at1d anchor; +10 basis points. | Correct reference revision received after cutoff. |
| D046 / breakeven change | R255 .0225→.0200 at5d anchor; −25 basis points. | Required5d reference absent, valid1d reference remains; no shortened horizon. |
| D047 / SOFR−EFFR | R257=.0532,R256=.0530; +2 basis points. | R256 has mismatched measurement-date identity. |
| D048 / broad USD change | R245100→120 at20d anchor; ExactRatioV1(20,1) percent. | Only5d reference available in unchanged20d request. |
| D049 / JPY per USD change | R274100→120 at1d anchor; ExactRatioV1(20,1) percent. | Reference explicitly identifies inverse USD-per-JPY quotation. |
| D050 / HKD per USD change | R2757.5→7.8 at1d anchor; ExactRatioV1(4,1) percent. | Otherwise compatible actual reference is0; denominator refusal. |
| D051 / CNY per USD change | R2767.5→7.2 at5d anchor; ExactRatioV1(-4,1) percent. | Reference explicitly identifies CNH instead of onshore CNY. |
| D052 / VIX change | R236100→120; {point_change=20,percent_change=20}. | Reference0: no partial point-only occurrence. |
| D053 / VVIX change | R237100→90; {point_change=-10,percent_change=-10}. | Only nearer post-anchor VVIX exists, no forward reference. |
| D054 / VIX1D change | R23810→11; {point_change=1,percent_change=10}. | Reference identifies VIX rather than VIX1D. |
| D055 / VIX9D change | R23920→20 in distinct observations; {point_change=0,percent_change=0}, actual stored occurrence. | Reference snapshot method differs from current. |
| D056 / VIX3M change | R24040→25; {point_change=-15,percent_change=-37.5}. | Required reference exists but is received after cutoff. |

For D052–D056 both named fields are ExactRatioV1 (e.g. D056 percent=-75/2), with separate index-point/percent units. Never collapse to a scalar or omit the second field. Each refusal starts with lawful public admissions and projections except the one named defect and verifies no new derived occurrence. Every success verifies complete typed value/units, exact versioned definition/parameters/context, chosen public raw lineage, owner/admission/logical identity and times plus ordinary public read-only SQLite reopen. Reopen is an assertion in that same new success case, not a separate storage test. Helpers cannot pre-materialise results or derive expected values from production.

Execution is numeric and sequential: accept/checkpoint one ID before the next. At D038 stop unless its authority is resolved. Do not silently skip D038/D040/D041 or replace them with D057–D059 to manufacture twenty completed signals. An explicit owner decision may defer a blocked ID and commission the remaining independent raw-only units; D041 remains dependent on D040.

## 5. Proposed controlled profiles and file boundaries

These profiles are proposals for later execution acceptance, not native source certification. All new configurations require exact owning brief/contract/admission binding before runtime. Reuse existing public factories/storage; preserve every old configuration and canonical payload byte.

### 5.1 D037

Extend `_realised_volatility.py` with D037 fixed20d profile and exact owning brief hash; preserve D032–D036 profiles unchanged. Introduce a distinct versioned calendar `controlled-risk-20d-calendar/1`, explicitly listing30September–20October2026 inclusive, each12:00–13:00Z, type controlled_cash, no breaks, including weekends deliberately. Twenty-one official13:00 closes; anchor30September, measured sessions1–20October. Each interval's eligible session intersection is1hour/(252×3600seconds)=1/252, total20/252. Use unchanged measured-time, log and root mechanisms and R151 native identity mapping. Do not extend the old calendar under its existing version or rerun its proofs.

L is the previously fixed50-significant-digit ROUND_HALF_EVEN ln(11/10) literal `0.095310179804324860043952123280765092220605365308644`. Treat L as an exact rational, evaluate sqrt((252/20)×L²), round only final root to50 significant digits half-even. Independent planning arithmetic used a200-digit Decimal context for sqrt((252/20)×L²), then50-digit ROUND_HALF_EVEN once, giving `0.33831757671837337403929019188671516632423102188566`. Freeze this literal and exact Decimal tuple in proof; do not call the production helper for the oracle or repeat numeric research.

### 5.2 D039

New `_true_range.py` owns fixed two-bar configuration/selection/arithmetic; use existing window context/request/storage. Controlled session20October12:00–13:00Z; previous close12:30, required five-minute bars ending12:35 and12:40, cutoff12:40:01, now12:40:02. Bind high/low/close to bar.high/bar.low/bar.close, native price, same public observation occurrence per bar, exact bar/session/5minute duration/unadjusted identities. Latest bar positions are selected before field completeness is checked. TR formula is K05, mean via Fraction, output exact ratio. Do not substitute R149/R150 for the declared R141/R142/R143.

### 5.3 D042–D056

New `_macro_changes.py` owns fixed raw-only slope/change profiles; extend `_window.py` routing and `api.py` only where the existing result union needs the distinct frozen carrier `IndexChangeV1(point_change:ExactRatioV1, percent_change:ExactRatioV1)`. Reuse current exact ratio/Decimal encoding and immutable store, no new store/codec/factory framework.

Synthetic provider `foundation-controlled-macro`, variant `macro_snapshot_v1`, sequence scope `foundation-controlled-macro/macro_snapshot_v1`; public mappings `mmt-macro-rNNN/1`, numeric path metric.value, native finite Decimal. Identity paths: metric.series, metric.measurement_date, metric.method, metric.quote_orientation. Exact per-R identifiers match the R catalogue and owning row (R274 JPY_per_USD, R275 HKD_per_USD, R276 onshore_CNY_per_USD); irrelevant orientation is explicitly not_applicable. Same series/method/orientation required across current/reference, measurement dates differ only by configured anchor. Simultaneous two-series slopes require equal measurement dates. Canonical yield/rate fraction native units with identity scale; do not infer conversion from magnitude or claim FRED Percent conversion proved. Index native units index_points; FX currency_per_USD. All remain controlled configurations.

T=20October2026 13:00Z, current atT, cutoff=T+1s, now=T+2s. Declared daily comparison anchors are exact UTC calendar-day offsets (1d=86400s,5d=432000s,20d=1728000s), a synthetic calendar-day convention, not a US trading calendar. D052–D056 choose1d only; no intraday eligibility claim. Latest eligible at/before anchor within60s is reference; current within60s, historic retrieval bound30days. Include an after-anchor value999 decoy in successful history cases, excluded from reference. Preserve event/receipt/revision/sequence identity and bounded full paging. Never interpolate, use a later event or silently shorten horizon. Named late-receipt negatives change receipt only; named identity negatives expose the actual incompatible native identity.

D042/D043 formula100×difference; D04710000×difference; D044–D04610000×(current-reference). Fraction arithmetic with finite exact Decimal output for these differences; D048–D051100×(current/reference−1) as exact ratios. IndexChangeV1 stores current-reference and100×(current/reference−1). No ambient Decimal rounding or floats.

All module names in §5 are under `src/nvda_desk/market_measurement_truth/`. Fixed definition IDs are `D037-REALISED-VOL-1`, `D039-ATR-1`, `D042-RATE-SLOPE-1`, `D043-RATE-SLOPE-1`, `D047-RATE-SPREAD-1`, `D044-RATE-CHANGE-1` through `D046-RATE-CHANGE-1`, `D048-PERCENT-CHANGE-1` through `D051-PERCENT-CHANGE-1`, and `D052-INDEX-CHANGE-1` through `D056-INDEX-CHANGE-1`. Parameter IDs use `mmt-dnnn-controlled/1`; selection IDs `mmt-dnnn-selection/1`; retain exact kernel/profile from the catalogue (P_VOL_WINDOW for D037/D039, P_BASIC for D042/D043/D047, P_WINDOW for the other raw changes). Bind only the selected horizon; other catalogue horizons remain unqualified.

### 5.4 Minimum admission and shared changes

At the first unblocked signal only, extend fixed ID literals/iteration/incorporation declarations in `tools/product_proof_claims.py` for the17 declared unblocked claims. Preserve loader algorithms, validators and old claims. Blocked IDs get no active proof target. Native per-ID paths follow existing patterns:

- `handoff/foundation_implementation/authority/DNNN_IMPLEMENTATION_BRIEF.md` and `DNNN_PROOF_CONTRACT.json`;
- `implementation/authority/DNNN_IMPLEMENTATION_AUTHORITY_BINDING.yaml`;
- `config/product_proof/market_measurement_dnnn/{claim.json,admission.json,generations/NNNN.json}`;
- exact §4 physical proof; `handoff/foundation_implementation/dnnn_execution/` for actual logs/review.

Use existing incorporated companions plus owning proof contract; determine exact count from actual bound rows once, not by copying a stale count. Do not change shared validators to bypass integrity, waive admission or mark unrun claims accepted. Seal only after textual/format/parsing inspection; any subsequent admitted proof change preserves the original generation and links the replacement. Scope beyond these named modules/admissions, changed shared semantics or a new numerical convention requires an explicit gap and owner decision before implementation.

## 6. Blocking authority decisions — no tests as a substitute

**D038:** catalogue declares R149/R150/R151, while legacy arithmetic uses R151 only. The F07 packet explicitly leaves high/low source roles, exact grid and pi/log numeric convention unresolved. Do not discard two dependencies, adopt a truncated pi constant or use BV=0 data to claim general bipower correctness. Required decision: dependency roles/co-occurrence contract; exact high-frequency grid; admitted pi representation/error and final rounding rule; then a bounded manifest discriminating nonzero BV and refusal. No runnable cases are authorised here.

**D040:** Annex C assigns it to downstream P02; K07 requires ordered feature schema. Required authority: concrete extraction paths from D020/D021/D027/D024, transform/scale/orientation/weights/intercept/clipping, output rule, temporal alignment and eligible derived-input public seam. Existing predecessor acceptance does not supply these decisions. No synthetic weights or raw surrogates.

**D041:** same downstream jurisdiction, required schema for D026/D040/D033 plus D040 acceptance and aligned predecessor selection. No score is implemented until those are resolved. These are explicit holds, not completed or silently excluded work. Root plan can operationalise accepted choices; it cannot create the missing domain policy.

## 7. Per-signal cycle after explicit execution commission

- [ ] Read owning authority/profile and reuse ledger; confirm no unresolved scope conflict and neither case has run before.
- [ ] Author two new strict cases and minimum immutable admission; freeze independent oracle. Inspect source/fixture independence and exact provenance; do not execute a preparation RED.
- [ ] Implement only owning delta; perform warranted changed-file statics once and record exact paths/outcomes. Stop on failure under §3.
- [ ] Commit clean candidate. Independent sub-agent reviews that delta, both cases and reused evidence in one judgement. If it finds a defect before runtime, repair without inventing a new test and reconcile any affected static evidence under §3.
- [ ] Reviewer alone runs once: `PYTHONPATH=src /workspace/scratch/83dd7c79f14f/d030-runtime/bin/python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_dnnn`. Only that admitted two-case target may execute. Do not run this command during planning.
- [ ] Record actual candidate/tree, brief/generation hashes, new test node IDs, changed paths, exact command/raw output, reused evidence, independent disposition and limitations in one concise root ledger entry plus owning raw log/review. No administrative report series.
- [ ] Accept only on sufficient semantic evidence and successful sole run. Commit accepted state; immediately create/verify/save a full-history Git bundle and provide its download before advancing. Bundle integrity checks are artefact checks, not product tests. Preserve uncertain save status explicitly; never claim a save based only on bundle creation.

At a blocker retain last accepted checkpoint and first unmet invariant. At D056 close the ledger and supply final cumulative bundle; no final test sweep or merge.

## 8. Planning disposition

| Item | State |
| --- | --- |
| D037–D056 plan | Prepared for owner review; implementation not started. |
| D037,D039,D042–D056 | Proposed controlled profiles and34 new cases; not executed or accepted. |
| D038,D040,D041 | BLOCKED on §6 authority; zero runnable cases. |
| Prior acceptance | Preserved at5fabf1c with original evidence; no rerun. |
| Planning validation | Text/source/diff inspection only; no tests, mypy or Ruff. |
| Main integration | Not performed; new work branch starts directly from D036. |

No new signal execution is recorded. Append real per-ID evidence here only when authorised and obtained.
