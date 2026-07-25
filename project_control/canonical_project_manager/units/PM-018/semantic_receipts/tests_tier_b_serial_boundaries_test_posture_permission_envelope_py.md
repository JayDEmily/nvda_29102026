# Semantic receipt — `tests/tier_b/serial_boundaries/test_posture_permission_envelope.py`

- Sequence `178`, PM-018; SHA-256 `1e54f36e12b7b6826826af356c3214c55a85f1ee8a2357eb88a6478c86733851`.
- Read full test `1-111`, posture contracts/evaluator/service, modifier/coefficient services and accepted coefficient/modifier vocabulary decisions. Included in Tier-B run: `49 passed in 10.75s`.

## G1 — posture contract/evaluator/service surfaces exist
- Locator `21-32` proves symbol/model presence only.
- Relation `related_but_not_proved`; strength `presence_only`.

## G2 — posture output separates permission envelope from two capital fields
- Locator `35-46` proves exact posture fields and exact absence of `deployment_action` and `authorised_notional_usd`.
- This is a valid bounded schema clause, but not full proof that posture cannot emit capital authority under other names or channels.
- Relation `bounded_separable_clause`; strength `boundary`.

## G3 — calm and stressed evaluations expose current coefficient/modifier values
- Locator `49-111` proves the current service produces allow/block states, exact 24/32 thresholds, baseline 0.35, stressed 0.25, hedge false/true and modifier-input carriage for two specimens.
- The exact numeric policy, caller-selected `negative_gamma_stress` activation and current config are implementation/config evidence. No current normative proposition establishes these exact values or this activation mechanism; the underlying source also depends on the non-admitted mutable/baseline surface taxonomy even though this test does not assert its label.
- Relation `authority_missing`; strength `behavioural`.

## File decision
- Groups/relationships `3/3`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Retain G2 as shadow-worthy boundary evidence. G3 requires explicit policy authority, version/fingerprint lineage and state-activation law before promotion; passing current-value assertions cannot create that authority.
