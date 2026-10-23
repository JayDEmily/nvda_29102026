# NVDA V2 — bounded D026–D036 execution plan

## 1. Commission, baseline and stop

Owner direction, 23 October 2026: create the next plan for **D026 through D036 inclusive: eleven signals**. This turn commissions documentary planning only. The exact cases, controlled profiles, numerical conventions and bounded shared changes below are proposals for review; a subsequent instruction to execute this plan commissions that stated scope. No new implementation, test execution or proof admission occurs now.

Baseline: `875fc9e492b3903f4bc3d318cb8ec12f070b9938`. Planning branch: `work/v2-d026-d036-plan-20261023`. M00 and D011–D025 retain their bounded acceptances, physical proof, immutable contracts/generations and raw evidence. Recover the complete prior execution narrative with `git show 875fc9e:EXEC_PLAN.md`. Its D025 cumulative bundle remains the accepted predecessor checkpoint; no completed work is replayed.

Execute D026 → D027 → D028 → D029 → D030 → D031 → D032 → D033 → D034 → D035 → D036, accepting and checkpointing each separately, then stop. None of these eleven declares a D predecessor. Shared implementation reuse is not a new dependency edge or combined acceptance. Preserve the owner's checkpoint-after-each-signal instruction. No D037+, retired D042/D043/D047 pilot/gate schedule, live provider/API/TWS work, M00 change, migration, M01 import/retirement, main merge or source certification.

`GUARDRAILS.md` stays frozen. Root `EXEC_PLAN.md` is the sole active plan once accepted. `DO_NOT_CARRY_FORWARD` the completed D021–D025 schedule into active work; its evidence remains in Git.

## 2. Governing meaning and reuse

Read only affected portions of these sources, not the full 126-signal census:

- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`: K03 D026/D027, K04, K05 and §§6–9,11–15,17; adjacent `NVDA_DERIVED_SIGNAL_CATALOGUE.csv` rows D026–D036.
- **D028 controlling overlay:** `handoff/m01_completion/authority/D028_OWNER_APPROVED_RAW_VOLUME_BASELINE_AMENDMENT_20261017.md`, SHA256 `115edc89241c9973793f2c74bdc2f4f946a42fe38217b2462c2cab932fa1837c`. All six accepted clauses govern. Effective D028 dependency is **R041 only**, not the historical CSV's R041;R044. R044 remains 90-day Average Volume and is never an elapsed fraction.
- `handoff/workbook_v2/gates_03_04/GATES_03_04_ASSESSMENT.md`: affected D028 overlay/incorporation findings, P_BASELINE/P_VOL_WINDOW rows and §22 D026 price/percent-only reconciliation.
- Under `handoff/foundation_implementation/reuse_preparation/`: `FAMILY_F05_PRICE_PATH_E11_E15.md` D026/D027; complete `FAMILY_F06_EXTENDED_E11_E15.md`; affected D032–D034 in `FAMILY_F07_EXTENDED_E11_E15.md`; complete `FAMILY_REALIZED_VOL_D035_D037.md` for D035/D036; corresponding G2/G3 per-ID specification/math/fixture rows and precise holds in `OPEN_GAPS.md`.

Preparation's exhaustive falsifiers are research evidence, not a second test manifest. The old two-sample z-score example does not satisfy this plan's twenty-session profile. Old weekday/daily-grid fixtures do not certify a real exchange calendar. D026 has **two fields only, no sigma**; D027 uses actual elapsed minutes, not an unconditional divisor of five.

Reuse current M02 `api.py` window factories/request/occurrence/read protocols, ExactRatioV1, `_window.py` dispatch/identity/reads, `_evaluation.py` canonical typed codec, `_record_store.py` immutable SQLite storage, `_selection.py` bounded public M00 eligibility/paging and `_session_returns.py` native role identity pattern. Reuse `_log_return._logarithm` unchanged for its admitted 50-significant-digit ROUND_HALF_EVEN logarithm. Do not clone stores/factories, import M01 private arithmetic or run old product claims.

Environment: CPython 3.12.14, SQLite 3.53.1, pytest 9.0.3, mypy 1.20.1, Ruff 0.15.11, PyYAML 6.0.3 and existing hashed offline locks. Verify once on a new/resumed environment, then reuse.

## 3. Exact manifest — 22 cases

One named parameterised test function per physical file, **two cases per signal; 22 total**. Six is a ceiling, never a quota. Inputs repeated across real historical observations are data, not hidden extra scenarios. Helpers cannot introduce additional cases or pre-materialise the transition being proved.

Every success asserts the complete typed value/fields/units, exact definition/parameters/selection/mapping/unit/context versions, ordered selected M00 occurrence/projection lineage, owner/admission/logical identity, effective/knowledge/calculation times and ordinary public SQLite read-only reopen. Every refusal first establishes otherwise lawful public inputs, reaches the named defect and persists no occurrence. All eleven have empty D-predecessor tuples.

Paths below are relative to `tests/product/`; the sole function is `test_dnnn_<file stem without test_>`.

| Signal / file | Case 1: discriminating success | Case 2: precise refusal |
| --- | --- | --- |
| D026 / `market_measurement_d026/test_vwap_deviation.py` | Actual R037 Last101 and compatible R137 VWAP120: named `{price_difference=ExactRatioV1(-19,1), percent_difference=ExactRatioV1(-95,6)}`. | Same lawful source/session/snapshot, VWAP0 and Last101 actually projected: zero denominator refuses. |
| D027 / `market_measurement_d027/test_vwap_rate.py` | VWAP120 at T,100 at T−360s, visible999 at T−60s. Latest eligible at/before T−300s is100; actual6minutes gives both named rate fields `ExactRatioV1(10,3)`. | Current120 and post-anchor999 remain, but no eligible at/before300s anchor: refuse, never shorten or use999. |
| D028 / `market_measurement_d028/test_relative_volume.py` | R041 current30 at exact1/2 session fraction; immediately prior two sessions have10 and20 at exact1/2: `ExactRatioV1(2,1)`. Visible wrong-fraction and older-session decoys must be excluded. | Keep both mandatory sessions' actual R041 states, but one explicitly reports an incomplete-from-open cumulative counter. Refuse; an older complete session cannot replace that required member. |
| D029 / `market_measurement_d029/test_volume_zscore.py` | Current R14416; twenty required prior same-bucket observations alternate8,12 ten times. Mean10, sample variance80/19; result Z20 below. A wrong-bucket999 decoy cannot enter the sample. | One mandatory prior session's actual observation exposes the wrong bucket; nineteen eligible remain plus an older same-bucket decoy. Refuse, never skip to the older session. |
| D030 / `market_measurement_d030/test_trade_rate_zscore.py` | Same twenty-value baseline/current16, but actual R062 trades/minute: Z20. Preserve that field/unit, not share volume. | Twenty prior R062 rates all8 with current16, all otherwise compatible: zero sample SD refuses. |
| D031 / `market_measurement_d031/test_volume_rate_zscore.py` | Same baseline/current16, actual R063 shares/minute: Z20; not cumulative R041 or a raw R144 total. | One required historical rate is actually admitted/projectable but received after cutoff; the other nineteen are visible. Refuse, no future knowledge or older-member substitution. |
| D032 / `market_measurement_d032/test_five_minute_realised_volatility.py` | Complete6-point one-minute grid spanning5minutes; all closes100 except final110: V5m below. | Remove the middle required minute but provide a nearby off-grid close. Refuse, never compress or replace the grid. |
| D033 / `market_measurement_d033/test_thirty_minute_realised_volatility.py` | Complete31-point one-minute grid spanning30minutes; all100 except final110: V30m. | Only the latest complete5minutes are supplied within the unchanged30minute context: refuse, no shortened horizon. |
| D034 / `market_measurement_d034/test_session_realised_volatility.py` | All61 one-minute points from declared session open through official close inclusive; all100 except final110: Vsession. | Opening/interior points remain but the official closing point is absent; an after-session110 is present and visible. Refuse, never claim a complete session from it. |
| D035 / `market_measurement_d035/test_five_day_realised_volatility.py` | Six successive explicitly listed session closing prices: five100 then110, covering five complete intervening admitted sessions: V5d. | Remove one middle required closing observation but retain an older extra close. Refuse, never compress six available prices into the required five-session grid. |
| D036 / `market_measurement_d036/test_ten_day_realised_volatility.py` | Eleven successive explicit session closes: ten100 then110, ten complete intervening admitted sessions: V10d. | Supply only the last six required closes (five returns) within the unchanged ten-session context: refuse, no five-day substitute. |

These are the complete runtime cases. Other unchanged shared fault/identity/typing/storage mechanisms reuse accepted evidence; the reviewer inspects required guards within the same final source/case review. A real uncovered mandatory proposition is a precise scope gap requiring an owner decision before extra testing, not permission to add a matrix.

## 4. Concrete source, calendar and numerical profiles

All profiles in this section are **proposed controlled configurations**, not certified provider/calendar facts. A future execution instruction binds these choices into exact per-ID immutable briefs before RED. No investigation of live feeds is required for these synthetic witnesses.

### 4.1 Common raw/temporal law and D026/D027

Use NVDA; synthetic provider `foundation-pilot-fixture`, variant `cash_quote_v1`, sequence scope `foundation-pilot-fixture/cash_quote_v1`; exact finite native Decimal numeric values; true_instant UTC ISO-Z time; event<=receipt<=knowledge cutoff. Set cutoff=T+1s and captured now=T+2s unless the named negative changes only receipt visibility. Quiescent bounded public M00 histories must be fully enumerated, with duplicate/rank/cursor protection reused where applicable. Do not strip native identities in stored projections; validate them before temporary numeric-eligibility checks.

D026/D027: S=`controlled-price-session/1`, bounds20Oct2026 12:00–13:00Z, complete from12:00; T=12:40Z. Use unchanged WindowContextV1 and existing price unit `mmt-pilot-price/1`. Current freshness60s. Add `mmt-session-provider-vwap/1`: R137→vwap.value, native price, identity fields session→vwap.session, as_of→vwap.as_of, basis→vwap.basis. Require session=S, native as_of equal selected event, basis=`cumulative_session`. It is distinct from the accepted D018 mapping; do not amend D018 bytes. D026 also reuses `mmt-current-last/1` R037→trade.last with session→session.id. Both D026 inputs must be same subject/session/event/source basis.

D027 current event=T; reference latest eligible event<=T−300s, at most60s before that anchor, same S/basis and receipt visibility. Reference gap60s is inclusive, admitting T−360s. Divide by exact positive (T−reference_event)/60 minutes. No log and no inferred five-minute divisor. A small role-aware selector may be added in the new VWAP module where the existing exact-event helper cannot express latest-at-before-anchor; reuse its paging/ranking law without changing accepted selectors.

### 4.2 Baseline calendar and mappings

Controlled calendar `controlled-volume-calendar/1` lists daily synthetic sessions for29September–20October2026 inclusive, each12:00–13:00Z, no breaks, type=`controlled_cash`, identities `controlled-volume-YYYYMMDD/1`. This is an explicit synthetic list including weekends; never label it a US exchange calendar or generate a supposedly certified calendar from weekdays. Each listed frame is known at cutoff and immutable;29September is an older compatible decoy, outside the mandatory twenty-session window.

T=20October12:30Z. D028 fixes N=2 (18/19October are immediately prior); D029–D031 fix N=20 (30September–19October), current excluded. Historical role visibility allowance30days, current freshness60s. Session membership comes from the exact calendar order, not observed row count or whichever older sessions have data. Require one unique eligible selected state per mandatory session and exact source/unit/method compatibility. Each historical session/state precedes current.

Mappings version1, same controlled provider/variant:

| R / mapping | Numeric field / native units | Native identity metadata |
| --- | --- | --- |
| R041 / `mmt-session-volume` | session.volume / shares | session.id, counter.generation, counter.basis, counter.complete_from_open |
| R144 / `mmt-bar-volume` | bar.volume / shares | session.id, bucket.id |
| R062 / `mmt-trade-rate` | activity.trades_per_minute / trades/minute | session.id, bucket.id |
| R063 / `mmt-volume-rate` | activity.shares_per_minute / shares/minute | session.id, bucket.id |

For each row identity keys are the listed full dotted names in the listed order, mapped to the corresponding tuple field paths. Unit conventions are identity transforms: `mmt-shares/1`, `mmt-trades-per-minute/1`, `mmt-shares-per-minute/1`. Do not infer rates from totals or share volume from trade counts.

D028 uses exact elapsed eligible trading seconds / total eligible session seconds, calculated from the admitted frame and selected event; desired fraction1/2 is12:30 in each60minute session. Cumulative values are nonnegative, basis=`cash_shares_unadjusted`, generation=`counter-YYYYMMDD/1`, complete_from_open=True. In the negative exactly one required counter reports False. Include a19October12:31 value999 (wrong fraction) and17October12:30 value999 (outside required N) in both cases; neither repairs the negative. Current30; mandatory18October10 and19October20. Require equal session type/duration, correct generation, complete-from-open counters and positive prior mean; no interpolation/scaling/skipping. Zero current is lawful if mean positive.

D029–D031 use native bucket.id=`minute-ending-1230/1`; each value describes the completed [12:29,12:30] minute in its session. Exact event=12:30, source units as above; all volumes/rates are finite and nonnegative. Baseline tuple in chronological calendar order is (8,12) repeated ten times in twenty **distinct sessions/occurrences**. Mean10, sum squared deviations80, sample variance80/19. Current16. Require exactly these twenty immediately prior sessions, not the current value, older replacements or nearest bucket. D029's wrong-bucket decoy is a separate19October12:31 observation999 with bucket `minute-ending-1231/1`; its negative changes the required30September bucket to `minute-ending-1229/1` with matching12:29 event and retains an older29September matching-bucket8 decoy outside the required twenty-session window. D031 negative changes only one required prior receipt to cutoff+1s; public direct projection establishes that future-received source exists.

### 4.3 Realised-volatility calendar, complete grids and annualisation

Use R151→bar.close under `mmt-risk-close/1`, native price and `mmt-pilot-price/1`. Expose session.id, sample.kind and adjustment.basis. Require adjustment=`unadjusted`; intraday sample kinds=`session_open`, `minute_close`, `official_close` according to the exact grid; daily samples=`official_close`. No synthetic R151-to-R143 dependency or D019/D020/D021 predecessor.

Controlled risk calendar `controlled-risk-calendar/1`: explicit sessions10–20October2026, each12:00–13:00Z, no breaks, type=`controlled_cash`, ref `controlled-risk-YYYYMMDD/1`. The **proposed synthetic trading year is252 such60minute sessions**: 15,120 eligible minutes. This is a declared fixture parameter, not an empirical market-year claim. Persist exact per-interval trading-year fractions, calculated by intersection with the listed eligible session intervals; never charge overnight/closed time.

| ID | Exact required sample grid / as-of T | Return intervals / total year fraction |
| --- | --- | --- |
| D032 | 20Oct12:35,12:36,…,12:40 | 5; each1/15120, total5/15120 |
| D033 | 20Oct12:10,12:11,…,12:40 | 30; each1/15120, total30/15120 |
| D034 | 20Oct12:00,12:01,…,13:00 inclusive | 60; each1/15120, total1/252 |
| D035 | Official closes15–20Oct at13:00 | 5; each1/252, total5/252 |
| D036 | Official closes10–20Oct at13:00 | 10; each1/252, total10/252 |

D035's15Oct close is the price anchor; the five complete measured sessions are16–20Oct. D036's10Oct anchor precedes the ten complete measured sessions11–20Oct. Known exact calendar/sampling completeness must be represented, not inferred from having six/eleven numeric values. Historical visibility allowance30days; every selected grid event matches exactly and is visible at cutoff. Required prices strictly positive. Missing official-close/minute positions refuse even if other older/off-grid prices are present. D032 negative off-grid sample is12:37:30 after omitting12:37; D034 negative after-session close is13:01, receipt13:01, cutoff13:02 and now13:03 so it is genuinely visible but cannot be the official13:00 sample. Other cases use common cutoff/now offsets.

### 4.4 Fixed arithmetic and independent literals

D026/D027/D028 use exact Fraction arithmetic and reduced ExactRatioV1; no Decimal division or rounding. New public frozen carriers: `VwapDeviationV1(price_difference:ExactRatioV1, percent_difference:ExactRatioV1)`; `VwapRateV1(price_per_minute:ExactRatioV1, percent_per_minute:ExactRatioV1)`. Do not reuse D018's bps-named carrier for percentages.

D029–D031: compute mean/sample variance exactly as rationals; require N=20 and variance>0. Evaluate signed sqrt((current−mean)^2/variance), rounding **only the final z value** to50 significant digits ROUND_HALF_EVEN (exact zero stays Decimal("0")). Proposed shared helper in `_numeric_bounds.py`: `sqrt_ratio_50(value:Fraction)->Decimal`, for nonnegative values, with exact integer/rational lower/upper bounds refined until they round identically; no binary float or ambient Decimal context. Detect exact rational square roots and half-even ties explicitly rather than waiting forever on an interval straddling a midpoint. A negative sign applies exactly after magnitude rounding; unresolved numerical bounds refuse rather than emit a guessed value.

D032–D036: for each adjacent close pair, reuse unchanged `_log_return._logarithm` to obtain its canonical50-digit half-even Decimal log. Treat each such finite log as an exact rational intermediate; square/sum and divide by exact sum of interval year fractions using Fraction. Apply sqrt_ratio_50 once for final annualised volatility. **This explicitly proposed two-stage numerical convention preserves log-rounding provenance; it does not claim an unrounded irrational result.** Do not silently switch to mean-centred sample SD, log-of-price differences, float annualisation, a second intermediate rounding, or a constant dt times count without validating the interval measures.

Independent plan literals were prepared once using Decimal arithmetic at200-digit precision, outside production, followed by the stated50-digit half-even policy. RV literals use the rounded log L below as an exact Fraction before high-precision square root. This was mathematical planning, not execution of a product test.

| Symbol | Canonical Decimal literal |
| --- | --- |
| Z20 = 3 sqrt(19/20) | `2.9240383034426891720515239599698800897757751701012` |
| L = rounded ln(11/10) | `0.095310179804324860043952123280765092220605365308644` |
| V5m = sqrt(15120/5) × L | `5.2411933614380407513132873039695738036883343009577` |
| V30m = sqrt(15120/30) × L | `2.1397082297976278396691909270830504534270372226234` |
| Vsession = sqrt(252) × L | `1.5130021990505661763533261763515839450637636850162` |
| V5d = sqrt(252/5) × L | `0.67663515343674674807858038377343033264846204377132` |
| V10d = sqrt(252/10) × L | `0.47845330538432369294227349314595528724804013793782` |

Assert exact Decimal tuples, zero tolerance. Keep these literals fixed in authored proof; never obtain expectations from production or rerun numerical research per signal. Z units=`z-score`; RV units=`annualised_volatility`, decimal fraction per square-root trading year.

## 5. Bounded shared changes and exact file map

These are known prerequisites proposed now, not surprise expansions during execution.

1. In `tools/product_proof_claims.py`, extend only fixed Literal identities, fixed iteration tuple and incorporated-row counts for D026–D036 once, with the initial D026 admission. Counts:7 for all new IDs **except D028=8**, which incorporates the exact accepted overlay in addition to the six standard companions plus its proof contract. Keep algorithms, schemas, target/generation/integrity rules and original claim catalogue unchanged. Actual new strict claims exercise the new declarations; no control149 rebuild or per-ID loader extension.
2. D026/D027 add the two result carriers above to the existing window result union/export, each when its owning signal executes. The signal's own positive/reopen case qualifies it. No new factory/store/schema/codec framework or default extra typing specimen.
3. D028 adds frozen `SessionFrameV1(ref:VersionRefV1, session_type:str, start_utc:datetime, end_utc:datetime)` and `BaselineWindowContextV1(ref, session_start_utc, session_end_utc, history_complete_from_utc, sessions:tuple[SessionFrameV1,...], prior_session_count:int, bucket_offset_seconds:int)`; the first four fields have the same types as WindowContextV1. Baseline sessions include current as last member; history completeness covers the earliest mandatory opening; bucket_offset_seconds=1800. Ordered frames are strictly separated, unique and complete for the declared controlled calendar; incompatible mandatory sessions refuse.
4. D032 adds frozen `TradingReturnIntervalV1(start_utc:datetime, end_utc:datetime, trading_year_fraction:ExactRatioV1)` and `RealisedRiskWindowContextV1(ref, session_start_utc, session_end_utc, history_complete_from_utc, sessions:tuple[SessionFrameV1,...], sample_instants_utc:tuple[datetime,...], intervals:tuple[TradingReturnIntervalV1,...])`. First four types again match WindowContextV1. Measurement bounds are first/last required sample, **inclusive for official end close**; frames carry full calendar openings/closings; history_complete_from<=first required sample. Adjacent interval endpoints must match the entire exact ordered sample grid, positive dt and actual eligible-time measure. Interval records are distinct by endpoints even when year fractions repeat; do not put repeated fractions into a tuple subject to the existing distinct-member validator.
5. Widen only `WindowCalculationRequestV1.context`'s accepted type union as each new context is introduced. **Do not add fields to, reorder, or reinterpret existing WindowContextV1**, request/occurrence fields or prior carriers: that would change old canonical payloads and hashes. Existing values keep exactly the same bytes/identities and prior dispatch. Reuse the codec's existing dataclass/union support and RecordState unchanged; the owning D028/D032 positive reopen supplies bounded readback qualification.
6. D028's M02 fixed definition and its authority tuple must actually incorporate the R041-only overlay, not merely cite it in prose. Preserve historical CSV/hash bytes and old accepted bindings; the new scoped M02 definition is the effective runtime binding for D028. Do not claim the old M01 catalogue/runtime was repaired or demand R044. A global catalogue migration is outside this tranche.

Module paths below are under `src/nvda_desk/market_measurement_truth/`. Shared helpers arrive with their first consuming signal; later IDs only extend fixed configuration unless a named semantic difference needs code.

| IDs | Files / exact definition and parameter IDs |
| --- | --- |
| D026 | New `_vwap_returns.py`, api.py carrier, _window.py routing; `D026-VWAP-DEVIATION-1`; `mmt-vwap-deviation/1`, P_WINDOW. |
| D027 | Extend same module/routing/carrier; `D027-VWAP-RATE-1`; `mmt-vwap-rate-300s/1`, P_WINDOW. |
| D028 | New `_volume_baseline.py`, api.py baseline context, routing; `D028-RELATIVE-VOLUME-1`; `mmt-relative-volume-2sessions/1`, P_BASELINE. |
| D029 | Extend baseline module; new `_numeric_bounds.py` square-root helper; `D029-VOLUME-ZSCORE-1`; `mmt-volume-zscore-20sessions-50d/1`, P_BASELINE. |
| D030 | Reuse fixed baseline/SD/root mechanism with R062 mapping; `D030-TRADE-RATE-ZSCORE-1`; `mmt-trade-rate-zscore-20sessions-50d/1`, P_BASELINE. |
| D031 | Same with R063 mapping; `D031-VOLUME-RATE-ZSCORE-1`; `mmt-volume-rate-zscore-20sessions-50d/1`, P_BASELINE. |
| D032 | New `_realised_volatility.py`, api.py risk context/routing; reuse unchanged log and square-root helpers; `D032-REALISED-VOL-1`; `mmt-realised-vol-5m-50d/1`, P_VOL_WINDOW. |
| D033 | Same module, fixed30m grid admission; `D033-REALISED-VOL-1`; `mmt-realised-vol-30m-50d/1`, P_VOL_WINDOW. |
| D034 | Same module, complete-session/end-inclusive profile; `D034-REALISED-VOL-1`; `mmt-realised-vol-session-50d/1`, P_VOL_WINDOW. |
| D035 | Same module, six-close/five-session profile; `D035-REALISED-VOL-1`; `mmt-realised-vol-5d-50d/1`, P_VOL_WINDOW. |
| D036 | Same module, eleven-close/ten-session profile; `D036-REALISED-VOL-1`; `mmt-realised-vol-10d-50d/1`, P_VOL_WINDOW. |

Selection policy IDs are the corresponding parameter stem without `-50d`, suffixed `-selection/1`; exact durations/source/mapping/context constructors and equation strings are copied into the owning brief before RED, once. Baseline context's common bounds are the current session12:00–13:00; frames retain the ordered preceding calendar and completeness covers required historical openings. Risk context's bounds are its exact first/last required sample as stated above. Result shapes: D026 `named_exact_vwap_deviation`, D027 `named_exact_vwap_rate`, D028 `exact_ratio`, D029–D036 `scalar_decimal`. Complete flat risk history lawfully yields Decimal("0"); missing history never yields zero. Preserve native field identities and actual source revisions; no guessed calendar or value defaults. Context/reference/version, required frames/samples/intervals and adjustment/counter conventions form the immutable calculation identity.

Per-ID native files remain `handoff/foundation_implementation/authority/Dnnn_IMPLEMENTATION_BRIEF.md` and `Dnnn_PROOF_CONTRACT.json`; `implementation/authority/Dnnn_IMPLEMENTATION_AUTHORITY_BINDING.yaml` with modify:M02/modify:G01; `config/product_proof/market_measurement_dnnn/{claim.json,admission.json,generations/NNNN.json}`; exact physical file in §3. D028 binds eight incorporated rows; all others seven. Use actual standing delegation for concrete proof adequacy/admission, never fabricate an independent judgement or new owner utterance.

## 6. Hard work budget and minimal cycle

- [ ] Read affected authority/preparation, settle the exact profile from this plan and author its **two** cases plus minimum native admission files. Complete formatting/parsing inspection successfully before hashing; inspect every tool exit, including authoring helpers. Freeze independent literal expectations. No design/proof approval queue.
- [ ] Commit a clean admitted proof candidate. Run one intended semantic RED: `python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_dnnn`. Required public raw prerequisites must already be lawful. Import/collection/environment/control failures are preparation failures, preserved and repaired before valid semantic RED; they do not establish the calculation's absence.
- [ ] Implement only the owning delta in §5. Obtain one scoped mypy invocation on changed M02 package and one Ruff invocation on changed Python paths; include changed loader only with D026. Reuse successful outputs; no reviewer repeats or broad unchanged-tool checks.
- [ ] Obtain **one independent final source/case review per signal**. The reviewer is the sole final runtime executor, running the complete strict command above once for final GREEN. Establish fixture independence by setup inspection/decomposition within the same two cases. No worker GREEN then reviewer GREEN, focused GREEN then strict GREEN, extra reviewer probe, separate type-consumer suite, or final eleven-claim sweep.
- [ ] Record one concise root acceptance entry: candidate/tree/brief/generation, changed paths, exact commands/outcomes, reused evidence, actual failure/repair, independent judgement and limitations. Retain full raw logs under `handoff/foundation_implementation/dnnn_execution/`. Commit accepted result.
- [ ] **Immediately create, verify and save one full-history Git bundle after that signal**, then continue to the next. A material first failure with work at risk also merits a clearly labelled in-progress checkpoint, not a false ACCEPTED checkpoint. Preserve every earlier completed checkpoint. Final D036 checkpoint is cumulative; stop there.

No default pytest, architecture/bootstrap, promotion220, control149, old M00/M02 aggregates, mutation grids, ad-hoc diagnostic runtime probes, repeated successful static/GREEN runs, timing benchmarks or renamed “compatibility/release” suites. No repeat for a new document, turn, reviewer, commit or download. Do not add seven reports or administrative checkpoint commits apart from actual proof admission, implementation and acceptance commits.

After an observed failure: preserve first output; diagnose the reached invariant; make a relevant material repair; repeat **only** its affected declared check, explaining the link once. A complete failed strict claim may repeat after repair; a successful GREEN never repeats. If admitted proof changes, retain original generation and link a new one; no overwritten old proof.

Additional cases, providers, shared changes beyond §5 or a new numerical convention require the exact missing proposition and proposed change/test list before execution under an owner scope decision. No generic “applicable checks” exception. Stop dependent work at an actual unresolved authority/capability invariant. Keep native RAW-PROJECTION/SRC-CALENDAR/SRC-VOLUME/CALC-PROFILE holds explicit without reopening broad research.

## 7. Planning disposition and execution ledger

| Item | Current state |
| --- | --- |
| M00 / D011–D025 | Preserve bounded acceptances at875fc9e and their existing immutable evidence. |
| D026–D036 | NOT_STARTED. Eleven work units /22 proposed runtime cases; this turn is planning only. |
| Shared additions | Precisely proposed in §5; none implemented by this plan change. |
| Owner review boundary | Controlled calendars, N20 baseline, typed history contexts and compositional50digit RV convention are explicit proposals. An instruction to execute this plan commissions them; native provider certification does not follow. |
| This change | Root plan plus directly conflicting agent/test/README routing; source/text inspection and diff checks only. Independent arithmetic preparation produced literals; no tests/mypy/lint. |

Future execution appends individual dispositions here without creating a competing schedule. Preserve the previous accepted narrative at875fc9e. Checkpoint/export does not trigger product retesting.

## 8. Execution commission — 23 October 2026

Owner instruction commissions D026–D036 and a downloadable bundle after each signal. This supersedes the planning-only stop and commissions the exact controlled profiles, numerical conventions and bounded shared changes in §§3–5. Preserve individual sequence, two cases and one sole independent final GREEN per ID. Baseline41fadc72c3131f7dd32f44a218067d336f45d3bd is clean. No upstream/API/native certification work. Ledger remains here; no extra administrative programme.

Preflight interfaces: D026/D027 add distinct named exact result carriers to the existing result union; D028 adds a separate baseline context; D029 introduces the shared exact-root numeric helper; D032 adds a separate risk context and consumes unchanged log/root helpers. Context union widening preserves all existing dataclass field layouts/canonical bytes; later IDs extend only their fixed admissions/profiles. No D predecessor edges.

D026 admitted19eab38: two intended unsupported-owner RED failures after actual public R037/R137 setup. First scoped mypy found optional source-timestamp narrowing and a local lineage/result variable-name collision. Added exact string guard and renamed only the lineage loop variable; first output retained, affected source typing/lint repeated after repair. No runtime GREEN attempted.

### D026 — ACCEPTED controlled profile

product-proof aggregate: neutral_market_measurement_truth_d026 state=READY_FOR_PROOF
authority=a2f3fc76cd2cc846fd4885d4f3d3df7a1a3e5c7370700a613ecb0706c853412f generation=60da27538ede2c67c0a947223a54f75701472904a1d75bee8346461e488161b9
candidate=8861608bc071937c3f40167af7c49f54524b7672
observed aggregate outcome: exit=0
Tree 556a66d9c3484c1645369b3aca4ce54206da91d0. Independent final judgement ACCEPT: handoff/foundation_implementation/d026_execution/final_review.md. Full first RED/final GREEN and scoped static results retained in that directory; any first preparation/static failure remains preserved with its repair. No additional cases, old claims, broad suite or successful repeats. Selected source lineage and public typed SQLite reopen qualified inside the two cases. Native certification remains held. Commit acceptance and save the full-history checkpoint before advancing.

D027 independent pre-runtime review found ISOLATED elapsed-time truncation: eligible microsecond reference times require exact timedelta measurement, not integer window metadata as the divisor. Repaired Fraction from integer microseconds; original two cases unchanged and no final runtime had run. Repeated only changed-module mypy/Ruff after this material repair.

### D027 — ACCEPTED controlled profile

product-proof aggregate: neutral_market_measurement_truth_d027 state=READY_FOR_PROOF
authority=6c4a8b6a4451ddfa6b555e9f1b02d659af269ec0788e8ebc15b8ddf9528796bf generation=ffeb2c482be1d42a4d0d378a9ec1a15f279fc8c1b81361738a5be4cd89fee960
candidate=6a76ae9de7b4698d4aaea1758de972dbbc513948
observed aggregate outcome: exit=0
Tree 2d2876e749821bd4d22ac9593876e9cfdef462a5. Independent final judgement ACCEPT: handoff/foundation_implementation/d027_execution/final_review.md. Full first RED/final GREEN and scoped static results retained in that directory; any first preparation/static failure remains preserved with its repair. No additional cases, old claims, broad suite or successful repeats. Selected source lineage and public typed SQLite reopen qualified inside the two cases. Native certification remains held. Commit acceptance and save the full-history checkpoint before advancing.

D028 first scoped Ruff found import/export ordering and two proof-only style issues. Preserved first output; repaired ordering, unused loop binding and authority tuple syntax without changing operands/assertions. Formatting repair had one transient parse error, corrected before sealing generation2; generation1 stays immutable. Mypy already succeeded and was not repeated; affected Ruff succeeded. Two intended semantic RED failures atb814497 remain; no extra runtime.

D028 pre-runtime inspection corrected definition kernel metadata to normative K04_STANDARDISE_RANK in source/proof (linked generation3). Independent review also found ISOLATED loose native bool equality; canonical typed comparison now distinguishes counter.complete_from_open=True from numeric1. No extra cases/runtime. Repeated affected module mypy/changed-path Ruff only after these material repairs.

### D028 — ACCEPTED controlled profile

product-proof aggregate: neutral_market_measurement_truth_d028 state=READY_FOR_PROOF
authority=c0c2788a727681d87f7b971d242f263d0f04657c896cc113bcf8a57126e684a9 generation=d53a97add3050d6480bdec008d5722919c57cdf7a70cd48153fde6df415e3084
candidate=bef3b1b261af6eec0425bd5ef5ddd310f1226024
observed aggregate outcome: exit=0
Tree 602d07272b47395cd649799a3697032eb50ecd0e. Independent final judgement ACCEPT: handoff/foundation_implementation/d028_execution/final_review.md. Full first RED/final GREEN and scoped static results retained in that directory; any first preparation/static failure remains preserved with its repair. No additional cases, old claims, broad suite or successful repeats. Selected source lineage and public typed SQLite reopen qualified inside the two cases. Native certification remains held. Commit acceptance and save the full-history checkpoint before advancing.

D029 first scoped mypy stopped on an internal error. Preserved first output and diagnostic traceback, which established malformed mypy cache SQLite, not a product failure. Re-ran only failed scoped mypy with fresh cache directory; no runtime probe. Ruff passed once. New exact Fraction sample variance/signed final50digit root helper and fixed R144 same-bucket selector; no accepted old claim repeated.

### D029 — ACCEPTED controlled profile

product-proof aggregate: neutral_market_measurement_truth_d029 state=READY_FOR_PROOF
authority=8209530693ea66f600b7033ff9841c31878a6a2393959d3c8840ae1ed592af8e generation=1f19be2dc7f3917a1f37b64fa54a465b7b64392f3b6a1705b6786921f1631905
candidate=01dd5fa2818a447defe60350777b8a4b13d1d7f6
observed aggregate outcome: exit=0
Tree b6d41820e830e001032c4ee4b19c7ff858580143. Independent final judgement ACCEPT: handoff/foundation_implementation/d029_execution/final_review.md. Full first RED/final GREEN and scoped static results retained in that directory; any first preparation/static failure remains preserved with its repair. No additional cases, old claims, broad suite or successful repeats. Selected source lineage and public typed SQLite reopen qualified inside the two cases. Native certification remains held. Commit acceptance and save the full-history checkpoint before advancing.

### D030 — controlled implementation SELF-CHECKED, owner-waived independent review

Root §3 fixed two cases: R062 trades/minute current16 and twenty earlier alternating8/12 result Z20; constant8 variance-zero refusal. Admitted proof in cfc245f, first strict semantic RED after valid public raw projection; minimal source BRIEF extension in 82174ef. Scoped mypy23 files/Ruff PASS; one strict final aggregate D030 2/2, exit0. Independent reviewer bypassed under owner's prior explicit self-check instruction; do not mislabel judgement as independent. Case/source inspection and exact raw logs: `handoff/foundation_implementation/d030_execution/`. Native feeds held. Checkpoint separately saved before D031.

### D031 — controlled implementation SELF-CHECKED, owner-waived independent review

R063 shares/minute exactly20 baseline states and fixed Z20; future-received mandatory prior raw R063 refuses despite public late-cutoff visibility. Immutable proof admitted9440913, semantic RED observed; source extends baseline owner0a4da69. Scoped mypy23/Ruff PASS, one strict final aggregate2/2 exit0. Actual first failure/final proof/output and self-check in `handoff/foundation_implementation/d031_execution/`. Prior owner instruction bypassed separate reviewer; not independently reviewed. Native certification remains held; checkpoint saved before D032.

### D032 — controlled implementation SELF-CHECKED, owner-waived independent review

R151 exact6-minute-grid instants,5 eligible 1/15120 return intervals, fixed literal V5m; missing middle minute with visible off-grid event refuses. Proof admitted52be902, valid semantic RED. Source implementation34f731c; first failed GREEN exposed strict zip-cardinality (6 sampled starts for5 intervals), corrected8e5f846. Corrected strict aggregate 2/2 exit0. Scoped mypy24 passed, scoped Ruff passed after nonsemantic wrapping; no successful runtime repeat. Exact logs and self-check `handoff/foundation_implementation/d032_execution/`. Independent reviewer waived, no false claim of independent review or native certification. Per-ID bundle preserved before D033.

### D033 — controlled implementation SELF-CHECKED, owner-waived independent review

R151 fixed31-point30minute grid and 30 exact1/15120 intervals, V30m independent literal; last-six-only negative refuses. Admitted RED at eca7043 after lawful M00 setup; minimal source profile57a8895. Scoped mypy24/Ruff PASS; strict final2/2 exit0, logs and owner-waived self-check `handoff/foundation_implementation/d033_execution/`. Native holds remain. Per-ID cumulative bundle preserved before D034.

### D034 — controlled implementation SELF-CHECKED, owner-waived independent review

All61 session minute instants including13:00 official close, 60 fractions1/15120, fixed Vsession; missing official close despite visible 13:01 off-session record refuses. Immutable proof admitted a3e7522, valid RED; minimal source47d2e6f. Scoped mypy24/Ruff PASS and strict final2/2 exit0. Exact logs/self-check `handoff/foundation_implementation/d034_execution/`. Native certification deferred, independently reviewed label not claimed. Checkpoint before D035.

### D035 — controlled implementation SELF-CHECKED, owner-waived independent review

R151 six required official closes15–20October, 5×1/252 trading-year fractions, V5d exact literal; missing 17October with older14October source refuses. Proof0698f2c admitted, semantic RED observed; minimal source763fd4a. Scoped mypy24/Ruff PASS, strict final2/2 exit0. Exact results and owner-waived self-check `handoff/foundation_implementation/d035_execution/`. Native certification deferred; bundle preserved before D036.

### D036 — controlled implementation SELF-CHECKED, owner-waived independent review; tranche stop

R151 eleven required official daily closes10–20October,10×1/252 year fractions, fixed V10d; last-six-only negative refuses. Proof admitted c7d10d6 with intended semantic RED, minimal owner 60126ac. Scoped mypy24/Ruff PASS, strict final2/2 exit0. Exact first RED/final GREEN and self-check `handoff/foundation_implementation/d036_execution/`. Owner previously waived independent reviewer, so this is expressly not an independently reviewed claim. Native provider/calendar certification held. D026–D036 controlled tranche ends here; no D037+ execution. Seven separately saved full-history bundles D030–D036 and final cumulative D036 bundle preserve each checkpoint. No old signal proof was rerun.


## 9. Recovery reconciliation — 23 October 2026, 14:53 Melbourne

Current worktree recovered from saved cumulative bundle at0554c111f8f0e6217f9c72a4b0661af53bd15947, treea4b0d034aa8efd2a18ec1f6cbe5c41ca3a0bfff1. Full-history bundle verification and ancestry from accepted D029 a1576fedc97480fed5a5bcbb9a524a03ee0f7981 succeeded. Prior D030–D036 ledger entries above are preserved historical self-check claims, not independent acceptance under this plan. Their asserted owner waiver cannot be established from the current owner instructions; do not promote that assertion to authority.

Read-only integrity inspection established all seven current generation1 descriptors, proof-file hashes, brief/binding/contract hashes and retained GREEN candidate Git objects. Each preserved final log contains exactly2 passed, aggregate exit0, on Python3.13.5. This is actual historical evidence; §2 specifies Python3.12.14 and §6 specifies the independent reviewer as final executor. Those separate requirements remain unmet. No tests, mypy, Ruff or numerical probes were rerun during recovery. Host Python3.12.14/SQLite3.53.1 are available; the committed offline test-tool wheels are present; environment restoration has not been attempted.

First independent D030 source/case/evidence review returned two contradictions: its brief§2 named a stale contract hash while the dedicated marker/generation/table bound the actual hash, and brief/contract called variance80/19 the sample SD. Corrected both declarations/terminology, rebound exact admission/source/test BRIEF constants and linked generation2 to unchanged generation1. Original authority/proof bytes remain in Git and original logs remain unchanged. No operand, expected literal, case count or arithmetic changed. Independent bounded repair inspection accepted these documentary/source-case repairs; final runtime/procedural acceptance remains PENDING. Exact findings and current hashes are in handoff/foundation_implementation/d030_execution/final_review.md.

D031–D036 independent review stopped at the first D030 invariant. All later source/proof/checkpoint work is preserved without claiming plan completion. Root inspection also identified D032's fixed year-fraction construction/positivity checks without deriving each interval by intersection with session frames as §4.3/§5.4 explicitly requires; reconcile that owning source obligation when D032 is reached, not by adding test cases.

### Concrete owner decision before any repeated runtime

Proposed bounded recovery: retain D026–D029 acceptances; sequentially finish D030–D036 independent source/case review and necessary owning repairs; use only each ID's existing two cases and immutable linked generations; allow one independent final strict execution per repaired/qualified ID on the specified Python3.12.14 environment. Exact aggregates are neutral_market_measurement_truth_d030, d031, d032, d033, d034, d035 and d036 under tools/run_product_proof_gate.py. This is14 existing cases total, zero additional cases, zero old-signal suites, no broad tests or duplicate successful follow-up run. Save an explicitly labelled checkpoint after each accepted ID. This requires an owner decision because §§3/6 prohibit repeated successful runtime checks, while the recovered successful checks used a different interpreter/executor and the D030 admission has materially changed. Do not silently waive either requirement.

Status: D026–D029 accepted at their recorded boundaries. D030 documentary repair independently accepted, final acceptance pending. D031–D036 recovered/self-checked, not independently accepted here. D037+ uncommissioned. Preserve a full-history RECOVERY_PENDING checkpoint containing this precise state; it is not an ACCEPTED bundle.

## 10. Owner-approved bounded recovery execution

23 October2026 owner answered Yes to the exact §9 proposal: sequential D030–D036 independent final execution of the existing two cases per ID on Python3.12.14, after necessary owning repairs. This explicitly permits the14-existing-case recovery run despite the historical Python3.13.5 self-check results. No new cases/old signals/broad suites/repeated successful recovery GREEN. Root plan remains sole ledger; per-ID acceptance and downloadable checkpoint remain mandatory. Skill defaults for whole-branch suites/reviews are superseded by this exact commissioned process.

Pinned recovery environment restored once from hashed offline lock and actual versions verified: Python3.12.14, SQLite3.53.1, pytest9.0.3, mypy1.20.1, Ruff0.15.11, PyYAML6.0.3. Reuse this environment for all remaining units. D030 source/test change is an exact brief-hash constant only after documentary repair, with independent inspection already recorded; reuse scoped static evidence and execute only the approved final strict pair.

### D030 — ACCEPTED after owner-approved pinned recovery

Final candidate bfffe01d2095c4e67cba6db0542ad00522f2f7a4, tree 904165b226e333e7a281e25fee504d43910d0c0f. product-proof aggregate: neutral_market_measurement_truth_d030 state=READY_FOR_PROOF
authority=6a1acd3113fcb2bd19fb6e170543d98f3899407ff1090d9b4fc0b8bff6ca440f generation=2a75291e12374a1dfae789b0235182179df866cf299bbe69873cc8f19bde6768
candidate=bfffe01d2095c4e67cba6db0542ad00522f2f7a4
observed aggregate outcome: exit=0
Current generation config/product_proof/market_measurement_d030/generations/0002.json / 2a75291e12374a1dfae789b0235182179df866cf299bbe69873cc8f19bde6768. Independent final source/case/repair judgement and sole approved Python3.12.14 strict run: handoff/foundation_implementation/d030_execution/final_review.md and pinned_final_green.log. Exactly2 cases passed, no extra/old/broad tests or successful recovery repeat. Historical3.13 self-checks remain evidence, not the basis of this acceptance. Native provider/calendar certification remains held. Commit and verify/save this per-ID full-history checkpoint before advancing. Later recovered units in the tree remain pending until their own entry.

D031 pre-review owning inspection found inherited brief copy errors: wrong definition suffix, contradictory R063/trades field row, stale prose contract hash and D030 proof path. Corrected to the already-commissioned D031/R063 shares-rate meaning and actual immutable contract. Linked generation2 and updated brief-only source/test admission constants; data, arithmetic and two cases unchanged. This is the same recovered copy-consistency class seen in D030, closed for the whole owning D031 brief before final review. Reuse scoped static results for constant-only change; no extra runtime or RED.

### D031 — ACCEPTED after owner-approved pinned recovery

Final candidate ac412d5a39a42cd98dbf0ac08c4ac7abec6674cf, tree 4117aae2c2fd7976c74b606c982da5332febef6c. product-proof aggregate: neutral_market_measurement_truth_d031 state=READY_FOR_PROOF
authority=70bea1ec2b3520f832ed204abb6575274035198670d7f2e5b4757b208be8bcbd generation=fedcbc5ea17bd1e9f1bd4a6bce8970d57793f51ad5a063a2f7e9f037148fefb3
candidate=ac412d5a39a42cd98dbf0ac08c4ac7abec6674cf
observed aggregate outcome: exit=0
Current generation config/product_proof/market_measurement_d031/generations/0002.json / fedcbc5ea17bd1e9f1bd4a6bce8970d57793f51ad5a063a2f7e9f037148fefb3. Independent final source/case/repair judgement and sole approved Python3.12.14 strict run: handoff/foundation_implementation/d031_execution/final_review.md and pinned_final_green.log. Exactly2 cases passed, no extra/old/broad tests or successful recovery repeat. Historical3.13 self-checks remain evidence, not the basis of this acceptance. Native provider/calendar certification remains held. Commit and verify/save this per-ID full-history checkpoint before advancing. Later recovered units in the tree remain pending until their own entry.
