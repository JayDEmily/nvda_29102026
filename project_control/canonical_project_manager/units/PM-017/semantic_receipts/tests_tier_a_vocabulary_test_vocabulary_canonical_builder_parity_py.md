# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py`

- Sequence `160`, PM-017; SHA-256 `4f27d249bca387eff802b3b2a369cbfa05e3b02eeb1b4d4ef7758f6ba28b4320`.
- Read full test `1-149`, builder/wrapper surfaces, accepted P1 vocabulary register, human registry, committed JSON and workflow projection law. Targeted run: `3 passed, 1 failed`.

## G1 — committed JSON equals both builder import paths

- Locator `23-42` requires exact dictionary parity between committed JSON, wrapper builder and native builder.
- This is valid deterministic projection proof; it does not establish human semantic completeness.
- Relation `bounded_separable_clause`; strength `substitution`.

## G2 — governed source hashes cover a fixed source set

- Locator `45-66` requires ten paths in builder hash coverage and excludes the generated synonym-candidate report.
- This proves current hash inventory, but the exact ten-path list is partly implementation-owned; hash inclusion does not establish semantic authority or full dependency closure.
- Relation `related_but_not_proved`; strength `presence_only`.

## G3 — durable row terms appear as projection tokens and human-registry headings

- Locator `69-112` validly requires the selected terms to occur canonically or by alias in the generated projection.
- It then requires nearly all selected phrases to exist as exact `###` headings. That contradicts P1's explicit decision that `Serial Desk-cognition` is an alias of the canonical heading `Serial Desk-cognition Spine`; an admitted alias is not required to be a separate heading. The current failure is therefore caused by an over-constrained test, not missing vocabulary authority.
- Relation `authority_contradictory`; strength `token_only`.

## G4 — disallowed phrase uniqueness/non-collision and historical appendix specimens

- Locator `115-149` validly checks projection-level disallowed uniqueness and non-collision with labels/aliases.
- Requiring four fragment-like phrases in a historical adjudication appendix proves only that appendix content; occurrence-scoped suppression and current semantic acceptance are not established.
- Relation `related_but_not_proved`; strength `historical_observational`.

## File decision

- Groups/relationships `4/4`; final `BLOCKED_P3_REPAIR`.
- Preserve G1 and the projection-level portion of G4. Repair G3 to recognise accepted aliases through projection metadata rather than demanding separate human-registry headings, and separate historical appendix inventory from current builder parity.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
