"""F4 RC01: native M00 temporal kinds, UTC, receipt age and local sessions.

All D001-D005 requests use the admitted M01 public graph; neither D001 nor
D003 is supplied as a precomputed test predecessor.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 9, 14, 0, tzinfo=UTC)
EVENT = NOW - timedelta(seconds=10)
FIELDS = ("R001", "R002", "R003", "R004", "R005", "R013", "R023", "R024")
VALUES: dict[str, object] = {
    "R001": "quote",
    "R002": "2026-10-10T00:59:50+11:00",
    "R003": "Australia/Melbourne",
    "R004": "Australia/Melbourne",
    "R005": "live",
    "R013": "2026-10-16",
    "R023": "exchange-schedule",
    "R024": "trading-hours",
}


def public_temporal(
    *, source_kind: str = "true_instant", missing: str | None = None,
    future: str | None = None, calendar_closed: bool = False,
    expiry_date: str = "2026-10-16", option_contract: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, tuple[api.RawInputBindingV1, ...]]:
    m00 = raw.create_owner()
    identity_fields = (
        ("contract_id", "OPT-20261016-150C"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-10-16"),
        ("strike", Decimal(150)),
        ("option_right", "call"),
    )
    identity = raw.RawSelectionIdentityV1(identity_fields)
    identity_paths = tuple(
        (key, ("identity", key)) for key, _ in identity_fields
    )
    for seq, rid in enumerate(FIELDS, 1):
        if rid == missing:
            continue
        instant = (
            NOW - timedelta(seconds=15)
            if rid == "R002" and source_kind != "true_instant"
            else EVENT
        )
        if rid == future:
            instant = NOW + timedelta(seconds=2)
        kind = source_kind if rid == "R002" else "true_instant"
        native = expiry_date if rid == "R013" else VALUES[rid]
        # Native temporal R002 may carry a date or collector-only source value.
        if rid == "R002" and source_kind == "date_only":
            native = "2026-10-10"
        if rid == "R002" and source_kind == "receipt_only":
            native = "collector-only"
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("time-" + rid),
                delivery_artifact_ref=raw.delivery_artifact_ref("rc01-" + rid),
                source_provider=raw.provider_id("controlled-rc01-time"),
                native_record={
                    "time": {"value": native},
                    **({"identity": dict(identity_fields)} if option_contract else {}),
                },
                received_ts_utc=instant,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc01-time:clock"),
                source_temporal_kind=kind,
                source_timestamp_raw=(
                    str(native) if rid == "R002" and kind != "receipt_only"
                    else instant.isoformat() if kind == "true_instant" else None
                ),
                source_timezone_native="Australia/Melbourne" if rid == "R002" else "UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="clock",
                subject_instrument="NVDA",
                native_units="native_time",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "time-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc01-time", "clock", ("time", "value"), "native_time",
                identity_paths if option_contract else (),
            ) for rid in FIELDS
        ),
        parameter_sets=(api.CalculationParameterSetV1(
            "time-config", 1, "P_TIME",
            (
                ("exchange_timezone", "Australia/Melbourne"),
                ("trading_date_boundary", "06:00"),
                ("expiry_time", "16:00"),
                ("market_open_weekdays", (5,)),
                ("market_closed_dates", ("2026-10-10",) if calendar_closed else ()),
                ("market_open_dates", ()),
                ("liquid_phases", ("overnight",)),
                ("session_phases", ("overnight|00:00|06:00", "day|06:00|16:00")),
            ),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "time-select-option" if option_contract else "time-select", 1,
            tuple(dict(identity_fields)) if option_contract else ("subject_instrument",),
            timedelta(seconds=30),
            timedelta(seconds=30), ("true_instant", "receipt_only", "date_only"), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "native-time", 1, "native_time", "native_time", Decimal(1), Decimal(0)
        ),),
        contexts=(),
        utc_now=lambda: NOW,
    )
    bindings = tuple(
        api.RawInputBindingV1(
            rid, api.VersionRefV1("time-map-" + rid, 1),
            api.VersionRefV1("native-time", 1), "NVDA",
            identity if option_contract else None,
        ) for rid in FIELDS
    )
    return owner, bindings


def request(
    did: str, bindings: tuple[api.RawInputBindingV1, ...], *,
    option_contract: bool = False,
) -> api.CalculationRequestV1:
    return api.CalculationRequestV1(
        did, "NVDA", NOW, NOW, "time-calculation", "time-config", 1,
        "time-select-option" if option_contract else "time-select", 1,
        (), raw_input_bindings=bindings,
    )


@pytest.mark.parametrize(("did", "expected"), [
    ("D001", EVENT),
    ("D002", (("basis", "source_event"), ("age_seconds", Decimal(10)))),
    ("D003", EVENT.astimezone(ZoneInfo("Australia/Melbourne"))),
    ("D004", date(2026, 10, 9)),
    ("D005", "overnight"),
])
def test_rc01_public_true_instant_utc_age_local_session_lineage_and_retry(
    did: str, expected: object
) -> None:
    owner, bindings = public_temporal()
    result = owner.materialise(request(did, bindings))
    assert result is not None
    assert result.result == expected
    assert "time-R002" in {x.observation_occurrence_id for x in result.raw_input_lineage}
    assert owner.materialise(request(did, bindings)) == result


def test_rc01_public_receipt_only_d002_age_without_fabricating_d001_instant() -> None:
    owner, bindings = public_temporal(source_kind="receipt_only")
    assert owner.materialise(request("D001", bindings)) is None
    age = owner.materialise(request("D002", bindings))
    assert age is not None
    assert age.result == (("basis", "collector_receipt"), ("age_seconds", Decimal(15)))
    assert {x.observation_occurrence_id for x in age.raw_input_lineage} >= {"time-R002"}
    assert age.predecessor_occurrence_ids == ()


def test_rc01_public_date_only_cannot_invent_d001_or_seconds_d002() -> None:
    owner, bindings = public_temporal(source_kind="date_only")
    assert owner.materialise(request("D001", bindings)) is None
    assert owner.materialise(request("D002", bindings)) is None


@pytest.mark.parametrize("did,missing", [
    ("D001", "R002"), ("D002", "R001"), ("D003", "R004"),
    ("D004", "R023"), ("D005", "R024"),
])
def test_rc01_public_missing_required_input_fails_closed(did: str, missing: str) -> None:
    owner, bindings = public_temporal(missing=missing)
    assert owner.materialise(request(did, bindings)) is None


def test_rc01_public_future_market_timezone_refused() -> None:
    owner, bindings = public_temporal(future="R004")
    assert owner.materialise(request("D003", bindings)) is None


@pytest.mark.parametrize(("did", "expected"), [
    ("D010", True),
    ("D085", 7),
    ("D086", None),
])
def test_rc01_public_market_calendar_expiry_with_actual_temporal_predecessors(
    did: str, expected: object
) -> None:
    option_contract = did in {"D085", "D086"}
    owner, bindings = public_temporal(option_contract=option_contract)
    result = owner.materialise(request(did, bindings, option_contract=option_contract))
    assert result is not None
    if did == "D086":
        expiry = datetime(2026, 10, 16, 16, tzinfo=ZoneInfo("Australia/Melbourne"))
        expected = Decimal(str((expiry.astimezone(UTC) - EVENT).total_seconds())) / (
            Decimal(86400) * Decimal(365)
        )
    assert result.result == expected
    source_ids = {x.observation_occurrence_id for x in result.raw_input_lineage}
    assert "time-R002" in source_ids
    assert result.predecessor_occurrence_ids
    if did in {"D085", "D086"}:
        assert "time-R013" in source_ids
    else:
        assert {"time-R005", "time-R023", "time-R024"} <= source_ids
    assert owner.materialise(request(did, bindings, option_contract=option_contract)) == result


def test_rc01_public_closed_market_calendar_emits_false_not_unknown() -> None:
    owner, bindings = public_temporal(calendar_closed=True)
    actual = owner.materialise(request("D010", bindings))
    assert actual is not None and actual.result is False


@pytest.mark.parametrize(("did", "missing"), [
    ("D010", "R005"), ("D085", "R013"), ("D086", "R013"),
])
def test_rc01_public_market_calendar_expiry_missing_input_refuses(
    did: str, missing: str
) -> None:
    option_contract = did in {"D085", "D086"}
    owner, bindings = public_temporal(missing=missing, option_contract=option_contract)
    assert owner.materialise(request(did, bindings, option_contract=option_contract)) is None


@pytest.mark.parametrize("did", ["D085", "D086"])
def test_rc01_public_expired_option_dates_refuse(did: str) -> None:
    owner, bindings = public_temporal(
        expiry_date="2026-10-01", option_contract=True
    )
    assert owner.materialise(request(did, bindings, option_contract=True)) is None
