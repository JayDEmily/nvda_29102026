# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 — Opening placement readiness surface receipt

## Scope

Selected proof-block family: `opening_placement_readiness_surface`.

Primary proof-block command:

```bash
PYTHONPATH=src:. python -m pytest tests/tier_a/downstream_runtime/test_downstream_opening_service_surface.py tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py tests/tier_a/adapters_egress/test_broker_boundary_surface.py -q
```

## Authority / oracle basis

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` row `5.12` defines opening architecture and placement readiness as downstream opening authorisation, placement readiness, and handoff structure after deployment authority. It prohibits capital sizing, serial candidate formation, parallel risk evaluation, and broker adapter implementation detail beyond the handoff contract.
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` local branch `ROADMAP_NEXT_THREE_HELD_GATES_5_4_5_9_5_12_BRANCH_001` permits downstream opening placement-readiness contracts, non-executing placement handoff material, service/domain wrappers, downstream opening and broker-boundary Tier A tests, proof-block manifest, retained-test registry, Makefile proof gates, receipts, and roadmap ledger entries. It closes concrete broker adapters, broker order submission, live order placement, capital sizing recomputation, serial candidate formation, and risk generation.
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` bounded 5.12 supplement assigns `src/nvda_desk/downstream/opening.py` as authoritative writer for placement readiness evaluation and non-executing placement handoff material. It requires every placement readiness result to identify consumed capital-deployment receipt id, serial candidate id, placement constraints, and broker boundary mode.

## Files read in this pass

- `tests/tier_a/downstream_runtime/test_downstream_opening_service_surface.py`
- `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py`
- `tests/tier_a/adapters_egress/test_broker_boundary_surface.py`
- `src/nvda_desk/contracts/downstream.py`
- `src/nvda_desk/contracts/capital.py` relevant `CapitalDeploymentDecision` contract region
- `src/nvda_desk/downstream/opening.py`
- `src/nvda_desk/domain/downstream/opening.py`
- `src/nvda_desk/services/downstream_opening_service.py`
- `src/nvda_desk/adapters/egress/broker_protocol.py`
- `config/proof_blocks.yaml` opening/playbook/exit proof-block region

## Added false-positive resistance cases

Added to `tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py`:

1. `test_opening_readiness_requires_capital_deployment_receipt_id`
   - Known-bad specimen: capital deployment decision has no `capital_deployment_receipt_id`.
   - Expected result: explicit service-level `ValueError` before incidental trace-model validation.
2. `test_opening_readiness_rejects_blank_serial_candidate_id`
   - Known-bad specimen: whitespace-only serial candidate id.
   - Expected result: explicit service-level `ValueError`.
3. `test_opening_readiness_blocks_continue_decision_with_zero_notional`
   - Known-bad specimen: `CONTINUE` action with positive deployable percentage but zero authorised notional.
   - Expected result: blocked readiness with no placement handoff and no broker/capital recomputation authority.
4. `test_opening_readiness_detaches_placement_constraints_from_caller_list`
   - Known-bad specimen: caller mutates placement constraints list after readiness evaluation.
   - Expected result: result trace and handoff preview remain copy-safe.
5. `test_opening_readiness_protocol_handoff_rejects_broker_execution_fields`
   - Known-bad specimen: hidden concrete broker execution field inside placement handoff material.
   - Expected result: Pydantic validation rejects hidden broker field.

## Baseline and determinism evidence

Initial selected proof-block run after amendment:

```text
11 passed in 0.23s
```

Determinism probe:

```text
RUN_1: 11 passed in 0.21s
RUN_2: 11 passed in 0.23s
RUN_3: 11 passed in 0.22s
```

Restored baseline after reversible mutation probes:

```text
11 passed in 0.23s
```

## Reversible mutation / fault-injection evidence

The following targeted mutants were introduced one at a time, run against the selected proof block, and restored after each run:

| Mutant | Result | Observed failure |
|---|---|---|
| capital receipt requirement disabled | KILLED | explicit service-level error assertion failed because downstream trace validation became incidental failure |
| blank serial candidate accepted | KILLED | `test_opening_readiness_rejects_blank_serial_candidate_id` did not raise |
| zero notional no longer blocks | KILLED | readiness state became `ready_for_protocol_handoff` instead of `blocked` |
| broker boundary accepts concrete adapter | KILLED | concrete broker boundary no longer raised |
| handoff accepts hidden broker fields | KILLED | hidden broker field no longer raised validation error |

## Claim boundary

This receipt proves local false-positive resistance hardening for the selected `opening_placement_readiness_surface` proof-block family only. It does not prove full Tier A reliability, full suite reliability, runtime correctness, broker execution correctness, live trading correctness, or that future untested invariants cannot false-positive.

## Next selected family

`playbook_library_architecture_surface`.
