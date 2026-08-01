# Unit 4 locked-install environment evidence

Date: 2026-08-01
Branch: `work/m00-testing-guardrail-repair-v1`

## Declared route

```text
rm -rf .venv
make install
```

Observed result: **BLOCKED_EXTERNAL_INDEX**

```text
Python OK: 3.13.5
uv sync --frozen --extra dev --no-editable --python 3.13.5
Failed to download polars==1.39.3 from the configured internal package mirror:
HTTP 404 Not Found.
```

## Public-index diagnostic

The lock origins were normalised from the private execution mirror to canonical PyPI registry and file hosts without changing dependency versions or hashes. A second diagnostic explicitly selected the public index:

```text
UV_INDEX_URL=https://pypi.org/simple uv sync --frozen --extra dev --no-editable --python 3.13.5
```

Observed result: **BLOCKED_EXTERNAL_DNS**

```text
Failed to download fastapi==0.135.1 from files.pythonhosted.org after retries:
DNS lookup failed with temporary name-resolution failure.
```

## Interpretation

The repository now defines one frozen, non-editable install route and portable lock origins. This worker environment cannot fetch the required package artefacts from either its configured mirror or public PyPI. No editable install, dependency substitution, copied site-package tree or fabricated installed-package smoke result was used.

The installed-package smoke target is therefore structurally validated by contract tests but remains runtime-unexecuted in this environment.
