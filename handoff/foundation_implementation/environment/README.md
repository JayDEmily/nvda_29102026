# Bounded CPython 3.12 offline environment

Authority: exact accepted SQLite implementation brief version3, §2. This is an environment checkpoint inside G5.1, not product proof or leaf acceptance. The bundle targets Linux x86_64 CPython3.12.14. It contains matching wheels, not an interpreter or PostgreSQL server. The observed host stdlib engine is SQLite3.53.1; this is not a wider deployment guarantee.

`vendor/wheels/` supplies the complete pinned runtime/build/development dependency closure. Each selected distribution is pinned and hashed in the adjacent lock files. `requirements-cp312-runtime.lock` has only PyYAML. `requirements-cp312-dev.lock` adds tools, their transitives, hatchling/editables and pure Psycopg for retained-source typechecking. `requirements-cp312-legacy-checks.lock` explicitly adds the optional binary PostgreSQL client for the still-unmodified A00 eager import. No server runs. That compatibility environment is not evidence of Psycopg-free A00 construction; the latter remains an admitted M00/A00 implementation obligation.

The exact metadata changes are Python==3.12.14, Ruffpy312, mypy3.12; PyYAML remains the sole mandatory runtime dependency; Psycopg[binary]3.3.4 is an explicit postgres extra; pure Psycopg3.3.4 is in dev. No source exclusion or missing-import suppression is added.

## Reproduction

Run from the repository root with CPython3.12.14 and uv (observed0.12.23). Choose new absent absolute environment/cache directories outside the repository; never reuse a working environment. Set `NVDA_PYTHON`, `NVDA_ENV` and `NVDA_CACHE` to those exact paths. These names do not replace system environment variables.

Runtime-only install, including an isolated offline project build:

```bash
uv venv --python "$NVDA_PYTHON" "$NVDA_ENV"
uv --cache-dir "$NVDA_CACHE" pip install --python "$NVDA_ENV/bin/python" --offline --require-hashes -r handoff/foundation_implementation/environment/requirements-cp312-runtime.lock
uv --cache-dir "$NVDA_CACHE" pip install --python "$NVDA_ENV/bin/python" --offline .
```

Use a different absent environment/cache pair for development. Install `requirements-cp312-dev.lock` with the same offline/hash command, then `uv --cache-dir "$NVDA_CACHE" pip install --python "$NVDA_ENV/bin/python" --offline -e '.[dev]'`. The separate retained-kernel compatibility profile installs `requirements-cp312-legacy-checks.lock`, then `-e '.[dev,postgres]'`. The repository's existing no-index/find-links configuration resolves only `vendor/wheels`; do not bypass it with `--no-config`. The first locked install enforces wheel hashes; the subsequent project install uses the already-pinned declared dependencies and isolated build requirements.

## Evidence boundary

Fresh runtime install must contain only project1.0.0 and PyYAML6.0.3, with neither Psycopg distribution. Importing architecture ingress and M00 public API is an environment/import observation, not production composition. Environmental STRICT/transaction/read-only/integrity checks establish SQLite engine capabilities only. They do not prove the unwritten M00 adapter, persistence failure semantics, G01 runner, D011 or a complete product aggregate.

Retained-kernel suite, full-source mypy and lint results must be reported individually, including failures. No product tests are admitted or executed by these files. Do not change a historical PostgreSQL-specific test to obtain SQLite green.
