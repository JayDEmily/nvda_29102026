"""F3b proof-before-source: D121/D122 exact signed-flow grouping at public M00/M01 seam.

Accepted K08: D120 signed notional grouped by contract's D091 delta label
and by D085 expiry/DTE; never by equal Dxxx occurrence IDs.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 8, 3, 0, tzinfo=UTC)
CONTRACTS = (
    ("C100", "call", "2026-12-18", Decimal("0.25"), Decimal("6"), Decimal("2")),
    ("P105", "put", "2026-12-25", Decimal("-0.75"), Decimal("4"), Decimal("3")),
)
TRADE_RAW = ("R034", "R035", "R120", "R121", "R126", "R127", "R015")
DATE_RAW = ("R001", "R002", "R003", "R004", "R013", "R023", "R024")
ALL_RAW = (*TRADE_RAW, "R112", *DATE_RAW)
EXACT = ("contract_id", "underlying_instrument", "expiry", "strike", "option_right")


def setup(
    target: str,
    *,
    omit: tuple[str, str] | None = None,
    conflict: tuple[str, str] | None = None,
    extra: tuple[str, str] | None = None,
    cutoff: datetime = NOW,
    wrong_child_version: bool = False,
) -> tuple[Any, api.CalculationRequestV1]:
    points: dict[str, list[raw.ProjectedRawValueV1]] = {rid: [] for rid in ALL_RAW}
    bindings: list[api.RawInputBindingV1] = []
    ids = TRADE_RAW + ("R112",) if target == "D121" else ALL_RAW
    for cid, right, expiry, delta, price, size in CONTRACTS:
        ident = raw.RawSelectionIdentityV1((
            ("contract_id", cid),
            ("underlying_instrument", "NVDA"),
            ("expiry", expiry),
            ("strike", Decimal("100") if cid == "C100" else Decimal("105")),
            ("option_right", right),
        ))
        values: dict[str, object] = {
            "R034": Decimal("4") if cid == "C100" else Decimal("5"),
            "R035": Decimal("6") if cid == "C100" else Decimal("7"),
            "R120": price,
            "R121": size,
            "R126": Decimal("4"),
            "R127": Decimal("6"),
            "R015": Decimal("100"),
            "R112": delta,
            "R001": Decimal("0"),
            "R002": NOW.isoformat(),
            "R003": "UTC",
            "R004": "UTC",
            "R013": expiry,
            "R023": Decimal("0"),
            "R024": Decimal("0"),
        }
        for rid in ids:
            if omit == (cid, rid):
                continue
            selected = ident
            if conflict == (cid, rid):
                selected = raw.RawSelectionIdentityV1(tuple(
                    (k, "wrong-contract" if k == "contract_id" else v) for k, v in ident.values
                ))
            value = values[rid]
            points[rid].append(raw.ProjectedRawValueV1(
                raw_signal_catalogue_id=raw.RawSignalCatalogueId(rid),
                observation_occurrence_id=raw.observation_occurrence_id(
                    f"trade-{cid}" if rid in {"R120", "R121", "R126", "R127", "R015"} else f"{rid}-{cid}"
                ),
                projection_mapping_id=f"map-{rid}", projection_mapping_version=1,
                source_provider="controlled", source_variant="snapshot",
                native_field_path=("field", rid), native_value=value, native_units="number",
                subject_instrument="NVDA", source_temporal_kind="true_instant",
                source_timestamp_raw=NOW.isoformat(), source_timezone_native="UTC",
                received_ts_utc=NOW, ingestion_sequence=100+len(points[rid]),
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled:snapshot"),
                revision_vintage_native="v1", selection_identity=selected,
            ))
            bindings.append(api.RawInputBindingV1(
                rid, api.VersionRefV1(f"map-{rid}",1), api.VersionRefV1("numeric",1),
                "NVDA", selection_identity=selected,
            ))
    if extra:
        # An unexpected bucket input must not be silently omitted.
        cid, rid = extra
        ident = raw.RawSelectionIdentityV1((
            ("contract_id", cid), ("underlying_instrument", "NVDA"),
            ("expiry", "2026-12-18"), ("strike", Decimal("110")),
            ("option_right", "call"),
        ))
        bindings.append(api.RawInputBindingV1(rid, api.VersionRefV1(f"map-{rid}",1), api.VersionRefV1("numeric",1), "NVDA", ident))

    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id: Any, **kwargs: Any) -> Any:
            return raw.ProjectedRawHistoryPageV1(tuple(points.get(raw_signal_catalogue_id.value, ())),None)

        def project_raw_value(self, *args: object, **kwargs: object) -> None:
            return None

    mappings = tuple(raw.RawSignalProjectionMappingV1(
        f"map-{rid}",1, raw.RawSignalCatalogueId(rid),"controlled", "snapshot",("field",rid),"number"
    ) for rid in ids)
    parameters = (
        api.CalculationParameterSetV1("basic",1,"P_BASIC",(("selection_mode", "exact"),)),
        api.CalculationParameterSetV1("time",1,"P_TIME",(("exchange_timezone","UTC"),)),
        api.CalculationParameterSetV1("rule",1,"P_RULE",(
            ("window_seconds",Decimal(60)),
            ("delta_bucket_boundaries",(Decimal("0"),Decimal("0.5"),Decimal("1"))),
            ("delta_bucket_labels",("wing","core")),
            ("dte_bucket_boundaries",(Decimal("0"),Decimal("75"),Decimal("100"))),
            ("dte_bucket_labels",("near","far")),
        )),
    )
    selection = api.InputSelectionPolicyVersionV1(
        "underlying-group",1,("underlying_instrument",),timedelta(days=1),
        timedelta(days=1),("true_instant",),(),
    )
    exact = replace(selection, context_id="exact-contract", join_keys=EXACT)
    owner = api.create_owner(
        raw_projection_reader=Reader(),raw_projection_mappings=mappings,
        parameter_sets=parameters,input_selection_policies=(selection,exact),
        unit_conventions=(api.UnitConventionVersionV1("numeric",1,"number","number",Decimal(1),Decimal(0)),),
        contexts=(),utc_now=lambda: NOW+timedelta(seconds=1),
    )
    req = api.CalculationRequestV1(
        target,"NVDA",NOW,cutoff,"calc-v1","rule",1,"underlying-group",1,(),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_BASIC","basic",1),
            api.ParameterProfileRefV1("P_RULE","rule",1),
            api.ParameterProfileRefV1("P_TIME","time",1),
        ),
        raw_input_bindings=tuple(bindings),
        predecessor_selection_policy_refs=tuple((did,api.VersionRefV1("exact-contract", 999 if wrong_child_version else 1)) for did in
            (("D120","D091") if target == "D121" else ("D120","D085"))),
    )
    return owner, req


@pytest.mark.parametrize("target",["D121","D122"])
def test_grouped_public_signed_notional_and_complete_identity_lineage(target: str) -> None:
    owner, req = setup(target)
    result = owner.materialise(req)
    assert result is not None
    if target == "D121":
        assert result.result == (
            (("2026-12-18", "call", "wing"), Decimal("1200")),
            (("2026-12-25", "put", "core"), Decimal("-1200")),
        )
    else:
        assert result.result == (
            (("2026-12-18", "far"), Decimal("1200")),
            (("2026-12-25", "far"), Decimal("-1200")),
        )
    children = [owner.reads.get_derived_occurrence(oid) for oid in result.predecessor_occurrence_ids]
    assert len(children) == 4
    assert {x.derived_signal_id for x in children if x} == (
        {"D120", "D091"} if target == "D121" else {"D120","D085"}
    )
    assert {x.selection_identity.value_for("contract_id") for x in children if x} == {"C100","P105"}
    assert {x.observation_occurrence_id for x in result.raw_input_lineage if x.raw_signal_id == "R120"} == {"trade-C100","trade-P105"}
    assert owner.materialise(req) == result


@pytest.mark.parametrize("target",["D121","D122"])
@pytest.mark.parametrize("missing",[("C100","R121"),("P105","R120")])
def test_grouped_public_refuses_missing_member(target: str, missing: tuple[str,str]) -> None:
    owner, req = setup(target,omit=missing)
    assert owner.materialise(req) is None


@pytest.mark.parametrize("target",["D121","D122"])
def test_grouped_public_refuses_wrong_contract_identity(target: str) -> None:
    owner, req = setup(target,conflict=("P105","R121"))
    assert owner.materialise(req) is None


@pytest.mark.parametrize("target",["D121","D122"])
def test_grouped_public_refuses_wrong_child_version(target: str) -> None:
    owner, req = setup(target,wrong_child_version=True)
    assert owner.materialise(req) is None


def test_grouped_public_refuses_unbound_delta_contract() -> None:
    owner, req = setup("D121",extra=("EXTRA","R112"))
    assert owner.materialise(req) is None
