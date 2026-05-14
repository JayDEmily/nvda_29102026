# NVDA imported-module subsystem disposition tranche v1 — admissibility and disposition note

Date: 2026-04-20
Active branch: `work/imported-module-subsystem-disposition-tranche-v1-20260420`
Baseline branch promoted to `main` before tranche start: `work/api-dto-broker-boundary-resolution-tranche-v1-20260420`
Promoted `main` head: `65f24831eb012f20b0114f63cdaab869dbcbfcc8`
Observed pre-promotion `main`: `aa4bad4728a0ea1cfc72570337584f1c8cc11a42`

## Direct answer

The truthful closeout state is **retire / quarantine**.

No live native runtime surface requires admission of `src/nvda_desk/legacy/imported/` in this tranche.
The top-level `legacy_import/` tree is retained as **historical source evidence only**.

## Scope reread completed for this audit

The audit reread, in full, the tranche brief, the routed frozen control pack, the workbook-authority companion docs, the retained test authority, the current audit workbook sheets named in the brief, the accepted API DTO / broker-boundary tranche report, all current native `src/` and `tests/` surfaces found by the dependence audit, and the full top-level `legacy_import/` tree.

Observed `legacy_import/` inventory after full-tree read:

- `source/` files: 128
- `tests/` files: 227
- `fixtures/` files: 16
- `config/` files: 9
- `scripts/` files: 3
- `schemas/` files: 1
- total files read: 384

## Audit questions and answers

### 1. Does any current native `src/` runtime surface import, instantiate, or depend on the top-level `legacy_import/` tree?

No.

Observed evidence:

- exact-string native search over `src/` and `tests/` for `legacy_import` and `nvda_desk.legacy.imported` returned only documentation references in `tests/README.md` and `tests/AGENTS.override.md`, not runtime or native-test imports;
- package build scope in `pyproject.toml` includes only `src/nvda_desk` and `src/scripts` for wheel build, and only `/src/nvda_desk`, `/src/scripts`, `/tests`, `/README.md`, and `/pyproject.toml` for sdist;
- no current native module path exists at `src/nvda_desk/legacy/imported/`.

### 2. Does any current native proof surface depend on the top-level `legacy_import/` tree in a way that makes retirement impossible in this tranche?

No.

Observed evidence:

- `tests/AGENTS.override.md` states that legacy tests under `legacy_import/tests/` are source evidence only;
- `tests/README.md` points to `legacy_import/tests/` as the location of legacy test source, but does not admit those tests as native authority;
- the current Tier A/B floor passes without any native import path into the top-level `legacy_import/` tree.

### 3. Which imported families, if any, still have live value that is not already absorbed into native homes?

Historical source, fixtures, and archive tests remain valuable as evidence only.
No live native runtime owner currently requires a bridge package.

Observed evidence:

- current native calendar/reference contracts use `ImportedReferenceBundle` terminology inside `src/nvda_desk/contracts/reference_data.py` and adjacent calendar reference surfaces, but that is a native reference-data contract family rather than a dependency on the top-level `legacy_import/` tree;
- current review code exposes `attach_imported_citations` in `src/nvda_desk/downstream/review_stage.py`, but this is a bounded review helper and not a bridge to the historical tree.

### 4. Are surviving imported-module references only conceptual / review-citation / DMP mention surfaces rather than live runtime ownership?

Yes.

Observed evidence:

- `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` and `docs/09_DMPV3_PROTOCOL_CORE.md` still mention imported-module packet emitters as architectural / packet-carriage concepts;
- no current native source file imports a module from `legacy_import/` or `nvda_desk.legacy.imported`.

### 5. Truthful disposition outcome

The truthful outcome is **retire / quarantine**.

Why:

- the benchmark workbook marks the family as provisional / reserved rather than mandatory always-admit runtime ownership;
- the repo already carries the historical material in a top-level evidence tree;
- native packaging excludes that tree;
- native tests already treat the historical tests as source evidence only;
- admitting a new native bridge package here would fabricate live capability that the current repo does not use.

## Stop-boundary result

This audit does **not** justify touching:

- `src/nvda_desk/analysis/scenarios/**`
- `src/nvda_desk/observability/**`
- any API, entry, ingress, replay, or broker boundary surface
- broad rewrites inside `legacy_import/`

The lawful next move is minimal explicit quarantine labelling plus one bounded Tier A containment proof family.
