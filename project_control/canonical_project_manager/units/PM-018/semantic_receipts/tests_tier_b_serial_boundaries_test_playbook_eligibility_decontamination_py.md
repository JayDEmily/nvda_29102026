# Semantic receipt — `tests/tier_b/serial_boundaries/test_playbook_eligibility_decontamination.py`

- Sequence `177`, PM-018; SHA-256 `3b918e4b79ce401d2f5fa3f6869e2a678b062fdd74868e0dae99ae19fa706181`.
- Read full test `1-46`, eligibility contracts, serial evaluator/service and playbook eligibility ownership propositions. Included in Tier-B run: `49 passed in 10.75s`.

## G1 — eligibility contract/evaluator/service surfaces exist
- Locator `21-31` proves symbol/model presence only.
- Relation `related_but_not_proved`; strength `presence_only`.

## G2 — eligibility output has bounded fields and omits two capital echoes
- Locator `34-46` proves exact schema presence for admissibility/family/setup and permission/no-trade fields, plus exact absence of `fresh_deployable_capital_pct` and `inventory_action_bias`.
- This supports the serial eligibility versus downstream-capital boundary, but does not reject all semantically equivalent foreign fields or exercise compilation behaviour.
- Relation `bounded_separable_clause`; strength `boundary`.

## File decision
- Groups/relationships `2/2`; final `ADMIT_TIER_B_SHADOW`.
- Admit the exact closed-schema boundary as shadow evidence. Promotion requires behavioural eligibility compilation and broader closed-schema foreign-authority rejection.
