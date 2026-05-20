# MAIN_RECONCILIATION_RECEIPT — 2026-05-20

## Purpose

Create a single clean `main` handoff from the current target-surface repair branch while preserving the useful but superseded old `main` work as historical evidence.

## User authority

The user explicitly authorised execution of the reconciliation gates to avoid handing off a splintered tarball and to end with a single `main`.

## Input branch state

| Item | Commit |
|---|---|
| Old `main` | `41f5a3926776904b31ee31abce5aa8ca40b186c4` |
| Current canonical content base | `1f417b39ddd75312f92670d7f0927813a5dffe8c` |
| Merge base | `8e319647c9e09e5e734fdeed409f82342edc760d` |

## Safety refs created

| Ref | Commit | Purpose |
|---|---|---|
| `archive/main-before-reconciliation-20260520` | `41f5a3926776904b31ee31abce5aa8ca40b186c4` | Preserves old `main` exactly. |
| `archive/work-fwd014-before-reconciliation-20260520` | `1f417b39ddd75312f92670d7f0927813a5dffe8c` | Preserves the pre-reconciliation target-surface repair branch exactly. |

Evidence: `var/audit/main_reconciliation_20260520/SAFETY_REFS.txt`.

## Decision

The current target-surface repair branch remains the active content base.

Old `main` is not merged wholesale because it reintroduces the superseded `non310_actual_completion_*` source-contract path and the old ledger narrative. Those files are preserved under audit history rather than live source/test/config authority.

## Old `main` preservation

Old `main` additions/modifications relative to the reconciliation base were copied under:

`var/audit/main_reconciliation_20260520/old_main_unique_snapshot/`

Classification evidence:

- `var/audit/main_reconciliation_20260520/OLD_MAIN_FILE_CLASSIFICATION.md`
- `var/audit/main_reconciliation_20260520/OLD_MAIN_FILE_CLASSIFICATION.csv`

Summary:

| Classification | Count | Action |
|---|---:|---|
| archive-only prior reopened completion audit | 40 | archived, not active authority |
| archive-only superseded actual-completion audit | 51 | archived, not active authority |
| archive-only superseded ledger narrative | 1 | archived, not merged |
| archive-only superseded live source contract | 6 | archived, not live-ported |
| archive-only superseded proof-block config | 1 | archived, not live-ported |
| archive-only superseded Tier A contract test | 5 | archived, not live-ported |

## Imported methodology and forensic artefacts

The following artefacts were imported so future threads do not need chat-history access:

| Repo path | Purpose |
|---|---|
| `docs/planning/NVDA10_ATLAS_TO_ACTIVE_CODEBASE_MIGRATION_METHODOLOGY_STANDALONE.md` | Standalone service-by-service method for migrating remaining Atlas ideas. |
| `var/audit/atlas_source_code_forensic_20260520/` | V2 forensic report and per-Atlas-ID classification records. |
| `var/audit/atlas_migration_process_recovery_20260520/` | Recovered historical Atlas migration workflow. |

The V2 forensic report records:

| Measure | Count |
|---|---:|
| Atlas ideas total | 1,716 |
| Mapped to the active codebase's 18 services | 1,716 |
| Included as existing source behaviour | 508 |
| Added/modified in source code | 80 |
| Not included in active-codebase source behaviour | 1,128 |

## Live authority boundary

The imported methodology and forensic artefacts are planning/audit evidence only. They do not implement source behaviour.

Live source/test/config state remains the current target-surface repair content unless future service-by-service Atlas migration work lawfully changes it through:

`normative documents → Tier A/B/C tests → source/YAML/config/schema/fixtures → proof → receipt/ledger update`.

## Branch-promotion intent

After validation, this reconciliation branch is intended to become the new `main`. Old `main` remains recoverable at `archive/main-before-reconciliation-20260520`.

## Validation

| Check | Status | Evidence |
|---|---:|---|
| `git diff --check` | 0 | `reports/git_diff_check.*` |
| `make scaffold-check` | 0 | `reports/scaffold_check.*` |
| Forensic JSON parse | 0 | `reports/validate_forensic_json.*` |
| Forensic count check | 0 | `reports/validate_forensic_counts.*` |
| Proof block registry check | 0 | `reports/proof_blocks_check_all.*`; `proof_blocks_check_all=PASS count=51` |
| Target-surface non-310 repair tests | 0 | `reports/targeted_non310_repair_tests_fast.*`; `430 passed in 9.23s` |
| FWD-014 capital-deployment proof | 0 | `reports/targeted_fwd014_capital_fast.*`; `29 passed in 0.47s` |

A first non-isolated `targeted_non310_repair_tests` run was interrupted by the outer execution timeout after partial progress; it has no status file and is superseded by the complete isolated run.

## Final intended state

After commit and branch promotion, `main` should point to this reconciled content state. The previous old `main` remains preserved at `archive/main-before-reconciliation-20260520`.

## Commit closeout update

Reconciliation content commit created before this closeout update: `86617a0afbb706725a0b9868fd77b9442ca82d91`.

This receipt update records that branch promotion should happen after this final closeout commit. The final promoted `main` commit is reported in the final response and package checksums.
