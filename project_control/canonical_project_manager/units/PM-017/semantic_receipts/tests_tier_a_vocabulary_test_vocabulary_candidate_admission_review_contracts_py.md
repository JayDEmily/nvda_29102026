# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_candidate_admission_review_contracts.py`

- Sequence `155`, PM-017; SHA-256 `d161f3cfd2232baf6f64e30f5c64bfe808197903eca819d44c28076329d41755`.
- Read full test `1-172`, full review helper implementation and workflow admission `ATLAS_FEATURE_ADMISSION_011`. Targeted run: `9 passed` inside `63 passed, 3 failed in 5.75s`.

## G1 — non-quarantine alias plan is reported admissible
- Locator `32-41` requires admissible status, alias-only plan and no error.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G2 — quarantine is reported without aborting review
- Locator `44-52` requires quarantined status, retained plan and reason.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G3 — incomplete add-new candidate is reported invalid
- Locator `55-65` requires invalid status and exact missing-field error.
- Relation `bounded_separable_clause`; strength `boundary`.
## G4 — malformed bridge payload is reported invalid
- Locator `68-76` retains candidate slug and missing-label error without a plan.
- Relation `bounded_separable_clause`; strength `boundary`.
## G5 — batch payload reviews preserve order and statuses
- Locator `79-97` requires ordered admissible/quarantined/invalid results.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G6 — review summary counts statuses and actions
- Locator `100-121` requires exact status/action counts while invalid entries contribute no action.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G7 — review report is JSON-ready
- Locator `124-140` requires status/action/reason serialization for admissible and quarantined entries.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G8 — invalid payload remains visible in report
- Locator `143-157` requires invalid count and retained candidate row with no plan.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G9 — non-list aliases become invalid review evidence
- Locator `160-172` requires invalid status, retained slug and exact error.
- Relation `bounded_separable_clause`; strength `boundary`.

## File decision

- Groups/relationships `9/9`; final `ADMIT_TIER_A_CURRENT` under `ATLAS_FEATURE_ADMISSION_011`.
- Review statuses are operational routing evidence only; `admissible` does not itself admit a durable term.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
