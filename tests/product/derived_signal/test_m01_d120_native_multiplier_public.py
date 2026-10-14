"""D120 native-field witnesses: catch R015 substitution and contract/time aliases."""

from __future__ import annotations

import importlib.util
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

SPEC = importlib.util.spec_from_file_location(
    "d120_native_fixture", Path(__file__).with_name("native_signed_flow_fixture.py")
)
assert SPEC is not None and SPEC.loader is not None
fixture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fixture)


def owner_for(points, *, selection=None):
    class Reader:
        def list_projected_raw_history(self, rid, **kwargs):
            return raw.ProjectedRawHistoryPageV1(tuple(points.get(rid.value, ())), None)

        def project_raw_value(self, *args, **kwargs):
            return None

    return api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=fixture.models,
        parameter_sets=fixture.params,
        input_selection_policies=(fixture.selection if selection is None else selection,),
        unit_conventions=fixture.units,
        contexts=(),
        utc_now=lambda: fixture.NOW + timedelta(minutes=1),
    )


def points():
    return {rid: (value,) for rid, value in fixture.points.items()}


def test_native_right_and_independent_metadata_multiplier_calculate_exact_notional():
    owner = owner_for(points())
    request = replace(
        fixture.request("D120"), calculation_definition_version="D120-NATIVE-MULTIPLIER-20261015-01"
    )
    result = owner.materialise(request)
    assert result is not None
    assert dict(result.result) == {
        "signed_contracts": Decimal("2"),
        "signed_premium_notional": Decimal("1200"),
    }
    assert {
        (item.raw_signal_id, item.observation_occurrence_id) for item in result.raw_input_lineage
    } >= {("R015", "contract-C100"), ("R016", "contract-C100"), ("R120", "obs-trade-C100")}
    assert owner.materialise(request) == result


@pytest.mark.parametrize(
    "multiplier,want", [(Decimal("10"), Decimal("120")), (Decimal("50"), Decimal("600"))]
)
def test_actual_multiplier_is_used_without_a_default(multiplier, want):
    data = points()
    data["R016"] = (replace(data["R016"][0], native_value=multiplier),)
    result = owner_for(data).materialise(fixture.request("D120"))
    assert result is not None and dict(result.result)["signed_premium_notional"] == want


@pytest.mark.parametrize("field", ["R015", "R016"])
def test_missing_contract_field_refuses(field):
    data = points()
    data.pop(field)
    assert owner_for(data).materialise(fixture.request("D120")) is None


@pytest.mark.parametrize(
    "value", [Decimal("0"), Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), "100", True]
)
def test_invalid_multiplier_refuses(value):
    data = points()
    data["R016"] = (replace(data["R016"][0], native_value=value),)
    assert owner_for(data).materialise(fixture.request("D120")) is None


@pytest.mark.parametrize("value", [Decimal("100"), "P", "call"])
def test_numeric_or_disagreeing_native_right_refuses(value):
    data = points()
    data["R015"] = (replace(data["R015"][0], native_value=value),)
    assert owner_for(data).materialise(fixture.request("D120")) is None


@pytest.mark.parametrize("field", ["R015", "R016"])
def test_metadata_for_another_contract_refuses(field):
    data = points()
    wrong = raw.RawSelectionIdentityV1(
        tuple(
            (key, "C200" if key == "contract_id" else value) for key, value in fixture.IDENT.values
        )
    )
    data[field] = (replace(data[field][0], selection_identity=wrong),)
    assert owner_for(data).materialise(fixture.request("D120")) is None


@pytest.mark.parametrize("field", ["R015", "R016"])
def test_metadata_discovered_after_trade_refuses_even_when_visible_at_later_cutoff(field):
    data = points()
    later = fixture.NOW + timedelta(seconds=1)
    data[field] = (replace(data[field][0], received_ts_utc=later),)
    request = replace(fixture.request("D120"), as_of_utc=later, knowledge_cutoff_utc=later)
    assert owner_for(data).materialise(request) is None


@pytest.mark.parametrize("field", ["R015", "R016"])
def test_latest_metadata_priority_tie_refuses(field):
    data = points()
    data[field] += (
        replace(
            data[field][0],
            observation_occurrence_id=raw.observation_occurrence_id("ambiguous-metadata"),
        ),
    )
    assert owner_for(data).materialise(fixture.request("D120")) is None


def test_latest_known_metadata_is_selected_and_older_metadata_is_not_claimed_as_input():
    data = points()
    older = replace(
        data["R016"][0],
        received_ts_utc=fixture.NOW - timedelta(seconds=2),
        observation_occurrence_id=raw.observation_occurrence_id("older-multiplier"),
        native_value=Decimal("10"),
    )
    data["R016"] = (older, *data["R016"])
    result = owner_for(data).materialise(fixture.request("D120"))
    assert result is not None and dict(result.result)["signed_premium_notional"] == Decimal("1200")
    assert {
        item.observation_occurrence_id
        for item in result.raw_input_lineage
        if item.raw_signal_id == "R016"
    } == {"contract-C100"}


def test_future_metadata_does_not_reprice_an_earlier_trade():
    data = points()
    later = fixture.NOW + timedelta(seconds=1)
    data["R016"] += (
        replace(
            data["R016"][0],
            received_ts_utc=later,
            observation_occurrence_id=raw.observation_occurrence_id("later-multiplier"),
            native_value=Decimal("10"),
        ),
    )
    request = replace(fixture.request("D120"), as_of_utc=later, knowledge_cutoff_utc=later)
    result = owner_for(data).materialise(request)
    assert result is not None and dict(result.result)["signed_premium_notional"] == Decimal("1200")
    assert {
        item.observation_occurrence_id
        for item in result.raw_input_lineage
        if item.raw_signal_id == "R016"
    } == {"contract-C100"}


def test_receipt_only_metadata_requires_explicit_temporal_permission():
    policy = replace(fixture.selection, temporal_basis_permissions=("true_instant",))
    assert owner_for(points(), selection=policy).materialise(fixture.request("D120")) is None


def test_stale_multiplier_refuses():
    data = points()
    data["R016"] = (replace(data["R016"][0], received_ts_utc=fixture.NOW - timedelta(minutes=2)),)
    assert owner_for(data).materialise(fixture.request("D120")) is None
