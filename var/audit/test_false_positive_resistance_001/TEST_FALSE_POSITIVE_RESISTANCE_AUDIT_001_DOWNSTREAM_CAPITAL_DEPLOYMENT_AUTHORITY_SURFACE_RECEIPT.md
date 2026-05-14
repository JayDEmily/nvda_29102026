# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 — Downstream capital deployment authority surface receipt

Date: 2026-05-10

## Scope

Selected family: `downstream_capital_deployment_authority_surface`

Primary architecture row: `5.17 Testing, proof, and checkpoint surfaces`
Supporting architecture row: `5.11 Downstream capital deployment authority`

## Gates executed

| Gate | Status | Evidence |
|---|---:|---|
| Gate 1 authority/oracle extraction | complete for selected family | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`; `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`; `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`; `config/proof_blocks.yaml` proof block `downstream_capital_deployment_authority_surface` |
| Gate 2 baseline execution | status `0` | `logs/capital_selected_after_amendment.status`; command in `logs/capital_selected_command.txt` |
| Gate 3 assertion-strength audit | complete for selected family | Existing tests covered contract presence, bounded capital state, trace preconditions, sizing, block/no-trade/reduce/continue precedence, serial confidence non-sizing, receipt emission, placement boundary, and DMP packet carriage. Gaps found around hidden broker/placement fields, optional trace-token normalisation, default placement closure, and receipt hidden authority fields. |
| Gate 4 known-bad specimens | complete for selected family | capital input with hidden broker/placement fields; whitespace optional parallel-risk packet ID; receipt default placement-open mutant; receipt with hidden broker field. |
| Gate 5 reversible mutation/fault probes | complete for selected family | three targeted mutants killed; statuses recorded in `logs/capital_mutation_*.status` |
| Gate 6 flake/determinism audit | complete for selected family | three repeat selected runs all status `0`; `logs/capital_determinism.statuses` |
| Gate 7 test amendment/creation | complete for selected family | four tests added to `tests/tier_a/capital_deployment/test_capital_contract_models.py` |
| Gate 8 promotion/regression lock | no tier promotion claimed | The selected family is locally hardened; no full Tier A or full-suite reliability claim is made. |

## Tests added

- `tests/tier_a/capital_deployment/test_capital_contract_models.py`
  - `test_capital_authority_input_rejects_hidden_broker_or_placement_fields`
  - `test_capital_optional_parallel_risk_trace_token_is_normalised`
  - `test_capital_deployment_receipt_builder_keeps_placement_authority_closed`
  - `test_capital_deployment_receipt_rejects_hidden_broker_execution_fields`

## Proof summary

| Proof | Status | Log |
|---|---:|---|
| Selected family after amendment | `0` | `logs/capital_selected_after_amendment.log` |
| Determinism repeat 1 | `0` | `logs/capital_determinism_1.log` |
| Determinism repeat 2 | `0` | `logs/capital_determinism_2.log` |
| Determinism repeat 3 | `0` | `logs/capital_determinism_3.log` |
| Mutation 1: capital input allows extra hidden authority fields | `1` killed | `logs/capital_mutation_1_input_extra_authority_fields.log` |
| Mutation 2: optional trace token no longer normalised | `1` killed | `logs/capital_mutation_2_optional_trace_not_normalised.log` |
| Mutation 3: receipt default opens placement authority | `1` killed | `logs/capital_mutation_3_receipt_opens_placement.log` |
| Selected family post-revert | `0` | `logs/capital_selected_post_revert.log` |

Selected-family result after amendment and post-revert: `25 passed`.

## Explicit non-claims

- This receipt does not prove full Tier A reliability.
- This receipt does not prove full-suite reliability.
- This receipt does not prove trading profitability or live order correctness.
- Current code behaviour was not used as the oracle.
- No VENV was created.
- `black` and `ruff` were not run by user instruction.
