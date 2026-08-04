# Gate 121 — Final Risk Gateway Join

Status: complete on `main`; historical-evaluation readiness pack closed through Gate 121

## Purpose

Make one final risk join authoritative after execution synthesis so posture, modifiers, execution, and final risk stop behaving like split permission worlds.

## What changed

- `ExecutionExpressionOutput` now carries `pre_final_risk_*` snapshots and a structured `final_risk_join` surface.
- `RiskGatewayService` now evaluates one runtime-facing final-risk disposition after execution synthesis and can allow, derisk, or block while preserving review-visible lineage.
- `DeskCognitionRuntime` now applies the final-risk join directly before review generation.
- `ReviewExplanationService` now exposes the final-risk join as its own review-visible packet surface and stage-reason packet.
- Regression coverage now freezes allow, derisk, block, and raw-versus-prepared parity behaviour for the joined runtime path.

## Proof slice

- `PYTHONPATH=src pytest -q tests/test_gate121_final_risk_gateway_join.py tests/test_gate121_historical_evaluation_readiness_closeout.py tests/test_gate103_raw_prepared_parity.py tests/test_execution_review_runtime.py tests/test_gate120_execution_geometry.py tests/test_gate119_candidate_adjudication.py tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_document_hygiene.py`

## Outcome

- final risk is now part of the runtime authority chain instead of a detached downstream service
- review packets now show whether final risk allowed, derisked, or veto-blocked the computed execution shape
- the historical-evaluation readiness pack is closed honestly through Gate 121 on `main`

## Packaged artefact

- `nvda_repo_historical_evaluation_readiness_pack_closed_gate121_main_2026-03-31.zip`
