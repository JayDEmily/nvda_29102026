# T01 zero-Ruff — independent runtime compatibility boundary

**Investigation:** 15 November 2026, Australia/Melbourne. **Type:** read-only operational-environment inspection; no proof execution, programme acceptance, generation mutation or runtime installation.

## Observed execution environment

The committed reproducible inventory `RUNTIME_PREFLIGHT.py` was executed under the existing isolated Ubuntu interpreter:

```text
/home/jds/nvda_uv3135_20261112/.venv/bin/python
```

Raw machine output: `RUNTIME_PREFLIGHT_RESULT.json`. Its observed values are:

- Interpreter: **CPython 3.13.5**
- Python `sqlite3.sqlite_version`: **3.49.1** for that selected interpreter
- Active repository `pyproject.toml` `requires-python`: **==3.13.5**
- Active `.python-version`: **3.13.5**
- `shutil.which("python3.12")`: **null in this process's PATH**; this is not an exhaustive claim about all available runtime files or machines.
- Seven claim contracts comprise **11 physical proof families**; all eleven `family.environment` fields record **CPython 3.12.14 and SQLite 3.53.1**. Five pilot families explicitly require proof of that exact environment; D030, D031, D032, D033, D035 and D036 record the same versions.

These are **observed and committed file/runtime facts**. `sqlite3.sqlite_version` reports the library used by this selected interpreter; it does not establish SQLite versions available in other Ubuntu interpreters, Windows, GitHub Actions or separately qualified runtimes.

## Authority boundary

Historical immutable proof contracts and prior accepted product evidence name CPython 3.12.14 / SQLite 3.53.1. The T01 proposed successor planning material, `handoff/planning/t01_recovered_successor_20261111/PROPOSED_EXEC_PLAN.md` around its runtime-target paragraph, records an **owner-approved target of CPython 3.13.5** but explicitly says historical proof evidence is not runtime-parity evidence. This *proposed* successor document is not installed as the active root `EXEC_PLAN.md`. Do not silently promote its proposed transition into authority for tests.

The direct Ruff remediation's independently verified source-equivalence judgement at `8d1f340940b43f46be3143a8565e6cc2c73ebe1b` is **unaffected** by this observation. A zero-Ruff static check under CPython 3.13.5 is not a product runtime qualification. No evidence from this inspection establishes that the numerical computations, persistence behaviour, SQLite feature set, type checking or controlled proof outcomes are equivalent between the old and new combinations.

## Exact disposition

1. **FIRST DEPENDENT BLOCKER remains `BLOCKED_PROGRAMME_ADMISSION_AUTHORITY`:** pilot 4→5 and six D030/D031/D032/D033/D035/D036 2→3 generations have no genuine specific programme admission decision or active pointer changes. This runtime investigation neither resolves nor adds a substitute to that gate.
2. **CONDITIONAL NEXT EXECUTION INPUT:** before a product-proof run is represented as meeting its bound contract, the actual selected interpreter, `sqlite3` library, all pinned dependencies and acceptance of any necessary version compatibility must be evidenced under the governing test authority. The observed 3.13.5/3.49.1 environment is **not established as equivalent** to the historical 3.12.14/3.53.1 proof environment.
3. **NO corrective runtime recommendation yet:** a version difference alone does not demonstrate a product defect or that any specific upgrade/downgrade is required. The required determination is governed runtime compatibility, not opportunistic environment modification.
4. **NOT PERFORMED:** pytest, product proof, architecture CI, model API job, generation creation/admission, changed proof expectations, new toolchain installation, branch merge or D145 activation.

This remains a separate read-only readiness fact. No green source/semantic/CI decision is implied by the absence of a runtime test.
