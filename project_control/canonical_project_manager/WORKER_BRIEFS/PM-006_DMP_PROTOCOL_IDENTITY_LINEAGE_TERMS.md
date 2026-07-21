# Worker Brief PM-006 — DMP, Protocol, Identity and Lineage Terms

## Dispatch state

`authorised_after_PM-005_pass`

## Exact outcome

Semantically adjudicate the DMP V3 protocol surfaces, packet fields, identity fields, lineage concepts and dependency packet identifiers. Preserve source identity, domain identity, packet occurrence, run/scenario identity and technical module identity as separately governed concepts wherever the protocol normatives require that distinction.

## Prerequisite

PM-005 must record `unit_result: pass` with no forbidden changes.

## Fixed concept set

Generated entries:

`DMP V3`; `DmpV3Envelope`; `DmpV3Packet`; `DeskModulePacketV3`; `packetrole`; `producer`; `lineage`; `validation`; `summary`; `dmpextensions`; `module_id`; `module_version`; `module_instance_id`; `grammar_role`; `behaviour_class`; `traceid`; `runid`; `scenarioid`; `Dependency Packet IDs`.

Working-overlay admissions:

`packet occurrence`; `provenance`.

Temporal field-level and workbook provenance were assigned to PM-005. Reuse their accepted distinctions but do not reopen them.

## Authority and tests

The DMP protocol normatives and higher identity/lineage doctrine establish meaning. Current packet schemas, serialisation code, fixtures and tests are observed implementation/proof evidence only. A passing packet test cannot admit a field name or prove that identity classes are correctly separated.

## Required full reads

Create the unit manifest first, then read root controls, programme controls, all prior outputs, and:

- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
- `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md`;
- `docs/03_DOMAIN_MODEL_CORE.md` and relevant identity/lineage material in its working overlays;
- `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`, and `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md`;
- `docs/05_GUARDRAILS_CORE.md` and `docs/05.1_GUARDRAILS_WORKING.md`;
- `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`, `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`, and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md`;
- `docs/09_DMPV3_PROTOCOL_CORE.md` and `docs/09.1_DMPV3_PROTOCOL_WORKING.md`;
- both vocabulary normatives and all three vocabulary documents;
- every source schema/contract file that defines `DmpV3Envelope`, `DmpV3Packet` or `DeskModulePacketV3`;
- Tier A DMP V3 and vocabulary tests mentioning a fixed concept, read-only;
- current builder and generated entries for this family.

## Required decisions

For every fixed concept record exact label, normalised slug, governing proposition/source locator, bounded definition/scope, semantic owner, relationships/distinctions, canonical label/slug, lawful aliases, disallowed phrases, lifecycle/status, semantic disposition (`retain`, `enrich`, `admit_new`, `alias`, `quarantine`, `retire`, or `reject`), the four-value candidate action when applicable (`enrich_existing`, `add_new`, `alias_only`, or `quarantine`), PM-010 projection action, rationale and evidence. Additionally record:

- protocol surface versus carrier versus field versus identity class;
- owner and lawful producer;
- required identity scope and collision boundary;
- lineage/provenance payload meaning;
- packet occurrence versus upstream source/domain identity;
- run, trace and scenario relationships;
- whether each legacy/camel-case label is canonical, alias-only or compatibility-only.

Do not infer semantic equivalence from similarly named packet classes. Do not collapse `traceid`, `runid`, `scenarioid`, `module_instance_id` or packet occurrence. Do not promote donor field spellings merely because current code serialises them.

## Allowed changes and outputs

Allowed changes are limited to `units/PM-006/**`, assigned human-registry additions/entries, and the matching `packet occurrence`/`provenance` admission text in section 10.8/10.7 when required. Required outputs are:

1. `PM-006_FULL_READ_MANIFEST.tsv`
2. `DMP_PROTOCOL_IDENTITY_LINEAGE_ADJUDICATION_REGISTER.tsv`
3. `PM-006_RECEIPT.md`
4. `VALIDATION_OUTPUT.txt`

Tests, schemas/contracts, runtime code, config, builder, generated JSON, Atlas, other families, root controls, roadmaps and ExecPlans are forbidden.

## Novel findings, validation and pass

Resolve and log novel concepts only within this family. Route stage/input carrier concepts to PM-007 and downstream/broker concepts to PM-008. Prove exact coverage, identity-class separation, unchanged unassigned vocabulary, unchanged tests/source/generated files, allowed-path compliance and `git diff --check`.

PM-006 passes only when every fixed concept has a complete decision and no identity or lineage class is silently collapsed. On pass, continue to PM-007.
