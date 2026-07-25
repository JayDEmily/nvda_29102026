# Semantic receipt — `tests/tier_a/review_runtime/test_review_contract_models.py`

- Sequence `137`, PM-016; SHA-256 `9cedc1c523b7da073350012029a8ddb667641a9ec6d10d5b407e679652d8d54e`.
- Read full test `1-120`, full review contract models, current review/explanation and vocabulary authority and PM-011 routes. Targeted run contribution: three tests passed inside `24 passed in 0.29s`.

## G1 — review model exports and coefficient fields

- Locator `22-42` proves eight exact symbols exist and two models expose a `resolved_coefficients` field.
- Presence does not establish semantic authority, required invariants, source/version lineage or correct ownership of coefficient snapshots.
- Relation `not_proved`; strength `presence_only`.

## G2 — failure taxonomy specimens

- Locator `45-89` proves selected enum strings can be carried into `FailureTaxonomyRecord` and one unknown value is rejected.
- `DATA_PROVENANCE_FAILURE`, `EXECUTION_EXPRESSION_FAILURE`, `SIZING_FAILURE`, `BAD_LUCK`, `BLOCKED_TRADE` and their combination rules are implementation-owned review taxonomy. No exact current normative proposition admits these classes, evidence-floor semantics or resolution precedence.
- The model can accept internally inconsistent flags/classes not challenged by the test.
- Relation `unsupported_policy_taxonomy`; strength `behavioural_schema_specimen`.

## G3 — economic-accountability tags

- Locator `92-120` proves six selected fields carry one bounded enum and reject one unknown string.
- The categories `value_add`, `capital_preservation`, `neutral`, `value_leak` and `unknown`, and their assignment to diagnosis/posture/timing/execution/sizing/non-action, lack exact current normative authority and no economic calculation is exercised.
- Relation `unsupported_policy_taxonomy`; strength `behavioural_schema_specimen`.

## File decision

- Groups/relationships `3/3`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve symbol/enum regression evidence only. Tier-A admission requires current propositions defining the failure taxonomy, resolution consistency and economic-accountability dimensions/tags, followed by tests of the governing invariants rather than selected serialization values.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
