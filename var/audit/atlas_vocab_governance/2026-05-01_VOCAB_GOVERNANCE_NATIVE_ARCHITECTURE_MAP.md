# Vocabulary governance native architecture map — 2026-05-01

## Result
The selected Atlas candidate maps to the Native Architecture Blueprint surface `Vocabulary governance interface` and owner `vocabulary governance authority`. The mapping is candidate-planning evidence only.

## Native Architecture Blueprint binding
| Blueprint clause | Planning implication |
|---|---|
| `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` §5.18 | Vocabulary governance owns durable term admission, aliases, quarantines, synonym collision handling, canonical vocabulary regeneration, and proof receipts. |
| §5.18 target owner | Future work must bind to `vocabulary governance authority`; this package does not alter that owner. |
| §5.18 target status | `thin_seam`; future implementation/conformance work must preserve the seam boundary. |
| §5.18 inputs | Candidate durable terms, aliases, disallowed phrases, synonym candidates, and architecture-surface language. |
| §5.18 outputs | Admitted terms, aliases, quarantines, canonical vocabulary JSON, and vocabulary proof receipts. |
| §5.18 prohibited outputs | Runtime trading decisions, architecture decisions without authority, and user-vernacular leakage. |
| §5.18 proof interface | Builder parity, synonym audit, disallowed-phrase checks, canonical JSON validation. |

## Selected-slice mapping summary
| Measure | Count |
|---|---:|
| Records in selected slice | 10 |
| Records with `passed_reuse_existing` vocabulary gate | 10 |
| Tier A proof records | 10 |
| Records with future tests-first route type | 6 |
| Records with future documentation/control clarification route type | 3 |
| Evidence-only records | 1 |

## Cross-surface dependencies
- `docs/10_*` and `docs/vocabulary/*` govern term admission and workflow language.
- `src/nvda_desk/schemas/vocabulary.py` and `src/nvda_desk/vocabulary_builder.py` are native code surfaces visible to the candidate, but this package does not change them.
- `data/vocabulary/canonical_vocabulary.json` is the canonical generated vocabulary data surface visible to proof and parity checks; this package does not regenerate it.
- `tests/tier_a/vocabulary/*` are future proof/test surfaces visible to the candidate; this package does not edit or run implementation tests.
- `config/proof_blocks.yaml` and `config/retained_test_registry.yaml` are future proof/registry surfaces visible to the candidate; this package does not change configuration.

## Architecture risk classification
The safest next route is a future tests-first conformance route with an initial control/vocabulary/proof intake gate. That gate must first settle the three `later_blueprint_leaf` records before any code-level conformance work is planned.
