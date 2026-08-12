#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
exec "$ROOT/.venv/bin/python" -B "$ROOT/.codex/hooks/runtime_identity_attest.py"
