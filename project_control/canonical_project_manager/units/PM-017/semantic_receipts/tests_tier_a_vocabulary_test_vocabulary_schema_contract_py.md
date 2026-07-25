# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_schema_contract.py`

- Sequence `164`, PM-017; SHA-256 `ba79cca9dea0b207a20d03130d823a11c8e5a15464bc27b2093c528535d39270`.
- Read full test `1-118`, full `VocabularyEntry`/`VocabularyDocument` validation implementation, and vocabulary core/working authority for one-term/one-meaning, explicit aliases and exact collision validation. Targeted run: `2 passed in 0.03s`.
- Starting state: imported schema symbols or synthetic documents containing exact token collisions. Action: inspect schema shape or serialise the document. Observed surface: symbol/dataclass shape and raised collision errors. The file does not prove semantic admission, human-registry completeness, builder parity or near-match synonym judgement.

## G1 — schema symbols and immutable dataclass shape are present

- Test locator `22-35`; authority working overlay lines `17-23` establishes the schema as the machine-structure and exact-collision layer.
- The assertions prove the current module, three named public symbols and frozen dataclass implementation shape.
- The named symbols are a lawful current seam, but frozen dataclass representation is implementation shape rather than a semantic proposition.
- Falsifier: remove/rename a named schema seam or make either class non-dataclass/non-frozen; lines `23-35` fail.
- Relation `related_but_not_proved`; strength `presence_only`; disposition `retain_as_structural_support`.

## G2 — duplicate canonical slug rejection

- Test locator `48-57`; authority core lines `8-11` and working overlay lines `20, 65`.
- The assertion proves exact normalised duplicate-slug rejection for the tested two-entry document.
- It does not prove semantic distinctness or detect near-synonyms.
- Falsifier: allow both `alpha` rows to serialise; line `56` fails.
- Relation `bounded_separable_clause`; strength `boundary`; disposition `retain`.

## G3 — cross-entry alias collision rejection

- Test locator `59-82`; authority core line `9` and working overlay lines `20, 57, 65`.
- The assertion proves that the same normalised alias cannot be owned by two entries.
- It does not decide whether any proposed alias is semantically lawful.
- Falsifier: accept both `shared alias` owners; line `81` fails.
- Relation `bounded_separable_clause`; strength `boundary`; disposition `retain`.

## G4 — cross-entry disallowed-token collision rejection

- Test locator `84-107`; authority working overlay lines `20, 57, 65`.
- The assertion proves the current exact machine collision rule for the same disallowed token on two entries.
- It does not make disallowed phrases global semantic suppressors; occurrence-scoped audit law remains separate.
- Falsifier: serialise both `shared forbidden` values; line `106` fails.
- Relation `bounded_separable_clause`; strength `boundary`; disposition `retain_with_scope_warning`.

## G5 — canonical label cannot be its own alias

- Test locator `109-118`; authority core lines `8-10` and working overlay lines `20, 57, 65`.
- The assertion proves rejection of the tested self-alias collision.
- It does not prove alias semantic equivalence beyond exact token identity.
- Falsifier: accept `Parallel Risk Lane` as both canonical label and alias; line `117` fails.
- Relation `bounded_separable_clause`; strength `boundary`; disposition `retain`.

## File decision

- Groups/relationships `5/5`; final `ADMIT_TIER_A_CURRENT`.
- Admission is limited to the current schema seam and exact collision boundaries. G1's frozen dataclass representation remains structural support, not normative proof.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
