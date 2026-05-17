# Phase 2 — consolidated service rebuild map

Status: `completed_planning_no_implementation`

Scope: **310** missing-behaviour clauses = 190 confirmed not-survived full intents + 120 partial missing deltas.

Deduplication rule: rebuild one native capability family per canonical review group and assigned owner surface. Do not rebuild per Atlas row.

## Owner service summary

| forward_id | architecture_row | owner_surface | total_missing_clauses | partial_delta_clauses | confirmed_deleted_clauses | canonical_groups |
| --- | --- | --- | --- | --- | --- | --- |
| FWD-001 | 5.18 | Vocabulary governance interface | 1 | 1 | 0 | CRG-017 |
| FWD-002 | 5.17 | Testing, proof, and checkpoint surfaces | 68 | 12 | 56 | CRG-002; CRG-003; CRG-009 |
| FWD-003 | 5.16 | Persistence, ledgers, and receipts | 54 | 3 | 51 | CRG-007; CRG-008 |
| FWD-005 | 5.1 | External source interfaces and API ingress | 30 | 27 | 3 | CRG-014; CRG-015 |
| FWD-007 | 5.3 | Raw signal families | 56 | 24 | 32 | CRG-001; CRG-012 |
| FWD-008 | 5.4 | Financial and event calendar architecture | 11 | 11 | 0 | CRG-006 |
| FWD-010 | 5.9 | Dynamic coefficient and modifier authority | 12 | 12 | 0 | CRG-011 |
| FWD-013 | 5.8 | Parallel risk lane | 8 | 5 | 3 | CRG-013 |
| FWD-015 | 5.12 | Opening architecture and placement readiness | 13 | 11 | 2 | CRG-005 |
| FWD-016 | 5.13 | Live position and inventory architecture | 2 | 0 | 2 | CRG-016 |
| FWD-017 | 5.14 | Exit and close architecture | 25 | 5 | 20 | CRG-004 |
| FWD-018 | 5.15 | Review and explanation layer | 30 | 9 | 21 | CRG-002; CRG-010 |

## Canonical review group dedup map

| canonical_group_id | canonical_review_group | total_clauses | partial_delta_clauses | confirmed_deleted_clauses | assigned_owner_surfaces |
| --- | --- | --- | --- | --- | --- |
| CRG-001 | Strategic ladder signal family and SLV market scoring | 32 | 0 | 32 | Raw signal families |
| CRG-002 | SLV replay, walk-forward, fragility, horizon, and experiment harness | 54 | 2 | 52 | Review and explanation layer; Testing, proof, and checkpoint surfaces |
| CRG-003 | Research notes, promotion decisions, and evaluation sidecar APIs | 11 | 5 | 6 | Testing, proof, and checkpoint surfaces |
| CRG-004 | Overnight carry market/replay and exit-continuation machinery | 25 | 5 | 20 | Exit and close architecture |
| CRG-005 | Broker execution lifecycle, account state, and typed order domain | 13 | 11 | 2 | Opening architecture and placement readiness |
| CRG-006 | Runtime financial/event calendar authority and proximity queries | 11 | 11 | 0 | Financial and event calendar architecture |
| CRG-007 | Canonical import registry schema, service, reports, and backlog views | 34 | 0 | 34 | Persistence, ledgers, and receipts |
| CRG-008 | Durable SQL/ORM persistence, DB factory, and seed data | 20 | 3 | 17 | Persistence, ledgers, and receipts |
| CRG-009 | Legacy fixture corpus loaders and row parsers | 16 | 7 | 9 | Testing, proof, and checkpoint surfaces |
| CRG-010 | Review packet daily health, module health, rendering, and reporting | 17 | 7 | 10 | Review and explanation layer |
| CRG-011 | Dynamic coefficient calibration, audit packets, and active replay harness | 12 | 12 | 0 | Dynamic coefficient and modifier authority |
| CRG-012 | Rich raw market substrate and signal service surfaces | 24 | 24 | 0 | Raw signal families |
| CRG-013 | Parallel risk candidate enrichment, consequence/fragility classes, and risk event APIs | 8 | 5 | 3 | Parallel risk lane |
| CRG-014 | API exposure for live internal mechanisms | 26 | 23 | 3 | External source interfaces and API ingress |
| CRG-015 | Authority/veto and block-event API surfaces | 4 | 4 | 0 | External source interfaces and API ingress |
| CRG-016 | Daily PnL reporting surface | 2 | 0 | 2 | Live position and inventory architecture |
| CRG-017 | Vocabulary document strict-extra-field enforcement | 1 | 1 | 0 | Vocabulary governance interface |

CSV details:

- `PHASE_2_CONSOLIDATED_REBUILD_SERVICE_MAP_310.csv`
- `PHASE_2_SERVICE_SUMMARY_BY_OWNER.csv`
- `PHASE_2_CANONICAL_GROUP_SERVICE_DEDUP_MAP_17.csv`
