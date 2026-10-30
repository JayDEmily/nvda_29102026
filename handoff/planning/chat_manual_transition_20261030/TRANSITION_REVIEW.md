# R2 CHAT_MANUAL transition — documentary proposal and review manifest

**Status:** PROPOSED_NOT_ACTIVE, not independent programme acceptance or product execution.
**Source execution branch:** `execution/accepted-r1-20261030`, exact starting commit `363923d47b81fca50e64036bef3c8601501e3c16`. The original `main` at intake was `8ff7d82377e9bf8f9fc75c1ecef70f0ab29a2ada`. The new `planning/chat-manual-r2-20261030` branch preserves source Git ancestry and must not be conflated with an accepted active successor.
**Method:** NVDA Planning_V1 `AMEND` + `GOVERNANCE_PROPOSAL`; not implementation.
**Files read in full:** live root `GUARDRAILS.md` (Git blob 54a4407609941f63f6b902076688ff102a3d5ba2), root `AGENTS.md` (fd471d4502368f4e530be9b8c1c76051883e8ad7), test `AGENTS.override.md` (280b50c5c028b2460b7e5c8920259dfaba5cb180), root `EXEC_PLAN.md` (f6e96651fb958933a3b2c2b49164530c780bbdfe), and plugin `PLANNING_STANDARD.md`, `WORKFLOWS.md`, approved `AGENTS_APPROVED.md`, `INTEGRITY_MANIFEST.json`, template and JSON schema. The original execution and test ledgers were fetched from the precise branch. No product code, contracts, test suites or external provider data were tested or reviewed for new semantic acceptance.

## A. Exact AGENTS governance proposal

The live 12,268-byte repository AGENTS at the source commit contains historical task-bound instructions and pins old delegated execution. The plugin reference is the owner's earlier approved 112-word draft (full-file SHA-256 `7ad648aad7a8d856cbb1891bba585eaa60b6f2ed8cd9e0273739987fa49a9bc6`). The proposed root AGENTS on this review branch is the **entire 112-word text** of that reference, changing only this independent-testing line:

```diff
-Spawn an independent worker for testing as required.
+Use independent testing arrangements specified in the `EXEC_PLAN.md`.
```

This **changes the approved reference bytes**, so it is a proposal requiring explicit exact-text owner approval before becoming active. The unchanged plugin reference remains authoritative evidence of what had already been approved; a reference hash never proves installation. Frozen GUARDRAILS remains unmodified.

## B. EXEC_PLAN amendment, scope, tests and dependency law

Retained exactly: 39 leaf identities (including L01a–d, L07a–b, L10a–c), original G0–G5 boundaries, named core20, seven further mandatory identities, 28 held dispositions, seven external holds, all prior accepted proof and review evidence, and D145 PAUSED with zero executable allocation. Both stock and selected options remain compulsory for D141/D142/D144. The proposal changes **when** independent product testing occurs, never **what** must be proved.

- Mode changes from delegated to `CHAT_MANUAL`: one implementation chat; a different manually managed Tester chat is the sole strict product executor at L32. Separate tester/persona and independent availability must be established before any proof. No assumption that this chat can spawn agents.
- Each owner leaf still resolves source/definition/policy first, authors finite exact allocated tests and independent oracles before implementation, commits scoped work and records `IMPLEMENTED_UNTESTED`. Documentary review may release source contracts, not product acceptances.
- A provisionally implemented parent can support child *implementation* only if the contractual interface and source/authority binding are stable and documented. No parent releases a child's `TESTED_ACCEPTED` or gate acceptance without actual parent proof. L32 final Tester executes and accepts in dependency order; first encountered invariant failure returns work to Worker and stops its descendants.
- The L32 existing final gate/leaf absorbs independent final testing before census and close-out, retaining the 39-leaf count. Later discovery of upstream defects is an acknowledged schedule trade-off; no blanket regression and no source/meaning shortcut.
- Existing 60 prospective signal physical cases plus up to 14 supporting cases remain prospective and their exact case IDs/budgets are not silently altered. Seven supporting history/option profiles count as zero new D identities. Unaffected accepted proof evidence is reused; new/invalidated proofs have exact independent execution and reached refusal obligations.
- The original execution `TEST_EVIDENCE_LEDGER.json` has 35 obligations, no new product runs and original delegated reviewer/schedule. The **separate** proposed ledger in this folder schedules 34 nonpaused obligations at L32 and leaves D145 on its paused L31. It retains every original evidence ref, contract placeholder, zero released case allocation and semantic state. The live ledger is untouched.

## C. Python 3.13.5 environmental transition

Owner-selected CPython 3.13.5 is the proposed target; observed chat interpreter is `/opt/pyvenv/bin/python` CPython 3.13.5, SQLite 3.46.1. Source `pyproject.toml` and `.python-version` still pin 3.12.14; Ruff targets py312 and mypy targets 3.12. The old `vendor/wheels` includes cp312-specific binaries. These are exact configuration mismatches, not proof the implementation is incompatible.

A project attachment `NVDA_PY313_OFFLINE_WHEELHOUSE_COMPLETE_20261023(1).zip` is available (29,555,356 bytes), with 16 wheels including cp313 PyYAML 6.0.3 and mypy 1.20.1, pytest 9.0.3 and Ruff 0.15.11. This assessor inspected archive listing/README/manifest and **recomputed all 16 SHA-256 values successfully**; ZIP CRC check found no corrupt member. This is wheel-byte integrity, **not** dependency installation, interpreter ABI execution, product test, SQLite parity or normative admission. Proposed configuration changes (after separate approved environment preparation): `requires-python = "==3.13.5"`, `.python-version = 3.13.5`, Ruff py313, mypy 3.13; reconcile `tool.uv.find-links` with the externally accessible 3.13 wheelhouse without uploading unnecessary binaries. Document the SQLite capabilities required by individual approved claims and test only affected propositions. No Python source/configuration file was changed by this proposal.

## D. Handover, L00 and the 124.58 MB package

Earlier accepted R1 section 5 requires a full historical base or cumulative additive Git bundle, fresh recipient restoration, SHA-256, ref/tip/tree/blob comparison and `git fsck --full`. Retain original baseline `97f944d51ab9e403250fe76910e2754b50425c73`, original 66 historical ref tips and all evidence. The release `nvda-l00-transfer-successor-40960483921` contains a producer-published 124,580,793-byte handover targeting `363923d4`. Its publication and Actions success do **not** establish independent L00 acceptance.

User rejects the redundant 124.58 MB manual transfer. Proposed alternative is `PINNED_REMOTE_CHECKPOINT` with exact GitHub commit and *all required remote refs*, reviewed non-Git asset manifest and independent fresh recipient clone/fetch/fsck/ref/tree/blob validation. This is **not yet verified end-to-end**: this container's `git ls-remote` failed DNS resolution (`Could not resolve host: github.com`), while the connected GitHub API can retrieve individual text files and commits, which does not establish Git object-closure restoration. If unavailable, use owner-approved full-history or smaller base-relative bundle with verified shared baseline; do not downgrade checkpoint integrity. Until owner approval of a demonstrated alternative, R1 checkpoint contract still applies and L00 remains not independently released.

## E. Activation and evidence gates

1. Obtain exact-text approval for the new AGENTS full replacement, test-local override, and R2 ExecPlan; the original approved 112-word plugin reference is not silently changed.
2. Conduct an independent bounded documentary review of scope, mode, source authority and concrete dependency/acceptance changes, plus readback of any later Codex commits not present at the starting Git SHA.
3. Validate the proposed ledger against the plugin schema, reconcile execution register without inventing completion, and designate an actually separate independent Tester chat.
4. Prove Python 3.13.5 packaging/SQLite mechanism and fresh historical Git receiver transfer, or preserve affected `BLOCKED` statuses.
5. Only then explicitly activate R2 on the agreed execution branch with a verified immutable commit/checkpoint. Do not begin implementation or product testing solely because this draft branch exists.

## F. Evidence and status matrix

| Deliverable | Proposed file/evidence | State |
|---|---|---|
| Frozen governance | Root `GUARDRAILS.md` unchanged on R1 | VERIFIED exact blob |
| Stable AGENTS amendment | Proposed root `AGENTS.md`, single mode-neutral change to earlier approved reference | PROPOSED / awaiting exact-text approval |
| Test-local override | Proposed `tests/AGENTS.override.md` | PROPOSED |
| Full M02 plan | Proposed `EXEC_PLAN.md` R2; same 39 leaf identities | PROPOSED / no independent reviewer |
| Historical and proposed test ledger | Original active ledger retained; `TEST_EVIDENCE_LEDGER_PROPOSED.json` created in this folder | PROPOSED / 0 runs |
| CPython 3.13.5 | Interpreter observed; 16 wheel ZIP hashes checked; old config not changed | PARTIAL VERIFIED / runtime admission UNKNOWN |
| L00 independent recipient restoration | Producer release published; fresh recipient restoration not established | BLOCKED_TRANSFER |
| Product implementation and independent proof | None executed in this amendment | NOT ATTEMPTED |

Original R1 Git history, test failures, proofs, claim/source authority, unresolved policy decisions, and paused D145 must be preserved. This branch contains governance **proposals**, not accepted programme state.
