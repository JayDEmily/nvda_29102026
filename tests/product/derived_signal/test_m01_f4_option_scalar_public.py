"""F4 RC02: exact-option public scalar bid/ask, moneyness, and log-moneyness.

All native data is controlled M00 input with immutable option-contract keys.
No M01 kernel, predecessor, or output is injected as a test fixture.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 1, 0, tzinfo=UTC)
FIELDS = ("R014", "R034", "R035", "R118")
VALUES = {
    "R014": Decimal(150),
    "R034": Decimal(99),
    "R035": Decimal(101),
    "R118": Decimal(120),
}
NAMES = {"R014": "strike", "R034": "bid", "R035": "ask", "R118": "spot"}
IDENTITY = raw.RawSelectionIdentityV1(
    (
        ("contract_id", "OPT-C1"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal(150)),
        ("option_right", "call"),
    )
)
KEY_PATHS = tuple((key, ("identity", key)) for key, _ in IDENTITY.values)


def public_option(
    *, missing: str | None = None, future: bool = False,
    zero_spot: bool = False, add_other_contract: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for i, contract in enumerate(("OPT-C1", "OPT-C2") if add_other_contract else ("OPT-C1",)):
        instant = NOW + timedelta(seconds=2) if future and i == 0 else NOW - timedelta(seconds=5)
        identity = dict(IDENTITY.values)
        identity["contract_id"] = contract
        data = dict(VALUES)
        if zero_spot:
            data["R118"] = Decimal(0)
        if i:
            data["R034"] = Decimal(900)
            data["R035"] = Decimal(1100)
            data["R118"] = Decimal(200)
        if missing is not None and i == 0:
            del data[missing]
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("scalar-" + contract),
                delivery_artifact_ref=raw.delivery_artifact_ref("scalar-" + contract),
                source_provider=raw.provider_id("controlled-option-scalars"),
                native_record={**{NAMES[rid]: v for rid, v in data.items()}, "identity": identity},
                received_ts_utc=instant,
                ingestion_sequence=i + 1,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("scalar:option"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=instant.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in FIELDS),
                source_variant="option-snapshot",
                subject_instrument="NVDA",
                native_units="price",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "scalar-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-option-scalars", "option-snapshot", (NAMES[rid],),
                "price", KEY_PATHS,
            ) for rid in FIELDS
        ),
        parameter_sets=(api.CalculationParameterSetV1(
            "scalar-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "scalar-option-select", 1, tuple(dict(IDENTITY.values)), timedelta(seconds=20),
            timedelta(seconds=20), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "scalar-price-unit", 1, "price", "price", Decimal(1), Decimal(0),
        ),),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=1),
    )
    req = api.CalculationRequestV1(
        "D087", "NVDA", NOW, NOW, "option-scalar", "scalar-basic", 1,
        "scalar-option-select", 1, (), raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("scalar-map-" + rid, 1),
                api.VersionRefV1("scalar-price-unit", 1), "NVDA", IDENTITY,
            ) for rid in FIELDS
        ),
    )
    return owner, req


@pytest.mark.parametrize(("did", "expected"), [
    ("D087", Decimal(100)),
    ("D088", Decimal(2)),
    ("D089", Decimal("1.25")),
    ("D090", Decimal("1.25").ln()),
])
def test_rc02_exact_option_public_algebra_value_lineage_retry_and_other_contract_exclusion(
    did: str, expected: Decimal,
) -> None:
    owner, req = public_option(add_other_contract=True)
    result = owner.materialise(replace(req, derived_signal_id=did))
    assert result is not None and result.result == expected
    assert result.selection_identity == IDENTITY
    required = {"R034", "R035"} if did in {"D087", "D088"} else {"R014", "R118"}
    assert {x.raw_signal_id for x in result.raw_input_lineage} == required
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {"scalar-OPT-C1"}
    if did == "D088":
        assert len(result.predecessor_occurrence_ids) == 1
        previous = owner.reads.get_derived_occurrence(result.predecessor_occurrence_ids[0])
        assert previous is not None and previous.derived_signal_id == "D087"
        assert previous.result == Decimal(100)
    else:
        assert result.predecessor_occurrence_ids == ()
    assert owner.materialise(replace(req, derived_signal_id=did)) == result


@pytest.mark.parametrize(("did", "missing"), [
    ("D087", "R034"), ("D088", "R035"),
    ("D089", "R118"), ("D090", "R014"),
])
def test_rc02_exact_option_public_algebra_refuses_missing_field(
    did: str, missing: str,
) -> None:
    owner, req = public_option(missing=missing)
    assert owner.materialise(replace(req, derived_signal_id=did)) is None


@pytest.mark.parametrize("did", ("D087", "D088", "D089", "D090"))
def test_rc02_exact_option_public_algebra_refuses_future_information(did: str) -> None:
    owner, req = public_option(future=True)
    assert owner.materialise(replace(req, derived_signal_id=did)) is None


@pytest.mark.parametrize("did", ("D089", "D090"))
def test_rc02_exact_option_public_moneyness_refuses_zero_spot(did: str) -> None:
    owner, req = public_option(zero_spot=True)
    assert owner.materialise(replace(req, derived_signal_id=did)) is None
