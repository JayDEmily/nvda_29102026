# Reviewer 020 — VI-11R11 proof-adequacy audit

## Assignment

Act as the fresh independent tester for **Tester Iteration 014**. Audit only the VI-10R11 proof
repair and return `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`. Do not implement product
behaviour, change `src/**`, repair the candidate in place or begin VI-12R.

## Exact target

- physical proof commit: `cca84de4ce2e9df52647352237c8a64e52a10db5`;
- physical proof tree: `6b7881fc045345eef357248f4fa8f75f38599923`;
- physical parent / Tester Iteration 013 continuity:
  `39b5ca75e74ecd5cdee50c66c3a26fe3f34aec65`;
- preserved failed predecessor: `548a61107fda52e643142542ddb60dee584bd46e`;
- physical changed path: one `tests/product/raw_signal/**` file;
- production-source changes: none.

Bind the review separately to the supplied archive SHA-256 after transport verification. Do not
infer repository identity from the filename.

## Mandatory read order

1. root `GUARDRAILS.md`;
2. root `AGENTS.md`;
3. root `EXEC_PLAN.md`;
4. `handoff/tester_continuity/iteration_013/RESPONSE.md` and `EVIDENCE.md`;
5. `implementation/proof/VI11R10_TESTER_ITERATION_013_DISPOSITION.md`;
6. `implementation/proof/VI10R11_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`;
7. `implementation/proof/VI10R11_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md`;
8. `tests/AGENTS.override.md`;
9. the physical diff and complete affected proof file.

## T013-F001 challenge

Against PostgreSQL 17.9, run the split-marker/surrogate payload canary and all five durable-success
commands. Confirm that:

- the predecessor literal-marker predicate accepts only the audit XID in the adversarial split;
- the successor trace captures both audit and payload XIDs and rejects that split;
- each valid command's complete post-`GO` database-write XID set is exactly the backend XID observed
  in `SyncRep` after exact fresh readback; and
- a new durable regular relation created after `READY` fails closed as untraced.

Challenge normalised multi-table representations, updates and deletes; none may hide a second
transaction behind one marker-bearing row.

## T013-F002 challenge

Confirm that each source/true/false semantic owner receives the forked record-only capability and
that its concrete default PostgreSQL adapter is constructed only in the child process. Verify the
parent capability exposes exactly the nine record operations, contains no `_inner`, and rejects a
private/non-protocol dispatch at the server boundary. Run the direct recovery and exact prior
`proxy._inner` canaries, plus the existing instance/container/partial/closure/class/slot/global/
module/weak-reference graph canaries.

Challenge any parent-reachable object that could recover the exact concrete adapter or invoke its
private semantic method. A technical transport handle is not itself a pass if it enables private
adapter dispatch outside the server allowlist.

## Environmental boundary

The Worker could not start PostgreSQL in the UID-0-only sandbox; all new live database cases are
Worker-`UNPROVED`, not passing. Run them independently. Preserve the nine mapped
namespace/filesystem propositions as `UNPROVED`; they are not passes and are not themselves a
rejection basis under current Programme Owner direction.

## Worker evidence to reproduce or challenge

```text
product proof control                     6 families / 13 of 13 obligations
product collection                        453 tests
focused non-database canaries              20 passed
U05 without live DSN                       28 failed / 27 passed
complete product without live DSN          420 failed / 33 passed
structural architecture validation         passed
architecture/bootstrap available axis      71 passed / 3 unexecuted
Ruff / dependency / public seams           passed
```

The Worker did not freshly establish live PostgreSQL execution or the exact Python-3.13.5
mypy/promotion axis. Independently run both and report them separately.

## Required response

Return exact archive/commit/tree identities, integrity results, independent reproduction, separate
dispositions for `T013-F001` and `T013-F002`, environmental caveat disposition, any new finding with
a concrete false-positive path, and the final Tester Iteration 014 verdict.
