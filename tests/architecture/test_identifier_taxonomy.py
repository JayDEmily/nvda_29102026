import shutil
from pathlib import Path

import pytest
import yaml

from nvda_desk.architecture.allocation import (
    load_implementation_allocations,
    resolve_candidate_identifiers,
)
from nvda_desk.architecture.identifiers import next_identifier, parse_identifier

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("value", ["M00", "M99", "M100", "P01", "G1000000", "A00", "K01", "S42"])
def test_category_correct_unbounded_identifiers_are_valid(value: str) -> None:
    assert str(parse_identifier(value)) == value


@pytest.mark.parametrize("value", ["M1", "M000", "X01", "m01", "M-01", "M", "M01x", "M-1"])
def test_malformed_or_unknown_categories_are_rejected(value: str) -> None:
    with pytest.raises(ValueError):
        parse_identifier(value)


def test_identifier_allocation_crosses_two_digit_boundary_without_enumeration() -> None:
    assert next_identifier("M", {"M00", "M98", "M99"}) == "M100"
    assert next_identifier("M", {"M999999"}) == "M1000000"


def test_post_reset_allocation_history_starts_empty() -> None:
    assert load_implementation_allocations(ROOT) == ()


def test_candidate_resolution_uses_current_post_reset_state_in_request_order() -> None:
    assert resolve_candidate_identifiers(ROOT, ["M", "M", "A"]) == ("M00", "M01", "A01")


def test_candidate_resolution_does_not_mutate_allocation_history() -> None:
    allocation_path = ROOT / "config/architecture/implementation_allocations.yaml"
    before = allocation_path.read_bytes()
    assert resolve_candidate_identifiers(ROOT, ["M"]) == ("M00",)
    assert allocation_path.read_bytes() == before


def test_candidate_resolution_honours_retired_and_durable_post_reset_ids(tmp_path: Path) -> None:
    repository = tmp_path / "repo"
    shutil.copytree(ROOT / "config", repository / "config")
    shutil.copytree(ROOT / "schemas", repository / "schemas")

    modules_path = repository / "config/architecture/modules.yaml"
    modules = yaml.safe_load(modules_path.read_text(encoding="utf-8"))
    modules["retired_ids"] = ["M00"]
    modules_path.write_text(yaml.safe_dump(modules, sort_keys=False), encoding="utf-8")

    allocations_path = repository / "config/architecture/implementation_allocations.yaml"
    allocations_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "implementation_allocations": [
                    {
                        "object_id": "M01",
                        "name": "previously_implemented",
                        "implemented_on": "2026-09-10",
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    assert resolve_candidate_identifiers(repository, ["M", "M"]) == ("M02", "M03")
