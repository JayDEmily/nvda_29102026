# Restart construction ExecPlan

**Authority:** user-accepted Step 5 + Step 6 implementation brief. This file operationalises that authority only.

## Immutable build inputs

- forensic archive SHA-256: `18ec9e5bdce4d1ec53ca8a8a1071c968be6d7876af4982b3da2a4f952d9538d8`
- semantic/kernel source commit: `c0bfa6d`
- runtime-reference commit: `79cbbb9db4427ff574ffc87dab45036496d99e21`
- Step-5 decision SHA-256: `8eedd78cf1d488ae0dac1842ca119e080b009ae17de9efd56672f67930abf354`
- Step-6 port manifest SHA-256: `3acfe267c2697eef2100fb844bcc1b7b15f5d7339c44edaf75d8cf4a9b483bcd`
- root baseline commit: `e137677e8c0f116ba21dadc2e951281820e09916`
- root baseline tree: `4f625f20f8882f3cdb249ac2b38046e28200d769`

## Units

1. **COMPLETED** — byte-preserved architecture/source baseline. Commit `e137677e8c0f116ba21dadc2e951281820e09916`.
2. **COMPLETED** — restart governance, instructions, role definitions, provenance.
3. **COMPLETED** — minimal Gate 0 authority + adversarial tests only.
4. **COMPLETED** — minimal Gate 0 implementation. Commit `79e3171242b15f3fdecb622d538ef1fc563cd0f4`.
5. **COMPLETED** — thin Gate-1+ semantic admission substrate.
6. **REJECTED_REPAIRABLE** — fresh independent Step-7 audit at candidate `db9a2f11d984d44bc16d1565a680a62fd1555d9a`; report SHA-256 `47c3af43acc3b18eb45abafd333175f2de62ca39db2f8cad31e2f17a6c2f6024`.
7. **COMPLETED** — bounded Step-7 audit repair, one acceptance unit at a time:
   - 7.1 **COMPLETED** — mandatory Git candidate binding composed into canonical semantic admission/state advance; commit `576e62d4e6032c333212a8bfe3bcdd7cbb27e6fc`;
   - 7.2 **COMPLETED** — exact work-order delegation required and scope/hash bound; commit `120ac59fe21a8b568bfbc50535d70292ab049b4e`;
   - 7.3 **COMPLETED** — accepted semantic index bound to real admission, exact candidate bytes, and source-authority hashes; commit `52064af1b087f8de059901cf4c3f4936d6aaa657`;
   - 7.4 **COMPLETED** — worker/reviewer provenance bound to protected Codex lifecycle receipts; commit `114c7790362af7751e2f6dfbc3f37f21b7a3e6dc`;
   - 7.5 **COMPLETED** — Gate-0 hooks aligned to supported event-specific deny/stop semantics, bounded spawn/wait orchestration, and fail-closed observable-tool policy; commit `ffbf349b6e7429499ffdfb9c27647aac87935d11`;
   - 7.6 **COMPLETED** — root `AGENTS.md` and programme `PLANS.md` are explicitly frozen and ordinary work-order mutation is mechanically rejected; commit `a60c4a239829ba9cc12b8b5ca3ba65a6db70d1fa`.
   - 7.7 **COMPLETED** — same-controller pre-audit found that F-05 runtime/tool-policy checks existed in tests but were not composed into Gate-0 static validation; the static validator now enforces the manifest/config/hook tool-surface policy; commit `3181e582163a036e4acfdfb5bf0349a27fd590aa`.
   - 7.8 **COMPLETED_PENDING_FINAL_VALIDATION** — caller-supplied admission/state maps were removed from the public state-advance seam. Work-order delegation now avoids Git self-reference by binding the complete material execution scope while Git containment binds the execution base; authority/delegation/state are loaded from immutable Git records. Commit `edd7e5d`.
   - 7.9 **COMPLETED_PENDING_FINAL_VALIDATION** — accepted semantic-index admission is bound to the raw candidate Git blob, active admitted bytes, and source-authority hashes; commit `7dcbf64`. Its public scheduling seam must also consume Git-rooted admission records as part of 7.8.
   - 7.10 **COMPLETED_PENDING_FINAL_VALIDATION** — `wait_agent` is limited to the documented temporal boundary while the one authorised child is in progress; no undocumented target-input binding is claimed; commit `be32caa`.
   - 7.11 **COMPLETED_PENDING_FINAL_VALIDATION** — Gate-0 `admit` remains the explicit admission action; a separate ordinary-WSL `commit-admission` action now revalidates sealed evidence, permits only the admission record + `ADMITTED_STATE.json`, creates and re-verifies one admission-control Git commit, and requires a clean worktree. Commit `b6486f1`.
8. **ACTIVE** — rerun full deterministic validation, provenance reconciliation, direct exact-port source-object re-verification, and same-controller pre-audit after 7.8–7.11. Same-controller review remains supporting evidence only and cannot admit the candidate.
9. **PENDING** — fresh independent re-audit of the repaired candidate. No `main` promotion, live Gate 0, or final preservation tarball is authorised unless that re-audit returns `ACCEPT_FOR_MAIN_PROMOTION_AND_STATIC_GATE0_PREPARATION`.

## Stop conditions

Stop at the first Step-6 authority conflict, exact-port/hash failure, unsupported OpenAI product assumption, new programme/domain decision, requirement for broader protected mutation, R2A dependency, speculative test proposition, or inability to keep Gate 0 independent from Gate 1+ machinery.

## Validation record

Update only with observed command results. Passing checks are bounded evidence, not semantic acceptance.
