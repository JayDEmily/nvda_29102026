import pkgutil
from pathlib import Path

import nvda_desk

ROOT = Path(__file__).resolve().parents[2]


def test_minimal_package_imports_and_declared_subpackages() -> None:
    assert nvda_desk.__version__ == "0.1.0"
    discovered = {item.name for item in pkgutil.iter_modules(nvda_desk.__path__)}
    assert discovered == {"architecture", "composition"}


def test_active_source_tree_contains_only_kernel_packages() -> None:
    package_root = ROOT / "src/nvda_desk"
    directories = {
        path.name for path in package_root.iterdir() if path.is_dir() and path.name != "__pycache__"
    }
    assert directories == {"architecture", "composition"}
