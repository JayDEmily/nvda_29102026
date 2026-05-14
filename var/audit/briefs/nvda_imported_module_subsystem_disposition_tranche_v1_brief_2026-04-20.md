# NVDA imported-module subsystem disposition tranche v1 brief
**Date:** 2026-04-20  
**Role:** executable tranche brief  
**Repo baseline used to draft this brief:** accepted API DTO / broker-boundary tranche repo on `work/api-dto-broker-boundary-resolution-tranche-v1-20260420` at `65f24831eb012f20b0114f63cdaab869dbcbfcc8`, with `main` still at `aa4bad4728a0ea1cfc72570337584f1c8cc11a42` pending promotion of the accepted API DTO / broker-boundary tranche  
**Directly re-used observed floor from the accepted state audit:** `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` → `100 passed`; `python3 -m compileall src tests/tier_a tests/tier_b` → clean

---

## 1. Direct instruction

Execute one bounded tranche to resolve the **imported-module subsystem reservation** truthfully.

This tranche is **not** package-home creation by default.

This tranche exists because the locked workbook keeps `nvda_desk.legacy.imported` as a **provisional / reserved** benchmark family rather than a mandatory always-admit runtime home.

The execution thread must first promote the accepted API DTO / broker-boundary tranche into `main`, then open exactly one tranche branch:

- `work/imported-module-subsystem-disposition-tranche-v1-20260420`

Do not start implementation from the currently supplied `main` until that promotion step is complete.

This tranche may end in one of only two truthful outcomes:

1. **retire / quarantine outcome** — the top-level `legacy_import/` tree is explicitly retained as historical source-evidence only, with no admitted native runtime package under `src/nvda_desk/legacy/imported/`; or
2. **bounded bridge outcome** — only if the audit proves a live native dependence that cannot be lawfully retired in this tranche, admit the minimum bounded native bridge surface under `src/nvda_desk/legacy/imported/` and keep it advisory / contained.

Default expected outcome unless direct evidence disproves it:

- **retire / quarantine outcome**

Do **not** fabricate a native imported subsystem merely to satisfy a workbook row literally.

---

## 2. Why this tranche is next

After acceptance of the API DTO / broker-boundary tranche, the remaining queue is no longer primarily about straightforward package-home creation.

Observed directly in the accepted repo state while drafting this brief:

- the remaining absent benchmark homes are:
  - `nvda_desk.legacy.imported`
  - `nvda_desk.analysis.scenarios`
  - `nvda_desk.observability`
- the workbook marks imported modules as **Provisional** in `Target_Structure` and **Reserved** in `Reservations`
- the repo already contains a large top-level `legacy_import/` tree with historical source, tests, fixtures, config, and scripts
- `tests/README.md` already says legacy test source lives under `legacy_import/tests/`
- `tests/AGENTS.override.md` already says legacy tests under `legacy_import/tests/` are **source evidence only**
- direct search over current native `src/` and `tests/` found **no live imports of `legacy_import` or `nvda_desk.legacy.imported`**
- `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` and `docs/09_DMPV3_PROTOCOL_CORE.md` still mention imported-module packet emitters as architecture / protocol concepts, so any retirement or containment decision must be explicit rather than assumed

So this tranche is a **disposition / containment tranche**, not a free-form feature tranche.

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
   - `Ownership_Matrix`
   - `Component_Skeleton`
   - `Test_Architecture`
8. the accepted API DTO / broker-boundary tranche report:
   - `var/audit/reports/nvda_api_dto_broker_boundary_resolution_tranche_v1_report_2026-04-20.md`
9. the current native and historical imported-module surfaces actually in scope:
   - `legacy_import/**`
   - any `src/` or `tests/` surfaces found by the dependence audit

Do not rely on memory or prior chat state.

---

## 4. Tranche objective

Produce one truthful disposition for the imported-module subsystem.

At tranche closeout, the repo should have:

- a direct answer about whether the imported-module subsystem is:
  - retired from native runtime ownership and quarantined as source evidence only, or
  - still needed as a bounded native advisory bridge
- explicit containment for whichever answer is truthful
- the minimum native proof mirror needed to keep that answer visible
- no silent leakage of bridge logic into native runtime ownership

This tranche must not widen into scenario work, observability work, or final whole-repo closeout.

---

## 5. Current repo facts that this tranche must respect

Observed directly while drafting this brief from the accepted API DTO / broker-boundary repo state:

- `main` is still at `aa4bad4728a0ea1cfc72570337584f1c8cc11a42`
- the accepted tranche branch is `work/api-dto-broker-boundary-resolution-tranche-v1-20260420` at `65f24831eb012f20b0114f63cdaab869dbcbfcc8`
- the final audited proof floor on that accepted state is **100 passed** and compileall clean
- there is **no** native `src/nvda_desk/legacy/imported/` package at tranche start
- there **is** a top-level `legacy_import/` tree containing:
  - `source/`
  - `tests/`
  - `fixtures/`
  - `config/`
  - `schemas/`
  - `scripts/`
- the current repo already treats legacy tests as source evidence rather than native authority
- direct native search found no current `src/` or native `tests/` imports of `legacy_import` or `nvda_desk.legacy.imported`
- review/runtime surfaces still contain bounded terminology such as `attach_imported_citations`, but not a native imported-module package

These facts mean the tranche begins from **containment / disposition uncertainty**, not from an already-admitted native subsystem.

---

## 6. Leaf queue

### Leaf 1 — dependence map and disposition audit

Produce one bounded audit note before changing runtime or proof surfaces.

Minimum required questions:

1. does any current native `src/` runtime surface import, instantiate, or depend on the top-level `legacy_import/` tree?
2. does any current native proof surface depend on the top-level `legacy_import/` tree in a way that makes retirement impossible in this tranche?
3. which imported families, if any, still have live value that is not already absorbed into native homes?
4. are the surviving imported-module references only conceptual / review-citation / DMP mention surfaces, rather than live runtime ownership?
5. is the truthful closeout state:
   - quarantine as source evidence only, or
   - minimum bounded advisory bridge?

Required output:

- one admissibility / disposition note under `var/audit/reports/`

Stop rule:

- do **not** create a native imported package in this leaf
- do **not** rewrite the historical tree in this leaf
- do **not** widen into scenarios or observability here

### Leaf 2 — disposition implementation

Implement the truthful disposition proven by Leaf 1.

#### 2A. Default expected outcome — retire / quarantine

If Leaf 1 finds no live native dependence that requires admission:

- keep `legacy_import/` as a **historical source-evidence tree**
- make that status explicit in the minimum lawful way
- do **not** create `src/nvda_desk/legacy/imported/`
- do **not** promote legacy code into native runtime just to satisfy literal package presence

Admissible implementation examples:

- a bounded top-level `legacy_import/README.md` or equivalent manifest/marker clarifying source-evidence-only status
- small containment notes or labels needed to stop future ambiguity

#### 2B. Exception outcome — bounded bridge admission

Only if Leaf 1 proves a live native dependence that cannot be lawfully retired in this tranche:

- admit the **minimum** native advisory bridge surface under `src/nvda_desk/legacy/imported/`
- keep it bounded to contracts / registry / advisory sidecars only
- do **not** let it co-reside silently inside serial runtime ownership
- do **not** promote historical breadth into a large native subsystem

If this exception is used, the tranche report must explain exactly why retirement/quarantine was false.

### Leaf 3 — minimum truthful proof mirror

Add only the minimum native proof required to keep the disposition visible.

Expected default proof shape if the result is retire / quarantine:

- one Tier A family asserting imported-module containment / non-dependence for native runtime surfaces
- retained registry admission for that family

Expected proof shape if the result is bounded bridge admission:

- one Tier A family asserting that the admitted native imported bridge remains advisory / bounded
- retained registry admission for that family

The proof may check:

- absence of native imports from the top-level `legacy_import/` evidence tree
- absence of silent runtime ownership by imported sidecars
- existence of explicit containment markers / bridge labels
- if a bridge package is admitted, that it is bounded to advisory contracts / registry style surfaces only

The proof must **not**:

- treat legacy tests as native authority
- widen into broad scenario, observability, or replay suites
- turn into full historical-tree validation

### Leaf 4 — tranche closeout

Required outputs:

- tranche report under `var/audit/reports/`
- brief copy under `var/audit/briefs/`
- ledger update in `var/audit/nvda_running_audit_log.xlsx`

The tranche report must state clearly:

- whether the imported-module subsystem closed as retired/quarantined or as bounded bridge admission
- why that answer is truthful against the current repo state
- exact proof commands and outputs
- whether `nvda_desk.legacy.imported` remains a retired benchmark reservation rather than a live native home
- any exact carry-forward note for `analysis.scenarios`, `observability`, or final closeout

---

## 7. Allowed surfaces

### 7.1 Runtime / repo surfaces allowed to change

Only these bounded surfaces may change if required by the audit:

- `legacy_import/**` — **only** for minimal containment markers / README / labels; not for broad rewrites
- `src/nvda_desk/legacy/**` — only if the exception outcome is proven and only for the minimum bounded advisory bridge surface
- narrowly adjacent package `__init__.py` files if required for truthful exports only

### 7.2 Proof surfaces allowed to change

Only these proof surfaces may change if needed:

- new bounded Tier A tests under `tests/tier_a/legacy_imported/`
- or another clearly bounded Tier A location if that is the more truthful native home for the containment family
- `config/retained_test_registry.yaml`

### 7.3 Audit / receipt surfaces allowed to change

- `var/audit/briefs/`
- `var/audit/reports/`
- `var/audit/nvda_running_audit_log.xlsx`

---

## 8. Prohibited surfaces

Do **not** touch:

- `src/nvda_desk/analysis/scenarios/**`
- `src/nvda_desk/observability/**`
- `src/nvda_desk/api/**`
- `src/nvda_desk/entry/**`
- `src/nvda_desk/ingress/**`
- `src/nvda_desk/testing/harnesses/**`
- `src/nvda_desk/runtime/**`
- broad `contracts/**` redesign
- replay/evaluation package work
- broker or API DTO follow-on work
- mass deletions or broad rewrites across the historical `legacy_import/` tree
- new third-party dependencies
- caches, venvs, or unrelated repo hygiene work

Do **not** change tests merely to fit current code if the hierarchy points the other way.

Do **not** admit a native imported package for cosmetic benchmark-home reasons only.

---

## 9. Proof commands required at closeout

Run and record at minimum:

### 9.1 Targeted tranche proof

Use the exact targeted paths corresponding to the admitted new or changed Tier A family for imported-module containment or bounded bridge truth.

### 9.2 Tranche proof floor

```bash
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b
python3 -m compileall src tests/tier_a tests/tier_b
```

This tranche does **not** require a full whole-repo end-to-end V&V programme.

---

## 10. Definition of done

This tranche is done only when all of the following are true:

1. the accepted API DTO / broker-boundary tranche has first been promoted to `main`
2. the tranche branch used is exactly `work/imported-module-subsystem-disposition-tranche-v1-20260420`
3. the dependence/disposition audit note exists and is truthful
4. the imported-module subsystem has one explicit truthful disposition:
   - retired / quarantined, or
   - bounded bridge admission
5. the minimum proof mirror exists and is admitted in the retained registry
6. `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` passes
7. `python3 -m compileall src tests/tier_a tests/tier_b` is clean
8. the tranche report, brief copy, and live ledger are updated truthfully
9. no prohibited surface was widened
10. no legacy test was treated as native authority

If the truthful answer is retirement/quarantine, that is fully admissible even though the workbook once named `nvda_desk.legacy.imported` as a provisional target family.

---

## 11. Direct instruction to the execution thread

Execute this tranche exactly as written.

Use one tranche branch only.
Use one active leaf at a time.
Use one commit per closed leaf.
Do not start the next leaf before the current leaf is fully closed and recorded.
Do not widen scope for convenience.
Do not fabricate a native imported subsystem merely to satisfy a spreadsheet literal.
When complete, return the updated repo zip and the tranche report.
