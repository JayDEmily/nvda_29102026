from __future__ import annotations

from collections import defaultdict
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from nvda_desk.config import Settings
from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.schemas.events import (
    DeskEventClass,
    EventConfidenceTier,
    EventFreshnessState,
    EventMaterialityTier,
    EventQueryWindow,
    EventSemanticPhase,
    LiveEventSnapshot,
    NormalisedEventRecord,
    RawEventSourceObservation,
)
from nvda_desk.schemas.financial_calendar import (
    FinancialCalendarCrosswalkRecord,
    FinancialCalendarEntityScope,
    FinancialCalendarEventType,
    FinancialCalendarImportedBundle,
    FinancialCalendarImportedRecord,
    FinancialCalendarProjectionTarget,
)
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    PrecursorFreshnessState,
    PrecursorRuntimePacket,
    PrecursorSourceClass,
    PrecursorStitchingAuthorityPacket,
    PrecursorTimestampDiscipline,
    PrecursorVenueSlice,
    PrecursorVenueUniverse,
    RawPrecursorField,
)
from nvda_desk.schemas.session_clock import (
    CalendarClosureClass,
    DeskCalendarAuthorityPacket,
    SessionBridgeRule,
    SessionTemplate,
    TradingVenue,
    VenueSessionContract,
    VenueTimezone,
)
from nvda_desk.services.event_ingestion import EventIngestionService
from nvda_desk.services.event_store import EventStoreService
from nvda_desk.services.financial_calendar_import import FinancialCalendarImportService
from nvda_desk.services.financial_calendar_reference import financial_calendar_crosswalk
from nvda_desk.services.market_state import MarketStateService


class FinancialCalendarProjectionService:
    """Project checked-in financial-calendar records into canonical repo surfaces."""

    _VENUE_MAPPING: dict[str, TradingVenue] = {
        "NYSE": TradingVenue.NASDAQ_US,
        "NASDAQ_US_EQ": TradingVenue.NASDAQ_US,
        "US_OPTIONS": TradingVenue.NASDAQ_US,
        "JPX_CASH": TradingVenue.JPX_CASH,
        "HKEX_SECURITIES": TradingVenue.HKEX_CASH,
        "SSE_PROXY": TradingVenue.SSE_CASH,
        "SZSE": TradingVenue.SZSE_CASH,
        "CFFEX_INDEX_FUTURES": TradingVenue.CFFEX_INDEX_FUTURES,
    }
    _VENUE_TEMPLATE: dict[TradingVenue, SessionTemplate] = {
        TradingVenue.NASDAQ_US: SessionTemplate.US_EQUITY_CONTINUOUS,
        TradingVenue.JPX_CASH: SessionTemplate.JPX_SPLIT_SESSION,
        TradingVenue.HKEX_CASH: SessionTemplate.HKEX_SPLIT_SESSION_WITH_CAS,
        TradingVenue.SSE_CASH: SessionTemplate.MAINLAND_CHINA_SPLIT_SESSION,
        TradingVenue.SZSE_CASH: SessionTemplate.MAINLAND_CHINA_SPLIT_SESSION,
        TradingVenue.CFFEX_INDEX_FUTURES: SessionTemplate.INDEX_FUTURES_SPLIT_SESSION,
    }
    _VENUE_TIMEZONE: dict[TradingVenue, VenueTimezone] = {
        TradingVenue.NASDAQ_US: VenueTimezone.AMERICA_NEW_YORK,
        TradingVenue.JPX_CASH: VenueTimezone.ASIA_TOKYO,
        TradingVenue.HKEX_CASH: VenueTimezone.ASIA_HONG_KONG,
        TradingVenue.SSE_CASH: VenueTimezone.ASIA_SHANGHAI,
        TradingVenue.SZSE_CASH: VenueTimezone.ASIA_SHANGHAI,
        TradingVenue.CFFEX_INDEX_FUTURES: VenueTimezone.ASIA_SHANGHAI,
    }
    _PRECURSOR_VENUE_MAPPING: dict[str, PrecursorVenueUniverse] = {
        "JPX_CASH": PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
        "JPX_DERIVATIVES": PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
        "HKEX_SECURITIES": PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX,
        "STOCK_CONNECT_NORTHBOUND": PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX,
        "STOCK_CONNECT_SOUTHBOUND": PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX,
        "SSE_PROXY": PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX,
        "SZSE": PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX,
        "CFFEX_INDEX_FUTURES": PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX,
    }
    _SOURCE_CONFIDENCE_BY_STATUS: dict[str, tuple[EventFreshnessState, EventConfidenceTier]] = {
        "official_confirmed": (EventFreshnessState.CURRENT, EventConfidenceTier.AUTHORITATIVE),
        "estimated": (EventFreshnessState.CURRENT, EventConfidenceTier.PROVISIONAL),
        "pending": (EventFreshnessState.DEFERRED, EventConfidenceTier.PROVISIONAL),
    }

    def __init__(self, repo_root: Path | str):
        self._repo_root = Path(repo_root)
        self._import_service = FinancialCalendarImportService(self._repo_root)
        self._bundle = self._import_service.import_bundle()
        self._crosswalk = financial_calendar_crosswalk()
        self._market_state = MarketStateService(classifier=SessionClockClassifier(Settings()))

    @property
    def imported_bundle(self) -> FinancialCalendarImportedBundle:
        return self._bundle

    def project_desk_calendar_authority(self, *, session_date: date) -> DeskCalendarAuthorityPacket:
        venue_contracts: dict[TradingVenue, VenueSessionContract] = {}
        closure_classes: set[CalendarClosureClass] = set()
        bridge_rules: set[SessionBridgeRule] = set()
        expiry_notes: list[str] = []
        for record in self._bundle.imported_records:
            crosswalk = self._match_crosswalk(record)
            if crosswalk is None or FinancialCalendarProjectionTarget.DESK_CALENDAR_AUTHORITY not in crosswalk.projection_targets:
                continue
            if not (record.start_date <= session_date <= record.end_date):
                continue
            event_closure_classes = self._closure_classes_for_record(record)
            event_bridge_rules = self._bridge_rules_for_record(record)
            closure_classes.update(event_closure_classes)
            bridge_rules.update(event_bridge_rules)
            for venue_name in record.venues:
                venue = self._VENUE_MAPPING.get(venue_name)
                if venue is None:
                    continue
                existing = venue_contracts.get(venue)
                if existing is None:
                    existing = VenueSessionContract(
                        venue=venue,
                        timezone=self._VENUE_TIMEZONE[venue],
                        template=self._VENUE_TEMPLATE[venue],
                        trading_days=self._future_trading_days(session_date, venue, lookahead_days=5),
                    )
                updated_closures = sorted(
                    {*(existing.closure_classes), *event_closure_classes}, key=lambda item: item.value
                )
                updated_bridges = sorted(
                    {*(existing.bridge_rules), *event_bridge_rules}, key=lambda item: item.value
                )
                venue_contracts[venue] = existing.model_copy(
                    update={
                        "closure_classes": updated_closures,
                        "bridge_rules": updated_bridges,
                        "notes": [*existing.notes, record.title],
                    }
                )
            if record.event_type is FinancialCalendarEventType.MONTHLY_OPTIONS_EXPIRY:
                expiry_notes.append(record.title)
        return DeskCalendarAuthorityPacket(
            venues=sorted(venue_contracts.values(), key=lambda item: item.venue.value),
            closure_classes=sorted(closure_classes, key=lambda item: item.value),
            bridge_rules=sorted(bridge_rules, key=lambda item: item.value),
            expiry_interaction_notes=sorted(dict.fromkeys(expiry_notes)),
        )

    def project_raw_event_observations(self, *, symbol: str = "NVDA") -> list[RawEventSourceObservation]:
        observations: list[RawEventSourceObservation] = []
        for record in self._bundle.imported_records:
            crosswalk = self._match_crosswalk(record)
            if crosswalk is None or FinancialCalendarProjectionTarget.RAW_EVENT_INGESTION not in crosswalk.projection_targets:
                continue
            event_at, window_start_at, window_end_at = self._event_window_datetimes(record, crosswalk)
            freshness_state, confidence_tier = self._SOURCE_CONFIDENCE_BY_STATUS.get(
                record.source_status,
                (EventFreshnessState.CURRENT, EventConfidenceTier.CORROBORATED),
            )
            observations.append(
                RawEventSourceObservation(
                    source=crosswalk.supported_source,
                    source_class=crosswalk.source_class,
                    symbol=symbol,
                    event_id=record.event_id,
                    event_at=event_at,
                    event_type=crosswalk.event_subclass or record.event_type.value,
                    label=record.title,
                    event_class=crosswalk.event_class,
                    event_subclass=crosswalk.event_subclass,
                    semantic_phase=self._semantic_phase_for_record(record, crosswalk),
                    materiality_tier=crosswalk.materiality_tier,
                    layer_id=record.layer_id.value,
                    jurisdiction=record.jurisdiction,
                    venues=list(record.venues),
                    entities=list(record.entities),
                    runtime_tags=list(record.runtime_tags),
                    evaluation_tags=list(record.evaluation_tags),
                    source_status=record.source_status,
                    source_document=record.source_document,
                    repo_artifact_id=record.repo_artifact_id,
                    repo_artifact_path=record.repo_artifact_path,
                    import_lineage_key=record.import_lineage_key,
                    window_start_at=window_start_at,
                    window_end_at=window_end_at,
                    observed_at=event_at,
                    freshness_state=freshness_state,
                    confidence_tier=confidence_tier,
                    lineage_key=record.import_lineage_key,
                    notes=[*crosswalk.notes, record.notes_md],
                )
            )
        return sorted(observations, key=lambda item: (item.event_at, item.event_id))

    def project_canonical_event_records(self, *, symbol: str = "NVDA") -> list[NormalisedEventRecord]:
        observations = self.project_raw_event_observations(symbol=symbol)
        return EventIngestionService().normalise(observations)

    def build_live_event_snapshot(
        self,
        *,
        requested_at: datetime,
        symbol: str = "NVDA",
        lookback_minutes: int = 240,
        lookahead_minutes: int = 1440,
        minimum_materiality: EventMaterialityTier = EventMaterialityTier.POSTURE_RELEVANT,
    ) -> LiveEventSnapshot:
        store = EventStoreService(self.project_canonical_event_records(symbol=symbol))
        return store.build_live_event_snapshot(
            requested_at=requested_at,
            symbol=symbol,
            query_window=EventQueryWindow(
                lookback_minutes=lookback_minutes,
                lookahead_minutes=lookahead_minutes,
            ),
            minimum_materiality=minimum_materiality,
        )

    def project_precursor_runtime_packet(self, *, requested_at: datetime) -> PrecursorRuntimePacket:
        authority = PrecursorStitchingAuthorityPacket(
            venue_order=list(PrecursorVenueUniverse),
            timestamp_disciplines=list(PrecursorTimestampDiscipline),
        )
        slices = self._project_precursor_slices(requested_at=requested_at)
        result = self._market_state.stitch_precursor_context(
            requested_at=requested_at,
            authority=authority,
            slices=slices,
        )
        return self._market_state.to_precursor_runtime_packet(result)

    def _project_precursor_slices(self, *, requested_at: datetime) -> list[PrecursorVenueSlice]:
        requested_day = requested_at.date()
        grouped: dict[PrecursorVenueUniverse, list[FinancialCalendarImportedRecord]] = defaultdict(list)
        for record in self._bundle.imported_records:
            if record.layer_id.value != "layer_04_asia_precursor_venue_context":
                continue
            if not (record.start_date <= requested_day <= record.end_date):
                continue
            for venue_name in record.venues:
                universe = self._PRECURSOR_VENUE_MAPPING.get(venue_name)
                if universe is not None:
                    grouped[universe].append(record)

        cash_missing = {
            venue
            for venue in (
                PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX,
                PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX,
                PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX,
            )
            if any(self._record_closes_precursor(record) for record in grouped.get(venue, []))
        }
        slices: list[PrecursorVenueSlice] = []
        for universe in PrecursorVenueUniverse:
            records = grouped.get(universe, [])
            if any(self._record_closes_precursor(record) for record in records):
                continue
            half_day = any("half_day" in tag for record in records for tag in record.runtime_tags)
            holiday_open = any("holiday_trading_active" in tag for record in records for tag in record.runtime_tags)
            source_class = self._source_class_for_precursor_venue(universe)
            session_close_at = self._projected_precursor_close_at(requested_at=requested_at, venue=universe)
            observed_at = session_close_at + timedelta(minutes=5)
            directional = 0.25
            agreement = 0.8
            divergence = 0.0
            persistence = 0.3
            pressure = 0.2
            carry_warning = 0.0
            freshness = PrecursorFreshnessState.CURRENT
            notes = [record.title for record in records]
            if half_day:
                directional = 0.0
                agreement = 0.35
                persistence = 0.15
                pressure = -0.25
                carry_warning = 0.55
                freshness = PrecursorFreshnessState.DEGRADED
            if holiday_open:
                directional = 0.35
                agreement = 0.5
                persistence = 0.4
                pressure = 0.15
            if universe is PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX and cash_missing:
                divergence = 0.8
                pressure = -0.65
                carry_warning = 0.8
                notes.append("futures_cash_divergence_from_calendar_projection")
            slices.append(
                PrecursorVenueSlice(
                    venue=universe,
                    source_class=source_class,
                    session_close_at=session_close_at,
                    observed_at=observed_at,
                    freshness_state=freshness,
                    raw_values={RawPrecursorField.CLOSE_TIMESTAMP: session_close_at},
                    derived_values={
                        DerivedPrecursorField.DIRECTIONAL_COMPOSITE_SCORE: directional,
                        DerivedPrecursorField.CROSS_VENUE_AGREEMENT_SCORE: agreement,
                        DerivedPrecursorField.FUTURES_CASH_DIVERGENCE_SCORE: divergence,
                        DerivedPrecursorField.IMPULSE_PERSISTENCE_SCORE: persistence,
                        DerivedPrecursorField.PRECURSOR_PRESSURE_SCORE: pressure,
                        DerivedPrecursorField.CARRY_RISK_WARNING_SCORE: carry_warning,
                    },
                    lineage_keys=[record.import_lineage_key for record in records],
                    notes=notes,
                )
            )
        return slices

    def _source_class_for_precursor_venue(self, venue: PrecursorVenueUniverse) -> PrecursorSourceClass:
        if venue is PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX:
            return PrecursorSourceClass.INDEX_FUTURES
        return PrecursorSourceClass.CASH_EQUITY_INDEX

    def _projected_precursor_close_at(
        self, *, requested_at: datetime, venue: PrecursorVenueUniverse
    ) -> datetime:
        hour_by_venue = {
            PrecursorVenueUniverse.JPX_CASH_INDEX_COMPLEX: 6,
            PrecursorVenueUniverse.HKEX_CASH_INDEX_COMPLEX: 8,
            PrecursorVenueUniverse.MAINLAND_CHINA_CASH_INDEX_COMPLEX: 7,
            PrecursorVenueUniverse.CFFEX_INDEX_FUTURES_COMPLEX: 7,
        }
        close_at = requested_at.replace(
            hour=hour_by_venue.get(venue, 6), minute=0, second=0, microsecond=0
        )
        if close_at > requested_at:
            close_at -= timedelta(days=1)
        return close_at

    def _match_crosswalk(
        self, record: FinancialCalendarImportedRecord
    ) -> FinancialCalendarCrosswalkRecord | None:
        candidates = [
            item
            for item in self._crosswalk
            if item.bundle_event_type is record.event_type and item.layer_id is record.layer_id
        ]
        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0]
        entities = {entity.upper() for entity in record.entities}
        for candidate in candidates:
            if candidate.entity_scope is FinancialCalendarEntityScope.NVDA_ONLY and entities == {"NVDA"}:
                return candidate
            if (
                candidate.entity_scope is FinancialCalendarEntityScope.DIRECT_READTHROUGH_MEGA_CAP
                and entities
                and entities != {"NVDA"}
            ):
                return candidate
        return candidates[0]

    def _event_window_datetimes(
        self,
        record: FinancialCalendarImportedRecord,
        crosswalk: FinancialCalendarCrosswalkRecord,
    ) -> tuple[datetime, datetime, datetime]:
        timezone = ZoneInfo(record.timezone)
        if record.start_time_local is not None:
            start_local_time = time.fromisoformat(record.start_time_local)
        elif crosswalk.event_class is DeskEventClass.VENUE_SESSION:
            start_local_time = time(0, 0)
        else:
            start_local_time = time(8, 30)
        start_dt = datetime.combine(record.start_date, start_local_time, tzinfo=timezone)

        if record.end_time_local is not None:
            end_local_time = time.fromisoformat(record.end_time_local)
            end_dt = datetime.combine(record.end_date, end_local_time, tzinfo=timezone)
        elif crosswalk.event_class in {DeskEventClass.MACRO, DeskEventClass.POLICY}:
            end_dt = start_dt + timedelta(hours=4)
        elif crosswalk.event_class in {DeskEventClass.COMPANY, DeskEventClass.PEER_COMPANY}:
            end_dt = start_dt + timedelta(hours=16)
        elif crosswalk.event_class is DeskEventClass.EXPIRY:
            end_dt = start_dt + timedelta(hours=7)
        else:
            end_dt = datetime.combine(record.end_date, time(23, 59), tzinfo=timezone)
        event_at = start_dt if crosswalk.event_class is not DeskEventClass.VENUE_SESSION else end_dt
        return event_at, start_dt.astimezone(UTC), end_dt.astimezone(UTC)

    def _semantic_phase_for_record(
        self,
        record: FinancialCalendarImportedRecord,
        crosswalk: FinancialCalendarCrosswalkRecord,
    ) -> EventSemanticPhase:
        if crosswalk.event_class in {DeskEventClass.MACRO, DeskEventClass.POLICY, DeskEventClass.COMPANY, DeskEventClass.PEER_COMPANY, DeskEventClass.EXPIRY}:
            return EventSemanticPhase.PRICED_RISK
        if "cooling_off" in record.runtime_tags:
            return EventSemanticPhase.REALISED_REACTION
        return crosswalk.semantic_phase

    def _future_trading_days(
        self, session_date: date, venue: TradingVenue, *, lookahead_days: int
    ) -> list[str]:
        """Project a bounded list of upcoming trading days for one venue."""

        days: list[str] = []
        cursor = session_date
        while len(days) < lookahead_days:
            if self._day_is_open_for_venue(cursor, venue):
                days.append(cursor.isoformat())
            cursor += timedelta(days=1)
        return days

    def _day_is_open_for_venue(self, session_date: date, venue: TradingVenue) -> bool:
        """Return whether one venue should be treated as open on one calendar date."""

        if session_date.weekday() >= 5:
            return False
        venue_aliases = {name for name, mapped in self._VENUE_MAPPING.items() if mapped is venue}
        closure_classes: set[CalendarClosureClass] = set()
        for record in self._bundle.imported_records:
            if not (record.start_date <= session_date <= record.end_date):
                continue
            if not venue_aliases.intersection(record.venues):
                continue
            closure_classes.update(self._closure_classes_for_record(record))
        return CalendarClosureClass.FULL_HOLIDAY not in closure_classes

    def _closure_classes_for_record(
        self, record: FinancialCalendarImportedRecord
    ) -> list[CalendarClosureClass]:
        if record.event_type in {
            FinancialCalendarEventType.MARKET_HOLIDAY,
            FinancialCalendarEventType.JPX_CASH_HOLIDAY,
            FinancialCalendarEventType.HKEX_CASH_HOLIDAY,
            FinancialCalendarEventType.MAINLAND_CASH_HOLIDAY,
            FinancialCalendarEventType.STOCK_CONNECT_CLOSED,
            FinancialCalendarEventType.JPX_DERIVATIVES_HOLIDAY_CLOSED,
        }:
            return [CalendarClosureClass.FULL_HOLIDAY]
        if record.event_type in {
            FinancialCalendarEventType.MARKET_HALF_DAY,
            FinancialCalendarEventType.OPTIONS_HALF_DAY,
            FinancialCalendarEventType.STOCK_CONNECT_HALF_DAY,
        }:
            return [CalendarClosureClass.HALF_DAY]
        if record.event_type is FinancialCalendarEventType.HKEX_HALF_DAY:
            return [CalendarClosureClass.HOLIDAY_EVE_HALF_DAY]
        return []

    def _bridge_rules_for_record(
        self, record: FinancialCalendarImportedRecord
    ) -> list[SessionBridgeRule]:
        rules: list[SessionBridgeRule] = []
        runtime_tags = set(record.runtime_tags)
        evaluation_tags = set(record.evaluation_tags)
        if "carry_rules_tighten" in runtime_tags:
            rules.append(SessionBridgeRule.US_EARLY_CLOSE)
        if record.event_type is FinancialCalendarEventType.HKEX_HALF_DAY:
            rules.append(SessionBridgeRule.HK_HOLIDAY_EVE_HALF_DAY)
        if record.event_type in {
            FinancialCalendarEventType.JPX_CASH_HOLIDAY,
            FinancialCalendarEventType.HKEX_CASH_HOLIDAY,
            FinancialCalendarEventType.MAINLAND_CASH_HOLIDAY,
            FinancialCalendarEventType.STOCK_CONNECT_CLOSED,
        }:
            rules.append(SessionBridgeRule.PRECURSOR_NEXT_US_SESSION_ONLY)
        if (
            record.event_type is FinancialCalendarEventType.MONTHLY_OPTIONS_EXPIRY
            and "half_day_session" in evaluation_tags
        ):
            rules.append(SessionBridgeRule.EXPIRY_COLLIDES_WITH_SHORTENED_SESSION)
        return rules

    def _record_closes_precursor(self, record: FinancialCalendarImportedRecord) -> bool:
        return record.event_type in {
            FinancialCalendarEventType.JPX_CASH_HOLIDAY,
            FinancialCalendarEventType.HKEX_CASH_HOLIDAY,
            FinancialCalendarEventType.STOCK_CONNECT_CLOSED,
            FinancialCalendarEventType.MAINLAND_CASH_HOLIDAY,
            FinancialCalendarEventType.JPX_DERIVATIVES_HOLIDAY_CLOSED,
        }
