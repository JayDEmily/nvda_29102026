# VI12R U06 Stage 4 — whole-U06 adversarial closure and Worker candidate evidence

## Status

**WORKER STAGE 4 COMPLETE — EXACT U06 CANDIDATE FROZEN — STAGE 5 NOT STARTED.**

This record is Worker evidence for U06 Stage 4. It is not independent Tester acceptance or
promotion.

## Governing boundary

- Active U06 ExecPlan on `main`: `c3ae566ff8367d83dc783289d9b553faa9a51325`.
- Stage 3 implementation predecessor: `36e694ee111db5ab45acc298fc7486f1fdc6ac4b`.
- Stage 3 evidence/handoff predecessor: `84fe26ea8598d4964c42434539abede401259b77`.
- Frozen U06 Worker candidate: `8462630277b04d431ad393e2b73039cacb5d6247`.
- Frozen candidate tree: `0a01dacbf54f61bd7f60cf5e68cc350c3cf8d0c6`.
- Work branch: `work/u06-a00-composition`.

## Stage-4 changes before candidate freeze

Stage 4 added no new product capability. The source/test changes close defects found by the
mandatory whole-U06 source trace and restore the accepted product-proof control boundary.

### 1. Production dependency-injection capability bypass closed

Before the Stage-4 repair, callers could combine `postgres_dsn` with a caller-supplied
`raw_signal_owner_factory`. A00 would construct the raw PostgreSQL persistence object and pass that
object into the arbitrary caller factory as `durability_port`. The caller factory could therefore
capture the technical persistence capability directly, bypassing the intended M00-owned semantic
boundary.

The candidate now makes the two construction paths mutually exclusive:

- production path: a valid `postgres_dsn` always constructs the admitted M00 owner through the
  imported public `create_owner` seam; a caller owner-factory override is rejected;
- proof-substitution path: a caller owner factory remains available only when no PostgreSQL DSN is
  supplied, so A00 creates and leaks no persistence capability to that caller.

The Stage-1 construction proof was strengthened accordingly.

### 2. Registered-policy result controls the policy-reference consistency check

Before the Stage-4 repair, A00 validated the caller policy reference against the policy object
submitted to registration rather than the exact policy object returned by M00 registration. The
accepted U06 dataflow law requires capture progression to be consistent with the identity/version
accepted by policy registration.

The candidate now derives the comparison reference from the exact `registered_policy` returned by
M00. An adversarial spy case returns a policy identity different from the submitted identity and
proves that A00 fails before capture realisation when the caller reference identifies only the
submitted policy.

### 3. Product-proof admission control restored without weakening it

`tools/validate_product_proof.py` lawfully requires every `tests/product/**/test_*.py` path to be an
admitted physical product-proof family. The repository had accumulated six later U05/U06
implementation-coupled stage regression files under `tests/product/raw_signal/` even though they
are not and must not become additional admitted product-proof families.

The candidate preserves the six accepted family paths unchanged and relocates only those six
supplemental stage regression files to `tests/implementation/raw_signal/`:

- U05 Stage 2 restart foundation;
- U05 Stage 3 observation restart;
- U05 Stage 4 assessment restart;
- U05 Stage 5 whole restart;
- U06 Stage 1 A00 construction;
- U06 Stage 3 PostgreSQL composition.

No assertion or semantic test content changed merely because of those relocations. Historical
evidence continues to identify the paths that existed at the historical commits it describes.
The current product-proof validator again passes with exactly six admitted physical families and
13/13 product obligations covered.

## Mandatory source-level logic trace

The realised candidate was traced through:

`A00 construction -> technical persistence construction -> M00 owner construction -> commands/reads -> sequential orchestration -> returned application result -> lifecycle/teardown`.

### A00 construction

- `create_application` is the production A00 construction entry point.
- The production path requires a non-empty PostgreSQL DSN.
- A00 constructs only the accepted non-owning PostgreSQL mechanism through the single declared
  technical exception `raw_signal_occurrence_truth._postgres.create_postgres_persistence`.
- The resulting persistence object is passed directly to the admitted public M00 `create_owner`
  constructor and is not stored on the A00 `Application` object.
- Production construction rejects a caller-supplied owner factory, closing the direct-capability
  leak described above.
- The optional eligibility resolver is passed unchanged to M00; A00 does not invoke it or define
  eligibility meaning.

### M00 construction and dependency direction

- A00 imports M00 semantic contracts/construction only through
  `nvda_desk.raw_signal_occurrence_truth.api`, plus the one declared technical PostgreSQL
  constructor exception.
- `config/architecture/dependency_rules.yaml` declares exactly `A00 -> M00`.
- A source search found no `nvda_desk.composition` import from the M00 package, so no realised
  `M00 -> A00` reverse dependency was found.
- No P01, K01, packet carrier, provider/network or downstream consumer is imported or selected by
  the A00 composition path.

### Commands, reads and sequential orchestration

A00 obtains only M00 `commands` and `reads` facets from the stored owner and performs the authorised
sequence:

1. register policy;
2. validate the caller scope-policy reference against the exact registered M00 policy result;
3. realise capture;
4. admit observation;
5. derive receipt-evidence relation using the exact M00-returned observation identity, capture
   identity and effective policy reference;
6. append assessment using the exact M00-returned capture identity and authoritative A00
   assessment inputs;
7. read the observation by the exact M00-returned observation identity.

A00 contains none of the M00-owned outcome literals `zero_received`, `one_or_more_received` or
`unknown_not_established`, and does not calculate eligibility or supersession meaning.

### Returned result and lifecycle

- `RawSignalSequenceResult` contains the exact semantic objects returned by M00; A00 does not
  recreate policy, capture, observation, relation, assessment or readback facts.
- The production path and dependency-substitution path exercise the same orchestration method; the
  real PostgreSQL Stage-3 discriminator proves the production factory rather than only the spy
  path.
- The A00 object stores only the M00 owner. Existing ordinary-object-graph proof finds no exposed
  PostgreSQL `transaction` capability under the accepted bounded public-seam law.
- A00 has no invented long-lived `start`, `stop`, `close` or `shutdown` surface. Existing real
  PostgreSQL proof confirms ordinary application-object teardown/GC does not mutate durable M00
  facts.

No unresolved ownership, dependency, dataflow or lifecycle defect remained established by this
trace.

## Exact proof environment

Decisive post-freeze proof used:

- CPython `3.13.5`;
- pytest `9.0.3` from the preserved offline U05 proof environment;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4` / psycopg-binary `3.3.4`;
- PostgreSQL `17.9`;
- PostgreSQL `fsync=on`, `synchronous_commit=on`, `full_page_writes=on` and Unix-socket-only
  transport;
- PyYAML `6.0.3` exposed through a dedicated PyYAML-only `PYTHONPATH` overlay, so the host
  site-packages directory did not shadow the preserved pytest/toolchain.

An earlier post-freeze aggregate run was functionally green at 479/479 but used a whole-host
site-packages overlay for PyYAML, which shadowed pytest 9.0.3 with host pytest 9.0.2. That run is not
used as the decisive environment evidence. The exact-environment rerun below supersedes it.

## Post-freeze validation against exact candidate `8462630277b04d431ad393e2b73039cacb5d6247`

### Admitted Raw Signal product-proof aggregate

Command surface: `tools/run_product_proof_gate.py --aggregate raw_signal_occurrence_truth_product`.

Result: **479/479 passed** under Python 3.13.5 / pytest 9.0.3.

The gate also reported:

- product-proof control structurally/semantically bound: PASS;
- admitted physical product families: exactly 6;
- covered current product obligations: 13/13;
- aggregate state: `READY_FOR_PROOF`.

The 479 cases include the admitted U01-U06 physical product families, including the configured
real-PostgreSQL U05 durability family and the accepted U06 A00 composition family.

### Supplemental accepted implementation-coupled predecessor proof

Relocated U05 Stage-2 through Stage-5 restart regressions: **27/27 passed**.

### U06 construction/delegation/real-composition closure set

- U06 Stage-1 construction regression;
- admitted U06 A00 composition family;
- U06 Stage-3 real PostgreSQL composition regression.

Result: **15/15 passed**.

### Architecture/bootstrap and static checks

- architecture/bootstrap: **74/74 passed**;
- mypy over `src`: **Success: no issues found in 16 source files**;
- Ruff over `src tests tools`: **All checks passed**;
- `git diff HEAD^..HEAD --check`: **PASS**.

## Candidate boundary

The whole-U06 Worker candidate is frozen at:

- commit `8462630277b04d431ad393e2b73039cacb5d6247`;
- tree `0a01dacbf54f61bd7f60cf5e68cc350c3cf8d0c6`.

No evidence/handoff edit after this freeze may modify candidate production/test/config/dependency
bytes.

## Remaining status

Stage 4 Worker closure is complete. The candidate is **not accepted or promoted**.

Stage 5 has not started. The next lawful action is fresh independent Tester review of exact
candidate `8462630277b04d431ad393e2b73039cacb5d6247` under the active U06 ExecPlan.
