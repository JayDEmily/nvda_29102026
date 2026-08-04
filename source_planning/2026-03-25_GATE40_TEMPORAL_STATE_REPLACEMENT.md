# Gate 40 — Temporal State Replacement

Status: complete on `main`

## Purpose

Replace the hard clock-bucket Step-1 classifier with a signal-aware temporal-state engine while keeping the binding `TemporalContextOutput` and DMP packet surfaces stable.

## Scope closed in Gate 40

- Replaced `SessionClockClassifier` as Step-1 truth with `TemporalStateClassifier`.
- Preserved `TemporalContextService` as the Step-1 orchestration boundary.
- Preserved `TemporalContextOutput` as the outward stage payload so DMP wrappers and downstream consumers did not drift.
- Added signal-derived temporal primitives to the runtime snapshot path.
- Fixed the event-window label inconsistency that was already present downstream.

## Closed files

- `src/nvda_desk/domain/temporal_state.py`
- `src/nvda_desk/domain/session_clock.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/dataset.py`
- `src/nvda_desk/services/real_data_loader.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `src/nvda_desk/services/temporal_context.py`
- `tests/test_temporal_context_signal_state.py`

## Validation

- `PYTHONPATH=src python3 -m pytest -q tests/test_temporal_context_signal_state.py tests/test_real_data_loader.py tests/test_posture_risk_and_playbook.py tests/test_dmp_protocol.py tests/test_dmp_v2_protocol.py tests/test_gate29_market_context_synthesis_contracts.py tests/test_gate30_options_ingress_primary_flow_contracts.py`

## Result

Gate 40 is closed. Step 1 now uses primitive temporal observables rather than elapsed-minute buckets while the DMP stage packet surface remains stable.
