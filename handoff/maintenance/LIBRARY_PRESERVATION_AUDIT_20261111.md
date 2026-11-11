# NVIDIA V2 — ChatGPT Library cleanup preservation audit

**Audit date:** 11 November 2026 (Melbourne)  
**Scope:** current actionable R2/G0/F02 successor source and the specific external archives identified during T01. **Not** an exhaustive count of every historical Library, Project, Google Drive or standalone research artefact.  
**Decision:** `SAFE_TO_DELETE_VERIFIED_DUPLICATES_ONLY`; `BLANKET_LIBRARY_DELETION_NOT_CERTIFIED`.

## 1. GitHub already preserves current project work

| Required current work | Remote evidence |
| --- | --- |
| Exact independently reviewed F02 recovered source, full Git ancestry and declared 66 original ref tips | `recovery/r2-g0-f02-20261111` at `16b7cc67f5d24336d3768e2da006819474a8c792` plus four `recovery/legacy-*-20261111` branches; `ORIGINAL_66_REFS.json` in T01 proposal; planner fresh Ubuntu GitHub-only receiver and separate ChatGPT independent documentary reviewer both verified 66/66 refs, 4,024 entries, exact inventory SHA-256 and `git fsck --full --no-reflogs` |
| Full successor authority proposal (not active) | `planning/t01-recovered-successor-20261111` source commit `aa8dc23608bb6d655aebd74e390a8b3d341735c7`; subsequent handover commit `768f18672d5f8a226e806b9fff68984ae027d739`. Original F02 root `AGENTS.md`, `EXEC_PLAN.md`, `GUARDRAILS.md`, test override and original ledgers remained untouched |
| Independent T01 documentary report | `review/t01-successor-independent-20261111` at `c7777881e28927e5e4957f8630028425d5004755`, report `handoff/review/t01_successor_independent_20261111/INDEPENDENT_REVIEW.md`, verdict `ACCEPT_DOCUMENTARY_PROPOSAL` only; separate reviewer did not commission/install active root or execute product tests |
| Repeatable ChatGPT/GitHub handover mechanism | `docs/automation/CHATGPT_GITHUB_HANDOVER_UIA_20261110.md` retained in proposal tree (same Git blob as `main`); successfully demonstrated one short-prompt cross-thread task and receipt |
| **One canonical Python 3.13 wheelhouse** | `preservation/nvda-py313-offline-wheelhouse-20261111` at `3ad81d10f29ab8f0423c4bb4f5428f07783f8cb8`. Archive `artifacts/offline_runtime/NVDA_PY313_OFFLINE_WHEELHOUSE_COMPLETE_20261023.zip`; 29,555,356 bytes; SHA-256 `33bc332bae5cc10d8b9dfc5ba6a4fe4664318c0e8ead6796f44e522172d2d504`. Verified ZIP CRC and all 16 embedded SHA256SUMS wheel entries; GitHub archive **re-cloned** into a fresh Ubuntu receiver and its SHA-256 independently matched |

The `JayDEmily/nvda_29102026` GitHub repository was reported **public** by GitHub's repository metadata during this audit. Do not post any private, licensed, credential-containing or confidential historical attachments without a separate content/permission decision. The existing preservation-wheelhouse branch contains standard dependency wheels and manifest only, not user account material.

## 2. External source archives physically retained outside Library

| Archive | Observed safe locations | Independently verified bytes |
| --- | --- | --- |
| F02 exact original review handover | Windows `C:\Users\james\Downloads\NVDA_R2_G0_L00_F02_INDEPENDENT_REVIEW_HANDOFF_20261031(1)(1).zip`; recovered derived bundle and evidence on Ubuntu `/home/jds/nvda_recovery_f02_20261111/` | ZIP 1,034,400 bytes; SHA-256 `987aef326d301775e313cdc32556924bef52c446e68ac4ff1c18508aae43767a`; additive 1,000,499 bytes, SHA-256 `b95f05ceba8d873603a5c79894011d2b0babbfc43df674e54175a55b0f11ad2b` |
| 28 October original L00 full-history baseline | Windows `C:\Users\james\Downloads\NVDA_DOWNSTREAM_RECONCILIATION_L00_CHECKPOINT_20261028.tar.gz`; extracted Git bundle and evidence on Ubuntu `/home/jds/nvda_recovery_f02_20261111/` | Original TAR.GZ 42,559,431 bytes; SHA-256 `4d02c82894513bff8d07af7a2af6a151cd3f5f14ece581ac0bf0d87ea9ed0430`; full-history bundle 42,608,833 bytes, SHA-256 `91db4a1989bff366c1f547c5776ca886c276b6b1310027ae929aa1cd1efee4b9` |
| Python 3.13 canonical wheelhouse | GitHub preservation branch **plus** Windows Downloads and the separately verified Ubuntu GitHub readback under `/home/jds/nvda_py313_github_readback_20261111/` | Full archive ZIP CRC + 16 wheel digests + original and independent GitHub readback SHA-256 matched |

**Important distinction:** the original F02 ZIP and 28 October TAR.GZ are **not themselves asserted to have been uploaded to GitHub as archive files**. Their necessary Git object graph and named historical tip content are remotely preserved and independently recoverable in GitHub; their original ZIP/TAR container bytes remain locally retained on Windows and extracted on Ubuntu. They are not necessary to re-fetch the current recovered source Git tree, but original non-Git archive integrity would depend on those retained local originals. Do not confuse remote Git source preservation with a raw original-archive backup.

The 17 original recovered `vendor/wheels/` files are in Git, but several wheels carry **CPython 3.12** ABI tags. They are not a substitute for the separately preserved Python 3.13 wheelhouse. The canonical 16-wheel CPython 3.13 archive has pure `psycopg==3.3.4`, but **no `psycopg_binary`** wheel.

## 3. Limits, residual risks, and cleanup rule

**Confirmed safe within this narrow task:** a future NVDA Worker can find the recovered F02 Git source, exact T01 authority proposal, original 66-ref manifest, independent report, GitHub handover runbook and one Python 3.13 offline wheelhouse *without accessing ChatGPT Library*. A fresh actual Ubuntu GitHub remote receiver for F02 and independent binary wheelhouse GitHub readback both passed.

**Not certified:**
- Exhaustive Library/Project/Drive population or historical byte-identity inventory of all original research, forensic attachments, policy/provider documents, unique evidence and other unrecovered archives. Earlier history raised unique non-Git evidence; this targeted audit did not search or hash every attachment.
- Exact SQLite **3.54.1 shared-library binary** and the required dynamic-loading qualification on current Ubuntu. The current wheelhouse does not provide it. It may be independently obtained/built under future authorised T03; no ready-to-run proof is claimed here.
- Psycopg 3.3.4 optional **binary** wheel and PostgreSQL **18.6 server**, their version/privilege qualification, and full T04 product evidence.
- Any separate commercial/private reference document not already committed to the repository; because the GitHub repo is public, do not automatically copy such material there.
- Successful future repeated unattended Browser automation or independent L32 product test acceptance. None follows from one transport test and a documentary review.

**Concrete cleanup decision for the owner:**

1. **Library copies of the verified F02 ZIP, 28 October baseline and CPython 3.13 wheelhouse are no longer the sole known access route for current R2/T01 continuation.** Their exact source/checkpoint and Python wheelhouse needs are covered by GitHub, and the first two original archives also have verified Windows/Ubuntu-side evidence. Thus duplicate copies with independently matching hashes can be removed from Library *for the stated purpose of resuming current R2/T01 work*.
2. **Do not bulk-delete every remaining NVIDIA Library item based on this audit.** This would require a deliberately scoped review of unique non-Git research/forensic content the user may still want. For current work, retain any unique **non-Git** policy-source material or exact SQLite runtime binary until another durable accessible copy is known, or explicitly decide that its original bytes are no longer needed.
3. Avoid retaining dozens of redundant historic CPython 3.12 wheelhouse ZIPs just because they exist; versioned Git already tracks the 17 original `vendor/wheels/` and this audit additionally preserved one verified CPython 3.13 dependency archive. Which *other* Library archives are redundant is not assumed without inspecting their identities.
4. This is a **preservation/status** record. No Library item was deleted, no accepted root authority was amended, no project test was run, and no existing history was rewritten.

## 4. Evidence sources and commands

Remote transport and Git readback: GitHub `fetch_file`, `compare_commits`, `get_repo`, and WSL `git ls-remote`, independent remote bare-receiver `git fsck --full --no-reflogs`, cloned canonical wheelhouse branch and `sha256sum`. Local archive checks: PowerShell `Get-FileHash -Algorithm SHA256`; Ubuntu `zipfile.testzip()`, internal `SHA256SUMS` per-wheel checks, `sha256sum`; source `git ls-files vendor/wheels` and `pyproject.toml` / `.python-version`.

Related committed evidence: `handoff/planning/t01_recovered_successor_20261111/ORIGINAL_66_REFS.json`, `GITHUB_REMOTE_RECEIVER_RECEIPT.json`, `UBUNTU_F02_RESTORATION_RECEIPT.json` and the exact independent review named above.

**Final classification:** `CURRENT_R2_SOURCE_AND_CANONICAL_PY313_WHEELHOUSE_GITHUB_PRESERVED` / `WHOLE_LIBRARY_NOT_EXHAUSTIVELY_PRESERVED`.
