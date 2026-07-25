# NVIDIA 2026 — Canonical Gate C Completion Protocol

## Frozen status

**Status:** `FROZEN_CANONICAL_GATE_C_PROTOCOL`
**Frozen at:** `2026-07-25 13:04:09 AEST`
**Owner:** User and Project Manager thread
**Parent programme plan:** `project_control/canonical_project_manager/EXEC_PLAN.md`
**Live position pointer:** `ROADMAP_LEDGER_V2.md`
**Scope:** remaining P2 test-authority reconciliation, P3 proof repair and P4 proof-envelope/order freeze
**Gate D:** closed

> **Sole operational checklist:** This file is the only checklist to follow for the remaining Gate C work. The parent ExecPlan governs the programme and `ROADMAP_LEDGER_V2.md` records the current position. Checkpoints, ledgers, receipts, reports, manifests and archives are supporting evidence only; they are not separate plans or additional checklists.

This document is the canonical operating protocol for completing Gate C. It is subordinate to the parent programme ExecPlan and does not replace the programme mandate, normative authority or live roadmap pointer.

It replaces the failed **execution method** of requiring one worker to perform a complete file adjudication, attack its own reasoning, write audit-perfect receipts, update ledgers and certify the package. It does not erase that work. Prior P2 receipts, matrices, registers and archives remain evidence and navigation material only until accepted under this protocol.

## One governing rule

> One worker performs one kind of reasoning about one bounded relationship. The Project Manager alone accepts semantic decisions. Mechanical workers only project accepted decisions.

## 1. Why this protocol exists

The programme made real progress, but the one-file P2 method repeatedly overloaded workers with three distinct jobs:

1. understand the test and exercised behaviour;
2. select and adversarially assess semantic authority; and
3. produce, integrate and validate a legally complete evidence package.

Measured results from the recovery and sequence adjudications show:

- workers often identified the correct safe direction;
- workers were substantially less reliable when required to audit their own reasoning;
- elaborate claim matrices created new failure surfaces unrelated to the architectural decision;
- positive-admission proposals were systematically over-optimistic;
- negative conclusions were repeatedly trapped in receipt-repair loops even though the safe architectural result was already non-admission;
- semantic-family work in P1 was more reliable because the worker stayed within one coherent reasoning class and integration was separate;
- prior Gate C normative units were more reliable when one accepted proposition preceded one proof boundary.

This protocol therefore uses **asymmetric escalation**:

- admission requires affirmative, independently accepted proof;
- non-admission requires enough evidence to show that current admission has not been established;
- a failed or defective positive-admission case cannot promote a test and does not require endless repair merely to keep it outside current authority.

## 2. Authority and control surfaces

Read and apply these surfaces in order.

| Role | Canonical surface | Meaning under this protocol |
|---|---|---|
| Programme mandate | `ATTACHMENT:CANONICAL_PROJECT_MANAGER_EXECUTION_BRIEF(1).md` | Defines the required P1 → P2 → P3 → P4 → Gate D outcome and the thirty-three-unit implementation programme. |
| Programme controller | `project_control/canonical_project_manager/EXEC_PLAN.md` | Single live programme ExecPlan above this protocol. |
| Gate C operating protocol | `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md` | This frozen method and shared checklist for P2–P4. |
| Live position | `ROADMAP_LEDGER_V2.md` | Records the current accepted leaf and next gate; it does not invent decisions. |
| Standing execution law | `AGENTS.md`, `PLANS.md`, applicable overrides, `ATTACHMENT:PROJECT_EXECUTION_METHOD.md` and `00_TASK/PROJECT_EXECUTION_METHOD.md` | Governs how work is performed; not programme progress. |
| P1 accepted sequencing | `project_control/canonical_project_manager/PM-001_TO_PM-010_WORKER_TABLE.md` | Preserved P1 unit allocation and accepted prerequisite structure. |
| Retired live pointer | `ROADMAP_LEDGER.md` | Tombstone that routes away from the retired roadmap; not current status. |
| P2 physical census | `project_control/canonical_project_manager/units/PM-011/P2_PHYSICAL_TEST_CENSUS.tsv` | Standing 179-file inventory and hashes. |
| P2 row-level state | `project_control/canonical_project_manager/P2_ABSOLUTE_SEMANTIC_READ_LEDGER.tsv` | Existing master row ledger. Historical `SEMANTICALLY_READ=YES` means a worker claimed completion, not Project Manager acceptance. |
| Earlier P2 method | `00_TASK/NVDA_P2_CLEAN_WORKER_SEMANTIC_REVIEW_EXEC_PLAN_20260722.md` | Superseded for execution; retained as failed-method evidence, inventory and constraints. |
| Earlier P2 candidate projections | `project_control/canonical_project_manager/units/PM-019/**` | Rejected candidate evidence. Must be rebuilt only from decisions accepted under this protocol. |
| Prior Gate C authority | `project_control/normative_authority_top_down_alignment/GATE_C_TEST_AUTHORITY_REGISTER.tsv` | Existing requirement-to-test routes to revalidate, not automatic current admission. |
| Prior Gate C requirements | `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv` | Requirement inventory and intended behaviours. |
| Closed P3 units | `project_control/normative_authority_top_down_alignment/GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv` | Exact eleven units and return gates. |
| Proof envelopes | `project_control/normative_authority_top_down_alignment/GATE_C2_PROOF_ENVELOPE_REGISTER.tsv` and envelope files | Historical proof state to be reissued at P4. |
| Prior Gate C summary | `project_control/normative_authority_top_down_alignment/GATE_C_EXECUTION_SUMMARY.md` | Historical Gate C execution summary; evidence only under the canonical programme. |
| Gate A–D chronology | `project_control/normative_authority_top_down_alignment/PROGRESS_LEDGER.md` | Historical gate record; does not schedule current work. |
| Gate D backlog/readiness | `project_control/normative_authority_top_down_alignment/GATE_D_IMPLEMENTATION_BACKLOG.tsv`, `project_control/normative_authority_top_down_alignment/GATE_D_READINESS_REPORT.md` | Historical evidence only until P4 re-freezes all thirty-three units. |
| Assembly snapshot | `CURRENT_PROJECT_STATE.md` | Historical assembly state; not current programme status. |
| Validation record | `project_control/canonical_project_manager/VALIDATION_LOG.md` | Reproducible control and validation evidence. |

No receipt, register, worker archive, green test, folder placement or generated prose can override this hierarchy.

## 3. Current accepted starting state

These checkboxes record the state accepted when this protocol was frozen.

- [x] `GC-000` Parent canonical programme remains `project_control/canonical_project_manager/EXEC_PLAN.md`.
- [x] `GC-001` P1 `PM-001`–`PM-010` is preserved as the accepted prerequisite.
- [x] `GC-002` PM-011 remains the standing 179-test physical census.
- [x] `GC-003` The prior one-file P2 method is stopped and retained as evidence, not governing execution.
- [x] `GC-004` The prior bulk P2 candidate, recovery receipts and PM-019/PM-020 outputs are not accepted as P2 completion.
- [x] `GC-005` Proposed positive sequences `071`, `078`, `087`, `090`, `091`, `092` and `094` do not enter current test authority merely from their worker returns.
- [x] `GC-006` Sequences `071` and `087` have accepted negative adjudications: not admitted and returned to P3 repair.
- [x] `GC-007` Sequences `078`, `090`, `091`, `092` and `094` remain not admitted because their positive admission was not established and their returned evidence was rejected.
- [x] `GC-008` P2 remains incomplete; P3, P4 and Gate D remain closed.
- [x] `GC-009` This protocol is frozen as the canonical method for finishing Gate C.

## 4. Non-negotiable operating constraints

1. **No production implementation during Gate C.** `src/**`, production configuration and runtime behaviour remain read-only unless the parent ExecPlan is explicitly amended.
2. **No worker self-acceptance.** Workers propose observations or relationships. The Project Manager accepts or rejects them.
3. **No semantic batching.** Mechanical inventory and projection may batch. Semantic judgement may not.
4. **No mandatory receipt per physical file.** The existing row ledger is the master record. Detailed standalone evidence is required only for accepted positive relationships, genuinely contested decisions or explicit return-gate specifications.
5. **No automatic admission.** Folder location, historical registry membership, test greenness, proof-block membership and prior receipt status do not establish current authority.
6. **No repair tennis for safe non-admission.** A rejected positive case remains outside authority. Repair it only when the test is required for the Gate C critical path or the Project Manager explicitly reopens it.
7. **No prior-disposition contamination in fresh semantic leaves.** Fresh workers receive clean source and authority, not previous conclusions.
8. **No worker programme conclusions.** Workers cannot open P3, P4 or Gate D.
9. **One open mutating unit.** Mechanical aggregation waits for accepted semantic decisions.
10. **Every checkbox is Project Manager controlled.** A worker may return evidence but may not tick this canonical checklist.

## 5. Leaf taxonomy

Each worker brief must name exactly one leaf type.

### `R` — Mechanical routing leaf

**Question:** Where does each test currently route mechanically?

Allowed:

- hashes, paths, existing requirement IDs, proof-block IDs, retained-registry routes, D-unit routes and census joins.

Forbidden:

- authority selection, proof-strength judgement, disposition or semantic acceptance.

Normal size: many rows where the operation is deterministic.

### `O` — Observation leaf

**Question:** What does this exact test actually do and observe?

Required output:

- starting state/input;
- action performed;
- exact asserted outputs, mutations, exceptions or absences;
- directly exercised surfaces;
- surfaces not observed;
- scoped test result.

Forbidden:

- normative proposition selection;
- tier or disposition decision;
- ledger mutation;
- self-audit or programme conclusion.

Normal size: one test. Maximum three only when the Project Manager establishes that the files are homogeneous and independent observation cards are returned.

### `S` — Conservative screening leaf

**Question:** Does the observation card expose a plausible exact current authority route?

Allowed results:

- `NO_PLAUSIBLE_CURRENT_ROUTE`;
- `PLAUSIBLE_ROUTE:<proposition-id>`;
- `UNCERTAIN_ROUTE:<bounded-question>`.

This is triage, not admission. A `NO_PLAUSIBLE_CURRENT_ROUTE` result permits current non-admission after Project Manager acceptance.

### `A` — Authority-relationship leaf

**Question:** Does one observed assertion surface prove one exact normative proposition or bounded separable clause?

Input is limited to:

- one accepted observation card;
- one exact proposed proposition and full authority context;
- the exact test/assertion and directly exercised surface needed for verification.

Required output:

1. test/assertion locator;
2. proposition and authority locator;
3. `yes`, `bounded_part` or `no`;
4. proof strength;
5. what is proved;
6. what is not proved;
7. decisive reason.

A formal falsifier is required only when the Project Manager asks for it to resolve a real positive-admission ambiguity. It is not mandatory bureaucracy for every negative result.

Normal size: exactly one test-observation ↔ one proposition relationship.

### `D` — Project Manager disposition leaf

**Question:** Given all accepted relationships for one physical test, what is its current file disposition?

Only the Project Manager may decide:

- `ADMIT_TIER_A_CURRENT`;
- `ADMIT_TIER_B_SHADOW`;
- `BLOCKED_P3_REPAIR`;
- `BLOCKED_MISSING_NORMATIVE_AUTHORITY`;
- `NON_AUTHORITATIVE_OBSERVATIONAL`;
- `RETIREMENT_RECOMMENDED_NOT_EXECUTED`;
- `NOT_ADMITTED_NO_CURRENT_ROUTE`.

### `P` — P3 proof-specification leaf

**Question:** What exact behavioural proof must exist for one frozen proposition and one closed D unit?

Required cases, where applicable:

- positive behaviour;
- prohibited behaviour;
- false-positive resistance;
- missing mandatory input;
- identity/lineage;
- state isolation;
- substitution;
- replay.

No test code or production implementation.

### `T` — P3 test-implementation leaf

**Question:** Does the worker implement the accepted proof specification exactly?

Allowed mutation: tests and explicitly authorised test support only.

Forbidden:

- changing the proposition;
- weakening the proof specification;
- production implementation;
- turning expected red into green by modifying authority.

### `V` — Independent validation leaf

**Question:** Does the returned test match the accepted proof specification and fail/pass for the truthful reason?

Owned by the Project Manager or an explicitly independent audit worker. It cannot be performed by the test author as final acceptance.

### `M` — Mechanical projection leaf

**Question:** Were accepted decisions copied exactly into existing ledgers, registers, proof envelopes and configuration projections?

No semantic text may be invented during this leaf.

## 6. P2 completion checklist

### Phase P2-A — Clean review source

- [ ] `P2-A01` Create one immutable review archive from the current accepted checkpoint.
- [ ] `P2-A02` Include tests, directly exercised source, normative documents, accepted P1 registers, PM-011, retained registry, proof blocks, Gate C requirements/authority and proof-envelope records.
- [ ] `P2-A03` Exclude prior P2 semantic receipts, candidate dispositions, sequence conclusions, rejected PM-019 projections and rejected PM-020 completion claims from fresh worker inputs.
- [ ] `P2-A04` Record archive SHA-256, Git branch/HEAD, safe extraction and read-only worker rule.
- [ ] `P2-A05` Project Manager accepts the review source.

**Pass:** one reproducible uncontaminated source exists.
**Fail:** fresh workers can see prior semantic conclusions or the source does not reproduce PM-011 hashes.

### Phase P2-B — Mechanical routing

- [ ] `P2-B01` Route all 179 PM-011 tests to existing Gate C requirement IDs, retained-registry routes, proof blocks, D units and the eleven closed P3 units where such routes already exist.
- [ ] `P2-B02` Mark tests with no existing route without inventing one.
- [ ] `P2-B03` Divide the population into `INCUMBENT_ROUTED`, `PLAUSIBLE_UNADMITTED` and `UNROUTED`.
- [ ] `P2-B04` Amend the existing P2 ledger schema so worker activity, Project Manager audit and current admission are distinct fields.
- [ ] `P2-B05` Preserve historical receipt paths and worker states without treating them as accepted authority.
- [ ] `P2-B06` Project Manager validates the routing and ledger migration.

**Pass:** every physical test occurs once and deterministic routes resolve.
**Fail:** routing requires semantic inference or any test disappears/duplicates.

### Phase P2-C — Observation cards

- [ ] `P2-C01` Complete accepted observation cards for all incumbent-routed tests.
- [ ] `P2-C02` Complete observation cards for plausible unadmitted tests.
- [ ] `P2-C03` Complete only the observation needed to support conservative screening for unrouted tests.
- [ ] `P2-C04` Confirm that observation workers made no authority, tier or disposition decisions.

**Pass:** every test has enough accepted factual observation to support screening or relationship review.
**Fail:** an observation card relies on filenames, imports, summaries or unverified prior receipts rather than the test and exercised surface.

### Phase P2-D — Conservative screening

- [ ] `P2-D01` Screen every observation card for a plausible exact current authority route.
- [ ] `P2-D02` Close `NO_PLAUSIBLE_CURRENT_ROUTE` files as current non-admission after Project Manager review.
- [ ] `P2-D03` Escalate only exact plausible or uncertain relationships.
- [ ] `P2-D04` Confirm that no file is escalated merely because it is in `tests/tier_a`, a retained registry or a proof block.

**Pass:** deep semantic review is limited to credible admission questions.
**Fail:** all files are forced through full adjudication or a test is admitted by historical metadata.

### Phase P2-E — Relationship adjudication

- [ ] `P2-E01` Complete one `A` leaf for every escalated test-observation ↔ proposition relationship.
- [ ] `P2-E02` Independently review every proposed positive Tier A relationship.
- [ ] `P2-E03` Independently review every proposed positive Tier B relationship.
- [ ] `P2-E04` Reject or narrow any relationship whose worker combines multiple propositions or proof obligations.
- [ ] `P2-E05` Confirm prior worker conclusions were not supplied to fresh relationship workers.

**Pass:** every positive relationship has exact accepted authority and bounded proof strength.
**Fail:** a worker self-accepts, bundles unrelated propositions or relies on green tests/metadata.

### Phase P2-F — File dispositions

- [ ] `P2-F01` Project Manager decides one current disposition for each of 179 physical tests.
- [ ] `P2-F02` Record `CURRENT_ADMISSION` separately from worker/read state.
- [ ] `P2-F03` Record concise non-admission reasons without manufacturing receipt dossiers.
- [ ] `P2-F04` Record exact P3 return gates only where the test is required by the Gate C critical path.
- [ ] `P2-F05` Confirm all seven previously proposed positive candidates remain outside authority unless reopened and affirmatively proven under this protocol.

**Pass:** 179 unique PM-accepted dispositions.
**Fail:** any unresolved row, implicit admission or worker-owned acceptance.

### Phase P2-G — Mechanical projection and validation

- [ ] `P2-G01` Rebuild PM-019 registers only from PM-accepted dispositions.
- [ ] `P2-G02` Update retained registry and proof blocks only as exact mechanical projections of accepted decisions.
- [ ] `P2-G03` Run one-to-one census, locator, authority, count and projection validation.
- [ ] `P2-G04` Run applicable Tier A, Tier B and Gate C proof routes without suppression.
- [ ] `P2-G05` Record `Verified`, `Failed`, `Unknown` and `Blocked` separately.
- [ ] `P2-G06` Project Manager performs final P2 acceptance review.
- [ ] `P2-G07` Mark P2 accepted and open P3 only after the Project Manager signs the combined baseline.

**P2 completion gate:** every current test has one PM-accepted disposition; every admitted relationship has exact authority and honest proof strength; P2 projections reproduce those decisions exactly.

## 7. P3 completion checklist — eleven closed units

For each unit, complete the leaves in order: authority sufficiency → proof specification → test implementation → independent validation. Production source remains read-only.

| Unit | Existing return gate | Authority sufficiency | Proof specification | Test implementation | Independent validation | PM accepted |
|---|---|---:|---:|---:|---:|---:|
| `D-009 / C-009` | Gate C1 behavioural proof enrichment | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-012 / C-012` | Gate C1 behavioural proof enrichment | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-015 / C-015` | Gate C1 behavioural proof enrichment after D-012 | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-010 / C-010` | Gate C2 test-authority reconciliation | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-016 / C-016` | Gate C2 after D-010 and D-015 | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-033 / C-033` | Gate C1 behavioural proof enrichment | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-017 / C-017` | Gate C2 test-authority reconciliation | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-031 / C-031` | Gate C2 test-authority reconciliation | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-021 / C-021` | Gate C2 test-authority reconciliation | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-048 / C-048` | Gate C2 test-authority reconciliation | [ ] | [ ] | [ ] | [ ] | [ ] |
| `D-041 / C-041` | Gate C2 after D-048 | [ ] | [ ] | [ ] | [ ] | [ ] |

P3 rules:

- one D unit at a time in dependency-safe order;
- the authority sufficiency decision is Project Manager owned;
- proof-specification workers receive frozen authority, not the whole programme;
- test implementers may not change production source;
- expected red is lawful where it truthfully exposes the implementation gap;
- the test author cannot provide final independent validation;
- a unit closes only after the Project Manager accepts the full authority → specification → test → validation chain.

## 8. P4 completion checklist

P4 is a projection and freeze stage, not a new semantic review.

- [ ] `P4-001` Confirm P2 is accepted.
- [ ] `P4-002` Confirm all eleven P3 units are accepted.
- [ ] `P4-003` Rebuild all thirty-three proof envelopes from accepted P2/P3 authority.
- [ ] `P4-004` Assign exactly one current status to every D unit: `implementation_executable_now` or `closed` with an exact return gate.
- [ ] `P4-005` Rebuild the dependency map and fixed total implementation order.
- [ ] `P4-006` Validate that all thirty-three units occur exactly once.
- [ ] `P4-007` Validate that no rejected test, stale receipt or historical admission re-enters by projection.
- [ ] `P4-008` Freeze proof envelopes, dependency order and current Gate D backlog.
- [ ] `P4-009` Project Manager accepts the Gate C combined baseline.
- [ ] `P4-010` Record the explicit Gate D opening decision.

**Gate C completion gate:** P1–P4 are accepted; all 179 tests have current dispositions; all eleven closed proof units have truthful proof authority; all thirty-three proof envelopes and the fixed implementation order are frozen; Gate D opening is an explicit separate decision.

## 9. Evidence economy and canonical recording

The purpose of evidence is to support decisions, not multiply documents.

### Required canonical records

- this checklist and protocol;
- `ROADMAP_LEDGER_V2.md` for the current leaf;
- the amended P2 row ledger for per-test worker/audit/admission state;
- accepted relationship records for positive or contested relationships;
- the existing P3 proof-envelope and D-unit registers;
- `VALIDATION_LOG.md` for commands and reproducible checks;
- Git commits and checkpoint hashes.

### Not required by default

- one standalone Markdown receipt per physical test;
- one archive per negative decision;
- one self-review per worker;
- one formal falsifier for an uncontested non-admission;
- repair of rejected worker paperwork solely to preserve non-admission;
- duplicate roadmaps or recovery-status documents.

Existing receipts remain available as historical evidence and navigation material. They do not need to be deleted or repaired unless reused for an accepted decision.

## 10. Worker brief contract

Every worker brief under this protocol must state:

1. leaf ID and leaf type;
2. one exact question;
3. immutable source archive and hash;
4. exact required reads;
5. exact allowed outputs;
6. exact forbidden decisions and mutations;
7. validation required;
8. return condition;
9. no follow-on selection;
10. Project Manager acceptance remains pending.

A worker brief fails before execution if it asks the worker to perform more than one of:

- factual observation;
- semantic relationship judgement;
- proof specification;
- test implementation;
- independent validation;
- mechanical projection.

## 11. Progress update rule

Only the Project Manager may update this checklist.

After an accepted leaf or phase:

1. tick the exact checkbox here;
2. update the current unit and next gate in `ROADMAP_LEDGER_V2.md`;
3. update the relevant existing row/register;
4. append reproducible validation evidence to `VALIDATION_LOG.md`;
5. create one bounded Git checkpoint where appropriate.

Do not create another roadmap, recovery status or master checklist.

## 12. Change control

This protocol is frozen.

It may change only when:

- the user explicitly changes the strategy;
- a concrete measured failure shows that one leaf remains too large or unsafe;
- the parent canonical ExecPlan changes the Gate C objective or authority; or
- a contradiction prevents truthful execution.

Any amendment must:

- preserve completed checkboxes and accepted evidence;
- state the measured defect;
- identify the exact clauses changed;
- avoid silently reopening Gate D;
- update the parent ExecPlan and live roadmap pointer in the same bounded governance change.

## 13. Current next leaf

**Next leaf:** `P2-A01` — create the immutable uncontaminated Gate C review archive.

No semantic worker should be dispatched until `P2-A01` through `P2-A05` pass.
