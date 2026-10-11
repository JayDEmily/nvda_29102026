# F4 authorised reconstruction — preservation checkpoint, not review candidate

**Date:** 2026-10-11. **Status:** IN PROGRESS, not F4 acceptance, not Stage-1 acceptance.
This is a newly reconstructed branch from original recovered `734cf58e8b826a065349b10efdac4019908e83fd`.
The previously reported `296fbae` and its uncommitted regression-history changes were not
recovered; no commit identity or previous result was invented or reused. Original
recovery archive remains separate and unchanged.

## Governing authority and bounded changes

Read root `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md` and tests-local `AGENTS.override.md`
plus catalogue/brief and prior F4 evidence. This reconstruction continues the F4
scope authorised by the Programme Owner; it does not alter GUARDRAILS, AGENTS,
the accepted normative catalogue, D116, D123, M00 ownership, or Stage-2 kernels.

- D041: proof-first commit `f0e6bcd`; production/API and row-proof commit `a521dfb`.
  A request now can bind a child calculation's independently versioned parameter
  profile without changing its parent's profile. Public D041 proves exact D026,
  D040 and D033 graph arithmetic, D040 parameter version distinctions, selected
  M00 source lineage, retry and missing-data refusals.
- D148: proof `f856059`, ledger `5551bee`. Six direct M00 macro sources and
  real D042/D044/D045 predecessor calculation produce `52.3695`, with explicit
  percentage-point versus basis-point units and full lineage/refusals.
- D149: proof `fe9039c`, ledger `a581aeb`. The score uses direct R257/R256,
  actual D047 rate spread and independently versioned D061 score; tests check
  exact arithmetic, public lineage, missing/late/wrong-subject refusal and retry.

The original F4 reconciliation was regenerated from the accepted CSV; the immutable
population/accounting invariants remain 174/144/30 Stage-1 rows, 491 dependency
edges plus D007 sentinel. Current bounded public edge proof increased from 303
to 319 and unresolved Stage-1-closed edges decreased from 52 to **36 across
8 rows**: D078 (7), D079 (4), D080 (4), D081 (4), D084 (3), D104 (2),
D132 (6), D150 (6). The **30 cross-stage own-kernel/refusal obligations** remain
unproven. These are not necessarily 66 software defects. Existing F1/F2/F3
proof and historical reviewer evidence are preserved, not re-admitted.

## Exact reproducible check results for current reconstructed tree

Runtime: Python 3.13.5, pinned pytest 9.0.3, Ruff 0.15.11, Mypy 1.20.1,
PostgreSQL 17.9 from supplied signed archive with `fsync=on`, `synchronous_commit=on`,
`full_page_writes=on`, distinct `nvda_m00_proof` and `nvda_m01_proof` roles and schemas.
Local dependency wheelhouse and database runtime are separate uploaded programme
inputs, not hidden inside this Git tree.

- Scoped D041: **5 passed** `d041_focused_5_pass.log`.
- Scoped D148: **5 passed** `d148_public_5_pass.log`.
- Scoped D149: **6 passed** `d149_public_6_pass.log`.
- Architecture/bootstrap: **74 passed**, `architecture_bootstrap_with_yaml.log`.
  Initial isolated venv attempt lacked PyYAML and stopped at collection; the
  initial failure `architecture_bootstrap.log` is preserved.
- Derived-product suite at earlier D041 tree: **571 passed**, `derived_product_regression.log`.
- Current broader suite **1,127 passed**: `pg_broader_non_durability.log`, command:
  `python -m pytest -q tests/architecture tests/bootstrap tests/product tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py`
  with M00/M01 DSNs configured and PyYAML 6.0.3 available via local path.
- Current isolated full M00 PostgreSQL durability suite: **55 passed** in one run,
  `m00_durability_clean.log`, command:
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=.:src python -m pytest -q tests/product/raw_signal/test_u05_postgresql_durability.py`,
  with admin PostgreSQL DSN. The clean environment has no ambient Pydantic.
- Changed-scope Ruff lint **PASS**: `ruff_changed_scope_lint.log` (including
  reconciliation generator); Ruff format **4 files formatted**:
  `ruff_changed_scope_format.log` (API and three new product tests).
- Mypy on 5 M01 derived source files **PASS**: `mypy_derived_source.log`.
- **Non-pass:** Whole-repository `ruff format --check .` identifies 62 pre-existing
  files requiring formatting; no unrelated formatting was undertaken.
  `ruff_repository_format_not_clean.log`.
- **Non-pass:** Full-source Mypy `mypy src` reports 5 missing `yaml` library typing
  stubs in architecture files in this isolated Python environment; it did not
  establish whole-source type success. `mypy_full_not_clean.log`.
- Reconciliation generator: **PASS**, `d149_reconciliation.log`. No whole-Stage-1
  semantic acceptance claim follows from counts or test results.

## Remaining execution

Next reconstruct exact D078–D081 coherent aligned factor-regression history and
lineage, respecting §5 K06; then D084 sector/dispersion separate child scopes,
D104 skew-rotation history, D132 exact option-liquidity inputs and D150 composite
risk, followed by the 30 cross-stage own-kernel and fail-closed proofs. Keep
proof-first Git commits, run full acceptance validation, and hand off for independent
review **only at the consolidated F4/Stage-1 candidate boundary**. Incomplete
future work does not authorise a Stage-2 implementation.
