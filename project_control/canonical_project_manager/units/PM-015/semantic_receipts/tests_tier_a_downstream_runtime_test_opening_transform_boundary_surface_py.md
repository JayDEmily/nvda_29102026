# Semantic receipt — `tests/tier_a/downstream_runtime/test_opening_transform_boundary_surface.py`

## File evidence

- Sequence `109`, unit `PM-015`; test SHA-256 `b0a0bc6b165e89094004b578a1201e6afd74de976fddc91df2c19f2758e2d21e`.
- Full reads: test `1-97`; complete opening implementation `src/nvda_desk/downstream/opening.py:1-119`; handoff validator `src/nvda_desk/contracts/downstream.py:63-101,234-260`; capital decision `src/nvda_desk/contracts/capital.py:150-179`; row-5.12/P1 opening and protocol authority.
- Raw test result: `3 passed in 0.13s`.

## G1 — `test_placement_handoff_rejects_execution_record_donor_payload_shape`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_transform_boundary_surface.py:16-22,53-67`; one nested payload containing exact execution-record keys is rejected.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`; P1 `Placement Handoff` and `Broker Protocol` records `P1-113`, `P1-114`; donor evidence is not live authority under `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:138-149`.
- Authority match: execution records and broker fills are outside the protocol-only handoff, and this is one bounded exact-key enforcement path.
- Behaviour proved: recursive validation rejects the tested `ExecutionRecord`, execution ID, fill ID and fill-price markers.
- Limitation: the validator is a finite exact-key blacklist; aliases, values, encoded records and future execution fields pass through the open preview mapping.
- Adversarial challenge: rename the same record fields to native-looking aliases; handoff validation succeeds.
- Exact-surface falsifier: permit the tested exact execution-record keys; the `pytest.raises` assertion at lines `54-67` must fail.
- Assertion that must fail and why: The `pytest.raises` context at lines `54-67` must fail if the handoff accepts the supplied nested `ExecutionRecord`, execution ID, fill ID and fill-price keys, because contract lines `85-101` recursively intersect those exact keys with a finite blacklist. Renaming the same record fields or encoding them as values leaves the open mapping valid.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; preserve the exact regression while replacing open preview payloads with a typed adapter-neutral handoff contract.

## G2 — `test_opening_service_preview_stays_in_native_handoff_shape`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_transform_boundary_surface.py:23-29,70-81`; one service output is compared with a five-key test-local set and a forbidden-key set.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`; P1 `Placement Handoff` record `P1-113`.
- Authority match: the five current keys are compatible with bounded handoff material, but the higher authority does not establish this exact open-mapping schema as complete or sufficient transformation.
- Behaviour proved: for one fabricated continue decision, the service emits exactly the five asserted top-level keys and none of the five test-listed execution-record keys.
- Limitation: values and cross-object identities are not validated; upstream capital truth is fabricated; the allowed set is test-authored; renamed execution semantics and unlisted keys can be added if the test constant is changed with them.
- Adversarial challenge: encode an execution instruction in `placement_constraint_ids` or under a renamed allowed value; all asserted key checks remain green.
- Exact-surface falsifier: add, remove or rename a current preview key, or insert one exact forbidden key; an assertion at lines `78-81` must fail.
- Assertion that must fail and why: The exact-key equality at line `80` must fail if the service preview adds, removes or renames a top-level key relative to the test-authored five-key set; the intersection assertion at line `81` must fail if one of the five exact execution-record keys appears anywhere in the preview. Neither assertion validates values, lineage or whether the allowed keys themselves conceal execution semantics.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; derive a typed preview schema from admitted authority and test value semantics and identity lineage.

## G3 — `test_opening_transform_boundary_does_not_import_execution_record_contracts`

- Test locator: `tests/tier_a/downstream_runtime/test_opening_transform_boundary_surface.py:84-97`; one source file is AST/text scanned for two exact names.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:330-336`; donor/target ownership law at `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:508`.
- Authority match: opening must not own execution records, but absence of two names in one file is not semantic transformation proof.
- Behaviour proved: `opening.py` does not directly import `ExecutionRecord` and does not contain the exact text `broker_execution_record`.
- Limitation: indirect imports, aliases, other files, injected dependencies, copied logic and renamed execution semantics pass.
- Adversarial challenge: import a wrapper or use `BrokerFillRecord`; both assertions remain green.
- Exact-surface falsifier: add the exact import or token to `opening.py`; an assertion at lines `96-97` must fail.
- Assertion that must fail and why: The assertion at line `96` must fail if `opening.py` directly imports a symbol named exactly `ExecutionRecord`, and line `97` must fail if the exact text `broker_execution_record` appears anywhere in that file. A wrapper import, alias, injected dependency, another module or renamed execution behaviour does not trigger either lexical check.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; prove complete dependency and behavioural ownership boundaries rather than two lexical absences.

## File decision

- Groups/relationships: `3/3`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- The exact execution-record key guard is useful, but a test-local five-key shape and one-file lexical scan do not prove native transformation, truthful upstream authority or complete protocol separation.
