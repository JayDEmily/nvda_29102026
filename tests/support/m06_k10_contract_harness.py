"""Independent reference harness for M06 K10 public-contract proof."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Any, Mapping

from nvda_desk.contracts.prepared_data import PreparedEventWindow, PreparedRuntimePayloadV1
from nvda_desk.m03_preparation import PreparedDataBuilder, SourceCaptureReference

CLOSED = (
    "prepared_truth",
    "packet_identity",
    "serial_candidate",
    "coefficient_modifier",
    "final_risk",
    "capital",
    "broker_order",
    "position_inventory",
    "lifecycle",
    "transaction",
    "replay",
)


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if hasattr(value, "model_dump"):
        return _canonical(value.model_dump(mode="python"))
    if is_dataclass(value):
        return _canonical(asdict(value))
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value)}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def fingerprint(value: Any) -> str:
    return sha256(
        json.dumps(_canonical(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def make_prepared(
    *,
    vix_level: float | None = 18.0,
    scheduled_event: bool = False,
    front_dte: int | None = 5,
    next_dte: int | None = 12,
    degraded: bool = False,
    now: datetime = datetime(2026, 7, 31, 10, 0, tzinfo=UTC),
):
    windows = ()
    if scheduled_event:
        windows = (
            PreparedEventWindow(
                event_id="event.nvda.earnings",
                window_start_utc=now - timedelta(minutes=30),
                window_end_utc=now + timedelta(minutes=30),
                tags=("scheduled_event_window_active",),
            ),
        )
    payload = PreparedRuntimePayloadV1(
        source_time_utc=now,
        runtime_bar_time_utc=now,
        spot_price=190.0,
        front_dte=front_dte,
        next_dte=next_dte,
        windows=windows,
        next_event_time_utc=now + timedelta(days=2),
        nvda_return_pct=1.2,
        nq_return_pct=0.4,
        vix_level=vix_level,
        window_count=len(windows),
        has_windows=bool(windows),
        minutes_to_next_event=2880,
        front_to_next_dte_spread=(
            (next_dte - front_dte) if front_dte is not None and next_dte is not None else None
        ),
    )
    source = SourceCaptureReference(
        capture_id="capture.market.20260731T100000Z",
        source_artifact_id="artifact.market.20260731T100000Z",
        family_id="market_runtime",
        contract_id="source.market.v1",
        schema_version="1.0.0",
        source_owner="m01",
        effective_at_utc=now,
        source_time_utc=now,
        temporal_precision="instant",
        input_fingerprint="a" * 64,
        validation_state="degraded" if degraded else "valid",
        limitations=("source_partial",) if degraded else (),
        semantic_fields=("vix_level", "front_dte", "next_dte", "windows"),
    )
    return PreparedDataBuilder().build(
        source_capture_refs=(source,),
        input_schema_versions={"market_runtime": "1.0.0"},
        schema_version="1.0.0",
        preparation_policy_version="prep.v1",
        alignment_policy_version="align.v1",
        fingerprint_policy_version="fingerprint.v1",
        canonicalisation_version="canonical.v1",
        derivation_versions={},
        effective_at_utc=now,
        payload=payload,
        payload_schema_version="1.0.0",
        validation_state="degraded" if degraded else "valid",
        completeness_state="degraded" if degraded else "complete",
        limitations=("source_partial",) if degraded else (),
        missing_optional_enrichments=("liquidity_context",) if degraded else (),
    )


@dataclass(frozen=True)
class ReferenceObservation:
    family: str
    state: str
    reason: str
    source_fields: tuple[str, ...]
    limitation: str | None = None

    @property
    def semantic_fingerprint(self) -> str:
        return fingerprint(self.__dict__)


@dataclass(frozen=True)
class ReferenceAssessment:
    state: str
    observations: tuple[ReferenceObservation, ...]
    caution_flags: tuple[str, ...]
    hard_blocks: tuple[str, ...]
    unknown_families: tuple[str, ...]
    limitations: tuple[str, ...]
    input_fingerprint: str
    policy_version: str
    closed_authority_classes: tuple[str, ...] = CLOSED
    foreign_authority_claimed: bool = False

    @property
    def semantic_fingerprint(self) -> str:
        return fingerprint(self.__dict__)


def reference_evaluate(
    prepared,
    *,
    policy_version: str = "parallel-risk.compat.v1",
    caution_threshold: float | None = 30.0,
    block_threshold: float | None = 50.0,
    threshold_authority_refs: tuple[str, ...] = (
        "m07:risk_vix_caution_threshold:v1",
        "m07:risk_vix_hot_threshold:v1",
    ),
) -> ReferenceAssessment:
    if not hasattr(prepared, "model_dump"):
        raise TypeError("typed_prepared_envelope_required")
    # Revalidate by reconstructing through the Pydantic contract.
    from nvda_desk.contracts.prepared_data import PreparedDataEnvelope

    governed = PreparedDataEnvelope.model_validate(prepared.model_dump(mode="python"))
    if not policy_version:
        raise ValueError("policy_version_required")
    if caution_threshold is None or block_threshold is None or not threshold_authority_refs:
        raise ValueError("threshold_authority_required")
    if caution_threshold >= block_threshold:
        raise ValueError("threshold_order_invalid")

    payload = governed.payload
    observations: list[ReferenceObservation] = [
        ReferenceObservation(
            family="concentration",
            state="unknown",
            reason="concentration_context_unavailable",
            source_fields=("concentration_context",),
            limitation="concentration_context_unavailable",
        ),
        ReferenceObservation(
            family="inventory_stress",
            state="unknown",
            reason="inventory_stress_context_unavailable",
            source_fields=("inventory_stress_context",),
            limitation="inventory_stress_context_unavailable",
        ),
        ReferenceObservation(
            family="liquidity",
            state="unknown",
            reason="liquidity_context_unavailable",
            source_fields=("liquidity_context",),
            limitation="liquidity_context_unavailable",
        ),
    ]
    tags = {tag for window in payload.windows for tag in window.tags}
    observations.append(
        ReferenceObservation(
            family="scheduled_event",
            state="caution" if "scheduled_event_window_active" in tags else "observe",
            reason=(
                "scheduled_event_window_active"
                if "scheduled_event_window_active" in tags
                else "no_active_scheduled_event_window"
            ),
            source_fields=("windows",),
        )
    )
    if payload.front_dte is None or payload.next_dte is None:
        observations.append(
            ReferenceObservation(
                family="options_term_structure",
                state="unknown",
                reason="options_dte_missing",
                source_fields=("front_dte", "next_dte"),
                limitation="options_term_structure_unavailable",
            )
        )
    else:
        inverted = payload.front_dte > payload.next_dte
        observations.append(
            ReferenceObservation(
                family="options_term_structure",
                state="caution" if inverted else "observe",
                reason=(
                    "front_term_structure_backwardation"
                    if inverted
                    else "front_term_structure_not_inverted"
                ),
                source_fields=("front_dte", "next_dte"),
            )
        )
    if payload.vix_level is None:
        observations.append(
            ReferenceObservation(
                family="volatility",
                state="unknown",
                reason="vix_level_missing",
                source_fields=("vix_level",),
                limitation="volatility_context_unavailable",
            )
        )
    else:
        state = (
            "block"
            if payload.vix_level >= block_threshold
            else ("caution" if payload.vix_level >= caution_threshold else "observe")
        )
        observations.append(
            ReferenceObservation(
                family="volatility",
                state=state,
                reason=(
                    "vix_block_threshold_reached"
                    if state == "block"
                    else (
                        "vix_caution_threshold_reached"
                        if state == "caution"
                        else "vix_below_caution_threshold"
                    )
                ),
                source_fields=("vix_level",),
            )
        )
    observations = sorted(observations, key=lambda item: item.family)
    hard_blocks = tuple(o.reason for o in observations if o.state == "block")
    caution_flags = tuple(o.reason for o in observations if o.state == "caution")
    unknown = tuple(o.family for o in observations if o.state == "unknown")
    limitations = tuple(
        sorted(set(governed.limitations) | {o.limitation for o in observations if o.limitation})
    )
    state = (
        "block"
        if hard_blocks
        else "caution" if caution_flags else "unknown" if unknown else "observe"
    )
    return ReferenceAssessment(
        state=state,
        observations=tuple(observations),
        caution_flags=caution_flags,
        hard_blocks=hard_blocks,
        unknown_families=unknown,
        limitations=limitations,
        input_fingerprint=fingerprint(
            {
                "prepared_id": governed.prepared_id,
                "prepared_fingerprint": governed.prepared_fingerprint,
                "effective_at_utc": governed.effective_at_utc,
                "validation_state": governed.validation_state,
                "limitations": governed.limitations,
                "payload": governed.payload,
                "policy_version": policy_version,
                "threshold_authority_refs": tuple(sorted(threshold_authority_refs)),
                "caution_threshold": caution_threshold,
                "block_threshold": block_threshold,
            }
        ),
        policy_version=policy_version,
    )
