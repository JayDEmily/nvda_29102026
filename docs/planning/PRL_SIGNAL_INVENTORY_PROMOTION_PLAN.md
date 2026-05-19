# Parallel Risk Lane signal inventory typed-promotion plan

Status: planning artefact for `PRL-MRP-008`.

## Decision

The future workbook tab `Parallel Risk Lane Signal Inventory` is governance/reference material. Runtime PRL code must consume only a typed promotion artefact:

`config/parallel_risk_signal_inventory.v1.yaml`

Future contracts:

- `ParallelRiskSignalInventoryDocument`
- `ParallelRiskExpectedSignalRecord`

## Lawful path

`Parallel Risk Lane Signal Inventory` workbook tab -> promotion/export process with workbook lineage -> `config/parallel_risk_signal_inventory.v1.yaml` -> typed contracts -> PRL missing/unavailable-signal helpers -> `ParallelRiskMinuteProfile`

## Required promoted fields

| Field | Purpose |
|---|---|
| `inventory_version` | Version of promoted inventory. |
| `source_workbook_path` | Governance workbook path. |
| `source_workbook_sheet` | `Parallel Risk Lane Signal Inventory`. |
| `source_workbook_fingerprint` | Workbook hash at promotion time. |
| `records[].signal_id` | Runtime-facing signal ID. |
| `records[].signal_family` | PRL family. |
| `records[].inventory_status` | available_now/upstream_but_not_projected/missing/deferred/excluded. |
| `records[].runtime_contract_target` | Expected typed carrier. |
| `records[].lawful_prl_use` | Whether PRL may consume the promoted signal. |
| `records[].workbook_lineage_refs` | Raw/derived workbook lineage refs. |
| `records[].missing_impact` | Missing-signal impact classification. |

## Non-goals

- Do not create the YAML file until the workbook tab exists.
- Do not read the workbook at runtime.
- Do not fabricate values for unavailable signal families.
- Do not add rich signal implementations.

## Risk semantics

Promotion records describe expected signal availability and evidence quality. They do not decide whether to trade and do not convert unavailable signals into defensive warnings.
