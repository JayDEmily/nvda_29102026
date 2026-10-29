"""RC21 D146: complete macro-level and native release-surprise factor via M00 public API."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
FAMILY = raw.RawSelectionIdentityV1((("release_family", "US-CPI"),))
GROWTH_IDS = ("R267", "R268", "R269", "R264", "R265", "R266")
GROWTH_VALUES = tuple((rid, Decimal(i)) for i, rid in enumerate(GROWTH_IDS, start=1))
HISTORY = (
    ("prior-1", 90, Decimal(110), Decimal(100)),
    ("prior-2", 60, Decimal(120), Decimal(100)),
    ("prior-3", 30, Decimal(140), Decimal(100)),
    ("current", 0, Decimal(150), Decimal(100)),
)
ALL_IDS = (*GROWTH_IDS, "R286", "R285")


def _make_public(
    *,
    missing: str | None = None,
    future: str | None = None,
    conflicting_family: str | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    records: list[tuple[tuple[str, ...], str, dict[str, Decimal], int, str]] = []
    for rid, amount in GROWTH_VALUES:
        records.append(((rid,), "growth-" + rid, {rid: amount}, 0, "US-CPI"))
    for tag, age, actual, consensus in HISTORY:
        records.append((("R286", "R285"), tag, {"R286": actual, "R285": consensus}, age, "US-CPI"))
    # A visible but unrelated macro family must not enter the current score or baseline.
    records.append(
        (("R286", "R285"), "other", {"R286": Decimal(900), "R285": Decimal(10)}, 1, "US-PCE")
    )
    for seq, (ids, tag, data, age, release_family) in enumerate(records, start=1):
        oid = f"rc21-growth-{tag}"
        if oid == missing:
            continue
        if missing is not None and missing.startswith(oid + "-"):
            del data[missing.removeprefix(oid + "-")]
        if oid == conflicting_family:
            release_family = "US-PCE"
        timestamp = NOW - timedelta(days=age, seconds=3)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref(oid),
                source_provider=raw.provider_id("controlled-rc21-growth"),
                native_record={"metric": data, "identity": {"release_family": release_family}},
                received_ts_utc=NOW + timedelta(seconds=2) if oid == future else timestamp,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc21:growth"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=timestamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in ids),
                source_variant="growth",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "growth-map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-rc21-growth",
                "growth",
                ("metric", rid),
                "canonical",
                (("release_family", ("identity", "release_family")),),
            )
            for rid in ALL_IDS
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "growth-score",
                1,
                "P_SCORE",
                (("intercept", Decimal(0)),),
                tuple(
                    api.ScoreFeatureV1(
                        signal_id,
                        "component",
                        (),
                        "identity",
                        None,
                        1,
                        Decimal(1),
                        None,
                        None,
                        (),
                    )
                    for signal_id in (*GROWTH_IDS, "D063")
                ),
            ),
            api.CalculationParameterSetV1(
                "growth-baseline",
                1,
                "P_BASELINE",
                (("history_count", 2), ("minimum_sample", 2)),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "growth-family",
                1,
                ("release_family",),
                timedelta(days=120),
                timedelta(days=120),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "growth-unit",
                1,
                "canonical",
                "canonical",
                Decimal(1),
                Decimal(0),
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D146",
        "NVDA",
        NOW,
        NOW,
        "rc21-growth-public",
        "growth-score",
        1,
        "growth-family",
        1,
        (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "growth-score", 1),
            api.ParameterProfileRefV1("P_BASELINE", "growth-baseline", 1),
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("growth-map-" + rid, 1),
                api.VersionRefV1("growth-unit", 1),
                "NVDA",
                FAMILY,
            )
            for rid in ALL_IDS
        ),
    )
    return owner, request


def test_d146_exact_growth_factor_with_release_lineage_and_retry() -> None:
    owner, req = _make_public()
    out = owner.materialise(req)
    assert out is not None
    # Prior release surprises 10,20,40: selected last 2 -> mean 30, sd sqrt(200).
    expected = Decimal(21) + Decimal(20) / Decimal(200).sqrt()
    assert abs(out.result - expected) < Decimal("0.000000000000000000001")
    assert out.selection_identity == FAMILY
    assert {x.raw_signal_id for x in out.raw_input_lineage} == set(ALL_IDS)
    assert len({x.observation_occurrence_id for x in out.raw_input_lineage}) == 10
    assert {
        owner.reads.get_derived_occurrence(pid).derived_signal_id
        for pid in out.predecessor_occurrence_ids
    } == {"D063"}
    assert owner.materialise(req) == out


def test_d146_refuses_missing_native_growth_component() -> None:
    owner, req = _make_public(missing="rc21-growth-growth-R268")
    assert owner.materialise(req) is None


def test_d146_refuses_incomplete_selected_macro_release() -> None:
    owner, req = _make_public(missing="rc21-growth-current-R285")
    assert owner.materialise(req) is None


def test_d146_refuses_future_growth_print() -> None:
    owner, req = _make_public(future="rc21-growth-growth-R269")
    assert owner.materialise(req) is None


def test_d146_does_not_substitute_wrong_release_family() -> None:
    owner, req = _make_public(conflicting_family="rc21-growth-growth-R267")
    assert owner.materialise(req) is None
