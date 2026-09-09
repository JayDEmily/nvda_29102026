import shutil
from pathlib import Path

import pytest

from nvda_desk.architecture.proof import load_and_validate_proof_state

ROOT = Path(__file__).resolve().parents[2]


def test_current_proof_population_is_exact_and_registry_derived() -> None:
    state = load_and_validate_proof_state(ROOT)
    assert len(state.families) == 9
    assert len(state.paths_for_set("architecture_kernel")) == 9
    assert {family["tier"] for family in state.families} == {"Tier A"}
    assert {family["lifecycle"] for family in state.families} == {"current_blocking"}


def test_unadmitted_physical_test_is_rejected(tmp_path: Path) -> None:
    for name in ("config", "schemas", "docs", "tests"):
        source = ROOT / name
        target = tmp_path / name
        if source.is_dir():
            shutil.copytree(source, target)
    extra = tmp_path / "tests/architecture/test_unadmitted.py"
    extra.write_text("def test_unadmitted(): assert True\n", encoding="utf-8")
    with pytest.raises(ValueError, match="test admission mismatch"):
        load_and_validate_proof_state(tmp_path)
