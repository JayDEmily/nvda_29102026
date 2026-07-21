# Worker Brief PM-005 — Calendar, Temporal and Provenance Terms

## Dispatch state

`authorised_after_PM-004_pass`

## Exact outcome

Semantically adjudicate the calendar, temporal-standard, temporal-audit and temporal-provenance family. Preserve the distinctions between reference truth, operational observations, derived context, source time, capture time, persistence time and provenance.

## Prerequisite

PM-004 must record `unit_result: pass` with no forbidden changes.

## Fixed concept set

Human headings:

`Event Calendar`; `Market Session Reference`; `Financial Event Reference`; `Operational Calendar State`; `Derived Runtime Calendar Context`.

Generated entries:

`Financial Calendar Reference Bundle`; `Financial Calendar Crosswalk`; `Financial Calendar Import Record`; `Event Calendar`; `Source Temporal Standard`; `source_time_raw`; `source_time_kind`; `source_timezone_raw`; `source_time_utc`; `source_date`; `captured_at_utc`; `persisted_at_utc`; `source_provider`; `source_channel`; `time_granularity`; `next_event_time_utc`; `window_start_utc`; `window_end_utc`; `runtime_bar_time_utc`; `Temporal Conformance Inventory`; `Already Conformant`; `Needs Proof/Test Remediation Only`; `Needs Code/Persistence Remediation in Tranche 3`; `Reserved / Blocked`; `Workbook Temporal Provenance`; `Field-level Provenance`.

The four matching calendar admissions in section 10.8 are included. General DMP `provenance` belongs to PM-006 and must not be decided here.

## Authority and tests

Calendar and temporal normatives establish meaning. Current contracts, importers, persistence code, workbook artefacts and tests are observed evidence only. Test colour cannot decide whether a timestamp or provenance term is authoritative, derived or complete.

## Required full reads

Create the unit manifest first, then read root controls, programme controls, all prior outputs, and:

- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
- `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md`;
- `docs/03_DOMAIN_MODEL_CORE.md`, `docs/03.1_DOMAIN_MODEL_WORKING.md`, and `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md`;
- `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`, and `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md`;
- `docs/05_GUARDRAILS_CORE.md` and `docs/05.1_GUARDRAILS_WORKING.md`;
- `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`, `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`, and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md`;
- both vocabulary normatives and all three vocabulary documents;
- `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`;
- `docs/planning/2026-03-25_GATE41_RAW_DERIVED_SIGNAL_WORKBOOK.md` and `docs/planning/2026-04-02_GATE159_WORKBOOK_LINEAGE_AND_CONSOLIDATION_AUDIT.md` for temporal/provenance propositions only;
- `src/nvda_desk/contracts/temporal.py` and every directly referenced calendar contract/module needed to understand the fixed concepts;
- Tier A calendar/temporal/vocabulary tests that mention a fixed concept, read-only;
- current builder and generated entries for this family.

## Required decisions

For every fixed concept record exact label, normalised slug, governing proposition/source locator, bounded definition/scope, semantic owner, relationships/distinctions, canonical label/slug, lawful aliases, disallowed phrases, lifecycle/status, semantic disposition (`retain`, `enrich`, `admit_new`, `alias`, `quarantine`, `retire`, or `reject`), the four-value candidate action when applicable (`enrich_existing`, `add_new`, `alias_only`, or `quarantine`), PM-010 projection action, rationale and evidence. Additionally record:

- authority class: reference, operational, derived, source-observed, capture, persistence, audit or provenance;
- owner and lawful writer;
- effective/as-of semantics;
- timezone/normalisation semantics where applicable;
- mutability and historical-preservation rule;
- relationship to source identity and field-level provenance.

Do not merge source, capture and persistence time. Do not let derived runtime context rewrite reference or operational history. Audit classifications must remain status labels, not behaviour authority.

## Allowed changes and outputs

Allowed changes are limited to `units/PM-005/**`, assigned registry entries, and the matching bounded calendar admissions in section 10.8. Required outputs are:

1. `PM-005_FULL_READ_MANIFEST.tsv`
2. `CALENDAR_TEMPORAL_PROVENANCE_ADJUDICATION_REGISTER.tsv`
3. `PM-005_RECEIPT.md`
4. `VALIDATION_OUTPUT.txt`

Tests, contracts, runtime code, config, builder, generated JSON, workbooks, Atlas, other families, root controls, roadmaps and ExecPlans are forbidden.

## Novel findings, validation and pass

Resolve and log novel concepts only inside this family. Route protocol identity/lineage to PM-006. Prove exact coverage, complete distinctions, unchanged unassigned vocabulary, unchanged tests/source/generated files, allowed-path compliance and `git diff --check`.

PM-005 passes only when every fixed concept has a complete decision and no temporal authority classes have been collapsed. On pass, continue to PM-006.
