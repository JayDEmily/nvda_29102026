# Temporal standard program — tranche 1 execution brief v2
## Normative admission only

## Purpose

This brief executes **Tranche 1 — normative admission** of the temporal-standard program.

This brief is self-contained on purpose. It does **not** depend on any external planning note or master brief file being present inside the repo.

This tranche admits the repo-wide temporal standard into the **working normative layer only**.

It does **not** perform code remediation, proof-surface remediation, or unfinished module work.

This is a **documents-only tranche plus receipts/closeout**.

---

## Baseline to use

Use this accepted repo zip as the required starting baseline:

- `NVIDIA_V7_module_6_authoritative_closeout_2026-04-22.zip`

Required starting state after unzip:

1. branch: `work/module-6-serial-spine-truth-pass-20260422`
2. committed HEAD: `ecbdf55cc700f5d87a8346b4a1e1c541618705d0`
3. repo clean: yes
4. authoritative closeout tag present:
   `module-6-serial-spine-authoritative-closeout-20260422`

Create the new tranche branch from that exact state.

Required new branch name:

- `work/temporal-standard-tranche-1-normative-admission-20260422`

If the provided repo is not actually on:
1. branch `work/module-6-serial-spine-truth-pass-20260422`
2. clean HEAD `ecbdf55cc700f5d87a8346b4a1e1c541618705d0`
3. with tag `module-6-serial-spine-authoritative-closeout-20260422`

stop and report the blocker before doing any work.

---

## Program context this tranche must obey

This tranche is the **first of four sequential temporal-standard tranches**.

The overall program order is:

1. admit the temporal law
2. audit the repo against it
3. fix proof/test/governor surfaces
4. fix code and persistence surfaces
5. run final repo-wide conformance audit
6. close out cleanly

This tranche is **step 1 only**.

That means:

1. define the law in the working normative layer
2. do not remediate code yet
3. do not remediate tests yet
4. do not restart unfinished runtime-module work yet

The blueprint/workbook remains the **anti-drift ownership benchmark**, not the primary temporal-law authority.

---

## Mandatory execution posture

1. Work on the new tranche branch only.
2. Do **not** merge to `main`.
3. Do **not** change runtime code, packet builders, persistence code, tests, harnesses, specimen artefacts, or replay fixtures in this tranche.
4. Do **not** widen Module 8 Stage B/C, Module 9, Module 10, or Module 11.
5. Read all required governing files **in full** before changing anything.
6. If output truncates, continue reading in chunks until the required source is fully read.
7. Return a **clean committed work branch** zip including `.git`.
8. Use the authoritative closeout-tag pattern at the end of the tranche.
9. One active leaf at a time.

This tranche is successful only if it stays narrow.

---

## Outcome target

At the end of this tranche, the repo must contain a coherent admitted **working-layer temporal standard** that covers:

1. architecture-level source temporal grammar
2. DMPV3 temporal mapping subset
3. anti-drift temporal guardrails
4. workbook temporal provenance rules

And the tranche must **not**:

1. remediate code yet
2. remediate tests yet
3. change runtime behaviour
4. start unfinished module work

This tranche defines the law only.

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
11. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
12. `docs/09_DMPV3_PROTOCOL_CORE.md`
13. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
14. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`

### Working/supplement targets to be edited

15. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
16. `docs/05.1_GUARDRAILS_WORKING.md`
17. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
18. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`

### Supporting authority/context already inside repo

19. `docs/planning/2026-04-02_GATE160_GOVERNED_SIGNAL_COEFFICIENT_REFERENCE_WORKBOOK_LAW.md`
20. `docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.md`
21. `docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.json`

### Existing audit surfaces

22. `var/audit/nvda_running_audit_log.xlsx`

Do not start editing until the full read is complete.

---

## Vocabulary gate

Before editing any working normative doc:

1. check whether any new durable term is actually required
2. likely terms to check include:
   1. source temporal standard
   2. source_time_raw
   3. source_time_kind
   4. source_timezone_raw
   5. source_time_utc
   6. source_date
   7. captured_at_utc
   8. persisted_at_utc
   9. source_provider
   10. source_channel
   11. time_granularity
   12. workbook temporal provenance
   13. anchor-row date
   14. field-level provenance
3. if a term is already governed, use it lawfully
4. if a term is not governed and is required as a durable term, admit it lawfully in the same tranche before using it in governed surfaces
5. if lawful admission is not possible in scope, stop and report the blocker

Do **not** silently invent temporal vocabulary in normative text.

---

## Mandatory L1 declarations before editing

In **L1**, before any document-edit leaf starts, record in the tranche report:

1. the exact documents to be changed:
   1. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
   2. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
   3. `docs/05.1_GUARDRAILS_WORKING.md`
   4. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
2. the exact section names that will be inserted or amended in each document
3. the exact vocabulary decisions
4. the exact workbook sheet names and row numbers being used only as anti-drift ownership references, if any are cited in the report
5. explicit statement that this tranche is **documents-only** and that code/tests are out of scope

If any of those L1 items cannot be stated exactly, stop and report the blocker before editing.

---

## Scope

### In scope

1. admit the architecture-level source temporal standard into `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
2. admit the DMPV3 temporal mapping subset into `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
3. admit the anti-drift temporal guardrails into `docs/05.1_GUARDRAILS_WORKING.md`
4. admit the workbook temporal provenance rule into `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
5. update the tranche report and live audit workbook
6. create the authoritative closeout tag for this tranche

### Out of scope

1. all runtime code changes
2. all persistence code changes
3. all test file changes
4. all harness/specimen changes
5. all packet-builder changes
6. all unfinished runtime modules
7. all blueprint rewrites
8. all provider-specific implementation logic

Do not drift outside that boundary.

---

## Required normative content

### A. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`

Add one bounded section for the repo-wide **source temporal standard**.

That section must define, at minimum:

1. `source_time_raw`
2. `source_time_kind`
3. `source_timezone_raw`
4. `source_time_utc`
5. `source_date`
6. `captured_at_utc`
7. `persisted_at_utc`
8. `source_provider`
9. `source_channel`
10. `time_granularity`

It must explicitly state:

1. this grammar applies above DMPV3 packet carriage
2. it governs raw captures, local capture files, derived raw surfaces, persistence records, workbook-derived specimens, replay/proof surfaces, and packets where relevant
3. it is provider-agnostic
4. it must support IBKR-style market data, FRED-style date-level data, and workbook-derived mixed-date reference-ledger specimens without overfitting to one provider

### B. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`

Add one bounded section for the **DMPV3 temporal mapping subset**.

That section must define, at minimum:

1. `packet.time` is packet emission time
2. source observation time may differ from packet emission time
3. source observation time must be preserved separately where relevant
4. DMPV3 inherits the `04.1` source temporal standard
5. DMPV3 must not invent precision the source did not have

It must not try to redefine the whole source temporal law inside DMP.

### C. `docs/05.1_GUARDRAILS_WORKING.md`

Add one short bounded section for **temporal anti-drift guardrails**.

It must state, at minimum:

1. do not invent timestamp precision
2. do not apply fake UTC normalisation
3. do not collapse mixed-date reference sources into one false observation timestamp
4. do not let module-local temporal grammars diverge from the admitted architecture-level temporal standard

### D. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`

Add one bounded section for **workbook temporal provenance**.

It must state, at minimum:

1. workbook dates are reference-ledger provenance
2. anchor rows may be blended from fields with different source dates
3. workbook-derived specimens must preserve field-level provenance where dates differ
4. workbook-derived promotions must not masquerade as same-moment live runtime captures
5. the workbook remains a governed reference ledger, not direct runtime authority

---

## Required writing discipline

1. Use direct, non-aspirational language.
2. Do not write optional or hand-wavy wording.
3. Do not create overlapping or contradictory timestamp rules between `04.1`, `09.1`, `05.1`, and `SIGNAL_WORKBOOK_AUTHORITY`.
4. Keep the hierarchy clear:
   1. `04.1` = upstream source temporal law
   2. `09.1` = DMP mapping subset
   3. `05.1` = anti-drift guardrails
   4. `SIGNAL_WORKBOOK_AUTHORITY` = workbook-specific provenance rule
5. Do not let the workbook become the primary temporal-law authority.
6. Do not let DMPV3 become the whole-source temporal-law authority.

---

## Required leaf structure

Use this exact bounded leaf sequence unless a blocker prevents it:

1. `L1-read-vocabulary-and-scope-declarations`
2. `L2-architecture-working-temporal-standard`
3. `L3-dmp-working-temporal-mapping-and-guardrails`
4. `L4-workbook-authority-temporal-provenance`
5. `L5-report-workbook-proof-and-clean-closeout`

One active leaf at a time.  
Do not batch everything into one opaque commit.

---

## Receipt requirements

Maintain and return:

1. `var/audit/briefs/` copy of this brief
2. `var/audit/2026-04-22_temporal_standard_tranche_1_normative_admission_report.md`
3. updates to `var/audit/nvda_running_audit_log.xlsx`

The report must include:

1. branch name
2. baseline commit
3. leaf chronology
4. exact closing commit for each leaf
5. vocabulary decisions
6. exact section names inserted/amended in each target document
7. explicit statement that this tranche is documents-only
8. exact authoritative closeout ref name
9. proof outputs
10. final authoritative packaged HEAD or authoritative closeout ref pattern, consistent with the closeout rule below

The report must not rely on “hand-back summary” placeholders.

---

## Proof requirements

This is a documents-only tranche, but proof still runs.

After the final receipt-reconciliation commit, rerun exactly:

1. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

2. compile proof  
   `python -m compileall src`

Record exact outputs in the report.

Do **not** add or modify tests in this tranche.

---

## Authoritative closeout mechanism — mandatory

Use this exact pattern:

1. make one final bounded receipt/closeout commit on the tranche branch
2. create one annotated Git tag named:

`temporal-standard-tranche-1-authoritative-closeout-20260422`

3. the tag must point to the final clean closeout commit
4. tracked receipts must record that exact authoritative closeout ref name
5. do **not** use:
   1. “recorded in hand-back summary”
   2. “exact hash reported in hand-back summary”
   3. self-reference placeholder wording

This closeout mechanism is mandatory.

---

## Branch and packaging requirements

1. Leave the branch as `work/temporal-standard-tranche-1-normative-admission-20260422`
2. Leave the branch unmerged
3. The final repo must be **clean**
4. The final repo must include the annotated tag:
   `temporal-standard-tranche-1-authoritative-closeout-20260422`
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
      8. exact documents changed
      9. exact section names added or amended

---

## Definition of done

Tranche 1 is complete only if all of the following are true:

1. it started from the exact accepted Module 6 baseline
2. `04.1` contains the architecture-level source temporal standard
3. `09.1` contains the DMPV3 temporal mapping subset
4. `05.1` contains the temporal anti-drift guardrails
5. `SIGNAL_WORKBOOK_AUTHORITY` contains the workbook temporal provenance rule
6. the tranche remained documents-only
7. report is complete
8. workbook is complete
9. report and workbook agree
10. the authoritative closeout tag exists and points to the final clean commit
11. proofs rerun clean
12. repo is clean
13. branch is unmerged

If any one of those is false, stop and report the blocker truthfully.
