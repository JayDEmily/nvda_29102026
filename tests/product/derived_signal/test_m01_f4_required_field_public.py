"""F4 RC18: expose the accepted D007 zero-edge public-reachability conflict.

This is an intentionally failing authority-derived witness until a permitted
runtime policy-to-M00 field-projection mechanism is established. Never treat it
as a passing proof or weaken the expected 2/3 result to 0.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

AT = datetime(2026, 10, 9, 9, 30, tzinfo=UTC)
RAW_IDS = ("R001", "R002", "R003")


def test_d007_public_required_field_completeness_counts_present_and_absent() -> None:
    m00 = raw.create_owner()
    m00.commands.admit_raw_observation_occurrence(
        raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id("f4-completeness"),
            delivery_artifact_ref=raw.delivery_artifact_ref("f4-completeness-source"),
            source_provider=raw.provider_id("controlled-completeness"),
            native_record={"fields": {"R001": Decimal(1), "R003": Decimal(1)}},
            received_ts_utc=AT,
            ingestion_sequence=1,
            ingestion_sequence_scope=raw.ingestion_sequence_scope(
                "controlled-completeness:snapshot"
            ),
            source_temporal_kind="true_instant",
            source_timestamp_raw=AT.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=(
                raw.RawSignalCatalogueId("R001"),
                raw.RawSignalCatalogueId("R003"),
            ),
            source_variant="snapshot",
            subject_instrument="NVDA",
            native_units="record",
            revision_vintage_native="v1",
        )
    )
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "f4-complete-map-" + rid,
            1,
            raw.RawSignalCatalogueId(rid),
            "controlled-completeness",
            "snapshot",
            ("fields", rid),
            "count",
        )
        for rid in RAW_IDS
    )
    policy = api.RequiredFieldPolicyV1("f4-required", 1, RAW_IDS)
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "f4-completeness-rule", 1, "P_RULE", (("rule", "required_field_completeness"),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "f4-completeness-selection",
                1,
                ("subject_instrument",),
                timedelta(seconds=10),
                timedelta(seconds=10),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1("f4-count", 1, "count", "count", Decimal(1), Decimal(0)),
        ),
        contexts=(policy,),
        utc_now=lambda: AT + timedelta(seconds=1),
    )
    request = api.CalculationRequestV1(
        "D007",
        "NVDA",
        AT,
        AT,
        "f4-completeness",
        "f4-completeness-rule",
        1,
        "f4-completeness-selection",
        1,
        (api.VersionRefV1("f4-required", 1),),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("f4-complete-map-" + rid, 1),
                api.VersionRefV1("f4-count", 1),
                "NVDA",
                None,
            )
            for rid in RAW_IDS
        ),
    )
    result = owner.materialise(request)
    assert result is not None
    assert result.result == Decimal(2) / Decimal(3)
    assert {
        (item.raw_signal_id, item.observation_occurrence_id) for item in result.raw_input_lineage
    } == {
        ("R001", "f4-completeness"),
        ("R003", "f4-completeness"),
    }
