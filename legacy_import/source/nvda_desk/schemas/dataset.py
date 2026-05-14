"""Typed contracts for deterministic real-data runtime preparation.

Gate E promotes the real-data path from bundle validation to prepared runtime
snapshots, explicit source lineage, cognition-ready conversion, and auditable
sanity reporting.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.checkpoints import CheckpointObservation
from nvda_desk.schemas.cognition import (
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    TemporalContextInput,
)
from nvda_desk.schemas.events import LiveEventSnapshot, NormalisedEventRecord
from nvda_desk.schemas.market import PrecursorRuntimePacket
from nvda_desk.schemas.options_units import OptionalVolFraction, VolFraction
from nvda_desk.schemas.session_clock import DeskCalendarAuthorityPacket


class ProvenanceRecord(BaseModel):
    """Provenance metadata for one imported dataset artifact."""

    model_config = ConfigDict(extra="forbid")

    source_name: str
    source_type: str
    captured_at: datetime
    symbol: str
    note: str = ""


class BarRecord(BaseModel):
    """One replay-ready OHLCV bar."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = Field(ge=0.0)


class OptionQuote(BaseModel):
    """One option quote inside a replay-ready chain snapshot."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    expiry: datetime
    strike: float
    side: str
    bid: float
    ask: float
    last: float | None = None
    iv: OptionalVolFraction = None
    delta: float | None = None
    gamma: float | None = None
    oi: float | None = None
    volume: float | None = None


class OptionSnapshotSequence(BaseModel):
    """Repeated-snapshot metadata for intraday chain sequences."""

    model_config = ConfigDict(extra="forbid")

    sequence_id: str
    snapshot_index: int = Field(ge=0)
    snapshot_count: int = Field(ge=1)
    window_minutes: int | None = Field(default=None, ge=0)


class OptionChainSnapshot(BaseModel):
    """Replay-ready option-chain snapshot for one symbol and timestamp."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    symbol: str
    sequence: OptionSnapshotSequence | None = None
    quotes: list[OptionQuote] = Field(default_factory=list)


class EventRecord(NormalisedEventRecord):
    """Replay-ready scheduled event record with preserved event richness."""


class RealDataBundle(BaseModel):
    """Replay-ready dataset bundle with explicit provenance."""

    model_config = ConfigDict(extra="forbid")

    provenance: ProvenanceRecord
    bars: list[BarRecord] = Field(default_factory=list)
    option_chain_snapshots: list[OptionChainSnapshot] = Field(default_factory=list)
    events: list[EventRecord] = Field(default_factory=list)


class PreparedStrikeCluster(BaseModel):
    """Prepared nearby strike cluster retained for downstream options logic."""

    model_config = ConfigDict(extra="forbid")

    strike: float
    side: str
    open_interest: float = Field(ge=0.0)
    volume: float = Field(ge=0.0)
    distance_to_spot_pct: float


class PreparedSequencePoint(BaseModel):
    """Prepared repeated-snapshot point derived from one chain sequence item."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    front_atm_iv: VolFraction
    next_atm_iv: VolFraction
    put_call_skew: float
    gamma_pressure_score: float
    spot_to_pin_distance_pct: float


class PreparedTenorPoint(BaseModel):
    """Prepared tenor point derived from one expiry on one chain snapshot."""

    model_config = ConfigDict(extra="forbid")

    tenor_dte: int = Field(ge=0)
    atm_iv: VolFraction = Field(ge=0.0)


class PreparedPinProgressionPoint(BaseModel):
    """Prepared distance-to-pin observation over a repeated snapshot sequence."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    distance_to_pin_pct: float




class PreparedRuntimeRegimePacket(BaseModel):
    """Bounded promoted cross-asset regime truth carried on prepared runtime snapshots.

    Purpose:
        Carry only the promoted cross-asset regime truth admitted by the
        upstream signal tranche, including partial live-capture states when some
        regime sources are still missing.
    Inputs:
        Source identity, alignment metadata, promoted regime primitives, live
        capture levels or returns when present, fallback notes, and checkpoint
        observations.
    Outputs:
        One typed promoted-regime packet suitable for prepared-runtime carriage.
    Side Effects:
        None.
    Failure Modes:
        Validation fails when provided regime primitives or checkpoint
        observations are malformed.
    Checkpoints:
        `upstream_signal.regime_packet.complete_requires_breadth_concentration`
        and `upstream_signal.regime_packet.capture_observed` observations are
        retained here when live regime ingress is built.
    """

    model_config = ConfigDict(extra="forbid")

    source_family: str
    source_symbols: list[str] = Field(default_factory=list)
    source_vendor: str = "admitted_runtime_or_fixture"
    observed_at: datetime
    aligned_to_runtime_ts: datetime
    alignment_age_seconds: int = Field(ge=0)
    alignment_state: str = "aligned"
    calendar_owner: str = "financial_calendar_reference_bundle"
    nvda_return_pct: float
    nq_return_pct: float | None = None
    nq_level: float | None = None
    es_return_pct: float | None = None
    es_level: float | None = None
    sox_return_pct: float | None = None
    sox_level: float | None = None
    breadth_score: float | None = Field(default=None, ge=0.0, le=1.0)
    concentration_score: float | None = Field(default=None, ge=0.0, le=1.0)
    vix_level: float | None = None
    vvix_level: float | None = None
    us10y: float | None = None
    us2y: float | None = None
    usdjpy: float | None = None
    completeness_state: str = "regime_core_only"
    fallback_notes: list[str] = Field(default_factory=list)
    checkpoint_observations: list[CheckpointObservation] = Field(default_factory=list)


class PreparedParticipationBaselinePacket(BaseModel):
    """Bounded same-bucket participation truth for runtime ingress.

    Purpose:
        Carry bounded same-bucket participation truth without pretending the
        current baseline proxy is a true historical same-bucket statistical
        baseline.
    Inputs:
        Observed participation state, optional proxy baseline state, owner
        metadata, fallback state, and checkpoint observations.
    Outputs:
        One typed participation packet for prepared-runtime carriage.
    Side Effects:
        None.
    Failure Modes:
        Validation fails when numeric participation fields or checkpoint
        observations are malformed.
    Checkpoints:
        Participation-baseline checkpoints are retained here so tests can
        inspect successful proxy reconstruction or deterministic failure
        conditions.
    """

    model_config = ConfigDict(extra="forbid")

    observed_at: datetime
    session_bucket_label: str
    calendar_owner: str = "financial_calendar_reference_bundle"
    observed_interval_volume_share: float | None = Field(default=None, ge=0.0)
    baseline_interval_volume_share: float | None = Field(default=None, ge=0.0)
    relative_volume_ratio: float | None = None
    observed_spread_bps: float | None = Field(default=None, ge=0.0)
    baseline_spread_bps: float | None = Field(default=None, ge=0.0)
    observed_trade_count: int | None = Field(default=None, ge=0)
    baseline_trade_count: float | None = Field(default=None, ge=0.0)
    baseline_available: bool = False
    fallback_state: str = "baseline_absent"
    checkpoint_observations: list[CheckpointObservation] = Field(default_factory=list)


class PreparedNormalisedFeatureSet(BaseModel):
    """Deterministic normalised prepared-runtime feature carriage with provenance."""

    model_config = ConfigDict(extra="forbid")

    intraday_move_vs_rolling_range_5m: float | None = None
    distance_to_vwap_vs_rolling_range_5m: float | None = None
    intraday_move_vs_price_realised_vol_15m: float | None = None
    front_iv_vs_front_realised_vol_ratio: float | None = None
    next_iv_vs_next_realised_vol_ratio: float | None = None
    atm_straddle_vs_spot_pct: float | None = None
    near_spot_front_volume_share: float | None = None
    provenance: dict[str, list[str]] = Field(default_factory=dict)


class PreparedRuntimeLineage(BaseModel):
    """Explicit lineage retained for one prepared runtime snapshot."""

    model_config = ConfigDict(extra="forbid")

    source_name: str
    source_type: str
    captured_at: datetime
    chain_ts: datetime
    aligned_bar_ts: datetime
    bar_age_seconds: int = Field(ge=0)
    event_ids: list[str] = Field(default_factory=list)
    event_lineage_keys: list[str] = Field(default_factory=list)
    precursor_lineage_keys: list[str] = Field(default_factory=list)
    sequence_id: str | None = None


class PreparedRuntimeSnapshot(BaseModel):
    """Runtime-ready snapshot distilled from aligned bars plus chain state."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    symbol: str
    aligned_bar_ts: datetime
    bar_age_seconds: int = Field(ge=0)
    spot_price: float
    prior_close_price: float | None = None
    session_open_price: float
    interval_volume_shares: float = Field(ge=0.0, default=0.0)
    cumulative_session_volume: float = Field(ge=0.0, default=0.0)
    session_vwap: float | None = None
    distance_to_vwap_pct: float | None = None
    vwap_slope_5m_pct: float | None = None
    opening_range_high_5m: float | None = None
    opening_range_low_5m: float | None = None
    opening_range_break_count: int = Field(ge=0, default=0)
    price_realised_vol_5m_pct: float | None = None
    price_realised_vol_15m_pct: float | None = None
    relative_volume_ratio: float | None = None
    rolling_range_5m_pct: float | None = None
    impulse_age_bars: int | None = None
    intraday_move_pct: float
    normalised_features: PreparedNormalisedFeatureSet | None = None
    promoted_regime_packet: PreparedRuntimeRegimePacket | None = None
    participation_baseline_packet: PreparedParticipationBaselinePacket | None = None
    prior_session_return_pct: float = 0.0
    front_expiry: datetime
    next_expiry: datetime
    front_dte: int = Field(ge=0)
    next_dte: int = Field(ge=0)
    front_atm_iv: VolFraction
    next_atm_iv: VolFraction
    put_call_skew: float
    gamma_pressure_score: float = Field(ge=0.0, le=1.0)
    call_put_imbalance: float = Field(ge=-1.0, le=1.0)
    oi_concentration: float = Field(ge=0.0, le=1.0)
    atm_straddle_value: float = Field(ge=0.0)
    front_realised_vol: VolFraction = Field(ge=0.0, default=0.0)
    next_realised_vol: VolFraction = Field(ge=0.0, default=0.0)
    snapshot_sequence_id: str | None = None
    snapshot_index: int = Field(ge=0, default=0)
    snapshot_count: int = Field(ge=1, default=1)
    snapshot_window_minutes: int | None = Field(default=None, ge=0)
    dominant_strike: float | None = None
    surface_anchor_to_spot_pct: float | None = None
    spot_to_pin_distance_pct: float = 0.0
    pin_progression_bias: str = "untracked"
    next_event_at: datetime | None = None
    live_event_snapshot: LiveEventSnapshot | None = None
    precursor_runtime_packet: PrecursorRuntimePacket | None = None
    desk_calendar_authority: DeskCalendarAuthorityPacket | None = Field(
        default=None, exclude_if=lambda value: value is None
    )
    call_oi_near_spot: float = Field(ge=0.0, default=0.0)
    put_oi_near_spot: float = Field(ge=0.0, default=0.0)
    front_volume_near_spot: float = Field(ge=0.0, default=0.0)
    next_volume_near_spot: float = Field(ge=0.0, default=0.0)
    nearby_strike_clusters: list[PreparedStrikeCluster] = Field(default_factory=list)
    repeated_snapshot_sequence: list[PreparedSequencePoint] = Field(default_factory=list)
    tenor_iv_curve: list[PreparedTenorPoint] = Field(default_factory=list)
    pin_progression_sequence: list[PreparedPinProgressionPoint] = Field(default_factory=list)
    lineage: PreparedRuntimeLineage


class PreparedRuntimeDataset(BaseModel):
    """Prepared runtime dataset retaining all snapshots and source provenance."""

    model_config = ConfigDict(extra="forbid")

    dataset_id: str
    symbol: str
    provenance: ProvenanceRecord
    snapshots: list[PreparedRuntimeSnapshot] = Field(default_factory=list)


class RuntimeSnapshotSanityReport(BaseModel):
    """Deterministic audit report for prepared runtime snapshots."""

    model_config = ConfigDict(extra="forbid")

    report_id: str
    symbol: str
    total_bars: int = Field(ge=0)
    total_chain_snapshots: int = Field(ge=0)
    prepared_snapshot_count: int = Field(ge=0)
    repeated_sequence_count: int = Field(ge=0)
    max_sequence_length: int = Field(ge=0)
    orphan_bar_count: int = Field(ge=0)
    orphan_chain_count: int = Field(ge=0)
    duplicate_bar_ts_count: int = Field(ge=0)
    duplicate_chain_ts_count: int = Field(ge=0)
    aligned_bar_coverage_pct: float = Field(ge=0.0, le=100.0)
    aligned_chain_coverage_pct: float = Field(ge=0.0, le=100.0)
    max_bar_age_seconds: int = Field(ge=0)
    monotonic_snapshot_timestamps: bool
    normalised_feature_snapshot_coverage_pct: float = Field(ge=0.0, le=100.0, default=0.0)
    event_linked_snapshot_count: int = Field(ge=0)
    reasons: list[str] = Field(default_factory=list)


class PreparedRuntimeFixturePack(BaseModel):
    """Deterministic fixture pack for repeated prepared-runtime ingestion tests."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str
    bundle: RealDataBundle
    prepared_dataset: PreparedRuntimeDataset
    sanity_report: RuntimeSnapshotSanityReport


class RealDataCognitionInputs(BaseModel):
    """Cognition-ready inputs derived from one prepared runtime snapshot.

    Purpose:
        Preserve the typed inputs consumed by the desk-cognition runtime plus
        checkpoint trace evidence for the upstream signal tranche.
    Inputs:
        One prepared-runtime snapshot translated into temporal, regime, and
        options-flow inputs.
    Outputs:
        One typed cognition-ingress packet.
    Side Effects:
        None.
    Failure Modes:
        Validation fails when any ingress packet or checkpoint observation is
        malformed.
    Checkpoints:
        Chain-to-cognition checkpoint observations are carried here so tests can
        inspect regime and participation wiring directly.
    """

    model_config = ConfigDict(extra="forbid")

    snapshot_ts: datetime
    lineage: PreparedRuntimeLineage
    temporal_input: TemporalContextInput
    regime_input: MarketRegimeContextInput | None = None
    options_flow_input: OptionsFlowContextInput
    normalised_features: PreparedNormalisedFeatureSet | None = None
    checkpoint_observations: list[CheckpointObservation] = Field(default_factory=list)


PreparedRuntimeRegimePacket.model_rebuild()
PreparedParticipationBaselinePacket.model_rebuild()
PreparedRuntimeSnapshot.model_rebuild()
PreparedRuntimeDataset.model_rebuild()
PreparedRuntimeFixturePack.model_rebuild()
RealDataCognitionInputs.model_rebuild()
