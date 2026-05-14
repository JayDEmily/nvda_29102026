"""Describe the admitted migration-lifecycle layout for persistence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PACKAGE_HOME = "nvda_desk.persistence.migrations"


@dataclass(frozen=True)
class MigrationLifecycleLayout:
    """Bounded description of the current migration-lifecycle layout."""

    package_home: str
    package_root: Path
    alembic_root: Path
    alembic_versions_root: Path

    def as_dict(self) -> dict[str, str]:
        """Return a string-safe view of the current layout."""
        return {
            "package_home": self.package_home,
            "package_root": str(self.package_root),
            "alembic_root": str(self.alembic_root),
            "alembic_versions_root": str(self.alembic_versions_root),
        }


def describe_migration_lifecycle(repo_root: Path | None = None) -> MigrationLifecycleLayout:
    """Return the admitted relationship between the package-owned home and Alembic tool root."""

    resolved_repo_root = (
        Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[4]
    )
    package_root = Path(__file__).resolve().parent
    alembic_root = (resolved_repo_root / "alembic").resolve()
    alembic_versions_root = (alembic_root / "versions").resolve()
    return MigrationLifecycleLayout(
        package_home=PACKAGE_HOME,
        package_root=package_root,
        alembic_root=alembic_root,
        alembic_versions_root=alembic_versions_root,
    )
