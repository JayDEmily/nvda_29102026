"""F4 RC13: D083 public contemporaneous fixed basket, not history SD."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
BASKET = ("NVDA", "AMD", "INTC")
PRICES = (
    ("NVDA", Decimal(120), Decimal(100)),
    ("AMD", Decimal(200), Decimal(200)),
    ("INTC", Decimal(90), Decimal(100)),
)


def _public(
    *,
    missing: tuple[str, str] | None = None,
    selection_basket: tuple[str, ...] = BASKET,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    seq = 0
    for instrument, current, prior in PRICES:
        for rid, value, age in (
            ("R037", current, timedelta(seconds=2)),
            ("R042", prior, timedelta(days=1)),
        ):
            if missing == (instrument, rid):
                continue
            seq += 1
            ts = NOW - age
            oid = instrument.lower() + "-" + rid
            m00.commands.admit_raw_observation_occurrence(
                raw.RawObservationOccurrenceV1(
                    concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=raw.observation_occurrence_id(oid),
                    delivery_artifact_ref=raw.delivery_artifact_ref("rc13-cross-" + oid),
                    source_provider=raw.provider_id("controlled-rc13-cross"),
                    native_record={"metric": {rid: value}},
                    received_ts_utc=ts,
                    ingestion_sequence=seq,
                    ingestion_sequence_scope=raw.ingestion_sequence_scope("rc13:cross"),
                    source_temporal_kind="true_instant",
                    source_timestamp_raw=ts.isoformat(),
                    source_timezone_native="UTC",
                    raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                    source_variant="metric",
                    subject_instrument=instrument,
                    native_units="canonical",
                    revision_vintage_native="v1",
                )
            )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc13-cross-map-" + rid, 1,
                raw.RawSignalCatalogueId(rid), "controlled-rc13-cross",
                "metric", ("metric", rid), "canonical",
            ) for rid in ("R037", "R042")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc13-cross", 1, "P_CROSS_SECTION",
                (("basket_membership", BASKET),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc13-cross-select", 1, ("subject_instrument",),
                timedelta(days=3), timedelta(days=3), ("true_instant",),
                selection_basket,
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc13-cross-unit", 1, "canonical", "canonical",
                Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        "D083", "NVDA", NOW, NOW, "rc13-cross-public",
        "rc13-cross", 1, "rc13-cross-select", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("rc13-cross-map-" + rid, 1),
                api.VersionRefV1("rc13-cross-unit", 1), instrument, None,
            )
            for instrument in BASKET for rid in ("R037", "R042")
        ),
    )
    return owner, req


def test_rc13_public_cross_section_exact_three_member_sample_dispersion() -> None:
    owner, req = _public()
    out = owner.materialise(req)
    assert out is not None
    returns = tuple((curr / prior).ln() for _, curr, prior in PRICES)
    mean = sum(returns, Decimal(0)) / Decimal(len(returns))
    expected = (
        sum(((r - mean) ** 2 for r in returns), Decimal(0))
        / Decimal(len(returns) - 1)
    ).sqrt()
    assert out.result == expected
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        member.lower() + "-" + rid
        for member in BASKET for rid in ("R037", "R042")
    }
    assert out.predecessor_occurrence_ids == ()
    assert owner.materialise(req) == out


def test_rc13_public_cross_section_missing_one_member_refuses() -> None:
    owner, req = _public(missing=("INTC", "R042"))
    assert owner.materialise(req) is None


def test_rc13_public_cross_section_immutable_basket_mismatch_refuses() -> None:
    owner, req = _public(selection_basket=("NVDA", "AMD"))
    assert owner.materialise(req) is None
