"""F4 proof-first: D029-D031 use exact source-native intraday baseline buckets.

The matching bucket is an immutable P_BASELINE selection rule and an admitted
M00 mapping identity; unrelated observed bars never supply a prior sample.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 14, 5, tzinfo=UTC)
ROWS = (("D029", "R144"), ("D030", "R062"), ("D031", "R063"))


def _request(did: str, rid: str, *, contaminated: bool = True,
             missing_matching_rule: bool = False,
             mismatched_history: bool = False):
    m00 = raw.create_owner()
    history_bucket = "09:31" if mismatched_history else "09:30"
    events = [
        ("tod-prior-a", Decimal(8), NOW - timedelta(days=3, minutes=5), history_bucket),
        ("tod-prior-b", Decimal(12), NOW - timedelta(days=2, minutes=5), history_bucket),
        ("tod-current", Decimal(16), NOW - timedelta(minutes=5), "09:30"),
    ]
    if contaminated:
        # A more recent historical observation at another time of day must
        # not displace or contribute to the exact matching baseline.
        events.insert(2, ("tod-wrong-bucket", Decimal(200),
                          NOW - timedelta(days=1, minutes=4), "09:31"))
    for sequence, (oid, value, at, bucket) in enumerate(events, start=1):
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("tod-" + oid),
                source_provider=raw.provider_id("controlled-tod"),
                native_record={"metrics": {rid: value}, "time_of_day_bucket": bucket},
                received_ts_utc=at,
                ingestion_sequence=sequence,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-tod:history"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=at.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="metric",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=(
            raw.RawSignalProjectionMappingV1(
                "tod-map", 1, raw.RawSignalCatalogueId(rid),
                "controlled-tod", "metric", ("metrics", rid), "canonical",
                selection_identity_field_paths=(("time_of_day_bucket", ("time_of_day_bucket",)),),
            ),
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "tod-baseline", 1, "P_BASELINE",
                (("history_count", 2), ("minimum_sample", 2))
                if missing_matching_rule else
                (("history_count", 2), ("minimum_sample", 2),
                 ("matching_rule", "source_native_time_of_day_bucket")),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "tod-subject", 1, ("subject_instrument",),
                timedelta(minutes=15), timedelta(minutes=15),
                ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "tod-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0)
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        did, "NVDA", NOW, NOW, "tod-public", "tod-baseline", 1,
        "tod-subject", 1, (),
        raw_input_bindings=(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("tod-map", 1),
                api.VersionRefV1("tod-unit", 1), "NVDA", None,
            ),
        ),
    )
    return owner, req


@pytest.mark.parametrize(("did", "rid"), ROWS)
def test_same_native_bucket_yields_exact_z_with_competing_bar(did: str, rid: str) -> None:
    owner, request = _request(did, rid)
    result = owner.materialise(request)
    assert result is not None
    assert result.result == Decimal(6) / Decimal(8).sqrt()
    assert {"tod-prior-a", "tod-prior-b", "tod-current"}.issubset(
        {item.observation_occurrence_id for item in result.raw_input_lineage}
    )
    assert owner.materialise(request) == result


@pytest.mark.parametrize(("did", "rid"), ROWS)
def test_no_same_bucket_history_must_refuse(did: str, rid: str) -> None:
    owner, request = _request(did, rid, mismatched_history=True)
    assert owner.materialise(request) is None


@pytest.mark.parametrize(("did", "rid"), ROWS)
def test_missing_versioned_bucket_matching_rule_must_refuse(did: str, rid: str) -> None:
    owner, request = _request(did, rid, missing_matching_rule=True, contaminated=False)
    assert owner.materialise(request) is None
