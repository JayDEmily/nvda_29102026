"""D077: two actual semiconductor proxies minus actual QQQ, with no fallback."""

import json
from copy import deepcopy
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "f98aabd7e7bdd479ed0c3cbf5720d6c13887c1b2d9f707e8f85548b547bc6076"
# The admitted source profile is read as data; fixed assertions below independently
# distinguish the two semiconductor proxies and the market reference.
PROFILE = json.loads(
    (
        Path(__file__).resolve().parents[3]
        / "handoff/foundation_implementation/authority/D077_PROFILE.json"
    ).read_text()
)
PARENTS = {
    identity: {
        "brief": PROFILE["parents"][identity]["brief_sha256"],
        "records": PROFILE["parents"][identity]["profile"]["records"],
        "subject": PROFILE["parents"][identity]["profile"]["subject"],
        "expected": PROFILE["parents"][identity]["profile"]["expected_50digit_half_even"],
    }
    for identity in ("D073", "D074", "D072")
}
assert tuple(PARENTS[x]["subject"] for x in PARENTS) == ("SMH", "SOXX", "QQQ")
assert tuple(PARENTS[x]["records"][0][4]["trade"]["last"] for x in PARENTS) == ("55", "50", "90")

MAP_SPECS = [
    [
        "R037",
        "mmt-r037-underlying",
        ["trade", "last"],
        "price",
        [
            ["instrument.id", ["instrument", "id"]],
            ["session.id", ["session", "id"]],
            ["adjustment.basis", ["adjustment", "basis"]],
            ["price.kind", ["price", "kind"]],
        ],
    ],
    [
        "R042",
        "mmt-r042-underlying",
        ["official_close", "value"],
        "price",
        [
            ["instrument.id", ["instrument", "id"]],
            ["session.id", ["session", "id"]],
            ["adjustment.basis", ["adjustment", "basis"]],
            ["price.kind", ["price", "kind"]],
        ],
    ],
]


def dt(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


T, REFERENCE, START, END = map(
    dt,
    (
        "2026-10-20T12:40:00Z",
        "2026-10-19T13:00:00Z",
        "2026-10-19T12:00:00Z",
        "2026-10-20T13:00:00Z",
    ),
)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=3)
CONTEXT = f.WindowContextV1(f.VersionRefV1("controlled-underlying-session", 1), START, END, START)
PROVIDER, VARIANT = "foundation-controlled-underlying", "last_prior_close_v1"
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        mid,
        1,
        r.RawSignalCatalogueId(rid),
        PROVIDER,
        VARIANT,
        tuple(path),
        unit,
        tuple((k, tuple(v)) for k, v in meta),
    )
    for rid, mid, path, unit, meta in MAP_SPECS
)
UNIT = f.UnitConventionVersionV1(
    "mmt-underlying-price", 1, "price", "price", Decimal("1"), Decimal("0")
)
AUTHORITY = (
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
    ),
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
    ),
)
EXPECTED_RATIO = (
    264587381217093609132624587634612596103723598411597,
    1000000000000000000000000000000000000000000000000000,
)


def selection(identity, basket=()):
    return f.InputSelectionPolicyVersionV1(
        "mmt-" + identity.lower() + "-selection",
        1,
        ("as_of_utc", "knowledge_cutoff_utc", "context", "return_convention")
        if basket
        else ("subject_instrument", "instrument.id", "session.id"),
        timedelta(days=1),
        timedelta(0),
        ("true_instant",),
        basket,
        PROVIDER,
        VARIANT,
        PROVIDER + "/" + VARIANT,
        100,
        1000,
    )


DEFINITION = f.CalculationDefinitionV1(
    "D077",
    "D077-RELATIVE-RETURN-1",
    "K02_ALGEBRA",
    "(D073+D074)/2-D072",
    (),
    ("D073", "D074", "D072"),
    "P_BASIC",
    "return_spread",
    "exact_ratio",
    AUTHORITY,
)
PARAM = f.CalculationParameterSetV1(
    "mmt-d077-controlled", 1, "P_BASIC", "SEMIS_VS_TECH", ("SMH", "SOXX", "QQQ")
)
POLICY = selection("D077", ("SMH", "SOXX", "QQQ"))


class PublicParents:
    def __init__(self, readers):
        self.readers = readers

    def get_derived_occurrence(self, identity):
        for reader in self.readers:
            value = reader.get_derived_occurrence(identity)
            if value is not None:
                return value
        return None

    def list_derived_history(self, **kwargs):
        return tuple(
            value for reader in self.readers for value in reader.list_derived_history(**kwargs)
        )


@pytest.mark.parametrize("refused", [False, True], ids=["success", "refusal"])
def test_d077_signal(tmp_path, refused):
    raw = r.create_owner()
    facts, readers = [], []
    # Genuine public predecessor production is setup, not execution/import of old acceptance tests.
    for identity in (("D073", "D072") if refused else ("D073", "D074", "D072")):
        spec = PARENTS[identity]
        subject = spec["subject"]
        cutoff = CUTOFF
        records = deepcopy(spec["records"])
        projected = []
        for index, (role, instrument, event, receipt, native) in enumerate(records):
            mapping = MAPS[role]
            value = native
            for part in mapping.native_field_path[:-1]:
                value = value[part]
            value[mapping.native_field_path[-1]] = Decimal(value[mapping.native_field_path[-1]])
            observation_id = "d077-" + identity.lower() + "-" + str(index)
            raw.commands.admit_raw_observation_occurrence(
                r.RawObservationOccurrenceV1(
                    concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=r.observation_occurrence_id(observation_id),
                    delivery_artifact_ref=r.delivery_artifact_ref("d077-controlled"),
                    source_provider=r.provider_id(PROVIDER),
                    native_record=native,
                    received_ts_utc=dt(receipt),
                    ingestion_sequence=len(facts) * 2 + index + 1,
                    ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                    source_temporal_kind="true_instant",
                    raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
                    source_variant=VARIANT,
                    subject_instrument=instrument,
                    native_units="price",
                    source_timestamp_raw=event,
                    source_timezone_native="UTC",
                )
            )
            page = raw.reads.list_projected_raw_history(
                mapping.raw_signal_catalogue_id,
                mappings=(mapping,),
                subject_instrument=subject,
                received_at_or_before_utc=cutoff,
                event_at_or_before_utc=T,
                limit=100,
                cursor=None,
            )
            assert page.next_cursor is None and len(page.items) == 1
            item = page.items[0]
            assert item.observation_occurrence_id.value == observation_id
            assert item.subject_instrument == instrument == subject
            assert item.received_ts_utc == dt(receipt) and item.source_timestamp_raw == event
            assert item.selection_identity == r.RawSelectionIdentityV1(
                (
                    ("instrument.id", subject),
                    (
                        "session.id",
                        "controlled-20oct12-13Z" if role == 0 else "controlled-19oct12-13Z",
                    ),
                    ("adjustment.basis", "controlled_unadjusted/1"),
                    ("price.kind", "current_last" if role == 0 else "official_close"),
                )
            )
            assert item.native_value == value[mapping.native_field_path[-1]]
            projected.append(item)
        definition = f.CalculationDefinitionV1(
            identity,
            identity + "-LOG-RETURN-1",
            "K03_CHANGE_RETURN",
            "ln(current/reference)",
            ("R037", "R042"),
            (),
            "P_WINDOW",
            "return",
            "scalar_decimal",
            AUTHORITY,
        )
        parameter = f.CalculationParameterSetV1(
            "mmt-" + identity.lower() + "-controlled", 1, "P_WINDOW", subject, (subject,)
        )
        policy = selection(identity)
        request = f.WindowCalculationRequestV1(
            f.CalculationRequestV1(
                identity,
                subject,
                T,
                cutoff,
                definition.calculation_definition_version,
                f.VersionRefV1(parameter.context_id, 1),
                f.VersionRefV1(policy.context_id, 1),
                (CONTEXT.ref,),
                tuple(
                    f.RawInputBindingV1(
                        m.raw_signal_catalogue_id.value,
                        f.VersionRefV1(m.mapping_id, 1),
                        f.VersionRefV1(UNIT.context_id, 1),
                        subject,
                    )
                    for m in MAPS
                ),
            ),
            CONTEXT,
            (),
        )
        admission = f.OwnerAdmissionV1("M02", spec["brief"])
        path = str(tmp_path / (identity + ".sqlite"))
        producer = f.create_window_owner(
            admission=admission,
            raw_projection_reader=raw.reads,
            storage=f.SQLiteStorageV1(path, True),
            utc_now=lambda: NOW,
        )
        actual = producer.materialise(request)
        assert type(actual) is f.WindowMeasurementOccurrenceV1
        assert (
            type(actual.result) is Decimal
            and actual.result.as_tuple() == Decimal(spec["expected"]).as_tuple()
        )
        assert actual.request == request and actual.definition == definition
        assert actual.parameter_set == parameter and actual.input_selection_policy == policy
        assert (
            actual.implementation_brief_sha256 == spec["brief"] and actual.owner_object_id == "M02"
        )
        assert actual.owner_namespace == "neutral_market_measurement_truth/window/v1"
        assert actual.projection_mappings == MAPS and actual.unit_conventions == (UNIT,)
        assert actual.predecessors == () and actual.window_seconds == 85200
        assert actual.raw_input_lineage == tuple(
            f.RawInputLineageV1(
                MAPS[role].raw_signal_catalogue_id.value,
                item.observation_occurrence_id.value,
                f.VersionRefV1(MAPS[role].mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1),
                item,
                item.native_value,
                T if role == 0 else REFERENCE,
            )
            for role, item in enumerate(projected)
        )
        assert (
            actual.effective_as_of_utc,
            actual.knowledge_cutoff_utc,
            actual.calculated_at_utc,
        ) == (T, cutoff, NOW)
        assert actual.units == "return" and actual.result_shape == "scalar_decimal"
        reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
        actual = reader.get_derived_occurrence(actual.derived_occurrence_id)
        assert actual == producer.reads.get_derived_occurrence(actual.derived_occurrence_id)
        facts.append(actual)
        readers.append(reader)
    expected_ids = ("D073", "D072") if refused else ("D073", "D074", "D072")
    assert tuple(p.derived_signal_id for p in facts) == expected_ids
    assert all(p.knowledge_cutoff_utc == CUTOFF for p in facts)
    assert all(p.request.context == CONTEXT for p in facts)
    # Every supplied predecessor is lawful; SOXX is absent only in the refusal.
    predecessors = PublicParents(readers)
    assert tuple(
        predecessors.get_derived_occurrence(p.derived_occurrence_id) for p in facts
    ) == tuple(facts)
    missing_soxx_id = "mmtwindow1:d077-required-d074-absent"
    if refused:
        assert predecessors.get_derived_occurrence(missing_soxx_id) is None
        predecessor_ids = (
            facts[0].derived_occurrence_id,
            missing_soxx_id,
            facts[1].derived_occurrence_id,
        )
    else:
        predecessor_ids = tuple(p.derived_occurrence_id for p in facts)
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D077",
            "SEMIS_VS_TECH",
            T,
            CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAM.context_id, 1),
            f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,),
            (),
        ),
        CONTEXT,
        predecessor_ids,
    )
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "D077.sqlite")
    owner = f.create_window_owner(
        admission=admission,
        raw_projection_reader=raw.reads,
        predecessor_reader=predecessors,
        storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    result = owner.materialise(request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(
        derived_signal_id="D077",
        subject_instrument="SEMIS_VS_TECH",
        effective_at_or_before_utc=T,
        knowledge_at_or_before_utc=CUTOFF,
        limit=10,
    )
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is f.ExactRatioV1 and result.result == f.ExactRatioV1(
        *EXPECTED_RATIO
    )
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAM and result.input_selection_policy == POLICY
    assert result.projection_mappings == result.unit_conventions == result.raw_input_lineage == ()
    assert result.predecessors == tuple(facts) and result.window_seconds == 85200
    assert tuple(line for p in result.predecessors for line in p.raw_input_lineage) == tuple(
        line for p in facts for line in p.raw_input_lineage
    )
    assert (
        result.owner_object_id == "M02"
        and result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    )
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == "D077"
    assert result.units == "return_spread" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        CUTOFF,
        NOW,
    )
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert (
        reader.get_derived_occurrence(result.derived_occurrence_id)
        == owner.reads.get_derived_occurrence(result.derived_occurrence_id)
        == result
    )
    assert reader.list_derived_history(**args) == (result,)
