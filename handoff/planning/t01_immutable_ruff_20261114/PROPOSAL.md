# PROPOSAL ONLY — SHA-bound historical Ruff baseline for immutable proof files

Date: 14 November 2026 (Melbourne). Status: **UNAPPROVED TECHNICAL PROTOTYPE**. No CI policy change, workflow bypass, product test, new generation, reviewer acceptance or main integration.

## Source state and distinct acceptance boundaries

- Repository: `JayDEmily/nvda_29102026`.
- Proposed branch: `planning/t01-immutable-ruff-policy-20261114`, from exact pinned `85f8c5fc96bde8eac86326d9f7b60f47893aad73` (which contains the existing independent-review request and does not change product source/proofs).
- Current explicit owner direction: complete the Python 3.13.5/uv CI repair, preserve historical proof and independent testing, do not move to governance promotion until required validation passes.
- `GUARDRAILS.md`: tests and validation are evidence, cannot be changed merely to manufacture success; authority and proof generation history cannot be forged.
- `docs/architecture/TEST_AND_PROMOTION_KERNEL.md`: exact architecture test admission and complete registry-derived blocking aggregate remain normative. **This proposal does not modify those rules**.
- `tests/AGENTS.override.md` historical controlled-proof restrictions: preserve unchanged admitted proof bytes; independent sole strict executor for any new product proof.

## Exact observed collision

The active workflow runs `uv run ruff check src tests tools`, with pinned `ruff==0.15.11` in `pyproject.toml`. On the clean candidate, Ruff reports **51** findings: E501 ×38, I001 ×5, B905 ×4, RUF007 ×4, **all contained within seven original immutable proof files**.

All seven source SHA-256 hashes match the `family_files` or `support_files` entry in the **currently selected** generation of their claims. These seven files remained byte-identical to base `8f236660e9b5982c242b6f114882f045cd1f291e`. Earlier PR #7 changed them and broke proof admission; revert rather than reseal old generations.

Canonical diagnostic representation (for each Ruff JSON diagnostic): `path` relative to repository root, `code`, `message`, and starting `row`/`column`; sort by path, row, column, code, message; JSON dump with `sort_keys=True`, compact separators and terminal LF; SHA-256:

`08ae839b0596c31ecb73a4667845f0d19dfe0c4503c52079434dd98e835a2a8f`.

## Proposal algorithm — *not active CI law*

`tools/proposed_admitted_ruff_baseline.py` and `config/lint/PROPOSED_SHA_BOUND_RUFF_BASELINE.json` form an independently reviewable experiment. The baseline manifest is itself locked in the prototype code by exact SHA-256:

`d38367ce1f63a1731c0cd9b69e12af021a291d71b0206f83ba17f3b69dbfc97c`.

The prototype:
1. Requires Ruff **0.15.11** and performs the same `ruff check src tests tools` traversal as the unchanged workflow.
2. Verifies each of exactly seven historical file byte hashes; rejects symlinks and paths escaping the repo.
3. Verifies the selected `admission.json` pointer and SHA-256 of the selected generation record, the claim ID, the exact family/support row, and its file hash.
4. Requires **exactly 51** diagnostics, the exact per-file distribution and the precise canonical diagnostic SHA-256. Any new/removed/changed lint diagnostic, new path, changed admitted bytes, changed generation or tool version **fails closed**.
5. Prints `NOT AN ACCEPTED LINT POLICY OR CI/PROMOTION PASS`. It is not invoked from GitHub Actions and does **not** replace existing lint or product-proofs.

This approach would permit historically admitted byte-immutable files to retain their known lint debt while continuing to forbid any *new* lint finding, but changes the acceptance meaning of the CI lint stage compared with the existing all-zero requirement. It **cannot** be adopted solely because this prototype runs successfully.

## Direct prototype verification

- Isolated WSL checkout of pinned parent, Python 3.13.5 + `uv==0.10.0`, offline `uv sync --locked --extra dev --offline`: 15 resolved / 14 installed, exit 0 (prior clean-branch check).
- Ruff 0.15.11 `check tools/proposed_admitted_ruff_baseline.py`: **All checks passed!**
- `.venv/bin/python tools/proposed_admitted_ruff_baseline.py`: exit **0**, exact original 51 diagnostic digest above.
- Deliberate negative conditions, all rejected without altering repository files: (a) forged source SHA-256; (b) forged current-generation pointer; (c) forged expected diagnostic-set SHA-256; (d) injected unexpected new Ruff diagnostic for a previously clean tool path. Each raises `ValueError` with a distinct refusal cause.
- `git diff --check`: exit 0.
- There are **no** product-gate runs, no affected source/test modifications and **no** CI result on this proposed lint baseline.

## Required independent decision before any activation

An independent reviewer should compare this proposal with the current normative all-zero Ruff policy and accepted proof-admission law, and decide whether its exact-legacy baseline is an acceptable **policy change**, or whether new proof generations and strictly controlled independent product re-admission are required instead. The reviewer must test both new lint detection and unchanged hash-bound proof provenance, evaluate completeness against all original lint rules, and record precise candidate SHA and verdict.

No worker is authorised to equate a successful prototype with owner approval. **Retain the existing workflow unchanged.** Other architecture fixture/physical-inventory defects are separate and remain unresolved, so even future approval of this policy would not alone clear full CI. PR #3 and main remain unmodified; D145 remains paused.
