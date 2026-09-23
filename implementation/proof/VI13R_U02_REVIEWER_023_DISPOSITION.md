# VI-13R U02 Reviewer 023 disposition

## Disposition

`FAIL / RETURN_TO_WORKER`

U02 may not be promoted. U03 remains prohibited. Independent standard validation is green, but the
realised U02 candidate exposes its mutable semantic owner state directly through both public facets,
which permits a caller to bypass the typed command boundary and violate accepted U02 truth.

## Binding

- source archive SHA-256: `a9d0a8b302db9bad5812f8ffff43c97dfafa25b8a80e6d92f89d64d6a57c2522`;
- source archive: `NVDA_G03_TESTER_VI13R_U02_R023_1790125061_FULL_GIT_20260923.tar(1).gz`;
- transported review-entry HEAD: `828b04e48632f11317bed544fb795702af167dad` / tree
  `177cdf30c965acecda4c870ed0cfada93ae1ba4e`;
- accepted/promoted U01 main: `b806447eb440a016826728af075e714beee23d31`;
- frozen U02 candidate: `a77dc596b7cbc3f248097df94d8dd0bef4491bec` / tree `1b8672a851f63c1bab8da02fb75de8357e4fad3c`;
- candidate parent: `b806447eb440a016826728af075e714beee23d31`;
- candidate production change: `src/nvda_desk/raw_signal_occurrence_truth/api.py` only;
- complete production diff SHA-256: `6770e58da79510651a7b704ca4e43dbfc3d3ede21da9d0455e419fd210d77a98`.

## Material inspected

The review read the full routing/governance set required by `README.md`, the accepted U02 semantic
authority, the accepted U01 seam/owner law carried forward into U02, Worker U02 evidence, complete
production diff/current `api.py`, and bounded U02 proof. The exact material and command record are
preserved in `handoff/review_cycles/TESTER_VI13R_U02_R023_1790125061/`.

## Independent validation

Exact review tooling: Python 3.13.5, pytest 9.0.3, mypy 1.20.1 (compiled), Ruff 0.15.11.

- focused U01+U02: 326 passed;
- positive strict mypy: pass;
- negative strict mypy: all 15 intended sites diagnosed;
- source mypy and Ruff: pass;
- product-proof, structural architecture, dependency and public-seam validators: pass;
- architecture/bootstrap and promotion: 74/74;
- diff and strict Git-integrity checks: pass.

These results show that the existing proof/control surface remains green. They do not establish
semantic acceptance against the concrete object-graph bypass below.

## R023-U02-F001 — public facets expose mutable semantic owner state

**Accepted propositions defeated:** BICP `BICP-COMP-002` and `IF-ARCH-004` prohibit private-state
bypass and bind cross-owner use to the M00 typed command/read boundary; IWO-U01 fixes M ownership
of the write boundary; IRB BC-003/IWO-U02 require at most one active capture-scope policy version at
an instant; Reviewer-023 is explicitly required to preserve referential U02 reads and accepted U01
seam law.

**Realised candidate:** `_CommandsV1` and `_ReadsV1` each store `_state` as an ordinary slot and
`create_owner()` gives both facets the same mutable `_U02State`. That state contains writable policy
and capture dictionaries.

**Concrete challenge:** two overlapping public `CaptureScopePolicyV1` values were constructed.
`owner.commands.register_capture_scope_policy(second)` correctly raised `ValueError`. Direct
ordinary access through `owner.commands._state` then inserted the rejected policy into both policy
maps. The public capture command subsequently admitted an owed-slot capture under the overlapping
policy at 12:01 UTC and the public read facet returned the forged policy. Mutating the same state
through `owner.reads._state` also erased an existing policy from referential readback.

No private module was imported and no monkey-patching, `eval`/`exec` or arbitrary metaprogramming
was used. This is the concrete mutable capability carried on the public objects returned by the
candidate itself. The leading underscore is not an enforcement boundary under the accepted Public
Seam Law.

**Smallest owning-layer repair:** U02 M-owner implementation and its bounded implementation-coupled
proof. Remove ordinary caller-reachable mutable semantic-state capability from the public command
and read facets, while preserving their accepted observable semantics, and add a regression that
closes the concrete bypass. Exact internal decomposition is implementation freedom. Do not alter
IRB/IWO meaning, weaken overlap/idempotency checks, activate U03, or expand persistence/provider
scope.

## Gate effect

Final Reviewer 023 disposition: **`FAIL / RETURN_TO_WORKER`**.

The frozen U02 candidate `a77dc596b7cbc3f248097df94d8dd0bef4491bec` is not promotable. Worker repair is limited to
`R023-U02-F001`; after a repaired candidate is frozen, a fresh independent U02 reviewer is required.
U03 remains prohibited until U02 later receives `PASS` and is lawfully promoted to forward `main`.
