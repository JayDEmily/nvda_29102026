# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py`

- Sequence `161`, PM-017; SHA-256 `16d933649798c8f27e90e09613873abc83757c1298ef9ec02e5f406b96c5f6e5`.
- Read full test `1-95`, `src/nvda_desk/schemas/vocabulary.py` JSON-helper and document-validation surfaces, and `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` lines 65-82. Targeted run: `5 passed in 0.05s`.
- Starting state: one valid synthetic vocabulary document or one deliberately invalid JSON/document specimen. Action: call one schema JSON helper. Observed surface: returned validated document, raised validation error, emitted JSON text, or filesystem existence. The file does not observe builder regeneration, semantic term admission, synonym-audit suppression, or full canonical-vocabulary parity.

## G1 — JSON mapping decode and governed document validation

- Test locator `37-43`; authority `ATLAS_FEATURE_ADMISSION_001`, workflow lines `67-69, 76-82`.
- The assertion proves that `from_json_text` decodes a mapping, delegates through the governed schema, and preserves the tested category, raw/derived tag and alias.
- It does not prove all document fields, builder ownership or semantic completeness.
- Falsifier: return an unvalidated dictionary or coerce the tested enum/alias incorrectly; assertions at lines `41-43` necessarily fail.
- Relation `bounded_separable_clause`; strength `behavioural`; disposition `retain`.

## G2 — non-mapping JSON root rejection

- Test locator `46-48`; authority workflow lines `69, 76-82`.
- The assertion proves rejection of the tested list-root specimen before document construction.
- It does not prove rejection of every malformed JSON text or every invalid mapping field.
- Falsifier: permit a list root; the expected-exception assertion at line `47` fails.
- Relation `bounded_separable_clause`; strength `boundary`; disposition `retain`.

## G3 — delegated governed-category rejection

- Test locator `51-56`; authority workflow lines `69, 72, 76-82`.
- The assertion proves that a decoded mapping with the tested ungoverned category reaches schema validation and is rejected.
- It does not prove semantic admission decisions or all schema constraints.
- Falsifier: bypass `VocabularyDocument` validation or accept the tested category; line `55` fails.
- Relation `bounded_separable_clause`; strength `boundary`; disposition `retain`.

## G4 — UTF-8 path helper delegation

- Test locator `59-67`; authority workflow lines `70, 76-82`.
- The assertion proves that the path helper reads the tested UTF-8 file and returns the validated canonical label through the text helper.
- It does not prove arbitrary encoding support, atomic file access or builder regeneration.
- Falsifier: read a different path/encoding or bypass parsing so the entry is absent; line `67` fails.
- Relation `exact_full_proof`; strength `behavioural`; disposition `retain`.

## G5 — validated JSON serialisation, round trip and no canonical-file write

- Test locator `70-95`; authority workflow lines `71-72, 76-82`.
- The assertions prove newline-terminated serialisation of the tested validated document, round-trip preservation of its raw/derived tag, and absence of a write to the nominated canonical-vocabulary path.
- They do not prove builder/generator parity, semantic completeness, or absence of writes to every other path.
- Falsifier: remove the newline, mutate the nominated path, or lose the tag on round trip; lines `93-95` fail.
- Relation `bounded_separable_clause`; strength `behavioural`; disposition `retain`.

## File decision

- Groups/relationships `5/5`; final `ADMIT_TIER_A_CURRENT`.
- The file is current bounded proof for the three admitted JSON schema helpers only. It must not be cited as vocabulary semantic admission, synonym-audit cleanliness, or committed builder parity.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
