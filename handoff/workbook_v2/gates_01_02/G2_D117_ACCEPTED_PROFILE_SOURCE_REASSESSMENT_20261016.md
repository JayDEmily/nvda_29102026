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
