"""Controlled literals, raw provisioning and child transport; no materialisation flow."""

import base64
import importlib
import importlib.util
import os
import pickle
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

ROOT = Path(__file__).resolve().parents[3]
BRIEF = "3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233"
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


def foundation():
    assert importlib.util.find_spec("nvda_desk.market_measurement_truth") is not None, (
        "accepted foundation public seam is missing"
    )
    return importlib.import_module("nvda_desk.market_measurement_truth.api")


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
    side, *, identity=None, value=None, event=None, receipt=None, sequence=None, **changes
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
        received_ts_utc=(ASOF - timedelta(seconds=1 if bid else 0)) if receipt is None else receipt,
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


def configuration(f, reader, *, storage=None, now=None, versions=(1,)):
    """Literal constructor arguments only: caller explicitly registers/materialises/reads."""
    refs = tuple(f.AuthorityArtifactRefV1(*item) for item in AUTHORITY)
    return dict(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        raw_projection_reader=reader,
        definitions=tuple(
            f.CalculationDefinitionV1(
                "D011",
                f"D011-MIDPOINT-{v}",
                "K02_ALGEBRA",
                "(R034 + R035) / 2",
                ("R034", "R035"),
                (),
                "P_BASIC",
                "price",
                "scalar_decimal",
                refs,
            )
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
        storage=f.MemoryStorageV1() if storage is None else storage,
        utc_now=(lambda: NOW) if now is None else now,
    )


def request(f, version=1, **changes):
    values = dict(
        derived_signal_id="D011",
        subject_instrument="NVDA",
        as_of_utc=ASOF,
        knowledge_cutoff_utc=ASOF,
        calculation_definition_version=f"D011-MIDPOINT-{version}",
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


def process_env():
    return dict(os.environ, PYTHONPATH=str(Path(__file__).parent))


def fresh_read(path, identity):
    return fresh_bundle(path, identity)["occurrence"]


def fresh_bundle(path, identity):
    # Expected content/configuration/raw reader are deliberately not sent to the child.
    code = """
import base64,pickle,sys
from nvda_desk.market_measurement_truth import api as f
r=f.create_reader(admission=f.OwnerAdmissionV1("M02",sys.argv[3]),
    storage=f.SQLiteReadStorageV1(sys.argv[1]))
occurrence=r.get_derived_occurrence(sys.argv[2])
value={"occurrence":occurrence}
if occurrence is not None:
    value.update(
        definition=r.get_calculation_definition(derived_signal_id=occurrence.derived_signal_id,
            calculation_definition_version=occurrence.calculation_definition_version),
        parameter=r.get_parameter_set(occurrence.parameter_context_refs[0]),
        selection=r.get_input_selection_policy(occurrence.parameter_context_refs[1]),
        units=tuple(r.get_unit_convention(ref) for ref in occurrence.convention_refs),
        mappings=tuple(r.get_projection_mapping(item.projection_mapping_ref)
            for item in occurrence.raw_input_lineage),
        history=r.list_derived_history(derived_signal_id=occurrence.derived_signal_id,
            subject_instrument=occurrence.subject_instrument,
            effective_at_or_before_utc=occurrence.effective_as_of_utc,
            knowledge_at_or_before_utc=occurrence.knowledge_cutoff_utc,limit=100))
print(base64.b64encode(pickle.dumps(value)).decode("ascii"))
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(path), identity, BRIEF],
        env=process_env(),
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    return pickle.loads(base64.b64decode(result.stdout))
