# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py`

- Sequence `163`, PM-017; SHA-256 `7686b5797689bb81c37b165e7f5d45eb7b375cc7c98473d751dfbf7ed27ff954`.
- Read full test `1-163`, committed canonical projection, accepted PM-004/PM-010 vocabulary decisions and relevant temporal/protocol records. Targeted run: `1 failed in 0.05s` at line 39.

## G1 — Parallel Risk, DMPV3 and calendar projection rows
- Locator `7-34` checks exact slug-to-contract presence for the lane, envelope and three calendar reference/import records.
- This is projection presence only; it does not prove runtime behaviour or semantic completeness.
- Relation `bounded_separable_clause`; strength `presence_only`.

## G2 — coefficient vocabulary projection
- Locator `36-71` mixes admitted coefficient/modifier terms with required `mutable_runtime_surface` and `baseline_only_surface` rows.
- PM-004 `CME-003` and `CME-004`, integrated at PM-010 rows 36-37, explicitly quarantine those two exact classes for missing higher normative authority. The current red result is therefore a truthful contradiction in the test expectation, not a missing generated entry.
- Relation `authority_contradictory`; strength `presence_only`.

## G3 — Source Temporal Standard and field projection
- Locator `73-121` checks the standard plus nine field-level slugs against exact contract strings.
- It proves only projection inventory and mapping-string parity, not source capture, UTC conversion, persistence or lineage behaviour.
- Relation `bounded_separable_clause`; strength `presence_only`.

## G4 — workbook and field-level provenance projection
- Locator `123-133` checks two exact projection rows.
- Relation `bounded_separable_clause`; strength `presence_only`.

## G5 — temporal conformance classification projection
- Locator `135-163` checks the inventory and four classification labels.
- These are planning/control classifications, not runtime conformance proof.
- Relation `related_but_not_proved`; strength `presence_only`.

## File decision
- Groups/relationships `5/5`; final `BLOCKED_P3_REPAIR`.
- Retain the admitted projection checks, remove or re-author the two quarantined class requirements, and keep the test description bounded to generated-registry presence. A green rewrite must not silently re-admit PM-004 quarantines.
- No protected source, test, configuration, normative, registry or proof-block file was changed.
