"""F4 RC13: M00 public subject-specific market/sector intraday return proofs.

D071-D075 must not reuse a different ETF's same-named R037/R042 prices.
The admitted raw contract and request subject select each exact instrument.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
INSTRUMENTS = (
    ("D071", "SPY"),
    ("D072", "QQQ"),
    ("D073", "SMH"),
    ("D074", "SOXX"),
    ("D075", "NVDA"),
)


def _public(
    did: str,
    subject: str,
    *,
    missing: str | None = None,
    wrong_subject: str | None = None,
    late: str | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    records = (
        ("R037", "current-price", Decimal(120), NOW - timedelta(seconds=2), subject),
        ("R042", "prior-close", Decimal(100), NOW - timedelta(days=1), subject),
        ("R037", "other-market-current", Decimal(900), NOW - timedelta(seconds=1), "AMD"),
        ("R042", "other-market-prior", Decimal(1), NOW - timedelta(days=1), "AMD"),
    )
    for seq, (rid, oid, val, stamp, record_subject) in enumerate(records, 1):
        if oid == missing:
            continue
        if oid == wrong_subject:
            record_subject = "AMD"
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("sector-" + oid),
                source_provider=raw.provider_id("controlled-rc13"),
                native_record={"market": {rid: val}},
                received_ts_utc=NOW + timedelta(seconds=3) if oid == late else stamp,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc13:markets"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="market",
                subject_instrument=record_subject,
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc13-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc13", "market", ("market", rid), "canonical",
            ) for rid in ("R037", "R042")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc13-window", 1, "P_WINDOW",
                (("window_seconds", 86400),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc13-select", 1, ("subject_instrument",),
                timedelta(days=3), timedelta(days=3),
                ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc13-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        did, subject, NOW, NOW,
        "rc13-sector-public", "rc13-window", 1,
        "rc13-select", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("rc13-map-" + rid, 1),
                api.VersionRefV1("rc13-unit", 1), subject, None,
            ) for rid in ("R037", "R042")
        ),
    )
    return owner, req


@pytest.mark.parametrize(("did", "subject"), INSTRUMENTS)
def test_rc13_public_returns_use_exact_requested_instrument(
    did: str, subject: str,
) -> None:
    owner, req = _public(did, subject)
    out = owner.materialise(req)
    assert out is not None and out.result == (Decimal(120) / Decimal(100)).ln()
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        "current-price", "prior-close",
    }
    assert out.predecessor_occurrence_ids == ()
    assert owner.materialise(req) == out


@pytest.mark.parametrize(("did", "subject"), INSTRUMENTS)
def test_rc13_public_returns_refuse_wrong_subject_reference(
    did: str, subject: str,
) -> None:
    owner, req = _public(did, subject, wrong_subject="prior-close")
    assert owner.materialise(req) is None


@pytest.mark.parametrize(("did", "subject"), INSTRUMENTS)
def test_rc13_public_returns_refuse_future_received_current(
    did: str, subject: str,
) -> None:
    owner, req = _public(did, subject, late="current-price")
    assert owner.materialise(req) is None
