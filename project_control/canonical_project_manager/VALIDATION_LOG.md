# Canonical Project Manager Validation Log

## PM-000 — Programme-control activation

### Baseline evidence

| Check | Observed result |
|---|---|
| Governed archive SHA-256 | `5a75fb237232d9b6a8bc804a81c6bc62c9ad7a719fee57346d632b39a060857c` |
| Baseline branch | `work/NVIDIA_2026_normative_authority_top_down_alignment_20260717` |
| Baseline commit | `f7bd3f46862fe9b33340f3f13951518795724fe7` |
| Baseline commit timestamp | `2026-07-20T08:17:46Z` |
| Baseline subject | `Decide bounded Gate D readiness` |
| Baseline status | Clean before PM branch creation |
| Baseline tracked files | 1,047 |
| PM working branch | `work/NVIDIA_2026_canonical_project_manager_20260720` |

### Read and inventory checks

- Root and subtree instruction files were discovered and semantically read in full.
- Root control placeholders/tombstone, the prior active plan, routing index, numbered normative corpus, vocabulary authority, normative-completion decisions N-01 through N-09, proof registers, all thirty-three proof-envelope files, and Gate D readiness evidence were semantically read in full.
- All 166 Tier A and all 13 Tier B Python test files were semantically read in full, together with `tests/AGENTS.override.md`, test support files, fixtures, the retained registry, proof blocks, and exercised runtime/configuration owners.
- All 203 Python files under `src/nvda_desk` were semantically read in full.
- Physical-to-retained inventory comparison produced 166/120 Tier A with 46 unlisted physical files and 13/13 Tier B with no difference.
- Live vocabulary recount produced 46 human headings, 87 generated entries, 26 normalised matches, 20 human-only labels, and 61 generated-only labels.
- Historical Git object verification at `f26b09f` reproduced the four Atlas source hashes and the eighteen-surface/1,716-record manifest counts recorded in the retained vocabulary slice.
- No 287-row cohort-register artefact was found in the supplied archives, live tree, or inspected reachable named paths. This remains a blocker rather than a negative proof that it never existed.

### Pytest environment attempts

1. `env PYTHONPATH=src python -m pytest ...` did not execute tests because the available Python 3.12 runtime had no `pytest` module.
2. `uv run --frozen pytest ...` could not initialise its default cache because `/root/.cache/uv` was read-only.
3. With cache and environment paths redirected to `/tmp`, the available Python 3.12 interpreter was correctly rejected because `pyproject.toml` requires Python 3.13.5.
4. `uv run --python 3.13.5 --frozen pytest ...` installed/selected CPython 3.13.5 and began locked environment creation, then failed fetching `pyyaml==6.0.3` from the package mirror with HTTP 502 after retries.
5. A fallback attempt to install `pytest` into a temporary Python 3.12 target failed because the package index proxy was unreachable.

Result: no pytest command is reported passed or failed at product level. Behavioural validation is `blocked_environment`; PM-000 uses only control/static/Git checks. The locked environment must be retried before a behavioural unit can be accepted.

### PM-000 control validation

| Check | Result |
|---|---|
| Current full-read manifest | 539 data rows; 539 unique paths |
| Current repo hashes in manifest | 534 repo paths checked; zero mismatches |
| External attachment records | 5 exact supplied SHA-256 records |
| Manifest status accounting | 531 `read_full_current`; 5 `authored_and_reread_full`; 2 binary archive inventories; 1 ten-record Atlas semantic projection |
| Required control files | 6/6 present and non-empty |
| Changed-path boundary | Only `PLANS.md`, `ROADMAP_LEDGER_V2.md`, and `project_control/canonical_project_manager/**` |
| Forbidden normative/test/source/config/generated mutation | None |
| Fixed implementation order | 33 unique units; exact canonical sequence |
| Closed-unit proof-return order | 11 unique units; exact canonical sequence |
| Physical test recount | Tier A 166, Tier B 13 |
| Retained reconciliation recount | Tier A 120 with 46 physical-only; Tier B 13 with zero difference |
| Vocabulary recount | 46 human, 87 generated, 26 matches, 20 human-only, 61 generated-only |
| Atlas vocabulary slice | 10 records; source metadata says 1,716/1,716 with matching historical object hashes |
| `make scaffold-check` | Passed: `repo scaffold present` |
| `python scripts/run_proof_block.py --check-all` | Passed: 51 proof blocks validated without executing them |
| PM-000 composite control validator | Passed: manifest 539, implementation order 33, closed order 11, Tier A 166/120, Tier B 13/13, vocabulary 46/87, Atlas slice 10 |
| `git diff --check` | Passed with no output |

The control files were reread in full after creation. PM-000 is accepted as a control checkpoint once the bounded commit is created and the resulting clean checkpoint/archive hash is reported. This acceptance does not open PM-001, P1 semantic mutation, test mutation, or Gate D implementation.

## 2026-07-25 — Canonical Gate C completion protocol freeze

### Outcome

- Parent programme plan remains `project_control/canonical_project_manager/EXEC_PLAN.md`.
- New frozen subordinate protocol: `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`.
- Live position pointer updated: `ROADMAP_LEDGER_V2.md`.
- Prior one-file P2 plan explicitly marked superseded for execution and retained as historical evidence.
- `CURRENT_PROJECT_STATE.md` marked as a historical assembly snapshot.
- Historical Gate A–D progress ledger preserved with an append-only continuation entry.
- P2 remains incomplete; P3, P4 and Gate D remain closed.
- No normative document, test, production source, configuration, fixture or generated trading artefact was authorised for mutation by this control leaf.

### Control validation

| Check | Result |
|---|---|
| Canonical checklist IDs | PASS — 56 unique checklist IDs |
| Frozen checked state | PASS — only `GC-000` through `GC-009` checked |
| P3 unit order | PASS — `D-009, D-012, D-015, D-010, D-016, D-033, D-017, D-031, D-021, D-048, D-041` |
| Referenced repository paths | PASS — all required internal control/evidence paths present |
| P2 standing ledger | PASS — 179 rows and 179 unique test paths |
| Old P2 plan status | PASS — explicitly superseded for execution and no worker dispatch |
| Programme/roadmap linkage | PASS — parent ExecPlan and live roadmap both reference the frozen Gate C protocol |
| Gate state | PASS — P2 incomplete; P3, P4 and Gate D closed |
| `git diff --check` | PASS |
| `make scaffold-check` | PASS — `repo scaffold present` |
| `python scripts/run_proof_block.py --check-all` | PASS — 51 proof blocks structurally validated |
| Forbidden mutation scan | PASS — no `src/`, `tests/`, `config/`, `schemas/`, `fixtures/`, `data/` or numbered normative-document change |

Structural validation does not establish semantic acceptance of P2, P3, P4 or Gate D.

## 2026-07-25 13:04:09 AEST — Sole Gate C checklist and main checkpoint

### Outcome

- `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md` now states explicitly that it is the sole operational checklist for the remaining Gate C work.
- `project_control/canonical_project_manager/EXEC_PLAN.md` remains the parent programme controller.
- `ROADMAP_LEDGER_V2.md` remains the current-position pointer.
- Checkpoints, ledgers, receipts, reports, manifests and archives are supporting evidence only and do not create parallel plans or checklists.
- The checkpoint branch is `main`.
- P2 remains incomplete; P3, P4 and Gate D remain closed.

### Validation

| Check | Result |
|---|---|
| Canonical checklist IDs | PASS — 56 unique IDs |
| Frozen checked state | PASS — only `GC-000` through `GC-009` checked |
| P3 unit order | PASS — eleven units in canonical dependency-safe order |
| P2 standing ledger | PASS — 179 rows and 179 unique test paths |
| Sole-checklist routing | PASS — protocol, parent ExecPlan and live roadmap agree |
| Main ancestry before promotion | PASS — prior `main` is an ancestor of the checkpoint commit chain |
| Forbidden mutation scan | PASS — no `src/`, `tests/`, `config/`, `schemas/`, `fixtures/`, `data/` or numbered normative-document change |
| `git diff --check` | PASS |
| `make scaffold-check` | PASS — `repo scaffold present` |
| `python scripts/run_proof_block.py --check-all` | PASS — 51 proof blocks structurally validated |

This is a control/checkpoint validation. It does not accept P2, open P3/P4, or authorise Gate D.

## 2026-07-25 — `CTRL-ARCH-001` module-architecture control integration

### Outcome

- User-accepted `M00`–`M15` Ownership Module architecture integrated into the live control stack.
- `M07` narrowed to `coefficient_modifier_authority`.
- Runtime/contract, state/transaction, governance/promotion and build/test dependency planes separated.
- Thirty-three historical `D-xxx` records retained as traceability obligations; numeric order no longer schedules implementation.
- Module-local Gate C replaces repository-wide P2–P4 completion as the prerequisite for unrelated alpha implementation.
- Progressive physical package migration recorded.
- Missing positive module obligations made explicit for `M07`, `M09`, `M10` and `M11`.
- Seven durable control terms admitted in the human vocabulary registry and projected through the unchanged deterministic builder.
- No production source, tests, runtime configuration or package layout changed.
- First later implementation module remains `M13 state_kernel`, closed until `M13-PROOF` passes after merge.

### Validation

| Check | Result |
|---|---|
| Custom `CTRL-ARCH-001` validator | PASS — 32 checks, zero failures |
| Ownership modules | PASS — 16 unique IDs, exactly `M00`–`M15` |
| Architecture surfaces | PASS — 18 |
| Atlas trace | PASS — 287 cohorts and 1,716 records retained |
| Historical implementation obligations | PASS — 33 unique `D-xxx` records; all have accepted module routes |
| Missing positive obligations | PASS — four (`M07`, `M09`, `M10`, `M11`) |
| Runtime/contract graph | PASS — acyclic, 13/13 domain nodes visited |
| Dependency semantics | PASS — accepted edges use provider/prerequisite → consumer/dependent; historical D-unit convention labelled historical |
| `M08 → M07` runtime dependency | PASS — absent |
| Accepted serial programme | PASS — 14 module entries; `M05`/`M06` reversible only when dependency-ready; no concurrent mutation |
| Workbook structural review | PASS — final control ranges reread through `artifact_tool`; zero formula-error matches |
| Workbook ZIP integrity | PASS — `unzip -t`, no errors |
| Machine-readable JSON | PASS — parsed by `json.tool` |
| Vocabulary builder stability | PASS — before/after SHA-256 `cc96fc074a407f8dfeb74cbb018595eecd37e5735e67964dc00a9a927ea23b71` |
| Vocabulary builder parity | PASS — generated payload exactly equals committed JSON; 124 records including seven new control records |
| Original brief preservation | PASS — semantic body equal after trailing-whitespace normalisation; leading supersession banner added |
| Changed-path boundary | PASS — only expressly opened controls, routed working authority, vocabulary projection and canonical architecture evidence |
| Forbidden source/test/config mutation | PASS — no changed path under `src/`, `tests/` or `config/` |
| `make scaffold-check` | PASS — `repo scaffold present` |
| `git diff --check` | PASS |

Behavioural tests were not used to claim runtime correctness because `CTRL-ARCH-001` changes no runtime behaviour. This entry does not claim module implementation, whole-test-suite authority, production readiness, merge or publication.

The bounded Git commit and Git-preserving archive are closeout evidence reported externally after the committed bytes exist; they are not self-recorded here because doing so would change those bytes recursively.


### External checkpoint closeout — module architecture control integration

| Check | Result |
|---|---|
| Integration commit | PASS — `9ec838a45bd4cf98313e83f73f47d376b1e42806` on `control/accept-module-architecture` |
| Git-preserving archive | PASS — `NVDA_MODULE_ARCHITECTURE_CONTROL_INTEGRATION_9ec838a_20260725.tar.gz` |
| Archive SHA-256 | `faa6d2e196923bcd1641b1616c2fb8bfb3cf0900e4972642b79e2943333d5d5b` |
| Archive bytes | `25193160` |
| Archive integrity | PASS — `gzip -t` |
| Fresh extraction | PASS — branch `control/accept-module-architecture`, commit `9ec838a45bd4cf98313e83f73f47d376b1e42806`, clean worktree |
| Vocabulary Tier A current | NOT GREEN — 18 failed, 83 passed |
| Vocabulary Tier A baseline `0c207f9b7186` | NOT GREEN — 18 failed, 83 passed |
| Vocabulary failed-node differential | PASS — identical 18 failed node IDs; no branch-induced failing node |
| Merge/push | NOT PERFORMED |

The archive proves the committed integration state. The evidence-record commit that contains this entry is reported separately and does not change the validated integration archive.

## 2026-07-25 19:00:46 AEST — `M13-PROOF` authority, Tier A candidate and falsification

### Outcome

- The accepted control-integration branch was fast-forwarded to local `main` at `b153cd1e3e0808991dcf9c188e380d935cfd9283`.
- Branch `proof/m13-state-kernel` was created from that accepted baseline.
- N-06 authority and the accepted `M13 state_kernel` ownership boundary were found sufficient for the minimal non-durable alpha transaction kernel.
- The historical three `C-024` tests were preserved unchanged and demoted to observational evidence for current M13 opening because they target the superseded package path and omit material transaction clauses.
- One current M13 Tier A candidate family was authored and registered through the retained-test registry and a dedicated proof block; blocking authority remains pending independent `MLC-V` acceptance.
- Six durable M13 contract terms were added to the human vocabulary registry and deterministic JSON projection.
- No production source or target `m13_state_kernel` package was created.

### Proof specification covered

- explicit non-durable memory status;
- command, policy, idempotency, result, state-version, sequence and receipt binding;
- idempotency scope by command type and consistency unit;
- exact duplicate replay without repeated mutation;
- conflicting reuse rejection;
- expected-version rejection before mutation;
- rollback after mutation failure;
- rollback after invalid receipt material;
- detached state and receipt readbacks;
- no global transaction, domain ownership, restart-recovery or external-effect claim.

### Validation

| Check | Result |
|---|---|
| Current repository M13 proof | EXPECTED RED — 9 failed solely because `nvda_desk.m13_state_kernel` is absent |
| Isolated conforming reference | PASS — 9 passed |
| Defective reference variants | PASS — all six rejected: durable-label lie, duplicate re-execution, raw-key-only scope, ignored state version, commit on exception, invalid receipt acceptance |
| Historical C-024 nodes | EXPECTED RED — 3 failed because superseded `nvda_desk.persistence.transactions` is absent |
| Proof-block structure | PASS — 52 blocks |
| Proof-executor contract | PASS — 21 passed |
| Retained-test registry | PASS — 121 Tier A files; 120 retained blockers plus one M13 candidate pending independent `MLC-V` acceptance |
| Vocabulary builder | PASS — deterministic 130-entry projection; SHA-256 `5279f27963f2745915e11381fbc6b81c128a228563400ad9a6623ab9b5f4fe95` |
| Vocabulary schema | PASS — 2 passed |
| Vocabulary builder parity | INHERITED RED — 1 failed, 3 passed; the same `Serial Desk-Cognition` heading failure exists at baseline `b153cd1` |
| Existing persistence shadow | PASS — 16 passed |
| Tier B checkpoint shadow | PASS — 2 passed |
| New test syntax | PASS — `compileall` |
| Ruff | UNAVAILABLE — the environment has no installed `ruff` module; no pass claim made |
| `make scaffold-check` | PASS — `repo scaffold present` |
| Production source mutation | NONE |

Raw commands, exit codes, reference source, mutant sources and outputs are retained at `project_control/canonical_project_manager/modules/M13/raw_validation/`.

### Gate result

`CLOSED:MLC-V_INDEPENDENT_PM_ACCEPTANCE_REQUIRED`

The same Project Manager execution pass authored the proof specification and test file. The governing protocol states that the test author cannot provide final acceptance. Mechanical reference and mutation validation demonstrate proof strength but do not waive that role-separation requirement.

`M13-IMPLEMENT` remains closed. The next lawful leaf is an independent read-only acceptance of the frozen M13 proof record and test file.


### M13 proof checkpoint closeout

| Check | Result |
|---|---|
| Proof checkpoint commit | `5f672ddf5a712a3446bada00ebcbbf1d7c0f321c` on `proof/m13-state-kernel` |
| Commit changed-path boundary | PASS — no `src/**`; one M13 test plus proof/config/vocabulary/control evidence |
| Worktree after proof commit | PASS — clean |
| Local `main` | remains `b153cd1e3e0808991dcf9c188e380d935cfd9283`; proof branch not merged |
| Gate state | `CLOSED:MLC-V_INDEPENDENT_PM_ACCEPTANCE_REQUIRED` |

The Git-preserving archive for the later evidence-record commit is reported externally after its bytes exist.

## 2026-07-25 — `M13-PROOF-REPAIR` receipt/repository atomicity return gate

### Input and provenance

- Worker source archive: `NVDA_M13_PROOF_CLOSED_4a25921_20260725.tar(2).gz`.
- Verified source archive SHA-256: `29820c89f27078b186484b0ae512aa35e781d5658adb9f0505a0afc576c3206f`.
- Source branch/commit: `proof/m13-state-kernel` / `4a259217f0ea5c841e514848523b7bd0c496e41f`.
- Repair branch: `proof/m13-state-kernel-repair`.
- The actual independent PM archive was unavailable in the worker filesystem. The user supplied the exact PM disposition, reported decision commit `50d82f2bed689fc72afcbf8250f9625f9908f1f3`, reported checkpoint SHA-256 `5c52aabc7d22a75e51e87a60d86ecd4d7c28c1bdba96e7ec79ec2a314a59214f`, direct probe and return instruction. This provenance limitation is recorded in `modules/M13/raw_validation/independent_pm_rejection_user_supplied.txt`.

### Independent PM defect

`CLOSED:the frozen suite does not prove rollback when the attesting receipt write fails; a commit-before-receipt implementation passes all nine tests while leaving committed state with no receipt`

The return gate authorised only `MLC-P → MLC-T` proof repair. M13 production implementation remained closed.

### Repair

- Preserved all original nine test functions and assertions byte-for-byte at function-source level.
- Added two module-local proof behaviours:
  - receipt-writer failure after visible participant mutation rolls back all participant-visible and internal truth and permits a clean sequence-1 retry;
  - repository-participant failure invokes participant rollback, leaves no participant-visible or internal truth committed, and permits a clean sequence-1 retry.
- Required an executable `RepositoryPort` transaction-participation seam (`prepare`, `commit`, `rollback`) rather than type existence alone.
- Added no production source and created no `m13_state_kernel` implementation package.

### Validation

| Check | Result |
|---|---|
| Original test preservation | PASS — baseline 9 tests; current 11; all baseline test-function source unchanged; exactly 2 appended tests |
| Current repository proof | EXPECTED RED — 11 failed solely because `nvda_desk.m13_state_kernel` is absent |
| Isolated conforming reference | PASS — 11 passed |
| PM commit-before-receipt mutant against original nine | FALSE POSITIVE REPRODUCED — 9 passed, 2 repaired tests deselected |
| PM commit-before-receipt mutant against repaired family | REJECTED — 2 failed, 9 passed |
| No-participant-rollback mutant | REJECTED — 2 failed, 9 passed |
| Original six mutants | PASS AS FALSIFICATION — each was rerun with the two repair tests deselected and rejected by its intended unchanged original test |
| YAML parse | PASS — retained registry and proof blocks |
| Proof-block structure | PASS — 52 blocks |
| Proof-executor contract | PASS — 21 passed |
| Existing persistence shadow | PASS — 16 passed |
| Tier B checkpoint shadow | PASS — 2 passed |
| Repaired test/reference/mutant syntax | PASS — `compileall` |
| `make scaffold-check` | PASS — `repo scaffold present` |
| Ruff | UNAVAILABLE — environment has no installed `ruff` module; no pass claim |
| Production source mutation | NONE |

Raw outputs, source variants and exit-code sidecars are retained under `project_control/canonical_project_manager/modules/M13/raw_validation/`.

### Gate result

`CLOSED:REPAIRED_PROOF_REQUIRES_INDEPENDENT_MLC-V_ACCEPTANCE`

The worker has closed the exact PM return gate mechanically but cannot provide independent final acceptance. `M13-IMPLEMENT` remains closed.


### M13 proof-repair checkpoint closeout

| Check | Result |
|---|---|
| Proof-repair commit | `2dd25e3bdf5759fcaa2320cfd5bba988f9908eee` on `proof/m13-state-kernel-repair` |
| Commit changed-path boundary | PASS — 40 paths, no `src/**`, one test file |
| Committed-state targeted proof | EXPECTED RED — 11 failed for absent `nvda_desk.m13_state_kernel` |
| Committed-state proof-block structure | PASS — 52 blocks |
| Committed-state proof-executor contract | PASS — 21 passed |
| Committed-state persistence shadow | PASS — 16 passed |
| Committed-state checkpoint shadow | PASS — 2 passed |
| Gate state | `CLOSED:REPAIRED_PROOF_REQUIRES_INDEPENDENT_MLC-V_ACCEPTANCE` |

Post-commit output is retained at `modules/M13/raw_validation/postcommit_validation_repair.txt`. The evidence-record commit containing this closeout does not change the repaired test semantics.

## 2026-07-26 — Lost `M13-PROOF-V2` Project Manager checkpoint reconstruction

### Reconstruction boundary

- Sole repository input: `NVDA_M13_PROOF_REPAIRED_490e63e_20260725.tar.gz`.
- Verified source SHA-256: `6f6cd368e8be9f2b69fa7448967714e4517fa7dea3ad787072d96aa8df3b455a`.
- Verified source branch/commit/worktree: `proof/m13-state-kernel-repair` / `490e63ed3c96da90a81239326e2d33dd77bdbf36` / clean.
- Recovery branch: `recovery/m13-pm-v2-closed`.
- Lost checkpoint identifiers are historical references only: `review/m13-proof-v2`, `7e95102ae21d246936bcad97bf2112db9c40a96f`, archive SHA-256 `9d780f4455d32e0ecd49190155d9643fdb9d0615d2cc559c882194f1d15f1801`. No exact-recreation claim is made.

### Reconstructed disposition

`CLOSED:the repaired suite does not prove rollback and clean retry when a RepositoryPort fails during prepare; a coordinator that registers participants for rollback only after prepare returns passes all eleven tests while leaving stale participant transaction state after the failure`

### Independent reproduction

| Check | Result |
|---|---|
| Frozen eleven-test SHA-256 | `f66b8cbe60a70c9dca02b2a65c6f6770273a1be213d5c203cb9fa29dd545d9ee` before and after PM work |
| Register-after-successful-prepare mutant | FALSE POSITIVE — 11 passed |
| First direct-probe attempt | failed after participant established pending state: `participant prepare failed` |
| Failing participant rollback | zero calls |
| Pending state after failure | present |
| Identical retry | failed: `stale pending transaction survived failed prepare` |
| Internal state/version/receipt | unchanged at state `{'count': 0}`, version `0`, no receipts |
| Production, normative and test mutation | none |

Evidence is retained under `modules/M13/raw_validation/` as the mutant source, executable probe, command output and exit-code sidecars.

### Supporting validation

| Check | Result |
|---|---|
| Isolated conforming reference | PASS — 11 passed |
| Existing commit-before-receipt mutant | REJECTED — 2 failed, 9 passed |
| Existing no-participant-rollback mutant | REJECTED — 2 failed, 9 passed |
| Current repository proof | EXPECTED RED — 11 failed solely because `nvda_desk.m13_state_kernel` is absent |
| Proof-block structure | PASS — 52 blocks |
| Proof-executor contract | PASS — 21 passed |
| Persistence shadow | PASS — 16 passed |
| Checkpoint shadow | PASS — 2 passed |
| Retained mutant/probe syntax | PASS |
| Scaffold | PASS — `repo scaffold present` |

### Gate result

`CLOSED:M13_PROOF_REPAIR_V2_REQUIRED_FOR_PREPARE_FAILURE_ROLLBACK_AND_CLEAN_RETRY`

The next lawful unit is proof repair only. M13 production implementation, M01 and all later modules remain closed.

## 2026-07-26 — `M13-PROOF-REPAIR-V2` worker prepare-failure repair

- Source checkpoint: reconstructed PM V2 branch `recovery/m13-pm-v2-closed` at `4d50939f308598efcb668487e2105f038a1fefd7`, archive SHA-256 `772e328d37df00e123a7cfd2569e285b47b188a9d3bf70a06e5a1b6689352a6b`.
- Worker branch: `proof/m13-state-kernel-repair-v2`.
- Original eleven test functions: PASS — all function-source SHA-256 values unchanged.
- Added proof: one prepare-failure participant fixture and one clean-retry test at `tests/tier_a/persistence/test_m13_state_kernel_contract.py:482-579`.
- Conforming reference: PASS — 12 passed.
- PM V2 prepare mutant: old family FALSE POSITIVE — 11 passed; repaired family REJECTED — 1 failed, 11 passed because the failing participant recorded zero rollback calls. The retained direct probe separately reproduces stale pending state and the poisoned identical retry.
- Commit-before-receipt and no-participant-rollback mutants: REJECTED — each 3 failed, 9 passed.
- Original six retained mutants: REJECTED by the repaired family.
- Current repository: EXPECTED RED — 12 failed solely because the production M13 package is absent.
- Proof-block structure: PASS — 52 blocks.
- Proof-executor contract: PASS — 21 passed.
- Persistence shadow excluding M13: PASS — 36 passed, 12 deselected.
- Tier B checkpoint shadow: PASS — 2 passed.
- YAML/registry path validation, syntax and scaffold: PASS.
- Production source, normative authority and proof configuration: unchanged.
- Gate result: `READY_FOR_INDEPENDENT_PM_REVIEW`; no proof acceptance or implementation opening claimed.

### Committed-state receipt

- Proof-repair commit: `7b3b04c4647ee13674e46c55227b5352cb8c8361`.
- Worktree before post-commit evidence: clean.
- Post-commit matrix: PASS — conforming 12/12; prepare mutant old 11/11 and repaired 1 failure/11 passes; all prior mutants rejected; production expected-red 12; proof blocks 52; proof executor 21; persistence shadow 36; checkpoint shadow 2.
- Immutable authority/configuration hashes: unchanged.
- Forbidden changed paths under `src/**`, `docs/**` and `config/**`: zero.
- Evidence: `project_control/canonical_project_manager/modules/M13/raw_validation/v2_postcommit_validation.txt`.
- Final acceptance remains pending independent Project Manager review. `M13-IMPLEMENT` remains closed.

## 2026-07-26 — Independent `M13-PROOF-REPAIR-V2` Project Manager V3 review

### Source verification

- Supplied archive: `NVDA_M13_PROOF_REPAIR_V2_READY_e59b8bd_20260726.tar(1).gz`.
- Archive SHA-256: `e644bd06430449efa8f8277f4ecf222f43dbc93bd8766cbd61f86a6b5d961b9a`.
- Source branch/commit/worktree: `proof/m13-state-kernel-repair-v2` / `e59b8bdfb5d1e34944aa1b661643c8e6570b940c` / clean.
- Review branch: `review/m13-proof-v3`.
- Twelve-test SHA-256: `f457aaba1f90a5f40c7e43cc34dbb26dada5fcb43292661f61a7b18e345fdc5f`.
- Preservation: all eleven source-checkpoint test functions unchanged; exactly one V2 test appended.

### Disposition

`CLOSED:the twelve-test suite does not prove rollback and clean retry for an earlier successfully prepared participant when a later RepositoryPort fails during prepare; a coordinator that rolls back only the participant that raises passes all twelve tests while leaving stale pending state in the earlier participant and poisoning the identical retry`

### Independent reproduction

| Check | Result |
|---|---|
| Conforming reference | PASS — 12 passed |
| Worker register-after-successful-prepare mutant | REJECTED — 1 failed, 11 passed |
| Independent rollback-only-current-prepare-participant mutant | **FALSE POSITIVE — 12 passed** |
| First direct-probe attempt | Later participant established pending state and failed during `prepare()` |
| Earlier participant rollback during first failure | **Absent**; it retained pending state |
| Identical retry | Failed on the earlier participant's stale pending state |
| Internal state/version/receipt | Unchanged at state `{'count': 0}`, version `0`, no receipts |
| Commit-before-receipt and no-participant-rollback mutants | Rejected — each 3 failed, 9 passed |
| Current repository M13 proof | EXPECTED RED — 12 failures solely because `nvda_desk.m13_state_kernel` is absent |
| Proof-block structure | PASS — 52 blocks |
| Proof-executor contract | PASS — 21 tests |
| Persistence shadow excluding M13 | PASS — 36 tests, 12 deselected |
| Checkpoint shadow | PASS — 2 tests |
| Scaffold | PASS |
| Production, normative and proof-configuration mutation | None |

The V2 test proves cleanup of the participant that itself raises during `prepare()`. It does not prove cleanup of an earlier successfully prepared participant when a later participant raises. This is a direct gap against N-06 and M13 proof-specification item 13, which requires every prepared participant to be rolled back.

### Gate result

`CLOSED:M13_PROOF_REPAIR_V3_REQUIRED_FOR_ALL_PRIOR_PREPARED_PARTICIPANT_ROLLBACK`

The next lawful unit is test-only proof repair. Preserve the twelve tests and add one two-participant prepare-failure case requiring rollback of both the later failing participant and every earlier prepared participant, followed by an uncontaminated identical retry committing as sequence/version `1`. M13 production implementation and all later modules remain closed.

Evidence is retained under `project_control/canonical_project_manager/modules/M13/raw_validation/`.

## 2026-07-26 — Independent `M13-PROOF-REPAIR-V3` Project Manager V4 review

### Source verification

- Supplied archive: `NVDA_M13_PROOF_REPAIR_V3_READY_6ef6e44_20260726.tar(1).gz`.
- Archive SHA-256: `4d41c7460690de774a61757d98d2907ac1df26a8fe0cbc3255b79ff89011a113`.
- Source branch/commit/worktree: `proof/m13-state-kernel-repair-v3` / `6ef6e448e28cd96138c0aaeb3d8f8334cad55eb1` / clean.
- Review branch: `review/m13-proof-v4`.
- Thirteen-test SHA-256: `9bca3237bd24e905ce8772d9360f56bb824fa36eb46c4c9e2d82d581e0744374`.
- Preservation: all twelve PM V3 source test functions unchanged; exactly one V3 test appended.

### Disposition

`CLOSED:the thirteen-test suite does not prove that a failed transaction leaves no idempotency binding; an implementation that reserves the scoped key and failed input after rollback passes all thirteen tests, permits exact retry, but falsely rejects a different uncommitted input using that key`

### Independent reproduction

| Check | Result |
|---|---|
| Conforming reference | PASS — 13 passed |
| Worker PM V3 target mutant, original twelve | FALSE POSITIVE REPRODUCED — 12 passed |
| Worker PM V3 target mutant, repaired thirteen | REJECTED — 1 failed, 12 passed |
| Independent failed-attempt idempotency-reservation mutant | **FALSE POSITIVE — 13 passed** |
| First probe attempt | Failed during participant `prepare()`; participant rollback ran and no pending state remained |
| Internal state/version/receipt after failure | Unchanged at state `{'count': 0}`, version `0`, no receipts |
| Different input using same uncommitted scoped key | **Falsely rejected** as `IdempotencyConflictError` by mutant |
| Conforming-reference outcome for same probe | Fresh commit as sequence/version `1` |
| Ten previously retained mutants | Rejected by the thirteen-test family |
| Current repository M13 proof | EXPECTED RED — 13 failures solely because `nvda_desk.m13_state_kernel` is absent |
| Proof-block structure | PASS — 52 blocks |
| Proof-executor contract | PASS — 21 tests |
| Persistence shadow excluding M13 | PASS — 36 tests, 13 deselected |
| Checkpoint shadow | PASS — 2 tests |
| YAML, syntax and scaffold | PASS |
| Production, normative, test and proof-configuration mutation during PM review | None |

The V3 repair closes the prior rollback-order defect. It does not prove the N-06 rule that idempotency binding occurs only with committed result/state/receipt truth. Exact retry can remain executable even while a hidden failed-attempt reservation blocks another uncommitted input.

### Gate result

`CLOSED:M13_PROOF_REPAIR_V4_REQUIRED_FOR_NO_FAILED_IDEMPOTENCY_BINDING`

The next lawful unit is test-only proof repair. Preserve the thirteen tests and add one failure/rollback case proving a different input with the same scoped key remains fresh and can commit as sequence/version `1`. M13 production implementation and all later modules remain closed.

Evidence is retained under `project_control/canonical_project_manager/modules/M13/raw_validation/`.

## 2026-07-26 — Independent `M13-PROOF-REPAIR-V4` Project Manager V5 review

### Source verification

- Supplied archive: `NVDA_M13_PROOF_REPAIR_V4_READY_31e8ac3_20260726.tar(1).gz`.
- Archive SHA-256: `83e1f2bfee1b0665b190383567436c6797e20907481b05091152426a72907d31`.
- Source branch/commit/worktree: `proof/m13-state-kernel-repair-v4` / `31e8ac38488466d1d457f98ffe014576423a5ebf` / clean.
- Review branch: `review/m13-proof-v5`.
- Fourteen-test SHA-256: `c1bc90aedf2905989c22f851f2560969868e87e50bca3f352f6bc91b91200cca`.
- Preservation: all thirteen source-checkpoint functions unchanged; exactly one V4 test appended.

### Disposition

`CLOSED:the fourteen-test suite proves no failed idempotency binding only for repository-participant failure; an implementation that reserves the scoped key only when the mutation raises passes all fourteen tests, leaves state/version/receipts uncommitted, but falsely rejects a different uncommitted input using that key`

### Independent reproduction

| Check | Result |
|---|---|
| Conforming reference | PASS — 14 passed |
| Worker PM V4 target mutant, original thirteen | FALSE POSITIVE REPRODUCED — 13 passed, 1 deselected |
| Worker PM V4 target mutant, repaired fourteen | REJECTED — 1 failed, 13 passed |
| Ten previously retained mutants | Rejected by the fourteen-test family |
| Independent mutation-failure reservation mutant | **FALSE POSITIVE — 14 passed** |
| Independent failed-binding-by-command-identity mutant | **FALSE POSITIVE — 14 passed** |
| Mutation-failure state/version/receipt truth | Clean at state `{'count': 0}`, version `0`, no receipts |
| Different input using same uncommitted scoped key | **Falsely rejected** as `IdempotencyConflictError` by mutant |
| Conforming-reference outcome | Fresh commit as sequence/version `1` |
| Corrected same-command-ID reuse after failed participant attempt | Mutant falsely conflicts; conforming reference commits sequence `1` |
| Current repository M13 proof | EXPECTED RED — 14 failures solely because `nvda_desk.m13_state_kernel` is absent |
| Proof-block structure | PASS — 52 blocks |
| Proof-executor contract | PASS — 21 tests |
| Checkpoint shadow | PASS — 2 tests |
| YAML, syntax and diff checks | PASS |
| Production, normative, test and proof-configuration mutation during PM review | None |

The V4 repair closes the participant-prepare failed-binding defect. It does not establish the same no-binding invariant for mutation failure or the other admitted failure classes. It also changes command ID and input fingerprint together, so a hidden reservation tied to one identity dimension remains invisible. A passing test proves only its exercised path and identity variation; the generic test name does not extend its semantics.

### Gate result

`CLOSED:M13_PROOF_REPAIR_V5_REQUIRED_FOR_NO_BINDING_ACROSS_PRE_COMMIT_FAILURES`

The next lawful unit is test-only proof repair. Preserve the fourteen tests and add a systematic public-seam no-binding matrix across stale expected version, mutation exception, invalid receipt/result, participant prepare/commit and receipt-writer failure. Vary command ID, fingerprint and policy version independently. M13 production implementation and all later modules remain closed.

Evidence is retained under `project_control/canonical_project_manager/modules/M13/raw_validation/`.


## 2026-07-26 — Independent `M13-PROOF-REPAIR-V5` Project Manager V6 acceptance

### Source verification

- Supplied archive: `NVDA_M13_PROOF_REPAIR_V5_fd52804_20260726.tar(1).gz`.
- Archive SHA-256: `ea7083aff6b36cab7988ba01ecade229007a856d90af00ad038fa1df94309293`.
- Source branch/commit/worktree: `proof/m13-state-kernel-repair-v5` / `fd52804ff6b3f2cda3bf2f499007146b30c7808b` / clean.
- Review branch: `review/m13-proof-v6`.
- Current proof-file SHA-256: `7f4fd1e3d9c7f7dc75675146f9e2a38d4fb259a1938986c7cdfc2b006ddfab0a`.

### Disposition

`IMPLEMENTATION_OPEN`

### Independent validation

| Check | Result |
|---|---|
| Fourteen-function preservation | PASS — no removed or changed AST |
| Current repository proof | EXPECTED RED — 46 failures solely from absent target package |
| Conforming reference | PASS — 46 passed |
| PM V5 mutation-failure mutant | Old family 14 passed; repaired family 3 failed/43 passed for hidden failed binding |
| PM V5 command-identity mutant | Old family 14 passed; repaired family 6 failed/40 passed for command-ID-only failed binding |
| Configurable failed-binding matrix | PASS — worker evidence 32/32; source, case IDs and intended assertions independently reviewed |
| Earlier retained mutants | PASS — worker evidence 11/11; full and target outputs, scripts and summaries independently reviewed |
| Changed-path boundary | PASS — proof repair changed only M13 test, proof record and raw evidence |
| Production/normative/config mutation during proof repair | None |

### Gate result

The proof is sufficient to constrain implementation of the non-durable alpha transaction kernel. `M13-IMPLEMENT` is open under the frozen 46-case family. This does not accept implementation, durability, restart recovery, external effects, M01 or later-module work.

### PM V6 post-acceptance independent closeout validation

The long falsification runners were re-executed in bounded batches from a disposable extraction so the worker's retained evidence was not overwritten.

| Check | Result |
|---|---|
| Configurable failed-binding variants | PASS — 32/32 independently rejected for the intended hidden-binding false conflict |
| Earlier retained mutants | PASS — 11/11 independently rejected in full-family and targeted runs for the intended defect |
| Proof executor | PASS — 21 passed |
| Persistence shadow excluding M13 | PASS — 36 passed, 46 deselected |
| Checkpoint shadow | PASS — 2 passed |
| Proof-block structure | PASS — 52 blocks |
| YAML parse | PASS |
| Python syntax | PASS |
| Repository scaffold | PASS |
| Git diff check | PASS |

Exact PM rerun records are retained under `project_control/canonical_project_manager/modules/M13/raw_validation/pm_v6_review/`.

## 2026-07-26 — Independent M13 implementation V1 review

### Source verification

- Supplied archive: `NVDA_M13_IMPLEMENTATION_PROPOSED_ddbd725_20260726.tar(1).gz`.
- Archive SHA-256: `f522111ce84bab3b785bb161a71c0bf00e569263d4ba050744d30b19ac933c5e`.
- Worker branch/commit/worktree: `implementation/m13-state-kernel` / `ddbd7257ab7305b2a3648f9f1d810b07670808aa` / clean.
- Frozen M13 proof SHA-256: `7f4fd1e3d9c7f7dc75675146f9e2a38d4fb259a1938986c7cdfc2b006ddfab0a`.
- Production changes: exactly four files under `src/nvda_desk/m13_state_kernel/`; no test, normative or proof-configuration mutation.

### Positive validation

| Check | Result |
|---|---|
| Frozen M13 proof | PASS — 46 passed |
| Complete persistence Tier A | PASS — 82 passed |
| Proof blocks | PASS — 52 |
| Proof executor | PASS — 21 passed |
| Checkpoint shadow | PASS — 2 passed |
| Architecture/integrity/public-contract worker validators | PASS |
| Implementation-derived mutant runner | PASS — eight full and targeted intended rejections independently observed |
| Complete repository shadow | 61 failed, 1247 passed; agrees with worker current-state count |

### Independent blocking probes

| Probe | Result | Observed defect |
|---|---|---|
| Re-entrant `execute()` during owner mutation | FAIL as required for detection | two receipts survive with sequence/version `1`; inner state is overwritten while its receipt/binding remains |
| Direct `AtomicReceipt` construction | FAIL as required for detection | mismatched receipt/key scope and float resulting version are accepted |

### Disposition

`CLOSED:M13_PROOF_REPAIR_V6_REQUIRED_FOR_REENTRANT_EXECUTION_AND_RECEIPT_CONTRACT_TRUTH`

The next unit is test-only proof repair. M13 source repair, merge, completion, M01 and later modules remain closed.

Exact PM evidence is retained under `project_control/canonical_project_manager/modules/M13/raw_validation/pm_implementation_v1_review/`.


## 2026-07-26 — Independent `M13-PROOF-REPAIR-V6` Project Manager review

### Source verification

- Archive SHA-256: `37f54c1d4581b2a30bc7770b4a55cc9acde81832bb98ba2935ad6e8bade5f93a`.
- Source branch/commit/worktree: `proof/m13-state-kernel-repair-v6` / `d01f75813260cae46597ed9d258ee68efb4b6508` / clean.
- Changed-path boundary: one M13 test plus M13 proof/evidence only; no production, normative or configuration mutation.

### Positive validation

- Frozen function AST: 15/15 unchanged; nine V6 functions added.
- Collection: 131.
- Conforming reference: 131 passed.
- Rejected implementation: 43 failed, 88 passed; original 46 green.
- Declared V6 mutants: 16/16 independently rejected in full and designated runs.
- Proof blocks 52; proof executor 21; non-M13 persistence 36; checkpoint 2; YAML and diff checks passed.

### Independent blocker

A module-global active-attempt guard passes all 131 cases. A direct two-instance public-seam probe passes on the conforming reference but fails on the global-guard mutant, which blocks a second unrelated `UnitOfWork` while the first is active.

### Gate result

`CLOSED:M13_PROOF_REPAIR_V7_REQUIRED_FOR_INSTANCE_SCOPED_ACTIVE_ATTEMPT_EXCLUSION`

Return only to test-only V7 proof repair. Production repair, merge, M01 and later modules remain closed.

## 2026-07-26 — Independent `M13-PROOF-REPAIR-V7` Project Manager acceptance

### Source verification

- Supplied archive: `NVDA_M13_PROOF_REPAIR_V7_aded5ed_20260726.tar(3).gz`.
- Archive SHA-256: `1eb29baac7b0e3253c499957d50b85fce1e1440ec43da26b1dc2a6a335bd4d72`.
- Worker branch/commit/worktree: `proof/m13-state-kernel-repair-v7` / `aded5edc1ad567a1f7d3a4231b918b3af1abd7bd` / clean.
- Accepted parent: `cf44a74385536672237de4747d084faaa7971b47`.
- Changed semantic paths: M13 proof test and M13 proof record only; no `src/**`, normative or configuration mutation.

### Disposition

`IMPLEMENTATION_REPAIR_OPEN`

### Independent validation

| Check | Result |
|---|---|
| Frozen V6 proof | PASS — 24/24 functions and 131/131 cases unchanged |
| V7 additions | PASS — two functions, 21 cases; total 152 |
| Conforming reference | PASS — 152 passed |
| Frozen rejected implementation | EXPECTED RED — 44 failed, 108 passed |
| PM global-guard distinction | PASS — frozen V6 false positive reproduced; V7 rejects it |
| V7 guard mutants | PASS — 8/8 designated targeted rejections independently rerun |
| Worker evidence integrity | PASS — 484 hashes verified |
| Proof blocks | PASS — 52 |
| Proof executor | PASS — 21 |
| Non-M13 persistence Tier A | PASS — 36 |
| Checkpoint shadow | PASS — 2 |
| Architecture boundary | PASS — M13 has no outgoing top-level dependency or cycle membership |
| Vocabulary exact parity | PASS — 1 |
| YAML | PASS |
| Ruff/Black independent rerun | unavailable in PM environment; worker outputs are integrity-hashed and no source/test formatting change was introduced during PM review |

### Gate result

The V7 proof closes the measured instance-scope false positive without weakening same-instance exclusion. Open only `M13-IMPLEMENT-REPAIR-V1` under the frozen 152-case family. M13 final acceptance, merge, M01 and later modules remain closed.

Independent evidence is retained under `project_control/canonical_project_manager/modules/M13/raw_validation/pm_v8_review/`.
