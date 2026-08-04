# NVDA Architecture Kernel

A behaviour-neutral Python architecture kernel for admitting modular runtime owners, protocols, governance planes, application shells, technical kernels and end-to-end architecture surfaces without inheriting the former NVDA business implementation.

The active runtime-module and surface registries are intentionally empty. `P01`, `G01`, `G02`, `A00` and `K01` are non-active structural identities only.

## Start here

Read, in order:

1. `AGENTS.md`;
2. `PLANS.md`;
3. `docs/architecture/ARCHITECTURE_KERNEL.md`;
4. `docs/architecture/ARCHITECTURE_KERNEL_RESET_BRIEF.md`.

## Reproducible local validation

The repository carries only the CPython 3.13.5 Linux x86_64 wheels required by the kernel and its admitted development proof.

```bash
uv sync --locked --extra dev --offline
uv run ruff check src tests tools
uv run python tools/validate_architecture.py
uv run python tools/run_promotion_gate.py --set architecture_kernel
```

These checks establish the named packaging and structural propositions only. They do not establish any future domain semantics.
