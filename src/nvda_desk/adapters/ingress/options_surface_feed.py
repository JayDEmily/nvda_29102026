"""Thin compatibility wrapper over the benchmark-owned raw bundle decode and preparation seam."""

from __future__ import annotations

from typing import Any, Mapping

from nvda_desk.cognition.ingress.options_mapper import build_options_flow_input
from nvda_desk.ingress.raw_bundle_loader import load_api_payload
from nvda_desk.preparation.runtime_preparer import prepare_runtime_dataset


def adapt_options_surface(payload: Mapping[str, Any]):
    """Return one typed options-flow input from a raw options payload."""

    bundle = load_api_payload(payload)
    dataset = prepare_runtime_dataset(bundle)
    return build_options_flow_input(dataset.primary_snapshot)
