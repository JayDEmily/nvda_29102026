# AKR-7.3 complete proof and promotion evidence

## Scope

AKR-7.3 establishes that the complete current architecture/bootstrap blocking proof population and the registry-derived `architecture_kernel` promotion set cover the same admitted proof jurisdiction and execute successfully from a clean committed predecessor state. This leaf does not prove packaging, semantic exclusion/behaviour-neutrality, or terminal readiness.

## Rehydrated predecessor

The volatile post-AKR-7.2 worktree from the earlier execution was unavailable. Execution was therefore rehydrated from the durable user-visible AKR-7.2 checkpoint archive:

- archive: `NVDA_AKR7_2_STATIC_ARCHITECTURE_TRACE_CHECKPOINT_20260910.tar.gz`
- archive SHA-256: `0fe3d37de9f325508c9e3a15eb9c171c8e268df7bc4ab920163e2e81ea396182`
- branch: `work/akr-7-final-pristine-kernel-proof`
- HEAD: `84e1e284317e66edeb0c3705e6c24a5a9a75d438`
- tree: `8a6ef3b6a6f501f2197b0bf8fbb2a2487e1bb643`

The included complete Git bundle was cloned and verified before this leaf. AKR-7.3 then began on independent branch `work/akr-7.3-complete-proof` from that exact commit.

## Human-read proof path

Before relying on green output, the following current proof-control surfaces were read together:

- `config/proof/test_families.yaml`
- `config/proof/proof_blocks.yaml`
- `config/proof/promotion_sets.yaml`
- `schemas/test_family.schema.json`
- `schemas/proof_block.schema.json`
- `schemas/promotion_set.schema.json`
- `src/nvda_desk/architecture/proof.py`
- `src/nvda_desk/architecture/promotion.py`
- `src/nvda_desk/architecture/validation.py`
- `tools/run_promotion_gate.py`
- `tests/AGENTS.override.md`
- all eleven Python files physically present below `tests/architecture/` and `tests/bootstrap/`.

The loader validates the three proof documents against their schemas, rejects duplicate IDs/paths, recursively discovers `test_*.py` below both governed test roots, requires exact equality between physical and admitted paths, requires each family to belong to exactly one compatible proof block, and requires current-blocking families to be reachable through a promotion set. `ProofState.paths_for_set()` resolves paths through the configured promotion-set -> proof-block -> family graph. The promotion runner requires an initially clean worktree, invokes aggregate architecture validation, resolves the configured test paths, executes those paths with the current interpreter, and rejects any worktree mutation caused by promotion.

## Environment reconstruction repeated for this rehydrated execution

Because the earlier external AKR-7.1 environment did not persist, its already-authorised offline reconstruction was repeated rather than using an inherited environment.

Commands:

```text
(cd vendor/wheels && sha256sum -c SHA256SUMS)
UV_OFFLINE=1 UV_PYTHON_DOWNLOADS=never uv lock --check --offline
UV_OFFLINE=1 UV_PYTHON_DOWNLOADS=never \
  UV_PROJECT_ENVIRONMENT=/mnt/data/nvda_akr7_env \
  uv sync --frozen --offline --extra dev --python 3.13.5
```

Observed:

- all 15 wheel hashes matched the committed manifest;
- offline lock resolution resolved 13 packages;
- a new external environment was created with CPython 3.13.5;
- the environment contained pytest 9.0.3, mypy 1.20.1 and PyYAML 6.0.3;
- repository Git status remained unchanged by reconstruction.

## Proof-jurisdiction reconciliation

A direct call through `load_and_validate_proof_state()` and recursive physical discovery established:

```text
physical_count 11
admitted_count 11
resolved_count 11
physical_eq_admitted True
resolved_eq_admitted True
```

The resolved paths were exactly:

```text
tests/architecture/test_activation_readiness.py
tests/architecture/test_dependency_direction.py
tests/architecture/test_identifier_taxonomy.py
tests/architecture/test_implementation_authority_ingress.py
tests/architecture/test_object_lifecycle.py
tests/architecture/test_proof_control.py
tests/architecture/test_public_seam_law.py
tests/architecture/test_registry_schema.py
tests/architecture/test_static_typecheck.py
tests/bootstrap/test_legacy_exclusion.py
tests/bootstrap/test_minimal_imports.py
```

## Complete blocking proof

Command:

```text
PYTHONPATH=src /mnt/data/nvda_akr7_env/bin/python -m pytest tests/architecture tests/bootstrap
```

Observed:

```text
platform linux -- Python 3.13.5, pytest-9.0.3, pluggy-1.6.0
collected 74 items
74 passed in 2.17s
```

The test population includes negative enforcement fixtures for incomplete active-owner projection, missing physical package/public seam, forbidden dependency direction, undeclared edges, module cycles, dynamic imports, private/public-seam bypass including `from nvda_desk import m02`, proof admission mismatches including nested physical tests, implementation-authority ingress failure modes, typed public-seam misuse and removed-runtime exclusion. Green execution is therefore evidence for those encoded propositions, not domain behaviour.

## Registry-derived promotion

Immediately before promotion, `git status --porcelain=v1` was empty.

Command:

```text
PYTHONPATH=src /mnt/data/nvda_akr7_env/bin/python tools/run_promotion_gate.py --set architecture_kernel
```

Observed architecture/promotion preamble:

```text
architecture objects: 4
active runtime modules: 0
implementation allocations: 0
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0
promotion set: architecture_kernel
resolved test paths: 11
```

The promotion execution collected the same 74 tests and reported `74 passed in 1.41s`. `git status --porcelain=v1` remained empty afterwards, so the promotion path did not mutate the repository.

## Semantic acceptance

The written proof jurisdiction, recursive physical discovery, admitted family registry and registry-derived promotion resolution agree on exactly eleven current blocking files. Both the complete blocking population and the aggregate promotion path exercised those same paths successfully from the clean predecessor state. No test, schema, validator or promotion criterion was changed to obtain this result.

This establishes AKR-7.3 only. Packaging remains AKR-7.4; active-tree/distribution behaviour-neutrality and exclusion remain AKR-7.5; terminal reconciliation remains AKR-7.6.
