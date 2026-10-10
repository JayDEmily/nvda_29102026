"""F4 RC14 public M00 test for exact-contract historical option volume z-score."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 6, tzinfo=UTC)
IDENTITY = raw.RawSelectionIdentityV1((
    ("contract_id", "NVDA-20261218-C150"),
    ("underlying_instrument", "NVDA"),
    ("expiry", "2026-12-18"),
    ("strike", Decimal(150)),
    ("option_right", "call"),
))
KEY_PATHS = tuple((key, ("identity", key)) for key, _ in IDENTITY.values)


def _public(*, missing: str | None = None, future: str | None = None,
            wrong_history: bool = False,
            zero_variance: bool = False):
    m00 = raw.create_owner()
    events = (
        ("prior-a", "R041", Decimal(8), 3),
        ("prior-b", "R041", Decimal(8) if zero_variance else Decimal(12), 2),
        ("wrong-contract", "R041", Decimal(200), 1),
        ("current", "R041", Decimal(16), 0),
        ("oi", "R075", Decimal(90), 0),
    )
    for seq, (oid, rid, value, days) in enumerate(events, 1):
        if oid == missing:
            continue
        identity = dict(IDENTITY.values)
        if oid == "wrong-contract" or (wrong_history and oid == "prior-a"):
            identity["contract_id"] = "DIFFERENT-CONTRACT"
        at = NOW - timedelta(days=days, seconds=5)
        m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id("opt-z-" + oid),
            delivery_artifact_ref=raw.delivery_artifact_ref("opt-z-" + oid),
            source_provider=raw.provider_id("controlled-option-z"),
            native_record={"metric": {rid: value}, "identity": identity},
            received_ts_utc=NOW + timedelta(seconds=1) if oid == future else at,
            ingestion_sequence=seq,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("rc14:option-z"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=at.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
            source_variant="option-volume-z",
            subject_instrument="NVDA", native_units="canonical", revision_vintage_native="v1",
        ))
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "option-z-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-option-z", "option-volume-z", ("metric", rid),
                "canonical", KEY_PATHS,
            ) for rid in ("R041", "R075")
        ),
        parameter_sets=(api.CalculationParameterSetV1(
            "option-z-baseline", 1, "P_BASELINE",
            (("history_count", 2), ("minimum_sample", 2)),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "option-z-selection", 1, tuple(dict(IDENTITY.values)),
            timedelta(days=4), timedelta(days=4), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "option-z-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
        ),),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        "D117", "NVDA", NOW, NOW, "option-z-public",
        "option-z-baseline", 1, "option-z-selection", 1, (),
        raw_input_bindings=tuple(api.RawInputBindingV1(
            rid, api.VersionRefV1("option-z-map-" + rid, 1),
            api.VersionRefV1("option-z-unit", 1), "NVDA", IDENTITY,
        ) for rid in ("R041", "R075")),
    )
    return owner, req


def test_d117_exact_contract_z_score_retries_and_lineage() -> None:
    owner, request = _public()
    result = owner.materialise(request)
    assert result is not None
    assert result.result == Decimal(6) / Decimal(8).sqrt()
    assert result.selection_identity == IDENTITY
    assert {item.observation_occurrence_id for item in result.raw_input_lineage} == {
        "opt-z-prior-a", "opt-z-prior-b", "opt-z-current", "opt-z-oi",
    }
    assert owner.materialise(request) == result


def test_d117_missing_matching_history_refuses() -> None:
    owner, request = _public(wrong_history=True)
    assert owner.materialise(request) is None


def test_d117_incomplete_history_refuses() -> None:
    owner, request = _public(missing="prior-a")
    assert owner.materialise(request) is None


def test_d117_zero_sample_variance_refuses() -> None:
    owner, request = _public(zero_variance=True)
    assert owner.materialise(request) is None


def test_d117_future_current_receipt_refuses() -> None:
    owner, request = _public(future="current")
    assert owner.materialise(request) is None


def test_d117_missing_required_open_interest_refuses() -> None:
    owner, request = _public(missing="oi")
    assert owner.materialise(request) is None
