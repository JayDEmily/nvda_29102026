# Atlas Surface Slice Pack — Active Pack

## Status

Active pack for materialising the large Atlas/Bridge JSON evidence into bounded `blueprint_surface` slice files.

## Purpose

This pack makes the Atlas evidence usable for future bounded tranches without repeatedly loading the full native satisfaction ledger, raw Atlas, coverage view, and owner map view.

## Scope

Permitted work:

- read the existing immutable Atlas/Bridge JSON evidence;
- generate one materialised slice file per `blueprint_surface`;
- generate manifest, checksum, schema, and tranche receipt surfaces;
- verify record counts, joins, checksums, and deterministic regeneration.

Prohibited work:

- no runtime code changes;
- no test changes;
- no new Atlas implementation tranche;
- no modification of original Atlas/Bridge source JSON files;
- no virtual environment creation.

## Output paths

- `scripts/materialise_atlas_surface_slices.py`
- `var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json`
- `var/audit/atlas_surface_slices/atlas_surface_slice_checksums.json`
- `var/audit/atlas_surface_slices/atlas_surface_slice.schema.json`
- `var/audit/atlas_surface_slices/slices/*.json`
- `var/audit/briefs/2026-04-28_ATLAS_SURFACE_SLICE_PACK_TRANCHE.md`
- `var/audit/ledgers/atlas_surface_slice_pack_tranche_ledger.json`
- `var/audit/ledgers/atlas_surface_slice_pack_tranche_ledger.schema.json`

## Required invariant

The generated surface slices are derived evidence only. They do not replace the original Atlas/Bridge JSON sources and do not themselves authorise implementation work.
