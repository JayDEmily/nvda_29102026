# Final Alpha Consolidation — Validation Summary

## Status

`IN_PROGRESS:FINAL_CLEAN_COMMIT_VALIDATION_PENDING`

## Baseline proved before consolidation edits

At clean commit `4db29df4d1831ebb75defe9148c15e9356a6876b` in CPython 3.13.5:

| Check | Result |
|---|---|
| Offline non-editable installation | PASS — 38 compatible distributions; dependency check passed |
| Installed-package smoke | PASS — imports from `.venv/site-packages` |
| Proof authority | PASS — 196 families, 198 test paths, 67 proof blocks |
| Promotion membership | PASS — 14 blocks, 14 families, 16 selected paths |
| Aggregate Tier A promotion | PASS — 14/14 blocks, 754 passed, zero skips |
| Promotion receipt verification | PASS — content hash `d593a360a7e2c5d291de274e17bd2f39b2afece9e0894eea239fa4cfea3b483b` |
| Tier B | PASS — 84 passed |
| Black | PASS — 473 files unchanged |
| Ruff | PASS — zero findings |
| Diff check | PASS |

Raw command output is retained outside Git under `/mnt/data/final_alpha_prevalidation/`; the repository retains this concise reproducible result.

## Consolidation findings

1. The M00 vocabulary definition contradicted the accepted application law by saying `RunCoordinator` invoked all M01–M13 seams in one governed run. It was corrected to the M03-start, M05/M06, M09, M10, M11 path with separate M12 delegation and internal M13 participation.
2. Current CLI/ASGI adapters remain on the explicitly noncanonical legacy orchestrator path.
3. Tier C contains no tests and establishes no operational assurance.
4. Current vocabulary audits are not clean except for m07; exact counts are in `VOCABULARY_AUDIT_SNAPSHOT.tsv`.
5. The previous 4db29df full-history checkpoint contained all Git objects and passed `git fsck`, but omitted six tracked worktree files. They were restored exactly from Git. The final archive must be produced from a fresh clean clone and independently verified.

## Final validation required

After the consolidation commit:

```bash
make install-offline RUNTIME_WHEELHOUSE_ZIP=<accepted-v6-runtime.zip> DEV_WHEELHOUSE_ZIP=<accepted-v4-dev.zip>
make installed-package-smoke
.venv/bin/python scripts/proof_authority.py --check --json
make promotion-check
make promotion-gate
.venv/bin/python scripts/verify_promotion_receipt.py <receipt>
.venv/bin/python -m pytest -q tests/tier_b
.venv/bin/black --check .
.venv/bin/ruff check .
git diff --check
```

The final checkpoint must additionally prove extracted branch/commit identity, an empty `git status --porcelain`, presence of all tracked files and `git fsck --full --no-dangling` exit zero.
