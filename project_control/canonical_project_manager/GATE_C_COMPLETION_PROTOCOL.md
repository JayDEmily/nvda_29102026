# NVIDIA 2026 — Canonical Module-Local Gate C Protocol

## Amended status

**Status:** `REPAIRED_PARALLEL_PROTOCOL_R2_AWAITING_INDEPENDENT_CONTROL_RETEST`
**Original global protocol frozen:** `2026-07-25 13:04:09 AEST`
**Strategy amendment accepted:** `2026-07-25`
**Owner:** User and Project Manager thread
**Parent programme plan:** `project_control/canonical_project_manager/EXEC_PLAN.md`
**Live position pointer:** `ROADMAP_LEDGER_V2.md`
**Scope:** module-local normative sufficiency, test authority, proof specification, test implementation, independent validation and final consolidation
**Production implementation:** closed during Cycle 1; later opened only for individually accepted dependency-safe module slices under PM-controlled lanes

This file remains the sole Gate C operating protocol. It no longer requires programme-wide adjudication of all 179 physical tests before any implementation. It establishes proof locally for the active ownership module while preserving the earlier global P2 work as historical evidence.

## One governing rule

> Normative meaning and accepted module ownership define the proof. The admitted proof constrains the active module's code. Test greenness alone establishes neither meaning nor authority.

## 1. Reason for amendment

The original protocol correctly separated observation, semantic judgement, test writing and acceptance. It remained impractical because it applied those operations globally across 179 physical tests before implementation could begin. Two weeks of full-time execution produced substantial evidence but little accepted delivery progress, and repeated long semantic tasks encouraged pattern-based automation rather than reliable contextual judgement.

The user therefore accepted a module-gated strategy:

- each worker handles one ownership module or bounded behaviour; dependency-independent units may occupy separate PM-controlled lanes;
- only tests relevant to each active boundary require immediate authority resolution;
- genuinely absent behaviour receives expected-red proof before implementation;
- unrelated tests remain visible as shadow evidence;
- global reconciliation moves to the final consolidation gate.

This is a scope and scheduling amendment. It does not weaken the normative → test → implementation hierarchy.

## 2. Authority and control surfaces

| Role | Canonical surface | Current meaning |
|---|---|---|
| Direct strategy authority | User acceptance in the Project Manager thread on 25 July 2026 | Supersedes the original brief's global Gate C and fixed-total-order clauses |
| Original programme mandate | `project_control/canonical_project_manager/CANONICAL_PROJECT_MANAGER_EXECUTION_BRIEF.md` | Semantic body preserved with a leading supersession banner and Markdown trailing-whitespace normalisation; source hash retained; scheduling clauses are historical evidence |
| Programme controller | `project_control/canonical_project_manager/EXEC_PLAN.md` | Controls accepted ownership modules, dependency readiness and current unit |
| Gate C protocol | this file | Controls local proof and final test reconciliation |
| Live position | `ROADMAP_LEDGER_V2.md` | Records the current control/module leaf |
| Architecture authority | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`, accepted Atlas architecture artefacts | Defines surfaces, owners, package direction and dependency planes |
| Standing execution law | `AGENTS.md`, `PLANS.md`, applicable overrides | Governs execution and evidence |
| P1 evidence | `PM-001`–`PM-010` records | Preserved accepted prerequisite evidence |
| Physical test census | PM-011, 179 files | Standing inventory; not a global prerequisite |
| Historical global P2 evidence | prior P2 ledgers, receipts, PM-019/PM-020 and sequence adjudications | Navigation and challenge evidence only |
| Historical Gate C/D evidence | `project_control/normative_authority_top_down_alignment/**` | Requirement, proof-envelope, dependency and `D-xxx` traceability evidence |
| Validation record | `project_control/canonical_project_manager/VALIDATION_LOG.md` | Reproducible commands and outcomes |

No receipt, folder location, green test, proof-block membership, workbook row or prior disposition automatically establishes authority.

## 3. Preserved accepted state

- [x] `HIST-001` P1 `PM-001`–`PM-010` remains accepted prerequisite evidence.
- [x] `HIST-002` PM-011 remains the standing 179-test physical census.
- [x] `HIST-003` The prior one-file P2 method remains superseded and available as evidence.
- [x] `HIST-004` The prior bulk P2 candidate and PM-019/PM-020 completion projections remain unaccepted.
- [x] `HIST-005` Earlier positive-admission proposals remain outside authority unless locally reopened and proven.
- [x] `HIST-006` `P2-A01` remains an accepted immutable historical review archive/checkpoint.
- [x] `HIST-007` Prior negative adjudications remain useful non-admission evidence.
- [x] `HIST-008` All 33 historical `D-xxx` records remain traceability obligations.

These preserved items do not keep the former global P2–P4 sequence active.

## 4. Clauses superseded for execution

The following former requirements are no longer active programme prerequisites:

- accepted observation cards for every physical test before any implementation;
- one Project Manager disposition for all 179 files before any module opens;
- proof repair of all eleven historically closed D units before unrelated implementation;
- rebuilding all 33 proof envelopes before any implementation;
- freezing one total D-unit order;
- treating every unreviewed test as a blocker.

They remain historical evidence and may be used during module-local review or final consolidation.

## 5. Non-negotiable constraints

1. No worker self-acceptance.
2. No semantic admission from directory placement, string similarity, registries, hashes or greenness.
3. No production implementation before the active module's local proof gate passes.
4. No weakening tests, norms or vocabulary to make code green.
5. No semantic batching across unrelated behaviours.
6. Mechanical routing and validation may batch; semantic decisions remain bounded.
7. Expected red is lawful when it truthfully proves absent implementation.
8. A local test may govern only its accepted proposition and exercised seam.
9. Unrelated legacy tests run as shadow evidence and do not dictate the active module.
10. Missing meaning returns to normative authority for the active behaviour only.
11. One mutating leaf may be open in each active PM-controlled lane; active lanes must have disjoint ownership and write sets, and no lane may select follow-on work.
12. Canonical acceptance and integration remain sequential and Project Manager controlled.
13. Every acceptance checkbox is Project Manager controlled.

## 6. Current test statuses

The Project Manager may assign these statuses within an active module:

- `ADMIT_TIER_A_CURRENT`
- `ADMIT_TIER_B_SHADOW`
- `BLOCKED_LOCAL_PROOF_REPAIR`
- `BLOCKED_MISSING_NORMATIVE_AUTHORITY`
- `NON_AUTHORITATIVE_OBSERVATIONAL`
- `RETIREMENT_RECOMMENDED_NOT_EXECUTED`
- `NOT_ADMITTED_NO_CURRENT_ROUTE`
- `LEGACY_SHADOW_UNADMITTED`

`LEGACY_SHADOW_UNADMITTED` is the neutral default for an unrelated test whose authority has not been reviewed under the current module. It preserves visibility without granting control.

## 7. Module-local proof gate

Each active module or bounded behaviour completes the following leaves in order. Different dependency-independent modules may occupy different PM-controlled lanes, but each lane contains one leaf only and returns before a later leaf is assigned.

### `MLC-A` — Authority sufficiency

**Question:** Is the required behaviour explicitly governed and owned?

Required record:

- exact normative proposition and locator;
- accepted ownership module and architecture surface;
- input → decision/transformation → output;
- identity, lineage, time, state and side effects;
- prohibited authority;
- mapped Atlas cohorts/records and `D-xxx` obligations, where relevant;
- any missing or contradictory meaning.

Allowed result:

- `AUTHORITY_SUFFICIENT`; or
- `BLOCKED_MISSING_NORMATIVE_AUTHORITY:<exact question>`.

If authority is missing, amend the existing routed normative surface first. Do not write authoritative tests or code from implementation invention.

### `MLC-R` — Relevant-test routing

**Question:** Which physical tests claim authority over the active module or behaviour?

Allowed:

- mechanical joins from PM-011, retained registries, proof blocks, Gate C requirements, `D-xxx` records and source ownership;
- marking unrelated tests `LEGACY_SHADOW_UNADMITTED`.

Forbidden:

- authority selection by filename or location;
- forcing all 179 tests into the active gate.

### `MLC-O` — Factual observation

**Question:** What does each relevant test actually exercise and assert?

Required:

- starting state/input;
- action;
- exact asserted output, mutation, exception or absence;
- exercised public seam;
- surfaces not observed;
- scoped execution result where run.

Observation may cover several tests only when they are demonstrably homogeneous and each file retains a distinct observation.

### `MLC-D` — Test disposition

**Question:** Does each observed test prove an exact accepted proposition for the active module?

Positive admission requires:

- exact assertion locator;
- exact proposition locator;
- what is proved;
- what is not proved;
- proof strength;
- false-positive resistance where material;
- independent Project Manager acceptance.

Safe non-admission requires enough evidence to show that current admission is not established. It does not require an elaborate receipt dossier.

### `MLC-P` — Proof specification

**Question:** What exact proof must exist before implementation opens?

Specify as applicable:

- positive behaviour;
- prohibited behaviour;
- missing mandatory input;
- false-positive resistance;
- identity and lineage;
- time semantics;
- state isolation and atomicity;
- ordering;
- substitution;
- replay;
- architecture boundary/dependency direction.

No test code or production implementation in this leaf.

### `MLC-T` — Test implementation

Implement the accepted proof specification exactly.

Allowed mutation:

- tests;
- explicitly authorised test support;
- normative/vocabulary files only when `MLC-A` already identified and authorised the exact missing meaning.

Forbidden:

- production source;
- broad fixture fabrication;
- weakening proof;
- changing the proposition to fit existing code.

A new test may and often should fail before implementation.

### `MLC-V` — Independent proof validation

The test author cannot provide final acceptance.

Validate:

- the test matches the accepted specification;
- it proves the public seam rather than a fixture or registry artefact;
- it fails or passes for the truthful reason;
- no unrelated authority was introduced;
- the relevant module proof set is sufficient to open implementation.

Allowed result:

- `IMPLEMENTATION_OPEN`; or
- `CLOSED:<exact return gate>`.

### `MLC-I` — Implementation and post-proof

After `IMPLEMENTATION_OPEN`:

1. implement the smallest semantically complete change;
2. run targeted admitted proof;
3. run affected admitted proof;
4. run architecture/dependency checks;
5. run the complete legacy suite as shadow evidence where available;
6. classify shadow failures locally;
7. complete post-change vocabulary review;
8. create one bounded checkpoint.

A shadow failure does not automatically require changing the new code. It triggers a review of the failed test's authority and affected behaviour.

## 8. Missing-feature route

When an active module reveals a feature or policy not covered by normative authority and tests:

```text
candidate feature
→ BLOCKED_MISSING_NORMATIVE_AUTHORITY
→ bounded amendment to the existing routed normative document
→ vocabulary admission if a durable term is new
→ accepted proof specification
→ expected-red test
→ independent validation
→ implementation
```

The active module remains closed only for the affected behaviour. Unrelated dependency-ready modules are not globally blocked.

## 9. `D-xxx` and Atlas treatment

- `D-xxx` IDs remain unchanged and preserve requirement/source/test provenance.
- They are routed beneath accepted module ownership and may be combined or split during module delivery without losing original trace links.
- The 287 cohorts and 1,716 Atlas records remain candidate behavioural evidence unless individually admitted.
- Accepted Atlas architecture allocation governs placement and ownership; it does not admit all Atlas behaviours.
- `M07` means `coefficient_modifier_authority`; the superseded label `policy_authority` must not be used as current ownership authority.
- Missing positive implementation obligations already identified for `M07`, `M09`, `M10` and `M11` must be defined when those modules open.

## 10. Final consolidation gate

Final consolidation occurs only after the module sequence.

Required:

- reconcile all remaining physical tests and historical candidate dispositions;
- compare fresh module decisions against earlier missing-authority candidates;
- confirm every `D-xxx` obligation is satisfied, superseded, rejected or explicitly deferred;
- confirm all accepted Atlas behaviours retain cohort/record traceability;
- run complete admitted Tier A, Tier B shadow and legacy shadow routes;
- run modularity, dependency, substitution, transaction, replay, vocabulary, proof-block and archive checks;
- record `Verified`, `Failed`, `Unknown` and `Blocked` separately;
- make any production, paper, live or operational-readiness decision separately.

Final consolidation must not retroactively legitimise a module that lacked local authority and proof when implemented.

## 11. Evidence economy

Required canonical records:

- this protocol;
- parent ExecPlan;
- live roadmap pointer;
- accepted architecture report/workbook/projections;
- one module-local proof record or existing register update per active module;
- validation log;
- Git commits and checkpoint hashes.

Not required by default:

- one receipt per unrelated physical test;
- one archive per non-admission;
- worker self-review;
- duplicate roadmaps;
- repair of rejected historical paperwork solely to preserve non-admission.

## 12. Worker brief contract

A module-local worker brief must state:

1. exact lane worker label `Lane <number><letter>W`, module/behaviour ID and leaf type;
2. matching tester label `Lane <number><letter>T`;
3. one question;
4. immutable source commit/archive supplied in the PM launch block;
5. exact branch name, read set, write set, dependency gate and shared locks;
6. required reads;
7. exact allowed and forbidden outputs;
8. validation and one returned candidate archive;
9. return condition and no follow-on selection;
10. Project Manager acceptance remains pending.

The matching tester brief must require independent reconstruction, ancestry and scope checks, semantic falsification appropriate to the leaf, one of `PASS`, `FAIL_REPAIRABLE` or `HARD_BLOCK`, and one tester-approved archive on PASS. Tester PASS means suitable for PM integration review only.

A worker brief fails if it combines factual observation, semantic judgement, proof specification, test writing, independent validation and implementation into one uncontrolled task.

## 13. Change control

This amended protocol may change only when:

- the user explicitly changes strategy;
- measured execution shows a local leaf is still too large or unsafe;
- the parent ExecPlan changes the objective; or
- a contradiction prevents truthful work.

Any amendment must preserve accepted evidence, state the measured defect, identify changed clauses, and update the parent ExecPlan and live roadmap in the same control change.


## 14. Current parallel cycle

**Control disposition:** `ACCEPTED:PARALLEL_CONTROL_R2_WORKER_LAUNCH_OPEN`.

The accepted M01 authority decision remains unchanged. `Parallel Control T1` returned PASS at tester commit `e672b27ca01efbd1f47de27d41fa54733bc73c63`, and the Project Manager independently accepted the tested control package. Four dependency-independent Cycle 1 proof leaves are open for worker launch from one PM-published immutable checkpoint:

| Lane pair | Unit | Mutation boundary |
|---|---|---|
| `Lane 1AW` / `Lane 1AT` | `M01-PROOF-MLC-R-V1` | one M01 routing record and lane-owned evidence only |
| `Lane 2AW` / `Lane 2AT` | `M04-PROOF-MLC-A-V1` | one M04 authority record and lane-owned evidence only |
| `Lane 3AW` / `Lane 3AT` | `M07-PROOF-MLC-A-V1` | one M07 authority record and lane-owned evidence only |
| `Lane 4AW` / `Lane 4AT` | `M08-PROOF-MLC-A-V1` | one M08 authority record and lane-owned evidence only |
| Lanes 5 and 6 | held | no dependency-safe additional semantic unit |

Cycle 1 production source, physical tests, configuration, normative documents, vocabulary registries, proof registries and global PM controls remain closed to all lane workers and lane testers. The control repair alone lawfully admits M15 workflow vocabulary and updates programme controls. Each lane tester reviews only its matching worker. The PM integrates any accepted results one at a time in the order M01, M04, M07, M08 and runs aggregate validation before publishing the next canonical checkpoint.

**Immediate gate:** publish the accepted full-history worker-launch checkpoint and issue the four exact worker briefs. Create a lane tester only after its matching worker returns.

No lane may begin `MLC-O`, `MLC-R` for another module, proof design, test mutation, implementation or a `B` assignment until the PM issues a new brief from an appropriate canonical checkpoint.
