"""Pure raw upstream-signal ingestion with non-interference guarantees."""

from __future__ import annotations

from collections.abc import Collection
from copy import deepcopy

from nvda_desk.contracts.upstream_signal import (
    RawUpstreamSignalInput,
    UpstreamIngressResult,
    UpstreamSanityTrace,
)

_FORBIDDEN_RUNTIME_DECISION_KEYS = frozenset(
    {
        "authorised_deployable_pct",
        "authorised_notional_usd",
        "brokerage_order",
        "lead_playbook_id",
        "order_qty",
        "position_size",
        "review_explanation",
        "trade_allowed",
    }
)


def _strip_forbidden_runtime_decision_keys(value: object) -> object:
    """Return a copy with runtime-decision keys removed at any nesting depth."""

    if isinstance(value, dict):
        return {
            key: _strip_forbidden_runtime_decision_keys(nested_value)
            for key, nested_value in value.items()
            if key not in _FORBIDDEN_RUNTIME_DECISION_KEYS
        }
    if isinstance(value, list):
        return [_strip_forbidden_runtime_decision_keys(item) for item in value]
    return deepcopy(value)


def _trace_payload(raw_signal: RawUpstreamSignalInput) -> dict[str, object]:
    """Return trace-only payload fields with runtime-decision keys stripped."""

    return {
        key: _strip_forbidden_runtime_decision_keys(value)
        for key, value in raw_signal.payload.items()
        if key not in _FORBIDDEN_RUNTIME_DECISION_KEYS
    }


def ingest_raw_upstream_signal(
    *,
    raw_signal: RawUpstreamSignalInput,
    dataset_packet_payload: dict,
    admitted_signal_families: Collection[str],
) -> UpstreamIngressResult:
    """Create a trace or quarantine result without mutating dataset or trade state."""

    packet_copy = deepcopy(dataset_packet_payload)
    admitted = raw_signal.signal_family_id in set(admitted_signal_families)
    if not admitted:
        return UpstreamIngressResult(
            dataset_packet_payload=packet_copy,
            sanity_trace=UpstreamSanityTrace(
                source_id=raw_signal.source_id,
                signal_family_id=raw_signal.signal_family_id,
                scope_id=raw_signal.scope_id,
                disposition="rejected_quarantined",
                rejection_reason="signal_family_not_admitted",
            ),
            trace_envelope={},
            quarantined=True,
            trade_decision_side_effects=[],
        )

    return UpstreamIngressResult(
        dataset_packet_payload=packet_copy,
        sanity_trace=UpstreamSanityTrace(
            source_id=raw_signal.source_id,
            signal_family_id=raw_signal.signal_family_id,
            scope_id=raw_signal.scope_id,
            disposition="admitted_trace_only",
        ),
        trace_envelope={
            "source_id": raw_signal.source_id,
            "signal_family_id": raw_signal.signal_family_id,
            "scope_id": raw_signal.scope_id,
            "payload": _trace_payload(raw_signal),
        },
        quarantined=False,
        trade_decision_side_effects=[],
    )
