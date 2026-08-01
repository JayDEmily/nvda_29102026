# NVDA M00 Pre-Execution Testing and Guardrail Audit

**Date:** 1 August 2026  
**Repository:** `Nvda11`  
**Branch:** `work/signal-phase-dmpv3-repair-v1`  
**Commit:** `258470526c36da61b3ff4162f1d5ad9e512a8b54`  
**Repository state after audit:** clean  
**Audit mode:** read-only; no M00 implementation or repository repair performed

## 1. Decision

**HOLD M00 implementation. Repair the test-admission and promotion control plane first.**

This is **not** a recommendation to rewrite the alpha codebase. The evidence points in the opposite direction: the current module-local proof blocks for M01–M13 all passed in the available diagnostic environment, and the full Tier B route also passed. The systemic weakness is concentrated in the machinery that decides:

1. which tests are authoritative;
2. which are blocking Tier A tests;
3. which proof blocks constitute the current promotion set;
4. whether that set was executed in the declared environment; and
5. whether a green result is sufficient evidence to begin M00.

At the current commit, that machinery is internally inconsistent. One admission authority is syntactically invalid, the proof executor can report `PASS` without reading it or executing tests, CI expects a retired manifest schema, and the physical Tier A tree contains mutually contradictory tests without one working selector that identifies the current law.

M00 is the final composition boundary. Starting it while the promotion selector is unreliable would make any later green result ambiguous: it could mean the architecture is correct, or merely that the wrong tests were selected.

## 2. Outcome

### Known true

- The active ExecPlan states `READY:M00_FINAL_COMPOSITION`; the prior signal-phase/DMPV3 repair is accepted, and M00 has not started (`project_control/canonical_project_manager/EXEC_PLAN.md:5`, `:325-333`).
- The roadmap states that M00 is the remaining composition unit and that M01–M13 are accepted (`ROADMAP_LEDGER_V2.md:7-13`, `:220-225`).
- No M00 implementation package, M00 test family or M00 project-control package exists at this commit. That is consistent with “not started”, but it means M00 has no admitted expected-red proof gate yet.
- All thirteen current module-local proof blocks passed in the available diagnostic environment: M13, M04, M01, M07, M08, M02, M03, M05, M06, M09, M10, M11 and M12. Tier B also passed 49 tests.
- `config/retained_test_registry.yaml` does not parse as YAML because two newly added `notes` values are malformed (`config/retained_test_registry.yaml:3743`, `:3766`).
- `scripts/run_proof_block.py --check-all` nevertheless returns `PASS count=64`, because it validates only the proof manifest structure and path existence; it neither reads the retained-test registry nor executes the proof commands (`scripts/run_proof_block.py:15-36`, `:88-124`, `:174-189`).
- The live admission/control surfaces disagree on schema and membership. The proof manifest identifies 64 blocks; its Tier A paths expand to 170 physical Tier A files. The repaired-in-memory registry inventory contains 121 files. The physical Tier A tree contains 181 files.
- The repository’s own testing law requires one authoritative aggregate route that resolves the admitted Tier A set, reconciles registry and manifest, executes all blockers, fails on red/missing/skipped/unreconciled results, and records environment and Git evidence (`docs/08.1_TESTING_AND_PROMOTION_WORKING.md:96-110`). No current command does this.

### Ruled out

- **“The whole alpha codebase is broken.”** Ruled out by the passing module-local proof blocks and Tier B diagnostics.
- **“M00 has already been executed.”** Ruled out by the active plan, roadmap and absence of M00 implementation/proof surfaces.
- **“A simple increase in unit-test count is the remedy.”** Ruled out. The central failure is authority selection and integration proof, not insufficient raw test volume.
- **“The existing proof-executor PASS is a promotion result.”** Ruled out by its implementation and its own contract tests: `--check-all` intentionally does not execute proof commands.
- **“All current full-suite failures are production defects.”** Ruled out. The physical tree contains stale, expected-red, historical and mutually contradictory assertions. The 250-class failure count cannot be interpreted semantically until admission is reconciled.

### Next gate

Before M00 implementation, complete one bounded control repair:

> Establish one machine-enforced, reproducible promotion route that derives the exact current Tier A set from reconciled authorities, executes it in the declared locked environment, and produces sufficient Git/environment/result evidence.

Then create and admit the M00 normative/proof package as expected-red before writing M00 production code.

## 3. Scope and method

The audit followed the repository’s authority chain rather than treating generic industry practice as replacement architecture.

### Repository authority inspected

- `00_TASK/PROJECT_EXECUTION_METHOD.md`
- `AGENTS.md`
- `PLANS.md`
- `tests/AGENTS.override.md`
- active `project_control/canonical_project_manager/EXEC_PLAN.md`
- root `ROADMAP_LEDGER_V2.md`
- core and working normative documents relevant to authority, architecture, process, testing, state, replay, vocabulary and module composition, including `docs/01*` through `docs/11*`
- `project_control/canonical_project_manager/CANONICAL_PROJECT_MANAGER_EXECUTION_BRIEF.md`
- architecture decision and traceability material relevant to M00 and the prior repair
- proof manifests, retained-test registry, Makefile, CI workflows and proof executor
- relevant API, dependency and legacy orchestrator code
- relevant legacy/current contradictory API tests and proof-model tests

### Validation performed

The audit used the repository read-only. Diagnostic execution used an available Python environment only where the declared installation route could not be established. Those results are evidence about test behaviour, **not promotion proof**.

Key diagnostics:

- Git branch/commit/status confirmation.
- YAML parse of both control files.
- Proof-manifest/registry/physical-tree membership comparison.
- `scripts/run_proof_block.py --check-all` behaviour.
- Individual execution of all thirteen current module-local proof blocks.
- Tier B execution.
- Tier A collection and split execution diagnostics.
- Separate execution of directly contradictory legacy and current API-law tests.
- Declared `make install` attempt.
- locked `uv sync --frozen --extra dev` attempt.

## 4. Positive baseline

The audit found substantial evidence that the architecture work is not merely decorative.

| Proof block | Diagnostic result |
|---|---:|
| M13 state kernel | 152 passed |
| M04 packet role | 271 passed |
| M01 source admission | 18 passed |
| M07 coefficient modifier | 20 passed |
| M08 playbook catalogue | 23 passed |
| M02 financial calendar | 33 passed |
| M03 prepared data | 29 passed |
| M05 serial cognition | 44 passed |
| M06 parallel risk | 33 passed |
| M09 capital authority | 42 passed |
| M10 execution gateway | 28 passed |
| M11 portfolio lifecycle | 23 passed |
| M12 authoritative replay | 22 passed |
| Tier B aggregate | 49 passed |

These results show that the module-local contracts are generally coherent enough to execute independently. They also demonstrate why a wholesale rewrite would be disproportionate. The weak point is the transition from local proof to whole-system acceptance.

## 5. Findings

### F1 — CRITICAL: the retained-test admission authority is unreadable

**Intended control**  
Tests must be explicitly admitted through the retained-test registry and proof manifest before they acquire Tier A authority (`tests/AGENTS.override.md:20-21`, `:33`, `:42-46`).

**Verified condition**  
`config/retained_test_registry.yaml` raises a YAML scanner error. Two entries use `notes: >- The ...`, which is not a valid block-scalar declaration (`config/retained_test_registry.yaml:3743`, `:3766`).

**Failure mechanism**  
Any process that relies on the registry cannot deterministically derive the current admitted set. A human may mentally repair the syntax, but that is not a machine-enforced control.

**Alpha classification**  
Real control defect, not acceptable alpha incompleteness. An alpha may have unfinished features; its test-authority file still has to parse.

**Smallest correction**

1. Repair the two malformed scalar entries.
2. Add a schema parser that rejects duplicate IDs, duplicate paths, unknown lifecycle/tier values and invalid counts.
3. Make this parser the first step of every proof and CI route.

**Recurrence detection**  
Tier A: control-file schema/semantic test. Tier B: malformed/duplicate fixture tests for the validator. Tier C: retained repair receipt.

---

### F2 — CRITICAL: the proof executor can produce a false-green control result

**Intended control**  
A proof result must identify and execute the exact admitted proposition in the declared environment. Green counts alone do not establish integration or promotion (`docs/08.1_TESTING_AND_PROMOTION_WORKING.md:13-36`, `:90-110`).

**Verified condition**  
`run_proof_block.py --check-all` returned `proof_blocks_check_all=PASS count=64` while the retained-test registry was invalid. The script loads only `config/proof_blocks.yaml`, checks fields/path existence and does not execute commands in `--check-all` mode (`scripts/run_proof_block.py:15-36`, `:88-124`, `:174-189`). Its Tier B contract tests explicitly require that validation mode not run the commands (`tests/tier_b/proof_model/test_proof_executor_contract.py:82-97`, `:388-409`).

**Failure mechanism**  
The script is behaving as implemented, but its result label is operationally stronger than its evidence. A green manifest-lint result can be mistaken for a green proof system even when the admission authority is unreadable.

**Alpha classification**  
System-design mismatch. The runner itself need not become a monolith; its status must be scoped accurately and composed into a real aggregate gate.

**Smallest correction**

- Rename or clearly scope `--check-all` as manifest validation.
- Add a separate aggregate command that parses both authorities, reconciles them, executes the resolved blocking set and fails closed.
- Prevent CI or closeout receipts from presenting manifest validation as promotion proof.

**Recurrence detection**  
Tier A: an intentionally broken registry must make the aggregate gate fail. Tier B: runner-mode contract tests. Tier C: historical receipts proving the old false-green case.

---

### F3 — CRITICAL: no authoritative aggregate promotion route exists

**Intended control**  
The project requires one exact aggregate process that:

- selects the current admitted Tier A set;
- checks registry/manifest agreement;
- executes every blocker;
- fails on red, missing, skipped or unreconciled tests;
- records environment and pre/post Git evidence.

This is explicit in `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:96-110` and was already required by the canonical execution brief before implementation (`project_control/canonical_project_manager/CANONICAL_PROJECT_MANAGER_EXECUTION_BRIEF.md:232-252`).

**Verified condition**

- `make test` executes the physical `tests` tree, not the admitted current set (`Makefile:110-112`).
- `make proof-block PROOF_BLOCK_ID=...` executes one selected block, not the aggregate (`Makefile:301-304`).
- `proof-executor-check` is token/static checking, not execution (`Makefile:70-84`).
- PR preflight runs compile plus the physical full suite and token checks (`.github/workflows/pr-preflight.yml:44-60`).

**Failure mechanism**  
There is no single answer to “what must pass now?”. Local blocks can pass while current expected-red obligations are omitted, or physical stale tests can keep CI permanently red.

**Alpha classification**  
Real promotion-control gap. This is precisely the kind of guardrail needed before final composition, even in an alpha.

**Smallest correction**  
Create one command, for example `make promotion-proof`, whose resolver is itself tested. Do not build a second independent inventory in CI; CI must call the same command.

**Recurrence detection**  
Tier A: aggregate-gate end-to-end control test with known admitted, omitted, stale, skipped and failing specimens. Tier B: resolver unit/property tests. Tier C: immutable gate receipts.

---

### F4 — CRITICAL: the three admission surfaces disagree materially

**Verified inventory**

| Surface | Current observed membership |
|---|---:|
| Physical `tests/tier_a` files | 181 |
| Tier A files expanded from proof-manifest paths | 170 |
| Registry inventory after in-memory syntax repair | 121 |
| Proof blocks | 64 total: 60 Tier A, 4 Tier B |

The registry’s 121 paths are contained in the manifest-expanded set, leaving 49 manifest-only Tier A paths with no machine-enforced explanation. Eleven physical Tier A files are absent from all proof-manifest path expansion, including several current Gate C authority tests and reopened proof rows.

Three proof blocks labelled Tier A also invoke Tier B paths. This may be deliberate composition, but the current schema does not explain the tier transition.

**Failure mechanism**  
The project correctly states that physical folder placement does not confer authority. However, the files that are meant to confer authority cannot currently be reconciled, so the true blocking set is not derivable.

**Alpha classification**  
Control reconciliation defect. It does **not** mean that all 49 manifest-only files are wrong or that the eleven omitted files must all block. It means their status is Unknown until classified through one authority.

**Smallest correction**

- Choose one canonical test-admission record.
- Make proof blocks reference admitted test IDs rather than independently globbing paths, or generate one surface from the other.
- Require an explicit lifecycle for every physical test: current blocking, current nonblocking, expected-red next gate, superseded compatibility, or historical.
- Reject unexplained cross-tier path inclusion.

**Recurrence detection**  
Tier A: zero-diff reconciliation test. Tier B: resolver tests for globs, duplicates and tier transitions. Tier C: archived supersession map.

---

### F5 — CRITICAL: the selected test authority currently favours superseded API behaviour

**Verified contradiction**

The legacy test `tests/tier_a/api/test_fwd005_api_exposure_contract.py` positively requires:

- cached internal mutable services;
- API-owned CRUD/state collections;
- veto/risk-block recording routes.

The current Gate C test `tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py` requires the opposite: no API-owned veto/risk-block collections or record routes, and fail-closed behaviour when authority is missing.

Executed separately in the diagnostic environment:

- legacy API file: **3 passed**;
- current Gate C file: **3 failed, 1 passed**.

The proof manifest includes the legacy file and omits the current Gate C file. The project’s own semantic-read ledger had classified the legacy test as blocked for repair and the current test as current Tier A. The live selector therefore inverts the documented authority.

**Failure mechanism**  
A green selected proof can reward the precise pre-M00 ownership pattern that M00 is intended to remove.

**Alpha classification**  
The current test failing before M00 is expected and useful. The defect is not the red test; it is that the promotion route omits it and retains the superseded positive assertion.

**Smallest correction**

- Remove the legacy test from the current blocking route or classify it explicitly as compatibility/historical proof.
- Admit the current test as expected-red for the M00 gate.
- Preserve both only where their lifecycle is explicit and non-conflicting.

**Recurrence detection**  
Tier A: authority-precedence test that proves current law supersedes legacy law. Tier B: conflict-detector fixtures. Tier C: retained legacy behaviour specimen.

---

### F6 — CRITICAL: active control-state documents disagree

**Verified condition**

- The active ExecPlan and roadmap identify M00 as the next lawful unit after the accepted repair.
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:13-32` still declares the M12 pack current and paused, with M00 not started.
- The core process law requires one coherent active control state.

**Failure mechanism**  
A worker following the live plan proceeds to M00; a worker treating the numbered working law as the current pack can stop or resume M12. AI workers are particularly likely to follow whichever authoritative-looking statement is nearest to their task.

**Alpha classification**  
Governance defect, not implementation incompleteness.

**Smallest correction**  
Update the working process law or explicitly demote its active-pack paragraph to historical status. Add a machine check that current module/status/pack agree across the live pointer, ExecPlan, roadmap and any document allowed to declare “current”.

**Recurrence detection**  
Tier A: active-control singleton test. Tier B: conflicting-document fixtures. Tier C: historical transition record.

---

### F7 — HIGH: CI uses retired schemas and stale counts

**Verified condition**

`.github/workflows/apply-remote-bridge-patch.yml:90-113` parses the registry and proof manifest but expects proof keys `blocks` and `block_id`; the live manifest uses `proof_blocks` and `proof_block_id`. It also expects a Tier A count of 75, while the current registry inventory declares 121. The registry currently fails before those checks are reached.

PR preflight separately runs the physical suite rather than the admitted aggregate route.

**Failure mechanism**  
CI can fail for obsolete structural reasons while still failing to establish current promotion readiness. That produces noise and encourages bypasses—the exact opposite of a useful blocking gate.

**Alpha classification**  
Real automation drift.

**Smallest correction**  
Delete duplicated schema interpretation from workflows. CI should call the repository-owned validator and aggregate gate. Counts should be derived, not hard-coded.

**Recurrence detection**  
Tier A: workflow calls canonical command. Tier B: schema-version compatibility tests. Tier C: CI receipt.

---

### F8 — HIGH: the declared environment is not reproducibly enforced

**Verified condition**

- The Makefile names `uv.lock` as an install-stamp input but performs `pip install -e ".[dev]"`, which does not consume the lock (`Makefile:12`, `:93-98`).
- In this environment, `make install` failed because pip could not resolve the declared `hatchling` build backend from the configured index.
- A separate `uv sync --frozen --extra dev` attempt also failed because the configured source returned 404 for the locked `fastapi==0.135.1` artifact.
- `pyproject.toml` places `.` and `src` directly on pytest’s import path, which allows source-tree imports to mask installation/package defects.

**Failure mechanism**  
Two workers can run “the tests” against different dependency sets or import layouts. A green source-tree test can coexist with a broken installable package.

**Alpha classification**  
The external index failure may be environment-specific; whether the authorised CI index resolves every pin is Unknown. The repository-level defect is verified: the canonical Make route does not enforce the lock it cites.

**Smallest correction**

- Make the declared route consume `uv.lock` or another single lock authority.
- Record Python, platform and dependency lock hash.
- Add one installed-package smoke route that does not depend on `pythonpath=src`.
- Keep fast source-tree unit tests if useful, but do not confuse them with packaging proof.

**Recurrence detection**  
Tier A: clean-environment locked install plus installed-package smoke. Tier B: source-tree fast tests. Tier C: environment receipt.

---

### F9 — HIGH: the physical Tier A command is neither a clean gate nor a reliable feedback loop

**Verified condition**

In the noncanonical diagnostic environment:

- Tier A collected 1,898 tests.
- The unsplit route reached approximately 94%, accumulated many failures and did not terminate within four minutes.
- A non-vocabulary partition completed with 1,548 passed and 247 failed in about 17 seconds.
- Repository validation records show a comparable full Tier A state after the prior repair: 1,648 passed and 250 failed, with prior nontermination history.

**Failure mechanism**  
The physical full suite mixes current blocking, expected-red, stale and historical assertions. It is too red to be a promotion gate and too noisy to localise failures. Running it unsplit also has a termination problem.

**Alpha classification**  
Expected-red tests are appropriate before implementation. Permanent ambiguity about which reds matter is not.

**Smallest correction**

- Make the admitted current set the blocking gate.
- Keep expected-red next-gate tests in an explicit separately reported route that must transition to blocking when implementation starts.
- Split known high-cost families and enforce per-block timeouts while preserving a whole-system aggregate result.
- Do not suppress failures with blanket `xfail` or deselection; encode lifecycle in the admission model.

**Recurrence detection**  
Tier A: bounded aggregate duration and zero unexplained failures/skips. Tier B: performance/timeout diagnostics. Tier C: historical full-tree trend only.

---

### F10 — HIGH: proof blocks do not identify exact normative propositions

**Verified condition**  
Proof-manifest entries contain `proof_block_id`, `tier`, `lifecycle`, `command` and `owns`. They do not contain an exact normative proposition locator. Registry entries frequently cite broad documents rather than a stable proposition ID or line-scoped rule.

The testing law requires an exact proposition and traceability sufficient to detect meaning changes (`docs/08.1_TESTING_AND_PROMOTION_WORKING.md:28-36`).

**Failure mechanism**  
A document can be edited substantially while a proof remains attached to its filename and appears valid. AI-generated tests then tend to preserve wording rather than semantics.

**Alpha classification**  
Traceability guardrail gap.

**Smallest correction**  
Assign stable normative proposition IDs and require every blocking proof block to reference them. Validation must fail if a referenced proposition is removed, duplicated or superseded without an explicit transition.

**Recurrence detection**  
Tier A: proposition-reference integrity. Tier B: supersession/renumbering fixtures. Tier C: decision lineage.

---

### F11 — HIGH: proof receipts are insufficient to reproduce or trust a promotion claim

**Verified condition**  
The proof runner’s receipt records mode, block, status, exit code, command, resolved command and owned paths (`scripts/run_proof_block.py:197-212`). It omits:

- Git commit and pre/post working-tree state;
- Python/platform/dependency or lock identity;
- resolved admitted test/node set;
- passed/failed/skipped/xfailed outcomes;
- collection failures and timeout state;
- output or evidence hashes.

**Failure mechanism**  
A receipt can show exit zero without proving which repository state, dependency set or exact tests produced it.

**Alpha classification**  
Evidence-quality defect. The remedy does not require a heavyweight provenance platform.

**Smallest correction**  
Add the smallest sufficient receipt: commit, branch, pre/post status, environment/lock hash, exact resolved node/path set, outcome counts, duration, command and log hash.

**Recurrence detection**  
Tier A: receipt-schema and tamper/missing-field tests. Tier B: formatter tests. Tier C: retained receipts.

---

### F12 — HIGH but expected: the legacy composition root still owns state, defaults and identity

**Verified condition**

The architecture explicitly marks `DeskRuntimeOrchestrator` as noncanonical and defines M00 as translation, dependency composition and run-lifecycle only (`docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:154-171`, `:319-330`, `:371-373`).

Current code still contains the pre-M00 composition debt:

- `src/nvda_desk/runtime/orchestrator.py:33-38` identifies itself as legacy/noncanonical.
- It creates run/trace/scenario identities and wall-clock time internally, constructs services internally and supplies an empty candidate-family collection (`:119-132`).
- `src/nvda_desk/api/app.py:51-96` constructs/caches services and invokes the legacy orchestrator.
- The API fabricates fallback lineage/decision identity and owns mutable event collections (`src/nvda_desk/api/app.py:278-304`, `:376-390`).
- `src/nvda_desk/api/deps.py:48-144` uses cached mutable stores/repositories plus hard-coded SQLite and starting-cash defaults.

**Failure mechanism**  
Without hard M00 proofs, a new shell can wrap these surfaces and appear complete while retaining the same hidden ownership and fabricated defaults.

**Alpha classification**  
Expected pre-M00 implementation debt, already recognised by the project as D-021/D-048. This is **not** evidence to rewrite M01–M13. It defines the M00 acceptance boundary.

**Smallest correction**  
Do not repair this piecemeal before the M00 proof package exists. Encode the composition laws first, then replace the canonical root while retaining legacy surfaces only as explicitly noncanonical compatibility paths.

**Recurrence detection**  
Tier A: M00 architectural and run-lifecycle tests described in Section 7. Tier B: legacy compatibility tests. Tier C: pre-M00 specimen/receipt.

---

### F13 — HIGH: M00 lacks its required pre-code normative/proof gate

**Verified condition**  
There is no M00 source package, M00 test family or M00 project-control package. Absence of implementation is correct because M00 has not started. However, the project’s method requires normative law and expected-red proof before implementation.

**Failure mechanism**  
“Ready for M00” can be interpreted as permission to start code directly, especially when the aggregate promotion gate is already ambiguous.

**Alpha classification**  
Missing next gate, not a defect in unfinished M00 code.

**Smallest correction**  
After F1–F11 are resolved, open M00 with a bounded C-NORM/C-PROOF unit. Only then begin implementation.

## 6. External best-practice comparison

The recommended repair is consistent with current primary guidance without importing heavyweight production ceremony into an alpha:

- **Google:** keep most tests fast and local, but use hermetic integration tests at meaningful boundaries to detect protocol and composition drift. Do not substitute a large end-to-end layer for precise lower-level proof.
- **Microsoft:** tests should be fast, isolated, repeatable and independent, with dependencies explicit and a known starting state. Integration tests should join real components for selected important scenarios rather than duplicate every unit case.
- **pytest/Python packaging practice:** test the installed package in at least one clean route so source-tree path configuration cannot conceal packaging defects. Register and enforce markers rather than relying on informal categorisation.
- **IBM:** testing should trace to specified requirements and begin with the requirement/design stage; integration testing validates modules working together, while end-to-end tests are reserved for critical complete workflows because they cost more to run and diagnose.

The project’s existing Tier A/B/C concept is compatible with these principles. The missing element is not a new framework; it is a trustworthy admission resolver and a small number of hermetic composition proofs.

## 7. Recommended path

### Gate 0 — repair the proof/admission control plane

Complete this as one bounded pre-M00 acceptance unit:

1. **Repair and validate the registry**
   - fix YAML;
   - define one schema;
   - reject duplicates, unknown lifecycle/tier values and unexplained physical tests.

2. **Reconcile authority**
   - update the active-pack contradiction in `docs/06.1`;
   - classify every test as current blocking, current nonblocking, next-gate expected-red, superseded compatibility or historical;
   - resolve the legacy/current API-test inversion.

3. **Create one aggregate command**
   - derive exact current Tier A from the canonical admission authority;
   - reconcile proof blocks;
   - execute all blockers;
   - fail on missing, red, skipped, collection-failed, timeout or unexplained membership;
   - output a sufficient receipt.

4. **Make CI call that command**
   - remove retired schema keys and hard-coded counts;
   - retain faster block-specific developer commands, but make only the aggregate route promotion-authoritative.

5. **Enforce the environment**
   - consume the lock in the canonical install route;
   - add installed-package smoke proof;
   - capture environment and lock identity.

**Exit criterion:** one aggregate current Tier A result is green and reproducible; all expected-red tests are explicitly reported outside that green set; Git remains clean.

### Gate 1 — open M00 C-NORM/C-PROOF before implementation

The M00 proof family should establish these architectural laws:

1. **Dependency direction**
   - no domain module imports M00;
   - M00 consumes only declared public APIs of M01–M13;
   - legacy runtime/API internals cannot become the canonical dependency surface.

2. **Translation-only shell**
   - transport DTOs are translated to domain/public contracts;
   - no business policy, source truth or decision default is owned by M00;
   - no fabricated run, trace, scenario, packet, decision or lineage identity.

3. **Run-scoped composition**
   - clock, ID source, configuration, repositories and services are injected at the composition boundary;
   - no module-global or cached mutable domain state;
   - two consecutive runs prove no cross-run state leakage.

4. **Fail-closed authority**
   - missing mandatory authority, identity or configuration fails explicitly;
   - no fallback starting capital, timestamps, empty candidate-family substitutions or synthetic decision identity.

5. **Canonical cognition path**
   - M03 remains the prepared parent;
   - M05/M06 emit DMPV3-bearing outputs;
   - M09 joins only packet-carried upstream cognition/risk inputs;
   - no parallel hidden re-evaluation path.

6. **Hermetic integration proof**
   - one in-process paper workflow crosses M00 through the declared public module surfaces to M10/M11 and read-only M12 evidence;
   - it uses deterministic injected time/identity and local temporary stores;
   - replay semantic determinism is distinguished from occurrence identity.

7. **Legacy quarantine**
   - `DeskRuntimeOrchestrator` cannot be selected as the canonical application root;
   - compatibility tests remain nonblocking unless they assert current public compatibility rather than superseded ownership.

These tests should initially be expected-red and visible. M00 code begins only after their authority and lifecycle are admitted through the repaired control plane.

## 8. Evidence artefacts

Generated outside the repository:

- `/mnt/data/nvda_audit_module_proof_results.tsv`
- `/mnt/data/nvda_audit_control_inventory.txt`
- `/mnt/data/nvda_audit_manifest_coverage.txt`
- `/mnt/data/nvda_audit_registry_manifest_diff.txt`
- `/mnt/data/nvda_audit_api_legacy_test.log`
- `/mnt/data/nvda_audit_api_current_test.log`
- `/mnt/data/nvda_audit_tier_a_collect.log`
- `/mnt/data/nvda_audit_tier_a_full.log`
- `/mnt/data/nvda_audit_tier_a_non_vocab.log`
- `/mnt/data/nvda_audit_tier_b.log`
- `/mnt/data/nvda_audit_make_install.log`
- `/mnt/data/nvda_audit_uv_sync.log`
- individual module proof logs under `/mnt/data/nvda_audit_proof_*.log`

## 9. Unknowns and limits

- The authorised CI/package index may resolve the locked dependencies that were unavailable in this environment. This was not verified.
- M00 behaviour cannot be tested because M00 has not been implemented and no M00 proof family exists.
- The approximately 250 physical-suite failures were not each semantically adjudicated. They are **not** claimed as 250 code defects.
- Passing module-local proof establishes those asserted local propositions only; it does not establish whole-system composition.
- Diagnostic execution did not use the canonical declared environment and therefore is not a promotion receipt.

## 10. Closeout

- **Repository mutations:** none.
- **M00 execution:** not started.
- **Git state:** clean at `258470526c36da61b3ff4162f1d5ad9e512a8b54` on `work/signal-phase-dmpv3-repair-v1`.
- **Audit disposition:** `HOLD_M00_PENDING_PROMOTION_CONTROL_REPAIR`.
- **Recommended scope:** repair the control plane, then implement M00 against an admitted expected-red composition proof package. Do not reopen or rewrite accepted M01–M13 modules without a failing current proposition that requires it.
