> **CONTROL STATUS — SUPERSEDED SCHEDULING AUTHORITY**
>
> This 20 July 2026 launch brief is retained as historical programme evidence. The user-approved 25 July 2026 strategy amendment supersedes its repository-wide test-adjudication prerequisite, fixed `D-xxx` total order and delayed implementation opening. Current authority is `AGENTS.md`, `PLANS.md`, `project_control/canonical_project_manager/EXEC_PLAN.md`, `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`, `ROADMAP_LEDGER_V2.md` and the routed architecture working authority. Unamended semantic principles in this brief remain evidence only where they do not conflict with those active controls.

# Canonical Project Manager Brief

## Governed Atlas integration and NVDA implementation programme

Version: 2.1 — 20 July 2026
Classification: launch brief for the human Project Manager
Repository maturity: alpha
Target form: governed modular monolith

This document is not the repository's task-specific `EXEC_PLAN.md`. The Project Manager must create that file as the first project-control artefact after completing the mandatory authority reading below. This brief tells the Project Manager what that plan must control and the exact order in which the work is to be performed.

## 1. Project command

### 1.1 Required outcome

#### 1.1.1

Integrate only those Atlas behaviours that are lawfully admitted by the current project authority, while bringing the governed alpha implementation into conformity with the current normative architecture and admitted proof.

#### 1.1.2

Complete the work as a controlled sequence of bounded semantic acceptance units. A unit is defined by one governed behaviour and its proof boundary. It is not defined merely by a file, folder, class, or Atlas cohort.

#### 1.1.3

For every unit, establish the normative meaning first, govern its terminology second, establish truthful tests third, decide what current behaviour is reusable fourth, and change implementation only after those gates pass.

### 1.2 The Project Manager's “top-down” model

#### 1.2.1

The Project Manager's central model is correct: authority and proof must move from higher layers to lower layers, and a dependant unit must not begin until its prerequisite has been accepted.

#### 1.2.2

Four different orders must not be confused:

1. General repository precedence is direct user instruction; applicable `AGENTS.md`; `PLANS.md`; `ROADMAP_LEDGER.md`; governing normative documents; route overrides; tests; implementation; then comments and docstrings.
2. Test work also obeys the more specific hierarchy and read sequence in `tests/AGENTS.override.md`, including official source material where external language, API, package, platform, or tool behaviour is at issue, vocabulary authority, test governance, the retained-test registry, and proof blocks.
3. Runtime governance moves from normative intent to admitted tests to implementation to explanatory documentation.
4. The architecture review order is the eighteen-surface order in the current blueprint, while the implementation order is the fixed dependency-valid sequence in section 6 of this brief.

#### 1.2.3

The architecture graph is acyclic, but it does not represent one literal runtime call stack. Calendar authority, packet carriage, persistence, proof, and vocabulary cross several runtime stages. This brief converts the acyclic dependency graph into one deliberate total order for the human Project Manager.

#### 1.2.4

No parallel implementation is permitted under this brief. Even where two units have no graph dependency, the later numbered unit waits until the earlier numbered unit is accepted and checkpointed. Parallel work requires an explicit amendment to the active `EXEC_PLAN.md`.

### 1.3 Controlling direction of work

#### 1.3.1

The controlling direction is:

> current authority → Atlas candidate assessment → vocabulary admission → behavioural proof → retain/refactor/replace decision → implementation → audit → acceptance

#### 1.3.2

Atlas is candidate behavioural evidence. It does not become a requirement merely because it is present in a cohort, sidecar, workbook row, prior test, or donor implementation.

#### 1.3.3

Existing code is evidence. It is neither automatically preserved nor automatically discarded.

#### 1.3.4

A passing test is bounded evidence. It is not proof that the architecture surface is complete, correctly owned, or future-proof.

## 2. First Project Manager task: establish authority and create the `EXEC_PLAN.md`

### 2.1 Freeze before reading

#### 2.1.1

Record the current archive hash, branch, commit, Git status, file inventory, and applicable repository root before any mutation.

#### 2.1.2

Do not alter normative documents, tests, vocabulary files, source, configuration, schemas, fixtures, migrations, registries, or proof records during this start-up task.

### 2.2 Inventory instruction scopes and read root authority

#### 2.2.1

Find every current `AGENTS.md` and `AGENTS.override.md` in the repository, whether or not an earlier report lists it. Record its path, governed subtree, and relationship to broader instructions.

#### 2.2.2

Read the repository-root `AGENTS.md` first. It determines the repository-wide authority hierarchy and the prerequisites for substantive work.

#### 2.2.3

Do not assume that every override is read immediately after the root file. Follow any prerequisite read sequence that governs that subtree. Read every discovered instruction file in full at its lawful point, including overrides outside the implementation path initially expected, and complete the full set before creating the new `EXEC_PLAN.md`.

#### 2.2.4

Record each instruction file's current path and hash in the full-read manifest. A search result, heading list, AST digest, summary, or prior receipt does not count as a full read.

### 2.3 Read current project control and the normative corpus

#### 2.3.1

Read the current root `PLANS.md`, `ROADMAP_LEDGER.md`, any named successor ledger, and the active approved `EXEC_PLAN.md` in full. Record placeholders, retired surfaces, and unresolved user-owned decisions exactly; do not silently fill or reinterpret them.

#### 2.3.2

Read `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md` in full and follow its current routing, rather than relying on a historical list of filenames.

#### 2.3.3

Read in full every routed current core document, working companion, addendum, ownership ledger, blueprint document, DMPV3 document, testing document, vocabulary document, vocabulary registry, and vocabulary workflow document.

#### 2.3.4

Read the active plan's Gate C proof authority, Gate D readiness report, dependency map, implementation backlog, and implementation-truth ledger. Treat their status claims as evidence to verify, not as a substitute for the normative text.

#### 2.3.5

Record any contradiction, ambiguity, stale route, missing owner, or insufficient proposition. No lower-layer work may decide missing normative meaning.

### 2.4 Read and understand the tests

#### 2.4.1

Before reading native test families, complete the test override's prerequisite sequence: root authority; routed normative core and relevant working companions; vocabulary core and human registry where durable terms or proof labels are involved; testing core and working companion; `config/retained_test_registry.yaml`; and `config/proof_blocks.yaml`.

#### 2.4.2

Then read `tests/AGENTS.override.md` in full. Its rule that greenness is not the target and its admission, registry, invariant, source-truth, runtime-reread, and proof-claim rules govern the test review.

#### 2.4.3

Read every current test file in full, together with the active pack, fixture, and aggregate command that purports to admit it. Folder placement alone does not establish Tier A, B, or C authority.

#### 2.4.4

For each test, identify the exact normative proposition, invariant, public seam, positive case, prohibited or false-positive case, proof tier, current assertion strength, and code path exercised.

#### 2.4.5

Read the exercised runtime code, docstrings, configuration, schemas, and fixtures before relying on the test's meaning. Compare the assertion with the actual behaviour.

#### 2.4.6

Classify presence-only, token-only, signature-only, and specimen-only tests honestly. They may prove that a surface exists; they do not prove that the governed behaviour works.

### 2.5 Rebase the Atlas planning evidence

#### 2.5.1

Reverify the Atlas and governed archive hashes, the 287 cohort rows, the 1,716 source-record links, the eighteen architecture-surface mappings, and the thirty-three Gate D work units against the live repository.

#### 2.5.2

Reread any referenced file whose bytes have changed since the Atlas snapshot. Narrow directory-only references to exact evidence. Do not use an unresolved historical reference to authorise implementation.

#### 2.5.3

Accept or amend the Atlas-to-requirement, Atlas-to-test, Atlas-to-surface, and Atlas-to-work-unit mappings before using them. Do not create one code unit per cohort.

### 2.6 Create the task-specific `EXEC_PLAN.md`

#### 2.6.1

The first project-control artefact created by the Project Manager shall be a new task-specific `EXEC_PLAN.md`.

#### 2.6.2

The new plan must identify the current baseline, authority, scope, invariants, this fixed work order, acceptance criteria, allowed files, forbidden files, evidence locations, validation commands, return gates, stop conditions, and closeout requirements.

#### 2.6.3

The plan must state exactly which decisions and evidence from the prior execution plan remain valid, which are superseded, and why. It must not silently replace the existing plan or rewrite accepted normative meaning.

#### 2.6.4

The plan must include a live progress record, decision record, roadblock record, validation record, full-read manifest, and current unit status.

#### 2.6.5

No normative, test, vocabulary, or implementation mutation may begin until the Project Manager has accepted and activated the new `EXEC_PLAN.md` through the repository's current control route.

### 2.7 Start-up pass condition

#### 2.7.1

Start-up passes only when the Project Manager can identify, from current files rather than memory:

1. the exact proposition governing each open unit;
2. the exact test authority governing it;
3. every hard prerequisite;
4. every changed or unresolved Atlas reference affecting it;
5. the vocabulary authority that will govern its terminology; and
6. the current implementation and state owner.

## 3. Pre-implementation control work

No Gate D implementation begins until sections 3.1 through 3.4 have passed in order.

### 3.1 Repair vocabulary semantic authority

#### 3.1.1 Establish the source of meaning

The human-readable normative vocabulary registry is the semantic authority. Generated JSON, the vocabulary builder, touch stamps, scanners, and synonym reports are projections or evidence tools. They cannot admit a term or decide its meaning.

#### 3.1.2 Reconcile the current divergence

Recount and reconcile the live human registry, generated document, builder seed, audit evidence, aliases, disallowed phrases, and quarantined candidates. The current planning baseline records 42 human registry headings and 87 generated entries, with two-way gaps; those figures must be reverified rather than copied forward as truth.

#### 3.1.3 Correct the proof direction

Vocabulary tests must prove this direction:

> admitted human semantic registry → deterministic builder/projection → generated JSON and audit evidence

They must not prove only that a hard-coded builder agrees with its own generated JSON.

#### 3.1.4 Apply normative order to the repair

If the vocabulary workflow is ambiguous or contradictory, correct the routed normative proposition first. Then establish tests for the corrected authority chain. Only then change the builder, generated projection, or audit tooling.

#### 3.1.5 Vocabulary-control pass condition

This task passes only when a human reviewer can determine the admitted meaning and owner of every durable term without treating generated code or JSON as semantic authority.

### 3.2 Reconcile test authority

#### 3.2.1 Reconcile the physical and admitted inventories

The current baseline contains 166 physical Tier A Python files and 13 Tier B files, while the retained Tier A reconciliation inventory names 120 files. Reconcile the 46-file difference file by file. Do not infer tier from the directory name.

#### 3.2.2 Establish exact authority

For every current test file, record whether authority comes from the retained registry, a proof block, an active pack, or another current route. Record the exact normative proposition and invariant it proves.

#### 3.2.3 Separate proof strength

Classify each test as behavioural, boundary, state-transition, identity/lineage, substitution, replay, presence-only, signature-only, token-only, specimen-only, or historical/observational. A test may have more than one relevant classification, but its strongest lawful claim must be explicit.

#### 3.2.4 Resolve contradictions upward

Where an older Tier A test conflicts with a newer normative test, do not choose the test that preserves current code. Read the governing proposition. If it is sufficient, revise or retire the conflicting test through the test-authority route. If it is insufficient, return to normative authority before changing either test.

#### 3.2.5 Freeze the proof baseline

Publish a reconciled test-authority register, proof-envelope register, dependency map, and aggregate execution route. Implementation may consume this frozen proof; it may not edit it to make code green.

### 3.3 Return the eleven closed units to proof authority

This is Gate C work. It changes no production implementation. Perform the following units in this exact order.

#### 3.3.1 D-009

Replace field-name presence proof for `StageInputBundle` with behavioural proof of construction, mandatory validation, identity/version propagation, detached copies, and failure when required authority is absent.

#### 3.3.2 D-012

Replace dataclass-field presence proof with behavioural proof of material derivation versions, input provenance, deterministic calculation, and replay equivalence.

#### 3.3.3 D-015

After D-012 proof passes, establish behavioural proof for prepared source-artifact identity, fingerprints, schema and policy versions, copy safety, and replay equivalence.

#### 3.3.4 D-010

Resolve the conflict between reference-packet degraded defaults and caller-owned runtime execution context. Record the exact role-specific rule for trace, run, scenario, source-artifact, and fingerprint authority; then freeze positive and prohibited tests.

#### 3.3.5 D-016

After D-010 and D-015 proof authority is ready, re-evaluate the runtime orchestration and DMP proof envelope. Prove deterministic domain output separately from process metadata and prove exact parent/dependency semantics.

#### 3.3.6 D-033

Replace signature inspection with behavioural proof that candidate families and playbook-registry authority are consumed, filtered, propagated, and kept free of capital or broker authority.

#### 3.3.7 D-017

Resolve the conflict between older Parallel Risk tests that accept missing context and the current fail-closed lineage requirement. Freeze the migration and runtime boundary explicitly.

#### 3.3.8 D-031

Resolve the conflict between structural inspection through `run_once` and governed execution through `run_once`. Establish separate named contracts if both behaviours are authorised; governed execution must fail closed on invalid input.

#### 3.3.9 D-021

Resolve the older API test that requires API-owned veto and risk-block collections against the current rule that the application shell owns no untyped domain state.

#### 3.3.10 D-048

Freeze proof for a transport/composition shell that cannot invent domain authority, depend on private repository storage, or own mutable domain collections.

#### 3.3.11 D-041

After D-048 proof authority passes, isolate exit/close proof from the API shell and require every input identifier and policy version to originate from its governed upstream owner.

### 3.4 Freeze the implementation order

#### 3.4.1

Reissue the thirty-three proof envelopes with one of two statuses only: `implementation_executable_now` or `closed` with an exact return gate.

#### 3.4.2

Confirm that the total order in section 6 contains every work unit exactly once and violates no hard prerequisite.

#### 3.4.3

If any unit remains closed, do not pretend that the sequence is ready. Resolve its return gate or record a hard blocker before implementation begins.

## 4. Mandatory acceptance cycle for every implementation unit

The Project Manager shall apply sections 4.1 through 4.10 to each unit in section 6. No step may be omitted because a change appears small.

### 4.1 Open only the named unit

#### 4.1.1

Confirm that the unit's proof envelope says `implementation_executable_now`, every prerequisite unit is accepted, and the working tree is at the preceding clean checkpoint.

#### 4.1.2

List the exact normative propositions, Atlas rows, tests, source symbols, configuration, state, and interfaces in scope. Everything else is out of scope for that unit.

### 4.2 Confirm normative sufficiency

#### 4.2.1

Write a plain-English input → decision/transformation → output statement for the unit.

#### 4.2.2

Confirm owners, mandatory and optional inputs, outputs, identity, time, state, side effects, error behaviour, replay obligations, and prohibited authority.

#### 4.2.3

If any required meaning is absent or ambiguous, stop the unit and return to the routed normative document. Amend and refreeze the norm before touching tests or code.

### 4.3 Assess the mapped Atlas evidence

#### 4.3.1

Pull only the Atlas cohort and record rows mapped to the unit's current requirement and architecture surface.

#### 4.3.2

For each candidate behaviour, record `already_governed`, `requires_normative_admission`, `contradictory`, `donor_plumbing_only`, `provisional`, or `not_applicable`.

#### 4.3.3

No Atlas-derived behaviour proceeds to tests until it is either already governed or has completed normative admission.

### 4.4 Perform the pre-change vocabulary audit

#### 4.4.1

Inventory every proposed new, renamed, or repurposed identifier in normative text, tests, fixtures, configuration, schemas, contracts, classes, functions, methods, fields, enum values, statuses, events, receipts, and public code.

#### 4.4.2

For each identifier, decide whether it expresses a durable project term. A local implementation name still requires assessment, but it does not require registry admission when it carries no durable governed meaning; record that rationale.

#### 4.4.3

For each durable candidate, use the governed disposition exactly: `enrich_existing`, `add_new`, `alias_only`, or `quarantine`.

#### 4.4.4

Complete semantic admission in the human registry before the term appears in admitted tests or implementation. Regenerate machine projections only after semantic admission.

### 4.5 Establish the tests before implementation

#### 4.5.1

Create or correct the smallest behavioural proof that expresses the governed public seam.

#### 4.5.2

Include, where applicable, the positive path, prohibited path, false-positive path, missing mandatory input, explicit optional absence, identity/lineage, ordering, state isolation, idempotency, failure rollback, substitution, and replay.

#### 4.5.3

Run the targeted proof against the unchanged implementation. The expected result is either a truthful red caused by the missing behaviour or a green result whose assertion has been shown not to be a false positive.

#### 4.5.4

If the test is contradictory, weak, or green for the wrong reason, return to test authority. Do not code against an untrustworthy test.

### 4.6 Decide retain, refactor, or replace

#### 4.6.1

Assess the exact current symbols and behaviours in the unit. Do not issue a file-wide or repository-wide decision merely because one part is defective.

#### 4.6.2

Record one disposition for each bounded component:

1. `retain` — governed behaviour, correct owner and boundary, and adequate proof;
2. `refactor` — governed behaviour worth preserving, but ownership, interface, coupling, or testability must change;
3. `behavioural_reference_only` — useful intent or algorithm, but the current implementation is not safe to carry forward;
4. `replace_boundary` — local behaviour may survive, but the seam, ownership, or state transition must be rebuilt;
5. `replace_core` — the underlying representation or mechanism contradicts the governed design; or
6. `remove_or_quarantine` — ungoverned, contradictory, duplicate, unreachable, or donor-only behaviour.

#### 4.6.3

State the evidence: governing proposition, test result, hidden dependency, coupling, state ownership, vocabulary status, migration risk, and replacement cost.

### 4.7 Implement the smallest semantically complete change

#### 4.7.1

Change only the admitted owner, contract, adapter, configuration, repository, or composition surface needed for the unit.

#### 4.7.2

Do not weaken admitted assertions, fabricate missing identity, hide failure, add speculative abstractions, introduce a generic plugin system, or create service/network boundaries not authorised by the modular-monolith architecture.

#### 4.7.3

Reread the changed input-to-output flow and every changed file in full.

### 4.8 Validate in increasing scope

#### 4.8.1

Run the unit's targeted positive and prohibited Tier A nodes first.

#### 4.8.2

Run all affected existing Tier A tests, then the complete admitted Tier A route.

#### 4.8.3

Run Tier B as shadow evidence. Treat Tier C as observational unless current authority explicitly promotes it.

#### 4.8.4

Run the unit's substitution, state, replay, proof-block, static, and repository-integrity checks where applicable.

### 4.9 Perform the post-change vocabulary audit

#### 4.9.1

Derive the identifier and term inventory from the actual diff, not from the pre-change proposal.

#### 4.9.2

Confirm that every durable term is admitted, every alias is lawful, removed terms are handled, no disallowed phrase was introduced, and generated projections match the human semantic registry.

#### 4.9.3

A passing scanner does not complete this audit. A semantic reviewer must decide every candidate and record the evidence.

### 4.10 Accept and checkpoint the unit

#### 4.10.1

Record the normative proposition, Atlas rows, vocabulary decisions, test nodes and results, retained/refactored/replaced symbols, diff, validation output, known limitations, and updated dependency state.

#### 4.10.2

Commit one semantic unit and confirm the expected clean state.

#### 4.10.3

Only after acceptance may the Project Manager open the next numbered unit.

## 5. Meaning of the implementation sequence

### 5.1

Section 6 is the only permitted implementation order under this brief. It deliberately begins at external authority and raw identity, establishes calendar and prepared-data truth, establishes atomic state and packet rules, completes serial cognition, completes the independent risk branch and final join, and composes application/downstream/review/replay last.

### 5.2

The “current-code disposition” stated for each unit is the evidence-based starting decision. The Project Manager must confirm it under section 4.6; the label is not permission to retain a whole file without inspection.

### 5.3

If an earlier unit already supplies all behaviour required by a later unit, the later unit still receives its own proof and acceptance record. It may close as verification-only; it must not be silently skipped.

## 6. Fixed serial implementation order

### 6.1 D-001 — external-source contract

Prerequisite: none after section 3 passes.
Work: require every admitted external family to enter through its named typed boundary; reject fabricated source identity and forbidden authority recursively.
Current-code disposition: refactor the existing external-source contract; retain recursive rejection and detached-copy behaviour only where behavioural tests prove it.

### 6.2 D-002 — raw-bundle and capture identity

Prerequisite: D-001 accepted.
Work: require source/capture identity, explicit market/options sections, temporal truth, and deterministic precedence; reject unrelated fallback mappings.
Current-code disposition: replace the permissive fallback core in the raw-bundle loader while retaining lawful typed decoding behaviour.

### 6.3 D-003 — ingress-adapter composition

Prerequisite: D-001 and D-002 accepted.
Work: make the market and options adapters compose the authoritative source and raw-bundle contracts while preserving identity and temporal lineage.
Current-code disposition: refactor the thin adapters; do not allow them to recreate source authority or bypass preparation.

### 6.4 D-049 — typed options evidence

Prerequisite: D-003 accepted.
Work: introduce the governed options-evidence envelope and make cognition consume a typed reference carrying identity, versions, observation time, completeness, and semantic fingerprint.
Current-code disposition: replace generic mapping authority in the options mapper; retain numeric coercion only as a bounded transform behind the typed contract.

### 6.5 D-050 — four-layer financial calendar

Prerequisite: D-049 accepted under this serial programme; no graph prerequisite.
Work: implement the exact four semantic layers, their owners, equal-value coalescence with complete lineage, and explicit supersession or fail-closed conflict.
Current-code disposition: retain useful reference import/projection algorithms; replace arbitrary layer labels and split calendar truth.

### 6.6 D-006 — calendar reference-to-operational composition

Prerequisite: D-050 accepted.
Work: provide one explicit owned composition from checked reference projection into operational query state, with duplicate and identity law and no candidate or sizing authority.
Current-code disposition: replace the missing composition and mixed API ownership; retain bounded query and sorting logic where proved.

### 6.7 D-007 — raw-signal family extension

Prerequisite: D-006 accepted under this serial programme; no graph prerequisite.
Work: make signal-family admission registry-driven and preserve source observation time, source identity, quarantine, and non-interference.
Current-code disposition: refactor the existing scope-lock and trace carriers; retain copy-safety and quarantine behaviour where proved.

### 6.8 D-051 — typed prepared-data envelope

Prerequisite: D-007 accepted under this serial programme; no graph prerequisite.
Work: implement mandatory prepared identity, source references, schema and policy versions, derivation versions, effective time, fingerprints, validation/completeness state, and typed payload kind.
Current-code disposition: replace the generic prepared-data core; retain deterministic transform functions only behind the new typed envelope.

### 6.9 D-052 — canonical field resolution

Prerequisite: D-051 accepted.
Work: resolve per-field candidates, coalesce equal values with complete provenance, and fail closed on unresolved mandatory conflicts unless an explicit field policy governs them.
Current-code disposition: replace implicit section-order precedence with a governed resolution contract and receipt.

### 6.10 D-012 — derivation provenance and replay

Prerequisite: D-052 accepted under this serial programme; proof authority repaired in D-012.
Work: assign a governed version and input provenance to every material derived field and prove deterministic re-execution.
Current-code disposition: retain individually correct pure calculations; refactor their lineage, version, and replay packaging.

### 6.11 D-015 — complete prepared lineage

Prerequisite: D-012 accepted.
Work: carry source-artifact IDs, input fingerprint, input schema versions, preparation policy version, derivation versions, detached copies, and replay equivalence.
Current-code disposition: replace the thin lineage record while preserving truthful source-kind and alignment facts.

### 6.12 D-053 — one common stage context

Prerequisite: D-049, D-051, and D-052 accepted; D-012 and D-015 are also complete under this serial programme.
Work: allocate one immutable common context and narrow temporal, regime, and options carriers that reference it; reject reference mismatch.
Current-code disposition: replace duplicated or implicit common metadata in stage inputs with the governed context contract.

### 6.13 D-009 — stage-bundle identity and versions

Prerequisite: D-053 accepted; proof authority repaired in D-009.
Work: prove mandatory bundle identity, source/capture lineage, input-schema version, and policy/config version without widening stage payloads.
Current-code disposition: refactor `StageInputBundle`; close as verification-only if D-053 has already supplied the complete governed behaviour.

### 6.14 D-054 — transaction and idempotency boundary

Prerequisite: D-009 accepted under this serial programme; no graph prerequisite.
Work: implement command identity, idempotency key plus input fingerprint, expected state version, atomic state-and-receipt visibility, duplicate replay, conflict, and rollback without a success receipt.
Current-code disposition: replace independent process-memory mutation as the material consistency mechanism; retain proven duplicate and copy invariants as local behaviour.

### 6.15 D-010 — DMPV3 execution context and lineage

Prerequisite: D-015 and D-054 accepted under this serial programme; proof authority repaired in D-010.
Work: preserve the common DMPV3 envelope while enforcing role-specific caller-owned identity, time, source-artifact lineage, fingerprint, and deterministic reproduction.
Current-code disposition: retain the typed envelope shape; replace constructors that invent trace, run, scenario, time, or lineage authority.

### 6.16 D-025 — temporal policy version

Prerequisite: D-009 and D-010 accepted.
Work: carry the version that defines temporal classification while preserving source time, explicit timezone conversion, event windows, and fail-closed behaviour.
Current-code disposition: retain the bounded clock and window algorithms; refactor the contract and receipts for versioned authority.

### 6.17 D-055 — signal-informed intraday phase

Prerequisite: D-007, D-050, and D-053 accepted.
Work: implement the governed seven-state signal-informed phase evaluator, transition/history rules, required signal families, and explicit clock-only degraded result.
Current-code disposition: add the governed evaluator; retain the existing clock classifier only as a subordinate input, not as complete phase authority.

### 6.18 D-027 — regime policy version

Prerequisite: D-009 accepted; D-055 accepted under this serial programme.
Work: carry the version defining the bounded regime classifier, prove unknown handling, and preserve the current authorised calculation until normative scope expands.
Current-code disposition: retain the local deterministic classifier; refactor its output and proof for explicit policy authority.

### 6.19 D-033 — candidate families and playbook registry

Prerequisite: D-027 accepted and the D-033 proof envelope repaired under section 3.3.6.
Work: supply candidate-family origin and replaceable registry authority through the public orchestration contract; prove filtering, stand-down, and no unrelated authority.
Current-code disposition: refactor eligibility composition; do not retain signature-only or hard-coded empty-candidate behaviour.

### 6.20 D-034 — execution-expression candidate identity

Prerequisite: D-033 accepted.
Work: carry deterministic candidate identity and lead-selection lineage through expression and lifecycle output without capital, sizing, broker, or placement authority.
Current-code disposition: refactor the current expression kernel; retain its bounded stand-down/lead-selection behaviour only where governed.

### 6.21 D-016 — serial-runtime orchestration and packet lineage

Prerequisite: D-010 and D-015 accepted; D-025, D-027, D-033, and D-034 are complete under this serial programme.
Work: compose explicit dependencies across the governed six-stage order, consume caller-owned context, emit exact packet dependencies, and keep domain output deterministic independently of emission metadata.
Current-code disposition: replace the current orchestrator's inline service construction and authority-ID generation; retain the governed six-stage order and proven stage-local algorithms.

### 6.22 D-031 — governed execution versus structural inspection

Prerequisite: D-016 accepted; proof authority repaired in D-031.
Work: make governed `run_once` reject invalid execution input and place any authorised structural inspection behind a separate explicit contract.
Current-code disposition: replace the partial-mapping fallback in the execution path; retain inspection only if separately governed and tested.

### 6.23 D-017 — Parallel Risk bootstrap identity and lineage

Prerequisite: D-016 and D-031 accepted under this serial programme; proof authority repaired in D-017.
Work: require the full admitted upstream identity, parent/dependency IDs, source artifacts, fingerprint, and execution context; prove that no undeclared serial output influences the lane.
Current-code disposition: replace permissive bootstrap construction; retain bounded independent environment assessment and risk-envelope algorithms.

### 6.24 D-020 — Parallel Risk state ownership

Prerequisite: D-017 and D-054 accepted.
Work: move policy decisions from module-global memory to an injected instance/run-owned repository with duplicate, identity, and isolation law.
Current-code disposition: replace `_RISK_POLICY_DECISIONS` and any cached mutable owner; retain the typed decision record if it remains governed.

### 6.25 D-035 — Parallel Risk policy integration

Prerequisite: D-017 and D-020 accepted.
Work: integrate governed Parallel Risk policy, state, and evidence without candidate formation, serial mutation, capital sizing, or broker authority.
Current-code disposition: refactor the bounded evaluation kernels behind the corrected run-scoped composition and state owner.

### 6.26 D-056 — final serial/parallel risk join

Prerequisite: D-034, D-035, and D-053 accepted.
Work: implement typed serial and Parallel Risk branches and the single categorical terminal join; any hard block or missing branch authority forces stand-down, while two clear branches permit only capital assessment.
Current-code disposition: replace the confidence-based simplified join; retain only independently proved branch calculations.

### 6.27 D-021 — remove API-owned untyped authority state

Prerequisite: D-056 accepted under this serial programme; proof authority repaired in D-021.
Work: remove or route veto and risk-block state through its typed domain owner so API storage cannot influence decisions directly.
Current-code disposition: remove the application-shell lists and route methods unless a separate current normative owner is admitted.

### 6.28 D-048 — application-shell composition boundary

Prerequisite: D-021 accepted; proof authority repaired in D-048.
Work: make HTTP/CLI code perform translation and dependency composition only, using run-scoped dependencies and public ports; forbid fabricated IDs, policy defaults, private storage access, and mutable domain collections.
Current-code disposition: replace the current mixed-responsibility application shell and cached mutable composition; retain governed endpoint intent only.

### 6.29 D-041 — exit/close upstream authority

Prerequisite: D-048 accepted; proof authority repaired in D-041.
Work: require all live-inventory, position, playbook, placement, capital, Parallel Risk, and policy identifiers to originate upstream; missing authority fails closed and handoff remains non-executing.
Current-code disposition: refactor the exit/close decision kernel behind a corrected input boundary; remove API-fabricated identifiers and defaults.

### 6.30 D-042 — overnight-carry identity and policy

Prerequisite: D-041 accepted.
Work: carry action ceiling, policy version, next-session source identity, no-execution status, and deterministic replay.
Current-code disposition: retain bounded carry calculations as behavioural kernels; refactor contracts and replay lineage.

### 6.31 D-044 — review packet lineage and missing material

Prerequisite: D-015, D-016, and D-041 accepted.
Work: expose explicit missing-material flags and complete packet, receipt, and source-artifact lineage while preserving redaction and read-only review authority.
Current-code disposition: retain safe redaction and read-only projection behaviour; refactor the packet and explanation contracts for complete evidence.

### 6.32 D-047 — replay evaluation identity

Prerequisite: D-016 accepted; D-044 accepted under this serial programme.
Work: require dataset and window identity, deterministic ranking, analysis-only authority, and an explicit comparison-only classification.
Current-code disposition: refactor the current comparison/walk-forward structures; prohibit them from claiming authoritative reconstruction or runtime promotion.

### 6.33 D-057 — authoritative replay

Prerequisite: D-010, D-015, D-016, D-054, D-055, and D-056 accepted; all earlier numbered units are complete under this serial programme.
Work: implement the governed replay classes, complete logical envelope, authority assessment, retrievable source/configuration/policy/state/receipt identity, and isolated semantic re-execution.
Current-code disposition: replace the authoritative replay core; retain mapping comparison only as subordinate non-authoritative evidence.

## 7. Atlas handling during the sequence

### 7.1 Atlas is processed inside each unit

#### 7.1.1

Do not build the governed architecture first and then mechanically pour Atlas into it. For every unit in section 6, assess its mapped Atlas rows during section 4.3 before tests and code are finalised.

#### 7.1.2

One Atlas cohort may contribute to several units. Several cohorts may be satisfied by one governed contract or abstraction. Preserve both directions of traceability.

### 7.2 Required Atlas disposition evidence

#### 7.2.1

For every mapped cohort and source record, retain:

1. original record identifier, source file, line interval, and hash;
2. cohort identifier and semantic statement;
3. current normative proposition and architecture surface;
4. current test and work-unit mapping;
5. admission, merge, split, rejection, provisional, or defer decision;
6. implemented or retained symbol, where applicable; and
7. proof and acceptance receipt.

#### 7.2.2

Rejected donor plumbing and contradictory material remain trace evidence. They do not create code debt merely because they are not ported.

#### 7.2.3

Provisional Atlas meaning and unresolved references fail closed. They require a named normative decision before implementation.

### 7.3 Atlas closeout condition

#### 7.3.1

Atlas closeout passes only when all 287 cohort rows and all 1,716 source records remain traceable and every admitted behaviour points to its governing proposition, accepted implementation surface, and proof.

## 8. Whole-system acceptance after D-057

### 8.1 Verify the governed runtime order

The implementation programme is complete only when the following runtime behaviour is composed and proved in its normative order. This list is the runtime order; it is not a replacement for the project work order in section 6.

#### 8.1.1

Real-data admission and preparation.

#### 8.1.2

Financial-calendar authority and runtime context.

#### 8.1.3

Temporal cognition, including signal-informed phase.

#### 8.1.4

Regime cognition.

#### 8.1.5

Options and flow cognition.

#### 8.1.6

Posture and risk permission.

#### 8.1.7

Playbook eligibility.

#### 8.1.8

Expression and execution candidate formation only.

#### 8.1.9

Downstream pre-deployment checks.

#### 8.1.10

Capital state, sizing, and deployment authority.

#### 8.1.11

Opening and non-executing placement readiness unless further authority exists.

#### 8.1.12

Execution bridge, receipt, and state feedback only to the extent currently admitted.

#### 8.1.13

Inventory, position, exit, close, and carry lifecycle.

#### 8.1.14

Review, explanation, comparison, and authoritative replay.

### 8.2 Verify the serial and parallel relationship

#### 8.2.1

The six serial cognition stages remain temporal, regime, options/flow, posture, eligibility, and expression/execution candidate formation.

#### 8.2.2

Parallel Risk remains an independent co-resident branch. It does not form the serial candidate or allocate capital.

#### 8.2.3

The two branches join exactly once before capital assessment. Missing branch authority or a hard block produces stand-down.

### 8.3 Reassess all eighteen architecture surfaces

#### 8.3.1

Update every row in the current implementation-truth ledger from current evidence. Do not carry forward `thin_seam`, `implemented`, or any other status without target-surface proof.

#### 8.3.2

For each surface, record its owner, contract, actual implementation, state writer, persistence boundary, tests, retained/refactored/replaced components, Atlas trace, and unresolved reservations.

#### 8.3.3

An architecture surface may be marked `implemented` only when the public behaviour, prohibited behaviour, state effects, identity/lineage, and required integration are proved. Presence of a package or class is insufficient.

### 8.4 Run final proof in order

#### 8.4.1

Run every unit's targeted Tier A proof, the complete reconciled Tier A route, Tier B shadow proof, applicable proof blocks, substitution checks, transaction and replay checks, and the governed end-to-end path.

#### 8.4.2

Reconcile collected case counts with the admitted registry. Explain parametrisation and any excluded or observational tests. Do not report only a green total.

#### 8.4.3

Record expected red tests as unresolved implementation gaps; do not suppress, skip, xfail, weaken, or silently reclassify them.

### 8.5 Perform the programme-wide vocabulary audit

#### 8.5.1

Audit the complete programme diff across normative documents, tests, fixtures, configuration, schemas, source, receipts, and public interfaces.

#### 8.5.2

Reconcile the human registry, aliases, disallowed phrases, generated JSON, builder output, audit candidates, and touch evidence.

#### 8.5.3

Closeout fails if any durable term is unadmitted, ambiguously owned, duplicated under an ungoverned synonym, or present only in generated authority.

### 8.6 Close retain/refactor/replace decisions

#### 8.6.1

Publish the final component-level decision register. Each retained behaviour must point to current normative authority and behavioural proof. Each replacement must point to the defect it removes and the migration evidence. Each removed item must retain traceability.

#### 8.6.2

Do not call the result a clean rewrite. Do not call it preservation of the alpha. The intended result is selective replacement of defective central seams with retention or refactoring of proved local behaviour.

### 8.7 Create the final checkpoint

#### 8.7.1

Record final branch, commit, clean/dirty state, archive hashes, changed files, test commands and outputs, proof receipts, traceability totals, open defects, and Unknowns.

#### 8.7.2

Close the task-specific `EXEC_PLAN.md` only after every acceptance unit and whole-system condition above is either passed or explicitly blocked by missing higher authority.

## 9. Project Manager stop and return rules

### 9.1 Return to normative authority when

#### 9.1.1

Required meaning, ownership, lifecycle, state, identity, time, policy, error, replay, or vocabulary semantics are missing or contradictory.

### 9.2 Return to vocabulary governance when

#### 9.2.1

A durable term is new, repurposed, ambiguous, duplicated, disallowed, or present in code/tests without human semantic admission.

### 9.3 Return to test authority when

#### 9.3.1

A test conflicts with current norms, lacks tier authority, proves only presence when behaviour is required, is green for the wrong reason, or has an incomplete proof envelope.

### 9.4 Do not stop for an ordinary implementation failure

#### 9.4.1

A truthful red test, import failure, incorrect implementation, stale fixture, or bounded vocabulary candidate is work to resolve through the appropriate gate. It is not permission to weaken proof or skip the unit.

### 9.5 Hard stop conditions

#### 9.5.1

Stop and obtain authority when a required normative decision, source artefact, credential, external action, destructive action, or unavailable dependency cannot be resolved within scope, or when continuing would create a false completion claim.

#### 9.5.2

Under this deliberately serial programme, a hard blocker in the current numbered unit stops later implementation. The Project Manager may not jump to an independent later unit merely to maintain visible progress without first amending the accepted `EXEC_PLAN.md`.

## 10. Explicit exclusions

### 10.1

Do not infer production retention periods, durable-storage topology, deployment topology, capacity, RTO/RPO, high availability, disaster recovery, live brokerage, credentials, or real-money execution from the alpha artefacts.

### 10.2

Do not invent numeric thresholds, dwell or grace periods, calibration values, or production replay storage where current authority leaves them configurable, reserved, provisional, or Unknown.

### 10.3

Do not introduce microservices, a generic plugin framework, distributed coordination, or an AI-agent runtime. The current governed target is a deterministic modular monolith.

### 10.4

Do not treat this brief, the planning workbook, a registry, a ledger, a proof receipt, or a generated vocabulary artefact as implementation proof. Completion must be demonstrated in the governed target surface.
