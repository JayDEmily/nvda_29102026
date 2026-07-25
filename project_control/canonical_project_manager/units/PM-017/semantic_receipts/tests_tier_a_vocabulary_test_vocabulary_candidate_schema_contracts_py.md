# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_candidate_schema_contracts.py`

- Sequence `159`, PM-017; SHA-256 `9c9499d1278c2c9103bde77147e0cd4903e3ce45709c50f6f050ffa6ed971063`.
- Read full test `1-93`, full vocabulary schema, current canonical projection and candidate-governance workflow. Targeted run: `5 passed, 1 failed`; the failure identifies two enum categories absent from the accepted projection.

## G1 — category enum equals currently projected canonical categories
- Locator `19-26` requires exact set equality and excludes `runtime_signal`.
- This is a valid drift guard between schema and accepted projection. It is currently red because `audit_surface` and `audit_classification` remain in the enum without projected entries; the red result is a real repair obligation, not a test defect.
- Relation `bounded_separable_clause`; strength `boundary`.
## G2 — raw/derived enum is exactly bounded
- Locator `29-30` requires `raw`, `derived`, and `not_applicable` only.
- Relation `exact_full_proof`; strength `presence_only`.
## G3 — ungoverned category/raw-derived values are rejected
- Locator `33-52` requires two invalid-entry specimens to fail validation.
- Relation `bounded_separable_clause`; strength `boundary`.
## G4 — candidate descriptor fields are carried
- Locator `55-73` requires family, setup variant, execution expression, horizon and derived tag on one entry.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G5 — entry index is a slug-keyed projection
- Locator `76-87` requires one entry to index by canonical slug.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G6 — empty document has empty index
- Locator `90-93` requires an empty projection.
- Relation `bounded_separable_clause`; strength `behavioural`.

## File decision

- Groups/relationships `6/6`; final `ADMIT_TIER_A_CURRENT`.
- The current G1 failure must return to schema/projection governance before P3; admission does not authorise selecting which side changes without semantic authority for the two orphan categories.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
