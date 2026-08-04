# 2026-04-01 Gate 148 Review, Trace, Replay, and Legacy Expectation Reconciliation

Status: complete on `main`

## Purpose

Migrate downstream review, bounded-trace, and legacy expectation consumers to the preserved-seam model now that the additive seam contracts exist.

## Admitted governed vocabulary

No new governed vocabulary is admitted in Gate 148.

Gate 148 only reuses already admitted terms and contracts:
- `admissibility_surface`
- `candidate_ownership`
- `overlay_risk_decision`
- `terminal_risk_application`
- `final_risk_join`
- `stage_local_handoff`

## Review consumer changes

`ReviewExplanationOutput.review_packet` now exposes additive top-level preserved-seam entries so downstream review consumers do not need to mine only the older nested stage packets:
- `ReviewExplanationOutput.review_packet["admissibility_surface"]`
- `ReviewExplanationOutput.review_packet["candidate_ownership"]`
- `ReviewExplanationOutput.review_packet["overlay_risk_decision"]`
- `ReviewExplanationOutput.review_packet["terminal_risk_application"]`

The nested compatibility and lineage surfaces remain intact on purpose:
- `ReviewExplanationOutput.review_packet["stage_local_handoff"]`
- `ReviewExplanationOutput.review_packet["final_risk_join"]`
- seven-stage runtime order
- review stage order
- DMP v2 packet lineage order

## Trace and replay consumer changes

`BoundedTraceRunResult` now carries the already admitted preserved-seam models directly:
- `BoundedTraceRunResult.admissibility_surface`
- `BoundedTraceRunResult.candidate_ownership`
- `BoundedTraceRunResult.overlay_risk_decision`
- `BoundedTraceRunResult.terminal_risk_application`

`BoundedTraceReviewService.render_markdown_report(...)` now includes a preserved seam snapshot section so human review can compare:
- Stage 5 admitted playbooks
- Stage 6 lead-owner selection
- overlay decision
- terminal decision

without abandoning the existing final-risk compatibility readout.

## Legacy expectation boundary

Gate 148 keeps `final_risk_join` as the bounded compatibility reference while legacy expectations are refreshed.

The preserved seam must agree with the final-risk compatibility surface on final allow / derisk / block outcomes, but Gate 148 does not remove or rename `final_risk_join`.

## Behaviour boundary

Gate 148 is a downstream-consumer reconciliation gate only. It must not change:
- runtime posture outcomes;
- admissibility outcomes;
- execution lead-selection outcomes;
- terminal allow / derisk / block outcomes;
- DMP v2 packet lineage order.
