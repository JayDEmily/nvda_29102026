# T00 — Independently restored pre-F02 Git-review submission (10 November 2026)

**Status:** `VERIFIED_PREDECESSOR_CHECKPOINT; F02_STILL_OPEN`  
**Scope:** inspect the user's newly supplied original 31 October independent Git-review ZIP and compare it to the exact previously reviewed candidate. This is **not** a re-review or acceptance of the later F02 Worker repair at `16b7cc67…`.  
**Governing record:** [T00_F02_RECOVERY_STATUS_20261110.md](T00_F02_RECOVERY_STATUS_20261110.md) and the proposed [ExecPlan stage T00](EXEC_PLAN.md).

## Exact user-supplied byte identity

- User attachment: `NVDA_R2_G0_L00_INDEPENDENT_GIT_REVIEW_HANDOFF_20261031(2).zip`
- Original attachment SHA-256: `b7709e51422f22cf003f6d5c0a148966c9353465da06483c025d701c1a3eed74`; size: **997,870** bytes.
- This hash **exactly matches** the previously independent-reviewed submission `NVDA_R2_G0_L00_INDEPENDENT_GIT_REVIEW_HANDOFF_20261031(1).zip`, as recorded in the full original review `NVDA_R2_G0_L00_INDEPENDENT_GIT_REVIEW_20261031.md` held in the user's Project Library.
- ZIP integrity: five unique path-safe regular-file members, `ZipFile.testzip()` no failed member. The members are the cumulative additive Git bundle, external Worker receipt, original 66-ref JSON, verification shell, and restoration README.
- Embedded prior **additive bundle** SHA-256: `e2a160c8b9925458ca5046b28dd4303896ea32498a27de7468335f7513681417`, size **997,880** bytes.

The exact original baseline was already separately mounted as `NVDA_DOWNSTREAM_RECONCILIATION_L00_CHECKPOINT_20261028.tar(2).gz`, SHA-256 `4d02c82894513bff8d07af7a2af6a151cd3f5f14ece581ac0bf0d87ea9ed0430`, size **42,559,431** bytes. Its embedded `NVDA_DOWNSTREAM_RECONCILIATION_L00_CHECKPOINT_20261028_FULL_HISTORY.bundle` hashed `91db4a1989bff366c1f547c5776ca886c276b6b1310027ae929aa1cd1efee4b9`.

## Independent read-only restoration observed this turn

The reviewer inspected the archive members without running any provided shell script. The two bundles were extracted by their exact paths into an isolated temporary directory. A **new bare Git receiver** was initialised; the reviewer invoked independent subprocess commands for `git bundle verify`, `git fetch`, `git rev-parse`, `git show-ref`, `git ls-tree`, `git diff-tree`, `git cat-file`, `git merge-base --is-ancestor` and `git fsck --full --no-reflogs`. The temporary receiver was discarded after verification; no user repository was changed.

| Reproducible check | Independently observed |
|---|---|
| Both Git bundles verified | PASS, with original baseline loaded before additive |
| Restored HEAD | `9a4f1e827accdd7cfe3d7a14d5575573589b1acd` — MATCH |
| HEAD tree | `b876d8824c456988cf40398d4bf6b9298906f9d6` — MATCH |
| Direct parent | `22a2f13189fa3f1a55b2fef265f93a6696c0155f` — MATCH |
| Historical snapshot | `4559694b0c5bd53e98cd88936b80091adbc3b275` — object exists, ancestor of parent |
| Original historical refs | **66/66** tip identities match receipt |
| Total restored named refs | **67**, including new local R2 candidate branch |
| Tracked file inventory | **4,024** paths; SHA-256 `d34ddb993c1a1dd3f877fed7eb004402d25703dfbb3a2a209be2eb8077890e63` — MATCH |
| `git fsck --full --no-reflogs` | Exit 0 |
| Parent-to-HEAD diff | Seven G0 documentary/evidence paths; no product-source edit |
| Later F02 repair `16b7cc67f5d24336d3768e2da006819474a8c792` | **Not present in this restored bundle** |

## Direct reproduction of original F02 finding

In the actual restored `9a4f1e827…` Git tree:

1. `handoff/m02_completion_28_execution/L00/R2_G0_SQLITE_INDEPENDENT_REVIEW_REQUEST.md:28` states that SQLite 3.54.1 launch uses tracked `tools/with_pinned_sqlite.sh`.
2. `handoff/m02_completion_28_execution/L00/R2_SQLITE_RUNTIME_DECISION.md:7` claims that same script launched CPython 3.13.5 via `NVDA_SQLITE_LIBDIR`.
3. `git cat-file -t HEAD:tools/with_pinned_sqlite.sh` returns failure: **the claimed helper is absent from the actual Git tree**.

This independently reproduces the precise prior F02 **documented-launcher/committed-tool mismatch**. It does not establish any failure of SQLite itself or the Worker's separately built `libsqlite3.so.0`.

## Disposition and the still-missing input

- **PASS:** exact uploaded ZIP matches the prior reviewer submission, base/additive restoration, claimed predecessor commit/tree, original refs, tracked inventory and Git integrity.
- **F01:** previously independently `CLOSED` in original documentary and Git reviews; no reopening from this duplicate predecessor submission.
- **F02 on `9a4f1e827…`:** `RETURN_FOR_BOUNDED_REPAIR`; mismatch directly reproduced.
- **F02 on `16b7cc67…`:** **UNKNOWN / NOT REVIEWED**. No later repaired commit or later independent reviewer verdict is present in this ZIP, so no independent acceptance can be assigned.
- **R2/G0 downstream:** keep dependent acceptance and activation blocked while the latest repaired bytes/verdict are inaccessible. No product tests or runtime probes were executed.

**Exact missing source:** `NVDA_R2_G0_L00_F02_INDEPENDENT_REVIEW_HANDOFF_20261031.zip` (Library metadata size **1,034,400** bytes), or its original cumulative additive `NVDA_R2_G0_L00_F02_SQLITE_LAUNCH_CORRECTION_CUMULATIVE_FROM_97f944d51ab9.bundle` (metadata size **1,000,499** bytes), and any applicable independently authored post-repair review. The Library currently advertises their filenames but does not provide an authorised raw-byte materialisation path to this conversation. The newly supplied earlier handoff does **not** substitute.

**No activation or source changes:** this report is an additive planning-branch evidence record. Original root `EXEC_PLAN.md`, `AGENTS.md`, `tests/AGENTS.override.md`, `GUARDRAILS.md`, source, proof claims, historical reviews and Git refs remain unchanged.
