"""F4 RC14: K02 skew must consume native R112 deltas, not infer them from IV labels."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 9, tzinfo=UTC)
EXPIRY = "2026-12-18"
# contract, right, strike, R112 delta, R111 IV
POINTS = (
    ("C25", "call", Decimal(155), Decimal("0.25"), Decimal("0.30")),
    ("P25", "put", Decimal(145), Decimal("-0.25"), Decimal("0.40")),
    ("C10", "call", Decimal(165), Decimal("0.10"), Decimal("0.20")),
    ("P10", "put", Decimal(135), Decimal("-0.10"), Decimal("0.50")),
    ("C50", "call", Decimal(150), Decimal("0.50"), Decimal("0.33")),
    ("P50", "put", Decimal(150), Decimal("-0.50"), Decimal("0.33")),
)
KEYS = ("contract_id", "underlying_instrument", "expiry", "strike", "option_right")
KEY_PATHS = tuple((key, ("identity", key)) for key in KEYS)


def _public(did: str, *, missing_contract_field: tuple[str, str] | None = None,
            wrong_delta: str | None = None, future_contract: str | None = None):
    m00 = raw.create_owner()
    bindings = []
    seq = 0
    for contract, right, strike, delta, iv in POINTS:
        identity = raw.RawSelectionIdentityV1((
            ("contract_id", contract), ("underlying_instrument", "NVDA"),
            ("expiry", EXPIRY), ("strike", strike), ("option_right", right),
        ))
        for rid, value in (("R111", iv), ("R112", delta), ("R015", strike)):
            if rid == "R015" and did == "D101":
                continue
            if missing_contract_field == (contract, rid):
                continue
            seq += 1
            at = NOW - timedelta(seconds=10)
            # R111 has no copied or fabricated `delta` identity: authoritative
            # numeric delta comes independently from source-native R112.
            m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(
                    f"skew-{contract}-{rid}"
                ),
                delivery_artifact_ref=raw.delivery_artifact_ref(f"skew-{contract}-{rid}"),
                source_provider=raw.provider_id("controlled-native-skew"),
                native_record={
                    "metric": {
                        rid: Decimal("0.30")
                        if wrong_delta == contract and rid == "R112"
                        else value
                    },
                    "identity": dict(identity.values),
                },
                received_ts_utc=NOW + timedelta(seconds=1)
                if future_contract == contract and rid == "R112" else at,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc14:native-skew"),
                source_temporal_kind="true_instant", source_timestamp_raw=at.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="native-option-point", subject_instrument="NVDA",
                native_units="canonical", revision_vintage_native="v1",
            ))
            bindings.append(api.RawInputBindingV1(
                rid, api.VersionRefV1("skew-map-" + rid, 1),
                api.VersionRefV1("skew-unit", 1), "NVDA", identity,
            ))
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(raw.RawSignalProjectionMappingV1(
            "skew-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
            "controlled-native-skew", "native-option-point", ("metric", rid),
            "canonical", KEY_PATHS,
        ) for rid in ("R111", "R112", "R015")),
        parameter_sets=(api.CalculationParameterSetV1(
            "skew-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "skew-exact-expiry", 1, ("underlying_instrument", "expiry"),
            timedelta(minutes=3), timedelta(minutes=3), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "skew-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
        ),),
        contexts=(), utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        did, "NVDA", NOW, NOW, "skew-public", "skew-basic", 1,
        "skew-exact-expiry", 1, (), raw_input_bindings=tuple(bindings),
    )
    return owner, request


@pytest.mark.parametrize("did,expected", (
    ("D099", Decimal(10)), ("D100", Decimal(30)), ("D101", Decimal(4)),
))
def test_skew_uses_native_delta_strike_exact_expiry_and_lineage(
    did: str, expected: Decimal
) -> None:
    owner, request = _public(did)
    out = owner.materialise(request)
    assert out is not None and out.result == expected
    assert {item.raw_signal_id for item in out.raw_input_lineage} == (
        {"R111", "R112"} if did == "D101" else {"R111", "R112", "R015"}
    )
    assert owner.materialise(request) == out


@pytest.mark.parametrize("did", ("D099", "D100", "D101"))
def test_skew_refuses_missing_native_delta_for_selected_contract(did: str) -> None:
    owner, request = _public(did, missing_contract_field=("P25", "R112"))
    assert owner.materialise(request) is None


def test_skew_refuses_missing_strike_for_selected_contract() -> None:
    owner, request = _public("D099", missing_contract_field=("P25", "R015"))
    assert owner.materialise(request) is None


def test_skew_refuses_future_required_native_delta() -> None:
    owner, request = _public("D099", future_contract="P25")
    assert owner.materialise(request) is None


def test_skew_refuses_delta_that_does_not_match_target_bucket() -> None:
    owner, request = _public("D099", wrong_delta="P25")
    assert owner.materialise(request) is None
