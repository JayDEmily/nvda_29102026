# NVDA persistence-migration-lifecycle tranche v1 — executable brief
**Date:** 2026-04-20  
**Purpose:** execute the next bounded tranche after the accepted boundary-home tranche by resolving the benchmark drift around `nvda_desk.persistence.migrations` and the migration-test family without widening persistence business logic or pretending the current top-level `alembic/` placeholders are already benchmark-final.  
**Type:** executable tranche brief, not an external programme map.

---

## 1. Direct answer

The next lawful tranche is **persistence-migration-lifecycle tranche v1**.

This tranche must start from the **accepted boundary-home state**, not from the older `main` baseline that existed before the boundary tranche was audited.

Current accepted state observed directly from the supplied executed repo:
- accepted branch: `work/boundary-home-convergence-tranche-v2-20260420`
- accepted branch `HEAD`: `167fd520321ce3925ae9ebd96abe508d9af377e5`
- current `main` in the supplied repo is still older: `f54fd937c88117aa9577a175bfc22a26456396d5`
- verified proof floor at the accepted boundary-home state:
  - `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` → `88 passed`
  - `python3 -m compileall src tests/tier_a tests/tier_b` → clean

This tranche must resolve the still-missing locked benchmark family:
- `src/nvda_desk/persistence/migrations/`

It must also leave the migration-proof surface more benchmark-truthful than the current hybrid state.

This tranche is **not** allowed to widen into replay, scenarios, observability, imported-module disposition, broker integration, entry/API/ingress follow-on work, or broad persistence-domain redesign.

---

## 2. Mandatory execution setup

### 2.1 Promotion precondition before the tranche branch exists

The prior tranche has already been audited accepted.

Before opening the next tranche branch, first make the accepted boundary-home state authoritative on `main`.

That means:
- if `main` is still `f54fd937c88117aa9577a175bfc22a26456396d5`
- and the accepted boundary tranche is still on `work/boundary-home-convergence-tranche-v2-20260420` at `167fd520321ce3925ae9ebd96abe508d9af377e5`

then first promote that accepted state to `main` without changing its content.

This promotion step is **not** a leaf in this new tranche. It is baseline reconciliation required so the new tranche does not inherit an ambiguous authority branch.

If the repo arrives already promoted, verify that `main == 167fd520321ce3925ae9ebd96abe508d9af377e5` and continue.

### 2.2 Work branch for this tranche

Create exactly one tranche branch from the promoted `main` baseline at `167fd520321ce3925ae9ebd96abe508d9af377e5`:

- `work/persistence-migration-lifecycle-tranche-v1-20260420`

Do not execute this tranche on `main`.

### 2.3 Mandatory reread before touching code or tests

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
- `var/audit/reports/nvda_boundary_home_convergence_tranche_v2_report_2026-04-20.md`

### 2.4 Workbook basis for this tranche

Use the locked workbook **by lineage**, not by blindly trusting stale literal pathing.

For this tranche, the controlling workbook anchors are:
- `Target_Structure!A3:G27`
- `Ownership_Matrix!A3:H50`
- `Component_Skeleton!A3:G45`
- `Test_Architecture!A3:H20`
- `Reservations!A3:H12`
- `Module_Allocation_Appendix!A3:H67`

Most load-bearing workbook rows for this tranche:
- `Target_Structure` rows naming:
  - `nvda_desk.persistence`
  - `nvda_desk.persistence.migrations`
- `Test_Architecture` row naming:
  - `migration tests`
- `Component_Skeleton` rows naming:
  - `persistence/execution_records.py`
  - `persistence/market_observations.py`
  - `persistence/research_logs.py`
  - `persistence/module_registry.py`
- `Ownership_Matrix` rows naming:
  - execution records persistence
  - market observation persistence
  - evaluation / experiment logging
  - module registry / promotion receipts

Important nuance:
- the workbook locks a **migration-lifecycle family** under `nvda_desk.persistence.migrations`
- the live repo currently has only top-level `alembic/` placeholders and no `src/nvda_desk/persistence/migrations/`
- this tranche must resolve that drift truthfully, not cosmetically

---

## 3. Tranche objective

Converge the migration-lifecycle owner truthfully.

That means:
1. decide whether the current workbook target can be satisfied directly in code without a governance correction
2. if yes, create the missing physical benchmark-owned migration home and make the migration-lifecycle boundary explicit
3. admit only the minimum truthful proof needed so the migration family is no longer guarded only indirectly
4. keep all other persistence-domain and runtime behaviour bounded
5. close the tranche with lawful receipts and one tranche report

This tranche is about **migration-lifecycle truth**, not about broad persistence refactoring.

---

## 4. Current repo facts that this tranche must respect

Observed directly from the supplied accepted boundary-home repo state:
- `src/nvda_desk/persistence/` exists and currently contains:
  - `__init__.py`
  - `execution_records.py`
  - `models.py`
  - `session_factory.py`
- top-level `alembic/` exists and currently contains only:
  - `alembic/README.md`
  - `alembic/versions/README.md`
- there is **no** physical `src/nvda_desk/persistence/migrations/` home
- migration lifecycle is currently protected only indirectly through:
  - `tests/tier_a/options_flow_history/test_options_flow_history_persistence_surface.py`
  - retained registry references to `alembic/versions`
- persistence-adjacent repository surfaces already exist under `src/nvda_desk/repositories/`, including:
  - `execution_event_repository.py`
  - `market_observation_repository.py`
  - `options_flow_history_repository.py`
  - `position_repository.py`
  - `capital_state_repository.py`
  - `review_repository.py`
  - `research_logs.py`
  - `module_registry.py`

This tranche must not use the migration family as an excuse to reshuffle all of those domains.

---

## 5. Ordered leaves inside this tranche

Only one leaf may be active at a time.  
Each closed leaf gets its own commit on the tranche branch.

### Leaf 1 — Migration-lifecycle owner audit and admissibility decision

#### Objective
Prove whether the workbook-locked `nvda_desk.persistence.migrations` target can be satisfied truthfully in the live repo **without** a governance correction.

#### Required outcome
Produce a bounded decision for this tranche:
- **code path admissible** — proceed to Leaf 2, or
- **governance correction required** — stop the tranche after a governance leaf / carry-forward note rather than faking convergence

#### Rules
- Re-read the workbook rows listed above against the live tree and against Alembic’s existing top-level expectations.
- Do **not** assume that a top-level Alembic tool root automatically invalidates a benchmark-owned migration family.
- Do **not** assume the opposite either.
- A truthful solution may be:
  - a real `src/nvda_desk/persistence/migrations/` home with bounded ownership and compatibility to a top-level Alembic tool root, or
  - a proven governance mismatch requiring a later-numbered governance document rather than code surgery
- If the audit proves governance correction is required, stop before runtime/test churn and record the exact blocker in the tranche report and live ledger.

#### Hard stop inside the leaf
Do not widen into execution-event, market-observation, position, capital, review, research-log, or module-registry redesign in this leaf.

---

### Leaf 2 — Migration-home convergence

#### Objective
If Leaf 1 proves the code path is admissible, create the missing physical benchmark-owned migration home and make the migration-lifecycle owner explicit.

#### Required outcome
At minimum, add:
- `src/nvda_desk/persistence/migrations/__init__.py`

Add further files only if they are required to make the migration-lifecycle boundary truthful.

Possible lawful additions include a bounded locator/bridge/check surface under `src/nvda_desk/persistence/migrations/` if needed to express the relationship between the package-owned migration lifecycle and the top-level Alembic tool root.

#### Rules
- Do **not** fabricate a rich migration system that the repo does not really have.
- Do **not** move unrelated persistence business logic into the migrations home.
- Top-level `alembic/` may remain if it is still the truthful tool root.
- If `alembic/` remains, the new package home must make the ownership relationship clearer, not more ambiguous.
- If the truthful solution requires bounded documentation or manifest code inside the new home, keep it migration-lifecycle only.

#### Hard stop inside the leaf
Do not convert repository classes, ORM models, runtime sessions, or downstream services in the same leaf.

---

### Leaf 3 — Minimum truthful migration proof mirror

#### Objective
Leave the tranche with a truthful proof surface for the admitted migration-lifecycle family.

#### Required outcome
Update retained/native proof only where this tranche changed the proof surface.

#### Rules
- Prefer the smallest truthful blocker that now protects the migration-lifecycle owner explicitly.
- If the new package home would otherwise have no direct blocker, admitting a bounded migration family under Tier A is lawful here.
- Any new or revised tests must protect only migration-lifecycle invariants such as:
  - the admitted migration home exists
  - the relationship between `src/nvda_desk/persistence/migrations/` and top-level `alembic/` is explicit and bounded
  - runtime persistence packages do not silently absorb migration ownership
- `config/retained_test_registry.yaml` may be edited only to the extent required to register the truthful bounded migration blocker(s).
- Existing persistence repository tests must **not** be rewritten merely to fit code convenience.

#### Expected proof floor at tranche closeout
Run and record:
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
- `python3 -m compileall src tests/tier_a tests/tier_b`

Run the offline two-bundle `.venv` proof only if this tranche touches packaging, installability, or proof invocation assumptions rather than only package-home and migration-lifecycle ownership.

#### Hard stop inside the leaf
Do not widen into broad persistence-family expansion, replay/evaluation harness work, or specimen-path work in this tranche.

---

### Leaf 4 — Tranche closeout

#### Objective
Close the tranche lawfully and leave the next state readable.

#### Required outcome
Produce:
- one tranche report under `var/audit/reports/`
- brief lineage under `var/audit/briefs/`
- live ledger updates in `var/audit/nvda_running_audit_log.xlsx` as required by the receipt law

#### Report content must include
- whether `main` required promotion from the accepted boundary-home branch before the tranche started
- authoritative baseline commit after that promotion step
- work branch name
- per-leaf commit hashes
- touched surfaces
- proof results
- whether `src/nvda_desk/persistence/migrations/` was admitted
- whether top-level `alembic/` remained and why
- benchmark-home count movement if it changed
- exact remaining absent benchmark homes after closeout
- exact carry-forward if Leaf 1 blocked direct code convergence

---

## 6. Touched, read-only, and prohibited surfaces

### 6.1 Touched surfaces allowed in this tranche
Only these surface groups may be touched, and only when required by the ordered leaves:
- `src/nvda_desk/persistence/migrations/**`
- minimal related edits under:
  - `src/nvda_desk/persistence/__init__.py`
  - top-level `alembic/**`
- minimum truthful migration-family proof surfaces, for example:
  - `tests/tier_a/migrations/**` if admitted
  - or a bounded existing Tier A family if that is the more truthful mirror
- `config/retained_test_registry.yaml`
- `var/audit/briefs/**`
- `var/audit/reports/**`
- `var/audit/nvda_running_audit_log.xlsx`

### 6.2 Read-only surfaces
These must be treated as authority or evidence only:
- the frozen `migration_prebuild/` pack unless Leaf 1 proves a governance correction is mandatory
- the locked workbook
- `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
- previous tranche reports and accepted briefs except for storing the current brief lineage
- existing persistence runtime and repository families unless a bounded wrapper/locator relation is required for migration-lifecycle truth

### 6.3 Prohibited surfaces in this tranche
Do not touch:
- `src/nvda_desk/entry/**`
- `src/nvda_desk/ingress/**`
- `src/nvda_desk/api/**`
- `src/nvda_desk/analysis/**`
- `src/nvda_desk/observability/**`
- `src/nvda_desk/legacy/**`
- broad `src/nvda_desk/repositories/**` redesign outside a strictly necessary migration-lifecycle bridge
- serial cognition, risk, capital, downstream, and review business logic
- packaging metadata or offline bundle contents unless Leaf 3 truthfully requires the offline proof path to be revisited

---

## 7. Proof and acceptance standard

This tranche is accepted only if all of the following are true:
- the accepted boundary-home state was first made authoritative on `main`
- exactly one tranche branch was used for this tranche
- the migration-lifecycle owner truth was resolved honestly
- if the code path was admissible, `src/nvda_desk/persistence/migrations/` now exists physically
- if the code path was **not** admissible, the tranche stopped truthfully with an explicit governance/carry-forward blocker rather than faking convergence
- required proof was rerun and recorded truthfully
- the report, brief lineage, and live ledger agree with branch truth

Do not call this tranche complete merely because the tests are green.

---

## 8. Definition of done

This tranche is done only when one of these two outcomes is reached truthfully:

### Outcome A — direct code convergence succeeded
- accepted boundary-home state promoted to `main`
- `work/persistence-migration-lifecycle-tranche-v1-20260420` executed from that baseline
- `src/nvda_desk/persistence/migrations/` admitted as a truthful benchmark-owned home
- bounded migration-family proof admitted or updated truthfully
- tranche report + brief lineage + live ledger all reconciled

### Outcome B — governance blocker proved first
- accepted boundary-home state promoted to `main`
- Leaf 1 proved the workbook target cannot be satisfied truthfully in code without governance correction
- no fake package-home convergence was claimed
- tranche report + live ledger record the exact blocker and required carry-forward governance action

Anything else is incomplete.
