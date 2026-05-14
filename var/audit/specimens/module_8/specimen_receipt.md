# Module 8 workbook-derived specimen receipt

## Classification

This is a governed workbook-derived specimen. It is not a live admitted raw bundle and not direct runtime authority.

## Workbook source

- workbook path: `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`
- primary row surface: `Anchor_Data!A7:AE7`
- exact sheet names used: `Anchor_Data`, `Live_Web_Baseline`

## Exact cells / rows used

- `Anchor_Data!A7:AE7`
- `Anchor_Data!A7`
- `Anchor_Data!B7`
- `Anchor_Data!G7`
- `Anchor_Data!M7`
- `Anchor_Data!AE7`
- `Live_Web_Baseline!B6:C6`
- `Live_Web_Baseline!B9:C9`
- `Live_Web_Baseline!B16:C16`

## Fields mapped directly

- `temporal.source_date` <- `Anchor_Data!A7` with anchor-row date only and field-level provenance preserved via `Anchor_Data!A7`
- `regime.vix_level` <- `Anchor_Data!M7` with field-level provenance `Live_Web_Baseline!B9:C9`
- `options_flow.spot_price` <- `Anchor_Data!B7` with field-level provenance `Live_Web_Baseline!B6:C6`

## Fields left missing explicitly

- `temporal.source_time_raw` = `null`
- `temporal.next_event_time_utc` = `null`
- `temporal.windows` = `[]`
- `regime.nvda_return_pct` = `null`
- `regime.nq_return_pct` = `null`
- `options_flow.front_dte` = `null`
- `options_flow.next_dte` = `null`

No exact raw workbook time token was preserved on the workbook promotion path inspected here, so `temporal.source_time_raw` remains `null` rather than being fabricated from `source_date`.

The workbook event flag at `Anchor_Data!AE7` was not promoted into `next_event_time_utc` or event windows because no lawful timestamped event record is present on the inspected workbook surfaces.

## Provenance rule preserved

- `Anchor_Data` row 7 is the primary mapping surface.
- `Anchor_Data!A7` is used as the anchor-row date only.
- `Live_Web_Baseline` field dates remain field-level provenance.
- Mixed-date workbook fields were not collapsed into one fake live observation timestamp.
- Packet emission time and persistence time were kept separate from workbook source-date provenance.

## Deterministic artefacts written

- stage input bundle JSON: `var/audit/specimens/module_8/stage_input_bundle.json`
- bootstrap input DMPV3 packet JSON: `var/audit/specimens/module_8/bootstrap_input_packet.json`
- Stage A output DMPV3 packet JSON: `var/audit/specimens/module_8/stage_a_output_packet.json`
- append-only observation record JSON: `var/audit/specimens/module_8/append_only_observation_record.json`
