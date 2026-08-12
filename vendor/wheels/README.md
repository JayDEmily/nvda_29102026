# Minimal offline wheelhouse

This directory contains only the dependencies required to build, install, lint and test the architecture kernel on CPython 3.13.5 Linux x86_64.

The wheels were selected from the user-supplied runtime and development wheelhouses. `SHA256SUMS` records the exact retained artefacts. The former runtime dependency population was not copied into the reset repository.

`uv.lock` resolves against this repository-relative directory. The lock is intentionally restricted to Linux x86_64 because the supplied `PyYAML` and `ruff` wheels are platform-specific.
