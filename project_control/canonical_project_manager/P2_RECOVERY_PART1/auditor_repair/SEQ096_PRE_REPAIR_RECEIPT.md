# Semantic receipt — `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py`

## File evidence

- Sequence `096`, unit `PM-015`; test SHA-256 `05c0d0c76deedd93be4e28ef5580beee9e2c0e333f8a2fa4cdaf255915a3ad23`.
- Full reads: test `1-361`; complete service `src/nvda_desk/downstream/live_inventory.py`; wrapper `src/nvda_desk/services/downstream_live_inventory_service.py`; position, capital and receipt repositories; live-inventory ownership `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-195`; target architecture `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`; transaction law `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-76`.
- Raw test result: `15 passed in 0.16s`.
- Adversarial probe: `project_control/canonical_project_manager/P2_RECOVERY_PART1/validation/096_adversarial_probe.txt` demonstrates duplicate requested-ID exposure inflation, cross-position duplicate fill acceptance, nested placement-authority acceptance, and position mutation surviving a duplicate-receipt failure.

## G1 — `test_downstream_live_inventory_service_surface_is_present`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:31-34`; assertions import one module and one class name.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`.
- Authority match: a live-inventory service belongs at this owner, but import/class presence does not prove its lawful inputs, outputs or state boundaries.
- Behaviour proved: the exact module and class attribute are importable.
- Limitation: no service method, repository read, reconciliation, receipt or prohibited-decision behaviour is exercised.
- Adversarial challenge: replace the class with an empty shell retaining its name; the test remains green.
- Exact-surface falsifier: remove or rename the class; the assertion at line `34` must fail.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; presence is supporting inventory only, not Tier A proof.

## G2 — snapshot repository reads and copy isolation

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:37-67,148-194`; three tests assert position/capital readback, selected snapshot identity, wrapper argument normalisation, receipt carriage and repository copy isolation.
- Authority locator: `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-195` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`.
- Authority match: reading repo-native position/capital state into a bounded inventory snapshot is a lawful separable clause.
- Behaviour proved: the service reads the asserted in-memory repository records, can select a named capital snapshot, normalises bounded wrapper inputs, derives the asserted receipt IDs and does not mutate the stored position when the returned snapshot is changed.
- Limitation: repositories are volatile arbitrary mappings; execution-record truth versus placeholder status, state versions, missing requested IDs, cross-object consistency, durability and restart behaviour are unproved.
- Adversarial challenge: return stale or semantically false mappings with the expected IDs and values; all assertions remain green.
- Exact-surface falsifier: read the latest capital snapshot instead of the requested one, retain a shared repository payload reference, or lose one asserted ID/value; an assertion at lines `51-67`, `160-162` or `184-194` must fail.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain these regressions while adding typed source truth, version and missing-state semantics.

## G3 — `test_live_inventory_receipt_write_is_explicit_and_append_only`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:70-86`; assertions verify one receipt kind/payload and duplicate-ID rejection.
- Authority locator: `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:21-44,50-76`.
- Authority match: explicit receipt append and duplicate rejection are lawful bounded clauses, while the same authority expressly states the current independent memory stores are not atomically bound or durable.
- Behaviour proved: snapshot receipt append is explicit, copyable and locally duplicate-protected in one process.
- Limitation: no idempotency fingerprint, state version, sequence, atomic state/receipt commit, conflict result, durability or restart recovery is proved.
- Adversarial challenge: append the receipt independently from material state or lose it on restart; the test remains green.
- Exact-surface falsifier: omit the receipt, alter its kind/payload, or allow a duplicate ID; an assertion at lines `81-86` must fail.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require the N-06 transaction/idempotency contract before Tier A admission.

## G4 — `test_live_inventory_does_not_invent_undeclared_exposure`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:89-96`; quantity-only state must produce no declared-exposure value.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354` and `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-181`.
- Authority match: the inventory surface may report preserved state but must not invent valuation/risk policy from quantity.
- Behaviour proved: the current aggregation ignores quantity when no `declared_exposure` is supplied.
- Limitation: the supplied declared exposure itself is not authenticated, typed, valued, versioned or reconciled to capital/risk limits.
- Adversarial challenge: supply an arbitrary false `declared_exposure`; the test accepts and reports it.
- Exact-surface falsifier: derive exposure from quantity in this fixture; the empty-map assertion at line `96` must fail.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; preserve non-invention while governing exposure source and valuation truth.

## G5 — `test_live_inventory_module_does_not_import_broker_or_candidate_authority`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:99-119`; an AST scan excludes four exact import roots from one file.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:347-353`.
- Authority match: broker placement, candidate formation and raw ingress are prohibited, but finite direct-import absence is not behavioural authority isolation.
- Behaviour proved: the scanned file has no direct import matching the four exact roots.
- Limitation: aliases, indirect imports, injected collaborators, open payloads, calls through other modules and side effects remain green.
- Adversarial challenge: import an alias or accept broker/candidate authority through a dictionary or collaborator outside the four roots.
- Exact-surface falsifier: add one direct forbidden import; the assertion at lines `115-119` must fail.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; replace finite import scans with executable authority-boundary tests.

## G6 — identifier validation and normalisation

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:122-145`; blank live/inventory/receipt IDs are rejected and one requested position ID is trimmed before readback.
- Authority locator: `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:29-38,50-56`.
- Authority match: stable non-empty command/state/receipt identities are necessary bounded clauses.
- Behaviour proved: the tested blank identifiers fail and whitespace around one requested ID is removed.
- Limitation: duplicate requested IDs are not rejected or deduplicated; the probe proves `[pos-1,pos-1]` doubles declared exposure from `2.5` to `5.0`.
- Adversarial challenge: repeat a normalised ID or use semantically colliding identities; current assertions remain green.
- Exact-surface falsifier: accept a tested blank ID or fail to trim the single requested ID; an assertion at lines `125-145` must fail.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; add uniqueness/collision invariants before aggregation.

## G7 — nominal fill reconciliation

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:197-263`; two caller mappings update one position, exposure, fill lists and one receipt.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`, `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:95-103`, and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-44`.
- Authority match: executed fill/state evidence may lawfully update live inventory, but an inventory reconciliation must consume admitted prior execution truth and commit state plus receipt atomically.
- Behaviour proved: the service normalises the supplied mappings, sums two declared-exposure deltas, records them in one in-memory position and emits the asserted reconciliation receipt payload.
- Limitation: arbitrary caller dictionaries stand in for execution evidence; source, execution/fill identity, quantity/price/economic invariants, prior state version and atomic receipt commit are absent.
- Adversarial challenge: label fabricated caller data `execution_event_repository` or use nonsensical numeric/state combinations; the test passes.
- Exact-surface falsifier: alter the asserted normalisation, exposure sum, stored fill list or receipt values; an assertion at lines `229-263` must fail.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require typed admitted execution evidence and N-06 transaction semantics.

## G8 — fill-evidence input boundary

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:266-301`; blank fill/position identity, one top-level broker key and empty input are rejected.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:347-353` and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:29-44`.
- Authority match: non-empty identities, non-empty commands and exclusion of placement authority are lawful bounded clauses.
- Behaviour proved: the exact tested invalid inputs fail before the nominal reconciliation path.
- Limitation: the key guard is top-level only; the probe proves nested `metadata.broker_order_id` is accepted and persisted. Other broker/execution aliases and semantic invalidity remain untested.
- Adversarial challenge: nest a forbidden placement field or rename it; all listed tests remain green.
- Exact-surface falsifier: accept one tested blank/empty input or top-level `broker_order_id`; the corresponding `pytest.raises` assertion at lines `269-301` must fail.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; use typed fill evidence and recursive/semantic authority rejection.

## G9 — duplicate and replay protection

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:304-361`; duplicate IDs within one request and replay against the same stored position must fail without changing that position.
- Authority locator: `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:42-76`.
- Authority match: duplicate replay must not repeat mutations, and state plus receipt must be one truthful transaction.
- Behaviour proved: the tested same-batch duplicate and same-position stored duplicate are detected before the asserted position changes.
- Limitation: duplicate identity is not global across positions; the probe proves the same `fill-1` is accepted on a later different position. More critically, position writes occur before receipt append: the probe shows a duplicate receipt raises while the new position remains mutated, contrary to lines `21-44`.
- Adversarial challenge: reuse a fill ID on another position or force receipt append failure after mutation; current tests remain green.
- Exact-surface falsifier: allow either tested duplicate to change `pos-1`; an assertion at lines `308-327` or `343-361` must fail.
- Semantic relation: `authority_contradictory`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require consistency-unit-scoped idempotency plus atomic rollback/commit tests before Tier A admission.

## File decision

- Groups/relationships: `9/9`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Nominal repository reads, copy isolation, exposure non-invention and local duplicate guards are useful; executable probes prove material identity, nested-authority and atomic-transaction defects.
