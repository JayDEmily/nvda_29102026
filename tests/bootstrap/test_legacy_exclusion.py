import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_no_former_runtime_package_is_active() -> None:
    source_root = ROOT / "src/nvda_desk"
    forbidden = [
        path.name
        for path in source_root.iterdir()
        if path.is_dir() and re.fullmatch(r"m(?:0[0-9]|1[0-5])_.*", path.name)
    ]
    assert forbidden == []
    for name in ("contracts", "packets", "preparation", "runtime", "cognition", "domain"):
        assert not (source_root / name).exists()


def test_blocking_proof_population_remains_within_kernel_jurisdictions() -> None:
    test_families = yaml.safe_load(
        (ROOT / "config/proof/test_families.yaml").read_text(encoding="utf-8")
    )
    assert all(
        item["path"].startswith(("tests/architecture/", "tests/bootstrap/"))
        for item in test_families["test_families"]
    )


def test_minimal_project_dependencies_and_entry_points_exclude_old_runtime() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    for dependency in (
        "fastapi",
        "sqlalchemy",
        "asyncpg",
        "ibapi",
        "polars",
        "openpyxl",
    ):
        assert dependency not in pyproject
    assert '"psycopg[binary]==3.3.4"' in pyproject
    assert "nvda-architecture-kernel" in pyproject
