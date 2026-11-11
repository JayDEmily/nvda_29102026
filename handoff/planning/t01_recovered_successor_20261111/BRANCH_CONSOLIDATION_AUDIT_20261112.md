# NVIDIA V2 — GitHub branch inventory and safe-consolidation decision

**Date:** 12 November 2026 (Melbourne)  
**Status:** READ-ONLY INVENTORY + NON-DESTRUCTIVE CONSOLIDATION; NO MAIN PROMOTION OR BRANCH DELETIONS  
**Repository:** `JayDEmily/nvda_29102026`  
**Scope:** Git branch administration only; not owner acceptance of successor authority, product implementation, runtime qualification or test acceptance.

## Recommended operating model

Use `main` as the published accepted baseline and **one designated active working branch** at a time. Independent reviewers may use temporary pinned branches as needed; after their results are safely admitted, close the temporary work branch. Distinguish an *active work branch* from retained historic/preservation refs. The goal is simple navigation, **not** deletion of required history or automatic promotion of a merely proposed plan.

The active working branch at this inventory is `work/t01-continuous-execution-20261112`. It includes the T01 successor proposal, the 12 November continuous-execution ADR, and the newest 11 November root `AGENTS.md` handover-runbook pointer.

GitHub official guidance: https://docs.github.com/en/get-started/using-github/github-flow and https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository. GitHub advises short-lived topic branches, review/merge into the default branch, and retiring merged/stale branches; it does **not** prescribe two total refs.

## Verified remote snapshot

- GitHub REST `GET /repos/JayDEmily/nvda_29102026/branches?per_page=100`: **26** branch refs.
- Default `main`: `7e2601a5e050d76202b1b6d3f69fc167a04c91f7`.
- One nominated active work ref: `work/t01-continuous-execution-20261112`, snapshot tip `4b92b1f5dbcd6b532ee812665a2bf71ed24e30f8` **before this inventory commit**.
- GitHub compare `main...work/t01-continuous-execution-20261112`: `status=diverged`, `ahead_by=13`, `behind_by=51`, merge-base `ae2eda56aebafa1d9c2002e4eb07dcbb9f2e08e3`. This is **not** a ready-to-merge candidate. GitHub compare file listings may be truncated; no exhaustive merged-tree/readback test was made.
- Existing `main` `EXEC_PLAN.md` Git blob `e35f11bf1fcde2be53b0c44f4818889e72509a39` is the historical 29 October 149-line documentary tranche; working-root `EXEC_PLAN.md` blob `95aa1090e02585673f81f16e9a72c150353c0120` is the recovered owner-approved **local R2** 39-leaf plan. Current successor in `handoff/planning/t01_recovered_successor_20261111/PROPOSED_EXEC_PLAN.md` is **not installed** as root.
- The 11 November documentary independent review `ACCEPT_DOCUMENTARY_PROPOSAL` is for pinned `aa8dc23608bb6d655aebd74e390a8b3d341735c7`, not for the later 12 November amended proposal or a programme admission.
- The two branches `nvda-imported-g4-20261029` and `nvda-m02-g4-imported` both point at `9bd59acba13ead7252e52e32e1b5d862adecd99a`; GitHub comparison shows each tip is a **main ancestor** (`ahead_by=0`, `behind_by=9`). They are possible future branch-name retirement candidates, not confirmed unneeded authority aliases.
- Recovery source `recovery/r2-g0-f02-20261111` and four `recovery/legacy-*` tips are needed to reconstruct the mapped historical 66 original refs; keep them. Several preservation/probe refs have **no common ancestor** with current `main`; do not delete or attempt an ordinary merge.
- No source/product tests or independent fresh recipient restore were run for this branch-administration change.

## Complete branch inventory at snapshot

| Branch | Exact tip SHA-1 | Organisational role (not an acceptance claim) |
|---|---|---|
| `execution/accepted-r1-20261030` | `363923d47b81fca50e64036bef3c8601501e3c16` | Earlier execution branch |
| `experiment/chatgpt-handoff-arithmetic-20261110-01` | `18090360b24fca36721cfa939d88a7cdc799b73f` | Isolated experiment / probe |
| `handover/ubuntu-investigation-adr-20261110` | `81b1ccdd801f52b6df3c3b9757d4ea98bb58cc18` | Historic or staging branch |
| `main` | `7e2601a5e050d76202b1b6d3f69fc167a04c91f7` | Default baseline |
| `maintenance/library-preservation-audit-20261111` | `2ad1c1cb4db200d1689013454cc263dbbb2e76e0` | Maintenance evidence branch |
| `nvda-imported-g4-20261029` | `9bd59acba13ead7252e52e32e1b5d862adecd99a` | Ancestor of main (retirement candidate) |
| `nvda-m02-g4-imported` | `9bd59acba13ead7252e52e32e1b5d862adecd99a` | Ancestor of main (retirement candidate) |
| `nvda-migration-staging-20261029` | `452511e4c26dd2e5d2c90d4cfb227002d1bb0f70` | Historic or staging branch |
| `nvda-preservation/kernel_aug04/heads/main` | `d24f9626a23b526384668b3cb26ee811b235eb5c` | Preservation ref |
| `nvda-preservation/kernel_aug04/remotes/origin/HEAD` | `d24f9626a23b526384668b3cb26ee811b235eb5c` | Preservation ref |
| `nvda-preservation/kernel_aug04/remotes/origin/main` | `d24f9626a23b526384668b3cb26ee811b235eb5c` | Preservation ref |
| `nvda-preservation/kernel_aug04/remotes/origin/work/vocabulary-governance-dedup-v1` | `9e1d22b627f7b94873d514616b4fce2d727ce9de` | Preservation ref |
| `nvda-preserved-akr7-probe` | `17263909abae9ca8cabb2440db282d12ff492ad6` | Isolated experiment / probe |
| `nvda-transport-probe` | `742017daf7e0a42d21114ff51a6107448973d160` | Isolated experiment / probe |
| `planning/chat-manual-r2-20261030` | `6feb50bf8a96e244cbd68eb57536f940be6335b3` | Historical/proposed planning branch |
| `planning/t01-authority-reconciliation-20261110` | `2bf81467953d0524cb4f0e3d7734282a75b73f49` | Historical/proposed planning branch |
| `planning/t01-recovered-successor-20261111` | `6b611f73c2d41b0f0ef7df85a9526156e4e10fae` | Historical/proposed planning branch |
| `planning/ubuntu-postgresql-transition-20261110` | `465de451d9c0bcd055d6385c0fc5d10cb9c49013` | Historical/proposed planning branch |
| `preservation/nvda-py313-offline-wheelhouse-20261111` | `3ad81d10f29ab8f0423c4bb4f5428f07783f8cb8` | Preservation ref |
| `recovery/legacy-d010-20261111` | `77471e5a851ec04e73c6dc63988868064de930f8` | Historic source-recovery ref |
| `recovery/legacy-d131-20261111` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | Historic source-recovery ref |
| `recovery/legacy-m00-brief2-20261111` | `0c86b187a23e750d39ce04f772f7d52c1bd578b0` | Historic source-recovery ref |
| `recovery/legacy-next20-20261111` | `8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e` | Historic source-recovery ref |
| `recovery/r2-g0-f02-20261111` | `16b7cc67f5d24336d3768e2da006819474a8c792` | Historic source-recovery ref |
| `review/t01-successor-independent-20261111` | `c7777881e28927e5e4957f8630028425d5004755` | Independent review record |
| `work/t01-continuous-execution-20261112` | `4b92b1f5dbcd6b532ee812665a2bf71ed24e30f8` | Designated active work |

## Ordered consolidation plan — remaining work

1. **Keep current working branch** for T01 planning and documentary reconciliation. Carry forward any verified minor edits from the predecessor branch; the newest runbook pointer has been copied and read back. Do not create extra planning branches merely to record owner approvals.
2. **Resolve acceptance and cross-lineage merge semantics:** inspect the exact diff between current `main` and the recovered R2 source; separate documentation to preserve from production/source updates; reconcile branch divergence, full history/required evidence refs and the governing `AGENTS.md`/`EXEC_PLAN.md` authority differences. Do not use a blind automatic merge of the entire 300+-file comparison or make a 'proposal' active simply by moving it to `main`.
3. **Promote accepted changes only:** present a reviewable main-target candidate with explicit allowed paths, exact approved authority, reviewer evidence, no weakening of tests, confirmed checkpoint/asset access and no change to D145 PAUSED. After that, integrate using an auditable non-force change and check `main` readback.
4. **Rebase or recreate the *next* working branch from the newly accepted `main`** after successful consolidation; do not force-rewrite the currently evidence-pinned working ref. Retain required historical snapshots/refs and immutable review records.
5. **Retire truly redundant topic branches only when independently proved unnecessary:** before deleting each, verify any unique tip, preservation purpose, explicit ref-name dependency, open review/PR, reproducible recovery route and readback. Keep recovery/legacy/preservation refs where their exact names or otherwise unreachable objects are required. GitHub's 'delete merged branch' recommendation is not authority to erase such evidence.
6. The intended end state is **one default accepted main + one active development branch**, with any necessary archival refs explicitly classified as *non-active* rather than mistaken for competing development fronts. No permanent special 'approval' branch is required.

## Execution boundaries this turn

**Completed:** GitHub documentation lookup, branch list and ancestry comparison, copied the latest planning-branch runbook pointer into the designated active work branch, created this inventory.  
**Not performed:** merging or writing `main`, changing default branch/rulesets, deleting refs, migrating archives, accepting a successor plan, product implementation/testing, or changing the frozen `GUARDRAILS.md`.

This inventory is a branch-management decision record, not a new ExecPlan or authority to advance NVIDIA product gates.
