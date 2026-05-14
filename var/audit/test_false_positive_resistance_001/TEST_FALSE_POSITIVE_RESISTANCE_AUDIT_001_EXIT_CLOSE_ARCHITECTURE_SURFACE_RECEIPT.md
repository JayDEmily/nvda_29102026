# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 — Exit/close architecture surface receipt

## Scope

Selected proof-block family: `exit_close_architecture_surface`.

Primary proof-block command:

```bash
PYTHONPATH=src:. python -m pytest tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py tests/tier_a/playbook tests/tier_a/capital_deployment -q
```

## Authority / oracle basis

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` row `5.14` defines exit and close architecture as bounded exit-policy decisions, close-readiness, close/trim handoff material, and reviewable closure receipts.
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` active bounded exception `ROADMAP_EXIT_CLOSE_5_14_BRANCH_001` opens row `5.14` for bounded exit-policy contracts, protocol-only close handoff material, exit/close receipts, and position-closure replay proof.
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` row `5.14` supplement assigns `src/nvda_desk/downstream/exit_close.py` as authoritative writer and forbids order placement, live inventory mutation, capital sizing recomputation, candidate formation, external source ingestion, and concrete broker execution.

## Files read in this pass

- `src/nvda_desk/contracts/exit_close.py`
- `src/nvda_desk/downstream/exit_close.py`
- `src/nvda_desk/services/exit_close_service.py`
- `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py`
- `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py`
- `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py`
- `tests/tier_a/playbook/test_playbook_library_architecture_surface.py`
- `tests/tier_a/capital_deployment/test_capital_contract_models.py`
- `config/proof_blocks.yaml` exit/close proof-block region

## Added false-positive resistance cases

Added to `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py`:

1. `test_exit_close_policy_rejects_inconsistent_unblocked_state`
2. `test_close_handoff_requires_trim_or_close_ready_decision`
3. `test_close_handoff_rejects_live_order_placement_flag`
4. `test_exit_close_receipt_rejects_input_trace_mismatch`
5. `test_exit_close_receipt_rejects_live_inventory_mutation_flag`
6. `test_exit_close_replay_fingerprint_changes_when_handoff_material_changes`

## Baseline and determinism evidence

Initial selected proof-block run after amendment:

```text
73 passed in 0.35s
```

Determinism probe:

```text
RUN_1: 73 passed in 0.36s
RUN_2: 73 passed in 0.36s
RUN_3: 73 passed in 0.34s
```

Restored baseline after reversible mutation probes:

```text
73 passed in 0.35s
```

## Reversible mutation / fault-injection evidence

The following targeted mutants were introduced one at a time, run against the selected proof block, and restored after each run:

| Mutant | Result | Observed failure |
|---|---|---|
| exit state consistency disabled | KILLED | inconsistent `requested_action` / `exit_state` accepted |
| handoff permits hold decisions | KILLED | hold decision produced close handoff |
| handoff protocol flags accepted | KILLED | live-order placement flag accepted |
| receipt input trace mismatch accepted | KILLED | mismatched receipt input trace accepted |
| receipt live inventory mutation accepted | KILLED | receipt live-inventory mutation flag accepted |
| replay fingerprint ignores handoff material | KILLED | changed handoff material produced identical replay fingerprint |

## Claim boundary

This receipt proves local false-positive resistance hardening for the selected `exit_close_architecture_surface` proof-block family only. It does not prove full Tier A reliability, full suite reliability, runtime correctness, broker execution correctness, live trading correctness, or that future untested invariants cannot false-positive.

## Next selected family

No further selected family is opened by this receipt. Next gate is final selected-proof-block rollup and packaging.
