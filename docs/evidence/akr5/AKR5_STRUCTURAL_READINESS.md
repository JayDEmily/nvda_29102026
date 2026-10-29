# AKR-5 dormant structural readiness evidence

## Scope

AKR-5 completes the structural controls required before the first real implementation brief can be admitted. It does not admit product semantics or a product module.

The leaf resumed from the recorded blocker commit:

`3d0f2330f76f54bd4fd0257c35391ed3bee7fa94`

The blocker was the absence of a pinned static type checker from the admitted offline dependency surface.

## Blocker resolution

The user supplied:

`NVDA_AKR5_TYPECHECKER_DEPENDENCY_INGRESS_20260909.tar(1).gz`

Observed SHA-256:

`3d4e9aa4f7483143f40c30a838f63b6c8b83abcaeee9a8bc8cfdefa5320bd00a`

Its internal SHA-256 manifest verified all four supplied wheels before integration.

The repository now vendors the missing development-only checker surface:

- `mypy==1.20.1`;
- `mypy_extensions==1.1.0`;
- `typing_extensions==4.15.0`;
- `librt==0.9.0`.

The pre-existing `pathspec==1.1.1` wheel satisfies mypy's remaining required dependency and was not duplicated.

`uv lock --offline` and `uv sync --offline --extra dev --frozen` resolved and installed the environment using only the repository-local wheelhouse. The resulting environment reported:

```text
Python 3.13.5
mypy 1.20.1 (compiled: yes)
pytest 9.0.3
ruff 0.15.11
```

Mypy is declared only in `[project.optional-dependencies].dev`; it is not a production/runtime dependency.

## Structural repairs

AKR-5 implemented the following bounded repairs:

1. removed the reset-only aggregate rejection of every active runtime module;
2. made the aggregate validator report the actual active-module count;
3. required active Python-visible owners to have a physically present registered package and public seam;
4. repaired `ImportFrom` owner/member resolution so forms such as `from nvda_desk import m02` cannot bypass owner/seam enforcement;
5. retained named dynamic-import rejection;
6. made physical architecture/bootstrap test discovery recursive;
7. required Python-visible package/public-seam declarations to occur as a pair;
8. extended active-module structural projection to explicitly declare component forms and durable-state writer/reader/persistence/replay boundaries;
9. added a repository-native `make typecheck` entry point using the pinned checker;
10. admitted blocking structural-readiness and typed-public-seam proof families;
11. rewrote reset-era bootstrap assertions that would otherwise permanently prohibit a lawful future active module/package.

## Real-path activation proof

The blocking tests use temporary repository copies containing the same committed schemas, registries, loaders and analyser used by the kernel.

They establish the following structural propositions within their tested scope:

- a minimally valid first active `M` is accepted by aggregate architecture validation;
- an active owner whose declared package/public seam is physically absent is rejected;
- lawful declarative and Python-visible `P` activation is representable;
- lawful Python-visible `K` activation is representable;
- valid declared `M -> M` dependencies are accepted;
- undeclared `M -> M` dependencies are rejected;
- category-forbidden reverse dependencies are rejected;
- `M` dependency cycles are rejected;
- private cross-owner imports are rejected;
- `from nvda_desk import m02` is rejected when it bypasses `M02`'s declared seam;
- supported named dynamic-import forms are rejected in runtime owners;
- incomplete active-module ownership/component/state projection is rejected;
- invalid one-sided Python-visible P/K package/seam activation is rejected;
- malformed public-seam exceptions are rejected by the committed loader/schema path;
- historical predecessor identities remain representable without reactivation;
- nested unadmitted physical tests are rejected by recursive proof accounting;
- current source passes the admitted static checker;
- an incompatible typed call through a Python-visible public seam is rejected by mypy.

These tests establish structural/mechanical behaviour only. They do not establish semantic adequacy of a future implementation brief or future module.

## Committed implementation state

Functional AKR-5 implementation commit:

`c335b33974fb6e4b4ac2e1987697ba4e5fe6cc3b`

At that commit, clean-worktree validation observed:

```text
make PYTHON=.venv/bin/python typecheck
Success: no issues found in 12 source files

architecture_kernel promotion
62 passed
11 admitted test families
1 promotion set
0 dependency/public-seam violations

ruff check src tests tools
All checks passed!

uv lock --check --offline
Resolved 13 packages

git fsck --full
completed without reported repository-integrity error
```

The production registries remain behaviour-neutral at this leaf: `config/architecture/modules.yaml` and `config/architecture/surfaces.yaml` remain empty.

## Boundary

AKR-5 does not claim the repository is terminally ready for a real product implementation brief. AKR-6 remains responsible for a bounded synthetic implementation-ready-brief ingress rehearsal without leaving domain/product code active in the committed production registries.
