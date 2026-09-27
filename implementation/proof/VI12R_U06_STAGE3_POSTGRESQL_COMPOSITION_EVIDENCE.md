# VI12R U06 Stage 3 — real production PostgreSQL/M00 sequential-composition evidence

## Status

**WORKER STAGE 3 COMPLETE — STAGE 4 NOT STARTED.**

This record is Worker evidence for U06 Stage 3 only. It is not a frozen whole-U06 candidate,
independent Tester acceptance, or promotion.

## Governing boundary

- Active U06 ExecPlan on `main`: `c3ae566ff8367d83dc783289d9b553faa9a51325`.
- Stage 2 implementation predecessor: `af3bc77349ccaff943f3eabbcce2e25612a42e3b`.
- Stage 2 evidence/handoff predecessor: `22f79bf41ce8a62cd3acdc9349c67cdf605e3582`.
- Stage 3 implementation/proof commit: `36e694ee111db5ab45acc298fc7486f1fdc6ac4b`.
- Stage 3 implementation/proof tree: `8de8247657d4c88370b491d964eeea0b90834087`.
- Work branch: `work/u06-a00-composition`.

## Changed paths in the Stage 3 implementation/proof commit

- `src/nvda_desk/composition/__init__.py`
- `tests/product/raw_signal/test_u06_stage3_postgresql_composition.py`

No file under `src/nvda_desk/raw_signal_occurrence_truth/**` changed.

## Stage 3 configuration discovery

The production M00 path correctly fails closed when in-slot evidence requires eligibility
adjudication but no separately admitted eligibility resolver is configured. IWO-U06 authorises A00
to construct/inject technical/configuration inputs, while the IWO eligibility boundary requires the
resolver to remain separately admitted/configured and prohibits A00/provider fixtures from silently
defining new Raw Signal semantics.

Stage 3 therefore adds one bounded A00 construction input:

`raw_signal_eligibility_resolver`

A00 forwards this callable unchanged to the M00 public `create_owner(...)` seam. A00 never invokes
it itself and contains no eligibility rule or Raw Signal outcome selection. If it is absent, M00's
existing fail-closed semantics remain unchanged.

## VERIFIED real production-composition proposition

Against the authorised PostgreSQL 17.9 / Psycopg 3.3.4 environment, the committed Stage 3 tree
establishes:

1. `create_application(postgres_dsn=..., raw_signal_eligibility_resolver=...)` follows the production
   default path and constructs the accepted PostgreSQL durability mechanism plus M00 owner.
2. `Application.run_raw_signal_proof_sequence(...)` executes the authorised policy -> capture ->
   observation -> relation -> assessment -> referential-read sequence through M00 command/read
   facets only.
3. The representative positive path yields a receipt relation and M00-derived
   `one_or_more_received` assessment when the separately configured eligibility authority returns
   true for the exact durable observation/effective policy facts.
4. PostgreSQL contains exactly one durable policy, capture, observation and assessment record after
   the sequence.
5. A completely fresh production `Application` against the same database performs an exact retry,
   returns the same semantic records and leaves each durable record count at one.
6. The application ordinary attribute/slot graph exposes no object with a PostgreSQL
   `transaction` capability under the already-accepted bounded public-seam proof law.
7. Deleting the application objects and forcing ordinary garbage collection does not mutate the
   durable facts; A00 invents no lifecycle side effect.
8. No P01, K01, provider network or downstream consumer is required by this path.

## Proof environment

- CPython `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4` / psycopg-binary `3.3.4`;
- PostgreSQL `17.9`;
- Unix-domain-socket DSN from `NVDA_TEST_POSTGRES_DSN`;
- PyYAML `6.0.3` supplied from the already-present host environment on `PYTHONPATH` for tests that
  import YAML; no network installation and no repository dependency mutation.

## Post-commit validation against exact Stage 3 implementation commit

### Stage 1–3 U06 proof set

Command scope:

- `test_u06_stage1_a00_construction.py`;
- `test_u06_a00_composition.py`;
- `test_u06_stage3_postgresql_composition.py`.

Result: **13 passed**.

Within that set:

- accepted U06 delegation/dataflow family: **7/7 passed**;
- focused real PostgreSQL production-composition discriminator: **1/1 passed**.

### Accepted U01-U04 predecessor regression

Result: **416/416 passed**.

### Accepted U05 restart predecessor slice

Result: **27/27 passed** across Stage-2 through Stage-5 restart files.

### Configured U05 real-PostgreSQL durability family

The 55-case file was executed in four bounded batches to stay below the execution-window limit:

- cases 1–15: **15/15 passed**;
- cases 16–30: **15/15 passed**;
- cases 31–45: **15/15 passed**;
- cases 46–55: **10/10 passed**.

Aggregate: **55/55 passed**.

One Python `multiprocessing` fork deprecation warning was emitted in the final batch; no assertion
or integrity failure occurred.

### Architecture/bootstrap and static checks

- architecture/bootstrap: **74/74 passed**;
- mypy over `src`: **Success: no issues found in 16 source files**;
- Ruff over `src tests tools`: **All checks passed**;
- `git diff HEAD^..HEAD --check`: **PASS**.

## Deliberately UNPROVED at Stage 3

Stage 3 does not perform the whole-U06 adversarial closure or source-level ownership trace required
by Stage 4. It therefore does not yet claim:

- one frozen complete U06 Worker candidate;
- independent whole-U06 challenge of all IA17-PROD-013 / ARCH-004/005/006 false positives;
- fresh independent Tester acceptance;
- promotion to `main`.

## Stage 3 exit

The real production PostgreSQL/M00 sequential-composition implementation/proof state is committed
at `36e694ee111db5ab45acc298fc7486f1fdc6ac4b` / tree
`8de8247657d4c88370b491d964eeea0b90834087`.

Stage 4 has not begun at this evidence boundary.
