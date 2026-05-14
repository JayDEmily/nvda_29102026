"""Decode admitted raw bundle payloads into one bounded typed ingress carrier."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RawBundleProvenance(BaseModel):
    """Minimal provenance carried with one admitted raw bundle."""

    model_config = ConfigDict(extra="forbid")
    source_kind: str
    transport: str = "mapping"
    source_time_raw: str | None = None
    source_time_kind: str | None = None
    source_timezone_raw: str | None = None
    source_time_utc: datetime | None = None
    source_date: date | None = None
    captured_at_utc: datetime | None = None
    persisted_at_utc: datetime | None = None
    source_provider: str | None = None
    source_channel: str | None = None
    time_granularity: str | None = None

    @model_validator(mode="after")
    def _require_source_temporal_truth(self) -> "RawBundleProvenance":
        if self.source_time_utc is None and self.source_date is None:
            raise ValueError("source temporal standard requires source_time_utc or source_date")
        return self


class RealDataBundle(BaseModel):
    """Typed raw bundle kept upstream of preparation and cognition ingress."""

    model_config = ConfigDict(extra="forbid")
    snapshot_id: str | None = None
    market_snapshot: dict[str, Any] = Field(default_factory=dict)
    options_surface: dict[str, Any] = Field(default_factory=dict)
    provenance: RawBundleProvenance


class RawBundleLoader:
    """Load raw bundles from bounded JSON or API boundary payloads."""

    def load_json_bundle(self, payload: Mapping[str, Any]) -> RealDataBundle:
        """Return one typed raw bundle from a JSON-shaped mapping."""

        return load_json_bundle(payload)

    def load_api_payload(self, payload: Mapping[str, Any]) -> RealDataBundle:
        """Return one typed raw bundle from an API-shaped mapping."""

        return load_api_payload(payload)


def _mapping_value(payload: Mapping[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _build_market_snapshot(payload: Mapping[str, Any]) -> dict[str, Any]:
    explicit = _mapping_value(payload, "market_snapshot")
    return explicit or dict(payload)


def _build_options_surface(
    payload: Mapping[str, Any], *, market_snapshot: Mapping[str, Any]
) -> dict[str, Any]:
    explicit = _mapping_value(payload, "options_surface")
    if explicit:
        return explicit
    direct_subset = {
        key: payload[key] for key in ("spot_price", "front_dte", "next_dte") if key in payload
    }
    return direct_subset or dict(market_snapshot)


def _first_present(payloads: tuple[Mapping[str, Any], ...], key: str) -> Any:
    for payload in payloads:
        if key in payload and payload[key] is not None:
            return payload[key]
    return None


def _build_bundle(payload: Mapping[str, Any], *, source_kind: str) -> RealDataBundle:
    market_snapshot = _build_market_snapshot(payload)
    options_surface = _build_options_surface(payload, market_snapshot=market_snapshot)
    temporal_sources = (payload, market_snapshot, options_surface)
    return RealDataBundle(
        snapshot_id=(
            str(payload["snapshot_id"])
            if "snapshot_id" in payload and payload["snapshot_id"] is not None
            else None
        ),
        market_snapshot=market_snapshot,
        options_surface=options_surface,
        provenance=RawBundleProvenance(
            source_kind=source_kind,
            transport="mapping",
            source_time_raw=_first_present(temporal_sources, "source_time_raw"),
            source_time_kind=_first_present(temporal_sources, "source_time_kind"),
            source_timezone_raw=_first_present(temporal_sources, "source_timezone_raw"),
            source_time_utc=_first_present(temporal_sources, "source_time_utc"),
            source_date=_first_present(temporal_sources, "source_date"),
            captured_at_utc=_first_present(temporal_sources, "captured_at_utc"),
            persisted_at_utc=_first_present(temporal_sources, "persisted_at_utc"),
            source_provider=_first_present(temporal_sources, "source_provider"),
            source_channel=_first_present(temporal_sources, "source_channel"),
            time_granularity=_first_present(temporal_sources, "time_granularity"),
        ),
    )


def load_json_bundle(payload: Mapping[str, Any]) -> RealDataBundle:
    """Return one typed raw bundle from a JSON-source mapping."""

    return _build_bundle(payload, source_kind="json_bundle")


def load_api_payload(payload: Mapping[str, Any]) -> RealDataBundle:
    """Return one typed raw bundle from an API-source mapping."""

    return _build_bundle(payload, source_kind="api_payload")
