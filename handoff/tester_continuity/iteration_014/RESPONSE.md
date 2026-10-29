# Tester Iteration 014 — bounded VI-11R11 proof-adequacy audit

## Verdict

**PASS**

No unresolved `PRE_IMPLEMENTATION_CONTRACT_PROOF` blocker remains in the exact VI-10R11 candidate.
Under the current bounded VI-11 transition law, the next lawful programme step is **VI-12R**. This
PASS does not execute VI-12R and does not relabel later implementation-coupled or real-boundary
proof obligations as complete.

## Exact binding

- supplied archive SHA-256: `bf8fa7da6644791edddb482af56307c637c1cd712115940b6a4835a757616119`;
- supplied transport HEAD/tree: `8d0786411ef96ef703af665d091b9495ada1886b` /
  `3aca29ae96a87a19a9fcfb8144e5b6acaabcfa7e`;
- submitted VI-10R11 handoff/tree: `8c87fef8ed38a6ebbbd1ec65eb34618df3834bbf` /
  `64a879fc7d914a4f26e8e2fffb4b1d26304122d5`;
- physical proof commit/tree: `cca84de4ce2e9df52647352237c8a64e52a10db5` /
  `6b7881fc045345eef357248f4fa8f75f38599923`;
- physical parent / Tester Iteration 013 continuity: `39b5ca75e74ecd5cdee50c66c3a26fe3f34aec65` /
  tree `b044dae0738d9a7bf416319dc18bc7ea59c379b9`;
- preserved predecessor proof: `548a61107fda52e643142542ddb60dee584bd46e` /
  tree `e4e0850990545b46d57bb8241596fa1e51c60451`;
- physical candidate changes exactly one path:
  `tests/product/raw_signal/test_u05_postgresql_durability.py`;
- production `src/**` changes in the physical candidate: zero;
- `git fsck --full --strict`: PASS;
- submitted repository was clean before tester continuity was added.

## Environment preflight

An offline exact project environment was reconstructed from preserved project artefacts:

```text
Python 3.13.5
pytest 9.0.3
PyYAML 6.0.3
psycopg 3.3.4
mypy 1.20.1
Ruff 0.15.11
```

The preserved PostgreSQL archive independently hashed to
`59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf`; its packaged
`SHA256SUMS` verified. A fresh cluster was initialised and run as UID/GID 65534 (`nobody`) over a
Unix-domain socket:

```text
PostgreSQL 17.9
fsync=on
synchronous_commit=on
full_page_writes=on
```

This sandbox also admitted the user/mount/PID namespace primitive used by the proof harness. Two
infrastructure boundary canaries were therefore run successfully. The nine realised-system
namespace/filesystem propositions are nevertheless preserved as `UNPROVED`, because the Raw Signal
production implementation does not yet exist and those propositions cannot truthfully be promoted
from harness capability to realised-product evidence.

## T013-F001 — disposition

**CLOSED for `PRE_IMPLEMENTATION_CONTRACT_PROOF`.**

The predecessor false positive was reproduced conceptually by the successor canary and the repaired
mechanism was exercised against live PostgreSQL 17.9. The current proof installs an `AFTER`
INSERT/UPDATE/DELETE trace over every pre-existing non-system regular relation only after the
semantic `READY` point, records PostgreSQL transaction IDs, fails closed if a new untraced regular
relation appears, and requires the complete traced write-XID set to equal the backend XID observed
at `SyncRep`.

Independent results:

```text
live PostgreSQL environment/barrier/READY-GO/split-surrogate canaries   4 passed
split-marker/surrogate successor canary                                passed
multi-table INSERT/UPDATE/DELETE challenge                             all 4 expected XIDs captured
post-trace new regular relation challenge                              rejected as untraced
```

The independent DML challenge produced four distinct expected XIDs (`775`, `776`, `777`, `778`)
and the tracer returned exactly those four XIDs. Creating a new regular table after trace
installation caused `_postgresql_write_trace_xids()` to fail closed with the new relation named in
the assertion.

The five eventual product durable-success parametrisations were also invoked. All five are
currently expected-red at the first missing Raw Signal public seam,
`CaptureScopePolicyV1`; no production write path exists yet to execute. Under the current bounded
VI-11 directive this is a later realised-system proof axis, not evidence that the pre-implementation
contract is defective.

No concrete current false-positive path was found that defeats BC-011/BC-015 while satisfying the
bounded pre-implementation contract.

## T013-F002 — disposition

**CLOSED for `PRE_IMPLEMENTATION_CONTRACT_PROOF`.**

The former `proxy._inner` recovery path is absent. The concrete adapter is constructed inside the
forked child, while the semantic-owner side receives a process-separated record-only capability.
The child dispatcher allowlists exactly the nine technical storage methods.

Independent process challenge:

```text
parent PID                               1655
child PID                                1657
adapter constructor PID                  1657
adapter constructed only in child        true
parent public callables                   exactly 9 admitted record operations
parent state                              _calls, _connection, _process
parent _inner                             absent
private _semantic_decision dispatch       rejected by child boundary
```

The direct private-recovery canary and exact former `proxy._inner` graph canary passed. The broader
focused graph/transaction set, including instance/container/partial/closure/class/slot/global/
module/weak-reference cases, completed at **22 passed / 33 deselected** in the exact project
runtime.

No concrete parent-reachable capability was found that recovers the exact child adapter or invokes
its private semantic method outside the nine-method server allowlist.

## Independent repository checks

```text
product-proof validator                  PASS; 6 families / 13 of 13 obligations
product collection                       453 tests
architecture structural validator        PASS
architecture/bootstrap                   74 passed
architecture_kernel promotion            74/74 passed
mypy src                                 PASS; 15 source files
Ruff src/tests/tools                     PASS
dependency direction                     PASS
public-seam validation                   PASS
git diff --check                         PASS
```

The first product-proof validator invocation omitted `PYTHONPATH=src` and failed with
`ModuleNotFoundError: nvda_desk`. Re-running with the repository source path supplied produced the
PASS above. That environment invocation error is not a candidate defect.

## Finding classification and routing

No new `PRE_IMPLEMENTATION_CONTRACT_PROOF` finding was established.

No realised `IMPLEMENTATION_COUPLED_ADVERSARIAL_PROOF` defect can yet be established because the
Raw Signal production implementation is intentionally absent. The existing proof cases that
challenge the realised default owner graph, concrete adapter exposure, transaction strategy and
related implementation topology remain mandatory at **VI-13R**; this PASS does not pre-accept their
future outcome.

The following remain `MILESTONE_REAL_BOUNDARY_PROOF` axes and are **UNPROVED** for the realised
product: the five product commit-acknowledgement commands, restart/kill-after-return/database-clone
and full durable-readback behaviour, and the nine mapped namespace/filesystem propositions. They
remain routed to **VI-14** (and clean package/install evidence to VI-15 where applicable). The
successful PostgreSQL and namespace harness canaries in this review establish harness capability;
they do not substitute for those later realised-system proofs.

## Disposition

Tester Iteration 014 returns **PASS** on the bounded VI-11 contract. `T013-F001` and `T013-F002` are
closed as pre-implementation blockers. Do not open VI-10R12 solely to harden the harness against a
hypothetical future implementation technique. Preserve later implementation-coupled and milestone
proof obligations at their governed gates.

Per the current root `EXEC_PLAN.md`, **VI-12R is the next lawful programme step**.
