from __future__ import annotations

import importlib
from pathlib import Path

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_review_replay_dmp_v3_lineage_surfaces_are_present() -> None:
    review_contracts = _require_module("nvda_desk.contracts.review")
    replay_contracts = _require_module("nvda_desk.contracts.replay")
    packet_contracts = _require_module("nvda_desk.packets.dmp_packets")

    _require_attr(review_contracts, "PacketLineageSurface")
    _require_attr(replay_contracts, "ReplayPacketLineage")
    _require_attr(packet_contracts, "DeskModulePacketV3")


def test_review_replay_dmp_v3_fixture_root_is_present() -> None:
    fixture_root = Path("fixtures/dmp_v3")
    if not fixture_root.exists():
        pytest.fail("Required fixture root is not implemented: fixtures/dmp_v3")
