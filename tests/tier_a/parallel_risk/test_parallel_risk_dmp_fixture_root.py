from __future__ import annotations

from pathlib import Path

import pytest


def test_dmp_v3_fixture_root_is_present_for_parallel_risk_shell_proofs() -> None:
    fixture_root = Path("fixtures/dmp_v3")

    assert fixture_root.parts == ("fixtures", "dmp_v3")
    if not fixture_root.exists():
        pytest.fail("Required fixture root is not implemented: fixtures/dmp_v3")
    assert fixture_root.exists() is True
    if not fixture_root.is_dir():
        pytest.fail("Required fixture root is not a directory: fixtures/dmp_v3")
    assert fixture_root.is_dir() is True
