# Kinenical / NVIDIA 2026 Canonical Delivery ExecPlan

## Status

`parallel_cycle_01_allocated_awaiting_worker_launch`

The user accepted the extended architecture review on 25 July 2026 and replaced the global Gate C certification route and fixed `D-xxx` total order with dependency-ready ownership-module delivery. On 28 July 2026 the user explicitly authorised a six-lane PM-controlled parallel workflow with independent worker/tester pairs and serial canonical integration. This remains one programme and one repository.

| Field | Current value |
|---|---|
| Plan owner | Project Manager thread |
| Original programme activated | 2026-07-20 (Australia/Melbourne) |
| Strategy amendments accepted | 2026-07-25 and 2026-07-28 (Australia/Melbourne) |
| Accepted control-integration checkpoint | local `main` at `b153cd1e3e0808991dcf9c188e380d935cfd9283` |
| Current branch | `control/parallel-workflow-enablement-v1` |
| Architecture | Governed modular monolith |
| Maturity | Alpha / `thin_seam`; no production, live-trading, paper-trading, durability or end-to-end completion claim |
| Accepted architecture surfaces | 18, sections 5.1–5.18 of the native blueprint |
| Accepted ownership modules | 16, `M00`–`M15` |
| Historical implementation obligations | 33 `D-xxx` records retained for traceability |
| Accepted M13 worker commit | `616fade4123def7870b7950bb3e644ffcc0ccc5a` |
| M01 authority PM closeout branch | `review/m01-authority-v1` |
| Active units | Cycle 1: `1A M01-MLC-R`, `2A M04-MLC-A`, `3A M07-MLC-A`, `4A M08-MLC-A`; Lanes 5 and 6 held |
| Mutation state | Cycle 1 is proof/control evidence only; each lane may change only its declared module record/evidence paths; source, tests, configuration, normative/vocabulary and global PM controls remain locked |
| First implementation module after proof acceptance | `M13 state_kernel` |
| Gate D | module-local only; dependency-safe slices may be worked in parallel after their own proof opens, but PM acceptance and integration remain serial |

## Objective

Deliver the alpha as a sequence of small, semantically complete, dependency-ready ownership modules. For each active module, establish exact normative authority and trustworthy local proof before changing its implementation. Preserve useful code and evidence, replace defective architecture seams, and avoid both a big-bang rewrite and a global test-certification programme that blocks unrelated implementation.

The required direction remains:

```text
normative meaning
→ governed vocabulary and accepted target ownership
→ module-local admitted proof
→ implementation
→ evidence and checkpoint
```

A passing test does not establish authority. An admitted test constrains implementation only after its relationship to governing meaning has been accepted.

## Authority

Apply authority in this order:

1. direct user instruction and explicit acceptance in the Project Manager thread;
2. the accepted canonical Project Manager brief and the user-approved 25 July 2026 strategy amendment recorded in this plan;
3. applicable `AGENTS.override.md` and repository-root `AGENTS.md`;
4. this ExecPlan, its live pointer `ROADMAP_LEDGER_V2.md`, and the active module-local proof protocol;
5. routed normative documents, accepted architecture allocations, governed vocabulary and approved specifications;
6. module-local admitted tests and proof authority;
7. source, configuration, schemas, fixtures and data;
8. ledgers, receipts, reports, manifests, generated projections and historical evidence;
9. `00_TASK/PROJECT_EXECUTION_METHOD.md` where higher authority is silent.

The original uploaded brief is preserved by source SHA-256 `43be514d3633651df5d404ee68e9741a879d4a4a6cf0da6dcbe2f40589f68bc8`. The repository copy at `project_control/canonical_project_manager/CANONICAL_PROJECT_MANAGER_EXECUTION_BRIEF.md` adds a leading control-status banner and normalises Markdown trailing whitespace only; its semantic body remains unchanged. Its execution-sequencing clauses are expressly superseded by the user's accepted amendment.

## Strategy amendment

### Preserved

- P1 `PM-001`–`PM-010` remains accepted prerequisite evidence.
- PM-011 remains the standing census of 179 physical tests.
- `P2-A01` remains an accepted immutable historical review archive and checkpoint.
- All earlier Gate A, Gate B, Gate C, Gate D, Atlas, vocabulary, proof-envelope, test, receipt and adjudication artefacts remain inspectable evidence.
- The 18 architecture surfaces, modular-monolith law, alpha status, owner separation, no-fabrication law, DMPV3 identity distinctions, serial/Parallel Risk separation and normative → test → code authority direction remain binding.
- All 33 `D-xxx` identifiers and their requirement/source/test links remain unchanged as traceability obligations.

### Superseded for execution control

- Global adjudication of all 179 physical tests before any production implementation.
- Mandatory completion of the former P2 → P3 → P4 sequence as a programme-wide Gate D prerequisite.
- The requirement that every `D-xxx` record become one standalone implementation branch.
- The fixed total order `D-001` through `D-057`.
- The prior Atlas blocker that stated the 287-cohort register was absent. The accepted architecture package now contains 287 cohorts and 1,716 records with mechanical trace validation.
- Historical `implementation_executable_now`, `closed`, or immediately-executable labels as current scheduling authority.

### Reason

Two weeks of full-time work demonstrated that global per-test semantic certification is economically incompatible with reliable model behaviour. The accepted replacement preserves semantic authority by reducing each worker's reasoning surface to one ownership module or one bounded behaviour inside that module. The later parallel amendment changes scheduling width, not unit size.


## Parallel workflow amendment — 28 July 2026

The Project Manager operates six permanent capacity lanes. Lanes are scheduling identifiers, not module ownership and not long-lived branches. Each assignment uses one disposable worker thread, one independent tester thread and one fresh branch from a named canonical checkpoint.

Thread labels are exact:

- worker: `Lane <number><assignment-letter>W`;
- tester: `Lane <number><assignment-letter>T`.

Cycle 1 uses `Lane 1AW/1AT`, `2AW/2AT`, `3AW/3AT` and `4AW/4AT`. Lanes 5 and 6 are held.

Parallel work is lawful only when the PM registry records:

- one semantic leaf or bounded implementation slice;
- runtime prerequisites;
- exact read and write sets;
- contract owner and test-file locks;
- global locked surfaces;
- common canonical archive/base commit;
- worker and tester branches;
- stale-base and integration-conflict treatment.

Workers and testers do not update the ExecPlan, roadmap, workflow registry, numbered normative documents, vocabulary/proof registries, root packaging or composition surfaces. They return one archive and stop. Tester PASS means `SUITABLE_FOR_PM_INTEGRATION_REVIEW`; it does not canonicalise the result.

The PM verifies and imports one tester-approved assignment at a time, in a declared queue order, reruns targeted/affected/governance checks, records the integration decision, then runs aggregate validation and publishes one new full-history checkpoint.

No lane-local continuation on unintegrated work is permitted during the pilot.

## Four-map model

| Map | Canonical meaning |
|---|---|
| Behavioural spine | End-to-end product function from external information through preparation, cognition, risk, capital, execution, lifecycle and review |
| Architecture surfaces | The 18 governed responsibility and review boundaries |
| Ownership modules | The 16 bounded code capabilities `M00`–`M15` |
| Implementation obligations | Existing `D-xxx` requirement/proof/source links and any bounded positive obligation added when an active module exposes a real coverage gap |

A surface is not necessarily a package. A module may serve several surfaces. A `D-xxx` record is a traceability obligation, not automatically a branch, package or full feature.

## Accepted ownership modules

| ID | Accepted name | Primary ownership | Current-code strategy |
|---|---|---|---|
| `M00` | `application_shell` | transport translation, dependency composition and run lifecycle; no business truth | rebuild composition shell |
| `M01` | `source_admission` | source identity, raw capture, source time and raw-signal registration | replace boundary; retain selected validation kernels |
| `M02` | `calendar` | four calendar layers, fact coalescence, supersession and runtime projection | retain reference algorithms; rebuild state/composition |
| `M03` | `preparation` | typed prepared envelope, field resolution and enrichment gaps | rebuild core; retain deterministic transformations |
| `M04` | `packet_protocol` | DMPV3 envelope validation and deliberate packet carriage only | retain envelope shape; replace fabricated defaults |
| `M05` | `serial_cognition` | ordered candidate-forming stages and stage-local carriers | retain stage order/selected classifiers; rebuild orchestration |
| `M06` | `parallel_risk` | independent environmental risk lane and final-risk contribution | retain bounded evaluators; rebuild composition/state |
| `M07` | `coefficient_modifier_authority` | versioned coefficients, modifiers, precedence and application receipts | refactor and narrow; not generic policy ownership |
| `M08` | `playbook_catalogue` | playbook definitions, catalogue and eligibility semantics | refactor behind catalogue contract |
| `M09` | `capital_authority` | final-risk join, pre-deployment gate, bounded sizing and capital decision | retain calculations; rebuild join/state boundary |
| `M10` | `execution_gateway` | opening readiness, placement intent, broker protocol and execution events | replace boundary and alpha adapters |
| `M11` | `portfolio_lifecycle` | fills, positions, inventory, carry, exit and close lifecycle | retain policy kernels; rebuild canonical state ownership |
| `M12` | `evidence_replay` | review projections, explanation, comparison and authoritative replay | retain read-only projections; rebuild replay core |
| `M13` | `state_kernel` | unit-of-work, idempotency, atomic state/receipt commit and storage ports | rebuild core |
| `M14` | `proof_promotion` | proof manifests, tier classification, checkpoints and promotion | governance plane; retain/refactor |
| `M15` | `vocabulary_governance` | durable term admission, canonical registry and projections | governance plane; retain/refactor |

No top-level split or merge is accepted. `M07 policy_authority` is superseded by `M07 coefficient_modifier_authority` because system-wide policy remains owned by the relevant domain modules.

## Dependency planes

Dependencies must be recorded separately.

| Plane | Meaning | Graph use |
|---|---|---|
| Runtime/contract | production call or consumed public contract | defines dependency readiness and runtime acyclicity |
| State/transaction participation | domain-owned state participates in `M13` transaction mechanism | does not transfer semantic ownership to `M13` |
| Governance/promotion | `M14`/`M15` proof and vocabulary prerequisites | acceptance control only, not a production import requirement |
| Build/test | fixtures, proof runners, schema generators and developer tooling | development only |

Accepted runtime/contract graph:

| Module | Dependencies |
|---|---|
| `M01` | none |
| `M02` | `M01` |
| `M03` | `M01`, `M02` |
| `M04` | none |
| `M05` | `M03`, `M04`, `M07`, `M08` |
| `M06` | `M03`, `M04` |
| `M07` | none |
| `M08` | none |
| `M09` | `M05`, `M06`, `M07` |
| `M10` | `M09` |
| `M11` | `M10` |
| `M12` | `M04` plus read-only evidence-export contracts |
| `M13` | none |

`M00` composes modules and is omitted from the domain dependency graph. `M14` and `M15` are governance prerequisites, not runtime dependencies. `M08 → M07` is not an accepted runtime dependency.


## Scope

### Current control amendment

In scope:

- reconcile the standing serial controls with the user-authorised PM-controlled parallel workflow;
- route the accepted parallel workflow and PM registry;
- establish exact lane/thread/branch naming;
- define dependency, read/write, contract-owner, test-file, stale-base and global locks;
- allocate and brief Cycle 1 Lanes 1A–4A;
- hold Lanes 5 and 6 explicitly;
- create four standalone worker briefs and four independent tester briefs;
- validate that no source, physical test, runtime configuration, normative-domain meaning, proof registry or vocabulary registry changed;
- create one control-only commit and Git-preserving archive.

Out of scope:

- executing any lane assignment;
- source, test, production configuration, fixture or runtime mutation;
- semantic acceptance of M04, M07 or M08 authority;
- M01 test observation or disposition;
- merge to `main`, push or publication.

### Programme scope after control acceptance

- up to six PM-controlled lanes, with one bounded unit per active lane;
- only dependency-ready and non-overlapping assignments may run concurrently;
- one worker and one independent tester per assignment;
- progressive module proof and package migration;
- serial PM acceptance and integration;
- final global reconciliation and whole-system proof after the module sequence.

## Invariants

1. One mutating leaf may be open per active PM-controlled lane; each leaf has disjoint semantic ownership and an exact write set.
2. The next module must be dependency-ready; numbering alone never opens it.
3. Normative meaning and target ownership precede test admission and implementation.
4. Missing or contradictory meaning returns to normative authority for the active module only.
5. Passing legacy tests do not acquire authority automatically.
6. Unreviewed unrelated tests remain visible as `LEGACY_SHADOW_UNADMITTED`.
7. Expected red is lawful when a newly admitted test truthfully exposes absent implementation.
8. Existing code is evidence: neither sacred nor disposable.
9. Package migration is progressive; no repository-wide move is authorised.
10. Required identity, lineage, time, state and policy authority is supplied by its owner.
11. Parallel Risk remains independent until the governed terminal join in `M09`.
12. No production, live, paper, durability or replay-completeness claim exceeds evidence.
13. Canonical acceptance, integration and global control mutation remain serial.
14. A lane never owns a module permanently and never selects its own follow-on assignment.
15. Any material read-set change before integration invalidates the tester verdict until revalidation.

## Programme gates

### `CTRL-ARCH-001` — Architecture control integration

**Pass:** all governing controls and accepted architecture artefacts agree; dependency planes are separated; `M07` is corrected; `D-xxx` obligations are retained without a fixed total order; module-local proof law is active; no source/test/runtime change occurred; validation, commit and archive evidence exist.

**Fail:** any remaining conflict or ambiguity, hidden behavioural mutation, broken workbook/graph, missing source hash or unrecorded authority change.


### `PARALLEL-CYCLE-01` — Four-lane proof pilot

**Pass:** all four lane pairs use the same canonical checkpoint; each assignment is one leaf; write sets and locks are disjoint; worker and tester briefs are standalone; Lanes 5 and 6 are held; no source/test/runtime mutation occurs; PM integration order and aggregate validation are explicit.

**Fail:** ambiguous ownership, shared writable files, autonomous continuation, missing tester independence, unrecorded stale-base handling, or any behavioural mutation in the control checkpoint.

### Module-local proof gate — `<Mxx>-PROOF`

Before implementation of one module or bounded behaviour:

1. confirm exact normative meaning, owner, inputs, outputs, state, side effects and prohibited authority;
2. map only the relevant Atlas cohorts/records and existing `D-xxx` obligations;
3. inspect only tests claiming authority over that module;
4. admit, repair, replace, demote or retire those tests;
5. resolve missing normative meaning before code;
6. write expected-red proof where required;
7. independently validate that the proof expresses the accepted requirement;
8. issue `implementation_open` or `closed:<return-gate>` for the module.

### Module implementation gate — `<Mxx>-IMPLEMENT`

Implement the smallest semantically complete module slice using the accepted code strategy. Run targeted admitted proof first, then affected proof and the complete legacy suite as shadow evidence. A shadow failure triggers local review; it does not automatically rewrite the new code.

### Module checkpoint — `<Mxx>-CHECKPOINT`

Record diff, tests, architecture dependency check, vocabulary audit, receipt, commit and clean checkpoint before selecting the next dependency-ready module.

### Final consolidation

After the module sequence:

- reconcile all remaining 179-test dispositions and historical missing-authority candidates;
- confirm all 33 `D-xxx` obligations are satisfied, superseded or explicitly rejected;
- run full admitted Tier A, Tier B shadow, replay, modularity, state, proof, vocabulary and archive checks;
- make any whole-system or operational readiness decision separately.


## Dependency waves and integration order

Assignments may run concurrently only inside a dependency-ready wave. Integration remains one accepted artefact at a time.

1. Accepted foundation: `M13 state_kernel`.
2. Current independent roots: `M01 source_admission`, `M04 packet_protocol`, `M07 coefficient_modifier_authority`, `M08 playbook_catalogue`.
3. `M02 calendar` after the required M01 contracts are canonical.
4. `M03 preparation` after M01 and M02.
5. `M05 serial_cognition` and `M06 parallel_risk` after their prerequisites; they may be separate concurrent assignments.
6. Serial causal chain: `M09 capital_authority` → `M10 execution_gateway` → `M11 portfolio_lifecycle`.
7. `M12 evidence_replay` after required evidence-export contracts are stable.
8. `M00 application_shell` final composition.

`M14` and `M15` apply continuously as PM-controlled governance planes and are not filler assignments for unused lanes.

Cycle 1 integration order is M01, M04, M07, M08. This order preserves deterministic programme continuity; it does not assert runtime dependency among the four roots.

## `D-xxx` treatment

- Preserve every existing `D-xxx` ID and its requirement, source, test and evidence links.
- Regroup the records beneath the accepted module owner.
- Do not infer that one `D-xxx` equals one branch or complete module.
- Split or combine implementation work only inside an accepted module brief while preserving the original IDs in traceability.
- Add a bounded positive obligation when an active module lacks one; current known gaps are `M07`, `M09`, `M10` and `M11`.
- Do not preserve the number 33 as a design objective. Preserve the evidence and obligations.

## Progressive package migration

The target package convention is `src/nvda_desk/mxx_<accepted_name>/`.

For each active module:

1. create the target package only when the module opens;
2. move, retain, refactor or replace only the active ownership boundary;
3. expose one explicit public API;
4. use temporary compatibility imports/adapters only with a removal condition;
5. prohibit new code in the superseded ownership location;
6. remove compatibility paths after consumers migrate;
7. validate runtime dependency direction after each checkpoint.

Local variables and private helpers are module-local vocabulary. New exported contracts, durable domain concepts or module IDs require global vocabulary and authority review.

## Evidence locations

- live pointer: `ROADMAP_LEDGER_V2.md`
- module-local proof protocol: `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`
- parallel operating law: `project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md`
- lane registry: `project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md`
- PM parallel-control decision: `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_PM_REVIEW_V1.md`
- parallel-control mechanical evidence: `project_control/canonical_project_manager/parallel_workflow_validation/`
- Cycle 1 briefs: `project_control/canonical_project_manager/PARALLEL_CYCLE_01/`
- architecture decision: `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md`
- architecture workbook: `project_control/canonical_project_manager/architecture/Atlas_Architecture_Traceability.xlsx`
- machine projection and graph: `project_control/canonical_project_manager/architecture/`
- full-read evidence: `project_control/canonical_project_manager/FULL_READ_MANIFEST.tsv`
- validation: `project_control/canonical_project_manager/VALIDATION_LOG.md`
- module evidence: `project_control/canonical_project_manager/units/<module-or-unit-id>/`
- historical Gate C/Gate D evidence: `project_control/normative_authority_top_down_alignment/`

## Validation routes

### Control-integration validation

```sh
git status --short --branch
git diff --check
# confirm changed paths are control/architecture only
# verify all required files are non-empty and hashes recorded
# validate workbook key ranges and formula-error scan
# validate accepted runtime graph is acyclic
# validate M00/M14/M15 are excluded from runtime-domain dependency cycles
# validate all 16 modules, 18 surfaces and 33 historical D records remain represented
```

Behavioural tests are not required for `CTRL-ARCH-001` because source, tests and runtime behaviour are unchanged. No behavioural pass claim may be made from this control-only unit.

### Module validation

Targeted admitted proof precedes affected admitted proof, complete admitted Tier A, Tier B shadow and the full legacy shadow suite. A command that does not execute is `blocked`, not `passed`.

## Progress

| Date | Unit | State | Evidence |
|---|---|---|---|
| 2026-07-20 | PM-000 | `accepted_control_checkpoint` | Original programme activated at baseline `f7bd3f46862f`. |
| 2026-07-25 | Gate C protocol | `historical_global_protocol_frozen` | Global P2 route frozen; later measured as impractical. |
| 2026-07-25 | P2-A01 | `accepted_historical_checkpoint` | Immutable archive and clean checkpoint accepted; evidence preserved. |
| 2026-07-25 | Extended architecture review | `user_accepted` | User accepted `M00`–`M15`, dependency-plane separation, progressive migration, local Gate C and module delivery. |
| 2026-07-25 | `CTRL-ARCH-001` | `accepted_and_fast_forwarded_to_main` | Local `main` now includes the accepted control integration through `b153cd1e3e0808991dcf9c188e380d935cfd9283`. |
| 2026-07-25 | `M13-PROOF` | `independent_pm_closed_atomicity_gap` | User-supplied independent PM disposition reported commit-before-receipt mutant passing 9/9 while leaving state visible without an attesting receipt; implementation remained closed and gate returned to `MLC-P → MLC-T`. |
| 2026-07-25 | `M13-PROOF-REPAIR` | `repaired_pending_independent_acceptance` | Original nine behaviours preserved; two participant/receipt-failure tests added; conforming reference 11/11; PM mutant now rejected 2 failures/9 passes while still passing original nine; no-participant-rollback mutant rejected; no `src/**` changes; proof-repair commit `2dd25e3bdf5759fcaa2320cfd5bba988f9908eee`. |
| 2026-07-26 | `M13-PROOF-V2-RECOVERY` | `independent_pm_closed_prepare_failure_gap_reconstructed` | From sole source `490e63ed3c96da90a81239326e2d33dd77bdbf36`, independently reproduced a coordinator that registers rollback responsibility only after successful `prepare()`: all eleven tests pass, while a direct probe leaves stale pending participant state, records zero rollback calls and poisons the identical retry. This reconstructs the lost PM V2 decision without claiming the lost commit or archive hash. |
| 2026-07-26 | `M13-PROOF-REPAIR-V2` | `worker_repair_ready_for_independent_review` | Commit `7b3b04c4647ee13674e46c55227b5352cb8c8361` preserves all eleven prior test functions, appends one prepare-failure rollback/clean-retry test, passes the conforming reference 12/12, reproduces the register-after-prepare mutant at old 11/11 and rejects it under the repaired family 1 failure/11 passes; no `src/**`, normative or proof-configuration change. |
| 2026-07-26 | `M13-PROOF-V3-REVIEW` | `independent_pm_closed_prior_prepared_participant_gap` | From clean source `e59b8bdfb5d1e34944aa1b661643c8e6570b940c`, a coordinator that rolls back only the participant currently raising during `prepare()` passes all 12 tests. With two participants, the first retains pending state when the second fails; the identical retry is poisoned. Return only to bounded `M13-PROOF-REPAIR-V3`. |
| 2026-07-26 | `M13-PROOF-REPAIR-V3` | `worker_repair_ready_for_independent_review` | Commit `6ef6e448e28cd96138c0aaeb3d8f8334cad55eb1` preserves the twelve functions and appends one two-participant later-prepare-failure rollback test; conforming reference 13/13 and the PM V3 mutant is rejected. |
| 2026-07-26 | `M13-PROOF-V4-REVIEW` | `independent_pm_closed_failed_idempotency_binding_gap` | A failed-attempt idempotency-reservation mutant passes all 13 tests. The exact retry remains executable, but a different uncommitted input using the same scoped key is falsely rejected, contradicting N-06 atomic binding and MLC-P no-binding-on-failure requirements. Return only to `M13-PROOF-REPAIR-V4`. |
| 2026-07-26 | `M13-PROOF-REPAIR-V4` | `worker_repair_ready_for_independent_review` | Commit `31e8ac38488466d1d457f98ffe014576423a5ebf` preserves the thirteen functions and appends one participant-failure no-binding/fresh-reuse test; conforming reference 14/14 and the PM V4 target mutant is rejected. |
| 2026-07-26 | `M13-PROOF-V5-REVIEW` | `independent_pm_closed_mutation_failure_binding_gap` | A mutation-failure-only idempotency-reservation mutant passes all 14 tests. State, version and receipts remain clean, but a different uncommitted input using the same scoped key is falsely rejected. A second adjacent mutant also passes 14/14 because the V4 test changes command identity and fingerprint together; it retains a failed binding that rejects corrected input under the same command identity. Return only to bounded `M13-PROOF-REPAIR-V5`; implementation remains closed. |
| 2026-07-26 | `M13-PROOF-V6-REVIEW` | `IMPLEMENTATION_OPEN` | Independent Project Manager acceptance: all fourteen frozen functions preserved, one 32-case failure/binding matrix admitted, conforming reference 46/46, both PM V5 false positives rejected by the repaired family, 32 configurable failed-binding mutants and 11 earlier retained mutants rejected for their intended reasons, and current repository remains expected-red solely because `nvda_desk.m13_state_kernel` is absent. |
| 2026-07-26 | `M13-IMPLEMENT-V1-REVIEW` | `independent_pm_closed_reentrancy_and_receipt_contract_gap` | Worker implementation passes 46/46 and bounded shadow validation, but a nested `execute()` during owner mutation commits two receipts at sequence/version 1, overwrites the inner state mutation and retains its receipt/binding. Exported `AtomicReceipt` also accepts scope mismatch and float resulting-version truth. Return only to test-only `M13-PROOF-REPAIR-V6`; implementation and M01 remain closed. |
| 2026-07-26 | `M13-PROOF-V7-REVIEW` | `independent_pm_closed_instance_scope_gap` | The V6 family collects 131 cases, passes the conforming reference and rejects its declared mutants, but a module-global active guard passes 131/131 while falsely blocking an unrelated second UnitOfWork instance. Return only to test-only `M13-PROOF-REPAIR-V7`. |
| 2026-07-26 | `M13-PROOF-V8-REVIEW` | `IMPLEMENTATION_REPAIR_OPEN` | Independent acceptance of V7: all 131 frozen cases preserved; 21 two-instance cases added; conforming reference 152/152; rejected implementation 44 failed/108 passed; eight over-broad guard mutants rejected by designated cases. Open only bounded `M13-IMPLEMENT-REPAIR-V1`. |
| 2026-07-27 | `M13-IMPLEMENT-REPAIR-V1` | `independent_pm_accepted` | Exact worker commit `616fade4123def7870b7950bb3e644ffcc0ccc5a` accepted after independent source reconstruction, blob verification, complete proof and bounded shadow validation. Open only `M01-PROOF-MLC-A-V1`; M01 production and test mutation remain closed. |

| 2026-07-28 | `PARALLEL-WORKFLOW-ENABLEMENT-V1` | `cycle_01_allocated_awaiting_worker_launch` | User authorised six permanent PM lanes; Cycle 1 assigns four dependency-independent proof leaves with exact worker/tester labels and holds Lanes 5–6. |

## Decisions

| ID | Decision |
|---|---|
| `DEC-MOD-001` | Accept `M00`–`M15` as target ownership architecture. |
| `DEC-MOD-002` | Rename `M07` to `coefficient_modifier_authority`. |
| `DEC-MOD-003` | Separate runtime/contract, state/transaction, governance/promotion and build/test dependencies. |
| `DEC-MOD-004` | Preserve 33 `D-xxx` records as traceability obligations, not a fixed branch sequence. |
| `DEC-MOD-005` | Add positive module obligations where current coverage is absent or incomplete for `M07`, `M09`, `M10` and `M11`. |
| `DEC-MOD-006` | Replace global Gate C prerequisite with module-local proof gates and final consolidation. |
| `DEC-MOD-007` | Migrate physical `Mxx` packages progressively. |
| `DEC-MOD-008` | Use the existing repository and Git history; do not create a new repository. |
| `DEC-MOD-009` | Open `M13` first after control integration is accepted. |
| `DEC-M13-001` | Accept N-06 and the M13 ownership boundary as sufficient to specify the minimal non-durable alpha transaction kernel. |
| `DEC-M13-002` | Preserve the original nine lawful M13 behaviours, but do not treat them as collectively sufficient after the independent Project Manager atomicity rejection. |
| `DEC-M13-003` | Repair M13 proof with executable repository participation and rollback on attesting-receipt or participant failure; keep implementation closed pending independent `MLC-V`. |
| `DEC-M13-004` | `CLOSED:the repaired suite does not prove rollback and clean retry when a RepositoryPort fails during prepare; a coordinator that registers participants for rollback only after prepare returns passes all eleven tests while leaving stale participant transaction state after the failure`. Return only to bounded `M13-PROOF-REPAIR-V2`; implementation remains closed. |
| `DEC-M13-005` | Worker proposed a minimum prepare-failure proof repair. Preserve the PM V2 `CLOSED` decision until an independent Project Manager accepts or rejects the repaired twelve-test family; `M13-IMPLEMENT` remains closed. |
| `DEC-M13-006` | `CLOSED:the twelve-test suite does not prove rollback and clean retry for an earlier successfully prepared participant when a later RepositoryPort fails during prepare; a coordinator that rolls back only the participant that raises passes all twelve tests while leaving stale pending state in the earlier participant and poisoning the identical retry`. Return only to `M13-PROOF-REPAIR-V3`; implementation remains closed. |
| `DEC-M13-007` | `CLOSED:the thirteen-test suite does not prove that a failed transaction leaves no idempotency binding; an implementation that reserves the scoped key and failed input after rollback passes all thirteen tests, permits exact retry, but falsely rejects a different uncommitted input using that key`. Return only to `M13-PROOF-REPAIR-V4`; implementation remains closed. |
| `DEC-M13-008` | `CLOSED:the fourteen-test suite proves no failed idempotency binding only for repository-participant failure; an implementation that reserves the scoped key only when the mutation raises passes all fourteen tests, leaves state/version/receipts uncommitted, but falsely rejects a different uncommitted input using that key`. Return only to `M13-PROOF-REPAIR-V5`; implementation remains closed. |
| `DEC-M13-009` | `IMPLEMENTATION_OPEN`: accept the 46-case M13 proof family as sufficient for the bounded non-durable alpha `state_kernel`; open only `M13-IMPLEMENT` under the frozen proof, with M01 and all later modules closed. |
| `DEC-M13-010` | `CLOSED:M13_PROOF_REPAIR_V6_REQUIRED_FOR_REENTRANT_EXECUTION_AND_RECEIPT_CONTRACT_TRUTH`: the implementation proposal permits nested execution before the active transaction commits, producing duplicate sequence/version receipts and overwritten state; exported `AtomicReceipt` also permits contradictory scope and non-integer resulting-version truth. Freeze production and return to test-only proof repair. |
| `DEC-M13-011` | `CLOSED:M13_PROOF_REPAIR_V7_REQUIRED_FOR_INSTANCE_SCOPED_ACTIVE_ATTEMPT_EXCLUSION`: a process-global active guard passes all 131 V6 cases while coupling distinct UnitOfWork instances and blocking an unrelated owner transaction. Preserve V6 proof and return to one positive two-instance independence proof plus global/class-guard falsification; production remains frozen. |
| `DEC-M13-012` | `IMPLEMENTATION_REPAIR_OPEN`: accept the 152-case V7 family as sufficient for instance-owned active-attempt exclusion and receipt truth. Open only repair of the frozen four-file M13 implementation; tests, normative authority, configuration, M13 acceptance/merge, M01 and later modules remain closed. |
| `DEC-M13-013` | `ACCEPTED:M13_IMPLEMENT_REPAIR_V1`: accept exact worker commit `616fade4123def7870b7950bb3e644ffcc0ccc5a`; preserve the bounded non-durable claims and open only M01 authority sufficiency. |
| `DEC-M01-001` | `ACCEPTED:M01_PROOF_MLC_A_V1`: accept exact worker checkpoint `eef4a2ff16d4aaf782ebe047c342999810fa102f`; current numbered authority is sufficient for the bounded general M01 source-admission contract. Family-specific mandatory/optional facts and identifier rules remain later contract/proof obligations. |
| `DEC-PAR-001` | Establish six permanent PM-controlled capacity lanes; lanes are not module ownership or long-lived branches. |
| `DEC-PAR-002` | Use exact thread names `Lane <n><letter>W` and `Lane <n><letter>T`; each assignment uses fresh worker/tester threads. |
| `DEC-PAR-003` | Permit only dependency-ready, disjoint assignments; keep Lanes 5 and 6 held when no lawful unit exists. |
| `DEC-PAR-004` | Workers and testers return one Git-preserving archive each; tester PASS is suitable for PM integration review only. |
| `DEC-PAR-005` | Canonical integration is sequential; Cycle 1 order is M01, M04, M07, M08; stale or conflicting outputs require revalidation. |


## Next gate

After publication of this control checkpoint, launch exactly these four worker threads from the same source archive:

- `Lane 1AW` — `M01-PROOF-MLC-R-V1`;
- `Lane 2AW` — `M04-PROOF-MLC-A-V1`;
- `Lane 3AW` — `M07-PROOF-MLC-A-V1`;
- `Lane 4AW` — `M08-PROOF-MLC-A-V1`.

Create their matching tester threads `Lane 1AT`, `2AT`, `3AT` and `4AT` only for the corresponding worker return. Lanes 5 and 6 remain held. No worker or tester may change source, physical tests, global controls or another lane's evidence, and no `B` assignment opens from an unintegrated result.

## Roadblocks and Unknowns

- Provenance limitation: this worker repair descends from original checkpoint `4a259217...`; the actual reported Project Manager checkpoint `50d82f2...` was not present in the worker filesystem. The user-supplied PM disposition and reported hashes are preserved as return-gate evidence in the M13 proof record.
- Recovery provenance: the later PM V2 checkpoint `7e95102...` / archive SHA-256 `9d780f...` was reported lost. The PM V2 decision was independently reconstructed from source commit `490e63e...` on `recovery/m13-pm-v2-closed`; no claim is made that the recovered commit or archive bytes reproduce the lost identifiers.
- Exact implementation details remain module-local decisions and are not frozen by this control integration.
- Production retention, backup, recovery, capacity, deployment topology, credentials and live/paper operating requirements remain intentionally unknown and out of scope.
- Historical candidate dispositions for missing normative authority remain evidence and must be reconciled when their owning module opens or during final consolidation.
- The current source package graph contains small historical cycles; their removal belongs to the affected module migrations and is not a control-only change.

## Stop and return conditions

Return upward when:

- required normative meaning for the active module is absent or contradictory;
- local proof cannot establish the governed seam;
- a proposed change crosses into another unopened ownership module;
- a durable exported term lacks a semantic disposition;
- validation reveals an unclassified dependency cycle or authority conflict;
- a destructive, external, merge, push or publication action requires approval.

Unrelated legacy-test ambiguity is not a programme-wide blocker. It remains shadow evidence until its owner module or final consolidation addresses it.

## Closeout

This ExecPlan closes when every accepted ownership module is implemented or explicitly rejected at its lawful boundary; all retained `D-xxx` obligations and accepted Atlas behaviour are traceable; module-local and final proof pass without suppression; architecture, vocabulary, replay, state and evidence agree; and the repository reaches an explicit final checkpoint.
