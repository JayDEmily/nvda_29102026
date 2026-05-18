# PRL risk-description vocabulary constraints

Status: planning constraint artefact for `PRL-MRP-023`.

## Purpose

Future plain-language Parallel Risk Lane output must be deterministic, vocabulary-governed, and risk-only. It must describe the environmental state-of-play without selecting an action.

## Governing sources

- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/vocabulary/vocabulary_registry.md`
- `data/vocabulary/canonical_vocabulary.json`

## Constraint set

1. Description output must use deterministic templates.
2. Templates must reference governed vocabulary entries or explicitly scoped local labels.
3. No free-form generative commentary is allowed in runtime PRL description output.
4. Description output must not contain trade advice or action verbs such as buy, sell, fade, chase, hedge, size up, stand down, take the trade, or avoid the trade.
5. Description output must not express capital sizing, order instructions, candidate formation, playbook selection, or review judgement.
6. Risk semantics must remain neutral: constructive, defensive, ambiguous, mixed, uncertainty, consequence, confidence, risk-rich, risk-poor, risk-compensated, risk-fragile, and risk-unclear states can be described without instructing action.
7. Future templates belong in the dedicated template registry planned as `data/parallel_risk/description_templates.v1.json`, not inside canonical vocabulary data.

## Non-goals

- Do not implement a renderer in this leaf.
- Do not create the template registry in this leaf.
- Do not add free-text fields to runtime contracts.
