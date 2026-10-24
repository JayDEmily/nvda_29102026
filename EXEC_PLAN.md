# NVDA V2 — D057–D076 bounded ExecPlan

Date: 24 October 2026 (Melbourne).
Status: OWNER ACCEPTED AND EXECUTION AUTHORISED on 24 October 2026 by explicit current instruction: “No, I accept it. I authorize. Proceed.” The five §5 holds remain; execute resolved units numerically. All five held IDs are explicitly owner-deferred under §§13–14; continue the resolved units in ascending order. The planning-only restrictions below describe the prior planning commission, not the current execution commission.
Baseline: `d0a905292c7439aec5bd9f099700f0ac58bdda25`.
Branch: `work/v2-d057-d076-plan-20261024`.

## 1. Goal and authority boundary

Prepare the next twenty original signal identities, D057 through D076, retaining the established efficient per-signal process. The owner requested the plan and independent review, preferably within two review rounds; more rounds are permitted for material unresolved issues. This request does not revive the completed D037–D056 schedule or commission product execution.

The prior three-signal plan/acceptance ledger remains exactly recoverable at `git show d0a9052:EXEC_PLAN.md`; the prior twenty-signal ledger is `git show fc82a07:EXEC_PLAN.md`. DO_NOT_CARRY_FORWARD their completed schedules as active work. Preserve all accepted source/tests, immutable generations, original failures/repairs and accepted checkpoints. No merge/push/history rewrite or GUARDRAILS.md modification.

This draft specifies controlled source/numeric proposals for fifteen foundation units and names five unresolved entry conditions. It does not pretend all twenty are immediately runnable: D061/D062/D064/D065/D070 are BLOCKED for the precise reasons in §5. No new runnable physical cases exist now. The eventual budget is two cases per resolved signal (at most forty initial cases if all twenty are resolved), not forty currently admitted cases. Six per signal is the absolute ceiling, never the target or permission to expand.

Owner review/acceptance and a separate execution commission are required. Proposed controlled choices below become authority only through explicit owner acceptance; the earlier full completion delegation applied to D040/D041 and does not silently approve new strategy parameters or a new peer. Accepted equations/identities are distinct from proposed source/profile conventions.

## 2. Evidence reuse and scope

Read current GUARDRAILS.md, AGENTS.md and applicable tests/AGENTS.override.md; obey their hierarchy. Fully read the applicable semantic authority, then reuse valid unchanged family/source/context inspection by Git identity/hash. Restrict later worker/reviewer context to the current signal, actual owning delta/dependencies/proof and relevant prior findings. No repeated catalogue-wide exploration, unchanged infrastructure review or large copied passages.

Canonical sources at the baseline:

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/workbook_v2/gates_03_04/DOWNSTREAM_SELF_SUFFICIENCY.md | 7660321c04752f00d591266d45a7858f9b81a7ab874072d08ec10400ab4b6d3e |

Relevant preparation: reuse_preparation/FAMILY_F13_EXTENDED_E11_E15.md (D057–60), FAMILY_F14_EXTENDED_E11_E15.md and F14_R284_R285_R286_CONTROLLED_SYNTHETIC_V1.json (D062/63), FAMILY_F15_EXTENDED_E11_E15.md (D066–69), FAMILY_F16_EXTENDED_E11_E15.md (D071–75), FAMILY_F17_EXTENDED_E11_E15.md (D076 only). The preparation root is handoff/foundation_implementation/reuse_preparation/. Its G2_126_D_SIGNAL_SOURCE_LINKED_SPECIFICATIONS.csv and G3 records are per-ID navigation/research, not new proof/admission. Read only the relevant source-research R rows if an identified question remains. Do not rederive accepted research or import M01 private controllers, tests, PostgreSQL fixtures or answers.

Preserve M00 and existing accepted M02/M03 production paths. Provider/TWS/API acquisition, live subscriptions, native source/calendar certification, M01 retirement/migration, other P02/P03 outputs, D077+, broad integration/E2E, performance and application/main integration are out of scope. A new public calculation facet required by a resolved owner is in scope after acceptance; it is distinct from provider/API collection. No token/cache savings are claimed without measurement.

## 3. Fixed identities, owners and dependencies

Dependency order in this table is logical, not an assertion about an existing implementation's internal tuple order; the per-ID owning manifest must freeze the actual ordered extraction/bindings before code.

| ID | Meaning / exact R or D inputs | Owning boundary / present disposition |
| --- | --- | --- |
| D057 | VIX1D/VIX9D term pair; R238,R239 | M02; controlled proposal §4.1 |
| D058 | VIX9D/VIX term pair; R239,R236 | M02; §4.1 |
| D059 | VIX/VIX3M term pair; R236,R240 | M02; §4.1 |
| D060 | VVIX/VIX ratio; R237,R236 | M02; §4.1 |
| D061 | US volatility regime score; D052,D053,D057,D058,D059,D060 | Preserved P02 / existing M03; OWNER-DEFERRED TO-DO §13; exact own score profile still required |
| D062 | Next scheduled event time; R284,D001 | M02 foundation jurisdiction; BLOCKED actual lawful D001 predecessor and event contract |
| D063 | Standardised macro surprise; R286,R285 | M02; controlled proposal §4.2 |
| D064 | Event importance score; R289 | Preserved P03; BLOCKED exact owner/source/P_SCORE |
| D065 | Active event window; R284,D062,D064; P_RULE | Preserved P03; BLOCKED exact owner/rule and branch-specific prerequisites |
| D066 | Nikkei return; R270 | M02; §4.3 |
| D067 | Hong Kong index return; R271 | M02; §4.3 |
| D068 | China index return; R272 | M02; §4.3 |
| D069 | China technology index return; R273 | M02; §4.3 |
| D070 | International overnight risk; D066,D067,D068,D069,D049,D050,D051 | Preserved P02 / existing M03; BLOCKED exact profile and horizon/FX policy |
| D071 | Broad-market return; R037,R042, subject SPY | M02; §4.4 |
| D072 | Technology return; R037,R042, subject QQQ | M02; §4.4 |
| D073 | Semiconductor return; R037,R042, subject SMH | M02; §4.4 |
| D074 | Semiconductor return; R037,R042, subject SOXX | M02; §4.4 |
| D075 | NVDA return; R037,R042, subject NVDA | M02; §4.4 |
| D076 | Technology minus broad return; D072,D071 | M02; §4.5 |

P03 is a proposed responsibility label, not a currently allocated runtime ID. Do not equate it with runtime M03, which already owns P02. New-owner ingress supplies category M plus a responsibility name; the kernel resolves the next unused ID at admission. No numeric reservation in this plan. Normal ingress, registration, public reader/writer edges, owner-local durability and scoped architecture proof must precede P03 runtime use.

Execution sequence, once commissioned: ascending numeric IDs, one accepted/saved unit before the next. At the first still-unresolved entry condition stop and report the exact gap; do not silently skip, defer, renumber or implement a prerequisite outside scope. The original first stop was D061; the owner has now explicitly deferred it under §13. The next unresolved entry is D062. An owner-approved explicit deferral or bounded prerequisite amendment may later change that sequence; neither is assumed now. D065's lawful post-event branch does not by itself require D062, but numeric skipping to reach it still needs an explicit disposition.

## 4. Specified controlled proposals and exact two-case targets

These are proposed synthetic contracts for owner review, never real-feed or real-calendar claims. Every future case starts from actual M00 public observations or actual public predecessor producers. Expected values are independently authored constants or equations; do not feed precomputed D results to the owner.

Common numeric law: finite exact Decimal raw values, explicit scale1/offset0 units unless the owning contract states otherwise; no float, magnitude-based conversion or ambient Decimal rounding. Exact ratios are reduced integer numerator/positive denominator. For log return use mathematical ln, existing bounded rational-log evaluation certifying one 50-significant-digit ROUND_HALF_EVEN value, refusal when its declared existing 32..512-term refinement cannot certify it. Do not change accepted log behaviour. D063 uses an exact rational baseline mean/sample variance and independently bounded square-root division certifying final50digit half-even z; the fixture gives exactly2. D076 subtracts the actual persisted rounded predecessor values exactly, not a fresh ln of a different combined ratio.

### 4.1 D057–D060: volatility term pairs

Decision T=20Oct2026 13:00Z, cutoff T+1s, now T+2s; scalar observations event T/receipt T, zero allowed inter-input event skew, age <=60s. Reuse the accepted synthetic foundation-controlled-macro / macro_snapshot_v1 native metric.value shape, metric series/measurement_date/method/quote_orientation identities, source scope and per-R mappings/units from _macro_changes.py at the baseline. Only new per-D definition/admission/selection content changes. Require actual exact selected latest eligible source occurrences and matching declared series/units; inspect complete bounded histories, no fallback from a selected invalid current value to an older complete value. No revision_vintage_native in this controlled profile.

R238=VIX1D15,R239=VIX9D20,R236=VIX25,R240=VIX3M30,R237=VVIX100; native and canonical units index_points, quote orientation not_applicable. Current metadata follows each record's UTC measurement date and the unchanged accepted per-R method convention.

| ID | New success value / typed shape | Single refusal with otherwise lawful inputs |
| --- | --- | --- |
| D057 | point_difference=-5; ratio=3/4 | Required R239 denominator is present and zero. |
| D058 | point_difference=-5; ratio=4/5 | R239 event T-1s while R236 event T; each is fresh, but the declared zero-skew join fails. |
| D059 | point_difference=-5; ratio=5/6 | Latest eligible R240 at T is zero; an older complete positive R240 exists but may not replace the selected invalid denominator. |
| D060 | ExactRatioV1(4,1), scalar ratio | Required R236 denominator is present and zero. |

Both fields for D057–59 are mandatory ExactRatioV1 in a new frozen TermPairV1(point_difference,ratio); units index_points / ratio, no percent conversion. Do not misuse IndexChangeV1's percent_change name. D060 is ratio, not percent or Decimal truncation.

### 4.2 D063: release-specific historical surprise

Reuse only D063's four release records in the existing F14 synthetic manifest: July/August/September prior pairs (consensus2.5,actual2.4),(2.5,2.5),(2.5,2.6), current October(2.5,2.7); declared same synthetic_pct_yoy units. Baseline N=3, sample denominator N-1, current excluded. Retain manifest release IDs/family, exact scheduled/forecast-known/actual-receipt timestamps and c1/a1 revisions. In this proposed controlled profile actual known_utc is its recorded receipt instant; no separate unknown provider publication time is asserted. As-of current release15Oct2026 12:30Z; cutoff13:00Z; now13:00:01Z. Only forecasts known strictly before their release may be paired; historical actuals/releases strictly precede current and all selected versions must be visible by cutoff.

Synthetic provider foundation-controlled-events, variant release_snapshot_v1; raw paths release.consensus for R285 and release.actual for R286. Each projection retains release.id, release.family, release.scheduled_utc, release.kind(consensus/actual), release.known_utc and release.revision. Native numerical values are Decimal, not the JSON manifest's documentary strings. Forecast observation event time is its known instant; actual observation event time is its release instant. The scheduled release identity is metadata, not a future event-time invention. Distinct M00 occurrences preserve the exact forecast/actual disclosures and raw receipts. Latest eligible version selection occurs within exact release/family/kind; no pairing across releases or backfill of a missing selected member.

Success: surprises[-.1,0,.1], current .2; mean0, sample variance .01, SD .1, z=2, complete typed Decimal/lineage/strict-prior baseline selection. Refusal: selected September historical actual is absent while its consensus and every other current/prior input are present. N=3 required: no shortening to two or substituting another release. This is one missing-pair scenario. Post-release forecast revisions and zero variance are source-reviewed obligations, not additional runtime cases.

### 4.3 D066–D069: controlled international daily logs

These four synthetic series have their own explicit current/prior UTC sample frames, not inferred JP/HK/China exchange calendars. T=20Oct2026 13:00Z, reference=19Oct2026 13:00Z, cutoff T+1s, now T+2s. Both sample instants required exactly, no holiday carry/interpolation/nearest-neighbour or later replacement. Dates/times here are invented controlled labels; native FRED date-only histories cannot be converted to these instants or used as if certified.

Provider foundation-controlled-international, variant daily_close_v1, scope same provider/variant. Native index.value Decimal; identity fields index.series,index.close_utc,index.adjustment_basis=controlled_unadjusted/1,index.close_kind=controlled_official. Mapping mmt-rNNN-international/1; unit mmt-rNNN-index-units/1, index_points->index_points scale1/offset0; R270=NIKKEI225,R271=NASDAQNQHK,R272=NASDAQNQCN,R273=NASDAQNQCN10. Calculation subject is NVDA (international context), series identity selects the exact index; no proxy substitution.

| ID | Reference→current / expected log | Single refusal |
| --- | --- | --- |
| D066 | 100→110 / L | Required prior close native adjustment_basis differs from controlled_unadjusted/1. |
| D067 | 200→180 / M | Current R271 exists but was received after cutoff. |
| D068 | 50→55 / L | Prior value0 exists; ln denominator invalid. |
| D069 | 80→100 / U | Prior sample only at reference+1s; exact required anchor absent. |

L=0.095310179804324860043952123280765092220605365308644.
M=-0.10536051565782630122750098083931279830612037298327.
U=0.22314355131420975576629509030983450337460108554801.
These independently established50digit log witnesses are frozen here for future proof; bind final Decimal tuple literals in owning proof. D068 deliberately uses a nonzero controlled registration witness instead of preparation's equal-price example; no old test is rerun.

### 4.4 D071–D075: same-subject prior official close/current log

T=20Oct2026 12:40Z. The controlled request domain permits cutoff T+1s or T+2s with now>=cutoff; standalone two-case fixtures use cutoff T+1s/now T+2s. This explicit domain permits D076's genuine mismatched-cutoff predecessor setup without changing an accepted definition later. Synthetic current session20Oct12–13Z; prior session19Oct12–13Z; official prior close timestamp19Oct13Z. Current event/receipt exactlyT, prior close event/receipt exactly prior session end; distinct observation IDs. Exact subject is SPY/QQQ/SMH/SOXX/NVDA respectively. Proxy choice SPY and QQQ is explicit, not silent SPX/NDX interchangeability.

Provider foundation-controlled-underlying, variant last_prior_close_v1. R037 at trade.last and R042 at official_close.value, Decimal price. Each binding retains instrument.id, session.id, adjustment.basis=controlled_unadjusted/1 and price.kind=current_last/official_close as applicable. R042 retains the prior session identity, never current session. Mapping mmt-r037-underlying/1 and mmt-r042-underlying/1; unit mmt-underlying-price/1 identity price units. No live IBKR mapping or US market calendar assertion. Current age0/skew0; prior freshness is the exact named previous synthetic session, not a current-price staleness cap.

| ID | Subject / prior→current / expected | Single refusal |
| --- | --- | --- |
| D071 | SPY /100→110 /L | Current SPY exists; the only prior official close is another subject QQQ. |
| D072 | QQQ /100→90 /M | Exact prior close has split_adjusted basis instead of declared unadjusted basis. |
| D073 | SMH /50→55 /L | Current SMH record exists with receipt after cutoff. |
| D074 | SOXX /40→44 /L | Correct-subject prior official close is present with value0. |
| D075 | NVDA /100→125 /U | Correct current last is present with negative price-1. |

Every success asserts actual subject-specific mappings/selected lineage; identical numerical L or reused source patterns do not make distinct registrations interchangeable. D074's nonzero witness avoids weak zero-only acceptance. No zero/negative native-domain enforcement beyond the positive-price requirement needed by ln is inferred.

### 4.5 D076: actual compatible QQQ minus SPY

Use actual accepted public D072 and D071 producers at §4.4's same T/cutoff/session/return convention; no prefilled1/20 and1/50 derived carriers from the documentary example. Request order D072, D071; subject US_TECH_VS_BROAD, members(QQQ,SPY), explicit cross-subject basket. Both definition/parameter/source conventions and exact official prior-close anchors must match their owning profiles.

Success: exact rational Fraction(M)-Fraction(L), where M/L are the persisted50digit representations fixed above; freeze its independent numerator/denominator before proof admission. Units return_spread, shape exact_ratio, actual complete nested predecessor/raw lineage. Refusal: both actual lawful predecessors exist, but D071 has knowledge cutoff T+2s while D072/request cutoffT+1s; new D071 producer request is lawful under its source contract and nowT+3s. No mixed knowledge snapshots. D071's two-value cutoff domain is explicitly proposed in §4.4 before its implementation; no accepted prerequisite needs amendment for this case.

## 5. Five precise authority-resolution units

These were originally named stops. D061 is now an explicit owner-approved deferral under §13; D062/D064/D065/D070 remain unresolved stops, with no implicit permission to add tests/IDs. Preserve their original identities, jurisdictions and dependencies.

### 5.1 D061 / P02 existing M03

Freeze one own K07 profile over the six actual inputs; name exact D052/D053 structured component paths (point_change versus percent_change), D057/58/59 point_difference versus ratio, and D060 scalar extraction. Declare transform/scale, optional clip or explicit absence, orientation, nonnegative weights, intercept, raw versus bounded output and numerical carrier. Catalogue generic score does not imply sigmoid. All direct as-of/cutoff snapshots must be compatible, and shared underlying current raw identities across direct parents must agree. D052/D053 and other old profiles stay unchanged; materialise them as setup via public factories, never their tests.

Missing policy is not supplied by existing D040/D041 coefficients. Obtain owner acceptance or explicit delegation for a concrete new profile, then bind its own immutable brief/JSON/proof contracts. Define its own public factory/result/readback extension within M03; no generic cross-peer score service. Only then freeze its two exact cases/oracle and admit execution.

### 5.2 D062 / actual D001 and event source law

Accepted law selects earliest relevant scheduled event strictly after as-of; retain seconds and exact minutes. F14 positive schedule is as-of21Oct12:00Z with known future events12:01:30 and12:03, plus past/exactly-now/late-received decoys; expected90seconds/3/2minutes. These are a candidate witness, not actual D001 evidence.

Baseline M02 source/API inspection found no D001 implementation; M01 remains bootstrap legacy and no M01 import/migration is authorised. An as-of datetime or fabricated D001 occurrence cannot replace the declared D001 dependency. Stop until an actual lawful public D001 contract/producer is supplied, or the owner separately authorises its bounded prerequisite implementation/acceptance. D001 would be an explicit additional unit with its own budget/checkpoint, not silently the twenty-first signal in this plan.

Also settle exact controlled R284 projection of scheduled UTC, event/relevance identity, schedule revision selection and disclosure/receipt versus scheduled time. M00 supports native string projections, while existing M02 RawInputLineageV1/codec is numeric-oriented; a temporal lineage/carrier/codec design must preserve exact ISO native bytes and parsed same UTC instant without modifying M00 or coercing schedule time into Decimal. No executed RED or numeric fixture can discharge this source/type/owner hold. Once resolved, declare exactly one success and one reached refusal.

### 5.3 D064 / P03 event importance

Before code, admit P03's bounded event-risk responsibility under a nonnumeric create intent, exact package/public seam, permitted M00/foundation reads, own SQLite writer/read-only boundary and immutable lineage. Do not allocate it to M03/P02 or M02 by convenience. Proposed package nvda_desk.event_risk_policy, public seam .api; numeric owner remains unresolved until normal kernel allocation.

R289 needs a concrete controlled/native value shape, event identity/revision/time/unit mapping and versioned interpretation. Existing numeric R289 fixtures do not prove a native category translation or historical sensitivity model. K07 does not implicitly map categories to numbers. Resolve explicit legal scalar extraction/parameter semantics, bounded importance interpretation and exact numerical profile; do not invent an unlisted categorical extractor or disguise a precomputed D064 answer as raw/context. Bind own authority, exact typed seam and two cases only after owner acceptance/delegation.

### 5.4 D065 / P03 event-centred policy

Reuse that admitted same P03 owner and actual own D064, with exact selected event ID/definition/profile joined to visible R284. Own immutable P_RULE sets pre/post durations, applicability threshold/inclusion and known-calendar coverage/absence semantics. Canonical kernel selects visible events in [as_of-post,as_of+pre], nearest absolute distance, exact tie earlier; output true only if selected event's D064 meets threshold. Preserve boolean and any additionally mandated score as a named typed carrier, not an arbitrary bool/score collapse.

D062 is a pre-event countdown and is not the sole post-event source. A strictly post-event branch may lawfully omit it under the accepted row; do not fabricate a future countdown or make it unconditionally mandatory. Full acceptance claims must distinguish implemented branch coverage, mandatory unproved branches and source review from runtime proof. Resolve exact supported profile/branch and complete contract before freezing two discriminatory cases; do not add pre/post/tie scenario loops. Missing required proposition is a reported scope gap, not silent weakening.

### 5.5 D070 / P02 existing M03

Freeze its own seven-input K07 schema, exact component paths, transform/scales, orientations, weights/intercept/output and numerical law. Equity ln returns differ from FX percent changes and quote orientations: no implicit scalarisation/unit mixing. Preserve all four index identities and JPY/HKD/onshore-CNY per-USD orientation.

Important predecessor compatibility: accepted D049/D050 profiles are1d while D051 is5d. Do not rerun/change D051 to fit a convenient daily assumption. The new immutable profile must explicitly accept those distinct named horizons and state their interpretation, or owner must commission a separate compatible prerequisite/profile amendment. Fix one exact calendar/as-of/knowledge universe and any required dispersion/FX-confirmation interpretation; a linear directional proxy must not be silently called proof of dispersion/predictive risk. Actual accepted D066–69 plus lawful D049–51 supply setup, not precomputed feature scores or tests. Resolve own brief/profile/factory and two exact cases/oracle after owner decision.

## 6. Minimal implementation and immutable declaration map

After a signal's authority/profile is accepted, freeze its exact per-ID file/type/case manifest before implementation. Do not create scaffolding for unresolved future units.

For specified M02 units, proposed private files: _volatility_terms.py (D057–60), _macro_surprise.py (D063), _international_returns.py (D066–69), _underlying_returns.py (D071–75), _relative_market_return.py (D076). Use existing api.py WindowCalculationRequestV1 / WindowMeasurementOccurrenceV1 / MeasurementWindowOwnerV1 / MeasurementWindowReadsV1 and create_window_owner/create_window_reader; add only per-ID routing in _window.py as each is admitted. Add only TermPairV1 and its explicit WindowMeasurementOccurrenceV1.result union member for D057–59. Existing scalar Decimal/ExactRatioV1 results cover the other specified units. Preserve old namespaces/validators/factories. Reuse accepted owner-local RecordState, typed codec and arithmetic helpers where exact contracts agree; any incompatible new temporal/profile carrier remains an entry hold, not an excuse for a broad framework.

Per-ID M02 authority: handoff/foundation_implementation/authority/Dnnn_IMPLEMENTATION_BRIEF.md, Dnnn_PROOF_CONTRACT.json; implementation/authority/Dnnn_IMPLEMENTATION_AUTHORITY_BINDING.yaml; config/product_proof/market_measurement_dnnn/{claim.json,admission.json,generations/0001.json}; tests/product/market_measurement_dnnn/test_signal.py, sole test_dnnn_signal with success/refusal IDs; owning dnnn_execution evidence directory. P02 follows existing handoff/configured_market_conditions and configured_conditions_dnnn pattern. P03 paths/public types are frozen at §5.3 admission, with a non-overlapping physical/config claim root.

One bounded fixed loader declaration extension in tools/product_proof_claims.py for the finite D057–D076 IDs/owners may be prepared during the first commissioned resolved unit, preserving every old claim, immutable generation/target/partition/validator algorithm. Add exact per-ID descriptors only as each authority is resolved. New peer target/seam must be represented honestly; never route it through an M02-only helper. No dynamic discovery, arbitrary claim registration, generic score service or shared runner relaxation. No loader or infrastructure change is authorised merely by this planning task.

Repeated identities, feature parameters, hashes, authority references and numerical constants derive from the canonical owning brief/JSON and committed proof bytes. Reuse exact accepted authority/implementation/proof infrastructure, inspect consistency once before sealing each immutable generation; retain originals and link replacements. No independent reconstruction of the same constants across companion reports, duplicated reasoning or unnecessary receipt framework. Keep required contracts, evidence, provenance and independent semantic judgement.

## 7. Execution cycle and efficiency rules

For each resolved commissioned signal, in numeric order:

1. Confirm its entry authority, exact owning delta, actual dependencies, two node IDs, numerical oracle and named refusal; consult relevant accepted evidence without executing it. Write/inspect the new proof before production code.
2. Author exactly two physical cases. Success proves the full typed value/units/definition/parameters/context/owner/admission/times, actual selected lineage and ordinary public read-only durable reopen within that same case. Refusal must begin with otherwise lawful actual source/predecessor facts, reach its single stated defect and persist no result/history. Actual public predecessor materialisation is lawful setup; old acceptance test invocation is not.
3. Implement only the owning delta. Initially run one warranted scoped mypy for new/changed production Python and one scoped Ruff for new/changed Python. Record exact file list, commands, output, relevant affected proposition. Reuse unchanged successful evidence; no package/repository sweep or checks for prose/hash-only changes. Perform only required scoped new-owner/new-file ingress/registry/import/public-seam checks; report inability to isolate required scope instead of silently broadening.
4. Commit a clean candidate. One independent final semantic reviewer is sole acceptance runtime executor, including authorised repair recovery. It assesses math/meaning, source and fixture sufficiency, exact version/selection joins, assertions' discriminatory power and relevant prior repair lineage; never rubber-stamp GREEN. Fixture-independent public action sequences belong inside the declared pair, not extra probes.
5. Sole strict invocation: `PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate <exact owning admitted claim>`. M02 claim neutral_market_measurement_truth_dnnn; P02 configured_market_conditions_dnnn; P03 exact claim freezes at admission. Expected exactly two observed passes, exit0, no skip/xfail/xpass/empty collection or governed mutation. Do not run focused cases successfully first and then strict aggregate.
6. Accept only on sufficient independent semantic judgement and strict GREEN. Preserve candidate/tree/brief/binding/contract/generation/source/proof hashes, complete original runtime output and concise final review/reuse/limitations. No routine runtime RED: its omission deliberately reduces test-first evidence; source review is not equivalent executed RED.
7. Commit the accepted state. Immediately create a cumulative full-history Git bundle, verify its complete history/accepted HEAD, save it and expose one downloadable checkpoint link before advancing. No end-of-batch delay, duplicate product run for bundling or final whole-branch sweep.

Do not run bare pytest, broad Makefile checks, architecture/bootstrap/promotion/control suites, old M00/M01/M02/M03 tests, benchmarks, live/provider/API probes, speculative scenarios, mutation matrices, copied/renamed old tests to evade the no-repeat rule, or extra implementer/reviewer GREEN. New code exercised via a new signal's genuine case is not repetition of its historical suite. The limit controls waste, not correctness or assertion strength. Six is the hard per-ID ceiling, never an automatic expansion from two; a missing mandatory proposition remains a scope gap requiring a concrete owner decision.

## 8. Narrow repair recovery

Prohibit rerunning previously accepted, unaffected tests. Preserve a failed check's complete original output, defect, affected proposition and relevant material repair; stop dependent work. The independent reviewer may rerun only the failed check after that repair. Successful checks may re-execute only if subsequent changes materially invalidate their evidence; identify changed bytes/proposition and why, retain both results. Sessions/reviewers/commits/documentation/bundles alone do not invalidate evidence. No retry without repair, speculative extra case or automatic broad regression.

Carry forward the owner's23October2026 16:14 exception: when the CURRENT new signal's initial strict two-case aggregate fails, the same independent reviewer may rerun that SAME aggregate (both cases) after documented relevant material repair. Preserve original outcome/defect/rationale/subsequent result. This is pre-authorised once this plan is accepted/commissioned, with no further owner approval. Previously accepted signals remain excluded except for the separate precisely documented materially-invalidated-evidence rule; no general regression permission is created. Do not modify the shared runner or acceptance infrastructure to implement recovery.

Static repair may be performed by the implementer; independent acceptance review examines the record and does not repeat unchanged successful statics. A new owner or carrier is not permission to requalify historical products; any actual invalidation of an accepted proposition must be explicitly identified and resolved narrowly before claiming it remains supported.

## 9. Runtime and context reuse

Keep CPython3.12.14, SQLite3.53.1, pytest9.0.3, mypy1.20.1, Ruff0.15.11, PyYAML6.0.3 and committed hashed offline locks/wheels. Do not switch to the attached Python3.13 wheelhouse. Supply an environment-specific absolute NVDA_PROOF_PYTHON; verify its current identity/pins before first use, or reuse unchanged actual verification and the original environment log by exact Git reference. Never bake a temporary interpreter path into this plan or silently use system Python.

A new branch/session/reviewer does not trigger dependency installation, environment requalification or repeated product tests. If the verified runtime is genuinely absent/changed, restore only the missing pinned environment and verify only changed facts, no product qualification probe. Planning requires no installation or runtime/static checks. Reuse relevant family/context/authority findings while bytes/applicability remain unchanged; keep independent judgement substantive. No model token/cache/performance saving claim without measurement.

## 10. This planning task: review, reconciliation and delivery

Allowed mutations now: EXEC_PLAN.md, AGENTS.md, tests/AGENTS.override.md, README.md and one concise review record under handoff/planning/d057_d076/. No product source/tests, dependency pins, authority bindings/proof contracts, claim descriptors/admissions/generations, architecture registry/allocation or GUARDRAILS.md changes.

Reconcile current root/test-local instructions to this proposed scope; retain exactly two cases, one independent executor, narrow recovery, no routine RED or historical regressions and all ownership/provenance law. Earlier D026–D036 six-case/TDD and completed-tranche instructions remain historical; do not silently reinstate them. Generic skill defaults for separate plan paths, executed RED, added tests, blanket suite/branch review or recurring new contexts do not override the owner methodology. Root EXEC_PLAN.md is the single plan once accepted.

- [x] Draft/self-review all twenty IDs against exact catalogue/authority and current public source; preserve five explicit entry holds.
- [x] One independent planning reviewer assesses scope, dependencies/owners, source/numeric proposals, two-case adequacy/limits, sequencing, no-repeat/recovery/environment and governing-law conflicts. Documentary inspection only; no product/static tests or implementation.
- [x] Independent round1 identified no material planning defects requiring repair; preserve its complete record. If later material defects arise, retain findings and concise exact resolutions. Aim for at most two review rounds, but do not conceal unresolved material defects to hit that target. Second round checks the fixes/relevant consequences, not an automatic fresh whole-repository investigation.
- [x] Commit planning/governance changes on this branch; provide exact commit and a verified downloadable full-history checkpoint containing the reviewed plan and record.
- [x] Owner review/acceptance and separate execution authorisation received in the current thread on 24 October 2026; execute under §§3–9.

## 11. Present ledger

Baseline accepted checkpoint d0a9052 remains preserved; no claim is made that main contains it. New planning branch was created from that clean exact HEAD. Fifteen controlled proposals are specified; five entry conditions remain explicit. No new product case exists or ran, no static/product/environment check ran, no new proof/owner was admitted. Read-only Git/source inspection and documentary preparation are not product qualification.

Independent review: READY FOR OWNER REVIEW AS A CONDITIONAL PLAN after one round, reviewed semantic candidate6e2d6a7b5fb3979239f886e6f7301fb5de4317f8. Full independent record: handoff/planning/d057_d076/review_round1.md. No material repair/re-review requested; only this disposition/checklist is updated after review, without changing the reviewed source/numeric/case/owner/efficiency proposals. Owner acceptance: PENDING. Execution commission for D057–D076: NOT GIVEN by this planning-only instruction. No conflict with frozen GUARDRAILS.md is knowingly overridden; any reviewer-identified material conflict must be recorded and resolved before handoff.

Close-out: read-only independent standard-library Decimal/Fraction documentary arithmetic also confirmed §4's L/M/U50digit literals and the D076 subtraction equation without importing/executing product code. This is numerical proposal preparation, not product proof, a static checker or environment qualification. Final planning commit and verified full-history bundle accompany the deliverable; implementation and all five authority-resolution decisions remain uncommissioned.

## 12. Current execution ledger

Owner accepted the exact supplied plan at 2f2cd9841504702c869412aadc83afb1f96b8d09 and authorised execution. This supersedes pending/planning-only status statements in §§1/10/11, README and agent instructions solely as to commission status. All source/numeric/case/owner/efficiency rules and five holds remain unchanged.

- D057: ACCEPTED controlled profile after independent final semantic review at d14431deb9ef53cd1994bbc3470a0f64f7bad216; strict aggregate exit0, exactly2 passed. Original precollection exit2/capture repair preserved; no product/runner repair. Evidence handoff/foundation_implementation/d057_execution/final_review.md and final_green.log. Cumulative full-history checkpoint must be verified/saved/exposed before D058.
- D058: ACCEPTED controlled profile at c9d0c61; one strict aggregate exit0, exactly2 passed (0.19s), independent review/output in d058_execution. Cumulative checkpoint required before D059.
- D059: ACCEPTED controlled profile at f27e44e; one strict aggregate exit0, exactly2 passed (0.18s), independent review/output in d059_execution. Generation0002 repairs pre-runtime no-fallback witness discrimination; original generation/test preserved. Cumulative checkpoint required before D060.
- D060: ACCEPTED controlled scalar profile at f99471d; one strict aggregate exit0, exactly2 passed (0.17s), independent review/output in d060_execution. Cumulative checkpoint to be verified/saved/exposed at close-out.
- D061: OWNER-DEFERRED TO-DO under §13; retain P02 / existing M03 ownership and the complete §5.1 requirements. No own score profile was supplied/accepted or choices delegated by the general execution authorisation. Need exact D052/D053 component paths, D057–59 pair extraction, D060 scalar, transform/scales/clip-or-absence/orientations, nonnegative weights/intercept, raw-or-bounded output/numerical carrier, compatible snapshot/shared-raw law and own immutable profile/factory/proof contract before execution. D061 is explicitly deferred; this does not automatically defer any other unresolved unit.

Execution uses the isolated supplied-bundle clone on its work branch. No baseline suite, routine runtime RED or whole-branch review is authorised; the accepted plan overrides generic skill defaults. One independent final reviewer/sole runtime executor per signal, two declared cases. Library skill used to save cumulative deliverables.

D057 checkpoint delivery: accepted412e91d78c76b03fc30095e0a87231379d65f705, cumulative bundle SHA256 bf272afef355d48b55a5ca541ae48556e81faefe1df7aa410f457c090ad8d4c4;948 all-ref reachable commits match restored mirror, full history/no prerequisites, restored fsck0, saved/exposed before D058.

D058 checkpoint delivery: accepted1d8e3a0cdb8d5de2116a741572b2a94c5711fc87, cumulative bundle SHA2563e2868e3036c4866976e01263133ab0e5ff5a7fd6e81cbeef321817b61bedca9;950 all-ref reachable commits match restored mirror, complete history/no prerequisites, restored fsck0, saved/exposed before D059.

D059 checkpoint delivery: accepted247ae27a4e2ad7881a2d7ef6456f751f5a083401, cumulative bundle SHA256855f5a6c08ce2a8d23781d11e35b2a95f0b74081ea89297628cf0d1c2640ff13;953 all-ref reachable commits match restored mirror, complete history/no prerequisites, restored fsck0, saved/exposed before D060.

### Execution close-out at the D061 authority hold

D057/D058/D059/D060 independently accepted with exactly two observed passes each (eight distinct cases total). No routine RED, old product test, speculative case or broad regression was run. D057’s initial invocation stopped before collection because in-repository output capture violated the clean-tree guard; original exit2 and capture-only repair are preserved. D059’s first documentary proof generation was strengthened before any runtime to discriminate fallback independently of skew; generation0001/original test remain recoverable and generation0002 is linked. Scoped checks/relevant material repair and all complete original runtime outputs remain in owning evidence directories. No executed RED is claimed.

Runtime stays CPython3.12.14/SQLite3.53.1/pytest9.0.3/mypy1.20.1/Ruff0.15.11/PyYAML6.0.3. Earlier session’s environment directory was absent; current exact interpreter was checked, only missing pinned dependencies restored from committed offline hashed wheels. Actual environment evidence was then reused for later units; the attached3.13 wheelhouse was not used.

Read full current guardrails/root/test instructions and initial plan; applicable K02/common calculation/lineage/projection law, exact D057–60 rows/F13 and relevant foundation/architecture authority/source were inspected. Applicable unchanged evidence was reused by identity; this is not a new audit of all126/209 rows, native source collection, predictive validation or integration/E2E. Full per-signal independent review scope/hashes/limits are in each final_review.md. Frozen guardrails and prior accepted product/source/proof bytes remain preserved. Only new registrations, required TermPairV1 public result and routing, finite claim declarations, owning proof/authority/evidence and current commission/ledger changed.

Next action requires D061’s explicit own-profile resolution or an explicit owner sequencing disposition. The other four holds D062/D064/D065/D070 remain as §5 specifies. No unresolved unit was skipped or implemented.

## 13. Owner sequencing amendment — D061 to-do; D062 next entry hold

The owner instructed: “why don't you mark that as a to-do and continue with the rest of the signals.” The referent is D061. This explicitly authorises parking D061 and continuing ascending numeric entry assessment; it does not supply D061 parameters, allocate a new owner or automatically defer another named hold.

- [ ] **D061 — OWNER-DEFERRED TO-DO:** composite US volatility regime score; responsibility P02, existing M03 configured_market_conditions. Preserve all §5.1 input/profile/meaning/proof requirements. It remains unimplemented/unaccepted. Resume only after its exact own profile is accepted or the owner explicitly delegates those choices.
- **D062 — BLOCKED at next entry:** §5.2 independently requires a lawful public D001 producer and settled R284 temporal projection/lineage contract. The D061 sequencing exception does not supply or waive either. No D062 proof/production/runtime was authored or executed. No D063+ unit was silently skipped to.

Ownership explanation: foundation §1 assigns strategy-independent neutral measurements to M02; AnnexC assigns D061 to P02, and current modules.yaml identifies that responsibility as existing M03. The criterion is semantic responsibility/policy meaning, not number of inputs or arithmetic complexity. D061 is still a deterministic calculation; its exact configured regime-score interpretation/profile belongs to P02/M03. No ownership change was discovered or made in this amendment.

Read-only D062 entry check at prior checkpoint14dbf87bb47e61ab8e438fb1dfc90fb355f2a34e inspected root §5.2, F14 source contract, M02 public API/raw lineage, numeric codec and current M02 source/proof/config registrations. Literal D001/D062 search in those M02 surfaces returned no matches; RawInputLineageV1.canonical_value remains Decimal, not a temporal native carrier. This corroborates the specified entry gap; it is not a claim that no historical/legacy implementation exists elsewhere. Legacy M01 import/migration and a new prerequisite D001 unit remain outside this commission.

D060 cumulative checkpoint was verified/restored/saved/exposed at14dbf87bb47e61ab8e438fb1dfc90fb355f2a34e, SHA25635f2584168b73a888d10735bfd5e950c8fc71e086abc877074e30d4c3b3ea8e9,955 all-ref reachable commits, restored fsck0. This documentary amendment changes no source/tests/contracts/immutable proof or accepted runtime evidence. No product/static/environment checks rerun. Earlier stop statements in §12 describe the prior close-out and are superseded solely for D061 sequencing by this section.

## 14. Owner authorises remaining held-unit deferrals and resolved execution

In response to the explicit proposal to park D062/D064/D065/D070 and execute the remaining resolved signals, the owner instructed: “Yes, I do. Proceed.” D061 remains deferred. This is sequencing authority, not acceptance/completion of a held signal or permission to invent its missing requirements.

Deferred to-do set: D061 (§5.1, P02/M03 own score profile), D062 (§5.2, lawful D001 and temporal event contract), D064 (§5.3, P03/source/profile admission), D065 (§5.4, P03/event-window rule/prerequisites), D070 (§5.5, own score/horizon/FX profile). Preserve their exact identities, owners, unresolved requirements and original evidence. They are not implemented or accepted by deferral.

Authorised remaining order: **D063, D066, D067, D068, D069, D071, D072, D073, D074, D075, D076**, one signal/independent final executor/verified saved exposed cumulative checkpoint at a time. No new D001 unit, P03 admission or held policy is commissioned. Any newly demonstrated unmet mandatory invariant still stops affected work under guardrails. All §§4/6–9 source/numeric/proof/no-repeat/recovery/environment disciplines remain.

- D063: acceptance/evidence recorded below.
- Initial remaining set at commission: D066–D069, D071–D076. Current per-ID acceptance entries below govern progress.

This section supersedes earlier stop/automatic-deferral prohibition statements solely for the five explicitly deferred IDs; no other sequencing or acceptance law changes. Prior checkpoint bb4446b1e089fc4814210bda160122db11f87b1b preserves the previous D062 entry hold.

- **D063: ACCEPTED controlled profile**, independently reviewed/strict execution at `31182f9464bb08dcca231a641615410392e10663`; exactly2 collected/2 passed, process and observed aggregate exit0. Full review and original output: handoff/foundation_implementation/d063_execution/. Scoped static/ingress evidence reused as recorded. Cumulative checkpoint must be verified/saved/exposed before next authorised signal.

- **D066: ACCEPTED controlled profile**, independently reviewed/strict execution at `e5d18b2414b071b36496c0bf815e3f95453ae2d6`; exactly2 collected/2 passed, process and observed aggregate exit0. Full review and original output: handoff/foundation_implementation/d066_execution/. Scoped static/ingress evidence reused as recorded. Cumulative checkpoint must be verified/saved/exposed before next authorised signal.

- **D067: ACCEPTED controlled profile**, independently reviewed/strict execution at `bf3b10ecc3bd6d09adabde2a4b21ef1cd03a9a90`; exactly2 collected/2 passed, process and observed aggregate exit0. Full review and original output: handoff/foundation_implementation/d067_execution/. Scoped static/ingress evidence reused as recorded. Cumulative checkpoint must be verified/saved/exposed before next authorised signal.

- **D068: ACCEPTED controlled profile**, independently reviewed/strict execution at `fd686f2106c896f73437c2e8e9a6a9f0eb452666`; exactly2 collected/2 passed, process and observed aggregate exit0. Full review and original output: handoff/foundation_implementation/d068_execution/. Scoped static/ingress evidence reused as recorded. Cumulative checkpoint must be verified/saved/exposed before next authorised signal.

- **D069: ACCEPTED controlled profile**, independently reviewed/strict execution at `f2852c577475bc945c08120ee42459efaf648217`; exactly2 collected/2 passed, process and observed aggregate exit0. Full review and original output: handoff/foundation_implementation/d069_execution/. Scoped static/ingress evidence reused as recorded. Cumulative checkpoint must be verified/saved/exposed before next authorised signal.

- **D071: ACCEPTED controlled profile**, independently reviewed/strict execution at `3b6d991b7f9d0f1a5c7b7190dc1b7fe13ee7a65c`; exactly2 collected/2 passed, process and observed aggregate exit0. Full review and original output: handoff/foundation_implementation/d071_execution/. Scoped static/ingress evidence reused as recorded. Cumulative checkpoint must be verified/saved/exposed before next authorised signal.

- **D072: ACCEPTED controlled profile**, independently reviewed/strict execution at `2f001691fb5638c8a5b28a35ee68d6198ff7f2f1`; exactly2 collected/2 passed, process and observed aggregate exit0. Full review and original output: handoff/foundation_implementation/d072_execution/. Scoped successful static/ingress evidence reused. Cumulative checkpoint verified/saved/exposed before next authorised signal.

- **D073: ACCEPTED controlled profile**, independently reviewed/strict execution at `98c2f8cd5386820538ba26aa255bc33ec5661cb6`; exactly2 collected/2 passed, process and observed aggregate exit0. Full review and original output: handoff/foundation_implementation/d073_execution/. Scoped successful static/ingress evidence reused. Cumulative checkpoint verified/saved/exposed before next authorised signal.

- **D074: ACCEPTED controlled profile**, independently reviewed/strict execution at `f13f1ae980aa4b30f5b559cd19954d2405cb7260`; exactly2 collected/2 passed, process and observed aggregate exit0. Full review and original output: handoff/foundation_implementation/d074_execution/. Scoped successful static/ingress evidence reused. Cumulative checkpoint verified/saved/exposed before next authorised signal.
