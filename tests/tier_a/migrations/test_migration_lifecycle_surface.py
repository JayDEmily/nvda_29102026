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


def test_migration_lifecycle_surface_is_present() -> None:
    package_module = _require_module("nvda_desk.persistence.migrations")
    assert package_module.__name__ == "nvda_desk.persistence.migrations"
    layout_module = _require_module("nvda_desk.persistence.migrations.layout")
    assert layout_module.__name__ == "nvda_desk.persistence.migrations.layout"

    assert _require_attr(package_module, "MigrationLifecycleLayout") is getattr(
        package_module, "MigrationLifecycleLayout"
    )
    assert _require_attr(package_module, "describe_migration_lifecycle") is getattr(
        package_module, "describe_migration_lifecycle"
    )
    assert _require_attr(layout_module, "PACKAGE_HOME") is getattr(layout_module, "PACKAGE_HOME")
    assert _require_attr(layout_module, "describe_migration_lifecycle") is getattr(
        layout_module, "describe_migration_lifecycle"
    )


def test_migration_lifecycle_boundary_is_explicit_and_bounded() -> None:
    layout_module = _require_module("nvda_desk.persistence.migrations.layout")
    assert layout_module.__name__ == "nvda_desk.persistence.migrations.layout"

    describe_migration_lifecycle = _require_attr(layout_module, "describe_migration_lifecycle")
    assert describe_migration_lifecycle is getattr(layout_module, "describe_migration_lifecycle")
    package_home = _require_attr(layout_module, "PACKAGE_HOME")
    assert package_home is getattr(layout_module, "PACKAGE_HOME")
    layout = describe_migration_lifecycle()

    assert package_home == "nvda_desk.persistence.migrations"
    assert layout.package_home == package_home
    assert layout.package_root.name == "migrations"
    assert layout.alembic_root == Path("alembic").resolve()
    assert layout.alembic_versions_root == Path("alembic/versions").resolve()
    assert layout.package_root != layout.alembic_root
    assert layout.alembic_versions_root.parent == layout.alembic_root

    alembic_readme = Path("alembic/README.md").read_text(encoding="utf-8")
    versions_readme = Path("alembic/versions/README.md").read_text(encoding="utf-8")
    assert "nvda_desk.persistence.migrations" in alembic_readme
    assert "placeholder" in alembic_readme.lower()
    assert "present revision-root placeholder" in versions_readme
