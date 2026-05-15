# Vocabulary Hash Coverage Remediation Report

Decision: update `GOVERNED_SOURCE_PATHS` to cover authoritative vocabulary law, workflow, registry, builder, schema, synonym-audit implementation, and committed canonical vocabulary while excluding generated synonym-audit output to avoid self-referential fingerprint churn.

## Current governed source set

- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/vocabulary/vocabulary_registry.md`
- `scripts/build_canonical_vocabulary.py`
- `src/nvda_desk/schemas/vocabulary.py`
- `src/nvda_desk/vocabulary_builder.py`
- `src/nvda_desk/vocabulary_synonym_audit.py`
- `data/vocabulary/canonical_vocabulary.json`

## Path decisions

| Path | Role | Decision | Included now | Evidence |
|---|---|---|---:|---|
| `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` | normative vocabulary law | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` | working vocabulary governance companion | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `docs/vocabulary/README.md` | vocabulary artefact index | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` | candidate/consolidation workflow authority | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `docs/vocabulary/vocabulary_registry.md` | durable term registry authority | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `scripts/build_canonical_vocabulary.py` | canonical builder wrapper/CLI authority | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `src/nvda_desk/schemas/vocabulary.py` | vocabulary schema authority | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `src/nvda_desk/vocabulary_builder.py` | canonical vocabulary builder authority | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `src/nvda_desk/vocabulary_synonym_audit.py` | synonym audit/fingerprint implementation authority | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `data/vocabulary/canonical_vocabulary.json` | committed canonical vocabulary artefact | `include_in_hash_set` | yes | `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` |
| `var/vocabulary/synonym_candidates.json` | generated synonym audit output | `audit_relevant_but_not_hash_source` | no | excluded by decision; proof-owned generated output, not source hash input |

## Result

DEF-001 status: `fixed`.
`var/vocabulary/synonym_candidates.json` remains governed by proof commands and artefact diff, but is not itself hashed as a source input.
