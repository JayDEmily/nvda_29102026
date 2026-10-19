"""Literal controlled records/configuration only; tests order all public operations."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw_api
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

ROOT = Path(__file__).resolve().parents[3]
BRIEF = "c23ea315c94b478c568f105e94891a03af62393792a1478c33027a0371738bb8"
ASOF = datetime(2026, 10, 16, 1, tzinfo=UTC)
NOW = ASOF + timedelta(seconds=1)
PROVIDER = "foundation-size-fixture"
SCOPE = PROVIDER + "/cash_size_v1"
AUTHORITY = (
    (
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
    ),
    (
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
    ),
)


def mapping(side, version=1):
    return raw_api.RawSignalProjectionMappingV1(
        "mmt-size-" + side,
        version,
        raw_api.RawSignalCatalogueId("R033" if side == "bid" else "R036"),
        PROVIDER,
        "cash_size_v1",
        ("quote", side + "_size"),
        "shares",
        (),
    )


def observation(side, *, value=None, identity=None, event=None, receipt=None, sequence=None):
    bid = side == "bid"
    event = ASOF - timedelta(seconds=2 if bid else 1) if event is None else event
    return raw_api.RawObservationOccurrenceV1(
        concept_id=raw_api.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=raw_api.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=raw_api.observation_occurrence_id(
            identity or "mmt-size-" + side + "-001"
        ),
        delivery_artifact_ref=raw_api.delivery_artifact_ref("mmt-size-delivery-001"),
        source_provider=raw_api.provider_id(PROVIDER),
        native_record={
            "quote": {side + "_size": Decimal("2" if bid else "1") if value is None else value}
        },
        received_ts_utc=ASOF - timedelta(seconds=1 if bid else 0) if receipt is None else receipt,
        ingestion_sequence=(1 if bid else 2) if sequence is None else sequence,
        ingestion_sequence_scope=raw_api.ingestion_sequence_scope(SCOPE),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=(raw_api.RawSignalCatalogueId("R033" if bid else "R036"),),
        source_variant="cash_size_v1",
        subject_instrument="NVDA",
        native_units="shares",
        source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
        source_timezone_native="UTC",
    )


def raw_source(path):
    """Provision an empty real M00 store; do not admit inputs or produce results."""
    return raw_api.create_owner(durability_port=create_sqlite_persistence(str(path), create=True))


def configuration(reader, path, *, versions=(1, 2), create=True, now=None):
    return dict(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        raw_projection_reader=reader,
        definitions=tuple(
            f.CalculationDefinitionV1(
                "D014",
                f"D014-SIZE-IMBALANCE-{v}",
                "K02_ALGEBRA",
                "(R033 - R036) / (R033 + R036)",
                ("R033", "R036"),
                (),
                "P_BASIC",
                "-1 to 1",
                "scalar_exact_ratio",
                tuple(f.AuthorityArtifactRefV1(*ref) for ref in AUTHORITY),
            )
            for v in versions
        ),
        parameter_sets=tuple(
            f.CalculationParameterSetV1("mmt-size-basic", v, "P_BASIC", "NVDA", ("NVDA",))
            for v in versions
        ),
        input_selection_policies=tuple(
            f.InputSelectionPolicyVersionV1(
                "mmt-size-selection",
                v,
                ("subject_instrument",),
                timedelta(seconds=60),
                timedelta(seconds=10),
                ("true_instant",),
                (),
                PROVIDER,
                "cash_size_v1",
                SCOPE,
                100,
                1000,
            )
            for v in versions
        ),
        unit_conventions=tuple(
            f.UnitConventionVersionV1(
                "mmt-size-shares", v, "shares", "shares", Decimal("1"), Decimal("0")
            )
            for v in versions
        ),
        raw_projection_mappings=tuple(
            mapping(side, v) for v in versions for side in ("bid", "ask")
        ),
        storage=f.SQLiteStorageV1(str(path), create),
        utc_now=(lambda: NOW) if now is None else now,
    )


def request(**changes):
    return f.CalculationRequestV1(
        **(
            dict(
                derived_signal_id="D014",
                subject_instrument="NVDA",
                as_of_utc=ASOF,
                knowledge_cutoff_utc=ASOF,
                calculation_definition_version="D014-SIZE-IMBALANCE-1",
                parameter_set_ref=f.VersionRefV1("mmt-size-basic", 1),
                input_selection_policy_ref=f.VersionRefV1("mmt-size-selection", 1),
                context_refs=(),
                raw_input_bindings=tuple(
                    f.RawInputBindingV1(
                        "R033" if side == "bid" else "R036",
                        f.VersionRefV1("mmt-size-" + side, 1),
                        f.VersionRefV1("mmt-size-shares", 1),
                        "NVDA",
                    )
                    for side in ("bid", "ask")
                ),
            )
            | changes
        )
    )
