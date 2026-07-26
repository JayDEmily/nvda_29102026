# ROADMAP_LEDGER_V2 — Live Programme Pointer

## Current authority

| Field | Value |
|---|---|
| Status | `m13_proof_accepted_implementation_open` |
| Programme ExecPlan | `project_control/canonical_project_manager/EXEC_PLAN.md` |
| Module-local Gate C protocol | `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md` |
| Accepted architecture report | `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md` |
| Accepted architecture workbook | `project_control/canonical_project_manager/architecture/Atlas_Architecture_Traceability.xlsx` |
| Control-integration baseline | fast-forwarded to `main` at `b153cd1e3e0808991dcf9c188e380d935cfd9283` |
| Current branch | `review/m13-proof-v6` |
| Current unit | `M13-IMPLEMENT` open; implement the accepted non-durable alpha `state_kernel` against the frozen 46-case proof family |
| Original M13 proof checkpoint | `5f672ddf5a712a3446bada00ebcbbf1d7c0f321c`; independently rejected for receipt-write atomicity gap |
| M13 proof-repair commit | `2dd25e3bdf5759fcaa2320cfd5bba988f9908eee` |
| M13 proof-repair V2 commit | `7b3b04c4647ee13674e46c55227b5352cb8c8361` |
| M13 proof-repair V3 commit | `6ef6e448e28cd96138c0aaeb3d8f8334cad55eb1` |
| M13 proof-repair V4 commit | `31e8ac38488466d1d457f98ffe014576423a5ebf` |
| M13 V2 review source | `proof/m13-state-kernel-repair-v2` at `e59b8bdfb5d1e34944aa1b661643c8e6570b940c` |
| Accepted ownership model | `M00`–`M15`; `M07 coefficient_modifier_authority` |
| Architecture surfaces | 18 accepted surfaces |
| Historical `D-xxx` records | 33 retained as traceability obligations, not a fixed total order |
| Production/source mutation | open only for the bounded `src/nvda_desk/m13_state_kernel/**` implementation on the next worker branch; tests, normative authority, proof configuration and later modules remain closed |
| First implementation module | `M13 state_kernel`; independent proof accepted and bounded implementation now open |
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
| `CTRL-ARCH-001-E` | `accepted` | integration commit `9ec838a45bd4cf98313e83f73f47d376b1e42806` and archive `NVDA_MODULE_ARCHITECTURE_CONTROL_INTEGRATION_9ec838a_20260725.tar.gz` (`faa6d2e196923bcd1641b1616c2fb8bfb3cf0900e4972642b79e2943333d5d5b`) verified clean after extraction |
| `CTRL-ARCH-001-MERGE` | `accepted` | fast-forward merge to local `main` at `b153cd1e3e0808991dcf9c188e380d935cfd9283` |
| `M13-PROOF-A/T` | `historical_partial_proof_preserved` | original nine lawful behaviours remain unchanged but were independently found insufficient for receipt-write/repository-participant atomicity |
| `M13-PROOF-PM1` | `closed_atomicity_false_positive` | user-supplied independent PM decision reproduced: commit-before-receipt mutant passes original 9/9 and leaves committed state without receipt |
| `M13-PROOF-REPAIR-P/T` | `completed_pending_independent_acceptance` | two participant/receipt-failure tests added; conforming reference 11/11; PM mutant and no-participant-rollback mutant rejected |
| `M13-PROOF-V2-RECOVERY` | `closed_prepare_failure_false_positive` | reconstructed independent decision: all eleven tests pass a coordinator that omits rollback of the participant that raises during `prepare()`, leaving stale pending state and poisoning identical retry |
| `M13-PROOF-REPAIR-V2` | `independent_pm_closed_prior_prepared_participant_gap` | a rollback-only-current-participant coordinator passes 12/12 while an earlier successfully prepared participant retains pending state when a later participant fails during `prepare()` |
| `M13-PROOF-REPAIR-V3` | `independent_pm_closed_failed_idempotency_binding_gap` | thirteen-test family rejects the prior rollback mutant but allows a failed transaction to reserve the scoped idempotency key and block a different uncommitted input |
| `M13-PROOF-REPAIR-V4` | `independent_pm_closed_mutation_failure_binding_gap` | fourteen-test family rejects participant-failure reservation but permits mutation-failure-only reservation of the same uncommitted key |
| `M13-PROOF-REPAIR-V5` | `independent_pm_accepted` | fourteen frozen functions preserved; 32-case failure/binding matrix accepted; conforming 46/46; PM V5, configurable and earlier mutants rejected |
| `M13-IMPLEMENT` | `IMPLEMENTATION_OPEN` | bounded non-durable alpha state-kernel implementation only; must return for independent PM implementation review |

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

During `M13-PROOF`, allowed changes were limited to:

- the M13 module-local proof record and raw validation evidence;
- one M13 Tier A contract test;
- retained-test and proof-block admission records;
- exact M13 durable vocabulary admissions and deterministic projection;
- the live ExecPlan, protocol, roadmap, validation log and read manifest.

Forbidden and not performed:

- `src/**`;
- production implementation or package creation;
- unrelated test repair;
- weakening N-06 transaction law;
- claiming durability, restart recovery or external-effect completion;
- push or publication.

## Next gate

`M13-PROOF-REPAIR-V5` is independently accepted. The frozen authoritative proof now contains 46 semantic items: fourteen preserved tests plus a 32-case matrix spanning eight admitted unsuccessful boundaries and four independently varied identity dimensions. The conforming reference passes 46/46; both PM V5 false positives, all 32 configurable failed-binding mutants and all 11 earlier retained mutants are rejected for their intended reasons.

The next lawful unit is `M13-IMPLEMENT` only. Implement the accepted public seam in `src/nvda_desk/m13_state_kernel/**` as a deliberately non-durable in-memory alpha kernel. Do not alter the frozen proof, normative authority, proof configuration, unrelated persistence code or later modules. The implementation must make the 46-case family green, preserve all shadow evidence, complete mutation and architecture validation, record exact evidence, commit and produce one Git-preserving checkpoint for independent PM review. M01 remains closed.
