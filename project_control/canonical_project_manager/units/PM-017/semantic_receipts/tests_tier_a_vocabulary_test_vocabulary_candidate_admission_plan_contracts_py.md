# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_candidate_admission_plan_contracts.py`

- Sequence `154`, PM-017; SHA-256 `fa801297cf36dba727ab8c4c6e993d1ba3a11ff648a121424f75192b8cbbe23f`.
- Read full test `1-278`, full candidate/admission implementation and workflow admissions `ATLAS_FEATURE_ADMISSION_006` and `007`. Targeted run: `13 passed` inside `63 passed, 3 failed in 5.75s`.

## G1 — quarantine plan serialises without a mutation plan
- Locator `33-52` requires quarantine action, no proposed entry/aliases and stable review payload.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G2 — add-new planning requires complete governance metadata
- Locator `55-59` requires missing owner/contract/raw-derived metadata to fail.
- Relation `bounded_separable_clause`; strength `boundary`.
## G3 — add-new planning produces one validated proposed entry
- Locator `62-89` requires exact field projection and no quarantine/alias plan.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G4 — alias-only planning offers only non-duplicate aliases
- Locator `92-104` requires existing alias match and one fresh alias candidate.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G5 — enrich-existing planning offers a non-duplicate alias
- Locator `107-118` requires existing-slug classification and one extension alias.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G6 — admission summary counts the four mechanical actions
- Locator `121-143` requires one count for each governed proposal label.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G7 — batch plans preserve input order
- Locator `146-157` requires alias-only then quarantine in source order.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G8 — add-new application returns a new document
- Locator `160-175` requires the source document unchanged and the new validated entry present in the returned document.
- Relation `bounded_separable_clause`; strength `state_transition`.
## G9 — alias application returns an updated copy
- Locator `178-188` requires existing and fresh aliases in the returned entry.
- Relation `bounded_separable_clause`; strength `state_transition`.
## G10 — quarantine application is rejected
- Locator `191-195` requires a quarantined candidate not to be applied.
- Relation `bounded_separable_clause`; strength `boundary`.
## G11 — ordered batch application composes alias and new-entry changes
- Locator `198-219` requires ordered pure-document application.
- Relation `bounded_separable_clause`; strength `state_transition`.
## G12 — blank governance metadata is rejected
- Locator `222-245` requires blank owner and contract values to fail separately.
- Relation `bounded_separable_clause`; strength `boundary`.
## G13 — multi-owner alias collision is quarantined before application
- Locator `248-278` requires cross-entry collision to reject rather than mutate.
- Relation `bounded_separable_clause`; strength `boundary`.

## File decision

- Groups/relationships `13/13`; final `ADMIT_TIER_A_CURRENT` under `ATLAS_FEATURE_ADMISSION_006/007`.
- These are mechanical planning and pure-document proof helpers only. No result constitutes human semantic admission or permission to write the committed canonical vocabulary.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
