# Worker Brief PM-004 — Coefficient, Modifier and Evaluation Terms

## Dispatch state

`authorised_after_PM-003_pass`

## Exact outcome

Semantically adjudicate the coefficient, modifier and evaluation family without changing coefficient runtime behaviour, tests or machine projection.

## Prerequisite

PM-003 must record `unit_result: pass` with no forbidden changes.

## Fixed concept set

Human headings:

`State-conditioned Modifier`; `Bounded Dynamic Coefficient`; `Review Horizon`; `Champion/Challenger Evaluation`; `Live-paper / Historical Evaluation Separation`; `Modifier Authority`.

Generated entries:

`Modifier Authority`; `Coefficient Authority`; `Mutable Runtime Surface`; `Baseline-only Surface`; `Effective Coefficient Lineage`; `State-conditioned Modifier`; `Bounded Dynamic Coefficient`; `Review Horizon`; `Champion/Challenger Evaluation`; `Live-paper / Historical Evaluation Separation`.

The matching historical admissions in section 10.7 are part of this unit.

## Authority and tests

Coefficient ownership, hard bounds, promotion authority and live-paper/historical separation in the governing normatives determine meaning. Current modifier code and tests are observations only. A passing modifier or vocabulary test cannot establish that a term is lawfully owned or complete.

## Required full reads

Create the unit manifest first, then read root controls, active programme controls, all prior unit outputs, and:

- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
- `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md`;
- `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md` and `docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md`;
- `docs/03_DOMAIN_MODEL_CORE.md` and relevant modifier/coefficient material in `docs/03.1_DOMAIN_MODEL_WORKING.md`;
- `docs/05_GUARDRAILS_CORE.md` and `docs/05.1_GUARDRAILS_WORKING.md`;
- `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`, `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`, and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md`;
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`, `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`, and all three vocabulary documents;
- `docs/planning/2026-04-02_GATE160_GOVERNED_SIGNAL_COEFFICIENT_REFERENCE_WORKBOOK_LAW.md`;
- `src/nvda_desk/cognition/modifiers/state_conditioned.py` and its package initializer;
- `tests/tier_a/modifiers/test_state_conditioned_modifier_surface.py` and `tests/tier_a/config/test_sequence8_coefficient_modifier_authority_specimen.py` read-only;
- current builder and generated vocabulary entries for this family.

## Required decisions

For every fixed concept record exact label, normalised slug, governing proposition/source locator, bounded definition/scope, semantic owner, relationships/distinctions, canonical label/slug, lawful aliases, disallowed phrases, lifecycle/status, semantic disposition (`retain`, `enrich`, `admit_new`, `alias`, `quarantine`, `retire`, or `reject`), the four-value candidate action when applicable (`enrich_existing`, `add_new`, `alias_only`, or `quarantine`), PM-010 projection action, rationale and evidence. Additionally state:

- whether it owns a value, changes a value, constrains a value, evaluates a candidate, records lineage, or classifies a surface;
- whether the concept may affect live authority;
- the exact promotion boundary;
- the distinction between mutable runtime authority and baseline-only evidence.

Do not collapse `Modifier Authority` and `Coefficient Authority` without proposition-level evidence. Do not turn champion/challenger evaluation into self-tuning authority.

## Allowed changes and outputs

Allowed changes are limited to `units/PM-004/**`, the assigned registry entries, and the matching bounded section-10.7 vocabulary admissions. Required outputs are:

1. `PM-004_FULL_READ_MANIFEST.tsv`
2. `COEFFICIENT_MODIFIER_EVALUATION_ADJUDICATION_REGISTER.tsv`
3. `PM-004_RECEIPT.md`
4. `VALIDATION_OUTPUT.txt`

Tests, config, coefficient/runtime code, builder, generated JSON, Atlas, other semantic families, root controls, roadmaps and ExecPlans are forbidden.

## Novel findings, validation and pass

Resolve and log novel concepts only when they belong to this family and higher authority supplies their meaning. Route all others forward. Prove exact once-only coverage of the fixed concept set, unchanged unassigned registry content, unchanged tests/source/generated artefacts, allowed-path compliance and `git diff --check`.

PM-004 passes only when every assigned concept has a complete decision and the authority boundaries remain explicit. On pass, continue to PM-005.
