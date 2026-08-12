# Dependency and Lock Report

## Platform boundary

- Python: exactly CPython 3.13.5.
- Operating system lock: Linux.
- Required machine: x86_64.
- Network policy: disabled for resolution and installation.
- Wheel source: repository-relative `vendor/wheels`.

This is a deliberate match to the user-supplied offline wheelhouse. Cross-platform portability is not proved.

## Direct dependencies

| Class | Package | Version | Purpose |
|---|---|---:|---|
| Runtime | PyYAML | 6.0.3 | Parse declarative YAML registries. |
| Development | pytest | 9.0.3 | Execute admitted architecture/bootstrap proof. |
| Development | ruff | 0.15.11 | Static lint and import-order validation. |
| Build backend | hatchling | 1.29.0 | Build wheel and source distribution. |

No former production dependency is declared. In particular, FastAPI, SQLAlchemy, asyncpg, psycopg, IB API, Polars and OpenPyXL are absent from `pyproject.toml` and installed package metadata.

## Reproducibility

- `uv.lock` resolves eight project/runtime/development packages from `vendor/wheels`.
- `vendor/wheels/SHA256SUMS` verifies all eleven retained direct, transitive and build-support wheels.
- The retained wheelhouse is approximately 14 MiB; the larger former runtime dependency population was not copied.
- `uv sync --locked --extra dev --offline` reconstructed a new environment without network access.
