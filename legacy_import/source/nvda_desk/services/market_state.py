from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import asc, desc, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.config import Settings
from nvda_desk.db.models import Bar1m, Instrument, OptionSnapshot
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.domain.temporal_state import TemporalSignalInput, TemporalStateClassifier
from nvda_desk.schemas.market import (
    Bar1mPayload,
    DerivedPrecursorField,
    IntradayBarsResponse,
    MarketSnapshotResponse,
    PrecursorContradictionClass,
    PrecursorFallbackDisposition,
    PrecursorFreshnessState,
    PrecursorPostureState,
    PrecursorRuntimePacket,
    PrecursorStitchingAuthorityPacket,
    PrecursorStitchingResult,
    PrecursorTimestampDiscipline,
    PrecursorVenueSlice,
    PrecursorVenueUniverse,
)
from nvda_desk.schemas.options import (
    OptionSnapshotPayload,
    OptionSurfaceResponse,
    OptionType,
)
from nvda_desk.schemas.session_clock import SessionClockFeaturePayload
from nvda_desk.schemas.temporal_surface import (
    SessionClockCompatibilityPayload,
    TemporalStateFeaturePayload,
)


class MarketStateService:
    def __init__(
        self,
        classifier: SessionClockClassifier,
        session_factory: sessionmaker[Session] | None = None,
        settings: Settings | None = None,
    ):
        self._classifier = classifier
        self._session_factory = session_factory
        self._temporal_classifier = TemporalStateClassifier(settings or Settings())

    def get_session_clock(self, ts: datetime) -> SessionClockFeaturePayload:
        state = self._classifier.classify(ts)
        return SessionClockCompatibilityPayload.from_state(state)

    def get_temporal_state(self, ts: datetime) -> TemporalStateFeaturePayload:
        return TemporalStateFeaturePayload.from_state(
            self._temporal_classifier.classify(TemporalSignalInput(ts=ts))
        )

    def get_market_snapshot(self, symbol: str, ts: datetime) -> MarketSnapshotResponse:
        latest_bar = self._get_latest_bar(symbol=symbol, ts=ts)
        return MarketSnapshotResponse(
            symbol=symbol,
            requested_at=ts,
            temporal_state=self.get_temporal_state(ts),
            session_clock=self.get_session_clock(ts),
            latest_bar=latest_bar,
        )

    def stitch_precursor_context(
        self,
        *,
        requested_at: datetime,
        authority: PrecursorStitchingAuthorityPacket,
        slices: list[PrecursorVenueSlice],
    ) -> PrecursorStitchingResult:
        """Assemble precursor slices into one deterministic pre-runtime truth surface."""

        order_lookup = {venue: idx for idx, venue in enumerate(authority.venue_order)}
        sorted_slices = sorted(
            slices,
            key=lambda item: (
                order_lookup.get(item.venue, len(order_lookup)),
                item.session_close_at,
                item.observed_at,
            ),
        )
        active_slices: list[PrecursorVenueSlice] = []
        dropped_venues: list[PrecursorVenueUniverse] = []
        fallback_dispositions: list[PrecursorFallbackDisposition] = []
        notes: list[str] = []
        lineage_keys: list[str] = []

        for slice_ in sorted_slices:
            lineage_keys.extend(slice_.lineage_keys)
            notes.extend(slice_.notes)
            if self._timestamp_misaligned(requested_at=requested_at, slice_=slice_):
                dropped_venues.append(slice_.venue)
                fallback_dispositions.append(
                    PrecursorFallbackDisposition.REQUIRE_STAND_DOWN_PRESSURE
                )
                notes.append(f"timestamp_misalignment:{slice_.venue.value}")
                continue
            active_slices.append(slice_)
            fallback_dispositions.append(self._fallback_for_slice(slice_))

        missing_venues = [
            venue
            for venue in authority.venue_order
            if venue not in {slice_.venue for slice_ in active_slices}
        ]
        contradiction_class = self._contradiction_class(active_slices)
        posture_state = self._posture_state(
            active_slices=active_slices,
            contradiction_class=contradiction_class,
            missing_venues=missing_venues,
        )
        if missing_venues:
            notes.extend(f"missing_venue:{venue.value}" for venue in missing_venues)
        if contradiction_class is not PrecursorContradictionClass.NONE:
            notes.append(f"contradiction_class:{contradiction_class.value}")

        return PrecursorStitchingResult(
            requested_at=requested_at,
            stitched_order=[slice_.venue for slice_ in active_slices],
            active_slices=active_slices,
            missing_venues=missing_venues,
            dropped_venues=dropped_venues,
            fallback_dispositions=fallback_dispositions,
            contradiction_class=contradiction_class,
            posture_state=posture_state,
            lineage_keys=sorted(set(lineage_keys)),
            notes=notes,
        )

    def to_precursor_runtime_packet(
        self, result: PrecursorStitchingResult
    ) -> PrecursorRuntimePacket:
        """Convert stitched precursor truth into the additive runtime packet shape."""

        raw_fields = sorted(
            {field for slice_ in result.active_slices for field in slice_.raw_values},
            key=lambda item: item.value,
        )
        derived_values = self._aggregate_derived_values(result.active_slices)
        derived_fields = sorted(derived_values, key=lambda item: item.value)
        return PrecursorRuntimePacket(
            requested_at=result.requested_at,
            stitched_order=result.stitched_order,
            active_venues=[slice_.venue for slice_ in result.active_slices],
            missing_venues=result.missing_venues,
            raw_fields=raw_fields,
            derived_fields=derived_fields,
            derived_values=derived_values,
            contradiction_class=result.contradiction_class,
            posture_state=result.posture_state,
            fallback_dispositions=result.fallback_dispositions,
            lineage_keys=result.lineage_keys,
            notes=result.notes,
        )

    def get_intraday_bars(self, symbol: str, ts: datetime, limit: int = 30) -> IntradayBarsResponse:
        bars = self._get_intraday_bars(symbol=symbol, ts=ts, limit=limit)
        return IntradayBarsResponse(symbol=symbol, requested_at=ts, bars=bars)

    def get_option_surface(
        self,
        *,
        symbol: str,
        as_of_date: date,
        requested_at: datetime,
        expiry: date | None = None,
        option_type: OptionType | None = None,
    ) -> OptionSurfaceResponse:
        snapshots = self._get_option_surface(
            symbol=symbol,
            as_of_date=as_of_date,
            expiry=expiry,
            option_type=option_type,
        )
        surface_expiry = expiry or (snapshots[0].expiry if snapshots else None)
        return OptionSurfaceResponse(
            symbol=symbol,
            requested_at=requested_at,
            as_of_date=as_of_date,
            expiry=surface_expiry,
            option_type=option_type,
            snapshots=snapshots,
        )


    def _aggregate_derived_values(
        self, active_slices: list[PrecursorVenueSlice]
    ) -> dict[DerivedPrecursorField, float]:
        aggregates: dict[DerivedPrecursorField, list[float]] = {}
        for slice_ in active_slices:
            for field, value in slice_.derived_values.items():
                aggregates.setdefault(field, []).append(float(value))
        result: dict[DerivedPrecursorField, float] = {}
        for field, values in aggregates.items():
            if field in {
                DerivedPrecursorField.CARRY_RISK_WARNING_SCORE,
                DerivedPrecursorField.FUTURES_CASH_DIVERGENCE_SCORE,
            }:
                aggregate = max(values, key=abs)
            else:
                aggregate = sum(values) / len(values)
            result[field] = round(aggregate, 4)
        return result

    def _get_latest_bar(self, symbol: str, ts: datetime) -> Bar1mPayload | None:
        bars = self._get_intraday_bars(symbol=symbol, ts=ts, limit=1)
        return bars[0] if bars else None

    def _get_intraday_bars(self, symbol: str, ts: datetime, limit: int) -> list[Bar1mPayload]:
        if self._session_factory is None:
            return []
        try:
            with self._session_factory() as session:
                stmt = (
                    select(Bar1m)
                    .join(Instrument)
                    .where(Instrument.symbol == symbol)
                    .where(Bar1m.ts_utc <= ts)
                    .order_by(desc(Bar1m.ts_utc))
                    .limit(limit)
                )
                rows = list(session.scalars(stmt))
        except OperationalError:
            return []
        rows.reverse()
        return [
            Bar1mPayload(
                ts_utc=(
                    row.ts_utc if row.ts_utc.tzinfo is not None else row.ts_utc.replace(tzinfo=UTC)
                ),
                open=row.open,
                high=row.high,
                low=row.low,
                close=row.close,
                volume=row.volume,
            )
            for row in rows
        ]

    def _get_option_surface(
        self,
        *,
        symbol: str,
        as_of_date: date,
        expiry: date | None,
        option_type: OptionType | None,
    ) -> list[OptionSnapshotPayload]:
        if self._session_factory is None:
            return []
        try:
            with self._session_factory() as session:
                instrument = session.scalar(select(Instrument).where(Instrument.symbol == symbol))
                if instrument is None:
                    return []
                chosen_expiry = expiry or self._infer_expiry(session, instrument.id, as_of_date)
                if chosen_expiry is None:
                    return []
                stmt = (
                    select(OptionSnapshot)
                    .where(OptionSnapshot.instrument_id == instrument.id)
                    .where(OptionSnapshot.as_of_date == as_of_date)
                    .where(OptionSnapshot.expiry == chosen_expiry)
                )
                if option_type is not None:
                    stmt = stmt.where(OptionSnapshot.option_type == option_type.value)
                rows = list(session.scalars(stmt.order_by(asc(OptionSnapshot.strike))))
        except OperationalError:
            return []
        return [self._to_option_payload(row) for row in rows]

    def _infer_expiry(self, session: Session, instrument_id: int, as_of_date: date) -> date | None:
        stmt = (
            select(OptionSnapshot.expiry)
            .where(OptionSnapshot.instrument_id == instrument_id)
            .where(OptionSnapshot.as_of_date == as_of_date)
            .where(OptionSnapshot.expiry.is_not(None))
            .order_by(asc(OptionSnapshot.expiry))
            .limit(1)
        )
        return session.scalar(stmt)

    def _to_option_payload(self, row: OptionSnapshot) -> OptionSnapshotPayload:
        return OptionSnapshotPayload(
            as_of_date=row.as_of_date,
            expiry=row.expiry,
            option_type=OptionType(row.option_type),
            strike=row.strike,
            bid=row.bid,
            ask=row.ask,
            last=row.last,
            volume=row.volume,
            open_interest=row.open_interest,
            iv=row.iv,
            delta=row.delta,
            gamma=row.gamma,
            delta_change=row.delta_change,
            provenance=row.provenance,
            confidence=row.confidence,
            source_document=row.source_document,
            source_pages=row.source_pages,
        )

    def _timestamp_misaligned(self, *, requested_at: datetime, slice_: PrecursorVenueSlice) -> bool:
        disciplines = {
            PrecursorTimestampDiscipline.REQUEST_TIME_MUST_NOT_PRECEDE_SOURCE_TIME,
            PrecursorTimestampDiscipline.NO_FORWARD_FILL_ACROSS_US_DECISION_WINDOW,
        }
        _ = disciplines  # keep lint honest about the explicit Gate 75 dependency.
        return slice_.session_close_at > requested_at or slice_.observed_at > requested_at

    def _fallback_for_slice(self, slice_: PrecursorVenueSlice) -> PrecursorFallbackDisposition:
        if slice_.freshness_state is PrecursorFreshnessState.CURRENT:
            return PrecursorFallbackDisposition.CONTINUE_NORMALLY
        if slice_.freshness_state is PrecursorFreshnessState.DEGRADED:
            return PrecursorFallbackDisposition.CONTINUE_WITH_DEGRADED_CONFIDENCE
        if slice_.freshness_state is PrecursorFreshnessState.STALE:
            return PrecursorFallbackDisposition.REQUIRE_STAND_DOWN_PRESSURE
        return PrecursorFallbackDisposition.CONTINUE_WITHOUT_VENUE

    def _contradiction_class(
        self, active_slices: list[PrecursorVenueSlice]
    ) -> PrecursorContradictionClass:
        if not active_slices:
            return PrecursorContradictionClass.BROAD_CROSS_VENUE_CONFLICT

        directional_signs = {
            1 if value > 0 else -1 if value < 0 else 0
            for slice_ in active_slices
            for field, value in slice_.derived_values.items()
            if field is DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE
        }
        if len({sign for sign in directional_signs if sign != 0}) > 1:
            return PrecursorContradictionClass.DIRECTIONAL_SPLIT

        futures_cash_divergence = any(
            field is DerivedPrecursorField.FUTURES_CASH_DIVERGENCE_SCORE and abs(value) >= 0.5
            for slice_ in active_slices
            for field, value in slice_.derived_values.items()
        )
        if futures_cash_divergence:
            return PrecursorContradictionClass.FUTURES_CASH_DIVERGENCE

        degraded_count = sum(
            slice_.freshness_state is not PrecursorFreshnessState.CURRENT
            for slice_ in active_slices
        )
        if degraded_count >= 2:
            return PrecursorContradictionClass.BROAD_CROSS_VENUE_CONFLICT
        return PrecursorContradictionClass.NONE

    def _posture_state(
        self,
        *,
        active_slices: list[PrecursorVenueSlice],
        contradiction_class: PrecursorContradictionClass,
        missing_venues: list[PrecursorVenueUniverse],
    ) -> PrecursorPostureState:
        aggregated = self._aggregate_derived_values(active_slices)
        precursor_pressure = aggregated.get(DerivedPrecursorField.PRECURSOR_PRESSURE_SCORE, 0.0)
        carry_warning = aggregated.get(DerivedPrecursorField.CARRY_RISK_WARNING_SCORE, 0.0)

        if contradiction_class in {
            PrecursorContradictionClass.TIMESTAMP_MISALIGNMENT,
            PrecursorContradictionClass.BROAD_CROSS_VENUE_CONFLICT,
        }:
            return PrecursorPostureState.UNRESOLVED_CONTEXT
        if contradiction_class is PrecursorContradictionClass.FUTURES_CASH_DIVERGENCE:
            return PrecursorPostureState.STAND_DOWN_PRESSURE
        if precursor_pressure <= -0.55 or carry_warning >= 0.75:
            return PrecursorPostureState.STAND_DOWN_PRESSURE
        if contradiction_class is PrecursorContradictionClass.DIRECTIONAL_SPLIT:
            return PrecursorPostureState.TIGHTENED_POSTURE
        if precursor_pressure <= -0.2 or carry_warning >= 0.45:
            return PrecursorPostureState.TIGHTENED_POSTURE
        if missing_venues or any(
            slice_.freshness_state is not PrecursorFreshnessState.CURRENT
            for slice_ in active_slices
        ):
            return PrecursorPostureState.DEGRADED_CONFIDENCE
        return PrecursorPostureState.NORMAL_CONFIDENCE
