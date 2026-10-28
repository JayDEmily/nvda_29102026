"""M02 receipt-only public-source selection and subscribed-side book reconstruction.

No M00 internals are imported. All observations and controls enter through the
existing public reader; a native source profile is a versioned synthetic scope.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import fields, replace
from datetime import datetime
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import _native_codec as codec
from . import api as f
from ._native_profiles import SPECS
from ._record_store import RecordState

BRIEF = "5b777c5842b091f6dc4bef148970c4cf81b68864bd24f5a1633d392f38d96ead"
NAMESPACE = "neutral_market_measurement_truth/native-source/v1"
_TIME = "collector_receipt"
_DEPTH_ROLES = {"R185", "R187", "R188", "R190", "R192", "R193", "R194", "R195", "R196", "R197"}
_CONTROL_KINDS = {"error316", "error317", "gap", "reconnect", "restart"}

# Exact L01 helper recipe's separately identified incoming G2 synthetic epoch.
_g2 = deepcopy(SPECS["A4"])
_g2.update(
    profile_ref={"context_id": "native-receipt-controls", "version": 1},
    generation="STK-SMART-G2",
    ingestion_scope="STK1/SMART/G2",
    complete_from_utc="2026-10-20T12:40:00Z",
    warmup_observation_ids=["REC-HELPER-G2-B0", "REC-HELPER-G2-A0"],
    warmup_side_levels={"1": 1, "0": 1},
)
SPECS["G2"] = _g2


def _instant(text: str) -> datetime:
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    f._utc(value)
    return value


def _profiles() -> dict[f.VersionRefV1, f.NativeSourceProfileV1]:
    answer = {}
    for spec in SPECS.values():
        mappings = tuple(
            raw.RawSignalProjectionMappingV1(
                source["mapping_id"],
                source["version"],
                raw.RawSignalCatalogueId(rid),
                source["source_provider"],
                source["source_variant"],
                tuple(source["native_field_path"]),
                source["native_units"],
                tuple((key, tuple(path)) for key, path in source["selection_identity_field_paths"]),
            )
            for rid, source in spec["mappings"].items()
        )
        profile = f.NativeSourceProfileV1(
            f.VersionRefV1(**spec["profile_ref"]),
            spec["provider"],
            spec["variant"],
            spec["subject"],
            spec["request"],
            spec["generation"],
            spec["ingestion_scope"],
            spec["requested_exchange"],
            spec["security_type"],
            spec["right"],
            spec["contract_identity"],
            _TIME,
            _instant(spec["complete_from_utc"]),
            tuple(spec["warmup_observation_ids"]),
            tuple((int(side), count) for side, count in sorted(spec["warmup_side_levels"].items())),
            mappings,
            spec["maximum_observations"],
            f.VersionRefV1(**spec["source_context_ref"]),
        )
        answer[profile.ref] = profile
    return answer


PROFILES = _profiles()


def _spec(profile: f.NativeSourceProfileV1) -> dict:
    return next(
        spec
        for spec in SPECS.values()
        if spec["profile_ref"]
        == {"context_id": profile.ref.context_id, "version": profile.ref.version}
    )


def _page_items(call: Callable[[str | None], object], *, cap: int, expected_page: type) -> tuple:
    items = []
    cursor = None
    seen = set()
    for _ in range(100):
        page = call(cursor)
        if type(page) is not expected_page or type(page.items) is not tuple:
            raise ValueError("public history page has wrong type")
        if page.next_cursor is not None and (
            type(page.next_cursor) is not str
            or not page.next_cursor
            or not page.items
            or page.next_cursor in seen
        ):
            raise ValueError("public history cursor failed progress")
        items.extend(page.items)
        if len(items) > cap:
            raise ValueError("public history exceeds admitted bound")
        if page.next_cursor is None:
            return tuple(items)
        seen.add(page.next_cursor)
        cursor = page.next_cursor
    raise ValueError("public history exceeds page bound")


def _native_path(record: Mapping, path: tuple[str, ...]) -> object:
    value: object = record
    for key in path:
        if not isinstance(value, Mapping) or key not in value:
            return None
        value = value[key]
    return value


def _contract_native(value: object) -> object:
    if type(value) is dict and set(value) == {"native_type", "value"}:
        kind, item = value["native_type"], value["value"]
        if kind == "NoneType":
            return None
        if kind == "int":
            return int(item)
        if kind == "str":
            return item
        raise ValueError("unsupported fixed contract identity type")
    if type(value) is dict:
        return {k: _contract_native(v) for k, v in value.items()}
    return value


def _observation_matches(
    item: raw.RawObservationOccurrenceV1, profile: f.NativeSourceProfileV1, cutoff: datetime
) -> bool:
    if type(item) is not raw.RawObservationOccurrenceV1:
        raise TypeError("public observation type mismatch")
    collector = _native_path(item.native_record, ("_collector",))
    spec = _spec(profile)
    return bool(type(collector) is dict or isinstance(collector, Mapping)) and (
        item.source_provider.value == profile.provider
        and item.source_variant == profile.variant
        and item.subject_instrument == profile.subject_instrument
        and item.received_ts_utc <= cutoff
        and item.received_ts_utc >= profile.complete_from_utc
        and item.source_temporal_kind == "receipt_only"
        and item.source_timestamp_raw is None
        and item.source_timezone_native is None
        and item.ingestion_sequence_scope.value == profile.ingestion_scope
        and _native_path(item.native_record, ("_collector", "request")) == profile.request
        and _native_path(item.native_record, ("_collector", "requested_exchange"))
        == profile.requested_exchange
        and _native_path(item.native_record, ("_collector", "generation")) == profile.generation
        and _native_path(item.native_record, ("_collector", "scenario_id")) == spec["scenario_id"]
        and _native_path(item.native_record, ("_collector", "contract_spec"))
        == _contract_native(spec["contract_spec"])
        and item.native_identifier == profile.subject_instrument
    )


def _controls(
    observations: tuple[raw.RawObservationOccurrenceV1, ...],
    profile: f.NativeSourceProfileV1,
    cutoff: datetime,
) -> tuple[f.NativeControlLineageV1, ...]:
    result = []
    ids: set[str] = set()
    for item in observations:
        if (
            type(item) is not raw.RawObservationOccurrenceV1
            or item.source_provider.value != profile.provider
            or item.source_variant != profile.variant
            or item.subject_instrument != profile.subject_instrument
            or item.received_ts_utc > cutoff
        ):
            raise ValueError("public control source mismatch")
        native = _native_path(item.native_record, ("_collector", "control"))
        if native is None:
            continue
        if not isinstance(native, Mapping) or set(native) != {
            "kind",
            "origin",
            "request",
            "generation_before",
            "generation_after",
            "invalidates",
            "schema_version",
        }:
            raise ValueError("malformed relevant control envelope")
        kind = native["kind"]
        if (
            kind not in _CONTROL_KINDS
            or native["schema_version"] != "m00-control-envelope/1"
            or native["request"] != profile.request
            or type(native["invalidates"]) is not bool
            or native["invalidates"] is not True
            or native["origin"]
            != ("provider_callback" if kind.startswith("error") else "collector_control")
            or _native_path(item.native_record, ("_collector", "requested_exchange"))
            != profile.requested_exchange
            or type(native["generation_before"]) is not str
            or type(native["generation_after"]) is not str
            or (
                native["generation_before"] != profile.generation
                and native["generation_after"] != profile.generation
            )
        ):
            raise ValueError("unadmitted control semantics")
        if item.observation_occurrence_id.value in ids:
            raise ValueError("duplicate control identity")
        ids.add(item.observation_occurrence_id.value)
        result.append(
            f.NativeControlLineageV1(
                item,
                kind,
                native["request"],
                native["generation_before"],
                native["generation_after"],
                native["invalidates"],
            )
        )
    return tuple(result)


def _fetch_observations(
    reader: f.NativeRawReaderV1, profile: f.NativeSourceProfileV1, cutoff: datetime
) -> tuple[raw.RawObservationOccurrenceV1, ...]:
    base = (
        (("_collector", "request"), profile.request),
        (("_collector", "requested_exchange"), profile.requested_exchange),
    )
    variants = (
        (*base, (("_collector", "generation"), profile.generation)),
        (*base, (("_collector", "control", "generation_after"), profile.generation)),
    )
    merged: dict[str, raw.RawObservationOccurrenceV1] = {}
    for selectors in variants:
        records = _page_items(
            lambda cursor, selectors=selectors: reader.list_raw_observation_history(
                subject_instrument=profile.subject_instrument,
                source_provider=profile.provider,
                source_variant=profile.variant,
                received_at_or_before_utc=cutoff,
                native_identity_selectors=selectors,
                limit=1,
                cursor=cursor,
            ),
            cap=profile.maximum_observations,
            expected_page=raw.RawObservationHistoryPageV1,
        )
        for item in records:
            if type(item) is not raw.RawObservationOccurrenceV1:
                raise ValueError("public history observation type mismatch")
            key = item.observation_occurrence_id.value
            if key in merged and codec.canonical(merged[key]) != codec.canonical(item):
                raise ValueError("conflicting duplicate public observation")
            merged[key] = item
    if len(merged) > profile.maximum_observations:
        raise ValueError("union of public histories exceeds bound")
    return tuple(merged.values())


def _fetch_lines(
    reader: f.NativeRawReaderV1,
    profile: f.NativeSourceProfileV1,
    observations: tuple[raw.RawObservationOccurrenceV1, ...],
    cutoff: datetime,
) -> tuple[f.NativeRawLineageV1, ...]:
    by_id = {o.observation_occurrence_id.value: o for o in observations}
    lines = []
    seen = set()
    for mapping in profile.projection_mappings:
        rid = mapping.raw_signal_catalogue_id.value
        items = _page_items(
            lambda cursor, mapping=mapping: reader.list_projected_raw_history(
                mapping.raw_signal_catalogue_id,
                mappings=(mapping,),
                subject_instrument=profile.subject_instrument,
                received_at_or_before_utc=cutoff,
                event_at_or_before_utc=None,
                limit=1,
                cursor=cursor,
            ),
            cap=profile.maximum_observations,
            expected_page=raw.ProjectedRawHistoryPageV1,
        )
        for item in items:
            if type(item) is not raw.ProjectedRawValueV1:
                raise ValueError("public projection type mismatch")
            oid = item.observation_occurrence_id.value
            identity = item.selection_identity
            if (
                identity is None
                or identity.value_for("generation") != profile.generation
                or identity.value_for("request") != profile.request
                or identity.value_for("requested_exchange") != profile.requested_exchange
                or identity.value_for("scenario_id") != _spec(profile)["scenario_id"]
                or identity.value_for("subject") != profile.subject_instrument
            ):
                continue
            if oid not in by_id:
                raise ValueError("projected observation lacks public identity facts")
            observation = by_id[oid]
            if not _observation_matches(observation, profile, cutoff):
                continue
            if (
                item.raw_signal_catalogue_id != mapping.raw_signal_catalogue_id
                or item.projection_mapping_id != mapping.mapping_id
                or item.projection_mapping_version != mapping.version
                or item.native_field_path != mapping.native_field_path
                or item.native_units != mapping.native_units
                or item.source_provider != profile.provider
                or item.source_variant != profile.variant
                or item.subject_instrument != profile.subject_instrument
                or item.source_temporal_kind != "receipt_only"
                or item.source_timestamp_raw is not None
                or item.source_timezone_native is not None
                or item.received_ts_utc != observation.received_ts_utc
                or item.ingestion_sequence != observation.ingestion_sequence
                or item.ingestion_sequence_scope != observation.ingestion_sequence_scope
                or identity is None
                or identity.value_for("generation") != profile.generation
                or identity.value_for("request") != profile.request
                or identity.value_for("requested_exchange") != profile.requested_exchange
                or identity.value_for("scenario_id") != _spec(profile)["scenario_id"]
                or identity.value_for("subject") != profile.subject_instrument
            ):
                raise ValueError("projection does not preserve exact public source")
            value = item.native_value
            expected_type = (
                int
                if rid in {"R185", "R187", "R188", "R192", "R194", "R195"}
                else str
                if rid == "R193"
                else datetime
                if rid == "R001"
                else Decimal
            )
            if type(value) is not expected_type or (
                type(value) is Decimal and not value.is_finite()
            ):
                raise ValueError("projected native value has wrong exact type")
            if rid == "R001" and value != item.received_ts_utc:
                raise ValueError("collector receipt role differs from envelope")
            key = oid, rid
            if key in seen:
                raise ValueError("duplicate role within one occurrence")
            seen.add(key)
            lines.append(
                f.NativeRawLineageV1(
                    rid,
                    oid,
                    f.VersionRefV1(mapping.mapping_id, mapping.version),
                    item,
                    cast(datetime | int | str | Decimal, value),
                    _TIME,
                    None,
                    item.received_ts_utc,
                )
            )
    return tuple(lines)


def _replay(
    profile: f.NativeSourceProfileV1,
    lines: tuple[f.NativeRawLineageV1, ...],
    controls: tuple[f.NativeControlLineageV1, ...],
) -> tuple[f.NativeBookRowV1, ...]:
    if profile.ref.context_id == "native-receipt-controls" and not any(
        c.kind == "restart"
        and c.generation_before == "STK-SMART-G1"
        and c.generation_after == "STK-SMART-G2"
        for c in controls
    ):
        raise ValueError("incoming G2 restart boundary absent")
    groups: dict[str, dict[str, f.NativeRawLineageV1]] = {}
    for line in lines:
        group = groups.setdefault(line.observation_occurrence_id, {})
        if line.raw_signal_id in group:
            raise ValueError("duplicate source role")
        group[line.raw_signal_id] = line
    if not groups:
        raise ValueError("no selected public observations")
    events = []
    for oid, group in groups.items():
        first = next(iter(group.values())).projection
        if any(
            (
                line.projection.received_ts_utc != first.received_ts_utc
                or line.projection.ingestion_sequence != first.ingestion_sequence
                or line.projection.ingestion_sequence_scope != first.ingestion_sequence_scope
                or line.projection.selection_identity != first.selection_identity
            )
            for line in group.values()
        ):
            raise ValueError("mixed callback group")
        events.append(
            (
                first.received_ts_utc,
                first.ingestion_sequence_scope.value,
                first.ingestion_sequence,
                oid,
                group,
                None,
            )
        )
    for control in controls:
        item = control.observation
        events.append(
            (
                item.received_ts_utc,
                item.ingestion_sequence_scope.value,
                item.ingestion_sequence,
                item.observation_occurrence_id.value,
                None,
                control,
            )
        )
    events.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    # Qualify the complete causal order before any positional or warm-up replay.
    # Otherwise an earlier malformed prefix can mask an unresolved later tie.
    prev = None
    for receipt, scope, seq, *_ in events:
        if prev is not None and (receipt == prev[0] and (scope != prev[1] or seq == prev[2])):
            raise ValueError("unresolved same-receipt causal order")
        prev = (receipt, scope, seq)
    standing: dict[int, list[f.NativeBookRowV1]] = {0: [], 1: []}
    warmup = profile.warmup_observation_ids
    warmup_seen: list[str] = []
    warmup_complete = not warmup
    for _receipt, _scope, _seq, oid, group, control in events:
        if control is not None:
            if control.invalidates:
                standing = {0: [], 1: []}
                warmup_seen = []
                warmup_complete = False
            continue
        assert group is not None
        roles = {mapping.raw_signal_catalogue_id.value for mapping in profile.projection_mappings}
        if not roles & _DEPTH_ROLES:
            if not set(group).issubset(roles):
                raise ValueError("unadmitted quote callback role")
            continue
        required = roles - ({"R189"} if profile.ref.context_id == "native-a4-stock" else set())
        if not required.issubset(group) or not set(group).issubset(roles):
            raise ValueError("incomplete required callback roles")
        direct = "R192" in roles
        pos = cast(int, group["R192" if direct else "R185"].canonical_value)
        op = cast(int, group["R194" if direct else "R187"].canonical_value)
        side = cast(int, group["R195" if direct else "R188"].canonical_value)
        size = cast(Decimal, group["R197" if direct else "R190"].canonical_value)
        price = (
            cast(Decimal | None, group["R196" if direct else "R189"].canonical_value)
            if ("R196" if direct else "R189") in group
            else None
        )
        mpid = cast(str, group["R193"].canonical_value) if direct else None
        if (
            type(pos) is not int
            or pos < 0
            or type(op) is not int
            or op not in (0, 1, 2)
            or type(side) is not int
            or side not in (0, 1)
            or size < 0
            or (price is not None and price < 0)
        ):
            raise ValueError("invalid native positional mutation")
        if warmup and len(warmup_seen) < len(warmup):
            if oid != warmup[len(warmup_seen)] or op != 0 or pos != len(standing[side]):
                raise ValueError("incomplete or noncontiguous warm-up")
            warmup_seen.append(oid)
        rows = standing[side]
        if op == 0:
            if pos > len(rows) or size <= 0 or (price is not None and price <= 0):
                raise ValueError("invalid insert")
            rows.insert(
                pos,
                f.NativeBookRowV1(side, pos, price, size, mpid, profile.requested_exchange, oid),
            )
        elif op == 1:
            if pos >= len(rows) or size <= 0 or (price is not None and price <= 0):
                raise ValueError("update without standing row")
            if direct and mpid != rows[pos].mpid:
                raise ValueError("direct MPID update changed identity")
            rows[pos] = f.NativeBookRowV1(
                side,
                pos,
                price if price is not None else rows[pos].price,
                size,
                mpid,
                profile.requested_exchange,
                oid,
            )
        else:
            if pos >= len(rows) or size != 0 or (direct and mpid != rows[pos].mpid):
                raise ValueError("delete without standing position")
            del rows[pos]
        rows[:] = [replace(row, position=i) for i, row in enumerate(rows)]
        if warmup and not warmup_complete and tuple(warmup_seen) == warmup:
            if any(len(standing[side]) < levels for side, levels in profile.warmup_side_levels):
                raise ValueError("complete warm-up prefix lacks required side coverage")
            warmup_complete = True
    # Coverage is a fact proved at completion of the exact known-empty prefix.
    # Lawful later deletes alter a known book; only a separate invalidation
    # clears completeness and requires a newly authorised full warm-up epoch.
    if warmup and (tuple(warmup_seen) != warmup or not warmup_complete):
        raise ValueError("book lacks complete post-control warm-up")
    return tuple((*standing[1], *standing[0]))


def _identity(value: f.NativeSourceSnapshotV1) -> str:
    payload = {
        field.name: getattr(value, field.name)
        for field in fields(value)
        if field.name not in ("source_snapshot_id", "calculated_at_utc")
    }
    return "mmtnative-source:" + hashlib.sha256(codec.canonical(payload)).hexdigest()


def _validate(value: f.NativeSourceSnapshotV1) -> None:
    if type(value) is not f.NativeSourceSnapshotV1:
        raise TypeError("exact native source snapshot required")
    f._Validated.__post_init__(value)
    mappings = {m.raw_signal_catalogue_id.value: m for m in value.profile.projection_mappings}
    for line in value.raw_input_lineage:
        projection = line.projection
        mapping = mappings.get(line.raw_signal_id)
        if (
            mapping is None
            or line.observation_occurrence_id != projection.observation_occurrence_id.value
            or line.projection_mapping_ref != f.VersionRefV1(mapping.mapping_id, mapping.version)
            or projection.projection_mapping_id != mapping.mapping_id
            or projection.projection_mapping_version != mapping.version
            or projection.native_field_path != mapping.native_field_path
            or projection.native_units != mapping.native_units
            or type(line.canonical_value) is not type(projection.native_value)
            or line.canonical_value != projection.native_value
            or line.received_ts_utc != projection.received_ts_utc
            or line.time_basis != _TIME
            or line.event_time_utc is not None
        ):
            raise ValueError("typed public projection lineage mismatch")
    if (
        _controls(
            tuple(c.observation for c in value.controls),
            value.profile,
            min(value.request.as_of_utc, value.request.knowledge_cutoff_utc),
        )
        != value.controls
    ):
        raise ValueError("control lineage differs from public observations")
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or PROFILES.get(value.profile.ref) != value.profile
        or value.profile.ref != value.request.source_profile_ref
        or value.effective_as_of_utc != value.request.as_of_utc
        or value.knowledge_cutoff_utc != value.request.knowledge_cutoff_utc
        or value.standing_rows != _replay(value.profile, value.raw_input_lineage, value.controls)
        or value.source_snapshot_id != _identity(value)
    ):
        raise ValueError("native snapshot source, replay or identity mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_source_snapshot(self, source_snapshot_id: str) -> f.NativeSourceSnapshotV1 | None:
        if type(source_snapshot_id) is not str or not source_snapshot_id:
            raise ValueError("source snapshot ID required")
        return next(
            (v for v in self.state.all() if v.source_snapshot_id == source_snapshot_id), None
        )

    def list_source_history(
        self,
        *,
        source_profile_ref: f.VersionRefV1,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.NativeSourceSnapshotV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if type(source_profile_ref) is not f.VersionRefV1 or type(limit) is not int or limit <= 0:
            raise ValueError("bounded native source history request required")
        rows = (
            v
            for v in self.state.all()
            if v.profile.ref == source_profile_ref
            and v.effective_as_of_utc <= effective_at_or_before_utc
            and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(
            sorted(
                rows,
                key=lambda v: (v.effective_as_of_utc, v.knowledge_cutoff_utc, v.source_snapshot_id),
                reverse=True,
            )
        )[:limit]


class _Owner:
    def __init__(
        self, reader: f.NativeRawReaderV1, state: RecordState, utc_now: Callable[[], datetime]
    ) -> None:
        self.reader, self.state, self.utc_now = reader, state, utc_now
        self.reads = _Reads(state)

    def materialise(self, request: f.NativeSourceRequestV1) -> f.NativeSourceSnapshotV1 | None:
        if (
            type(request) is not f.NativeSourceRequestV1
            or request.source_profile_ref not in PROFILES
        ):
            raise ValueError("unadmitted native source request")
        profile = PROFILES[request.source_profile_ref]
        cutoff = min(request.as_of_utc, request.knowledge_cutoff_utc)
        if cutoff < profile.complete_from_utc:
            return None
        now = self.utc_now()
        f._utc(now)
        try:
            observations = _fetch_observations(self.reader, profile, cutoff)
            controls = _controls(observations, profile, cutoff)
            lines = _fetch_lines(self.reader, profile, observations, cutoff)
            rows = _replay(profile, lines, controls)
        except (ValueError, TypeError, KeyError):
            return None
        value = f.NativeSourceSnapshotV1(
            "M02",
            NAMESPACE,
            BRIEF,
            "pending",
            request,
            profile,
            lines,
            controls,
            rows,
            request.as_of_utc,
            request.knowledge_cutoff_utc,
            now,
        )
        value = replace(value, source_snapshot_id=_identity(value))
        _validate(value)
        return cast(f.NativeSourceSnapshotV1, self.state.append(value))


def _state(storage: f.MemoryStorageV1 | f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(
        storage,
        lambda payload: codec.decode(payload, f.NativeSourceSnapshotV1),
        _validate,
        encode=codec.canonical,
        identity_field="source_snapshot_id",
    )


def build_owner(
    admission: f.OwnerAdmissionV1,
    reader: f.NativeRawReaderV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.NativeSourceOwnerV1:
    if (
        type(admission) is not f.OwnerAdmissionV1
        or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(utc_now)
        or not callable(getattr(reader, "list_projected_raw_history", None))
        or not callable(getattr(reader, "list_raw_observation_history", None))
    ):
        raise ValueError("native source admission or public reader mismatch")
    return _Owner(reader, _state(storage), utc_now)


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
) -> f.NativeSourceReadsV1:
    if (
        type(admission) is not f.OwnerAdmissionV1
        or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) is not f.SQLiteReadStorageV1
    ):
        raise ValueError("native read-only source admission mismatch")
    return _Reads(_state(storage))
