"""Prepare admitted raw bundles into one bounded prepared runtime substrate."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

from nvda_desk.ingress.raw_bundle_loader import RealDataBundle, load_api_payload


@dataclass(slots=True)
class PreparedRuntimeLineage:
    """Trace how one prepared runtime snapshot was formed."""

    source_kind: str
    transport: str
    source_snapshot_id: str | None = None
    source_sections: tuple[str, ...] = ()
    alignment_policy: str = "unaligned"
    runtime_bar_time_utc: datetime | None = None
    derived_field_names: tuple[str, ...] = ()


@dataclass(slots=True)
class PreparedRuntimeSnapshot(Mapping[str, Any]):
    """One prepared runtime snapshot that downstream mappers can consume."""

    snapshot_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    lineage: PreparedRuntimeLineage = field(
        default_factory=lambda: PreparedRuntimeLineage(
            source_kind="legacy_payload",
            transport="mapping",
        )
    )
    derived_fields: dict[str, Any] = field(default_factory=dict)
    missing_optional_enrichments: list[str] = field(default_factory=list)
    failed_enrichments: list[str] = field(default_factory=list)

    def __getitem__(self, key: str) -> Any:
        return self.payload[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.payload)

    def __len__(self) -> int:
        return len(self.payload)

    def get(self, key: str, default: Any = None) -> Any:
        return self.payload.get(key, default)

    @property
    def runtime_bar_time_utc(self) -> datetime | None:
        return self.lineage.runtime_bar_time_utc

    def as_mapping(self) -> dict[str, Any]:
        """Return a detached mapping view of the prepared payload."""

        return deepcopy(self.payload)


@dataclass(slots=True)
class PreparedRuntimeDataset:
    """Prepared runtime dataset emitted from one or more admitted raw bundles."""

    snapshots: list[PreparedRuntimeSnapshot] = field(default_factory=list)
    dataset_lineage: list[PreparedRuntimeLineage] = field(default_factory=list)
    missing_optional_enrichments: list[str] = field(default_factory=list)
    failed_enrichments: list[str] = field(default_factory=list)

    @property
    def primary_snapshot(self) -> PreparedRuntimeSnapshot:
        if not self.snapshots:
            raise ValueError("PreparedRuntimeDataset does not contain any snapshots.")
        return self.snapshots[0]


class RuntimePreparationService:
    """Own deterministic raw-to-prepared runtime substrate transformation."""

    def prepare(
        self,
        raw_bundle: RealDataBundle | Mapping[str, Any] | None = None,
        *,
        snapshot_id: str | None = None,
        payload: Mapping[str, Any] | None = None,
        runtime_bar_time_utc: datetime | None = None,
    ) -> PreparedRuntimeSnapshot:
        """Return one prepared runtime snapshot for the supplied raw input."""

        if raw_bundle is not None:
            return prepare_runtime_dataset(
                raw_bundle, runtime_bar_time_utc=runtime_bar_time_utc
            ).primary_snapshot
        return prepare_runtime_snapshot(
            snapshot_id=snapshot_id,
            payload=payload,
            runtime_bar_time_utc=runtime_bar_time_utc,
        )

    def prepare_dataset(
        self,
        raw_bundle: (
            RealDataBundle | Mapping[str, Any] | Iterable[RealDataBundle | Mapping[str, Any]]
        ),
        *,
        runtime_bar_time_utc: datetime | None = None,
    ) -> PreparedRuntimeDataset:
        """Return a prepared runtime dataset for one or more admitted raw bundles."""

        return prepare_runtime_dataset(raw_bundle, runtime_bar_time_utc=runtime_bar_time_utc)


def align_snapshot_to_bar(
    snapshot_payload: Mapping[str, Any],
    *,
    source_time_utc: datetime | None = None,
    source_date: date | None = None,
    runtime_bar_time_utc: datetime | None = None,
) -> tuple[dict[str, Any], str]:
    """Return a payload aligned to an explicit or minute-floored runtime bar."""

    aligned_payload = dict(snapshot_payload)
    if source_time_utc is not None:
        aligned_payload["source_time_utc"] = source_time_utc
    if source_date is not None:
        aligned_payload["source_date"] = source_date

    if runtime_bar_time_utc is not None:
        aligned_payload["runtime_bar_time_utc"] = runtime_bar_time_utc
        return aligned_payload, "explicit_runtime_bar_time_utc"

    resolved_source_time_utc = _optional_datetime(aligned_payload, "source_time_utc")
    if resolved_source_time_utc is None:
        return aligned_payload, "missing_source_time_utc"

    aligned_payload["runtime_bar_time_utc"] = resolved_source_time_utc.replace(
        second=0, microsecond=0
    )
    return aligned_payload, "floor_minute_from_source_time_utc"


def derive_runtime_features(
    snapshot_payload: Mapping[str, Any],
) -> tuple[dict[str, Any], list[str], list[str]]:
    """Return deterministic derived features and explicit optional-enrichment state."""

    derived: dict[str, Any] = {}
    missing_optional: list[str] = []
    failed: list[str] = []

    windows = snapshot_payload.get("windows")
    if windows is None:
        missing_optional.append("window_count:windows")
    elif isinstance(windows, list):
        derived["window_count"] = len(windows)
        derived["has_windows"] = bool(windows)
    else:
        failed.append("window_count:windows_not_list")

    source_time_utc = _optional_datetime(snapshot_payload, "source_time_utc")
    next_event_time_utc = _optional_datetime(snapshot_payload, "next_event_time_utc")
    if next_event_time_utc is None:
        missing_optional.append("minutes_to_next_event:next_event_time_utc")
    elif isinstance(source_time_utc, datetime) and isinstance(next_event_time_utc, datetime):
        derived["minutes_to_next_event"] = int(
            (next_event_time_utc - source_time_utc).total_seconds() // 60
        )
    else:
        failed.append("minutes_to_next_event:invalid_temporal_inputs")

    front_dte = snapshot_payload.get("front_dte")
    next_dte = snapshot_payload.get("next_dte")
    if front_dte is None or next_dte is None:
        missing_optional.append("front_to_next_dte_spread:dte_inputs")
    else:
        try:
            derived["front_to_next_dte_spread"] = int(next_dte) - int(front_dte)
        except (TypeError, ValueError):
            failed.append("front_to_next_dte_spread:invalid_dte_inputs")

    if snapshot_payload.get("nvda_return_pct") is None:
        close_key = next(
            (
                key
                for key in ("prior_close", "previous_close", "reference_close")
                if snapshot_payload.get(key) is not None
            ),
            None,
        )
        if snapshot_payload.get("market_spot_price") is None or close_key is None:
            missing_optional.append("nvda_return_pct:price_inputs")
        else:
            try:
                close_price = float(snapshot_payload[close_key])
                if close_price == 0:
                    failed.append("nvda_return_pct:zero_close_price")
                else:
                    market_spot_price = float(snapshot_payload["market_spot_price"])
                    derived["nvda_return_pct"] = (market_spot_price - close_price) / close_price
            except (TypeError, ValueError):
                failed.append("nvda_return_pct:invalid_price_inputs")

    return derived, missing_optional, failed


def prepare_runtime_dataset(
    raw_bundle: RealDataBundle | Mapping[str, Any] | Iterable[RealDataBundle | Mapping[str, Any]],
    *,
    runtime_bar_time_utc: datetime | None = None,
) -> PreparedRuntimeDataset:
    """Return the lawful prepared substrate for one or more admitted raw bundles."""

    prepared_snapshots: list[PreparedRuntimeSnapshot] = []
    dataset_missing: list[str] = []
    dataset_failed: list[str] = []

    for bundle in _iter_bundles(raw_bundle):
        prepared = _prepare_single_bundle(bundle, runtime_bar_time_utc=runtime_bar_time_utc)
        prepared_snapshots.append(prepared)
        dataset_missing.extend(
            _prefix_list(prepared.snapshot_id, prepared.missing_optional_enrichments)
        )
        dataset_failed.extend(_prefix_list(prepared.snapshot_id, prepared.failed_enrichments))

    return PreparedRuntimeDataset(
        snapshots=prepared_snapshots,
        dataset_lineage=[snapshot.lineage for snapshot in prepared_snapshots],
        missing_optional_enrichments=dataset_missing,
        failed_enrichments=dataset_failed,
    )


def prepare_runtime_snapshot(
    *,
    snapshot_id: str | None = None,
    payload: Mapping[str, Any] | None = None,
    runtime_bar_time_utc: datetime | None = None,
) -> PreparedRuntimeSnapshot:
    """Return one prepared snapshot from a legacy payload-only preparation call."""

    payload_mapping = deepcopy(dict(payload or {}))
    aligned_payload, alignment_policy = align_snapshot_to_bar(
        payload_mapping,
        source_time_utc=_optional_datetime(payload_mapping, "source_time_utc"),
        source_date=_optional_date(payload_mapping, "source_date"),
        runtime_bar_time_utc=runtime_bar_time_utc,
    )
    derived_fields, missing_optional, failed = derive_runtime_features(aligned_payload)
    prepared_payload = dict(aligned_payload)
    prepared_payload.update(derived_fields)
    return PreparedRuntimeSnapshot(
        snapshot_id=snapshot_id,
        payload=prepared_payload,
        lineage=PreparedRuntimeLineage(
            source_kind="legacy_payload",
            transport="mapping",
            source_snapshot_id=snapshot_id,
            source_sections=("payload",),
            alignment_policy=alignment_policy,
            runtime_bar_time_utc=prepared_payload.get("runtime_bar_time_utc"),
            derived_field_names=tuple(sorted(derived_fields)),
        ),
        derived_fields=derived_fields,
        missing_optional_enrichments=missing_optional,
        failed_enrichments=failed,
    )


def _iter_bundles(
    raw_bundle: RealDataBundle | Mapping[str, Any] | Iterable[RealDataBundle | Mapping[str, Any]],
) -> Iterator[RealDataBundle]:
    if isinstance(raw_bundle, RealDataBundle):
        yield raw_bundle
        return
    if isinstance(raw_bundle, Mapping):
        yield load_api_payload(raw_bundle)
        return
    for item in raw_bundle:
        if isinstance(item, RealDataBundle):
            yield item
        elif isinstance(item, Mapping):
            yield load_api_payload(item)
        else:
            raise TypeError(f"Unsupported raw bundle item type: {type(item)!r}")


def _prepare_single_bundle(
    bundle: RealDataBundle, *, runtime_bar_time_utc: datetime | None = None
) -> PreparedRuntimeSnapshot:
    combined_payload = _combine_raw_sections(bundle)
    source_time_utc = _resolve_source_time_utc(bundle)
    source_date = _resolve_source_date(bundle)
    aligned_payload, alignment_policy = align_snapshot_to_bar(
        combined_payload,
        source_time_utc=source_time_utc,
        source_date=source_date,
        runtime_bar_time_utc=runtime_bar_time_utc,
    )
    derived_fields, missing_optional, failed = derive_runtime_features(aligned_payload)
    prepared_payload = dict(aligned_payload)
    prepared_payload.update(derived_fields)
    return PreparedRuntimeSnapshot(
        snapshot_id=bundle.snapshot_id,
        payload=prepared_payload,
        lineage=PreparedRuntimeLineage(
            source_kind=bundle.provenance.source_kind,
            transport=bundle.provenance.transport,
            source_snapshot_id=bundle.snapshot_id,
            source_sections=_source_sections(bundle),
            alignment_policy=alignment_policy,
            runtime_bar_time_utc=prepared_payload.get("runtime_bar_time_utc"),
            derived_field_names=tuple(sorted(derived_fields)),
        ),
        derived_fields=derived_fields,
        missing_optional_enrichments=missing_optional,
        failed_enrichments=failed,
    )


def _combine_raw_sections(bundle: RealDataBundle) -> dict[str, Any]:
    market_snapshot = dict(bundle.market_snapshot)
    options_surface = _effective_options_surface(bundle)
    provenance_payload = bundle.provenance.model_dump(
        mode="python", exclude={"source_kind", "transport"}, exclude_none=True
    )
    payload: dict[str, Any] = {}

    if "spot_price" in market_snapshot:
        payload["market_spot_price"] = market_snapshot["spot_price"]
    if "spot_price" in options_surface:
        payload["options_spot_price"] = options_surface["spot_price"]
        payload["spot_price"] = options_surface["spot_price"]
    elif "spot_price" in market_snapshot:
        payload["spot_price"] = market_snapshot["spot_price"]

    for key in (
        "nvda_return_pct",
        "nq_return_pct",
        "vix_level",
        "prior_close",
        "previous_close",
        "reference_close",
        "source_time_raw",
        "source_time_kind",
        "source_timezone_raw",
        "source_time_utc",
        "source_date",
        "captured_at_utc",
        "persisted_at_utc",
        "source_provider",
        "source_channel",
        "time_granularity",
    ):
        if key in market_snapshot:
            payload[key] = market_snapshot[key]
        elif key in options_surface:
            payload[key] = options_surface[key]
        elif key in provenance_payload:
            payload[key] = provenance_payload[key]

    next_event_time_utc = _optional_datetime(market_snapshot, "next_event_time_utc")
    if next_event_time_utc is not None:
        payload["next_event_time_utc"] = next_event_time_utc

    windows = market_snapshot.get("windows")
    if windows is not None:
        payload["windows"] = _normalise_windows(windows)

    for key in ("front_dte", "next_dte"):
        if key in options_surface:
            payload[key] = options_surface[key]

    return payload


def _resolve_source_time_utc(bundle: RealDataBundle) -> datetime | None:
    provenance_source_time_utc = bundle.provenance.source_time_utc
    if isinstance(provenance_source_time_utc, datetime):
        return provenance_source_time_utc
    for section in (bundle.market_snapshot, bundle.options_surface):
        source_time_utc = _optional_datetime(section, "source_time_utc")
        if isinstance(source_time_utc, datetime):
            return source_time_utc
    return None


def _resolve_source_date(bundle: RealDataBundle) -> date | None:
    provenance_source_date = bundle.provenance.source_date
    if isinstance(provenance_source_date, date):
        return provenance_source_date
    for section in (bundle.market_snapshot, bundle.options_surface):
        source_date = _optional_date(section, "source_date")
        if isinstance(source_date, date):
            return source_date
    return None


def _source_sections(bundle: RealDataBundle) -> tuple[str, ...]:
    sections: list[str] = []
    if bundle.market_snapshot:
        sections.append("market_snapshot")
    if bundle.options_surface:
        sections.append("options_surface")
    return tuple(sections)


def _effective_options_surface(bundle: RealDataBundle) -> dict[str, Any]:
    options_surface = dict(bundle.options_surface)
    if not options_surface:
        return dict(bundle.market_snapshot)
    if "spot_price" not in options_surface and "spot_price" in bundle.market_snapshot:
        options_surface["spot_price"] = bundle.market_snapshot["spot_price"]
    return options_surface


def _optional_datetime(mapping: Mapping[str, Any], key: str) -> datetime | None:
    value = mapping.get(key)
    if isinstance(value, datetime):
        return value
    return None


def _optional_date(mapping: Mapping[str, Any], key: str) -> date | None:
    value = mapping.get(key)
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    return None


def _normalise_windows(windows: Any) -> list[dict[str, Any]]:
    if not isinstance(windows, list):
        raise TypeError("Prepared snapshot field 'windows' must be a list when present.")
    normalised: list[dict[str, Any]] = []
    for item in windows:
        if not isinstance(item, Mapping):
            raise TypeError("Window items must be mappings.")
        normalised.append(
            {
                "event_id": item["event_id"],
                "window_start_utc": item["window_start_utc"],
                "window_end_utc": item["window_end_utc"],
                "tags": list(item.get("tags", [])),
            }
        )
    return normalised


def _prefix_list(snapshot_id: str | None, values: list[str]) -> list[str]:
    prefix = snapshot_id if snapshot_id is not None else "snapshot:none"
    return [f"{prefix}:{value}" for value in values]
