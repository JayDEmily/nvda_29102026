# Worker Brief PM-009 — Parallel Risk, Persistence, Review, Explanation and Playbook Terms

## Dispatch state

`authorised_after_PM-008_pass`

## Exact outcome

Semantically adjudicate the parallel-risk, observation-persistence, review, explanation and playbook family. Preserve the boundary between advisory risk observation and serial/capital authority, and between evidence/review/explanation and runtime decision authority.

## Prerequisite

PM-008 must record `unit_result: pass` with no forbidden changes.

## Fixed concept set

Human headings:

`Parallel Risk Lane`; `Review Layer`; `Explanation Layer`; `Playbook Library`.

Generated entries:

`Parallel Risk Lane`; `Environment Assessment`; `Candidate Audit`; `Stage-read State`; `Parallel-risk Observation Store`; `Write-only Persistence`; `Append-only Observation Record`; `Review Layer`; `Explanation Layer`; `Playbook Library`.

`Candidate Audit` here means the parallel-risk observation concept. Vocabulary synonym/candidate audit machinery is not redefined by this unit.

## Authority and tests

The operating model, risk/replay, persistence, ownership, playbook and guardrail normatives establish meaning. Current risk code, stores, templates and tests are observations only. Green tests cannot promote an advisory lane into serial or capital authority and cannot prove persistence or review completeness.

## Required full reads

Create the unit manifest first, then read root controls, programme controls, all prior outputs, and:

- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
- `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md`;
- all three briefing/execution operating-model documents under `docs/02*`;
- `docs/03_DOMAIN_MODEL_CORE.md` and `docs/03.1_DOMAIN_MODEL_WORKING.md`;
- `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` and `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`;
- both guardrail documents;
- all three runtime ownership/state/replay documents under `docs/07*`;
- both vocabulary normatives and all three vocabulary documents;
- `docs/planning/PRL_MINUTE_RISK_PROFILE_ARCHITECTURE_DECISIONS.md`;
- `docs/planning/PRL_RISK_DESCRIPTION_VOCABULARY_CONSTRAINTS.md`;
- `docs/planning/PRL_MINUTE_RISK_PROFILE_MASTER_ROADMAP.md` only for current authority/status distinctions;
- every directly governing `src/nvda_desk/domain/parallel_risk/**` file, relevant persistence interface, and public review/explanation/playbook contract needed to understand a fixed concept;
- Tier A parallel-risk and vocabulary tests mentioning fixed concepts, read-only;
- current builder and generated entries for this family.

## Required decisions

For every fixed concept record exact label, normalised slug, governing proposition/source locator, bounded definition/scope, semantic owner, relationships/distinctions, canonical label/slug, lawful aliases, disallowed phrases, lifecycle/status, semantic disposition (`retain`, `enrich`, `admit_new`, `alias`, `quarantine`, `retire`, or `reject`), the four-value candidate action when applicable (`enrich_existing`, `add_new`, `alias_only`, or `quarantine`), PM-010 projection action, rationale and evidence. Additionally record:

- advisory, observation, persistence, review, explanation or playbook authority class;
- owner, lawful writer and consumer;
- allowed influence on the serial spine and capital decision;
- append/write-only semantics and replay implications;
- distinction between assessment, candidate audit and stage-read state;
- distinction between review evidence, explanation output and playbook authority.

Do not grant parallel risk independent deployment authority. Do not allow an observation store to become a decision owner. Do not treat explanations or reviews as retroactive runtime authority. Do not conflate the playbook library with playbook eligibility.

## Allowed changes and outputs

Allowed changes are limited to `units/PM-009/**`, assigned registry entries, and matching bounded vocabulary admissions when required. Required outputs are:

1. `PM-009_FULL_READ_MANIFEST.tsv`
2. `PARALLEL_RISK_REVIEW_PLAYBOOK_ADJUDICATION_REGISTER.tsv`
3. `PM-009_RECEIPT.md`
4. `VALIDATION_OUTPUT.txt`

Tests, risk/persistence/runtime code, config, builder, generated JSON, Atlas, other families, root controls, roadmaps and ExecPlans are forbidden.

## Novel findings, validation and pass

Resolve and log novel concepts only within this family. A synonym-audit tooling concept belongs to PM-010 integration evidence unless it reveals a semantic conflict. Prove exact coverage, authority separation, unchanged unassigned vocabulary, unchanged tests/source/generated files, allowed-path compliance and `git diff --check`.

PM-009 passes only when every fixed concept has a complete decision and advisory/evidence surfaces remain non-deploying. On pass, continue to PM-010.
