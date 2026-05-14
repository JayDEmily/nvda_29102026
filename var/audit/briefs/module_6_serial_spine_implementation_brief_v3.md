# Module 6 — serial spine implementation brief v3

## Purpose

This brief advances **Module 6 — Serial spine** only.

It starts from the **actually provided clean Module 8 recovery-closeout repo** and moves the repo forward by hardening the **serial runtime path** and the **lawful serial stage packet-emission surfaces** that are already supportable from that accepted-provided baseline.

This brief is **not** for final risk, capital deployment, downstream operations, Stage B market translation, Stage C candidate semantics, analytics, or normative-document rewriting.

---

## Corrected baseline to use

Use the repo zip that was actually provided to the execution thread:

`NVIDIA_V7_module_8_parallel_risk_lane_recovery_closeout_2026-04-22.zip`

Required starting state after unzip:

1. branch: `work/module-8-parallel-risk-lane-truth-pass-20260421`
2. committed HEAD: `4eb965e2d213c3de86baa7526c7c8a4ff8e20b34`
3. repo clean: yes

Create the new work branch from that exact state.

Required new branch name:

`work/module-6-serial-spine-truth-pass-20260422`

If the provided repo is not actually on:
1. branch `work/module-8-parallel-risk-lane-truth-pass-20260421`
2. clean HEAD `4eb965e2d213c3de86baa7526c7c8a4ff8e20b34`

then stop and report the blocker.

---

## Mandatory execution posture

1. Work on the new Module 6 branch only.
2. Do **not** merge to `main`.
3. Do **not** rewrite normative documents in this tranche.
4. Do **not** widen Module 9, 10, or 11 beyond the minimum lawful proof-visible glue explicitly allowed below.
5. Do **not** re-open Module 7 or Module 8 design except where Module 6 must lawfully interoperate with their admitted surfaces.
6. Read all required governing files **in full** before changing anything.
7. If file output truncates, continue reading in chunks until the full required source has been read.
8. Return a **clean committed work branch** zip including `.git`.

---

## Outcome target

At the end of this tranche, the repo must truthfully support:

1. a stronger native serial runtime path
2. explicit lawful stage outputs for the serial spine where those outputs are already supportable from the accepted baseline
3. lawful DMPV3 packet emission for the serial stage outputs that are truthfully implemented in this tranche
4. preservation of serial ordering and bounded stage ownership
5. no hidden state introduced into the serial spine
6. no speculative widening into final risk, capital deployment, or downstream behaviour
7. groundwork that makes later Module 8 Stage B / Stage C enrichment possible **without inventing interim contracts**

---

## Mandatory read order before changing anything

Read these in full, in this order.

### Control surfaces and tranche law

1. `AGENTS.md`
2. `migration_prebuild/00_hierarchical_order.md`
3. `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`
4. `migration_prebuild/04_rebuild_execution_order.md`
5. `migration_prebuild/05_nvda_final_recommendations_report_2026-04-18.md`
6. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
7. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`

### Core docs

8. `docs/01_NORMATIVE_CORE.md`
9. `docs/03_DOMAIN_MODEL_CORE.md`
10. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`
11. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
12. `docs/09_DMPV3_PROTOCOL_CORE.md`
13. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
14. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`

### Existing audit and module reports

15. `var/audit/nvda_running_audit_log.xlsx`
16. `var/audit/2026-04-21_module_7_dmpv3_packet_carriage_truth_pass_report.md`
17. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`

### Native Module 6 / adjacent sources

18. `src/nvda_desk/runtime/orchestrator.py`
19. every file under `src/nvda_desk/cognition/serial/`
20. every file under `src/nvda_desk/domain/temporal/`
21. every file under `src/nvda_desk/domain/regime/`
22. every file under `src/nvda_desk/domain/options_flow/`
23. every file under `src/nvda_desk/domain/posture/`
24. every file under `src/nvda_desk/domain/eligibility/`
25. every file under `src/nvda_desk/domain/execution/`
26. `src/nvda_desk/contracts/stage_inputs.py`
27. `src/nvda_desk/contracts/temporal.py`
28. `src/nvda_desk/contracts/regime.py`
29. `src/nvda_desk/contracts/options_flow.py`
30. `src/nvda_desk/contracts/packets.py`
31. `src/nvda_desk/packets/dmp_packets.py`
32. `src/nvda_desk/services/final_risk_service.py`
33. `src/nvda_desk/services/parallel_risk_lane_service.py`

### Legacy evidence to read in full

34. `legacy_import/source/nvda_desk/services/cognition_runtime.py`
35. `legacy_import/source/nvda_desk/schemas/dmp.py`
36. `legacy_import/source/nvda_desk/schemas/dmp_envelope.py`

Do not make serial-runtime or packet-emission claims until those sources are fully read.

---

## Vocabulary gate

Before coding:

1. check whether every durable term used by this tranche is already governed
2. likely terms to check include:
   1. serial spine
   2. stage output
   3. stage packet
   4. execution candidate
   5. stage sequence
   6. stage dependency
3. workbook usage or legacy usage alone does **not** admit a term
4. if a new durable term is actually required, admit it lawfully before using it in governed surfaces
5. if lawful admission is not possible in scope, stop and report the blocker

Do not silently invent serial-stage terminology.

---

## Mandatory L1 declarations before any implementation coding

In **L1**, and before any implementation leaf starts, you must record in the tranche report:

1. the **exact workbook sheet names and exact row numbers** being relied on
2. the **exact targeted test files** that will be added or updated
3. the **exact stage packet emitters** classified into:
   1. **mandatory in this tranche**
   2. **conditional in this tranche**
   3. **reserved for later**
4. any stage whose lawful output is still too thin or ambiguous to packetise truthfully

If any of those four items cannot be stated exactly, stop and report the blocker before coding.

---

## Invariant and test-family gate

Before coding, identify and record the real invariants.

At minimum, think in terms of:

1. serial stage ordering is explicit and truthful
2. each stage owns only its bounded answer
3. admitted stage outputs can be emitted through lawful DMPV3 packet carriage
4. packet lineage and dependency surfaces are truthful
5. serial runtime remains stateless
6. no parallel-risk, capital, or downstream module absorbs serial meaning by convenience

Record the targeted test-family decision in the tranche report before implementation.

Do **not** postpone the test decision until after coding.

---

## Scope

### In scope

1. harden the native serial runtime path
2. define or tighten the admitted serial stage output contract surfaces already justified by the workbook/docs
3. emit lawful DMPV3 packets for admitted serial stage outputs implemented in this tranche
4. preserve truthful stage dependency / lineage surfaces
5. add or re-author the minimum targeted tests needed
6. update the tranche report and live audit workbook

### Out of scope

1. rewriting normative documents
2. implementing Module 8 Stage B / Stage C directly
3. widening final risk, capital deployment, or downstream operations beyond the minimal proof-visible glue explicitly allowed below
4. adding analytics or persistence not already justified for Module 6
5. general repo cleanup unrelated to Module 6

---

## Mandatory vs conditional stage work

### Mandatory in this tranche

1. strengthen the serial runtime path itself
2. strengthen the lawful typed stage outputs that are already supportable from the accepted baseline
3. emit lawful DMPV3 packets for the stage outputs that can be packetised truthfully from the accepted baseline
4. preserve stage order, dependency, and lineage surfaces

### Conditional in this tranche

A stage packet emitter is only in scope if the accepted baseline already gives it a lawful typed stage output without widening adjacent modules or inventing interim fields.

If a stage would require:

1. inventing new output fields
2. widening final risk / capital / downstream consumers
3. widening Module 8 Stage B / Stage C logic
4. creating temporary convenience contracts just to make packet emission “complete”

then that stage emitter is **not** mandatory in this tranche. Record it as **reserved** and receipt it truthfully.

### Reserved, not invented

If a stage lacks a lawful typed output in the accepted baseline, reserve it.  
Do **not** fake completeness by inventing interim contracts.

---

## Required implementation shape

### A. Strengthen serial stage outputs

Tighten the current stage output surfaces so they are lawful, typed, and inspectable.

The intended serial stage order remains:

1. temporal
2. market regime
3. options and flow
4. posture and risk permission
5. playbook eligibility
6. expression and execution

Do **not** collapse them into one opaque blob.

### B. Emit lawful DMPV3 stage packets

Use the admitted Module 7 packet-carriage surfaces to emit lawful packets only for the serial stages that are truthfully implemented in this tranche.

At minimum:

1. preserve stage order
2. preserve stage dependencies
3. preserve trace / run / scenario / lineage surfaces required by the active DMPV3 rules
4. do not invent fields that the current stage outputs do not lawfully own

### C. Runtime wiring rule

The runtime/orchestrator path may be strengthened only enough to make the serial stage outputs and packet carriage lawful and inspectable.

#### Allowed glue

1. stage sequencing
2. stage output assembly
3. packet emission
4. proof-visible lineage support only

#### Forbidden glue

1. widening final risk to absorb serial logic
2. widening capital deployment
3. widening downstream operations
4. hiding stage boundaries behind one convenience wrapper
5. inventing interim contracts solely to satisfy packet emission

---

## Workbook alignment requirement

Before coding, record in the tranche report in **L1** the exact workbook rows used.

At minimum identify:

1. exact `Target_Structure` sheet row numbers relevant to serial runtime
2. exact `Module_Allocation_Appendix` sheet row numbers for:
   1. temporal
   2. regime
   3. options/flow
   4. posture
   5. eligibility
   6. execution
3. exact `Seam_Contracts` sheet row numbers for:
   1. cognition ingress -> serial runtime
   2. serial runtime -> packet carriage
   3. execution candidate -> final risk join

If workbook ownership is ambiguous, stop and report that ambiguity before implementation.

---

## Required leaf structure

Recommended bounded leaves:

1. `L1-read-vocabulary-workbook-invariant-test-gate`
2. `L2-serial-stage-output-contract-hardening`
3. `L3-serial-stage-packet-builders-and-runtime-wiring`
4. `L4-targeted-tests-and-proof`
5. `L5-report-workbook-and-clean-closeout`

Do not batch everything into one opaque commit.

---

## Receipt requirements

Maintain and return:

1. `var/audit/briefs/` copy of this brief
2. `var/audit/<dated>_module_6_serial_spine_truth_pass_report.md`
3. updates to `var/audit/nvda_running_audit_log.xlsx`

The report must include:

1. branch name
2. baseline commit
3. leaf chronology
4. exact closing commit for each leaf
5. vocabulary decisions
6. invariant/test-family decisions
7. exact workbook sheet names and exact row numbers used
8. exact targeted test files named in L1
9. exact stage packet emitters classified as mandatory / conditional / reserved
10. exact targeted proof outputs
11. final authoritative packaged HEAD
12. explicit scope note that Module 8 Stage B/C and Module 10/11 remained out of scope

Do not leave report ambiguity for later.

---

## Proof requirements

After implementation, rerun:

1. vocabulary tests relevant to any changed vocabulary surfaces
2. the exact targeted Module 6 / packet / lineage tests named in L1
3. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
4. compile proof  
   `python -m compileall src`

Record exact outputs in the report.

If no existing targeted test family fits, record that as an explicit L1 decision before implementation and add the narrowest truthful new targeted test file.

---

## Clean closeout rule

When done:

1. branch must remain `work/module-6-serial-spine-truth-pass-20260422`
2. branch must remain unmerged
3. repo must be clean
4. report and workbook must agree
5. one authoritative packaged HEAD must be recorded
6. no dirty working tree is allowed

---

## Definition of done

Module 6 is complete only if all of the following are true:

1. it starts from the actually provided clean Module 8 recovery-closeout baseline `4eb965e2d213c3de86baa7526c7c8a4ff8e20b34`
2. the native serial runtime path is strengthened truthfully
3. admitted stage outputs exist as typed inspectable surfaces
4. lawful DMPV3 stage packet emission exists for the stages declared **mandatory in L1**
5. packet lineage/dependency surfaces are truthful
6. the serial spine remains stateless
7. stages declared **conditional or reserved in L1** are receipted truthfully and not faked
8. Module 8 Stage B/C are not widened in this tranche
9. final risk / capital / downstream are not widened beyond allowed proof-visible glue
10. proofs rerun clean
11. the repo is clean
12. the branch is unmerged

If any one of those is false, stop and report the blocker truthfully.

---

## Return requirements

Return exactly:

1. the updated repo zip including `.git`
2. a concise execution summary stating:
   1. branch name
   2. baseline commit
   3. final HEAD commit
   4. whether the repo is clean
   5. proof results
   6. exact workbook sheet names and row numbers used
   7. exact targeted test files used
   8. mandatory / conditional / reserved stage packet emitters
   9. whether any blocker remains

Then stop and await further instructions.
