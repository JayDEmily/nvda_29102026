# 2026-04-01 Gate 143 Additive Stage-Local Handoff

Status: complete on `main`

## Purpose

Admit only the additive preserved handoff surface Gate 142 proved necessary, carry it through runtime and review entry surfaces, and keep terminal behaviour unchanged.

## Admitted governed vocabulary

Gate 143 lawfully admits two new governed terms through the canonical vocabulary workflow:
- `stage_local_handoff`
- `terminal_risk_decision`

These map to:
- `nvda_desk.schemas.cognition.StageLocalHandoffSurface`
- `nvda_desk.schemas.risk.RiskDecision`

## Runtime contract changes

### Added additive contract
- `StageLocalHandoffSurface` in `src/nvda_desk/schemas/cognition.py`

### Added additive carriage only
- `ReviewExplanationInput.stage_local_handoff`
- `ReviewExplanationOutput.stage_local_handoff`
- `DeskCognitionRuntimeResult.stage_local_handoff`

### Runtime assembly path

Observed now in `src/nvda_desk/services/cognition_runtime.py`:
- preserve `cited_posture_pre_modifier` after selector-contract citations;
- preserve `cited_eligibility` after selector-contract citations;
- preserve `execution_pre_modifier` before `apply_to_execution(...)` mutates execution;
- preserve `execution_post_modifier_pre_final_risk` after modifier mutation but before terminal application;
- preserve `final_risk_decision` before `apply_final_join(...)` mutates execution;
- package those into `StageLocalHandoffSurface` and pass it additively into review and the runtime result.

## Review exposure

`src/nvda_desk/services/review_explanation.py` now exposes the additive handoff surface in:
- `ReviewExplanationOutput.stage_local_handoff`
- `review_packet["stage_local_handoff"]`

The existing final review surfaces remain intact.

## Compatibility boundary preserved in Gate 143

Retained unchanged on purpose:
- seven-stage runtime order;
- existing `modifier_runtime_packet` carriage;
- existing `pre_final_risk_*` compatibility fields;
- existing `final_risk_join` compatibility field and review packet exposure;
- existing final-risk application semantics.

## Behaviour boundary

Gate 143 is additive only. It must not change:
- final allowed / derisked / blocked outcomes;
- stage order;
- review stage order;
- DMP v2 packet lineage order.
