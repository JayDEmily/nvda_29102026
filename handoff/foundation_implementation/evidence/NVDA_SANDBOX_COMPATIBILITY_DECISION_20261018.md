# NVDA sandbox compatibility decision and accepted architectural direction

18 October 2026. Revision 2. Status: OWNER_ACCEPTED_ARCHITECTURAL_DIRECTION; implementation and runtime compatibility not established.

## Owner acceptance — 18 October 2026, 17:38 Australia/Melbourne

The owner answered **“Yes, I do.”** to the specific question: **“Do you accept that change from database-enforced separation to trusted-application separation?”**

The presented revision's SHA256 was `5d96de573052047f7d2c68dd4168fccab90d96a555ccd9ce8cdefb25676cce06`. Its assessment and proposed-amendment body remain unchanged below.

This records acceptance of the proposed single trusted application SQLite direction: separate owner-local stores and typed public interfaces, with application-enforced boundaries instead of PostgreSQL role-enforced isolation. The absence of protection against arbitrary same-process/same-OS-identity access is an explicitly accepted limitation for this profile. This decision must not be reopened merely because historical PostgreSQL-specific requirements remain in the repository.

Python 3.12.14 remains a candidate requiring compatible dependencies and fresh authorised compatibility evidence. The owner's preceding willingness to change Python does not certify that evidence. No production readiness, project test result, migration, live integration or gate acceptance follows from this decision.

The assessment and proposed amendment below are retained as the decision's rationale and bounded scope. Their earlier pending-approval wording is historical where it concerns the isolation-model choice; this acceptance record governs that choice. Detailed physical design, repository incorporation and execution-plan activation remain separate work. No root ExecPlan or repository authority file has been changed by this document update.

### Successor handoff

Carry this accepted decision into the current project candidate before implementation. Reconcile any later Gate 5 authority/changes against the exact assessed baseline below; do not reset to the older Gates 3–4 tree. Incorporate a versioned SQLite-profile overlay at the identified M00/derived authority and proof boundaries, preserving the historical PostgreSQL record. Then fix the codecs, transaction policy, compatible dependency bundle and proof scope in the bounded execution plan. No further approval of the already accepted trusted-application trade-off is required.

## Decision

Python 3.12.14 is a credible compatibility candidate, but the supplied dependency bundle is not sufficient to establish a supported 3.12 environment. SQLite is a credible transactional storage candidate, but it is **not equivalent to the current authorised PostgreSQL architecture**. The material difference is database-enforced separation of owners, not arithmetic or the spelling of a dependency.

For the owner's requirement to develop and exercise the actual supported runtime inside this sandbox, propose an explicit **single trusted application deployment profile using SQLite**, with separate owner-local stores and existing typed public seams. This profile deliberately replaces database-role enforcement with application-boundary discipline. It does not protect one owner from arbitrary code executing with the same operating-system identity and filesystem access. Owner acceptance of that changed guarantee is required before implementation. If that guarantee must remain unchanged, this SQLite proposal must be rejected: this investigation has not established a sandbox-only solution satisfying it.

The earlier recommendation to use SQLite was incomplete because it had not yet traced the database privilege requirement. A basic SQLite smoke check cannot support a claim of architectural equivalence.

## Exact evidence baseline and limits

- Repository archive: `NVDA_V2_GATES_03_04_ACCEPTED_CLOSED_FULL_GIT_20261017.tar.gz`.
- SHA256: `74c08b8b02d7cdd469d60d1c4f4eede8eec0e2c630d3a6d3facfc63e3888fc44` — recalculated and matched before extraction.
- HEAD: `5b66faaf19e03f841cda97b31b208cef08c77720` — read directly.
- `git status --porcelain`: empty. `git fsck --full`: exit 0, with dangling historical objects reported; none pruned.
- This assessment concerns that exact snapshot. It does not claim to include any later Gate 5 work from another thread. Reconcile a later accepted candidate before applying changes; do not overwrite it with this older baseline.
- No repository files, pins, acceptance criteria or runtime configuration changed. No project imports, tests, lint/typecheck suites, database operations or application execution occurred in this assessment pass. Static AST parsing is source inspection, not execution.

## What the authority actually requires

Master ADR-WBV2-003 §§2, 8 requires preservation of semantic ownership, typed foundational access, independent peers, exact lineage and explicit state/compatibility transitions. It does not itself choose SQLite or waive storage isolation.

The inspected lower-level contracts are explicit:

1. `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md`, BC-011 and BC-015: PostgreSQL representations, own-transaction commit truth and real PostgreSQL integration evidence. Original M16 terminology in this source is historical identity context; current product-proof metadata binds the raw owner to M00.
2. `implementation/authority/VI04_AUTHORITY_CLOSURE.md`: recorded owner approval of psycopg 3.3.4 and bounded PostgreSQL physical design. PostgreSQL 17.9 is a proof-environment version, not a production-version mandate.
3. `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`, §10, lines 478–498: separate PostgreSQL schema and writer role, no calculation-owner database privilege on M00 relations, and durable occurrence/context/lineage state. §§11–14 preserve temporal distinctions, exact lineage and append-only recalculation.
4. `config/product_proof/families.yaml`, `rsot_u05_postgresql_durability`, lines 265–339: explicitly excludes SQLite/local files standing in for PostgreSQL. Includes fresh-process and isolation-environment obligations. These cannot simply be renamed to obtain a pass.
5. Accepted planning roadmap, §3 A01 item 5 and pilot proof table: carries schema/role isolation and denial of inherited/SET ROLE access into the proposed successor.

`docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md` distinguishes domain ownership from non-owning storage mechanisms. A changed mechanism may preserve domain meaning, but must still have an expressly authorised writer/reader boundary.

## Compatibility findings

| Area | Evidence and disposition |
|---|---|
| Current interpreter | `python3 --version` returned 3.12.14. The project pins 3.13.5. Do not pin 3.12.4 by transcription error. |
| Python syntax | All 156 `.py` files under `src`, `tests` and `tools` parsed with Python 3.12's AST grammar without SyntaxError. This proves syntax compatibility only; imports, dependencies and runtime behaviour remain unproved. |
| Python package supply | The U05 archive contains CPython-3.13-specific wheels for mypy 1.20.1, psycopg_binary 3.3.4 and librt 0.9.0. It does not contain PyYAML or hatchling wheels. The inspected repository has no `vendor` directory although its uv configuration points to `vendor/wheels`. A 3.12 pin requires a complete compatible wheel bundle and validation; changing pyproject alone is insufficient. |
| PostgreSQL host capability | The prior environment investigation executed the existing 17.9 binary successfully. Cluster creation was blocked by root-only UID/GID mapping, failed ownership assignment and denied user-namespace mapping. No server was started. Rebuilding does not address that identity restriction. |
| SQLite host capability | Prior isolated probe established commit, rollback, fresh-process readback and integrity checking with SQLite 3.53.1. It did not exercise project code, crash recovery or owner isolation. |
| M00 adaptation boundary | `raw_signal_occurrence_truth/api.py` lines 850–904 exposes a private transaction port. Its PostgreSQL adapter stores owner-decided records and uses explicit table locking and constraints. This is a usable design boundary; replacement behaviour is unproved. |
| Derived adaptation boundary | `derived_signal_calculation_truth/api.py` lines 951–959 exposes append/get/list persistence. The complete `_postgres.py` was read: it validates schema/role identity, table/column privileges and assumable roles on connections. These checks are substantive enforcement, not interchangeable connection setup. |
| Application construction | Complete `composition/__init__.py` was read. `create_application` requires a PostgreSQL DSN for production and injects the PostgreSQL mechanism into M00. Its factory-only branch is explicitly proof-only. It must not be repurposed as a production bypass. |
| Exact values and ordering | PostgreSQL NUMERIC, timestamptz, bytea, arrays and JSONB need explicit SQLite encodings. Existing typed native and derived codecs are reuse candidates. SQLite numeric affinity must not silently round arbitrary integers/Decimal values or change temporal ordering. |
| Isolation | SQLite has no GRANT/REVOKE role model. Separate files in this root-only sandbox do not establish a separate security principal. Private Python objects and authoriser callbacks must not be advertised as equivalent database-role isolation. |
| Scale and deployment | SQLite serialises writes per database file. Required throughput and deployment topology are not established by the inspected authority; no performance/SLA promise is justified. Sandbox workspace survival and always-on operation are separate from committed database transactions. |

## Proposed amendment — exact decision for owner consideration

The following is proposed text, not current authority:

> Authorise preparation and implementation, under a separately accepted bounded execution plan, of a single trusted application persistence profile using SQLite for sandbox development and its corresponding supported deployment. Preserve all accepted mathematical, identity, temporal, lineage, retry, supersession, transaction-success and peer-independence meanings. M00 and each calculation owner retain their own persistence adapter and separate database file; consumers obtain facts only through the owner's typed public seam. Composition injects only each owner's own store and lawful readers. No module may directly open another owner's database, and no downstream peer service or shared strategy layer is introduced.
>
> For this profile, replace the requirement for PostgreSQL schemas/roles with application-enforced ownership boundaries. Explicitly withdraw the claim that database credentials prevent arbitrary same-process or same-OS-identity code from accessing another owner's state. This is a changed assurance boundary, not equivalent PostgreSQL isolation. A deployment requiring that stronger isolation is outside this profile and requires separate architecture and acceptance.
>
> Admit CPython 3.12.14 as the candidate runtime, conditional on complete compatible dependency supply and fresh authorised compatibility evidence. Do not treat static parsing as runtime acceptance. Preserve historical PostgreSQL code, authority and proof results as historical evidence; no old PostgreSQL result certifies the SQLite profile. No existing state migration, live IBKR integration, trading or gate acceptance is authorised by this amendment alone.

This decision is necessary because §10 of the derived brief requires database-role isolation. The owner's instruction to assess whatever works does not silently approve withdrawing that guarantee.

## Concrete implementation design, conditional on that decision

Keep domain algorithms and public result meanings intact. Implement owner-local `_sqlite.py` adapters through the existing private persistence interfaces; do not build a shared semantic persistence service. A00 selects the expressly admitted profile at construction. Missing/invalid storage must fail closed, never fall back to memory.

Use explicit transactions, commit before reporting durable success, enable and read back foreign-key enforcement on every connection, and choose a fixed journal/synchronisation policy in the physical design. `BEGIN IMMEDIATE` is the candidate write-transaction mechanism for read/decide/append operations; it must be proved against contention and retry semantics. Database locking failure must remain an unachieved operation, not a fabricated observation or automatic success. No new retry timing or SLA is implied.

Reuse native-value binary encoding only after proving exact round trips. Store arbitrary integers and Decimal payloads losslessly rather than relying on SQLite numeric affinity. Define separate sortable representations for range/high-water queries; decimal text lexical order is not numeric order. Preserve true-instant/date-only/receipt-only distinctions, microseconds and independently supplied nanoseconds. Encode structured lineage and arrays with explicit type/version semantics. Keep domain decisions inside owners.

Preserve each occurrence/assessment's own transaction boundary; do not introduce whole-graph or cross-owner atomicity. Keep same-ID/same-content retries idempotent and conflicting content rejected, including racing submissions. No historical database is assumed empty. Existing persisted-state census, export/import and reversible cutover need separate migration authority before use on real data.

## Affected surfaces and acceptance sequence

1. **Authority and physical design:** versioned overlay to the M00 brief/VI04 and derived brief §10; reconcile downstream authority/proof bindings and the current successor plan; fix exact codecs, transaction policy, trusted-process boundary and snapshot/restore scope. Do not edit frozen GUARDRAILS or rewrite historical acceptance. The exact later Gate 5 baseline must be reconciled first.
2. **Runtime and adapters:** update `pyproject.toml` Python/Ruff/mypy targets, supply compatible pinned wheels and bootstrap checks, implement the two owner-local adapters and admitted composition branch. Decide whether psycopg remains an explicit optional legacy dependency; unconditional composition imports must not make it mandatory for SQLite. Do not delete historical PostgreSQL paths merely to simplify installation.
3. **Proof and admission:** preserve existing domain proof propositions while explicitly replacing backend-specific claims through authority. Prove exact types/lineage, commit-before-return, failed-write absence, fresh-process recovery, competing retries, per-scope high-water order, append-only assessment chains, no fabricated zero, and owner public-seam use. Prove the actual SQLite production path and test failure of missing storage. Role-isolation tests remain historical PostgreSQL evidence, not renamed SQLite passes. Record the changed assurance boundary in the acceptance decision.

Python acceptance must include clean offline installation, relevant imports/runtime behaviour, targeted product checks, lint/typecheck and architecture validation under the admitted environment. These are future obligations, not executed results. Dependency-installation failures are environment failures, not intended behavioural RED results.

A reusable handoff must include exact interpreter/dependency/database-engine versions, hashes, a non-destructive preflight and a consistent snapshot/restore procedure. Filesystem transaction durability does not promise survival of sandbox removal. Performance and live service deployment remain separately scoped.

## Evidence references and coverage

Read in full: root GUARDRAILS and AGENTS; root closed ExecPlan (including separately recovered truncated passage); master ADR-WBV2-003 across complete output segments; M00 IRB; VI04; ownership law; composition module; derived PostgreSQL adapter. Read relevant complete sections: derived brief §§9–14; both API persistence protocols and derived constructor; U05 product-proof family; roadmap authority/pilot/environment sections. The prior investigation read the complete raw PostgreSQL adapter. Other calculation semantics were not re-audited, and no claim of whole-project 3.12 compatibility is made.

Primary technical references:

- SQLite omitted SQL: https://www.sqlite.org/omitted.html — no GRANT/REVOKE; underlying file permissions apply.
- SQLite isolation: https://www.sqlite.org/isolation.html — serialised writes and transaction isolation.
- SQLite appropriate uses: https://www.sqlite.org/whentouse.html — deployment and concurrency trade-offs.
- Psycopg installation: https://www.psycopg.org/psycopg3/docs/basic/install.html — binary client installation is not server installation.

Outcome: the static compatibility assessment identifies a concrete feasible design direction and one material assurance decision. It does not establish an implemented solution, replace the current database authority or accept a project gate.
