# Tester Iteration 013 — Evidence

## Source and Git identity

- Source archive: `NVDA_G03_VI11R10_TESTER_ITERATION_013_FULL_GIT_20260922.tar.gz`
- SHA-256: `f67ef9c88c9b6470f46200815f5ac4b29505f3ce309a6a3ca482eeb6832280b3`
- Submitted HEAD/tree: `2b17c3b545242475889b85aa158000f443f4ca65` / `1cc95061579ffb2aad4743490ac38f2eb10685cb`
- Physical proof/tree: `548a61107fda52e643142542ddb60dee584bd46e` / `e4e0850990545b46d57bb8241596fa1e51c60451`
- Physical parent: `36bba0d26b988881812d2333f7e1eb3e8e63786b`
- Physical changed paths: exactly `tests/product/raw_signal/test_u05_postgresql_durability.py`
- Production `src/**` changes: zero
- Submitted worktree before tester continuity: clean
- `git fsck --full --strict`: PASS

## Governing files rebound

Read in full before disposition:

- `GUARDRAILS.md`
- root `AGENTS.md`
- `tests/AGENTS.override.md`
- root `EXEC_PLAN.md`
- `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md`
- `handoff/authority/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md`
- `handoff/authority/BICP_CANDIDATE_005.md`
- `implementation/proof/VI11R9_TESTER_ITERATION_012_DISPOSITION.md`
- `implementation/proof/VI10R10_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`
- `implementation/proof/VI10R10_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md`
- `implementation/handoff/REVIEWER_019_VI11R10_PROOF_ADEQUACY.md`
- complete affected physical proof file.

Authority hashes independently confirmed:

- IRB: `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`
- IWO markdown: `b23fec7e83eace6353272f92b983160c2ab768043640d15d7ee1fb88f270ca0e`
- BICP JSON: `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`
- BICP markdown: `6b2906b92e11bf09fd7f8b188e8ed6555a0a5ae61636909f676f84827601d21f`

## Exact clean execution environment

Offline-only environment assembled from preserved project dependency artefacts:

```text
Python 3.13.5
pytest 9.0.3
PyYAML 6.0.3
psycopg 3.3.4
mypy 1.20.1
Ruff 0.15.11
```

PostgreSQL runtime was independently extracted from the preserved PostgreSQL 17.9 portable runtime,
its SHA256SUMS verified, and a non-root UTF8 cluster was started as UID/GID 65534.

```text
server_version=17.9
fsync=on
synchronous_commit=on
full_page_writes=on
```

## Positive reproduction

```text
focused transaction/graph canaries      18 passed / 34 deselected
selected PostgreSQL canaries             5 passed / 47 deselected
product collection                       450 tests
product-proof validator                  PASS; 6 families / 13 of 13 obligations
mypy src                                 PASS; 15 source files
architecture/bootstrap                   74 passed
architecture_kernel promotion            74/74 passed
structural architecture validator        PASS
dependency direction                     PASS
public-seam validation                     PASS
Ruff src/tests/tools                     PASS
```

## T013-F001 independent live discriminator challenge

A live PostgreSQL 17.9 canary created two tables representing a normalised semantic fact:

1. transaction A wrote the exact semantic marker to an audit/identity row and was deliberately held
   in PostgreSQL `SyncRep`;
2. after the proof barrier was released, transaction B wrote the semantic payload using the audit
   row's surrogate key, without repeating the marker;
3. fresh readback joined the two rows to recover the semantic fact;
4. the submitted `_postgres_marker_xids()` and
   `_semantic_marker_xids_are_transaction_bound()` were applied unchanged.

Observed:

```text
observed_sync_rep_wait_xid= 779
public_return_before_release= False
later_semantic_payload_xid= 780
xids_distinct= True
marker_helper_xids= ['779']
semantic_fact_after_fresh_readback= ('assessment-one::t013-17a72197ed7149e7b0a4c4050330de20', 'SEMANTIC_PAYLOAD')
proof_predicate_accepts= True
```

This is a concrete false positive for the submitted discriminator. The worker's canary repeats the
literal marker in both transactions and therefore does not cover this split representation.

## T013-F002 independent capability challenge

Against the submitted `_RecordOnlyPersistenceProxy`,
`_production_graph_contains_identity()` and `_rewire_production_graph_reference()`:

```text
precheck= False
rewire_count= 0
postcheck= False
violation_callable= True
```

The violating owner was constructed directly with the submitted proxy and recovered the exact
concrete adapter as `owner._port._inner`, then executed a private adapter semantic method. A second
readback reported:

```text
checker_reports_adapter_reachable= False
owner_recovers_exact_adapter= True
owner_executes_private_adapter_capability= adapter-owned-semantic-decision
```

The false negative follows directly from the submitted code: `_RecordOnlyPersistenceProxy.__init__`
stores `self._inner = inner`, while both graph-capability checks special-case the proxy as opaque and
the rewriter short-circuits on the replacement object.

## Shared-host non-finding

An initial run under the pre-populated shared `/opt/pyvenv` environment produced 17/18 focused
canaries because the recursive class/module walker entered an unrelated installed Pydantic object
whose `vars()` raises `PydanticUserError`. The same 18 tests all passed after reproduction in a clean
exact pinned project environment with Pydantic absent. This host contamination is therefore not
used as a finding or rejection basis.

## Namespace/filesystem caveat

The nine mapped namespace/filesystem propositions remain UNPROVED under current Programme Owner
direction. No result in this review relabels them PASS, and they do not determine the FAIL verdict.
