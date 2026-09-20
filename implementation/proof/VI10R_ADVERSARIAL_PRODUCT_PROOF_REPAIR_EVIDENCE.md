# VI-10R — Adversarial Product Proof Repair Evidence

## Status

`SUCCESSOR PROOF CANDIDATE — PRE-IMPLEMENTATION — PENDING FRESH VI-11 RECHALLENGE`

This record is proof-layer evidence only. It does not claim product implementation, product
semantic acceptance, VI-11 acceptance, or authority to enter VI-12R.

## Bound predecessor and reviewer finding set

- failed VI-10 physical proof target:
  `f83efd9b489dbe7072da8c96320504a468c55a1a`
- failed VI-10 physical proof tree:
  `beba36d889696915bbcecccd861dab9ab0c1a4cd`
- VI-11 reviewed submission:
  `e778df15d7a478741cde53ffe8a0373e59e2820e`
- VI-11 submission tree:
  `4612b37480e5145d769a88cf73590b511273ae1c`
- Tester Iteration 003 response SHA-256:
  `74a39cc175d3d34837971b76e78007fd891940ca7a3d5db76af7036a5df9a482`
- repair-control baseline:
  `e3fe1344b4b8b87adac47d5a2771c1b66ec6e03f`
- repair-control baseline tree:
  `8b0dee55c6bb050b46bae30611438a778a7cc381`

The six returned findings are `T003-F001` through `T003-F006`. The failed proof candidate
remains in ordinary Git history; this repair is a successor.

## Authority reread before mutation

Worker 005 reread the current repository governance, accepted `EXEC_PLAN.md`, the six exact
routed METHOD-006 normative authorities, exact IRB/BICP/IWO, `tests/AGENTS.override.md`, the
current architecture/bootstrap proof corpus, and the preserved historical Tier A/B/C testing
method evidence before changing the physical product proof.

No upstream semantic or architecture authority was changed.

## Finding-to-repair map

### T003-F001 — real PostgreSQL durability/restart process boundary

Repaired by:

- `tests/product/raw_signal/_process_probe.py`, which invokes only the production public
  `create_owner` path and fixed proof specimens from a genuinely separate Python process;
- U05 write/read, assessment history, retry/conflict, failed-write and restart cases that use
  distinct subprocesses and assert distinct process IDs;
- each subprocess receives a fresh working directory, `HOME`, `TMPDIR` and `XDG_DATA_HOME`, so
  same-process or ordinary per-user/per-CWD local state cannot stand in for durability;
- direct PostgreSQL user-table row-count change is observed around a committed semantic write;
- an otherwise valid semantic read is attempted with a deliberately invalid PostgreSQL DSN and
  must fail rather than fall back to alternative local state;
- failed-write absence is observed by a later fresh process;
- restart policy write, reconciliation and durable readback cross fresh process boundaries.

The subprocess driver contains no outcome or product-decision logic.

### T003-F002 — production owner/composition path rather than private test semantics

Repaired by:

- `_support.build_owner()` now requires the production public `api.create_owner` factory;
- `_build_test_owner` is no longer a construction path;
- U06 requires production `composition.create_application` rather than
  `_build_test_application`;
- U06 injects only an opaque spy owner factory, records command/read call order, and requires A00
  to return the exact opaque M00 result objects by identity;
- composition-source checks reject private M00 state/table/repository bypass and Raw Signal
  outcome literals.

The remaining occurrences of the old private symbol names are negative assertions proving those
paths are absent, not calls to them.

### T003-F003 — evidence-discriminated assessment outcomes

Repaired by:

- normal `append_assessment()` no longer accepts an `outcome` argument;
- zero is tested with no eligible committed receipt visible at `evidence_as_of_ts_utc`;
- one-or-more is tested only after eligible committed receipt evidence exists;
- caller-supplied `outcome=` is a prohibited path and must fail;
- late evidence first records lawful zero, then admits eligible evidence, then appends
  one-or-more superseding zero without overwrite;
- broken/self/non-immediate supersession remains negative proof;
- `unknown_not_established` creation remains on the authorised missing-owed-slot restart path in
  U05 rather than being caller-selected in U04.

### T003-F004 — policy version non-overlap

Repaired by:

- lawful v2 begins exactly at v1's exclusive `12:02:00Z` deactivation boundary;
- a separate v2-at-`12:01:00Z` case must be rejected as overlapping authority.

### T003-F005 — physical identity substitution matrix

Repaired by:

- U01 parameterised constructor negatives substitute actual concept, contract, scope-policy,
  capture, observation, assessment, provider/native-source and delivery identities across other
  identity positions;
- U03 repeats material observation/delivery/provider/native/scope substitutions at the command
  boundary;
- inactive workbook/run/replay/lineage/packet/universal IDs are tested as prohibited unadmitted
  authority fields rather than invented active layers.

### T003-F006 — contract-wide `.v1` compatibility discrimination

Repaired by U01 with independently collected matrix cases for:

- actual constructor requiredness for all five v1 contracts;
- all required fields rejecting null;
- UTC time fields rejecting naive time values;
- discriminants/allowed values across all five contracts;
- observation provenance requiredness;
- identity-law substitutions;
- lawful optional absence;
- a compatibility discriminator that accepts a synthetic genuinely optional additive field but
  rejects field removal, requiredness drift and new required fields.

No unadmitted v2 contract is invented.

## Physical proof population after repair

`python -m pytest --collect-only -q tests/product/raw_signal`

Result: `155 tests collected`.

Per-family population:

- U01 contract/owner/compatibility: 92 tests;
- U02 schedule/policy: 12 tests;
- U03 observation/native/temporal: 21 tests;
- U04 relation/assessment: 17 tests;
- U05 PostgreSQL durability/restart: 8 tests;
- U06 A00 composition: 5 tests.

Product-proof control validation remains exactly six admitted families covering the same 13/13
current product obligations. Product tier treatment remains `NOT_CLASSIFIED`; the architecture
axis remains separate.

## Pre-implementation execution state

Environment:

- Python 3.13.5;
- pytest 9.0.3;
- Ruff 0.15.11;
- mypy 1.20.1;
- Psycopg 3.3.4 and psycopg-binary 3.3.4 wheels copied from the preserved Project consolidation
  bundle and verified against its `MANIFEST.tsv` SHA-256 values:
  - `b6bbc25ccf05c8fad3b061d9db2ef0909a555171b84b07f29458a447253d679a`;
  - `c677c4ad433cb7150c8cd304a0769ae3bcfbe5ea0676eb53faa7b1443b16d0d3`.

`python -m pytest -q tests/product/raw_signal`

Observed result: `150 failed, 5 passed`.

The red state is expected before VI-12R. Observed failures are attributable to missing production
M00 contract/factory symbols, missing production A00 `create_application`, or the absent mandatory
`NVDA_TEST_POSTGRES_DSN`. There was no collection error or malformed-test import failure.

## Architecture/non-regression checks on the dirty successor worktree

Observed before committing the candidate:

- `python tools/validate_product_proof.py` — PASS, six families, 13/13 obligations;
- `python tools/validate_architecture.py` — PASS;
- `python -m pytest -q tests/architecture tests/bootstrap` — `74 passed`;
- `python -m mypy src` — PASS, no issues in 15 source files;
- `ruff check src tests tools` — PASS;
- `nvda-check-dependencies` — PASS;
- `nvda-check-public-seams` — PASS;
- `git diff --check` — PASS.

## Mutation boundary

The successor repair changes product-proof metadata/support/tests plus this evidence/control layer.
There is no mutation under `src/nvda_desk/**`, `config/architecture/**`, or `config/proof/**`.
IRB/BICP/IWO/METHOD-006 bytes and the 13 accepted product obligations are unchanged.

## Remaining required step

Commit the successor proof candidate, rerun clean-worktree product and architecture aggregate
checks against that exact Git state, bind the final commit/tree in a successor evidence/control
record, and hand the candidate to a fresh independent VI-11 reviewer. VI-12R remains prohibited.
