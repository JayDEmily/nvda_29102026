# Vocabulary Governance Deduplication ExecPlan

## Status

**Status:** completed; awaiting review and integration
**Date:** 2026-08-03
**Immutable baseline:** `98c462a4f8fb258b79429ec083565d6f2e2fffd9`
**Branch:** `work/vocabulary-governance-dedup-v1`
**Current unit:** none

## Objective

Simplify `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` so it remains vocabulary-governance law rather than a duplicate term dictionary, while preserving the existing vocabulary schema, builder, human registry and generated JSON architecture and preserving exact normative lineage for admitted tests and historical evidence.

## Non-goals

- no new vocabulary JSON schema or parallel registry format;
- no change to runtime/domain behaviour;
- no weakening, retirement, broad redirect or semantic re-authoring of admitted tests;
- no hand-editing of generated vocabulary JSON;
- no migration or rewriting of completed historical receipts merely because their former line locators become historical;
- no use of the out-of-date routing index as authority for this unit.

## Authority

1. direct user instruction in the current thread;
2. `AGENTS.md` and `PLANS.md`;
3. this ExecPlan and the live roadmap pointer;
4. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` and `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`;
5. the existing vocabulary registry, workflow, schema, builder and generated projection;
6. admitted vocabulary and normative-authority tests;
7. source/configuration/generated surfaces;
8. historical evidence;
9. `00_TASK/PROJECT_EXECUTION_METHOD.md` where higher authority is silent.

## In scope

- `ROADMAP_LEDGER_V2.md` live pointer/state;
- this plan and its evidence directory;
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`;
- existing vocabulary process documents where exact source/lineage wording must be reconciled;
- `docs/vocabulary/vocabulary_registry.md` only where an admitted term currently exists solely in `10.1` or lacks exact existing-schema metadata;
- existing vocabulary builder/schema/generated projection only where required to preserve the current architecture and parity;
- exact active tests/fixtures whose lineage references the changed normative surface;
- validation receipts and a bounded branch commit.

## Invariants and prohibited shortcuts

- normative intent remains above tests and code;
- the existing vocabulary data model and schema are preserved unless direct evidence proves a bounded defect requiring amendment;
- every removed admission remains semantically represented in the accepted registry and generated projection before removal;
- section-level lineage is preserved through exact stable admission identifiers and registry/JSON locators, not a vague document-wide redirect;
- generated JSON is regenerated through the existing builder only;
- no test proposition is weakened, skipped, xfailed, deleted, hidden or redirected to a less exact authority;
- historical receipts remain historical evidence and are not rewritten to fabricate contemporaneous locators.

## Acceptance units

### Unit A — authority and lineage inventory

Pass when all governing and directly affected files are read in full, all current `10.1` term admissions are mapped against the existing registry and generated JSON, and every active test/fixture/source dependency on `10.1` is classified.

### Unit B — normative deduplication and exact redirect

Pass when `10.1` contains standing governance law plus a compact exact lineage table for moved admissions, and no term admission is removed unless its semantic record is present through the existing vocabulary system.

### Unit C — downstream reconciliation

Pass when the existing registry/builder/projection and any active lineage tests or fixtures agree with the revised normative surface without changing the established JSON format.

### Unit D — validation and closeout

Pass when targeted vocabulary proof, normative lineage proof, aggregate relevant tests, generated-parity checks, diff checks and Git-state checks pass; evidence is recorded; the plan and roadmap are closed accurately; and the branch is committed cleanly.

## Required reads

Recorded in `FULL_READ_MANIFEST.tsv`. At minimum: root controls, vocabulary normative pair, vocabulary process documents, registry, generated JSON, schema, builder, build script, directly affected tests/fixtures, and any proof/config surface discovered by the lineage inventory.

## Evidence

- `project_control/vocabulary_governance_dedup_20260803/FULL_READ_MANIFEST.tsv`
- `project_control/vocabulary_governance_dedup_20260803/evidence/LINEAGE_INVENTORY.tsv`
- `project_control/vocabulary_governance_dedup_20260803/evidence/ADMISSION_COVERAGE.tsv`
- `project_control/vocabulary_governance_dedup_20260803/evidence/VALIDATION_LOG.txt`

## Validation

- `git diff --check`
- existing vocabulary builder generation/check path
- exact vocabulary Tier A tests
- exact normative-lineage tests discovered by Unit A
- relevant proof-authority/check scripts if their declared source set includes changed files
- Git branch, status, diff and commit inspection

## Return and stop conditions

Execute through Unit D unless a hard blocker proves that an admission cannot be represented through the existing schema without a user-level architectural decision. Do not stop merely because a test fails or a locator changes.

## Progress

- [x] Branch created from exact clean baseline.
- [x] Unit A
- [x] Unit B
- [x] Unit C
- [x] Unit D

## Decisions

- The out-of-date routing index is not authority for this task.
- A stable exact lineage map is permitted as a transitional compatibility surface; a vague document-level redirect is not.
- Historical evidence is preserved rather than mass-rewritten.

## Roadblocks

- The repository-wide global synonym clean gate remains blocked by five pre-existing occurrences in `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`. Baseline and post-change candidate sets are identical; this unit did not suppress or alter them and did not update the clean touch stamp.

## Unknowns

- The complete repository test-suite result is unknown. One `pytest -q` attempt reached approximately 89% before the 600-second execution ceiling and produced no final verdict. The exact affected vocabulary and M00 proof blocks passed.

## Outcome

- The existing vocabulary schema, builder and JSON shape were preserved unchanged.
- `10.1` was reduced from 6,806 to 4,234 words: 2,572 words removed, a 37.79% reduction.
- Sixteen retained admission sections now preserve exact section identity, semantic-decision references and 90 unique canonical IDs as stable lineage redirects.
- All 90 redirected IDs resolve to accepted records in `docs/vocabulary/vocabulary_registry.md` and entries in the 194-entry generated JSON projection.
- Eight stale line-number locators in registry projection metadata were converted to stable `10.7`/`10.8` section locators and the JSON projection was regenerated through the existing builder.
- One central Tier A proof validates every redirect section, decision reference and exact ID set. The only direct module test that depended on duplicated term prose, M00, now resolves `10.26` through the registry and JSON. No mass test rewrite was required.
- Relevant validation: 22 focused tests passed; the complete Tier A vocabulary directory passed 105 tests; the complete M00 application-shell directory passed 26 tests; active-control/proof-authority validation passed.
- Historical receipts and archived evidence were not rewritten. The stale routing index was not used as authority.
