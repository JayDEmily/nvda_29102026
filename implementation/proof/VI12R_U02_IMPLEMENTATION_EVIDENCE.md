# VI-12R U02 implementation evidence

## Status

**WORKER CANDIDATE — NOT INDEPENDENTLY ACCEPTED.**

## Promotion and exact lineage

- Reviewer-022 accepted repaired U01 candidate: `e8b659d7849d2f95b64ba32bed8090a8290358d4`.
- Reviewer-022 PASS commit: `4db58e9091083500a2505023a302f36447185029`.
- Returned tester/handoff HEAD promoted by fast-forward to forward `main`:
  `b806447eb440a016826728af075e714beee23d31`.
- Both accepted U01 and Reviewer-022 PASS are ancestors of that `main`.
- U02 branch: `work/vi12r-u02-capture-policy-owed-slot`.
- U02 production candidate: `a77dc596b7cbc3f248097df94d8dd0bef4491bec`.
- U02 production tree: `1b8672a851f63c1bab8da02fb75de8357e4fad3c`.
- U02 production parent: `b806447eb440a016826728af075e714beee23d31`.
- Production candidate changes exactly one path:
  `src/nvda_desk/raw_signal_occurrence_truth/api.py`.
- Candidate binary diff SHA-256:
  `6770e58da79510651a7b704ca4e43dbfc3d3ede21da9d0455e419fd210d77a98`.

## Implemented proposition

IWO-U02 only: immutable capture-scope policy versions and exact owed-slot truth.

The candidate implements:

- exact UTC `:00` / `:30` half-minute activation, deactivation and slot alignment;
- strict later-than-activation deactivation when declared;
- no overlapping active policy intervals in this bounded slice;
- immutable same-policy-identity/version retry: identical registration is idempotent and changed
  content fails closed;
- exact 30-second `[start,end)` scheduled occurrences;
- no owed slot before activation or at/after declared deactivation;
- stable `(scope_policy_ref, slot_start_utc)` slot identity distinct from opaque
  `capture_occurrence_id`;
- same-slot/same-capture retry recovery; second capture identity for the same stable slot fails;
- reuse of one opaque capture identity for a different slot fails;
- referential U02 reads for registered policy versions and scheduled capture occurrences.

U03-U05 command/read behaviour remains deliberately `NotImplementedError`. No PostgreSQL,
persistence, provider mapping/admission, receipt relation, assessment or A00 composition was added.

## Exact validation environment

```text
Python 3.13.5
pytest 9.0.3
mypy 1.20.1 (compiled)
Ruff 0.15.11
```

The exact pinned pytest/Ruff/mypy wheels were recovered from preserved project artefacts outside the
repository. No environment tooling was committed to the candidate.

## Validation on exact committed candidate

With `HEAD=a77dc596b7cbc3f248097df94d8dd0bef4491bec` and clean worktree:

- focused U01+U02 product proof: **326 passed**;
- full `mypy src`: **success, 15 source files**;
- Ruff `src`: **pass**;
- product-proof control: **PASS**, six families, 13/13 obligations;
- public-seam validation: **PASS**;
- structural architecture validation: **PASS**, zero dependency/public-seam violations;
- architecture/bootstrap tests: **74 passed**;
- `architecture_kernel` promotion set: **74 passed**;
- `git diff --check`: pass;
- `git fsck --full --strict`: pass;
- committed worktree: clean.

## Scope and next gate

This Worker evidence does not accept U02. Fresh VI-13R Reviewer 023 must review the actual U02
candidate against IRB BC-003/BC-004/BC-010, IWO-U02 and the bounded U02 proof. U03 remains
prohibited until U02 is independently accepted and lawfully promoted to forward `main`.
