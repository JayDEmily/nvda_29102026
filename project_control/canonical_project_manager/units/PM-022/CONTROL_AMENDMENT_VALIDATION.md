# PM-022 Gate C evidence-economy control amendment

## Disposition

`PASS:CONTROL_ROUTE_AMENDED_VALIDATION_UNCHANGED`

## User-directed decision

Retain the semantic order `normative authority → admitted proof → module-local implementation`, but stop treating duplicate successful raw validation output as a default tracked deliverable. Required validation still executes.

## Measured basis

| Module | Retained validation lines | Retained bytes | Largest duplicate pair |
|---|---:|---:|---|
| M07 K12 | 44,256 | 2,393,201 | baseline/current Tier A text: 1,193,730 + 1,182,419 bytes |
| M08 K13 | 44,897 | 2,445,671 | current/baseline Tier A text: 1,196,850 + 1,193,654 bytes |
| M02 K04 | 42,555 | 2,979,828 | baseline/current Tier A JUnit XML: 1,467,134 + 1,452,878 bytes |

Each module already retained a concise validation summary containing the decisive counts, failing-node delta and limitations.

## Validation

| Check | Result |
|---|---|
| Current-target full-read manifest | PASS — 20 entries; zero missing paths |
| Pre-mutation hash boundary | PASS — all four intended control files changed; zero read-only hash drift |
| Branch/checkpoint route consistency | PASS |
| Explicit validation non-waiver language | PASS across ExecPlan, protocol, roadmap and process overlay |
| `git diff --check` | PASS |
| `python scripts/run_proof_block.py --check-all` | PASS — 57 blocks |
| `python -m pytest -q tests/tier_b/proof_model/test_proof_executor_contract.py` | PASS — 21 tests |

## Claim boundary

This amendment changes evidence retention and baseline-rerun defaults only. It does not skip, narrow, suppress or weaken blocking, affected, aggregate, architecture, vocabulary or shadow validation. Raw output remains mandatory when it contains a novel regression, non-deterministic result, material environment failure or evidence required for high-consequence independent review.
