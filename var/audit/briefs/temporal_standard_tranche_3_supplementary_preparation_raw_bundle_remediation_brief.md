# Temporal standard program — tranche 3 supplementary remediation brief v2
## Preparation / raw-bundle seam correction only, with tranche-4 disregard instruction

## Purpose

This brief exists because the attempted Tranche 4 repo-wide audit correctly found a real blocker in the **preparation / raw-bundle seam**.

This brief is for the **same execution thread** that attempted Tranche 4.

The required action is:

1. **disregard the unfinished Tranche 4 attempt**
2. return to the accepted Tranche 3 baseline
3. perform one **narrow supplementary Tranche 3 remediation**
4. close that supplementary Tranche 3 remediation cleanly
5. stop and await further instructions

Do **not** continue Tranche 4 from the blocked state.
Do **not** try to repair Tranche 4 in place.

---

## Mandatory instruction about the blocked Tranche 4 attempt

The prior Tranche 4 attempt is **not** to be continued.

Treat it as:

1. a valid failed audit attempt
2. a useful blocker discovery
3. **not** the branch/repo state to continue from

That means:

1. do **not** keep the Tranche 4 branch as the move-forward baseline
2. do **not** create a Tranche 4 closeout tag
3. do **not** try to reconcile Tranche 4 receipts as if the audit passed
4. do **not** package a Tranche 4 success repo

The Tranche 4 attempt should be disregarded for execution purposes except as blocker evidence.

---

## Correct baseline to use

Use the **accepted Tranche 3 supplementary raw-truth closeout repo** as the remediation baseline.

Required baseline artefact:

- `NVIDIA_V7_temporal_standard_tranche_3_supplementary_raw_truth_closeout_2026-04-22.zip`

Required starting state after unzip:

1. branch: `work/temporal-standard-tranche-3-code-persistence-remediation-20260422`
2. committed HEAD: `2c9437ae92642d3213c88b81b65f2e2f19b5ba4b`
3. repo clean: yes
4. authoritative closeout tag present:
   `temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-raw-truth`

Create the new remediation branch from that exact state.

Required new branch name:

- `work/temporal-standard-tranche-3-supplementary-preparation-raw-bundle-remediation-20260422`

If the provided repo is not actually on:
1. branch `work/temporal-standard-tranche-3-code-persistence-remediation-20260422`
2. clean HEAD `2c9437ae92642d3213c88b81b65f2e2f19b5ba4b`
3. with tag `temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-raw-truth`

stop immediately and report the blocker before doing any other work.

---

## Why this supplementary remediation exists

The blocked Tranche 4 audit found a real contradiction between:

1. the accepted Tranche 3 remediation receipts
and
2. the live preparation/raw-bundle seam

### Blocker evidence already identified

1. `src/nvda_desk/preparation/runtime_preparer.py:362-370`
   still resolves source observation time from:
   - `bundle.provenance.observed_at`

2. `src/nvda_desk/ingress/raw_bundle_loader.py:11-18`
   still defines:
   - `RawBundleProvenance.observed_at`

3. `src/nvda_desk/ingress/raw_bundle_loader.py:72-83`
   still populates that same internal field from payload key:
   - `observed_at`

But the accepted Tranche 3 report states that this seam had already been remediated away from the legacy/internal temporal grammar:
- `var/audit/2026-04-22_temporal_standard_tranche_3_code_persistence_remediation_report.md:39-47`

That contradiction must now be fixed truthfully.

---

## Mandatory execution posture

1. Work on the new supplementary Tranche 3 branch only.
2. Do **not** merge to `main`.
3. Do **not** continue the blocked Tranche 4 branch.
4. Do **not** widen Module 8 Stage B/C, Module 9, Module 10, or Module 11.
5. Do **not** reopen the full Tranche 3 deferred set.
6. Do **not** introduce backward-compatibility aliases, shims, or dual temporal grammars.
7. Read all required governing files and all required seam files **in full** before changing anything.
8. If output truncates, continue reading in chunks until the required source is fully read.
9. One active leaf at a time.
10. Return a clean committed work branch zip including `.git`.

This supplementary work succeeds only if it stays narrow.

---

## Blocker discipline — mandatory

If a blocker is encountered, the executor must:

1. stop immediately
2. make no further changes
3. not improvise
4. not keep going “just to see”
5. not partially execute later leaves
6. not create substitute assumptions
7. return the exact blocker with evidence

The executor is not allowed to wing it, keep going anyway, or work around it silently.

---

## Anti-shortcut / anti-path-to-green discipline — mandatory

The executor must not optimise for:

1. the smallest apparent fix
2. the fastest route to green
3. the fewest files touched
4. keeping old field names alive for convenience

Instead, optimise for:

1. exact brief conformance
2. full required reading
3. truthful remediation of the seam
4. truthful receipts
5. one canonical grammar only

Green proofs do not excuse skipped required remediation.

---

## Scope

### In scope

This supplementary remediation is limited to the **preparation / raw-bundle seam** and the exact directly coupled proof/receipt surfaces required to close that seam truthfully.

At minimum this includes:

1. `src/nvda_desk/ingress/raw_bundle_loader.py`
2. `src/nvda_desk/preparation/runtime_preparer.py`

And, if directly coupled and truthfully required:

3. minimal directly coupled contract/proof surfaces
4. Tranche 3 report and workbook receipts

### Out of scope

1. the rest of Tranche 3 deferred surfaces
2. Tranche 4 execution
3. Module 8 Stage B / Stage C
4. Module 9
5. Module 10
6. Module 11
7. normative-document rewrites
8. backward-compatibility layers

If a change outside the narrow seam is truly unavoidable, it must be:
1. minimal
2. explicitly receipted
3. justified as unavoidable seam glue
4. not a backdoor tranche expansion

---

## Mandatory read order before changing anything

Read these in full, in this order:

1. `AGENTS.md`
2. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
3. `docs/05.1_GUARDRAILS_WORKING.md`
4. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
5. `var/audit/2026-04-22_temporal_standard_tranche_3_code_persistence_remediation_report.md`
6. `var/audit/2026-04-22_temporal_standard_tranche_2_conformance_audit_report.md`
7. `var/audit/nvda_running_audit_log.xlsx`
8. `src/nvda_desk/ingress/raw_bundle_loader.py`
9. `src/nvda_desk/preparation/runtime_preparer.py`

Also read in full any directly coupled proof files you determine must change.
Do not start changing anything until the full read is complete.

---

## Required remediation rule

The internal legacy field `observed_at` must be removed from the **active preparation/raw-bundle seam**.

That means:

1. do **not** keep `observed_at` alive as an internal compatibility field
2. do **not** alias it to a new canonical field
3. do **not** preserve dual grammar
4. do **not** keep reading from it in `runtime_preparer.py`

The seam must instead use only the admitted temporal grammar.

If the source artefact truth is:
1. raw token
2. date
3. UTC timestamp
4. capture time
5. persistence time

then the seam must carry those through the admitted canonical fields only.

No backward compatibility.

---

## Required implementation rules

### A. Raw-bundle provenance correction

Correct `src/nvda_desk/ingress/raw_bundle_loader.py` so the active internal provenance carrier no longer uses the legacy field name `observed_at`.

### B. Preparation seam correction

Correct `src/nvda_desk/preparation/runtime_preparer.py` so it no longer reads `bundle.provenance.observed_at`.

### C. Truth preservation

The remediation must preserve:

1. raw source truth
2. admitted temporal standard
3. no invented precision
4. no fake UTC normalisation
5. no compatibility shim
6. no hidden fallback to old grammar

### D. Coupled proof updates

Update only the minimum directly coupled proof surfaces needed to assert the corrected seam truthfully.

Do **not** weaken tests.
Do **not** add forward-looking tests for other work.
Do **not** widen proof scope outside the seam.

---

## Mandatory L1 declarations before coding

In **L1**, before any implementation leaf starts, record in the supplementary report:

1. exact files to change
2. exact proof files to change, if any
3. explicit statement that:
   1. the blocked Tranche 4 attempt is disregarded and not continued
   2. the supplementary remediation starts from accepted Tranche 3 baseline `2c9437ae92642d3213c88b81b65f2e2f19b5ba4b`
   3. `observed_at` will be removed from the active seam
   4. no backward compatibility is allowed

If any of those cannot be stated exactly, stop and report the blocker before doing further work.

---

## Required leaf structure

Use this exact bounded sequence unless a blocker prevents it:

1. `SL1-read-scope-and-seam-declarations`
2. `SL2-raw-bundle-provenance-remediation`
3. `SL3-preparation-seam-remediation`
4. `SL4-coupled-proof-and-receipt-remediation`
5. `SL5-clean-closeout`

One active leaf at a time.
Do not batch everything into one opaque commit.

---

## Proof requirements

After the final supplementary closeout commit, rerun exactly:

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

1. the blocked Tranche 4 attempt was disregarded for execution purposes
2. the supplementary remediation began from accepted Tranche 3 baseline `2c9437ae92642d3213c88b81b65f2e2f19b5ba4b`
3. the preparation/raw-bundle seam was corrected
4. internal `observed_at` dependency was removed from the active seam
5. exact proof files changed, if any
6. authoritative closeout ref used for this supplementary closeout

The report must not rely on hand-back-summary placeholders.

---

## Authoritative closeout mechanism — mandatory

Use this exact pattern:

1. make one final bounded supplementary closeout commit on the existing supplementary Tranche 3 branch
2. create one annotated Git tag named:

`temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-preparation-raw-bundle`

3. the tag must point to the final clean supplementary closeout commit
4. tracked receipts must record that exact authoritative closeout ref name
5. do not use hand-back-summary placeholder wording

---

## Branch and packaging requirements

1. leave the branch as `work/temporal-standard-tranche-3-supplementary-preparation-raw-bundle-remediation-20260422`
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
   8. exact files changed
   9. exact proof files changed, if any

---

## Definition of done

This supplementary brief is complete only if all of the following are true:

1. the blocked Tranche 4 attempt was disregarded and not continued
2. the work started from accepted Tranche 3 baseline `2c9437ae92642d3213c88b81b65f2e2f19b5ba4b`
3. `observed_at` is removed from the active preparation/raw-bundle seam
4. `runtime_preparer.py` no longer depends on `bundle.provenance.observed_at`
5. no backward-compatibility shim was introduced
6. updated report is complete
7. workbook is updated
8. proofs rerun clean
9. repo is clean
10. branch remains unmerged
11. supplementary authoritative closeout tag exists and points to the final clean commit

If any one of those is false, stop and report the blocker truthfully.
