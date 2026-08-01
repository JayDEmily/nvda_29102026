"""Contract package for bounded native runtime schemas.

Submodules are loaded lazily so importing one contract family cannot execute
unrelated families and create import-order-dependent cycles.
"""

from __future__ import annotations

from importlib import import_module
from types import ModuleType

__all__ = [
    "capital",
    "coefficient_authority",
    "common",
    "downstream",
    "eligibility",
    "execution",
    "modifiers",
    "options_flow",
    "options_flow_history",
    "packets",
    "playbook",
    "parallel_risk",
    "posture",
    "reference_data",
    "regime",
    "replay",
    "review",
    "risk",
    "stage_inputs",
    "temporal",
    "trace_review",
]


def __getattr__(name: str) -> ModuleType:
    if name not in __all__:
        raise AttributeError(name)
    module = import_module(f"{__name__}.{name}")
    globals()[name] = module
    return module


def __dir__() -> list[str]:
    return sorted((*globals(), *__all__))
