# NVDA V2 — bounded D021–D025 execution plan

## 1. Authority, baseline and current stop

Owner direction, 22 October 2026: prepare the next plan for **D021, D022, D023, D024 and D025**, retaining the expedited workflow and restrictions on repeated/out-of-scope testing. **This instruction commissions planning only. No signal implementation, proof admission or runtime testing starts in this turn.** The ten-case manifest and the precisely bounded prerequisites below are proposed for owner review; a subsequent instruction to execute this plan commissions that stated scope.

Baseline: `4885e144c7d214831f8e781ee939b2cf0f4a0cfb`, branch `work/v2-d021-d025-plan-20261022`. Accepted M00 and D011–D020 behaviours, physical tests, immutable briefs/contracts/generations and evidence remain preserved. The preceding root plan and its complete acceptance history are recoverable with `git show 4885e14:EXEC_PLAN.md`. Do not replay its completed work.

Execute in order **D021 → D022 → D023 → D024 → D025**, accept each individually, then stop. These are five signal work units; they do not require five simultaneous agents or five separate planning/review programmes. D024 depends on accepted D021 and actual D019/D020 producers. No D026+, retired D042/D043/D047 pilot, old gate schedule, live provider/TWS work, source certification, M00 mutation, migration or main merge is in scope.

`GUARDRAILS.md` remains frozen and governs authority/evidence. Preserve standing delegation for concrete controlled profiles and hash-bound admission; the plan cannot create domain authority or convert a proposal into acceptance.

## 2. Reuse before new work

Primary meaning: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`, K02/K03 and §§6–9,11–15,17; adjacent `NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, rows D021–D025. Preparation: `handoff/foundation_implementation/reuse_preparation/FAMILY_F05_PRICE_PATH_E11_E15.md` and the affected G2/G3 source-linked and typed-math rows. Reuse its established findings and literals. Do not repeat the 126-signal census, M01 audit, native-source investigation or earlier fixture research. Historical exhaustive falsifiers are not this tranche's test manifest.

Reuse these current M02 mechanisms rather than cloning them:

| Existing path under src/nvda_desk/market_measurement_truth/ | Reused proposition |
| --- | --- |
| `api.py` | WindowContextV1, WindowCalculationRequestV1, WindowMeasurementOccurrenceV1, ExactRatioV1 and existing owner/read contracts. |
| `_log_return.py` | Exact positive-price log ratio, rational remainder bounds, 50-significant-digit ROUND_HALF_EVEN output; fixed-anchor current/reference mechanism. |
| `_selection.py` | Public M00 history enumeration, receipt/event visibility, source/type/unit eligibility, duplicate/rank/paging checks where applicable. |
| `_window.py` | Exact-admission routing, existing public ID/history reads and logical occurrence identity. |
| `_evaluation.py` | Canonical typed encoding/decoding, including the repaired declared-scalar-type-alias handling. |
| `_record_store.py` | Existing immutable owner-local SQLite profile, atomic first fact, integrity checking and ordinary durable readback. |
| `_vwap_comparison.py` | Pattern for validating native selection identities and complete actual window-predecessor snapshots; do not copy its D018-specific equation. |

Normal construction of actual D019/D020/D021 prerequisites inside D024's cases is allowed. It is **not** permission to execute their old tests or strict claims. Never inject predecessor numbers, use private M01 calculators, calculate expectations with production helpers, or treat old green evidence as proof of new signal semantics.

Use the pinned CPython3.12.14 / SQLite3.53.1 environment and existing offline pytest9.0.3, mypy1.20.1, Ruff0.15.11 and PyYAML6.0.3. Check actual environment once on a genuinely new/resumed environment, then reuse it; do not rebuild or requalify it per signal.

## 3. Exact manifest — ten cases total

**Two cases per signal, one named parameterised test function per physical file. Maximum six remains an absolute ceiling, not a target: do not pad these two-case sets.** Success includes the complete relevant typed value, every required field/unit, definition/configuration/context/identity, selected raw and actual predecessor lineage, and ordinary public durable reopen. Refusal must reach its named incompatibility with otherwise lawful prerequisites and persist no occurrence.

Let:

- `L1 = 0.087011376989629766167765901873749540976783972605843`;
- `L5 = 0.18232155679395462621171802515451463319738933791449`;
- `L30 = 0.40546510810816438197801311546434913657199042346249`.

These are finite canonical 50-significant-digit, round-half-even log oracles for ln(12/11), ln(6/5) and ln(3/2). L1/L5 are reused from accepted D019/D020. L30 was prepared once during planning independently of production, using Decimal ln(3)−ln(2) at200digits then rounding to50; no product test was run. Assert exact Decimal tuples for scalar returns, with no comparison tolerance. Do not silently change precision, rederive these literals per worker, or replace finite numeric proof with a symbolic ln string.

| ID / path under tests/product/ | Case 1: positive and discriminating input | Case 2: precise refusal |
| --- | --- | --- |
| D021 / `market_measurement_d021/test_thirty_minute_log_return.py`; `test_d021_thirty_minute_log_return` | R143 current120 at T, reference80 at T−1800s; visible shorter100 at T−300s. Fixed1800s selection gives **L30**, not ln(120/100). | Retain current120 and shorter100, omit every eligible reference at/before T−1800s: refuse, never shorten to300s. |
| D022 / `market_measurement_d022/test_session_return.py`; `test_d022_session_return` | R037 current120 and R043 current-session open100, with explicit matching session identity: ln(6/5) = **L5**. | Current120 exists; same-valued R043100 is actually present from a different declared session, otherwise source/type/unit/receipt-valid: refuse. An empty M00 page or ordinary freshness failure cannot stand in for the session mismatch. |
| D023 / `market_measurement_d023/test_overnight_gap.py`; `test_d023_overnight_gap` | R037 current pre-market120 for target session and R042 previous **official** close80 for its explicitly linked previous session: ln(3/2) = **L30**. | Current120 exists; previous-session80 is actually present but is an intraday fact, not the official close: refuse. Do not replace the required official close with a numerically identical tick. |
| D024 / `market_measurement_d024/test_return_acceleration.py`; `test_d024_return_acceleration` | Actual compatible D019=L1, D020=L5, D021=L30 produced from public R143120/110/100/80 at T/T−60/T−300/T−1800. Retain all five named exact-rate fields specified below. | Produce lawful actual D019 and D020, with no eligible1800s history so actual D021 is absent; request has only the available predecessor IDs. Refuse because the mandatory third horizon is absent, not because another prerequisite is broken. |
| D025 / `market_measurement_d025/test_session_range_position.py`; `test_d025_session_range_position` | Explicit native R039 High109, R040 Low91, R037 Last94, same subject/session/snapshot: (94−91)/(109−91) = **ExactRatioV1(1,6)**. Asymmetry detects reversed High/Low. | High=Low=Last=91 with otherwise compatible complete inputs: refuse specifically on zero range. No clamping, rounding to a Decimal or inferred replacement range. |

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

## 4. File map and bounded prerequisites

Known missing capabilities are identified now rather than rediscovered mid-signal. They are proposed parts of the next execution commission, **not work performed or authorised for execution by this planning turn**:

1. **One declaration-only claim-loader extension:** `tools/product_proof_claims.py` currently enumerates D012–D020. Extend the fixed Literal identities, fixed iteration tuple and seven-row incorporated-byte counts to D021–D025 once. Bind that exact five-ID scope in D021's initial brief/binding under the execution commission; no separate preliminary review programme. Keep validators, target rules, hashes, partitions and immutable generation algorithms unchanged. Do not add dynamic claim discovery, alter the original hash-bound catalogue, redo the old149-control family, or extend controls per signal. Strict loading of the five actual admitted claims exercises the new declarations as those signals run; no preliminary runtime-control ceremony is added. A change beyond declarations must stop with its precise unproved obligation and proposed test list.
2. **One D024 result extension:** add the exact carrier in §3.2 to `api.py` and reuse existing typed union/dataclass decoding and `_record_store.py`. The existing D024 success/readback is its bounded qualification; no new schema/store/codec framework, generic fault suite or automatic negative typing specimen.

| Signal | Calculation files and fixed identities |
| --- | --- |
| D021 | Modify `_log_return.py` admission/horizon maps for D021/1800s; definition `D021-LOG-RETURN-1`, parameter `mmt-log-1800s-50d-half-even/1`. Reuse existing routing. |
| D022 | Add shared `_session_returns.py` for session-role selection and reuse the existing log function; route through `_window.py`. Definition `D022-SESSION-RETURN-1`, parameter `mmt-session-return-50d-half-even/1`, P_WINDOW. |
| D023 | Extend that same session-return module with the explicit previous-official-close/pre-market pairing; no second log implementation. Definition `D023-OVERNIGHT-GAP-1`, parameter `mmt-overnight-gap-50d-half-even/1`, P_WINDOW. |
| D024 | Add `_return_acceleration.py`, route through `_window.py`, and the single carrier extension above. Definition `D024-RETURN-ACCELERATION-1`, parameter `mmt-return-acceleration/1`, P_WINDOW. |
| D025 | Add `_session_range.py`, route through `_window.py`; existing ExactRatioV1. Definition `D025-SESSION-RANGE-1`, parameter `mmt-session-range/1`, P_BASIC. |

All module names above are relative to `src/nvda_desk/market_measurement_truth/`. Keep public `create_window_owner`, `create_window_reader`, WindowCalculationRequestV1 and MeasurementWindowReadsV1. Do not give individual signals their own API/store/registration architecture. New source-role policies and raw mappings are immutable signal configuration; exact constructors are recorded once in that signal's brief before RED.

Per ID Dnnn, use existing native paths:

- `handoff/foundation_implementation/authority/Dnnn_IMPLEMENTATION_BRIEF.md` and `Dnnn_PROOF_CONTRACT.json`;
- `implementation/authority/Dnnn_IMPLEMENTATION_AUTHORITY_BINDING.yaml`;
- `config/product_proof/market_measurement_dnnn/{claim.json,admission.json,generations/0001.json}`;
- the exact physical file/function in §3.

Format and inspect proof before sealing hashes. Retain the seven-row incorporated-byte convention and prospective concrete delegated admission. If a real repair changes admitted proof, retain its original generation and link a new one. Never overwrite accepted evidence or fabricate an independent adequacy judgement.

## 5. Hard execution budget

- **Exactly one admitted semantic RED and one final complete strict GREEN per signal.** Assign the final independent reviewer as the sole final runtime executor; no worker GREEN followed by reviewer GREEN, focused GREEN followed by aggregate GREEN, or rerun for commit/report/download.
- Strict command for each ID: `python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_dnnn`. The runner already checks readiness, binding, names, hashes, outcomes and governed bytes. Do not prepend duplicate validators except to diagnose an actual control failure. Use a clean admitted candidate; malformed authority/import/environment failure is not semantic RED.
- **No default pytest, architecture/bootstrap, promotion220, control149, old M00/M02 claims, mutation matrices, ad-hoc probes or final five-claim sweep.** Do not rename these activities compatibility, review or release checks to evade the limit.
- **No hidden cases:** helpers, loops, reviewer scripts and expanded bodies cannot introduce extra scenarios. Normal actual dependency construction and complete assertions inside the ten named cases are allowed. Prior generic retry/paging/fault/type evidence is reused where applicable; no recreated test matrix.
- **One independent final review per signal**, covering source, exact two cases and fixture sequencing. No separate design/proof/implementation approval rounds or whole-tranche runtime requalification. Satisfy fixture independence within those cases; no extra adversarial sequence.
- **One scoped mypy invocation and one changed-path Ruff invocation for the current delta.** Check the changed M02 package; when the fixed loader first changes, include that file once in the same scoped invocation. Do not repeatedly type/lint unchanged tools, run full-repository lint, add consumer specimens by default or have the reviewer repeat successful checks. Format proof before hash admission.
- After an actual failure, preserve the first result, diagnose the reached invariant, make a relevant material repair and repeat only the affected declared check. Explain the link in one line. Never retry unchanged code to chase green. A complete failed strict claim may repeat after repair; a successful GREEN does not.
- Additional tests or shared changes outside §4 require an explicit owner scope decision identifying the exact missing proposition and exact added test list **before execution**. No generic “applicable checks” exception. Missing required authority/capability stops only the dependent work; it does not authorise speculative downstream repairs.

## 6. Minimal worker cycle and handoff

For each signal, complete this one cycle without separate administrative work units:

- [ ] Read only affected authority/preparation and this plan; reuse established conclusions and settle the exact controlled profile.
- [ ] Prepare its two physical cases and minimum native authority/claim/generation files; inspect source/fixtures and formats before sealing. Incorporate the single §4 loader extension before the first admitted claim is run.
- [ ] Commit a clean admitted candidate; run the strict claim once for intended semantic RED, then implement only the named delta.
- [ ] Inspect the completed delta; obtain the scoped static results and one independent final review. The designated reviewer executes the sole final strict GREEN.
- [ ] Record one concise root acceptance entry: ID, candidate/tree/generation, changed paths, exact commands/outcomes, reused evidence, actual failure/repair, independent judgement and limitations; retain full logs under `handoff/foundation_implementation/dnnn_execution/`.
- [ ] Commit the accepted result and stop at the owner-designated boundary. At D025 or an explicitly requested delivery boundary, export one recoverable full-history bundle, verify the bundle itself and make it downloadable. Packaging/closing documentation does not trigger product retesting.

Do not add seven reports, review queues, implementation-independent checkpoint commits or per-signal archives. Reuse proven bytes and receipts. The owner has observed faster delivery; retain that direction without claiming a measured tenfold improvement. Record actual runtime outcomes and material rework concisely; no timing/benchmarking programme.

## 7. Current status

| Item | State |
| --- | --- |
| M00 and D011–D020 | Preserve accepted bounded state at baseline4885e144c7d214831f8e781ee939b2cf0f4a0cfb. Prior full disposition remains in that Git version of the plan and existing execution logs. |
| D021, D022, D023, D024, D025 | NOT_STARTED. Ten-case manifest and proposed controlled profiles prepared; no implementation/proof execution authorised by this turn. |
| Claim-loader declarations / D024 carrier | Known bounded prerequisites proposed in §4; not implemented. |
| This planning change | Root plan plus directly conflicting worker/README guidance only; textual diff/source inspection, no tests/mypy/lint. |

## 8. Execution commission and ledger — 23 October 2026

Owner instruction commissions D021 through D025 in order and a full-history verified downloadable checkpoint after each individual acceptance. This supersedes the planning-only stop and single-final-bundle schedule above. All other bounded case/review/check restrictions apply. Recovered c03f70f from the saved bundle into this isolated checkout; the older dirty D015 checkout is preserved untouched. Environment rebuilt once offline from the pinned hashed dev lock: CPython3.12.14, SQLite3.53.1, pytest9.0.3, mypy1.20.1, Ruff0.15.11, PyYAML6.0.3. Preflight: D021 extends the accepted fixed-log configuration; D024 consumes actual compatible D019/D020/D021 occurrences. Root ledger carries progress; no separate skill bookkeeping or extra qualification suites.

D021 first admitted candidate f8cb77a: strict semantic RED, two intended unsupported-owner failures after lawful public history setup. Candidate bce077f implements only fixed1800s admission, with scoped mypy18files and changed-path Ruff passing. The single final reviewer found an ISOLATED test context preparation error before final runtime: completeness remained12:30 instead of12:00. Repair changes that existing context literal only; generation1 retained and generation2 linked. No final runtime had run, no extra case or earlier test rerun. Static results reused: no source/type/lint-sensitive edit.

### D021 — ACCEPTED controlled profile

Final candidate b96b79091c55395c1011875849b93f1f3f255ce9, tree eb9a7709b597365f06c82ef34ec0398c2229d234, generation2 SHA256724e06bec1635893c5b3e4613cf96c463adab4af0054926225ff4678705086f9. Independent /root/d021_final_review ACCEPT; sole final strict command exit0,2passed0.38s. Scoped mypy18files/Ruff passed. Full first RED, final GREEN and independent judgement under d021_execution. Reused unchanged log/selection/record-store evidence; no old claim reruns. Native source/calendar certification remains held. Commit acceptance, verify/export checkpoint, then D022.

D022 candidate4c438d4 admitted generation1 reached semantic RED (2 unsupported-owner failures after both raw role projections present). New shared session-role selector validates native identity before ordinary numeric eligibility and retains actual projections. First scoped mypy caught a local string/RawSelectionIdentityV1 name collision; renamed only the occurrence-id variable, preserving the required selection identity. First output retained; rerun only affected static check (and changed-path Ruff for the source edit), before the sole final runtime.

### D022 — ACCEPTED controlled profile

Candidate87c5c8124cb4592c170ec8d65fa4ed827192889e, tree78f22db11e2a871e23734d3c6a673e4a79e218c4, generation1 SHA2566519b745d283dbffbaa4a18db0212ee7ed68787672e08321c0d348a6457d48d0. Independent /root/d022_final_review ACCEPT; sole strict final2passed0.24s exit0. Native wrong-session open is actually projected and otherwise role-time eligible; refusal reaches identity compatibility. All typed fields, selected raw lineage and public SQLite reopen passed. Scoped mypy18files and changed-path Ruff pass; first static collision output preserved. No extra cases/old claims/duplicate GREEN. Full records d022_execution. Native feed/calendar holds remain. Checkpoint after this acceptance, then D023.

D023 first candidate9ce8cfb strict execution stopped at collection syntax failure (exit5), not semantic RED: a generated native mapping tuple lacked two closing parentheses. Preserved raw output as collection_first_failure.log. Corrected syntax and formatted existing two cases before sealing linked generation2; generation1 preserved. No production behaviour written before valid semantic RED. The authoring helper now requires a successful completed format operation before hashes/admission, preventing this preparation mechanism from recurring.

### D023 — ACCEPTED controlled profile

Candidate267adf1c47f7bdff912fbc720aa3ffc7b9b13b5c, tree8ecf8149158806a6ab23a14f7dd1f2faec1cc36a, generation2 SHA256ec252ea5e144b12783c3957557293110676c8d75a486da68e865328411148e31. Independent /root/d023_final_review ACCEPT; sole final strict2passed0.33s exit0, complete native role, typed metadata/lineage and public SQLite reopening. Scoped mypy18files/Ruff pass. First collection failure preserved distinctly from semantic RED. D022 selector/log mechanism reused unchanged; no old tests or extra scenarios. Native source/calendar certification remains held. Checkpoint after acceptance, then D024.

D024 candidatec34eb9f strict semantic RED reached unsupported consumer after actual D019/D020/D021 construction (positive all3, negative onlyD019/D020). Implemented frozen five-field exact carrier, existing window dispatch and thin actual-predecessor calculation. Ultimate raw lineage is distinct current/one/five/thirty, while complete three predecessor snapshots preserve all edges; this follows existing typed tuple uniqueness. Scoped mypy19files passed. First Ruff found only new public export ordering; moved the export into lexical order, retained first output and repeated affected api.py lint only. No source meaning/test changes or extra consumer specimen.
