# Tester Iteration 014 — evidence

## Source identity and integrity

- source archive SHA-256: `bf8fa7da6644791edddb482af56307c637c1cd712115940b6a4835a757616119`;
- transport HEAD/tree: `8d0786411ef96ef703af665d091b9495ada1886b` /
  `3aca29ae96a87a19a9fcfb8144e5b6acaabcfa7e`;
- submitted handoff/tree: `8c87fef8ed38a6ebbbd1ec65eb34618df3834bbf` /
  `64a879fc7d914a4f26e8e2fffb4b1d26304122d5`;
- physical proof/tree/parent: `cca84de4ce2e9df52647352237c8a64e52a10db5` /
  `6b7881fc045345eef357248f4fa8f75f38599923` /
  `39b5ca75e74ecd5cdee50c66c3a26fe3f34aec65`;
- physical diff: one modified U05 product-proof file, zero `src/**` changes;
- `git fsck --full --strict`: PASS.

Authority hashes rebound:

```text
IRB markdown   938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342
BICP JSON      5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed
BICP markdown  6b2906b92e11bf09fd7f8b188e8ed6555a0a5ae61636909f676f84827601d21f
```

```text
IWO markdown   b23fec7e83eace6353272f92b983160c2ab768043640d15d7ee1fb88f270ca0e
```

## Governing material inspected

Read before disposition:

- `GUARDRAILS.md`;
- root `AGENTS.md`;
- root `EXEC_PLAN.md`;
- `implementation/handoff/TESTER_ITERATION_014_BOUNDED_REVIEW_DIRECTIVE.md`;
- Tester Iteration 013 `RESPONSE.md` and `EVIDENCE.md`;
- `implementation/proof/VI11R10_TESTER_ITERATION_013_DISPOSITION.md`;
- VI-10R11 repair design and evidence;
- `tests/AGENTS.override.md`;
- complete VI-10R11 physical diff and complete affected U05 proof file;
- Reviewer 020 historical assignment;
- accepted IRB, BICP and IWO semantic authorities relevant to BC-011/BC-013/BC-015 and U05.

## Exact runtime

Offline pinned environment:

```text
Python 3.13.5
PyYAML 6.0.3
pytest 9.0.3
psycopg 3.3.4
mypy 1.20.1
Ruff 0.15.11
```

Portable PostgreSQL archive:

```text
archive sha256=59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf
PostgreSQL 17.9
fsync=on
synchronous_commit=on
full_page_writes=on
server OS user=nobody (UID/GID 65534)
Unix-domain socket only
```

Packaged `SHA256SUMS` verification: PASS.

## Focused execution results

```text
new VI-10R11 repair tests                                      4 passed
focused transaction/graph canaries                            22 passed / 33 deselected
live PG env + SyncRep + READY/GO + split-surrogate            4 passed
namespace/filesystem harness canaries                          2 passed
five product durable-success parametrisations                 5 expected-red
  reason for each: missing pre-implementation public symbol
  CaptureScopePolicyV1
product proof control                                          PASS; 6 families / 13/13
product collection                                             453 tests
architecture/bootstrap                                         74 passed
architecture_kernel promotion                                  74/74 passed
mypy                                                            PASS; 15 source files
structural architecture                                        PASS
Ruff                                                            PASS
dependency direction                                           PASS
public seams                                                    PASS
git diff --check                                               PASS
```

## Independent T013-F001 challenge

The live successor split-marker/surrogate canary passed. A separate tester challenge created two
regular tables before trace installation, then committed INSERT, UPDATE, a second-table INSERT and
DELETE in four independent transactions. Observed XIDs were:

```text
expected: 775 776 777 778
traced:   775 776 777 778
```

The sets matched exactly. A new regular table created after trace installation was then detected as
untraced and the helper failed closed.

## Independent T013-F002 challenge

A tester canary instrumented adapter construction by PID. The adapter constructor ran in child PID
1657, not parent PID 1655. Parent state contained only `_calls`, `_connection`, `_process`; `_inner`
was absent. Public callables were exactly the nine methods in `_STORAGE_PROTOCOL_BOUND_ARITY`.
A `_semantic_decision` request was rejected as outside the record-only protocol.

## Preserved limits

Passing harness canaries are not promoted into realised-product evidence. The production
implementation does not yet exist. Therefore the five real product commit-acknowledgement paths,
restart/clone/kill-after-return/durable-readback behaviour, and nine mapped namespace/filesystem
propositions remain `UNPROVED` milestone evidence and are not used as a VI-11 rejection basis.
