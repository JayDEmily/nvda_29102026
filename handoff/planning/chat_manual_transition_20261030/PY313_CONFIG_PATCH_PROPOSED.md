# Proposed CPython 3.13.5 configuration amendment — NOT APPLIED

The current owner requires CPython **3.13.5** for the resumed CHAT_MANUAL work. This document records the minimal textual changes to source configuration; **none are applied to `pyproject.toml` or `.python-version` on the review branch or active branch** until the exact environment mechanism and governed contract are accepted.

```diff
--- a/.python-version
+++ b/.python-version
@@
-3.12.14
+3.13.5
--- a/pyproject.toml
+++ b/pyproject.toml
@@ [project]
-requires-python = "==3.12.14"
+requires-python = "==3.13.5"
@@ [tool.ruff]
-target-version = "py312"
+target-version = "py313"
@@ [tool.mypy]
-python_version = "3.12"
+python_version = "3.13"
```

## Preconditions and boundaries

- Existing `pyproject.toml` has `[tool.uv] no-index = true` with `find-links = ["vendor/wheels"]`. The current committed vendor wheelhouse contains CPython 3.12-specific binaries. Do not silently point it to absent CPython 3.13 files.
- Project attachment `NVDA_PY313_OFFLINE_WHEELHOUSE_COMPLETE_20261023(1).zip` exists at 29,555,356 bytes. Inspect performed 30 October: 16 wheel names, all 16 declared wheel SHA-256 values matched recomputation; ZIP CRC check passed. Includes CPython 3.13 wheels for PyYAML==6.0.3, mypy==1.20.1 and pure/compatible pytest==9.0.3, Ruff==0.15.11. This does not qualify optional `psycopg[binary]` extras or SQLite equivalence.
- Create a **separate** governed dependency-readiness decision that binds the exact external wheelhouse location and manifests. Do not add package archives to GitHub just to make the plan draft work.
- CPython 3.13.5 is observed in this chat at `/opt/pyvenv/bin/python`; SQLite currently reports 3.46.1. Earlier accepted project proof/qualification relied on CPython 3.12.14 and SQLite 3.53.1. Preserve the old immutable proofs and obtain only the necessary new acceptance evidence for any material runtime/SQLite difference; do not rerun unchanged product proofs reflexively.
- The repository `README.md` still describes historical 25 October work and `Makefile` has broad `architecture-tests`, `typecheck` and `lint` targets. Do not invoke those blanket targets during documentary transition; only exact authorised later checks qualify.
- No dependency installation, project configuration mutation or product test is recorded by this patch proposal.

Proposed owner decision: approve the stated 3.13.5 target and exact minimal config diff **conditional on** viable offline dependency/source/readback route and necessary SQLite compatibility evidence. Activation and test authority remain separate.
