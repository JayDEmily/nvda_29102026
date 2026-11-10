# T00 documentary evidence — R2/G0/F02 recovery status

**Date:** 10 November 2026 (Australia/Melbourne)  
**Status:** `T00_PARTIAL_VERIFIED / BLOCKED_RECOVERY_OF_REPAIRED_CANDIDATE`  
**Purpose:** Preserve exactly what this investigation could verify about F02. **This is a read-only investigation record, not an independent F02 repair acceptance, active ExecPlan or product-test result.**  
**Related proposed sequence:** [EXEC_PLAN.md](EXEC_PLAN.md), stage T00; [companion ADR](ADR_20261110_POSTGRESQL_ADDITIONAL_BACKEND.md).

## 1. Verified earlier independent dispositions

The text of the following original independent reports was read **in full** from the user's NVDA Library (the exact original raw Markdown bytes were not materialisable in the current container):

1. **`NVDA_R2_G0_INDEPENDENT_DOCUMENTARY_REVIEW_20261030.md`**, 30 October: returned original candidate `f9a6de2400b22f361678ffd545d7e38666b8bae5` for F01, unqualified `TEST_EVIDENCE_LEDGER.json` candidate identity; the cumulative Git bundle was not reviewed.
2. **`NVDA_R2_G0_L00_INDEPENDENT_REVIEW_AMENDED_20261031.md`**, 31 October: independently accepted the bounded **F01 provenance-documentary correction**, and explicitly did **not** accept overall G0/L00 without restored Git candidate/checkpoint.
3. **`NVDA_R2_G0_L00_INDEPENDENT_GIT_REVIEW_20261031.md`**, 31 October: independently restored the cumulative baseline/additive checkpoint; `PASS_GIT_CHECKPOINT`, F01 `CLOSED`; full G0/L00 `RETURN_FOR_BOUNDED_REPAIR` for newly identified **F02**, not for a measured SQLite or product defect.

The reviewed exact F02 predecessor is commit **`9a4f1e827accdd7cfe3d7a14d5575573589b1acd`**, tree **`b876d8824c456988cf40398d4bf6b9298906f9d6`**, direct parent `22a2f13189fa3f1a55b2fef265f93a6696c0155f`; independent report states `git bundle verify`, restoration, 66/66 original refs, 4,024-entry tracked inventory and `git fsck --full` passed on that predecessor. It does **not** cover the later repair.

**Exact F02 mismatch on that predecessor:** `handoff/m02_completion_28_execution/L00/R2_G0_SQLITE_INDEPENDENT_REVIEW_REQUEST.md:28` and `handoff/m02_completion_28_execution/L00/R2_SQLITE_RUNTIME_DECISION.md:7` claimed a tracked launcher `tools/with_pinned_sqlite.sh` loaded the SQLite 3.54.1 library. The independent reviewer examined the Git tree and found no such file in that candidate or its cited predecessors. The prescribed repair was to supply the actual tracked executable helper **or** correct those documents to the real reproducible `LD_LIBRARY_PATH` invocation, then re-export and independently restore the new bundle. No product-test rerun was justified.

## 2. Later Worker repair — attributed, not independently accepted

The original Worker conversation reports a bounded documentary correction of both launcher assertions to a direct `LD_LIBRARY_PATH` launch mechanism; it reports CPython 3.13.5 / SQLite 3.54.1 non-product preflight, fresh bundle restoration, 66 ref tips, the 4,024-entry tracked listing and `git fsck`. **Those are attributed Worker reports, not newly observed here.**

- Reported repaired commit: `16b7cc67f5d24336d3768e2da006819474a8c792`.
- Reported repaired tree: `2b2bd7c1b7342f22909339a99150e2a395039e06`.
- Reported cumulative additive: `NVDA_R2_G0_L00_F02_SQLITE_LAUNCH_CORRECTION_CUMULATIVE_FROM_97f944d51ab9.bundle`.
- Reported review handoff: `NVDA_R2_G0_L00_F02_INDEPENDENT_REVIEW_HANDOFF_20261031.zip`.
- Reported final external receipt: `R2_G0_L00_F02_FINAL_EXTERNAL_RECEIPT_20261031.json` (contained within the inaccessible handoff/other candidate source).
- Worker's disposition: `WORKER_REPAIR_VERIFIED — INDEPENDENT_G0_ACCEPTANCE_PENDING`.
- Reported product tests: zero.
- **No post-repair independent F02 review or acceptance of this exact repaired SHA was found in the inspected records.** This is a scoped evidence statement, not a claim that such a review could not exist elsewhere.

## 3. Current file inventory and actual access limitation

The user's NVDA Project Library reports the following **metadata only**:

| Library file | File ID | Bytes | Created UTC |
|---|---|---:|---|
| `NVDA_R2_G0_L00_F02_INDEPENDENT_REVIEW_HANDOFF_20261031.zip` | `file_00000000a7f081faa2c1531fe4082b7d` | 1,034,400 | 2026-10-30 23:25:08 |
| `NVDA_R2_G0_L00_F02_SQLITE_LAUNCH_CORRECTION_CUMULATIVE_FROM_97f944d51ab9.bundle` | `file_00000000c30c81faa707d08785cc1da4` | 1,000,499 | 2026-10-30 23:25:12 |

Two `files.materialize` original-byte attempts, on these exact Library file IDs, returned `This Project file does not have an authorized raw-byte materialization path`. A `files.read` attempt on both files returned the same limitation. The original *review Markdown text* remained readable. Neither ZIP nor bundle was downloaded/hashed/restored in this T00 investigation, so the listed file sizes do not independently prove their contents.

Searches for the relevant F02/G0 filename terms in both connected Google Drive accounts (Shoko and James Student) returned no matching results; this is **not** a general proof of absence across other storage systems. The current model container's `/mnt/data` contains nine separate older historical NVDA archives/bundles (August through 28 October), but not these exact later files. Filename-search checks on the connected user's Ubuntu home and Windows Users directories did not identify the exact later handoff; some Windows locations denied read permission.

On the real Ubuntu PC, the freshly cloned `/home/jds/nvda_29102026` working tree remained clean at `main` `8ff7d82377e9bf8f9fc75c1ecef70f0ab29a2ada`. Explicit `git cat-file -t` checks for the local-only commits `22a2f131…`, `9a4f1e827…` and `16b7cc67…` failed; those objects are **not present in the currently cloned object's namespace**. This does not undermine the reviewer-verified earlier bundle, only our current inability to inspect its successor.

The separate Ubuntu original-baseline + R1 L00 successor transfer had previously been verified with its original ref tips, source/target tree and `git fsck`. That result is **not** an acceptance of the local R2/F02 repaired candidate.

## 4. Exact remaining T00 acceptance condition

**F02 repair disposition: `UNKNOWN_AFTER_WORKER_REPAIR`.**  
**T00 recovery: `BLOCKED_RAW_CANDIDATE_AND_INDEPENDENT_VERDICT`.**  
**F01 original documentary correction:** previously independently `ACCEPT_DOCUMENTARY` (bounded).  
**Git transport for predecessor `9a4f1e827…`:** previously independently `PASS_GIT_CHECKPOINT` (bounded).  
**Latest `16b7cc67…` exact Git restore, tree, runtime launcher and independent acceptance:** NOT YET VERIFIED.

The first unmet invariant is receipt of the **original 31 October F02 ZIP or exact cumulative Git bundle bytes** through an authorised accessible path, followed by an independent readback/review of the repaired candidate. A ZIP filename or Worker report cannot substitute for the missing bytes or reviewer determination.

### Required bounded verification once bytes are available

1. Record original ZIP SHA-256, size, member list, no traversal/duplicate/symlink hazards and exact member manifest integrity. Identify the embedded or companion bundle and external receipt, without assuming the ZIP contains everything.
2. Independently restore the original fixed baseline and full F02 additive into a separate receiver; run `git bundle verify`, verify all declared refs including original 66, exact repaired SHA/tree/parent chain, full tracked file inventory, ancestry and `git fsck --full`.
3. Compare actual predecessor-to-repair Git diff with the two specific F02 documentation claims; check the new `LD_LIBRARY_PATH` invocation, library-source identity and its documented prerequisites. Do not require a fabricated helper.
4. Verify any required **non-product** SQLite version/preflight on an authorised reproducible environment; do not infer dynamic-link qualification from Markdown alone. Keep original nine worker-reported feature checks attributed unless independently witnessed.
5. Have an independent documentary reviewer determine `ACCEPT_F02`, `RETURN_FOR_BOUNDED_REPAIR` or `BLOCKED` for the exact repaired candidate. Record the independent report and link all checks to that SHA; do not retroactively amend the older review.
6. Only after actual accepted root authority and explicit separate commission update the active G0 ledger, select an execution branch or proceed to dependent product implementation.

## 5. No changes during T00

This record is added **only to the proposed planning branch**, without changing `GUARDRAILS.md`, `AGENTS.md`, root `EXEC_PLAN.md`, any source, tests, proof admission or environment. No product tests, package installations, operational server changes, proof outcomes or remote-main changes were performed. No G0, L00, R2 or backend activation is claimed.

**Next specific input:** make `NVDA_R2_G0_L00_F02_INDEPENDENT_REVIEW_HANDOFF_20261031.zip` (1,034,400 bytes) available as an actual readable attachment or a verified accessible link; recovery then resumes at the independent Git-restore checkpoint.
