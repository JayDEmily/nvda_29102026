"""Thin compatibility wrapper over the benchmark-owned raw bundle decode and preparation seam."""

from __future__ import annotations

from typing import Any, Mapping

from nvda_desk.contracts.external_source import (
    ExternalIngressMode,
    ExternalPayloadCarrier,
    ExternalSourceFamily,
    ExternalSourceInterfaceSpec,
)
from nvda_desk.ingress.raw_bundle_loader import load_api_payload
from nvda_desk.preparation.runtime_preparer import PreparedRuntimeSnapshot, prepare_runtime_dataset


def adapt_market_snapshot(
    payload: Mapping[str, Any], *, snapshot_id: str | None = None
) -> PreparedRuntimeSnapshot:
    """Return one prepared runtime snapshot from a raw market payload."""

    bundle_payload = dict(payload)
    if snapshot_id is not None:
        bundle_payload["snapshot_id"] = snapshot_id
    ExternalPayloadCarrier(
        interface=ExternalSourceInterfaceSpec(
            source_id="legacy-recorded-market-adapter",
            source_family=ExternalSourceFamily.MARKET,
            ingress_mode=ExternalIngressMode.RECORDED_API_RESPONSE,
            typed_carrier_name="ExternalPayloadCarrier",
        ),
        payload=bundle_payload,
    )
    bundle = load_api_payload(bundle_payload)
    dataset = prepare_runtime_dataset(bundle)
    return dataset.primary_snapshot
