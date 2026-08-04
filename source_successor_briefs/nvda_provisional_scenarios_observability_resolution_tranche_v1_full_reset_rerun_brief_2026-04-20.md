# NVDA provisional scenarios / observability resolution tranche v1 — full reset and rerun brief

**Type:** corrective reset + full rerun brief  
**Date:** 2026-04-20  
**Audience:** execution thread  
**Controlling repo input:** the uploaded repo zip that contains the failed supplemental-fix attempt  
**Purpose:** discard the contaminated repair attempt, return to the last accepted baseline, and re-execute the tranche cleanly with the original substantive scope and stricter full-read / truthful-receipt requirements.

---

## 1. Direct instruction

This brief has two parts and both are mandatory.

### Part A — reset
Discard the defective corrective attempt as the active execution path.

### Part B — rerun
Re-execute the original provisional scenarios / observability tranche cleanly from the last accepted baseline.

Do **not** band-aid the failed supplemental-fix branch.  
Do **not** preserve or reuse invented chronology from the failed supplemental-fix report or ledger rows.  
Do **not** redesign the tranche.

Return:

1. an updated repo zip
2. a concise execution summary stating:
   - exact starting baseline
   - exact rerun branch
   - exact final `HEAD`
   - exact leaf commit hashes
   - exact proof outputs
   - whether the failed supplemental-fix branch was superseded rather than repaired in place

---

## 2. Why this brief exists

The original tranche outcome was substantively correct, but the first execution violated one-leaf / one-commit law.  
The supplemental-fix attempt then failed harder by:

- not actually re-executing from `main`
- preserving the old defective history
- writing report / ledger chronology that was not truthful to Git

That means the only clean repair is:

- reset to the last accepted baseline
- create a new rerun branch
- re-execute the tranche serially
- populate report and ledger only from real commits on that rerun branch

---

## 3. Mandatory full read before any change

Read all of the following **in full** before touching runtime, proof, report, ledger, or Git state.

Chunked reading is allowed.  
Sampling is **not** allowed.  
Do **not** self-authorise “relevant parts only”.

### 3.1 Governing repo sources
1. `AGENTS.md`
2. `migration_prebuild/AGENTS.override.md`
3. ordered `migration_prebuild/` pack through `14_frozen_authority_and_mutability_law_2026-04-20.md`
4. `var/audit/README.md`
5. `tests/AGENTS.override.md`
6. `config/retained_test_registry.yaml`

### 3.2 Tranche-specific sources
7. `var/audit/briefs/nvda_provisional_scenarios_observability_resolution_tranche_v1_brief_2026-04-20.md`
8. `var/audit/reports/nvda_provisional_scenarios_observability_resolution_tranche_v1_report_2026-04-20.md`
9. `var/audit/reports/nvda_provisional_scenarios_observability_resolution_tranche_v1_admissibility_note_2026-04-20.md`
10. `nvda_provisional_scenarios_observability_resolution_tranche_v1_supplemental_fix_brief_2026-04-20.md` if present in-repo; otherwise use the uploaded supplemental brief as read-only reference

### 3.3 Workbook sources
11. `var/audit/nvda_running_audit_log.xlsx` — read the workbook in full, including the tranche receipt sheet and summary sheets, before changing it
12. locked benchmark workbook sheets relevant to this tranche — read in full:
   - `Target_Structure`
   - `Reservations`
   - `Test_Architecture`
   - `Seam_Contracts`

### 3.4 Native repo surfaces directly relevant to the tranche
13. `src/nvda_desk/analysis/replay/**`
14. `tests/tier_a/analysis/test_replay_evaluation_surface.py`
15. `tests/tier_a/observability/test_observability_reservation_surface.py` if already present
16. any current native runtime or proof surfaces that mention `scenarios` or `observability`

Do not begin Part A or Part B until this full read is complete.

---

## 4. Part A — reset / rollback law

### 4.1 Accepted baseline
The last accepted baseline is:

- `main` at `5a0bafb74b0a512cd32efae548501b1366d9b161`

This is the only lawful starting point for the rerun.

### 4.2 Failed branch treatment
Treat these as contaminated evidence branches, not active repair surfaces:

- `work/provisional-scenarios-observability-resolution-tranche-v1-20260420`
- `work/provisional-scenarios-observability-resolution-tranche-v1-fix-20260420`

Do **not** continue work on either branch.  
Do **not** amend their commits.  
Do **not** try to “correct” their existing report/ledger narrative in place.

### 4.3 New rerun branch
Create a fresh rerun branch from the accepted baseline:

- `work/provisional-scenarios-observability-resolution-tranche-v1-rerun-20260420`

### 4.4 Reset outcome
At the end of Part A, the active work branch must have:

- merge-base against `main` = `5a0bafb74b0a512cd32efae548501b1366d9b161`
- no parentage through either contaminated branch
- no reuse of invented corrective hashes from the failed supplemental attempt

Part A does **not** require deleting old branch refs.  
It requires ceasing to use them and superseding them with a clean rerun branch.

Commit for Part A:
- no dedicated runtime commit required
- the proof of reset is the new branch ancestry and the explicit statement in the final report

---

## 5. Part B — rerun of the original tranche with tightened execution rules

The substantive target remains the original brief’s target:

- `src/nvda_desk/analysis/scenarios/` remains absent unless a truthful bounded admission is proven
- `src/nvda_desk/observability/` remains absent unless a truthful bounded admission is proven

Expected default outcome remains:

- `analysis.scenarios` → reserved / containment
- `observability` → reserved / containment

Given the accepted audit history so far, the expected lawful rerun outcome is still:

- no new native runtime package homes
- bounded proof/reporting only

### Tightened rules for this rerun
1. **Read order is binding.** Full reads above are mandatory.
2. **One active leaf at a time.** No parallel work.
3. **One closed leaf = one commit.** No exceptions.
4. **Report and ledger may cite only hashes that actually exist in Git on the rerun branch.**
5. **No post-closeout narrative repair commit** unless the closeout leaf itself lawfully requires one and that leaf is named in advance.
6. **Do not infer workbook irrelevance.** The workbook is in scope for this tranche.
7. **Do not widen runtime scope.** This remains a reservation-resolution / containment tranche.

---

## 6. Mandatory rerun leaf queue

### L1 — admissibility note refresh
Refresh the admissibility note from the clean rerun branch and accepted baseline.

Allowed surfaces:
- `var/audit/reports/nvda_provisional_scenarios_observability_resolution_tranche_v1_admissibility_note_2026-04-20.md`
- live workbook receipt surfaces only if the governing law requires receipt recording at this point

Required outcome:
- note states the clean rerun branch
- note states the accepted baseline
- note states the truthful current disposition basis for `analysis.scenarios` and `observability`

Commit: **one commit for L1 only**

### L2 — analysis scenarios reserved-absence disposition
Recreate only the `analysis.scenarios` reserved-absence proof shape.

Allowed surfaces:
- `tests/tier_a/analysis/test_replay_evaluation_surface.py`
- `config/retained_test_registry.yaml` only for the bounded analysis-scenarios-related entries if needed
- live workbook receipt surfaces only if required by the governing law

Required outcome:
- `analysis.scenarios` absence remains explicit and truthful
- no `src/nvda_desk/analysis/scenarios/` package is created

Commit: **one commit for L2 only**

### L3 — observability reserved-absence disposition
Recreate only the `observability` reserved-absence proof shape.

Allowed surfaces:
- `tests/tier_a/observability/test_observability_reservation_surface.py`
- `config/retained_test_registry.yaml` only for the bounded observability-related entries if needed
- live workbook receipt surfaces only if required by the governing law

Required outcome:
- `observability` absence remains explicit and truthful
- no `src/nvda_desk/observability/` package is created

Commit: **one commit for L3 only**

### L4 — tranche closeout report
Write the tranche report for the rerun.

Allowed surfaces:
- `var/audit/reports/nvda_provisional_scenarios_observability_resolution_tranche_v1_report_2026-04-20.md`

Required content:
- exact accepted baseline
- exact rerun branch name
- exact L1 / L2 / L3 commit hashes from the rerun branch
- proof outputs
- clear statement that this rerun supersedes both earlier defective attempts
- no invented or missing commit hashes

Commit: **one commit for L4 only**

### L5 — final receipt reconciliation / brief storage / closeout
Finish the live ledger and any brief-storage reconciliation required by repo law.

Allowed surfaces:
- `var/audit/nvda_running_audit_log.xlsx`
- `var/audit/briefs/` only if the brief copy needs reconciliation

Required outcome:
- receipt surfaces cite only real rerun-branch hashes
- prior contaminated chronology is superseded, not mixed into the rerun narrative
- if a closeout row cannot truthfully carry its own final hash in the same commit, use the repo’s already-admitted receipt rule rather than inventing a hash

Commit: **one commit for L5 only**

---

## 7. Prohibitions

Do **not**:

- create `src/nvda_desk/analysis/scenarios/`
- create `src/nvda_desk/observability/`
- widen into API / entry / ingress / persistence / testing harnesses / runtime / legacy imported work
- merge L2 and L3 into one commit
- continue on top of either contaminated branch
- cite non-existent hashes in report or workbook
- say a file was reviewed in full unless it actually was
- treat the workbook as optional or “relevant parts only”

---

## 8. Proof requirements

Run these at minimum before final closeout:

```bash
PYTHONPATH=src pytest -q \
  tests/tier_a/analysis/test_replay_evaluation_surface.py \
  tests/tier_a/observability/test_observability_reservation_surface.py
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b
python3 -m compileall src tests/tier_a tests/tier_b
```

Report exact outputs.

---

## 9. Acceptance criteria

This brief is satisfied only if **all** of the following are true:

1. the rerun branch starts from `main` at `5a0bafb74b0a512cd32efae548501b1366d9b161`
2. the rerun branch does not inherit active repair chronology from the contaminated branches
3. substantive reserved outcomes are unchanged
4. `analysis.scenarios` and `observability` remain absent from native runtime
5. L1, L2, L3, L4, and L5 each have their own real commits
6. the report truthfully records the rerun chronology
7. the live ledger truthfully records the rerun chronology
8. Tier A+B passes
9. compileall is clean

If any one of the above is false, this rerun is not complete.

---

## 10. Definition of done

Done means:

- the contaminated supplemental-fix path is superseded
- the tranche is re-executed cleanly from the accepted baseline
- the substantive reserved outcome remains unchanged
- the rerun chronology is real and visible in Git, report, and ledger
- the repo is returned as an updated zip
