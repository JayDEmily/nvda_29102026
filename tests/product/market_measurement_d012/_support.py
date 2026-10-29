"""Authority literals and store/child provisioning only; callers order operations."""

import base64
import os
import pickle
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw_api
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

ROOT = Path(__file__).resolve().parents[3]
BRIEF = "a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393"
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


def configuration(
    reader, path, *, create=True, now=None, versions=(1,), identities=("D012",), brief=BRIEF
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


def request(version=1, *, identity="D012", **changes):
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


def history(reads, identity="D012"):
    return reads.list_derived_history(
        derived_signal_id=identity,
        subject_instrument="NVDA",
        effective_at_or_before_utc=ASOF,
        knowledge_at_or_before_utc=NOW,
        limit=1000,
    )


def child_env(source=None):
    return dict(
        os.environ,
        PYTHONPATH=os.pathsep.join(
            [str((ROOT if source is None else source) / "src"), str(Path(__file__).parent)]
        ),
    )


def fresh_bundle(path, identity, *, brief=BRIEF):
    # Child receives no expected value, configuration, calculator or raw reader.
    code = """
import base64,pickle,sys
from nvda_desk.market_measurement_truth import api as f
r=f.create_reader(admission=f.OwnerAdmissionV1('M02',sys.argv[3]),
    storage=f.SQLiteReadStorageV1(sys.argv[1]))
o=r.get_derived_occurrence(sys.argv[2])
value={'occurrence':o}
if o is not None:
    value.update(definition=r.get_calculation_definition(derived_signal_id=o.derived_signal_id,
        calculation_definition_version=o.calculation_definition_version),
        parameter=r.get_parameter_set(o.parameter_context_refs[0]),
        selection=r.get_input_selection_policy(o.parameter_context_refs[1]),
        units=tuple(r.get_unit_convention(x) for x in o.convention_refs),
        mappings=tuple(r.get_projection_mapping(x.projection_mapping_ref)
            for x in o.raw_input_lineage),
        history=r.list_derived_history(derived_signal_id=o.derived_signal_id,subject_instrument='NVDA',
            effective_at_or_before_utc=o.effective_as_of_utc,
            knowledge_at_or_before_utc=o.knowledge_cutoff_utc,limit=100))
print(base64.b64encode(pickle.dumps(value)).decode())
"""
    p = subprocess.run(
        [sys.executable, "-c", code, str(path), identity, brief],
        env=child_env(),
        text=True,
        capture_output=True,
        timeout=20,
    )
    assert p.returncode == 0, p.stderr
    return pickle.loads(base64.b64decode(p.stdout))
