# NVDA10 Project Structure

The active codebase lives at the repository root.

## Active Codebase

- `AGENTS.md`, `PLANS.md`, `README.md`, `pyproject.toml`, and `uv.lock` define the working project surface.
- `src/`, `tests/`, `docs/`, `config/`, `data/`, `fixtures/`, `schemas/`, `scripts/`, `tools/`, `intent_migration/`, `legacy_import/`, and `var/` are copied from the audited active source bundle.
- `var/audit/` is retained as part of the active audited codebase state.

## Control And Evidence

- `project_control/` contains concise project-universe control indexes and workflow notes.
- `evidence_index/` contains concise summaries for GAP-006, Stage1E, Atlas, and historical source status.
- `_archive/` contains raw input bundles, audit reports, search reports, and historical reference capsules.
- `assembly_reports/` contains assembly ledgers, command logs, GitHub push result, and layout verification.

Raw project-universe TAR files are intentionally stored under `_archive/` or controlled support folders, not at the repository root.
