# 2026-05-01 Atlas planning/compiler route setup plan

Status: Stage 1 planning/control-surface route setup only.

## 1. Source authority and route boundaries

| Authority/input | Stage 1 status |
|---|---|
| Current user repair instruction | Opens bounded Plan2 repair and forbids applying the rejected bundle. |
| `/mnt/data/atlas_plan2.md` | Active worker-control document for Stage 1 reset workflow and patch shape. |
| Active repo ZIP | `/mnt/data/NVIDIA9_remotetest-main (1).zip`. |
| Repo authority | `READY_TO_CONSIDER_ATLAS = false` remains recorded; Atlas implementation remains closed. |
| Planning-compiler ZIP | Reference-only planning discipline. |

This plan is subordinate to repo authority and preserves the hard prohibitions recorded in `var/audit/atlas_plan2/source_lock_authority_receipt.md`.

## 2. Atlas evidence intake model

The Atlas evidence package is present in the active repo ZIP and is not an absent blocker.

Ordinary Stage 1 and future roadmap planning may use:

- `var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json`
- `var/audit/atlas_surface_slices/atlas_surface_slice_checksums.json`
- `var/audit/atlas_surface_slices/atlas_surface_slice.schema.json`
- the 18 JSON slice files under `var/audit/atlas_surface_slices/slices/`
- `var/audit/briefs/2026-04-28_ATLAS_SURFACE_SLICE_PACK_TRANCHE.md`
- `var/audit/briefs/2026-04-28_ATLAS_TRANCHE_ROADMAP_PLAN.md`

The original source JSON files remain retained source evidence:

- `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json`
- `var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json`
- `var/audit/imports/atlas_bridge_inputs/legacy_file_coverage_view.json`
- `var/audit/imports/atlas_bridge_inputs/legacy_owner_map_view.json`

Inventory details are recorded in `var/audit/atlas_plan2/atlas_evidence_inventory.md`.

## 3. Compiler-discipline adaptation model

Stage 1 adopts planning-compiler discipline as a control method only:

1. preserve source instruction and Atlas evidence provenance;
2. reconcile any future tranche brief against repo authority and vocabulary law;
3. classify obligations/prohibitions/proof needs explicitly;
4. prevent direct lowering from raw Atlas evidence into implementation leaves;
5. require future dispatch to one bounded tranche at a time;
6. require release/losslessness audit before a future implementation handoff.

The mapping is recorded in `var/audit/atlas_plan2/compiler_reference_mapping.md`.

## 4. Vocabulary gate requirements

Future Atlas tranche planning must classify durable terms before treating them as canonical. The current candidate classifications are recorded in `var/audit/atlas_plan2/vocabulary_candidate_classification.md`.

Stage 1 does not modify:

- `docs/vocabulary/vocabulary_registry.md`
- `data/vocabulary/canonical_vocabulary.json`
- vocabulary schemas or generator code

## 5. Proof/testing classification requirements

Current Stage 1 proof is control-surface proof only. It consists of:

- archive source lock and authority intake;
- JSON parse validation for 25 present Atlas JSON files;
- checksum and validate-only evidence for the materialised slice pack;
- patch dry-run evidence;
- prohibited-path checks.

Runtime proof and pytest implementation proof are prohibited in Stage 1. Proof classification is recorded in `var/audit/atlas_plan2/testing_proof_classification.md`.

## 6. Losslessness requirements

A future Atlas tranche must not rely on this Stage 1 package as semantic proof of every Atlas record. Before any implementation route opens, the future tranche must prove:

- selected slice records reconcile to manifest/checksum evidence;
- raw/source obligations are either binding-carried, context-carried with justification, or lawfully excluded;
- vocabulary terms are admitted, aliased, or quarantined;
- exact implementation leaves are derived only after an accepted semantic boundary exists;
- no Stage 1 control receipt is used as runtime correctness proof.

## 7. Stop conditions

Stop future Atlas planning or implementation if:

- source ZIP/hash does not match the selected route input;
- required manifest, checksum, schema, source JSON, or selected slice file is missing;
- `jq -e .` or checksum/validate-only evidence fails;
- repo authority blocks the route;
- a proposed patch touches prohibited paths;
- future work would modify generated slices without reopening the slice-pack repair route;
- future work would open runtime/test/compiler/vocabulary changes without an authorised route;
- a semantic claim requires full reading of a giant JSON payload and the future worker cannot perform it.

## 8. Later implementation boundary

This plan does not open Atlas implementation. Later implementation may start only after a future route explicitly selects one bounded Atlas tranche and supplies:

- accepted brief or equivalent repo-authorised semantic boundary;
- selected slice evidence;
- vocabulary classification/admission handling;
- proof-tier ownership;
- exact touched/read-only/prohibited surfaces;
- patch and closeout obligations.

## 9. Dispatch method for future Atlas tranche planning

The next lawful planning step is roadmap/dispatch planning over the present 18-slice package, not implementation. The future worker should:

1. read current repo authority from the fresh working tree;
2. read the manifest, checksums, schema, and roadmap plan;
3. validate JSON and checksums;
4. create or repair the coarse roadmap ledger if authorised;
5. select at most one implementation-tranche candidate as candidate-only;
6. stop before executable implementation leaves unless a new route explicitly opens them.

## 10. Explicit non-readiness claims

This plan does not claim:

- `READY_TO_CONSIDER_ATLAS = true`;
- Atlas implementation readiness;
- runtime readiness;
- all repo proof gates pass;
- full semantic review of all 1716 Atlas records;
- active code/test alignment with Atlas evidence.
