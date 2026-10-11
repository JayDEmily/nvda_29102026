"""Authority-derived, provider-independent official OI proofs at the actual M00->M01 seam.

These controlled source fields are test-contract fields mapped through admitted M00;
they make NO representation about IBKR, OCC or live reporting-period mappings.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 11, 12, tzinfo=UTC)
PERIOD_KEYS = (
    "official_reporting_period_id",
    "official_reporting_period_order",
    "official_revision_id",
    "official_revision_precedence",
)


@dataclass(frozen=True)
class OI:
    oid: str
    period: str | None
    order: int | None
    revision: str | None
    precedence: int | None
    value: int
    right: str = "call"
    contract: str = "C150"
    event_days: int = 1
    receipt_seconds: int = 10
    version: int = 1
    source: str = "controlled-official-oi"


BASE = (
    OI("prior", "2026-10-09", 1, "first", 1, 100, event_days=2, receipt_seconds=100),
    OI("current", "2026-10-10", 2, "first", 1, 125, event_days=1, receipt_seconds=50),
)


def _identity(contract: str, right: str) -> raw.RawSelectionIdentityV1:
    return raw.RawSelectionIdentityV1(
        (
            ("contract_id", contract),
            ("underlying_instrument", "NVDA"),
            ("expiry", "2026-12-18"),
            ("strike", Decimal(150)),
            ("option_right", right),
        )
    )


def _public(
    records: tuple[OI, ...] = BASE,
    *,
    right: str = "call",
    cutoff: datetime = NOW,
    mapping_version: int = 1,
    bind_opposite: bool = False,
    persistence: object | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for i, rec in enumerate(records, 1):
        selection = dict(_identity(rec.contract, rec.right).values)
        period_values = (rec.period, rec.order, rec.revision, rec.precedence)
        for key, value in zip(PERIOD_KEYS, period_values, strict=True):
            if value is not None:
                selection[key] = value
        event = NOW - timedelta(days=rec.event_days)
        rid = "R047" if rec.right == "call" else "R048"
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("controlled-" + rec.oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("controlled-" + rec.oid),
                source_provider=raw.provider_id(rec.source),
                native_record={"quantity": Decimal(rec.value), "identity": selection},
                received_ts_utc=NOW - timedelta(seconds=rec.receipt_seconds),
                ingestion_sequence=i,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled:official-oi"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=event.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="controlled-periods",
                subject_instrument="NVDA",
                native_units="contracts",
                revision_vintage_native=f"opaque-{rec.version}",
            )
        )
    chosen = _identity("C150" if right == "call" else "P150", right)
    # All controlled source fields are explicitly M00-mapped identities; they
    # are not inferred from receipt, event timestamp or native-vintage strings.
    fields = tuple((key, ("identity", key)) for key, _ in chosen.values)
    fields += tuple((key, ("identity", key)) for key in PERIOD_KEYS)
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            f"controlled-map-{rid}",
            mapping_version,
            raw.RawSignalCatalogueId(rid),
            "controlled-official-oi",
            "controlled-periods",
            ("quantity",),
            "contracts",
            fields,
        )
        for rid in ("R047", "R048")
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "controlled-d123", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "controlled-option",
                1,
                tuple(key for key, _ in chosen.values),
                timedelta(days=5),
                timedelta(days=5),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "controlled-contracts", 1, "contracts", "contracts", Decimal(1), Decimal(0)
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
        **({"persistence": persistence} if persistence is not None else {}),
    )
    bindings = [
        api.RawInputBindingV1(
            "R047" if right == "call" else "R048",
            api.VersionRefV1(
                "controlled-map-" + ("R047" if right == "call" else "R048"), mapping_version
            ),
            api.VersionRefV1("controlled-contracts", 1),
            "NVDA",
            chosen,
        )
    ]
    if bind_opposite:
        opposite = "put" if right == "call" else "call"
        rid = "R048" if right == "call" else "R047"
        bindings.append(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("controlled-map-" + rid, mapping_version),
                api.VersionRefV1("controlled-contracts", 1),
                "NVDA",
                _identity("P150" if opposite == "put" else "C150", opposite),
            )
        )
    request = api.CalculationRequestV1(
        "D123",
        "NVDA",
        NOW,
        cutoff,
        "D123-20261011-01",
        "controlled-d123",
        1,
        "controlled-option",
        1,
        (),
        raw_input_bindings=tuple(bindings),
    )
    return owner, request


@pytest.mark.parametrize("right,contract", (("call", "C150"), ("put", "P150")))
def test_d123_exact_right_and_only_two_persisted_sources(right: str, contract: str) -> None:
    records = tuple(replace(r, right=right, contract=contract) for r in BASE)
    opposite = OI(
        "opposite",
        "2026-10-10",
        2,
        "first",
        1,
        999,
        right="put" if right == "call" else "call",
        contract="P150" if right == "call" else "C150",
    )
    decoy = OI(
        "other-strike-contract",
        "2026-10-10",
        2,
        "first",
        1,
        999,
        right=right,
        contract="C151" if right == "call" else "P151",
    )
    for included_opposite in (False, True):
        owner, req = _public(
            records + (decoy,) + ((opposite,) if included_opposite else ()), right=right
        )
        result = owner.materialise(req)
        assert result is not None and result.result == Decimal(25)
        assert result.selection_identity == _identity(contract, right)
        assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {
            "controlled-prior",
            "controlled-current",
        }
        assert {x.raw_signal_id for x in result.raw_input_lineage} == {
            "R047" if right == "call" else "R048",
        }
        assert owner.materialise(req) == result


def test_d123_explicit_revision_precedence_out_of_arrival_order_and_cutoff() -> None:
    # Prior period corrected later in *receipt order* than the newer reporting
    # period: latest two ticks differ from latest two official periods.
    correction = OI(
        "revision", "2026-10-09", 1, "correction", 2, 110, event_days=2, receipt_seconds=5
    )
    owner, req = _public((*BASE, correction))
    final = owner.materialise(req)
    assert final is not None and final.result == Decimal(15)
    assert {x.observation_occurrence_id for x in final.raw_input_lineage} == {
        "controlled-revision",
        "controlled-current",
    }
    owner_cut, req_cut = _public((*BASE, correction), cutoff=NOW - timedelta(seconds=20))
    historical = owner_cut.materialise(req_cut)
    assert historical is not None and historical.result == Decimal(25)
    assert {x.observation_occurrence_id for x in historical.raw_input_lineage} == {
        "controlled-prior",
        "controlled-current",
    }


@pytest.mark.parametrize(
    "records",
    (
        BASE[:1],
        (replace(BASE[0], period=None), BASE[1]),
        (replace(BASE[0], order=None), BASE[1]),
        (replace(BASE[0], revision=None), BASE[1]),
        (replace(BASE[0], precedence=None), BASE[1]),
        (BASE[0], replace(BASE[1], order=1)),
        (BASE[0], replace(BASE[1], period="2026-10-09")),
        (BASE[0], replace(BASE[1], precedence=0)),
        (
            BASE[0],
            replace(BASE[1], revision="first", precedence=2),
            replace(BASE[1], oid="ambiguous", revision="other", precedence=2),
        ),
        (BASE[0], BASE[1], replace(BASE[0], oid="conflicting-period-order", order=3)),
    ),
)
def test_d123_refuses_missing_ambiguous_or_incompatible_history(records: tuple[OI, ...]) -> None:
    owner, req = _public(records)
    assert owner.materialise(req) is None


def test_d123_refuses_future_knowledge_missing_applicable_and_wrong_right() -> None:
    owner, req = _public(BASE, cutoff=NOW - timedelta(seconds=75))
    assert owner.materialise(req) is None
    wrong = tuple(replace(rec, right="put", contract="P150") for rec in BASE)
    owner, req = _public(wrong, right="call")
    assert owner.materialise(req) is None
    owner, req = _public(BASE, mapping_version=2)
    # Different mapping version is valid if consistently declared; a request
    # pointing at an unregistered version must fail separately.
    assert owner.materialise(req) is not None
    from dataclasses import replace as dc_replace

    broken = dc_replace(
        req,
        raw_input_bindings=(
            dc_replace(
                req.raw_input_bindings[0],
                projection_mapping_ref=api.VersionRefV1("controlled-map-R047", 1),
            ),
        ),
    )
    assert owner.materialise(broken) is None
