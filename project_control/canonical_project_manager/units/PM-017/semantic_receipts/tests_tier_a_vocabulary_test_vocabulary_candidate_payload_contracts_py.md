# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_candidate_payload_contracts.py`

- Sequence `157`, PM-017; SHA-256 `c5176d6e4d67659dc7a76b0db34b5502f078714593c051b4d8e7b7cab20bf991`.
- Read full test `1-95`, candidate payload implementation and workflow admission `ATLAS_FEATURE_ADMISSION_003`. Targeted run: `5 passed` inside `63 passed, 3 failed in 5.75s`.

## G1 — bridge payload becomes a candidate with normalised tokens
- Locator `31-44` requires fields and alias to produce the three expected tokens.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G2 — aliases must be a list
- Locator `47-55` requires one malformed payload to fail.
- Relation `bounded_separable_clause`; strength `boundary`.
## G3 — payload classification delegates to governed classifier
- Locator `58-68` requires an allowed-alias payload to yield alias-only and owning slug.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G4 — unknown category is rejected
- Locator `71-79` requires one ungoverned category to fail.
- Relation `bounded_separable_clause`; strength `boundary`.
## G5 — ordered batch classification preserves action order
- Locator `82-95` requires enrich/add/quarantine in source order.
- Relation `bounded_separable_clause`; strength `behavioural`.

## File decision

- Groups/relationships `5/5`; final `ADMIT_TIER_A_CURRENT` under `ATLAS_FEATURE_ADMISSION_003`.
- The payload bridge remains a mechanical review helper and cannot perform semantic admission or mutate canonical vocabulary.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
