"""F4 D110: exact pair straddle-to-spot percentage via admitted M00 projections."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 11, 4, tzinfo=UTC)
PAIR = ("underlying_instrument", "expiry", "strike")
EXACT = ("contract_id", *PAIR, "option_right")


def _contract(cid: str, right: str) -> raw.RawSelectionIdentityV1:
    return raw.RawSelectionIdentityV1(
        (
            ("contract_id", cid),
            ("underlying_instrument", "NVDA"),
            ("expiry", "2026-12-18"),
            ("strike", Decimal(100)),
            ("option_right", right),
        )
    )


def _setup(
    *,
    no_spot: bool = False,
    wrong_spot: bool = False,
    future_spot: bool = False,
    missing_put: bool = False,
):
    m00 = raw.create_owner()
    call = _contract("C100", "call")
    put = _contract("P100", "put")
    pair = raw.RawSelectionIdentityV1(tuple((k, dict(call.values)[k]) for k in PAIR))
    observations = [
        ("R034", "C100", call, Decimal(4)),
        ("R035", "C100", call, Decimal(6)),
        ("R034", "P100", put, Decimal(3)),
        ("R035", "P100", put, Decimal(5)),
        ("R112", "C100", call, Decimal("0.5")),
        ("R112", "P100", put, Decimal("-0.5")),
        ("R014", "C100", call, Decimal(100)),
        ("R014", "P100", put, Decimal(100)),
        ("R118", "SPOT", pair, Decimal(100)),
    ]
    if no_spot:
        observations = [v for v in observations if v[0] != "R118"]
    if missing_put:
        observations = [v for v in observations if not (v[0] == "R035" and v[1] == "P100")]
    binds = []
    for index, (rid, name, ident, value) in enumerate(observations, 1):
        if rid == "R118" and wrong_spot:
            ident = raw.RawSelectionIdentityV1(
                (
                    ("underlying_instrument", "AMD"),
                    ("expiry", "2026-12-18"),
                    ("strike", Decimal(100)),
                )
            )
        stamp = (
            NOW + timedelta(seconds=1)
            if rid == "R118" and future_spot
            else NOW - timedelta(seconds=2)
        )
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(f"d110-{rid}-{name}"),
                delivery_artifact_ref=raw.delivery_artifact_ref(f"d110-{rid}-{name}"),
                source_provider=raw.provider_id("controlled-d110"),
                native_record={"value": {rid: value}, "identity": dict(ident.values)},
                received_ts_utc=stamp,
                ingestion_sequence=index,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("f4:d110"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="controlled-straddle",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
        binds.append(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1(f"d110-map-{rid}", 1),
                api.VersionRefV1("d110-unit", 1),
                "NVDA",
                ident,
            )
        )
    ids = ("R034", "R035", "R112", "R014", "R118")
    mappers = tuple(
        raw.RawSignalProjectionMappingV1(
            f"d110-map-{rid}",
            1,
            raw.RawSignalCatalogueId(rid),
            "controlled-d110",
            "controlled-straddle",
            ("value", rid),
            "canonical",
            tuple((key, ("identity", key)) for key in (PAIR if rid == "R118" else EXACT)),
        )
        for rid in ids
    )
    basic = api.CalculationParameterSetV1(
        "d110-basic",
        1,
        "P_BASIC",
        (
            ("subject_instrument", "NVDA"),
            ("atm_delta_bucket", "atm"),
        ),
    )
    rules = api.CalculationParameterSetV1(
        "d110-rule",
        1,
        "P_RULE",
        (
            ("delta_bucket_boundaries", (Decimal(0), Decimal("0.4"), Decimal(1))),
            ("delta_bucket_labels", ("wing", "atm")),
        ),
    )
    sel = api.InputSelectionPolicyVersionV1(
        "d110-parent",
        1,
        PAIR,
        timedelta(minutes=1),
        timedelta(seconds=10),
        ("true_instant",),
        (),
    )
    exact = replace(sel, context_id="d110-child", join_keys=EXACT)
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappers,
        parameter_sets=(basic, rules),
        input_selection_policies=(sel, exact),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "d110-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0)
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        "D110",
        "NVDA",
        NOW,
        NOW,
        "d110-20261011",
        "d110-basic",
        1,
        "d110-parent",
        1,
        (),
        raw_input_bindings=tuple(binds),
        parameter_profile_refs=(api.ParameterProfileRefV1("P_RULE", "d110-rule", 1),),
        predecessor_selection_policy_refs=(
            ("D087", api.VersionRefV1("d110-child", 1)),
            ("D091", api.VersionRefV1("d110-child", 1)),
        ),
    )
    return owner, req


def test_d110_straddle_expected_move_percent_and_full_ultimate_lineage() -> None:
    owner, req = _setup()
    result = owner.materialise(req)
    assert result is not None and result.result == Decimal(9)
    assert {item.raw_signal_id for item in result.raw_input_lineage} == {
        "R034",
        "R035",
        "R112",
        "R118",
    }
    assert {item.observation_occurrence_id for item in result.raw_input_lineage} >= {
        "d110-R118-SPOT",
        "d110-R035-P100",
        "d110-R035-C100",
    }
    assert {
        owner.reads.get_derived_occurrence(pid).derived_signal_id
        for pid in result.predecessor_occurrence_ids
    } == {"D109"}
    assert owner.materialise(req) == result


def test_d110_missing_wrong_or_future_spot_and_incomplete_straddle_refuse() -> None:
    for changes in (
        {"no_spot": True},
        {"wrong_spot": True},
        {"future_spot": True},
        {"missing_put": True},
    ):
        owner, req = _setup(**changes)
        assert owner.materialise(req) is None, changes
