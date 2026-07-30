# ROADMAP_LEDGER_V2 — Live Canonical Programme Pointer

## Current state

| Field | Value |
|---|---|
| Status | `m04_k07_mlc_p_active_after_disposition` |
| Current programme | existing canonical M00–M15 module-local delivery programme |
| Current branch | `control/atlas-current-path-rebase-gate-c-continuation-v1` from `integration/parallel-cycle-01` at `73f1e7ab3ce212c9951f03c407e94741e6c68913` |
| Accepted launch checkpoint | `review/parallel-control-r2-accepted` / `ee67c752d14073a959fda478f31f4466b6952cae` |
| Integrated Cycle 01 state | through PM Lane 4 acceptance `d6cfff9ab00cb5772baad26b14a8d388b08a241a` |
| Aggregate closeout | `project_control/canonical_project_manager/parallel_cycle_01_closeout/CYCLE_01_PM_AGGREGATE_CLOSEOUT.md` |
| Aggregate mechanical evidence | `project_control/canonical_project_manager/parallel_cycle_01_closeout/CYCLE_01_AGGREGATE_MECHANICAL_VALIDATION.txt` — 28 PASS, 0 FAIL |
| Parallel operating law | `project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md` |
| Workflow registry | `project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md` |
| Cycle 1 brief pack | `project_control/canonical_project_manager/PARALLEL_CYCLE_01/` |
| Completed control unit | Atlas current-governing-document repair passed at `27fa427` |
| Completed Gate C leaf | M04 K07 section 9.10 added; M04 MLC-A recheck `AUTHORITY_SUFFICIENT` |
| Completed Gate C routing leaf | `M04-PROOF-MLC-R-V1` — 25 physical K07 claim files routed; 154 other census files remain `LEGACY_SHADOW_UNADMITTED` |
| Completed governance prerequisite | `M15-VOCABULARY-NAMESPACE-REPAIR-V1` — namespaced machine identities and 95-file M04 scoped candidate audit passed |
| Completed observation leaf | `M04-PROOF-MLC-O-V1` — 25 files read; 357 tests observed as 347 passed / 10 failed |
| Completed disposition leaf | `M04-PROOF-MLC-D-V1` — one bounded expected-red admission; all other files partial, contradictory, consumer-only or unlisted-role evidence |
| Current control leaf | `M04-PROOF-MLC-P-V1` — exact K07 proof specification |
| Validation records | existing architecture `Validation_Receipt.md` for the Atlas repair and existing PM `VALIDATION_LOG.md` for M15 |
| Production/source mutation | closed |
| Physical-test mutation | closed |
| Implementation | closed; no implementation opens from the trace repair or the next normative leaf |

Read the ExecPlan, Gate C protocol, parallel operating law and workflow registry before issuing any new assignment.

## Parallel Cycle 01 closeout

| Assignment | Unit | PM state | Bounded outcome |
|---|---|---|---|
| `1A` | `M01-PROOF-MLC-R-V1` | `AGGREGATE_VALIDATED_CLOSED` | 179 unique physical tests reconciled; 20 current M01 claim routes and 159 bounded M01 shadows |
| `2A` | `M04-PROOF-MLC-A-V1` | `AGGREGATE_VALIDATED_CLOSED` | `BLOCKED_MISSING_NORMATIVE_AUTHORITY` for the complete K07 packet-role matrix |
| `3A` | `M07-PROOF-MLC-A-V1` | `AGGREGATE_VALIDATED_CLOSED` | `BLOCKED_MISSING_NORMATIVE_AUTHORITY` for K12 bundle/application authority; `OBL-M07-POSITIVE` remains open |
| `4A` | `M08-PROOF-MLC-A-V1` | `AGGREGATE_VALIDATED_CLOSED` | `BLOCKED_MISSING_NORMATIVE_AUTHORITY` for K13 catalogue/eligibility decision authority |
| 5 | held | `HELD_BLOCKED_DEPENDENCY` | no new assignment allocated |
| 6 | held | `HELD_BLOCKED_DEPENDENCY` | no new assignment allocated |

## Dependency and return gates

1. M01 routing is accepted, but `M01-PROOF-MLC-O-V1` remains queued behind the sole current M04 leaf.
2. M04 K07 numbered authority, MLC-A, MLC-R, MLC-O, MLC-D and the bounded M15 namespace/scoped-audit prerequisite are complete. M04 MLC-P proof specification is active.
3. M07 requires one bounded numbered normative proposition defining K12 identity/version, precedence/conflict, hard-bound and deterministic application/receipt semantics before MLC-A can close.
4. M08 requires one bounded numbered normative proposition defining K13 identities, mandatory inputs, deterministic ordering/tie-break/lead selection, stand-down states and lawful lifecycle carriage before MLC-A can close.
5. M02 remains downstream of canonical M01 contracts; the remaining dependency waves are unchanged.
6. Lanes 5 and 6 remain held until the PM allocates dependency-ready and non-overlapping semantic units.

## Immediate next gate

Execute `M04-PROOF-MLC-P-V1`: specify the complete ten-role proof family, R/C/O/N lineage matrix, named validation facts, lawful outcomes, contradiction checks and false-positive mutants. Do not mutate physical tests, fixtures, runtime configuration or production source.

M07 K12, M08 K13 and M01 MLC-O remain queued; behavioural test mutation and production implementation remain closed until their own preceding Gate C leaves pass.
