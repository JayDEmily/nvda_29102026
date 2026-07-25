# Semantic receipt — `tests/tier_a/normative_authority/test_gate_c_remaining_normative_contracts.py`

- Sequence `148`, PM-017; SHA-256 `d1544b9fa8fd2c8339ed4cbc83694fb2cbfbbf93823d85c7d12fecd61029a98b`.
- Read full test `1-277`, directly exercised signal, identifier, SQL, coefficient, expression, capital, inventory, overnight and review surfaces, propositions `C-007;C-014;C-022;C-029;C-030;C-034;C-037;C-040;C-042;C-044`, and Gate C admission evidence. Targeted run: `7 passed, 4 failed`, within the frozen expected-red pack.

## G1 — registry-driven signal family preserves source identity and no decision side effects
- Locator `35-60` adds one coverage entry and requires source/family identity, unchanged dataset payload and empty decision-side-effect list.
- Relation `bounded_separable_clause`; strength `identity_lineage`.
## G2 — raw signal contract carries observation time
- Locator `63-64` requires at least one of two exact temporal fields. This is intentionally minimal schema proof, not full temporal semantics.
- Relation `bounded_separable_clause`; strength `presence_only`.
## G3 — identifier-role matrix covers mandatory roles and ownership
- Locator `67-98` requires eleven roles, uniqueness, non-empty originator/forbidden-creator columns and fail/withhold semantics for mandatory absence.
- It proves the checked matrix content, not runtime propagation.
- Relation `bounded_separable_clause`; strength `presence_only`.
## G4 — durable SQL demo remains bounded away from material state ownership
- Locator `101-118` requires an exact five-method public surface and absence of four material-state writer names.
- This exact class surface is proved; semantic equivalents elsewhere are not.
- Relation `bounded_separable_clause`; strength `boundary`.
## G5 — coefficient receipt preserves baseline/effective/modifier/closed authority
- Locator `121-137` requires authority/schema/fingerprint plus exact coefficient values, modifier input and two closed authority classes.
- Relation `bounded_separable_clause`; strength `identity_lineage`.
## G6 — coefficient authority is path-substitutable and replay-versioned
- Locator `140-156` substitutes a YAML authority ID and requires that ID, schema version and replay fingerprint in the receipt.
- Relation `bounded_separable_clause`; strength `substitution`.
## G7 — execution expression carries candidate identity without capital/broker fields
- Locator `159-180` requires `candidate_id` and excludes four exact top-level authority fields.
- This does not detect renamed/nested authority or side effects.
- Relation `bounded_separable_clause`; strength `boundary`.
## G8 — capital sizing is reproducible and independent of serial confidence
- Locator `210-226` requires equal sizing at confidence 0.1/0.9, deterministic receipt, policy trace and closed placement authority.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G9 — fill reconciliation is idempotent and inventory snapshot excludes serial outputs
- Locator `229-247` requires duplicate fill rejection and absence of one exact serial field.
- It proves the duplicate specimen and field boundary, not complete atomicity across state and receipt.
- Relation `bounded_separable_clause`; strength `state_transition`.
## G10 — overnight carry carries policy and next-session source identity
- Locator `250-262` requires one policy field and at least one of two source identity fields. Schema proof only.
- Relation `bounded_separable_clause`; strength `presence_only`.
## G11 — review packets expose missing material/lineage without runtime mutation default
- Locator `265-277` requires missing-material and source-lineage field families and false default runtime mutation.
- The flag default is not behavioural non-mutation proof.
- Relation `bounded_separable_clause`; strength `presence_only`.

## File decision

- Groups/relationships `11/11`; final `ADMIT_TIER_A_CURRENT` under the Gate C admission receipt.
- Four current failures remain Gate D implementation obligations. Token/field absence clauses are admitted only for their exact named surfaces.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
