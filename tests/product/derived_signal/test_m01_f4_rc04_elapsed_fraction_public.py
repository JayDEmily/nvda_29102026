"""F4 RC04 proof-first: D028 historical samples must match session fraction.

The accepted brief §5 K04 and the authoritative R041/R044 edge mandate
same-elapsed-session-time baseline, not an arbitrary pair of prior R041 rows.
These fixtures use identical M00 observation IDs for each R041/R044 pair.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)


def _public(
    fractions: tuple[Decimal, Decimal, Decimal],
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    values = (
        (Decimal(8), Decimal(999), Decimal(12), Decimal(16))
        if len(fractions) == 4
        else (Decimal(8), Decimal(12), Decimal(16))
    )
    for i, (fraction, value) in enumerate(zip(fractions, values, strict=True)):
        instant = NOW - timedelta(minutes=2 * (len(fractions) - i))
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(f"elapsed-{i}"),
                delivery_artifact_ref=raw.delivery_artifact_ref(f"elapsed-{i}"),
                source_provider=raw.provider_id("controlled-rc04-elapsed"),
                native_record={"metrics": {"R041": value, "R044": fraction}},
                received_ts_utc=instant,
                ingestion_sequence=i + 1,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc04:elapsed"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=instant.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(
                    raw.RawSignalCatalogueId("R041"), raw.RawSignalCatalogueId("R044")
                ),
                source_variant="metric",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                f"elapsed-map-{rid}", 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc04-elapsed", "metric",
                ("metrics", rid), "canonical",
            )
            for rid in ("R041", "R044")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "elapsed-baseline", 1, "P_BASELINE",
                (("history_count", 2), ("minimum_sample", 2)),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "elapsed-subject", 1, ("subject_instrument",),
                timedelta(minutes=15), timedelta(minutes=15),
                ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "elapsed-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D028", "NVDA", NOW, NOW, "rc04-elapsed-public",
        "elapsed-baseline", 1, "elapsed-subject", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1(f"elapsed-map-{rid}", 1),
                api.VersionRefV1("elapsed-unit", 1), "NVDA", None,
            )
            for rid in ("R041", "R044")
        ),
    )
    return owner, request


def test_d028_public_requires_historical_baseline_at_current_session_fraction() -> None:
    owner, request = _public(
        (Decimal("0.25"), Decimal("0.75"), Decimal("0.5"))
    )
    # There are two earlier R041 values, but neither belongs to the
    # current R044 elapsed-session-fraction bucket.  No valid baseline exists.
    assert owner.materialise(request) is None


def test_d028_public_same_fraction_history_gives_exact_volume_ratio() -> None:
    owner, request = _public(
        (Decimal("0.5"), Decimal("0.5"), Decimal("0.5"))
    )
    result = owner.materialise(request)
    assert result is not None and result.result == Decimal("1.6")
    assert {r.observation_occurrence_id for r in result.raw_input_lineage} == {
        "elapsed-0", "elapsed-1", "elapsed-2"
    }
    assert owner.materialise(request) == result


def test_d028_public_skips_interleaved_wrong_fraction_in_complete_history() -> None:
    owner, request = _public(
        (Decimal("0.5"), Decimal("0.25"), Decimal("0.5"), Decimal("0.5"))
    )
    # The intervening 999 quantity must not displace either valid .5
    # historical volume, even though it is temporally nearer.
    result = owner.materialise(request)
    assert result is not None and result.result == Decimal("1.6")
    assert owner.materialise(request) == result


def test_d028_public_refuses_invalid_native_session_fraction() -> None:
    owner, request = _public(
        (Decimal("0.5"), Decimal("1.5"), Decimal("0.5"))
    )
    assert owner.materialise(request) is None
