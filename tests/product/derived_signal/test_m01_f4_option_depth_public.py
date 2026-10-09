"""F4 RC12: D131 native M00 option-depth reconstruction against exact D087 midpoint."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 19, tzinfo=UTC)
QUOTE = ("R034", "R035")
BOOK = ("R185", "R187", "R188", "R189", "R190")
FIELDS = (*QUOTE, *BOOK)
NAMES = ("bid", "ask", "position", "operation", "side", "price", "size")
UNITS = ("price", "price", "position", "operation", "side", "price", "quantity")
IDENTITY_PATHS = (
    ("contract_id", ("identity", "contract_id")),
    ("underlying_instrument", ("identity", "underlying_instrument")),
    ("expiry", ("identity", "expiry")),
    ("strike", ("identity", "strike")),
    ("option_right", ("identity", "option_right")),
)
IDENTITY = raw.RawSelectionIdentityV1(
    (
        ("contract_id", "C1"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal(150)),
        ("option_right", "call"),
    )
)
ROWS = (
    ("bid-first", -7, "C1", 0, "insert", "bid", Decimal("99.5"), 10),
    ("ask-first", -6, "C1", 0, "insert", "ask", Decimal("100.5"), 8),
    ("bid-second", -5, "C1", 1, "insert", "bid", Decimal("98"), 5),
    ("bid-push", -4, "C1", 0, "insert", "bid", Decimal("99.9"), 7),
    ("decoy", -3, "C2", 0, "insert", "bid", Decimal("99.9"), 900),
)


def _identity_record(contract: str) -> dict[str, object]:
    return {
        "contract_id": contract,
        "underlying_instrument": "NVDA",
        "expiry": "2026-12-18",
        "strike": Decimal(150),
        "option_right": "call",
    }


def _public_depth(
    *, missing_operation: bool = False, omit_quote: bool = False
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    quote_at = NOW - timedelta(seconds=8)
    if not omit_quote:
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("option-q"),
                delivery_artifact_ref=raw.delivery_artifact_ref("option-q"),
                source_provider=raw.provider_id("option-quotes"),
                native_record={
                    "bid": Decimal(99),
                    "ask": Decimal(101),
                    "identity": _identity_record("C1"),
                },
                received_ts_utc=quote_at,
                ingestion_sequence=1,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("option-quotes:q"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=quote_at.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in QUOTE),
                source_variant="option_quote",
                subject_instrument="NVDA",
                native_units="option_quote",
                revision_vintage_native="v1",
            )
        )
    for seq, (tag, offset, contract, position, operation, side, price, size) in enumerate(ROWS, 1):
        moment = NOW + timedelta(seconds=offset)
        native: dict[str, object] = {
            "position": position,
            "operation": operation,
            "side": side,
            "price": price,
            "size": Decimal(size),
        }
        if tag == "bid-push" and missing_operation:
            del native["operation"]
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("option-" + tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("option-" + tag),
                source_provider=raw.provider_id("option-book"),
                native_record={"book": native, "identity": _identity_record(contract)},
                received_ts_utc=moment,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("option-book:book"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=moment.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in BOOK),
                source_variant="option_depth",
                subject_instrument="NVDA",
                native_units="option_book",
                revision_vintage_native="v1",
            )
        )
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "option-map-" + rid,
            1,
            raw.RawSignalCatalogueId(rid),
            "option-quotes" if i < 2 else "option-book",
            "option_quote" if i < 2 else "option_depth",
            (name,) if i < 2 else ("book", name),
            UNITS[i],
            IDENTITY_PATHS,
        )
        for i, (rid, name) in enumerate(zip(FIELDS, NAMES, strict=True))
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "option-basic",
                1,
                "P_BASIC",
                (("depth_price_distance", Decimal("0.75")), ("subject_instrument", "NVDA")),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "option-selection",
                1,
                ("contract_id", "underlying_instrument", "expiry", "strike", "option_right"),
                timedelta(seconds=20),
                timedelta(seconds=20),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=tuple(
            api.UnitConventionVersionV1("option-unit-" + rid, 1, unit, unit, Decimal(1), Decimal(0))
            for rid, unit in zip(FIELDS, UNITS, strict=True)
        ),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=1),
    )
    request = api.CalculationRequestV1(
        "D131",
        "NVDA",
        NOW,
        NOW,
        "option-depth-v1",
        "option-basic",
        1,
        "option-selection",
        1,
        (),
        parameter_profile_refs=(api.ParameterProfileRefV1("P_BASIC", "option-basic", 1),),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("option-map-" + rid, 1),
                api.VersionRefV1("option-unit-" + rid, 1),
                "NVDA",
                IDENTITY,
            )
            for rid in FIELDS
        ),
    )
    return owner, request


def test_d131_public_option_selection_midpoint_and_insert_shifted_depth() -> None:
    owner, request = _public_depth()
    result = owner.materialise(request)
    assert result is not None
    assert result.result == Decimal(25)
    assert result.selection_identity == IDENTITY
    assert {r.raw_signal_id for r in result.raw_input_lineage} == set(FIELDS)
    assert {r.observation_occurrence_id for r in result.raw_input_lineage} == {
        "option-q",
        "option-bid-first",
        "option-ask-first",
        "option-bid-second",
        "option-bid-push",
    }
    assert "option-decoy" not in {r.observation_occurrence_id for r in result.raw_input_lineage}
    assert result.predecessor_occurrence_ids
    pred = owner.reads.get_derived_occurrence(result.predecessor_occurrence_ids[0])
    assert pred is not None and pred.derived_signal_id == "D087"
    assert pred.selection_identity == IDENTITY
    assert owner.materialise(request) == result
    # Within the intermediate historical cutoff, the pushed row is not yet eligible.
    older = owner.materialise(
        replace(
            request,
            as_of_utc=NOW - timedelta(seconds=5),
            knowledge_cutoff_utc=NOW - timedelta(seconds=5),
        )
    )
    assert older is not None and older.result == Decimal(18)


def test_d131_public_refuses_missing_event_operation_and_required_midpoint() -> None:
    broken, request = _public_depth(missing_operation=True)
    assert broken.materialise(request) is None
    unpriced, req = _public_depth(omit_quote=True)
    assert unpriced.materialise(req) is None
