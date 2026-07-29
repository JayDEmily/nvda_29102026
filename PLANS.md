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

1. direct user instruction and explicit user acceptance;
2. the accepted project brief and any explicit user-approved strategy amendment;
3. applicable `AGENTS.override.md` and repo-root `AGENTS.md`;
4. the active task-specific ExecPlan and its live roadmap pointer;
5. routed normative intent, accepted architecture allocations, semantic vocabulary authority and approved specifications;
6. admitted test/proof authority;
7. source, configuration, schemas, fixtures, generated data, comments and docstrings;
8. ledgers, receipts, reports, manifests, generated projections and historical evidence;
9. `00_TASK/PROJECT_EXECUTION_METHOD.md` only where higher authority is silent.

This standing plan defines plan-selection and live-pointer conventions; it does not silently alter an accepted brief or applicable repository instruction. Lower surfaces cannot create or override higher authority. Generated artefacts, test location, historical receipts, green tests, Atlas rows and current code are evidence only for the claims they actually prove. An accepted Atlas ownership map governs architecture only to the extent expressly adopted by the active ExecPlan and routed architecture documents; it does not automatically admit Atlas behavioural content.

## Plan selection

Continue an existing active task-specific ExecPlan when its objective, baseline, authority, and acceptance units still govern the requested work.

Create and activate a new task-specific ExecPlan when:

- the user opens a materially new programme or authority class;
- the current plan is closed or explicitly superseded as a whole;
- a prior plan cannot lawfully contain the new outcome; or
- a concrete control defect requires a successor plan.

Amend the existing active ExecPlan instead when the user explicitly changes strategy inside the same programme and requires existing control surfaces to remain the single source of authority. The amendment must state which prior decisions and evidence remain valid, which clauses are superseded, and why. Do not silently replace or silently reinterpret an active plan.

## Required task-specific ExecPlan content

Every active task-specific ExecPlan must record:

- status and current unit;
- exact objective and non-goals;
- authority and immutable baseline;
- in-scope and out-of-scope surfaces;
- invariants and prohibited shortcuts;
- semantic acceptance units, lane allocation where applicable, and prerequisites;
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

The default route permits only one mutating unit. The accepted parallel-workflow amendment may instead open one bounded mutating unit in each PM-controlled lane when the active ExecPlan records dependency readiness, disjoint semantic ownership, exact read/write sets, shared locks and a common canonical base. Unit numbering is a traceability identifier, not automatic execution order.

Parallel worker and tester activity does not parallelise canonical authority. The Project Manager accepts and integrates one approved assignment at a time, reruns affected and aggregate proof, then publishes the next canonical checkpoint. A lane may never choose or continue into its own next unit.

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

A worker must not receive the entire programme as its task, select follow-on work, broaden its unit, alter root control surfaces, or claim programme completion. A PM-issued lane uses the exact thread label `Lane <number><letter>W`; its independent tester uses `Lane <number><letter>T`. Each assignment uses a fresh short-lived branch from the named canonical base. The Project Manager reviews the returned files/diff and tester evidence before acceptance and serial integration. The brief must name the assignment revision, exact Worker Candidate Archive and exact tester verdict artefacts; a PASS tester return must include a reconstructable Git bundle, manifests, hashes, claims, verdict and raw validation rather than an informal archive.

## Vocabulary, tests, and Atlas

- Human-readable accepted vocabulary meaning precedes builder code and generated JSON.
- Semantic admission cannot be automated from string similarity, a scanner, a builder seed, or Atlas evidence.
- Test tier and authority require an explicit current route; folder placement is insufficient.
- A green test proves only its exercised assertion and can still be weak or false-positive.
- Atlas behavioural content is candidate intent. It enters tests or code only after normative and vocabulary admission and exact current mapping.
- A formally accepted Atlas ownership/module allocation may govern target placement without admitting every contributing cohort as behaviour.
- Every accepted Atlas behaviour preserves source-record and cohort traceability; missing evidence blocks only the dependent module or behaviour, not unrelated dependency-ready modules.

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
