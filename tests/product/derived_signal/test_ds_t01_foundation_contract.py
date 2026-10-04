from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, is_dataclass
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from ._support import require_m01_api, require_m01_symbol

CONTEXT_TYPES = (
    "CalculationParameterSetV1",
    "RequiredFieldPolicyV1",
    "CandidateStructureContextV1",
    "CandidateSetContextV1",
    "LivePositionContextV1",
    "OrderIntentContextV1",
    "EntryStateContextV1",
    "EvaluationSetV1",
    "RecalculationScheduleV1",
    "UnitConventionVersionV1",
    "PnLConventionVersionV1",
    "OptionRevaluationConventionVersionV1",
    "ExecutionCostScheduleVersionV1",
    "AttributionPathContextV1",
    "InputSelectionPolicyVersionV1",
)


@pytest.mark.parametrize("type_name", CONTEXT_TYPES)
def test_admitted_non_signal_context_types_are_frozen_and_version_identified(
    type_name: str,
) -> None:
    context_type = require_m01_symbol(type_name)
    assert is_dataclass(context_type), type_name
    params = context_type.__dataclass_params__
    assert params.frozen, type_name
    field_names = {field.name for field in fields(context_type)}
    assert {"context_id", "version"} <= field_names


def test_unit_conversion_requires_explicit_convention_and_never_uses_magnitude_heuristics() -> None:
    convention_type = require_m01_symbol("UnitConventionVersionV1")
    percent = convention_type(
        context_id="units-percent-to-fraction",
        version=1,
        native_units="percent",
        canonical_units="fraction",
        scale=Decimal("0.01"),
        offset=Decimal("0"),
    )
    fraction = convention_type(
        context_id="units-fraction",
        version=1,
        native_units="fraction",
        canonical_units="fraction",
        scale=Decimal("1"),
        offset=Decimal("0"),
    )
    assert percent.convert(Decimal("5"), native_units="percent") == Decimal("0.05")
    assert fraction.convert(Decimal("0.05"), native_units="fraction") == Decimal("0.05")
    with pytest.raises(ValueError, match="native_units"):
        percent.convert(Decimal("0.05"), native_units="fraction")
    with pytest.raises(FrozenInstanceError):
        percent.version = 2


def test_derived_occurrence_carrier_exposes_exact_identity_time_result_and_lineage_fields() -> None:
    occurrence_type = require_m01_symbol("DerivedSignalOccurrenceV1")
    field_names = {field.name for field in fields(occurrence_type)}
    required = {
        "derived_signal_id",
        "derived_occurrence_id",
        "calculation_definition_version",
        "parameter_context_refs",
        "subject_instrument",
        "universe",
        "effective_as_of_utc",
        "window",
        "knowledge_cutoff_utc",
        "calculated_at_utc",
        "result",
        "units",
        "result_shape",
        "raw_input_lineage",
        "predecessor_occurrence_ids",
        "convention_refs",
        "supersedes_derived_occurrence_id",
    }
    assert required <= field_names
    assert occurrence_type.__dataclass_params__.frozen


def test_public_seam_distinguishes_absence_without_fabricating_default_occurrence() -> None:
    api = require_m01_api()

    class NoRawProjection:
        def project_raw_value(self, *args: object, **kwargs: object) -> None:
            return None

        def list_projected_raw_history(self, *args: object, **kwargs: object) -> tuple[()]:
            return ()

    request_type = getattr(api, "CalculationRequestV1", None)
    create_owner = getattr(api, "create_owner", None)
    if request_type is None or create_owner is None:
        pytest.fail("DS-T01 expected CalculationRequestV1 and create_owner on the M01 public seam")

    request = request_type(
        derived_signal_id="D011",
        subject_instrument="NVDA",
        as_of_utc=datetime(2026, 10, 4, 1, tzinfo=UTC),
        knowledge_cutoff_utc=datetime(2026, 10, 4, 1, tzinfo=UTC),
        calculation_definition_version="calc-v1",
        parameter_set_id="params",
        parameter_set_version=1,
        input_selection_policy_id="selection",
        input_selection_policy_version=1,
        context_refs=(),
    )
    owner = create_owner(raw_projection_reader=NoRawProjection())
    assert owner.materialise(request) is None
    assert owner.reads.get_derived_occurrence("missing-occurrence") is None
    assert owner.reads.list_derived_history(
        derived_signal_id="D011", subject_instrument="NVDA", limit=10
    ) == ()


def test_public_seam_has_no_external_effect_commands() -> None:
    api = require_m01_api()
    create_owner = getattr(api, "create_owner", None)
    if create_owner is None:
        pytest.fail("DS-T01 expected create_owner on the M01 public seam")

    class NoRawProjection:
        def project_raw_value(self, *args: object, **kwargs: object) -> None:
            return None

        def list_projected_raw_history(self, *args: object, **kwargs: object) -> tuple[()]:
            return ()

    owner = create_owner(raw_projection_reader=NoRawProjection())
    prohibited = {"place_order", "cancel_order", "modify_order", "mutate_account", "send_provider"}
    assert prohibited.isdisjoint(dir(owner))
    assert prohibited.isdisjoint(dir(owner.reads))
