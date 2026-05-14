# SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001_RECEIPT

Date: 2026-05-09
Type: planning/control reconciliation

## Purpose

Reconcile local sandbox commits, reset-safe TAR outputs, package hashes, package contents, receipts, and ledger state before any external merge/replay claim.

## Authority intake actually inspected

- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `docs/planning/2026-05-09_HELD_ROW_AUTHORITY_BRIEFING_PACK_001.md`
- `var/audit/roadmap_planning/ROADMAP_LEDGER_PROGRAMME_PLANNING_AND_EXECUTION_QUEUE_001_RECEIPT.md`

## Touched files

- `ROADMAP_LEDGER.md`
- `docs/planning/2026-05-09_SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001.md`
- `var/audit/roadmap_planning/SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001_RECEIPT.md`
- `var/audit/roadmap_planning/SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001_PACKAGE_LEDGER.tsv`
- `var/audit/roadmap_planning/SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001_COMMIT_PACKAGE_LEDGER.tsv`
- `var/audit/roadmap_planning/SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001_TAR_CONTENT_INDEX.txt`
- `var/audit/roadmap_planning/current_git_log_before_reconciliation.txt`

## Checks run

- Local Git history check for referenced commits.
- SHA256 computed for each reset-safe package.
- Sidecar `.sha256` comparison for each reset-safe package.
- Python `tarfile.open(..., r:gz)` member listing for each reset-safe package.
- Package content scan for patch/diff material, receipt/evidence material, changed-file manifests, and commit pointers.

## Result

All seven expected reset-safe packages were present, gzip-tar readable, sidecar-hash matched, and mapped to commits present in local Git history.

The setup package is classified separately as `setup_evidence_replay_candidate` because it contains setup evidence and patches rather than a proof receipt.

External/GitHub acceptance remains `pending_external_acceptance_or_merge`.

## Output ledgers

- `var/audit/roadmap_planning/SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001_PACKAGE_LEDGER.tsv`
- `var/audit/roadmap_planning/SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001_COMMIT_PACKAGE_LEDGER.tsv`
- `var/audit/roadmap_planning/SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001_TAR_CONTENT_INDEX.txt`

## Planning proof

- `git diff --check`: status `0`
- TSV parse check: package ledger `7` rows; commit/package ledger `7` rows; held-row matrix `8` rows; held-row file ledger `68` rows.
