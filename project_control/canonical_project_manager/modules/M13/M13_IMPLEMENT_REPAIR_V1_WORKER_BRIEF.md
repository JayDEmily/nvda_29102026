# M13 Implementation Repair V1 — Worker Brief

## Source checkpoint

Use the Project Manager implementation-repair-open checkpoint supplied with this brief as the sole repository input.

Verify its stated archive SHA-256, branch, commit, clean worktree, complete `.git` history and frozen M13 proof-file SHA-256 before changing anything.

Create branch:

`work/m13-state-kernel-implementation-repair-v1`

## Role and question

Act only as the M13 implementation-repair worker.

Answer one question:

> Can the frozen four-file M13 implementation be minimally repaired so that it passes the complete accepted 152-case M13 proof while preserving N-06 ownership, atomicity, idempotency, rollback, sequence, replay and non-durable boundaries?

Complete this bounded unit uninterruptedly through implementation, proof, mutation, shadow, record, Git and fresh-checkpoint validation.

## Required reading

Read in full:

1. `00_TASK/PROJECT_EXECUTION_METHOD.md`
2. `AGENTS.md`
3. `PLANS.md`
4. `tests/AGENTS.override.md`
5. `project_control/canonical_project_manager/EXEC_PLAN.md`
6. `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`
7. `ROADMAP_LEDGER_V2.md`
8. `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md`
9. the N-06 decision;
10. the complete M13 proof record;
11. `M13_IMPLEMENTATION_PM_REVIEW_V1.md`;
12. `M13_PROOF_PM_REVIEW_V6.md`;
13. `M13_PROOF_PM_REVIEW_V7.md`;
14. the complete frozen 152-case proof file;
15. the complete four-file rejected implementation;
16. all V6/V7 conforming references, PM probes and retained mutant summaries;
17. the previous M13 implementation worker record and brief.

## Allowed changes

Production changes are limited to:

- `src/nvda_desk/m13_state_kernel/__init__.py`
- `src/nvda_desk/m13_state_kernel/contracts.py`
- `src/nvda_desk/m13_state_kernel/ports.py`
- `src/nvda_desk/m13_state_kernel/in_memory.py`

Modify only files required by the smallest lawful repair.

Worker-owned records/evidence may be added under the existing M13 module-control and raw-validation surfaces.

## Forbidden changes

Do not:

- modify any test or test parameter;
- modify normative documents;
- modify proof-block or retained-test configuration;
- alter unrelated source, persistence code or later modules;
- broaden M13 into domain-state ownership;
- claim thread safety, process durability, restart recovery, distributed transactions or external-effect completion;
- merge to `main`;
- begin M01;
- self-accept M13.

## Repair leaf 1 — instance-owned active-attempt exclusion

Repair `InMemoryUnitOfWork` so that:

1. active-attempt state belongs to one instance only;
2. same-instance nested `execute()` is rejected before nested mutation or participant work;
3. the guard is installed before any caller- or participant-controlled callback can run;
4. the guard remains installed through participant prepare, commit and rollback completion;
5. the guard clears after every terminal success or failure through a reliable `finally` path;
6. duplicate replay and validation failures do not leave active residue;
7. distinct instances remain independently executable even when command type and consistency-unit strings match;
8. no process-, module-, class- or scope-global guard is introduced.

Do not weaken idempotency or optimistic-version behaviour to implement the guard.

## Repair leaf 2 — coherent `AtomicReceipt`

Repair the public receipt contract so that:

1. `command_type` equals `idempotency_key.command_type`;
2. `consistency_unit_id` equals `idempotency_key.consistency_unit_id`;
3. `prior_state_version` is an exact non-negative `int`, excluding `bool`;
4. `resulting_state_version` is an exact positive `int`, excluding `bool`, and equals prior plus one;
5. `sequence` is an exact positive `int`, excluding `bool`;
6. all existing required identity fields remain non-empty;
7. duplicate replay preserves every committed receipt truth field except the explicit replay indicator;
8. no new identifier grammar or domain policy is invented.

## Repair leaf 3 — preserve prior M13 truth

The repair must preserve:

- scoped idempotency and semantic-input conflict handling;
- expected-version rejection;
- state-plus-receipt atomic publication;
- rollback of every prepared or partially prepared participant;
- no binding on any failed attempt;
- deterministic committed version and sequence;
- detached state and receipt readbacks;
- exact duplicate replay without mutation;
- explicitly `non_durable_in_memory` status;
- no hidden domain ownership.

## Required proof and falsification

1. Prove the frozen test file is byte-for-byte unchanged from the PM checkpoint.
2. Run the complete M13 family: 152/152 must pass.
3. Run all eight V7 over-broad-guard mutants: each must remain rejected by its intended case.
4. Run all 16 V6 mutants.
5. Run all earlier retained M13 mutants, both PM V5 mutants, all 32 V5 configurable mutants and all eight previous implementation-derived mutants.
6. Add at least six implementation-derived repair mutants covering:
   - no active guard;
   - module-global guard;
   - guard installed after mutation begins;
   - guard cleared before participant commit;
   - receipt scope checks only one dimension;
   - resulting version accepts float/bool.
7. For each new mutant, require full and designated targeted rejection for the intended semantic reason.
8. Do not count interface errors, import failures or unrelated broken success paths as mutant rejection.

## Required validation

Run and retain exact commands, exit codes and unedited output for:

- complete 152-case M13 proof;
- complete persistence Tier A;
- proof blocks;
- proof executor;
- checkpoint shadow;
- affected architecture-boundary tests;
- relevant vocabulary parity;
- YAML parsing;
- Python compilation;
- Ruff and Black checks where configured;
- `git diff --check`;
- changed-path validation;
- complete repository shadow suite with comparison to the accepted PM baseline.

Unrelated existing shadow failures are evidence, not automatic repair authority.

## Records

Update only worker-owned M13 implementation records and raw evidence.

Record:

- exact source changes and rationale;
- proof-to-source mapping;
- guard lifecycle and ownership;
- receipt invariant mapping;
- all proof and mutant results;
- shadow comparison;
- changed paths;
- final branch, commit and hashes;
- archive SHA-256 and fresh-extraction rerun.

Label the result exactly:

`PROPOSED_M13_IMPLEMENTATION_REPAIR_V1_AWAITING_INDEPENDENT_PROJECT_MANAGER_REVIEW`

## Git and checkpoint

Commit only the bounded implementation repair and worker-owned evidence.

Create exactly one Git-preserving archive outside the repository. Verify through fresh extraction:

- branch;
- commit;
- clean worktree;
- frozen proof hash;
- complete 152-case pass;
- representative mutant from every repair class;
- evidence integrity;
- complete `.git` history.

Return one archive only with SHA-256 stated inline.

End with:

`READY_FOR_INDEPENDENT_PM_IMPLEMENTATION_REVIEW`
