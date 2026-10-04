# DS-T01 — foundation proof boundary evidence

## Status and claim boundary

**AUTONOMOUS WORKER CANDIDATE EVIDENCE — foundation proof authored before DS-I01 production implementation; foundation implementation PASS is not claimed.**

DS-T01 establishes executable proof for the already-admitted foundation boundary required by REQ-003, REQ-004, REQ-005, REQ-008 and REQ-010. The proof is intentionally expected-red where DS-I01 production behaviour or the mandatory PostgreSQL proof environment does not yet exist. It does not implement M00 projection behaviour, create the M01 source package, establish database roles/schemas, calculate any `Dxxx`, or claim DS-I01 acceptance.

## Accepted predecessor and execution state

DS-A04 independent review was admitted before DS-T01 entry:

- reviewed repair commit/tree: `7fff5cec71f6a1635ec9771ddbc225c391683cf9` / `59a73a0cb4f25bb58d6241a393a3a1cea55f881e`;
- review packet SHA-256: `0b300704527a2cc74a035dd1b4e221e33a726e0509f18721e33d04a35d2f201d`;
- reviewer result internal SHA-256: `449e85697b9cdc7c6c2ebd5f3281b5ad36abc61313ece5afe16178843cbfd706`;
- preserved reviewer-result file SHA-256: `65272d69c5b8c18a5eff22ea35193ef8bdfa4b2186412c6e63b666d9532d389a`;
- reviewer actor instance: `90a693b05a379582a3d4b5b77158b636`;
- verdict/route: `pass` / `PASS`;
- acceptance commit/tag: `ad5508f65760dc1b1949f067223f35cdc3e46cfb`, `accepted/DS-A04`;
- post-admission controller checkpoint: `cfec16ba3cb79e526558a76466fe03803e2f83a7` / tree `364901195b96171e176ae7389a760c2d447332e7`.

At that admitted state `projectctl ready` routed `DS-T01`, actor class `AUTONOMOUS`.

DS-T01 execution branch:

- branch: `work/ds-t01-foundation-proof-v2`;
- source HEAD/tree: `cfec16ba3cb79e526558a76466fe03803e2f83a7` / `364901195b96171e176ae7389a760c2d447332e7`;
- worker session actor instance: `92d8552e11233094bd4348f4ccab41b7`;
- generated context size: 44,657 bytes.

A first branch-entry attempt created historical commit `629d3bfd...` containing only an LCR branch transition. `projectctl check` rejected that shape because the LCR checkpoint source no longer matched the immediate first parent. No proof or production bytes were changed in that failed branch. The current branch uses the repository-prescribed coalesced pattern: branch admission and first lawful DS-T01 work are committed together with the regenerated LCR rather than rewriting history or bypassing the invariant.

## Authority-derived proof surface

The accepted brief and work order require foundation proof for six bounded areas. DS-T01 maps those obligations to physical proof as follows.

| Authority proposition | Physical proof |
|---|---|
| M00 field-level projection requires one exact `RawSignalProjectionMapping`; missing/ambiguous mappings or missing field/units refuse output | `tests/product/derived_signal/test_ds_t01_m00_projection.py` |
| Projected raw values preserve native value/units and source/mapping/temporal/receipt/subject/revision lineage; raw history is bounded, deterministic and paginated without duplication | `tests/product/derived_signal/test_ds_t01_m00_projection.py` |
| Required non-signal contexts are immutable/version-identified; unit conversion is explicit and rejects unit mismatch/magnitude heuristics | `tests/product/derived_signal/test_ds_t01_foundation_contract.py` |
| Derived occurrence carrier exposes exact identity, version, time, result shape and raw/predecessor/convention lineage; public reads distinguish absence from a value | `tests/product/derived_signal/test_ds_t01_foundation_contract.py` |
| M00 and M01 use distinct PostgreSQL user/schema boundaries and M01 lacks read/write privilege on M00-owned relations; M01 persistence factory remains private mechanism | `tests/implementation/derived_signal/test_ds_t01_persistence_isolation.py` |
| M01 never imports M00 private persistence/raw occurrence carrier, references M00 private table names directly, or introduces external-effect client/command surfaces | `tests/implementation/derived_signal/test_ds_t01_source_boundaries.py` |

The public-symbol spellings used by these tests are executable mechanism contracts for DS-I01, not changes to accepted Derived Signal mathematics, package/distribution identity or downstream effect authority. The architecture-admitted Python owner/public seam remains `nvda_desk.derived_signal_calculation_truth` / `nvda_desk.derived_signal_calculation_truth.api`.

## Collected proof

Command:

```text
PYTHONPATH=src /mnt/data/ds_a03_proof_env/venv/bin/python -m pytest --collect-only -q \
  tests/product/derived_signal tests/implementation/derived_signal
```

Observed:

```text
27 tests collected in 0.03s
```

Collected cases comprise:

- 4 M00 projection/history tests;
- 15 immutable/version-identified context-type instances;
- 4 additional M01 public-contract tests (unit conversion, occurrence carrier, absence semantics, no external-effect commands);
- 2 PostgreSQL persistence/isolation tests;
- 2 source-boundary tests.

No test skips missing production implementation, a missing required mapping or an absent PostgreSQL proof boundary.

## Expected-red pre-implementation execution

Command:

```text
PYTHONPATH=src /mnt/data/ds_a03_proof_env/venv/bin/python -m pytest -q \
  tests/product/derived_signal tests/implementation/derived_signal
```

Observed:

```text
27 failed in 0.06s
```

The failures are attributable to the intended pre-implementation/proof-environment boundary:

- 19 tests require the not-yet-created `nvda_desk.derived_signal_calculation_truth.api` public seam/types;
- 4 tests require the not-yet-implemented M00 typed raw projection symbols/read methods;
- 1 PostgreSQL boundary test fails closed because `NVDA_TEST_M00_POSTGRES_DSN` (and therefore the paired M01 proof boundary) is not configured in this Worker execution;
- 1 test requires the not-yet-created M01 private PostgreSQL persistence mechanism;
- 2 source-boundary tests require the not-yet-created M01 source package.

The PostgreSQL test does not substitute SQLite, an in-memory persistence fixture or a shared writer identity for the absent real proof DSNs. The implementation task must provide/exercise the real separated roles/schemas before this proposition can become green.

This expected-red disposition is proof-first evidence only. It is not a semantic or implementation PASS.

## Existing architecture regression proof

DS-T01 does not modify architecture registry/allocation/dependency/public-seam state. The current architecture/bootstrap proof was re-run with the preserved Python 3.13/PostgreSQL proof environment, the existing host PyYAML dependency, and a process-local Git `safe.directory` setting required only because the extracted handoff ownership differs from the runtime user.

Observed:

```text
python -m pytest tests/architecture tests/bootstrap -q
74 passed in 2.09s

python tools/validate_architecture.py
architecture objects: 6
active runtime modules: 1
implementation allocations: 2
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation
```

An earlier run without the process-local Git safety setting produced `73 passed, 1 failed`; the sole failure was Git's extracted-directory ownership refusal inside `validate_implementation_authority.py`, not an architecture assertion. No repository/global Git configuration was changed to obtain the clean rerun.

## Change boundary

DS-T01 changes only its authorised proof surfaces:

- `tests/product/derived_signal/__init__.py`;
- `tests/product/derived_signal/_support.py`;
- `tests/product/derived_signal/test_ds_t01_m00_projection.py`;
- `tests/product/derived_signal/test_ds_t01_foundation_contract.py`;
- `tests/implementation/derived_signal/test_ds_t01_persistence_isolation.py`;
- `tests/implementation/derived_signal/test_ds_t01_source_boundaries.py`;
- this `implementation/proof/DS_FOUNDATION_PROOF_EVIDENCE.md`.

No `src/**`, architecture registry/allocation, package metadata, schema, accepted brief, requirement, task/delegation or governance meaning is changed by the proof authoring itself.

## Claim boundary

This evidence establishes only that the DS-T01 foundation proof boundary has been physically authored, collected and exercised expected-red before production implementation, while the inherited architecture proof remains green.

It does **not** establish that M00 projection or M01 foundation behaviour is implemented, that PostgreSQL role/schema isolation has passed, that any `Dxxx` is calculable, that DS-I01 is accepted, or that later kernel/integration/package proof has been reached.
