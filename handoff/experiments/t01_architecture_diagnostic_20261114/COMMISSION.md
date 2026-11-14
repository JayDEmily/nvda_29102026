# T01 diagnostic CI commissioning — not an acceptance policy

Date: 14 November 2026 (Australia/Melbourne).

## Exact scope and lineage

Repository: `JayDEmily/nvda_29102026`. Experimental branch `experiment/t01-architecture-diagnostic-20261114`, base local composition `c8a776e7f33e4051935985a10b59d40fd3b5a34c`.

That base was produced by cherry-picking the unchanged proposal-only PR #10 verifier and manifest on top of the proof-preserving PR #12 (`b67f3e92470fe4e3281546fbc6fc62e347d5f0ee`). The base preserves the 51 Ruff diagnostics exactly and passes direct entrypoint refusal probes for changed source, pointer, manifest and a new F821 diagnostic.

## Experiment

Add **one** standalone `.github/workflows/t01-experimental-architecture-diagnostic.yml`. Do **not** modify `.github/workflows/architecture-kernel.yml`, existing `ruff check src tests tools`, `pyproject.toml`, any product test/proof/generation, governance file, or previous independent-review branch.

The experiment runs full-history checkout, pinned uv 0.10.0 with the offline CPython 3.13.5 locked installation, the **unapproved** SHA-bound historical Ruff baseline proposal, then the exact existing `tools/run_promotion_gate.py --set architecture_kernel` Tier A architecture/bootstrap aggregate and `git diff --check`.

**Why this is not a bypass:** It is a separate labelled non-promoting diagnostic run so that the architecture path can be observed without falsely marking the repository's still-failing original Ruff policy green. The original, mandatory `architecture-kernel` job remains unchanged and red at 51 legacy findings until a proper policy decision. This diagnostic is neither an admitted replacement for that job nor proof of semantic acceptance.

The active `config/proof/promotion_sets.yaml` and `test_families.yaml` resolve `architecture_kernel` to Tier A architecture/bootstrap families only, **not** controlled product proof families. Historical generation files and test source remain immutable.

## Prior exact evidence

- Main `ded4b98e1e5999d1ddf2f067e660b691917bcd71`: 53 Ruff findings.
- PR #12 `b67f3e92470fe4e3281546fbc6fc62e347d5f0ee`: 51, all identical historical findings, zero new.
- PR #12 affected historical/current fixture controls: 61/61 pass under disk-backed WSL `--basetemp`, raw log SHA-256 `f7450d86589502f4fa7f438d96d90ba6ad046591e23c7d27c8069e21fbb530d3`.
- Local proposal-on-PR12 Ruff verifier: exact 51 accepted as **proposed-only** matching legacy diagnoses, rejected four temporary negative mutations and restored Git-clean state.

## Stop and reporting law

On any diagnostic failure, preserve the first failed stage and classify it against current tests, actual authority and code; do **not** automatically repair unrelated later checks or reseal proof records. Do not claim the original required CI passed. No merge to main, no adoption of the proposed governance PR #3, no D145 release, and no product proof acceptance from this experiment. Independent semantic review of the policy choice and fixture corrections remains outstanding.

Report the exact GitHub Actions run/job, each step's pass/fail, test counts and the originally skipped architecture gate's first material failure once observed.
