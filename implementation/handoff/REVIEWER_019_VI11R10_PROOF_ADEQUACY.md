# Reviewer 019 — VI-11R10 proof-adequacy audit

## Assignment

Act as the fresh independent tester for **Tester Iteration 013**. Audit only the VI-10R10 proof
repair and return `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`. Do not implement product
behaviour, change `src/**`, repair the candidate in place or begin VI-12R.

## Exact target

- physical proof commit: `548a61107fda52e643142542ddb60dee584bd46e`;
- physical proof tree: `e4e0850990545b46d57bb8241596fa1e51c60451`;
- physical parent/handoff: `36bba0d26b988881812d2333f7e1eb3e8e63786b`;
- preserved failed predecessor: `0917e0319a460a6d7ffb40b776b716f80f8f8684`;
- physical changed path: one `tests/product/raw_signal/**` file;
- production-source changes: none.

Bind the review separately to the supplied archive SHA-256 after transport verification. Do not
infer repository identity from the filename.

## Mandatory read order

1. root `GUARDRAILS.md`;
2. root `AGENTS.md`;
3. root `EXEC_PLAN.md`;
4. `implementation/proof/VI11R9_TESTER_ITERATION_012_DISPOSITION.md`;
5. `implementation/proof/VI10R10_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`;
6. `implementation/proof/VI10R10_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md`;
7. `tests/AGENTS.override.md`;
8. the physical diff and affected proof file.

## T012-F001 challenge

Run the two-commit transaction canary against PostgreSQL 17.9. For all five durable-success paths,
verify that the backend transaction ID observed in `SyncRep` is the sole `xmin` of every durable
row carrying the exact expected record identity after fresh readback. Challenge a post-`GO`
setup/audit transaction which copies the record identity before a later semantic commit; it must
produce multiple transaction identities and fail.

## T012-F002 challenge

Confirm that the opposing-eligibility proof constructs each semantic owner with the record-only
injected port, rather than exposing the concrete adapter and repairing the graph afterwards. Run
the weak-reference, weak-method, proxy and callable-proxy canaries after the ordinary direct port
has already been removed. Challenge any remaining recoverable concrete capability outside the
record-only injection boundary.

## Environmental boundary

The Worker could not start the attached PostgreSQL runtime because this sandbox maps only UID 0;
the new database-backed transaction canary is therefore Worker-`UNPROVED`, not passing. Run it
independently. Separately preserve the nine mapped namespace/filesystem propositions as
`UNPROVED`; they are not passes and are not themselves a rejection basis under current Programme
Owner direction.

## Worker evidence to reproduce or challenge

```text
product proof control                     6 families / 13 of 13 obligations
product collection                        450 tests
focused transaction/graph canaries        18 passed
U05 without live DSN                      28 failed / 24 passed
complete product without live DSN         420 failed / 30 passed
structural architecture validation        passed
architecture/bootstrap available axis     71 passed / 3 deselected
Ruff / dependency / public seams          passed
```

The Worker did not freshly establish live PostgreSQL execution or the exact Python-3.13.5
mypy/promotion axis. Independently run both and report them separately.

## Required response

Return exact archive/commit/tree identities, integrity results, independent reproduction,
separate dispositions for `T012-F001` and `T012-F002`, the environmental caveat disposition, any
new finding with a concrete false-positive path, and the final Tester Iteration 013 verdict.
