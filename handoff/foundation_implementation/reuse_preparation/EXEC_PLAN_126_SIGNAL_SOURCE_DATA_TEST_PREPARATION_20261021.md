# NVDA V2 — 126-Signal Source-Data and Test-Preparation ExecPlan

**Date:** 21 October 2026
**Status:** OWNER-APPROVED TASK-LOCAL RESEARCH EXECPLAN — GATES NOT YET EXECUTED; NOT THE ACTIVE ROOT PROGRAMME PLAN
**Jurisdiction:** Task-local research and documentary preparation. The accepted root `EXEC_PLAN.md` remains the sole active programme plan. This plan does not amend it or grant M02 implementation, source admission, proof admission or pilot authority.

## 0. Commission, authority and scope

### 0.1 Objective

Complete the practical input/source-contract and test-vector research left open by the M01→M02 reuse preparation. The deliverable is an evidence-linked, implementation-facing specification for **each of the 126 foundation D-signals**, sufficiently concrete that the implementation worker can use the prepared source facts, typed examples, independent expected outcomes, fixture conditions and existing M01 knowledge rather than repeat routine research or invent numeric formats, ranges, clocks or identities.

**Research once per shared raw source; apply the result to every dependent D-signal.** Do not perform 126 independent provider investigations. Distinguish externally verifiable facts, accepted project requirements, proposed operational policies and matters requiring actual owner/source authority. Solve answerable questions here; do not merely transfer them to the implementation worker.

### 0.2 Pinned inputs and limits

- Frozen governance: `GUARDRAILS.md` and applicable `AGENTS.md`/overrides; neither may be changed.
- Existing root `EXEC_PLAN.md`: read as authority, **do not replace**. Resolve the then-current live state before later activation or transfer.
- Recoverable review baseline: `19c14ee461140649110d5d1cc4c1d5d7f40123be` (historical D014 partial state, not automatically the current worker HEAD).
- Preparation bundle: `NVDA_V2_M01_M02_REUSE_ALL_126_ASSESSED_20261020.bundle`; branch `work/v2-g6-m01-m02-reuse-prep-20261020`; HEAD `3951b89790a4ae9fc8947de3e20a75c71acfbf78`.
- Primary starting records: `handoff/foundation_implementation/reuse_preparation/{M01_M02_REUSE_CROSSWALK.csv,E0_2_FAMILY_COVERAGE.csv,FAMILY_*.md,OPEN_GAPS.md,HANDOFF.md}` and governing Annex B, accepted corrections, M00 API/SQLite contracts, M01 code/tests, and applicable M02 contracts.
- At this snapshot: **126 unique foundation D IDs**, **35 preparation families**, **82 distinct referenced raw R IDs** in crosswalk `raw_R_refs`, and **83 separate downstream IDs**. Recompute and reconcile against effective authority at execution; none of these counts admits source mappings or M02 outputs.
- The user intends to stop the concurrent pilot. **Verify that it has actually stopped before any shared-branch work.** This draft neither stops it nor modifies its environment.

### 0.3 Authority and modification boundary

Research and prepare specifications only. Use an **isolated research branch descended from the verified preparation HEAD**, preserving the original branch and complete ancestry. Restrict future documentary changes to `handoff/foundation_implementation/reuse_preparation/`, subject to confirmation of the active root plan. Owner approval of this task-local plan was given on 21 October 2026. Do not modify root governance, current programme plan, M00/M01/M02 runtime, tests, provider integration, SQLite schemas, accepted briefs, immutable proof, bindings, or main. Do not migrate/retire M01 or alter the separate 83 downstream signals.

Permitted research: read-only repository inspection; official public source specifications, API documentation, release notes, calendars and series metadata; precise public observations where lawfully available; and independent offline arithmetic/fixture calculations. Authenticated APIs, subscriptions, IBKR sessions, live acquisition or database operations require their own existing access/authority; this plan supplies none. Do not represent documentary research as operational source certification or executable acceptance.

## 1. Required attributes — every D-signal

Each D row must contain or **link exactly** to all applicable fields below. Store shared provider/raw details once in a keyed source record and refer to them by R ID and source-contract ID. `NOT_APPLICABLE` requires a reason; `UNKNOWN` requires the missing fact, checked sources and next decision/receiver. No unexplained blank or generic “check provider” hold.

### 1.1 Identity, authority and reusable work

1. **Identity:** canonical D ID/name, accepted family/kernel, current foundation classification, preparation family and governing calculation/configuration version.
2. **Authority:** exact accepted equation/semantic rule, effective amendments, repository path/section and pinned commit; distinguish authoritative rule from historical workbook description.
3. **Input graph:** ordered raw R IDs, derived D predecessors, selection dependencies, mandatory/optional inputs, and absence versus missing-value behaviour.
4. **M01 reuse:** specific code symbol/branch, actual tests, fixture locations, reusable algorithms and known defects; classify `REUSE_AS_SPEC`, `REEXPRESS`, `NOT_REUSABLE` or `UNKNOWN`. Do not import private M01 or PostgreSQL assumptions as M02 proof.
5. **Target seam:** applicable M00 projection, M02 public/result representation and SQLite contract; exact unsupported or new interface obligation.

### 1.2 Native inputs — linked for **every required raw R**

6. **Source identification:** actual provider/publisher, native product or series, exchange/venue where relevant, contract/instrument/right/expiry and exact source field/path/message/tick identifier. Distinguish official source from broker-distributed or derived field.
7. **Availability:** live/historical/delayed/snapshot status, frequency/cadence, entitlements/licensing, applicable subscriptions, source completeness and known API limits; record `UNVERIFIED` where access has not been tested.
8. **Native representation:** native datatype and payload example, price/currency/quantity/percentage/basis-point units, scale, native display versus canonical fraction, adjustment/multiplier conventions, tick/step/granularity and documented significant digits. Specify lossless Decimal/integer conversion where supported; no invented precision or arbitrary trillion-scale design target.
9. **Value envelope:** documented admissible domain, sign/zero rules and source-defined bounds **separately** from a labelled representative operating range and extreme/stress-test values. Record sample date/period and source. If no authoritative numeric maximum exists, say so; do not turn observed ranges into rejection thresholds. Specify invalid/out-of-domain examples only when an actual contract justifies refusal.
10. **Missing and exceptional values:** absent field, provider sentinel/placeholder, null/N/A, non-finite, stale, halted, delayed, erroneous or contradictory values; whether absence, refusal, defer or explicit status is required by accepted authority.
11. **Time semantics:** event instant versus date-only versus receipt-only; actual publisher timezone/offset, source date/time field, UTC representation where a true instant exists, precision, receipt/ingestion clock, clock skew, publication lag and applicable session/holiday/DST calendar/version. **Never fabricate midnight UTC from a date-only field.**
12. **History and revisions:** official publication/observation date, effective versus receipt/as-of time, preliminary/final/revised values, vintage/as-of semantics, correction/cancellation, delayed arrival, and how a particular version is selected or held unresolved.
13. **Identity and order:** provider observation/trade/bar/book-event key, subject/contract identity, source sequence, page/cursor semantics, duplicates, out-of-order messages, gaps, resets, reconnect/replay and deduplication; existing M00 opaque IDs and immutable lineage requirements. Do not require UUIDs unless an accepted contract does.
14. **Provenance:** raw source reference/version, native field, normalisation rule/version, collection variant, source event/receipt identifiers and information required to reconstruct the selected input. Explicitly state whether an existing M00 projection implements the mapping or whether it is a proposal/hold.
15. **Cross-source compatibility:** sampling/alignment tolerance, same-day versus same-instant versus same-session rule, official closes versus intraday values, revision coherence, source selection precedence and mismatched-source refusal. No implicit forward fill or interpolation.

### 1.3 Calculation and output contract

16. **Exact function:** complete equation/algorithm and parameter semantics, operand order, constants, units, sign, conditionals, aggregation, weighting, and fixed versus externally governed parameters.
17. **Selection state:** eligible record rules, latest/earliest/window/session membership, lookback cardinality, warm-up, as-of and receipt cut-offs, missing predecessor behaviour, and contract/calendar matching.
18. **Output:** scalar/Decimal/exact rational/datetime/structured/basket/surface/book representation, unit, quantisation or preservation law, output identity/version, lineage and refused/undefined states. No guessed rounding policy.
19. **Domain-specific authority:** for options, Greeks, IV and volatility, specify contract matching, expiry, underlying/multiplier, exercise/settlement and model/profile holds; for market depth specify level/venue, snapshot completeness, operations, resets and sequence; for time-series specify calendar/windows; for regressions/densities specify exact model and fit authority or a blocking hold.
20. **Numerical witnesses:** independently calculated valid positive/negative/zero examples where meaningful, scale/precision boundaries, realistic provider-shaped example and one discriminating case for each materially distinct branch. Cite inputs and show expected outputs in canonical units. Where no authorised oracle exists, identify exactly which model/policy prevents one.
21. **Refusal witnesses:** missing, mismatched, stale, wrong subject/contract/source, erroneous unit/scale, invalid version, incomplete history, conflicting duplicates, wrong order, unsupported field and corrupted identity as applicable, each with expected non-write/non-change behaviour.

### 1.4 Fixture, proof and engineering handoff

22. **Fixture preconditions:** exact raw/native and canonical records, timestamp kinds, identities/versions, required history length, ordering, pages/cursors, selected as-of and receipt cutoff; sufficient data to reach the intended fault. A helper may provision inputs but must not calculate the expected oracle or pre-execute the operation under test.
23. **Execution sequence:** initial state; admission/projection steps; first calculation; retry/version change/fault; expected result/refusal; immediate history and readback assertions. Separate first INSERT from retries and real native pagination from synthetic fault injection.
24. **Independence checks:** tests that distinguish wrong unit factor, operand swap, different equation, wrong source, stale revision, rounding/coercion, partial history and a helper that accidentally pre-satisfies a semantic transition.
25. **Persistence/proof mapping:** expected M02 typed result, immutable claim/version and per-ID lineage, SQLite first-write/idempotency/integrity/restart/fresh read-only proof and relevant static, negative typing and strict regression obligations; note **required future proof**, not executed/admitted proof.
26. **Handoff status:** `PREPARED_FOR_CONCRETE_AUTHORITY`, `RESEARCH_CLOSED_WITH_PRECISE_HOLD`, `AUTHORITY_BLOCKED` or `NOT_YET_RESEARCHED`, each separately for mathematical oracle, native source, temporal policy, model and M02 seam; exact first unmet condition and receiver.
27. **Evidence:** official URL/document/version/access date and pinpoint location for provider claims; exact file/Git/symbol or workbook row for project claims; observation period for empirical examples; evidence classification `PROVIDER_DOCUMENTED`, `PUBLIC_SAMPLE`, `ACCEPTED_PROJECT`, `PROPOSED_POLICY`, `UNKNOWN` or `NOT_APPLICABLE` **per material fact**.

## 2. Execution gates and leaves

### Gate 0 — recover baseline and establish complete inventory

**0.1** Read the frozen governing files in full, applicable accepted root plan and exact 126/83 authority. Verify the bundle, ref, ancestry, current preparation records and any superseding accepted corrections. Do not substitute this historical review checkpoint for a live worker state.

**0.2** Create the coverage index from the existing crosswalk: exactly one record per canonical foundation D; retain 35 initial preparation families; deduplicate actual R-source inquiries and shared calendars/models; identify upstream D dependencies and all existing holds. Confirm 126 IDs, family coverage, source references and zero silent dropouts.

**Gate 0 exit:** reproducible source inventory, unchanged accepted identities, explicit baseline/authority limitations and a bounded research queue. Stop only dependencies affected by contradictory authority.

### Gate 1 — establish shared provider/raw-source specifications

**1.1** For each distinct raw R input required by the 126 D signals, resolve fields 6–15 once. Start with accepted project source maps and actual M00 projections; then consult the **primary** publisher/provider documentation (IBKR, FRED, Cboe, official exchange/index/calendar or another *actually mapped* publisher). Check field definitions and native payload semantics, not just marketing or API overview pages. Inspect relevant official change notes and examples.

**1.2** Resolve source-specific value format and realistic fixture envelopes using official specifications and labelled dated examples. Where helpful and lawfully accessible, inspect bounded historical/public observations; document the sample window and limitations. Do not fabricate provider maximums, reject valid negative values, or choose numeric representation from outlandish hypothetical magnitudes.

**1.3** Trace each raw input through actual M00 identity/temporal/SQLite contracts and current M02 acceptance seams. Record exact compatibility: supported, needs new profile/adapter, needs owner source policy, or unavailable. For date-only FRED series, for example, research the date/vintage semantics and identify the exact selector mismatch; **do not invent a UTC event instant**. Reuse M00's existing capabilities where applicable.

**1.4** Build shared calendar, options-contract, official OI, trade/volume, market-depth state/replay, event-vintage and model convention notes only where demanded by the R/D dependency graph. Resolve factual issues here; refer genuine discretionary semantic choices to the owner with a narrow recommended disposition and consequences.

**Gate 1 exit:** every referenced R has an evidence-backed specification or a **precise researched hold**. No generic “research FRED/IBKR” placeholders remain. A shared hold is recorded once and propagated to its actual dependants.

### Gate 2 — enrich all 126 D specifications by compatible family

**2.1** Work through the 35 preparation families in dependency order. Reuse their existing M01 code/test locators, equations, histories and witnesses. Reconcile source-contract references from Gate 1 and effective accepted overlays. **Do not re-audit completed unrelated mathematics.**

**2.2** For each of the 126 D IDs, complete fields 1–5 and 16–21, linking shared source facts rather than copying them. Calculate the fixed numeric oracles independently of production code. For model-dependent, ambiguous or externally governed semantics, research available primary methodological authority and preserve a precise unresolved decision where no accepted convention exists.

**2.3** Distinguish three things explicitly: (a) a provider fact now established, (b) an engineering conversion/fixture we can specify from existing accepted authority, and (c) a new policy requiring lawful acceptance. Do not postpone (a) or (b) merely because (c) is unresolved.

**Gate 2 exit:** 126 individually attributable source-linked calculation specifications, with no missing ID, hidden assumed unit/clock/range, or unlabelled hold. `RESEARCH_CLOSED_WITH_PRECISE_HOLD` is legitimate research completion but **not** implementation readiness.

### Gate 3 — precompute test vectors and executable fixture instructions

**3.1** For every D, prepare fields 22–25: independently traceable positive, negative and boundary oracles, explicit raw-to-canonical values, fault preconditions and public operation sequence. Use deterministic synthetic fixtures and, where valuable, a separately labelled real provider example. Never make future tests depend on an unpinned live market value.

**3.2** For each materially distinct family mechanism, challenge an oracle and an adversarial sequence independently of the legacy helper. Include actual input cardinality, cursor/offset exhaustion, record ordering, native revisions, incorrect scalar factor, wrong source/identity, and storage restart where applicable. The D014 four-failure fixture lesson is an explicit pre-authoring check.

**3.3** Produce concise M02 implementation-facing test specifications with exact expected values/assertions and required lineage/refusal/durability evidence. Clearly identify any case blocked by absent source, model or implementation authority. Do not author, change, run or admit production tests under this research plan.

**Gate 3 exit:** every D has directly usable test vectors/instructions **or** an explicit first unsatisfied contract that prevents a valid oracle. The instructions distinguish already established shared mechanisms from per-D semantic obligations; no synthetic example is mislabelled native-certified.

### Gate 4 — independent challenge, reconciliation and verified transfer

**4.1** Reconcile every D, its exact R dependencies, relevant D predecessors and fixture vectors. Check numerical examples independently, provider citations, field consistency, missing/sentinel handling, range classifications, times, identities and hold propagation. Independently challenge at least one representative source-to-output vector and one negative/temporal sequence per compatible family **plus each materially unique calculation or source profile**. Author self-check is not independent programme acceptance.

**4.2** Update the existing crosswalk and family packets, `OPEN_GAPS.md` and `HANDOFF.md`. Add only the minimum normalised shared source index and machine-readable test-vector file needed to prevent duplication. Classify 126 rows by actual research/fixture readiness; list remaining **owner policy decisions separately from provider questions**. The final handoff must say which facts the implementation worker should **not** re-research and precisely which decisions/contracts remain open.

**4.3** Commit documentary changes on the isolated research branch. Verify changed paths, IDs/references, no frozen or implementation/test/proof mutation, Git ancestry, complete bundle creation, and fresh-clone HEAD/tree/tracked-content recovery. Retain earlier history; do not rewrite or replace the original bundle without a recoverable successor. Reconcile against live worker authority **at transfer**, without asserting that the snapshot is its current HEAD.

**Gate 4 exit:** one recoverable successor Git bundle containing the completed research and pre-test specifications; a short coverage/hold report and exact commit/tree/hash; zero unsupported `READY` claims. Not G6.1/G6.4 acceptance.

## 3. Minimal output structure and quality rules

Keep outputs under `handoff/foundation_implementation/reuse_preparation/` on the authorised isolated branch:

- **Extend** `M01_M02_REUSE_CROSSWALK.csv` rather than replace it: 126 keyed rows with source-contract and test-vector references, per-domain statuses and evidence locators.
- **Add** one normalised source/raw-contract index keyed by distinct R and source/profile version. Include referenced official citations and document dates; shared facts occur once.
- **Extend** only affected `FAMILY_*.md` packets with equations, conversion rules, history, representative operating envelopes, boundary witnesses and unresolved semantics. Avoid one narrative report per D.
- **Add** a structured, machine-readable test-vector manifest keyed by D ID and scenario ID; represent complex outputs in typed scenario records, not a flattened scalar spreadsheet. Expected outcomes are independently derived, not scraped from production code.
- **Update** `OPEN_GAPS.md` and `HANDOFF.md` with precise decision ownership and implementation instructions. No second programme plan, redundant receipt collection or duplicate provider dossiers.

For every field, distinguish **documented native domain**, **representative observed range**, **proposed stress-test envelope** and **accepted rejection bound**. They are different propositions. Use `Decimal`/integer/time/structured types appropriate to the actual source and accepted contract; do not choose an enormous arbitrary limit merely to appear safe. Preserve missing, negative and zero cases where lawful.

For every real-data example record publisher, series/contract, observation date/instant, vintage if relevant, source units and canonical conversion. For every deterministic test record fixture values, expected answer/refusal, accepted formula and exact distinguishing assertion. Real examples support realism; pinned synthetic vectors keep tests repeatable.

## 4. Completion, holds and efficiency discipline

**Research closure is not source admission.** Completion requires 126/126 individual inspected D dispositions; all relevant distinct R references resolved to source evidence or precise exhausted holds; an applicable oracle/fixture for each authorised computation or exact reason it cannot be derived; and reproducible bundle transfer. Report separately: researched, usable without further factual lookup, policy-held, source-access-held, model-held and implementation/proof-held. A completed investigation may legitimately leave an exact authority decision open; it may not present that D as ready for native execution.

At first required governance/integrity failure stop dependent work. A missing provider fact calls for targeted primary research before classification as `UNKNOWN`; lack of an authenticated service must not prevent using published documentation. Continue independent families if their dependencies are closed. Do not over-investigate hypothetical edge cases lacking relevance to an accepted source contract. One official provider finding should settle every dependent D, with individual consequences recorded without repeated searches.

**Owner decision:** the owner approved this task-local plan and its isolated research-branch scope on 21 October 2026. This commit establishes the plan only; none of its research gates or leaves has been executed. Later incorporation into the active Gate 6 pilot, source/profile authority or root `EXEC_PLAN.md` requires the then-applicable reconciliation and approval. This commission does not claim that the pilot has stopped or that any D042/D043/D047 source hold is already closed.

**Approval recorded:** 21 October 2026 (owner instruction in this conversation).
