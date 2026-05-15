# FWD-008/FWD-009 ordered replay boundary receipt

Status: `bounded_closed_current`

## Boundary controls

- Phase A accepted and merged the worker lineage through FWD-007 before FWD-008 was opened.
- FWD-008 was closed before FWD-009 was opened.
- FWD-010 was not opened.
- No original Atlas/Bridge JSON or generated Atlas slice was mutated.
- No source/test/config/fixture/data/dependency/vocabulary mutation was made in Phase B.

## Ordered results

- FWD-008: `bounded_closed_current`, selected coverage `117/117`, unresolved `0`.
- FWD-009: `bounded_closed_current`, selected coverage `51/51`, unresolved `0`.

## Remaining boundary

Next roadmap row is FWD-010 / 5.9 Dynamic coefficient and modifier authority. It remains unopened by this package.

## Broad validation after ledger update

- `git diff --check`: exit `0`.
- `python scripts/run_proof_block.py --check-all`: exit `0`, `proof_blocks_check_all=PASS count=46`.
- `PYTHONPATH=src python -m pytest -q tests/tier_b`: rerun exit `0`, `49 passed`.
- `PYTHONPATH=src python -m pytest -q tests/tier_a`: exit `0`, `560 passed`.
- Note: Tier A pytest rewrote `var/vocabulary/synonym_candidates.json` to the fixture fingerprint during test execution; that generated side effect was reset before commit.
