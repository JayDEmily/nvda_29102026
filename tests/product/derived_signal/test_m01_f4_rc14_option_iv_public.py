"""F4 RC14: exact option-contract M00 public bid/ask IV calculations."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 3, tzinfo=UTC)
IDENTITY = raw.RawSelectionIdentityV1(
    (
        ("contract_id", "OPT-C1"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal(150)),
        ("option_right", "call"),
    )
)
FIELDS = ("R084", "R093")


def _public(
    *,
    missing: str | None = None,
    future: bool = False,
    other_contract: bool = True,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for i, contract in enumerate(("OPT-C1", "OPT-C2") if other_contract else ("OPT-C1",)):
        stamp = NOW + timedelta(seconds=2) if future and i == 0 else NOW - timedelta(seconds=3)
        identity = dict(IDENTITY.values)
        identity["contract_id"] = contract
        data = (
            {"R084": Decimal("0.48"), "R093": Decimal("0.52")}
            if i == 0 else {"R084": Decimal("0.11"), "R093": Decimal("0.88")}
        )
        if missing is not None and i == 0:
            data.pop(missing)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("iv-" + contract),
                delivery_artifact_ref=raw.delivery_artifact_ref("iv-" + contract),
                source_provider=raw.provider_id("controlled-rc14-iv"),
                native_record={"iv": data, "identity": identity},
                received_ts_utc=stamp,
                ingestion_sequence=i + 1,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc14:iv"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in FIELDS),
                source_variant="iv-quote",
                subject_instrument="NVDA",
                native_units="decimal_volatility",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc14-iv-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc14-iv", "iv-quote", ("iv", rid),
                "decimal_volatility",
                tuple((key, ("identity", key)) for key, _ in IDENTITY.values),
            ) for rid in FIELDS
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc14-iv-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc14-iv-select", 1, tuple(dict(IDENTITY.values)),
                timedelta(seconds=20), timedelta(seconds=20), ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc14-iv-unit", 1, "decimal_volatility", "decimal_volatility",
                Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D092", "NVDA", NOW, NOW, "rc14-iv-public",
        "rc14-iv-basic", 1, "rc14-iv-select", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("rc14-iv-map-" + rid, 1),
                api.VersionRefV1("rc14-iv-unit", 1), "NVDA", IDENTITY,
            ) for rid in FIELDS
        ),
    )
    return owner, request


@pytest.mark.parametrize(
    ("did", "expected"),
    (("D092", Decimal("0.50")), ("D093", Decimal(4))),
)
def test_rc14_public_mid_iv_and_vol_point_spread_exact_contract(
    did: str, expected: Decimal,
) -> None:
    owner, req = _public()
    req = replace(req, derived_signal_id=did)
    out = owner.materialise(req)
    assert out is not None and out.result == expected
    assert out.selection_identity == IDENTITY
    assert {r.raw_signal_id for r in out.raw_input_lineage} == set(FIELDS)
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {"iv-OPT-C1"}
    assert out.predecessor_occurrence_ids == ()
    assert owner.materialise(req) == out


@pytest.mark.parametrize(("did", "missing"), (("D092", "R084"), ("D093", "R093")))
def test_rc14_public_option_iv_missing_required_source_refuses(
    did: str, missing: str,
) -> None:
    owner, req = _public(missing=missing)
    assert owner.materialise(replace(req, derived_signal_id=did)) is None


@pytest.mark.parametrize("did", ("D092", "D093"))
def test_rc14_public_option_iv_future_receipt_refuses(did: str) -> None:
    owner, req = _public(future=True)
    assert owner.materialise(replace(req, derived_signal_id=did)) is None
