"""Configurable proof-only V7 false-positive active-guard implementations.

These variants are external falsification evidence. They deliberately preserve
the admitted non-durable successful behaviour while assigning active-attempt
exclusion to an over-broad owner. They are not production implementations.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any

MODE = os.environ.get("M13_V7_GUARD_MUTANT", "")
MODES = {
    "module_global_active_flag",
    "class_global_static_active_flag",
    "universal_active_marker_registry",
    "guard_keyed_only_by_command_type",
    "guard_keyed_only_by_consistency_unit_id",
    "guard_keyed_only_by_command_type_and_consistency_unit_id",
    "guard_shared_by_concrete_class",
    "early_clear_before_participant_commit_with_global_coupling",
}
if MODE not in MODES:
    raise ValueError(f"unsupported M13_V7_GUARD_MUTANT: {MODE!r}")

REFERENCE_PATH = Path(__file__).parents[1] / "v6_worker/v6_reference_conforming_source.py"
SPEC = importlib.util.spec_from_file_location("_m13_v7_reference", REFERENCE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load V7 conforming reference: {REFERENCE_PATH}")
_reference = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = _reference
SPEC.loader.exec_module(_reference)

IdempotencyConflictError = _reference.IdempotencyConflictError
StateVersionConflictError = _reference.StateVersionConflictError
IdempotencyKey = _reference.IdempotencyKey
TransactionCommand = _reference.TransactionCommand
AtomicReceipt = _reference.AtomicReceipt
RepositoryPort = _reference.RepositoryPort
UnitOfWork = _reference.UnitOfWork

_MODULE_ACTIVE = False
_UNIVERSAL_REGISTRY: set[str] = set()
_SCOPED_REGISTRY: set[Any] = set()
_CONCRETE_CLASS_REGISTRY: set[type[Any]] = set()


class _EarlyClearProxy(RepositoryPort):
    def __init__(self, *, target: RepositoryPort, boundary: Any, final: bool) -> None:
        self.target = target
        self.boundary = boundary
        self.final = final

    def prepare(self, *, command: Any, working_state: Any, receipt: Any) -> None:
        self.target.prepare(
            command=command,
            working_state=working_state,
            receipt=receipt,
        )
        if self.final:
            self.boundary._release_guard_before_commit()

    def commit(self) -> None:
        self.target.commit()

    def rollback(self) -> None:
        self.target.rollback()


class InMemoryUnitOfWork(_reference.InMemoryUnitOfWork):
    """Reference behaviour with one separately selectable over-broad guard."""

    _class_global_active = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._guard_key: Any = None
        self._guard_acquired = False
        if MODE == "early_clear_before_participant_commit_with_global_coupling":
            ports = self._repository_ports
            self._repository_ports = tuple(
                _EarlyClearProxy(
                    target=port,
                    boundary=self,
                    final=index == len(ports) - 1,
                )
                for index, port in enumerate(ports)
            )

    @staticmethod
    def _overbroad_key(command: TransactionCommand) -> Any:
        if MODE == "guard_keyed_only_by_command_type":
            return command.idempotency_key.command_type
        if MODE == "guard_keyed_only_by_consistency_unit_id":
            return command.idempotency_key.consistency_unit_id
        if MODE == "guard_keyed_only_by_command_type_and_consistency_unit_id":
            return (
                command.idempotency_key.command_type,
                command.idempotency_key.consistency_unit_id,
            )
        return None

    def _is_overbroad_guard_active(self, command: TransactionCommand) -> bool:
        if MODE in {
            "module_global_active_flag",
            "early_clear_before_participant_commit_with_global_coupling",
        }:
            return _MODULE_ACTIVE
        if MODE == "class_global_static_active_flag":
            return InMemoryUnitOfWork._class_global_active
        if MODE == "universal_active_marker_registry":
            return "active" in _UNIVERSAL_REGISTRY
        if MODE == "guard_shared_by_concrete_class":
            return type(self) in _CONCRETE_CLASS_REGISTRY
        return self._overbroad_key(command) in _SCOPED_REGISTRY

    def _acquire_overbroad_guard(self, command: TransactionCommand) -> None:
        global _MODULE_ACTIVE
        if MODE in {
            "module_global_active_flag",
            "early_clear_before_participant_commit_with_global_coupling",
        }:
            _MODULE_ACTIVE = True
        elif MODE == "class_global_static_active_flag":
            InMemoryUnitOfWork._class_global_active = True
        elif MODE == "universal_active_marker_registry":
            _UNIVERSAL_REGISTRY.add("active")
        elif MODE == "guard_shared_by_concrete_class":
            _CONCRETE_CLASS_REGISTRY.add(type(self))
        else:
            self._guard_key = self._overbroad_key(command)
            _SCOPED_REGISTRY.add(self._guard_key)
        self._guard_acquired = True

    def _release_overbroad_guard(self) -> None:
        global _MODULE_ACTIVE
        if not self._guard_acquired:
            return
        if MODE in {
            "module_global_active_flag",
            "early_clear_before_participant_commit_with_global_coupling",
        }:
            _MODULE_ACTIVE = False
        elif MODE == "class_global_static_active_flag":
            InMemoryUnitOfWork._class_global_active = False
        elif MODE == "universal_active_marker_registry":
            _UNIVERSAL_REGISTRY.discard("active")
        elif MODE == "guard_shared_by_concrete_class":
            _CONCRETE_CLASS_REGISTRY.discard(type(self))
        else:
            _SCOPED_REGISTRY.discard(self._guard_key)
        self._guard_acquired = False

    def _release_guard_before_commit(self) -> None:
        if MODE != "early_clear_before_participant_commit_with_global_coupling":
            return
        self._active_attempt = False
        self._release_overbroad_guard()

    def execute(
        self,
        *,
        command: TransactionCommand,
        mutation: Any,
    ) -> AtomicReceipt:
        if not isinstance(command, TransactionCommand):
            raise TypeError("command must be a TransactionCommand")
        if not callable(mutation):
            raise TypeError("mutation must be callable")
        if self._active_attempt or self._is_overbroad_guard_active(command):
            raise RuntimeError("UnitOfWork.execute attempt is already active")

        self._active_attempt = True
        self._acquire_overbroad_guard(command)
        try:
            return self._execute_active(command=command, mutation=mutation)
        finally:
            self._release_overbroad_guard()
            self._active_attempt = False
