# T01 — reconciled source, authority and checkpoint decision

**Date:** 11 November 2026, Australia/Melbourne
**Status:** `SOURCE_RECOVERED_AND_PUBLISHED / PROPOSED_SUCCESSOR_NOT_ACTIVE`
**Scope:** exact documentary/transport reconciliation and proposed governing files, not NVIDIA implementation, product testing, runtime/driver acceptance or programme promotion.

## 1. Verified source and provenance

The source for these proposals is the **exact original recovered local R2/G0/F02 commit** `16b7cc67f5d24336d3768e2da006819474a8c792`, tree `2b2bd7c1b7342f22909339a99150e2a395039e06`, direct parent `9a4f1e827accdd7cfe3d7a14d5575573589b1acd`; it is **not** the older GitHub draft and not the current `main` tree.

Two distinct independent read-only restorations ran during this T01 investigation: one in a fresh isolated container bare repository; the other on authorised Windows `DESKTOP-I188O30` / WSL Ubuntu, using the original F02 ZIP and original 28 October full-history baseline downloaded from the user's ChatGPT Library. The Windows SHA-256 of the downloaded ZIP and baseline matched the previously independently recorded file identities.

- F02 ZIP SHA-256: `987aef326d301775e313cdc32556924bef52c446e68ac4ff1c18508aae43767a`, 1,034,400 bytes.
- Additive bundle SHA-256: `b95f05ceba8d873603a5c79894011d2b0babbfc43df674e54175a55b0f11ad2b`, 1,000,499 bytes.
- Baseline archive SHA-256: `4d02c82894513bff8d07af7a2af6a151cd3f5f14ece581ac0bf0d87ea9ed0430`, 42,559,431 bytes.
- Baseline full-history Git bundle SHA-256: `91db4a1989bff366c1f547c5776ca886c276b6b1310027ae929aa1cd1efee4b9`, 42,608,833 bytes.
- Exact candidate SHA/tree/parent, 66/66 original named tip identities (67 restored refs total), 4,024 tracked file entries/inventory SHA-256 `6e24293d7908a3bce9e950bfd16cfa967c06c907a4f72bf54b8de0172dbdd432`, both `git bundle verify`, and `git fsck --full --no-reflogs` PASS.
- The F02 commit changes exactly two documentation files: `handoff/m02_completion_28_execution/L00/R2_G0_SQLITE_INDEPENDENT_REVIEW_REQUEST.md` and `handoff/m02_completion_28_execution/L00/R2_SQLITE_RUNTIME_DECISION.md`. The original claim of tracked `tools/with_pinned_sqlite.sh` was false; the repaired records identify the real tracked `tools/check_sqlite_runtime.py` plus a conditional `NVDA_SQLITE_LIBDIR` / `LD_LIBRARY_PATH` launch.
- On 10 November, an independent documentary reviewer issued `ACCEPT_DOCUMENTARY_F02 / PASS_GIT_CHECKPOINT` for these *exact bytes*. No independent SQLite binary qualification, product-test acceptance or active successor-plan acceptance follows from that review.

Verifiable receipts retained verbatim in this directory: `UBUNTU_F02_RESTORATION_RECEIPT.json`, `ORIGINAL_66_REFS.json`, `GITHUB_REMOTE_RECEIVER_RECEIPT.json`. The baseline and additive raw bundles are staged in the isolated Ubuntu recovery directory, not committed to source Git.

## 2. Actual Git publication and fresh receiver

The authorised WSL Git client atomically pushed five **new** source-recovery refs into `JayDEmily/nvda_29102026` (no ref overwrites, no force-push):

| Remote branch | Exact SHA |
| --- | --- |
| `recovery/r2-g0-f02-20261111` | `16b7cc67f5d24336d3768e2da006819474a8c792` |
| `recovery/legacy-d131-20261111` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` |
| `recovery/legacy-d010-20261111` | `77471e5a851ec04e73c6dc63988868064de930f8` |
| `recovery/legacy-next20-20261111` | `8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e` |
| `recovery/legacy-m00-brief2-20261111` | `0c86b187a23e750d39ce04f772f7d52c1bd578b0` |

The candidate's ancestors hold 9 of 13 original unique historical tips. The four additional branches preserve the remaining four non-ancestor tips, which were otherwise at risk of being absent from the remote. Five remote refs do **not** equal 66 original ref names. The full 66-name/tip map is preserved by `ORIGINAL_66_REFS.json`.

A **separate fresh Ubuntu bare Git receiver** fetched these five refs solely from GitHub, independently recreated the 66 original named refs from the immutable source manifest, matched target HEAD/tree and 4,024 tracked entries/inventory SHA-256, and passed `git fsck --full --no-reflogs`. The result is `GITHUB_REMOTE_FRESH_RECEIVER_FULL_GIT_INTEGRITY_PASS`, **performed by this planner, not a separate ChatGPT tester**. Historical evidence refs not in the manifest and non-Git SQLite shared-library assets have not received independent end-to-end receiver verification.

The separate 10 November **arithmetic** cross-thread proof established Chrome ChatGPT project message submission, fresh-thread GitHub discovery and a committed result. It did *not* inspect 4,024 paths or independently test the revived full-history receiver. The exact method is now in `docs/automation/CHATGPT_GITHUB_HANDOVER_UIA_20261110.md`, copied byte-for-byte from `main` onto this proposed successor lineage, with no automatic role activation.

## 3. Chronology and actual authority

1. The historical R1 branch `execution/accepted-r1-20261030` @ `363923d47b81fca50e64036bef3c8601501e3c16` was commissioned but stalled at L00 transfer; its WORK_DELEGATED per-leaf test schedule and old bundle law are not evidence of R2 acceptance.
2. GitHub `planning/chat-manual-r2-20261030` @ `6feb50bf8a96e244cbd68eb57536f940be6335b3` was an explicitly *proposed* CHAT_MANUAL model. Its root text is **not** the accepted 30 October local R2 root.
3. The recovered local R2, subsequently independently reviewed at F02, explicitly records the owner's approval for separate manual Worker/Tester and a **local bundle-only** workflow. Its 463-line root `EXEC_PLAN.md`, local `AGENTS.md` and test override remain unchanged on the 16b7 recovered source. Local-only/no-GitHub directions are historical to that phase.
4. Current owner's **later** direction selects independent ChatGPT Worker/Tester conversations inside NVDA where practical, Ubuntu and GitHub durable handover, and a PostgreSQL **additional** M00 backend alongside retained M00/M02 SQLite. The November PostgreSQL ADR is owner-endorsed *direction*, not tested backend or implementation commission.
5. `main` @ `7e2601a5e050d76202b1b6d3f69fc167a04c91f7` contains the successful Windows UI Automation/GitHub runbook. A newer timestamp or main branch does **not** override the recovered R2 source tree. This proposal deliberately carries forward only the runbook content as a documented tool operation.
6. The 10 November T00–T07 supplementary plan is `PROPOSED_NOT_ACTIVE`. Do not install it as a competing root ExecPlan; its approved parts must be reconciled into one exact successor.

**Historical source versus proposed target difference:** the reviewed local `EXEC_PLAN.md` is the 39-leaf `R2_CHAT_MANUAL_LOCAL_OWNER_APPROVED` document (Git blob `95aa1090e02585673f81f16e9a72c150353c0120`). The new complete `PROPOSED_EXEC_PLAN.md` is derived from *those* 39 source leaf contracts, replacing only appropriately scoped transport and authority descriptions, and appending a separate T00–T07 roadmap, **not** overriding original source. A complete separate owner-reviewed diff is still required before copying it to the active root.

## 4. Exact proposed artefacts (not installed)

- `PROPOSED_EXEC_PLAN.md`: full 39-leaf successor text, 39 preserved GitHub leaf rules, original scope and proof limits, explicit source/decision history, proposed GitHub-pinned checkpoint contract, no newly admitted product cases, 8 supplemental T-stages.
- `PROPOSED_AGENTS.md`: full proposed root instruction, includes navigation to the exact operational handover runbook; not an effective root `AGENTS.md`.
- `PROPOSED_TESTS_AGENTS.override.md`: full proposed test-local supplement; sole independent Tester at L32, untested Worker, existing negative/strict proofs preserved, stage authority explicitly not activated.
- `PROPOSED_TEST_EVIDENCE_LEDGER.json`: **DRAFT**, complete original 35 proof obligations byte-semantically unchanged, 34 scheduled L32 plus paused D145 L31, zero executed product runs, zero released cases. Source SHA updated only in proposed `repository.candidate_commit`; active original ledger unchanged.
- `PROPOSAL_SOURCE_MANIFEST.json`: original source Git blobs and proposed scope.
- Three attached source/remote integrity receipts, including explicit statement separate ChatGPT Tester has **not** run.
- Copied main runbook at `docs/automation/CHATGPT_GITHUB_HANDOVER_UIA_20261110.md`, sole new documentation path outside this proposal folder.

Proposals were audited under the exact original `handoff/planning/m02_foundation_completion_20261030/TEST_EVIDENCE_LEDGER.schema.json` with Python `jsonschema` Draft202012Validator, **FULL PASS**, and independent assertions that 35 source obligations match unchanged, 39 plan leaf headings remain, D145 paused, zero new runs and fixed original GUARDRAILS blob. An initial draft contained two *new proposal-generation schema mismatches* (status outside enum, extra repository key); these were corrected **before** committing. They were not defects in the original R2 source.

No root `EXEC_PLAN.md`, root `AGENTS.md`, `tests/AGENTS.override.md`, frozen `GUARDRAILS.md`, existing ledgers, source code, tests or product proof admission were altered.

## 5. Material unknowns and exact next gates

1. **T01 formal acceptance pending.** Proposed complete successor root, AGENTS and test override require **genuinely independent documentary review of exact committed files** and owner's exact acceptance. After that, a separately authorised installation can promote the proposed root and update the active registers with a recorded reviewable commit. This packet does not do so.
2. **T02 separate Tester independent receiver pending.** The planner verified the actual Git-only receiver; a distinct ChatGPT Tester must run its *own* fresh Git restoration, check every required historical/evidence ref name/tip closure, tree/full inventory, full fsck, external asset identity and publish its own receipt. A simple file-preview or arithmetic example is insufficient.
3. **T03 actual Ubuntu environment unqualified.** Re-run no product tests merely because Python changed; separately establish exact CPython3.13.5 and dynamic-linked SQLite3.54.1 binary from an identified source and governed dependency set. No current runtime qualification result is claimed in this T01.
4. **T04 additional M00 PostgreSQL not qualified.** Existing M00 PostgreSQL adapter and A00 selection are observed in source. PostgreSQL server 18.6 and Psycopg3.3.4 operation, schemas/roles and separately admitted M00 persistence/concurrency claims remain future separately governed work; M02 SQLite and M01 bootstrap stay unchanged.
5. **No product implementation/test/gate/identity acceptance** from this documentary work. Retain 39 leaves, 35 signal proof obligations, 27 new mandatory identities (20 core + 7 further), 28 held (including D145 paused), seven external holds, 98 historical controlled profiles and the 126 conditional foundation accounting. No automatic new D identity acceptance or backend claim.

**Proposed next commissioning step:** a fresh ChatGPT independent documentary reviewer of this pinned branch (GitHub-based), not a coder, with explicit no-product-test and no-implementation boundaries. Its review and verified report commit are evidence for the owner's subsequent successor authority decision. The *full independent Git receiver* is a distinct proof operation that may be included only with an explicit bounded review instruction.

## 6. Local verification and commands

- `python3 /home/jds/nvda_recovery_f02_20261111/restore_f02.py`: WSL original ZIP+baseline independent Git restore, receipt; zero product tests.
- `python3 /home/jds/nvda_recovery_f02_20261111/verify_remote_f02.py`: WSL *fresh GitHub-only* Git receiver; original 66 tips recreated from verified manifest, exact tree and fsck pass.
- `python3 /home/jds/nvda_recovery_f02_20261111/validate_t01.py`: full JSON Schema validation and leaf/proof-count/status integrity checks.
- The exact scripted local candidate, commit tree and remote commits can be independently checked with `git rev-parse`, `git diff`, `git ls-tree`, `git show-ref`, `git fsck` and `git ls-remote`.

**Evidence scope:** documents/receipts and Git checks as recorded; no SQLite dynamic loading or PostgreSQL server tests, no NVIDIA source changes, no owner acceptance.