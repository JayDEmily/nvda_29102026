import pytest

from nvda_desk.architecture.identifiers import next_identifier, parse_identifier


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
