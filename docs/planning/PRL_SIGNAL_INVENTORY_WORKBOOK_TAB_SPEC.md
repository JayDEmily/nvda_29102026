# Parallel Risk Lane Signal Inventory workbook-tab specification

Status: planning artefact for `PRL-MRP-006`.

## Purpose

The expected-signal inventory for the Parallel Risk Lane belongs in the governed Excel signal workbook, not in an isolated code constant and not in a free-floating Markdown table.

Future workbook tab name:

`Parallel Risk Lane Signal Inventory`

Known workbook path:

`data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`

Existing raw-signal / raw-primitives sheet:

`Raw_Primitives_Catalog`

## Runtime boundary

This specification does not authorise runtime workbook reads. The lawful data path remains:

`workbook/reference doctrine -> typed promotion artefact with workbook lineage -> config/contracts -> runtime PRL input -> RiskAtomState / SignalSnapshotEntry / registers -> ParallelRiskMinuteProfile`

## Required future columns

| Column | Purpose |
|---|---|
| `signal_id` | Stable runtime-facing signal identifier. |
| `signal_family` | PRL risk/signal family. |
| `inventory_status` | One of available_now, upstream_but_not_projected, missing, deferred, excluded. |
| `raw_workbook_lineage_ref` | Link to raw/primitives source sheet/cell/range where available. |
| `derived_workbook_lineage_ref` | Link to derived feature source sheet/cell/range where available. |
| `runtime_contract_target` | Future typed config/contract carrier, if known. |
| `lawful_prl_use` | Whether PRL may consume the typed promoted signal. |
| `missing_handling` | How absence should affect confidence/atom availability. |
| `unavailable_handling` | How unavailable future signals are represented without fabricated values. |
| `exclusion_reason` | Required when status is excluded. |
| `notes` | Governance notes only, no trade advice. |

## Required statuses

- `available_now`: already present in typed runtime PRL input or lawful signal snapshot.
- `upstream_but_not_projected`: exists upstream but not yet projected into PRL.
- `missing`: expected for PRL but currently absent.
- `deferred`: future rich signal family lacking typed runtime source.
- `excluded`: outside PRL authority, for example trade action, capital sizing, order instruction, review judgement, or direct workbook runtime read.

## Risk semantics

Inventory status is neutral state-of-play metadata. It supports constructive, defensive, ambiguous, mixed, and consequence-side risk descriptions by making signal availability explicit. It must not imply buy/sell/fade/chase/hedge/size/avoid actions.

## Non-goals for this leaf

- Do not edit the Excel workbook.
- Do not create the new tab yet.
- Do not create runtime config promotion yet.
- Do not make PRL read the workbook directly.
