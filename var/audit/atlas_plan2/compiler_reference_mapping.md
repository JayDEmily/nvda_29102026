# Atlas Plan2 compiler-reference mapping

Status: planning-compiler reference concepts mapped for Stage 1 planning/control-surface use only.

## Reference boundary

| Boundary | State |
|---|---|
| Planning-compiler ZIP extracted | `/mnt/data/atlas_plan2_repair_compiler_ref/repo` |
| Compiler code modified | No. |
| Compiler concepts imported as executable code | No. |
| Atlas made executable | No. |
| Use of compiler material | Planning discipline only. |

## Reference files read in full

| File | Relevant rule carried forward |
|---|---|
| `AGENTS.md` | Source brief must not lower directly into leaves; accepted brief, atom matrix, ExecPlan, ordered leaves, dual safety audit preserve meaning. |
| `PLANS.md` | Proposal 1A path and no silent vocabulary mutation. |
| `README.md` | Canonical model and authority order. |
| `docs/01_operating_model.md` | Six-stage model and release/closeout audit split. |
| `docs/02_terms_and_boundaries.md` | Semantic boundary, binding-atom, and authority definitions. |
| `docs/03_closeout_audit.md` | Raw-section and binding-atom accounting rules; closeout evidence rules. |
| `corpus/SEED_CORPUS.md` | Seed corpus is source intake only, not authority. |

## Mapping table

| Planning compiler concept | Atlas planning equivalent | Allowed Stage 1 use | Prohibited use | Vocabulary status |
|---|---|---|---|---|
| source brief | Current user instruction plus `atlas_plan2.md`; future single Atlas tranche brief | Preserve original intent and prohibitions before route planning. | Treat raw Atlas record text as accepted implementation authority. | `alias_only` to source-intent input for this Stage 1 package. |
| accepted brief | Future accepted Atlas tranche brief after repo-authority/vocabulary reconciliation | Require a future semantic boundary before any implementation tranche. | Claim this Stage 1 plan is an implementation accepted brief. | `add_new` candidate unless repo vocabulary already admits the term in a future gate. |
| binding atom | Atomic Atlas planning obligation/prohibition/proof requirement | Use as future planning decomposition unit for one selected tranche. | Generate executable leaves from unvalidated raw Atlas records. | `add_new` candidate; quarantined until vocabulary gate. |
| atom matrix | Matrix carrying every accepted obligation/prohibition with provenance | Require future losslessness proof from tranche brief to leaves. | Make the matrix peer authority over accepted Markdown. | `add_new` candidate; Stage 1 records the concept only. |
| ExecPlan | Repo-local execution plan surface governed by `PLANS.md` | Future tranche may use an ExecPlan-style route after accepted brief and inventory. | Create or update repo `EXEC_PLAN.md` in this reset. | `enrich_existing` candidate because repo `PLANS.md` already uses execution-plan language. |
| ordered leaves | Sequential bounded future work units under a lawful active tranche | Future implementation tranche may emit leaves only after accepted brief and proof design. | Open executable implementation leaves in Stage 1. | `enrich_existing` candidate because `leaf` is admitted in working vocabulary. |
| release audit | Pre-handoff check from source/accepted brief through plan/leaves | Require future Atlas tranche package to prove no loss before dispatch. | Treat release audit as runtime proof. | `add_new` candidate for planning discipline. |
| losslessness proof | Proof that source obligations, prohibitions, order, vocabulary, and evidence survive downstream | Require future Atlas tranche plan to reconcile source records, manifest, slices, and selected scope. | Claim all 1716 records are semantically proven by this Stage 1 inventory. | `add_new` candidate; concept remains planning-only. |

## Stage 1 adaptation rule

Compiler discipline is adopted as a control pattern: source intake -> accepted semantic boundary -> explicit atom/proof mapping -> dispatchable future tranche plan -> later audit. No planning-compiler code, generated compiler artefact, Atlas runtime implementation, pytest implementation change, or vocabulary mutation is authorised by this mapping.
