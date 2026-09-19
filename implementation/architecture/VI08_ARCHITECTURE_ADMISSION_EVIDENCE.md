# VI-08 Architecture Admission Evidence — Recovered Execution

## Status

`WORKER_CANDIDATE`

This evidence records the VI-08 architecture-admission execution reconstructed on 2026-09-20 after the prior sandbox runtime lost its unpreserved Worker Git object database. It does not reuse or claim the lost commit identities. The reconstruction starts from the exact attached thin Worker 001 Git transport and re-derives the VI-08 state from the governing handoff and current authority.

## Baseline

Attached Worker 001 transport repository:

- transport HEAD: `8133432ba8a07e4d04d83b14af5c3c4bd12e6b0e`
- transport tree: `2220077c621eb9fef5b9b2cd37377c6926ff148a`
- authoritative pre-implementation source recorded by the Worker brief: `d095954c16a9818eadb60d6364148229f2dc4558`
- PM handoff source recorded by the Worker brief: `7795705727d8ac2935949ba9e4acce672fa463a1`

The recovered execution does not reconstruct omitted historical Git ancestry; it preserves the thin transport ancestry exactly as supplied.

## Pre-mutation implementation-authority check

Command on untouched transport state:

```text
python tools/validate_implementation_authority.py \
  --binding implementation/authority/implementation_authority_binding.yaml \
  --brief handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md
```

Observed:

```text
PASS: implementation authority brief_sha256=938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342
candidate_targets: create:raw_signal_occurrence_truth->M00, modify:A00
```

Untouched baseline proof also passed before mutation:

- structural architecture validation: PASS;
- architecture/bootstrap tests: `74 passed`;
- `architecture_kernel` promotion set: PASS, 11 resolved test paths;
- mypy: `Success: no issues found in 13 source files`;
- Ruff: `All checks passed!`.

## Mutation

The VI-07 architecture design was applied:

- M00 admitted as active `raw_signal_occurrence_truth` owner;
- package `nvda_desk.raw_signal_occurrence_truth` and public seam `nvda_desk.raw_signal_occurrence_truth.api` created;
- A00 permitted dependency extended by exactly M00;
- exactly one declared owner edge added: `A00 -> M00`;
- exactly one durable implementation allocation added for M00;
- no Raw Signal product implementation was added.

### Necessary proof-fixture updates

The lawful admission made five architecture test files stale because they encoded the historical empty-module/empty-allocation state or constructed synthetic module registries while retaining the now-real A00 -> M00 dependency.

The following files were updated under explicit Programme Owner authority to preserve their existing propositions against the newly admitted architecture state:

- `tests/architecture/test_activation_readiness.py`
- `tests/architecture/test_dependency_direction.py`
- `tests/architecture/test_identifier_taxonomy.py`
- `tests/architecture/test_implementation_authority_ingress.py`
- `tests/architecture/test_registry_schema.py`

No test was removed, skipped, downgraded, de-admitted or semantically weakened. Synthetic fixtures that replace the real module set now also remove the real A00 -> M00 binding inside that synthetic repository so they remain internally coherent. Current-state allocation/candidate expectations now reflect consumed M00 and next candidate M01.

## Post-mutation validation before commit

Observed results:

```text
python tools/validate_architecture.py
PASS: structural architecture validation
architecture objects: 5
active runtime modules: 1
implementation allocations: 1
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0

python -m pytest tests/architecture tests/bootstrap -q
74 passed

python -m mypy src
Success: no issues found in 15 source files

ruff check src tests tools
All checks passed!

nvda-check-dependencies
PASS: dependency direction and cycle validation

nvda-check-public-seams
PASS: public-seam validation

git diff --check
PASS (no output)
```

## Changed paths

Architecture-admission paths:

```text
config/architecture/application_shells.yaml
config/architecture/dependency_rules.yaml
config/architecture/implementation_allocations.yaml
config/architecture/modules.yaml
src/nvda_desk/raw_signal_occurrence_truth/__init__.py
src/nvda_desk/raw_signal_occurrence_truth/api.py
implementation/architecture/VI08_ARCHITECTURE_ADMISSION_EVIDENCE.md
```

Separately authorised proof-fixture/current-state updates:

```text
tests/architecture/test_activation_readiness.py
tests/architecture/test_dependency_direction.py
tests/architecture/test_identifier_taxonomy.py
tests/architecture/test_implementation_authority_ingress.py
tests/architecture/test_registry_schema.py
```

## Product-behaviour boundary

The admitted package contains only module docstrings:

- `__init__.py`: package description only;
- `api.py`: public-seam description only.

No product decision logic, persistence implementation, provider/network integration, replay, P01/DMPV3, K01, downstream consumer, live external effect/account capability or product proof was added in VI-08.

## Clean committed-state promotion

Pending at the time this record is first committed. The recovery execution must run `python tools/run_promotion_gate.py --set architecture_kernel` from the clean committed candidate and record the resulting commit/tree in a successor evidence update before VI-08 recovery is treated as closed.
