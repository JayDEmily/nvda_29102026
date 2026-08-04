# 2026-04-01 Gate 145 Modifier Emitted-Policy Compatibility Bridge

Status: complete on `main`

## Purpose

Make packet-authoritative modifier consequences explicit on posture and execution outputs so later consumers stop inferring modifier effects only from flat compatibility fields and free-text reasons.

## Admitted governed vocabulary

Gate 145 lawfully admits one new governed term through the canonical vocabulary workflow:
- `modifier_compatibility_bridge`

This maps to:
- `nvda_desk.schemas.cognition.ModifierCompatibilityBridgeSurface`

## Runtime contract changes

### Added additive compatibility bridge
- `ModifierCompatibilityBridgeSurface`
- `PostureRiskOutput.modifier_compatibility_bridge`
- `ExecutionExpressionOutput.modifier_compatibility_bridge`

### Modifier authority boundary now explicit

`ModifierRuntimePacket` remains the authority.

`StateConditionedModifierService.apply_to_posture(...)` now:
- preserves the Gate 144 posture-owned surfaces untouched;
- records which flat posture fields were changed as a bounded compatibility bridge;
- carries packet authority, applied policy ids, and target-fresh consequences explicitly on `modifier_compatibility_bridge`.

`StateConditionedModifierService.apply_to_execution(...)` now:
- treats execution mutation as a bounded correction bridge only;
- records when execute-time operative surfaces already match packet authority and therefore need no extra override;
- still carries the packet and bounded compatibility reasons without inventing a second private modifier interpretation.

## Review and preserved handoff exposure

No new review-stage order or packet-order change lands in Gate 145. The new bridge surfaces are exposed additively through existing model-dump paths:
- `ReviewExplanationOutput.review_packet["posture"]["modifier_compatibility_bridge"]`
- `ReviewExplanationOutput.review_packet["execution"]["modifier_compatibility_bridge"]`
- `ReviewExplanationOutput.review_packet["stage_local_handoff"]["execution_post_modifier_pre_final_risk"]["modifier_compatibility_bridge"]`

## Compatibility boundary preserved in Gate 145

Retained unchanged on purpose:
- `ModifierRuntimePacket` as the authority;
- existing `effective_policy`, `modifier_control_law`, and review-lineage packet surfaces;
- existing flat posture/execution compatibility fields;
- existing stage order and final-risk behaviour.

## Behaviour boundary

Gate 145 remains bounded. It must not change:
- stage order;
- final-risk application semantics;
- review stage order;
- DMP v2 packet lineage order.
