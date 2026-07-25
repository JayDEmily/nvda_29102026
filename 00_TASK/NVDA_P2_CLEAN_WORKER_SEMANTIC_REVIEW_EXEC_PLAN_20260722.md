# NVIDIA 2026 — P2 Clean-Worker Semantic Review ExecPlan

Version: 3.0  
Date: 22 July 2026  
Status: `authorised_not_started`  
Execution mode: `uninterrupted_serial_p2_review`  
P3: `closed`  
P2 acceptance: `Project Manager only`

## 1. Controlling instruction

### 1.1 Outcome

Produce a new P2 test-authority candidate from the clean repository supplied with this plan.

For every physical Tier A and Tier B Python test file, determine from direct reading:

1. what each assertion group actually observes and proves;
2. which exact current proposition, if any, governs that proved behaviour;
3. what the assertions do not prove;
4. the lawful proof strength and file disposition; and
5. the exact return gate where proof or authority is insufficient.

The worker produces an audit candidate. The worker does not accept P2.

### 1.2 Launch block

> Hydrate the supplied clean tarball and execute this ExecPlan in full. Read `00_TASK/PROJECT_EXECUTION_METHOD.md`, repository control files and routed authority before semantic work. Work strictly in the PM-012 through PM-020 order below and one semantic acceptance unit at a time. Read the complete test, the complete directly exercised surfaces and the complete governing authority before deciding meaning. Do not use scripts, search, summaries, AST output, generated text or repeated templates to make semantic decisions. Continue through all 179 files, integration, validation and packaging. Do not stop at a count, unit boundary, test run, ledger, receipt, validator or tarball. Stop early only for the hard blockers in section 12. P3 remains closed. Project Manager acceptance remains pending.

## 2. Clean baseline

### 2.1 Repository identity

| Field | Required value |
|---|---|
| Repository root | `NVIDIA_2026/` |
| Git branch | `work/NVIDIA_2026_pm001_pm010_restart_20260721` |
| Git HEAD | `21c1e5eccfbb818bdd422afd42117f23b1f74f26` |
| Physical Tier A Python tests | `166` |
| Physical Tier B Python tests | `13` |
| Total physical Python tests | `179` |
| Accepted P1 evidence | `PM-001` through `PM-010` present |
| Standing P2 census | `PM-011` present |
| P2 semantic candidate evidence | absent |
| Initial semantic ledger rows | `179`, all `SEMANTICALLY_READ=NO` |

The working tree is intentionally dirty because accepted P1 files and PM-001–PM-011 evidence are uncommitted relative to HEAD. Preserve that state.

### 2.2 Provenance

This clean baseline was assembled from:

- corrected PM-001–PM-010 snapshot SHA-256 `e18b0643aaec536bd9f22b3eb080efa891c3603f15c1bbd40f218b1bda82b077`; and
- PM-011 from the complete fourth-reopen archive SHA-256 `1e6ae44439c5249cb04ed10b8abe4773b9bb97e843cc76545cd48b7dc97b6ca3`.

All 179 physical test files match the `baseline_sha256` values in:

```text
project_control/canonical_project_manager/units/PM-011/P2_PHYSICAL_TEST_CENSUS.tsv
```

The later P2-modified tests, registries, proof blocks, Makefile changes, PM-012–PM-020 registers, repeated reopen manifests, self-reviews, probes, validators, logs, stale metadata and Python caches are deliberately absent.

### 2.3 Input gate

Before mutation:

1. verify the tarball checksum supplied in the launch message;
2. verify safe extraction;
3. verify branch, HEAD and `git status --short --branch`;
4. reproduce the 166/13/179 file counts;
5. recompute every physical-test SHA-256 against PM-011; and
6. confirm PM-012 through PM-020 directories do not already exist.

If any check fails, stop as `WRONG_BASELINE`. Do not repair or substitute the baseline from memory.

## 3. Authority and scope

### 3.1 Authority order

1. the user's launch instruction;
2. this task-specific ExecPlan;
3. `00_TASK/PROJECT_EXECUTION_METHOD.md`;
4. repository `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER_V2.md` and applicable overrides;
5. the wider canonical programme plan for non-conflicting programme law;
6. current normative documents and accepted PM-001–PM-010 decisions;
7. tests;
8. implementation, configuration, schemas, fixtures and generated artefacts as observed surfaces;
9. ledgers, receipts, manifests, validators and logs as evidence only.

A lower surface cannot create or broaden higher authority. A green test cannot cure an invalid authority link.

### 3.2 In scope

- reproduce PM-011 mechanically;
- semantically review all 179 files allocated by PM-011;
- decide every assertion group's current authority, proof strength and disposition;
- create PM-012 through PM-018 evidence;
- build PM-019 integration from the completed semantic decisions;
- update only the registry/proof projections required by the accepted decisions;
- perform PM-020 structural and behavioural validation; and
- package a complete audit candidate.

### 3.3 Out of scope

- P3, P4 or Gate D implementation;
- new normative meaning;
- accepted P1 semantic changes;
- production/runtime source edits;
- test edits, additions, deletion, retirement, weakening, `skip` or `xfail`;
- semantic admission from directory placement, current registry membership or test greenness;
- automated semantic judgement; and
- worker acceptance of P2.

If a test requires strengthening, record the exact deficit and return gate. Do not repair it inside this review.

## 4. Required reading gate

Before the first semantic decision, read in full and record in a new current full-read manifest:

1. `00_TASK/PROJECT_EXECUTION_METHOD.md`;
2. root `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER_V2.md` and the active programme plan;
3. `tests/AGENTS.override.md` and every prerequisite it names;
4. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
5. every current routed normative source relevant to P2;
6. the complete normative proposition register and Gate C requirement register;
7. accepted PM-001–PM-010 decision registers and their exact source locators;
8. `config/retained_test_registry.yaml` and `config/proof_blocks.yaml`; and
9. every PM-011 file.

Create:

```text
project_control/canonical_project_manager/P2_CLEAN_REVIEW_FULL_READ_MANIFEST.tsv
```

Search, snippets, headings, line counts, AST output, summaries and generated manifests may assist navigation. They do not satisfy a full-read requirement.

## 5. Absolute semantic-read ledger

### 5.1 Controlling file

Use the pre-created ledger:

```text
project_control/canonical_project_manager/P2_ABSOLUTE_SEMANTIC_READ_LEDGER.tsv
```

It contains exactly one row for each physical test file and begins with all 179 rows set to `NO`.

Columns:

```text
SEQUENCE
ALLOCATED_UNIT
TEST_PATH
SEMANTICALLY_READ
RECEIPT_PATH
ASSERTION_GROUP_COUNT
RELATIONSHIP_COUNT
FINAL_FILE_DISPOSITION
STATUS_NOTE
```

### 5.2 Meaning of `YES`

`SEMANTICALLY_READ=YES` means only that the worker claims the prescribed complete file cycle in section 7 was performed and identifies its manual receipt.

It is a process record, not proof of correctness and not acceptance.

Set a row to `YES` only after its receipt is complete. If later evidence invalidates the receipt, reset the row to `NO`, reread the affected material and repair it.

### 5.3 Serial-write control

One semantic write operation may create or revise only:

- one test-file receipt; and
- that file's single ledger row.

No write operation may add, close or rewrite multiple test-file receipts or multiple semantic ledger rows. Mechanical validators may check the ledger but may not write semantic fields.

## 6. Fixed execution order

Process units strictly in this order. Within each unit, process test paths in repository-relative lexical order.

| Unit | Family | Files |
|---|---|---:|
| PM-012 | upstream inputs and preparation | 39 |
| PM-013 | serial cognition, playbook, capital and entry | 19 |
| PM-014 | Parallel Risk and specimens | 36 |
| PM-015 | persistence, options and downstream lifecycle | 33 |
| PM-016 | review, replay, API, egress and observability | 14 |
| PM-017 | vocabulary, normative tests, migration and legacy containment | 25 |
| PM-018 | Tier B shadow | 13 |

The allocation source is PM-011. Nearest-label similarity does not decide ownership.

Do not open the next unit until every ledger row allocated to the current unit is `YES` and its unit receipt accurately records unresolved blocks.

## 7. One-file semantic cycle

For one test file only:

### 7.1 Read the complete test

Read every import, fixture, helper, parametrisation, setup/teardown path, monkeypatch, assertion, expected exception, comment, docstring and neighbouring test.

Restate in your own words:

- starting state or input;
- action performed;
- exact surface observed;
- exact asserted output, mutation or failure;
- distinct assertion groups; and
- surfaces the test never observes.

### 7.2 Read the exercised surfaces

Read every directly relevant implementation, schema, fixture, configuration, registry, generated artefact or repository text surface in full. Follow helpers and imports far enough to understand what each assertion actually exercises.

Do not infer behaviour from a filename, symbol, import or mock.

### 7.3 Discover authority from meaning

Start from observed behaviour, not from terminology or an existing registry route.

Read the complete candidate authority document and the full proposition context needed to understand owner, lifecycle stage, conditions, exclusions and abstraction level.

For a composite proposition, enumerate every required conjunct. The test proves the whole proposition only if its assertions prove every conjunct. Otherwise use only an exact separable clause, if one exists.

### 7.4 Decide every assertion group separately

For each proposed test–proposition relationship, record:

1. exact test and assertion locator;
2. exact proposition ID and source locator;
3. test behaviour in plain English;
4. authority meaning in plain English;
5. why owner, stage, boundary and abstraction match or do not match;
6. exact behaviour proved;
7. what is not proved;
8. one falsifier that changes the exact surface observed by the named assertion;
9. the assertion that must fail and why;
10. semantic relation;
11. proof strength; and
12. disposition and return gate.

Allowed semantic relations:

- `exact_full_proof`
- `bounded_separable_clause`
- `related_but_not_proved`
- `no_semantic_fit`
- `authority_missing`
- `authority_contradictory`

Allowed proof strengths:

- `behavioural`
- `boundary`
- `state_transition`
- `identity_lineage`
- `substitution`
- `replay`
- `presence_only`
- `signature_only`
- `token_only`
- `specimen_only`
- `historical_observational`

Allowed final file dispositions:

- `ADMIT_TIER_A_CURRENT`
- `ADMIT_TIER_B_SHADOW`
- `BLOCKED_P3_REPAIR`
- `BLOCKED_MISSING_NORMATIVE_AUTHORITY`
- `NON_AUTHORITATIVE_OBSERVATIONAL`
- `RETIREMENT_RECOMMENDED_NOT_EXECUTED`

### 7.5 Challenge the relationship

Return to authority first and describe an implementation that violates the cited proposition while preserving everything the test does not inspect.

Then reread the exact assertions and answer:

> Would this test necessarily fail?

Name the failing assertion. If none necessarily fails, narrow, demote, block or reject the relationship.

This is an internal adversarial challenge. Do not call it independent review.

### 7.6 Write one receipt and close one row

Create one manually authored receipt:

```text
project_control/canonical_project_manager/units/<PM-unit>/semantic_receipts/<test-path-slug>.md
```

The receipt contains the complete file restatement and one separately reasoned relationship section for every assertion group. If no lawful relationship exists, state `NO_VALID_AUTHORITY_RELATIONSHIP` and explain why.

Only after the receipt is complete:

1. update that file's one ledger row to `YES`;
2. record counts and disposition;
3. validate that exactly one receipt and one ledger row changed; and
4. continue to the next file without returning to the user.

## 8. Semantic rules and measured failure patterns

### 8.1 Core rules

- Related does not mean proved.
- Shared vocabulary, architectural adjacency, downstream use and subsystem membership do not establish authority.
- Current code and passing tests are observations, not normative authority.
- Directory placement does not establish tier.
- Builder/generated parity does not prove human-authority completeness.
- Presence, signature, token and specimen checks must not be described as behavioural proof.
- Usefulness is not authority.

### 8.2 Reject these repeated failure patterns

Before closing each receipt, test it against:

1. lexical similarity substituted for meaning;
2. downstream join law used as lane-internal authority;
3. wrong owner, lifecycle stage or abstraction level;
4. one fragment treated as proof of a composite proposition;
5. builder parity treated as completeness;
6. admitted and quarantined requirements reversed;
7. a falsifier aimed at a surface the test never observes;
8. generic or copied reasoning reused across unrelated relationships;
9. previous counts preserved as targets;
10. structural validation described as semantic acceptance; and
11. absolute worker paths or extraction-location assumptions.

Any hit keeps the ledger row at `NO` until repaired.

## 9. Automation boundary

Automation may perform only deterministic work such as:

- inventories, hashes and counts;
- test collection and execution;
- path and locator validation;
- schema and enumeration validation;
- projection of already-written identifiers and dispositions; and
- archive and manifest verification.

Automation must not:

- select or infer authority;
- group assertions semantically;
- write or rewrite test/authority restatements;
- generate limitations, falsifiers, proof strengths or dispositions;
- mark `SEMANTICALLY_READ=YES`;
- copy one rationale across rows; or
- certify semantic correctness.

If any script or bulk transformation writes semantic content, invalidate the affected rows to `NO` and redo them manually.

## 10. PM-019 integration

Do not begin PM-019 until all 179 ledger rows are `YES`.

Build current test-authority, proposition-traceability, proof and dependency registers only from the completed receipts. Mechanical projection may copy explicit identifiers, paths, locators, classifications, dispositions and counts. It may not generate semantic rationale or change a decision.

PM-019 must demonstrate mechanically:

- all 179 physical files occur exactly once;
- every assertion group has a recorded disposition;
- every retained relationship resolves to an exact authority locator;
- blocked files name an exact deficit and return gate;
- no rejected relationship is restored through a generic substitute; and
- all counts derive from current evidence rather than historical targets.

Every PM-019 validator output must state:

```text
Structural validation does not establish semantic acceptance.
```

Only after the registers agree may the worker update `config/retained_test_registry.yaml` and `config/proof_blocks.yaml` as mechanical projections of the decisions. No other tracked project file may change.

## 11. PM-020 validation and packaging

Validate:

1. physical file discovery and PM-011 hash continuity;
2. ledger completeness and one-to-one receipt coverage;
3. required fields and allowed enumerations;
4. authority-ID and source-locator resolution;
5. repository-relative exercised paths;
6. exact PM-019 projection;
7. expected-red node correspondence with Gate D obligations;
8. no unexpected failure, skip, `xfail` or collection error;
9. tracked-file mutation limited to authorised projections;
10. one authoritative current count set; and
11. reproduction from a fresh extraction at an arbitrary path.

Run targeted tests, complete Tier A, Tier B shadow and required proof routes without suppression. Preserve raw output.

If the locked CPython 3.13.5 environment cannot initialise because the external package gateway fails, record that route as `Unknown`, preserve the exact error and continue all other lawful validation.

Package the complete repository, including `.git`, with:

- a repository file manifest;
- branch, HEAD and dirty-state evidence;
- tracked diff and changed-path list;
- raw validation outputs;
- open defects and Unknowns;
- archive checksum; and
- a safe-extraction verification log.

Packaging does not establish acceptance.

## 12. Continuation and hard blockers

Do not stop because a relationship is difficult, authority is absent for one test, a test is red, a count changes, a unit closes, or a validator/package exists. Record the lawful blocked disposition and continue.

Stop early only when one condition prevents all remaining lawful work:

1. wrong baseline;
2. required governing source is unavailable;
3. material authority is contradictory and cannot be resolved by the hierarchy;
4. tool/runtime failure remains after safe recovery and blocks all remaining work;
5. further work requires destructive or out-of-scope authority; or
6. observable context failure makes truthful semantic continuation impossible.

A hard-block return must state:

- last completed file and next required file;
- ledger `YES` and `NO` counts;
- exact blocker and evidence;
- authority and files inspected;
- recovery attempts;
- work still executable, if any; and
- exact missing input or authority required.

## 13. Completion standard

Return a P2 candidate only when:

- the baseline gate passed;
- all 179 ledger rows are `YES`;
- every assertion group has an honest disposition;
- every retained relationship has exact assertion and authority locators, a bounded claim, an honest limitation and an exact-surface falsifier;
- every relationship survived the internal challenge or was narrowed, blocked or rejected;
- no semantic content was script-generated or batch-written;
- PM-019 exactly reflects the receipts;
- PM-020 structural and behavioural validation ran as far as the environment lawfully allowed;
- all mutations stayed inside scope;
- one current archive and count set was returned; and
- P3 remained closed.

Closeout must state separately:

```text
Verified
Failed
Unknown
Blocked
Git state
Validation executed
Artefacts returned
Next Project Manager gate
```

Do not claim `P2 accepted`. State `P2 candidate returned for independent Project Manager audit`.
