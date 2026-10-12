"""Programme-owner 2026-10-12 D104: 10delta-minus-25delta change of changes.

Source-derived mandatory pair/history and exact-lineage proof. No live-provider claims.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import _stage1, api
from nvda_desk.raw_signal_occurrence_truth import api as raw

AT = datetime(2026, 10, 12, 4, tzinfo=UTC)
PRIOR = AT - timedelta(minutes=1)
EXPIRY = "2026-12-18"
CONTRACTS = (
    ("C25", "call", Decimal(155), Decimal("0.25")),
    ("P25", "put", Decimal(145), Decimal("-0.25")),
    ("C10", "call", Decimal(165), Decimal("0.10")),
    ("P10", "put", Decimal(135), Decimal("-0.10")),
)
KEYS = ("contract_id", "underlying_instrument", "expiry", "strike", "option_right")
KEY_PATHS = tuple((key, ("identity", key)) for key in KEYS)


def _kv(
    family: str,
    value: int,
    phase: str,
    *,
    expiry: str = EXPIRY,
    subject: str = "NVDA",
    stamp: datetime | None = None,
) -> _stage1.KernelValueV1:
    return _stage1.KernelValueV1(
        value=Decimal(value),
        occurrence_id=f"{family}:{phase}",
        effective_at_utc=stamp or (AT if phase == "current" else PRIOR),
        received_ts_utc=stamp or (AT if phase == "current" else PRIOR),
        subject_instrument=subject,
        source_temporal_kind="derived",
        metadata=(("underlying_instrument", subject), ("expiry", expiry)),
    )


def _kernel(values99=(10, 20), values100=(30, 40), **override: object):
    history = {
        "D099": tuple(
            _kv("D099", val, stage)
            for stage, val in zip(("prior", "current"), values99, strict=True)
        ),
        "D100": tuple(
            _kv("D100", val, stage)
            for stage, val in zip(("prior", "current"), values100, strict=True)
        ),
    }
    history.update(override)
    return _stage1.evaluate_stage1_kernel(
        "D104",
        raw_inputs={},
        derived_inputs=history,
        parameter_set=api.CalculationParameterSetV1(
            "d104", 1, "P_WINDOW", (("anchor_seconds", 60),)
        ),
        contexts=(),
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )


@pytest.mark.parametrize(
    "values99,values100,expected",
    [
        ((10, 20), (30, 40), Decimal(0)),
        ((10, 20), (30, 50), Decimal(10)),
        ((10, 20), (30, 35), Decimal(-5)),
        ((10, 20), (30, 25), Decimal(-15)),
    ],
)
def test_authorised_difference_of_differences(values99, values100, expected):
    value = _kernel(values99, values100)
    assert value is not None and value.value == expected
    assert len(value.input_occurrence_ids) == 4


def test_absent_family_or_prior_or_late_anchor_refuses():
    assert _kernel(D100=()) is None
    assert _kernel(D099=(_kv("D099", 20, "current"),)) is None
    assert (
        _kernel(
            D100=(
                _kv("D100", 30, "prior", stamp=AT - timedelta(seconds=40)),
                _kv("D100", 40, "current"),
            )
        )
        is None
    )


@pytest.mark.parametrize("family", ["D099", "D100"])
def test_mismatched_expiry_refuses(family):
    original = (_kv(family, 10, "prior"), _kv(family, 20, "current", expiry="2027-01-15"))
    assert _kernel(**{family: original}) is None


def _controlled_public(
    *, missing: str | None = None, wrong_expiry: str | None = None, future: str | None = None
):
    m00 = raw.create_owner()
    bindings = []
    seq = 0
    for moment, tag in ((PRIOR, "prior"), (AT, "current")):
        for cid, right, strike, delta in CONTRACTS:
            # D099 10 -> 20; D100 30 -> 40.  All point IV values are fractions.
            iv = (
                Decimal("0.30")
                if cid == "C25"
                else (Decimal("0.40") if tag == "prior" else Decimal("0.50"))
                if cid == "P25"
                else Decimal("0.20")
                if cid == "C10"
                else (Decimal("0.50") if tag == "prior" else Decimal("0.60"))
            )
            identity = raw.RawSelectionIdentityV1(
                (
                    ("contract_id", cid),
                    ("underlying_instrument", "NVDA"),
                    ("expiry", "2027-01-15" if cid == wrong_expiry else EXPIRY),
                    ("strike", strike),
                    ("option_right", right),
                )
            )
            for rid, val in (("R111", iv), ("R112", delta), ("R015", strike)):
                if tag == "prior" and f"{cid}-{rid}" == missing:
                    continue
                seq += 1
                key = f"d104-{tag}-{cid}-{rid}"
                m00.commands.admit_raw_observation_occurrence(
                    raw.RawObservationOccurrenceV1(
                        concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                        contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                        observation_occurrence_id=raw.observation_occurrence_id(key),
                        delivery_artifact_ref=raw.delivery_artifact_ref(key),
                        source_provider=raw.provider_id("controlled-d104"),
                        native_record={"metric": {rid: val}, "identity": dict(identity.values)},
                        received_ts_utc=AT + timedelta(seconds=1) if key == future else moment,
                        ingestion_sequence=seq,
                        ingestion_sequence_scope=raw.ingestion_sequence_scope("f4:d104"),
                        source_temporal_kind="true_instant",
                        source_timestamp_raw=moment.isoformat(),
                        source_timezone_native="UTC",
                        raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                        source_variant="surface-point",
                        subject_instrument="NVDA",
                        native_units="canonical",
                        revision_vintage_native="v1",
                    )
                )
                bind = api.RawInputBindingV1(
                    rid,
                    api.VersionRefV1("d104-map-" + rid, 1),
                    api.VersionRefV1("d104-unit", 1),
                    "NVDA",
                    identity,
                )
                if bind not in bindings:
                    bindings.append(bind)
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "d104-map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-d104",
                "surface-point",
                ("metric", rid),
                "canonical",
                KEY_PATHS,
            )
            for rid in ("R111", "R112", "R015")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "d104-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
            ),
            api.CalculationParameterSetV1("d104-window", 1, "P_WINDOW", (("anchor_seconds", 60),)),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "d104-exact-expiry",
                1,
                ("underlying_instrument", "expiry"),
                timedelta(minutes=5),
                timedelta(minutes=5),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "d104-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0)
            ),
        ),
        contexts=(),
        utc_now=lambda: AT + timedelta(seconds=2),
    )
    request = api.CalculationRequestV1(
        "D104",
        "NVDA",
        AT,
        AT,
        "d104-authorised",
        "d104-window",
        1,
        "d104-exact-expiry",
        1,
        (),
        parameter_profile_refs=(api.ParameterProfileRefV1("P_BASIC", "d104-basic", 1),),
        raw_input_bindings=tuple(bindings),
    )
    return owner, request


def test_public_history_via_m00_then_persisted_exact_lineage():
    owner, request = _controlled_public()
    # Create prior published D099/D100 states through the same admitted M00
    # projections. No manually inserted derived answer is permitted.
    for family in ("D099", "D100"):
        prior_request = replace(
            request,
            derived_signal_id=family,
            as_of_utc=PRIOR,
            knowledge_cutoff_utc=PRIOR,
            parameter_set_id="d104-basic",
            parameter_set_version=1,
        )
        prior = owner.materialise(prior_request)
        assert prior is not None, f"prior {family} not publicly materialised"
    current = owner.materialise(request)
    assert current is not None and current.result == Decimal(0)
    assert len(current.predecessor_occurrence_ids) == 4
    raw_ids = {x.observation_occurrence_id for x in current.raw_input_lineage}
    assert all(x.startswith("d104-") for x in raw_ids)
    assert len(raw_ids) == 24
    assert owner.materialise(request) == current


def test_public_refuses_missing_prior_source():
    owner, request = _controlled_public(missing="P25-R112")
    assert (
        owner.materialise(
            replace(
                request,
                as_of_utc=PRIOR,
                knowledge_cutoff_utc=PRIOR,
                derived_signal_id="D099",
                parameter_set_id="d104-basic",
            )
        )
        is None
    )
    assert owner.materialise(request) is None
