# M13 State Kernel Implementation — Long-Running Worker Brief

## Execution mode

Work uninterruptedly through the complete bounded `M13-IMPLEMENT` acceptance unit.

This is a deliberately extended implementation task. Do not stop after creating the package, making one test pass, making all 46 tests pass, running one mutant, updating records, committing, or creating an unverified archive. Continue through every safe in-scope implementation, falsification, regression, architecture, vocabulary, Git and checkpoint gate.

Stop only for a genuine hard blocker: source mismatch; missing or contradictory authority; an accepted test defect; an unavoidable change outside M13 ownership; unavailable dependency that cannot be repaired within scope; destructive action requiring approval; or unsafe repository state.

## Role

Act only as the M13 implementation worker.

The independent Project Manager has issued:

`IMPLEMENTATION_OPEN`

Implement the smallest semantically complete non-durable alpha `M13 state_kernel` under the accepted N-06 authority and frozen 46-case proof family.

The worker may propose implementation completion but may not provide final M13 acceptance.

## Scope

### Allowed production mutation

- `src/nvda_desk/m13_state_kernel/**` only.

### Allowed non-production mutation

- worker-owned M13 implementation records and raw validation evidence;
- the active ExecPlan/roadmap progress fields only where repository law requires the worker to record implementation progress, without issuing final acceptance;
- a module-local implementation validation script where needed.

### Closed surfaces

Do not:

- modify the frozen M13 test file or any other test semantics;
- modify normative documents;
- modify vocabulary authority unless a genuinely new durable exported term is discovered, in which case stop at the exact authority blocker rather than inventing it;
- modify proof-block or retained-test configuration;
- modify existing persistence, repository, capital, position, API, domain or later-module source;
- copy the retained conforming reference snapshot wholesale as the implementation;
- claim durability, restart recovery, crash recovery, multi-process safety, external-effect completion, production readiness or global transaction authority;
- begin M01 or another module;
- merge to `main`;
- issue final module acceptance.

## Required reading

Read in full before source mutation:

1. `00_TASK/PROJECT_EXECUTION_METHOD.md`
2. `AGENTS.md`
3. `PLANS.md`
4. `tests/AGENTS.override.md`
5. `project_control/canonical_project_manager/EXEC_PLAN.md`
6. `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`
7. `ROADMAP_LEDGER_V2.md`
8. `project_control/canonical_project_manager/modules/M13/M13_PROOF_RECORD.md`
9. this implementation brief
10. the complete frozen M13 contract file
11. N-06 in `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md`
12. the M13 ownership allocation in the accepted architecture report/workbook or machine projection
13. the existing persistence and repository source relevant to avoiding duplicate ownership
14. all retained M13 mutant sources and V5 matrix evidence
15. vocabulary entries for State Kernel, Unit of Work, Idempotency Key, Atomic Receipt, Repository Port and Transaction Command

The retained conforming reference is falsification evidence, not implementation authority. Derive the implementation from N-06, accepted ownership and the frozen proof.

# Semantic acceptance leaves

Complete one leaf fully before the next.

## `M13-I01` — Package and ownership boundary

Create the progressive target package:

`src/nvda_desk/m13_state_kernel/`

Define a clear internal organisation and one explicit public export surface.

The package must own only:

- transaction coordination mechanics;
- scoped idempotency binding;
- expected-version enforcement;
- atomic receipt and sequence publication;
- repository-participant coordination;
- storage/participant protocols;
- the explicitly non-durable in-memory alpha adapter.

It must not own the semantic meaning of capital, positions, calendar facts, risk observations, execution or other domain records.

Pass criteria:

- accepted public names are exported;
- no imports from unopened domain modules;
- no reverse dependency into API, cognition, capital, downstream or review code;
- package remains a shared foundation rather than a global business service.

## `M13-I02` — Immutable public contract types

Implement and validate the accepted public seam:

- `UnitOfWork`
- `RepositoryPort`
- `IdempotencyKey`
- `TransactionCommand`
- `AtomicReceipt`
- `InMemoryUnitOfWork`
- `IdempotencyConflictError`
- `StateVersionConflictError`

Requirements:

- identities and committed receipts are immutable value objects where lawful;
- required string identifiers are non-empty;
- input fingerprints and policy versions are retained exactly;
- scoped key identity includes key value, command type and consistency-unit ID;
- command identity independently preserves command ID, semantic input fingerprint and policy version;
- receipt truth binds command, scope, fingerprint, policy, result, prior/resulting versions and committed sequence;
- no timestamp or wall-clock dependency is introduced merely for decoration.

## `M13-I03` — Detached non-durable state adapter

Implement the in-memory adapter with explicit:

`durability == "non_durable_in_memory"`

Requirements:

- initial state is defensively copied;
- working state is isolated from committed state;
- snapshots and receipt reads return detached copies;
- external mutation of caller inputs or returned snapshots cannot change committed truth;
- state version begins at `0`;
- committed sequence begins at `0` and advances only with a successful atomic commit;
- no filesystem, SQLite, network, process-global singleton or external service is used.

## `M13-I04` — Version and idempotency law

Implement the N-06 ordering rules:

1. resolve exact duplicate replay before stale-version rejection where the accepted proof requires replay of an already committed command;
2. reject conflicting reuse of a committed scoped key when command ID, fingerprint or policy differs;
3. reject stale expected state version before mutation or participant work;
4. bind an idempotency key only with the final committed result/state/version/sequence/receipt tuple;
5. leave no binding after any unsuccessful attempt;
6. preserve independence when the same raw key value is used under a different command type or consistency-unit ID.

Exact duplicate replay must:

- return the original receipt/result identity;
- set only the replay response's `duplicate_replay` indicator;
- not rerun mutation;
- not invoke repository participants;
- not increment state version, sequence or receipt count;
- not alter the originally stored receipt.

## `M13-I05` — Owner mutation and receipt construction

Execute owner mutation against an isolated working copy.

Requirements:

- mutation exceptions publish nothing;
- mutation output must be a valid mapping;
- `receipt_id` and `result_id` must be non-empty;
- invalid output or identity publishes no state, version, sequence, participant truth, receipt or idempotency binding;
- receipt construction occurs before participant preparation;
- the successful receipt represents the proposed transaction but is not internally published before the complete participant boundary succeeds.

## `M13-I06` — Repository-participant atomic coordination

Implement the accepted `RepositoryPort` coordination through the public seam.

For each successful transaction:

1. register rollback responsibility before calling each participant's `prepare()`;
2. call `prepare(command, working_state, receipt)` in declared order;
3. call `commit()` in declared order only after every prepare succeeds;
4. after every participant commit succeeds, atomically publish internal state, state version, sequence, receipt and idempotency binding.

For every failure during prepare or commit:

- roll back the participant that raises where it may have established pending or visible truth;
- roll back every earlier prepared or committed participant in reverse order;
- roll back receipt-writer truth identically to state-participant truth;
- tolerate rollback only to the extent admitted by the proof; do not suppress the primary failure with unrelated cleanup logic;
- leave no pending participant state;
- restore any participant-visible state to its pre-attempt snapshot through the participant's own rollback contract;
- publish no internal state, version, sequence, receipt or idempotency binding;
- permit a corrected or identical retry to begin cleanly at the actual current version.

Do not infer a special participant type from a name or private field. All participants use the same accepted protocol.

## `M13-I07` — Full frozen proof closure

Run the frozen M13 family without altering it.

Required result:

- 46/46 pass against production implementation.

Inspect every case, including all 32 parameter IDs. Do not treat a summary count as sufficient if an unexpected deselection, xfail, skip or collection change occurred.

Retain exact command, output and exit code.

## `M13-I08` — False-positive and mutation resistance

Run the frozen family against:

- both PM V5 false-positive implementations;
- all 32 configurable failed-binding variants;
- all 11 earlier retained M13 mutants.

Required:

- the production implementation passes 46/46;
- each mutant remains rejected for its intended defect;
- no mutant rejection is accepted when caused by an unrelated interface mismatch, fixture error or missing successful behaviour;
- the implementation source itself is inspected against the mutant classes to confirm it has not reproduced an equivalent hidden defect under different structure.

Also create at least the following bounded implementation-level mutants from the actual implementation or an equivalent AST/configurable harness:

1. publish idempotency binding before participant prepare;
2. publish internal state before final participant commit;
3. omit rollback of the participant that raises during prepare;
4. omit rollback of an earlier committed participant;
5. mutate the stored receipt when returning duplicate replay;
6. leak mutable state through `snapshot_state()`;
7. ignore policy version in committed identity;
8. increment sequence on failed attempts.

The accepted family must reject each for the intended reason. Retain exact evidence.

## `M13-I09` — Architecture and ownership validation

Prove from the target source surface:

- M13 has no import dependency on M00–M12 domain modules;
- no new top-level package cycle is introduced;
- production code does not import tests or raw-validation evidence;
- production code does not import the conforming reference or mutant sources;
- only the accepted M13 package was added or changed under `src/**`;
- no domain repository ownership was transferred into M13;
- no persistence durability claim was introduced.

Use AST/import inventory as mechanical evidence, then inspect the actual imports and responsibilities semantically.

## `M13-I10` — Vocabulary review

Review every new exported name and durable concept.

Expected result:

- existing admitted vocabulary is reused;
- private helpers and local implementation names remain module-local;
- no new global durable term is required.

If a genuinely new durable cross-module term is required, stop at `BLOCKED_MISSING_VOCABULARY_AUTHORITY`; do not silently add or rename it during implementation.

## `M13-I11` — Affected and shadow validation

Run:

1. targeted M13 Tier A proof;
2. complete persistence Tier A surface;
3. proof-block structural validation;
4. proof-executor contract;
5. checkpoint shadow;
6. architecture/dependency checks;
7. vocabulary builder/parity checks;
8. complete repository test suite as shadow evidence where executable in the environment.

For the complete shadow suite:

- retain the exact output and exit code;
- compare failures against the source checkpoint;
- classify every new or changed failure as affected, unrelated legacy shadow, environment-specific or a genuine implementation regression;
- do not suppress, skip, edit or weaken tests;
- do not change M13 code merely to satisfy an unadmitted unrelated test without semantic review.

The required implementation acceptance condition is zero new unexplained regressions and all admitted M13 proof green.

## `M13-I12` — Code quality and failure inspection

Before closeout:

- inspect all M13 source in full;
- run syntax and available static/type validation;
- run `git diff --check`;
- verify no broad exception suppression;
- verify the primary transaction failure is not hidden by rollback failure handling;
- verify no public mutable collection is exposed;
- verify no dead or unused compatibility code was added;
- verify comments explain non-obvious transaction law rather than repeat code;
- verify implementation is materially independent of the retained reference snapshot.

## `M13-I13` — Records, commit and checkpoint

Update only worker-owned M13 implementation records and required live progress fields.

Record:

- implementation structure and ownership rationale;
- public contracts;
- transaction ordering;
- rollback ordering;
- idempotency ordering;
- every validation command and exit code;
- production proof result;
- mutation results;
- architecture and vocabulary review;
- complete shadow comparison;
- changed paths;
- final branch and commit;
- tracked evidence hashes.

Label the worker result exactly:

`PROPOSED_M13_IMPLEMENTATION_AWAITING_INDEPENDENT_PROJECT_MANAGER_REVIEW`

Commit one bounded implementation checkpoint on a new worker branch. Do not merge.

Create exactly one Git-preserving archive outside the repository containing the complete `.git` history. Verify from a fresh extraction:

- archive integrity and SHA-256;
- branch and commit;
- clean worktree;
- exact production source hashes;
- frozen test hash and test-count preservation;
- 46/46 targeted proof;
- architecture boundary;
- required evidence integrity.

Return one archive only and end with:

`READY_FOR_INDEPENDENT_PM_IMPLEMENTATION_REVIEW`

# Acceptance summary

The implementation worker succeeds only when all of the following are true:

- source checkpoint verified;
- only bounded M13 production source and allowed records changed;
- frozen proof semantics unchanged;
- production M13 proof 46/46;
- no skips, xfails or deselections conceal proof;
- PM V5, configurable, earlier and implementation-derived mutants rejected for intended reasons;
- affected suites pass;
- complete shadow suite recorded and no new unexplained regression remains;
- architecture remains acyclic and M13 domain-independent;
- vocabulary review passes without invented authority;
- one clean commit exists;
- one fresh-extraction-verified Git archive exists;
- final status remains a worker proposal awaiting independent PM review.
