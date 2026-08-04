# Atlas Surface Slice Pack Tranche

Status: closed
Promotion readiness: true for derived slice-pack use; no runtime implementation work opened
Implementation tranche opened: false

## Purpose

Materialise the large Atlas/Bridge evidence files into bounded `blueprint_surface` slice files so future Atlas tranches can read one native architecture slice instead of repeatedly loading the full native satisfaction ledger, raw Atlas, coverage view, and owner map view.

## Scope boundary

In scope:

- read immutable Atlas/Bridge JSON evidence;
- generate one materialised JSON slice per native `blueprint_surface`;
- generate manifest, checksum, and slice schema surfaces;
- verify counts, joins, uniqueness, and deterministic checksums;
- close this as data-preparation work only.

Out of scope:

- no runtime source changes;
- no test changes;
- no feature implementation leaves;
- no new Atlas implementation tranche;
- no mutation of original Atlas/Bridge source JSON files;
- no virtual environment creation.

## Authority and evidence read

- `AGENTS.md`
- `PLANS.md`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- `docs/01_NORMATIVE_CORE.md`
- `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md`
- `docs/05_GUARDRAILS_CORE.md`
- `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json`
- `var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json`
- `var/audit/imports/atlas_bridge_inputs/legacy_file_coverage_view.json`
- `var/audit/imports/atlas_bridge_inputs/legacy_owner_map_view.json`

## Touched surfaces

- `AGENTS.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `intent_migration/atlas_surface_slice_pack/AGENTS.override.md`
- `scripts/materialise_atlas_surface_slices.py`
- `var/audit/atlas_surface_slices/atlas_surface_slice.schema.json`
- `var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json`
- `var/audit/atlas_surface_slices/atlas_surface_slice_checksums.json`
- `var/audit/atlas_surface_slices/slices/*.json`
- `var/audit/briefs/2026-04-28_ATLAS_SURFACE_SLICE_PACK_TRANCHE.md`
- `var/audit/ledgers/atlas_surface_slice_pack_tranche_ledger.json`
- `var/audit/ledgers/atlas_surface_slice_pack_tranche_ledger.schema.json`

## Output contracts

The generated slice pack contains:

- one manifest at `var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json`;
- one checksum manifest at `var/audit/atlas_surface_slices/atlas_surface_slice_checksums.json`;
- one slice schema at `var/audit/atlas_surface_slices/atlas_surface_slice.schema.json`;
- 18 slice files under `var/audit/atlas_surface_slices/slices/`, one per `blueprint_surface`.

The original Atlas/Bridge evidence files remain immutable source evidence.

## Ordered leaf queue

| Leaf | Status | Purpose | Evidence |
|---|---|---|---|
| ATLAS-SLICE-L01 | closed | Admit active slice-pack route and bounded plan | `AGENTS.md`; `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`; this brief |
| ATLAS-SLICE-L02 | closed | Generate materialised surface slices | `scripts/materialise_atlas_surface_slices.py`; `var/audit/atlas_surface_slices/` |
| ATLAS-SLICE-L03 | closed | Validate counts, joins, checksums, and closeout | manifest validation; checksum manifest; tranche ledger |

## Proof obligations

Required checks:

- source native ledger record count equals 1716;
- raw Atlas record count equals 1716;
- generated slice count equals 18;
- total records across slices equals 1716;
- unique `atlas_record_id` count across slices equals 1716;
- no duplicate native `atlas_record_id` values;
- no duplicate raw Atlas `atlas_record_id` values;
- every native record has a matching raw Atlas record;
- coverage refs and owner refs join only to native ledger IDs;
- generated file checksums validate;
- generated outputs parse as JSON;
- no runtime source or test files are changed.

## Verification result

The materialisation script reported:

```text
slice_count: 18
total_records: 1716
validation_result: passed
failures: []
unique_atlas_record_ids_across_slices: 1716
```

The manifest records:

```text
native_record_count: 1716
raw_record_count: 1716
slice_count: 18
total_records_across_slices: 1716
slice_total_matches_native_record_count: true
```

## Stop conditions

Stop if:

- any native ledger record lacks a raw Atlas match;
- any generated slice duplicates an `atlas_record_id`;
- total slice records do not equal 1716;
- any original Atlas/Bridge source file is modified;
- runtime source or tests are touched;
- JSON parse or checksum validation fails.

No stop condition fired.

## Discoveries and corrections

The first checksum validation attempt failed because the manifest checksum was calculated before the final manifest state was stable. The generator was corrected so the manifest is final before checksums are calculated. The final validation passed.

## Decision log

- The split key is `records[*].blueprint_surface` from `native_intent_satisfaction_ledger.json`.
- The raw Atlas joins to the native ledger by `atlas_record_id`.
- Coverage refs and owner refs are materialised into each slice by `atlas_record_id`.
- The 18 generated slice files are usability shards, not implementation tranches.

## Carry-forward blockers

- Large surfaces may still need sub-splitting into multiple implementation tranches.
- Slice files do not prove active code/test alignment.
- Future Atlas tranche selection must read the relevant slice and then apply normative docs → tests/proofs → code hierarchy.
