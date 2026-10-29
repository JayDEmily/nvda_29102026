"""F4 RC15 D168 two exact candidate legs through the admitted M00 projection."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
LEG_DATA = (
    ("C100", (Decimal("0.50"), Decimal("0.10"), Decimal("0.20"), Decimal("-0.05"), Decimal(100))),
    ("P100", (Decimal("-0.40"), Decimal("0.08"), Decimal("0.15"), Decimal("-0.04"), Decimal(100))),
    ("C105", (Decimal(1000), Decimal(1000), Decimal(1000), Decimal(1000), Decimal(100))),
)
FIELD_IDS = ("R112", "R115", "R116", "R117", "R016")
LEGS = ("C100", "P100")
CANDIDATE = api.CandidateStructureContextV1(
    "rc15-candidate",
    1,
    "two-leg-hedge",
    LEGS,
    ("buy", "sell"),
    (Decimal(2), Decimal(3)),
    Decimal(1),
    (),
    (),
    Decimal(1000),
)


def _public(
    *,
    missing: tuple[str, str] | None = None,
    future_second: bool = False,
    selection_members: tuple[str, ...] = LEGS,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for seq, (contract, amounts) in enumerate(LEG_DATA, start=1):
        fields = dict(zip(FIELD_IDS, amounts, strict=True))
        if missing is not None and missing[0] == contract:
            del fields[missing[1]]
        ts = NOW - timedelta(seconds=2)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(
                    "candidate-leg-" + contract
                ),
                delivery_artifact_ref=raw.delivery_artifact_ref("candidate-leg-" + contract),
                source_provider=raw.provider_id("controlled-rc15-legs"),
                native_record={"greeks": fields},
                received_ts_utc=NOW + timedelta(seconds=1)
                if future_second and contract == "P100"
                else ts,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc15:candidate-legs"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=ts.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in FIELD_IDS),
                source_variant="candidate-greeks",
                subject_instrument=contract,
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc15-candidate-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-rc15-legs",
                "candidate-greeks",
                ("greeks", rid),
                "canonical",
            )
            for rid in FIELD_IDS
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc15-basic",
                1,
                "P_BASIC",
                (("subject_instrument", "NVDA"),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc15-candidate-select",
                1,
                ("subject_instrument",),
                timedelta(seconds=30),
                timedelta(seconds=30),
                ("true_instant",),
                selection_members,
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc15-unit",
                1,
                "canonical",
                "canonical",
                Decimal(1),
                Decimal(0),
            ),
        ),
        contexts=(CANDIDATE,),
        utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        "D168",
        "NVDA",
        NOW,
        NOW,
        "rc15-candidate-public",
        "rc15-basic",
        1,
        "rc15-candidate-select",
        1,
        (api.VersionRefV1("rc15-candidate", 1),),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("rc15-candidate-" + rid, 1),
                api.VersionRefV1("rc15-unit", 1),
                contract,
                None,
            )
            for contract in LEGS
            for rid in FIELD_IDS
        ),
    )
    return owner, req


def test_d168_public_candidate_greeks_exact_two_leg_vector_and_lineage() -> None:
    owner, req = _public()
    out = owner.materialise(req)
    assert out is not None
    assert dict(out.result) == {
        "delta": Decimal(220),
        "gamma": Decimal(-4),
        "vega": Decimal(-5),
        "theta": Decimal(2),
    }
    assert {item.raw_signal_id for item in out.raw_input_lineage} == set(FIELD_IDS)
    assert {item.observation_occurrence_id for item in out.raw_input_lineage} == {
        "candidate-leg-C100",
        "candidate-leg-P100",
    }
    assert out.predecessor_occurrence_ids == ()
    assert owner.materialise(req) == out


def test_d168_public_candidate_greeks_refuses_incomplete_selected_leg() -> None:
    owner, req = _public(missing=("P100", "R115"))
    assert owner.materialise(req) is None


def test_d168_public_candidate_greeks_refuses_future_received_selected_leg() -> None:
    owner, req = _public(future_second=True)
    assert owner.materialise(req) is None


def test_d168_public_candidate_greeks_requires_exact_candidate_context() -> None:
    owner, req = _public()
    assert owner.materialise(replace(req, context_refs=())) is None


def test_d168_public_candidate_greeks_rejects_incompatible_basket_selection() -> None:
    owner, req = _public(selection_members=("C100",))
    assert owner.materialise(req) is None
