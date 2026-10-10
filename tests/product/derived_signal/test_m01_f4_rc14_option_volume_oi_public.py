"""F4 RC14: D116 option volume/OI through exact-contract M00 bindings."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
IDENTITY = raw.RawSelectionIdentityV1(
    (
        ("contract_id", "C-20261218-150"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal(150)),
        ("option_right", "call"),
    )
)
KEY_PATHS = tuple((key, ("identity", key)) for key, _ in IDENTITY.values)


def _public(
    *,
    missing: str | None = None,
    oi_zero: bool = False,
    future: str | None = None,
    wrong_contract: str | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    values = (("R041", Decimal(300)), ("R075", Decimal(0) if oi_zero else Decimal(200)))
    for i, (rid, value) in enumerate(values, 1):
        if rid == missing:
            continue
        identity = dict(IDENTITY.values)
        if rid == wrong_contract:
            identity["contract_id"] = "OTHER-CALL"
        instant = NOW - timedelta(seconds=4)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("option-oi-" + rid),
                delivery_artifact_ref=raw.delivery_artifact_ref("option-oi-" + rid),
                source_provider=raw.provider_id("controlled-option-oi"),
                native_record={"metric": {rid: value}, "identity": identity},
                received_ts_utc=NOW + timedelta(seconds=2) if rid == future else instant,
                ingestion_sequence=i,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc14:volume-oi"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=instant.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="option-volume-oi",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "volume-oi-map-" + rid, 1,
                raw.RawSignalCatalogueId(rid),
                "controlled-option-oi", "option-volume-oi",
                ("metric", rid), "canonical", KEY_PATHS,
            ) for rid in ("R041", "R075")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "volume-oi-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "volume-oi-select", 1, tuple(dict(IDENTITY.values)),
                timedelta(seconds=30), timedelta(seconds=30),
                ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "volume-oi-unit", 1, "canonical", "canonical",
                Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        "D116", "NVDA", NOW, NOW, "volume-oi-public",
        "volume-oi-basic", 1, "volume-oi-select", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("volume-oi-map-" + rid, 1),
                api.VersionRefV1("volume-oi-unit", 1), "NVDA", IDENTITY,
            ) for rid in ("R041", "R075")
        ),
    )
    return owner, req


def test_rc14_public_d116_exact_contract_volume_to_oi_3_over_2() -> None:
    owner, req = _public()
    out = owner.materialise(req)
    assert out is not None and out.result == Decimal("1.5")
    assert out.selection_identity == IDENTITY
    assert {r.raw_signal_id for r in out.raw_input_lineage} == {"R041", "R075"}
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        "option-oi-R041", "option-oi-R075"
    }
    assert owner.materialise(req) == out


def test_rc14_public_d116_missing_oi_refuses() -> None:
    owner, req = _public(missing="R075")
    assert owner.materialise(req) is None


def test_rc14_public_d116_zero_open_interest_refuses() -> None:
    owner, req = _public(oi_zero=True)
    assert owner.materialise(req) is None


def test_rc14_public_d116_mismatched_open_interest_contract_refuses() -> None:
    owner, req = _public(wrong_contract="R075")
    assert owner.materialise(req) is None


def test_rc14_public_d116_future_oi_receipt_refuses() -> None:
    owner, req = _public(future="R075")
    assert owner.materialise(req) is None
