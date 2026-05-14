from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BRIDGE = ROOT / "tools" / "ai_patch_bridge"


def test_persistent_worker_docs_and_scripts_exist() -> None:
    assert (BRIDGE / "docs" / "PERSISTENT_WORKER.md").exists()
    assert (BRIDGE / "scripts" / "bridge_doctor.sh").exists()
    assert (BRIDGE / "scripts" / "install_user_service.sh").exists()
    assert (BRIDGE / "systemd" / "nvda10-ai-patch-bridge.service.template").exists()


def test_service_template_uses_existing_foreground_watch_target() -> None:
    text = (BRIDGE / "systemd" / "nvda10-ai-patch-bridge.service.template").read_text(
        encoding="utf-8"
    )
    assert "ExecStart=/usr/bin/env bash -lc 'make ai-bridge-watch'" in text
    assert "Restart=always" in text
    assert "AI_PATCH_REPO_ROOT" in text
    assert "Environment=AI_PATCH_REPO=JayDEmily/nvda10" in text
    assert "Environment=AI_PATCH_ISSUE=2" in text


def test_doctor_checks_current_control_gates() -> None:
    text = (BRIDGE / "scripts" / "bridge_doctor.sh").read_text(encoding="utf-8")
    assert "bridge-blueprint-check" in text
    assert "proof-executor-check" in text
    assert "ai-bridge-blueprint-check" in text
    assert "ai-bridge-proof-executor-check" in text
    assert "gh auth status" in text


def test_installer_writes_user_systemd_service_not_system_service() -> None:
    text = (BRIDGE / "scripts" / "install_user_service.sh").read_text(encoding="utf-8")
    assert ".config/systemd/user" in text
    assert "systemctl --user daemon-reload" in text
    assert "systemctl --user restart nvda10-ai-patch-bridge.service" in text
    assert "make ai-bridge-watch" in text
