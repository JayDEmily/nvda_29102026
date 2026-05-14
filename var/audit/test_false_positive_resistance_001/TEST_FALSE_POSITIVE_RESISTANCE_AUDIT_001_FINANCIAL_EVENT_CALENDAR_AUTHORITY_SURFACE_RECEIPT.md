# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 — Financial/event calendar authority surface receipt

Date: 2026-05-10

## Scope

Selected family: `financial_event_calendar_authority_surface`

Primary architecture row: `5.17 Testing, proof, and checkpoint surfaces`
Supporting architecture row: `5.4 Financial and event calendar architecture`

## Gates executed

| Gate | Status | Evidence |
|---|---:|---|
| Gate 1 authority/oracle extraction | complete for selected family | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`; `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`; `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`; `config/proof_blocks.yaml` proof block `financial_event_calendar_authority_surface` |
| Gate 2 baseline execution | status `0` | `logs/calendar_selected_after_amendment.status`; command in `logs/calendar_selected_command.txt` |
| Gate 3 assertion-strength audit | complete for selected family | Existing tests covered duplicate artifact IDs, unknown layer refs, forbidden runtime keys, checked reference trace, operational surfaces, and projection/crosswalk presence. Gaps found around duplicate layer IDs, duplicate event IDs, and detached crosswalk records. |
| Gate 4 known-bad specimens | complete for selected family | duplicate layer ID manifest; duplicate event IDs in projection rows; caller-mutated crosswalk record lists. |
| Gate 5 reversible mutation/fault probes | complete for selected family | three targeted mutants killed; statuses recorded in `logs/calendar_mutation_*.status` |
| Gate 6 flake/determinism audit | complete for selected family | three repeat selected runs all status `0`; `logs/calendar_determinism.statuses` |
| Gate 7 test amendment/creation | complete for selected family | three tests added across financial calendar and reference crosswalk files |
| Gate 8 promotion/regression lock | no tier promotion claimed | The selected family is locally hardened; no full Tier A or full-suite reliability claim is made. |

## Tests added

- `tests/tier_a/financial_calendar/test_financial_calendar_authority_surface.py`
  - `test_calendar_manifest_rejects_duplicate_layer_ids`
  - `test_calendar_projection_rejects_duplicate_event_ids`
- `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py`
  - `test_calendar_reference_crosswalk_returns_detached_records`

## Proof summary

| Proof | Status | Log |
|---|---:|---|
| Selected family after amendment | `0` | `logs/calendar_selected_after_amendment.log` |
| Determinism repeat 1 | `0` | `logs/calendar_determinism_1.log` |
| Determinism repeat 2 | `0` | `logs/calendar_determinism_2.log` |
| Determinism repeat 3 | `0` | `logs/calendar_determinism_3.log` |
| Mutation 1: duplicate layer IDs not checked | `1` killed | `logs/calendar_mutation_1_duplicate_layer_ids.log` |
| Mutation 2: duplicate event IDs not rejected | `1` killed | `logs/calendar_mutation_2_duplicate_event_ids.log` |
| Mutation 3: crosswalk returns shared mutable records | `1` killed | `logs/calendar_mutation_3_crosswalk_shared_records.log` |
| Selected family post-revert | `0` | `logs/calendar_selected_post_revert.log` |

Selected-family result after amendment and post-revert: `12 passed`.

## Explicit non-claims

- This receipt does not prove full Tier A reliability.
- This receipt does not prove full-suite reliability.
- This receipt does not prove correctness of future live calendar ingestion.
- Current code behaviour was not used as the oracle.
- No VENV was created.
- `black` and `ruff` were not run by user instruction.
