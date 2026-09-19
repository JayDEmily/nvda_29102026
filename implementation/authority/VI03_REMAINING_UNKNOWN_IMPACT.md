# VI-03 — Remaining-Unknown / execution-prerequisite impact map

## Verdict

**VI-03 identified BLOCKING_UNKNOWN items; VI-04 current programme authority now closes the implementation-required set recorded below.**

The exact accepted IRB allows most BC-016 Unknowns to remain unresolved because this tranche can avoid claiming or implementing those capabilities. It does not allow the physical PostgreSQL realisation needed for BC-011 / IA22R01-PROD-009 / VI-14 to be selected by implementation convenience.

The semantic-authority blockers for the terminal path are the required physical PostgreSQL realisation and the final owner-package name required for truthful active-module admission. Final distribution/version metadata remains a later packaging blocker. The previously reported PostgreSQL execution-capability blocker is **retracted**: a real PostgreSQL 17.9 server and Psycopg 3.3.4 client have now been built/run end-to-end from preserved project artefacts outside the repository. That technical availability does not select either version or mechanism as current product authority.

This map makes no authority decision and selects no value. It was re-opened after the user directed inspection of the frozen pre-reset skeleton architecture and its `pyproject.toml`; that evidence narrows the available choices but does not itself select a current PostgreSQL realisation.

## Governing rule

BC-013 and BC-016 require implementation to stop rather than choose a Remaining Unknown. IA-16 repeats that physical PostgreSQL layout/types/indexes/partitions/pooling/driver are non-free Unknowns if implementation requires them. Candidate 005 preserves the same stop rule.

The terminal successor plan requires real PostgreSQL transaction/readback/failure/restart evidence. Therefore the subset of physical PostgreSQL choices necessary to instantiate that proof cannot remain unresolved through VI-14/VI-15.

## Exact impact map

| Remaining Unknown | VI-03 classification | First dependent leaf | Evidence-backed reason |
|---|---|---|---|
| concrete scope contents / provider eligibility / record mappings | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-003 leaves concrete mappings Unknown. The bounded owner can accept configured policy/mapping authority as input; N15 proof may use explicit controlled fixtures without claiming a real provider mapping. No provider integration is authorised. |
| provider revision / retransmission equivalence | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-010 requires a newly received retransmission to remain a new observation absent separately admitted equivalence. No equivalence algorithm is needed to implement that conservative rule. |
| clock accuracy / drift / leap / smear / wake latency | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-004 fixes nominal slot truth and explicitly forbids treating wake time as schedule truth. No live-clock accuracy claim is required by the bounded proof. |
| finality / watermarks / exact counts / member queries | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-007/008 explicitly prohibit these stronger meanings. Proof must show they are not inferred. |
| provider duplicate equivalence / exactly-once | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-010 explicitly requires no such inference. Retry/conflict law is independently implementable. |
| pre-commit raw loss / bounded recovery | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-011 explicitly promises no bounded recovery or recovery of pre-commit raw loss. |
| availability / latency / throughput / RTO / RPO | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-011/016 expressly leave these outside and no terminal proof claims them. |
| opaque-ID generation / collision handling / cross-process recovery | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | The bounded semantics require typed opaque occurrence identities and retry/conflict handling, but do not require this tranche to select a production ID-generation algorithm or collision/recovery guarantee. The implementation can preserve owner control by accepting/injecting an opaque-ID source at a technical boundary while tests use controlled IDs. No operational ID-generator fitness claim is made. |
| physical PostgreSQL table/layout design | `BLOCKING_UNKNOWN` | VI-10 / VI-12R / VI-14 | BC-011 requires separate append-oriented logical PostgreSQL representations and real transaction/readback/restart evidence. A real adapter cannot exercise those claims without some physical relation/layout design. IA-16 says this choice is not implementation freedom. |
| SQL/database types for the required PostgreSQL representation | `BLOCKING_UNKNOWN` | VI-10 / VI-12R / VI-14 | Real PostgreSQL persistence must encode the required identity/time/native/assessment facts. Selecting physical SQL/database types is explicitly BC-013/016 Unknown and is required for real execution. |
| PostgreSQL indexes | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | No performance/SLA/query-plan claim is admitted. A minimal correctness proof need not create indexes beyond any database-intrinsic constraint mechanism separately authorised by the physical layout decision. |
| PostgreSQL partitions | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | No scale/retention/performance partitioning claim is admitted. |
| PostgreSQL connection pooling | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | No concurrency/throughput/pooling requirement is admitted. A correctness proof may use direct connections once a driver is authorised. |
| PostgreSQL driver selection | `BLOCKING_UNKNOWN` | VI-10 / VI-12R / VI-14 | A Python implementation and real PostgreSQL proof require an actual transport/driver mechanism or separately authorised equivalent. BC-013/016 explicitly names driver selection as Remaining Unknown. |
| concrete repository/store form where dependent on physical design | `BLOCKING_UNKNOWN` | VI-12R / VI-14 | IA-16 explicitly leaves this non-free where it depends on unresolved physical design. The semantic port is fixed; its concrete PostgreSQL implementation is not. |
| retention / deletion / deterministic recomputation / P01 | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-011/016 explicitly exclude these claims. Referential readback is required only for the slice non-deletion lifetime; no duration/deletion/recompute/P01 behaviour is selected. |
| provider adapters | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-013 excludes provider/API selection/networking. A00 composition proof may use controlled source-ingress fixtures without claiming a real provider adapter. |
| validation / quarantine | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-009/013 explicitly do not define provider bad-tick/duplicate/quarantine validity. |
| D001+ | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-005/013 exclude D001+ derivation and raw `event_ts_utc`. |
| downstream consumers / behaviour | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-001 and BICP admit A00 only; no downstream business consumer is authorised. |
| historical-M re-establishment detail | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | Current kernel allocation is post-reset; historical M16/pre-reset identities are not current lineage endpoints. |
| final package naming / version metadata | `BLOCKING_UNKNOWN` | VI-04 authority closure; package name is consumed by VI-07/VI-08, final distribution/version claim by VI-15 | Candidate 005 preserves final package naming/version metadata as non-free. Although the schema can mechanically represent a `placeholder` M row without package/seam metadata, the accepted VI-07 plan requires the exact admission mutation to include public-seam/package metadata and expressly forbids a fake placeholder used merely to split branches. Current runtime-module admission law and the module template create the owner package/public seam before proof/composition, and an `active` executable M requires both to exist physically. Therefore the owner package name is required for truthful VI-07/VI-08 admission. Distribution/version metadata is not required by the module registry itself and may remain unresolved until the VI-15 packaging claim. The create-intent responsibility name is explicitly not a package/public-seam name, so `raw_signal_occurrence_truth` cannot be silently reused as the package name. |
| provider/collector-specific ingestion-sequence scope / overflow | `NOT_REQUIRED_FOR_THIS_TRANCHE` | none | BC-005/016 fix only typed local scope and no-global-order inference. Controlled ingress may provide sequence/scope values; no provider-specific overflow policy is claimed. |


## Frozen skeleton / packaging evidence re-check

The user explicitly directed VI-03 back to the frozen skeleton architecture and `pyproject.toml`. The exact preserved 2026-08-04 full-history reset archive was inspected rather than relying on prior summaries.

### What the frozen architecture actually fixes

The formally accepted pre-reset architecture decision records:

- one governed modular monolith with explicit internal ports;
- storage adapters as explicit volatility/extension points;
- module-owned repository ports rather than persistence ownership leakage;
- progressive target packages under the historical convention `src/nvda_desk/mxx_module_name/`;
- for the persistence tangle specifically: `M13 atomic UnitOfWork/idempotency; module-owned repository ports; durable adapter selected later`.

The linked working architecture says the declared dependency set supported SQLAlchemy and PostgreSQL-capable drivers, but explicitly qualifies that as **present technical direction, not a production database decision**. It also requires persistence technology not to leak into domain algorithms.

Those statements support the current M-owner persistence-port / non-owning-adapter architecture. They do **not** select a physical PostgreSQL table layout, SQL type mapping, driver, or durable adapter implementation.

### What the preserved pre-reset `pyproject.toml` proves

At reset base commit `d24f9626a23b526384668b3cb26ee811b235eb5c`, `pyproject.toml` declared all of:

- `asyncpg==0.31.0`;
- `psycopg[binary]==3.3.3`;
- `SQLAlchemy==2.0.48`;
- plus unrelated production dependencies.

The architecture reset then deliberately deleted that production `pyproject.toml` and regenerated the behaviour-neutral kernel packaging surface. Current `pyproject.toml` now declares:

- distribution `nvda-architecture-kernel==0.1.0`;
- package root `src/nvda_desk`;
- sole runtime dependency `PyYAML==6.0.3`;
- offline dependency resolution from `vendor/wheels`.

Therefore the historical package metadata establishes known prior technical options and versions, not one uniquely selected current PostgreSQL driver. The current package metadata establishes the existing distribution/build boundary, not final Raw Signal owner-package naming authority.

### Consequences for this tranche

1. The previous statement that the absence of a PostgreSQL driver from the current kernel `pyproject.toml` itself evidenced a missing design decision was incomplete. Its absence is expected because the frozen behaviour-neutral kernel intentionally stripped unadmitted production dependencies.
2. `tests/bootstrap/test_legacy_exclusion.py` proves AK-PKG-002 for the behaviour-neutral kernel state: old/unadmitted runtime dependencies must not enter merely from history. It is not a permanent architectural ban on an explicitly admitted future production dependency.
3. Adding a PostgreSQL dependency later would therefore require exact current admission and corresponding proof-scope repair; the current exclusion test cannot be weakened merely for green, but its proposition must be re-evaluated against the newly admitted implementation state.
4. Historical presence of `asyncpg`, `psycopg[binary]` and SQLAlchemy does not resolve the BICP driver Unknown because more than one PostgreSQL-capable path was present and the frozen architecture expressly declined to make a production database decision.
5. Final owner-package naming is required before VI-07/VI-08 can perform the truthful active-module admission contemplated by the accepted plan. The schema's ability to represent a `placeholder` does not authorise using a placeholder as an artificial staging state: the plan expressly forbids that manoeuvre, while current extension law and the module template place package/public-seam creation in the runtime-module admission path. The historical `mxx_module_name` pattern narrows physical form but does not select the final package name. Final distribution/version metadata is a separate later dependency of VI-15 and remains unresolved until current authority closes it.

## Full-history physical-design check

The preserved pre-reset architecture full history and the later R2 clean-rebuild history were searched for PostgreSQL/Raw Signal DDL and driver/store implementation evidence. The pre-reset history does contain `CREATE TABLE` changes, but the inspected hits are legacy SQLite/state-kernel or other unrelated persistence implementations. The R2 Raw Signal material is a quarantined candidate authority surface; its history contains no Raw Signal `CREATE TABLE` commit and its own text keeps physical table/index/partition/pooling decisions subordinate/deferred.

Therefore no inspected frozen/current-authority evidence supplies a current Raw Signal PostgreSQL DDL/type/store decision. The historical package `nvda_desk.raw_signal_persistence` and its public API are likewise quarantined candidate evidence rather than current package authority.

## Physical PostgreSQL authority gap

The smallest presently identified semantic-authority gap is limited to the concrete mechanism necessary to discharge BC-011:

1. physical PostgreSQL relation/table layout sufficient for policy/capture, assessment and raw-observation append-oriented durability and referential reads;
2. SQL/database types needed by that layout;
3. PostgreSQL driver/mechanism selection for the Python adapter;
4. concrete repository/store realisation only to the extent it is determined by 1–3.

Indexes, partitions and pooling are not required by the current bounded correctness claim and therefore remain unresolved rather than being selected pre-emptively.

A lawful VI-04 resolution may either specify these choices directly or explicitly delegate selection of the **smallest correctness-only physical PostgreSQL realisation** to the implementation worker. Such delegation must itself be current human/programme authority and must not grant semantic authority to PostgreSQL/schema/driver choices.

## Current execution-capability observation

This is separate from semantic authority. The earlier VI-03 observation based only on pre-installed PATH/import state is superseded by an end-to-end preserved-artefact test recorded in `implementation/authority/VI03_POSTGRES_EXECUTION_CAPABILITY.md`.

**VERIFIED:** the current environment can build and run a real PostgreSQL 17.9 server from the preserved source archive and can connect to that server with the preserved Psycopg 3.3.4 binary wheel pair. A fresh isolated non-root cluster was started with PostgreSQL defaults reporting `fsync=on`, `synchronous_commit=on` and `full_page_writes=on`; both `psql` and Psycopg connected successfully; the server then stopped cleanly.

This closes the execution-capability question only. It does **not** make PostgreSQL 17.9 or Psycopg 3.3.4 current implementation authority. In particular, the 2026-08-07 Psycopg requirements pack is strong historical evidence of a prior intended/approved dependency, but the later accepted BICP expressly carries driver selection forward as a Remaining Unknown and therefore governs the current tranche.

Later VI-10/VI-14 proof may use this preserved-material route only after VI-04 establishes the exact authorised mechanism/dependency.

## Stop disposition

VI-03 itself is complete when this map is committed and validated. Downstream work that depends on physical PostgreSQL realisation is **BLOCKED** until VI-04 supplies explicit authority for the required physical choices.

The current plan does not permit the implementation worker to choose them merely because the user delegated routine continuation. VI-04 must also close the owner-package-name authority gap before VI-07/VI-08; final distribution/version metadata may remain deferred until its VI-15 dependency is reached.


## VI-04 authority closure

Current human/programme authority on 2026-09-19 is recorded in `implementation/authority/VI04_AUTHORITY_CLOSURE.md`. It authorises:

- owner package `nvda_desk.raw_signal_occurrence_truth`;
- public seam `nvda_desk.raw_signal_occurrence_truth.api`;
- PostgreSQL driver `psycopg[binary]==3.3.4`;
- bounded worker selection of the smallest correctness-only PostgreSQL relation layout, SQL types and dependent direct repository/adapter form necessary for BC-011;
- PostgreSQL 17.9 as the recorded proof environment, without making it a production-version requirement.

It expressly leaves partitioning, pooling, performance/SLA policy and final distribution/version metadata unresolved, except that database-intrinsic correctness constraints may be used where required to enforce the authorised semantic invariants.

Accordingly, the VI-03 `BLOCKING_UNKNOWN` set no longer blocks VI-05 onward. Final distribution/version metadata remains deferred to its VI-15 dependency and must be closed there before packaging.
