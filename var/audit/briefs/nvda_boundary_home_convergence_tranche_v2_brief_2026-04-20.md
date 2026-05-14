# NVDA boundary-home-convergence tranche v2 — executable brief
**Date:** 2026-04-20  
**Purpose:** execute the next bounded implementation tranche from the current closed `main` state by converging the next locked benchmark homes at the runtime boundary: `nvda_desk.entry`, `nvda_desk.ingress`, and the benchmark API module cut required to support them.  
**Type:** executable tranche brief, not an external programme map.

---

## 1. Direct answer

The next lawful tranche is **boundary-home convergence tranche v2**.

It must start from:
- authoritative branch: `main`
- baseline commit: `f54fd937c88117aa9577a175bfc22a26456396d5`
- current verified floor at brief creation:
  - `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` → `82 passed`
  - `python3 -m compileall src tests/tier_a tests/tier_b` → clean

This tranche must create or lawfully converge the next locked benchmark-owned boundary homes:
- `src/nvda_desk/entry/`
- `src/nvda_desk/ingress/`
- benchmark API cut required to support them:
  - `src/nvda_desk/api/app.py`
  - `src/nvda_desk/api/deps.py`

This tranche is **not** allowed to widen into replay, scenarios, observability, imported-module disposition, persistence migrations, broker integration, or downstream policy expansion.

---

## 2. Mandatory execution setup

### 2.1 Work branch
Create exactly one tranche branch from `main` at `f54fd937c88117aa9577a175bfc22a26456396d5`:

- `work/boundary-home-convergence-tranche-v2-20260420`

Do not execute this tranche on `main`.

### 2.2 Mandatory reread before touching code
Read the governing migration pack in order, headed by:
- `AGENTS.md`
- `migration_prebuild/AGENTS.override.md`

Then reread the ordered migration documents under `migration_prebuild/` through:
- `00_hierarchical_order.md`
- `01_nvda_best_practice_blueprint_v3_final.xlsx`
- `02_vocabulary_dictionary_system_audit.md`
- `03_nvda_test_ordering_review_2026-04-18.md`
- `04_rebuild_execution_order.md`
- `05_nvda_final_recommendations_report_2026-04-18.md`
- `06_tier_family_normalisation.md`
- `07_wave1_truth_pass_and_completeness_2026-04-19.md`
- `08_repository_runtime_hardening_2026-04-19.md`
- `09_upstream_serial_domain_hardening_2026-04-19.md`
- `10_adapter_registry_hardening_2026-04-19.md`
- `11_completeness_matrix_all_workbook_paths_present_2026-04-19.md`
- `12_future_brief_and_carry_forward_law_2026-04-19.md`
- `13_tranche_leaf_commit_promotion_law_2026-04-20.md`
- `14_frozen_authority_and_mutability_law_2026-04-20.md`

Also reread:
- `var/audit/README.md`
- `var/audit/nvda_running_audit_log.xlsx`
- `config/retained_test_registry.yaml`
- `tests/AGENTS.override.md`
- `var/audit/reports/nvda_migration_state_audit_report_v1_2026-04-20.md`
- `var/audit/reports/nvda_benchmark_home_convergence_tranche_v1_report_2026-04-20.md`

### 2.3 Workbook basis for this tranche
Use the locked workbook **by lineage**, not by blindly trusting stale literal pathing.

For this tranche, the controlling workbook anchors are:
- `Target_Structure!A3:G27`
- `Ownership_Matrix!A3:H38`
- `Component_Skeleton!A3:G39`
- `Test_Architecture!A3:H20`
- `Reservations!A3:H12`

Most load-bearing target rows for this tranche:
- `Target_Structure` rows naming `nvda_desk.entry`, `nvda_desk.api`, `nvda_desk.ingress`, `nvda_desk.preparation`, `nvda_desk.cognition.ingress`
- `Component_Skeleton` rows naming:
  - `entry/asgi.py`
  - `entry/cli.py`
  - `api/app.py`
  - `api/deps.py`
  - `ingress/raw_bundle_loader.py`
- `Test_Architecture` rows naming:
  - config authority separation
  - reference vs ingress separation
  - preparation seam
  - ingress translation

---

## 3. Tranche objective

Converge the next locked benchmark boundary homes **without feature invention**.

That means:
1. create the missing physical homes for `entry` and `ingress`
2. reconcile the API module cut so boundary bootstrap is benchmark-shaped rather than hidden under `api/http/app.py`
3. preserve truthful ownership boundaries between:
   - reference vs ingress
   - ingress vs preparation
   - API wiring vs runtime orchestration
4. admit only the minimum proof needed so the new boundary homes are not unguarded
5. close the tranche with lawful receipts and one report

---

## 4. Current repo facts that this tranche must respect

Observed directly from the current repo state at `f54fd93`:
- current boundary-related live surfaces include:
  - `src/nvda_desk/api/http/app.py`
  - `src/nvda_desk/adapters/ingress/calendar_feed.py`
  - `src/nvda_desk/adapters/ingress/market_snapshot_feed.py`
  - `src/nvda_desk/adapters/ingress/options_surface_feed.py`
  - `src/nvda_desk/preparation/runtime_preparer.py`
  - `src/nvda_desk/cognition/ingress/*.py`
  - `src/nvda_desk/runtime/orchestrator.py`
- physical homes already converged in the previous tranche include:
  - `src/nvda_desk/config/`
  - `src/nvda_desk/cognition/modifiers/`
  - `src/nvda_desk/calendar/reference/`
  - `src/nvda_desk/calendar/operational/`
- the still-absent locked benchmark homes include:
  - `src/nvda_desk/entry/`
  - `src/nvda_desk/ingress/`
- the current API cut is still hybrid because the repo has `src/nvda_desk/api/http/app.py` rather than the benchmark-owned `src/nvda_desk/api/app.py` and `src/nvda_desk/api/deps.py`

This tranche must reduce that drift and stop there.

---

## 5. Ordered leaves inside this tranche

Only one leaf may be active at a time.  
Each closed leaf gets its own commit on the tranche branch.

### Leaf 1 — API boundary module-cut convergence

#### Objective
Create the benchmark-owned API boundary cut needed for entry composition.

#### Required outcome
Add:
- `src/nvda_desk/api/__init__.py` if absent
- `src/nvda_desk/api/app.py`
- `src/nvda_desk/api/deps.py`

#### Rules
- `api/app.py` must own route registration / app wiring at the bounded rebuild-phase level only.
- `api/deps.py` must own dependency composition at the bounded rebuild-phase level only.
- Do **not** invent a richer web stack than the repo currently has.
- `src/nvda_desk/api/http/app.py` may remain only as a thin compatibility wrapper if needed.
- If the truthful current boundary is still a minimal shell, preserve that minimal shell; do not fabricate route families or external framework complexity.

#### Hard stop inside the leaf
Do not open broker DTO expansion, route proliferation, auth, persistence injection growth, or API feature work.

---

### Leaf 2 — Entry home convergence

#### Objective
Create the physical benchmark-owned `entry` home and move or wrap bootstrap responsibility into it.

#### Required outcome
Add:
- `src/nvda_desk/entry/__init__.py`
- `src/nvda_desk/entry/asgi.py`
- `src/nvda_desk/entry/cli.py`

#### Rules
- `entry/asgi.py` must be the truthful runtime/bootstrap surface for API app creation.
- `entry/cli.py` must be a truthful bounded CLI bootstrap surface only.
- Do **not** invent replay or eval command behaviour that depends on not-yet-converged homes such as `analysis.replay` or `analysis.scenarios`.
- If only a smaller lawful CLI surface is currently possible, implement the smaller truthful surface and record the carry-forward explicitly in the tranche report.
- Runtime orchestration must remain owned by `src/nvda_desk/runtime/orchestrator.py` unless a purely boundary-level wrapper is required.

#### Hard stop inside the leaf
Do not turn this leaf into replay tooling, evaluation tooling, or deployment-system work.

---

### Leaf 3 — Ingress home convergence

#### Objective
Create the physical benchmark-owned `ingress` home and move admitted raw-bundle/source-decode ownership into it without contaminating reference authority.

#### Required outcome
Add:
- `src/nvda_desk/ingress/__init__.py`
- `src/nvda_desk/ingress/raw_bundle_loader.py`

#### Rules
- `ingress/raw_bundle_loader.py` must own only admitted raw bundle / source decode responsibility.
- It must remain clearly upstream of `preparation/runtime_preparer.py` and `cognition/ingress/*.py`.
- It must **not** absorb calendar reference ownership from `src/nvda_desk/calendar/reference/`.
- `src/nvda_desk/adapters/ingress/market_snapshot_feed.py` and `src/nvda_desk/adapters/ingress/options_surface_feed.py` may remain only as thin wrappers if compatibility is needed.
- `src/nvda_desk/adapters/ingress/calendar_feed.py` must remain reference-boundary only; do not reclassify calendar reference import as runtime ingress.
- If the current repo lacks typed raw bundle contracts, admit only the minimum truthful contract/model surface needed for the new home. Keep it bounded to ingress and do not widen packet, replay, or runtime logic in the same leaf.

#### Hard stop inside the leaf
Do not open preparation feature derivation, cognition-stage logic, or reference bundle redesign.

---

### Leaf 4 — Minimum truthful proof mirror for touched boundary homes

#### Objective
Leave the tranche with a truthful proof surface for the new homes and the touched boundaries, without inflating test scope.

#### Required outcome
Update retained/native proof only where the tranche actually changed the proof surface.

#### Rules
- Prefer updating existing bounded families over admitting new families **unless** a touched benchmark-owned home would otherwise have no truthful blocker.
- Minimum proof scope may include only what this tranche actually touched:
  - API/entry bootstrap surface presence and bounded composition
  - ingress raw-bundle loader surface
  - reference vs ingress separation where the ingress and calendar wrappers meet
  - ingress → preparation seam truth where ownership moved
- Do **not** open replay/specimen-path, imported-module, persistence migration, or observability proof families here.
- Any retained-test-registry edits must remain bounded to the touched families only.

#### Expected proof floor at tranche closeout
Run and record:
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
- `python3 -m compileall src tests/tier_a tests/tier_b`

Run the offline two-bundle `.venv` proof only if this tranche touches packaging, installability, or proof invocation assumptions.

---

### Leaf 5 — Tranche closeout

#### Objective
Close the tranche lawfully and leave the next state readable.

#### Required outcome
Produce:
- one tranche report under `var/audit/reports/`
- brief lineage under `var/audit/briefs/` if required by the current repo law
- live ledger updates in `var/audit/nvda_running_audit_log.xlsx` as required by the receipt law

#### Report content must include
- baseline branch and commit
- work branch name
- per-leaf commit hashes
- touched surfaces
- proof results
- benchmark-home count movement if it changed
- exact remaining absent benchmark homes after tranche closeout
- exact carry-forward created by the tranche

---

## 6. Touched, read-only, and prohibited surfaces

### 6.1 Expected touched surfaces
At minimum, expect touch only within these bounded areas if the tranche proceeds lawfully:
- `src/nvda_desk/api/`
- `src/nvda_desk/entry/`
- `src/nvda_desk/ingress/`
- thin compatibility wrappers only where required:
  - `src/nvda_desk/api/http/app.py`
  - `src/nvda_desk/adapters/ingress/*.py`
- directly adjacent runtime boundary files only if strictly required by composition:
  - `src/nvda_desk/runtime/orchestrator.py`
  - `src/nvda_desk/preparation/runtime_preparer.py`
- only the minimum directly-caused proof files and retained-test-registry lines
- tranche receipt/report surfaces under `var/audit/`

### 6.2 Read-only mandatory surfaces
Do not rewrite these except as the repo’s routing law permits:
- `migration_prebuild/` pack
- locked workbook benchmark
- core normative docs under `docs/`
- already-closed audit reports except for new report creation

### 6.3 Prohibited surfaces in this tranche
Do not touch:
- `src/nvda_desk/analysis/`
- `src/nvda_desk/legacy/`
- `src/nvda_desk/observability/`
- `src/nvda_desk/persistence/migrations/`
- broker live-boundary work
- replay/scenario work
- downstream policy expansion
- coefficient-authority expansion beyond current admitted surfaces
- frozen governance document content except as a lawful governance leaf, which this tranche is not

---

## 7. Truth rules for this tranche

1. Do not change tests merely to fit existing code.
2. Do not fabricate richer runtime behaviour than the current repo can truthfully support.
3. Do not move reference authority into ingress.
4. Do not let API composition become a hiding place for runtime orchestration or broker logic.
5. If a benchmark module cut cannot be satisfied truthfully without opening a different governed objective, stop and report the blocker rather than smearing tranches together.
6. Runtime code is the truth surface when docstrings diverge, but hierarchy still applies: governance and admitted proof outrank convenience edits.
7. Any new durable term must obey the vocabulary workflow before admission.

---

## 8. Evidence requirements

The execution report for this tranche must label claims as:
- **Observed directly**
- **Inferred**
- **Unknown**

And must back material claims with:
- file paths and line ranges where applicable
- workbook sheet names and cells where applicable
- direct proof outputs
- Git commit hashes for each closed leaf

---

## 9. Stop boundary

This tranche stops when all of the following are true:
1. `entry` exists physically as a truthful boundary home
2. `ingress` exists physically as a truthful boundary home
3. the API cut needed to support them exists at `api/app.py` and `api/deps.py` or a truthful blocker is declared
4. only the minimum necessary proof mirror has been updated
5. the full native proof floor is green
6. tranche receipts and one report are written

This tranche does **not** continue into:
- persistence migration truth
- replay/specimen-path convergence
- DTO/broker reservation resolution
- imported-module disposition
- provisional architecture refinement
- final whole-programme closeout

---

## 10. Expected artefacts from execution of this brief

At lawful completion, expect:
- one updated repo branch containing serial leaf commits
- one tranche report, suggested filename:
  - `var/audit/reports/nvda_boundary_home_convergence_tranche_v2_report_2026-04-20.md`
- brief lineage stored in-repo if the current audit-law requires it, suggested filename:
  - `var/audit/briefs/nvda_boundary_home_convergence_tranche_v2_brief_2026-04-20.md`
- updated live receipt workbook
- updated repo zip for handoff back to the audit thread

---

## 11. Reason this brief exists

`T06` closed the first benchmark-home convergence tranche and moved the repo from `13 / 24` to `17 / 24` benchmark homes physically present.

The next highest-confidence locked drift is now at the system boundary.

This tranche exists to reduce that drift before moving into persistence migration truth, replay/evaluation convergence, DTO/broker reservation resolution, or later provisional architecture work.
