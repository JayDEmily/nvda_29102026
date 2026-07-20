# PLANS.md — Governed Execution Standard

## Status and purpose

This standing plan is accepted under the user's 2026-07-20 instruction to establish a Project Manager thread, complete the placeholder plan, and manage later worker threads through bounded standalone briefs.

`PLANS.md` defines how project plans are selected and executed. It is not a mutable progress log and does not define trading-system meaning. Current state belongs in `ROADMAP_LEDGER_V2.md`; task detail belongs in the active task-specific ExecPlan.

## Live route

1. Read `AGENTS.md` in full.
2. Read this file in full.
3. Read the retirement pointer in `ROADMAP_LEDGER.md` and then the live successor `ROADMAP_LEDGER_V2.md` in full.
4. Follow the single active ExecPlan named by `ROADMAP_LEDGER_V2.md`.
5. Read every applicable route override, normative document, proof authority, and directly affected file in its lawful order before mutation.

The active programme at acceptance is:

- plan: `project_control/canonical_project_manager/EXEC_PLAN.md`;
- live pointer: `ROADMAP_LEDGER_V2.md`;
- full-read evidence: `project_control/canonical_project_manager/FULL_READ_MANIFEST.tsv`;
- validation evidence: `project_control/canonical_project_manager/VALIDATION_LOG.md`.

If the live pointer and a task-local plan disagree, stop behavioural mutation, record the conflict, and return to control authority. Historical files that still use the word `active` do not displace the live pointer.

## Authority and truth order

For the canonical programme, apply:

1. direct user instruction;
2. accepted project brief and execution method named by the active plan;
3. repository instructions;
4. this standing plan and the live roadmap pointer;
5. the active task-specific ExecPlan;
6. routed normative intent and semantic vocabulary authority;
7. admitted test/proof authority;
8. source, configuration, fixtures, generated data, comments, and docstrings.

Lower surfaces cannot create or override higher authority. Generated artefacts, test location, historical receipts, green tests, Atlas rows, and current code are evidence only for the claims they actually prove.

## Plan selection

Continue an existing active task-specific ExecPlan when its objective, baseline, authority, and acceptance units still govern the requested work.

Create and activate a new task-specific ExecPlan when:

- the user opens a materially new programme or authority class;
- the current plan is closed or explicitly superseded;
- the baseline or fixed execution order changes materially;
- a prior plan cannot lawfully contain the new outcome; or
- a concrete control defect requires a successor plan.

Do not silently replace an active plan. The successor must state which prior decisions/evidence remain valid, what is superseded, and why.

## Required task-specific ExecPlan content

Every active task-specific ExecPlan must record:

- status and current unit;
- exact objective and non-goals;
- authority and immutable baseline;
- in-scope and out-of-scope surfaces;
- invariants and prohibited shortcuts;
- serial acceptance units and prerequisites;
- pass/fail conditions;
- exact required reads;
- exact allowed and forbidden files;
- evidence locations and artefact names;
- targeted and aggregate validation commands;
- return gates and stop conditions;
- progress, decisions, roadblocks, validation, unknowns, and closeout;
- the current full-read manifest;
- treatment of any prior active plan and historical evidence.

An ExecPlan may organise work. It may not invent normative meaning, test authority, Atlas admission, or implementation status.

## Semantic acceptance units

One unit is one governed behaviour and its proof boundary. A unit is not defined merely by a file, folder, class, issue, worker, or Atlas cohort.

Only one mutating unit may be open. A later unit waits for acceptance and a clean checkpoint even if it appears graph-independent. Parallel work requires an explicit amendment to the active ExecPlan.

For every unit:

1. confirm prerequisites, clean preceding checkpoint, and exact authority;
2. state input → decision/transformation → output in plain English;
3. confirm owner, identity, time, state, side effects, replay, and prohibited authority;
4. assess only mapped Atlas evidence and admit nothing automatically;
5. complete the pre-change semantic vocabulary audit;
6. establish trustworthy behavioural proof before implementation;
7. decide retain, refactor, behavioural-reference-only, replace-boundary, replace-core, or remove/quarantine for each affected bounded component;
8. implement the smallest semantically complete change;
9. validate in increasing scope;
10. complete the post-change semantic vocabulary audit from the actual diff;
11. record evidence and create one bounded checkpoint before opening the next unit.

## Worker-thread rules

The Project Manager owns scheduling, integration, acceptance, and programme claims.

A worker brief must be a standalone Markdown file and must contain only the bounded context necessary for one unit:

- unit ID and exact outcome;
- current baseline/branch and active plan;
- governing propositions and read order;
- exact inputs, outputs, and pass/fail boundary;
- exact allowed and forbidden paths;
- required validation and artefacts;
- stop/return conditions;
- a reminder that shared files are live and unrelated changes must be preserved.

A worker must not receive the entire programme as its task, select follow-on work, broaden its unit, alter root control surfaces, or claim programme completion. The Project Manager reviews the returned files/diff and evidence before acceptance.

## Vocabulary, tests, and Atlas

- Human-readable accepted vocabulary meaning precedes builder code and generated JSON.
- Semantic admission cannot be automated from string similarity, a scanner, a builder seed, or Atlas evidence.
- Test tier and authority require an explicit current route; folder placement is insufficient.
- A green test proves only its exercised assertion and can still be weak or false-positive.
- Atlas is candidate intent. It enters tests or code only after normative and vocabulary admission and exact current mapping.
- Every accepted Atlas behaviour preserves source-record and cohort traceability; missing evidence blocks the dependent unit.

## Evidence and validation

Material claims require inspectable evidence: exact paths, hashes, command output, diffs, tests, receipts, manifests, or archives.

Before a checkpoint, run when relevant and available:

- `git status --short --branch`;
- `git diff --check`;
- the unit's targeted positive and prohibited proof;
- affected admitted Tier A proof;
- complete admitted Tier A route;
- Tier B shadow proof;
- proof-block, registry, manifest, schema, static, substitution, state, replay, and archive checks required by the unit.

If a command cannot run, record the exact environmental failure and run the next-best non-equivalent check. Never report `passed` for a command that did not execute.

## Git and packaging

- Preserve unrelated work and audit history.
- Do not merge, rebase, rewrite, push, publish, or open a pull request without explicit authority.
- Prefer one bounded commit per accepted semantic unit.
- A tarball/checkpoint must have a recorded SHA-256 and exact source commit/status.
- Packaging is evidence and handoff convenience, not permission to stop or a completion claim.

## Plan mutation

This file is now a frozen standing control surface. Routine progress must update `ROADMAP_LEDGER_V2.md`, the active ExecPlan, and unit receipts—not this file.

Change `PLANS.md` only when the user explicitly opens it again or a concrete standing-control defect cannot be truthfully resolved elsewhere. Such a change is its own bounded governance unit.
