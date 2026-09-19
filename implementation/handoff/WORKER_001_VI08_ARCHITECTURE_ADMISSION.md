# Worker 001 Brief — VI-08 Minimal Lawful Durable Architecture Admission

## Role

You are the implementation Worker for one bounded unit. Do not act as Project Manager, methodology designer, programme authority or independent reviewer.

## Objective

Implement the already-derived VI-07 architecture-admission design against the supplied skeletal codebase. This assignment admits the Raw Signal Occurrence Truth owner into the existing architecture kernel. It does **not** implement Raw Signal product behaviour.

## Mandatory read order before mutation

Read these in order:

1. root `GUARDRAILS.md` — in full;
2. root `AGENTS.md` — in full;
3. root `EXEC_PLAN.md` — current VI Gate plan and current VI-08 boundary;
4. `implementation/handoff/WORKER_001_VI08_ARCHITECTURE_ADMISSION.md` — this bounded task;
5. `handoff/control/CURRENT_STATE.md` and the G03 files under `handoff/macro_gates/` — macro Gate/Leaf authority only;
6. `handoff/authority/BICP_CANDIDATE_005.md` and `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md` — accepted implementation meaning;
7. `implementation/authority/VI04_AUTHORITY_CLOSURE.md` — explicit owner/package/driver/physical-realisation authority;
8. `implementation/work_order/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md` — only the bounded architecture/owner constraints relevant to VI-08;
9. `implementation/architecture/VI07_ARCHITECTURE_ADMISSION_DESIGN.md` — exact mutation design;
10. `docs/architecture/ARCHITECTURE_KERNEL.md` — in full, including its authority map;
11. `docs/architecture/ARCHITECTURAL_OBJECT_TAXONOMY.md` — normative propositions, `M` and `A` categories, and lifecycle statuses;
12. `docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md` — in full;
13. `docs/architecture/DEPENDENCY_LAWS.md` — in full;
14. `docs/architecture/PUBLIC_SEAM_LAW.md` — in full;
15. `docs/architecture/EXTENSION_AND_RETIREMENT_RULES.md` — normative propositions and runtime-module admission;
16. `docs/architecture/IMPLEMENTATION_AUTHORITY_INGRESS.md` — normative propositions, two-sided admission boundary, brief handling and failure disposition;
17. `docs/architecture/TEST_AND_PROMOTION_KERNEL.md` — in full;
18. inspect the current registries/configs/schemas touched by VI-07 before editing them;
19. inspect the relevant existing architecture/bootstrap tests and `tests/AGENTS.override.md` before changing anything under `tests/`;
20. inspect `pyproject.toml` and `Makefile` for the repository's declared tooling/build surface.

The 2026-08-04 reset brief and 2026-09-02 conformance ADR are historical evidence, not steady-state owners. Read them only if a current invariant requires historical challenge.

## Dependency/environment rule

This packet intentionally contains **no wheelhouse, package archives, dependency payloads, virtual environment or `uv.lock`**. Required dependency artefacts are available separately as attachments to the ChatGPT Project. Locating the applicable attached dependency artefacts and constructing the task-local environment are Worker responsibilities.

Do not infer dependency availability from this packet alone. If a required Project attachment cannot be located or used, report `BLOCKED` with the exact missing requirement.

## Exact baseline

This is a thin native Git transport repository. Its transport commit/tree and source provenance are recorded in the outer `PROVENANCE.md`.

The authoritative pre-implementation source identity remains:

- source commit: `d095954c16a9818eadb60d6364148229f2dc4558`;
- source tree: `7fdb0e5308f3af187134bc3ebf633835748e9475`;
- PM handoff source commit: `7795705727d8ac2935949ba9e4acce672fa463a1`;
- PM handoff source tree: `f34d17bfda83e52f58dfe72760e4f286e083355c`.

Omitted Git history and excluded dependency/cache files are deliberate transport reductions. Do not reconstruct omitted history or treat transport identity as replacement historical ancestry.

Immediately before mutation, rerun implementation-authority ingress against the supplied exact IRB and confirm the projection is still:

```text
create:raw_signal_occurrence_truth->M00, modify:A00
```

If it is not, stop and report `BLOCKED`; do not force `M00`.

## Authorised mutation

Execute the exact VI-07 design only. The expected changed-path set is:

```text
config/architecture/modules.yaml
config/architecture/application_shells.yaml
config/architecture/dependency_rules.yaml
config/architecture/implementation_allocations.yaml
src/nvda_desk/raw_signal_occurrence_truth/__init__.py
src/nvda_desk/raw_signal_occurrence_truth/api.py
implementation/architecture/VI08_ARCHITECTURE_ADMISSION_EVIDENCE.md
```

A path outside that set requires a written reason tied to an actually failing current invariant. Do not make opportunistic adjacent changes.

## Forbidden in this unit

Do not add Raw Signal domain decision logic, PostgreSQL persistence code, product-proof registries, product tests, provider/network integration, replay, P01/DMPV3, K01, downstream consumers, live effects/accounts, packaging/version decisions, or any Remaining-Unknown default.

Do not weaken or rewrite existing architecture proof merely to obtain green.

## Required evidence

Before claiming completion:

1. rerun exact implementation-authority ingress against the supplied IRB;
2. run architecture/schema validation;
3. run the architecture/bootstrap test set;
4. run the architecture promotion gate;
5. run type checking and linting when the Worker has established the required environment from the Project attachments;
6. inspect the final diff and confirm no Raw Signal product behaviour was introduced;
7. write `implementation/architecture/VI08_ARCHITECTURE_ADMISSION_EVIDENCE.md` recording commands, results, changed paths and any limitations;
8. commit the candidate in this supplied Git repository and report the final commit/tree.

A green command proves only the proposition it exercises. Any failed required invariant is a stop condition; report the first failure without weakening the proof.

## Return contract

Return only:

- status: `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED`;
- final Git commit and tree;
- changed paths;
- exact validation commands and concise results;
- any unresolved concern or first blocker.

Do not claim independent review. The PM will route review/test separately after your candidate returns.
