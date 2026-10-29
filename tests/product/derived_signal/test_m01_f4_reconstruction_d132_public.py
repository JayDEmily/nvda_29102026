"""F4 reconstruction D132: exact M00 liquidity measurements plus D088/D131.

A public option score is lawful only when the four direct inputs and both
computed predecessors refer to the same explicit option-contract identity.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 8, tzinfo=UTC)
IDENTITY_KEYS = ("contract_id", "underlying_instrument", "expiry", "strike", "option_right")
IDENTITY = raw.RawSelectionIdentityV1(
    (
        ("contract_id", "C132"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal(150)),
        ("option_right", "call"),
    )
)
IDENTITY_PATHS = tuple((key, ("identity", key)) for key in IDENTITY_KEYS)
DIRECT = {
    "R033": ("spread", Decimal(2), "price"),
    "R036": ("top_size", Decimal(10), "quantity"),
    "R041": ("volume", Decimal(300), "contracts"),
    "R062": ("event_countdown", Decimal(120), "seconds"),
    "R034": ("bid", Decimal(99), "price"),
    "R035": ("ask", Decimal(101), "price"),
}
BOOK = {
    "R185": ("position", "position"),
    "R187": ("operation", "operation"),
    "R188": ("side", "side"),
    "R189": ("price", "price"),
    "R190": ("size", "quantity"),
}
ROWS = (
    ("bid-first", -7, "C132", 0, "insert", "bid", Decimal("99.5"), 10),
    ("ask-first", -6, "C132", 0, "insert", "ask", Decimal("100.5"), 8),
    ("bid-second", -5, "C132", 1, "insert", "bid", Decimal("98"), 5),
    ("bid-push", -4, "C132", 0, "insert", "bid", Decimal("99.9"), 7),
    ("decoy", -3, "OTHER", 0, "insert", "bid", Decimal("99.9"), 900),
)


def _identity(contract: str) -> dict[str, object]:
    return {**dict(IDENTITY.values), "contract_id": contract}


def _feature(did: str) -> api.ScoreFeatureV1:
    return api.ScoreFeatureV1(did, "component", (), "identity", None, 1, Decimal(1), None, None, ())


def _public(
    *, omit: str | None = None, future: str | None = None, wrong_contract: str | None = None
):
    m00 = raw.create_owner()
    quote = {name: value for rid, (name, value, _) in DIRECT.items() if rid != omit}
    m00.commands.admit_raw_observation_occurrence(
        raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id("recon-d132-snapshot"),
            delivery_artifact_ref=raw.delivery_artifact_ref("recon-d132-snapshot"),
            source_provider=raw.provider_id("controlled-d132-quote"),
            native_record={
                "metric": quote,
                "identity": _identity("OTHER" if wrong_contract else "C132"),
            },
            received_ts_utc=NOW + timedelta(seconds=1)
            if future == "snapshot"
            else NOW - timedelta(seconds=8),
            ingestion_sequence=1,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("recon:d132:quote"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=(NOW - timedelta(seconds=8)).isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in DIRECT),
            source_variant="option-snapshot",
            subject_instrument="NVDA",
            native_units="mixed",
            revision_vintage_native="v1",
        )
    )
    for i, (tag, offset, contract, position, operation, side, price, size) in enumerate(ROWS, 1):
        at = NOW + timedelta(seconds=offset)
        event = {
            "position": position,
            "operation": operation,
            "side": side,
            "price": price,
            "size": Decimal(size),
        }
        if omit == "R187" and tag == "bid-push":
            del event["operation"]
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("recon-d132-" + tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("recon-d132-" + tag),
                source_provider=raw.provider_id("controlled-d132-book"),
                native_record={"book": event, "identity": _identity(contract)},
                received_ts_utc=NOW + timedelta(seconds=1) if future == tag else at,
                ingestion_sequence=i,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("recon:d132:book"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=at.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in BOOK),
                source_variant="option-depth",
                subject_instrument="NVDA",
                native_units="book",
                revision_vintage_native="v1",
            )
        )
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            f"recon-d132-map-{rid}",
            1,
            raw.RawSignalCatalogueId(rid),
            "controlled-d132-quote",
            "option-snapshot",
            ("metric", name),
            unit,
            IDENTITY_PATHS,
        )
        for rid, (name, _, unit) in DIRECT.items()
    ) + tuple(
        raw.RawSignalProjectionMappingV1(
            f"recon-d132-map-{rid}",
            1,
            raw.RawSignalCatalogueId(rid),
            "controlled-d132-book",
            "option-depth",
            ("book", name),
            unit,
            IDENTITY_PATHS,
        )
        for rid, (name, unit) in BOOK.items()
    )
    units = {rid: unit for rid, (_, _, unit) in DIRECT.items()}
    units.update({rid: unit for rid, (_, unit) in BOOK.items()})
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "recon-d132-score",
                1,
                "P_SCORE",
                (("intercept", Decimal(0)),),
                tuple(
                    _feature(rid)
                    for rid in (*DIRECT.keys(), "D088", "D131")
                    if rid not in ("R034", "R035")
                ),
            ),
            api.CalculationParameterSetV1(
                "recon-d132-basic",
                1,
                "P_BASIC",
                (("depth_price_distance", Decimal("0.75")), ("subject_instrument", "NVDA")),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "recon-d132-select",
                1,
                IDENTITY_KEYS,
                timedelta(seconds=20),
                timedelta(seconds=20),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=tuple(
            api.UnitConventionVersionV1(
                f"recon-d132-unit-{rid}",
                1,
                unit,
                unit,
                Decimal(1),
                Decimal(0),
            )
            for rid, unit in units.items()
        ),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=1),
    )
    req = api.CalculationRequestV1(
        "D132",
        "NVDA",
        NOW,
        NOW,
        "recon-d132-definition",
        "recon-d132-score",
        1,
        "recon-d132-select",
        1,
        (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "recon-d132-score", 1),
            api.ParameterProfileRefV1("P_BASIC", "recon-d132-basic", 1),
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1(f"recon-d132-map-{rid}", 1),
                api.VersionRefV1(f"recon-d132-unit-{rid}", 1),
                "NVDA",
                IDENTITY,
            )
            for rid in (*DIRECT, *BOOK)
        ),
    )
    return owner, req


def test_reconstructed_d132_exact_contract_composite_public_and_lineage():
    owner, req = _public()
    out = owner.materialise(req)
    assert out is not None
    assert out.result == Decimal(459)  # 2 + 10 + 300 + 120 + D088=2 + D131=25
    assert {
        owner.reads.get_derived_occurrence(pid).derived_signal_id
        for pid in out.predecessor_occurrence_ids
    } == {"D088", "D131"}
    assert {r.raw_signal_id for r in out.raw_input_lineage} == set(DIRECT) | set(BOOK)
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        "recon-d132-snapshot",
        *("recon-d132-" + row[0] for row in ROWS if row[0] != "decoy"),
    }
    assert out.selection_identity == IDENTITY
    assert owner.materialise(req) == out


def test_reconstructed_d132_missing_mandatory_liquidity_refuses():
    owner, req = _public(omit="R062")
    assert owner.materialise(req) is None


def test_reconstructed_d132_missing_order_book_operation_refuses():
    owner, req = _public(omit="R187")
    assert owner.materialise(req) is None


def test_reconstructed_d132_future_required_source_refuses():
    owner, req = _public(future="snapshot")
    assert owner.materialise(req) is None


def test_reconstructed_d132_wrong_contract_refuses():
    owner, req = _public(wrong_contract="snapshot")
    assert owner.materialise(req) is None


def test_reconstructed_d132_incompatible_mapping_version_refuses():
    owner, req = _public()
    altered = tuple(
        replace(b, projection_mapping_ref=api.VersionRefV1("recon-d132-map-R041", 2))
        if b.raw_signal_id == "R041"
        else b
        for b in req.raw_input_bindings
    )
    assert owner.materialise(replace(req, raw_input_bindings=altered)) is None


def test_reconstructed_d132_missing_quote_required_for_spread_refuses():
    owner, req = _public(omit="R035")
    assert owner.materialise(req) is None


def test_reconstructed_d132_ineligible_future_book_event_is_excluded_from_depth():
    owner, req = _public(future="bid-push")
    out = owner.materialise(req)
    # An ineligible book update is not a mandatory event. The lawful earlier
    # book still produces depth 18; accepting its future update would yield 25.
    assert out is not None and out.result == Decimal(452)
    assert "recon-d132-bid-push" not in {
        source.observation_occurrence_id for source in out.raw_input_lineage
    }


def test_reconstructed_d132_selected_identity_mismatch_refuses():
    owner, req = _public()
    wrong = raw.RawSelectionIdentityV1(
        (
            ("contract_id", "C132"),
            ("underlying_instrument", "NVDA"),
            ("expiry", "2026-12-18"),
            ("strike", Decimal(151)),
            ("option_right", "call"),
        )
    )
    altered = tuple(
        replace(binding, selection_identity=wrong) if binding.raw_signal_id == "R041" else binding
        for binding in req.raw_input_bindings
    )
    assert owner.materialise(replace(req, raw_input_bindings=altered)) is None
