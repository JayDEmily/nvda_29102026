# Gate 3 — Assertion-strength audit: proof_executor_contract

Status before amendment: `PARTIAL_WEAK_ASSERTION_RISK_FOUND`
Status after amendment: `IMPROVED_FOR_SELECTED_KNOWN_BAD_CASES`

## Existing assertion surface before amendment

The original file had 14 tests. Useful behavioural coverage existed for manifest description, check mode, check-all mode, JSON receipt writing, JSON list output, and python interpreter resolution.

Weaknesses found:

| Weakness | Evidence | Risk |
|---|---|---|
| Several tests asserted source text rather than behaviour | original tests read `scripts/run_proof_block.py`, `Makefile`, and manifest text directly, e.g. current lines `12-23`, `53-58`, `135-145` | false positive if required behaviour disappears but tokens remain |
| No unknown-block rejection test | no original known-bad temporary manifest exercised `_find_block` failure | executor could accept/route wrong IDs without test failure |
| No missing-owned-path execution-blocking test | original lines `53-58` only checked source strings for `_validate_owned_paths` | runner could skip validation and execute commands despite missing ownership |
| No duplicate-block rejection test | no original duplicate manifest fixture | manifest ambiguity could survive |
| No non-mapping block rejection test | no original malformed list entry fixture | malformed proof block could survive |
| No shell-injection resistance test | original `test_proof_block_runner_resolves_python_to_current_interpreter` only called `_resolve_command` directly, lines `226-236` | command execution could change to `shell=True` and still pass |

## Classification

| Test group | Classification before amendment | Classification after amendment |
|---|---|---|
| control-surface presence/token tests | smoke / harness-only | retained as smoke |
| describe/check/check-all receipt tests | behavioural assertion | retained |
| current interpreter resolution | behavioural unit assertion | retained |
| unknown-block/missing-owned/duplicate/non-mapping/no-shell tests | missing | added as strong negative behavioural assertions |

No Tier promotion was made. This family remains Tier B.
