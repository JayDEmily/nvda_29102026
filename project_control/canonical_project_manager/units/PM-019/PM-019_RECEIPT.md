# PM-019 integration receipt

## Outcome

`FAIL — integration candidate projected, active configuration projection blocked.`

PM-019 began only after the absolute semantic ledger reached `179 YES / 0 NO`. Deterministic projection copied the completed receipts into four current registers without generating or changing semantic decisions:

- `P2_CURRENT_TEST_AUTHORITY_CANDIDATE_REGISTER.tsv` — `179` files;
- `P2_ASSERTION_GROUP_PROPOSITION_TRACEABILITY_REGISTER.tsv` — `777` assertion groups;
- `P2_PROOF_DISPOSITION_REGISTER.tsv` — `179` file dispositions; and
- `P2_DEPENDENCY_RETURN_GATE_REGISTER.tsv` — `143` non-admitted files.

## Current file decisions

- `31 ADMIT_TIER_A_CURRENT`
- `5 ADMIT_TIER_B_SHADOW`
- `74 BLOCKED_P3_REPAIR`
- `35 BLOCKED_MISSING_NORMATIVE_AUTHORITY`
- `20 NON_AUTHORITATIVE_OBSERVATIONAL`
- `14 RETIREMENT_RECOMMENDED_NOT_EXECUTED`

## Validator result

`PM-019_VALIDATION.txt` exits `1` and states the required warning:

> Structural validation does not establish semantic acceptance.

Verified mechanically:

- all 179 physical files occur exactly once;
- all 777 receipt-declared groups occur once;
- all 143 non-admitted files occur in the return-gate register;
- rejected file dispositions were not restored through a generic candidate status; and
- the proof register covers the same 179-file population.

Failed mechanically:

- `99` assertion groups do not project one allowed semantic-relation enum;
- `123` assertion groups do not project one allowed proof-strength enum;
- `214` admitted assertion-group relationships lack an exact group-level authority locator projection; and
- `6` non-admitted receipts lack a mechanically detectable explicit deficit/return-gate phrase in the projected file-decision section.

## Configuration gate

`config/retained_test_registry.yaml` and `config/proof_blocks.yaml` were **not changed**. Section 10 of the ExecPlan permits those projections only after the PM-019 registers agree. They do not agree, so changing active authority configuration would be an unauthorised promotion and would hide the failed integration state.

## Return gate

Project Manager or an authorised semantic repair pass must reopen the identified receipt relationships one file at a time, normalise only after rereading the test, exercised surfaces and authority, and then rerun PM-019. No bulk semantic rewrite is lawful.

PM-019 integration evidence is complete as a failed candidate. It does not establish P2 acceptance.
