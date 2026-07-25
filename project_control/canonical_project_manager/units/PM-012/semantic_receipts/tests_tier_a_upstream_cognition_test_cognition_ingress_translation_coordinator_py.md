# Semantic receipt — `tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py`

## Process/restatement
- Sequence `027`, PM-012; SHA `51865e58ebf373de06d6a0eb4bdf5efbad1c09fb27a8ae93abc22d6cf9aae397`.
- Read full test `1-82`, translator, stage-input bundle and called preparation/mappers; routes inspected. Pytest: `2 passed in 0.18s`.
- The file checks translator symbols and runs one API-shaped raw bundle through preparation and translation, asserting selected temporal, regime and options values in a typed `StageInputBundle`.

## Relationships
1. `26-31`; `N04.2-009`, `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:205-217`: symbol presence only. Removing an export fails `30-31`; inert/wrong implementations pass. `related_but_not_proved` / `presence_only`; no behavioural credit.
2. `34-82`; `N04.2-008`/`N04.2-009`, `179-217`, and `N03.2-001`, `docs/03.2...:15-29`: one prepared dataset is narrowed into three typed carriers and selected values retain their chosen source sections. Altering a mapped value/type fails `73-82`. It does not prove common-context identity/lineage/version/fingerprint, all stage carriers, field-resolution receipts, source truth or replay. `bounded_separable_clause` / `behavioural`; admit narrow end-to-end projection specimen.

## File disposition
- Groups/relationships `2/2`; `ADMIT_TIER_A_CURRENT` limited to the observed raw→prepared→three-carrier field projection and typed bundle construction.
- No complete preparation, lineage, six-stage ingress, replay or authority-boundary claim. No implementation/test mutation.
