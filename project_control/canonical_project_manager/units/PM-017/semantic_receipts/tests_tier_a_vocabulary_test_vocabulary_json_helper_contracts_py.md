# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py`

- Sequence `162`, PM-017; SHA-256 `bf6c4a8255f7750ec21f240497fe57a83e9c509894bb1e3e2feca508c2e987ff`.
- Read full test `1-92`, complete JSON helper/schema implementation and vocabulary governance sections 10.2, 10.5 and 10.6. Targeted run: `9 passed in 0.05s`.

## G1 — mapping decode and field carriage
- Locator `31-38` proves one valid mapping becomes a validated document and carries schema, registry and contract fields.
- Relation `bounded_separable_clause`; strength `behavioural`.

## G2 — non-object roots are rejected
- Locator `41-44` covers list, string and number roots.
- Relation `bounded_separable_clause`; strength `boundary`.

## G3 — invalid entries shape is rejected
- Locator `47-52` proves the entries field cannot be a string.
- Relation `bounded_separable_clause`; strength `boundary`.

## G4 — unknown top-level fields are rejected
- Locator `55-60` proves closed top-level document shape for one extra-field specimen.
- Relation `bounded_separable_clause`; strength `boundary`.

## G5 — UTF-8 path helper delegates to document validation
- Locator `63-69` proves one path-loaded document is decoded and indexed.
- Relation `bounded_separable_clause`; strength `behavioural`.

## G6 — emitted JSON round-trips exactly at schema level
- Locator `72-83` proves newline termination and `to_dict` equality after reparsing.
- It does not prove semantic admission or human-registry completeness.
- Relation `bounded_separable_clause`; strength `substitution`.

## G7 — text serialisation does not mutate the committed projection
- Locator `86-92` proves one helper call leaves the tracked canonical JSON bytes unchanged.
- It does not prove no other code path can mutate that file.
- Relation `bounded_separable_clause`; strength `boundary`.

## File decision
- Groups/relationships `7/7`; final `ADMIT_TIER_A_CURRENT`.
- Admission is limited to closed-schema JSON helper behaviour. It does not elevate schema or generated JSON above accepted human semantic authority.
- No protected source, test, configuration, normative, registry or proof-block file was changed.
