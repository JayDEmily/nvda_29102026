"""D175 account subjects stay account subjects through the admitted M00 seam."""

from datetime import timedelta
from decimal import Decimal

import pytest
from tests.product.derived_signal.test_m01_f4_approved_monetary_policy import NOW, fixture

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw


@pytest.mark.parametrize("account_subject,expected_reads", [("account-subject", 4), ("OTHER", 0)])
def test_d175_public_account_projection_preserves_subject_and_refuses_wrong_scope(
    account_subject, expected_reads, monkeypatch
):
    f = fixture()
    m00 = raw.create_owner()
    ids = ("R205", "R206", "R209", "R208")
    mapping = []
    for sequence, identity in enumerate(ids, 1):
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(identity + "-account"),
                delivery_artifact_ref=raw.delivery_artifact_ref(identity + "-delivery"),
                source_provider=raw.provider_id("controlled-account"),
                native_record={
                    "value": f["raw"][identity][0].value,
                    "account_identity": "account",
                    "currency": "USD",
                },
                received_ts_utc=NOW,
                ingestion_sequence=sequence,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("account-fixture"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=NOW.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(identity),),
                subject_instrument=account_subject,
                native_units="USD",
                revision_vintage_native="1",
            )
        )
        mapping.append(
            raw.RawSignalProjectionMappingV1(
                "map-" + identity,
                1,
                raw.RawSignalCatalogueId(identity),
                "controlled-account",
                None,
                ("value",),
                "USD",
                selection_identity_field_paths=(
                    ("account_identity", ("account_identity",)),
                    ("currency", ("currency",)),
                ),
            )
        )
    reads = []
    predecessor_reads = []
    original_history = api._OwnerV1._compatible_history

    def history_spy(self, **kwargs):
        predecessor_reads.append(kwargs["derived_signal_id"])
        return original_history(self, **kwargs)

    monkeypatch.setattr(api._OwnerV1, "_compatible_history", history_spy)

    class Reader:
        def list_projected_raw_history(self, *args, **kwargs):
            reads.append(kwargs["subject_instrument"])
            return m00.reads.list_projected_raw_history(*args, **kwargs)

    owner = api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=tuple(mapping),
        parameter_sets=(
            api.CalculationParameterSetV1("tail-producer", 1, "P_UTILITY", (("rule", "tail"),)),
            api.CalculationParameterSetV1("policy", 1, "P_RULE", tuple(f["params"].items())),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "selection",
                1,
                ("subject_instrument",),
                timedelta(seconds=5),
                timedelta(seconds=5),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1("usd", 1, "USD", "USD", Decimal(1), Decimal(0)),
        ),
        contexts=f["contexts"],
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D175",
        "NVDA",
        NOW,
        NOW,
        "account-proof",
        "policy",
        1,
        "selection",
        1,
        tuple(api.VersionRefV1(c.context_id, c.version) for c in f["contexts"]),
        parameter_profile_refs=(api.ParameterProfileRefV1("P_UTILITY", "tail-producer", 1),),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                identity,
                api.VersionRefV1("map-" + identity, 1),
                api.VersionRefV1("usd", 1),
                account_subject,
                api.RawSelectionIdentityV1((("account_identity", "account"), ("currency", "USD"))),
            )
            for identity in ids
        ),
    )
    assert owner.materialise(request) is None  # D162/D174 Stage-2 production remains absent.
    assert predecessor_reads == (["D162"] if expected_reads else [])
    assert len(reads) == expected_reads
    assert all(subject == "account-subject" for subject in reads)
