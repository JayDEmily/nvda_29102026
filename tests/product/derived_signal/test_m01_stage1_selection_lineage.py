from __future__ import annotations

from dataclasses import fields
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw_api

NOW = datetime(2026, 10, 8, 5, 30, tzinfo=UTC)
OPTION_KEYS = (
    "contract_id",
    "underlying_instrument",
    "expiry",
    "strike",
    "option_right",
)


def _identity(contract_id: str) -> raw_api.RawSelectionIdentityV1:
    return raw_api.RawSelectionIdentityV1(
        values=(
            ("contract_id", contract_id),
            ("underlying_instrument", "NVDA"),
            ("expiry", "2026-12-18"),
            ("strike", Decimal("150")),
            ("option_right", "call"),
        )
    )


def _parameter(profile: str, context_id: str, **values: object) -> api.CalculationParameterSetV1:
    configured = values or {"selection_mode": "exact"}
    return api.CalculationParameterSetV1(
        context_id=context_id,
        version=1,
        profile=profile,
        parameters=tuple(configured.items()),
    )


def _selection(context_id: str) -> api.InputSelectionPolicyVersionV1:
    return api.InputSelectionPolicyVersionV1(
        context_id=context_id,
        version=1,
        join_keys=OPTION_KEYS,
        maximum_staleness=timedelta(minutes=1),
        maximum_skew=timedelta(seconds=10),
        temporal_basis_permissions=("true_instant",),
        basket_membership=(),
    )


def _projected(
    raw_id: str,
    *,
    native_value: object,
    native_units: str,
    occurrence_id: str,
    identity: raw_api.RawSelectionIdentityV1,
) -> raw_api.ProjectedRawValueV1:
    return raw_api.ProjectedRawValueV1(
        raw_signal_catalogue_id=raw_api.RawSignalCatalogueId(raw_id),
        observation_occurrence_id=raw_api.observation_occurrence_id(occurrence_id),
        projection_mapping_id=f"m-{raw_id}",
        projection_mapping_version=1,
        source_provider="p",
        source_variant="snapshot",
        native_field_path=("field", raw_id),
        native_value=native_value,  # type: ignore[arg-type]
        native_units=native_units,
        subject_instrument="NVDA",
        source_temporal_kind="true_instant",
        source_timestamp_raw=NOW.isoformat(),
        source_timezone_native="UTC",
        received_ts_utc=NOW,
        ingestion_sequence=int(raw_id[1:]),
        ingestion_sequence_scope=raw_api.ingestion_sequence_scope("p:snapshot"),
        revision_vintage_native=None,
        selection_identity=identity,
    )


def _d131_owner_and_request(
    *, quote_contract: str, depth_contract: str
) -> tuple[object, api.CalculationRequestV1, raw_api.RawSelectionIdentityV1]:
    quote_identity = _identity(quote_contract)
    depth_identity = _identity(depth_contract)
    projected = {
        "R034": _projected(
            "R034",
            native_value=Decimal("100"),
            native_units="price",
            occurrence_id="q-bid",
            identity=quote_identity,
        ),
        "R035": _projected(
            "R035",
            native_value=Decimal("101"),
            native_units="price",
            occurrence_id="q-ask",
            identity=quote_identity,
        ),
        "R185": _projected(
            "R185",
            native_value=1,
            native_units="position",
            occurrence_id="depth1",
            identity=depth_identity,
        ),
        "R187": _projected(
            "R187",
            native_value="insert",
            native_units="operation",
            occurrence_id="depth1",
            identity=depth_identity,
        ),
        "R188": _projected(
            "R188",
            native_value="bid",
            native_units="side",
            occurrence_id="depth1",
            identity=depth_identity,
        ),
        "R189": _projected(
            "R189",
            native_value=Decimal("100.5"),
            native_units="price",
            occurrence_id="depth1",
            identity=depth_identity,
        ),
        "R190": _projected(
            "R190",
            native_value=Decimal("10"),
            native_units="size",
            occurrence_id="depth1",
            identity=depth_identity,
        ),
    }

    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id: Any, **kwargs: Any) -> Any:
            item = projected.get(raw_signal_catalogue_id.value)
            return raw_api.ProjectedRawHistoryPageV1(
                items=() if item is None else (item,), next_cursor=None
            )

        def project_raw_value(self, *args: object, **kwargs: object) -> object | None:
            return None

    p_basic = _parameter("P_BASIC", "p-basic", depth_price_distance=Decimal("1"))
    selection = _selection("selection-d131")
    units = {
        "price": api.UnitConventionVersionV1(
            context_id="u-price",
            version=1,
            native_units="price",
            canonical_units="price",
            scale=Decimal("1"),
            offset=Decimal("0"),
        ),
        "position": api.UnitConventionVersionV1(
            context_id="u-position",
            version=1,
            native_units="position",
            canonical_units="position",
            scale=Decimal("1"),
            offset=Decimal("0"),
        ),
        "operation": api.UnitConventionVersionV1(
            context_id="u-operation",
            version=1,
            native_units="operation",
            canonical_units="operation",
            scale=Decimal("1"),
            offset=Decimal("0"),
        ),
        "side": api.UnitConventionVersionV1(
            context_id="u-side",
            version=1,
            native_units="side",
            canonical_units="side",
            scale=Decimal("1"),
            offset=Decimal("0"),
        ),
        "size": api.UnitConventionVersionV1(
            context_id="u-size",
            version=1,
            native_units="size",
            canonical_units="size",
            scale=Decimal("1"),
            offset=Decimal("0"),
        ),
    }
    raw_units = {
        "R034": "price",
        "R035": "price",
        "R185": "position",
        "R187": "operation",
        "R188": "side",
        "R189": "price",
        "R190": "size",
    }
    mappings = tuple(
        raw_api.RawSignalProjectionMappingV1(
            mapping_id=f"m-{raw_id}",
            version=1,
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId(raw_id),
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("field", raw_id),
            native_units=native_units,
        )
        for raw_id, native_units in raw_units.items()
    )
    bindings = tuple(
        api.RawInputBindingV1(
            raw_id,
            api.VersionRefV1(f"m-{raw_id}", 1),
            api.VersionRefV1(units[native_units].context_id, 1),
            "NVDA",
            selection_identity=quote_identity if raw_id in {"R034", "R035"} else depth_identity,
        )
        for raw_id, native_units in raw_units.items()
    )
    owner = api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=mappings,
        parameter_sets=(p_basic,),
        input_selection_policies=(selection,),
        unit_conventions=tuple(units.values()),
        contexts=(),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        derived_signal_id="D131",
        subject_instrument="NVDA",
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        calculation_definition_version="calc-v1",
        parameter_set_id=p_basic.context_id,
        parameter_set_version=1,
        input_selection_policy_id=selection.context_id,
        input_selection_policy_version=1,
        context_refs=(),
        parameter_profile_refs=(api.ParameterProfileRefV1("P_BASIC", p_basic.context_id, 1),),
        raw_input_bindings=bindings,
    )
    return owner, request, quote_identity


def test_leaf1_refuses_d131_raw_to_predecessor_contract_mismatch_and_retains_identity() -> None:
    mismatched_owner, mismatched_request, _ = _d131_owner_and_request(
        quote_contract="C1", depth_contract="C2"
    )
    assert getattr(mismatched_owner, "materialise")(mismatched_request) is None

    matched_owner, matched_request, expected_identity = _d131_owner_and_request(
        quote_contract="C1", depth_contract="C1"
    )
    occurrence = getattr(matched_owner, "materialise")(matched_request)
    assert occurrence is not None
    assert occurrence.result == Decimal("10")
    assert getattr(occurrence, "selection_identity", None) == expected_identity
    predecessor = getattr(matched_owner, "reads").get_derived_occurrence(
        occurrence.predecessor_occurrence_ids[0]
    )
    assert predecessor is not None
    assert getattr(predecessor, "selection_identity", None) == expected_identity


class _SeededPersistence:
    def __init__(self, values: tuple[api.DerivedSignalOccurrenceV1, ...]) -> None:
        self._values = {value.derived_occurrence_id: value for value in values}

    def append_occurrence(
        self, value: api.DerivedSignalOccurrenceV1
    ) -> api.DerivedSignalOccurrenceV1:
        existing = self._values.get(value.derived_occurrence_id)
        if existing is not None and existing != value:
            raise ValueError("conflicting occurrence")
        self._values[value.derived_occurrence_id] = value
        return value

    def get_occurrence(self, derived_occurrence_id: str) -> api.DerivedSignalOccurrenceV1 | None:
        return self._values.get(derived_occurrence_id)

    def list_occurrences(
        self, *, derived_signal_id: str, subject_instrument: str, limit: int
    ) -> tuple[api.DerivedSignalOccurrenceV1, ...]:
        return tuple(
            value
            for value in self._values.values()
            if value.derived_signal_id == derived_signal_id
            and value.subject_instrument == subject_instrument
        )[:limit]


class _NoRawReader:
    def list_projected_raw_history(self, *args: object, **kwargs: object) -> object:
        return raw_api.ProjectedRawHistoryPageV1(items=(), next_cursor=None)

    def project_raw_value(self, *args: object, **kwargs: object) -> object | None:
        return None


def _seeded_stage2_occurrence(
    derived_id: str,
    occurrence_id: str,
    result: api.DerivedResultV1,
    *,
    parameter_ref: api.VersionRefV1,
    selection_ref: api.VersionRefV1,
    selection_identity: raw_api.RawSelectionIdentityV1 | None,
) -> api.DerivedSignalOccurrenceV1:
    if "selection_identity" not in {field.name for field in fields(api.DerivedSignalOccurrenceV1)}:
        pytest.fail(
            "Leaf 1 requires durable selected identity on DerivedSignalOccurrenceV1 before "
            "predecessor reuse can be independently validated"
        )
    return api.DerivedSignalOccurrenceV1(
        derived_signal_id=derived_id,
        derived_occurrence_id=occurrence_id,
        calculation_definition_version="calc-v1",
        parameter_context_refs=(parameter_ref, selection_ref),
        subject_instrument="NVDA",
        universe=None,
        effective_as_of_utc=NOW,
        window=None,
        knowledge_cutoff_utc=NOW,
        calculated_at_utc=NOW,
        result=result,
        units="utility/currency" if derived_id == "D188" else "utility score",
        result_shape="scalar" if derived_id == "D188" else "structured",
        raw_input_lineage=(),
        predecessor_occurrence_ids=(),
        convention_refs=(),
        supersedes_derived_occurrence_id=None,
        selection_identity=selection_identity,  # type: ignore[call-arg]
    )


def _d190_owner_and_request(
    *, left_contract: str, right_contract: str | None
) -> tuple[object, api.CalculationRequestV1, raw_api.RawSelectionIdentityV1]:
    p_basic = _parameter("P_BASIC", "p-basic-d190")
    p_utility = _parameter("P_UTILITY", "p-utility-d190", utility_mode="exact")
    selection = _selection("selection-d190")
    selection_ref = api.VersionRefV1(selection.context_id, 1)
    utility_ref = api.VersionRefV1(p_utility.context_id, 1)
    left_identity = _identity(left_contract)
    right_identity = None if right_contract is None else _identity(right_contract)
    seeded = (
        _seeded_stage2_occurrence(
            "D188",
            "d188-seeded",
            Decimal("5"),
            parameter_ref=utility_ref,
            selection_ref=selection_ref,
            selection_identity=left_identity,
        ),
        _seeded_stage2_occurrence(
            "D165",
            "d165-seeded",
            (("candidate", "A"), ("value", Decimal("8"))),
            parameter_ref=utility_ref,
            selection_ref=selection_ref,
            selection_identity=right_identity,
        ),
    )
    candidates = api.CandidateSetContextV1(
        context_id="candidate-set-d190",
        version=1,
        candidate_identities=("A",),
        eligibility_classes=(("A", "modify"),),
        neighbour_relations=(),
    )
    owner = api.create_owner(
        raw_projection_reader=_NoRawReader(),
        persistence=_SeededPersistence(seeded),
        parameter_sets=(p_basic, p_utility),
        input_selection_policies=(selection,),
        contexts=(candidates,),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        derived_signal_id="D190",
        subject_instrument="NVDA",
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        calculation_definition_version="calc-v1",
        parameter_set_id=p_basic.context_id,
        parameter_set_version=1,
        input_selection_policy_id=selection.context_id,
        input_selection_policy_version=1,
        context_refs=(api.VersionRefV1(candidates.context_id, 1),),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_BASIC", p_basic.context_id, 1),
            api.ParameterProfileRefV1("P_UTILITY", p_utility.context_id, 1),
        ),
        raw_input_bindings=(),
    )
    return owner, request, left_identity


def test_leaf1_refuses_predecessor_to_predecessor_selection_mismatch_or_absence() -> None:
    matched_owner, matched_request, expected_identity = _d190_owner_and_request(
        left_contract="C1", right_contract="C1"
    )
    matched = getattr(matched_owner, "materialise")(matched_request)
    assert matched is not None
    assert matched.result == Decimal("3")
    assert getattr(matched, "selection_identity", None) == expected_identity

    mismatched_owner, mismatched_request, _ = _d190_owner_and_request(
        left_contract="C1", right_contract="C2"
    )
    assert getattr(mismatched_owner, "materialise")(mismatched_request) is None

    absent_owner, absent_request, _ = _d190_owner_and_request(
        left_contract="C1", right_contract=None
    )
    assert getattr(absent_owner, "materialise")(absent_request) is None
