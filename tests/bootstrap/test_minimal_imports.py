import pkgutil
from pathlib import Path

import nvda_desk
from nvda_desk.architecture.registry import ArchitectureRegistry

ROOT = Path(__file__).resolve().parents[2]


def _admitted_top_level_packages(*, statuses: set[str]) -> set[str]:
    registry = ArchitectureRegistry.from_repository(ROOT)
    return {
        item.package.split(".", 1)[1].split(".", 1)[0]
        for item in registry.package_owners()
        if item.status in statuses and item.package is not None
    }


def test_package_imports_match_kernel_plus_admitted_owner_packages() -> None:
    assert nvda_desk.__version__ == "1.0.0"
    discovered = {item.name for item in pkgutil.iter_modules(nvda_desk.__path__)}
    required = {"architecture", "composition"} | _admitted_top_level_packages(statuses={"active"})
    permitted = {"architecture", "composition"} | _admitted_top_level_packages(
        statuses={"bootstrap", "active"}
    )
    # AK-EXT bootstrap may declare a seam before its physical implementation.
    assert required <= discovered <= permitted


def test_active_source_tree_matches_kernel_plus_admitted_owner_packages() -> None:
    package_root = ROOT / "src/nvda_desk"
    directories = {
        path.name for path in package_root.iterdir() if path.is_dir() and path.name != "__pycache__"
    }
    required = {"architecture", "composition"} | _admitted_top_level_packages(statuses={"active"})
    permitted = {"architecture", "composition"} | _admitted_top_level_packages(
        statuses={"bootstrap", "active"}
    )
    assert required <= directories <= permitted
