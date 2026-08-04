# NVDA provisional scenarios / observability resolution tranche v1 brief
**Date:** 2026-04-20  
**Role:** executable tranche brief  
**Repo baseline used to draft this brief:** accepted imported-module subsystem disposition tranche repo on `work/imported-module-subsystem-disposition-tranche-v1-20260420` at `5a0bafb74b0a512cd32efae548501b1366d9b161`, with `main` still at `65f24831eb012f20b0114f63cdaab869dbcbfcc8` pending promotion of the accepted imported-module tranche  
**Directly re-used observed floor from the accepted state audit:** `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` → `102 passed`; `python3 -m compileall src tests/tier_a tests/tier_b` → clean

---

## 1. Direct instruction

Execute one bounded tranche to resolve the two remaining **provisional benchmark families** still absent as native homes:

- `nvda_desk.analysis.scenarios`
- `nvda_desk.observability`

This tranche is a **reservation-resolution / containment tranche**, not free-form feature work.

The execution thread must first promote the accepted imported-module tranche into `main`, then open exactly one tranche branch:

- `work/provisional-scenarios-observability-resolution-tranche-v1-20260420`

Do not start implementation from the currently supplied `main` until that promotion step is complete.

This tranche may end in only truthful outcomes for each family:

1. **bounded admission outcome** — admit the minimum native package home only if the audit proves a real bounded owner already exists in current native behaviour and can be admitted without fabricating capability; or
2. **reserved / containment outcome** — keep the family absent as a native package in this tranche, make the absence explicit in proof/reporting, and carry the resolved reservation into final closeout.

Default expected outcomes unless direct evidence disproves them:

- `nvda_desk.analysis.scenarios` → **reserved / containment outcome**
- `nvda_desk.observability` → **reserved / containment outcome**

Do **not** create package homes merely to make the workbook look more literally complete.

---

## 2. Why this tranche is next

After acceptance of the imported-module disposition tranche, the remaining benchmark-home question is no longer broad migration. It is the truthful disposition of the last two absent **provisional** families.

Observed directly in the accepted repo state while drafting this brief:

- benchmark-home count after accepted imported-module closeout remains **21 / 24**
- the remaining absent benchmark homes are:
  - `nvda_desk.legacy.imported` — now explicitly retired / quarantined rather than an open live-home question
  - `nvda_desk.analysis.scenarios`
  - `nvda_desk.observability`
- the workbook marks:
  - `nvda_desk.analysis.scenarios` as **Provisional** in `Target_Structure`
  - `nvda_desk.observability` as **Provisional** in `Target_Structure`
  - `Observability package exact shape` as **Provisional** in `Reservations`
- the current native replay tranche already asserts that replay remains outside scenarios and that `src/nvda_desk/analysis/scenarios/` is absent
- direct search across current native `src/` and native Tier A / Tier B tests found no existing native `observability` package and no clear structured-logging / metrics owner that would justify admission by default
- current scenario mentions are bounded to contracts, review lineage, and specimen-path metadata rather than an admitted scenario subsystem home

So this tranche is a **truth-resolution tranche** for the last two open provisional families before final closeout.

---

## 3. Governing sources to reread before work

Read these in full before touching runtime, proof, or receipt surfaces:

1. repo-root `AGENTS.md`
2. `migration_prebuild/AGENTS.override.md`
3. ordered `migration_prebuild/` pack through `14_frozen_authority_and_mutability_law_2026-04-20.md`
4. `var/audit/README.md`
5. `config/retained_test_registry.yaml`
6. `tests/AGENTS.override.md`
7. the workbook sheets relevant to this tranche:
   - `Target_Structure`
   - `Reservations`
   - `Test_Architecture`
   - `Seam_Contracts`
8. the accepted imported-module tranche report:
   - `var/audit/reports/nvda_imported_module_subsystem_disposition_tranche_v1_report_2026-04-20.md`
9. the current native surfaces directly relevant to this tranche:
   - `src/nvda_desk/analysis/replay/**`
   - `src/nvda_desk/testing/harnesses/canonical_runtime.py`
   - `src/nvda_desk/contracts/trace_review.py`
   - any current runtime or proof surfaces found by the admissibility audit that mention scenarios or observability

Do not rely on memory or prior chat state.

---

## 4. Tranche objective

Produce one truthful disposition for the two remaining provisional benchmark families.

At tranche closeout, the repo should have:

- a direct answer about whether `analysis.scenarios` becomes a bounded native home now or remains a resolved reserved absence
- a direct answer about whether `observability` becomes a bounded native home now or remains a resolved reserved absence
- the minimum native proof mirror needed to keep those answers visible
- no silent feature inflation into scenario engines, metrics stacks, or logging frameworks
- a clear carry-forward state for final closeout

This tranche must not widen into final whole-repo reconciliation. It exists to remove ambiguity before that closeout.

---

## 5. Current repo facts that this tranche must respect

Observed directly while drafting this brief from the accepted imported-module repo state:

- `main` is still at `65f24831eb012f20b0114f63cdaab869dbcbfcc8`
- the accepted tranche branch is `work/imported-module-subsystem-disposition-tranche-v1-20260420` at `5a0bafb74b0a512cd32efae548501b1366d9b161`
- the final audited proof floor on that accepted state is **102 passed** and compileall clean
- `src/nvda_desk/analysis/replay/` exists and is already protected by Tier A proof asserting it stays analysis-only and outside scenarios
- `src/nvda_desk/analysis/scenarios/` does **not** exist at tranche start
- `src/nvda_desk/observability/` does **not** exist at tranche start
- current native references to scenario concepts are bounded to trace/review contracts and specimen-path metadata; no admitted `analysis.scenarios` package owner exists yet
- current native search found no admitted structured logging / metrics / correlation helper package that would justify default `observability` admission

These facts mean the tranche begins from **provisional reservation uncertainty**, not from already-admitted package homes.

---

## 6. Leaf queue

### Leaf 1 — admissibility reread for the two provisional families

Produce one bounded admissibility note before changing runtime or proof surfaces.

Minimum required questions:

1. does any current native runtime or admitted proof surface require a distinct `analysis.scenarios` package home right now, or are current scenario mentions still bounded metadata / analysis containment only?
2. does any current native runtime or admitted proof surface require a distinct `observability` package home right now, or would admission fabricate capability?
3. if either family is admitted, what is the **minimum bounded owner** that can be created without inventing a large subsystem?
4. if either family remains absent, what exact proof/reporting surface keeps that absence explicit and non-ambiguous?

Required output:

- one admissibility note under `var/audit/reports/`

Stop rule:

- do **not** create package homes in this leaf
- do **not** widen replay into scenario orchestration here
- do **not** introduce logging / metrics frameworks here

### Leaf 2 — `analysis.scenarios` disposition

Implement the truthful disposition proven by Leaf 1.

#### 2A. Default expected outcome — reserved / containment

If Leaf 1 finds no live bounded owner that requires admission now:

- keep `src/nvda_desk/analysis/scenarios/` absent in this tranche
- preserve the current truth that replay/evaluation remains outside scenarios
- make that absence explicit only through bounded proof/reporting, not by inventing a placeholder package

#### 2B. Exception outcome — bounded native admission

Only if Leaf 1 proves a current native bounded owner already exists and admission would reduce ambiguity without inventing new behaviour:

- admit the **minimum** native package under `src/nvda_desk/analysis/scenarios/`
- keep it bounded to analysis-only scenario schemas / helper services / experiment surfaces
- do **not** introduce live trading ownership, broad scenario engines, or replay/CLI/API widening

If this exception is used, the tranche report must explain exactly why continued absence was false.

### Leaf 3 — `observability` disposition

Implement the truthful disposition proven by Leaf 1.

#### 3A. Default expected outcome — reserved / containment

If Leaf 1 finds no live bounded owner that requires admission now:

- keep `src/nvda_desk/observability/` absent in this tranche
- keep structured logging / metrics / audit correlation as resolved reservation rather than fabricated subsystem
- make that absence explicit only through bounded proof/reporting

#### 3B. Exception outcome — bounded native admission

Only if Leaf 1 proves a current native bounded owner already exists and admission would reflect actual code rather than create new capability:

- admit the **minimum** native package under `src/nvda_desk/observability/`
- keep it bounded to logging helpers, metric emitters, or correlation helpers only
- do **not** let it own business decisions, packet mutation, persistence rules, or runtime orchestration

If this exception is used, the tranche report must explain exactly why continued absence was false.

### Leaf 4 — minimum truthful proof mirror

Add only the minimum native proof required to keep the two dispositions visible.

Expected default proof shape from the current evidence:

- keep or minimally extend the existing Tier A replay-analysis family that already asserts `analysis.scenarios` absence if that family remains truthful
- add only the minimum bounded Tier A proof needed to keep `observability` absence / containment explicit
- admit any new proof family or blocker in `config/retained_test_registry.yaml`

If one of the two families is admitted instead of kept absent:

- add only the minimum Tier A proof asserting the admitted package stays within its bounded owner shape

The proof must **not**:

- widen into broad scenario simulation suites
- widen into logging/metrics integration stacks
- create whole-repo V&V
- replace truthful absence with cosmetic package checks

### Leaf 5 — tranche closeout

Required outputs:

- tranche report under `var/audit/reports/`
- brief copy under `var/audit/briefs/`
- ledger update in `var/audit/nvda_running_audit_log.xlsx`

The tranche report must state clearly:

- whether `analysis.scenarios` closed as bounded admission or resolved reserved absence
- whether `observability` closed as bounded admission or resolved reserved absence
- why those answers are truthful against the current repo state
- exact proof commands and outputs
- the resulting benchmark-home count after closeout
- the exact carry-forward state for final benchmark reconciliation / promotion closeout

---

## 7. Allowed surfaces

### 7.1 Runtime / repo surfaces allowed to change

Only these bounded surfaces may change if required by the audit:

- `src/nvda_desk/analysis/scenarios/**` — only if the exception admission outcome is proven
- `src/nvda_desk/observability/**` — only if the exception admission outcome is proven
- narrowly adjacent package `__init__.py` files if required for truthful exports only

Default expected outcome: **no new runtime package homes are created**.

### 7.2 Proof surfaces allowed to change

Only these proof surfaces may change if needed:

- existing bounded Tier A analysis containment family under `tests/tier_a/analysis/**`
- new bounded Tier A observability containment family if truly needed, for example under `tests/tier_a/observability/**`
- `config/retained_test_registry.yaml`

### 7.3 Audit / receipt surfaces allowed to change

- `var/audit/briefs/`
- `var/audit/reports/`
- `var/audit/nvda_running_audit_log.xlsx`

---

## 8. Prohibited surfaces

Do **not** touch:

- `src/nvda_desk/api/**`
- `src/nvda_desk/entry/**`
- `src/nvda_desk/ingress/**`
- `src/nvda_desk/persistence/**`
- `src/nvda_desk/testing/harnesses/**`
- `src/nvda_desk/runtime/**`
- `src/nvda_desk/legacy/**`
- `legacy_import/**`
- broad `contracts/**` redesign
- whole-repo architecture rewrites
- final closeout artefacts beyond truthful carry-forward notes

Do **not** reopen imported-module disposition in this tranche.

---

## 9. Required proof commands

At minimum, run and record:

```bash
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b
python3 -m compileall src tests/tier_a tests/tier_b
```

Also run any targeted tranche proof introduced by Leaf 4.

Do not claim success without the direct outputs.

---

## 10. Definition of done

This tranche is done only when:

1. the accepted imported-module tranche has first been promoted into `main`
2. one admissibility note exists for the two provisional families
3. `analysis.scenarios` has a truthful disposition (bounded admission or resolved reserved absence)
4. `observability` has a truthful disposition (bounded admission or resolved reserved absence)
5. the minimum truthful proof mirror exists and is admitted in the retained registry if changed
6. Tier A + Tier B proof is green
7. compileall is clean
8. tranche report, brief copy, and live ledger are updated truthfully
9. the tranche report states the exact carry-forward state for the final benchmark reconciliation / promotion closeout tranche

If the truthful result is that both families remain absent as resolved reservations, that is acceptable **only if** the report and proof make that state explicit and non-cosmetic.
