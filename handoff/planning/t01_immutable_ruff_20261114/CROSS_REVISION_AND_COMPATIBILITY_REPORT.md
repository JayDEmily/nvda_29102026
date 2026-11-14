# T01 — Cross-revision Ruff debt and proposal compatibility evidence

**14 November 2026 (Australia/Melbourne). STATUS: AUTHOR VERIFIED / PROPOSAL ONLY / INDEPENDENT REVIEW AND OWNER POLICY DECISION PENDING.**

## Exact Git witnesses

- Repository `JayDEmily/nvda_29102026`; original `main`: `ded4b98e1e5999d1ddf2f067e660b691917bcd71` (unchanged).
- Proof-preserving fixture successor, draft PR #12: `b67f3e92470fe4e3281546fbc6fc62e347d5f0ee` (clean).
- Standalone proposal, draft PR #10 original source commit: `fece3d56e1259f8b4b084451069c08851de9e0cb`.
- **Local isolated composition only**: cherry-picked the PR #10 proposal on top of PR #12 into disposable WSL branch `experiment/t01-ruff-proposal-on-fixture-split-20261114`, commit `c8a776e7f33e4051935985a10b59d40fd3b5a34c`. No GitHub branch/pull request created for this experiment; PRs #10 and #12 remain independent draft sources.
- Isolated environment CPython 3.13.5, uv 0.10.0, locked offline sync: 15 resolved, 14 installed, exit zero. Ruff 0.15.11.

## Independent cross-revision baseline census

The same installed Ruff 0.15.11 binary executed `ruff check --output-format=json src tests tools` against **three separate exact Git worktrees**. Normalised diagnostics by relative path, code, message, starting row and column; compared full sets, not just counts.

| Git tree | E501 | I001 | B905 | RUF007 | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| `main` at `ded4b98e` | 40 | 5 | 4 | 4 | 53 |
| PR #12 at `b67f3e9` | 38 | 5 | 4 | 4 | 51 |
| Local PR #10 proposal applied to PR #12, `c8a776e` | 38 | 5 | 4 | 4 | 51 |

**Exactly 51 diagnostic tuples are common to `main` and PR #12; zero new tuples in PR #12.** The only removed mainline errors are two E501 lines in (1) `src/nvda_desk/derived_signal_calculation_truth/_financial_policy.py` and (2) `tests/product/derived_signal/test_m01_stage1_semantics.py`. All remaining 51 reside in seven original SHA-admitted proof family/support files, and on PR #12 all seven match their selected generation SHA-256 records. The unaltered proposal commit adds no new Ruff diagnostic.

This verifies the 51 are **historical mainline lint findings**, not new source-quality regressions caused by the Python/uv or fixture repair. It does NOT mean the existing strict zero-diagnostic CI policy can be silently waived.

## Normative vs implemented lint boundary

- `docs/architecture/TEST_AND_PROMOTION_KERNEL.md` (unchanged blob `f30a9cec974c25d1e45cd5564fc4b72bd57733aa`) defines AK-PROOF-001 exact admission and AK-PROOF-002 registry-derived `architecture_kernel` gate; **it does not establish a historical lint exception**.
- `Makefile` `lint` invokes `ruff check src tests tools`; `.github/workflows/architecture-kernel.yml` likewise invokes `uv run ruff check src tests tools` *before* the architecture gate. `pyproject.toml` pins Ruff 0.15.11 and `E,F,I,UP,B,SIM,RUF` rules. These are the currently implemented checks.
- Frozen `GUARDRAILS.md` forbids weakening validators merely for green. A hash-bound historical baseline changes the lint acceptance meaning, even though it retains strict diagnostic detection; **PR #10 does not authorise applying it to CI**.

## Actual combined-tree executable negative probes

On the exact isolated combined tree `c8a776e`, called the real prototype entrypoint `.venv/bin/python tools/proposed_admitted_ruff_baseline.py` (not a mocked `verify()` helper):

1. Original pristine combined tree: exit `0`, 51 exact diagnostics, digest `08ae839b0596c31ecb73a4667845f0d19dfe0c4503c52079434dd98e835a2a8f`.
2. Temporary mutation of a SHA-admitted product proof source: exit `1`, `admitted source bytes changed`.
3. Temporary mutation of a current proof generation pointer SHA: exit `1`, `generation bytes or pointer changed`.
4. Temporary alteration of the proposal baseline manifest: exit `1`, `baseline manifest byte identity changed`.
5. Temporary *new F821 Ruff diagnostic* in a previously clean `src` file: exit `1`, `Ruff findings changed by path`.
6. All temporary changes restored byte-for-byte: exit `0` on the exact original 51; `git status --porcelain` returned empty.

The local unmodified receipt is 1,347 bytes, SHA-256 `77a289b4f48630e9448030819e3de5eda67ce04c8d9956d3df9595223f434b6a`. The audit reproducer checks the exact detached experimental commit and a clean worktree before making any temporary modifications, and restores each mutation in `finally`; it is **not part of live CI**.

## Decision and exclusions

**Verified:** original 51 findings predate these repairs, all remain SHA-admitted on current proof-preserving tree; the proposed verifier is compatible with PR #12 and refuses real negative cases in a controlled worktree.

**Unknown/unapproved:** whether the owner/independent semantic reviewer accepts a policy-defined baseline instead of requiring every current historical file be re-admitted under a new proof generation. A policy decision cannot be inferred from a clean test of the prototype. No actual product proof execution, full architecture promotion run, CI replacement, merge, D145 activation or governance installation is claimed.

**Recommended bounded decision for independent review:** compare both lawful routes under the actual proof-admission and lint purposes, select an explicit acceptance law if warranted, and only thereafter amend CI in a separately reviewed candidate. Keep existing Ruff whole-tree check failing until authority is established; do not reseal old generations or forge evidence.

## Durable files

- `CROSS_REVISION_CENSUS.log`: same Ruff executable's read-only three-tree comparison outputs, including full per-file counts.
- `COMBINED_NEGATIVE_PROBES.log`: raw executable probe result summary with positive/negative/restore checks.
- `COMBINED_NEGATIVE_PROBES_REPRODUCER.py`: original pinned local scratch reproducer preserved as evidence, **not a production or CI script**.
