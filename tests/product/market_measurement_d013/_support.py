"""Authority literals and store/child provisioning only; callers order operations."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw_api
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

ROOT = Path(__file__).resolve().parents[3]
PREDECESSOR_BRIEF = "a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393"
OLD_BRIEF = "3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233"
ASOF = datetime(2026, 10, 16, 1, tzinfo=UTC)
NOW = ASOF + timedelta(seconds=1)
PROVIDER = "foundation-pilot-fixture"
SCOPE = PROVIDER + "/cash_quote_v1"
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
        "mmt-pilot-" + side,
        version,
        raw_api.RawSignalCatalogueId("R034" if side == "bid" else "R035"),
        PROVIDER,
        "cash_quote_v1",
        ("quote", side),
        "price",
        (),
    )


def observation(
    side, *, value=None, identity=None, event=None, receipt=None, sequence=None, **changes
):
    bid = side == "bid"
    event = ASOF - timedelta(seconds=2 if bid else 1) if event is None else event
    values = dict(
        concept_id=raw_api.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=raw_api.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=raw_api.observation_occurrence_id(
            identity or f"mmt-pilot-{side}-001"
        ),
        delivery_artifact_ref=raw_api.delivery_artifact_ref("mmt-pilot-delivery-001"),
        source_provider=raw_api.provider_id(PROVIDER),
        native_record={
            "quote": {side: Decimal("100" if bid else "102") if value is None else value}
        },
        received_ts_utc=ASOF - timedelta(seconds=1 if bid else 0) if receipt is None else receipt,
        ingestion_sequence=(1 if bid else 2) if sequence is None else sequence,
        ingestion_sequence_scope=raw_api.ingestion_sequence_scope(SCOPE),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=(raw_api.RawSignalCatalogueId("R034" if bid else "R035"),),
        source_variant="cash_quote_v1",
        subject_instrument="NVDA",
        native_units="price",
        source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
        source_timezone_native="UTC",
    )
    return raw_api.RawObservationOccurrenceV1(**(values | changes))


def raw_source(path):
    """No observations admitted by provisioning; caller supplies actual inputs."""
    return raw_api.create_owner(durability_port=create_sqlite_persistence(str(path), create=True))


def predecessor_configuration(
    reader,
    path,
    *,
    create=True,
    now=None,
    versions=(1,),
    identities=("D011", "D012"),
    brief=PREDECESSOR_BRIEF,
):
    return dict(
        admission=f.OwnerAdmissionV1("M02", brief),
        raw_projection_reader=reader,
        definitions=tuple(
            f.CalculationDefinitionV1(
                identity,
                f"{identity}-{'SPREAD' if identity == 'D012' else 'MIDPOINT'}-{v}",
                "K02_ALGEBRA",
                "R035 - R034" if identity == "D012" else "(R034 + R035) / 2",
                ("R034", "R035"),
                (),
                "P_BASIC",
                "price",
                "scalar_decimal",
                tuple(f.AuthorityArtifactRefV1(*ref) for ref in AUTHORITY),
            )
            for identity in identities
            for v in versions
        ),
        parameter_sets=tuple(
            f.CalculationParameterSetV1("mmt-pilot-basic", v, "P_BASIC", "NVDA", ("NVDA",))
            for v in versions
        ),
        input_selection_policies=tuple(
            f.InputSelectionPolicyVersionV1(
                "mmt-pilot-selection",
                v,
                ("subject_instrument",),
                timedelta(seconds=60),
                timedelta(seconds=10),
                ("true_instant",),
                (),
                PROVIDER,
                "cash_quote_v1",
                SCOPE,
                100,
                1000,
            )
            for v in versions
        ),
        unit_conventions=tuple(
            f.UnitConventionVersionV1(
                "mmt-pilot-price", v, "price", "price", Decimal("1"), Decimal("0")
            )
            for v in versions
        ),
        raw_projection_mappings=tuple(
            mapping(side, v) for v in versions for side in ("bid", "ask")
        ),
        storage=f.SQLiteStorageV1(str(path), create),
        utc_now=(lambda: NOW) if now is None else now,
    )


def predecessor_request(version=1, *, identity="D012", **changes):
    label = "SPREAD" if identity == "D012" else "MIDPOINT"
    values = dict(
        derived_signal_id=identity,
        subject_instrument="NVDA",
        as_of_utc=ASOF,
        knowledge_cutoff_utc=ASOF,
        calculation_definition_version=f"{identity}-{label}-{version}",
        parameter_set_ref=f.VersionRefV1("mmt-pilot-basic", version),
        input_selection_policy_ref=f.VersionRefV1("mmt-pilot-selection", version),
        context_refs=(),
        raw_input_bindings=tuple(
            f.RawInputBindingV1(
                "R034" if side == "bid" else "R035",
                f.VersionRefV1("mmt-pilot-" + side, version),
                f.VersionRefV1("mmt-pilot-price", version),
                "NVDA",
            )
            for side in ("bid", "ask")
        ),
    )
    return f.CalculationRequestV1(**(values | changes))


BRIEF = "1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148"


def ratio_configuration(reader, path, *, create=True, versions=(1, 2), now=None):
    """Literal configuration only: no predecessor reads, production or expected answer."""
    return dict(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        predecessor_reader=reader,
        definitions=tuple(
            f.CalculationDefinitionV1(
                "D013",
                f"D013-RELATIVE-SPREAD-{v}",
                "K02_ALGEBRA",
                "100 * D012 / D011",
                (),
                ("D011", "D012"),
                "P_BASIC",
                "percent",
                "scalar_exact_ratio",
                tuple(f.AuthorityArtifactRefV1(*ref) for ref in AUTHORITY),
            )
            for v in versions
        ),
        parameter_sets=tuple(
            f.CalculationParameterSetV1("mmt-pilot-basic", v, "P_BASIC", "NVDA", ("NVDA",))
            for v in versions
        ),
        storage=f.SQLiteStorageV1(str(path), create),
        utc_now=(lambda: NOW) if now is None else now,
    )


def ratio_request(midpoint_id, spread_id, **changes):
    values = dict(
        derived_signal_id="D013",
        subject_instrument="NVDA",
        as_of_utc=ASOF,
        knowledge_cutoff_utc=ASOF,
        calculation_definition_version="D013-RELATIVE-SPREAD-1",
        parameter_set_ref=f.VersionRefV1("mmt-pilot-basic", 1),
        predecessor_occurrence_ids=(midpoint_id, spread_id),
    )
    return f.RatioCalculationRequestV1(**(values | changes))
