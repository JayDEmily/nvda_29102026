# Atlas Tranche Roadmap Plan

Status: planned; execution not started.

## Purpose

Create a coarse Atlas migration roadmap from the materialised `blueprint_surface` slice pack.

The roadmap is required before opening the next Atlas implementation tranche because the slice pack contains 18 native architecture surfaces and 1716 Atlas records. Future work must not return to full-batch Atlas processing for ordinary implementation planning.

## Authority and inputs

Mandatory inputs:

- `AGENTS.md`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `intent_migration/atlas_tranche_roadmap/AGENTS.override.md`
- `var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json`
- `var/audit/atlas_surface_slices/atlas_surface_slice_checksums.json`

Retained evidence only:

- original Atlas/Bridge JSON files under `var/audit/imports/atlas_bridge_inputs/`
- native Bridge ledger under `var/audit/ledgers/intent_migration/`

The materialised slice files are the ordinary planning input. The original giant JSON files are not reread unless the slice pack checksum or join truth is challenged.

## Planning rule

The roadmap plans all Atlas migration at coarse level.

It must not pre-author exact implementation leaves for every surface.

Exact leaves are created only when a single roadmap tranche becomes active and its local code/test/control surfaces have been read.

## Known slice inventory

The current slice manifest records 18 `blueprint_surface` slices and 1716 records.

| Surface | Slice name | Records | Initial roadmap posture |
|---|---:|---:|---|
| External source interfaces and API ingress | `external_source_interfaces_and_api_ingress` | 234 | split required |
| Dynamic coefficient and modifier authority | `dynamic_coefficient_and_modifier_authority` | 193 | split required |
| Review and explanation layer | `review_and_explanation_layer` | 143 | split likely |
| Serial desk-cognition spine | `serial_desk_cognition_spine` | 139 | split likely |
| Raw signal families | `raw_signal_families` | 123 | split likely |
| Financial and event calendar architecture | `financial_and_event_calendar_architecture` | 117 | split likely |
| Raw capture and source temporal law | `raw_capture_and_source_temporal_law` | 108 | split likely |
| Persistence, ledgers, and receipts | `persistence_ledgers_and_receipts` | 97 | split maybe |
| Playbook library architecture | `playbook_library_architecture` | 95 | split maybe |
| Exit and close architecture | `exit_and_close_architecture` | 90 | split maybe |
| Opening architecture and placement readiness | `opening_architecture_and_placement_readiness` | 74 | one or two tranches |
| DMPV3 packet carriage | `dmpv3_packet_carriage` | 73 | one or two tranches |
| Testing, proof, and checkpoint surfaces | `testing_proof_and_checkpoint_surfaces` | 72 | one or two tranches |
| Parallel risk lane | `parallel_risk_lane` | 57 | one tranche likely |
| Prepared ingress and runtime context preparation | `prepared_ingress_and_runtime_context_preparation` | 51 | one tranche likely |
| Live position and inventory architecture | `live_position_and_inventory_architecture` | 38 | one tranche likely |
| Vocabulary governance interface | `vocabulary_governance_interface` | 10 | one tranche likely |
| Downstream capital deployment authority | `downstream_capital_deployment_authority` | 2 | already piloted; no new roadmap implementation tranche until carry-forward blockers are separately routed |

## Roadmap split heuristic

Use the following starting heuristic and adjust only when slice content proves a different split is safer:

- 1 to 60 records: usually one tranche;
- 61 to 100 records: one or two tranches depending on blueprint/test split;
- 101 to 150 records: two or three tranches;
- 151 to 220 records: three or four tranches;
- more than 220 records: at least four tranches.

A tranche may be smaller than the heuristic when:

- blueprint-first work must precede test-first work;
- existing tests are presence-only or registry-uncertain;
- the surface crosses multiple owned modules;
- a prior pilot has already closed part of the surface;
- runtime verification risk is high.

## Planned roadmap leaves

### ROADMAP-L01 — Build roadmap ledger

Create `var/audit/ledgers/atlas_tranche_roadmap_ledger.json` and schema from the 18 materialised slice records.

The ledger must include, for each proposed roadmap tranche:

- tranche id;
- source `blueprint_surface`;
- source slice path;
- record count range or exact included record count;
- satisfaction-state summary;
- implementation-leaf-type summary;
- likely phase: blueprint-first, test-first, code-conformance, or closeout-only;
- dependency notes;
- risk notes;
- status.

### ROADMAP-L02 — Select first implementation candidate

Select exactly one next implementation-tranche candidate from the roadmap.

The selection must prefer:

- small blast radius;
- governance or proof leverage;
- clear active-code mapping;
- low risk of reopening large Atlas files;
- no dependency on unresolved runtime-health blockers.

The candidate is expected, but not pre-committed, to be `Vocabulary governance interface` unless the roadmap ledger proves another surface is safer.

### ROADMAP-L03 — Closeout

Close the roadmap pack only after:

- route surfaces agree;
- roadmap ledger and schema parse;
- total planned source records reconcile to 1716 or explicitly exclude records already closed by prior tranche evidence;
- no runtime code or tests were changed;
- no implementation leaves were opened;
- next implementation candidate is recorded as candidate only, not executed.

## Non-goals

This plan does not:

- execute any Atlas implementation tranche;
- refactor runtime code;
- modify tests;
- change original Atlas/Bridge JSON files;
- claim final exact leaf lists for all future tranches.

## Pass condition for executing this plan

A future agent can choose the next single Atlas implementation tranche by reading a small roadmap ledger and the selected surface slice, without loading the giant Atlas/Bridge JSON files or guessing from memory.
