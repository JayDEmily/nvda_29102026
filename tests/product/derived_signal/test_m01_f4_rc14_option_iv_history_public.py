"""F4 RC14: option-contract M00 IV history for D094/D095."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 3, tzinfo=UTC)
END = NOW - timedelta(seconds=2)
IDENTITY = raw.RawSelectionIdentityV1(
    (
        ("contract_id", "OPT-C1"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal(150)),
        ("option_right", "call"),
    )
)
KEY_PATHS = tuple((key, ("identity", key)) for key, _ in IDENTITY.values)


def _public(
    *,
    omit: tuple[str, ...] = (),
    wrong_contract: tuple[str, ...] = (),
    future_current: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    series = (
        ("R111", "iv-current", Decimal("0.53"), END),
        ("R111", "iv-anchor-5m", Decimal("0.50"), END - timedelta(minutes=5)),
        ("R111", "iv-anchor-day", Decimal("0.48"), END - timedelta(days=1)),
        ("R111", "iv-near", Decimal("0.90"), END - timedelta(minutes=2)),
        ("R183", "iv-context", Decimal("0.55"), END),
    )
    for seq, (rid, oid, value, instant) in enumerate(series, 1):
        if oid in omit:
            continue
        contract = "OPT-C2" if oid in wrong_contract else "OPT-C1"
        identity = dict(IDENTITY.values)
        identity["contract_id"] = contract
        received = NOW + timedelta(seconds=3) if oid == "iv-current" and future_current else instant
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref(oid),
                source_provider=raw.provider_id("controlled-rc14-history"),
                native_record={"metric": {rid: value}, "identity": identity},
                received_ts_utc=received,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc14:history"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=instant.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="iv-history",
                subject_instrument="NVDA",
                native_units="decimal_volatility",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc14-history-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc14-history", "iv-history", ("metric", rid),
                "decimal_volatility", KEY_PATHS,
            ) for rid in ("R111", "R183")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc14-history-window", 1, "P_WINDOW",
                (("window_seconds", 86400),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc14-history-select", 1, tuple(dict(IDENTITY.values)),
                timedelta(days=3), timedelta(days=3),
                ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc14-history-unit", 1,
                "decimal_volatility", "decimal_volatility", Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        "D094", "NVDA", NOW, NOW, "rc14-history-public",
        "rc14-history-window", 1, "rc14-history-select", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("rc14-history-map-" + rid, 1),
                api.VersionRefV1("rc14-history-unit", 1), "NVDA", IDENTITY,
            ) for rid in ("R111", "R183")
        ),
    )
    return owner, req


@pytest.mark.parametrize(
    ("did", "expected"),
    (("D094", Decimal(3)), ("D095", Decimal(5))),
)
def test_rc14_public_iv_change_exact_history_anchor_and_lineage(
    did: str, expected: Decimal,
) -> None:
    owner, req = _public()
    out = owner.materialise(replace(req, derived_signal_id=did))
    assert out is not None and out.result == expected
    assert out.selection_identity == IDENTITY
    observed = {r.observation_occurrence_id for r in out.raw_input_lineage}
    assert {"iv-current", "iv-near", "iv-anchor-5m", "iv-anchor-day"} <= observed
    assert "iv-context" in observed if did == "D095" else "iv-context" not in observed
    assert out.predecessor_occurrence_ids == ()
    assert owner.materialise(replace(req, derived_signal_id=did)) == out


@pytest.mark.parametrize(
    ("did", "missing"),
    (
        ("D094", ("iv-anchor-5m", "iv-anchor-day")),
        ("D095", ("iv-anchor-day",)),
        ("D095", ("iv-context",)),
    ),
)
def test_rc14_public_iv_change_missing_any_eligible_prior_or_field_refuses(
    did: str, missing: tuple[str, ...],
) -> None:
    owner, req = _public(omit=missing)
    assert owner.materialise(replace(req, derived_signal_id=did)) is None


@pytest.mark.parametrize(
    ("did", "wrong"),
    (("D094", ("iv-anchor-5m", "iv-anchor-day")), ("D095", ("iv-anchor-day",))),
)
def test_rc14_public_iv_change_no_eligible_same_contract_reference_refuses(
    did: str, wrong: tuple[str, ...],
) -> None:
    owner, req = _public(wrong_contract=wrong)
    assert owner.materialise(replace(req, derived_signal_id=did)) is None
