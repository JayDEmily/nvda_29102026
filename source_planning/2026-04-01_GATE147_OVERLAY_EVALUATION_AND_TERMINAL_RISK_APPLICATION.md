# 2026-04-01 Gate 147 Overlay Evaluation and Terminal-Risk Application

Status: complete on `main`

## Purpose

Split the preserved overlay-evaluation decision from the posture-aware terminal-risk application step while keeping the final-risk compatibility surfaces and stage order unchanged.

## Admitted governed vocabulary

Gate 147 lawfully admits two new governed terms through the canonical vocabulary workflow:
- `overlay_risk_decision`
- `terminal_risk_application`

These map to:
- `nvda_desk.schemas.risk.RiskDecision`
- `nvda_desk.schemas.cognition.TerminalRiskApplicationSurface`

## Runtime contract changes

### Added additive terminal-risk seam inside the preserved handoff surface
- `StageLocalHandoffSurface.overlay_risk_decision`
- `StageLocalHandoffSurface.terminal_risk_application`
- `TerminalRiskApplicationSurface`
- `TerminalRiskOverlapClass`

### Risk-gateway split made explicit

`RiskGatewayService.evaluate_overlay(...)` now preserves the overlay-evaluation decision as the raw output of the current market/portfolio overlay rules.

`RiskGatewayService.build_terminal_risk_application(...)` now applies posture-aware terminal authority to that preserved overlay decision and records the overlap class that explains why the final decision stayed aligned, derisked further, or escalated to a block.

`RiskGatewayService.evaluate_runtime_join(...)` remains as the bounded compatibility wrapper returning only the final decision so downstream consumers remain stable until Gate 148.

## Frozen overlap classes in Gate 147

The additive `TerminalRiskOverlapClass` ledger freezes the observed overlap classes now admitted by the repo:
- `overlay_allow_no_terminal_override`
- `overlay_derisk_no_terminal_override`
- `overlay_block_no_terminal_override`
- `posture_derisk_supersedes_overlay_allow`
- `posture_block_supersedes_overlay_allow`
- `posture_block_supersedes_overlay_derisk`
- `posture_block_aligns_with_overlay_block`

## Review and preserved handoff exposure

No new stage order or packet order lands in Gate 147. The new seam is visible additively through the existing preserved handoff surface:
- `ReviewExplanationOutput.review_packet["stage_local_handoff"]["overlay_risk_decision"]`
- `ReviewExplanationOutput.review_packet["stage_local_handoff"]["terminal_risk_application"]`

## Compatibility boundary preserved in Gate 147

Retained unchanged on purpose:
- `ExecutionExpressionOutput.final_risk_join`
- `pre_final_risk_*` compatibility fields
- seven-stage runtime order
- review stage order
- DMP v2 packet lineage order
- final-risk execution reshaping in `apply_final_join(...)`

## Behaviour boundary

Gate 147 is additive plus seam-classificatory only. It must not change:
- final allow / derisk / block outcomes;
- final-risk execution effects;
- review stage order;
- DMP v2 packet lineage order.
