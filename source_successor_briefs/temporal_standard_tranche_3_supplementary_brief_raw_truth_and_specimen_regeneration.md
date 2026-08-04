# Temporal standard program — tranche 3 supplementary brief
## Source temporal raw-truth correction and specimen artefact regeneration only

## Purpose

This supplementary brief exists because the submitted Tranche 3 repo is **substantively close**, but it is **not yet accepted**.

The remaining gaps are narrow and specific:

1. the canonical helper currently fabricates `source_time_raw` from normalised `source_time_utc` or `source_date`
2. the checked-in Module 8 specimen artefacts under `var/audit/specimens/module_8/` still carry the pre-remediation temporal grammar (`observed_at`, `next_event_at`) and were not regenerated to the admitted temporal grammar

This supplementary brief fixes **only those gaps**.

Do **not** reopen the broader tranche.
Do **not** widen unfinished runtime modules.
Do **not** redesign the temporal standard.

---

## Baseline

Start from the submitted Tranche 3 repo exactly as handed back for audit.

Expected starting state after unzip:

1. branch: `work/temporal-standard-tranche-3-code-persistence-remediation-20260422`
2. committed HEAD: `c941fc92c01d86506c0166f9e618f2ae5c02894a`
3. repo clean: yes
4. authoritative closeout tag present:
   `temporal-standard-tranche-3-authoritative-closeout-20260422`

If the provided repo does not match that exact branch and clean starting HEAD, stop immediately and report the blocker.

---

## Why the submitted repo is not yet accepted

### A. `source_time_raw` is not being preserved as raw source truth

The admitted architecture rule says:

- `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:33`
  `source_time_raw` = the **exact source-supplied time token as captured from the source artefact**

But the current helper does this instead:

- `src/nvda_desk/contracts/temporal.py:84-89`

It fabricates `source_time_raw` by deriving it from:
1. `source_time_utc` via ISO formatting, or
2. `source_date` via ISO formatting

That is not the exact source-supplied token.
It is a normalised derivative.

### B. The checked-in workbook specimen artefacts are stale and still carry the old temporal grammar

Current checked-in artefacts still contain fields such as:

1. `observed_at`
2. `next_event_at`

Evidence:

- `var/audit/specimens/module_8/stage_input_bundle.json:20-23`
- `var/audit/specimens/module_8/bootstrap_input_packet.json:48-52`
- `var/audit/specimens/module_8/stage_a_output_packet.json:13-20`
- `var/audit/specimens/module_8/specimen_receipt.md:27-40`

But the remediated harness source now writes the new grammar, for example:

- `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py:424-437`

So the checked-in artefacts are stale and contradict the remediated code and admitted temporal law.

---

## Mandatory execution posture

1. Work on the existing Tranche 3 branch only.
2. Do **not** merge to `main`.
3. Do **not** reopen the broader tranche scope.
4. Do **not** widen Module 8 Stage B/C, Module 9, Module 10, or Module 11.
5. Do **not** invent backward-compatibility shims, aliases, or dual temporal grammars.
6. Do **not** preserve old field names alongside new canonical names.
7. One active leaf at a time.
8. Return a clean committed work branch zip including `.git`.
9. Use the authoritative closeout-tag pattern again after the supplementary reconciliation commit.

This supplementary work is successful only if it stays narrow.

---

## Blocker discipline — mandatory

If a blocker is encountered, the executor must:

1. stop immediately
2. make no further changes
3. not improvise
4. not keep going “just to see”
5. not create substitute assumptions
6. return the exact blocker with evidence

---

## Scope

### In scope

1. correct `source_time_raw` handling so it reflects the admitted temporal law truthfully
2. update the exact surfaces that rely on that correction, if any, within this narrow boundary
3. regenerate the checked-in Module 8 specimen artefacts under `var/audit/specimens/module_8/`
4. update the Tranche 3 report and workbook receipts
5. rerun the proof floor
6. create one new authoritative closeout tag for the corrected supplementary closeout

### Out of scope

1. broad runtime redesign
2. broad additional temporal remediation
3. unfinished runtime modules
4. normative-document rewrites
5. backward-compatibility alias layers

---

## Mandatory read order before changing anything

Read these in full, in this order:

1. `AGENTS.md`
2. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
3. `docs/05.1_GUARDRAILS_WORKING.md`
4. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
5. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
6. `var/audit/2026-04-22_temporal_standard_tranche_3_code_persistence_remediation_report.md`
7. `src/nvda_desk/contracts/temporal.py`
8. `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`
9. all checked-in files under `var/audit/specimens/module_8/`

Do not start changing anything until that read is complete.

---

## Required implementation rules

### 1. `source_time_raw` rule

`source_time_raw` must reflect the exact source-supplied time token as captured from the source artefact.

That means:

1. do **not** auto-generate `source_time_raw` from `source_time_utc`
2. do **not** auto-generate `source_time_raw` from `source_date`
3. if the exact raw token exists, carry it explicitly
4. if the exact raw token does not exist on a given surface, leave `source_time_raw` as `None`
5. do **not** fill it with a convenient normalised value just to avoid nulls

This rule is mandatory.

### 2. Workbook specimen rule

For the workbook-derived specimen:

1. preserve `source_date` as the lawful source observation truth
2. preserve field-level provenance in the receipt/lineage
3. do **not** fabricate a raw token if the workbook promotion path did not explicitly carry one
4. therefore, if no exact raw token is being preserved from the workbook promotion path, `source_time_raw` must remain `null`

### 3. No backward compatibility

Do **not**:
1. reintroduce `observed_at`
2. reintroduce `next_event_at`
3. keep legacy names as aliases or properties
4. add compatibility shims

The objective is replacement and convergence, not coexistence.

### 4. Checked-in artefacts must be regenerated

After correcting the helper/path, you must regenerate the checked-in Module 8 artefacts so they reflect the remediated canonical grammar.

At minimum regenerate:

1. `var/audit/specimens/module_8/stage_input_bundle.json`
2. `var/audit/specimens/module_8/bootstrap_input_packet.json`
3. `var/audit/specimens/module_8/stage_a_output_packet.json`
4. `var/audit/specimens/module_8/append_only_observation_record.json`
5. `var/audit/specimens/module_8/specimen_receipt.md`

They must no longer contain:
1. `observed_at`
2. `next_event_at`

and must reflect the admitted temporal grammar truthfully.

---

## Mandatory L1 declarations before coding

In **L1**, before any code-edit leaf starts, record in the supplementary report:

1. exact files to change
2. exact files to regenerate
3. exact proof files to rerun
4. explicit statement that:
   1. `source_time_raw` will no longer be auto-fabricated
   2. stale checked-in specimen artefacts will be regenerated
   3. no backward-compatibility shims are allowed

If any of those cannot be stated exactly, stop and report the blocker before changing anything.

---

## Required leaf structure

Use this exact bounded sequence unless a blocker prevents it:

1. `SL1-read-scope-and-raw-truth-declarations`
2. `SL2-source-time-raw-correction`
3. `SL3-specimen-artefact-regeneration`
4. `SL4-report-workbook-proof-and-clean-closeout`

One active leaf at a time.
Do not batch everything into one opaque commit.

---

## Proof requirements

After the supplementary reconciliation commit, rerun exactly:

1. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

2. compile proof  
   `python -m compileall src`

Record exact outputs in the updated report.

---

## Receipt requirements

Maintain and return:

1. updated `var/audit/2026-04-22_temporal_standard_tranche_3_code_persistence_remediation_report.md`
2. updated `var/audit/nvda_running_audit_log.xlsx`
3. one brief copy under `var/audit/briefs/`

The updated report must explicitly state:

1. `source_time_raw` correction rule applied
2. specimen artefacts regenerated
3. stale `observed_at` / `next_event_at` artefacts removed from the checked-in specimen set
4. authoritative closeout ref used for this supplementary closeout

The report must not rely on hand-back-summary placeholders.

---

## Authoritative closeout mechanism — mandatory

Use this exact pattern:

1. make one final bounded supplementary closeout commit on the existing Tranche 3 branch
2. create one annotated Git tag named:

`temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-raw-truth`

3. the tag must point to the final clean supplementary closeout commit
4. tracked receipts must record that exact authoritative closeout ref name
5. do not use hand-back-summary placeholder wording

---

## Branch and packaging requirements

1. leave the branch as `work/temporal-standard-tranche-3-code-persistence-remediation-20260422`
2. leave the branch unmerged
3. final repo must be clean
4. include the annotated supplementary closeout tag
5. zip the full repo including `.git`

Return:

1. updated repo zip
2. concise execution summary with:
   1. branch name
   2. starting HEAD
   3. final HEAD
   4. supplementary authoritative closeout ref name
   5. exact tag target commit
   6. whether repo is clean
   7. proof results

---

## Definition of done

This supplementary brief is complete only if all of the following are true:

1. `source_time_raw` is no longer auto-fabricated
2. checked-in specimen artefacts are regenerated
3. checked-in specimen artefacts no longer use `observed_at`
4. checked-in specimen artefacts no longer use `next_event_at`
5. no backward-compatibility shim was introduced
6. updated report is complete
7. workbook is updated
8. proofs rerun clean
9. repo is clean
10. branch remains unmerged
11. supplementary authoritative closeout tag exists and points to the final clean commit

If any one of those is false, stop and report the blocker truthfully.
