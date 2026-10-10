"""F4 RC14: D103 matched-grid IV surface change through the admitted M00 seam."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
SUBJECT = raw.RawSelectionIdentityV1((("underlying_instrument", "NVDA"),))
KEY_PATHS = (
    ("underlying_instrument", ("identity", "underlying_instrument")),
    ("snapshot", ("identity", "snapshot")),
    ("grid_key", ("identity", "grid_key")),
)
ROWS = (
    ("prior-atm", "prior", "ATM", Decimal("0.30"), 302),
    ("prior-otm", "prior", "OTM", Decimal("0.40"), 302),
    ("current-atm", "current", "ATM", Decimal("0.35"), 2),
    ("current-otm", "current", "OTM", Decimal("0.45"), 2),
)


def _public(
    *, missing: str | None = None, future: str | None = None,
    wrong_subject: str | None = None, duplicate: bool = False,
    reverse: bool = False, malformed_label: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    records = list(ROWS)
    if duplicate:
        records.append(("prior-atm-duplicate", "prior", "ATM", Decimal("0.10"), 301))
    for seq, (oid, snap, grid, iv, seconds) in enumerate(records, 1):
        if oid == missing:
            continue
        ident = {"underlying_instrument": "AMD" if oid == wrong_subject else "NVDA",
                 "snapshot": snap, "grid_key": grid}
        if reverse:
            seconds = 302 if snap == "current" else 2
        if malformed_label and oid == "prior-otm":
            ident["snapshot"] = "unlabelled"
        stamp = NOW - timedelta(seconds=seconds)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("rc14-shift-" + oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("rc14-shift-" + oid),
                source_provider=raw.provider_id("controlled-rc14-surface"),
                native_record={"metric": {"R111": iv}, "identity": ident},
                received_ts_utc=(NOW + timedelta(seconds=3) if oid == future else stamp),
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc14:surface"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId("R111"),),
                source_variant="matched-iv-grid",
                subject_instrument=ident["underlying_instrument"],
                native_units="decimal_volatility", revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=(raw.RawSignalProjectionMappingV1(
            "rc14-shift-map", 1, raw.RawSignalCatalogueId("R111"),
            "controlled-rc14-surface", "matched-iv-grid", ("metric", "R111"),
            "decimal_volatility", KEY_PATHS,
        ),),
        parameter_sets=(api.CalculationParameterSetV1(
            "rc14-shift-window", 1, "P_WINDOW", (("anchor_seconds", 300),),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "rc14-shift-select", 1, ("underlying_instrument",),
            timedelta(seconds=600), timedelta(seconds=600), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "rc14-shift-unit", 1, "decimal_volatility", "decimal_volatility",
            Decimal(1), Decimal(0),
        ),),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        "D103", "NVDA", NOW, NOW, "rc14-surface-public",
        "rc14-shift-window", 1, "rc14-shift-select", 1, (),
        raw_input_bindings=(api.RawInputBindingV1(
            "R111", api.VersionRefV1("rc14-shift-map", 1),
            api.VersionRefV1("rc14-shift-unit", 1), "NVDA", SUBJECT,
        ),),
    )
    return owner, req


def test_rc14_public_surface_shift_exact_matched_two_point_mean_and_lineage() -> None:
    owner, req = _public()
    out = owner.materialise(req)
    assert out is not None and out.result == Decimal(5)
    assert {item.observation_occurrence_id for item in out.raw_input_lineage} == {
        "rc14-shift-" + oid for oid, *_ in ROWS
    }
    assert out.predecessor_occurrence_ids == ()
    assert owner.materialise(req) == out


def test_rc14_public_surface_shift_refuses_missing_prior_grid_point() -> None:
    owner, req = _public(missing="prior-otm")
    assert owner.materialise(req) is None


def test_rc14_public_surface_shift_refuses_missing_current_grid_point() -> None:
    owner, req = _public(missing="current-atm")
    assert owner.materialise(req) is None


def test_rc14_public_surface_shift_refuses_future_member() -> None:
    owner, req = _public(future="prior-otm")
    assert owner.materialise(req) is None


def test_rc14_public_surface_shift_refuses_wrong_instrument_grid_member() -> None:
    owner, req = _public(wrong_subject="prior-otm")
    assert owner.materialise(req) is None


def test_rc14_public_surface_shift_refuses_ambiguous_duplicate_grid() -> None:
    owner, req = _public(duplicate=True)
    assert owner.materialise(req) is None


def test_rc14_public_surface_shift_refuses_reversed_snapshot_chronology() -> None:
    owner, req = _public(reverse=True)
    assert owner.materialise(req) is None


def test_rc14_public_surface_shift_refuses_unclassified_snapshot() -> None:
    owner, req = _public(malformed_label=True)
    assert owner.materialise(req) is None
