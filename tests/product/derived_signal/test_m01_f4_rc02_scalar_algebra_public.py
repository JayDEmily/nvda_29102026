"""F4 RC02: independently admitted M00 field values for eight scalar algebra rows.

Each source field is a separate native raw observation; M01 fetches them using
versioned projection/unit bindings rather than direct kernel fixture injection.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 14, tzinfo=UTC)


@dataclass(frozen=True)
class Case:
    did: str
    inputs: tuple[tuple[str, Decimal], ...]
    expected: Decimal | tuple[tuple[str, Decimal], ...]


CASES = (
    Case("D025", (("R039", Decimal(90)), ("R040", Decimal(110)), ("R037", Decimal(100))),
         Decimal("0.5")),
    Case("D042", (("R247", Decimal("0.04")), ("R249", Decimal("0.0525"))),
         Decimal("1.25")),
    Case("D043", (("R246", Decimal("0.0425")), ("R249", Decimal("0.0525"))),
         Decimal("1")),
    Case("D047", (("R257", Decimal("0.052")), ("R256", Decimal("0.051"))),
         Decimal(10)),
    Case("D057", (("R238", Decimal(18)), ("R239", Decimal(20))),
         (("point_difference", Decimal(-2)), ("ratio", Decimal("0.9")))),
    Case("D058", (("R239", Decimal(20)), ("R236", Decimal(19))),
         (("point_difference", Decimal(1)), ("ratio", Decimal(20) / Decimal(19)))),
    Case("D059", (("R236", Decimal(19)), ("R240", Decimal(21))),
         (("point_difference", Decimal(-2)), ("ratio", Decimal(19) / Decimal(21)))),
    Case("D060", (("R237", Decimal(110)), ("R236", Decimal(19))),
         Decimal(110) / Decimal(19)),
)


def public_scalar(
    case: Case,
    *, omit: str | None = None,
    future: str | None = None,
    other_subject: str | None = None,
    overrides: dict[str, Decimal] | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for seq, (rid, default) in enumerate(case.inputs, 1):
        if rid == omit:
            continue
        value = (overrides or {}).get(rid, default)
        stamp = NOW + timedelta(seconds=1) if rid == future else NOW - timedelta(seconds=seq)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(case.did + "-" + rid),
                delivery_artifact_ref=raw.delivery_artifact_ref("scalar-" + case.did + rid),
                source_provider=raw.provider_id("controlled-rc02-scalar"),
                native_record={"metric": {"value": value}},
                received_ts_utc=stamp,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-rc02:metrics"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="metric",
                subject_instrument="OTHER" if rid == other_subject else "NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "scalar-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
            "controlled-rc02-scalar", "metric", ("metric", "value"), "canonical",
        )
        for rid, _ in case.inputs
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(api.CalculationParameterSetV1(
            "rc02-scalar-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "rc02-scalar-select", 1, ("subject_instrument",),
            timedelta(seconds=10), timedelta(seconds=10), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "scalar-canonical", 1, "canonical", "canonical", Decimal(1), Decimal(0)
        ),),
        contexts=(),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        case.did, "NVDA", NOW, NOW, "rc02-scalar", "rc02-scalar-basic", 1,
        "rc02-scalar-select", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("scalar-map-" + rid, 1),
                api.VersionRefV1("scalar-canonical", 1), "NVDA", None,
            )
            for rid, _ in case.inputs
        ),
    )
    return owner, request


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.did)
def test_rc02_public_algebra_result_lineage_and_repeat(case: Case) -> None:
    owner, request = public_scalar(case)
    output = owner.materialise(request)
    assert output is not None
    assert output.result == case.expected
    assert {item.raw_signal_id for item in output.raw_input_lineage} == {
        rid for rid, _ in case.inputs
    }
    assert {item.observation_occurrence_id for item in output.raw_input_lineage} == {
        case.did + "-" + rid for rid, _ in case.inputs
    }
    assert owner.materialise(request) == output


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.did)
def test_rc02_public_algebra_missing_input_refused(case: Case) -> None:
    owner, request = public_scalar(case, omit=case.inputs[-1][0])
    assert owner.materialise(request) is None


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.did)
def test_rc02_public_algebra_future_and_subject_mismatch_refused(case: Case) -> None:
    last_rid = case.inputs[-1][0]
    future_owner, request = public_scalar(case, future=last_rid)
    assert future_owner.materialise(request) is None
    other_owner, request = public_scalar(case, other_subject=last_rid)
    assert other_owner.materialise(request) is None


def test_rc02_public_d025_zero_session_range_and_d060_zero_vix_refused() -> None:
    d025, request = public_scalar(CASES[0], overrides={"R040": Decimal(90)})
    assert d025.materialise(request) is None
    d060, request = public_scalar(CASES[-1], overrides={"R236": Decimal(0)})
    assert d060.materialise(request) is None
