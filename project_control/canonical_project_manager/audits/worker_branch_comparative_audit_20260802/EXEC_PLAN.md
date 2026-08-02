# Comparative Worker Audit Evidence Integration ExecPlan

## Status

Active — evidence integration only.

## Objective

Preserve the completed two-branch comparative audit inside the selected continuation repository so a later canonical-continuation worker can inspect the branch decision, validation evidence, salvage inventory and donor lessons from the repository itself.

## Authority

1. User instruction to create a new branch from the selected continuation repository and place the comparative audit package, audit report, salvage inventory and comparison matrix in that branch.
2. Repository `AGENTS.md`, `PLANS.md` and `00_TASK/PROJECT_EXECUTION_METHOD.md`.
3. Canonical project-manager ExecPlan and live roadmap as historical/current programme context.
4. The uploaded comparative audit package as evidence, not implementation authority.

## Immutable baseline

- Source branch: `work/post-alpha-comprehensive-debt-retirement-v1`
- Source commit: `617127f6cb354591a875985788552360e72fd392`
- Working branch: `work/comparative-worker-audit-evidence-integration-v1`

## Scope

### In scope

- verify the uploaded comparative-audit package against its internal SHA-256 manifest;
- retain the original package archive;
- retain the extracted report, comparison matrix, salvage inventory, validation summary, supporting evidence, exact gap inventories and donor patch exports;
- record provenance, Git state, hashes and package validation;
- publish one full-history checkpoint archive from the resulting branch.

### Out of scope

- applying, cherry-picking or rewriting any donor repair;
- changing source, tests, normative documents, canonical ExecPlan, roadmap status or accepted module semantics;
- reopening or closing the post-alpha programme based solely on the audit;
- treating audit findings, donor patches or test transcripts as implementation proof;
- merge, rebase, push or history rewrite.

## Invariants

- The comparative audit remains challenge and planning evidence only.
- The selected continuation repository remains the base.
- Original audit filenames and internal package hashes remain reproducible.
- No canonical control surface is silently rewritten.
- No donor patch is applied during this unit.

## Acceptance unit

### Unit 1 — Preserve comparative audit evidence

**Pass:**

- branch descends exactly from `617127f6cb354591a875985788552360e72fd392`;
- original audit archive is retained with a recorded SHA-256;
- all extracted files listed in the supplied `SHA256SUMS.txt` verify;
- the audit report, `salvage_inventory.csv`, `progress_quality_matrix.csv` and `validation_summary.json` are present;
- supporting evidence and donor patch exports are retained without execution;
- `git diff --check` passes for integration-authored files; byte-preserved imported evidence is validated by its supplied SHA-256 manifest rather than whitespace-normalised;
- the final commit and clean Git state are recorded;
- a verified full-history checkpoint archive is produced.

**Fail:**

- any source/test/normative/canonical-plan mutation occurs;
- a package hash fails;
- donor changes are applied;
- audit conclusions are promoted to canonical implementation status.

## Required reads

The current-target read manifest is `FULL_READ_MANIFEST.tsv` in this directory.

## Allowed files

Only this directory may be added or changed for repository content:

`project_control/canonical_project_manager/audits/worker_branch_comparative_audit_20260802/`

## Validation

- `sha256sum -c audit_material/SHA256SUMS.txt`
- archive SHA-256 and `gzip -t`
- required-file inventory
- `git diff --check` on integration-authored files
- `git status --short --branch`
- archive content listing and SHA-256 after checkpoint creation

## Artefacts

- `FULL_READ_MANIFEST.tsv`
- `INTEGRATION_RECEIPT.md`
- `SOURCE_PACKAGE_SHA256.txt`
- original package archive
- extracted `audit_material/`
- downloadable full-history checkpoint archive

## Progress

- 2026-08-02: branch created from the selected continuation commit.
- 2026-08-02: uploaded audit package verified against its internal SHA-256 manifest before repository mutation.

## Decisions

- Preserve the entire audit package and extracted material. This avoids reducing the future worker to the four headline files while retaining exact supporting evidence and donor provenance.
- Do not edit the canonical ExecPlan or roadmap. This bounded evidence-integration unit does not itself adjudicate or implement the audit findings.

## Roadblocks

None at plan creation.

## Validation

Pending execution.

## Unknowns

- Which donor findings remain applicable after future continuation work is intentionally not adjudicated in this unit.

## Closeout

Pending.
