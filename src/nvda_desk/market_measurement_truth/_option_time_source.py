"""Exact controlled option-time public M00 source; no injected read or write adapter."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import fields
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import _native_codec as native
from . import api as f

ROOT = Path(__file__).resolve().parents[3]
LEAF = "handoff/m02_completion_28_execution/L07a/"
POLICY_PATH = LEAF + "OPTION_TIME_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json"
POLICY_SHA = "14a3ba2308f519d90d11eb450ac484a2c922507b7e04041c740297527a1d847a"
BRIEF_PATH = LEAF + "D001_IMPLEMENTATION_BRIEF.md"
BRIEF = "222d0919c67c05f6436f985b8262ace985ab11dea30fc045333ee13fa10a8d8d"
BINDING_PATH = "implementation/authority/T01_D001_OPTION_TIME_AUTHORITY_BINDING.yaml"
BINDING_SHA = "ff80ea7dd3aa7674723b758dda9173356bda75119ba996ece5bf4c1a9ff2cf35"
OWNER_PATH = (
    "handoff/m02_completion_28_execution/"
    "OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json"
)
OWNER_SHA = "6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41"
SUBJECT = "controlled-nvda-c110-20261023"
SPECIMENS = (
    "EARLIER",
    "MAIN",
    "CROSS_CLOSE",
    "SAME_DAY",
    "AT_EXPIRY",
    "AFTER",
    "R002_DATE_ONLY",
    "R002_RECEIPT_ONLY",
    "R003_OFFSET_MISMATCH",
    "R004_FOREIGN_ZONE",
    "R024_SCHEDULE_MISMATCH",
    "R001_VALUE_MISMATCH",
    "R013_ORIGINAL_UNITS",
    "R013_DATE_MISMATCH",
    "R013_CONTRACT_MISMATCH",
)
ROLES = ("R001", "R002", "R003", "R004", "R013", "R023", "R024")


def _pinned(path: str, digest: str) -> bytes:
    data = (ROOT / path).read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError("option time authority bytes mismatch: " + path)
    return data


def policy() -> dict[str, Any]:
    for path, digest in ((BRIEF_PATH, BRIEF), (BINDING_PATH, BINDING_SHA), (OWNER_PATH, OWNER_SHA)):
        _pinned(path, digest)
    return json.loads(_pinned(POLICY_PATH, POLICY_SHA))["source"]


def check_admission(admission: f.OwnerAdmissionV1) -> None:
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted option-time owner")
    policy()


def _digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    ).hexdigest()


def _native(value: Any) -> Any:
    if type(value) is dict:
        if set(value) == {"native_type", "text"}:
            if value["native_type"] != "Decimal" or type(value["text"]) is not str:
                raise ValueError("invalid native Decimal literal")
            return Decimal(value["text"])
        return {k: _native(v) for k, v in value.items()}
    if type(value) is list:
        return [_native(v) for v in value]
    if type(value) in (str, int, bool) or value is None:
        return value
    raise ValueError("unsupported native literal")


def _original(literal: dict[str, Any]) -> raw.RawObservationOccurrenceV1:
    values = dict(literal)
    for key, factory in (
        ("concept_id", raw.concept_id),
        ("contract_id", raw.contract_id),
        ("observation_occurrence_id", raw.observation_occurrence_id),
        ("delivery_artifact_ref", raw.delivery_artifact_ref),
        ("source_provider", raw.provider_id),
        ("ingestion_sequence_scope", raw.ingestion_sequence_scope),
    ):
        values[key] = factory(values[key])
    values["native_record"] = _native(values["native_record"])
    values["received_ts_utc"] = datetime.fromisoformat(values["received_ts_utc"])
    values["raw_signal_catalogue_ids"] = tuple(
        raw.RawSignalCatalogueId(rid) for rid in values["raw_signal_catalogue_ids"]
    )
    return raw.RawObservationOccurrenceV1(**values)


def _path(record: Mapping[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = record
    for name in path:
        if not isinstance(value, Mapping) or name not in value:
            raise ValueError("missing actual native field")
        value = value[name]
    return value


def mapping_for(rid: str) -> raw.RawSignalProjectionMappingV1:
    row = policy()["role_mappings"][rid]
    return raw.RawSignalProjectionMappingV1(
        row["mapping_id"],
        row["version"],
        raw.RawSignalCatalogueId(row["raw_signal_catalogue_id"]),
        row["source_provider"],
        row["source_variant"],
        tuple(row["native_field_path"]),
        row["native_units"],
        tuple((k, tuple(path)) for k, path in row["selection_identity_field_paths"]),
    )


def _specimen(name: str) -> tuple[str, tuple[raw.RawObservationOccurrenceV1, ...]]:
    if type(name) is not str or name not in SPECIMENS:
        raise ValueError("unadmitted first-stage option-time specimen")
    (row,) = [item for item in policy()["exact_specimens"] if item["id"] == name]
    members = row["members"]
    digest = _digest(members)
    originals = tuple(_original(item) for item in members)
    if (
        digest != row["expanded_member_sha256"]
        or len(members) != row["member_count"]
        or len(originals) != len(ROLES)
        or len({item.observation_occurrence_id for item in originals}) != len(ROLES)
        or sorted(_role(item) for item in originals) != sorted(ROLES)
    ):
        raise ValueError("immutable option-time source roster mismatch")
    return digest, originals


def _role(original: raw.RawObservationOccurrenceV1) -> str:
    if (
        type(original) is not raw.RawObservationOccurrenceV1
        or len(original.raw_signal_catalogue_ids or ()) != 1
    ):
        raise ValueError("exact original role required")
    assert original.raw_signal_catalogue_ids is not None
    return original.raw_signal_catalogue_ids[0].value


def _exact_original(
    actual: raw.RawObservationOccurrenceV1 | None,
    expected: raw.RawObservationOccurrenceV1,
) -> raw.RawObservationOccurrenceV1:
    if type(actual) is not raw.RawObservationOccurrenceV1 or native.canonical(
        actual
    ) != native.canonical(expected):
        raise ValueError("actual original differs from admitted literal")
    return actual


def check_projection(
    original: raw.RawObservationOccurrenceV1,
    projection: raw.ProjectedRawValueV1,
    mapping: raw.RawSignalProjectionMappingV1,
) -> None:
    if (
        type(original) is not raw.RawObservationOccurrenceV1
        or type(projection) is not raw.ProjectedRawValueV1
        or original.raw_signal_catalogue_ids != (mapping.raw_signal_catalogue_id,)
        or original.source_provider.value != mapping.source_provider
        or original.source_variant != mapping.source_variant
    ):
        raise ValueError("actual original and projection role/identity required")
    expected = {
        "raw_signal_catalogue_id": mapping.raw_signal_catalogue_id,
        "observation_occurrence_id": original.observation_occurrence_id,
        "projection_mapping_id": mapping.mapping_id,
        "projection_mapping_version": mapping.version,
        "source_provider": original.source_provider.value,
        "source_variant": original.source_variant,
        "native_field_path": mapping.native_field_path,
        "native_value": _path(original.native_record, mapping.native_field_path),
        "native_units": mapping.native_units,
        "subject_instrument": original.subject_instrument,
        "source_temporal_kind": original.source_temporal_kind,
        "source_timestamp_raw": original.source_timestamp_raw,
        "source_timezone_native": original.source_timezone_native,
        "received_ts_utc": original.received_ts_utc,
        "ingestion_sequence": original.ingestion_sequence,
        "ingestion_sequence_scope": original.ingestion_sequence_scope,
        "revision_vintage_native": original.revision_vintage_native,
        "selection_identity": raw.RawSelectionIdentityV1(
            tuple(
                (key, _path(original.native_record, path))
                for key, path in mapping.selection_identity_field_paths
            )
        ),
    }
    actual = {field.name: getattr(projection, field.name) for field in fields(projection)}
    if native.canonical(actual) != native.canonical(expected):
        raise ValueError("actual projection/original relation mismatch")


def _order(original: raw.RawObservationOccurrenceV1) -> tuple[datetime, str, int, str]:
    return (
        original.received_ts_utc,
        original.ingestion_sequence_scope.value,
        original.ingestion_sequence,
        original.observation_occurrence_id.value,
    )


def _direct(reads: Any, original: raw.RawObservationOccurrenceV1) -> raw.ProjectedRawValueV1:
    actual = _exact_original(
        reads.get_raw_observation_occurrence(original.observation_occurrence_id), original
    )
    mapping = mapping_for(_role(actual))
    projection = reads.project_raw_value(
        mapping.raw_signal_catalogue_id,
        actual.observation_occurrence_id,
        mappings=(mapping,),
    )
    if type(projection) is not raw.ProjectedRawValueV1:
        raise ValueError("missing actual direct projection")
    check_projection(actual, projection, mapping)
    return projection


def build_source(admission: f.OwnerAdmissionV1, specimen_id: str) -> f.OptionTimeSourceV1:
    check_admission(admission)
    return _build_sealed_source(admission, specimen_id)


def _build_sealed_source(
    admission: f.OwnerAdmissionV1, specimen_id: str,
) -> f.OptionTimeSourceV1:
    digest, originals = _specimen(specimen_id)
    owner = raw.create_owner()
    for original in originals:
        _exact_original(owner.commands.admit_raw_observation_occurrence(original), original)
    for original in originals:
        _direct(owner.reads, original)
    reads = owner.reads
    del owner
    return f.OptionTimeSourceV1._from_sealed(
        admission=admission,
        specimen_id=specimen_id,
        digest=digest,
        count=len(originals),
        getter=reads.get_raw_observation_occurrence,
        projection=reads.project_raw_value,
        history=reads.list_projected_raw_history,
    )


def live_pair(
    source: f.OptionTimeSourceV1,
    cutoff: datetime,
) -> tuple[tuple[raw.RawObservationOccurrenceV1, ...], tuple[raw.ProjectedRawValueV1, ...]]:
    selected = _live_roles(source, cutoff)
    return tuple(selected[r][0] for r in ("R002", "R003")), tuple(
        selected[r][1] for r in ("R002", "R003")
    )


def _live_roles(
    source: f.OptionTimeSourceV1,
    cutoff: datetime,
) -> dict[str, tuple[raw.RawObservationOccurrenceV1, raw.ProjectedRawValueV1]]:
    digest, originals = _specimen(source.specimen_id)
    if source.expanded_sha256 != digest or source.expanded_count != len(originals):
        raise ValueError("sealed option-time roster mismatch")
    selected = {}
    for rid in ROLES:
        mapping = mapping_for(rid)
        expected = sorted(
            (o for o in originals if _role(o) == rid and o.received_ts_utc <= cutoff),
            key=_order,
        )
        cursor = None
        cursors: set[str] = set()
        actual = []
        seen = set()
        for _ in range(20):
            page = source.list_projected_raw_history(
                mapping.raw_signal_catalogue_id,
                mappings=(mapping,),
                subject_instrument=SUBJECT,
                received_at_or_before_utc=cutoff,
                event_at_or_before_utc=None,
                limit=2,
                cursor=cursor,
            )
            if (
                type(page) is not raw.ProjectedRawHistoryPageV1
                or type(page.items) is not tuple
                or len(page.items) > 2
            ):
                raise ValueError("invalid bounded option-time history")
            for projection in page.items:
                if (
                    type(projection) is not raw.ProjectedRawValueV1
                    or projection.observation_occurrence_id in seen
                ):
                    raise ValueError("invalid or duplicate option-time projection")
                seen.add(projection.observation_occurrence_id)
                actual.append(projection)
            if page.next_cursor is None:
                break
            if (
                not page.items
                or type(page.next_cursor) is not str
                or not page.next_cursor
                or page.next_cursor in cursors
            ):
                raise ValueError("nonprogressing option-time cursor")
            cursors.add(page.next_cursor)
            cursor = page.next_cursor
        else:
            raise ValueError("option-time history page bound exhausted")
        if len(expected) != 1 or len(actual) != 1:
            raise ValueError("incomplete option-time frame role")
        original = _exact_original(
            source.get_raw_observation_occurrence(expected[0].observation_occurrence_id),
            expected[0],
        )
        direct = _direct(source, original)
        if native.canonical(actual[0]) != native.canonical(direct):
            raise ValueError("direct and history projection mismatch")
        selected[rid] = original, actual[0]
    return selected


def validate_pair(
    originals: tuple[raw.RawObservationOccurrenceV1, ...],
    projections: tuple[raw.ProjectedRawValueV1, ...],
) -> None:
    if len(originals) != 2 or len(projections) != 2:
        raise ValueError("two exact option-time roles required")
    # Verify co-occurrence of both complete selected facts in a permitted
    # literal frame. Do not bind unrelated R001 or calendar/expiry facts.
    actual = native.canonical(originals)
    if not any(
        actual
        == native.canonical(
            tuple(
                next(o for o in _specimen(name)[1] if _role(o) == rid) for rid in ("R002", "R003")
            )
        )
        for name in SPECIMENS
    ):
        raise ValueError("selected option-time originals not a permitted pair")
    for rid, original, projection in zip(("R002", "R003"), originals, projections, strict=True):
        check_projection(original, projection, mapping_for(rid))


LOCAL_BRIEF_PATH = LEAF + "D003_IMPLEMENTATION_BRIEF.md"
LOCAL_BRIEF = "0c588c6d06690f2e8fd23898cb4c219263dfc9b0924b071b40c2f92098ee5344"
LOCAL_BINDING_PATH = "implementation/authority/T01_D003_OPTION_TIME_AUTHORITY_BINDING.yaml"
LOCAL_BINDING_SHA = "a26f84b5ea86e6b5899b303ac4fe0f79d0915f5d2106392f4cf3ba40cbd48637"


def local_policy() -> dict[str, Any]:
    _pinned(LOCAL_BRIEF_PATH, LOCAL_BRIEF)
    _pinned(LOCAL_BINDING_PATH, LOCAL_BINDING_SHA)
    return policy()


def check_local_admission(admission: f.OwnerAdmissionV1) -> None:
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1(
        "M02", LOCAL_BRIEF,
    ):
        raise ValueError("unadmitted D003 option-time owner")
    local_policy()


def build_local_source(admission: f.OwnerAdmissionV1, specimen_id: str) -> f.OptionTimeSourceV1:
    check_local_admission(admission)
    return _build_sealed_source(admission, specimen_id)


def live_local_roles(
    raw_source: f.OptionTimeSourceV1, cutoff: datetime,
) -> dict[str, tuple[raw.RawObservationOccurrenceV1, raw.ProjectedRawValueV1]]:
    return _live_roles(raw_source, cutoff)


def validate_local_roles(
    originals: tuple[raw.RawObservationOccurrenceV1, ...],
    projections: tuple[raw.ProjectedRawValueV1, ...],
) -> None:
    """Require the complete selected parent pair and R004 from one literal roster."""
    if len(originals) != 3 or len(projections) != 3:
        raise ValueError("D003 requires exact parent pair plus selected R004")
    roles = ("R002", "R003", "R004")
    actual = native.canonical(originals)
    for name in SPECIMENS:
        _, roster = _specimen(name)
        expected = tuple(next(o for o in roster if _role(o) == rid) for rid in roles)
        if actual == native.canonical(expected):
            break
    else:
        raise ValueError("D003 selected originals do not co-occur in one admitted roster")
    for rid, original, projection in zip(roles, originals, projections, strict=True):
        check_projection(original, projection, mapping_for(rid))


EXPIRY_BRIEF_PATH = LEAF + "D086_IMPLEMENTATION_BRIEF.md"
EXPIRY_BRIEF = "e5747d9ba697d16281e09c115db932a60f559c03937f243be06f7c01d107b676"
EXPIRY_BINDING_PATH = "implementation/authority/T01_D086_OPTION_TIME_AUTHORITY_BINDING.yaml"
EXPIRY_BINDING_SHA = "9ccd773c689bf24e443cd23ebba534b637781dda48fb9377bf23d32718889b97"


def expiry_policy() -> dict[str, Any]:
    _pinned(EXPIRY_BRIEF_PATH, EXPIRY_BRIEF)
    _pinned(EXPIRY_BINDING_PATH, EXPIRY_BINDING_SHA)
    return policy()


def check_expiry_admission(admission: f.OwnerAdmissionV1) -> None:
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1(
        "M02", EXPIRY_BRIEF,
    ):
        raise ValueError("unadmitted D086 option-time owner")
    expiry_policy()


def build_expiry_source(admission: f.OwnerAdmissionV1, specimen_id: str) -> f.OptionTimeSourceV1:
    check_expiry_admission(admission)
    return _build_sealed_source(admission, specimen_id)


def live_expiry_roles(
    raw_source: f.OptionTimeSourceV1, cutoff: datetime,
) -> dict[str, tuple[raw.RawObservationOccurrenceV1, raw.ProjectedRawValueV1]]:
    return _live_roles(raw_source, cutoff)


def validate_expiry_roles(
    originals: tuple[raw.RawObservationOccurrenceV1, ...],
    projections: tuple[raw.ProjectedRawValueV1, ...],
) -> None:
    """Require the complete selected parent pair and R013 from one literal roster."""
    if len(originals) != 3 or len(projections) != 3:
        raise ValueError("D086 requires exact parent pair plus selected R013")
    roles = ("R002", "R003", "R013")
    actual = native.canonical(originals)
    for name in SPECIMENS:
        _, roster = _specimen(name)
        expected = tuple(next(o for o in roster if _role(o) == rid) for rid in roles)
        if actual == native.canonical(expected):
            break
    else:
        raise ValueError("D086 selected originals do not co-occur in one admitted roster")
    for rid, original, projection in zip(roles, originals, projections, strict=True):
        check_projection(original, projection, mapping_for(rid))
