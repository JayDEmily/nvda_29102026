# Architecture Kernel Reset ExecPlan

## Status

**Active** on branch `work/architecture-kernel-reset-v1`.

Current unit: Unit 5 — packaging, environment and closeout.

## Objective

Execute `docs/architecture/ARCHITECTURE_KERNEL_RESET_BRIEF.md` from immutable base commit `d24f9626a23b526384668b3cb26ee811b235eb5c` and produce a minimal, behaviour-neutral, extensible architecture kernel while preserving full Git history.

## Authority

1. Direct user instruction dated 2026-08-04 to create the branch, adopt the rewritten brief and execute it.
2. `docs/architecture/ARCHITECTURE_KERNEL_RESET_BRIEF.md`.
3. Applicable existing root and test override authority until replaced by the brief.
4. Reusable laws extracted from the architecture, testing, vocabulary, protocol and technical-architecture documents listed in the full-read manifest.
5. The supplied architecture and test-lineage audit as historical evidence only.

Immutable baseline: `d24f9626a23b526384668b3cb26ee811b235eb5c`.

Current full-read manifest: `docs/evidence/architecture_kernel_reset_20260804/FULL_READ_MANIFEST.tsv`.

## Scope

In scope:

- active-tree reset;
- architecture taxonomy and registries;
- schemas and templates;
- minimal registry/composition code;
- architecture, bootstrap and promotion-control proof;
- minimal packaging and lock regeneration;
- audit and lineage evidence;
- bounded commits and full-history handoff archive.

Out of scope:

- business capability design;
- DMPV3 schema or runtime behaviour;
- state/transaction implementation;
- migration of historical module behaviour;
- live trading or production-readiness claims;
- merging or pushing the branch.

## Invariants and prohibited shortcuts

- Preserve Git history; no rebase, squash, orphan branch or history rewrite.
- Do not archive removed implementation inside the active tree.
- Do not pre-populate runtime modules or surfaces.
- Do not create fictional placeholder implementation.
- Do not claim that registry presence proves implementation.
- Do not weaken an old assertion to make it green; old behavioural proof is superseded and removed as a whole by direct authority.
- No fixed object-count limit, identifier enum or identifier-specific dispatch.
- Python public-seam enforcement must be repository-owned and mechanical.
- Mechanical proof does not establish future domain semantics.

## Acceptance units

### Unit 1 — Authority and branch activation

Pass: branch, brief, plan, full-read manifest and live pointer identify the exact reset authority and baseline.

Allowed changes: control surfaces and reset evidence only.

Validation: Git state, hashes, manifest completeness and diff check.

### Unit 2 — Active-tree strip-down

Pass: inherited production, behavioural tests, old admissions, ledgers, receipts, migration artefacts and stale overlays are absent from the active tree; legal and minimal bootstrap assets remain.

Allowed changes: repository-wide deletions and minimal directory scaffolding.

Validation: deleted/retained inventories and forbidden-path scans.

### Unit 3 — Architecture kernel authority and registries

Pass: taxonomy, dependency, public-seam, lifecycle and extension laws are explicit; registries and schemas support unbounded identifiers; modules and surfaces are empty; P01/G01/G02/A00/K01 are truthful placeholders/framework identities.

Allowed changes: `docs/architecture/**`, `docs/history/**`, `config/**`, `schemas/**`, `templates/**`.

Validation: schema and registry checks including M99→M100 and retired-ID non-reuse.

### Unit 4 — Minimal implementation and proof framework

Pass: registry loading, composition rejection, import/dependency/public-seam checking, proof admission and aggregate promotion execute without inherited business behaviour.

Allowed changes: `src/**`, `tools/**`, `tests/**`, `Makefile`, minimal CI.

Validation: architecture tests, bootstrap tests, static checks and promotion gate.

### Unit 5 — Packaging, environment and closeout

Pass: minimal dependencies and regenerated lock install cleanly; built artefact imports outside repository; no former package is included; all required validation passes; commits, inventories, logs and archive are complete.

Allowed changes: packaging, lock, evidence, plan closeout and README/AGENTS.

Validation: exact commands recorded in `docs/evidence/architecture_kernel_reset_20260804/validation/`.

## Required final validation

- `uv sync --locked --extra dev` in a clean environment;
- build wheel and sdist;
- install wheel into an isolated environment outside the repository and import `nvda_desk`;
- `python tools/validate_architecture.py`;
- `python tools/check_dependencies.py`;
- `python tools/check_public_seams.py`;
- architecture/bootstrap tests;
- authoritative aggregate promotion gate;
- forbidden legacy import and package-content checks;
- `git diff --check d24f9626a23b526384668b3cb26ee811b235eb5c..HEAD`;
- `git fsck --full`;
- final clean-worktree check.

## Evidence and artefacts

Evidence root: `docs/evidence/architecture_kernel_reset_20260804/`.

Required artefacts:

- full-read manifest;
- retained and deleted inventories;
- final tree;
- validation command and output logs;
- lineage index;
- commit and Git-state receipt;
- full-history tarball and SHA-256.

## Progress

- Unit 1: completed; evidence in `docs/evidence/architecture_kernel_reset_20260804/validation/unit1_control_activation.txt`.
- Unit 2: completed; 5,962-file baseline classified and inherited active implementation removed. Evidence: `docs/evidence/architecture_kernel_reset_20260804/BASELINE_FILE_INVENTORY.tsv` and `validation/unit2_strip_down.txt`.
- Unit 3: completed; architecture authority, schemas, registries, templates, crosswalk and lineage index created. Validation: `docs/evidence/architecture_kernel_reset_20260804/validation/unit3_registry_schema_validation.txt`.
- Unit 4: completed; generic registry, composition, dependency/public-seam enforcement and exact proof control implemented. Validation: `docs/evidence/architecture_kernel_reset_20260804/validation/unit4_implementation_and_proof.txt`.
- Unit 5: active.

## Decisions

- The direct brief supersedes the former business implementation and proof population on this branch.
- Existing tests are not edited to fit the reset; they are retired from the active tree and remain intact in Git history.
- `PLANS.md` is the active task-specific ExecPlan for this reset.

## Roadblocks

- The first offline lock attempt required a Windows-only `colorama` artefact that is absent from the supplied Linux wheelhouse. The minimal lock is therefore explicitly constrained to Linux x86_64, matching the supplied CPython 3.13.5 wheelhouse; final proof remains pending.

## Unknowns

- Whether any legal or packaging metadata outside the brief must be retained; preserve `LICENSE` and record any additional bounded retention.

## Closeout

Open. Final verdict pending Units 1–5.
