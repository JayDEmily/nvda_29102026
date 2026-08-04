Status: complete on `main`; Gate 127 is now the active gate
# Gate 126 — Bounded Temporal Threshold Authority

## What closed

Gate 126 is complete on `main`. The admitted temporal threshold and timing subset now reads from `config/coefficient_authority.v1.yaml` through `TemporalStateClassifier` rather than private classifier literals. The runtime still treats the workbook as research provenance only, not direct runtime truth.

## What changed

- added governed temporal-threshold and timing-parameter loading to `TemporalStateClassifier` using `TemporalThresholdId` and `TimingParameterId`;
- added deterministic conversion from percent primitives to basis-point threshold comparison where the governed authority is expressed in basis points;
- kept non-admitted classifier hits such as break-count floors and certain open-window guards explicit, rather than silently inflating the governed surface;
- updated the canonical threshold-edge and prepared/raw harness expectations to match current runtime truth after final-risk and event-window evolution.

## Receipt

- branch: `work/gate-126-temporal-threshold-authority-20260331`
- start commit: `569aa64`
- closing proof command: `PYTHONPATH=src pytest -q tests/test_gate126_temporal_threshold_authority.py tests/test_gate98_threshold_edges.py tests/test_gate96_canonical_runtime_harness.py tests/test_gate102_raw_runtime_harness.py`
- observed result: `17 passed`

## Truth clarified during closeout

The old declared slice still carried stale expectations. The current lawful runtime truth is now frozen explicitly:

- `gamma_pressure_score=0.95` remains `destabilising`, but final risk derisks `target_fresh_deployable_pct` from the pre-final-risk expectation to `19.6625`;
- the canonical prepared and raw harnesses both now prove `event_imminent_window`, no active playbooks, and `final_risk=derisk` with `target_fresh_deployable_pct=0.0`;
- no Asia/Japan raw coefficient was admitted by stealth.

## Why this is honest

This gate did not reopen the coefficient universe. It admitted only the bounded temporal subset already frozen by Gate 122 and used the existing governed authority file rather than promoting workbook sheets or salvage registry entries into live runtime law.
