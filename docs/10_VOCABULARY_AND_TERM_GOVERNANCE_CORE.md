# 10_VOCABULARY_AND_TERM_GOVERNANCE_CORE

All repo paths in the numbered control stack are repo-root-relative.


## Frozen rules

- one durable term must map to one governed meaning
- aliases must be explicit rather than accidental
- compatibility labels must not silently become canonical runtime truth
- machine vocabulary identities must use the admitted `namespace.canonical_slug` form; collision and audit scope must follow the owning namespace plus explicitly imported shared vocabulary
- durable terms must not be admitted into docs, schemas, manifests, receipts, or code unless they are already governed or the same bounded gate lawfully updates the vocabulary system first

## Authoritative artefacts

Use these together:

- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/vocabulary/vocabulary_registry.md`
- `src/nvda_desk/schemas/vocabulary.py`
- `src/nvda_desk/vocabulary_builder.py`
- `scripts/build_canonical_vocabulary.py`
- `data/vocabulary/canonical_vocabulary.json`

## Admission rule

The vocabulary system is an admission system, not a free-form glossary.

Candidate terms must be classified as exactly one of:
- `enrich_existing`
- `add_new`
- `alias_only`
- `quarantine`

A new durable term must land in live repo surfaces only after lawful admission.

## Supporting migrated surfaces

The detailed supporting material remains in:
- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/reference/vocabulary_dictionary_system_audit.md`

## Native Architecture Blueprint boundary

Within native code-structure architecture scope, this document must be read with `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

`docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` owns target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability for native code-structure architecture.

It does not override the authority hierarchy defined by `docs/01_NORMATIVE_CORE.md`.

All durable terms used by live control documents must be governed by `docs/vocabulary/vocabulary_registry.md` or lawfully admitted by the vocabulary process before they become canonical language.
