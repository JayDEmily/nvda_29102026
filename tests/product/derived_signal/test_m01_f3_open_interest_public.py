"""F3 proof-first public D124 strike/expiry concentration over distinct contracts.

Accepted K08 D124: combine call/put OI by exact strike and expiry before
computing shares and HHI; native M00 observations retain contract identity.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 8, 3, 0, tzinfo=UTC)


def public_concentration(
    *,
    missing_identity: bool = False,
    duplicate_call: bool = False,
    negative_oi: bool = False,
) -> tuple[Any, api.CalculationRequestV1]:
    records: list[tuple[str, str, str, Decimal, str, Decimal]] = [
        ("R047", "C100", "2026-12-18", Decimal(100), "call", Decimal(30)),
        ("R048", "P100", "2026-12-18", Decimal(100), "put", Decimal(20)),
        ("R047", "C105", "2026-12-18", Decimal(105), "call", Decimal(70)),
    ]
    if duplicate_call:
        records.append(records[0])
    if negative_oi:
        records[0] = (*records[0][:-1], Decimal(-30))
    projections: dict[str, list[raw.ProjectedRawValueV1]] = {"R047": [], "R048": []}
    bindings: list[api.RawInputBindingV1] = []
    for idx, (rid, cid, expiry, strike, right, value) in enumerate(records):
        vals: tuple[tuple[str, object], ...] = (
            ("contract_id", cid),
            ("underlying_instrument", "NVDA"),
            *(() if (missing_identity and cid == "P100") else (("expiry", expiry),)),
            ("strike", strike),
            ("option_right", right),
        )
        ident = raw.RawSelectionIdentityV1(vals)
        projections[rid].append(
            raw.ProjectedRawValueV1(
                raw_signal_catalogue_id=raw.RawSignalCatalogueId(rid),
                observation_occurrence_id=raw.observation_occurrence_id(f"oi-{idx}-{cid}"),
                projection_mapping_id=f"map-{rid}",
                projection_mapping_version=1,
                source_provider="controlled",
                source_variant="chain",
                native_field_path=("field", rid),
                native_value=value,
                native_units="contracts",
                subject_instrument="NVDA",
                source_temporal_kind="true_instant",
                source_timestamp_raw=NOW.isoformat(),
                source_timezone_native="UTC",
                received_ts_utc=NOW,
                ingestion_sequence=idx + 1,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled:chain"),
                revision_vintage_native="v1",
                selection_identity=ident,
            )
        )
        bindings.append(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1(f"map-{rid}", 1),
                api.VersionRefV1("contracts", 1),
                "NVDA",
                ident,
            )
        )

    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id: Any, **kwargs: Any) -> Any:
            return raw.ProjectedRawHistoryPageV1(
                tuple(projections.get(raw_signal_catalogue_id.value, ())), None
            )

        def project_raw_value(self, *args: object, **kwargs: object) -> None:
            return None

    owner = api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                f"map-{rid}",
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled",
                "chain",
                ("field", rid),
                "contracts",
            )
            for rid in ("R047", "R048")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1("rule", 1, "P_RULE", (("grouping", "strike_expiry"),)),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "oi-chain",
                1,
                ("underlying_instrument",),
                timedelta(days=1),
                timedelta(days=1),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "contracts", 1, "contracts", "contracts", Decimal(1), Decimal(0)
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW + timedelta(seconds=1),
    )
    request = api.CalculationRequestV1(
        "D124",
        "NVDA",
        NOW,
        NOW,
        "calc-v1",
        "rule",
        1,
        "oi-chain",
        1,
        (),
        parameter_profile_refs=(api.ParameterProfileRefV1("P_RULE", "rule", 1),),
        raw_input_bindings=tuple(bindings),
    )
    return owner, request


def test_d124_public_groups_call_put_same_strike_and_proves_hhi_and_lineage() -> None:
    owner, request = public_concentration()
    result = owner.materialise(request)
    assert result is not None
    fields = dict(result.result)
    assert fields["hhi"] == Decimal(37) / Decimal(72)
    assert dict(fields["shares"]) == {
        ("2026-12-18", Decimal(100)): Decimal(5) / Decimal(12),
        ("2026-12-18", Decimal(105)): Decimal(7) / Decimal(12),
    }
    assert {r.observation_occurrence_id for r in result.raw_input_lineage} == {
        "oi-0-C100",
        "oi-1-P100",
        "oi-2-C105",
    }


@pytest.mark.parametrize("variation", ["missing_identity", "duplicate_call", "negative_oi"])
def test_d124_public_refuses_invalid_contract_grouping(variation: str) -> None:
    if variation == "duplicate_call":
        # The admitted request type rejects duplicate raw/identity bindings
        # before the owner is constructed; this is still a fail-closed refusal.
        with pytest.raises(ValueError, match="distinct raw-signal/subject/selection"):
            public_concentration(duplicate_call=True)
        return
    owner, request = public_concentration(**{variation: True})
    assert owner.materialise(request) is None
