# Proposed ExecPlan — Ubuntu transition, R2/G0 reconciliation and bounded M00 PostgreSQL admission

**Plan ID:** NVDA-UBUNTU-R2-POSTGRES-M00-20261110  
**Date:** 10 November 2026 (Australia/Melbourne)  
**Status:** `PROPOSED_NOT_ACTIVE / DOCUMENTARY_PLANNING_ONLY`  
**Scope:** prerequisite recovery and independent handover, exact environment qualification, and a *separately governed* PostgreSQL M00 persistence profile.  
**Decision basis:** [ADR_20261110_POSTGRESQL_ADDITIONAL_BACKEND.md](ADR_20261110_POSTGRESQL_ADDITIONAL_BACKEND.md).  
**Owner direction:** record the ADR and plan before executing. **No product-code, runtime, test or active-plan change is authorised merely by this file.**

## 0. Authority, baseline and relation to the 39-leaf programme

The frozen root `GUARDRAILS.md` (Git blob `54a4407609941f63f6b902076688ff102a3d5ba2`) governs every step. Applicable root `AGENTS.md`, `tests/AGENTS.override.md`, exact implementation authority, original tests and current explicitly accepted root ExecPlan must be read again when a leaf is commissioned. No external historical record self-accepts.

- Current commissioned R1 reference: `execution/accepted-r1-20261030` @ `363923d47b81fca50e64036bef3c8601501e3c16`; root plan declares L00 blocked on historical transfer.
- Published R2 proposal: `planning/chat-manual-r2-20261030` @ `6feb50bf8a96e244cbd68eb57536f940be6335b3`, expressly `PROPOSED_NOT_ACTIVE`. The owner's later local R2 `CHAT_MANUAL` approval is separate evidence and does not make GitHub's older proposal byte-identical or automatically active.
- Local R2/G0 predecessor `9a4f1e827accdd7cfe3d7a14d5575573589b1acd`: independent Git transport PASS, F01 CLOSED, F02 RETURN_FOR_BOUNDED_REPAIR. Later F02 Worker repair is attributed to `16b7cc67f5d24336d3768e2da006819474a8c792`; **independent acceptance and final exact bytes are UNKNOWN**.
- Ubuntu Git checkout `/home/jds/nvda_29102026`: default `main` HEAD `8ff7d82377e9bf8f9fc75c1ecef70f0ab29a2ada`, clean when inspected. A separate original-baseline + R1 successor bare-Git restoration has independently matched 66 original and 779 release-declared ref tips, target commit/tree, tracked inventory and `git fsck`. This does not independently accept R2/F02.
- In-scope existing programme census is **39 leaves / 35 D-signal proof obligations / 27 mandatory new D identities (20 core + seven extensions) / 28 currently unresolved foundation identities / seven external holds / D145 PAUSED**. The proposed R2 schedule retains **60 prospective new-signal physical cases** plus **up to 14 conditional supporting cases**. PostgreSQL M00 backend proof is **additional and separately allocated**: do not silently insert cases into these existing D-signal allocations, release any G1–G5 signal gate, or change the 126 = 98 + 28 accounting.
- This proposed supplementary sequence is **not a second concurrently active root plan**. Following independent review and explicit owner acceptance, integrate its approved obligations with the reconciled successor root `EXEC_PLAN.md` and ledger. Until that event, preserve the existing accepted root and history. No same-name root replacement, merge or branch promotion from this planning record.

## 1. Required outcome and non-goals

### Actual deliverables before execution resumes

1. Exact recoverable and independently reviewed last applicable R2/G0 candidate, with F02 disposition and lineage, or a specific `BLOCKED` entry if inaccessible.
2. A single accepted root execution authority, exact AGENTS/test-override alignment and unchanged programme census, with the approved separate `CHAT_MANUAL` Tester role.
3. Demonstrated **independent GitHub pinned-commit handover** by a genuinely different Tester chat using its own checkout and complete required history/evidence, or preservation of the previously accepted bundle strategy until a suitable substitute is proved and approved.
4. Exact supported Ubuntu CPython/SQLite environment and dependency/runner qualification, preserving old evidence without asserting backend equivalence.
5. An independently reviewed M00 PostgreSQL additional-profile contract and proof admission, with a reproducible server/package/driver/version and distinct role/schema boundary.
6. Only if separately commissioned: minimal M00 PostgreSQL adjustments needed to satisfy that contract, tests authored before code, immutable candidate and `IMPLEMENTED_UNTESTED`.
7. At the authorised L32 Tester boundary: independent targeted PostgreSQL and affected integration proof, with literal commands, outcome/lineage evidence, immutable public readback and explicit acceptance/return/blocked disposition.
8. Durable final Git records and honest unresolved-work census; no historical proof or signal automatically reclassified.

### Outside scope

No M01 activation/retirement, M02 PostgreSQL conversion, migration of actual SQLite data, new D-signal equation or signal acceptance, D145 reactivation, external market-provider access, order execution, live service/production deployment, network exposure, performance SLA, `asyncio` redesign or new generic storage abstraction. Existing SQLite stays operationally and historically intact. Installation and product test execution begin only under a later accepted and commissioned plan.

## 2. Dependency gates and stopping points

These T-stages are *pre-activation planning labels*, not additions to or renumbering of R2's 39 leaves. All are `PROPOSED_NOT_STARTED` at publication; already observed historical checks are inputs, not newly completed stages.

| Stage | Semantic deliverable | Predecessors | Independent evidence / release condition |
|---|---|---|---|
| T00 — Recover evidence | Latest R2/G0/F02 candidate, original independent review and repair chronology | Current read authority | Exact restored commits, parent/tree, changed paths, F02 mechanism and post-repair independent disposition; retain missing-evidence blocker if unavailable |
| T01 — Authority reconciliation | One accepted R2 successor baseline, mode, AGENTS, proof ledger, transfer scope | T00 evidence for affected claims | Review exact delta from R1/R2/local; preserve all 39 leaves, 35 obligations, original cases and D145 pause; obtain specific owner acceptance |
| T02 — Independent transport | GitHub-to-independent-Tester pinned commit receipt | T01 approved transport direction | Second chat fresh clone/fetch, exact ref/tip closure, HEAD/tree/blob inventory, provenance/non-Git hash manifest, `git fsck --full`, literal readback log; fallback bundle if unproved |
| T03 — Runtime qualification | Reproducible Ubuntu project-specific runtime and compatible SQLite pathway | T00/T01 approved environment scope | CPython 3.13.5, actual SQLite 3.54.1 launch path where applicable, dependency/wheel/runner pins, recorded preflight and independent F02 review; no automatic historical product reruns |
| T04 — PostgreSQL authority and environment contract | Bound PG18.6 candidate + M00 backend proof proposal | T01; T03 Python package baseline as needed | Exact PG package/server and Psycopg version; M00 roles/permissions, old claim disposition, concurrency/outcome proposition, explicit new physical cases/admission and independent contract review |
| T05 — Bounded source candidate | M00 PostgreSQL feature only if genuinely missing | T04 exact accepted authority and separate execution commission | Minimal enumerated diff, public M00/A00 law preserved, proof authored before behaviour, no broad tests by Worker; committed `IMPLEMENTED_UNTESTED` |
| T06 — Separate product testing | Independent PG persistence/concurrency proof | T05 and governed R2 L32 entry | Sole Tester executes newly admitted necessary cases in dependency order; records independent oracles, real server outcomes, typed durable readback, case/claim generation and semantic dispositions |
| T07 — Reconciliation close-out | Truthful promotion/blocked record and next implementation release | T02/T03/T04 and T06 where in scope | Independent reviewer checks manifests, unchanged proof/history, explicit backend status and unresolved holds; owner acceptance before any new active root/scope promotion |

**Stop law:** A missing F02 acceptance prevents dependent R2/G0 release; an unproved independent receiver prevents changing the checkpoint strategy; an unavailable matching server/driver prevents backend product claims; an unadmitted contract prevents M00 implementation; an unavailable independent Tester prevents L32 product acceptance. Unrelated documentary preparation may continue without declaring any dependent gate complete. Stop first missing invariant, preserve original evidence.

## 3. T00 — F02 and R2/G0 reconciliation procedure

Read the original independent review `NVDA_R2_G0_L00_INDEPENDENT_GIT_REVIEW_20261031.md` in full: it established Git PASS/F01 CLOSED and F02 that a documented *tracked* `tools/with_pinned_sqlite.sh` was absent. Read the subsequent Worker repair record, not just its summary. Obtain exact **`NVDA_R2_G0_L00_F02_INDEPENDENT_REVIEW_HANDOFF_20261031.zip`** and its cumulative additive Git bundle if currently inaccessible. Restore with original fixed baseline `97f944d51ab9e403250fe76910e2754b50425c73` and required 66 original refs.

Verify: package/member SHA and traversal safety; `git bundle verify` and prerequisites; actual commit `16b7cc67f5d24336d3768e2da006819474a8c792` and tree versus external receipt; all historical and newly declared ref tips; parent chain to `9a4f1e827...`; exact Git changed paths; absence or replacement of the originally misdocumented launcher; actual reproducible `LD_LIBRARY_PATH` mechanism and source/version identity; independent reviewer verdict and `git fsck --full`. F02 repair **Worker-reported PASS** is not independent `ACCEPT`. If original bytes or verdict are not accessible, record `UNKNOWN/BLOCKED_RECOVERY`; do not invent a retrospective acceptance. Keep historical R1 L00 Git integrity as a separate already verified proposition.

## 4. T01/T02 — governance and transport

- Produce exact, reviewable proposed root `AGENTS.md`, scoped `tests/AGENTS.override.md`, active ExecPlan delta, execution ledger and proof ledger against the last verified R2/G0 candidate. Owner's prior CHAT_MANUAL approval is real but does not automatically adopt differing published text bytes. Current R2 `AGENTS.md` contains a 112-word mode-neutral draft and the approved testing arrangement names a separate Tester at L32.
- Preserve R1 history and all 35 proof obligations. No product cases move to earlier leaves without explicit owner schedule amendment; documentary contract reviews remain earlier. Preserve old independent reviewer findings/recurrent mechanisms.
- Propose replacing repetitive manually transported archives with `PINNED_REMOTE_CHECKPOINT` **only after** the second real ChatGPT Tester can independently access GitHub and a fresh separate checkout. Pin SHA, branch, tree, full tracked path/object inventory, required original 66 tips plus any currently missing historical aliases/evidence refs, and external artefact SHA-256. Compare actual declared ref namespace; do not substitute mere existence of tip objects for a required named-ref map.
- The Tester executes read-only Git restoration/closure tests, not NVDA product tests, during this transport qualification. GitHub producer publication or an API file preview alone is insufficient. Preserve the accepted bundle/cumulative-additive fallback if equivalence is not proved; any transport strategy change requires owner approval and exact root-plan update. Never rewrite main or history to simplify the test.

## 5. T03/T04 — Python, SQLite and PostgreSQL environment admission

### Python and SQLite

Verify and bind the *actual* Python 3.13.5 binary, reproducible wheel/build dependency set, project `pyproject.toml`, `.python-version`, Ruff, mypy, strict runner and required SQLite 3.54.1 library/version/source preflight. The currently published GitHub `pyproject.toml` still requires Python 3.12.14 while the Ubuntu standalone 3.13.5 interpreter is available; this mismatch requires an exact scoped config decision. Check F02 launch semantics before relying on the old runtime receipt. The old CPython 3.12.14/SQLite 3.53.1 product evidence remains historically valid only for its exact candidate and proposition; neither broad rerun nor parity is assumed.

### PostgreSQL server and driver

Proposed initial Ubuntu server pin: **PostgreSQL 18.6** package `postgresql-18=18.6-0ubuntu0.26.04.1`, as observed in Ubuntu 26.04.1 `apt-cache policy` on 10 November 2026. Package/version availability is a read-only observation; installing, enabling a service, provisioning credentials, altering package sources, creating a database or operating production infrastructure requires the later commissioned execution scope. Independently bind `SELECT version()`, `SHOW server_version`, package manager/source identity and actual server/socket/permissions when that work is authorised.

Use existing `psycopg[binary]==3.3.4` optional runtime dependency and `psycopg==3.3.4` development/type-check dependency unless their actual Python 3.13.5 or server compatibility fails. They are already in `pyproject.toml`; do not add duplicates or install a server through Python metadata. Check the exact Python wheel/ABI and connection test; select a distinct M00 writer role/schema and read-only consumer privilege profile. A separate M01 role/schema remains historical design, not an activated owner. No secret DSN/password enters Git.

The original M00 PostgreSQL U05 proof is tied to **PostgreSQL 17.9** and old PostgreSQL-only assumptions. It remains `HISTORICAL_NOT_RUNNABLE` under the current SQLite claim. New PG18.6 execution needs explicit owner-approved proof contract/generation and an independent source/test review; do not simply change a legacy hard-coded 17.9 expectation to obtain green.

### Definition of non-product readiness

A successful installation or simple `SELECT 1` is **environment connectivity only**. It cannot demonstrate persistence correctness, concurrency, ownership, failure semantics, complete source fidelity or M02 operation. No product tests are executed in T03/T04; those belong to T06/L32 once separately admitted.

## 6. T04/T05 — bounded M00 scope and exact changes

Read in full the accepted M00 IRB/SQLite owner amendment and implemented public M00 contract, A00 `create_application`, both existing M00 adapters, `config/architecture/modules.yaml`, technical-import exceptions, current active proof admissions, historical PostgreSQL U01–U06 tests, current SQLite RSQL claim, and the isolated M01 privilege tests. Document exact satisfied requirements and deficiencies *before proposing a modification*.

M00 remains sole semantic owner. Keep exactly one backend selected per A00 composition; preserve M00 typed public projections, schedule/assessment and transaction-outcome semantics. PostgreSQL physical SQL/driver must not own decisions or grant M01 direct write/read access to M00 relations. Preserve M02 separate SQLite identities and read-only public M00 ingress.

Any source change must list its specific target files, authority, purpose and proof. Likely inspection surfaces (not pre-authorised edits): `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py`, `src/nvda_desk/composition/__init__.py`, `pyproject.toml` **only if justified**, `config/product_proof/claims.json`, associated separately admitted family/schema/generation, targeted M00/A00 tests and the exact runtime manifest. Reuse existing working code wherever it satisfies the contract; do not refactor M02 or build a shared storage framework just to expose a new backend.

The Worker may author exact independently derived test oracles before code and commit an unexecuted candidate. `IMPLEMENTED_UNTESTED` is not a product-accepted state. An observed deficiency must be grounded in the actual code/tests/contract, never inferred from absence of a newly invented wrapper.

## 7. T06 — independent real-PostgreSQL product proof at L32

The independent Tester, on the exact pinned candidate and supported server, must have a **separately admitted finite test allocation**, not an inherited permission to run arbitrary legacy suites. At minimum its contract should distinguish these semantic propositions, with targeted cases rather than generic smoke proxies:

1. M00 exact public record and native typed-content roundtrip over real PostgreSQL, including source/receipt/time/identity and immutable readback from a fresh client/process.
2. Actual successful M00 command only **after its own PostgreSQL transaction commit**; rollback/write failure never fabricates stored truth; a post-commit lost acknowledgement has the required uncertain-outcome recovery semantics.
3. Identical logical identity/content retry converges; conflicting content under the same immutable identity refuses rather than overwrites; normal distinct identities remain independently durable.
4. At least **two distinct client connections/sessions** overlap lawful write transactions and a separate reader exercises the declared visibility/isolation contract. Establish overlap with observed server/transaction state rather than only timers; conflicts/deadlocks/serialization failures are classified, not treated as arbitrary data absence.
5. M00-only writer privilege, prohibited M01/direct cross-owner SQL, and correctly scoped public read projection under actual PostgreSQL roles.
6. A00 `postgres_dsn` path preserves exact A00→M00 delegation and rejects conflicting `sqlite_path`, invalid configuration and private ownership leakage. Retained SQLite selection must remain supported without Psycopg being a mandatory runtime import.

The Tester records literal commands, accepted test path/claim/generation, PostgreSQL server+driver/version identity, actual results, reached refusal and durable public readbacks. Independent oracles must not come solely from Worker fixture helpers. Reviewer classifies recurring failure classes, preserves failed run bytes, and returns bounded defects to Worker for repair. Re-execute failed tests only after material repair, and passed tests only after material invalidation; protect existing SQLite and historical PostgreSQL proof.

**No declaration of concurrency capability, backend acceptance or a completed G5 may precede these independent observations.** All new D-signal product tests remain subject to the separately accepted R2 L32 dependency-ordered schedule; new M00 PG tests do not consume the 60 + up-to-14 D-signal case budget without separate approval.

## 8. Acceptance and close-out

Stage completion is a reproducible evidence record, not a label. For each authorised stage, record: exact owner decision/reference, Git SHA/parent/tree and changed paths, full inspected authority and proof inputs, test commands and environment if run, output/exit status, independent review, preserved historical/ref manifest, outstanding items, and first unmet invariant. A Git commit or accepted ADR is not execution acceptance.

T07 reports the disposition of every declared deliverable in §1 (`VERIFIED / ACCEPTED / IMPLEMENTED_UNTESTED / UNKNOWN / BLOCKED / OUT_OF_SCOPE`). It must state explicitly:
- whether latest R2/G0/F02 is independently accepted;
- whether a single active successor root plan and test authority has been admitted;
- whether the distinct Tester has verified remote handover;
- actual Python/SQLite/PostgreSQL version and driver evidence;
- actual M00 PostgreSQL source contract and product proof outcome;
- retained SQLite backend, M01 bootstrap, M02 SQLite, original proof generations, 39 leaves, 35 obligations, seven external holds and D145 pause;
- what remains before the original R2 G1–G5 implementation may proceed.

No automatic main merge, historical ref pruning, original checkpoint destruction, server activation, product testing or downstream financial work follows from publication of this draft. Independent documentary review and **specific owner acceptance of the complete successor/root-plan integration** precede any implementation commission.

## 9. Reference index

- [Companion ADR](ADR_20261110_POSTGRESQL_ADDITIONAL_BACKEND.md)
- `GUARDRAILS.md`, original accepted R1 and published proposed R2 `EXEC_PLAN.md`
- `handoff/planning/chat_manual_transition_20261030/TRANSITION_REVIEW.md`
- `handoff/foundation_implementation/authority/SQLITE_PROFILE_OWNER_AMENDMENT_20261018.md`
- `handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md`
- `config/architecture/modules.yaml`; `docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md`; `docs/architecture/PUBLIC_SEAM_LAW.md`; `docs/architecture/TEST_AND_PROMOTION_KERNEL.md`
- `config/product_proof/claims.json` and `config/product_proof/families.yaml`; `tests/product/raw_signal/test_u05_postgresql_durability.py`; `tests/product/raw_signal_sqlite/test_sqlite_durability.py`
- `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py`; `src/nvda_desk/raw_signal_occurrence_truth/_sqlite.py`; `src/nvda_desk/composition/__init__.py`; `src/nvda_desk/market_measurement_truth/_sqlite.py`
- Historical independent F02 findings from `NVDA_R2_G0_L00_INDEPENDENT_GIT_REVIEW_20261031.md`, later Worker F02 repair receipt not independently accepted
- Official PostgreSQL MVCC/versioning: https://www.postgresql.org/docs/current/mvcc.html ; https://www.postgresql.org/support/versioning/
- Official Psycopg concurrent operations: https://www.psycopg.org/psycopg3/docs/advanced/async.html
- Official SQLite WAL/concurrency: https://www.sqlite.org/wal.html

**Publication effect:** a reviewable planning artefact and evidence pointer only; no active execution-status change.
