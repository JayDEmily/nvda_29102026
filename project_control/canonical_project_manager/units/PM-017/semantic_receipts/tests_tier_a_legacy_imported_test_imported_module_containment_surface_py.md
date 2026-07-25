# Semantic receipt — `tests/tier_a/legacy_imported/test_imported_module_containment_surface.py`

- Sequence `142`, PM-017; SHA-256 `3cc363c3f823a4f41f3672421cd87bdf33cb1869ae376be21ee784009203e65d`.
- Read full test `1-130`, `legacy_import/README.md`, package selection in `pyproject.toml`, the current Donor Evidence vocabulary authority and PM-011 routes. Targeted run: `4 passed` inside the four-file run that produced `7 passed, 29 failed`.

## G1 — native runtime and proof have no direct legacy-package imports

- Locator `84-93` scans every Python file under `src`, `tests/tier_a` and `tests/tier_b`, excluding itself, and asserts the native package path is absent and no static import resolves under `legacy_import` or `nvda_desk.legacy.imported`.
- This exactly proves the current static-import containment boundary for the scanned population. It does not detect imports assembled through variables, aliases outside the two prefixes, file loading, subprocesses or copied donor semantics.
- Relation `bounded_separable_clause`; strength `boundary`.

## G2 — transform-boundary donor mentions are not imports

- Locator `96-102` proves each of nine named guard files contains the donor-root string while its AST contains no static import under either forbidden prefix.
- This is a bounded false-positive resistance clause for those nine files only; it does not establish the semantic quality of their transform tests.
- Relation `bounded_separable_clause`; strength `boundary`.

## G3 — archive and packaging quarantine are explicit

- Locator `105-121` proves the archive README states historical-evidence-only status, no admitted native imported package, and no native runtime/Tier A/Tier B import permission; `pyproject.toml` packages only native source/scripts and does not package `legacy_import`.
- This proves checked-in declaration and package-selection state, not runtime non-reachability through every mechanism.
- Relation `bounded_separable_clause`; strength `presence_only`.

## G4 — literal dynamic imports are absent

- Locator `123-130` scans the same population for literal-string calls to `__import__` and `importlib.import_module` under the two forbidden prefixes and finds none.
- Computed strings, aliased import functions and other loading mechanisms remain outside the observation.
- Relation `bounded_separable_clause`; strength `boundary`.

## File decision

- Groups/relationships `4/4`; final `ADMIT_TIER_A_CURRENT` for the four exact bounded containment clauses only.
- Admission does not prove absence of copied donor behaviour or every possible dynamic loading path.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
