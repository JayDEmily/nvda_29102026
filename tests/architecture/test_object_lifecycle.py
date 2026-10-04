from pathlib import Path

import pytest

from nvda_desk.architecture.registry import ArchitectureObject, ArchitectureRegistry
from nvda_desk.composition import CompositionPlan

ROOT = Path(__file__).resolve().parents[2]


def test_non_active_foundation_identities_are_not_composable() -> None:
    registry = ArchitectureRegistry.from_repository(ROOT)
    assert registry.get("M01").status == "placeholder"
    for object_id in ("M01", "P01", "G01", "A00", "K01"):
        with pytest.raises(ValueError, match="not composable"):
            registry.require_composable(object_id)


def test_retired_identifier_and_lifecycle_lineage_are_validated() -> None:
    item = ArchitectureObject("M100", "candidate", "placeholder", "candidate")
    with pytest.raises(ValueError, match="retired identifiers were reused"):
        ArchitectureRegistry((item,), frozenset({"M100"}))

    malformed = ArchitectureObject(
        "M100", "candidate", "placeholder", "candidate", predecessors=("NOT_AN_ID",)
    )
    with pytest.raises(ValueError, match="invalid architecture identifier"):
        ArchitectureRegistry((malformed,), frozenset())

    retired_lineage = ArchitectureObject(
        "P100", "contract", "placeholder", "contract", predecessors=("M104",)
    )
    ArchitectureRegistry((retired_lineage,), frozenset({"M104"}))

    unreserved_lineage = ArchitectureObject(
        "P101", "contract", "placeholder", "contract", predecessors=("M105",)
    )
    with pytest.raises(ValueError, match="unregistered lifecycle predecessor M105"):
        ArchitectureRegistry((unreserved_lineage,), frozenset())

    predecessor = ArchitectureObject("M100", "old", "deprecated", "old", successors=("M101",))
    successor = ArchitectureObject(
        "M101",
        "new",
        "active",
        "new",
        package="nvda_desk.new",
        public_seam="nvda_desk.new.api",
        predecessors=("M100",),
    )
    ArchitectureRegistry((predecessor, successor), frozenset())

    current_without_reciprocal = ArchitectureObject(
        "M100", "old", "deprecated", "old"
    )
    one_sided = ArchitectureObject(
        "M102", "one_sided", "placeholder", "one-sided", predecessors=("M100",)
    )
    with pytest.raises(ValueError, match="does not name M102 as successor"):
        ArchitectureRegistry((current_without_reciprocal, one_sided), frozenset())


def test_active_executable_object_requires_package_and_public_seam() -> None:
    for object_id in ("M100", "K100"):
        item = ArchitectureObject(object_id, "candidate", "active", "candidate")
        with pytest.raises(ValueError, match="lacks package/public_seam"):
            ArchitectureRegistry((item,), frozenset())

    declarative_protocol = ArchitectureObject("P100", "contract", "active", "contract")
    registry = ArchitectureRegistry((declarative_protocol,), frozenset())
    assert registry.package_owners() == ()

    python_visible_protocol = ArchitectureObject(
        "P101",
        "python_contract",
        "active",
        "contract",
        package="nvda_desk.protocol_contract",
        public_seam="nvda_desk.protocol_contract.api",
    )
    registry = ArchitectureRegistry((python_visible_protocol,), frozenset())
    assert registry.package_owners() == (python_visible_protocol,)

    active_module = ArchitectureObject(
        "M102",
        "runtime",
        "active",
        "runtime",
        package="nvda_desk.runtime",
        public_seam="nvda_desk.runtime.api",
    )
    active_kernel = ArchitectureObject(
        "K102",
        "kernel",
        "active",
        "kernel",
        package="nvda_desk.kernel",
        public_seam="nvda_desk.kernel.api",
    )
    registry = ArchitectureRegistry((active_module, active_kernel), frozenset())
    assert CompositionPlan.from_registry(registry).object_ids == ("K102", "M102")
