# Semantic receipt — `tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py`

## Process and restatement
- Sequence/unit `026` / `PM-012`; SHA-256 `526c27bdd92c163037652cfb92d550d711d8094cafa3972544ce94f6ead1f9c9`.
- Read full test `1-138`, full three mappers and prepared snapshot implementation, authority and routes. Targeted pytest: `4 passed in 0.20s`.
- The file checks mapper-symbol presence, maps one prepared snapshot into temporal/regime/options typed inputs, checks explicit optional absence, and rejects temporal mapping when source date/timestamp is absent.

## Relationships
1. **`24-34`; `N04.2-009`, `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:205-217`.** Three mapper symbols exist. Proves presence only; inert/wrong mappers pass. Falsifier: remove export; `32-34` fails. `related_but_not_proved` / `presence_only`; no behavioural credit.
2. **`37-85`; `N04.2-008`/`N04.2-009`, `179-217`; options boundary `N03.2-001`, `docs/03.2...:15-29`.** Selected prepared primitives are projected into three typed stage inputs without passing the whole snapshot. Falsifier: change a mapped field; `74-85` fails. Does not prove prepared identity/lineage, mapping version, all stage-owned fields or semantic derivation truth. `bounded_separable_clause` / `behavioural`; admit narrow projection.
3. **`88-120`; `N04.2-003`/`N04.2-008`, `66-89,179-203`.** Optional regime/options values remain `None` and are named in `missing_fields`; date-only temporal truth remains date-only. Falsifier: fabricate a value or omit missing marker; `110-120` fails. Does not distinguish mandatory from optional under a complete stage contract. `bounded_separable_clause` / `boundary`; admit narrow explicit-absence behaviour.
4. **`123-138`; `N04-003`, `docs/04.1...:44-72`; `N04.2-003`.** Temporal mapper fails when neither source timestamp nor source date exists, preventing wall-clock substitution. Falsifier: return an input; expected exception fails. Does not test all invalid temporal inconsistencies. `exact_full_proof` / `boundary`; admit.

## File-level disposition
- Groups/relationships `4` / `4`; final disposition `ADMIT_TIER_A_CURRENT`.
- Admission is limited to the asserted field projections, explicit optional absence and missing-source-time failure. No prepared-envelope identity/version/fingerprint, mapping-version, complete stage-carrier, derivation, replay or end-to-end cognition claim.
- No implementation or test mutation executed.
