# Gate 2 — accepted D117 profile: source and calendar reassessment

**Date:** 16 October 2026 — Australia/Melbourne.

**Disposition:** Profile P1–P6 is OWNER ACCEPTED. D117 classification remains UNKNOWN; G2I-011 remains BLOCKED on the source/counter/calendar contract. Gate 2 remains unaccepted. A missing live deployment is not the reason for this planning blocker.

## 1. Accepted meaning and inspected scope

The exact accepted text and reviewed Git/digest identity are in `handoff/m01_completion/authority/D117_OWNER_APPROVED_EXACT_CONTRACT_BASELINE_20261016.md`. No further owner approval is requested for those clauses or the R041-only dependency. The immutable first version compares the same option contract at the same elapsed regular-session minute against twenty immediately preceding completed regular sessions. Receipt cutoffs and the sixty-second interval are binding; no substitute contract, shortened sample or later backfill is allowed.

Inspected: root guardrails/agent map/ExecPlan; preceding D117 dependency acceptance, exact profile proposal, authority index, accepted planning-boundary record and A1–A7 proposal; current D117/G2I-011 and its architecture link in the three cumulative registers; registered M00/M01 responsibilities; M00 public API `RawObservationOccurrenceV1`, `RawSelectionIdentityV1`, `RawSignalProjectionMappingV1` and `ProjectedRawValueV1` declarations and their adjacent validation. This is a bounded source-contract inspection, not a C–E implementation census. No application imports, tests, runtime validators, database or broker operations ran.

The historical G2.2–G2.4 fields remain as-of assessment evidence; current PB fields and owner overlays supersede their obsolete R075/profile-undecided requirements. An unchanged historical field must not be read as revoking current acceptance.

## 2. Primary provider evidence

All URLs below were retrieved on 16 October 2026. Documentation is evidence of the described provider interface, not certification of this project's collector.

| Evidence | Established observation | Limit |
|---|---|---|
| [IBKR Streaming Data](https://www.interactivebrokers.com/docs/tws-api/doc/md/streaming-data), Available Tick Types / Volume Data / EWrapper.TickSize | Tick 8 is native daily contract volume; native volume is not updated for every trade. `tickSize` carries request ID, field and size. | These inspected definitions do not establish a particular option's counter reset/session boundary, current-session certification or a project's historical receipt stream. |
| [IBKR Contract Details introduction](https://www.interactivebrokers.com/docs/tws-api/doc/contracts-financial-instruments/contract-details/introduction) and [ContractDetails reference](https://www.interactivebrokers.com/docs/tws-api/ref/contract-details), schedule/timezone fields | Contract lookup can return multiple matches. Schedule fields include tradingHours, liquidHours and timeZoneId; liquidHours describes regular hours on the specified exchange. | A specific contract/exchange, retained schedule coverage and immutable calendar binding have not been established here. Native timezone strings need justified IANA interpretation. |
| [IBKR Delayed Market Data](https://www.interactivebrokers.com/docs/tws-api/doc/md/delayed-data), Request/Receive Market Data Type | Request-scoped callbacks distinguish live, frozen and delayed modes. | This does not show that a selected R041 occurrence preserves that status or proves the intended counter session. |
| [IBKR Market Data introduction](https://www.interactivebrokers.com/docs/tws-api/doc/md/introduction), Historical Data Filtering | Historical data is filtered and may differ from live data; later historical queries can return adjusted data. | A historical bar request is not established as equivalent to the accepted live-native-volume receipt history. |

The older official GitHub tick-types, ContractDetails, market-data-type and historical-limitations pages were also opened as corroboration and explicitly identify themselves as deprecated. Current official pages above govern the findings. Search-index hits for four deeper documentation paths returned 404 when opened; an initial available-tick-types parent was inaccessible. Those failed fetches are not treated as evidence. Navigation through the current documentation yielded the consolidated pages cited above. Third-party search results and comments were not relied upon.

## 3. Separate propositions and disposition

| ID | Required proposition | Evidence state / remaining work |
|---|---|---|
| SC-D117-01 | Exact selected option identity and request/source variant, plus native field-to-R041 unit correspondence | Provider shape partly established. A version-specific option-contract mapping/identity/unit contract is still required. Do not apply stock-lot scaling automatically to options. |
| SC-D117-02 | The selected daily counter's session/reset meaning and its compatibility with the accepted regular-session comparison | UNKNOWN from inspected documentation. This is the first unresolved meaning invariant. Obtain provider/version-specific primary evidence of counter period/reset and late-correction treatment. The profile samples reported volume, so revisions are retained as reported; do not infer trade-time completeness. |
| SC-D117-03 | A feasible authoritative calendar and timezone binding covering current plus twenty prior sessions, including early closes | Schedule fields exist. Contract/exchange selection, historical schedule coverage, IANA mapping and immutable calendar/version provenance remain unestablished. A generic stock-hours assumption cannot fill these fields. |
| SC-D117-04 | Request/status lineage can justify real-time mode and intended session without inventing native fields | Request-scoped mode reporting documented; required occurrence association/generation and counter/session evidence must be specified. Existing optional M00 metadata is not proof that an IBKR instance supplies it. |
| SC-D117-05 | Prior inputs are original eligible receipts visible by each historical cutoff, with strict same-stream order | Accepted law is exact. M00 types represent receipt time, sequence/scope, native record and versioned projection; an actual mapping/stream is not established. A later download cannot create a receipt that occurred at an earlier cutoff. No new history-retention capability is claimed. |
| SC-D117-06 | Actual lawful collection, retention, mapping, public projection and result conformity | UNPROVEN operational work. Receives later C–E hold points only after the classification-critical contract above is established under A1/A2. No production admission now. |

**Reasoning from accepted law:** even a numerically matching bar cannot prove what the project received by an earlier historical cutoff. Summing historical minute bars or substituting RTVolume/RTTradeVolume also changes the selected source/period without an established equivalence. The accepted profile already forbids these silent substitutions; this assessment introduces no new mathematical rule.

Sixty-second receipt freshness is not a guarantee of sixty-second source-event freshness. Duplicate/retransmitted callbacks and old counter values require justified eligibility; recent delivery alone does not certify the session. A quiet contract may have no eligible observation and correctly refuse. The approval does not guarantee universal minute-by-minute output or twenty-session availability.

## 4. Exact continuation and receiving boundary

Next dependent investigation: establish SC-D117-01/02 for a specified supported IBKR API/source variant, then establish SC-D117-03/04 calendar/status feasibility. A competent source contract can answer these without connecting the project. Actual entitlement, capture and source-to-public-output conformity remain future work; no live action is authorised.

The required evidence is a counter/session/reset specification and source/calendar contract, not another owner approval of P1–P6. Do not convert this documentary stop into repeated measurement approvals or waive the missing semantics. Independent Gate 2 documentary issues may proceed under existing authority; no dependent D117 eligibility upgrade is claimed here.

The 209-identity, 21-issue and 124-link populations and classifications remain unchanged: 100 conditional foundation candidates, 74 established non-foundation classifications and 35 material unknowns. Only D117/G2I-011 current decision fields and its D117/G2I-021 architecture-dependent status receive this result. G2I-021 is not resolved because D117's final classification remains unknown. The L2 blockers and other decisions remain outstanding.

Main, root plan, guardrails, all agent instructions, original proposal, catalogue/runtime/workbook/source/test/schema/registry files remain unchanged. Package verification is separate from source semantics; archive extraction/readback and Git integrity do not establish source admission.

## 5. Owner-requested scope audit and correction — 16 October 2026, 23:02 Melbourne

**Audit baseline:** `55c7c83fc21e7a28fe8d06d021286ae2ea5294f0`; comparison origin `5845623caa5b4d7fc078df5415c12acc4c0e739b` (supplied acquisition-scope checkpoint). The owner asked to continue D117 and confirm alignment with the ExecPlan and subsequent authorisations. This section corrects the scope of the evidence gaps above; it does not amend accepted P1–P6 or accept a classification.

| Work performed | Controlling authority | Audit result |
|---|---|---|
| Investigate D117 meaning, R075 role and complete input contract | ExecPlan G2.2/G2.3/G2.4/G2.6; accepted A1–A7 permits independent documentary work after L2 blocker | Within authorised Gate 2 investigation. D117 is not a dependency on resolving the L2 book. |
| Remove mandatory R075 input | Owner accepted `D117-RAW-VOLUME-HISTORY-20261016-01`, exact six clauses at `ca11e1aa683e6561150d1c809f7af88162eaca7c` | Authorised semantic overlay; not an unapproved code/catalogue edit. |
| Fix first exact-contract 20-session receipt-time version | Owner accepted P1–P6 of `D117-BASELINE-EXACT-CONTRACT-20SESSION-RECEIPT-20261016-01` at `ee82fa7460a8a253c16d2704a8d9cc2aae7bfdcc` | Explicit subsequent domain authority supplements the original plan's no-unapproved-definition-change boundary. These choices are accepted, not newly pending. |
| Documentary source feasibility versus actual deployment evidence | Accepted A1/A2/A3 and P6 | Prior gap descriptions mixed these categories in places; corrected below. |
| Gate 2 exit, successor planning and implementation | ExecPlan exit rules and accepted A7 | Gate 2 remains unaccepted. No successor plan activated, implementation, integration or main merge. |

**Direct Git audit:** all twelve changed paths between the comparison checkpoints are handoff assessment/authority/index/register files. Root `EXEC_PLAN.md` remains SHA-256 `8abed334586aea28b22db7ec6fd0614f41cdb47a02b08cb4e839eb61b96e8b0e`; guardrails and root agents are byte-identical to the supplied checkpoint. No production source, tests, workbook, schema, runtime configuration, architecture registry or other non-handoff path changed. Main remains `77d82bd8ee4268673715fe7e5653b6a65a299b54`.

The three register populations remain 209/21/124. Comparison of their inherited columns finds changes only to D117, G2I-011 and D117's G2I-021 link; four planning/operational columns were appended to all records under A6. Thus the visually large CSV diff is not evidence of a 209-row reclassification. Historical source/classification fields are retained. The new audit makes no retrospective claim about executing tests: only Git/documentary inspections were performed in these passes.

### 5.1 Exact correction to prior gap descriptions

The sentence in §3 SC-D117-05 that an actual mapping/stream is not established is an **operational observation**, not an independent Gate 2 semantic blocker. The same qualification applies to §2/§3 references to a specific contract ID, instantiated calendar/version, retained history and actual occurrence/status association. Their absence in an unbuilt deployment does not itself prevent planning classification. Earlier broad “source/counter/calendar” wording must not be interpreted as requiring live capture or twenty collected sessions to close Gate 2.

A1 still requires evidence that the specified source can express the necessary meaning. A3 permits deployment-bound values only within an explicit, classification-preserving contract. Therefore:

- Contract IDs/request IDs/mapping-instance IDs remain future bindings. The required exact identity, field correspondence, option-volume units and permissible source variant must be semantically settled now; sample IDs are not proof.
- P2 already fixes the applicable contract's authoritative regular-session calendar, immutable version, IANA timezone, same elapsed minute and early-close refusal. A fabricated current calendar ID is unnecessary. A concrete binding and complete historical schedule coverage are prerequisites for valid runtime output; source feasibility and any meaning-changing calendar choice must still be resolved before classification.
- Provider schedule/timezone fields and request-scoped market-data-mode reporting are documented. This supports representational feasibility; it does not certify an acquisition deployment. Source-specific date/session/counter meaning is a separate question.
- P3/P5 already fix original receipt cutoffs, sequence scope and lineage. Proving actual retention, mapping, chronological capture and public projection is receiving operational work, subject to A2. A full twenty-session live capture is not imposed as a planning prerequisite.

No operational item is declared finally deferred while its associated semantic contract remains unresolved. The correction prevents actual-instance absence from serving as a substitute reason for the remaining semantic blocker; it does not waive that blocker or establish the missing contract.

## 6. Continued D117 investigation — narrowed counter-period question

Reopened the current official [Streaming Data](https://www.interactivebrokers.com/docs/tws-api/doc/md/streaming-data) request/tick table/Volume Data/callback sections, [Contract Details introduction](https://www.interactivebrokers.com/docs/tws-api/doc/contracts-financial-instruments/contract-details/introduction) and [Delayed Market Data](https://www.interactivebrokers.com/docs/tws-api/doc/md/delayed-data), specifically their schedule and mode sections.

**Verified provider description:** `reqMktData` uses an instrument contract and request ID; tick 8 is daily volume via `tickSize`. Native volume may include late transactions/corrections and is not a per-trade update. This supports a reported-volume observable, not a complete trade tape. The generic callback shape does not itself attach a volume-counter date. Provider “delayed transactions” within native volume must not be confused with the separate delayed-market-data delivery mode.

**Separate reasoning from accepted meaning:** the regular-session minute defines the comparison coordinate. It does not, by itself, establish that the native numerator contains only regular-hours trades or resets exactly at the regular open. No opening-value subtraction, reset detector or exclusion of extended-hours trades is authorised by P1–P6. Retain the reported value; establish its counter period rather than changing it.

**First unresolved source invariant:** establish what “day” identifies for the selected option native-volume stream and how a received value can be assigned to that counter period at the regular-session cutoff, particularly on first delivery/reconnect/day rollover. Recent receipt and a real-time mode flag alone do not prove that date. No exact reset instant, native day field or certification marker is invented. This remains UNKNOWN from the inspected primary material, not a universal claim that IBKR has no answer.

A bounded additional official-domain search for native/daily-volume reset and option-volume period semantics did not establish that invariant. Results concerning API order-ID reset do not concern volume and were excluded. General option-volume display descriptions and repeated tick-table hits did not establish the missing rollover/association rule. This search is not an exhaustive absence proof; third-party sites and comments were not used.

### 6.1 Concrete evidence request prepared, not sent

The next source-custodian/provider evidence needs to answer this exact question:

> For the supported TWS API `reqMktData` stream of one identified US equity option (`OPT`), with `tickSize` field 8 as the native volume source: what precisely defines the reported volume day/counter period and units; what happens at day rollover and first delivery/reconnect; and which documented response or request/session/status relationship establishes that a delivered value belongs to the intended current volume day rather than a retained earlier day? Identify the applicable interface/version qualifications and explain how late reports or cancellations affect the reported value and period assignment.

This is a prepared technical question, not a message to IBKR or another person; no external contact occurred. A primary specification, applicable provider clarification or other admissible source evidence may answer it. A project schema or an assistant's invented adapter field cannot answer it. Actual source-capture proof remains separately commissioned work.

**Current result:** owner-approved input and baseline definitions retained; operational-only gaps separated; D117 classification remains UNKNOWN solely where the classification-critical source contract is incomplete. Gate 2 remains BLOCKED. The next useful dependent action is obtain/evaluate the counter-period evidence above, not another measurement approval or repeated test run. No new owner decision is requested in this checkpoint.

### 6.2 Packaging integrity failure and exact recovery

An initial inherited-byte preservation comparison stopped with `tarfile.ReadError: unexpected end of data`. The previous local archive `NVDA_V2_GATE_2_D117_BASELINE_ACCEPTED_SOURCE_REVIEW_FULL_GIT_20261016.tar.gz` was 12,988,416 bytes with SHA-256 `dbdd5d22b491949c0a1e869d29fe7e4b0da10ec0924d7a8f54b63433d2ed6b50`, instead of the previously recorded 17,132,530 bytes / `f70adbb5a89d8547554e3a7707df3de5a59945de1f4613169c4d0479a8ffb74b`. `gzip -t` independently reported unexpected end of file. The cause of truncation is UNKNOWN; no stronger cause is inferred.

Packaging stopped at that failure. The saved version was retrieved separately from `libfile_ed688f2eb4bc8191b8d2cb0bf0e855ee`, version 0. Its bytes and SHA-256 exactly match the recorded 17,132,530-byte original. The same full inherited-file archive-to-workspace comparison was rerun against those recovered exact bytes and succeeded for every unchanged tracked file. This is exact recovery and repetition of the failed required check, not substitution of a weaker Git-only check. The truncated local file remains preserved as discrepancy evidence; the failed attempt is not labelled PASS. Final candidate packaging still requires separate extraction/readback, complete regular-file byte equality and Git integrity checks.

## 7. Current owner direction: required input contract, not upstream API commissioning

**Current authority:** after the previous checkpoint the programme owner said: “No, you're out of scope. The API to IBKR is another module entirely.” The owner then instructed: “Okay, keep working on the plan that looks to close gate two.” This explicit correction governs the present continuation. It is not treated as approval of a live source or as blanket closure of all other classification issues.

The assistant's prior demand for an IBKR response as the next D117 task crossed this boundary. Sections 3–6 above remain historical investigation evidence, including real provider unknowns, but their routing of the acquisition investigation as a prerequisite to the D117 calculation-boundary assessment is superseded by this section. No provider contact or further API investigation is performed here. No native field, day-reset rule or certification signal has been invented to make that correction.

### 7.1 Complete required D117 interface and responsibility split

The following restates the already accepted dependency amendment and P1–P6; it does not introduce another measurement convention or runtime schema.

| Boundary | Required responsibility / fact | Exclusion or hold point |
|---|---|---|
| Separate upstream acquisition module | Supply reported cumulative volume for one exact option contract, with justified source/variant, units, counter-period/session association and real-time status; preserve the acquisition evidence needed for provenance. | Exact IBKR request/callback/reset interpretation and conformity belong to that separately commissioned module. No assertion that it currently supplies these facts. |
| M00 raw boundary | Preserve original observations, source identity/period/status evidence, temporal kind, receipt time/order and versioned field/unit projection under its public seam. Required counter/session association must be justified, not fabricated by a new native-field claim. | No network client, D117 z-score, cumulative-counter summation, interpolation or guessed event time. No actual admitted mapping is asserted. |
| Calculation boundary, proposed M02 | Consume current and historical R041 volume facts only, under matching exact contract/provider/variant/native-counter meaning and canonical contract-count units. Bind the accepted profile, calendar, selection/mapping/unit versions and cutoff lineage. | No R075, D predecessor, portfolio/candidate/order context, provider-specific parsing fallback or acquisition responsibility. |

Each eligible input must be established as belonging to its intended source-volume period/session. The producer must justify that association through native evidence or lawful source/request/status provenance; D117 is not authorised to invent it from receipt date, sequence name, presumed midnight reset or regular opening. The regular-session minute is the comparison coordinate, not a new claim that the source counter contains regular-hours trades only.

The accepted sample law remains exactly twenty immediately preceding completed regular sessions and the current session, one value at the same elapsed minute of each, receipt interval `(T-60 seconds, T]`, strict receipt/sequence selection and historical knowledge cutoff. All values are finite and non-negative. Genuine zero is allowed, missing is not zero. No substitute contract, backfill, shorter window, skipped early-close coordinate or imputation. Historical mean uses 20 values; sample variance denominator is 19; output is `(current-mean)/sample_sd`, dimensionless, with strictly positive sample SD. Required metadata/configuration are provenance and fixed measurement conventions, not extra numerical R inputs.

A concrete deployment may not emit a valid occurrence until those input, period, calendar, history, unit and lineage obligations are proved. This output prohibition remains intact even though the consumer's planning classification no longer commissions its upstream producer.

### 7.2 Row-specific strategy-independence reassessment

| ADR-WBV2-001 / ExecPlan criterion | Exact basis | Assessment |
|---|---|---|
| Complete market/source-time numerical closure | Accepted R041-only amendment; full 209-node D graph statically reconstructed; D117 has no D predecessor or descendant. | Numerical direct and terminal R set is R041. No upstream strategy calculation hidden in a D chain. |
| Fixed descriptive meaning | K04 sample z-score plus accepted P1–P6 exact-contract twenty-session version. | Describes reported volume relative to that contract's prior reported activity; no forecast or trade instruction. |
| Non-strategy configuration | Immutable horizon, minute coordinate, receipt freshness, calendar/version and strict exact-contract matching; no peer bucket or strategy coefficient. | Configuration changes require a separate measurement version; short-history contracts refuse. |
| Selection, units, history and failure contract | Required interface above plus P1–P5 and brief §§6/8/9/11/17. | Defined at the consuming boundary. Actual source conformity remains a producer/admission obligation, not a missing D117 equation or discretionary selection convention. |
| Implementation, public materialisation, durability and tests | ExecPlan G2.4 and ADR1 classification-versus-implementation distinction. | Not proved or admitted by this assessment. Required later evidence remains explicit. |

**New assessment proposal:** `PROPOSED_M02_SEMANTIC_ELIGIBLE_CONDITIONAL` for this restricted D117 version. “Conditional” means lawful source/input provision, implementation, proof and admission before output; it does not reserve an unselected mathematical window, bucket or strategy meaning. No remaining material D117 definition decision is identified within this accepted consumer contract. The unresolved IBKR counter/callback facts are not asserted resolved; their investigation is assigned outside this Gate 2 consumer assessment by the owner's current scope direction.

This is a reasoned classification proposal for the eventual Gate 2 exit candidate, **not an owner-approved final allocation, a runtime M02 admission or Gate 2 acceptance**. It is not derived from the historical YES label. G2I-011 is resolved for this bounded planning assessment; it retains its ID and all history. The D117 link to G2I-021 no longer blocks a choice between foundation and peer responsibility; the wider group-boundary issue remains open for other identities.

### 7.3 Receiving obligations — no silent waiver

| Reference | Receiver | Required evidence and acceptance hold point | Consequence of failure |
|---|---|---|---|
| D117-UPSTREAM-01 | Separately commissioned acquisition-module authority/implementer; not opened here | Source/unit/counter-period/status contract and actual capture conformity, including first delivery, rollover and reconnect. Must be accepted before D117 production input admission. | No eligible R041 for this profile; no D117 output. Return an incompatible source to source/contract authority; never silently change the estimator. |
| D117-M00-01 | Later C–E raw-boundary/public-ingress work | Versioned field projection, actual subject/period/status provenance, receipt/order/history retention, calendar binding and public readback. | Refuse missing/ambiguous projections or insufficient history; no provider parsing inside D117. |
| D117-CALC-01 | Later C–E calculation implementation/proof | Synchronise catalogue/hash bindings under authority; prove exact P1–P6 arithmetic, cutoff, units, complete history, refusal, lineage, retries and durable public results. | No implementation acceptance or valid production occurrence. |
| D117-EXIT-01 | Programme owner at eventual Gate 2 exit | Evaluate this exact classification proposal with the rest of the gate evidence and remaining decisions. | Gate 2 remains unaccepted until its mandatory exit propositions are satisfied. |

The source/module responsibility is named; a specific human implementer and executable later unit must be commissioned in the separately accepted receiving plan before execution. D117 has zero declared descendants, so this change does not claim downstream numerical propagation. Original 209/21/124 identities/records remain; the current classification proposal now totals 101 conditional foundation candidates, 74 established non-foundation classifications and 34 material unknowns.

**Next work under the existing Gate 2 plan:** resolve remaining calculation-boundary definitions and classification disagreements in dependency order; see `GATE_2_CLOSURE_WORKING_AGENDA_20261016.md`. Do not reopen accepted D117 choices or investigate the upstream IBKR module in this tranche. Do not apply the D117-specific reassessment automatically to other source/readiness problems without examining their own required calculation contract.
