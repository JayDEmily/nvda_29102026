# DS-A03 — architecture admission evidence

## Scope and claim boundary

This record supports DS-A03 only: durable architecture allocation/boundary admission plus a bounded downstream implementation work order. It does **not** claim DS-A04 independent-review PASS, executable M01 implementation, Derived Signal calculation proof, package release authority or final project acceptance.

Candidate SHA-256 before this evidence record is committed:

`c73128c9144cbb2b107a31e5a524fd7769d7e3b2932019f864d9e38de8b3fe9e  implementation/architecture/DS_ARCHITECTURE_ADMISSION_CANDIDATE.md`

Work-order SHA-256:

`77ec86a9cf9b3357d913a401985ed203a480ee74cfecafc5a8fa2ee4e70fae50  implementation/work_order/DS_IMPLEMENTATION_WORK_ORDER.md`

## 1. Accepted predecessor state

DS-A02 was admitted on `main` at commit `4740566dd9176d8700d09fbc4b3fe64b36070c9c`, tagged `accepted/DS-A02`.

The preserved reviewer-authored result is stored at:

`.pcm/control/independent_review_results/DS-A02/11685c4c6dd0f59f67fc9cf336980cd0c6f71d58af8587f97f86b4bd930e6098.json`

Observed identities:

- file SHA-256: `2f988b138a4ae22b136b910aacf7abd3351102365e39c339bd2c2c95596c9262`;
- internal result SHA-256: `aaed1aa84021df158670da17c5bd6f7c390e5a277eb7a519abe67b383ff4c8c2`;
- review packet SHA-256: `11685c4c6dd0f59f67fc9cf336980cd0c6f71d58af8587f97f86b4bd930e6098`;
- reviewer actor instance: `73bd570bd89988b33c0bcecb2b5a1fa7`;
- verdict/route: `pass` / `PASS`.

DS-A03 work entered on `work/ds-a03-architecture-admission` at branch-admission commit `9502afd961f8a82ca5e09691d2e3924ca55e225b` / tree `54d6158a257a16fa7643ab2aad0262a4be63aa2b`. PCM `check` passed and `ready` identified DS-A03 before execution context was requested.

## 2. Mechanical identifier resolution before mutation

The exact DS-A01 binding was revalidated against the exact accepted Markdown brief before architecture mutation. Observed output:

```text
PASS: implementation authority brief_sha256=603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c
candidate_targets: create:derived_signal_calculation_truth->M01, modify:M00
```

Pre-mutation architecture state contained M00 as the only registered/durably allocated runtime-module identity and did not contain M01 in the registered, retired or durable-allocation sets. The native resolver therefore selected M01 mechanically; DS-A03 did not choose a numeric identifier independently of that result.

## 3. Baseline proof environment and proof

A direct architecture/bootstrap test invocation using the ambient `/opt/pyvenv` Python could not collect the suite because that environment lacked `psycopg`:

```text
ModuleNotFoundError: No module named 'psycopg'
1 error during collection
```

No architecture conclusion was drawn from that environment failure.

The preserved U05 offline proof-environment bootstrap was then reconstructed under `/mnt/data/ds_a03_proof_env`; tests were executed with the repository `src`, the exact reconstructed proof-environment site-packages and the already-present host PyYAML installation. Before DS-A03 mutation, observed architecture/bootstrap proof was:

```text
74 passed
architecture objects: 5
active runtime modules: 1
implementation allocations: 1
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0
PASS: structural architecture validation
Success: no issues found in 16 source files
All checks passed!
```

## 4. Exact architecture mutation

DS-A03 changes only the authorised architecture/work-order/proof-fixture surfaces:

- `config/architecture/implementation_allocations.yaml`: durably consumes `M01` as `derived_signal_calculation_truth`;
- `config/architecture/modules.yaml`: adds non-composable placeholder M01 identity with bounded ownership, inputs/outputs, M00-only dependency, declared future package/public seam, separate persistence boundary, external-effect exclusions and replay obligations; extends M00 only with the accepted additive read-only M01 raw-value/history reader boundary;
- `config/architecture/dependency_rules.yaml`: adds exactly one owner edge `M01 -> M00`;
- `implementation/architecture/DS_ARCHITECTURE_ADMISSION_CANDIDATE.md`: exact DS-A04 candidate narrative;
- `implementation/work_order/DS_IMPLEMENTATION_WORK_ORDER.md`: bounded downstream work order following the existing proof-first task graph.

No `src/**`, package metadata, schema, M00 stored-payload definition or production behaviour is changed by DS-A03.

## 5. Stale architecture-proof fixture updates

The first full architecture/bootstrap run after lawful M01 admission produced `13 failed, 61 passed`. Inspection established that the failures were current-state fixture/expectation coupling to the previously consumed M00-only architecture:

- object census expected five base objects rather than six;
- durable allocation history expected only M00;
- generic next-M candidate resolution still expected M01;
- synthetic retired/durable allocation fixtures reused the now-consumed M01 identity.

Only the affected architecture fixtures/expectations were updated:

- `tests/architecture/test_activation_readiness.py`;
- `tests/architecture/test_identifier_taxonomy.py`;
- `tests/architecture/test_implementation_authority_ingress.py`;
- `tests/architecture/test_registry_schema.py`;
- `tests/architecture/test_object_lifecycle.py`.

The lifecycle proof was strengthened to include M01 explicitly among non-active, non-composable identities. No negative fixture, validator, acceptance rule or test admission was removed or weakened.

## 6. Post-mutation proof before commit

With the stale architecture fixtures corrected, observed results are:

```text
python -m pytest tests/architecture tests/bootstrap -q
74 passed in 3.34s

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

python -m mypy src --show-error-codes
Success: no issues found in 16 source files

ruff check src tests tools
All checks passed!

git diff --check
PASS (no output)
```

A pre-commit invocation of `tools/run_promotion_gate.py` returned `FAIL: worktree is not clean before promotion`. This is the promotion wrapper's clean-candidate invariant, not an architecture/test failure. DS-A03 does not bypass it: clean committed-state promotion is required after the candidate commit and will be recorded as successor evidence before DS-A03 closeout.

## 7. Admission semantics and non-claims

- M01 is durably allocated but remains `placeholder`; no M01 implementation shell is admitted and active runtime modules remain exactly one (M00).
- M01's only declared owner dependency is M00; no reverse edge is introduced.
- M00 remains Raw Signal semantic owner and writer; the only DS-A03 change to M00 is its accepted additive typed read projection boundary.
- M01's PostgreSQL role/schema names and physical layout remain unresolved; only the required ownership/separation invariant is admitted.
- No provider/network integration, external effect or downstream action authority is admitted.
- Final distribution name/version remains deferred to `DS-PO01`.
- The accepted D catalogue/kernels/dependency meanings are unchanged.

## 8. Clean committed-state promotion

The architecture/work-order candidate was first committed at:

- commit: `560bb5995d109dfa7de2ff773bddfe49e494319c`;
- tree: `2d7d2c65a130e47162a4825bd26a703afcda2477`;
- worktree: clean before promotion.

From that exact clean state, observed results were:

```text
python .pcm/projectctl.py check
CHECK: PASS
ready=DS-A03

python tools/run_promotion_gate.py --set architecture_kernel
74 passed
PASS: structural architecture validation
promotion set: architecture_kernel
resolved test paths: 11

python tools/validate_architecture.py
architecture objects: 6
active runtime modules: 1
implementation allocations: 2
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0
PASS: structural architecture validation

python -m pytest tests/architecture tests/bootstrap -q
74 passed

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

python -m mypy src --show-error-codes
Success: no issues found in 16 source files

ruff check src tests tools
All checks passed!

git diff --check
PASS (no output)

git status --porcelain
<empty>
```

This successor evidence update changes evidence text only. The review packet source identity will bind the final Git commit/tree containing this exact evidence; DS-A04 remains a separate independent-review responsibility.

## 9. DS-A04 lifecycle-truth repair

The independent DS-A04 reviewer returned one substantive in-envelope repair finding: repository taxonomy defines `placeholder` as an identity with no admitted implementation and `bootstrap` as a minimal shell that exists but is not active, while DS-A03 created no M01 source package. The reviewer explicitly treated the stale repository-fingerprint bookkeeping issue as non-substantive and required no further cycle for it. The supplied reviewer response identified result SHA-256 `7f3352afdcd59796f74e28236237450804674070cd11bcaf44e14e727b45b721`.

The bounded repair changes only lifecycle truth and corresponding evidence/work-order wording:

- `config/architecture/modules.yaml`: M01 lifecycle `bootstrap` -> `placeholder`;
- `implementation/architecture/DS_ARCHITECTURE_ADMISSION_CANDIDATE.md`: explains that no implementation shell exists and `placeholder` is therefore the truthful lifecycle;
- `implementation/work_order/DS_IMPLEMENTATION_WORK_ORDER.md`: carries `placeholder` as the current lifecycle without changing downstream authority;
- `tests/architecture/test_object_lifecycle.py`: asserts the admitted M01 registry state is exactly `placeholder` while retaining the existing non-composability proof.

No source package, executable M01 behaviour, architecture identity, allocation, dependency edge, public-seam declaration, persistence boundary, requirement, work-order scope or accepted calculation meaning is added or changed by this repair.

Observed repair validation:

```text
python -m pytest tests/architecture/test_object_lifecycle.py -q
3 passed

python -m pytest tests/architecture tests/bootstrap -q
74 passed

python tools/validate_architecture.py
architecture objects: 6
active runtime modules: 1
implementation allocations: 2
dependency/public-seam violations: 0
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

mypy src --show-error-codes
Success: no issues found in 16 source files

ruff check src tests tools
All checks passed!

git diff --check
PASS (no output)

test ! -e src/nvda_desk/derived_signal_calculation_truth
PASS: M01 source package absent
```
