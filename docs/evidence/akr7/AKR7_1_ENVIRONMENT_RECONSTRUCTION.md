# AKR-7.1 environment reconstruction evidence

## Scope

AKR-7.1 establishes only that the repository can reconstruct the development/proof environment from the dependency authority it currently carries and can invoke the repository-native mechanisms needed by later AKR-7 leaves.

It does not semantically accept AKR-7.2 through AKR-7.5. In particular, the build probe recorded here is dependency/toolchain proof only; distribution-content inspection and isolated-install proof remain AKR-7.4 work.

Start state:

```text
branch: work/akr-7-final-pristine-kernel-proof
HEAD: 610a66365ce7ce981f6f6702c2062875fd1f4c3b
```

## Dependency and build authority inspected

The following current files were read before creating the fresh environment:

```text
pyproject.toml
uv.lock
.python-version
vendor/wheels/README.md
vendor/wheels/SHA256SUMS
Makefile
README.md
src/nvda_desk/architecture/cli.py
src/nvda_desk/architecture/promotion.py
tools/validate_architecture.py
tools/check_dependencies.py
tools/check_public_seams.py
tools/run_promotion_gate.py
tools/validate_implementation_authority.py
```

Observed current authority:

- `pyproject.toml` requires Python `==3.13.5` and runtime `PyYAML==6.0.3`;
- development dependencies are `pytest==9.0.3`, `ruff==0.15.11` and `mypy==1.20.1`;
- the build backend is `hatchling==1.29.0`;
- `uv.lock` is restricted to Linux and records the project/runtime/development dependency graph against `vendor/wheels`;
- `[tool.uv]` sets `no-index = true`, `find-links = ["vendor/wheels"]` and requires Linux x86_64;
- `.python-version` is `3.13.5`;
- the Makefile exposes architecture validation, architecture/bootstrap tests, promotion, implementation-authority validation and type checking; build authority is declared by `pyproject.toml` and invoked with `uv build`.

## Admitted wheelhouse integrity

Every artefact named by `vendor/wheels/SHA256SUMS` was present and:

```text
(cd vendor/wheels && sha256sum -c SHA256SUMS)
```

reported `OK` for all 15 retained wheels, including the build backend/dependencies, runtime dependency and development/proof dependencies.

## Fresh reconstruction

No repository-local `.venv` or other virtual environment existed before the reconstruction.

The available local interpreter and resolver used for reconstruction were:

```text
uv 0.10.0
CPython 3.13.5
```

A new external environment was created at `/mnt/data/nvda_akr7_env_7_1` with network resolution disabled and Python downloads disabled:

```text
export UV_PROJECT_ENVIRONMENT=/mnt/data/nvda_akr7_env_7_1
export UV_OFFLINE=1
export UV_PYTHON_DOWNLOADS=never
uv lock --check --offline
uv sync --frozen --offline --extra dev --python 3.13.5
```

Observed results:

```text
uv lock --check --offline
Resolved 13 packages

uv sync --frozen --offline --extra dev --python 3.13.5
Creating virtual environment at: /mnt/data/nvda_akr7_env_7_1
Built nvda-architecture-kernel from the repository
Prepared 13 packages
Installed 13 packages
```

The reconstructed interpreter reported:

```text
Python 3.13.5
/mnt/data/nvda_akr7_env_7_1/bin/python
```

The environment contained the locked runtime/development set required by the later Python proof path: `PyYAML 6.0.3`, `pytest 9.0.3`, `mypy 1.20.1` and its locked dependencies, and `ruff 0.15.11`. The editable kernel package was installed as `nvda-architecture-kernel 0.1.0`.

The build backend is not a project runtime/development dependency. Its availability from the same admitted wheelhouse was established separately by the successful offline build probe below.

## Repository-native mechanism invocation

Using only the reconstructed environment for Python execution:

```text
make validate PYTHON=/mnt/data/nvda_akr7_env_7_1/bin/python
```

ran the repository architecture validator and returned zero exit status.

```text
make typecheck PYTHON=/mnt/data/nvda_akr7_env_7_1/bin/python
```

invoked the admitted checker and reported:

```text
Success: no issues found in 13 source files
```

Test mechanism availability was established without claiming the AKR-7.3 aggregate proof result:

```text
/mnt/data/nvda_akr7_env_7_1/bin/python -m pytest --collect-only -q tests/architecture tests/bootstrap
```

which collected `74` tests.

Promotion mechanism availability was established using its non-executing check-only path:

```text
/mnt/data/nvda_akr7_env_7_1/bin/python tools/run_promotion_gate.py --set architecture_kernel --check-only
```

which resolved `11` test paths and returned zero exit status. `src/nvda_desk/architecture/promotion.py` was read before using this result; `check_only=True` performs clean-worktree checking, architecture/proof-state loading and promotion-path resolution, but does not execute pytest.

All five installed console-script surfaces declared by `pyproject.toml` were also present and accepted `--help` from the fresh environment:

```text
nvda-validate-architecture
nvda-check-dependencies
nvda-check-public-seams
nvda-promotion-gate
nvda-validate-implementation-authority
```

## Offline build-mechanism probe

With `UV_OFFLINE=1` still active, the declared Hatchling build path was invoked to an external scratch directory:

```text
uv build --offline --out-dir /mnt/data/nvda_akr7_1_build_probe
```

It completed successfully and produced:

```text
nvda_architecture_kernel-0.1.0.tar.gz
nvda_architecture_kernel-0.1.0-py3-none-any.whl
```

This establishes that the currently admitted offline dependency surface supplies the build backend and its required dependencies. The artefacts were not treated as AKR-7.4 package proof and were not installed or semantically accepted here.

## Leaf conclusion

AKR-7.1 acceptance is established for the current committed source state: a newly reconstructed CPython 3.13.5 environment, created under offline/no-download constraints from the repository-admitted wheelhouse and lock, is sufficient to invoke the downstream validation, static type-check, test, promotion-resolution and build mechanisms.

No required downstream Python/build dependency was found absent from the admitted offline surface during this leaf.

AKR-7.2 was not executed as part of this evidence record.
