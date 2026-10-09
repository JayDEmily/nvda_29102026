"""F4 RC02: independent M00 public quote and size arithmetic/lineage proofs.

The four related D rows are requested independently through the admitted M01
owner; predecessor D011/D012 for D013 is not injected by the test.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 14, tzinfo=UTC)
FIELDS = ("R034", "R035", "R033", "R036")
VALUES = {"R034": Decimal(100), "R035": Decimal(102), "R033": Decimal(8), "R036": Decimal(2)}


def public_book_quote(
    *, missing: str | None = None, future: str | None = None,
    wrong_subject: str | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, tuple[api.RawInputBindingV1, ...]]:
    m00 = raw.create_owner()
    for seq, rid in enumerate(FIELDS, 1):
        if rid == missing:
            continue
        timestamp = NOW + timedelta(seconds=1) if rid == future else NOW - timedelta(seconds=1)
        subject = "OTHER" if rid == wrong_subject else "NVDA"
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("rc02-" + rid),
                delivery_artifact_ref=raw.delivery_artifact_ref("rc02-delivery-" + rid),
                source_provider=raw.provider_id("controlled-rc02"),
                native_record={"quote": {"value": VALUES[rid]}},
                received_ts_utc=timestamp,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-rc02:quote"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=timestamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="quote",
                subject_instrument=subject,
                native_units="native",
                revision_vintage_native="v1",
            )
        )
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "rc02-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
            "controlled-rc02", "quote", ("quote", "value"),
            "price" if rid in ("R034", "R035") else "contracts",
        )
        for rid in FIELDS
    )
    unit_conventions = tuple(
        api.UnitConventionVersionV1(
            "rc02-unit-" + rid, 1, unit, unit, Decimal(1), Decimal(0)
        )
        for rid in FIELDS
        for unit in ("price" if rid in ("R034", "R035") else "contracts",)
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc02-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc02-policy", 1, ("subject_instrument",),
                timedelta(seconds=10), timedelta(seconds=10), ("true_instant",), (),
            ),
        ),
        unit_conventions=unit_conventions,
        contexts=(),
        utc_now=lambda: NOW,
    )
    bindings = tuple(
        api.RawInputBindingV1(
            rid, api.VersionRefV1("rc02-map-" + rid, 1),
            api.VersionRefV1("rc02-unit-" + rid, 1), "NVDA", None,
        )
        for rid in FIELDS
    )
    return owner, bindings


def request(did: str, bindings: tuple[api.RawInputBindingV1, ...]) -> api.CalculationRequestV1:
    return api.CalculationRequestV1(
        did, "NVDA", NOW, NOW, "rc02-20261009", "rc02-basic", 1,
        "rc02-policy", 1, (), raw_input_bindings=bindings,
    )


@pytest.mark.parametrize(
    ("did", "expected", "expected_fields"),
    [
        ("D011", Decimal(101), {"R034", "R035"}),
        ("D012", Decimal(2), {"R034", "R035"}),
        ("D013", Decimal(200) / Decimal(101), {"R034", "R035"}),
        ("D014", Decimal("0.6"), {"R033", "R036"}),
    ],
)
def test_rc02_public_nbbo_exact_arithmetic_raw_lineage_and_retry(
    did: str, expected: Decimal, expected_fields: set[str]
) -> None:
    owner, bindings = public_book_quote()
    output = owner.materialise(request(did, bindings))
    assert output is not None
    assert output.result == expected
    assert {entry.raw_signal_id for entry in output.raw_input_lineage} == expected_fields
    assert {entry.observation_occurrence_id for entry in output.raw_input_lineage} == {
        "rc02-" + rid for rid in expected_fields
    }
    if did == "D013":
        assert {
            owner.reads.get_derived_occurrence(oid).derived_signal_id
            for oid in output.predecessor_occurrence_ids
        } == {"D011", "D012"}
    assert owner.materialise(request(did, bindings)) == output


@pytest.mark.parametrize(
    ("did", "missing"),
    [("D011", "R035"), ("D012", "R034"), ("D013", "R035"), ("D014", "R036")],
)
def test_rc02_public_nbbo_refuses_missing_required_source(did: str, missing: str) -> None:
    owner, bindings = public_book_quote(missing=missing)
    assert owner.materialise(request(did, bindings)) is None


@pytest.mark.parametrize("did,field", [("D011", "R035"), ("D013", "R035"), ("D014", "R036")])
def test_rc02_public_nbbo_refuses_future_or_wrong_subject(did: str, field: str) -> None:
    future, bindings = public_book_quote(future=field)
    assert future.materialise(request(did, bindings)) is None
    other, bindings = public_book_quote(wrong_subject=field)
    assert other.materialise(request(did, bindings)) is None
