# PROJECT_EXECUTION_METHOD.md

Version: 2026-07-17  
Purpose: fallback execution method for long-running repository, coding, migration, sandbox, document, workbook and audit work.

This file exists to prevent semantic drift, premature closure, false completion claims, registry-only proof, unnecessary pauses, silent authority changes and automated substitutes for human semantic judgement.

It is method guidance. It is not live domain authority.

---

## 1. Activation

Use this method when work involves one or more of the following:

- a repository, branch, worktree, archive, patch or codebase;
- a long-running sandbox task;
- an implementation, migration, reconciliation or repair;
- a semantic audit or coverage claim;
- a plan, gate, leaf, row-set, ledger or acceptance decision;
- durable files or artefacts that must survive handoff;
- work requiring traceability, validation or Git history.

Read applicable `AGENTS.override.md`, `AGENTS.md` and task plans before acting.

If an active task-specific ExecPlan already exists, continue it. Do not restart merely because the task is complex.

Create a new ExecPlan only when:

1. the user authorises it;
2. repository instructions require it; or
3. the task explicitly asks for one.

Do not assume a file named `PLANS.md` is the active plan. It may be a specification for how plans must be written. Inspect its contents and follow the repository’s convention.

---

## 2. Authority order

Apply authority in this order:

1. the user’s current instruction and explicit approvals;
2. the accepted task brief, hard launch block or agreed scope;
3. applicable `AGENTS.override.md` and `AGENTS.md`;
4. the active task-specific ExecPlan;
5. normative documents and approved specifications;
6. tests;
7. source, configuration, fixtures and data;
8. ledgers, registries, receipts, logs and historical artefacts;
9. this fallback method where higher authority is silent.

Rules:

- A plan must not silently rewrite an accepted brief.
- A ledger, receipt or generated artefact must not rewrite normative intent.
- Downstream implementation evidence does not become upstream semantic authority.
- Resolve material contradictions before relying on the disputed instruction.
- Do not invent missing authority.

---

## 3. Execution mode

Determine the mode from the user’s request and the governing brief.

### 3.1 Interactive mode

Use for planning, diagnosis, audit discussion, ambiguous scope or work where the user asks for staged updates.

Before non-trivial action, state only:

- outcome;
- allowed effects;
- pass/fail criterion;
- first gate.

After a gate, report:

```text
Known true:
Ruled out:
Next gate:
```

Keep this compact. Do not turn a simple task into process theatre.

### 3.2 Uninterrupted execution mode

Treat instructions such as “execute”, “continue”, “do the work”, “complete the brief” or “keep working” as authority to continue through safe in-scope work unless the user requests live updates.

In this mode:

- do not emit an upfront plan or preamble merely to announce work;
- do not return after an ordinary gate passes;
- record gates, decisions, progress and validation in the active plan, ledger or receipts;
- continue until the authorised scope is exhausted or a genuine stop condition occurs.

Do not claim work continues after returning a response. Complete the current run or report the actual blocker.

### 3.3 Planning only

- Do not mutate source or durable project files unless authorised.
- Preserve raw intent.
- Define scope, authority, acceptance, order, validation, artefacts and stop conditions.
- Do not jump directly from vague brainstorm to implementation leaves where an accepted brief or plan is required.

### 3.4 Audit only

- Do not patch unless authorised.
- Treat prior summaries and completion claims as claims to verify.
- Report one material defect per row or finding.
- Separate `Verified`, `Inferred`, `Unknown` and `Blocked`.

### 3.5 Structural triage only

Allowed:

- inventories;
- search;
- dependency maps;
- AST/schema extraction;
- line and row counts;
- surface maps.

Structural triage is reconnaissance. It does not prove:

- full review;
- semantic equivalence;
- correctness;
- implementation completion;
- final acceptance.

### 3.6 Closeout or handoff

- state exactly what changed;
- provide evidence;
- list open defects and Unknowns;
- preserve patches, archives and reports;
- record Git and validation state;
- do not claim completion unless the acceptance criteria pass.

---

## 4. Instruction economy

State recurring method rules once in this file.

Do not copy this entire method into:

- custom instructions;
- every task brief;
- every ExecPlan;
- every gate;
- every receipt.

Task files should contain only task-specific authority, scope, decisions, exceptions and evidence.

Retain examples or explicit prohibitions when they correct a measured failure. Do not delete proven controls merely to make the prompt shorter.

---

## 5. Semantic reading rule

When a task requires semantic coverage, equivalence, authority, reconciliation, acceptance or full review, read the in-scope material in full.

The following may assist navigation and validation but do not constitute semantic reading:

- filenames;
- headings;
- snippets;
- summaries;
- search or grep output;
- Python scripts;
- AST extraction;
- embeddings;
- manifests;
- counts;
- schema extraction;
- generated registries.

Automation may perform deterministic work such as:

- inventory;
- counting;
- filtering;
- joining;
- deduplication;
- formatting;
- mechanical validation.

Automation must not certify:

- semantic equivalence;
- semantic absence;
- authority;
- intent preservation;
- final acceptance.

If a file or row was not read in full, do not claim that it was.

If full reading is impossible because required material is unavailable, identify the missing material and classify the task as blocked rather than silently downgrading the standard.

---

## 6. Semantic acceptance unit

Work one semantic acceptance unit at a time.

The unit may be:

- one gate;
- one leaf;
- one row or bounded row-set;
- one behaviour;
- one contract;
- one independently provable surface.

The unit is defined by meaning and acceptance, not by whichever file boundary is convenient.

Within one unit:

1. identify governing authority;
2. read the required material;
3. state or record pass/fail;
4. inspect existing tests and implementation;
5. make the smallest lawful change;
6. validate the target behaviour;
7. record evidence;
8. commit where appropriate;
9. continue to the next authorised unit.

Deterministic inventory or validation may be batched. Semantic adjudication and final acceptance may not.

---

## 7. Documents, tests and implementation

Use the following direction of authority:

```text
normative documentation
→ tests
→ source/configuration/fixtures
```

Where required behaviour is missing or materially ambiguous:

1. establish or update authorised normative documentation;
2. add or update tests that express the requirement;
3. implement the behaviour;
4. validate the target surface.

Do not change normative meaning merely to make current code or tests pass.

Do not weaken tests to fit an implementation defect.

---

## 8. ExecPlan rules

An ExecPlan is a living operational record, subordinate to the accepted brief and repository authority.

Minimum contents:

```md
# [Task] ExecPlan

## Status
planning / active / blocked / closed

## Objective
Exact required outcome.

## Authority
Governing user instruction, brief, AGENTS files, normative documents and baseline.

## Scope
In scope:
- ...

Out of scope:
- ...

## Invariants
Requirements that must not change.

## Acceptance units
### Unit 1: [name]
Pass:
Fail:
Required reads:
Allowed changes:
Validation:
Artefacts:

## Progress
Dated or sequenced execution entries.

## Decisions
Material decisions and evidence.

## Roadblocks
Issue, classification and resolution.

## Validation
Commands, tests and observed output.

## Artefacts
Patches, commits, reports and archives.

## Unknowns
Unresolved matters.

## Closeout
Completed, verified, blocked and remaining.
```

Rules:

- Keep the ExecPlan current.
- Record discoveries that change execution.
- Do not use it to invent authority.
- Do not mark progress complete without evidence.
- During uninterrupted execution, log gates here rather than returning to the user.

---

## 9. Evidence and claim discipline

Never claim `reviewed`, `fixed`, `implemented`, `passed`, `complete`, `verified`, `aligned` or `clean` without evidence.

Accepted evidence includes:

- exact path and line range;
- diff;
- command output;
- test output;
- commit hash;
- generated artefact;
- read receipt;
- current official documentation.

Where proof is unavailable, label the claim:

- `Inferred`;
- `Unknown`; or
- `Blocked`.

Smooth prose is not evidence.

---

## 10. Target-surface completion

A registry, ledger, receipt, index, generated row, checklist or proof-block pass is not implementation proof by itself.

Completion requires evidence in the actual target surface, as applicable:

- behavioural tests;
- source/configuration/fixture behaviour;
- exact paths and lines;
- passing validation;
- unit-specific rationale;
- replay or lineage evidence.

Do not close work using only:

- a registry entry;
- a status field;
- a broad receipt;
- grouped satisfaction;
- “already covered” without exact evidence;
- tests that prove only that the registry exists.

Checkpoint passed does not mean task complete.

---

## 11. Suppression prohibition

Do not make validation appear green by suppressing evidence.

Forbidden unless explicitly authorised and justified:

- `skip` or `xfail`;
- weakened assertions;
- deleted or renamed tests to avoid collection;
- narrowed discovery;
- fake fixtures;
- swallowed exceptions;
- placeholder implementations labelled complete;
- proof or vocabulary suppression;
- edited generated validation artefacts;
- monkeypatches that bypass real behaviour;
- broad coverage exclusions.

A changed test must become more accurate or stricter, not weaker.

---

## 12. Roadblocks

Classify each roadblock as fixable or hard.

### 12.1 Fixable roadblocks

Examples:

- failing tests;
- import or path errors;
- missing exports;
- schema mismatch;
- stale fixture;
- vocabulary admission issue;
- proof-block failure;
- formatting or lint failure;
- ambiguity resolvable from in-scope authority.

Required action:

1. inspect authority, tests and source;
2. identify the cause;
3. make the smallest lawful fix;
4. rerun validation;
5. continue.

Do not stop for fixable roadblocks during uninterrupted execution.

### 12.2 Hard blockers

Stop only when the issue cannot be resolved lawfully inside authorised scope, including:

- required authority or source artefact is missing;
- required external data, credential or dependency is unavailable;
- destructive or external action needs approval;
- repository authority forbids the action;
- all remaining work depends on a blocked prerequisite;
- tool or context state is unsafe and risks false claims or work loss.

When blocked, report:

- the blocker;
- evidence;
- material inspected;
- why it cannot be fixed in scope;
- the exact item or approval required.

---

## 13. Stop condition

Do not stop merely because:

- one gate or unit passed;
- a test failed;
- an import broke;
- a path moved;
- a fixture is stale or missing;
- a vocabulary or proof check failed;
- a row is difficult;
- the next step is harder;
- a polished summary is available.

Stop only when:

1. authorised scope is exhausted and acceptance passes;
2. the governing brief explicitly requires a check-in;
3. a genuine hard blocker exists;
4. continuing would risk false claims or work loss.

---

## 14. Git and artefact preservation

For repository work:

- identify branch, HEAD and status before mutation;
- use a worker branch unless governing instructions say otherwise;
- keep commits semantically bounded;
- commit after each completed acceptance unit where feasible;
- do not merge to `main` without required audit and validation;
- record baseline and final commit;
- report changed files and clean/dirty state.

Before closeout, preserve useful work through one or more of:

- Git commits;
- patch or diff;
- changed-file archive;
- generated report;
- updated durable files;
- command and validation logs;
- artefact manifest.

If Git is unavailable, create equivalent durable evidence.

---

## 15. Official-source escalation

For uncertainty about OpenAI, APIs, SDKs, dependencies, cloud services, platforms or vendor-specific behaviour:

1. consult current authoritative documentation;
2. use official sources for that vendor or upstream project;
3. record the source in the decision log;
4. distinguish documented fact from inference.

For OpenAI, ChatGPT, Codex and the OpenAI API, use current official OpenAI sources only unless the user explicitly requests otherwise.

---

## 16. Closeout standard

The task may be called complete only when all applicable conditions pass:

- required authority was read;
- required semantic material was read in full or authorised triage was used;
- acceptance units were completed individually;
- work remained in scope;
- material claims have evidence;
- required tests and checks ran;
- target-surface behaviour is proved;
- no suppression was used;
- Git and artefacts are preserved;
- open defects and Unknowns are listed;
- the active plan is closed accurately.

Closeout must state:

```text
Outcome:
Authority used:
Acceptance completed:
Validation:
Commits/Git state:
Artefacts:
Open defects:
Unknowns:
```

---

## 17. Failure patterns to correct immediately

Correct the process if the worker:

- substitutes search or scripts for semantic reading;
- treats filenames, headings or snippets as full review;
- batches semantic units because they appear similar;
- treats a plan, ledger, registry or receipt as target behaviour;
- creates a plan without authority;
- emits a preamble and stops during uninterrupted execution;
- reports every gate to the user when it should be logged internally;
- claims tests passed without output;
- claims alignment without line-level evidence;
- weakens validation to achieve green status;
- stops at an ordinary fixable roadblock;
- restarts completed work without evidence that it is invalid;
- invents missing requirements;
- optimises for plausible closure instead of evidenced completion.

---

## 18. Final rule

Use less repeated process language, not less discipline.

Optimise for evidenced completion.
