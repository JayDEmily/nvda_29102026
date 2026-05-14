# Temporal standard program — tranche 2 execution brief v1
## Conformance audit and proof-surface remediation only

## Purpose

This brief executes **Tranche 2 — conformance audit and proof-surface remediation** of the temporal-standard program.

This brief is self-contained on purpose.
It does **not** depend on any external planning note or master brief file being present inside the repo.

This tranche has two jobs only:

1. perform a **full repo-wide temporal conformance audit** across the currently active rebuilt surfaces
2. remediate the **governor / proof / targeted test layer only where that can be done truthfully without code remediation**

This tranche does **not** perform the large code/persistence remediation work. That belongs to Tranche 3.

This is an **audit-plus-proof tranche**, not a runtime implementation tranche.

---

## Baseline to use

Use this accepted repo zip as the required starting baseline:

- `NVIDIA_V7_temporal_standard_tranche_1_normative_admission_2026-04-22.zip`

Required starting state after unzip:

1. branch: `work/temporal-standard-tranche-1-normative-admission-20260422`
2. committed HEAD: `912ade700d4516551404c437c06660632b1dc479`
3. repo clean: yes
4. authoritative closeout tag present:
   `temporal-standard-tranche-1-authoritative-closeout-20260422`

Create the new tranche branch from that exact state.

Required new branch name:

- `work/temporal-standard-tranche-2-conformance-audit-proof-remediation-20260422`

If the provided repo is not actually on:
1. branch `work/temporal-standard-tranche-1-normative-admission-20260422`
2. clean HEAD `912ade700d4516551404c437c06660632b1dc479`
3. with tag `temporal-standard-tranche-1-authoritative-closeout-20260422`

stop immediately and report the blocker before doing any other work.

---

## Program context this tranche must obey

This tranche is **step 2 and the proof-facing part of step 3** in the temporal-standard program order:

1. admit the temporal law
2. audit the repo against it
3. fix proof/test/governor surfaces
4. fix code and persistence surfaces
5. run final repo-wide conformance audit
6. close out cleanly

This tranche does:

1. the full conformance inventory
2. the proof/governor remediation that can be done truthfully now

This tranche does **not** do the code/persistence remediation itself.

The blueprint/workbook remains the **anti-drift ownership benchmark**, not the primary temporal-law authority.

---

## Mandatory execution posture

1. Work on the new tranche branch only.
2. Do **not** merge to `main`.
3. Do **not** change runtime code, packet builders, persistence code, harness code, or replay code in this tranche, except the minimum proof-only support surfaces if and only if they are required to express the audit truthfully and do not change runtime behaviour.
4. Do **not** widen Module 8 Stage B/C, Module 9, Module 10, or Module 11.
5. Read all required governing files and all required audited source files **in full** before changing anything.
6. If output truncates, continue reading in chunks until the required source is fully read.
7. Return a **clean committed work branch** zip including `.git`.
8. Use the authoritative closeout-tag pattern at the end of the tranche.
9. One active leaf at a time.

This tranche is successful only if it stays narrow.

---

## Blocker discipline — mandatory

If a blocker is encountered, the executor must:

1. **stop immediately**
2. **make no further changes**
3. **not improvise**
4. **not keep reading onward “just to see”**
5. **not partially execute later leaves**
6. **not create substitute assumptions or substitute baselines**
7. **return the exact blocker with evidence**

A blocker includes, at minimum:

1. wrong baseline repo identity
2. missing required files named by the brief
3. missing required tags/branches
4. inability to state L1 declarations exactly
5. vocabulary admission not possible in scope
6. inability to classify an active temporal surface truthfully
7. proof-floor impossibility caused by the provided baseline
8. any instruction conflict between the brief and the actual repo contents

The executor is **not** allowed to “wing it”, “keep going anyway”, or “work around it silently”.

---

## Anti-shortcut / anti-path-to-green discipline — mandatory

The executor must not optimise for:

1. the smallest apparent audit set
2. the fastest route to green proofs
3. the smallest vocabulary delta
4. the fewest affected surfaces
5. the least reading work
6. the shortest route to a superficially plausible answer

Instead, the executor must optimise for:

1. exact brief conformance
2. exact hierarchy order
3. full required reading
4. sequential completion of required work
5. truthful receipts
6. explicit preservation of scope boundaries

If this brief says **at minimum** certain surfaces, tests, or reports must be handled, the executor must handle **all of them**.
The executor is not allowed to reduce that set because a smaller set would be easier or more efficient.

Green proofs do **not** excuse skipped required work.

---

## Outcome target

At the end of this tranche, the repo must contain:

1. a complete temporal conformance inventory for the currently active rebuilt surfaces
2. explicit classification of each audited surface as:
   1. already conformant
   2. needs proof/test remediation only
   3. needs code/persistence remediation in Tranche 3
   4. reserved / blocked
3. the proof/test/governor surfaces updated only where that can be done truthfully now
4. explicit receipts for every surface that must be deferred to Tranche 3
5. one clean authoritative closeout for this tranche

And the tranche must **not**:

1. silently remediate runtime code
2. silently remediate persistence code
3. start unfinished module work
4. fake conformance through weak tests or hand-wavy classifications

---

## Mandatory read order before changing anything

Read these in full, in this order.

### Control surfaces

1. `AGENTS.md`
2. `migration_prebuild/00_hierarchical_order.md`
3. `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`
4. `migration_prebuild/04_rebuild_execution_order.md`
5. `migration_prebuild/05_nvda_final_recommendations_report_2026-04-18.md`
6. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
7. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`

### Core normative docs

8. `docs/01_NORMATIVE_CORE.md`
9. `docs/03_DOMAIN_MODEL_CORE.md`
10. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`
11. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
12. `docs/05.1_GUARDRAILS_WORKING.md`
13. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
14. `docs/09_DMPV3_PROTOCOL_CORE.md`
15. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
16. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
17. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
18. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`

### Accepted module reports and active audit surfaces

19. `var/audit/2026-04-21_module_3_preparation_truth_pass_report.md`
20. `var/audit/2026-04-21_module_4_cognition_ingress_truth_pass_report.md`
21. `var/audit/2026-04-21_module_7_dmpv3_packet_carriage_truth_pass_report.md`
22. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`
23. `var/audit/2026-04-22_module_6_serial_spine_truth_pass_report.md`
24. `var/audit/2026-04-22_temporal_standard_tranche_1_normative_admission_report.md`
25. `var/audit/nvda_running_audit_log.xlsx`

### Active rebuilt source surfaces to audit in full

#### Module 3 / Preparation
26. every file under `src/nvda_desk/preparation/`

#### Module 4 / Cognition ingress
27. every file under `src/nvda_desk/cognition/ingress/`
28. `src/nvda_desk/contracts/stage_inputs.py`

#### Module 7 / DMP packet carriage
29. `src/nvda_desk/contracts/packets.py`
30. `src/nvda_desk/packets/dmp_packets.py`

#### Module 8 / Parallel-risk bootstrap + persistence + specimen
31. `src/nvda_desk/contracts/parallel_risk.py`
32. `src/nvda_desk/services/parallel_risk_lane_service.py`
33. `src/nvda_desk/risk/parallel/evaluate.py`
34. every file under `src/nvda_desk/domain/parallel_risk/`
35. `src/nvda_desk/persistence/parallel_risk_observations.py`
36. every file under `src/nvda_desk/testing/harnesses/`

#### Module 6 / Serial spine
37. `src/nvda_desk/runtime/orchestrator.py`
38. every file under `src/nvda_desk/cognition/serial/`
39. every file under `src/nvda_desk/domain/temporal/`
40. every file under `src/nvda_desk/domain/regime/`
41. every file under `src/nvda_desk/domain/options_flow/`
42. every file under `src/nvda_desk/domain/posture/`
43. every file under `src/nvda_desk/domain/eligibility/`
44. every file under `src/nvda_desk/domain/execution/`
45. `src/nvda_desk/contracts/temporal.py`
46. `src/nvda_desk/contracts/regime.py`
47. `src/nvda_desk/contracts/options_flow.py`

### Existing proof/test surfaces to audit in full

48. every file under `tests/tier_a/vocabulary/`
49. every file under `tests/tier_a/packets/`
50. every file under `tests/tier_a/parallel_risk/`
51. every file under `tests/tier_a/runtime/`
52. every file under `tests/tier_a/testing_harnesses/`
53. every file under `tests/tier_a/persistence/`
54. every file under `tests/tier_b/review_lineage/`

Do not start changing anything until the full read is complete.

---

## Vocabulary gate

Before auditing or changing proof surfaces:

1. check whether any new durable temporal-conformance term is actually required
2. likely terms to check include:
   1. temporal conformance inventory
   2. conformant
   3. needs proof remediation only
   4. needs code remediation
   5. reserved / blocked
   6. source_time_raw
   7. source_time_kind
   8. source_time_utc
   9. source_date
   10. captured_at_utc
   11. persisted_at_utc
   12. source_provider
   13. source_channel
   14. time_granularity
3. if a term is already governed, use it lawfully
4. if a term is not governed and is required as a durable term, admit it lawfully in the same tranche before using it in governed surfaces
5. if lawful admission is not possible in scope, stop and report the blocker

Do **not** silently invent conformance terminology.

---

## Mandatory L1 declarations before any audit or proof work

In **L1**, before any implementation leaf starts, record in the tranche report:

1. the exact active source surfaces to be inventoried
2. the exact proof/test files to be audited
3. the exact conformance classification headings to be used
4. the exact workbook sheet names and row numbers being used only as anti-drift ownership references, if any are cited in the report
5. explicit statement that this tranche is:
   1. **audit-first**
   2. **proof/governor remediation only where truthful now**
   3. **no runtime code remediation**

If any of those L1 items cannot be stated exactly, stop and report the blocker before doing further work.

---

## Scope

### In scope

1. full temporal conformance inventory across the active rebuilt surfaces listed above
2. truthful classification of every audited surface
3. proof/test/governor remediation only where that remediation can be done truthfully without code remediation
4. receipts for all surfaces that must be deferred to Tranche 3
5. update the tranche report and live audit workbook
6. create the authoritative closeout tag for this tranche

### Out of scope

1. runtime code remediation
2. persistence code remediation
3. harness/specimen logic remediation
4. packet-builder logic remediation
5. unfinished runtime module work
6. blueprint rewrites
7. provider-specific implementation logic

If a surface needs code changes to conform, classify it and defer it to Tranche 3.
Do **not** fix it in this tranche.

---

## Required audit and classification work

You must build one explicit conformance inventory covering all active rebuilt surfaces listed in the read order.

For every audited surface, classify it as exactly one of:

1. **already conformant**
2. **needs proof/test remediation only**
3. **needs code/persistence remediation in Tranche 3**
4. **reserved / blocked**

For each classification entry, record:

1. surface path
2. temporal fields/concepts present
3. temporal rule(s) from Tranche 1 that apply
4. current conformance status
5. why that classification is truthful
6. next action, if any

Do not leave surfaces unclassified.

---

## Required proof/governor remediation rule

You may change proof/test surfaces only when one of these is true:

1. the code is already conformant and the test surface is stale or incomplete
2. the code is already conformant and a missing proof surface must be added
3. a governor/proof surface can be corrected without changing runtime behaviour

You must **not**:

1. write tests that pretend nonconformant code is conformant
2. weaken tests just to make green easy
3. add failing forward-looking tests for Tranche 3 work and call that “done”
4. change runtime code under cover of “test remediation”

If a surface needs runtime changes to become conformant, record it for Tranche 3 instead of faking proof in Tranche 2.

---

## Required output artefacts

This tranche must create:

1. `var/audit/2026-04-22_temporal_standard_tranche_2_conformance_audit_report.md`
2. one explicit temporal conformance inventory table inside that report
3. updates to `var/audit/nvda_running_audit_log.xlsx`
4. `var/audit/briefs/` copy of this brief

If needed for clarity, you may also create one bounded machine-readable audit artefact under:

- `var/audit/temporal_conformance_inventory.json`

But only if it exactly mirrors the report and does not replace it.

---

## Required leaf structure

Use this exact bounded leaf sequence unless a blocker prevents it:

1. `L1-read-vocabulary-and-scope-declarations`
2. `L2-full-conformance-inventory`
3. `L3-proof-governor-remediation-only`
4. `L4-report-workbook-proof-and-clean-closeout`

One active leaf at a time.  
Do not batch everything into one opaque commit.

---

## Receipt requirements

Maintain and return:

1. `var/audit/briefs/` copy of this brief
2. `var/audit/2026-04-22_temporal_standard_tranche_2_conformance_audit_report.md`
3. updates to `var/audit/nvda_running_audit_log.xlsx`

The report must include:

1. branch name
2. baseline commit
3. leaf chronology
4. exact closing commit for each leaf
5. vocabulary decisions
6. exact surfaces audited
7. exact conformance classifications for each surface
8. exact proof/test files changed, if any
9. explicit statement that runtime code remediation remained out of scope
10. exact authoritative closeout ref name
11. proof outputs
12. final authoritative packaged HEAD or authoritative closeout ref pattern, consistent with the closeout rule below

The report must not rely on “hand-back summary” placeholders.

---

## Proof requirements

After the final receipt-reconciliation commit, rerun exactly:

1. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

2. compile proof  
   `python -m compileall src`

Record exact outputs in the report.

If proof/governor surfaces were updated, that rerun must reflect those changes truthfully.

---

## Authoritative closeout mechanism — mandatory

Use this exact pattern:

1. make one final bounded receipt/closeout commit on the tranche branch
2. create one annotated Git tag named:

`temporal-standard-tranche-2-authoritative-closeout-20260422`

3. the tag must point to the final clean closeout commit
4. tracked receipts must record that exact authoritative closeout ref name
5. do **not** use:
   1. “recorded in hand-back summary”
   2. “exact hash reported in hand-back summary”
   3. self-reference placeholder wording

This closeout mechanism is mandatory.

---

## Branch and packaging requirements

1. Leave the branch as `work/temporal-standard-tranche-2-conformance-audit-proof-remediation-20260422`
2. Leave the branch unmerged
3. The final repo must be **clean**
4. The final repo must include the annotated tag:
   `temporal-standard-tranche-2-authoritative-closeout-20260422`
5. Zip the **full repo including `.git`**
6. Return:
   1. the updated repo zip
   2. a concise execution summary with:
      1. branch name
      2. baseline commit
      3. final HEAD
      4. authoritative closeout ref name
      5. exact tag target commit
      6. whether the repo is clean
      7. proof results
      8. exact surfaces audited
      9. exact proof/test files changed, if any
      10. classification counts by category

---

## Definition of done

Tranche 2 is complete only if all of the following are true:

1. it started from the exact accepted Tranche 1 baseline
2. every active rebuilt temporal surface named by this brief was read and classified
3. the conformance inventory is complete
4. any proof/governor remediation performed is truthful and does not change runtime behaviour
5. all surfaces needing runtime/persistence remediation are explicitly receipted for Tranche 3
6. the tranche remained audit/proof-only
7. report is complete
8. workbook is complete
9. report and workbook agree
10. the authoritative closeout tag exists and points to the final clean commit
11. proofs rerun clean
12. repo is clean
13. branch is unmerged

If any one of those is false, stop and report the blocker truthfully.
