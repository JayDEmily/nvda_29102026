# Semantic receipt — `tests/tier_a/vocabulary/test_dmp_v3_vocabulary_terms.py`

- Sequence `150`, PM-017; SHA-256 `48e171e51b6b03bd8fd2239817d12f3ae1d2d7f147a082b8393eef7b50999c89`.
- Read full test `1-36`, all eighteen projected entries, their accepted P1 protocol decisions and the human vocabulary registry. Targeted run: `1 passed` inside `63 passed, 3 failed in 5.75s`.

## G1 — required DMPV3 protocol terms and contract mappings are projected

- Locator `7-36` requires eighteen exact slugs in the committed JSON and exact `maps_to_contract` values.
- The slugs/mappings resolve to accepted P1 protocol records, so this is valid bounded projection proof. It does not prove protocol behaviour, human-registry completeness or semantic correctness beyond those eighteen accepted records.
- Relation `bounded_separable_clause`; strength `presence_only`.

## File decision

- Groups/relationships `1/1`; final `ADMIT_TIER_A_CURRENT` for exact projection presence/mapping only.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
