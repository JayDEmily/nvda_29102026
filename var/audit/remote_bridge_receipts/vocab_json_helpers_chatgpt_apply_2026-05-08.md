# Remote bridge receipt — vocabulary JSON helpers apply

Status: APPLIED_TO_MAIN_WITH_SANDBOX_MERGE_PROBE

Repository: `JayDEmily/nvda10`
Target branch: `main`
Source package: `NVDA10_PM_WORKER_OUTPUT_VOCAB_JSON_HELPERS_GREEN_2026-05-08.tar.gz`
Source package size_bytes: `54227`
Source package sha256: `201b3985b60893d8b58c67509e2f900813fed5764caecc469250a3ab6cb45c30`

## Important base observation

The package was built on branch `codex/update-pyproject-metadata` at base commit `0c5b599633afaa0be28e1f00e96fac7b245d9366`, after prior green replay commit `7003b3eaec1ffed5a1dffae9bc56a2579b519b5c`, and final worker commit `ab1fe6809ff7dd6075fdae1d31d650f737060b94`.

Current GitHub `main` before this apply was `49d3c60f6024d8ce425c3096a1aadf3edeec7a50` after PR #1 merge. Current `main` did not contain the prior schema implementation layer, so the uploaded second-layer patch was not applied blindly. Instead, the final changed files from the worker output package were applied as the intended final state.

## Files applied

- `src/nvda_desk/schemas/vocabulary.py`
- `tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py`

## Worker package validation recorded

The worker package recorded:

- baseline red proof: expected failure for missing JSON helpers
- `py_compile_json_helper`: status `0`
- `final_json_helper_pytest`: `5 passed`
- `candidate_schema_regression_pytest`: `6 passed`
- `targeted_vocabulary_no_synonym_pytest`: `19 passed`
- `git diff --cached --check`: status `0`
- `ruff`: unavailable in `/opt/pyvenv`; no ruff pass claimed

## Local ChatGPT sandbox merge probe

A local synthetic merge probe was run before GitHub commit using the final `vocabulary.py` and helper test from the package plus a smoke test matching current `main` schema expectations.

Command shape:

```text
python -m py_compile src/nvda_desk/schemas/vocabulary.py tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py tests/tier_a/vocabulary/test_current_main_schema_smoke.py
PYTHONPATH=src pytest -q tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py tests/tier_a/vocabulary/test_current_main_schema_smoke.py
```

Observed result:

```text
7 passed in 0.23s
```

## Claims

Proven:

- uploaded package was inspected;
- changed-file set was identified as one modified source file and one added test file;
- current GitHub `main` was checked before apply;
- the uploaded patch was not blindly applied because base layers differed;
- final intended files from the package passed a local syntax and targeted smoke probe;
- final files were staged for direct `main` commit through the GitHub connector.

Not proven:

- full repository test suite on GitHub `main`;
- ruff pass;
- WSL/Codex consumption of this change.
