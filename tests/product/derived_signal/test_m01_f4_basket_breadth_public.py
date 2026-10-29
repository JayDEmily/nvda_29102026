"""F4 RC13: public D151 basket breadth with component-specific coverage.

Controlled M00 records expose native prices using field-level mappings.  The
accepted K02 rule excludes missing component pairs from that component's
denominator; it must not coerce them to false or borrow other members.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 3, tzinfo=UTC)
MEMBERS = ("A", "B", "C")
PRICES: dict[str, dict[str, Decimal]] = {
    "A": {"R037": Decimal(11), "R043": Decimal(10), "R137": Decimal("10.5"), "R042": Decimal(10)},
    "B": {"R037": Decimal(9), "R043": Decimal(10), "R137": Decimal("9.5"), "R042": Decimal(8)},
    "C": {"R037": Decimal(12), "R043": Decimal(10), "R042": Decimal(13)},
}
RAW_IDS = ("R037", "R043", "R137", "R042")


def _public_breadth() -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for seq, member in enumerate(MEMBERS, 1):
        native = {"price": {rid: value for rid, value in PRICES[member].items()}}
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("f4-basket-" + member),
                delivery_artifact_ref=raw.delivery_artifact_ref("delivery-" + member),
                source_provider=raw.provider_id("controlled-basket"),
                native_record=native,
                received_ts_utc=NOW - timedelta(seconds=1),
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-basket:prices"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=(NOW - timedelta(seconds=1)).isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(
                    raw.RawSignalCatalogueId(rid) for rid in PRICES[member]
                ),
                source_variant="prices",
                subject_instrument=member,
                native_units="native_prices",
                revision_vintage_native="v1",
            )
        )
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "f4-map-" + rid,
            1,
            raw.RawSignalCatalogueId(rid),
            "controlled-basket",
            "prices",
            ("price", rid),
            "usd",
        )
        for rid in RAW_IDS
    )
    unit = api.UnitConventionVersionV1("f4-usd", 1, "usd", "usd", Decimal(1), Decimal(0))
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "f4-basket", 1, "P_BASIC", (("basket_membership", MEMBERS),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "f4-cross-section",
                1,
                ("subject_instrument",),
                timedelta(seconds=5),
                timedelta(seconds=5),
                ("true_instant",),
                MEMBERS,
            ),
        ),
        unit_conventions=(unit,),
        contexts=(),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D151",
        "NVDA",
        NOW,
        NOW,
        "f4-controlled-v1",
        "f4-basket",
        1,
        "f4-cross-section",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("f4-map-" + rid, 1),
                api.VersionRefV1("f4-usd", 1),
                member,
                None,
            )
            for rid in RAW_IDS
            for member in MEMBERS
        ),
    )
    return owner, request


def test_d151_public_component_breadth_exact_denominators_and_lineage() -> None:
    owner, request = _public_breadth()
    result = owner.materialise(request)
    assert result is not None
    fields = dict(result.result)
    assert fields["positive_return_fraction"] == Decimal(2) / Decimal(3)
    assert fields["above_vwap_fraction"] == Decimal(1) / Decimal(2)
    assert fields["above_prior_close_fraction"] == Decimal(2) / Decimal(3)
    assert {item.observation_occurrence_id for item in result.raw_input_lineage} == {
        "f4-basket-A",
        "f4-basket-B",
        "f4-basket-C",
    }
    assert owner.materialise(request) == result


def test_d151_public_refuses_different_versioned_basket() -> None:
    owner, request = _public_breadth()
    # Every configured member must be selected for price/last, while the
    # accepted D151 component denominators may exclude unavailable VWAP.
    missing_member = tuple(
        binding
        for binding in request.raw_input_bindings
        if not (binding.raw_signal_id == "R037" and binding.subject_instrument == "C")
    )
    assert owner.materialise(replace(request, raw_input_bindings=missing_member)) is None
    assert owner.materialise(replace(request, input_selection_policy_id="unknown")) is None
