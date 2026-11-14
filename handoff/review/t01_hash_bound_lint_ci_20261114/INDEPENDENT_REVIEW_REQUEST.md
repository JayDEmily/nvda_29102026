# T01 — mandatory lint policy integration candidate: independent review request

Date: 14 November 2026, Melbourne. **Status: DRAFT POLICY CANDIDATE / NOT OWNER-ACCEPTED / NOT MERGEABLE UNTIL INDEPENDENT REVIEW.**

## Pinned authority and purpose

Repository: `JayDEmily/nvda_29102026`. Candidate branch `work/t01-hash-bound-lint-ci-20261114`, derived from proof-preserving PR #12 `b67f3e92470fe4e3281546fbc6fc62e347d5f0ee`. The independent source of the proposed verifier is PR #10 original `fece3d56e1259f8b4b084451069c08851de9e0cb`; this branch cherry-picks that exact commit without changing the verifier or manifest.

The current required `.github/workflows/architecture-kernel.yml` runs whole-tree `uv run ruff check src tests tools` before the admitted Tier A promotion runner. The code and proof generation corpus has **51 historical Ruff findings** in seven SHA-bound proof-family/support files. The 51 diagnostics exist on `main` at `ded4b98e...` as part of 53 Ruff findings; the proof-preserving PR #12 fixes the two non-admitted E501 errors. An earlier attempt to reformat those seven admitted files (PR #7) invalidated their SHA-256 family/support proof admissions. Do not reseal generations or weaken proof admission to satisfy lint.

The existing `docs/architecture/TEST_AND_PROMOTION_KERNEL.md` establishes exact admission and registry-derived blocking architecture proof. It does not by itself admit a Ruff exception. Frozen `GUARDRAILS.md` bars altering validators merely to manufacture green; this candidate is a **proposed change to lint policy** with a stronger provenance constraint than a broad ignore, and therefore requires independent review and explicit programme acceptance before merge.

## Exact candidate diff

1. Carry forward from PR #10 `tools/proposed_admitted_ruff_baseline.py`, `config/lint/PROPOSED_SHA_BOUND_RUFF_BASELINE.json`, and the original proposal explanation. The unchanged verifier calls the **same complete Ruff 0.15.11 traversal** and requires exactly the reviewed historical 51 diagnostic identities and locations; it checks all seven source-file SHA-256 values, selected admission pointer/generation SHA, claim identity and family/support row; a new/changed finding fails.
2. Change **one step** in `.github/workflows/architecture-kernel.yml` from `uv run ruff check src tests tools` to `uv run python tools/proposed_admitted_ruff_baseline.py`, with conspicuous PROPOSAL ONLY / NOT AUTHORISED comment and step label. Do not change checkout history (still depth 0), uv version (0.10.0), locked install, architecture promotion command, or Git diff check.
3. The separate non-promoting PR #13 diagnostic workflow **is not carried forward** to this candidate, so the intended mandatory-run validation is the only 221-case GitHub architecture suite triggered by the new PR.
4. Preserve all product source/test/proof bytes, history, accepted module/implementation authority, frozen roots and offline wheelhouse/lockfile. Never claim a test-green workflow authorises itself as programme law.

## Already obtained independent GitHub Actions diagnostic evidence

- Source: [PR #13](https://github.com/JayDEmily/nvda_29102026/pull/13), exact test candidate `c98e0801c5db9cdfa51b93b4b2f92521dca1bb39`.
- [Experimental non-promoting job 43550877449 / 132312782937](https://github.com/JayDEmily/nvda_29102026/actions/runs/43550877449/job/132312782937): **SUCCESS** for complete-history checkout, Python 3.13.5 locked installation, proposed exact SHA-bound lint, unchanged `tools/run_promotion_gate.py --set architecture_kernel`, and Git diff check. Pytest **221 passed in 1717.00 seconds** (28m36s); 11 Tier A architecture/bootstrap family paths selected, 0 dependency/public-seam violations.
- [Original mandatory CI on same head, 43550877422 / 132312782794](https://github.com/JayDEmily/nvda_29102026/actions/runs/43550877422/job/132312782794): **FAIL** at unmodified whole-tree Ruff, exact 51 historical diagnostics; downstream architecture skipped. This is not evidence of an architecture failure.
- Independently exercised the proposed verifier's real CLI on a disposable PR #10 + PR #12 composition: original 51 exact digest PASSED; changed admitted file, changed current-generation pointer, changed baseline manifest and new F821 error in clean `src` each REJECTED; exact original restored and `git status` clean. Raw log SHA-256 `77a289b4f48630e9448030819e3de5eda67ce04c8d9956d3df9595223f434b6a`.
- Verified all fourteen product, proof, source, runtime and governing Git object identities matched between PR #12 and diagnostic head; no product proof files or accepted hash records changed.

## Required review and acceptance

1. Independently inspect exact candidate base/head and every diff; establish whether the fixed 51-diagnostic baseline is a defensible *revised lint acceptance contract* rather than an inadmissible waiver.
2. Independently verify exact current proof generations and byte identities and adverse behaviour of the verifier (including new clean-source diagnostics and tampered proof admissions).
3. Verify the **new mandatory workflow** really executes the same checked lint traversal through the verifier and the unchanged full Tier A promotion set; observe its own GitHub Actions result before claiming technical CI completion.
4. Return `ACCEPT_POLICY_CANDIDATE`, `RETURN`, `PARTIAL`, or `BLOCKED` with exact evidence. A candidate GREEN does not self-authorise adoption of a new acceptance criterion. Record owner policy decision explicitly before merging this change into `main`.
5. Reconcile earlier accepted documentary PR #3 and exact main integration separately. D145 remains paused; no product proof execution, generation re-admission, successor ExecPlan activation or guardrail mutation is commissioned by this lint repair.

This is a worker-authored design/submission, **not an independent reviewer verdict**, not product acceptance, and not programme authority to merge.
