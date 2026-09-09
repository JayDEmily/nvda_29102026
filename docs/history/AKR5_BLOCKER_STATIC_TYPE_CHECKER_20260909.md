# AKR-5 blocker — hermetic static type checker

Status: BLOCKED evidence. This file is historical execution evidence, not architecture authority.

## Acceptance unit

`AKR-5 — Complete dormant structural readiness`.

The accepted ExecPlan requires the static typed-seam dependency to be resolved before dependent AKR-5 work proceeds. It states that if no suitable pinned development-only static type checker can be installed under the admitted environment constraints, the gate must record the exact blocker and stop.

## Verified repository/runtime state

At AKR-5 entry:

- parent/AKR-4 commit: `fcf2d9a6c8b28ab91a4b90673bfafc261f222d47`;
- branch: `work/akr-5-dormant-structural-readiness`;
- pinned project Python: `3.13.5`;
- observed hermetic project interpreter: `.venv/bin/python`, Python `3.13.5`;
- observed machine: `x86_64`;
- `[tool.uv]` is `no-index = true` and resolves from `vendor/wheels`;
- `uv.lock` contains no `mypy` package;
- `vendor/wheels` contains no mypy, Pyright, basedpyright, pytype, Pyre or `ty` checker wheel;
- no `mypy`, `pyright`, `basedpyright`, `pytype`, `pyre` or `ty` command is installed in the runtime;
- the supplied project/archive payloads were searched for checker wheels and none was found.

External package evidence checked on 2026-09-09 establishes that mypy `2.3.1` is published for Python `>=3.10` and that a CPython 3.13 manylinux x86-64 wheel exists. That package is not part of the admitted local offline dependency surface.

Direct attempts to obtain the wheel from this runtime failed before package retrieval because outbound DNS/network access to `files.pythonhosted.org`/PyPI is unavailable.

## First unmet invariant

The repository cannot presently demonstrate a **pinned, offline-reproducible static type checker** that can be installed from the admitted dependency surface.

Ruff is retained as lint evidence only. It is not substituted for the typed public-seam proposition.

## Stop boundary

No downstream AKR-5 implementation was performed after this blocker was established. In particular, this attempt did not repair or claim completion of:

- first-active-module aggregate validation;
- `ImportFrom` public-seam enforcement;
- recursive physical-test discovery;
- category activation paths;
- typed seam incompatibility proof.

Those remain authorised AKR-5 work, but dependent execution is blocked until a suitable checker and its complete offline-installable dependency set are available and admitted.

## Baseline proof before blocker record

The exact AKR-4 parent state was revalidated before recording the blocker:

- structural architecture validation: PASS;
- architecture/bootstrap tests: `44 passed`;
- Ruff: PASS;
- registry-derived `architecture_kernel` promotion: `44 passed`;
- architecture objects: `5`;
- active runtime modules: `0`;
- admitted test families: `9`;
- promotion sets: `1`;
- dependency/public-seam violations reported by the current checker: `0`.

These observations do not establish AKR-5 acceptance.
