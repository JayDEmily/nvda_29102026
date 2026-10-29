# VI12R U06 Stage 1 — A00 production construction/lifecycle evidence

## Status

**WORKER STAGE 1 COMPLETE — STAGE 2 NOT STARTED.**

This record is Worker evidence for U06 Stage 1 only. It is not U06 acceptance, Tester review,
or promotion.

## Governing boundary

- Active plan commit on `main`: `c3ae566ff8367d83dc783289d9b553faa9a51325`.
- U06 Stage 1 purpose: establish the minimum truthful A00 production construction/lifecycle
  boundary before implementing the sequential Raw Signal use case.
- Stage 1 implementation/proof commit: `674621f7c4c548f382b709c6ba0a7aa13a4dfc0c`.
- Stage 1 implementation/proof tree: `531dee18cccc76b18279f518280500c63ce32b32`.
- Work branch: `work/u06-a00-composition`.

## Changed paths in the Stage 1 implementation/proof commit

- `src/nvda_desk/composition/__init__.py`
- `config/architecture/dependency_rules.yaml`
- `config/product_proof/families.yaml`
- `tests/product/raw_signal/test_u06_a00_composition.py`
- `tests/product/raw_signal/test_u06_stage1_a00_construction.py`

No file under `src/nvda_desk/raw_signal_occurrence_truth/**` changed in Stage 1.

## VERIFIED construction proposition

The committed Stage 1 tree establishes the following bounded construction behaviour:

1. `nvda_desk.composition.create_application` now exists as the A00 production construction seam.
2. The production-default construction path requires a non-empty PostgreSQL DSN.
3. A00 constructs the accepted non-owning PostgreSQL mechanism with
   `create_postgres_persistence(dsn)` and injects that exact technical dependency into the M00
   `create_owner(..., durability_port=...)` construction seam.
4. The returned `Application` retains only the constructed M00 owner. A00 does not retain the
   PostgreSQL adapter as a separate application capability.
5. The proof-only owner-factory injection path remains bounded to substituting the M00 owner for
   delegation proof; no public persistence-factory injection surface was added.
6. A00 contains no Raw Signal policy/capture/observation/relation/assessment decision logic.
7. The accepted owner edge remains exactly `A00 -> M00`; no reverse, P01, K01 or downstream edge
   was introduced.

## Technical-constructor seam treatment

The accepted IWO requires A00 to construct/inject the non-owning PostgreSQL adapter while the
registered M00 semantic public seam remains `nvda_desk.raw_signal_occurrence_truth.api`.

Stage 1 therefore records one explicit and symbol-specific architecture exception:

`A00 -> M00 : nvda_desk.raw_signal_occurrence_truth._postgres.create_postgres_persistence`

The U06 proof constrains this exception to that exact technical constructor. It does not admit
M00 private semantic state, tables, repository mutation, `_PostgresPersistence` internals or any
other private symbol as an A00 semantic API.

## Lifecycle trace

The accepted U05 PostgreSQL mechanism opens/closes its connection during schema initialisation and
opens/closes one connection per transaction. It exposes no long-lived startup/shutdown resource
contract for A00 to own. Stage 1 therefore deliberately adds no artificial `start`, `stop`, `close`
or `shutdown` application lifecycle API.

## Proof environment

The preserved offline proof environment was reconstructed and verified before Stage 1 proof:

- CPython `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4` / psycopg-binary `3.3.4`;
- PostgreSQL `17.9`;
- UTF8;
- `fsync=on`;
- `synchronous_commit=on`;
- `full_page_writes=on`;
- Unix-domain-socket transport.

PyYAML `6.0.3` was supplied from the already-present project host environment on `PYTHONPATH` for
architecture/proof files that import YAML; no network installation occurred and no repository file
was changed for that overlay.

## Post-commit validation against exact Stage 1 implementation commit

### Focused Stage 1 construction proof

Command:

`pytest -q tests/product/raw_signal/test_u06_stage1_a00_construction.py`

Result: **5 passed**.

This includes construction of the real PostgreSQL-backed default application path using
`NVDA_TEST_POSTGRES_DSN`.

### Architecture/bootstrap

Command:

`pytest -q tests/architecture tests/bootstrap`

Result: **74 passed**.

This includes the repository dependency analyser accepting the one exact technical-constructor
exception while preserving the declared `A00 -> M00` owner edge.

### Accepted U01-U04 predecessor regression set

Command scope:

- `test_u01_contract_owner_boundary.py`
- `test_u02_capture_schedule.py`
- `test_u03_observation_native_temporal.py`
- `test_u04_receipt_assessment.py`

Result: **416 passed**.

### Static checks

- mypy over `src`: **Success: no issues found in 16 source files**.
- Ruff over `src tests tools`: **All checks passed**.
- `git diff HEAD^..HEAD --check`: **PASS**.
- modified YAML documents: `yaml.safe_load` **PASS**.

## Deliberately UNPROVED at Stage 1

The complete U06 product family was executed as a stage-state discriminator:

`pytest -q tests/product/raw_signal/test_u06_a00_composition.py`

Observed result: **5 passed / 2 failed**.

Both failures are exactly the absent Stage 2 sequential application method
`Application.run_raw_signal_proof_sequence`. They do not indicate a failed Stage 1 invariant; the
active ExecPlan explicitly does not require the full sequential business path to be implemented or
green at Stage 1.

Accordingly Stage 1 does **not** claim:

- policy -> capture -> observation -> relation -> assessment -> readback orchestration;
- caller policy-reference mismatch handling in A00;
- whole-U06 real PostgreSQL sequential composition;
- U06 candidate closure, independent Tester acceptance or promotion.

Those remain later-stage obligations.

## Stage 1 exit

The exact Stage 1 implementation/proof state is committed and clean at
`674621f7c4c548f382b709c6ba0a7aa13a4dfc0c` / tree
`531dee18cccc76b18279f518280500c63ce32b32`.

Stage 2 has not begun.
