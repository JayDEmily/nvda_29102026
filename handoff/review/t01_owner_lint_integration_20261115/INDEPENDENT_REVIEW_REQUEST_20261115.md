# Independent review request — T01 owner-adopted SHA-bound Ruff integration

**Date:** 15 November 2026. **Reviewer role:** independent ChatGPT reviewer/tester conversation, not the worker who prepared this integration. **Repository:** `JayDEmily/nvda_29102026`.

## Immutable review entrypoints

- **Base main:** `a73349834fe4aa1422c194da0492315044b32b98`.
- **PR #14 independently reviewed predecessor:** `831471d69afd092779a6810ee570285182be88a8`.
- **Ordinary two-parent main-derived merge:** `35f01b0dbcd4fdd5703b00afa582bac134f78985`, preserving the owner first-line root AGENTS instruction.
- **Integration-policy and governance-proposal implementation commit:** `c8d4346a9f56a1e38aa3bc48e4f4e891ceb2551d`.
- **Reviewer must verify the *actual final published PR head* independently**, and its ancestry containing these exact commits, before reviewing or asserting acceptance. The extra handover/negative-test receipt commit does not change the implementation proposition.
- **Original policy reviewer:** branch `review/t01-historical-lint-cumulative-20261115`, tip `41558c469e2ff7b5f504b1731b1525c7922da92b`. Technical verdict: ACCEPT_POLICY_CANDIDATE; owner adoption was pending then.
- **Current owner decision:** explicit user message “I agree, proceed. I agree, proceed.” immediately following a precise recommendation adopting the 51-diagnostic SHA-bound Ruff criterion and commissioning an independently reviewed main-derived candidate, **not yet an approval for main merge**.

## Reviewer must check the complete integration, not just policy diff

1. Read current `GUARDRAILS.md` in full, main AGENTS, scoped test override and current root ExecPlan; verify no governing-root or proof-admission file changed relative to main.
2. Compare entire candidate endpoint to main, classify **all** changed technical, wheel, fixture, policy, review and documentary paths; follow the reviewed 23-path historical PR #14 ancestry. Check no “DO_NOT_CARRY_FORWARD” classification is converted into actual history deletion.
3. Inspect actual new `tools/sha_bound_ruff_gate.py`, manifest SHA and `OWNER_ADOPTED_PENDING_MAIN_INTEGRATION` status. Require Ruff 0.15.11, exactly 51 canonical findings and unchanged seven proof file/generation/pointer hashes. Check all errors are refused rather than hidden.
4. Run `make lint` in correct pinned environment and the exact GitHub Actions lint entrypoint, prove they use the **same** verifier and get the same semantic result; verify mandatory original architecture promotion remains and the full-history Git checkout is present.
5. Inspect evidence for five specific adversarial refusals on a **disposable** exact implementation checkout. The author ran the modified independent reviewer harness preserved as `OWNER_POLICY_ADVERSARIAL_TEST.py` and recorded `OWNER_POLICY_ADVERSARIAL_RESULT.json`. Independently reproduce at least one negative from a fresh unrelated temporary worktree, never the live candidate or admitted proof records.
6. Independently assess the four newly vendored wheel archives, locked install, exact Python3.13.5 target, changed architecture fixture semantics and the two original AST-equivalent formatting changes (original 23-path PR #14 historical scope); distinguish archived 221/221 CI on old PR #14 from **fresh Actions on final current candidate**. Report absent or failed final CI honestly.
7. Inspect proposed `handoff/planning/t01_owner_lint_integration_20261115` texts and independently verify: original PR #3 source copy hashes, newer owner AGENTS first line, all **39** leaves, **35** original obligations, **34** still scheduled at L32, D145 explicitly blocked at L31, no new admitted physical cases, no active plan/override/ledger replacement.
8. Assess prospective dependency-window mapping (11 G1 / 12 G2 / 4 G3 / 7 G4; D145 paused) critically for real source-dependent and parent-dependent proof ordering. This window mapping is **NOT YET ADOPTED** and is not release authority; return concerns/proposed changes as documentary findings, without running product proof.
9. Verify current main and PR #14 remain unchanged and draft PR #3 is not installed. Full provenance, original Git history and independent Tester authority are mandatory; no D145 activation.
10. Return a scope-specific `ACCEPT_INTEGRATION_CANDIDATE`, `RETURN`, `PARTIAL` or `BLOCKED` with exact Git SHA, source lines, test record and remaining owner decisions. Any semantic finding must identify the primary requirement and exact mismatch; do not infer a product defect merely from lint exceptions.

## Strict exclusions

No main merge, no proof-source formatting, no proof-generation admission/seal, no live model/API job, no product-case execution, no SQLite/PostgreSQL installation or runtime compatibility claim, no external/irreversible operation, no D145 reactivation. The independent reviewer may create a **review report** on a separate review branch but not make implementation changes in this review.

**Required owner decision after independent review:** explicit approval of the *exact final integration candidate* for main, and separate adoption of any T01 root-governance programme change. Owner's policy choice in this chat already covers the narrow lint criterion, not these later gates.
