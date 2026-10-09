# Current Repository State

## Status

## 10-10-2026 F4 RC01 + RC14 exact-contract proof; clean M00 durability (current)

**F4 internal checkpoint only, Stage 1 not accepted.** Public M00 tests now cover
D010's versioned market-session calendar (including known false closure),
D085/D086 exact option-contract whole days and ACT/365F expiry, and the
contract-qualified D087/D088 midpoint/spread and D089/D090 strike/spot and log
moneyness (including cross-contract decoy, missing/future/zero-spot refusal and
native/derived lineage). Added proof commits `daf8ab2` and `d4442fa`;
no production code change was required for these additional seven rows.

All **832 applicable non-durability tests** pass under pinned pytest 9.0.3,
Python 3.13.5, PostgreSQL 17.9 and independent M00/M01 roles. Ruff and
source mypy pass. The previously excluded 55 M00 PostgreSQL durability tests
have now **all passed in eight non-overlapping batches in a clean pinned Python
virtualenv**. The failed ambient-Pydantic graph-walk invocation and successful
isolated readback are both preserved; see
`handoff/m01_completion/proof/f4_20261009/F4_M00_DURABILITY_CLEAN_READBACK.md`.

Conservative authority-locked ledger: **490 dependency edges + D007 sentinel**;
**222 outstanding Stage-1-closed public relationship edges across 92 rows**;
**30 cross-stage own-kernel and lawful public refusal obligations still open**.
No Stage-1 acceptance or Stage-2 authority is asserted. Historical 240/255/272
counts below are superseded by this readback, not erased from Git.

## 10-10-2026 F4 RC01 temporal and RC02 VWAP gap public proofs — latest

**F4 remains internally in progress, not an acceptance submission.** The public
M00→M01 graph proof for D018 establishes exact recursively constructed D017
VWAP against independent provider VWAP, exact numeric difference/bps, lineage,
and missing/ineligible-input refusal (proof commit `ff1bb57`). D001–D005
independent temporal public proofs use true provider-native instants, session
boundary and source kinds. They exposed a D002 public graph failure for a
lawful `receipt_only` observation (`97857be` failing proof). The bounded repair
at `d5c34df` uses actual selected M00 R002 source kind: true-instants still
require D001, while receipt-only age uses M00 received time with no fabricated
D001; date-only refuses seconds-valued age. The governing catalogue and M00
source ownership were unchanged.

Applicable combined PostgreSQL 17.9 non-durability regression: **809 passed**;
Ruff and source mypy (21 files) passed. Full-Git checkpoint and exact current
commit are recorded in Git, with commands and logs in
`handoff/m01_completion/proof/f4_20261009/`. Current catalogue remains
**490 authoritative edges + D007 sentinel**; **240 Stage-1-closed edge
obligations across 99 rows** remain unproved, as do the **30 cross-stage
own-kernel/public-refusal obligations**. These are evidence obligations, not
presumptively production defects. Stage 1 not accepted; Stage 2 unauthorised.
The earlier 255/272 counts below are preserved historical checkpoints.

## 10-10-2026 F4 RC02 expanded continuation — latest proof inventory

**Internal checkpoint only:** A further eight RC02 raw-scalar rows have been
proved through independent controlled M00 public records: D025, D042, D043,
D047, D057, D058, D059 and D060. Each has exact persisted numerical result,
separate raw occurrence lineage, missing-source refusal, future/foreign-subject
refusal and retry proof; D025/D060 additionally refuse zero denominators.
Proof-first Git commit `892ab71`. Combined PostgreSQL 17.9 M00/M01 regression:
**793 passed**; Ruff and 21-file mypy checks pass. There is no production code
change in the expanded RC02 proof unit.

The current reconciled 490 authoritative edges and D007 zero-edge sentinel
contain **255 unproved Stage-1-closed relationship edges across 105 rows**;
**30 cross-stage own-kernel/public-refusal obligations** remain unproved.
Neither Stage 1 nor F4 is accepted. Stage 2 remains unauthorised. See the
latest `F4_PROGRESS_READBACK.json` for exact dispositions. The immediately
following 272-edge RC02 and earlier F4 entries are historical snapshots, not
current status.

## 10-10-2026 current F4 continuation — supersedes older F4 blocker/count statements below

**ACTIVE: F4 INTERNAL PROOF; NOT A STAGE-1 CANDIDATE.** The Programme Owner's
09-10-2026 narrow normative exception adding R187 to D134/D135 and the shared
positional-book repair are committed in the ancestry. Most recent RC12 book
public proofs are in the base checkpoint `db943a7`; the inherited blocker is
resolved, not an active authority stop. The retained original red witness and
explicit-operation green replay are both in Git. The accepted catalogue digest
is `8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a`.

**Further F4 RC02:** New independent public-M00 proofs for D011/D012/D013/D014
establish exact NBBO arithmetic (101, 2, 200/101, 0.6), raw/predecessor lineage,
missing/future/wrong-subject refusal and deterministic retry. Eleven focused tests
pass. Reconciliation readback accounts for 490 normative edges plus D007 sentinel;
**272 Stage-1-closed dependency proofs remain open across 113 rows** and all
**30 cross-stage own-kernel/refusal obligations remain open**. No unproved edge
has been labelled a defect or accepted by inference.

Current post-RC02 rerun: **768 applicable non-durability tests passed** against
live PostgreSQL 17.9 with distinct M00/M01 test roles; Ruff clean and source
mypy 21 files clean. The first attempt had one test-environment database CREATE
privilege failure; corrected role setup and whole-suite rerun are preserved as
separate logs. The 55 M00 durability tests **have not been rerun in this pass**.
Source of truth for exact per-edge status:
`handoff/m01_completion/proof/f4_20261009/F4_PROGRESS_READBACK.json` and the
associated F4 ledger/matrices. F4 remains in progress; Stage 1 not accepted;
Stage 2 unauthorised. Older headings/statements below retain historical context
and must not be read as current routing or counts.

**M01 COMPLETION CONTINUATION — F4 INTERNAL PROOF IN PROGRESS; F2 ACCEPTED, F3 WORKER CHECKPOINT PRESERVED; STAGE 1 NOT ACCEPTED**

The previous foundation-cleanup checkpoint was not the end of M01. Current Programme Owner instruction is to continue and finish M01 before commissioning a later module.

**09-10-2026 F3 worker checkpoint:** Following independent F2 `F2_ACCEPTED`, F3a D109/D170 exact-contract graph proofs and F3b D121/D122/D124 multi-contract grouping repairs have been committed proof-first, and F3c reconciles 488 F1 edges (plus one zero-edge sentinel) with accepted F2 and bounded F3 evidence. All 720 combined applicable tests and 55 separately batched M00 durability cases pass; static/type/architecture checks pass. **This is F3 worker evidence only, not Stage-1 or F4 acceptance**. Full F4 class/144-row public reachability evidence remains unreconciled. Details: `handoff/m01_completion/proof/f3_20261009/F3_PROOF_AND_F4_BOUNDARY.md`. F4 is next; Stage 2 is unauthorised. Older F2-era statuses below are retained as history and superseded by this paragraph for current F3 routing.

**09-10-2026 F4 INTERNAL WORKER CHECKPOINT (most recent):** After the F3 `36105f0` proof checkpoint, F4 public M00→M01 witnesses established D145 four-field OFI event reconstruction and D151 component-specific basket breadth, with proof-before-production repair for D145 incomplete-event refusal. Combined regression: 725 passed with separate PostgreSQL M00/M01 role connections; Ruff, mypy and structural validation passed. The exact F1/F3 relationship readback now records 8 bounded F4 edges and **344 Stage-1-closed edges still awaiting edge-specific F4 proof**. Full 144-row public reachability and 30 cross-stage own-kernel/refusal evidence are **not yet established**. This is **not** a Stage-1 review candidate; F4 continues internally without an intermediate reviewer round-trip. See `handoff/m01_completion/proof/f4_20261009/F4_WORKER_PROGRESS_AND_UNRESOLVED.md`. The earlier F3/F2 statuses below remain historical evidence.

**09-10-2026 F4 LATEST — AUTHORITY BLOCKED (supersedes earlier F4 internal progress):** F4 continued with proof-first D139/D140/D143/D144 book semantics and D007 public policy-projection repair. A new controlled public D134/D135 test exposes an operation dependency mismatch: the accepted D134/D135 raw set is R185/R188/R190, whereas the source reconstructs with undeclared R187. Whether these declared inputs constitute a complete snapshot or require event-stream replay lacks a governing snapshot-completeness/representation contract; therefore F4 is **BLOCKED** at this first invariant, not complete and not a Stage-1 review candidate. Proof-first failing witness is preserved. Current ledger retains 317 unproved Stage-1-closed dependency edges (including D134/D135) and the unproved full 144/30 row obligations. The bounded regression excluding the deliberately failing witness passes 734 tests. Exact blocker and recommended single authority resolution: `handoff/m01_completion/proof/f4_20261009/F4_RC12_D134_D135_AUTHORITY_BLOCKER.md`. No Stage-1 or Stage-2 acceptance/authority. Earlier statuses below are historical.

## Repository boundary

- Continuation branch: `work/m01-completion`.
- Branch base: clean `main` commit `8cd63f2723b936ea8f5a6cfb558b69a4750e6667`, tree `c1bd5cdcbbee31bbb3b18a43840f47e607f254e8`.
- Package/distribution version remains `1.0.0`.
- `.pcm/` is not active authority and must not be recreated.
- M00 remains the completed Raw Signal semantic owner.
- M01 architecture identity and foundation are established; M01 remains incomplete until the accepted D001–D209 calculation responsibility and integration are realised and independently accepted.

## Accepted starting evidence

The final independent foundation review PASS is preserved at:

`handoff/m01_completion/review/DS_R01_FOUNDATION_PASS.json`

Result semantic SHA-256:

`13de5887f33c5806581536adc05d052b7ac3398b76458ed39d9381b7b2f2ca91`

Exact accepted M01 authority is under `handoff/m01_completion/authority/` and indexed by `handoff/m01_completion/AUTHORITY_INDEX.md`.

## Current actor and next action

**Independent consolidated F2 disposition, 09-10-2026:** Candidate `867b875ba58063d2531ba67c9fe9fa2c76adc310` has now received bounded **F2_ACCEPTED** independent review. Report: `handoff/m01_completion/review/M01_F2_CONSOLIDATED_INDEPENDENT_REVIEW_20261009.md`; worker routing: `handoff/m01_completion/repair/M01_F3_AFTER_F2_ACCEPTANCE_WORKER_HANDOFF_20261009.md`. F3 is the next authorised internal unit; F4 remains the next whole-Stage-1 independent acceptance boundary. Real provider-native event identity and real R289 category-to-score extraction remain unverified. **F2 acceptance is not Stage-1 acceptance; Stage 2 remains blocked.** The older blocked/checkpoint descriptions below are historical and superseded in current routing.

**LATEST programme-owner decision 09-10-2026 14:13 AEDT — controlled provider-independent F2b authorised:** The 13:55 missing-live-provider-field stop is superseded **only for provider-independent M01 calculation**. Controlled versioned M00 projections with canonical `event_id` and explicit `(source_provider, source_variant, event_id)` were used to prove raw R289 K07 scoring and R284/D064 event matching, competing event ranking, revised schedule/importance, cutoff, ambiguity, version refusal and source/predecessor lineage. F2a contemporaneous trade/quote repair and reviewer witnesses are carried forward. F2 relationship ledger and proof evidence: `handoff/m01_completion/proof/f2_observation_identity_20261009/F2_EDGE_RECONCILIATION.csv` and `handoff/m01_completion/proof/f2b_provider_independent_20261009/`. **One consolidated F2 candidate is for independent review, NOT accepted**. Actual provider-native mappings/stability and live-provider integration remain unverified; no M00 provider adapter or future strategy `event_filter_enabled` was implemented. F3, F4, Stage 2 remain unauthorised. Historical statuses below are superseded by this paragraph to the extent they identify live-provider absence as an F2b implementation blocker.


**F2b source-verification checkpoint — Programme Owner's PROPOSED event-identity rule, 2026-10-09 13:55 AEDT:** The proposed `(source_provider, source_variant, event_id)` correlation is structurally representable via versioned M00 selection-identity mappings, but the active repository contains **no actual provider-native R284/R289 event records, exact native event-ID path or demonstrated identifier stability across revisions**. The first mandatory source invariant is therefore `UNKNOWN` and F2b remains **BLOCKED** *specifically on the missing provider-native field/contract*, rather than on a general inability to express correlation. See `handoff/m01_completion/repair/M01_F2B_AUTHORITY_BLOCKER_20261009.md` for exact searches, source-contract requirement and the separate raw-only D064 scoring code gap. No F2b production change, proof-first repair, F2 acceptance or F3/F4/Stage-2 authority has resulted. Preserve earlier F2a and 13:41 event-filter separation; retain one consolidated reviewer return only when authorised closure is actually proved.


**Current checkpoint (09-10-2026): F2a has a proof-first temporal-sign repair at worker Git `ede6c6b7efe32ea5a45f0be160f25d377535a821`. F2b remains `BLOCKED` on the unestablished stable event identity and revision-matching law connecting separately updated R284 and R289 records.** The programme owner has clarified that M01 must preserve actual D064 scores and D065 `TRUE`/`FALSE` calculations. The proposed event-level coefficient range `0.01–100` and permanently-`TRUE` D065 are rejected. The *deferred*, non-M01 strategy parameter is `event_filter_enabled: Boolean = FALSE`; downstream FALSE means no event-window filtering, TRUE applies the actual D065 result, and unavailable D065 must not be coerced into a Boolean. This is a decision-record only, not permission to implement that future module or to relax the blocker. See `handoff/m01_completion/repair/M01_F2B_AUTHORITY_BLOCKER_20261009.md` for the exact unchanged authority question. No F2b/F2/Stage-1 acceptance; no F3/F4/Stage-2 authorisation.

**Historical 13:41 checkpoint actor — superseded in blocker detail by the 13:55 source-verification checkpoint above:** The prior authorised routing was F2a contemporaneous quote/trade repair, then F2b D064/D065 event-score prerequisite and other F2 observation relationships, with two internal proof-before-code checkpoints and one consolidated independent F2 review only after both units are proved. That routing amendment remains in root `EXEC_PLAN.md` and `handoff/m01_completion/repair/M01_F2_CONSOLIDATED_WORKER_HANDOFF_20261009.md`; it superseded the F2a-only *interim reviewer stop* but never overrode the mandatory immediate stop for a missing F2b identity/revision rule. F1 remains accepted; F2, F3, Stage 1 and Stage 2 are not accepted/authorised.

Programme Owner amended the Stage-1 acceptance boundary on 2026-10-08 to resolve the normative cross-stage dependency circularity: 174 Stage-1-kernel rows comprise 144 Stage-1-closed rows and 30 cross-stage rows whose end-to-end reachability is deferred until Stage 2. The amendment is recorded in root `EXEC_PLAN.md` and `handoff/m01_completion/STAGE1_ACCEPTANCE_BOUNDARY_AMENDMENT_20261008.md`.

The latest independent Stage-1 review of worker `514cf90` is `REPAIR` / `RECURRENT_CLASS`, recorded in `handoff/m01_completion/review/M01_STAGE1_REVIEW_RESULT_514cf90e4c49.json` and `handoff/m01_completion/repair/M01_STAGE1_SIGNED_TRADE_LINEAGE_REVIEW_HANDOFF_20261008.md`. Public-seam D015→D016 and D015→D120 proofs fail: exact trade sign +1 is lost through mistaken cross-namespace occurrence-ID joins, producing persisted zero instead of signed volume/notional. D121/D122 grouping remains independently unassessed. The prior D109/D170 selection repair was not invalidated by these proofs.

**Latest Programme Owner plan amendment (2026-10-08):** root `EXEC_PLAN.md` (plan-change commit `89f6c012342f1508222700a3acb1f301b6c6723b`) introduces F1→independent inventory review→F2→F3→F4→independent whole-Stage-1 review. The independent reviewer has now issued `F1_INVENTORY_ACCEPTED` for evidence-only candidate `d27b275bbdc696fab561f20a9fd94dfd4a92de47`, recorded at `handoff/m01_completion/review/M01_F1_INDEPENDENT_REVIEW_20261009.md`. **Execute F2 only** in the next worker pass under `handoff/m01_completion/repair/M01_F2_OBSERVATION_IDENTITY_WORKER_HANDOFF_20261009.md`, using proof-before-production commits. Earlier three-leaf proofs are preserved for F4 reconciliation; they are not declared accepted. See `handoff/m01_completion/foundation/STAGE1_F1_INVENTORY_ONLY_WORKER_HANDOFF_20261008.md`. **Stage-1 acceptance is blocked; do not start Stage 2.**

Financial Calendar, later-module work, PCM reinstatement and package-version changes remain out of scope.
