# Atlas Plan2 vocabulary candidate classification

Status: vocabulary candidates classified; no vocabulary registry or canonical vocabulary file modified.

## Authority rule

Vocabulary authority requires candidate terms to be classified as exactly one of `enrich_existing`, `add_new`, `alias_only`, or `quarantine`. This Stage 1 reset records classifications only. It does not admit new canonical vocabulary.

## Candidate table

| Candidate term | Classification | Reason | Stage 1 handling |
|---|---|---|---|
| source brief | `alias_only` | Useful compiler term for source-intent input; repo already has active brief/plan surfaces. | Use only when referring to compiler discipline. |
| accepted brief | `add_new` | Distinct semantic-boundary concept not present as canonical registry term. | Future vocabulary gate required before canonical use. |
| binding atom | `add_new` | Durable planning decomposition term from compiler reference. | Quarantine from normative repo language until admitted. |
| atom matrix | `add_new` | Derived matrix concept from compiler reference. | Future vocabulary gate required. |
| ExecPlan | `enrich_existing` | Repo `PLANS.md` already uses execution-plan/ExecPlan-style language. | Use as repo-plan discipline, not as new runtime object. |
| ordered leaves | `enrich_existing` | `leaf` is admitted in the working vocabulary overlay; ordered sequencing is process discipline. | Future tranche may use under `PLANS.md`. |
| release audit | `add_new` | Compiler-specific pre-handoff audit label. | Treat as candidate planning term only. |
| losslessness proof | `add_new` | Useful proof concept for preserving obligations/prohibitions/source scope. | Record as candidate proof term only. |
| Atlas surface slice | `alias_only` | Existing slice-pack artefact term refers to generated `blueprint_surface` slice files. | Use as evidence label, not implementation authority. |
| blueprint_surface | `quarantine` | Existing JSON key appears in Atlas evidence; canonical human-facing repo term is `architecture surface`. | Preserve as JSON-field label only. |
| implementation leaf | `quarantine` | Appears in Atlas evidence fields, but Stage 1 cannot open implementation leaves. | Keep as evidence field; no executable leaf creation. |

## Non-admission statement

No durable term is admitted by this file. Any future Atlas tranche that needs these terms in live normative or executable planning surfaces must run a lawful vocabulary gate first or carry the term as explicitly quarantined evidence language.
