# T01 architecture-kernel CI reconciliation — bounded worker findings

Date: 14 November 2026, Melbourne. Status: PARTIAL / INDEPENDENT REVIEW PENDING / NO MAIN PROMOTION.

## Pinned Git and scope
Repository: `JayDEmily/nvda_29102026`.
Main at assessment: `ded4b98e1e5999d1ddf2f067e660b691917bcd71`.
Python 3.13.5 and offline wheelhouse candidate PR #5: `8f236660e9b5982c242b6f114882f045cd1f291e`.
Unqualified Ruff formatting PR #7: `8674d1e6fb81cefe6cd66ec45808348bb4f2e793`.
New follow-on work branch: `work/t01-ci-history-repair-20261114`.

Original CI witness: [run 43205348398](https://github.com/JayDEmily/nvda_29102026/actions/runs/43205348398), validate job 131139000821, failed with 132 architecture tests failed and 89 passed. The same run passed `uv sync --locked --extra dev` and `uv run ruff check src tests tools`; CI `git diff --check` was skipped. This witness preceded the new corrections and is not their validation.

## Two bounded corrections published as separate commits

1. `ef0b2527810acf84593a9a39ab1ac7e9f8b72b8a` — add `fetch-depth: 0` to `.github/workflows/architecture-kernel.yml` (`actions/checkout@v4`). The existing `tools/product_proof_claims.py::_admission_history` enumerates retained Git commits and previous pointer/generation transitions. The old checkout's default depth of one commit (confirmed in official actions/checkout v4 README) is incompatible with that validation. Verification: valid YAML parsed with `fetch-depth == 0`; `git diff --check` passed. Previously, after `git fetch --unshallow` in a separate WSL clone, static admission-history checks for market_measurement, market_measurement_d032 and market_measurement_d033 all passed. These are not a whole-workflow result.
2. `70374225bb6098698c9558eed5809836ce768d4d` — update `tests/architecture/test_identifier_taxonomy.py`, `test_implementation_authority_ingress.py` and `test_registry_schema.py` to account for the already admitted M03 configured_market_conditions allocation, dated 2026-10-24. Source `config/architecture/modules.yaml` contains current M00/M01/M02/M03; `implementation_allocations.yaml` assigns M03. [Historical independent D040 review](https://github.com/JayDEmily/nvda_29102026/blob/171a9149dea53f44a1bd1fec6a1d7971c3c1a9f3/handoff/configured_market_conditions/d040_execution/final_review.md) explicitly establishes lawful nonnumeric M03 ingress for the D040 controlled profile. Those architecture tests last changed on 19 October, before M03 admission on 23–24 October. The tests still assert exact ordered current IDs, prospective IDs, nonmutation, retired+allocated gaps and ingress templates; none is skipped or suppressed. Local command: `.venv/bin/python -m pytest -q tests/architecture/test_identifier_taxonomy.py tests/architecture/test_implementation_authority_ingress.py tests/architecture/test_registry_schema.py` -> **37 passed in 1.24 s**. Changed-file Ruff -> `All checks passed!`. `git diff --check` -> exit 0. This is author validation, not independent review.

## Current first unresolved invariant — proof-admitted immutable bytes

Seven test files formatted in PR #7 are SHA-256-bound by existing `config/product_proof/**/generations/*.json` records. The existing generation files match the parent bytes, not the reformatted bytes. `tools/product_proof_claims.py:396-405` correctly rejects the altered family/support hashes. It is not valid to retrospectively reseal or rewrite old generations. A syntax-tree equivalence check does not establish proof admission. No new generation was created; no product proof was executed.

## Additional test-fixture and source issues still unresolved

- `tests/architecture/test_proof_control.py::_copy_candidate` intentionally constructs an M02-absent historical pre-admission universe but retains the later M03 owner which declares a dependency on M02; its resulting temporary architecture state is invalid. A candidate fix to remove transitive dependent owners *only inside the fixture* was tested and **failed** one targeted architecture test at the next authority check: `modify target M02 is not registered`, because the copied current authority binding now requires modification of existing M02. The trial edit was **reverted before any commit**. The fixture's historical purpose and current authority need explicit reconciliation; do not simply delete M03, change real module registrations or weaken tests.
- A historical physical-test inventory assertion in the same architecture file expects 93 `test_*.py` paths; the failing CI snapshot found 198. This requires a proof-partition census and authority reconciliation, not blind rewriting to 198.
- No complete end-to-end re-run of the architecture gate after the two new commits. CI remains **BLOCKED**; independent review of the bounded corrections remains pending.

## Safe next action

Independently review both new commits and the source/authority lineage. Reconcile frozen byte-bound proof tests through an independently governed admission or explicit policy decision, without weakening existing validators. Rebuild the historical pre-admission architecture fixtures against their intended authority and audit full physical proof partitions before changing their assertions. Only after warranted repairs rerun mandatory CI; preserve original failures and all generations. Do not merge PR #5/#7, alter frozen GUARDRAILS or adopt new root governance until required gates pass. D145 remains paused.

This document is a WORKER finding, not an independent reviewer verdict, acceptance, test certification, Git receiver receipt or authority to modify source/domain rules.
