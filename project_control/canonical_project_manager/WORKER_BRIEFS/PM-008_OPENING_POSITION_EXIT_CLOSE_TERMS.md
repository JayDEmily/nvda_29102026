# Worker Brief PM-008 — Opening, Placement, Position, Inventory, Exit and Close Terms

## Dispatch state

`authorised_after_PM-007_pass`

## Exact outcome

Semantically adjudicate the downstream opening-through-close family. Preserve each authority transition from capital decision through opening, readiness, handoff, broker protocol, live position, inventory, exit and close.

## Prerequisite

PM-007 must record `unit_result: pass` with no forbidden changes.

## Fixed concept set

Human headings and matching generated entries:

`Opening Architecture`; `Downstream Opening`; `Placement Readiness`; `Placement Handoff`; `Broker Protocol`; `Live Position`; `Inventory Architecture`; `Exit Architecture`; `Close Architecture`.

No stage, capital-decision, parallel-risk or review concept may be re-adjudicated here.

## Authority and tests

Domain, architecture, ownership, state/risk/replay and guardrail normatives establish downstream meaning. Current contracts, broker adapters, state models and tests are observations only. Passing tests do not prove that a boundary owns lawful deployment or lifecycle authority.

## Required full reads

Create the unit manifest first, then read root controls, programme controls, all prior outputs, and:

- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
- `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md`;
- both briefing/execution operating-model documents;
- `docs/03_DOMAIN_MODEL_CORE.md` and `docs/03.1_DOMAIN_MODEL_WORKING.md`;
- `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` and `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`;
- both guardrail documents;
- all three runtime ownership/state/replay documents under `docs/07*`;
- both vocabulary normatives and all three vocabulary documents;
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md` for target owners/seams;
- `src/nvda_desk/contracts/downstream.py` and every directly governing public contract/source file for the fixed concepts;
- Tier A tests mentioning fixed concepts, read-only;
- current builder and generated entries for this family.

## Required decisions

For every fixed concept record exact label, normalised slug, governing proposition/source locator, bounded definition/scope, semantic owner, relationships/distinctions, canonical label/slug, lawful aliases, disallowed phrases, lifecycle/status, semantic disposition (`retain`, `enrich`, `admit_new`, `alias`, `quarantine`, `retire`, or `reject`), the four-value candidate action when applicable (`enrich_existing`, `add_new`, `alias_only`, or `quarantine`), PM-010 projection action, rationale and evidence. Additionally record:

- input authority and output carrier for each transition;
- owner and lawful writer;
- whether the term is architecture, decision, readiness state, handoff carrier, protocol, live state, inventory owner, exit authority or closure authority;
- lifecycle transition and prohibited upstream/downstream authority;
- distinctions among opening, placement, broker submission, live position, inventory, exit and close.

Do not treat Placement Readiness as order authority. Do not conflate Placement Handoff with Broker Protocol. Do not use Live Position, Inventory Architecture, Exit Architecture or Close Architecture interchangeably.

## Allowed changes and outputs

Allowed changes are limited to `units/PM-008/**`, assigned registry entries, and matching bounded vocabulary admissions when required. Required outputs are:

1. `PM-008_FULL_READ_MANIFEST.tsv`
2. `OPENING_POSITION_EXIT_CLOSE_ADJUDICATION_REGISTER.tsv`
3. `PM-008_RECEIPT.md`
4. `VALIDATION_OUTPUT.txt`

Tests, runtime/contracts, config, builder, generated JSON, Atlas, other families, root controls, roadmaps and ExecPlans are forbidden.

## Novel findings, validation and pass

Resolve and log novel concepts only within this downstream family. Route review/explanation/playbook concepts to PM-009. Prove exact coverage, lifecycle/owner separation, unchanged unassigned vocabulary, unchanged tests/source/generated files, allowed-path compliance and `git diff --check`.

PM-008 passes only when every fixed concept has a complete decision and each authority transition remains explicit. On pass, continue to PM-009.
