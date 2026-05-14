# Persistent worker enablement pack receipt

Status: UNAPPLIED_LOCAL_ENABLEMENT_PACK

Target repository: `JayDEmily/nvda10`
Expected starting main SHA at pack creation: `d417a26bfb2320b6f4a55d35336fd0c155641ba2`

## Files proposed

- `tools/ai_patch_bridge/docs/PERSISTENT_WORKER.md`
- `tools/ai_patch_bridge/scripts/bridge_doctor.sh`
- `tools/ai_patch_bridge/scripts/install_user_service.sh`
- `tools/ai_patch_bridge/systemd/nvda10-ai-patch-bridge.service.template`
- `tools/ai_patch_bridge/tests/test_persistent_worker_assets.py`
- `var/audit/remote_bridge_receipts/persistent_worker_enablement_pack_2026-05-08.md`

## Purpose

Make first Ubuntu bring-up easier by adding a doctor check and a `systemd --user` service installer around the existing bridge watcher.

## Non-claims

This pack does not claim:

- it was applied to GitHub;
- the user service has been run on Ubuntu;
- GitHub authentication is configured locally;
- Codex CLI execution is working;
- full end-to-end bridge automation is proven.
