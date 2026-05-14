"""Deterministic real-data runtime preparation service.

This service validates real-data bundles, aligns chain snapshots with bars,
preserves provenance, prepares cognition-facing runtime snapshots, and emits a
sanity report that exposes sequencing coverage and data-quality gaps.
"""

from __future__ import annotations

import json
from bisect import bisect_right
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from math import sqrt
from pathlib import Path

from sqlalchemy import desc, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.config import Settings
from nvda_desk.schemas.dataset import (
    BarRecord,
    EventRecord,
    OptionChainSnapshot,
    OptionQuote,
    PreparedNormalisedFeatureSet,
    PreparedPinProgressionPoint,
    PreparedRuntimeDataset,
    PreparedRuntimeRegimePacket,
    PreparedRuntimeFixturePack,
    PreparedRuntimeLineage,
    PreparedRuntimeSnapshot,
    PreparedSequencePoint,
    PreparedStrikeCluster,
    PreparedTenorPoint,
    RealDataBundle,
    RuntimeSnapshotSanityReport,
)
from nvda_desk.db.models import Bar1m, Instrument
from nvda_desk.db.session import create_session_factory
from nvda_desk.services.event_store import EventStoreService
from nvda_desk.services.upstream_signal_ingress import build_participation_baseline_packet


class RealDataLoaderService:
    """Prepare aligned runtime snapshots from validated real-data bundles.

    Purpose:
        Turn validated bars plus option-chain snapshots into deterministic,
        provenance-preserving runtime datasets.
    Inputs:
        `RealDataBundle` objects loaded from JSON or in-memory mappings.
    Outputs:
        `PreparedRuntimeDataset`, `PreparedRuntimeFixturePack`, and
        `RuntimeSnapshotSanityReport` objects.
    Determinism:
        Uses stable bar-to-chain alignment, fixed near-spot windows, and stable
        sorting for snapshots, clusters, and tenor points.
    """


    def __init__(self, settings: Settings | None = None):
        self._settings = Settings() if settings is None else settings
        self._session_factory: sessionmaker[Session] | None = None
        if self._settings.database_url:
            self._session_factory = create_session_factory(self._settings.database_url)

    def load_json_bundle(self, path: Path) -> RealDataBundle:
        """Load one replay-ready dataset bundle from a JSON file."""

        raw = json.loads(path.read_text(encoding="utf-8"))
        return RealDataBundle.model_validate(raw)

    def load_mapping(self, payload: Mapping[str, object]) -> RealDataBundle:
        """Validate one in-memory dataset mapping as a replay-ready bundle."""

        return RealDataBundle.model_validate(payload)

    def load_fixture_pack(self, path: Path) -> PreparedRuntimeFixturePack:
        """Load one deterministic prepared-runtime fixture pack from disk."""

        raw = json.loads(path.read_text(encoding="utf-8"))
        return PreparedRuntimeFixturePack.model_validate(raw)

    def prepare_runtime_dataset(
        self,
        bundle: RealDataBundle,
        *,
        dataset_id: str | None = None,
        max_bar_age_minutes: int = 10,
    ) -> PreparedRuntimeDataset:
        """Prepare a provenance-preserving runtime dataset from one real-data bundle."""

        ordered_bars = sorted(bundle.bars, key=lambda bar: bar.ts)
        ordered_chains = sorted(bundle.option_chain_snapshots, key=lambda snapshot: snapshot.ts)
        if not ordered_bars:
            raise ValueError("real-data bundle must contain at least one bar")
        if not ordered_chains:
            raise ValueError("real-data bundle must contain at least one option-chain snapshot")

        bar_timestamps = [bar.ts for bar in ordered_bars]
        event_store = EventStoreService(bundle.events)
        session_open_price = float(ordered_bars[0].open)
        snapshots: list[PreparedRuntimeSnapshot] = []
        for chain in ordered_chains:
            aligned_bar = self._find_aligned_bar(
                chain_ts=chain.ts,
                ordered_bars=ordered_bars,
                bar_timestamps=bar_timestamps,
                max_bar_age_minutes=max_bar_age_minutes,
            )
            if aligned_bar is None:
                continue
            snapshots.append(
                self._prepare_one_snapshot(
                    bundle=bundle,
                    chain=chain,
                    aligned_bar=aligned_bar,
                    ordered_bars=ordered_bars,
                    ordered_chains=ordered_chains,
                    session_open_price=session_open_price,
                    event_store=event_store,
                )
            )

        resolved_dataset_id = dataset_id or self._dataset_id(bundle)
        return PreparedRuntimeDataset(
            dataset_id=resolved_dataset_id,
            symbol=bundle.provenance.symbol,
            provenance=bundle.provenance,
            snapshots=snapshots,
        )

    def build_fixture_pack(
        self, bundle: RealDataBundle, *, pack_id: str
    ) -> PreparedRuntimeFixturePack:
        """Build one deterministic prepared-runtime fixture pack from a raw bundle."""

        prepared_dataset = self.prepare_runtime_dataset(bundle, dataset_id=f"{pack_id}-dataset")
        sanity_report = self.build_runtime_snapshot_sanity_report(bundle, prepared_dataset)
        return PreparedRuntimeFixturePack(
            pack_id=pack_id,
            bundle=bundle,
            prepared_dataset=prepared_dataset,
            sanity_report=sanity_report,
        )

    def build_runtime_snapshot_sanity_report(
        self,
        bundle: RealDataBundle,
        prepared_dataset: PreparedRuntimeDataset,
    ) -> RuntimeSnapshotSanityReport:
        """Emit a deterministic sanity report for one prepared runtime dataset."""

        used_bar_ts = {snapshot.lineage.aligned_bar_ts for snapshot in prepared_dataset.snapshots}
        used_chain_ts = {snapshot.lineage.chain_ts for snapshot in prepared_dataset.snapshots}
        sequence_lengths = Counter(
            snapshot.snapshot_sequence_id
            for snapshot in prepared_dataset.snapshots
            if snapshot.snapshot_sequence_id is not None
        )
        duplicate_bar_ts_count = len(bundle.bars) - len({bar.ts for bar in bundle.bars})
        duplicate_chain_ts_count = len(bundle.option_chain_snapshots) - len(
            {snapshot.ts for snapshot in bundle.option_chain_snapshots}
        )
        max_bar_age_seconds = max(
            (snapshot.bar_age_seconds for snapshot in prepared_dataset.snapshots),
            default=0,
        )
        monotonic_snapshot_timestamps = all(
            left.ts <= right.ts
            for left, right in zip(
                prepared_dataset.snapshots, prepared_dataset.snapshots[1:], strict=False
            )
        )
        total_bars = len(bundle.bars)
        total_chains = len(bundle.option_chain_snapshots)
        normalised_feature_snapshot_coverage_pct = (
            round(
                (
                    sum(
                        1
                        for snapshot in prepared_dataset.snapshots
                        if snapshot.normalised_features is not None
                        and bool(snapshot.normalised_features.provenance)
                    )
                    / len(prepared_dataset.snapshots)
                )
                * 100.0,
                4,
            )
            if prepared_dataset.snapshots
            else 0.0
        )
        aligned_bar_coverage_pct = (
            round((len(used_bar_ts) / total_bars) * 100.0, 4) if total_bars else 0.0
        )
        aligned_chain_coverage_pct = (
            round((len(used_chain_ts) / total_chains) * 100.0, 4) if total_chains else 0.0
        )
        reasons = [
            f"prepared_snapshot_count:{len(prepared_dataset.snapshots)}",
            f"aligned_bar_coverage_pct:{aligned_bar_coverage_pct}",
            f"aligned_chain_coverage_pct:{aligned_chain_coverage_pct}",
            f"orphan_bar_count:{max(total_bars - len(used_bar_ts), 0)}",
            f"orphan_chain_count:{max(total_chains - len(used_chain_ts), 0)}",
            f"max_bar_age_seconds:{max_bar_age_seconds}",
            f"normalised_feature_snapshot_coverage_pct:{normalised_feature_snapshot_coverage_pct}",
        ]
        if duplicate_bar_ts_count:
            reasons.append(f"duplicate_bar_ts_count:{duplicate_bar_ts_count}")
        if duplicate_chain_ts_count:
            reasons.append(f"duplicate_chain_ts_count:{duplicate_chain_ts_count}")
        if not monotonic_snapshot_timestamps:
            reasons.append("snapshot_order:non_monotonic")
        return RuntimeSnapshotSanityReport(
            report_id=f"{prepared_dataset.dataset_id}-sanity",
            symbol=prepared_dataset.symbol,
            total_bars=total_bars,
            total_chain_snapshots=total_chains,
            prepared_snapshot_count=len(prepared_dataset.snapshots),
            repeated_sequence_count=sum(1 for length in sequence_lengths.values() if length >= 2),
            max_sequence_length=max(sequence_lengths.values(), default=0),
            orphan_bar_count=max(total_bars - len(used_bar_ts), 0),
            orphan_chain_count=max(total_chains - len(used_chain_ts), 0),
            duplicate_bar_ts_count=duplicate_bar_ts_count,
            duplicate_chain_ts_count=duplicate_chain_ts_count,
            aligned_bar_coverage_pct=aligned_bar_coverage_pct,
            aligned_chain_coverage_pct=aligned_chain_coverage_pct,
            max_bar_age_seconds=max_bar_age_seconds,
            monotonic_snapshot_timestamps=monotonic_snapshot_timestamps,
            normalised_feature_snapshot_coverage_pct=normalised_feature_snapshot_coverage_pct,
            event_linked_snapshot_count=sum(
                1 for snapshot in prepared_dataset.snapshots if snapshot.next_event_at is not None
            ),
            reasons=reasons,
        )

    def _prepare_one_snapshot(
        self,
        *,
        bundle: RealDataBundle,
        chain: OptionChainSnapshot,
        aligned_bar: BarRecord,
        ordered_bars: Sequence[BarRecord],
        ordered_chains: Sequence[OptionChainSnapshot],
        session_open_price: float,
        event_store: EventStoreService,
    ) -> PreparedRuntimeSnapshot:
        """Build one prepared runtime snapshot from one aligned chain and bar."""

        expiries = sorted({quote.expiry for quote in chain.quotes})
        if len(expiries) < 2:
            raise ValueError("option chain snapshot must contain at least two expiries")
        front_expiry, next_expiry = expiries[:2]
        front_quotes = [quote for quote in chain.quotes if quote.expiry == front_expiry]
        next_quotes = [quote for quote in chain.quotes if quote.expiry == next_expiry]
        front_call, front_put = self._nearest_call_put(front_quotes, aligned_bar.close)
        next_call, next_put = self._nearest_call_put(next_quotes, aligned_bar.close)
        bars_up_to_ts = [bar for bar in ordered_bars if bar.ts <= chain.ts]
        prior_close_price = self._prior_close_price(chain.ts, ordered_bars)
        session_vwap = self._session_vwap(bars_up_to_ts)
        vwap_5m_ago = self._session_vwap(bars_up_to_ts[:-5]) if len(bars_up_to_ts) > 5 else None
        opening_range_high, opening_range_low = self._opening_range_5m(ordered_bars)
        dominant_strike = self._dominant_strike(front_quotes)
        spot_to_pin_distance_pct = self._spot_to_pin_distance_pct(
            aligned_bar.close, dominant_strike
        )
        surface_anchor_to_spot_pct = self._surface_anchor_to_spot_pct(front_quotes, aligned_bar.close)
        repeated_sequence = self._build_repeated_snapshot_sequence(
            current_chain=chain,
            ordered_chains=ordered_chains,
            ordered_bars=ordered_bars,
        )
        pin_progression_sequence = [
            PreparedPinProgressionPoint(
                ts=point.ts, distance_to_pin_pct=point.spot_to_pin_distance_pct
            )
            for point in repeated_sequence
        ]
        pin_progression_bias = self._pin_progression_bias(pin_progression_sequence)
        front_realised_vol = round(
            self._realised_vol_proxy(chain.ts, ordered_bars, lookback_bars=6), 4
        )
        next_realised_vol = round(
            self._realised_vol_proxy(chain.ts, ordered_bars, lookback_bars=12), 4
        )
        live_event_snapshot = event_store.build_live_event_snapshot(
            requested_at=chain.ts, symbol=bundle.provenance.symbol
        )
        next_event = live_event_snapshot.next_event
        event_ids = [event.event_id for event in live_event_snapshot.nearby_events]
        bar_age_seconds = max(0, int((chain.ts - aligned_bar.ts).total_seconds()))
        distance_to_vwap_pct = None
        if session_vwap not in {None, 0.0}:
            assert session_vwap is not None
            distance_to_vwap_pct = round(
                self._pct_change(float(aligned_bar.close), float(session_vwap)), 4
            )
        vwap_slope_5m_pct = None
        if session_vwap not in {None, 0.0} and vwap_5m_ago not in {None, 0.0}:
            assert session_vwap is not None
            assert vwap_5m_ago is not None
            vwap_slope_5m_pct = round(self._pct_change(float(session_vwap), float(vwap_5m_ago)), 4)
        prior_session_return_pct = 0.0
        if prior_close_price not in {None, 0.0} and session_open_price is not None:
            assert prior_close_price is not None
            prior_session_return_pct = round(
                self._pct_change(float(session_open_price), float(prior_close_price)), 4
            )
        price_realised_vol_5m_pct = round(
            self._realised_vol_proxy(chain.ts, ordered_bars, lookback_bars=5), 4
        )
        price_realised_vol_15m_pct = round(
            self._realised_vol_proxy(chain.ts, ordered_bars, lookback_bars=15), 4
        )
        relative_volume_ratio = round(
            self._relative_volume_ratio(bars_up_to_ts, lookback_bars=5), 4
        )
        rolling_range_5m_pct = round(self._rolling_range_pct(bars_up_to_ts, lookback_bars=5), 4)
        intraday_move_pct = self._pct_change(float(aligned_bar.close), session_open_price)
        front_atm_iv = round(self._average_defined(front_call.iv, front_put.iv), 4)
        next_atm_iv = round(self._average_defined(next_call.iv, next_put.iv), 4)
        atm_straddle_value = round(self._mid(front_call) + self._mid(front_put), 4)
        front_volume_near_spot = round(self._near_spot_volume(front_quotes, aligned_bar.close), 4)
        next_volume_near_spot = round(self._near_spot_volume(next_quotes, aligned_bar.close), 4)
        normalised_features = self._normalised_features(
            intraday_move_pct=intraday_move_pct,
            rolling_range_5m_pct=rolling_range_5m_pct,
            distance_to_vwap_pct=distance_to_vwap_pct,
            price_realised_vol_15m_pct=price_realised_vol_15m_pct,
            front_atm_iv=front_atm_iv,
            next_atm_iv=next_atm_iv,
            front_realised_vol=front_realised_vol,
            next_realised_vol=next_realised_vol,
            atm_straddle_value=atm_straddle_value,
            spot_price=float(aligned_bar.close),
            front_volume_near_spot=front_volume_near_spot,
            total_front_volume=sum(float(quote.volume or 0.0) for quote in front_quotes),
        )
        return PreparedRuntimeSnapshot(
            ts=chain.ts,
            symbol=bundle.provenance.symbol,
            aligned_bar_ts=aligned_bar.ts,
            bar_age_seconds=bar_age_seconds,
            spot_price=float(aligned_bar.close),
            prior_close_price=prior_close_price,
            session_open_price=session_open_price,
            interval_volume_shares=float(aligned_bar.volume),
            cumulative_session_volume=round(sum(float(bar.volume) for bar in bars_up_to_ts), 4),
            session_vwap=round(session_vwap, 4) if session_vwap is not None else None,
            distance_to_vwap_pct=distance_to_vwap_pct,
            vwap_slope_5m_pct=vwap_slope_5m_pct,
            opening_range_high_5m=opening_range_high,
            opening_range_low_5m=opening_range_low,
            opening_range_break_count=self._opening_range_break_count(
                bars_up_to_ts, opening_range_high, opening_range_low
            ),
            price_realised_vol_5m_pct=price_realised_vol_5m_pct,
            price_realised_vol_15m_pct=price_realised_vol_15m_pct,
            relative_volume_ratio=relative_volume_ratio,
            rolling_range_5m_pct=rolling_range_5m_pct,
            impulse_age_bars=self._impulse_age_bars(bars_up_to_ts, threshold_pct=0.35),
            intraday_move_pct=intraday_move_pct,
            normalised_features=normalised_features,
            promoted_regime_packet=self._build_promoted_regime_packet(
                ts=chain.ts,
                bundle_symbol=bundle.provenance.symbol,
                nvda_level=float(aligned_bar.close),
                nvda_return_pct=intraday_move_pct,
                calendar_owner_present=False,
            ),
            participation_baseline_packet=build_participation_baseline_packet(
                ts=chain.ts,
                interval_volume_shares=float(aligned_bar.volume),
                relative_volume_ratio=relative_volume_ratio,
                settings=self._settings,
                calendar_owner_present=False,
            ),
            prior_session_return_pct=prior_session_return_pct,
            front_expiry=front_expiry,
            next_expiry=next_expiry,
            front_dte=max(0, (front_expiry.date() - chain.ts.date()).days),
            next_dte=max(0, (next_expiry.date() - chain.ts.date()).days),
            front_atm_iv=front_atm_iv,
            next_atm_iv=next_atm_iv,
            put_call_skew=round((front_put.iv or 0.0) - (front_call.iv or 0.0), 4),
            gamma_pressure_score=round(min(1.0, self._gamma_pressure_score(front_quotes)), 4),
            call_put_imbalance=round(self._call_put_imbalance(front_quotes), 4),
            oi_concentration=round(self._oi_concentration(front_quotes, aligned_bar.close), 4),
            atm_straddle_value=atm_straddle_value,
            front_realised_vol=front_realised_vol,
            next_realised_vol=next_realised_vol,
            snapshot_sequence_id=(
                chain.sequence.sequence_id if chain.sequence is not None else None
            ),
            snapshot_index=(chain.sequence.snapshot_index if chain.sequence is not None else 0),
            snapshot_count=(chain.sequence.snapshot_count if chain.sequence is not None else 1),
            snapshot_window_minutes=(
                chain.sequence.window_minutes if chain.sequence is not None else None
            ),
            dominant_strike=dominant_strike,
            spot_to_pin_distance_pct=spot_to_pin_distance_pct,
            surface_anchor_to_spot_pct=surface_anchor_to_spot_pct,
            pin_progression_bias=pin_progression_bias,
            next_event_at=next_event.event_at if next_event is not None else None,
            live_event_snapshot=live_event_snapshot,
            call_oi_near_spot=round(
                self._near_spot_oi(front_quotes, aligned_bar.close, side="call"), 4
            ),
            put_oi_near_spot=round(
                self._near_spot_oi(front_quotes, aligned_bar.close, side="put"), 4
            ),
            front_volume_near_spot=front_volume_near_spot,
            next_volume_near_spot=next_volume_near_spot,
            nearby_strike_clusters=self._nearby_strike_clusters(front_quotes, aligned_bar.close),
            repeated_snapshot_sequence=repeated_sequence,
            tenor_iv_curve=self._tenor_iv_curve(chain, aligned_bar.close),
            pin_progression_sequence=pin_progression_sequence,
            lineage=PreparedRuntimeLineage(
                source_name=bundle.provenance.source_name,
                source_type=bundle.provenance.source_type,
                captured_at=bundle.provenance.captured_at,
                chain_ts=chain.ts,
                aligned_bar_ts=aligned_bar.ts,
                bar_age_seconds=bar_age_seconds,
                event_ids=event_ids,
                event_lineage_keys=list(live_event_snapshot.lineage_keys),
                sequence_id=(chain.sequence.sequence_id if chain.sequence is not None else None),
            ),
        )

    def _build_promoted_regime_packet(
        self,
        *,
        ts: datetime,
        bundle_symbol: str,
        nvda_level: float,
        nvda_return_pct: float,
        calendar_owner_present: bool,
    ) -> PreparedRuntimeRegimePacket:
        """Build one bounded promoted regime packet from admitted live capture surfaces.

        Purpose:
            Read the admitted live capture path for cross-asset regime symbols and
            attach one non-synthetic promoted regime packet to each prepared
            runtime snapshot.
        Inputs:
            The runtime timestamp, NVDA live values from the aligned snapshot,
            and calendar-owner presence.
        Outputs:
            One `PreparedRuntimeRegimePacket`, including explicit fallback notes
            when external capture symbols are missing.
        Side Effects:
            Reads the configured runtime database when it is available.
        Failure Modes:
            Database access failures are captured as fallback notes rather than
            raising, so prepared-runtime generation remains deterministic.
        Checkpoints:
            `upstream_signal.regime_packet.capture_observed` exposes the live
            source coverage and fallback state.
        """

        fallback_notes: list[str] = []
        source_symbols: list[str] = [bundle_symbol]
        source_vendor = 'runtime_capture_database'
        observed_at = ts
        max_alignment_age_seconds = 0

        source_map = {
            'nq': ('QQQ', ['NQ', 'QQQ']),
            'es': ('SPY', ['ES', 'SPY']),
            'sox': ('SOXX', ['SOX', 'SOXX', 'SMH']),
            'vix': ('VIX', ['VIX']),
            'vvix': ('VVIX', ['VVIX']),
            'us10y': ('US10Y', ['US10Y']),
            'us2y': ('US2Y', ['US2Y']),
            'usdjpy': ('USDJPY', ['USDJPY']),
        }
        captured: dict[str, float | None] = {
            'nq_return_pct': None,
            'nq_level': None,
            'es_return_pct': None,
            'es_level': None,
            'sox_return_pct': None,
            'sox_level': None,
            'vix_level': None,
            'vvix_level': None,
            'us10y': None,
            'us2y': None,
            'usdjpy': None,
        }

        if self._session_factory is None:
            fallback_notes.append('capture_db_unconfigured')
        else:
            try:
                with self._session_factory() as session:
                    nq_bar, nq_symbol = self._latest_bar_for_any_symbol(session, source_map['nq'][1], ts)
                    if nq_bar is None:
                        fallback_notes.append('missing_source:nq_proxy')
                    else:
                        source_symbols.append(nq_symbol)
                        max_alignment_age_seconds = max(
                            max_alignment_age_seconds,
                            self._bar_age_seconds(ts, nq_bar.ts_utc),
                        )
                        captured['nq_level'] = float(nq_bar.close)
                        captured['nq_return_pct'] = self._session_return_pct(session, nq_bar.instrument_id, ts)

                    es_bar, es_symbol = self._latest_bar_for_any_symbol(session, source_map['es'][1], ts)
                    if es_bar is None:
                        fallback_notes.append('missing_source:es_proxy')
                    else:
                        source_symbols.append(es_symbol)
                        max_alignment_age_seconds = max(
                            max_alignment_age_seconds,
                            self._bar_age_seconds(ts, es_bar.ts_utc),
                        )
                        captured['es_level'] = float(es_bar.close)
                        captured['es_return_pct'] = self._session_return_pct(session, es_bar.instrument_id, ts)

                    sox_bar, sox_symbol = self._latest_bar_for_any_symbol(session, source_map['sox'][1], ts)
                    if sox_bar is None:
                        fallback_notes.append('missing_source:sox_proxy')
                    else:
                        source_symbols.append(sox_symbol)
                        max_alignment_age_seconds = max(
                            max_alignment_age_seconds,
                            self._bar_age_seconds(ts, sox_bar.ts_utc),
                        )
                        captured['sox_level'] = float(sox_bar.close)
                        captured['sox_return_pct'] = self._session_return_pct(session, sox_bar.instrument_id, ts)

                    for key in ('vix', 'vvix', 'us10y', 'us2y', 'usdjpy'):
                        bar, symbol = self._latest_bar_for_any_symbol(session, source_map[key][1], ts)
                        if bar is None:
                            fallback_notes.append(f'missing_source:{key}')
                            continue
                        source_symbols.append(symbol)
                        max_alignment_age_seconds = max(
                            max_alignment_age_seconds,
                            self._bar_age_seconds(ts, bar.ts_utc),
                        )
                        captured_key = 'vix_level' if key == 'vix' else 'vvix_level' if key == 'vvix' else key
                        captured[captured_key] = float(bar.close)
            except OperationalError:
                fallback_notes.append('capture_db_unavailable')
            except Exception as exc:
                fallback_notes.append(f'capture_db_error:{type(exc).__name__}')

        source_symbols = sorted(set(source_symbols))
        if len(source_symbols) == 1:
            source_vendor = 'runtime_capture_missing_external_sources'
        completeness_state = (
            'complete_for_live_ingress'
            if all(
                value is not None
                for value in (
                    captured['nq_return_pct'],
                    captured['es_return_pct'],
                    captured['sox_return_pct'],
                    captured['vix_level'],
                    captured['vvix_level'],
                    captured['us10y'],
                    captured['us2y'],
                    captured['usdjpy'],
                )
            )
            else 'regime_core_only'
        )
        alignment_state = 'aligned_same_bucket' if not fallback_notes else 'aligned_with_capture_fallbacks'
        from nvda_desk.services.upstream_signal_checkpointing import (  # local import avoids cycle noise
            CHECKPOINT_REGIME_PACKET_CAPTURE_OBSERVED,
            checkpoint_observation,
        )
        packet = PreparedRuntimeRegimePacket(
            source_family='prepared_runtime_live_capture',
            source_symbols=source_symbols,
            source_vendor=source_vendor,
            observed_at=observed_at,
            aligned_to_runtime_ts=ts,
            alignment_age_seconds=max_alignment_age_seconds,
            alignment_state=alignment_state,
            calendar_owner=(
                'financial_calendar_reference_bundle'
                if calendar_owner_present
                else 'session_clock_fallback'
            ),
            nvda_return_pct=round(nvda_return_pct, 4),
            nq_return_pct=self._round_or_none(captured['nq_return_pct']),
            nq_level=self._round_or_none(captured['nq_level']),
            es_return_pct=self._round_or_none(captured['es_return_pct']),
            es_level=self._round_or_none(captured['es_level']),
            sox_return_pct=self._round_or_none(captured['sox_return_pct']),
            sox_level=self._round_or_none(captured['sox_level']),
            vix_level=self._round_or_none(captured['vix_level']),
            vvix_level=self._round_or_none(captured['vvix_level']),
            us10y=self._round_or_none(captured['us10y']),
            us2y=self._round_or_none(captured['us2y']),
            usdjpy=self._round_or_none(captured['usdjpy']),
            completeness_state=completeness_state,
            fallback_notes=fallback_notes,
        )
        packet.checkpoint_observations.append(
            checkpoint_observation(
                checkpoint_name=CHECKPOINT_REGIME_PACKET_CAPTURE_OBSERVED,
                input_snapshot={
                    'runtime_ts': ts.isoformat(),
                    'bundle_symbol': bundle_symbol,
                    'calendar_owner_present': calendar_owner_present,
                },
                output_snapshot={
                    'source_symbols': source_symbols,
                    'completeness_state': packet.completeness_state,
                    'fallback_notes': fallback_notes,
                    'nq_level_present': packet.nq_level is not None,
                    'es_level_present': packet.es_level is not None,
                    'sox_level_present': packet.sox_level is not None,
                    'vix_level_present': packet.vix_level is not None,
                    'vvix_level_present': packet.vvix_level is not None,
                    'us10y_present': packet.us10y is not None,
                    'us2y_present': packet.us2y is not None,
                    'usdjpy_present': packet.usdjpy is not None,
                },
                timestamp=ts,
            )
        )
        return packet

    def _latest_bar_for_any_symbol(
        self,
        session: Session,
        candidates: list[str],
        ts: datetime,
    ) -> tuple[Bar1m | None, str | None]:
        for symbol in candidates:
            instrument = session.scalar(select(Instrument).where(Instrument.symbol == symbol))
            if instrument is None:
                continue
            row = session.scalar(
                select(Bar1m)
                .where(Bar1m.instrument_id == instrument.id)
                .where(Bar1m.ts_utc <= ts)
                .order_by(desc(Bar1m.ts_utc))
                .limit(1)
            )
            if row is not None:
                return row, symbol
        return None, None

    def _session_return_pct(self, session: Session, instrument_id: int, ts: datetime) -> float | None:
        first_bar = session.scalar(
            select(Bar1m)
            .where(Bar1m.instrument_id == instrument_id)
            .where(Bar1m.ts_utc <= ts)
            .order_by(Bar1m.ts_utc)
            .limit(1)
        )
        latest_bar = session.scalar(
            select(Bar1m)
            .where(Bar1m.instrument_id == instrument_id)
            .where(Bar1m.ts_utc <= ts)
            .order_by(desc(Bar1m.ts_utc))
            .limit(1)
        )
        if first_bar is None or latest_bar is None or float(first_bar.open) == 0.0:
            return None
        return round(self._pct_change(float(latest_bar.close), float(first_bar.open)), 4)

    def _bar_age_seconds(self, requested_at: datetime, bar_ts: datetime) -> int:
        resolved = bar_ts if bar_ts.tzinfo is not None else bar_ts.replace(tzinfo=UTC)
        return max(0, int((requested_at - resolved).total_seconds()))

    def _round_or_none(self, value: float | None) -> float | None:
        return None if value is None else round(float(value), 4)

    def _find_aligned_bar(
        self,
        *,
        chain_ts: datetime,
        ordered_bars: Sequence[BarRecord],
        bar_timestamps: Sequence[datetime],
        max_bar_age_minutes: int,
    ) -> BarRecord | None:
        """Return the latest bar at or before one chain timestamp within tolerance."""

        index = bisect_right(bar_timestamps, chain_ts) - 1
        if index < 0:
            return None
        bar = ordered_bars[index]
        bar_age_seconds = (chain_ts - bar.ts).total_seconds()
        if bar_age_seconds < 0 or bar_age_seconds > max_bar_age_minutes * 60:
            return None
        return bar

    def _nearest_call_put(
        self, quotes: Sequence[OptionQuote], spot_price: float
    ) -> tuple[OptionQuote, OptionQuote]:
        """Return the nearest call and put quotes around spot."""

        calls = [quote for quote in quotes if quote.side == "call"]
        puts = [quote for quote in quotes if quote.side == "put"]
        if not calls or not puts:
            raise ValueError("each expiry must contain at least one call and one put")
        nearest_call = min(calls, key=lambda quote: abs(quote.strike - spot_price))
        nearest_put = min(puts, key=lambda quote: abs(quote.strike - spot_price))
        return nearest_call, nearest_put

    def _average_defined(self, left: float | None, right: float | None) -> float:
        """Average two possibly missing values while requiring at least one."""

        values = [value for value in (left, right) if value is not None]
        if not values:
            raise ValueError("expected at least one defined option field")
        return sum(values) / len(values)

    def _mid(self, quote: OptionQuote) -> float:
        """Return the midpoint for one quote-like object."""

        return (float(quote.bid) + float(quote.ask)) / 2.0

    def _gamma_pressure_score(self, quotes: Sequence[OptionQuote]) -> float:
        """Build a bounded gamma-pressure proxy from near-expiry quotes."""

        weighted_gamma = 0.0
        weighted_size = 0.0
        for quote in quotes:
            gamma = float(quote.gamma or 0.0)
            volume = float(quote.volume or 0.0)
            weighted_gamma += abs(gamma) * max(volume, 1.0)
            weighted_size += max(volume, 1.0)
        if weighted_size <= 0.0:
            return 0.0
        return min(1.0, weighted_gamma / weighted_size * 10.0)

    def _call_put_imbalance(self, quotes: Sequence[OptionQuote]) -> float:
        """Build a bounded front-expiry call/put volume imbalance."""

        call_volume = sum(float(quote.volume or 0.0) for quote in quotes if quote.side == "call")
        put_volume = sum(float(quote.volume or 0.0) for quote in quotes if quote.side == "put")
        total = call_volume + put_volume
        if total <= 0.0:
            return 0.0
        return (call_volume - put_volume) / total

    def _oi_concentration(self, quotes: Sequence[OptionQuote], spot_price: float) -> float:
        """Build a bounded OI concentration proxy around spot."""

        total_oi = sum(float(quote.oi or 0.0) for quote in quotes)
        if total_oi <= 0.0:
            return 0.0
        near_spot_oi = sum(
            float(quote.oi or 0.0)
            for quote in quotes
            if abs((float(quote.strike) - spot_price) / max(spot_price, 1.0)) <= 0.02
        )
        return near_spot_oi / total_oi

    def _near_spot_oi(
        self, quotes: Sequence[OptionQuote], spot_price: float, *, side: str
    ) -> float:
        """Return near-spot open interest for one side of the chain."""

        return sum(
            float(quote.oi or 0.0)
            for quote in quotes
            if quote.side == side
            and abs((float(quote.strike) - spot_price) / max(spot_price, 1.0)) <= 0.02
        )

    def _near_spot_volume(self, quotes: Sequence[OptionQuote], spot_price: float) -> float:
        """Return near-spot volume for one expiry slice."""

        return sum(
            float(quote.volume or 0.0)
            for quote in quotes
            if abs((float(quote.strike) - spot_price) / max(spot_price, 1.0)) <= 0.02
        )

    def _lawful_weight(self, quote: OptionQuote) -> float:
        """Return the lawful weight available for strike ranking."""

        return float(quote.oi or 0.0) + float(quote.volume or 0.0)

    def _dominant_strike(self, quotes: Sequence[OptionQuote]) -> float | None:
        """Return the dominant near-expiry strike by open interest and volume."""

        weighted_quotes = [quote for quote in quotes if self._lawful_weight(quote) > 0.0]
        if not weighted_quotes:
            return None
        dominant_quote = max(weighted_quotes, key=self._lawful_weight)
        return float(dominant_quote.strike)

    def _spot_to_pin_distance_pct(self, spot_price: float, dominant_strike: float | None) -> float:
        """Return the live distance from spot to the dominant strike."""

        if dominant_strike is None:
            return 0.0
        return round(abs((spot_price - dominant_strike) / max(spot_price, 1.0)) * 100.0, 4)

    def _normalised_features(
        self,
        *,
        intraday_move_pct: float,
        rolling_range_5m_pct: float,
        distance_to_vwap_pct: float | None,
        price_realised_vol_15m_pct: float,
        front_atm_iv: float,
        next_atm_iv: float,
        front_realised_vol: float,
        next_realised_vol: float,
        atm_straddle_value: float,
        spot_price: float,
        front_volume_near_spot: float,
        total_front_volume: float,
    ) -> PreparedNormalisedFeatureSet:
        """Build the bounded normalised prepared-runtime feature set."""

        provenance = {
            "intraday_move_vs_rolling_range_5m": ["intraday_move_pct", "rolling_range_5m_pct"],
            "distance_to_vwap_vs_rolling_range_5m": ["distance_to_vwap_pct", "rolling_range_5m_pct"],
            "intraday_move_vs_price_realised_vol_15m": ["intraday_move_pct", "price_realised_vol_15m_pct"],
            "front_iv_vs_front_realised_vol_ratio": ["front_atm_iv", "front_realised_vol"],
            "next_iv_vs_next_realised_vol_ratio": ["next_atm_iv", "next_realised_vol"],
            "atm_straddle_vs_spot_pct": ["atm_straddle_value", "spot_price"],
            "near_spot_front_volume_share": ["front_volume_near_spot", "front_expiry_total_volume"],
        }
        return PreparedNormalisedFeatureSet(
            intraday_move_vs_rolling_range_5m=self._safe_ratio(intraday_move_pct, rolling_range_5m_pct),
            distance_to_vwap_vs_rolling_range_5m=self._safe_ratio(distance_to_vwap_pct, rolling_range_5m_pct),
            intraday_move_vs_price_realised_vol_15m=self._safe_ratio(intraday_move_pct, price_realised_vol_15m_pct),
            front_iv_vs_front_realised_vol_ratio=self._safe_ratio(front_atm_iv, front_realised_vol),
            next_iv_vs_next_realised_vol_ratio=self._safe_ratio(next_atm_iv, next_realised_vol),
            atm_straddle_vs_spot_pct=self._safe_ratio(atm_straddle_value * 100.0, spot_price),
            near_spot_front_volume_share=self._safe_ratio(front_volume_near_spot, total_front_volume),
            provenance=provenance,
        )

    def _safe_ratio(self, numerator: float | None, denominator: float | None) -> float | None:
        """Return one bounded ratio while keeping missing or zero denominators explicit."""

        if numerator is None or denominator is None or abs(denominator) <= 1e-9:
            return None
        return round(float(numerator) / float(denominator), 4)

    def _build_repeated_snapshot_sequence(
        self,
        *,
        current_chain: OptionChainSnapshot,
        ordered_chains: Sequence[OptionChainSnapshot],
        ordered_bars: Sequence[BarRecord],
    ) -> list[PreparedSequencePoint]:
        """Build repeated-snapshot progression points for one chain sequence."""

        related_chains = self._related_chains(current_chain, ordered_chains)
        ordered_bar_ts = [bar.ts for bar in ordered_bars]
        points: list[PreparedSequencePoint] = []
        for chain in related_chains:
            aligned_bar = self._find_aligned_bar(
                chain_ts=chain.ts,
                ordered_bars=ordered_bars,
                bar_timestamps=ordered_bar_ts,
                max_bar_age_minutes=10,
            )
            if aligned_bar is None:
                continue
            expiries = sorted({quote.expiry for quote in chain.quotes})
            if len(expiries) < 2:
                continue
            front_expiry, next_expiry = expiries[:2]
            front_quotes = [quote for quote in chain.quotes if quote.expiry == front_expiry]
            next_quotes = [quote for quote in chain.quotes if quote.expiry == next_expiry]
            front_call, front_put = self._nearest_call_put(front_quotes, aligned_bar.close)
            next_call, next_put = self._nearest_call_put(next_quotes, aligned_bar.close)
            dominant_strike = self._dominant_strike(front_quotes)
            points.append(
                PreparedSequencePoint(
                    ts=chain.ts,
                    front_atm_iv=round(self._average_defined(front_call.iv, front_put.iv), 4),
                    next_atm_iv=round(self._average_defined(next_call.iv, next_put.iv), 4),
                    put_call_skew=round((front_put.iv or 0.0) - (front_call.iv or 0.0), 4),
                    gamma_pressure_score=round(
                        min(1.0, self._gamma_pressure_score(front_quotes)), 4
                    ),
                    spot_to_pin_distance_pct=self._spot_to_pin_distance_pct(
                        aligned_bar.close, dominant_strike
                    ),
                )
            )
        return points

    def _related_chains(
        self,
        current_chain: OptionChainSnapshot,
        ordered_chains: Sequence[OptionChainSnapshot],
    ) -> list[OptionChainSnapshot]:
        """Return the related repeated chain sequence for one chain snapshot."""

        if current_chain.sequence is None:
            return [current_chain]
        sequence_id = current_chain.sequence.sequence_id
        return [
            chain
            for chain in ordered_chains
            if chain.sequence is not None and chain.sequence.sequence_id == sequence_id
        ]

    def _tenor_iv_curve(
        self, chain: OptionChainSnapshot, spot_price: float
    ) -> list[PreparedTenorPoint]:
        """Build a deterministic IV tenor curve from one chain snapshot."""

        tenor_points: list[PreparedTenorPoint] = []
        for expiry in sorted({quote.expiry for quote in chain.quotes}):
            expiry_quotes = [quote for quote in chain.quotes if quote.expiry == expiry]
            call, put = self._nearest_call_put(expiry_quotes, spot_price)
            tenor_points.append(
                PreparedTenorPoint(
                    tenor_dte=max(0, (expiry.date() - chain.ts.date()).days),
                    atm_iv=round(self._average_defined(call.iv, put.iv), 4),
                )
            )
        return tenor_points

    def _surface_anchor_to_spot_pct(
        self, quotes: Sequence[OptionQuote], spot_price: float
    ) -> float | None:
        """Return the bounded near-spot premium anchor distance from live spot."""

        strike_totals: dict[float, dict[str, float]] = {}
        for quote in quotes:
            if abs((float(quote.strike) - spot_price) / max(spot_price, 1.0)) > 0.03:
                continue
            mid = self._mid(quote)
            if mid <= 0.0:
                continue
            bucket = strike_totals.setdefault(float(quote.strike), {"call": 0.0, "put": 0.0})
            if quote.side in bucket:
                bucket[quote.side] += mid
        weighted_pairs = [
            (strike, values["call"] + values["put"])
            for strike, values in strike_totals.items()
            if (values["call"] + values["put"]) > 0.0
        ]
        if not weighted_pairs:
            return None
        total_weight = sum(weight for _, weight in weighted_pairs)
        if total_weight <= 0.0:
            return None
        anchor_strike = sum(strike * weight for strike, weight in weighted_pairs) / total_weight
        return round(abs((spot_price - anchor_strike) / max(spot_price, 1.0)) * 100.0, 4)

    def _nearby_strike_clusters(
        self, quotes: Sequence[OptionQuote], spot_price: float
    ) -> list[PreparedStrikeCluster]:
        """Build deterministic nearby strike-cluster observations around spot."""

        nearby_quotes = [
            quote
            for quote in quotes
            if abs((float(quote.strike) - spot_price) / max(spot_price, 1.0)) <= 0.03
        ]
        weighted_quotes = [quote for quote in nearby_quotes if self._lawful_weight(quote) > 0.0]
        ordered_quotes = sorted(weighted_quotes, key=self._lawful_weight, reverse=True)
        clusters: list[PreparedStrikeCluster] = []
        for quote in ordered_quotes[:4]:
            clusters.append(
                PreparedStrikeCluster(
                    strike=float(quote.strike),
                    side=quote.side,
                    open_interest=float(quote.oi or 0.0),
                    volume=float(quote.volume or 0.0),
                    distance_to_spot_pct=round(
                        abs((float(quote.strike) - spot_price) / max(spot_price, 1.0)) * 100.0,
                        4,
                    ),
                )
            )
        return clusters

    def _pin_progression_bias(self, sequence: Sequence[PreparedPinProgressionPoint]) -> str:
        """Infer whether repeated snapshots are pinning in or releasing away."""

        if len(sequence) < 2:
            return "untracked"
        ordered = sorted(sequence, key=lambda point: point.ts)
        first = ordered[0].distance_to_pin_pct
        last = ordered[-1].distance_to_pin_pct
        if last < first - 0.1:
            return "pinning_in"
        if last > first + 0.1:
            return "releasing_from_pin"
        if last <= 0.35:
            return "pin_stable"
        return "pin_noise"

    def _next_event(self, ts: datetime, events: Sequence[EventRecord]) -> EventRecord | None:
        """Return the next event at or after one timestamp."""

        future_events = sorted(
            (event for event in events if event.event_at >= ts),
            key=lambda event: event.event_at,
        )
        return future_events[0] if future_events else None

    def _prior_close_price(self, ts: datetime, ordered_bars: Sequence[BarRecord]) -> float | None:
        """Return the prior-session close when the bundle spans multiple dates."""

        prior_bars = [bar for bar in ordered_bars if bar.ts.date() < ts.date()]
        if not prior_bars:
            return None
        return float(prior_bars[-1].close)

    def _session_vwap(self, bars: Sequence[BarRecord]) -> float | None:
        """Return a simple session VWAP built from bar typical prices."""

        total_volume = sum(float(bar.volume) for bar in bars)
        if total_volume <= 0.0:
            return None
        weighted_total = sum(
            (((float(bar.high) + float(bar.low) + float(bar.close)) / 3.0) * float(bar.volume))
            for bar in bars
        )
        return weighted_total / total_volume

    def _opening_range_5m(
        self, ordered_bars: Sequence[BarRecord]
    ) -> tuple[float | None, float | None]:
        """Return the first five-bar opening range for the current session."""

        if not ordered_bars:
            return None, None
        session_date = ordered_bars[0].ts.date()
        same_day = [bar for bar in ordered_bars if bar.ts.date() == session_date][:5]
        if not same_day:
            return None, None
        return round(max(float(bar.high) for bar in same_day), 4), round(
            min(float(bar.low) for bar in same_day), 4
        )

    def _opening_range_break_count(
        self,
        bars: Sequence[BarRecord],
        opening_range_high: float | None,
        opening_range_low: float | None,
    ) -> int:
        """Count bars that break the first five-bar opening range."""

        if opening_range_high is None or opening_range_low is None:
            return 0
        post_range = list(bars[5:])
        return sum(
            1
            for bar in post_range
            if float(bar.close) > opening_range_high or float(bar.close) < opening_range_low
        )

    def _relative_volume_ratio(self, bars: Sequence[BarRecord], *, lookback_bars: int) -> float:
        """Return current bar volume divided by recent average bar volume."""

        if not bars:
            return 0.0
        current = float(bars[-1].volume)
        baseline_window = [float(bar.volume) for bar in bars[-(lookback_bars + 1) : -1]]
        if not baseline_window:
            return 1.0
        baseline = sum(baseline_window) / len(baseline_window)
        if baseline <= 0.0:
            return 1.0
        return current / baseline

    def _rolling_range_pct(self, bars: Sequence[BarRecord], *, lookback_bars: int) -> float:
        """Return the recent high-low range as a percent of the latest close."""

        window = list(bars[-lookback_bars:])
        if not window:
            return 0.0
        highest = max(float(bar.high) for bar in window)
        lowest = min(float(bar.low) for bar in window)
        latest_close = float(window[-1].close)
        if latest_close <= 0.0:
            return 0.0
        return ((highest - lowest) / latest_close) * 100.0

    def _impulse_age_bars(self, bars: Sequence[BarRecord], *, threshold_pct: float) -> int | None:
        """Return bars since the last threshold-sized close-to-close impulse."""

        closes = [float(bar.close) for bar in bars]
        if len(closes) < 2:
            return None
        bars_since = 0
        for left, right in zip(reversed(closes[:-1]), reversed(closes[1:]), strict=False):
            move_pct = abs(((right / left) - 1.0) * 100.0) if left > 0.0 else 0.0
            if move_pct >= threshold_pct:
                return bars_since
            bars_since += 1
        return bars_since

    def _realised_vol_proxy(
        self, ts: datetime, ordered_bars: Sequence[BarRecord], *, lookback_bars: int
    ) -> float:
        """Build a simple deterministic realised-vol proxy from recent bars."""

        bars_up_to_ts = [bar for bar in ordered_bars if bar.ts <= ts]
        closes = [float(bar.close) for bar in bars_up_to_ts[-lookback_bars:]]
        if len(closes) < 2:
            return 0.0
        returns = [
            ((right / left) - 1.0) * 100.0
            for left, right in zip(closes, closes[1:], strict=False)
            if left > 0.0
        ]
        if not returns:
            return 0.0
        mean = sum(returns) / len(returns)
        variance = sum((value - mean) ** 2 for value in returns) / len(returns)
        return float(sqrt(variance))

    def _pct_change(self, value: float, base: float) -> float:
        """Return a bounded percentage change, or zero when the base is unusable."""

        if base == 0.0:
            return 0.0
        return round(((value / base) - 1.0) * 100.0, 4)

    def _dataset_id(self, bundle: RealDataBundle) -> str:
        """Return a deterministic dataset identifier for one bundle."""

        captured = bundle.provenance.captured_at.strftime("%Y%m%dT%H%M%SZ")
        return f"prepared-{bundle.provenance.symbol.lower()}-{captured}"
