# Reviewer 017 — VI-11R8 Proof-Adequacy Audit

## Assignment

Act as the fresh independent tester for **Tester Iteration 011**. Audit the VI-10R8 proof repair
and return one explicit verdict: `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`.

This is a proof-adequacy audit only. Do not implement product behaviour, change `src/**`, repair
the candidate in place, or begin VI-12R.

## Exact target

- physical proof commit: `7dc7ce0bb4d162d785bac5b0f431bdab77d954e7`
- physical proof tree: `134ddc76e61f9751e46cb1990c762ee028f86719`
- physical parent: `0f9c0b74fb10bd6542614651427ac72a13ed68d0`
- repair/disposition parent: `e58a0a6116dfccde8645d4ea6b423774953adb48`
- amended pre-TCP checkpoint: `09a6fd77829838522b0a7b037f068c5d1f30f3e1`
- physical changed path:
  `tests/product/raw_signal/test_u05_postgresql_durability.py`
- production-source changes: none

Bind the review separately to the supplied archive SHA-256 after transport verification. Do not
infer repository identity from the archive filename.

## Mandatory read order

1. root `GUARDRAILS.md`;
2. root `AGENTS.md`;
3. root `EXEC_PLAN.md`;
4. `implementation/proof/VI11R7_TESTER_ITERATION_010_DISPOSITION.md`;
5. `implementation/proof/VI10R8_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`;
6. `implementation/proof/VI10R8_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md`;
7. `implementation/proof/VI10R8_WORKER_VALIDATION_BLOCKED.md` as preserved earlier evidence;
8. `tests/AGENTS.override.md`;
9. the physical diff and every affected proof helper/test path.

## Findings under review

### T010-F001 — server COMMIT acknowledgement across every durable-success command

Challenge the five parameterised command cases independently. Confirm that each warms the same
selected command path, establishes only its prerequisites, observes its uniquely named backend
in PostgreSQL `SyncRep` with no public-return marker, releases the server barrier, requires no
open writer transaction and performs fresh public readback against a parent-held expected record.

### T010-F002 — nested ordinary-container and cached capability capture

Challenge direct references, ordinary owner objects, recursive list/dict/tuple/set/frozenset
containers, `functools.partial` function/argument/keyword captures, closures/defaults and admitted
public bound-record methods. Confirm that concrete/private adapter capability cannot remain
reachable after rewriting and that the implementation-independent canaries would catch the
relevant false positives.

## Degraded-TCP audit boundary

The current user expressly authorised forward progress with a TCP caveat. The tester must keep
two conclusions separate:

1. whether the T010-F001/T010-F002 proof repair is semantically adequate; and
2. whether the nine mapped namespace/filesystem propositions were established in this worker
   environment.

The second conclusion is already `UNPROVED` in the Worker evidence. TCP used a real PostgreSQL
17.9 server, but it did not supply the mapped mount/network/PID namespace or exclusive local
filesystem. Confirm that:

- TCP requires the exact `NVDA_U05_DEGRADED_TCP=1` opt-in;
- the default Unix-socket/namespace path is unchanged;
- namespace-dependent cases fail with `DEGRADED TCP VALIDATION: UNPROVED`;
- none is skipped, xfailed or counted as passing; and
- no product/proof PASS is inferred from the degraded run.

If the audit requires the nine propositions themselves to pass, return `BLOCKED` for that exact
environmental reason rather than converting degraded evidence into acceptance.

## Worker-observed evidence to reproduce or challenge

```text
product proof control                  PASS; 6 families; 13/13 obligations
product collection                    438 tests
U05 degraded TCP                      24 failed / 16 passed
  explicit boundary                  9 failed as UNPROVED
  absent production                  15 failed
complete product degraded TCP        416 failed / 22 passed
  explicit boundary                  9 failed as UNPROVED
  absent production/static          407 failed
architecture/bootstrap              74 passed
architecture_kernel promotion       74 passed; rc=0
mypy / Ruff / dependency / seams    PASS
Git integrity / clean state         PASS
```

Use the separately supplied PostgreSQL runtime only after verifying its outer SHA-256
`59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf` and internal 1,937-file
manifest.

## Required response

Return:

- exact archive, commit and tree identities actually reviewed;
- transport and internal-integrity results;
- independent reproduction results and environment boundary;
- separate dispositions for `T010-F001` and `T010-F002`;
- an explicit disposition for the degraded-TCP caveat;
- any new finding with severity, exact evidence, false-positive path and owning layer; and
- the final Tester Iteration 011 verdict.
