# Module 8 — Parallel risk lane implementation brief v2

## Purpose

This brief advances **Module 8 — Parallel risk lane** only.

The safe plan is fixed and non-negotiable:

1. rebuild the native parallel risk lane as a lawful **DMPV3 input/output** runtime path
2. add **write-only parallel-risk persistence wiring only**
3. defer analytics
4. defer live read-back from the new persistence store
5. keep the serial spine stateless
6. do not widen Module 9, Module 10, or Module 11 beyond explicitly allowed glue

This brief is written to prevent scope drift.  
Do not interpret aspirational future design as mandatory current implementation.

---

## Mandatory execution posture

1. Work on a **new work branch only**.
2. Do **not** merge to `main`.
3. Do **not** close the branch.
4. Do **not** improvise outside scope.
5. Read all required governing sources **in full** before changing anything.
6. If output truncates, continue reading in chunks until the required file is fully read.
7. The returned repo must be a **clean committed work branch**.
8. Zip the **full repo including `.git`**.
9. Stop when done and await further instructions.

---

## Baseline

This Module 8 tranche must start from the **accepted Module 7 closeout state**.

Required baseline:

1. branch lineage source: `work/module-7-dmpv3-packet-carriage-truth-pass-20260421`
2. accepted authoritative closeout commit: `27bc66c360ea258b3a5798b813f1130a432bd97f`

Create the new Module 8 work branch from that exact accepted Module 7 closeout state.

Required new branch name:

`work/module-8-parallel-risk-lane-truth-pass-20260421`

If the provided repo is not actually based on the accepted Module 7 closeout state, stop and report that as a blocker.

---

## Outcome target

At the end of this tranche, the repo must truthfully support all of the following:

1. the native parallel risk lane has one lawful **bootstrap DMPV3 input** path
2. the native parallel risk lane emits one lawful **bootstrap DMPV3 output** path
3. the lane remains bounded to **independent parallel-risk / environment-assessment meaning**
4. the lane preserves explicit lineage, dependency packet IDs, and stage-read state for the implemented bootstrap path
5. the lane has a **parallel-risk-owned write-only persistence seam**
6. that persistence seam is **append-only / receiptable**
7. no analytics are installed over that persistence seam yet
8. no live decision logic reads from that persistence seam yet
9. the serial spine remains stateless
10. any richer Stage B / Stage C enrichments are implemented only if the accepted baseline already supports them lawfully; otherwise they are recorded as reserved follow-on seams

---

## Mandatory read order before changing anything

Read these in full, in this exact order.

### Control surfaces and tranche law

1. `AGENTS.md`
2. `migration_prebuild/00_hierarchical_order.md`
3. `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`
4. `migration_prebuild/04_rebuild_execution_order.md`
5. `migration_prebuild/05_nvda_final_recommendations_report_2026-04-18.md`
6. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
7. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`

### Core normative and operating docs

8. `docs/01_NORMATIVE_CORE.md`
9. `docs/03_DOMAIN_MODEL_CORE.md`
10. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`
11. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
12. `docs/09_DMPV3_PROTOCOL_CORE.md`
13. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
14. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
15. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`

### Test law

16. `tests/AGENTS.override.md`

### Existing audit and brief surfaces

17. `var/audit/nvda_running_audit_log.xlsx`
18. `var/audit/briefs/module_7_dmpv3_packet_carriage_implementation_brief_v1.md`
19. `var/audit/2026-04-21_module_7_dmpv3_packet_carriage_truth_pass_report.md`

### Native Module 8 / adjacent native sources to read in full

20. `src/nvda_desk/contracts/parallel_risk.py`
21. `src/nvda_desk/services/parallel_risk_lane_service.py`
22. `src/nvda_desk/risk/parallel/evaluate.py`
23. `src/nvda_desk/domain/parallel_risk/environment_assessment.py`
24. `src/nvda_desk/domain/parallel_risk/candidate_audit.py`
25. `src/nvda_desk/contracts/packets.py`
26. `src/nvda_desk/packets/dmp_packets.py`
27. `src/nvda_desk/services/final_risk_service.py`
28. `src/nvda_desk/preparation/runtime_preparer.py`
29. `src/nvda_desk/cognition/ingress/translator.py`
30. `src/nvda_desk/contracts/stage_inputs.py`
31. every file under `src/nvda_desk/domain/parallel_risk/`
32. every file under `src/nvda_desk/risk/parallel/`
33. every file under `src/nvda_desk/repositories/` relevant to state/review/reference/execution storage
34. every file under `src/nvda_desk/persistence/` relevant to storage patterns

### Retained legacy evidence to read in full

35. `legacy_import/source/nvda_desk/services/parallel_risk_lane.py`
36. `legacy_import/source/nvda_desk/services/cognition_runtime.py`
37. `legacy_import/source/nvda_desk/schemas/parallel_risk.py`
38. `legacy_import/source/nvda_desk/schemas/dmp_envelope.py`
39. `legacy_import/source/nvda_desk/schemas/dmp.py`
40. any directly referenced legacy storage / repository files if needed to understand lawful write-only persistence shape

Do not claim comparison or design decisions until those sources are fully read.

---

## Vocabulary gate — mandatory before coding

Before changing code, docs, tests, manifests, or receipts:

1. check whether every durable term used by this brief is already governed in:
   1. `data/vocabulary/canonical_vocabulary.json`
   2. `src/nvda_desk/schemas/vocabulary.py`
   3. the vocabulary governance docs
2. terms that require checking include, at minimum:
   1. parallel risk lane
   2. environment assessment
   3. candidate audit
   4. market translation
   5. candidate semantics
   6. stage-read state
   7. dependency packet IDs
   8. parallel-risk observation store
   9. write-only persistence
   10. append-only observation record
3. workbook usage alone does **not** lawfully admit a term
4. if a term is missing, classify it through the lawful workflow as exactly one of:
   1. `enrich_existing`
   2. `add_new`
   3. `alias_only`
   4. `quarantine`
5. update the vocabulary surfaces first in the same bounded gate, then continue
6. if lawful admission is not possible in scope, stop and report the blocker

Do not silently invent language.

---

## Invariant and test-family gate — mandatory before coding

Before writing implementation changes:

1. identify the real invariants that Module 8 must protect
2. identify the existing Tier A / Tier B families that already govern those invariants
3. name the exact targeted test files to be added, updated, or left unchanged
4. record that named targeted test set in the tranche report **before** implementation leaves start
5. decide truthfully whether each required test action is:
   1. re-author
   2. extend
   3. defer
   4. archive
   5. block
6. do **not** pre-decide “probably no tests needed”

At minimum, the report must explicitly name tests for these invariant groups:

1. lawful bootstrap DMPV3 input to the lane
2. lawful bootstrap DMPV3 output from the lane
3. preservation of parallel-risk bounded ownership
4. preservation of stage-read / lineage / dependency packet IDs
5. write-only persistence only
6. no live read-back from the new persistence store in this tranche
7. serial spine remains stateless

---

## Workbook gate — mandatory in L1 before coding

Before implementation leaves start:

1. identify the exact governing workbook sheet names and row numbers used for this tranche
2. record them in the tranche report during **L1**
3. if workbook row ownership or seam ownership is ambiguous, stop and report the ambiguity before coding

At minimum, identify and record:

1. `Target_Structure` row for Parallel Risk
2. relevant `Module_Allocation_Appendix` rows for:
   1. environment assessment
   2. candidate audit
   3. lane service
3. relevant `Seam_Contracts` rows for:
   1. packet carriage
   2. bootstrap lane input
   3. parallel-risk runtime path output
   4. persistence ownership touched by this tranche

Do not wave at the workbook. Record exact row references.

---

## Scope

### In scope

1. one lawful **bootstrap** DMPV3 input contract for the lane
2. one lawful **bootstrap** DMPV3 output contract for the lane
3. native Stage A bootstrap lane flow using the accepted Module 7 packet-carriage surface
4. preservation of lawful packet lineage and stage-read state for the bootstrap path
5. one **parallel-risk-owned append-only write-only persistence seam**
6. minimum required tests and receipts
7. minimum allowed glue only, as explicitly listed below

### Out of scope

1. historical analytics over the new persistence store
2. live decision logic reading from the new persistence store
3. changing the serial spine into a stateful system
4. widening capital deployment into portfolio-management behaviour
5. widening downstream operations into analytics consumption
6. inventing new upstream live packet emitters in Modules 3, 4, or 6
7. general repo cleanup unrelated to Module 8
8. speculative extensions beyond what the docs, workbook, and retained legacy evidence justify

---

## Design constraints that must be preserved

1. The lane must remain a **separate module** answering the bounded question:  
   **what did the independent parallel risk lane conclude about the present environment?**
2. The lane must not become:
   1. serial candidate formation
   2. fresh-capital decision
   3. downstream management / exit / close logic
3. The serial spine must remain stateless.
4. The new persistence surface must be **parallel-risk-owned**, not a hidden shared shortcut.
5. The new persistence surface must be **write-only** in this tranche.
6. If a future analytical reader is desirable, leave that as a reserved later seam, not live functionality.

---

## Exact allowed glue and exact forbidden glue

### Allowed in this tranche

1. a bounded **Module 8-owned bootstrap adapter** that wraps already-admitted accepted-baseline upstream truth surfaces into the lane’s bootstrap DMPV3 input packet, if no existing lawful upstream packet emitter already exists
2. DMP packet builder exposure needed for the lane’s own packet emission
3. lineage / inspection surfaces needed for tests and review receipts
4. one parallel-risk-owned write helper / repository / append-only persistence surface

### Not allowed in this tranche

1. widening Modules 3, 4, or 6 so they begin emitting new live packet families just to satisfy Module 8
2. widening `FinalRiskService` so it consumes the lane output
3. widening capital deployment
4. widening downstream operations
5. adding live consumer logic for the new persistence store
6. adding analytical readers or derived analytics tables
7. creating a shared hidden state store masquerading as parallel-risk persistence

If any required change would force one of the forbidden items, stop and report the blocker.

---

## Exact minimum DMP input set for this tranche

The minimum required DMPV3 input set is:

1. one lawful **bootstrap lane input packet** representing the admitted upstream truth needed to start the lane
2. that bootstrap packet must be built from already-admitted accepted-baseline upstream truth surfaces
3. if the accepted baseline already exposes a lawful native upstream DMP packet that satisfies this, consume it
4. if it does not, create a **bounded Module 8-owned bootstrap adapter** that wraps the already-admitted upstream truth into the lane’s bootstrap input packet
5. do **not** widen upstream modules to emit new live packets in this tranche

This is the minimum mandatory target for current Module 8.  
Do not invent a richer packet ecosystem just to make the story look complete.

---

## Mandatory vs conditional implementation shape

### Mandatory in this tranche

#### Stage A — bootstrap / evaluate

You must implement Stage A.

Stage A must:

1. receive one lawful bootstrap DMPV3 input packet
2. produce one lawful bootstrap parallel-risk DMPV3 output packet
3. preserve invariant reads
4. preserve stage-read state
5. preserve trace / run / scenario / lineage surfaces required by the active DMPV3 rules
6. remain bounded to independent parallel-risk / environment-assessment meaning

#### Write-only persistence seam

You must implement one write-only persistence seam.

That seam must:

1. use the existing native repository / persistence pattern unless impossible
2. be parallel-risk-owned
3. be append-only / receiptable
4. write only:
   1. admitted input packet IDs
   2. emitted output packet IDs
   3. bounded observation payload
   4. timestamps
   5. trace / run / scenario IDs
   6. lineage references needed for later audit
5. expose **no readers** in this tranche
6. expose **no analytics tables** in this tranche
7. expose **no live read-back path** in this tranche

### Conditional in this tranche

#### Stage B — market translation enrichment

Stage B is **conditional**.

Implement Stage B only if the accepted baseline already exposes lawful upstream packet inputs needed for it **without widening other modules**.

If lawful upstream packet inputs do **not** already exist in the accepted baseline:

1. do not invent interim contracts
2. do not widen upstream modules
3. record Stage B as a reserved follow-on seam in the report
4. do not treat Stage B as a blocker for accepting this tranche

#### Stage C — candidate-semantics enrichment

Stage C is **conditional**.

Implement Stage C only if the accepted baseline already exposes lawful upstream packet inputs needed for it **without widening other modules**.

If lawful upstream packet inputs do **not** already exist in the accepted baseline:

1. do not invent interim contracts
2. do not widen upstream modules
3. record Stage C as a reserved follow-on seam in the report
4. do not treat Stage C as a blocker for accepting this tranche

---

## Required leaf structure

Use a bounded leaf sequence. The exact titles may vary, but the truth boundaries must not.

Recommended leaf structure:

1. **L1 — Read / vocabulary / workbook / invariant / targeted-test gate**
2. **L2 — Bootstrap DMP input/output contracts and packet builders**
3. **L3 — Stage A lane service/runtime wiring**
4. **L4 — Write-only persistence seam**
5. **L5 — Conditional Stage B/C decision, tests, proof, receipts, workbook closeout**

Do not batch everything into one opaque commit.

---

## Receipt and report requirements

You must create and maintain:

1. `var/audit/briefs/` copy of this brief
2. `var/audit/<dated>_module_8_parallel_risk_lane_truth_pass_report.md`
3. updates to `var/audit/nvda_running_audit_log.xlsx`

The report must include:

1. branch name
2. baseline commit
3. leaf chronology
4. exact closing commit for each leaf
5. vocabulary decisions
6. invariant/test-family decisions
7. exact workbook sheet names and row numbers used
8. exact named targeted test files chosen in L1
9. exact statement of what the new persistence seam stores
10. exact statement that analytics and live read-back remain out of scope
11. whether Stage B was implemented or reserved
12. whether Stage C was implemented or reserved
13. proof outputs
14. final clean HEAD
15. explicit notes for any truthful limitation or blocker

Do not leave report/workbook ambiguity for later.

---

## Proof requirements

Run the proofs needed by the actual invariant changes.

At minimum, after implementation is complete, rerun:

1. vocabulary gate tests relevant to changed vocabulary surfaces
2. targeted Module 8 / packet / lineage / persistence tests named in L1
3. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
4. compile proof  
   `python -m compileall src`

Targeted proof must directly demonstrate:

1. lawful bootstrap DMPV3 input to the lane
2. lawful bootstrap DMPV3 output from the lane
3. stage-read / lineage preservation for the implemented path
4. write-only persistence behaviour
5. absence of live read-back dependency from the new persistence seam in this tranche

Record exact outputs in the tranche report.

---

## Clean closeout rule

When complete:

1. branch must remain `work/module-8-parallel-risk-lane-truth-pass-20260421`
2. branch must remain unmerged
3. repo must be clean on `git status`
4. report and workbook must agree
5. package the full repo including `.git`

If exact self-reference inside tracked receipt files creates ambiguity, resolve it truthfully using the same clean-closeout discipline learned from Module 7:

1. one authoritative packaged HEAD
2. no dirty working tree
3. explicit note where exact self-reference is impossible

---

## Definition of done

Module 8 is complete only if all of the following are true:

1. it starts from the accepted Module 7 closeout baseline
2. Stage A bootstrap DMPV3 input exists
3. Stage A bootstrap DMPV3 output exists
4. the lane remains bounded to independent parallel-risk meaning
5. staged lineage / dependency / stage-read surfaces are preserved for the implemented path
6. the write-only parallel-risk persistence seam exists
7. the new persistence seam is append-only / receiptable
8. no analytics are installed over that seam yet
9. no live decision logic reads from that seam yet
10. serial spine remains stateless
11. targeted proof reruns clean
12. full shell proof reruns clean
13. compile proof reruns clean
14. receipts are complete
15. workbook is complete
16. repo is clean
17. branch is unmerged
18. Stage B and Stage C are either truthfully implemented from already-lawful baseline packet inputs or explicitly reserved in the report

If any one of those is false, stop and report the blocker truthfully.

---

## Return requirements

Return exactly:

1. the updated repo zip including `.git`
2. a concise execution summary stating:
   1. branch name
   2. base commit
   3. final HEAD commit
   4. whether the repo is clean
   5. proof results
   6. vocabulary decisions
   7. workbook rows used
   8. named targeted test files used
   9. whether Stage B was implemented or reserved
   10. whether Stage C was implemented or reserved
   11. whether any blocker remains

Then stop and await further instructions.
