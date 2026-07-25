# Semantic receipt — `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py`

## File evidence

- Sequence `105`, unit `PM-015`; test SHA-256 `194a9e3bd1d1f9247809ec5008519d9d898c7c8342dc2ec44c697f44029663ab`.
- Full reads: test `1-124`; all five enumerated active files; complete `src/nvda_desk/downstream/live_inventory.py:1-295`; relevant contracts `src/nvda_desk/contracts/downstream.py:149-205`; architecture `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`; ownership `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-195` and working supplement `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:146-153`.
- Raw test result: `4 passed in 0.13s`.

## G1 — `test_live_inventory_files_do_not_import_capital_opening_broker_or_exit_authority`

- Test locator: `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py:18-86`; AST imports in five fixed paths are checked against nine prohibited prefixes.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`; `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:146-153`.
- Authority match: the authority prohibits opening, broker placement, candidate, capital-sizing and ungoverned mutation semantics, but it does not define compliance as absence of these finite import names.
- Behaviour proved: the currently enumerated files do not directly import the listed module prefixes.
- Limitation: local aliases, indirect dependencies, runtime imports, renamed modules, injected objects and equivalent foreign authority all pass; the active-file list is manually finite.
- Adversarial challenge: move capital/opening authority behind an unlisted helper or pass it through `source_payload`; every tested import assertion remains green.
- Exact-surface falsifier: add one listed prohibited import to an enumerated file; the assertion at lines `84-86` must fail.
- Assertion that must fail and why: The empty-set assertion at lines `84-86` must fail when any one of the nine exact prohibited prefixes is imported by one of the five enumerated paths, because that mutation adds a member to the `forbidden` set computed at lines `76-83`. This only falsifies the finite direct-import condition; aliases, injected dependencies, runtime imports and unlisted helper files remain outside the detector.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; replace finite path-name exclusion with behavioural ownership and dependency tests over the complete live-inventory surface.

## G2 — `test_live_inventory_contract_fields_remain_inventory_only`

- Test locator: `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py:38-100`; five model field sets exclude nine names and a freeze-state default is asserted.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`; `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:148-152`.
- Authority match: inventory-only ownership and no invented policy are authoritative, but field-name absence and a literal freeze string do not prove source meaning or prohibit hidden authority in open mappings.
- Behaviour proved: the present top-level schemas omit the finite prohibited names and the snapshot default says `architecture_only_no_policy`.
- Limitation: both position and capital state accept arbitrary `source_payload`; aliases and nested foreign authority pass except for a separate finite donor-key blacklist; the freeze state is declarative.
- Adversarial challenge: place opening authorisation under a renamed nested key in `source_payload`; the asserted field set and freeze string remain unchanged.
- Exact-surface falsifier: add one exact prohibited field or change the default freeze value; an assertion at lines `99-100` must fail.
- Assertion that must fail and why: The disjointness assertion at line `99` must fail if one of the nine exact prohibited names becomes a top-level field on any of the five models, while the literal equality at line `100` must fail if the snapshot default changes from `architecture_only_no_policy`. Neither assertion reacts to renamed or nested authority carried inside `source_payload`, so passing them cannot establish semantic inventory-only ownership.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; constrain typed source evidence and prove semantic separation rather than exact field spelling.

## G3 — `test_live_inventory_snapshot_builder_accepts_inventory_readback_inputs_only`

- Test locator: `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py:103-110`; parameter names on `build_live_snapshot` are compared with finite allowed/prohibited sets.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:347-353`; `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:148-152`.
- Authority match: repository state and explicit live IDs are lawful inputs, but the signature test does not prove input identity, uniqueness, repository truth, exposure derivation or receipt transaction behaviour.
- Behaviour proved: the current method exposes the named readback identifiers and omits the listed opening/capital authority parameter names.
- Limitation: duplicated `live_ids` can duplicate records and inflate snapshot counts; absent repositories create identifier-only states; arbitrary repository mappings cross through `source_payload`; receipt append failure is not tested.
- Adversarial challenge: request the same stored position twice or supply a payload containing renamed placement authority; the signature assertions remain green.
- Exact-surface falsifier: add one exact prohibited parameter or remove one required name; an assertion at lines `107-110` must fail.
- Assertion that must fail and why: The disjointness check at line `107` must fail if the method signature adds an exact name from `PROHIBITED_BUILD_PARAMETERS`; the required-name subset at lines `108-110` must fail if any listed readback identifier disappears. The assertions inspect spelling only and therefore do not fail when foreign authority is hidden in an allowed object, repository payload or differently named parameter.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `signature_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; add behavioural identity, uniqueness, source-schema, fallback and transaction tests.

## G4 — `test_live_inventory_reconciliation_accepts_fill_evidence_inputs_only`

- Test locator: `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py:112-124`; the reconciliation signature is checked for six required and seven prohibited parameter names.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:347-353`; `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:148-151`.
- Authority match: fill/state updates are lawful inputs and repository/receipt ownership is explicit, but parameter spelling does not prove evidence authority, atomicity or lawful mutation.
- Behaviour proved: the method currently accepts a fill-evidence iterable and named reconciliation/inventory/capital/receipt identifiers without the listed opening parameters.
- Limitation: fill events are open mappings guarded by six exact keys; a fill ID can be reused across different positions; repository mutation occurs before receipt append, so duplicate-receipt failure leaves mutated state; no rollback, idempotency or cross-record authority proof exists.
- Adversarial challenge: reconcile a cross-position duplicate fill ID or force receipt append failure after position writes; the signature assertions remain green while state integrity fails.
- Exact-surface falsifier: add an exact prohibited parameter or remove one required name; an assertion at lines `116-124` must fail.
- Assertion that must fail and why: The disjointness assertion at line `116` must fail if an exact prohibited build parameter is added to `reconcile_fill_evidence`, and the subset assertion at lines `117-124` must fail if one of the six named inputs is removed. Those failures say nothing about the open mapping accepted as `fill_evidence`, cross-position reuse of a fill identifier, or the non-atomic write-then-receipt sequence at runtime lines `121-159`.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `signature_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; enforce typed fill evidence, global identity, atomic repository/receipt commit and rollback before Tier-A return.

## File decision

- Groups/relationships: `4/4`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- The tests preserve four narrow structural facts, but they do not prove the row-5.13 behavioural boundary and leave demonstrated identity, payload-authority and transaction defects green.
