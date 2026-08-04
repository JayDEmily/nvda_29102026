# Gate 120 — Execution Geometry Enrichment

Status: complete on `main`

## Purpose

Make execution output rich enough to simulate actual order behaviour by carrying governed execution geometry rather than stopping at entry style and scaling fractions.

## What changed

- `ExecutionTemplateSpec` now owns bounded geometry defaults for bias, ladder spacing, chase distance, stop distance, take-profit distance, hedge ratio, and base per-slice risk.
- `ExecutionExpressionOutput` now carries explicit execution-geometry fields and geometry notes.
- `ExecutionExpressionService` now derives context-aware geometry from the chosen execution template and the current runtime state.

## Proof slice

- `PYTHONPATH=src pytest -q tests/test_gate120_execution_geometry.py tests/test_playbook_registry.py tests/test_gate52_native_playbook_hierarchy.py tests/test_execution_review_runtime.py tests/test_gate118_mutable_surface_operability.py tests/test_gate100_bounded_scenario_matrix.py tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_document_hygiene.py`

## Outcome

- execution output now carries deployment geometry that changes with event and gamma stress
- geometry remains template-backed rather than inventing a second execution doctrine
- review-visible execution packets now expose how the selected lead would actually be deployed
