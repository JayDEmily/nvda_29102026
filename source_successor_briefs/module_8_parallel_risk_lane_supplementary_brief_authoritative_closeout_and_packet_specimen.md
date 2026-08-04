# Module 8 — supplementary brief for authoritative closeout and governed packet specimen

## Purpose

This supplementary brief exists to do **two things only** on the existing Module 8 work branch:

1. close out Module 8 with **one clean authoritative packaged HEAD**
2. create **one bounded governed-workbook-derived Module 8 packet specimen** using the native Module 8 DMPV3 path that now exists

Do **not** reopen Module 8 design, vocabulary design, Stage B, Stage C, analytics, or live persistence consumption.

This is a bounded follow-on brief, not a redesign brief.

---

## Baseline

Use the submitted Module 8 branch as the starting point.

Expected branch:

`work/module-8-parallel-risk-lane-truth-pass-20260421`

Expected current submitted HEAD before this supplementary work:

`4adbf969c7133e0627cf3b0566027ab662e9ae4c`

If the repo handed to you does not match that branch lineage, stop and report the blocker.

---

## Why this supplementary brief exists

### A. Receipt closeout gap

The current submitted Module 8 branch is substantively strong, but the tracked receipt surfaces still do **not** record one single authoritative packaged HEAD cleanly.

Observed current receipt issue:

1. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md` records `L5` as `SELF_REFERENCE_LIMITATION_AUTHORITATIVE_PACKAGED_HEAD`
2. `var/audit/nvda_running_audit_log.xlsx` records the same limitation token for Module 8 `L5`
3. the actual packaged Git HEAD is `4adbf969c7133e0627cf3b0566027ab662e9ae4c`

That is the same closeout ambiguity pattern that had to be corrected for Module 7.

### B. Packet specimen gap

The current Module 8 branch now has a lawful **bootstrap DMPV3 packet path**, but it still does **not** produce one concrete governed-workbook-derived specimen artefact that a human can inspect.

The user specifically wants one proper packet emitted “in the way that now exists”.

This supplementary brief therefore adds:

1. one bounded **specimen builder / harness**
2. one bounded **specimen receipt**
3. one bounded **specimen packet artefact set**

This specimen must be clearly labelled as:

- **reference-ledger-derived**
- **bounded specimen**
- **not direct live runtime authority**
- **not a claim that the workbook is a full canonical raw runtime bundle**

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
15. `docs/planning/2026-04-02_GATE160_GOVERNED_SIGNAL_COEFFICIENT_REFERENCE_WORKBOOK_LAW.md`
16. `docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.md`
17. `docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.json`
18. `var/audit/briefs/module_8_parallel_risk_lane_implementation_brief_v2.md`
19. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`
20. `var/audit/nvda_running_audit_log.xlsx`
21. `src/nvda_desk/contracts/packets.py`
22. `src/nvda_desk/contracts/parallel_risk.py`
23. `src/nvda_desk/contracts/stage_inputs.py`
24. `src/nvda_desk/contracts/temporal.py`
25. `src/nvda_desk/contracts/regime.py`
26. `src/nvda_desk/contracts/options_flow.py`
27. `src/nvda_desk/services/parallel_risk_lane_service.py`
28. `src/nvda_desk/risk/parallel/evaluate.py`
29. `src/nvda_desk/persistence/parallel_risk_observations.py`
30. `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`

If workbook inspection output truncates, continue reading in chunks until the required surfaces are fully inspected.

---

## Scope

### In scope

1. authoritative clean closeout of Module 8 receipt surfaces
2. one governed-workbook-derived specimen Stage Input Bundle mapping
3. one lawful bootstrap input DMPV3 packet emitted from that specimen
4. one lawful Stage A parallel-risk output DMPV3 packet emitted from that specimen
5. one append-only observation record built from that specimen pair
6. one bounded script / harness / fixture path that reproduces that specimen deterministically
7. one targeted proof for the specimen path
8. updated report and workbook receipts

### Out of scope

1. widening live runtime to read the workbook directly
2. changing Module 3 / 4 / 6 runtime emitters
3. Stage B market translation implementation
4. Stage C candidate-semantics implementation
5. analytics over the observation store
6. live read-back from the observation store
7. changing final risk / capital / downstream consumers
8. pretending the workbook is a full canonical raw runtime bundle

---

## Design constraints that must be preserved

1. The workbook remains a **governed live reference ledger**, not direct runtime authority.
2. The specimen is a **bounded reference-ledger-derived packet specimen**, not a live admitted runtime capture.
3. The specimen must use the **existing lawful native Module 8 packet path** rather than inventing a parallel one.
4. Missing raw truth must remain explicit.
5. The specimen may manually promote workbook values into typed contracts, but that promotion must be:
   1. explicit
   2. receipted
   3. lineaged to workbook sheet/cell/row references
6. No live module may begin reading the workbook directly as a runtime shortcut.

---

## Required implementation shape

### Part 1 — authoritative closeout repair

Create one supplementary closeout commit sequence on the existing Module 8 branch so that:

1. the repo remains on `work/module-8-parallel-risk-lane-truth-pass-20260421`
2. the repo ends **clean**
3. the final packaged HEAD is **one single authoritative closeout commit**
4. the report and workbook record that authoritative packaged HEAD truthfully
5. the self-reference limitation is stated explicitly, but the tracked receipt surfaces must still identify the authoritative packaged HEAD in the same way Module 7 was eventually normalised

Do not return another ambiguous `SELF_REFERENCE_LIMITATION_AUTHORITATIVE_PACKAGED_HEAD` token as the final tracked closeout identity.

### Part 2 — governed-workbook-derived specimen mapping

Build one deterministic specimen mapping using the canonical governed workbook:

`data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`

Required source policy:

1. prefer `Live_Web_Baseline` as the real reference seed surface
2. use `Anchor_Data` as the row-wise anchored handoff surface where needed
3. do **not** use `Synthetic_Raw` as if it were the one real seed
4. record the exact sheet names and exact cell or row references used
5. if a needed field is absent from the workbook, leave it explicit as missing rather than inventing it

Required mapping target:

Build one `StageInputBundle` using only the fields lawfully supported by the current typed contracts:

1. `TemporalContextInput`
2. `MarketRegimeContextInput`
3. `OptionsFlowContextInput`

The mapping must be explicit and receipted.

Examples of lawful current target fields include:

1. temporal:
   1. `observed_at`
   2. `next_event_at`
   3. bounded event windows if lawfully derivable
2. regime:
   1. `nvda_return_pct`
   2. `nq_return_pct`
   3. `vix_level`
   4. `missing_fields`
3. options flow:
   1. `spot_price`
   2. `front_dte`
   3. `next_dte`
   4. `missing_fields`

If one of those fields is not lawfully derivable from the workbook surfaces inspected, record it in `missing_fields` rather than inventing a proxy.

### Part 3 — specimen packet emission

Using the existing native Module 8 service path, emit:

1. one bootstrap input DMPV3 packet
2. one Stage A parallel-risk output DMPV3 packet
3. one append-only observation record built from that packet pair

The specimen path must run through the **existing native builder/service surfaces**, not a fake JSON hand-write.

Use:

1. `ParallelRiskLaneService.build_bootstrap_input_packet(...)`
2. `ParallelRiskLaneService.evaluate(...)` or `run_bootstrap(...)`
3. `build_parallel_risk_observation_record(...)`

### Part 4 — specimen artefacts

Write deterministic artefacts to a bounded non-normative artefact home. Use one of these if already suitable, otherwise create the narrowest truthful equivalent:

1. `var/audit/specimens/module_8/`
2. `var/audit/specimens/parallel_risk/`

Required artefacts:

1. one JSON file for the mapped `StageInputBundle`
2. one JSON file for the bootstrap input DMPV3 packet
3. one JSON file for the Stage A output DMPV3 packet
4. one JSON file for the append-only observation record
5. one short MD receipt explaining:
   1. workbook path used
   2. sheets/cells/rows used
   3. which fields were mapped directly
   4. which fields were left missing explicitly
   5. that this is a governed-workbook-derived specimen and not a live admitted raw bundle

### Part 5 — lineage requirement for the specimen

The specimen packet lineage must explicitly carry workbook origin in a bounded truthful way.

Use the existing DMPV3 lineage / extension surfaces. At minimum, the specimen receipts must make it obvious:

1. which workbook file was the source reference
2. which sheets/cells/rows were used
3. that the specimen was manually promoted from governed workbook reference, not from direct runtime capture

Do this through lawful lineage / extension metadata and the specimen receipt, not by inventing a new hidden side channel.

---

## Vocabulary gate

Before implementing the specimen path, check whether any new durable terms are required.

Likely terms to check:

1. workbook-derived specimen
2. reference-ledger-derived specimen
3. workbook mapping receipt
4. packet specimen

If no new durable term is required, record that truthfully.
If a new durable term is required, admit it lawfully through the existing vocabulary workflow before using it in governed surfaces.

Do not silently invent specimen terminology.

---

## Test gate

Add or update only the minimum targeted proof needed for this supplementary work.

At minimum, prove:

1. the specimen mapping builds a lawful `StageInputBundle`
2. the specimen emits a lawful bootstrap DMPV3 packet
3. the specimen emits a lawful Stage A output DMPV3 packet
4. the observation record can be built from the pair
5. the specimen path does not widen live runtime authority
6. the repo remains clean and the receipt closeout is authoritative

Record the exact targeted test files in the supplementary report before implementation.

---

## Required leaf structure

Use a bounded supplementary leaf sequence. Recommended:

1. `SL1-closeout-receipt-normalisation`
2. `SL2-workbook-specimen-mapping`
3. `SL3-specimen-emission-and-observation-record`
4. `SL4-tests-proof-and-authoritative-closeout`

Do not batch everything into one opaque commit.

---

## Receipt requirements

Create and maintain:

1. updated `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`
2. updated `var/audit/nvda_running_audit_log.xlsx`
3. one brief copy under `var/audit/briefs/`
4. one specimen receipt MD under the specimen artefact home

The updated Module 8 truth-pass report must add:

1. the supplementary leaf chronology
2. the authoritative packaged HEAD
3. the exact workbook source path
4. the exact sheet/cell/row mapping used
5. the exact artefact paths written
6. the exact targeted proofs rerun

---

## Proof requirements

After the supplementary work, rerun:

1. the targeted specimen proof file(s)
2. the existing targeted Module 8 packet / persistence / lineage proof family as affected
3. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
4. compile proof  
   `python -m compileall src`

Record exact outputs in the report.

---

## Clean closeout rule

When done:

1. the branch must remain `work/module-8-parallel-risk-lane-truth-pass-20260421`
2. the branch must remain unmerged
3. the final packaged repo must be **clean**
4. there must be one single authoritative packaged HEAD
5. the report and workbook must agree on that packaged HEAD
6. the specimen artefacts must exist and be referenced in the report
7. no dirty working tree is allowed

---

## Definition of done

This supplementary brief is complete only if all of the following are true:

1. Module 8 closeout ambiguity is resolved
2. one authoritative packaged HEAD is recorded truthfully
3. the repo is clean
4. one governed-workbook-derived specimen mapping exists
5. one lawful bootstrap input DMPV3 packet specimen exists
6. one lawful Stage A output DMPV3 packet specimen exists
7. one append-only observation record specimen exists
8. the specimen receipt explains source sheets/cells/rows and missing fields truthfully
9. no live runtime module was widened to read the workbook directly
10. proofs rerun clean

If any one of those is false, stop and report the blocker truthfully.

---

## Return requirements

Return exactly:

1. the updated repo zip including `.git`
2. a concise execution summary stating:
   1. branch name
   2. base commit
   3. final HEAD commit
   4. repo clean or not
   5. targeted proof results
   6. full shell proof result
   7. exact specimen artefact paths
   8. exact workbook sheets/cells/rows used
   9. whether any blocker remains

Then stop and await further instructions.
