# Module 8 — recovery and closeout brief from paused supplementary state

## Purpose

This brief is for a **new stateless execution thread**.

The thread will receive only:

1. the paused repo zip  
   `NVIDIA_V7_module_8_parallel_risk_lane_supplementary_paused_state_2026-04-21.zip`

The job is to **resume from that paused state**, finish the bounded Module 8 specimen work, and then perform **one clean authoritative closeout**.

This is **not** a redesign brief.

Do **not** restart Module 8 from scratch.  
Do **not** begin normative-document rewriting in this tranche.

---

## What happened before this brief

The repo already has:

1. accepted Module 7 baseline lineage
2. substantive Module 8 branch work
3. a partially completed supplementary specimen harness
4. a receipt-closeout attempt that happened too early

The paused state is useful and must be resumed, not discarded.

---

## Mandatory execution posture

1. Work only on the existing Module 8 work branch preserved in the zip.
2. Do **not** restart from `main`.
3. Do **not** create a new design or architecture plan.
4. Do **not** rewrite normative documents in this tranche.
5. Do **not** widen Module 9, 10, or 11 beyond the minimum already allowed.
6. Do **not** implement Stage B or Stage C.
7. Do **not** turn the workbook into live runtime authority.
8. The returned repo must be a **clean committed work branch**.
9. Zip the **full repo including `.git`**.
10. Stop when done and await further instructions.

---

## Baseline you must use

After unzipping, confirm all of the following before changing anything:

1. branch: `work/module-8-parallel-risk-lane-truth-pass-20260421`
2. committed HEAD: `cd3b96a0b0318a30d35934848f37e9decb26b8a0`
3. working tree contains these useful uncommitted supplementary files:
   1. `src/nvda_desk/testing/harnesses/__init__.py`
   2. `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`
   3. `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py`

If any of those are missing, stop and report the blocker.

---

## What this tranche must do

This tranche has only two jobs:

### Job 1 — finish the bounded workbook-derived specimen path

Take the existing paused supplementary work and finish it so the repo produces:

1. one mapped `StageInputBundle`
2. one bootstrap input DMPV3 packet
3. one Stage A parallel-risk output DMPV3 packet
4. one append-only observation record
5. one bounded specimen artefact set
6. one targeted proof for that specimen path

### Job 2 — then do one final authoritative closeout

Only **after Job 1 is complete**, do one clean closeout so that:

1. the repo is clean
2. the branch is still unmerged
3. there is one authoritative packaged HEAD
4. the report and workbook agree
5. the zip handed back is audit-ready

---

## What is already correct in the paused specimen draft

Do **not** throw away the good parts.

The paused specimen harness already correctly does these things:

1. uses the governed workbook at  
   `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`
2. uses `Anchor_Data` row 7 as the primary mapping surface
3. uses `Anchor_Data!A7` as the anchor-row date
4. records field-level provenance from `Live_Web_Baseline`
5. leaves missing fields explicit instead of inventing values

Preserve those choices unless you find a direct contradiction in the governing sources.

---

## The specific date/provenance rule you must preserve

This is important.

The workbook specimen is **not** a same-moment live runtime capture.

Treat it as:

1. a **governed workbook-derived specimen**
2. using `Anchor_Data` row 7 as the primary mapping surface
3. using `Anchor_Data!A7` as the anchor-row date only
4. using `Live_Web_Baseline` field dates as field-level provenance
5. **not** collapsing mixed-date workbook fields into one fake live observation timestamp

That means:

1. do **not** choose one convenient `Live_Web_Baseline` date as packet `observed_at`
2. do **not** apply fake UTC normalisation
3. do **not** invent missing fields
4. do **not** claim the workbook is direct live runtime authority

If a field is not lawfully derivable, leave it explicit as missing.

---

## Mandatory read order before changing anything

Read these in full, in this order:

1. `AGENTS.md`
2. `migration_prebuild/00_hierarchical_order.md`
3. `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`
4. `migration_prebuild/04_rebuild_execution_order.md`
5. `migration_prebuild/05_nvda_final_recommendations_report_2026-04-18.md`
6. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
7. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`
8. `docs/01_NORMATIVE_CORE.md`
9. `docs/03_DOMAIN_MODEL_CORE.md`
10. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`
11. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
12. `docs/09_DMPV3_PROTOCOL_CORE.md`
13. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
14. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
15. `var/audit/briefs/module_8_parallel_risk_lane_implementation_brief_v2.md`
16. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`
17. `var/audit/nvda_running_audit_log.xlsx`
18. `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`
19. `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py`
20. `src/nvda_desk/contracts/packets.py`
21. `src/nvda_desk/contracts/parallel_risk.py`
22. `src/nvda_desk/contracts/stage_inputs.py`
23. `src/nvda_desk/services/parallel_risk_lane_service.py`
24. `src/nvda_desk/risk/parallel/evaluate.py`
25. `src/nvda_desk/persistence/parallel_risk_observations.py`
26. `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`

If any file output truncates, continue reading in chunks until the required source is fully read.

---

## Scope

### In scope

1. resume the paused specimen harness work
2. finish the lawful specimen mapping path
3. emit the specimen packets through the existing native Module 8 path
4. build the append-only observation record
5. write specimen artefacts and a specimen receipt
6. add the minimum targeted proof needed
7. update the Module 8 report and workbook
8. perform one final authoritative closeout

### Out of scope

1. normative-document rewrites
2. Stage B market translation implementation
3. Stage C candidate-semantics implementation
4. analytics over the observation store
5. live runtime reading from the workbook
6. live runtime reading from the new persistence store
7. widening final risk, capital deployment, or downstream operations
8. general repo cleanup unrelated to this bounded completion task

---

## Required implementation shape

### Part A — finish the specimen mapping

Using the governed workbook:

`data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`

finish the existing harness so it builds one lawful `StageInputBundle` using only the fields supported by the current native contracts.

Use:

1. `Anchor_Data` row 7 as the primary mapping row
2. `Live_Web_Baseline` only as field-level provenance
3. explicit missing fields where derivation is not lawful

The mapping must stay bounded to current admitted contracts.

### Part B — emit the specimen packets through the existing Module 8 path

Using the existing native Module 8 surfaces, emit:

1. one bootstrap input DMPV3 packet
2. one Stage A parallel-risk output DMPV3 packet
3. one append-only observation record built from the packet pair

Do this through the existing lawful builder/service path.

Do **not** hand-write fake packet JSON and call it done.

### Part C — write specimen artefacts

Write bounded artefacts under a narrow specimen home, for example:

1. `var/audit/specimens/module_8/`

Required artefacts:

1. mapped `StageInputBundle` JSON
2. bootstrap input DMPV3 packet JSON
3. Stage A output DMPV3 packet JSON
4. append-only observation record JSON
5. short specimen receipt MD

The specimen receipt must state:

1. workbook path used
2. exact sheet names used
3. exact cells / row references used
4. which fields were mapped directly
5. which fields were left missing explicitly
6. that this is a governed workbook-derived specimen, not a live admitted raw bundle

### Part D — add targeted proof

Add or extend only the minimum targeted proof needed to show:

1. the specimen mapping builds a lawful `StageInputBundle`
2. the specimen emits a lawful bootstrap DMPV3 packet
3. the specimen emits a lawful Stage A output DMPV3 packet
4. the observation record can be built from the pair
5. the specimen path does not widen live runtime authority

Record the exact targeted test files in the report before final closeout.

### Part E — only then do one final closeout

After the specimen path is complete and proofs pass:

1. update `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`
2. update `var/audit/nvda_running_audit_log.xlsx`
3. record one authoritative packaged HEAD
4. ensure the report and workbook agree
5. ensure `git status` is clean

Do **not** do receipt-only commits before the specimen work is finished.

---

## Vocabulary gate

Before adding any new durable term, check whether it is already governed.

Likely specimen terms to check:

1. workbook-derived specimen
2. packet specimen
3. workbook mapping receipt
4. reference-ledger-derived specimen

If a new durable term is not required, say so explicitly in the report.
If one is required, admit it lawfully before using it in governed surfaces.

Do not silently invent specimen terminology.

---

## Leaf structure

Use a bounded supplementary sequence. Recommended:

1. `RL1` — read / confirm paused state / vocabulary gate
2. `RL2` — finish specimen mapping
3. `RL3` — specimen packet emission and observation record
4. `RL4` — targeted tests
5. `RL5` — final authoritative closeout

Do not batch everything into one opaque commit.

---

## Receipt requirements

Maintain and return:

1. updated `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`
2. updated `var/audit/nvda_running_audit_log.xlsx`
3. one brief copy under `var/audit/briefs/`
4. the specimen artefacts
5. the specimen receipt MD

The report must include:

1. branch name
2. starting paused HEAD
3. supplementary leaf chronology
4. exact closing commit for each supplementary leaf
5. exact workbook path used
6. exact sheet / cell / row references used
7. exact specimen artefact paths
8. exact targeted proof outputs
9. final authoritative packaged HEAD
10. explicit note that normative-document rewriting was intentionally out of scope

---

## Proof requirements

After implementation is complete, rerun:

1. targeted specimen proof file(s)
2. any affected existing Module 8 targeted proof
3. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
4. compile proof  
   `python -m compileall src`

Record exact outputs in the report.

---

## Clean closeout rule

When done:

1. branch must still be `work/module-8-parallel-risk-lane-truth-pass-20260421`
2. branch must remain unmerged
3. repo must be clean
4. report and workbook must agree
5. one single authoritative packaged HEAD must be recorded
6. specimen artefacts must exist and be referenced in the report
7. no dirty working tree is allowed

---

## Definition of done

This recovery tranche is complete only if all of the following are true:

1. paused state was resumed, not discarded
2. the specimen mapping is complete
3. the bootstrap DMPV3 packet specimen exists
4. the Stage A output DMPV3 packet specimen exists
5. the append-only observation record specimen exists
6. the specimen receipt is truthful
7. targeted proof passes
8. full shell proof passes
9. compile proof is clean
10. the final repo is clean
11. the final branch is unmerged
12. one authoritative packaged HEAD is recorded in the tracked receipts

If any one of those is false, stop and report the blocker truthfully.

---

## Return requirements

Return exactly:

1. the updated repo zip including `.git`
2. a concise execution summary stating:
   1. branch name
   2. starting paused HEAD
   3. final HEAD commit
   4. whether the repo is clean
   5. targeted proof results
   6. full shell proof result
   7. exact specimen artefact paths
   8. exact workbook sheets / cells / rows used
   9. whether any blocker remains

Then stop and await further instructions.
