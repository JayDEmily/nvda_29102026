from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from ._support import projection_mapping, raw_observation, require_m01_symbol


def _version_ref(token: str = "ctx"):
    return require_m01_symbol("VersionRefV1")(context_id=token, version=1)


def _raw_lineage(raw_id: str = "R001"):
    return require_m01_symbol("RawInputLineageV1")(
        raw_signal_id=raw_id,
        observation_occurrence_id="obs-1",
        projection_mapping_id="mapping-1",
        projection_mapping_version=1,
        unit_convention_id="unit-1",
        unit_convention_version=1,
        native_units="percent",
        canonical_units="fraction",
    )


def _occurrence(**overrides: object):
    occurrence_type = require_m01_symbol("DerivedSignalOccurrenceV1")
    values: dict[str, object] = {
        "derived_signal_id": "D011",
        "derived_occurrence_id": "derived-1",
        "calculation_definition_version": "calc-v1",
        "parameter_context_refs": (_version_ref("params"),),
        "subject_instrument": "NVDA",
        "universe": None,
        "effective_as_of_utc": datetime(2026, 10, 4, 1, tzinfo=UTC),
        "window": None,
        "knowledge_cutoff_utc": datetime(2026, 10, 4, 1, tzinfo=UTC),
        "calculated_at_utc": datetime(2026, 10, 4, 1, 0, 1, tzinfo=UTC),
        "result": Decimal("123.45"),
        "units": "USD",
        "result_shape": "scalar_numeric",
        "raw_input_lineage": (_raw_lineage(),),
        "predecessor_occurrence_ids": (),
        "convention_refs": (_version_ref("units"),),
        "supersedes_derived_occurrence_id": None,
    }
    values.update(overrides)
    return occurrence_type(**values)


def _request(**overrides: object):
    request_type = require_m01_symbol("CalculationRequestV1")
    values: dict[str, object] = {
        "derived_signal_id": "D011",
        "subject_instrument": "NVDA",
        "as_of_utc": datetime(2026, 10, 4, 1, tzinfo=UTC),
        "knowledge_cutoff_utc": datetime(2026, 10, 4, 1, tzinfo=UTC),
        "calculation_definition_version": "calc-v1",
        "parameter_set_id": "params",
        "parameter_set_version": 1,
        "input_selection_policy_id": "selection",
        "input_selection_policy_version": 1,
        "context_refs": (_version_ref("candidate"),),
    }
    values.update(overrides)
    return request_type(**values)


def test_m00_history_can_filter_true_instant_by_event_time_independently_of_receipt_time() -> None:
    owner = raw_api.create_owner()
    receipt = datetime(2026, 10, 4, 1, 0, tzinfo=UTC)
    event = datetime(2026, 10, 4, 2, 0, tzinfo=UTC)
    observation = replace(
        raw_observation("1", native_value=Decimal("5"), received_ts_utc=receipt),
        source_timestamp_raw=event.isoformat(),
        source_timezone_native="UTC",
        source_temporal_kind="true_instant",
    )
    owner.commands.admit_raw_observation_occurrence(observation)

    page = owner.reads.list_projected_raw_history(
        raw_api.RawSignalCatalogueId("R001"),
        mappings=(projection_mapping(),),
        subject_instrument="NVDA",
        received_at_or_before_utc=receipt + timedelta(minutes=30),
        event_at_or_before_utc=receipt + timedelta(minutes=30),
        limit=10,
        cursor=None,
    )
    assert page.items == ()


def test_m00_event_time_filter_never_fabricates_event_time_for_receipt_only_observation() -> None:
    owner = raw_api.create_owner()
    receipt = datetime(2026, 10, 4, 1, 0, tzinfo=UTC)
    observation = replace(
        raw_observation("2", native_value=Decimal("5"), received_ts_utc=receipt),
        source_temporal_kind="receipt_only",
        source_timestamp_raw=None,
        source_timezone_native=None,
    )
    owner.commands.admit_raw_observation_occurrence(observation)

    page = owner.reads.list_projected_raw_history(
        raw_api.RawSignalCatalogueId("R001"),
        mappings=(projection_mapping(),),
        subject_instrument="NVDA",
        received_at_or_before_utc=receipt + timedelta(hours=1),
        event_at_or_before_utc=receipt + timedelta(hours=1),
        limit=10,
        cursor=None,
    )
    assert page.items == ()


@pytest.mark.parametrize("raw_id", ["ABCD", "R000", "R324", "R01", "R0001"])
def test_raw_input_lineage_requires_canonical_admitted_r_identity(raw_id: str) -> None:
    with pytest.raises(ValueError, match="raw_signal_id"):
        _raw_lineage(raw_id)


def test_calculation_request_context_refs_are_exact_version_refs() -> None:
    with pytest.raises(TypeError, match="context_refs"):
        _request(context_refs=("candidate:v1",))


def test_calculation_request_context_refs_do_not_accept_duplicate_identity_versions() -> None:
    duplicate = _version_ref("candidate")
    with pytest.raises(ValueError, match="context_refs"):
        _request(context_refs=(duplicate, duplicate))


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("parameter_context_refs", ("params:v1",)),
        ("raw_input_lineage", ("R001:obs-1",)),
        ("convention_refs", ("units:v1",)),
    ],
)
def test_occurrence_lineage_collections_require_exact_typed_refs(
    field_name: str, bad_value: tuple[str, ...]
) -> None:
    with pytest.raises(TypeError, match=field_name):
        _occurrence(**{field_name: bad_value})


def test_occurrence_version_ref_collections_reject_duplicate_identity_versions() -> None:
    duplicate = _version_ref("params")
    with pytest.raises(ValueError, match="parameter_context_refs"):
        _occurrence(parameter_context_refs=(duplicate, duplicate))


def test_occurrence_predecessor_ids_are_non_empty_and_distinct() -> None:
    with pytest.raises(ValueError, match="predecessor_occurrence_ids"):
        _occurrence(predecessor_occurrence_ids=("",))
    with pytest.raises(ValueError, match="predecessor_occurrence_ids"):
        _occurrence(predecessor_occurrence_ids=("d-prev", "d-prev"))


def test_occurrence_universe_members_are_non_empty_and_distinct() -> None:
    with pytest.raises(ValueError, match="universe"):
        _occurrence(universe=("NVDA", ""))
    with pytest.raises(ValueError, match="universe"):
        _occurrence(universe=("NVDA", "NVDA"))


def test_persisted_occurrence_result_cannot_be_none_because_absence_is_separate() -> None:
    with pytest.raises((TypeError, ValueError), match="result"):
        _occurrence(result=None)


@pytest.mark.parametrize("bad_result", [[1, 2], {"x": 1}, 1.25, object()])
def test_persisted_occurrence_result_rejects_unadmitted_mutable_or_float_carriers(
    bad_result: object,
) -> None:
    with pytest.raises((TypeError, ValueError), match="result"):
        _occurrence(result=bad_result)


def test_persisted_occurrence_nested_tuple_result_accepts_admitted_typed_carrier() -> None:
    occurrence = _occurrence(
        result=(Decimal("1.0"), ("up", True), datetime(2026, 10, 4, 1, tzinfo=UTC)),
        result_shape="structured",
    )
    assert occurrence.result_shape == "structured"


def test_repaired_clause6_contexts_remain_constructible_with_context_specific_content() -> None:
    candidate_type = require_m01_symbol("CandidateStructureContextV1")
    selection_type = require_m01_symbol("InputSelectionPolicyVersionV1")

    candidate = candidate_type(
        context_id="candidate-1",
        version=1,
        candidate_identity="candidate-1",
        leg_contract_identities=("NVDA-C-20261218-150",),
        leg_sides=("buy",),
        leg_quantities=(Decimal("1"),),
        quantity=Decimal("1"),
        premium_assumptions=(("entry_premium", Decimal("5.25")),),
        entry_assumptions=(("entry_basis", "premium"),),
        risk_capital_currency=Decimal("10000"),
    )
    selection = selection_type(
        context_id="selection-1",
        version=1,
        join_keys=("subject_instrument",),
        maximum_staleness=timedelta(minutes=5),
        maximum_skew=timedelta(seconds=2),
        temporal_basis_permissions=("true_instant", "receipt_only"),
        basket_membership=("NVDA",),
    )
    assert candidate.candidate_identity == "candidate-1"
    assert selection.maximum_staleness == timedelta(minutes=5)
