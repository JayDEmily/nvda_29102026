"""F4 RC12: D134/D135 native snapshot public reachability witness.

The accepted CSV declares only R185/R188/R190 for each row, while the
current code's book-event reconstruction requires undeclared R187. This
public witness must not be labelled green or a provider integration proof.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

AT = datetime(2026, 10, 9, 9, tzinfo=UTC)
REQUIRED = ("R185", "R188", "R190")


def _public_snapshot() -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for n, (side, size) in enumerate((("bid", Decimal(10)), ("ask", Decimal(7))), 1):
        moment = AT - timedelta(seconds=1)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("depth-" + side),
                delivery_artifact_ref=raw.delivery_artifact_ref("depth-source" + side),
                source_provider=raw.provider_id("controlled-snapshot"),
                native_record={"level": 1, "side": side, "size": size},
                received_ts_utc=moment,
                ingestion_sequence=n,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-snapshot:depth"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=moment.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in REQUIRED),
                source_variant="depth",
                subject_instrument="NVDA",
                native_units="book_snapshot",
                revision_vintage_native="v1",
            )
        )
    names = ("level", "side", "size")
    units = ("level", "side", "contracts")
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "depth-map-" + rid,
            1,
            raw.RawSignalCatalogueId(rid),
            "controlled-snapshot",
            "depth",
            (name,),
            unit,
        )
        for rid, name, unit in zip(REQUIRED, names, units, strict=True)
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1("depth-basic", 1, "P_BASIC", (("depth_levels", 1),)),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "depth-selection",
                1,
                ("subject_instrument",),
                timedelta(seconds=5),
                timedelta(seconds=5),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=tuple(
            api.UnitConventionVersionV1(
                "depth-unit-" + rid,
                1,
                unit,
                unit,
                Decimal(1),
                Decimal(0),
            )
            for rid, unit in zip(REQUIRED, units, strict=True)
        ),
        contexts=(),
        utc_now=lambda: AT + timedelta(seconds=1),
    )
    request = api.CalculationRequestV1(
        "D134",
        "NVDA",
        AT,
        AT,
        "f4-snapshot",
        "depth-basic",
        1,
        "depth-selection",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("depth-map-" + rid, 1),
                api.VersionRefV1("depth-unit-" + rid, 1),
                "NVDA",
                None,
            )
            for rid in REQUIRED
        ),
    )
    return owner, request


def test_d134_d135_and_d136_have_nonzero_lawful_public_depths_without_undeclared_operations() -> (
    None
):
    owner, request = _public_snapshot()
    bid = owner.materialise(request)
    ask = owner.materialise(replace(request, derived_signal_id="D135"))
    ratio = owner.materialise(replace(request, derived_signal_id="D136"))
    assert bid is not None and bid.result == Decimal(10)
    assert ask is not None and ask.result == Decimal(7)
    assert ratio is not None and ratio.result == Decimal(3) / Decimal(17)
    assert {x.observation_occurrence_id for x in bid.raw_input_lineage} == {
        "depth-bid",
        "depth-ask",
    }
