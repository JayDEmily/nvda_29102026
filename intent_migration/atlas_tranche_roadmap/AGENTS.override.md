# Atlas Tranche Roadmap — Active Pack

## Status

Active bounded planning-only pack for the Atlas roadmap/tranche-selection route.

This pack is not an implementation tranche. Worker Gate 4 only makes this pack the active bounded planning route; it does not create roadmap ledger/schema files, score or select a candidate tranche, or open implementation. Those outputs remain closed unless a later PM brief explicitly opens the later gate.

## Purpose

This pack converts the 18 materialised Atlas surface slices into a bounded migration roadmap so future work can select one implementation tranche at a time without reloading the giant Atlas/Bridge JSON files.

## Mandatory reading

Read these surfaces before executing this pack:

1. `AGENTS.md`
2. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
3. `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
4. `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
5. `var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json`
6. `var/audit/atlas_surface_slices/atlas_surface_slice_checksums.json`
7. `var/audit/briefs/2026-04-28_ATLAS_TRANCHE_ROADMAP_PLAN.md`

## Scope

Permitted work:

- read the materialised Atlas surface slice manifest and per-surface slice files when a later PM-authorised roadmap-planning gate requires it;
- create a coarse roadmap ledger from the 18 `blueprint_surface` slices only when a later PM brief explicitly opens roadmap ledger/schema creation;
- classify proposed roadmap tranches by record count, leaf-type mix, satisfaction status, dependency posture, and execution risk only inside a later authorised roadmap-planning gate;
- propose tranche splits where a surface is too large or internally heterogeneous only inside a later authorised roadmap-planning gate;
- record at most candidate-only implementation-tranche selection after the roadmap ledger exists and only when a later PM brief explicitly authorises candidate selection;
- update route and receipt surfaces required for this roadmap pack.

Gate 4 route-transition boundary:

- Gate 4 opens only the active planning route.
- Gate 4 does not create roadmap ledger/schema outputs.
- Gate 4 does not score, rank, or select candidate tranches.
- Gate 4 does not claim full semantic review of all 1,716 Atlas records.
- Gate 4 does not change runtime code, pytest implementation files, vocabulary files, generated Atlas slices, original Atlas/Bridge source JSON, or planning-compiler code.

Prohibited work:

- no runtime code changes;
- no test changes;
- no edits to original Atlas/Bridge source JSON files;
- no edits to generated surface slice files unless this pack is explicitly reopened as a slice-pack repair;
- no execution of Atlas implementation leaves;
- no virtual environment creation;
- no roadmap ledger/schema creation unless a later PM brief explicitly opens that gate;
- no candidate scoring or candidate selection unless a later PM brief explicitly opens that gate;
- no vocabulary mutation;
- no planning-compiler code import;
- no Atlas-readiness or repo-wide proof-completion claims.

## Output paths

Planned execution outputs:

- `var/audit/ledgers/atlas_tranche_roadmap_ledger.json`
- `var/audit/ledgers/atlas_tranche_roadmap_ledger.schema.json`
- `var/audit/briefs/2026-04-28_ATLAS_TRANCHE_ROADMAP_CLOSEOUT.md`

Already committed planning surface:

- `var/audit/briefs/2026-04-28_ATLAS_TRANCHE_ROADMAP_PLAN.md`

## Required invariant

The roadmap may plan the migration at coarse level only. Exact implementation leaves must be written only when a single roadmap tranche becomes active.
