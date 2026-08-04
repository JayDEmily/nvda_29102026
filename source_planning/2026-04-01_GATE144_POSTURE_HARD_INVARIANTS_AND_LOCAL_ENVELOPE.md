# 2026-04-01 Gate 144 Posture Hard Invariants and Local Envelope

Status: complete on `main`

## Purpose

Separate posture-owned hard-stop truth from posture-local envelope truth while keeping later selector citations and modifier notes explicit as downstream annotations rather than hiding them only in the flat `reasons` list.

## Admitted governed vocabulary

Gate 144 lawfully admits three new governed terms through the canonical vocabulary workflow:
- `posture_hard_invariants`
- `posture_local_envelope`
- `posture_downstream_annotations`

These map to:
- `nvda_desk.schemas.cognition.PostureHardInvariantsSurface`
- `nvda_desk.schemas.cognition.PostureLocalEnvelopeSurface`
- `nvda_desk.schemas.cognition.PostureRiskOutput.downstream_annotations`

## Runtime contract changes

### Added additive posture-owned surfaces
- `PostureHardInvariantsSurface`
- `PostureLocalEnvelopeSurface`
- `PostureRiskOutput.downstream_annotations`

### Ownership boundary now explicit

`PostureRiskService.evaluate(...)` now materialises:
- hard-block truth in `hard_invariants`;
- posture-owned base permission, base posture label, deployable-capital envelope, and derisk reasons in `local_envelope`;
- no selector or modifier notes in those posture-owned surfaces.

`_posture_with_contract_citations(...)` and `StateConditionedModifierService.apply_to_posture(...)` now append non-posture-owned notes to `downstream_annotations` while retaining the flat `reasons` list for compatibility.

## Review and preserved handoff exposure

No new stage order or review packet order was introduced in Gate 144. The new posture-owned surfaces and downstream annotations are visible through the existing model-dump paths:
- `ReviewExplanationOutput.review_packet["posture"]`
- `ReviewExplanationOutput.review_packet["stage_local_handoff"]["cited_posture_pre_modifier"]`

## Compatibility boundary preserved in Gate 144

Retained unchanged on purpose:
- seven-stage runtime order;
- `modifier_runtime_packet` carriage;
- existing flat posture fields and `reasons` list;
- existing `stage_local_handoff` contract and `final_risk_join` compatibility fields.

## Behaviour boundary

Gate 144 is additive and classificatory only. It must not change:
- allowed / derisked / blocked outcomes;
- final-risk application semantics;
- review stage order;
- DMP v2 packet lineage order.
