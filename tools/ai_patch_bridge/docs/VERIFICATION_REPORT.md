# Verification report

Generated in ChatGPT sandbox after the venv/Makefile fail-safe audit.

## Files read during audit

The following in-scope files were read before modification or verification:

- `AGENTS.md`
- `Makefile`
- `README.md`
- `pyproject.toml`
- `scripts/ai_patch_bridge.py`
- `scripts/check_bridge_hygiene.py`
- `scripts/format_bridge_text.py`
- `scripts/run_bridge_tests.py`
- `src/ai_patch_bridge/__init__.py`
- `src/ai_patch_bridge/cli.py`
- `src/ai_patch_bridge/core.py`
- `src/ai_patch_bridge/test_runner.py`
- `tests/test_ai_patch_bridge.py`
- `tests/fixtures/mock_target.py`
- `docs/INSTALL_AI_PATCH_BRIDGE.md`
- `examples/sample_patch.diff`
- `examples/generated/example_ai_patch_comment.md`

## Defects found in this audit

1. `make test` depended on `pytest`, but sandbox pytest imports/execution were unstable. The bridge's own regression tests are now stdlib-only.
2. `tests/test_ai_patch_bridge.py` invoked the wrapper script directly, so the shebang could select the wrong Python. The test now calls the bridge CLI entrypoint in-process.
3. Running bridge scripts directly from `scripts/` could shadow the real `ai_patch_bridge` package. The wrappers now remove the script directory from `sys.path` before importing the package.
4. The previous `lint` target depended on external Ruff/Black. In this sandbox those tools were not reliable enough for a bridge self-test. The bridge lint target is now stdlib-only: `compileall` plus a text hygiene script.
5. `pyproject.toml` carried project dependencies that the bridge itself does not need. The standalone bridge pack now has `dependencies = []`; the host project keeps its own real dependencies.
6. `Makefile` used `/usr/bin/env bash` as `SHELL`. It now uses `/bin/bash`, which is the deterministic make-compatible shell path in this sandbox.

## Venv created

A Python 3.13.5 virtual environment was created in the sandbox using:

```bash
/opt/pyvenv/bin/uv venv --python /usr/bin/python3 .venv_uv
```

Observed:

```text
Using CPython 3.13.5 interpreter at: /usr/bin/python3
Creating virtual environment at: .venv_uv
Python 3.13.5
```

The venv is not included in the delivered zip.

## Makefile targets verified in sandbox

These targets were run successfully with `PYTHON=/usr/bin/python3`:

```bash
make PYTHON=/usr/bin/python3 test
make PYTHON=/usr/bin/python3 ai-bridge-self-test
make PYTHON=/usr/bin/python3 ai-bridge-make-example-comment
make PYTHON=/usr/bin/python3 lint
```

Observed successful outputs included:

```text
Ran 6 bridge tests; failures=0
AI_PATCH_V1 self-test passed.
examples/generated/example_ai_patch_comment.md
Bridge hygiene check passed.
```

## Preflight result in sandbox

`make PYTHON=/usr/bin/python3 ai-bridge-preflight` was run and correctly failed because this sandbox is not the user's authenticated local WSL environment.

Observed blockers:

```text
gh: not installed
codex: not installed
repo root: not a git repository
```

That is expected in this sandbox. On the user's machine, preflight is the live readiness gate.

## Install target status

The bridge package is intentionally stdlib-only at runtime. `pyproject.toml` now declares no runtime dependencies.

`make install` is retained for a normal local WSL venv:

```bash
make install
```

In this sandbox, `pip`/`uv pip` installer processes were intermittently unstable under `make`, so `make install` is not claimed as passed here. The operational targets above do not require installation because they run with `PYTHONPATH=src`.

## Not run

These were not run because this sandbox is not the authenticated local machine:

```text
Codex CLI execution
gh auth status
GitHub issue polling with real credentials
GitHub receipt posting
Git push to origin
make ai-bridge-once
make ai-bridge-watch
```

## Current verified state

The delivered pack is verified for:

- AI_PATCH_V1 encode/decode/hash validation;
- executor filtering for `local-codex`;
- concatenated GitHub CLI JSON page parsing;
- stdlib regression test runner;
- Makefile test/self-test/comment-generation/lint gates;
- expected sandbox preflight failure.

## Edge-case hardening pass

Additional edge cases were added after tracing long sandbox runs and rescue-branch preservation.

### Changes

- Added explicit executor metadata validation.
- Added branch namespace validation by executor:
  - `local-codex` -> `work/...`
  - `github-action` -> `work/...`
  - `rescue-branch` -> `rescue/...`
- Added `commit_policy` and `test_policy` metadata fields.
- Added rescue branch generation through `make ai-bridge-make-rescue-example-comment`.
- Added configurable local bridge executor filter with `--accepted-executor`.
- Added edge-case documentation in `docs/EDGE_CASES_AND_BRANCH_LANES.md`.

### Verified commands

```bash
/usr/bin/python3 -m venv --without-pip .venv
PYTHON=.venv/bin/python make test
PYTHON=.venv/bin/python make lint
PYTHON=.venv/bin/python make ai-bridge-self-test
PYTHON=.venv/bin/python make ai-bridge-make-example-comment
PYTHON=.venv/bin/python make ai-bridge-make-rescue-example-comment
```

### Observed result

```text
Ran 10 bridge tests; failures=0
Bridge hygiene check passed.
AI_PATCH_V1 self-test passed.
examples/generated/example_ai_patch_comment.md
examples/generated/example_rescue_ai_patch_comment.md
```


## Scenario-lane and remote-freshness hardening pass

Date: 2026-04-28

Changes verified in this pass:

- Added `PLANS.md` with scenarios A-G and lane selection rules.
- Added `make ai-bridge-scenarios` and individual `make ai-bridge-scenario-a` through `make ai-bridge-scenario-g` gates.
- Added `src/ai_patch_bridge/scenario_tests.py` for offline lane validation.
- Hardened local-Codex branch preparation to fetch `origin` first, verify `origin/<base_branch>`, and create target branches from remote base truth instead of a potentially stale local `main`.
- Added AGENTS.md remote freshness law and scenario routing law.

Commands run with `PYTHON=/usr/bin/python3`:

```bash
make PYTHON=/usr/bin/python3 test
make PYTHON=/usr/bin/python3 lint
make PYTHON=/usr/bin/python3 ai-bridge-scenarios
make PYTHON=/usr/bin/python3 ai-bridge-scenario-a
make PYTHON=/usr/bin/python3 ai-bridge-scenario-b
make PYTHON=/usr/bin/python3 ai-bridge-scenario-c
make PYTHON=/usr/bin/python3 ai-bridge-scenario-d
make PYTHON=/usr/bin/python3 ai-bridge-scenario-e
make PYTHON=/usr/bin/python3 ai-bridge-scenario-f
make PYTHON=/usr/bin/python3 ai-bridge-scenario-g
make PYTHON=/usr/bin/python3 ai-bridge-self-test
make PYTHON=/usr/bin/python3 ai-bridge-make-example-comment
make PYTHON=/usr/bin/python3 ai-bridge-make-rescue-example-comment
```

Observed pass conditions:

- Bridge test runner: `Ran 12 bridge tests; failures=0`.
- Scenario aggregate target passed scenarios A-G plus invalid rescue policy.
- Each individual scenario target passed exactly its named scenario.
- Lint target passed compileall and bridge hygiene check.

Not run here:

- Live GitHub polling.
- Codex CLI execution.
- Real git fetch/push from the user's WSL repo.
