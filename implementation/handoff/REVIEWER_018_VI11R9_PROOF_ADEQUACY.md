# Reviewer 018 — VI-11R9 proof-adequacy audit

## Assignment

Act as the fresh independent tester for **Tester Iteration 012**. Audit only the VI-10R9 proof
repair and return `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`. Do not implement product
behaviour, change `src/**`, repair the candidate in place or begin VI-12R.

## Exact target

- physical proof commit: `0917e0319a460a6d7ffb40b776b716f80f8f8684`;
- physical proof tree: `fd5a1cb626f1fb7c41602f989d5f900c080f9537`;
- physical parent/handoff: `d1bad95bddd8b868449f2566b40d38126d50a789`;
- physical changed paths: two `tests/product/raw_signal/**` files;
- production-source changes: none.

Bind the review separately to the supplied archive SHA-256 after transport verification. Do not
infer repository identity from the filename.

## Mandatory read order

1. root `GUARDRAILS.md`;
2. root `AGENTS.md`;
3. root `EXEC_PLAN.md`;
4. `implementation/proof/VI11R8_TESTER_ITERATION_011_DISPOSITION.md`;
5. `implementation/proof/VI10R9_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`;
6. `implementation/proof/VI10R9_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md`;
7. `tests/AGENTS.override.md`;
8. the physical diff and both affected proof files.

## T011-F001 challenge

Confirm for all five durable-success paths that owner construction and command-input preparation
finish before `READY`; the server barrier is installed only after `READY`; the child cannot call
the selected semantic command before `GO`; and the observed post-`GO` `SyncRep` wait cannot be the
canary's already-committed owner-setup transaction. Challenge early-returning semantic writes and
per-owner/per-process setup transactions independently.

## T011-F002 challenge

Re-run the tester's class-level cache canary and challenge slots, referenced globals and reachable
module storage. Confirm both the rewriter and post-rewrite checker fail closed on concrete/private
capability outside `vars(instance)`, while prior nested-container/partial/closure coverage and
admitted public-record rewrites remain intact.

## Degraded-TCP boundary

Per current Programme Owner direction, keep proof adequacy separate from the nine environment
propositions. They remain `UNPROVED`, are not passes, and must not be used as evidence that mapped
namespace/filesystem isolation succeeded.

## Worker evidence to reproduce or challenge

```text
product proof control                     6 families / 13 of 13 obligations
product collection                        444 tests
U05 degraded TCP                          24 failed / 22 passed
complete product degraded TCP             416 failed / 28 passed
graph canaries                            13 passed
real PostgreSQL handshake canary          passed
structural architecture validation        passed
Ruff / dependency / public seams          passed
```

The Worker did not freshly establish the exact Python-3.13.5 mypy/promotion axis in its reset
workspace. Independently rerun that unchanged axis and report it separately.

## Required response

Return exact archive/commit/tree identities, integrity results, independent reproduction, separate
dispositions for `T011-F001` and `T011-F002`, the degraded-TCP caveat disposition, any new finding
with a concrete false-positive path, and the final Tester Iteration 012 verdict.
