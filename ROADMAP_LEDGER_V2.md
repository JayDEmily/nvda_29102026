# ROADMAP_LEDGER_V2 — Live Programme Pointer

## Current authority

| Field | Value |
|---|---|
| Status | `module_architecture_control_integration_validated_awaiting_commit_archive_and_merge` |
| Programme ExecPlan | `project_control/canonical_project_manager/EXEC_PLAN.md` |
| Module-local Gate C protocol | `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md` |
| Accepted architecture report | `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md` |
| Accepted architecture workbook | `project_control/canonical_project_manager/architecture/Atlas_Architecture_Traceability.xlsx` |
| Control-integration baseline | `main` at `0c207f9b71868f82d2abdca6c9091556b5a214c5` |
| Current branch | `control/accept-module-architecture` |
| Current unit | `CTRL-ARCH-001-E` — create the bounded commit and external Git-preserving archive |
| Accepted ownership model | `M00`–`M15`; `M07 coefficient_modifier_authority` |
| Architecture surfaces | 18 accepted surfaces |
| Historical `D-xxx` records | 33 retained as traceability obligations, not a fixed total order |
| Production/source/test mutation | closed on the control-integration branch |
| First implementation module | `M13 state_kernel`, after control integration is accepted and merged |
| Gate D | module-gated; no global opening |

Read the programme ExecPlan first, then the module-local Gate C protocol. This roadmap records current position only. Historical Gate C ledgers, receipts, test dispositions, proof envelopes and Gate D readiness artefacts remain evidence and do not schedule current work.

## Accepted strategy

- The existing repository and Git history remain authoritative; no new repository will be created.
- The four maps are locked as: behavioural spine, 18 architecture surfaces, 16 ownership modules and implementation obligations.
- `M00`–`M15` are accepted target ownership modules; no top-level split or merge is currently required.
- `M07 policy_authority` is superseded by `M07 coefficient_modifier_authority`.
- Runtime/contract, state/transaction, governance/promotion and build/test dependencies are separate planes.
- The target runtime graph is acyclic. `M00` is the composition shell; `M14` and `M15` are governance-plane prerequisites rather than production dependencies.
- Physical package migration is progressive, one active module at a time.
- Global P2–P4 completion is no longer required before implementation.
- Each active module completes a local authority-and-proof gate before source mutation.
- Unrelated unreviewed tests remain `LEGACY_SHADOW_UNADMITTED` and continue to run as shadow evidence where available.
- Existing `D-xxx` identifiers and evidence remain intact, but numbering does not establish implementation order.
- Positive implementation coverage remains to be defined locally for the known gaps in `M07`, `M09`, `M10` and `M11`.

## Preserved historical truth

- P1 `PM-001`–`PM-010` remains accepted prerequisite evidence.
- PM-011 remains the standing 179-test physical census.
- `P2-A01` remains an accepted immutable historical review archive/checkpoint.
- Earlier bulk P2 projections and worker positive-admission proposals remain unaccepted unless reopened under a module-local proof gate.
- Earlier negative adjudications, expected-red tests, Gate B findings, proof envelopes and all 33 `D-xxx` records remain evidence.
- The supplied architecture package contains 287 cohorts and 1,716 records and resolves the previous absence blocker mechanically; behavioural admission remains row-specific.

## Current control-integration gate

| Leaf | State | Exit condition |
|---|---|---|
| `CTRL-ARCH-001-A` | `accepted` | user accepted the extended architecture review |
| `CTRL-ARCH-001-B` | `accepted` | `AGENTS.md`, `PLANS.md`, ExecPlan, Gate C protocol and roadmap agree |
| `CTRL-ARCH-001-C` | `accepted` | architecture report, workbook, machine projection, graph and working blueprint agree |
| `CTRL-ARCH-001-D` | `accepted` | control-only validation passed; no source/test/runtime mutation |
| `CTRL-ARCH-001-E` | `current` | bounded commit, clean checkpoint and Git-preserving archive exist; final evidence is external to avoid self-referential mutation |
| `M13-PROOF` | `closed` | opens only after `CTRL-ARCH-001` is accepted and merged |
| `M13-IMPLEMENT` | `closed` | opens only after the local M13 proof gate issues `IMPLEMENTATION_OPEN` |

## Initial serial module order

1. `M13 state_kernel`
2. `M01 source_admission`
3. `M02 calendar`
4. `M03 preparation`
5. `M04 packet_protocol`
6. `M07 coefficient_modifier_authority`
7. `M08 playbook_catalogue`
8. `M05 serial_cognition`
9. `M06 parallel_risk`
10. `M09 capital_authority`
11. `M10 execution_gateway`
12. `M11 portfolio_lifecycle`
13. `M12 evidence_replay`
14. `M00 application_shell`

`M05` and `M06` may be reversed when both are dependency-ready, but only one mutating module remains open.

`M14 proof_promotion` and `M15 vocabulary_governance` apply continuously and are not runtime implementation stages.

## Mutation boundary

During `CTRL-ARCH-001`, allowed changes are limited to:

- `AGENTS.md` and `PLANS.md`, explicitly opened by the user;
- `ROADMAP_LEDGER.md` only to replace its stale successor placeholder with the live pointer;
- `ROADMAP_LEDGER_V2.md`;
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`;
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`;
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`;
- `docs/vocabulary/vocabulary_registry.md` and the deterministic `data/vocabulary/canonical_vocabulary.json` projection for accepted durable control terms;
- `project_control/canonical_project_manager/**`.

Forbidden during this unit:

- `src/**`;
- tests or test support;
- production configuration, schemas, fixtures or migrations;
- package migration;
- implementation of `M13` or any other module;
- merge, push or publication.

## Next gate

Create the bounded control-integration commit and validated Git-preserving archive. After user/Project Manager acceptance and merge to `main`, open `M13-PROOF`.
