# Audit and brief history

This folder contains the durable audit surfaces that must be carried forward with every authoritative work package.

## Frozen evidence

- `briefs/` stores the authored brief lineage used in the rebuild and post-audit sequence reviews. Those files are frozen once written.
- `reports/` stores audit reports and packaging receipts. Those files are frozen once written.
- The migration governance pack under `migration_prebuild/` is frozen in place within the active tranche except for a dedicated governance leaf that admits a later-numbered control document and updates routing.

## Dynamic evidence

- `ledgers/` stores the active machine-readable JSON execution ledger family.
- Within an active tranche, the active brief-child JSON ledger under `ledgers/` is the single always-live mutable execution ledger surface.
- The active JSON ledger does not replace the brief or the locked benchmark workbook.
- `nvda_running_audit_log.xlsx` is retained as historical archive only after the admitting governance leaf.

## Thin receipt rule inside the JSON ledger

The active JSON ledger must contain one thin machine-readable receipt surface for tranche and leaf closure.

That receipt surface records, at minimum:

- ledger version and status
- tranche identifier
- parent brief path and content hash
- ordered step status
- active branch name
- baseline / head / closeout refs when known
- status
- proof status
- governing source
- short note or carry-forward blocker

Human-readable audit narration remains in briefs and audit reports.

Update the active JSON ledger in place. Do not create a second live execution ledger for the same active brief. The Excel workbook remains carried forward but is no longer updated as the live ledger.
