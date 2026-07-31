# NVIDIA 2026 — Canonical Alpha Delivery ExecPlan

## Status

**Status:** `ACTIVE:MVP_FAST_TRACK_M02_GATE_D`
**Amendment date:** `2026-07-31`
**Owner:** User and Project Manager thread
**Live pointer:** `ROADMAP_LEDGER_V2.md`
**Gate C protocol:** `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`

The user has directed that the alpha move from control-heavy certification into
normative, proof and implementation delivery. This plan preserves the accepted
M00–M15 architecture and the hierarchy `normative documents → tests → code`,
while removing checkpoints that do not create a new semantic state.

## 1. Objective

Deliver a deterministic, inspectable alpha that maps the cognition of a
high-grade single-name NVDA desk:

1. admit and preserve source facts;
2. prepare typed runtime context;
3. interpret temporal, regime and options-flow state;
4. determine posture and eligible playbooks;
5. form one execution expression;
6. join independent risk and fresh-capital authority;
7. create bounded downstream opening/lifecycle evidence;
8. preserve review and replay lineage.

The alpha remains a modular monolith. It is not a live-trading, autonomous,
production-durable or profitability-proven system.

## 2. Delivery rule

Each bounded behaviour advances through three semantic states:

`C-NORM normative closure → C-PROOF minimum truthful proof → Gate D implementation`

Only the first two states belong to Gate C. Gate D opens module-locally as soon
as the owning behaviour passes them. Programme-wide Gate C completion is not a
prerequisite to starting code.

The former eight-leaf MLC route and worker/tester archive cycle remain
historical evidence. They may be reused when helpful but are not mandatory
delivery mechanics.

## 3. Accepted architecture

| ID | Ownership Module | Owns | Alpha treatment |
|---|---|---|---|
| M00 | application_shell | HTTP/CLI translation and dependency composition | replace mixed composition root last |
| M01 | source_admission | source identity, raw capture and source-family admission | refactor around one ingress owner |
| M02 | calendar | four-layer financial-calendar reference and projection | retain algorithms; replace split truth |
| M03 | preparation | typed prepared context and field-resolution evidence | replace generic mapping core |
| M04 | packet_protocol | DMPV3 carriage validation only | retain envelope; remove fabricated defaults |
| M05 | serial_cognition | six ordered candidate-forming stages | retain local kernels; replace orchestrator |
| M06 | parallel_risk | independent environmental risk lane | complete explicit, run-scoped composition |
| M07 | coefficient_modifier_authority | versioned coefficients, precedence, bounds and receipts | complete K12 then refactor |
| M08 | playbook_catalogue | definitions, catalogue and eligibility semantics | complete K13 then refactor |
| M09 | capital_authority | pre-deployment join, sizing and fresh-capital decision | retain calculations; rebuild state/join |
| M10 | execution_gateway | readiness, paper boundary and execution receipts | replace boundary before operational use |
| M11 | portfolio_lifecycle | position, inventory, exit and close lifecycle | retain kernels; replace state ownership |
| M12 | evidence_replay | review, explanation and authoritative replay classification | retain projections; replace replay core |
| M13 | state_kernel | transaction, idempotency, atomic receipt and storage ports | accepted alpha implementation |
| M14 | proof_promotion | proof manifests, tiers and promotion evidence | continuous governance |
| M15 | vocabulary_governance | namespaced term admission and projections | continuous governance |

The 18 canonical surfaces remain `thin_seam`; none is promoted to production
readiness by this plan.

## 4. Dependency graph

Runtime prerequisites are:

- M01: none
- M02: M01
- M03: M01, M02
- M04: none
- M05: M03, M04, M07, M08
- M06: M03, M04
- M07: none
- M08: none
- M09: M05, M06, M07
- M10: M09
- M11: M10
- M12: M04 plus accepted evidence-export contracts
- M00: final composition

M13 supplies transaction mechanics without owning domain meaning. M14 and M15
are governance prerequisites, not universal runtime imports.

## 5. Atlas treatment

The accepted Atlas package contains 287 cohorts and 1,716 source records. Its
allocation and lineage govern routing; its behavioural content is candidate
evidence.

For the active behaviour only:

1. inspect the relevant cohort rows and record lineage;
2. admit, reject, split, merge or defer the behaviour in the existing normative
   or module record;
3. retain cohort/record trace;
4. do not create a dossier for every member record;
5. do not port donor plumbing or contradictions merely because they exist.

The accepted record dispositions already distinguish 288 retained native
items, 380 strengthening items, 152 new normative candidates, 94
contradictions and 494 rejected donor-plumbing items. Implementation must
preserve those distinctions.

## 6. Proof and implementation economy

Gate C proof should normally contain:

- one conforming public-seam case;
- the material fail-closed or prohibited case;
- one plausible false-positive challenge.

Add state, replay, substitution, ordering or numeric proof only when the active
behaviour owns it.

Independent validation is mandatory for:

- M13 transaction/atomicity work;
- M09 capital sizing/deployment;
- M10 broker/execution acknowledgement and fill work;
- M11 position/inventory/exit mutation;
- durable migrations or equivalent irreversible/high-consequence boundaries.

For ordinary deterministic surfaces, a reproducible Project Manager check in
the existing validation log is sufficient.

After Gate C passes, Gate D:

1. changes the smallest owner-local production surface;
2. runs targeted and affected admitted tests;
3. runs architecture and vocabulary checks where affected;
4. runs the full legacy suite as shadow evidence when available;
5. records new failures without treating unadmitted tests as automatic
   authority;
6. checkpoints the completed slice.

## 7. Current state

### Completed

- Atlas architecture and M00–M15 ownership accepted.
- Atlas current-path repair passed at `27fa427`.
- M13 alpha state kernel accepted after risk-appropriate independent proof.
- M15 namespaced vocabulary/scoped audit repair passed at `6d3ec80`.
- M04 K07 normative authority is complete in
  `docs/09.1_DMPV3_PROTOCOL_WORKING.md` section 9.10.
- M04 K07 Gate D is accepted: 271 admitted proof cases pass, the retained
  admitted partial case passes, and the source-checkpoint shadow comparison
  contains zero new failing Tier A nodes.
- M01 source admission satisfies C-NORM, C-PROOF and bounded Gate D: 18 focused
  public-seam cases pass, the proof manifest and executor contract pass, and the
  full Tier A shadow comparison contains zero new failing nodes.
- M07 K12 C-NORM is accepted in runtime-ownership section 7.7, vocabulary
  section 10.16 and architecture section 11.10.3.1; the exact public contracts
  are `PolicyBundle`, `ModifierDecision` and `ModifierApplicationReceipt`.
- M07 K12 satisfies C-NORM, C-PROOF and bounded Gate D: 20 focused cases pass,
  all five named mutants remain killed, the seven expected-red production cases
  are green, copied invalid authority is revalidated, and the exact Tier A
  shadow comparison contains zero new failing nodes.
- M08 K13 C-NORM is accepted in runtime-ownership section 7.8, vocabulary
  section 10.17 and architecture section 11.10.3.2; the exact public contracts
  are `PlaybookDefinition`, `PlaybookCatalogue` and `EligibilityDecision`.
- M08 K13 satisfies C-NORM, C-PROOF and bounded Gate D: 23 focused cases
  pass, all five named mutants remain killed, the seven expected-red production
  cases are green, copied authority and nested metadata are revalidated or
  frozen, and the exact Tier A shadow comparison contains zero new failing nodes.
- M02 K04 C-NORM is accepted in runtime-ownership section 7.9, vocabulary
  section 10.18 and architecture section 11.10.3.3; the exact public contracts
  are `CalendarFactCandidate`, `FinancialCalendarSnapshot` and
  `CalendarProjection`.

### Converted decision

M04 satisfies `C-NORM`, `C-PROOF` and bounded K07 Gate D. The former separate
MLC-V gate remains superseded because it would add another control cycle
without a new semantic claim. No broader M04, live or production-readiness
claim follows from this acceptance.

M01 satisfies `C-NORM`, `C-PROOF` and bounded source-admission Gate D. The
accepted seam is offline, contract-driven, fail-closed and explicitly volatile;
it does not establish live provider connectivity, durable replay, M02 calendar
semantics, M03 preparation or downstream decision authority.

M07 satisfies `C-NORM`, `C-PROOF` and bounded K12 Gate D. The accepted package
is immutable, deterministic and side-effect-free; it does not create generic
policy, capital, playbook, execution, lifecycle, replay, transaction or
external-state-mutation authority.

M08 satisfies `C-NORM`, `C-PROOF` and bounded K13 Gate D. The accepted package
is immutable, deterministic and side-effect-free; it preserves catalogue,
posture, context and material-fact lineage, and it does not acquire candidate
expression, capital, execution, lifecycle mutation, replay, transaction or
runtime self-tuning authority.

### Queued

- M02 K04: implement the accepted canonical public seam and resolve the seven exact production reds.

## 8. Immediate work

Implement bounded M02 K04 Gate D:

1. add the canonical `nvda_desk.m02_financial_calendar` public package only;
2. implement immutable K04 contracts, exact four-layer identity, deterministic snapshot validation and side-effect-free projection;
3. preserve equal-value lineage, explicit operational supersession and fail-closed conflict/absence states;
4. resolve the seven exact production-facing proof cases without weakening the 13 reference/mutant cases;
5. compare affected and full shadow failures against the exact C-PROOF baseline before acceptance.

Do not recreate the retired MLC sequence or create another roadmap.

## 9. Programme sequence

Recommended sequence from the current state:

1. M02 then M03;
2. M05 and M06 when dependencies are ready;
3. M09, M10, M11 and M12;
4. M00 final composition;
5. final alpha consolidation.

M07 and M08 may be completed before M01 if that shortens the critical path to
M05. M05 and M06 may proceed independently after prerequisites. Canonical
integration remains serial where shared files overlap.

## 10. Evidence and controls

Current control surfaces:

- `AGENTS.md`
- `PLANS.md`
- `00_TASK/PROJECT_EXECUTION_METHOD.md`
- this ExecPlan
- `GATE_C_COMPLETION_PROTOCOL.md`
- `ROADMAP_LEDGER_V2.md`
- accepted architecture report/workbook
- existing module records
- existing validation log
- Git

Historical plans, lane briefs, MLC leaf records, receipts and archives remain
inspectable evidence. They do not override this current plan or require repair
merely to preserve history.

## 11. Checkpoint and stop conditions

Stop the active behaviour only when:

- normative meaning is missing or contradictory;
- ownership or dependency direction is unclear;
- proof does not exercise the public seam;
- a required high-consequence independent review is absent;
- the change would invent live, production or operational policy;
- unrelated worktree changes overlap the active write set.

Otherwise continue through the three semantic states without asking for a new
approval at each administrative sub-step.

The programme closes when every accepted module behaviour is implemented or
explicitly rejected/deferred, Atlas and `D-xxx` lineage is retained, admitted
proof and full shadow validation are recorded, dependency/vocabulary/state/
replay boundaries agree, and an explicit alpha checkpoint is published.
