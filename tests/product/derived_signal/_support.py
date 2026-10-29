from __future__ import annotations

import importlib
from datetime import UTC, datetime
from decimal import Decimal
from types import ModuleType
from typing import Any

import pytest

from nvda_desk.raw_signal_occurrence_truth import api as raw_api


def require_m00_symbol(name: str) -> Any:
    value = getattr(raw_api, name, None)
    if value is None:
        pytest.fail(f"DS-T01 expected M00 public projection symbol {name!r} is not implemented")
    return value


def require_m01_api() -> ModuleType:
    try:
        return importlib.import_module("nvda_desk.derived_signal_calculation_truth.api")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "DS-T01 expected public seam nvda_desk.derived_signal_calculation_truth.api "
            "is not implemented",
            pytrace=False,
        )
        raise AssertionError from exc


def require_m01_symbol(name: str) -> Any:
    module = require_m01_api()
    value = getattr(module, name, None)
    if value is None:
        pytest.fail(f"DS-T01 expected M01 public symbol {name!r} is not implemented")
    return value


def raw_observation(
    token: str,
    *,
    native_value: Decimal,
    received_ts_utc: datetime,
    subject: str = "NVDA",
    raw_ids: tuple[str, ...] = ("R001", "R002"),
    source_variant: str = "snapshot",
) -> raw_api.RawObservationOccurrenceV1:
    return raw_api.RawObservationOccurrenceV1(
        concept_id=raw_api.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=raw_api.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=raw_api.observation_occurrence_id(f"obs-{token}"),
        delivery_artifact_ref=raw_api.delivery_artifact_ref(f"delivery-{token}"),
        source_provider=raw_api.provider_id("provider-a"),
        native_record={"quote": {"bid": native_value, "ask": native_value + Decimal("1")}},
        received_ts_utc=received_ts_utc,
        ingestion_sequence=int(token),
        ingestion_sequence_scope=raw_api.ingestion_sequence_scope("provider-a:snapshot"),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=tuple(raw_api.RawSignalCatalogueId(value) for value in raw_ids),
        source_variant=source_variant,
        subject_instrument=subject,
        native_units="provider_record",
        revision_vintage_native=f"rev-{token}",
        source_timestamp_raw=received_ts_utc.astimezone(UTC).isoformat(),
        source_timezone_native="UTC",
    )


def projection_mapping(
    *, raw_id: str = "R001", field_path: tuple[str, ...] = ("quote", "bid"), version: int = 1
) -> Any:
    mapping_type = require_m00_symbol("RawSignalProjectionMappingV1")
    return mapping_type(
        mapping_id=f"provider-a:snapshot:{raw_id}:v{version}:{'.'.join(field_path)}",
        version=version,
        raw_signal_catalogue_id=raw_api.RawSignalCatalogueId(raw_id),
        source_provider="provider-a",
        source_variant="snapshot",
        native_field_path=field_path,
        native_units="percent",
    )
