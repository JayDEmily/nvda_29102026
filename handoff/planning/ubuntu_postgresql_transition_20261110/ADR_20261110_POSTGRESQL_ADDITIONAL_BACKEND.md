# ADR — Additional PostgreSQL persistence profile for NVDA on Ubuntu

**ADR ID:** ADR-NVDA-20261110-PG-01  
**Date:** 10 November 2026 (Australia/Melbourne)  
**Status:** OWNER-ENDORSED ARCHITECTURAL DIRECTION; DOCUMENTED FOR REVIEW; NOT AN IMPLEMENTATION COMMISSION OR PRODUCT ACCEPTANCE.  
**Scope:** an additional, bounded M00 PostgreSQL persistence profile; preservation of the currently admitted SQLite profile; associated runtime and independent-proof boundaries.  
**Companion proposed plan:** [EXEC_PLAN.md](EXEC_PLAN.md). This ADR is not the active root `EXEC_PLAN.md`.

## 1. Problem and historical decision

On 18 October 2026 the owner accepted a **trusted-application SQLite profile** in place of mandatory PostgreSQL database-role isolation for that execution environment. The accepted amendment explicitly preserved M00 semantic contracts, separated owner-local stores, the historical PostgreSQL path and historical tests. It did **not** declare PostgreSQL fundamentally unsuitable. See `handoff/foundation_implementation/authority/SQLITE_PROFILE_OWNER_AMENDMENT_20261018.md` §§1–5 and `SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md` §§1, 4–6.

On 10 November 2026 the owner explained that the earlier exclusion was materially influenced by ChatGPT sandbox execution limitations and endorsed investigating PostgreSQL again now that Ubuntu WSL2 and GitHub are accessible. The owner separately directed creation of this ADR and an ExecPlan **before execution**. This present architectural direction does not grant acceptance of unreviewed implementation bytes, PostgreSQL tests or runtime results.

PostgreSQL MVCC permits concurrent readers and writers in distinct sessions, subject to row conflicts, isolation and transaction outcomes. SQLite has concurrent readers; WAL can overlap a reader with one writer, but only one writer at a time. In this repository the admitted SQLite M00 and M02 stores use rollback-journal `delete`, `busy_timeout=0` and `BEGIN IMMEDIATE`, rather than WAL. These are materially different concurrency profiles, not interchangeable drivers.

Primary technical references:
- PostgreSQL concurrency/isolation: https://www.postgresql.org/docs/current/mvcc.html and https://www.postgresql.org/docs/16/mvcc-intro.html
- SQLite WAL: https://www.sqlite.org/wal.html
- Psycopg 3 connection and asyncio model: https://www.psycopg.org/psycopg3/docs/advanced/async.html
- PostgreSQL supported versions: https://www.postgresql.org/support/versioning/

## 2. Observed repository and Ubuntu baseline (not proof of acceptance)

At published R2 planning commit `6feb50bf8a96e244cbd68eb57536f940be6335b3`:
- `pyproject.toml` pins Python `==3.12.14`, optional `postgres = ["psycopg[binary]==3.3.4"]` and development `psycopg==3.3.4`. **PostgreSQL driver dependency already exists.** A Python project file cannot install or pin the PostgreSQL *server*.
- `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py` provides a private M00 PostgreSQL persistence mechanism; `src/nvda_desk/composition/__init__.py:create_application` already accepts exactly one of `postgres_dsn` or `sqlite_path`; `config/architecture/dependency_rules.yaml` declares the narrow A00→M00 technical-constructor exception.
- `src/nvda_desk/derived_signal_calculation_truth/_postgres.py` is an M01-private mechanism. `config/architecture/modules.yaml` registers M01 `bootstrap`, not active/composable; it requires a separate schema/write role from M00.
- `src/nvda_desk/market_measurement_truth/_sqlite.py` and `_record_store.py` implement M02's current SQLite-specific durable state. No equivalent currently admitted M02 PostgreSQL backend has been established.
- `config/product_proof/claims.json` labels the original M00 PostgreSQL claim `HISTORICAL_NOT_RUNNABLE` for the SQLite candidate; the active SQLite M00 and M02 claims are separately identified. Original PostgreSQL tests remain retained, including `tests/product/raw_signal/test_u05_postgresql_durability.py`; their historical outcomes cannot be reclassified as current-green.
- `GUARDRAILS.md` is frozen; the existing commissioned R1 plan is at `execution/accepted-r1-20261030` commit `363923d47b81fca50e64036bef3c8601501e3c16`. GitHub R2 remains `PROPOSED_NOT_ACTIVE`; later local R2/G0 work and F02 repair still require independent reconciliation.

Direct Ubuntu read-only checks (10 November): WSL Ubuntu 26.04.1, available standalone CPython 3.13.5, no PostgreSQL server/CLI package detected, and `apt-cache policy postgresql-18` lists **candidate `18.6-0ubuntu0.26.04.1`**, not installed. This is a proposed *initial local test-server package pin*, not an installation, production server selection or evidence that legacy tests fixed to PostgreSQL 17.9 work unchanged. Existing Ubuntu Python 3.13.5 reports SQLite 3.49.1; the later local R2/G0 SQLite 3.54.1 path remains under independent review.

## 3. Decision and precise limits

**D1 — Preserve SQLite.** Retain accepted SQLite M00/M02 implementations, proofs and historical exact environments. Adding a separate backend does not invalidate valid SQLite proof, alter mathematical definitions or migrate existing stored files. No change to `GUARDRAILS.md` or historical Git objects.

**D2 — Qualify existing PostgreSQL for M00 first.** Preserve and inspect the existing M00 private adapter and A00 public constructor, then introduce/activate a *separately admitted* PostgreSQL M00 product profile only after exact authority, runtime, server, credentials/roles, source candidate and proof-generation bindings are established. PostgreSQL is a technical persistence mechanism and acquires no Raw Signal semantic ownership. M00 remains the sole writer of its own truth through its defined command/persistence boundary.

**D3 — No automatic downstream migration.** M01 remains `bootstrap` with its pre-existing private PostgreSQL schema/role model; no M01 activation, proof promotion, direct M00-table privilege or data migration is authorised. M02 remains on its admitted separate SQLite store. A PostgreSQL M02 backend or higher-throughput architecture requires a later exact domain/authority/proof decision, not extrapolation from M00 compatibility.

**D4 — State the concurrency claim narrowly.** The additional profile should demonstrably support at least two independent PostgreSQL client connections attempting lawful writes to distinct M00 occurrences while readers retrieve durable facts, without global one-writer SQLite-file locking. This is a finite functional concurrency proposition, not an unspecified throughput, latency, fairness or always-success promise. Conflicting writes/unique keys, isolation retries and deadlocks may wait or fail. Independently verify exact outcomes, immutable identities, public semantics, commit-before-success, rollback/non-fabrication, uncertain commits/reconciliation, multi-client readback and least-privilege roles. A session/cursor within one Psycopg connection is **not** independent execution; use separate transactions/connections.

**D5 — Async is a separate choice.** Current M00 PostgreSQL code uses synchronous `psycopg.connect()`. This decision neither promises nor mandates `AsyncConnection`, an event loop, connection pooling, ingestion scheduling or a live provider. A later demonstrated non-blocking caller requirement can justify a separate acceptance unit.

**D6 — Pin at the correct layers.** Keep the existing Python Psycopg `3.3.4` pin unless actual new-runtime incompatibility is shown; reconcile Python 3.13.5 metadata/wheels under the R2 environment authority. Provision and record an exact Ubuntu PostgreSQL **18.6** test-server build (`18.6-0ubuntu0.26.04.1` is the observed candidate), with repeatable package/source provenance and server `SHOW server_version` evidence. Installation/version admission comes in the proposed ExecPlan, not this ADR. Legacy `17.9`-specific proof is historical and requires explicit version-aware admission; do not edit expectations merely to obtain green.

**D7 — Keep independent testing and Git provenance.** CHAT_MANUAL means a separate independent Tester chat, not the Worker acting as its own tester. The owner-approved R2 design defers *new product executions* to L32, retaining contract and source review earlier, 39 leaves, 35 obligations, 27 mandatory D identities, 60 prospective signal cases plus up to 14 supporting, and D145 paused. A new M00 PostgreSQL proof allocation is a separately defined scope and **does not silently consume or increase those D-signal budgets**. GitHub's pinned commit can replace manual package transport only after a separate receiver independently verifies exact candidate, refs, tree/blob closure, non-Git evidence and full Git integrity under an owner-approved checkpoint strategy. No replacement is presumed from successful push alone.

## 4. Consequences and acceptance boundary

Benefits: an actual server-based persistence option for multi-client use, PostgreSQL MVCC concurrency, and re-use of substantial existing M00/M01 technical code without deleting SQLite history. Costs: server installation/maintenance, per-owner schema/role management, transaction-isolation and failure semantics, backup/recovery responsibilities, different physical schema and a separate proof generation. A local test server is not production deployment approval.

The unchanged semantic requirements include: preservation of native value types/opaque identities; source-event versus receipt-time distinctions; bounded capture policy; append-only assessment; idempotent identical-content retry versus same-ID conflict; exact actor/source lineage; actual transaction commit before acknowledged success; fresh-process, independent readback; no direct cross-owner SQL.

**Not decided or authorised here:** software installation, dependency changes, schema migration, M02 PostgreSQL conversion, product-test execution, Python asynchronous refactor, provider integration, R2 activation, F02 independent acceptance, new financial signal acceptance or main-branch promotion.

## 5. Dependencies and status

The historical 31 October independent reviewer found **F02**: a documented tracked `tools/with_pinned_sqlite.sh` helper absent from the reviewed R2/G0 Git candidate `9a4f1e827accdd7cfe3d7a14d5575573589b1acd`. A later Worker record attributes a repair to commit `16b7cc67f5d24336d3768e2da006819474a8c792`; its independent acceptance remains **UNKNOWN** until actual bytes and reviewer evidence are recovered and checked. This concern belongs to the R2/G0 transition, not a demonstrated PostgreSQL failure.

The separate prior Ubuntu L00 original-base plus successor restoration and object validation passed. This is Git transfer integrity for the older R1 candidate, not complete R2/F02 documentary acceptance or the separate fresh-chat receiver test.

**Adoption path:** independent documentary review of this ADR and companion proposed plan; recovery/acceptance of applicable R2/G0 state; exact owner acceptance of a successor root plan/claim authority; commissioned bounded environment and code work; independent product proof at authorised L32 boundary; final Git evidence. The planning branch itself creates no new active authority.

## 6. Evidence map

- `GUARDRAILS.md` blob `54a4407609941f63f6b902076688ff102a3d5ba2`
- `handoff/foundation_implementation/authority/SQLITE_PROFILE_OWNER_AMENDMENT_20261018.md`
- `handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md`
- `config/architecture/modules.yaml`; `config/architecture/dependency_rules.yaml`; `docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md`
- `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py`; `src/nvda_desk/derived_signal_calculation_truth/_postgres.py`; `src/nvda_desk/composition/__init__.py`; `src/nvda_desk/market_measurement_truth/_record_store.py`
- `config/product_proof/claims.json`; `config/product_proof/families.yaml`; `tests/product/raw_signal/test_u05_postgresql_durability.py`; `tests/product/raw_signal_sqlite/test_sqlite_durability.py`
- `execution/accepted-r1-20261030:EXEC_PLAN.md`; `planning/chat-manual-r2-20261030:EXEC_PLAN.md`; `handoff/planning/chat_manual_transition_20261030/TRANSITION_REVIEW.md`
- 31 October independent review `NVDA_R2_G0_L00_INDEPENDENT_GIT_REVIEW_20261031.md` (historical review evidence, not acceptance of later repair)
- This 10 November owner conversation: supplementary PostgreSQL direction and documentation-before-execution instruction.

**Documentary status:** decision recorded; review, active-plan admission and implementation remain separate.
