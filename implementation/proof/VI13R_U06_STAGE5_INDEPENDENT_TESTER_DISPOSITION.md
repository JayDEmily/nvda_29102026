# VI-13R U06 Stage 5 — Independent Tester disposition

**Date:** 2026-09-28
**Role:** fresh independent `TESTER`
**Programme-owner routing:** explicit current instruction to act as the Tester thread and execute the attached candidate
**Reviewed frozen candidate:** `8462630277b04d431ad393e2b73039cacb5d6247`
**Candidate tree:** `0a01dacbf54f61bd7f60cf5e68cc350c3cf8d0c6`
**Disposition:** `PASS`

## 1. Scope and candidate identity

The Tester reviewed the exact Stage-4 U06 candidate required by the active `EXEC_PLAN.md`.

The supplied handoff repository was at later documentation commit
`5224b928117cf12e1213e44cac4afdc09435e628`. The only paths changed between the frozen candidate
and that handoff commit were:

- `handoff/control/CURRENT_STATE.md`;
- `implementation/proof/VI12R_U06_STAGE4_WHOLE_CANDIDATE_EVIDENCE.md`.

No production, test, architecture/configuration or dependency bytes changed after the frozen
candidate. Independent execution was performed in a detached worktree at the exact candidate commit
and tree above. That candidate worktree remained clean.

## 2. Authority and source-level trace

The review traced the current `GUARDRAILS.md`, applicable `AGENTS.md` instructions, active
`EXEC_PLAN.md`, accepted BICP/IWO U06 obligations, relevant historical U06 review findings, realised
A00 composition source, M00 public seam and PostgreSQL constructor boundary.

The source trace established for the reviewed candidate:

- production `create_application(postgres_dsn=...)` constructs the admitted private technical
  PostgreSQL persistence dependency and injects it into the admitted M00 owner;
- the proof-only owner-factory path is mutually exclusive with the production PostgreSQL path;
- A00 stores only the M00 owner in the ordinary application object graph;
- A00 obtains M00 `commands` and `reads` and performs the admitted sequence through those facets;
- policy identity/version is checked against the exact policy returned by M00 registration before
  capture progression;
- capture, observation, relation, assessment and readback arguments use the authorised caller inputs
  or exact preceding M00 results as required;
- A00 does not calculate Raw Signal assessment outcomes or eligibility semantics;
- A00 contains no SQL/table/repository mutation path. Its only private M00 import is the explicitly
  admitted `create_postgres_persistence` construction exception;
- no reverse M00 -> A00 source dependency was found;
- no P01, K01, DMPV3 packet-carrier, provider/network or downstream-consumer activation was found in
  the U06 composition path.

The PostgreSQL constructor itself was inspected: it owns connection/schema/transaction mechanics
inside the M00 private technical module and exposes only the persistence port returned for A00
injection.

## 3. Independent proof environment

The supplied offline proof environment was independently verified and reconstructed as:

- Python `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4`;
- PostgreSQL `17.9`;
- Unix-socket PostgreSQL with `fsync=on`, `synchronous_commit=on`, and `full_page_writes=on`.

The bootstrap bundle does not itself provide PyYAML, which the architecture checks require. The
already-present PyYAML `6.0.3` package was exposed as a narrow `PYTHONPATH` overlay while retaining
pytest and the remaining proof dependencies from the reconstructed environment. Candidate bytes were
not modified.

## 4. Independent validation

Against exact candidate `8462630277b04d431ad393e2b73039cacb5d6247`:

- product-proof control validation: **PASS**, 13/13 required product obligations covered across the
  six admitted physical product families;
- admitted product cases outside the PostgreSQL-heavy U05 family: **424/424 passed**;
- admitted U05 product cases, executed in four bounded groups: **55/55 passed**;
- therefore every admitted product case received an explicit result: **479/479 passed**;
- supplemental U05 Stage-2–5 restart proof: **27/27 passed**;
- U06 construction/delegation/real-PostgreSQL closure set: **15/15 passed**;
- architecture/bootstrap: **74/74 passed**;
- structural architecture validation: **PASS**, zero dependency/public-seam violations;
- dependency-direction/cycle validation: **PASS**;
- public-seam validation: **PASS**;
- mypy: **success, 16 source files**;
- Ruff: **passed**;
- candidate `git diff --check`: **PASS**;
- candidate `git fsck --full`: exit `0`; six dangling blobs were reported diagnostically with no
  integrity failure.

The monolithic aggregate product-proof invocation exceeded the available single-command execution
window while progressing through the PostgreSQL-heavy U05 family; it did not emit an assertion
failure. That incomplete invocation is not counted as a pass. The Tester instead collected the exact
55 U05 node IDs and executed them in bounded groups, alongside the other 424 admitted cases, so all
479 admitted product cases have explicit green results.

## 5. Fixture-independent production-path challenge

To satisfy reviewer fixture-independence, the Tester exercised a manually constructed authority-derived
sequence through the declared public production seam without using the Worker helper fixture.

The challenge:

- constructed typed public policy/observation/identity values directly;
- created A00 via `create_application(postgres_dsn=...)` with the production PostgreSQL-backed M00
  owner;
- ran policy -> capture -> observation -> relation -> assessment -> referential-read;
- observed M00-owned assessment outcome `one_or_more_received` with exact supplied assessment
  evidence timestamp;
- observed one durable row in each material semantic table;
- reconstructed a fresh production application and repeated the same sequence, obtaining the same
  semantic result without duplicate durable rows;
- supplied a deliberately mismatched caller policy reference and observed fail-closed rejection
  before capture progression, with durable row counts unchanged;
- inspected the ordinary A00 object graph and found no direct transaction, PostgreSQL adapter or
  durability-port attribute exposed by `Application`.

Observed durable counts were `(1, 1, 1, 1)` after the first sequence, after the fresh-application
retry, and after the rejected policy-reference challenge.

## 6. Historical U06 risk findings

The relevant prior U06 proof-review findings were inspected as risk evidence:

- complete A00 command/read argument wiring, not merely command order;
- capture policy identity must derive from the exact registered/effective M00 policy result.

The reviewed candidate contains direct proof for both risks, and the independent source/production
challenge found no residual defect of either class. Because this review returns `PASS`, no recurrence
classification is required.

## 7. Disposition

`PASS`.

No material U06 Stage-5 defect is established by this independent review. This is fresh Tester
acceptance of exact candidate `8462630277b04d431ad393e2b73039cacb5d6247` / tree
`0a01dacbf54f61bd7f60cf5e68cc350c3cf8d0c6`; it is not programme promotion.

The next lawful action under the active `EXEC_PLAN.md` is Stage 6: preserve this Tester disposition,
promote the exact accepted U06 lineage into `main` with ancestry preserved, record exact
candidate/review/promotion identities, update current-state authority, verify post-candidate byte
identity and Git integrity/readback, and stop. No U07 is authorised by the current plan.
