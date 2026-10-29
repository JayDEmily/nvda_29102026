# Gate 2 — Level-II planning-contract reassessment after owner acceptance

**Date:** 16 October 2026 — Australia/Melbourne.

**Authority:** `G2_PLANNING_BOUNDARY_OWNER_ACCEPTANCE_20261016.md`, acceptance commit `021d998`; exact accepted amendment `G2-PLANNING-BOUNDARY-20261016-01`, A1–A7. Root `EXEC_PLAN.md` remains frozen. This is G2.3/G2.4/G2.6 documentary investigation, not C–E execution.

**Result:** The required native field vocabulary is supported by primary evidence. The request-to-callback applicability and usable initial-book readiness law are not fully established. D138 and D145 therefore remain separately **UNKNOWN_CLASSIFICATION_MATERIAL**. Actual subscriptions, collector configuration and runtime conformity remain unproved later work. The accepted planning overlay does not resolve either D by itself.

## 1. What was inspected

- Accepted planning amendment and owner decision, frozen root guardrails, agent map and ExecPlan; original-M01 authority index and D138/D145 owner-approved dependency amendment.
- Effective catalogue rows D011, D138 and D145; original brief §5 K06/K17; earlier L2 source-custodian and acquisition-scope records.
- Original workbook `NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`, `Raw Signals!A189:Y195`, `Derived Signals!A142:O142` and `A149:O149`, including blank cells and notes. Read-only ZIP/XML extraction; workbook unchanged.
- IBKR current [Market Depth guide](https://www.interactivebrokers.com/docs/tws-api/doc/md/market-depth), Request/Receive and both callback definitions; [Error Codes](https://www.interactivebrokers.com/docs/tws-api/doc/error-handling/error-codes), 316/317.
- IBKR's explicitly deprecated [Market Depth guide](https://interactivebrokers.github.io/tws-api/market_depth.html), Requesting/Market Maker or Exchange/Receiving, and [EWrapper reference](https://interactivebrokers.github.io/tws-api/interfaceIBApi_1_1EWrapper.html), both depth callbacks and `tickSnapshotEnd`. Historical corroboration is distinguished from current documentation.

No IBKR account/session, acquisition process, native capture, source-admission certificate or application execution was inspected. Searches of official documentation did not establish a stronger depth-initialisation completion contract. An inaccessible guessed documentation path and unsuccessful link-resolution calls were not treated as evidence; the identified pages above were retrieved directly.

## 2. Required source vocabulary: supported, not deployed

The original raw workbook explicitly separates SMART R185–R191 from direct-depth sources. Its SMART source is `EWrapper.updateMktDepthL2`; receipt time is authoritative and callback event time is absent. The approved dependency overlay gives both calculations five R fields, without changing their native meanings:

| Required R | Native field | Preserved interpretation |
|---|---|---|
| R185 | `position` | Book row position |
| R187 | `operation` | Numeric operation: 0 insert, 1 update, 2 delete |
| R188 | `side` | Numeric side: 0 ask, 1 bid |
| R189 | `price` | Native depth-row price |
| R190 | `size` | Native displayed size, with instrument/unit identity retained |

This vocabulary is corroborated by the provider callback definitions. The five values must retain common occurrence, subject, request and generation provenance; independently matching latest field values cannot establish one coherent mutation. Native enum preservation is a source obligation; converting them to consumer text symbols requires a lawful versioned interpretation later, not relabelling raw truth now.

`marketMaker` and `isSmartDepth` exist in the L2 callback grammar. Their source-selection/provenance role must be explicit, but no new direct D dependency on R186/R191 is approved in this pass. No actual mapping instance, request ID, conId, purchased entitlement, API version or session is invented.

### 2.1 SC-L2-02: a narrower verified fact does not settle routing

The current guide's Receive bullets associate SMART true with `updateMktDepth`, but its immediately following definition calls that callback direct-only. Its L2 definition also describes a SMART-dependent exchange field. The older official guide instead ties the callback to the availability of market-maker/exchange information. The older EWrapper reference explicitly describes an L2 SMART response flag.

**Supported:** a SMART-aware L2 representation matching the workbook fields is documented. **Not established:** one current, unambiguous request/venue/API selection contract that guarantees the required variant. The older reference does not silently overrule the current contradictory guide. Selecting only a supported callback and refusing incompatible input is a valid required acceptance boundary; it is not evidence that the chosen acquisition request can supply it.

The receiving evidence can be a competent provider clarification/version-specific primary specification establishing the route; a live connection is not made a universal Gate 2 prerequisite. Actual selected callback receipt remains a distinct later conformity proposition.

## 3. SC-L2-05: readiness is a source-semantic question

The older official depth guide describes initial delivery of requested/available rows followed by row mutations and permits fewer rows when depth is smaller. The inspected current guide specifies requested rows per side. Neither inspected depth section establishes a project-usable initial completion signal or an exact cutover law for a sparse book.

The EWrapper `tickSnapshotEnd` documentation concerns market-data snapshots and references `reqMktData`; it is not established here as a depth initialisation barrier. Do not borrow its timing or treat it as a `reqMktDepth` completion callback.

Consequently:

- Observed row count alone is not certified readiness. Waiting a fixed interval is not a source guarantee. Neither is added as a heuristic.
- A source contract must establish what known state exists before the first admitted mutation, how initial rows and updates interleave/order, which visible subset is claimed, and how a known sufficient prefix is proved at a calculation cutoff.
- A trace shows what happened in that capture. Without a justified protocol/readiness law, it does not prove completeness for all relevant initialisation cases.
- There is no demonstrated impossibility of a lawful readiness rule. The result is **UNKNOWN**, limited to the evidence inspected; it is not a claim that IBKR can never support these calculations.

The approved project reset requirement remains. Current provider codes require resubscription after 316 and clearing depth after 317. The plan must distinguish those events, invalidate affected state/generation and refuse dependent results until justified readiness returns. Actual code conformity is later proof.

## 4. Per-proposition disposition and receiving responsibility

Each row separates planning meaning from later operation; none certifies an operational source. PB-L2 references are the accepted amendment's receiving-work references, not newly opened gates.

| ID | Current planning assessment | Later operational obligation / hold point |
|---|---|---|
| SC-L2-01 | Required SMART/source/subject/depth scope and deployment-binding distinction recorded; exact supported selection not yet settled | PB-L2-01: bind actual contract, entitlement, request, session and versions; no source admission on intent alone |
| SC-L2-02 | Native SMART-aware L2 grammar supported; current guaranteed request/callback applicability remains BLOCKED | PB-L2-01: selected callback conformity; do not substitute direct R identities |
| SC-L2-03 | Required R-to-field/enum vocabulary supported; complete versioned selection/unit contract still incomplete | PB-L2-02: instantiate mapping and prove same-occurrence public projection and unit interpretation |
| SC-L2-04 | Receipt-only/order/generation requirements retained; exact loss/gap/tie/initial-interleave contract not established | PB-L2-02/03: observed ordering and recovery conformity, without invented exchange timestamps |
| SC-L2-05 | Initial-book readiness and available-depth cutover remain BLOCKED; no invented marker or timer | PB-L2-03: prove implementation conforms to the eventual accepted readiness law |
| SC-L2-06 | Provider reset/halt requirements corroborated; project generation/reinitialisation contract still depends on SC-L2-05 | PB-L2-03: reset/halt/reconnect/refusal witnesses; no stale-state carryover |
| SC-L2-07 | D138 standing-depth/D011-cutoff requirement established by accepted meaning; complete source selection remains BLOCKED | PB-L2-04: D138 standing-state/OLS-selection conformity, distinct from D145 |
| SC-L2-08 | D145 consecutive-state/predecessor/window requirement established by accepted meaning; sufficient state history remains BLOCKED | PB-L2-04: D145 predecessor/warm-up/window conformity, distinct from D138 |
| SC-L2-09 | Metadata roles recorded separately; no extra direct-R approval or source-family substitution | PB-L2-01/02: actual metadata and selection conformity after the required planning decision |

These are not nine resolved contracts. Actual deployment values and implementation proof are later work; unresolved source feasibility and selection/readiness meaning stay in Gate 2. No blanket deferral is entered for either material issue.

## 5. Independent D consequences

**D138 / G2I-015:** keep the approved five-R list plus D011, K06 per-side OLS, top-N scope and complete standing-depth/cutoff refusal. Planning-source closure remains blocked on applicable callback selection, readiness and exact state/cutoff/units/convention contract. Its current implementation branch's treatment of triples is later engineering evidence, not the deciding reason to classify the intended measurement downstream.

**D145 / G2I-018:** keep the approved five-R list, K17 equation and 1s/5s/1m obligations. Planning-source closure remains blocked on deterministically available prior/current best states, source/generation ordering and sufficient predecessor/window history. A price-key implementation is not proof of position-addressed input conformity; that existing implementation question goes to C–E after meaning is settled.

The existing descendant issue links remain unchanged. No downstream semantic disqualifier is reversed, no classification count improves and no module count is selected. The three registers gain explicit planning/operational overlay fields; their earlier findings remain historical as-of entries.

## 6. Exact missing source evidence; no broker action requested now

The next L2 source-custodian input must answer these bounded questions with an identified official/versioned basis:

1. For a SMART request with the intended security/venue support, which callback variant is supported and what resolves the current guide's conflicting route descriptions? Establish selection compatibility with the workbook's SMART R family; do not infer it from the request flag alone.
2. What exact protocol establishes usable initial standing state, including a book with fewer than requested rows? Is there a depth-specific completion boundary or another provable initial-prefix/readiness law? Describe ordering/interleaving and sparse/empty cases without an invented timeout.
3. How does that law restart after 316/317/reconnect, and what guarantees permit D138's cutoff state and D145's complete predecessor/window history to be selected from one valid generation?

This is an **unsent evidence request**, not permission to contact IBKR, purchase a subscription, connect the API or implement a collector. A competent primary specification can resolve planning questions without current integration. Operational traces and tests remain future conformity evidence.

**Continuation:** stop the dependent L2 closure at these facts. Investigate independent `G2I-011` / D117 next: its catalogue has no D predecessor and only R041/R075 terminals, so its source-role question does not depend on L2 readiness. Do not open C–E or ask for Gate 2 acceptance while material classifications remain unknown.

## 7. Evidence limits and programme status

The accepted overlay is effective; Gate 2 itself is not accepted. This pass makes no live-source or implementation claim. No application tests, runtime validator, database or broker operation ran. Original workbook/catalogue, approved mathematics, production source, schemas, registry, root governance and accepted main remain unchanged. The previously unavailable September implementation-admission attachment is now provisioned in this turn, but is not needed for these bounded source questions and was not inspected here; no claim of its verification is made.
