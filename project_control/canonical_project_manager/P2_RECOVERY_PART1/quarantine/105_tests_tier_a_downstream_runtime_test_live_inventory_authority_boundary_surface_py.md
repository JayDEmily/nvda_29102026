# Reconstructed semantic receipt — `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py`

- Sequence `105`, PM-015; test SHA-256 `194a9e3bd1d1f9247809ec5008519d9d898c7c8342dc2ec44c697f44029663ab`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.downstream: DownstreamLiveInventorySnapshot, InventoryExposureState, InventoryStateReceipt, LiveCapitalState, LivePositionState; nvda_desk.downstream.live_inventory: DownstreamLiveInventoryService.
- Surviving decision summary: Import, field and signature name checks underprove row 5.13; arbitrary source_payload carries foreign authority, duplicate fallback IDs inflate state, and reconciliation transaction defects remain untested.

## Complete test restatement

- Lines `73-86` `test_live_inventory_files_do_not_import_capital_opening_broker_or_exit_authority`: executes the named specimen/boundary and observes checks at lines `84`. The exact assertions are enumerated in the relationship sections below.
- Lines `89-100` `test_live_inventory_contract_fields_remain_inventory_only`: executes the named specimen/boundary and observes checks at lines `99, 100`. The exact assertions are enumerated in the relationship sections below.
- Lines `103-110` `test_live_inventory_snapshot_builder_accepts_inventory_readback_inputs_only`: executes the named specimen/boundary and observes checks at lines `107, 108`. The exact assertions are enumerated in the relationship sections below.
- Lines `112-124` `test_live_inventory_reconciliation_accepts_fill_evidence_inputs_only`: executes the named specimen/boundary and observes checks at lines `116, 117`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_live_inventory_files_do_not_import_capital_opening_broker_or_exit_authority`

- Test locator: `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py:73-86`. Checks: L84 assert `forbidden == set()`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Import, field and signature name checks underprove row 5.13; arbitrary source_payload carries foreign authority, duplicate fallback IDs inflate state, and reconciliation transaction defects remain untested.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_live_inventory_contract_fields_remain_inventory_only`

- Test locator: `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py:89-100`. Checks: L99 assert `exposed_fields.isdisjoint(PROHIBITED_AUTHORITY_FIELDS)`; L100 assert `DownstreamLiveInventorySnapshot().policy_freeze_state == "architecture_only_no_policy"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Import, field and signature name checks underprove row 5.13; arbitrary source_payload carries foreign authority, duplicate fallback IDs inflate state, and reconciliation transaction defects remain untested.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_live_inventory_snapshot_builder_accepts_inventory_readback_inputs_only`

- Test locator: `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py:103-110`. Checks: L107 assert `parameter_names.isdisjoint(PROHIBITED_BUILD_PARAMETERS)`; L108 assert `{"self", "live_ids", "inventory_id", "capital_snapshot_id", "receipt_id"}.issubset( parameter_names )`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Import, field and signature name checks underprove row 5.13; arbitrary source_payload carries foreign authority, duplicate fallback IDs inflate state, and reconciliation transaction defects remain untested.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G4 — `test_live_inventory_reconciliation_accepts_fill_evidence_inputs_only`

- Test locator: `tests/tier_a/downstream_runtime/test_live_inventory_authority_boundary_surface.py:112-124`. Checks: L116 assert `parameter_names.isdisjoint(PROHIBITED_BUILD_PARAMETERS)`; L117 assert `{ "self", "fill_evidence", "reconciliation_id", "inventory_id", "capital_snapshot_id", "receipt_id", }.issubset(parameter_names)`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Import, field and signature name checks underprove row 5.13; arbitrary source_payload carries foreign authority, duplicate fallback IDs inflate state, and reconciliation transaction defects remain untested.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `4/4`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
