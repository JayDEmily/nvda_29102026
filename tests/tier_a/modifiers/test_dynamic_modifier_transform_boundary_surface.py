"""Tier A transform-boundary tests for dynamic coefficient/modifier authority."""

from __future__ import annotations

import ast
from pathlib import Path


ACTIVE_DYNAMIC_MODIFIER_FILES = [
    Path("src/nvda_desk/cognition/modifiers/__init__.py"),
    Path("src/nvda_desk/cognition/modifiers/state_conditioned.py"),
    Path("src/nvda_desk/config/coefficient_authority.py"),
    Path("src/nvda_desk/contracts/coefficient_authority.py"),
    Path("src/nvda_desk/contracts/modifiers.py"),
    Path("src/nvda_desk/services/coefficient_authority_service.py"),
    Path("src/nvda_desk/domain/posture/modifier_application.py"),
]

FORBIDDEN_DONOR_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.config_models",
    "nvda_desk.schemas.cognition",
    "nvda_desk.schemas.market",
    "nvda_desk.schemas.risk",
    "nvda_desk.schemas.state_policy",
    "nvda_desk.services.state_conditioned_modifier",
)

FORBIDDEN_DONOR_STATE_POLICY_NAMES = {
    "CombinationLaw",
    "EffectiveCoefficientLineage",
    "KillSwitchCondition",
    "ModifierPriorityBand",
    "ModifierTransformType",
    "MutableRuntimeSurface",
    "NonActionClass",
    "ResolvedRuntimeSurfaceValue",
    "SignalConflictClass",
}


def _imports_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def _top_level_defs_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
    }


def test_active_dynamic_modifier_files_do_not_import_donor_modifier_stack() -> None:
    """Native row 5.9 files must not recreate the donor schema/service stack by import."""

    for path in ACTIVE_DYNAMIC_MODIFIER_FILES:
        imports = _imports_for(path)
        forbidden = {
            imported
            for imported in imports
            if any(
                imported == prefix or imported.startswith(f"{prefix}.")
                for prefix in FORBIDDEN_DONOR_IMPORT_PREFIXES
            )
        }
        assert forbidden == set(), f"{path} imports donor modifier stack modules: {sorted(forbidden)}"


def test_active_dynamic_modifier_files_do_not_redeclare_donor_state_policy_surface() -> None:
    """The native surface keeps lean coefficient/modifier contracts instead of donor state-policy grammar."""

    for path in ACTIVE_DYNAMIC_MODIFIER_FILES:
        declared = _top_level_defs_for(path)
        forbidden = declared & FORBIDDEN_DONOR_STATE_POLICY_NAMES
        assert forbidden == set(), f"{path} redeclares donor state-policy names: {sorted(forbidden)}"


def test_compatibility_wrappers_remain_thin_native_forwarders() -> None:
    """Compatibility paths must forward to native owners without carrying donor runtime logic."""

    service_module = ast.parse(
        Path("src/nvda_desk/services/coefficient_authority_service.py").read_text(encoding="utf-8")
    )
    service_defs = _top_level_defs_for(Path("src/nvda_desk/services/coefficient_authority_service.py"))
    assert service_defs == set()
    service_imports = _imports_for(Path("src/nvda_desk/services/coefficient_authority_service.py"))
    assert service_imports == {"__future__", "nvda_desk.config.coefficient_authority"}
    assert len(service_module.body) <= 4

    modifier_defs = _top_level_defs_for(Path("src/nvda_desk/domain/posture/modifier_application.py"))
    assert modifier_defs == {"apply_modifiers"}
    modifier_imports = _imports_for(Path("src/nvda_desk/domain/posture/modifier_application.py"))
    assert modifier_imports == {"__future__", "nvda_desk.cognition.modifiers.state_conditioned"}
