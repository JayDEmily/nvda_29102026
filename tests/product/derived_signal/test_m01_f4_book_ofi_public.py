"""F4 RC12: admitted M00 record projection to D145, no injected book states.

Proof data are controlled records; not a live book-provider integration assertion.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

AS_OF = datetime(2026, 10, 9, 3, 0, tzinfo=UTC)
FIELDS = ("R187", "R188", "R189", "R190")
UNITS = ("operation", "side", "price", "quantity")


def _public_book(
    *,
    late_quote: bool = False,
    missing_side: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    events: tuple[tuple[str, int, str, str, Decimal, Decimal], ...] = (
        ("init-bid", -3, "insert", "bid", Decimal(100), Decimal(10)),
        ("init-ask", -3, "insert", "ask", Decimal(101), Decimal(8)),
        ("adjust-bid", -2, "update", "bid", Decimal(100), Decimal(12)),
        ("adjust-ask", -1, "update", "ask", Decimal(101), Decimal(7)),
    )
    for seq, (tag, seconds, operation, side, price, quantity) in enumerate(events, 1):
        moment = AS_OF + timedelta(seconds=(10 if late_quote and tag == "adjust-ask" else seconds))
        native: dict[str, object] = {
            "book": {"operation": operation, "side": side, "price": price, "quantity": quantity}
        }
        obs = raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id(tag),
            delivery_artifact_ref=raw.delivery_artifact_ref("delivery-" + tag),
            source_provider=raw.provider_id("controlled-book"),
            native_record=native,
            received_ts_utc=moment,
            ingestion_sequence=seq,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-book:smart"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=moment.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=tuple(
                raw.RawSignalCatalogueId(rid)
                for rid in FIELDS
                if not (missing_side and tag == "adjust-ask" and rid == "R188")
            ),
            source_variant="smart",
            subject_instrument="NVDA",
            native_units="native_book",
            revision_vintage_native="revision-1",
        )
        m00.commands.admit_raw_observation_occurrence(obs)

    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            mapping_id="f4-map-" + rid,
            version=1,
            raw_signal_catalogue_id=raw.RawSignalCatalogueId(rid),
            source_provider="controlled-book",
            source_variant="smart",
            native_field_path=("book", field),
            native_units=units,
        )
        for rid, field, units in zip(
            FIELDS, ("operation", "side", "price", "quantity"), UNITS, strict=True
        )
    )
    units = tuple(
        api.UnitConventionVersionV1(
            context_id="f4-unit-" + value,
            version=1,
            native_units=value,
            canonical_units=value,
            scale=Decimal(1),
            offset=Decimal(0),
        )
        for value in UNITS
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1("f4-ofi", 1, "P_OFI", (("window_seconds", 5),)),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "f4-book-selection",
                1,
                ("subject_instrument",),
                timedelta(seconds=5),
                timedelta(seconds=5),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=units,
        contexts=(),
        utc_now=lambda: AS_OF + timedelta(seconds=20),
    )
    request = api.CalculationRequestV1(
        derived_signal_id="D145",
        subject_instrument="NVDA",
        as_of_utc=AS_OF,
        knowledge_cutoff_utc=AS_OF,
        calculation_definition_version="f4-controlled-v1",
        parameter_set_id="f4-ofi",
        parameter_set_version=1,
        input_selection_policy_id="f4-book-selection",
        input_selection_policy_version=1,
        context_refs=(),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("f4-map-" + rid, 1),
                api.VersionRefV1("f4-unit-" + unit, 1),
                "NVDA",
                None,
            )
            for rid, unit in zip(FIELDS, UNITS, strict=True)
        ),
    )
    return owner, request


def test_d145_public_reconstructed_ofi_and_complete_source_lineage() -> None:
    owner, request = _public_book()
    result = owner.materialise(request)
    assert result is not None
    assert result.result == Decimal(3)
    assert {item.observation_occurrence_id for item in result.raw_input_lineage} == {
        "init-bid",
        "init-ask",
        "adjust-bid",
        "adjust-ask",
    }
    assert {item.raw_signal_id for item in result.raw_input_lineage} == set(FIELDS)
    assert owner.materialise(request) == result


def test_d145_public_refuses_missing_required_native_field() -> None:
    owner, request = _public_book(missing_side=True)
    assert owner.materialise(request) is None


def test_d145_public_refuses_future_update_and_missing_cutoff_history() -> None:
    owner, request = _public_book(late_quote=True)
    # Late event/receipt must not be used as an earlier book mutation.
    result = owner.materialise(request)
    assert result is not None
    assert result.result == Decimal(2)
    assert "adjust-ask" not in {item.observation_occurrence_id for item in result.raw_input_lineage}
    assert (
        owner.materialise(replace(request, knowledge_cutoff_utc=AS_OF - timedelta(seconds=4)))
        is None
    )
