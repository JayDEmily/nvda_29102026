# Vocabulary Governance

This folder governs canonical repo language after the architecture is pinned.

## What this is for

- keep one term meaning one thing;
- keep aliases explicit rather than accidental;
- stop stale `session_clock`-era labels or duplicate playbook labels from drifting back in;
- preserve the difference between raw primitives, derived features, stage labels, family labels, setup variants, execution expressions, and workflow-routing concepts such as Step 0 calendar/horizon and carry handoff.

## What this is not for

- not a blind merge target for stale harvested vocabulary payloads;
- not a runtime redesign surface;
- not a free-form glossary detached from typed contracts.

## Authority and projection surfaces

1. vocabulary law: `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` and `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`;
2. human-readable governed meaning: the accepted records in `docs/vocabulary/vocabulary_registry.md`; retained admission sections in the normative overlay preserve lineage only;
3. feeder and reconciliation workflow: `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`;
4. machine schema and projection implementation: `src/nvda_desk/schemas/vocabulary.py`, `src/nvda_desk/vocabulary_builder.py`, and `scripts/build_canonical_vocabulary.py`;
5. committed generated enforcement projection: `data/vocabulary/canonical_vocabulary.json`;
6. candidate reports, touch stamps and tests: bounded evidence only.

Generated artefacts, scanners, stamps, helpers and green tests cannot create semantic admission or redefine a durable term. Accepted human-readable meaning must precede and govern its machine projection. A lineage redirect in `10.1` identifies an admission decision and canonical identities; it does not duplicate or override the registry records.

## Accepted registry record

Each `###` record in `vocabulary_registry.md` carries the complete human meaning first: definition, scope, semantic owner, relationships, aliases, disallowed or misleading use, and lifecycle. Its single `Projection metadata:` JSON line is an explicit admission/projection record, not a second semantic source. It records the accepted canonical label/slug, vocabulary namespace, structural projection fields, decision references, machine-safe aliases/disallowed tokens, contextual omissions, and historical noncanonical phrase inventory. The registry header records admitted namespace scan scopes and imports. That phrase inventory is descriptive only and never suppresses an audit globally; exact resolved occurrences are evidenced in the PM-010 candidate-disposition register by path, line, column and context hash.

The builder must fail on a missing, duplicated, unknown or contradictory projection field. It may transform these records into `VocabularyEntry` objects; it must not seed terms, infer missing meaning, or restore a label from tests or previous generated JSON.

## Occurrence-scoped candidate resolution

Canonical labels and lawful aliases are recognised inside their admitted namespace plus imported `global` vocabulary. Machine identity is `namespace.canonical_slug`; the namespace prefix is not imposed on human labels or ordinary code symbols. A noncanonical phrase disposition suppresses only the exact evidenced occurrence with the same path, line, column, normalised phrase and source-context SHA-256 inside the audit's declared scan scope. A new path, new occurrence or changed context must be reported again. Disallowed phrases and historical phrase inventories remain semantic evidence, not canonical exact tokens.
