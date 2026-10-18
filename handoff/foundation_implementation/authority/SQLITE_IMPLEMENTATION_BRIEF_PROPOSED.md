# NVDA V2 — SQLite implementation-ready brief, version 3

Date: 18 October 2026 — Australia/Melbourne.

**PROPOSED_EXACT_IMPLEMENTATION_PACKAGE; NOT_ACCEPTED_FOR_IMPLEMENTATION.** The SQLite trusted-application direction is already accepted. This file fixes its physical implementation and proof scope for the required exact-byte review. It does not inherit the version-2 native binding or authorise code/test execution by being written. The root ExecPlan remains the single plan.

## 1. Incorporated meaning and projection

The exact incorporated-byte table at the end is part of this brief. Read the preserved version-2 foundation brief in full. Its §§1–6 and AnnexesB/C supply the D011 public contract, equation, exact controlled instance, selection, serialization and identity behaviour unchanged except for the explicit storage/exception changes in §3 below. Its full126 target, 83 downstream outputs/26 peers, effective mathematical overlays, 36 work receivers/54 inherited obligations/eight holds remain. No native IBKR mapping is admitted. Owner namespace remains `neutral_market_measurement_truth/v1`; new occurrences bind this newly accepted brief's digest, never the old digest by substitution.

M00 meaning comes from all sixteen BC clauses in the incorporated IRB, under current M00 identity and the accepted SQLite amendment. Only PostgreSQL mechanism/OS-role prescriptions are replaced. Policy, half-open slots, native logical records, three temporal kinds, receipt relation, append-only three-state assessment, identity/retry, public ownership and compatibility meanings are unchanged. All authority unknowns outside this bounded physical storage choice remain unknown.

Projection intents for a future accepted native binding are exactly `create M neutral_market_measurement_truth`, `modify M00`, `modify G01`, and **`modify A00`**. M00 now includes the bounded SQLite adapter, public persistence-failure exception and its reader-consumer declaration. A00 is explicitly included because production construction changes; it is not inferred from a storage dependency. G01 covers the incorporated claim/admission change. No numeric create ID is supplied. Existing M01 production code/ownership is not modified.

Original version2, PA-02 proposals, original M00 proof/config/tests, the earlier binding and all Git history remain recoverable and unchanged in this document pass. A new binding must identify this exact file's raw SHA256 and genuine acceptance of these physical choices, including A00 scope. It may not retain an old acceptance reference beside an unaccepted new digest.

## 2. Supported profile and resource contract

One trusted application; one local regular SQLite file per semantic owner; no ATTACH, cross-owner SQL, shared-cache/in-memory durable substitute or separate semantic storage service. These rules constrain conforming application code. They do not claim protection against arbitrary same-process or same-OS-identity file access. Separate files/reader facets are not database roles. No non-root UID, chroot, mount/PID/network namespace, server daemon or PostgreSQL installation is a prerequisite for this profile.

Candidate proof environment: CPython3.12.14, SQLite3.53.1 as the observed proof-engine version; pytest9.0.3, mypy1.20.1, Ruff0.15.11, PyYAML6.0.3 and hatchling1.29.0. SQLite3.53.1 is a recorded proof environment, not a general production-version mandate. STRICT tables require engine3.37.0 or later; the exact admitted proof environment must also provide foreign-key enforcement and synchronisation features. No engine/version support claim follows before actual checks. Psycopg is not required for this profile; retain it only as optional `postgres` extra at3.3.4 for explicitly selected historical construction. No unconditional Psycopg import may prevent SQLite construction or component tests.

Change `pyproject.toml` Python requirement to `==3.12.14`, Ruff target to `py312`, mypy target to`3.12` only in the later authorised environment unit. Retain the other pins above unless a separately identified incompatibility requires a new decision. Supply CPython-3.12-compatible mypy/librt and other binary wheels, PyYAML, hatchling and complete transitive build/runtime/dev dependencies in a hash-recorded offline bundle. The existing cp313 wheels are not reused as cp312 wheels. A clean isolated install must succeed under the actual pin; changing metadata or parsing source is not compatibility proof. No blind `uv --no-config` install counts as reproducible bundle acceptance.

Retained PostgreSQL source remains in full-project static-check scope. Include pure `psycopg==3.3.4` in the development/typechecking dependency set so its imports can be resolved without a server; `psycopg[binary]==3.3.4` remains only the explicit optional postgres runtime extra. Do not suppress missing-import errors or exclude retained modules to manufacture typecheck success. SQLite runtime construction must still succeed in a clean runtime-only environment without either Psycopg distribution. This separates optional development source coverage from the SQLite application's actual server/runtime requirements.

Storage paths are exact non-empty absolute string paths to local regular files. Reject `:memory:`, URI/query input, relative path, symlink/non-regular targets and non-existent parent directories. Resolve canonical paths at construction; runtime configuration supplies paths, never selects owner meaning. Existing file identity/schema must match. No network-filesystem support is claimed. No actual legacy file is opened, overwritten or migrated by proof.

Writer creation requires explicit `create=True` and a previously absent file; create exclusively and initialise within a single schema transaction. Existing or empty pre-existing files with `create=True` fail without truncation. Normal writers/readers use SQLite URI internally with properly encoded canonical path and `mode=rw`/`mode=ro` respectively, `uri=True`; never `immutable=1` for a changing store. A normal writer must not silently recreate a missing store. SQLite files and transient journals are the only semantic persistence for this profile.

## 3. Exact interface changes

Foundation: every version-2 public dataclass/Protocol/signature remains exact except the following intentional replacements. Remove the unimplemented pilot PostgreSQL storage constructors from this profile, preserving their old specification in Git:

```python
@dataclass(frozen=True, slots=True)
class SQLiteStorageV1:
    database_path: str
    create: bool

@dataclass(frozen=True, slots=True)
class SQLiteReadStorageV1:
    database_path: str
```

`create_owner` retains all version-2 named parameters/return type; only `storage` becomes `MemoryStorageV1 | SQLiteStorageV1`. `create_reader(*, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1) -> MeasurementReadsV1` is exact. Storage dataclasses have no defaults/extra fields; `create` is exact bool. Memory is explicit component proof only, never production fallback.

Each owner's `api.py` exports its own `PersistenceFailureV1(RuntimeError)` with signature `__init__(self, message: str, *, outcome_uncertain: bool = False) -> None` and readable `outcome_uncertain: bool`. M00 adds this exception without changing any v1 record field or existing public command/read signature. Foundation uses its declared owner-local exception. Wrong configuration type/content retains the existing TypeError/ValueError distinction; missing/corrupt/unavailable storage and transaction failure raise the relevant persistence exception. An ordinary unavailable-input result is never used for a storage failure.

M00 private technical constructor: `create_sqlite_persistence(database_path: str, *, create: bool = False) -> _PersistencePort` in owner-local `_sqlite.py`, consuming the existing private transaction protocol unchanged. Its only public port callable is `transaction(write: bool)` under that protocol. It stores owner-decided records and does not decide schedule, eligibility, assessment outcome or relation semantics. Existing record-only proxy/adapter-capability separation remains a proposition about conforming owner composition; it is not OS security.

A00 `create_application` retains existing keyword parameters and return type and adds `sqlite_path: str | None = None`. Exactly one of nonempty `sqlite_path` or `postgres_dsn` is required for production. The existing owner-factory-only path is still proof-only and cannot be combined with either store. Both stores, neither store without the proof factory, malformed paths/DSNs, or factory plus store raise TypeError/ValueError as appropriate. SQLite construction calls `create_sqlite_persistence(sqlite_path, create=False)` then public M00 `create_owner(durability_port=...)`. A00 does not initialise a missing database or compute domain outcomes. PostgreSQL import is lazy on its explicitly selected path. The technical-seam exception in `config/architecture/dependency_rules.yaml` adds only `nvda_desk.raw_signal_occurrence_truth._sqlite.create_sqlite_persistence` for A00→M00, retaining the existing exception. No broad private-import wildcard. The underlying M00→A00 edge remains prohibited.

## 4. Connections, transactions and committed-success law

Use stdlib `sqlite3`, explicit SQL transactions with implicit transaction management disabled (`isolation_level=None`), no global shared connection and no callbacks implementing domain decisions. Connection setup outside a transaction must read back `foreign_keys=1`, `journal_mode=delete`, `synchronous=3` (EXTRA), and `busy_timeout=0`. Set those values on writer connections and reject unsupported/mismatched settings. Reader connections use `mode=ro`, `query_only=1`, foreign keys on and busy timeout0; validate file ID/version/journal policy without attempting schema/configuration writes. A reader may report a hot-journal recovery/open failure; it must not silently reopen writable.

Write operations use `BEGIN IMMEDIATE`; read operations use `BEGIN` for a consistent own-operation snapshot. Keep transactions on one connection. Successful context exit issues COMMIT and returns success only afterwards; exceptions roll back an open transaction. No per-file automatic retries, background work or latency/SLA promise. SQLITE_BUSY/LOCKED is an explicit unachieved operation unless commit outcome is uncertain, not missing market data. Concurrent identical callers may observe contention; retrying the same logical operation after the competing commit returns the one committed record. Differing content under the same immutable identity refuses.

On an error before COMMIT, after confirmed rollback, raise `PersistenceFailureV1(..., outcome_uncertain=False)`. If the attempt to commit may have completed but acknowledgement is unavailable, use `outcome_uncertain=True`; never assert rollback/absence without evidence. Resolve by exact identity read/idempotent retry, preserving original calculation time. No valid occurrence is returned while outcome remains uncertain.

M00 retains each command's own transaction. Restart reconciliation commits a newly owed capture before its separate unknown assessment; failure of assessment must not roll back an already committed capture. No cross-kind/whole-graph/cross-owner atomicity, replay equivalence, RTO/RPO, retention/deletion or recovery deadline is introduced. Foundation configuration registration is one atomic transaction; an occurrence append plus full immutable reference validation is one transaction. Definitions/configuration without a result do not mean a successful calculation.

Committed SQL transaction evidence remains conditional on the filesystem/VFS behaving correctly. A sandbox file does not promise survival of workspace deletion or an always-on production service. Proof uses SQLite backup API to make a consistent clone into another disposable path; no live database is copied by uncoordinated file copying. Actual operational snapshot/restore policy remains separately scoped.

## 5. Exact physical data and lossless encoding

Use STRICT tables. `PRAGMA application_id` identifies raw store as hexadecimal`0x4e560001`, foundation as`0x4e560002`; `user_version=1`. Check both before serving any existing store. Wrong owner/version, invalid payload hash or inconsistent keys/indexes fails closed; there is no opportunistic repair/migration. No metadata table acquires semantic authority.

Every table below has `payload BLOB NOT NULL` containing complete typed content and `content_sha256 TEXT NOT NULL` containing its lowercase64hex digest. Primary-key columns are explicitly NOT NULL. Optional semantic absence uses SQL NULL only in declared optional index columns and remains explicit in the full payload. Foreign keys use default NO ACTION; no cascade deletion. Create no UPDATE/DELETE production method; add BEFORE UPDATE/DELETE abort triggers on semantic tables, while explicitly treating them as accidental-mutation safeguards, not hostile-code protection.

M00 has exactly four semantic tables, retaining these existing names and keys:

| Table | Additional exact columns/constraints |
| --- | --- |
| `rsot_capture_scope_policy_v1` | `scope_policy_id TEXT`, `scope_policy_version TEXT`, `scope_policy_ref TEXT UNIQUE`, `activation_ts_utc TEXT`, nullable`deactivation_ts_utc TEXT`, `eligibility_policy_ref TEXT`; primary key(id,version); deactivation, when present, lexically later than activation. |
| `rsot_scheduled_capture_occurrence_v1` | `capture_occurrence_id TEXT PRIMARY KEY`, `scope_policy_ref TEXT` foreign key to policy ref, `slot_start_utc TEXT`, `slot_end_utc TEXT`; UNIQUE(policy ref,slot start). |
| `rsot_raw_observation_occurrence_v1` | `observation_occurrence_id TEXT PRIMARY KEY`, `received_ts_utc TEXT`, `ingestion_sequence_scope TEXT`, `ingestion_sequence TEXT`, `ingestion_sort_key BLOB`; no invented capture foreign key. |
| `rsot_capture_receipt_presence_assessment_v1` | `assessment_occurrence_id TEXT PRIMARY KEY`, `capture_occurrence_ref TEXT` foreign key to capture, `outcome TEXT` CHECK the exact three accepted literals, `evidence_as_of_ts_utc TEXT`, nullable UNIQUE`supersedes_assessment_ref TEXT` self foreign key. Unique partial index on capture ref where predecessor IS NULL. |

All non-nullable columns above are NOT NULL. M00 retains the accepted complete v1 record in each payload, not just the listed search fields. Same-capture/immediate-predecessor/eligibility/high-water decisions remain owner-side under the existing transaction port and serialized write transaction; do not transfer those decisions into SQL triggers. No relation-membership table is introduced.

M00 payload encoding: ASCII-safe UTF-8 canonical JSON using sorted keys, separators `(',',':')`, all declared dataclass fields by name including optional nulls. Typed opaque IDs encode `{kind:<public factory name>,value:<exact .value>}` and decode only through that public factory. UTC metadata instants use fixed-width`YYYY-MM-DDTHH:MM:SS.ffffffZ` for year0001–9999; native source strings are not normalized. Integer metadata uses tagged exact signed decimal text. The native_record alone uses the existing `NVDA-NATIVE-V1\0` binary algorithm, encoded as lowercasehex in this JSON. Extract that codec to owner-local `_native_codec.py` without changing its tags/bytes or importing Psycopg: it preserves bool/int distinctions, arbitrary integers, float IEEE bits including signed zero/nonfinite values, Decimal tuple including permitted nonfinite forms, str/bytes/list/tuple/mapping and provider null. Raw native nonfinite data is not newly rejected because the D011 projected Decimal domain is finite.

For raw ingestion ordering, store canonical signed decimal text and an exact BLOB sort key: for nonnegative v, `0x01 || uint64be(number_of_decimal_digits) || ASCII(decimal_digits)`; for negative v, `0x00 || uint64be(2**64-1-number_of_abs_decimal_digits) || ASCII(9-complement of each abs digit)`. Zero is nonnegative single digit`0`; no leading zeros or negative zero in integer metadata. This supports numeric ordering without SQLite64-bit coercion. Decode/query verifies text/key/payload agreement. Scope isolation stays exact; never compare sequences across scopes as global time.

Foundation has exactly the three version-2 logical tables in its separate file, storing its unchanged tagged canonical content as BLOB rather than bytea:

| Table | Exact key/index columns in addition to payload/hash |
| --- | --- |
| `mmt_definition_v1` | `owner_namespace TEXT`, `derived_signal_id TEXT`, `calculation_definition_version TEXT`; composite primary key. |
| `mmt_configuration_v1` | `owner_namespace TEXT`, `kind TEXT` CHECK parameter/selection/unit/raw_mapping, `context_id TEXT`, `version TEXT`; composite primary key. |
| `mmt_occurrence_v1` | `derived_occurrence_id TEXT PRIMARY KEY`, `owner_object_id TEXT`, `owner_namespace TEXT`, `implementation_brief_sha256 TEXT`, `derived_signal_id TEXT`, `calculation_definition_version TEXT`, `subject_instrument TEXT`, `effective_as_of_utc TEXT`, `knowledge_cutoff_utc TEXT`, `logical_identity_payload BLOB`, `logical_identity_sha256 TEXT`; foreign key(namespace,D,definition version) to definition. |

Other configuration-reference membership is validated by exact immutable reads within the occurrence transaction. Use the version-2 canonical tagged Decimal/identity/time representation, including signed zero/trailing zeros; hashes and index columns must agree with decoded records. Preserve version-2 newest-first bounded-history ordering; stable fixed-width UTC strings provide chronological index keys. All three semantic tables have immutable update/delete abort triggers. No new financial equation or successor schema alias is created.

## 6. Exact change boundary and proof/admission

Future production changes are limited to M00 `api.py` (exception only; semantic algorithms unchanged unless a separately identified contract defect is returned), new `_sqlite.py` and `_native_codec.py`, A00 `composition/__init__.py`, and the version-2 new foundation package with `_sqlite.py` replacing its unimplemented `_postgres.py` surface. Add no generic shared persistence/strategy framework. `pyproject.toml`, bounded A00 technical-import/dependency/admission metadata and PA-02 control files change only through their exact accepted diff. No transitional M01 adapter is required merely to prove the new owner; its actual conversion/migration remains out of scope.

The incorporated `SQLITE_PROOF_ADMISSION_PROPOSED.md` and four JSON companions define the new raw SQLite claim, revised foundation claim, legacy witness receivers and historical legacy claim treatment. They replace version2's PostgreSQL-only proof/regression assumptions for this new profile. The original legacy registry remains byte-identical evidence; it is not reported as runnable SQLite proof. All13 old M00 obligation scopes have explicit new receivers; all seven FND propositions remain. No test source is deleted/renamed to obtain green.

Required new M00 physical proof files are under `tests/product/raw_signal_sqlite/`: `test_contract_native.py`, `test_schedule_assessment.py`, `test_sqlite_durability.py`, `test_composition.py`, plus required `_support.py`. The first two must exercise the real file-backed public owner too, not only a memory fixture. Use existing literal authoritative specimens as inputs where faithful; independently derive assertions. Do not import/alias old pytest test functions or use old PostgreSQL process helpers as sole proof. `_support.py` provisions literals/store/processes only and does not pre-compose the transition being proved. Existing six raw_signal paths and87 derived paths remain preserved and explicitly accounted for.

Control mechanics are proved first in a provisional reviewed candidate. New M00 physical proof is then authored/reviewed/admitted against the existing actual M00 target and exact contract, with intentionally missing SQLite capability as RED only after environment/admission preconditions hold. Implement M00 storage/composition; obtain full new M00 regression; only then complete control acceptance/bootstrap and G5.1. This avoids requiring M00 SQLite GREEN before the proof mechanism can execute its own admitted development proof. Control candidate readiness, product evidence and final control acceptance remain distinct.

G5.2 retains four ordered proof-before-behaviour units: public D011 boundary, full selection/history, immutable identity/public types, real SQLite durability. The first four foundation proof families preserve version2's exact inputs/assertions with new storage/type configuration; FND-P07 now tests SQLite commit/read-only API/transaction/process/payload provenance, explicitly excluding role-security assertions. Independent review directly performs materialise→later-clock retry, refused request→history read, version change→old/new read and fresh read-only reopen. G5.3 remains separately authorised; no gate closes from this proposal.

## 7. Scope acceptance and recovery

Accepting this exact brief would accept its bounded physical choices, added A00 projection, new raw SQLite proof claim and revised control policy. It would not certify those implementations or their runtime compatibility. The conceptual trusted-application trade-off has already been accepted and is not being reopened. Until exact implementation acceptance exists, preserve old native binding unchanged and do not claim SQLite ingress passed. Once it exists, update the binding atomically to this raw digest with a genuine new reference and four intents, validate under the admitted environment and preserve the predecessor in Git.

Checkpoint before each implementation unit's proof/behaviour; no main merge, history rewrite or actual-state cutover. Any failing integrity/admission/environment invariant stops dependent execution. No skip, absent dependency, missing collected test or changed expected answer manufactures success. Deliver the exact brief/proof/control package and full-Git history for one reviewable acceptance decision before code.

## 8. Exact incorporated bytes

The incorporation table is filled from actual raw bytes after the non-circular companions are authored. No self-digest is embedded. The version-2 brief is pinned as its own exact byte object; its historical Annex-A snapshots are resolved at its stated preparation commit as already prescribed by the active plan, not silently rehashed around the current tree. This file's explicit storage/control overrides govern conflicting version2 prescriptions. All unchanged mathematics/types remain incorporated.

SQLITE-FOUNDATION-CONTRACT-SHA256: 6f93441993e57e12ab4111fe8b98d08ad227c174a706aeab2c2eb14d4494501a

SQLITE-M00-CONTRACT-SHA256: 70a6a0e0d216ef3b6eb3b600b72880dc8dd159215ec761e391eeaf2c1148706f

SQLITE-CLAIM-CATALOGUE-SHA256: ad62fcd57ce837771f732864cbae7e47d9721f0311d21c3b96e05881d83cc317

SQLITE-LEGACY-DISPOSITIONS-SHA256: 26a7c0e03c5f5ddf6872aab9826ce7602891a9dccc482f9f338ce5c6d0883db7

| Path | SHA-256 |
| --- | --- |
| `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` | `282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7` |
| `handoff/foundation_implementation/authority/SQLITE_PROFILE_OWNER_AMENDMENT_20261018.md` | `be6b43bb5ccb9a57003bb77b4f2bfc00a404c6e11da5b355c39644e7a0a647bd` |
| `handoff/foundation_implementation/authority/SQLITE_PROOF_ADMISSION_PROPOSED.md` | `dccf43f17fb741e7ba2d033073f8be7b10f0c2bdf09e464619fa9337dcb1760b` |
| `handoff/foundation_implementation/authority/FOUNDATION_SQLITE_PROOF_CONTRACT_PROPOSED.json` | `6f93441993e57e12ab4111fe8b98d08ad227c174a706aeab2c2eb14d4494501a` |
| `handoff/foundation_implementation/authority/M00_SQLITE_PROOF_CONTRACT_PROPOSED.json` | `70a6a0e0d216ef3b6eb3b600b72880dc8dd159215ec761e391eeaf2c1148706f` |
| `handoff/foundation_implementation/authority/SQLITE_PRODUCT_PROOF_CLAIMS_PROPOSED.json` | `ad62fcd57ce837771f732864cbae7e47d9721f0311d21c3b96e05881d83cc317` |
| `handoff/foundation_implementation/authority/SQLITE_LEGACY_PROOF_DISPOSITIONS_PROPOSED.json` | `26a7c0e03c5f5ddf6872aab9826ce7602891a9dccc482f9f338ce5c6d0883db7` |
| `handoff/foundation_implementation/authority/PA02_PRODUCT_PROOF_ADMISSION_PROPOSED.md` | `76a40bb8ba2f5809c222d08cafb05a1f8e3e35a847d286b1e7abdb28a281aa7a` |
| `handoff/foundation_implementation/authority/PA02_PRODUCT_PATH_DISPOSITIONS_PROPOSED.json` | `df08ac8fa5539e35d03af8c027a15426c857769f02c78ed21946f9f17b436641` |
| `handoff/foundation_implementation/evidence/NVDA_SANDBOX_COMPATIBILITY_DECISION_20261018.md` | `22b57c9eed05aa15cd8693ca97646bcb6ac944301e364938d20a1c551dd66684` |
| `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md` | `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342` |
| `docs/architecture/IMPLEMENTATION_AUTHORITY_INGRESS.md` | `1de870b7054bf055f9abf0c664e928d59bc790282b1d3d4d9b888e98ae8b01c8` |
| `docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md` | `cfe995ebccee824037b897bcc47b292d2114db8b131feab4aac8e8a245a0bde0` |
| `handoff/workbook_v2/decisions/ADR_WBV2_003_V2_INVESTIGATION_COMMISSIONING_BRIEF_VERBATIM.md` | `7a05874fbd4971d03bcef47d5cdaf8020f533a10a6a73cf0ef276b8cb446f771` |

Technical references for these proposed choices: https://www.sqlite.org/pragma.html (EXTRA synchronisation and foreign keys); https://www.sqlite.org/uri.html (rw/ro open modes); https://www.sqlite.org/backup.html (consistent backup); https://www.sqlite.org/omitted.html (no GRANT/REVOKE). They describe mechanisms, not project authority or proved runtime outcomes.
