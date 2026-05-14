# Proof-block bridge doctrine update receipt

Status: PROOF_BLOCK_DOCTRINE_COMMITTED_TO_MAIN

Repository: `JayDEmily/nvda10`
Target branch: `main`
Starting main SHA: `f55fe5c0cb5413c46aaa2a5e47e9880146d9342d`

## Files updated

- `project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md`
- `Makefile`
- `tools/ai_patch_bridge/Makefile`
- `tools/ai_patch_bridge/AGENTS.override.md`
- `.github/workflows/pr-preflight.yml`
- `var/audit/remote_bridge_receipts/proof_block_bridge_doctrine_update_2026-05-08.md`

## Why this was added

The proof-block executor package made `config/proof_blocks.yaml` executable through:

```bash
make proof-block BLOCK=vocabulary_governance_conformance
```

That is now a first-class bridge lane and needed to be documented in the same control surfaces as the remote bridge blueprint.

## Control gates added

Root Makefile:

```bash
make proof-executor-check
```

Bridge-local Makefile delegation:

```bash
make -C tools/ai_patch_bridge ai-bridge-proof-executor-check
```

PR preflight workflow now also runs:

```bash
make proof-executor-check
```

## Non-claims

This receipt does not claim:

- WSL watcher ingestion is implemented;
- Codex CLI consumed the proof-block lane;
- GitHub Actions has run the full vocabulary proof block after this update;
- the full repository test suite was rerun for this documentation/control update.
