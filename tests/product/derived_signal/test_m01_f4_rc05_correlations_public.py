"""F4 RC05 proof-first: D082 requires common-grid price *returns*, not levels.

Uses admitted M00 observations and the configured P_REGRESSION exact-length
return window. The two price series have perfectly anti-correlated daily log
returns, despite their price-level Pearson coefficient differing from -1.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
BASKET = ("NVDA", "SPY")
PRICES = {
    "NVDA": (Decimal(100), Decimal(110), Decimal(99), Decimal("108.9")),
    "SPY": (Decimal(100), Decimal(90), Decimal(99), Decimal("89.1")),
}


def _public(
    *, missing: tuple[str, int] | None = None,
    future: tuple[str, int] | None = None,
    flat: bool = False,
    basket: tuple[str, ...] = BASKET,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    seq = 0
    for subject, prices in PRICES.items():
        for i, price in enumerate(prices):
            if missing == (subject, i):
                continue
            seq += 1
            stamp = NOW - timedelta(minutes=4 - i)
            oid = f"{subject.lower()}-{i}"
            value = Decimal(100) if flat and subject == "SPY" else price
            m00.commands.admit_raw_observation_occurrence(
                raw.RawObservationOccurrenceV1(
                    concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=raw.observation_occurrence_id(oid),
                    delivery_artifact_ref=raw.delivery_artifact_ref("rc05-" + oid),
                    source_provider=raw.provider_id("controlled-rc05-corr"),
                    native_record={"metrics": {"R151": value}},
                    received_ts_utc=NOW + timedelta(seconds=1) if future == (subject, i) else stamp,
                    ingestion_sequence=seq,
                    ingestion_sequence_scope=raw.ingestion_sequence_scope("rc05:corr"),
                    source_temporal_kind="true_instant",
                    source_timestamp_raw=stamp.isoformat(),
                    source_timezone_native="UTC",
                    raw_signal_catalogue_ids=(raw.RawSignalCatalogueId("R151"),),
                    source_variant="price-close",
                    subject_instrument=subject,
                    native_units="canonical",
                    revision_vintage_native="v1",
                )
            )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=(
            raw.RawSignalProjectionMappingV1(
                "rc05-corr-map", 1, raw.RawSignalCatalogueId("R151"),
                "controlled-rc05-corr", "price-close", ("metrics", "R151"), "canonical",
            ),
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc05-corr-window", 1, "P_REGRESSION",
                (("minimum_sample", 3), ("history_count", 3)),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc05-corr-policy", 1, ("subject_instrument",),
                timedelta(minutes=15), timedelta(minutes=15), ("true_instant",), basket,
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc05-corr-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        "D082", "NVDA", NOW, NOW, "rc05-public", "rc05-corr-window", 1,
        "rc05-corr-policy", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                "R151", api.VersionRefV1("rc05-corr-map", 1),
                api.VersionRefV1("rc05-corr-unit", 1), member, None,
            ) for member in BASKET
        ),
    )
    return owner, req


def test_d082_public_uses_aligned_log_returns_not_price_levels() -> None:
    owner, request = _public()
    out = owner.materialise(request)
    assert out is not None
    assert dict(out.result) == {
        "subjects": ("NVDA", "SPY"),
        "matrix": ((Decimal(1), Decimal(-1)), (Decimal(-1), Decimal(1))),
    }
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        f"{member.lower()}-{i}" for member in BASKET for i in range(4)
    }
    assert out.predecessor_occurrence_ids == ()
    assert owner.materialise(request) == out


def test_d082_public_missing_common_grid_point_refuses() -> None:
    owner, req = _public(missing=("SPY", 2))
    assert owner.materialise(req) is None


def test_d082_public_future_common_grid_point_refuses() -> None:
    owner, req = _public(future=("SPY", 3))
    assert owner.materialise(req) is None


def test_d082_public_zero_variance_return_series_refuses() -> None:
    owner, req = _public(flat=True)
    assert owner.materialise(req) is None


def test_d082_public_immutable_basket_mismatch_refuses() -> None:
    owner, req = _public(basket=("NVDA",))
    assert owner.materialise(req) is None
