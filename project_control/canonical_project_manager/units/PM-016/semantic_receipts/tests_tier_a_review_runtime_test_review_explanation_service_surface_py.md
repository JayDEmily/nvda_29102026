# Semantic receipt — `tests/tier_a/review_runtime/test_review_explanation_service_surface.py`

- Sequence `138`, PM-016; SHA-256 `3c841cb5346a6fc341acf0ce222b33a2e653bd57ac0c11cecdd34f5aebe3d5ab`.
- Read full test `1-110`, full review explanation service and contracts, coefficient snapshot contract, current review/explanation/replay authority and PM-011 routes. Targeted run contribution: four tests passed inside `24 passed in 0.29s`.

## G1 — service symbol presence

- Locator `29-32` proves the module/class exists only.
- Relation `not_proved`; strength `presence_only`.

## G2 — missing-material report for empty inputs

- Locator `35-55` proves empty inputs produce three selected missing-material labels, empty lineage lists and `lineage_complete=False`.
- This is useful fail-visible behaviour for the exercised fields. It omits source packet IDs from the completeness criteria and does not require versions, retrievability, state/output evidence or truthful source availability.
- Relation `bounded_clause_partially_proved`; strength `behavioural`.

## G3 — detached lineage output

- Locator `57-79` proves output list mutation does not mutate two input models and marks `lineage_complete=True` when summary, one resolved-surface string and one packet ID are present.
- The completeness label is overclaimed: caller-supplied IDs/labels are accepted without verifying any underlying evidence or source packet. Current authority states complete preserved evidence is not established.
- Relation `contradictory_completeness_claim`; strength `behavioural`.

## G4 — coefficient snapshot detachment

- Locator `81-110` proves a resolved-coefficient model is serialised into a detached dictionary.
- It does not prove the coefficient/policy is governed, that `owner_stage="review"` is lawful, or that the snapshot is complete/versioned. The test protects copy safety only.
- Relation `related_but_not_proved`; strength `behavioural_copy_boundary`.

## File decision

- Groups/relationships `4/4`; final `BLOCKED_P3_REPAIR`.
- Preserve missing-material and copy-detachment clauses. Repair must define completeness from verified retrievable source/version/state/output evidence, require source-packet availability where applicable, and avoid declaring lineage complete from caller IDs and surface labels alone.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
