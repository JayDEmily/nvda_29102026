# T00 — Independent bounded F02 re-review and Git restoration

**Review date:** 10 November 2026, Australia/Melbourne  
**Reviewer role:** independent documentary and Git-integrity assessor; not the F02 Worker, not the L32 product Tester.  
**Candidate:** `16b7cc67f5d24336d3768e2da006819474a8c792` (tree `2b2bd7c1b7342f22909339a99150e2a395039e06`).  
**Previous candidate:** `9a4f1e827accdd7cfe3d7a14d5575573589b1acd`.  
**Authority:** frozen `GUARDRAILS.md`; this candidate's complete `AGENTS.md`, `tests/AGENTS.override.md` and 463-line `EXEC_PLAN.md`; original 31 October independent F01/F02 findings and exact corrected Git bytes.  
**Result:** **`ACCEPT_DOCUMENTARY_F02` and `PASS_GIT_CHECKPOINT` for this exact candidate.** Historic R2 G0/L00 documentary/checkpoint corrections have no remaining demonstrated F01/F02 discrepancy. **Neither active successor release nor independent SQLite engine execution nor G1–G5 product acceptance is granted by this review.**

## 1. Exact inputs and inspection scope

New user-uploaded handover:
- `NVDA_R2_G0_L00_F02_INDEPENDENT_REVIEW_HANDOFF_20261031(1).zip`
- Size **1,034,400** bytes; SHA-256 **`987aef326d301775e313cdc32556924bef52c446e68ac4ff1c18508aae43767a`**.
- All **13** ZIP members are unique, path-safe regular files; `ZipFile.testzip()` reports none damaged.
- Contains the F02 cumulative bundle, external post-commit receipt, original 66-ref manifest, independently inspectable G0 documents and copied exact governing/config/tool bytes.
- F02 cumulative Git bundle: **1,000,499** bytes; SHA-256 **`b95f05ceba8d873603a5c79894011d2b0babbfc43df674e54175a55b0f11ad2b`**. Exact match to external receipt.
- Original fixed baseline `NVDA_DOWNSTREAM_RECONCILIATION_L00_CHECKPOINT_20261028.tar(2).gz`: **42,559,431** bytes, SHA-256 `4d02c82894513bff8d07af7a2af6a151cd3f5f14ece581ac0bf0d87ea9ed0430`. Embedded full-history bundle **42,608,833** bytes, SHA-256 `91db4a1989bff366c1f547c5776ca886c276b6b1310027ae929aa1cd1efee4b9`. Both independently rehashed and matched to receipt.

The original independent predecessor review `NVDA_R2_G0_L00_INDEPENDENT_GIT_REVIEW_20261031.md` had previously established `PASS_GIT_CHECKPOINT` at `9a4f1e82…`, `F01 CLOSED`, and `RETURN_FOR_BOUNDED_REPAIR` for F02. This review examined actual *later repair bytes*, not merely that older acceptance report. All included governing files were inspected, including the full 463-line local plan.

## 2. Independent fresh restoration and integrity

The reviewer **did not execute the Worker-supplied `VERIFY_F02_CHECKPOINT.sh`**. Instead, an independent Python/subprocess verification performed the following in a new temporary bare Git receiver, leaving the user's live Ubuntu Git checkout untouched:

1. SHA and archive-member safety validation; extraction of only the fixed full-history bundle and this exact additive bundle.
2. `git init --bare`; `git bundle verify` for the baseline; fetch the original `refs/*`; independently `git bundle verify` for the additive; fetch only its named `refs/heads/work/chat-manual-r2-approved` candidate ref; set receiver HEAD.
3. `git rev-parse HEAD`, `HEAD^{tree}`, `HEAD^`, `git merge-base --is-ancestor` for the historical fixed base `97f944d51ab9e403250fe76910e2754b50425c73`, synthetic GitHub R2 snapshot `4559694b0c5bd53e98cd88936b80091adbc3b275`, and the exact previous F02 candidate `9a4f1e82…`.
4. Independently re-resolve every named original ref against `ORIGINAL_BASELINE_REFS.json`; compare the complete `git ls-tree -r --full-tree HEAD` inventory count and its exact SHA-256; compare the last-commit changed paths with the receipt; compare eight unchanged governing/source/ledger blob identities both to the parent and receipt; compare all ten supplied tracked-file copies byte-for-byte with Git blobs.
5. `git fsck --full --no-reflogs` — exit **0**, no issues reported.

| Invariant | Independently observed |
|---|---|
| Base/additive `git bundle verify` | Both exit 0 |
| HEAD | `16b7cc67f5d24336d3768e2da006819474a8c792` — exact |
| HEAD tree | `2b2bd7c1b7342f22909339a99150e2a395039e06` — exact |
| Direct parent | `9a4f1e827accdd7cfe3d7a14d5575573589b1acd` — exact |
| Historical base / snapshot / predecessor ancestry | All verified ancestors |
| Historical refs | **66/66** original names and tips exact |
| Total restored ref names | **67** |
| Tracked inventory | **4,024**, SHA-256 `6e24293d7908a3bce9e950bfd16cfa967c06c907a4f72bf54b8de0172dbdd432` — exact |
| Final commit diff | **Exactly two documentary paths** |
| Unchanged `GUARDRAILS.md`, `AGENTS.md`, `tests/AGENTS.override.md`, `EXEC_PLAN.md`, `pyproject.toml`, `tools/check_sqlite_runtime.py`, `EXECUTION_REGISTER.json`, `TEST_EVIDENCE_LEDGER.json` | Exact SHA-256/parent Git-blobs unchanged |
| Proof ledger | **35 obligations**, **0** newly recorded product test runs; exact blob preserved |
| Git object integrity | `git fsck --full --no-reflogs` exit 0 |

## 3. F02 semantic analysis: direct predecessor-to-repair diff

**Original demonstrated mismatch:** predecessor `9a4f1e82…` claimed a tracked `tools/with_pinned_sqlite.sh` launcher in the G0 independent-review request and runtime decision. The actual predecessor repository did not contain that path. Original reviewer expressly offered either a real committed helper or a corrected description of the actual reproducible invocation. This was a documentary reproducibility discrepancy, **not** a demonstrated SQLite or NVDA product-code defect.

**Observed repaired candidate:** `git diff-tree --no-commit-id --name-only -r HEAD` returns **only**
- `handoff/m02_completion_28_execution/L00/R2_G0_SQLITE_INDEPENDENT_REVIEW_REQUEST.md`
- `handoff/m02_completion_28_execution/L00/R2_SQLITE_RUNTIME_DECISION.md`

Both files now explicitly label the old tracked-helper statement inaccurate and identify the existing `tools/check_sqlite_runtime.py` as the only tracked preflight. The new exact documented shell invocation is:

```bash
export NVDA_SQLITE_LIBDIR=/absolute/path/to/sqlite-3.54.1/lib
test -f "$NVDA_SQLITE_LIBDIR/libsqlite3.so.0"
LD_LIBRARY_PATH="$NVDA_SQLITE_LIBDIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" python tools/check_sqlite_runtime.py
```

The old `tools/with_pinned_sqlite.sh` string **still occurs solely as a historical error disclosure**, not as an executable dependency. The initial audit heuristic that rejected any mention of the helper was too broad; inspection of the actual diff corrected that heuristic. No original test or production file was changed or weakened, and the alleged helper remains absent in the actual repaired Git tree as expected.

The direct shell command is a valid *conditional* executable specification for a selected CPython 3.13.5 and an existing verified `libsqlite3.so.0` directory. Its output checks the exact Python and SQLite pins in `pyproject.toml`; the preflight script itself reports source ID and exits nonzero for a version mismatch. An actual host must separately satisfy Python selection and dynamic-link loading. There is no unsupported claim that the command can run on a new host **without** the external binary.

## 4. Non-Git SQLite runtime evidence: accepted provenance, not independent execution

The unchanged **committed** `R2_SQLITE_3541_RUNTIME_VERIFIED.json` was examined inside the newly restored Git candidate. It identifies the full `gcc -O0 -g0 -fPIC -shared -Wl,-soname,libsqlite3.so.0 … sqlite3.c …` build, source SHA-256, official source SHA3-256, version, official source ID, nine feature-probe outcomes and binary SHA-256 `c53706980906943301153b630aeddba1b4aab6fe5eeda5752d8293952707db4e`. Those fields match the separately supplied new external receipt, including `python_actual=3.13.5`, `sqlite_actual=3.54.1`, source ID `2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76`, and Worker-reported preflight exit **0**.

**Not independently executed in this review:** rebuilding SQLite, loading that exact `libsqlite3.so.0`, running `tools/check_sqlite_runtime.py` on a real CPython 3.13.5/SQLite 3.54.1 host, or rerunning any of the nine non-product storage probes. The shared library/source archive is intentionally non-Git and not in the uploaded ZIP. Receipt/manifest agreement is **independent documentary consistency**, not physical reproduction of the runtime. This boundary is explicit rather than manufactured as a new F02 defect.

## 5. Disposition, programme boundaries and next stage

- **F01:** retain prior independent `CLOSED/ACCEPT_DOCUMENTARY`; the original historical object `f9a6de…` and unavailable intervening original GitHub commit chain remain honestly unclaimed.
- **F02 on repaired commit `16b7cc67…`: `ACCEPT_DOCUMENTARY_F02`.** The exact false tracked-helper assertion is corrected through the permitted direct-invocation method; both changed paths and the unchanged legitimate preflight mechanism are independently checked.
- **Git transfer for repaired commit: `PASS_GIT_CHECKPOINT`** (new independent fresh restore for this exact SHA).
- **Historical local R2/G0/L00 documentary correction set:** F01 and F02 documentary mismatches resolved with independent review evidence; no further **demonstrated** documentary discrepancy in the reviewed scope. Do **not** mislabel this as an independently executed SQLite qualification or an active-root ExecPlan acceptance.
- **Full current Ubuntu G0 readiness:** remains dependent on reconciled owner-approved root authority and exact runtime/asset verification on the *new* Ubuntu host (proposed T01/T03). The original library pathname `/mnt/data/nvda_f02_work/…` was Worker-local, not an existing Ubuntu path.
- **Programme/implementation state:** 39 leaves, 35 proof obligations, 27 new mandatory D identities, D145 PAUSED; zero new product runs/cases; no implementation, PostgreSQL migration, M02 acceptance or L32 execution justified by this review.
- **T00 raw-byte recovery:** no longer blocked for this F02 repaired candidate. Proceed to T01 **documentary authority reconciliation**, not G1–G4 product work. The proposed ADR/ExecPlan remain planning-only and do not override the accepted root.

Independent verification artefact: `NVDA_F02_INDEPENDENT_REVIEW_EVIDENCE_20261110.json`, produced in the assessor container, SHA-256 **`176b690d20757bbfb6686e521c3cf324443880e63e5b3c2cad4aa62255faa567`**. It includes literal source/archive hashes, Git refs/tips, check results and the exact two-file Git diff. No test runner, application code or external mutable database was executed.

**Final scoped verdict:** `ACCEPT_DOCUMENTARY_F02 / PASS_GIT_CHECKPOINT_16b7cc67 / NO_INDEPENDENT_SQLITE_RUNTIME_EXECUTION / NO_PRODUCT_TEST_ACCEPTANCE`.
