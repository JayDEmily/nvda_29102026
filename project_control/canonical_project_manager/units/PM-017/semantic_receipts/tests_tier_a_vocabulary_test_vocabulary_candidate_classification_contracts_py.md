# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_candidate_classification_contracts.py`

- Sequence `156`, PM-017; SHA-256 `275d6d12dd1aa63eaad7e73b60cd2e0281351766a3a0e7bbe75dbf77407ece57`.
- Read full test `1-132`, full classifier implementation and workflow admission `ATLAS_FEATURE_ADMISSION_002`. Targeted run: `8 passed` inside `63 passed, 3 failed in 5.75s`.

## G1 — classifier action enum is exactly the governed proposal set
- Locator `36-42` requires four action labels.
- Relation `exact_full_proof`; strength `presence_only`.
## G2 — canonical slug match proposes enrich-existing
- Locator `45-54` requires one slug-collision specimen.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G3 — canonical label match proposes enrich-existing
- Locator `57-66` requires one label-collision specimen.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G4 — allowed alias match proposes alias-only
- Locator `69-78` requires one allowed-alias specimen and owning slug.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G5 — no collision proposes add-new
- Locator `81-92` requires one collision-free specimen with no matched slug.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G6 — disallowed phrase proposes quarantine
- Locator `95-104` requires one disallowed-token specimen and owning slug.
- Relation `bounded_separable_clause`; strength `boundary`.
## G7 — multi-entry collision proposes quarantine
- Locator `107-116` requires conflicting slug/label ownership to quarantine without selecting one owner.
- Relation `bounded_separable_clause`; strength `boundary`.
## G8 — classification serialisation is stable
- Locator `119-132` requires exact add-new payload/reason serialization.
- Relation `bounded_separable_clause`; strength `behavioural`.

## File decision

- Groups/relationships `8/8`; final `ADMIT_TIER_A_CURRENT` under `ATLAS_FEATURE_ADMISSION_002`.
- These token/collision outcomes are proposals only and do not prove synonymy, novelty, ownership, scope or final human disposition.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
