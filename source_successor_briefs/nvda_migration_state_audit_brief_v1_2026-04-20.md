# NVDA migration — tranche-state audit brief v1
**Date:** 2026-04-20  
**Purpose:** audit the full migration state against the current migration governance pack, the locked workbook benchmark, the retained test authority, the live ledger, and Git chronology, then produce a revised grounded view of what is already solid, what is drifting, and what remains unclosed.  
**Important execution rule:** this document is a **brief only**. Do **not** implement new runtime code, write new tests, or change governance surfaces in the same turn that creates or first reviews this brief.

---

## 1. Direct answer

The next lawful tranche is an **audit tranche**, not another code tranche.

The repo now has:
- a real migration governance pack in `migration_prebuild/`
- explicit tranche / serial leaf / commit / promotion law in `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`
- a thin live receipt surface in `var/audit/nvda_running_audit_log.xlsx`
- a current green native floor: `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` -> `76 passed`
- a clean compilation floor: `python3 -m compileall src tests/tier_a tests/tier_b`

But the current repo state has **not yet been re-audited** against that stricter tranche/leaf law.

So the next lawful work is to:
1. re-read the migration control stack in order,
2. reconcile workbook benchmark, ledger, tests, and Git chronology,
3. revise the earlier “already solid / gaps” audit against the current law,
4. identify exactly what remains open,
5. queue the next implementation tranche only after that audit is complete.

This tranche is therefore an **audit and closure-map tranche** only.

---

## 2. State basis for this brief

### 2.1 Repo state used for this brief
- branch: `work/prebuild-tranche-leaf-ledger-law-20260420`
- HEAD at brief creation: `d388864df307da9ba7e57ad9cc22e33de7b296e8`

### 2.2 Verified current floor used for this brief
Observed directly in the current repo state:
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` -> `76 passed`
- `python3 -m compileall src tests/tier_a tests/tier_b` completed without compile failure

### 2.3 Current governance surfaces relevant to this brief
Read in current repo state:
- `migration_prebuild/AGENTS.override.md`
- `migration_prebuild/00_hierarchical_order.md`
- `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`
- `migration_prebuild/02_vocabulary_dictionary_system_audit.md`
- `migration_prebuild/03_nvda_test_ordering_review_2026-04-18.md`
- `migration_prebuild/04_rebuild_execution_order.md`
- `migration_prebuild/05_nvda_final_recommendations_report_2026-04-18.md`
- `migration_prebuild/06_tier_family_normalisation.md`
- `migration_prebuild/07_wave1_truth_pass_and_completeness_2026-04-19.md`
- `migration_prebuild/08_repository_runtime_hardening_2026-04-19.md`
- `migration_prebuild/09_upstream_serial_domain_hardening_2026-04-19.md`
- `migration_prebuild/10_adapter_registry_hardening_2026-04-19.md`
- `migration_prebuild/11_completeness_matrix_all_workbook_paths_present_2026-04-19.md`
- `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
- `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`
- `var/audit/README.md`
- `var/audit/nvda_running_audit_log.xlsx`
- `config/retained_test_registry.yaml`
- `tests/AGENTS.override.md`

---

## 3. Controlling order for this tranche

This tranche must apply the following order and must say so explicitly in its output:

1. **migration governance documents** in the ordered `migration_prebuild/` stack
2. **locked workbook benchmark by lineage**, not by blindly trusting stale literal file paths
3. **live audit receipt surface** in `var/audit/`
4. **retained/native test authority and proof surfaces**
5. **runtime code and runtime-relevant files**
6. **Git chronology and branch/commit history** as tranche/leaf closure evidence

If two surfaces appear to disagree, the audit must reconcile them truthfully. It must not silently prefer stale inventory text over direct repo observation.

---

## 4. Tranche objective

Produce a grounded migration-state audit that answers these questions:

1. What is already solid in the current repo state?
2. What is partially aligned but still drifting?
3. What remains unclosed against the workbook-owned target and migration law?
4. Where does the ledger agree with live repo reality, and where does it drift?
5. Does the current Git chronology actually show lawful tranche / serial leaf closure?
6. What is the next bounded implementation tranche after this audit?

This tranche must **not** perform implementation. It exists to close state understanding before the next code tranche.

---

## 5. Ordered leaves inside this tranche

This tranche may contain multiple leaves, but only one active leaf at a time.

### Leaf 1 — control-stack reread and routing audit
Re-read the ordered migration governance pack and confirm:
- read order
- control hierarchy
- workbook routing
- ledger routing
- test/proof routing
- any duplicated or conflicting instructions

Output requirement:
- explicit statement of whether the migration governance pack is internally coherent after the new tranche/leaf law landed

### Leaf 2 — workbook and family/domain benchmark audit
Using the workbook as locked benchmark by lineage, verify:
- target structure
- family/domain decomposition
- test-architecture mirror
- whether the current repo still has major hybrid surfaces relative to the benchmark

Output requirement:
- bounded list of benchmark-aligned areas vs. still-hybrid areas

### Leaf 3 — ledger and receipt-surface audit
Audit `var/audit/nvda_running_audit_log.xlsx` and `var/audit/README.md` against live repo reality.

Check:
- whether the live sheets reflect current migration pack contents
- whether stale rows remain
- whether the new tranche/leaf receipt surface is usable and thin
- whether ledger fields are enough for stateless execution receipts

Output requirement:
- explicit agreement/drift findings for the live receipt surface

### Leaf 4 — Git chronology and tranche/leaf closure audit
Audit the active history relevant to the migration process.

Check:
- whether recent work was actually completed in serial leaves
- whether receipt updates required later reconciliation commits
- whether the branch chronology matches the governance law now in force
- where prior tranches were lawful, partial, or loose

Output requirement:
- truthful chronology judgement, not a flattering one

### Leaf 5 — revised “already solid / gaps / next tranche” matrix
Replace the prior rough state picture with a revised grounded matrix.

The matrix must separate:
- **Known true**
- **Partially aligned / drifting**
- **Not yet true**
- **Unknown until deeper tranche work**

Then queue **one** next implementation tranche only.

Output requirement:
- one bounded next tranche recommendation
- no runtime edits in the audit tranche itself

---

## 6. Hard constraints

### 6.1 Do not implement code in this tranche
This tranche must not:
- change runtime code
- add new tests
- change the workbook benchmark
- expand the migration pack
- promote new families into runtime authority

### 6.2 Do not trust prose over direct observation
If README text, workbook rows, or ledger rows disagree with the live repo tree, the audit must say so explicitly.

### 6.3 Do not collapse domains into vague summaries
If a gap belongs to a bounded family/domain, it must be named as such.

### 6.4 Do not turn the ledger into a second plan
The audit may criticise ledger drift, but it must preserve the rule that the ledger is a receipt surface only.

---

## 7. Proof and evidence requirements

The audit output must cite direct evidence from:
- file paths and line ranges where applicable
- workbook sheet names and cells where applicable
- direct Git output where applicable
- direct test/compile outputs where applicable

Claims must be labelled as one of:
- **Observed directly**
- **Inferred**
- **Unknown**

---

## 8. Stop boundary

This tranche stops when all of the following are true:
1. the full migration state has been re-audited against the current tranche/leaf law,
2. a revised grounded “solid / drifting / not yet true / unknown” matrix exists,
3. the ledger position is truthfully assessed,
4. Git chronology has been judged against the serial-leaf rule,
5. exactly one next implementation tranche is identified.

It does **not** continue into implementation.

---

## 9. Expected artefacts from execution of this brief

The future execution of this brief should produce:
- one audit report in `var/audit/reports/`
- ledger updates only if the current receipt law requires them for tranche closure
- no runtime code diffs
- no new tests
- no workbook edits

---

## 10. Reason this brief exists

The previous tranche formalised the operating law.

This tranche exists so the repo does not jump back into implementation with an outdated state picture. It forces a clean re-baseline first, then only one bounded implementation tranche after that.
