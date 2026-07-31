# NVIDIA 2026 — Canonical Alpha Delivery ExecPlan

## Status

**Status:** `ACTIVE:MVP_FAST_TRACK_M07_GATE_D`
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
- M07 K12 C-PROOF is accepted: 11 reference and false-positive checks pass,
  all five named mutants are killed, the M07 vocabulary boundary is clean and
  seven exact production-facing cases remain red because the canonical public
  package is absent.

### Converted decision

M04 satisfies `C-NORM`, `C-PROOF` and bounded K07 Gate D. The former separate
MLC-V gate remains superseded because it would add another control cycle
without a new semantic claim. No broader M04, live or production-readiness
claim follows from this acceptance.

M01 satisfies `C-NORM`, `C-PROOF` and bounded source-admission Gate D. The
accepted seam is offline, contract-driven, fail-closed and explicitly volatile;
it does not establish live provider connectivity, durable replay, M02 calendar
semantics, M03 preparation or downstream decision authority.

### Queued

- M07: implement the bounded K12 public seam; no generic policy, capital,
  strategy, replay, transaction or downstream-mutation authority is open.
- M08: add the K13 catalogue/eligibility identity, ordering, tie-break,
  stand-down and lifecycle-carriage proposition; then minimum proof.

## 8. Immediate work

Implement the smallest M07 K12 public seam required by the accepted proof:
`PolicyBundle`, `ModifierDecision`, `ModifierApplicationReceipt`, deterministic
bundle resolution and receipt construction. Preserve lawful absence,
authority-owned precedence/conflict, post-algebra hard bounds, deterministic
lineage and the side-effect boundary.

Use the existing M07 module records, validation log and proof registry. Do not
create a generic policy engine, a new roadmap, a receipt hierarchy or another
worker/tester archive pair.

## 9. Programme sequence

Recommended sequence from the current state:

1. M04 K07 Gate D;
2. M01 proof and Gate D;
3. M07 and M08 normative/proof slices;
4. M02 then M03;
5. M05 and M06 when dependencies are ready;
6. M09, M10, M11 and M12;
7. M00 final composition;
8. final alpha consolidation.

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
