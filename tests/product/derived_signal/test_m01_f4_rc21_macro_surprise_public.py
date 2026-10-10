"""F4 RC21: release-specific historical macro-surprise z-score through admitted M00."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
IDENTITY = raw.RawSelectionIdentityV1((("release_family", "US-CPI"),))
FIELDS = ("R286", "R285")
ROWS = (
    ("prior-1", 90, Decimal(110), Decimal(100)),
    ("prior-2", 60, Decimal(120), Decimal(100)),
    ("prior-3", 30, Decimal(140), Decimal(100)),
    ("current", 0, Decimal(150), Decimal(100)),
    ("other-family", 1, Decimal(1000), Decimal(10)),
)


def _public(
    *, missing_field: tuple[str, str] | None = None,
    zero_sd: bool = False,
    future_current: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for seq, (tag, days, actual, consensus) in enumerate(ROWS, 1):
        stamp = NOW - timedelta(days=days, seconds=3)
        if zero_sd and tag in ("prior-2", "prior-3"):
            actual = Decimal(110)
        if zero_sd and tag == "current":
            actual = Decimal(150)
        data = {"R286": actual, "R285": consensus}
        if missing_field is not None and tag == missing_field[0]:
            del data[missing_field[1]]
        family = "US-PCE" if tag == "other-family" else "US-CPI"
        m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id("surprise-" + tag),
            delivery_artifact_ref=raw.delivery_artifact_ref("surprise-" + tag),
            source_provider=raw.provider_id("controlled-rc21-macro"),
            native_record={"fields": data, "identity": {"release_family": family}},
            received_ts_utc=(
                NOW + timedelta(seconds=1) if future_current and tag == "current" else stamp
            ),
            ingestion_sequence=seq,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("rc21:macro-surprise"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=stamp.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in FIELDS),
            source_variant="macro-surprise", subject_instrument="NVDA",
            native_units="canonical", revision_vintage_native="v1",
        ))
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(raw.RawSignalProjectionMappingV1(
            "rc21-surprise-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
            "controlled-rc21-macro", "macro-surprise", ("fields", rid), "canonical",
            (("release_family", ("identity", "release_family")),),
        ) for rid in FIELDS),
        parameter_sets=(api.CalculationParameterSetV1(
            "rc21-surprise-baseline", 1, "P_BASELINE",
            (("history_count", 2), ("minimum_sample", 2)),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "rc21-surprise-select", 1, ("release_family",),
            timedelta(days=120), timedelta(days=120), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "rc21-surprise-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
        ),), contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        "D063", "NVDA", NOW, NOW, "rc21-surprise-public", "rc21-surprise-baseline", 1,
        "rc21-surprise-select", 1, (),
        raw_input_bindings=tuple(api.RawInputBindingV1(
            rid, api.VersionRefV1("rc21-surprise-map-" + rid, 1),
            api.VersionRefV1("rc21-surprise-unit", 1), "NVDA", IDENTITY,
        ) for rid in FIELDS),
    )
    return owner, req


def test_rc21_macro_surprise_zscore_exact_release_group_lineage_and_retry() -> None:
    owner, req = _public()
    result = owner.materialise(req)
    expected = Decimal(20) / Decimal(200).sqrt()
    assert result is not None and abs(result.result - expected) < Decimal("0.000000000000000000001")
    assert result.selection_identity == IDENTITY
    assert {r.raw_signal_id for r in result.raw_input_lineage} == set(FIELDS)
    assert {r.observation_occurrence_id for r in result.raw_input_lineage} == {
        "surprise-prior-1", "surprise-prior-2", "surprise-prior-3", "surprise-current",
    }
    assert owner.materialise(req) == result


def test_rc21_macro_surprise_refuses_incomplete_latest_release() -> None:
    owner, req = _public(missing_field=("current", "R285"))
    assert owner.materialise(req) is None


def test_rc21_macro_surprise_refuses_incomplete_selected_history_release() -> None:
    owner, req = _public(missing_field=("prior-3", "R285"))
    assert owner.materialise(req) is None


def test_rc21_macro_surprise_rejects_zero_historical_variance() -> None:
    owner, req = _public(zero_sd=True)
    assert owner.materialise(req) is None


def test_rc21_macro_surprise_excludes_future_unreceived_current_release() -> None:
    owner, req = _public(future_current=True)
    result = owner.materialise(req)
    assert result is None or all(
        r.observation_occurrence_id != "surprise-current" for r in result.raw_input_lineage
    )
