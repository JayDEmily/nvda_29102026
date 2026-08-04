# 2026-04-01 Gate 146 Eligibility Admissibility and Execution Candidate Ownership

Status: complete on `main`

## Purpose

Clarify the boundary between Stage 5 admissibility and Stage 6 candidate ownership so later gates stop inferring ownership from overlapping compatibility lists.

## Admitted governed vocabulary

Gate 146 lawfully admits two new governed terms through the canonical vocabulary workflow:
- `eligibility_admissibility`
- `execution_candidate_ownership`

These map to:
- `nvda_desk.schemas.cognition.EligibilityAdmissibilitySurface`
- `nvda_desk.schemas.cognition.ExecutionCandidateOwnershipSurface`

## Runtime contract changes

### Added additive admissibility surface on Stage 5 output
- `EligibilityAdmissibilitySurface`
- `PlaybookEligibilityOutput.admissibility_surface`

### Added additive candidate-ownership surface on Stage 6 output
- `ExecutionCandidateOwnershipSurface`
- `ExecutionExpressionOutput.candidate_ownership`

## Boundary made explicit

`PlaybookEligibilityService.evaluate(...)` now freezes Stage 5 as admissibility-only truth:
- permission state and no-trade reasons;
- admissible and watch family ids;
- admissible and watch setup-variant ids;
- admissible and watch playbook ids.

`ExecutionExpressionService.evaluate(...)` now freezes Stage 6 as candidate-ownership truth:
- which admitted playbook ids execution saw;
- which playbook ids were actually adjudicated;
- the selected lead playbook id;
- contradiction-resolution lineage.

## Review and preserved handoff exposure

No new stage order or packet order lands in Gate 146. The new surfaces are exposed additively through the existing model-dump paths:
- `ReviewExplanationOutput.review_packet["eligibility"]["admissibility_surface"]`
- `ReviewExplanationOutput.review_packet["execution"]["candidate_ownership"]`
- `ReviewExplanationOutput.review_packet["stage_local_handoff"]["cited_eligibility"]["admissibility_surface"]`
- `ReviewExplanationOutput.review_packet["stage_local_handoff"]["execution_pre_modifier"]["candidate_ownership"]`

## Compatibility boundary preserved in Gate 146

Retained unchanged on purpose:
- the existing Stage 5 `add_candidates`, `hold_candidates`, `trim_candidates`, `reduce_candidates`, `hedge_candidates`, and `watch_only_candidates` compatibility lists;
- the existing Stage 6 `candidate_adjudication`, `lead_selection_score`, `lead_selection_reasons`, and final-risk compatibility fields;
- seven-stage runtime order;
- review stage order;
- DMP v2 packet lineage order.

## Behaviour boundary

Gate 146 is additive and classificatory only. It must not change:
- admissible / watch / ineligible outcomes;
- lead-playbook selection or final execution geometry;
- final-risk application semantics;
- review stage order;
- DMP v2 packet lineage order.
