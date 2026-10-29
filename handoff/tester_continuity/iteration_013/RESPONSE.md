# Tester Iteration 013 — VI-11R10 Proof-Adequacy Audit

## Verdict

**FAIL / RETURN_TO_WORKER**

The verdict is **not based on the degraded-TCP / namespace environment**.

The worker materially strengthened both prior areas and the submitted focused canaries reproduce
cleanly in an exact Python 3.13.5 project environment. However, two independent Critical
false-positive paths remain. Both are continuations of the two Tester Iteration 012 findings; no
unrelated new proof category is introduced by this review.

VI-12R remains prohibited.

## Exact binding

- submitted archive SHA-256: `f67ef9c88c9b6470f46200815f5ac4b29505f3ce309a6a3ca482eeb6832280b3`
- submitted handoff HEAD: `2b17c3b545242475889b85aa158000f443f4ca65`
- submitted handoff tree: `1cc95061579ffb2aad4743490ac38f2eb10685cb`
- physical proof commit: `548a61107fda52e643142542ddb60dee584bd46e`
- physical proof tree: `e4e0850990545b46d57bb8241596fa1e51c60451`
- physical parent/handoff: `36bba0d26b988881812d2333f7e1eb3e8e63786b`
- preserved rejected Iteration 012 physical proof: `0917e031...` as recorded in current governing evidence
- physical commit changes exactly one path: `tests/product/raw_signal/test_u05_postgresql_durability.py`
- production-source changes in the physical commit: none

## Iteration 012 finding status

- `T012-F001`: **PARTIALLY CLOSED**
- `T012-F002`: **PARTIALLY CLOSED**

The READY/GO owner-construction ordering, backend-XID capture, literal-marker/XID check,
record-only injection construction and weak-reference detection are real improvements. They do not
yet make the proof discriminative against the two cases below.

## T013-F001 — CRITICAL — Literal-marker XID correlation can bind SyncRep to an audit/identity transaction while semantic state is committed separately

**Continuation of:** `T012-F001`

**Violated authority:** IRB BC-011/BC-015; IA22R01-PROD-009; IWO-U05 durability boundary.

**Physical proof location:**

- `tests/product/raw_signal/test_u05_postgresql_durability.py:967-999`
- `tests/product/raw_signal/test_u05_postgresql_durability.py:1225-1261`
- `tests/product/raw_signal/test_u05_postgresql_durability.py:1380-1507`

**Concrete wrong implementation that can pass:**

After the proof-owned `GO`, transaction A writes an audit/identity row containing the exact expected
semantic marker and reaches PostgreSQL `SyncRep`. The proof records transaction A's `backend_xid`
and releases the barrier. Transaction B then writes the actual semantic payload using a surrogate
or foreign-key reference to transaction A's row, without repeating the literal marker. Fresh
readback can reconstruct the expected semantic record from A+B. `_postgres_marker_xids()` searches
only rows whose `row_to_json(...)` text contains the literal marker, so it sees only transaction A.
The predicate therefore accepts transaction A as the semantic durability transaction even though
the semantic payload was committed by transaction B.

**Independent live PostgreSQL 17.9 canary:**

```text
observed_sync_rep_wait_xid= 779
public_return_before_release= False
later_semantic_payload_xid= 780
xids_distinct= True
marker_helper_xids= ['779']
semantic_fact_after_fresh_readback= ('assessment-one::t013-17a72197ed7149e7b0a4c4050330de20', 'SEMANTIC_PAYLOAD')
proof_predicate_accepts= True
```

The worker's own two-commit canary puts the same literal marker in both the audit and semantic rows,
so it correctly detects two XIDs for that representation but does not challenge a normalised/split
representation in which only the audit/identity row carries the marker.

**Why this matters:** the proof is intended to establish that the transaction whose server-side
acknowledgement gates public success is the transaction making the semantic record durable. A text
search for the semantic marker is not a structural identity for every physical row or transaction
that may constitute that semantic record.

**Smallest owning-layer repair:** bind the observed transaction identity at the actual semantic
persistence operation rather than inferring it from post-hoc marker-text search. The proof must
establish that all writes constituting the semantic append occur in the same transaction whose XID
was observed in `SyncRep`. Add an implementation-independent adversarial canary in which only the
audit/identity row contains the marker and the semantic payload is joined by a surrogate; that case
must be rejected.

## T013-F002 — CRITICAL — The injected “record-only” proxy itself exposes the concrete adapter capability

**Continuation of:** `T012-F002`

**Violated authority:** IRB BC-001/BC-013/BC-015; IA17-PROD-001/IA17-PROD-011; IWO persistence
ownership boundary.

**Physical proof location:**

- `tests/product/raw_signal/test_u05_postgresql_durability.py:1946-1994`
- `tests/product/raw_signal/test_u05_postgresql_durability.py:2039-2045`
- `tests/product/raw_signal/test_u05_postgresql_durability.py:2115-2119`
- `tests/product/raw_signal/test_u05_postgresql_durability.py:2246-2271`
- `tests/product/raw_signal/test_u05_postgresql_durability.py:2675-2695`

**Concrete wrong implementation that can pass:** the semantic owner is constructed with the new
`_RecordOnlyPersistenceProxy`, but that proxy stores the real concrete adapter as ordinary attribute
`self._inner`. A violating owner can therefore execute, for example,
`self._port._inner._semantic_decision(...)`. The graph checker deliberately treats every
`_RecordOnlyPersistenceProxy` as opaque and the rewriter short-circuits when it encounters the
replacement object, so this recoverable concrete capability is reported absent.

**Independent exact-runtime canary:**

```text
precheck= False
rewire_count= 0
postcheck= False
violation_callable= True
```

A second direct readback established:

```text
checker_reports_adapter_reachable= False
owner_recovers_exact_adapter= True
owner_executes_private_adapter_capability= adapter-owned-semantic-decision
```

This means the statement that the newly constructed semantic owner “never receives the concrete
adapter” is not true at the capability boundary: it receives an object from which the exact
concrete adapter is directly recoverable.

**Smallest owning-layer repair:** do not inject a wrapper that contains a recoverable concrete
adapter. Use a genuinely record-only persistence capability whose reachable state does not contain
the concrete adapter at all (for example a proof-owned record-only PostgreSQL implementation over
the same durable state), or another structural boundary that makes the concrete adapter capability
unavailable to the semantic owner. Add a canary that attempts recovery through the injected port
itself; the proof must fail if any concrete/private adapter capability is recoverable.

## Independent positive verification

From the exact submitted bytes/current Git repository:

- archive SHA-256 independently computed as above;
- submitted worktree clean before tester continuity was added;
- `git fsck --full --strict`: PASS;
- exact submitted HEAD/tree and physical proof commit/tree match the worker handoff;
- physical proof parent is exactly `36bba0d26b988881812d2333f7e1eb3e8e63786b`;
- physical proof changes one test path and zero `src/**` production files;
- product-proof validator: PASS, 6 physical families / 13 of 13 required obligations;
- independent product collection: **450 tests**;
- exact clean runtime: Python 3.13.5, pytest 9.0.3, PyYAML 6.0.3, psycopg 3.3.4,
  mypy 1.20.1, Ruff 0.15.11;
- submitted focused transaction/graph canaries: **18 passed / 34 deselected** in that clean exact
  runtime;
- live PostgreSQL runtime: PostgreSQL 17.9, `fsync=on`, `synchronous_commit=on`,
  `full_page_writes=on`;
- selected worker PostgreSQL canaries including SyncRep barrier, READY/GO handshake and the submitted
  two-XID marker canary: **5 passed / 47 deselected** in the exact clean runtime;
- `python -m mypy src`: PASS, no issues in 15 source files;
- architecture/bootstrap: **74 passed**;
- `architecture_kernel` promotion: **74/74 passed**;
- structural architecture, dependency and public-seam validators: PASS;
- Ruff over `src tests tools`: PASS.

A shared host Python environment initially exposed one unrelated Pydantic traversal exception in the
broad graph helper. Reproduction in a clean environment containing the project's exact pinned
runtime/test dependencies produced the worker's claimed 18/18 focused result, so that host pollution
is **not** used as a finding or rejection basis.

## Environmental caveat disposition

Per current Programme Owner direction, the nine mapped namespace/filesystem propositions remain
**UNPROVED**. They are not counted as passing and they are not used as a rejection basis. The
PostgreSQL executions above establish the database-backed canaries only; they do not relabel those
nine propositions.

## Disposition

Return only to the proof layer. Preserve this failed physical proof in ordinary Git history. Do not
change IRB/BICP/IWO/METHOD-006 meaning and do not begin VI-12R.

Repair `T013-F001` and `T013-F002` and return a genuinely new proof state for Tester Iteration 014.
