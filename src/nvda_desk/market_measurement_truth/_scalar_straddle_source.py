"""Sealed controlled scalar pair source; no caller-provided ingress or read adapter."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, fields
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import _native_codec as codec
from . import api as f

ROOT = Path(__file__).resolve().parents[3]
LEAF = "handoff/m02_completion_28_execution/L10c/"
POLICY_PATH = LEAF + "SCALAR_STRADDLE_SOURCE_POLICY_PROPOSED_20261125.json"
MANIFEST_PATH = LEAF + "SCALAR_STRADDLE_FINITE_SPECIMENS_PROPOSED_20261125.json"
BRIEF_PATH = LEAF + "SCALAR_STRADDLE_PREEDIT_DESIGN_AND_REVIEW_20261125.md"
POLICY_SHA = "279f1cd166ad0c11585c9776dc4a45b5d949946a513717c39f1dcc9a816e8561"
MANIFEST_SHA = "5e341ef9289f185d4ae9da53eaca9852735af632b17400a89a10508a114dd760"
BRIEF = "04697219c5d5057ac3884aceb09d754dc391a66f6ed4a425459c938c684b1d8d"
OWNER_PATH = LEAF + "OWNER_SCALAR_STRADDLE_CONDITIONAL_EXECUTION_GRANT_20261125.json"
OWNER_SHA = "a7fb45cc876e1450f59678c6599113d86b7b59db9a855e0481edd64f717dc375"
INVENTORY_PATH = LEAF + "SCALAR_STRADDLE_FINITE_CASES_PROPOSED_20261125.json"
INVENTORY_SHA = "d8fd00cb7352d11fcd364b98a533b894b45c864d2cd6311b8db5cb70eaf57480"
C1 = "controlled-nvda-c110-20261023"
C2 = "controlled-nvda-p110-20261023"
SUBJECT = "T01-L10C-NVDA-20261023-110"
PROVIDER = "foundation-controlled-options"
VARIANT = "option_snapshot_v1"
SCOPE = PROVIDER + "/" + VARIANT
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
STAMP = "2026-10-20T12:40:00Z"
META = (
    ("contract.id", ("contract", "id")),
    ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")),
    ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")),
    ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("model.convention", ("model", "convention")),
    ("value.role", ("value", "role")),
)
ROLES = (
    (C1, "R034"), (C1, "R035"), (C2, "R034"), (C2, "R035"),
    (C1, "R112"), (C2, "R112"),
)
LABELS = ("C1-bid", "C1-ask", "C2-bid", "C2-ask", "C1-delta", "C2-delta")
MAPS = tuple(
    raw.RawSignalProjectionMappingV1(
        "mmt-" + rid.lower() + "-option", 1, raw.RawSignalCatalogueId(rid),
        PROVIDER, VARIANT, path, units, META,
    )
    for rid, path, units in (
        ("R034", ("quote", "bid"), "USD_per_share"),
        ("R035", ("quote", "ask"), "USD_per_share"),
        ("R112", ("model", "delta"), "delta_fraction"),
        ("R118", ("model", "underlying_price"), "USD_per_share"),
    )
)
VALUE_ROLES = {
    "R034": "option_bid", "R035": "option_ask",
    "R112": "model_delta", "R118": "model_underlying_price",
}
PRICE_UNIT = f.UnitConventionVersionV1(
    "mmt-option-price", 1, "USD_per_share", "USD_per_share", Decimal("1"), Decimal("0"),
)
DELTA_UNIT = f.UnitConventionVersionV1(
    "mmt-option-delta", 1, "delta_fraction", "delta_fraction", Decimal("1"), Decimal("0"),
)


def check_admission(admission: f.OwnerAdmissionV1) -> None:
    if (
        type(admission) is not f.OwnerAdmissionV1
        or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
    ):
        raise ValueError("unadmitted scalar straddle owner")


def _pinned(path: str, expected: str) -> dict[str, Any]:
    payload = (ROOT / path).read_bytes()
    if hashlib.sha256(payload).hexdigest() != expected:
        raise ValueError("scalar straddle authority bytes mismatch: " + path)
    doc = json.loads(payload)
    if type(doc) is not dict:
        raise ValueError("scalar authority document must be an object")
    return doc


def _digest(members: list[dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(
        members, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False,
    ).encode("ascii")).hexdigest()


def _native(value: Any) -> Any:
    if type(value) is dict:
        if set(value) == {"native_type", "text"}:
            if value["native_type"] != "Decimal" or type(value["text"]) is not str:
                raise ValueError("invalid literal native Decimal")
            return Decimal(value["text"])
        return {key: _native(item) for key, item in value.items()}
    if type(value) in (str, int, bool) or value is None:
        return value
    raise ValueError("unsupported finite-manifest native carrier")


def _literal_value(record: Mapping[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = record
    for name in path:
        if not isinstance(value, Mapping) or name not in value:
            raise ValueError("missing exact native field")
        value = value[name]
    return value


def mapping_for(rid: str) -> raw.RawSignalProjectionMappingV1:
    return next(mapping for mapping in MAPS if mapping.raw_signal_catalogue_id.value == rid)


def _raw_from_literal(literal: dict[str, Any]) -> raw.RawObservationOccurrenceV1:
    # This is the only literal ingress constructor. On durable readback it is
    # an expected-content comparator, never a replacement observation.
    values = dict(literal)
    for key, factory in (
        ("concept_id", raw.concept_id), ("contract_id", raw.contract_id),
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


def _literal_core(members: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        member for member in members
        if member["observation"]["raw_signal_catalogue_ids"] != ["R118"]
    ]


@dataclass(frozen=True, slots=True)
class _Specimen:
    name: str
    full_sha: str
    core_sha: str
    members: tuple[dict[str, Any], ...]
    core: tuple[dict[str, Any], ...]


def _load_specimens() -> tuple[_Specimen, ...]:
    policy = _pinned(POLICY_PATH, POLICY_SHA)
    manifest = _pinned(MANIFEST_PATH, MANIFEST_SHA)
    owner = _pinned(OWNER_PATH, OWNER_SHA)
    inventory = _pinned(INVENTORY_PATH, INVENTORY_SHA)
    grant = owner["exact_proposal_approved"]
    if (
        grant["brief"]["sha256"] != BRIEF
        or grant["specimen_manifest"]["sha256"] != MANIFEST_SHA
        or grant["finite_inventory"]["sha256"] != INVENTORY_SHA
        or grant["proposed_exact_nonfungible_ceilings"] != {
            "SUPPORT": 16, "D109": 8, "D110": 10,
        }
    ):
        raise ValueError("scalar straddle finite authority mismatch")
    base = policy["positive_source_specimen"]["members"]
    if (
        type(base) is not list or len(base) != 7
        or tuple(member["member_id"] for member in base) != (*LABELS, "C1-spot")
    ):
        raise ValueError("invalid base roster")
    rows = manifest["specimens"]
    if len(rows) != 23 or len({row["specimen_id"] for row in rows}) != 23:
        raise ValueError("unadmitted specimen roster")
    cases = inventory["physical_cases"]
    # All full specimens are owner-admitted through an exact case's primary
    # or alternate specimen pin. The parent-only D087 witness is not a source
    # factory choice.
    expected_names = {case["specimen"] for case in cases}
    expected_names.update(
        case["alternate_actual_parent_specimen"] for case in cases
        if "alternate_actual_parent_specimen" in case
    )
    if expected_names != {row["specimen_id"] for row in rows}:
        raise ValueError("specimen admission inventory mismatch")
    result = []
    for row in rows:
        # Operations are from immutable hash-pinned data, not caller commands.
        members = list(base)
        for operation in row["literal_operations"]:
            op = operation["op"]
            if op == "append":
                members.append(operation["member"])
                continue
            indexes = [
                i for i, member in enumerate(members)
                if member["member_id"] == operation["target_member_id"]
            ]
            if len(indexes) != 1:
                raise ValueError("ambiguous immutable literal operation")
            if op == "omit":
                members.pop(indexes[0])
            elif op == "replace":
                members[indexes[0]] = operation["member"]
            else:
                raise ValueError("unadmitted literal operation")
        core = _literal_core(members)
        full_sha, core_sha = _digest(members), _digest(core)
        if (
            len(members) != row["full_member_count"]
            or len(core) != row["core_member_count"]
            or full_sha != row["expanded_member_sha256"]
            or core_sha != row["core_member_sha256"]
            or not 6 <= len(members) <= 8
        ):
            raise ValueError("immutable expanded roster hash/cardinality mismatch")
        result.append(_Specimen(
            row["specimen_id"], full_sha, core_sha, tuple(members), tuple(core),
        ))
    return tuple(result)


def _specimen(name: str) -> _Specimen:
    if type(name) is not str:
        raise TypeError("exact finite specimen identity required")
    matches = tuple(row for row in _load_specimens() if row.name == name)
    if len(matches) != 1:
        raise ValueError("unadmitted scalar straddle specimen")
    return matches[0]


def _core_slot(original: raw.RawObservationOccurrenceV1) -> tuple[str, str]:
    if (
        type(original) is not raw.RawObservationOccurrenceV1
        or original.subject_instrument not in (C1, C2)
        or original.raw_signal_catalogue_ids is None
        or len(original.raw_signal_catalogue_ids) != 1
    ):
        raise ValueError("unadmitted original scalar role")
    assert original.subject_instrument is not None
    return original.subject_instrument, original.raw_signal_catalogue_ids[0].value


def _exact_original(
    actual: raw.RawObservationOccurrenceV1 | None, literal: dict[str, Any],
) -> raw.RawObservationOccurrenceV1:
    if (
        type(actual) is not raw.RawObservationOccurrenceV1
        or codec.canonical(actual) != codec.canonical(_raw_from_literal(literal))
    ):
        raise ValueError("actual original does not match immutable manifest fact")
    return actual


def _role_name(subject: str, rid: str) -> str:
    return ("C1" if subject == C1 else "C2") + "/" + rid


class _CoreRefusal(ValueError):
    def __init__(self, stage: str, field: str) -> None:
        super().__init__(f"{stage}: {field}")
        self.stage, self.field = stage, field


def _check_core_original(
    original: raw.RawObservationOccurrenceV1, subject: str, rid: str,
) -> Decimal:
    # One predicate across BOTH slots and ALL core roles. Compare actual
    # native metadata before projection filters can hide a malformed fact.
    mapping = mapping_for(rid)
    if original.native_units != mapping.native_units:
        raise _CoreRefusal("CORE_ORIGINAL_METADATA", "observation.native_units")
    if original.source_timestamp_raw != STAMP:
        raise _CoreRefusal("CORE_ORIGINAL_CLOCK", "observation.source_timestamp_raw")
    for name, expected in (
        ("received_ts_utc", T), ("source_temporal_kind", "true_instant"),
        ("source_timezone_native", "UTC"),
    ):
        if getattr(original, name) != expected:
            raise _CoreRefusal("CORE_ORIGINAL_CLOCK", "observation." + name)
    if (
        _core_slot(original) != (subject, rid)
        or original.source_provider.value != PROVIDER
        or original.source_variant != VARIANT
        or original.ingestion_sequence_scope.value != SCOPE
    ):
        raise _CoreRefusal("CORE_ORIGINAL_IDENTITY", "observation.source_identity")
    # Optional absence and exact remaining outer fields are independently
    # matched against the hash-pinned full literal by _exact_original.
    expected_identity = (
        subject, "NVDA", "2026-10-23", "110", "C" if subject == C1 else "P",
        "USD", "100", "option", "controlled-model/1", VALUE_ROLES[rid],
    )
    for (_, path), expected in zip(META, expected_identity, strict=True):
        try:
            actual = _literal_value(original.native_record, path)
        except ValueError as exc:
            raise _CoreRefusal(
                "CORE_ORIGINAL_IDENTITY", "observation.native_record." + ".".join(path),
            ) from exc
        if type(actual) is not str or actual != expected:
            raise _CoreRefusal(
                "CORE_ORIGINAL_IDENTITY", "observation.native_record." + ".".join(path),
            )
    field = "observation.native_record." + ".".join(mapping.native_field_path)
    value = _literal_value(original.native_record, mapping.native_field_path)
    if type(value) is not Decimal:
        raise _CoreRefusal("CORE_DOMAIN_TYPE", field)
    if not value.is_finite():
        raise _CoreRefusal("CORE_DOMAIN_FINITE", field)
    if rid == "R112":
        if value.copy_abs() > Decimal(1):
            raise _CoreRefusal("CORE_DOMAIN_RANGE", field)
        if (subject == C1 and value < 0) or (subject == C2 and value > 0):
            raise _CoreRefusal("CORE_DOMAIN_RIGHT_SIGN", field)
    elif value < 0:
        raise _CoreRefusal("CORE_DOMAIN_RANGE", field)
    return value


def _check_roster(
    originals: Sequence[raw.RawObservationOccurrenceV1],
) -> dict[tuple[str, str], raw.RawObservationOccurrenceV1]:
    by_role: dict[tuple[str, str], list[raw.RawObservationOccurrenceV1]] = {}
    for original in originals:
        role = _core_slot(original)
        # All actual R118 originals are retained but are not part of core
        # acceptance. D110 alone interprets their cardinality/value/metadata.
        if role[1] == "R118":
            continue
        by_role.setdefault(role, []).append(original)
    for subject, rid in ROLES:
        if len(by_role.get((subject, rid), ())) != 1:
            raise _CoreRefusal("CORE_ROLE_CARDINALITY", _role_name(subject, rid))
    if set(by_role) != set(ROLES):
        raise _CoreRefusal("CORE_ROLE_CARDINALITY", "unexpected-core-role")
    core = {role: by_role[role][0] for role in ROLES}
    values = {
        role: _check_core_original(original, *role) for role, original in core.items()
    }
    for subject in (C1, C2):
        if values[subject, "R034"] > values[subject, "R035"]:
            raise _CoreRefusal("CORE_QUOTE_ORDER", _role_name(subject, "R035"))
    return core



def _check_projection(
    projection: raw.ProjectedRawValueV1,
    original: raw.RawObservationOccurrenceV1,
    mapping: raw.RawSignalProjectionMappingV1,
) -> None:
    # Compare the entire actual typed projection against its exact relation
    # to the verified original and fixed mapping. Never use a constructed
    # projection as a source or as a replacement for the actual M00 read.
    if type(projection) is not raw.ProjectedRawValueV1:
        raise ValueError("exact typed M00 projection required")
    expected = {
        "raw_signal_catalogue_id": mapping.raw_signal_catalogue_id,
        "observation_occurrence_id": original.observation_occurrence_id,
        "projection_mapping_id": mapping.mapping_id,
        "projection_mapping_version": mapping.version,
        "source_provider": original.source_provider.value,
        "source_variant": original.source_variant,
        "native_field_path": mapping.native_field_path,
        "native_value": _literal_value(original.native_record, mapping.native_field_path),
        "native_units": mapping.native_units,
        "subject_instrument": original.subject_instrument,
        "source_temporal_kind": original.source_temporal_kind,
        "source_timestamp_raw": original.source_timestamp_raw,
        "source_timezone_native": original.source_timezone_native,
        "received_ts_utc": original.received_ts_utc,
        "ingestion_sequence": original.ingestion_sequence,
        "ingestion_sequence_scope": original.ingestion_sequence_scope,
        "revision_vintage_native": original.revision_vintage_native,
        "selection_identity": raw.RawSelectionIdentityV1(tuple(
            (key, _literal_value(original.native_record, path))
            for key, path in mapping.selection_identity_field_paths
        )),
    }
    actual = {field.name: getattr(projection, field.name) for field in fields(projection)}
    if codec.canonical(actual) != codec.canonical(expected):
        raise ValueError("exact projection/original relation mismatch")


def _history(
    reads: f.D091RawReadPortV1, subject: str, rid: str,
) -> tuple[raw.ProjectedRawValueV1, ...]:
    mapping = mapping_for(rid)
    cursor: str | None = None
    cursors: set[str] = set()
    seen: set[str] = set()
    items = []
    for _ in range(1000):
        page = reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument=subject, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=cursor,
        )
        if (
            type(page) is not raw.ProjectedRawHistoryPageV1
            or type(page.items) is not tuple or len(page.items) > 100
        ):
            raise ValueError("malformed bounded scalar source page")
        for item in page.items:
            if (
                type(item) is not raw.ProjectedRawValueV1
                or item.raw_signal_catalogue_id != mapping.raw_signal_catalogue_id
                or item.subject_instrument != subject
            ):
                raise ValueError("unexpected scalar projection role")
            oid = item.observation_occurrence_id.value
            if oid in seen:
                raise ValueError("duplicate scalar projection identity")
            seen.add(oid)
            items.append(item)
            if len(items) > 8:
                raise ValueError("scalar projection roster exceeds finite source")
        if page.next_cursor is None:
            return tuple(items)
        if (
            type(page.next_cursor) is not str or not page.next_cursor
            or not page.items or page.next_cursor == cursor or page.next_cursor in cursors
        ):
            raise ValueError("nonprogressing scalar source cursor")
        cursors.add(page.next_cursor)
        cursor = page.next_cursor
    raise ValueError("scalar source page bound exhausted")


def _live_role(
    reads: f.D091RawReadPortV1,
    original: raw.RawObservationOccurrenceV1,
    subject: str,
    rid: str,
) -> tuple[raw.RawObservationOccurrenceV1, raw.ProjectedRawValueV1]:
    items = _history(reads, subject, rid)
    if len(items) != 1 or items[0].observation_occurrence_id != original.observation_occurrence_id:
        raise ValueError("incomplete or conflicting scalar projection roster")
    actual = reads.get_raw_observation_occurrence(items[0].observation_occurrence_id)
    if (
        type(actual) is not raw.RawObservationOccurrenceV1
        or codec.canonical(actual) != codec.canonical(original)
    ):
        raise ValueError("actual M00 getter disagrees with sealed original")
    _check_projection(items[0], actual, mapping_for(rid))
    return actual, items[0]


def _validated_core_literals(
    digest: str,
) -> tuple[dict[str, Any], ...]:
    # Do not accept a stored digest as authority. Resolve it only to a
    # complete, valid six-role core of the immutable admitted full specimens.
    matches = [row.core for row in _load_specimens() if row.core_sha == digest]
    if not matches or len(matches[0]) != len(ROLES):
        raise ValueError("unknown or incomplete scalar core digest")
    core = matches[0]
    if _digest(list(core)) != digest or any(other != core for other in matches):
        raise ValueError("ambiguous scalar core digest")
    if tuple(member["member_id"] for member in core) != LABELS:
        raise ValueError("unexpected ordered scalar core roster")
    originals = tuple(_raw_from_literal(member["observation"]) for member in core)
    if len({original.observation_occurrence_id for original in originals}) != len(ROLES):
        raise ValueError("nonunique core identities")
    _check_roster(originals)
    return core


def core_literal(digest: str, subject: str, rid: str) -> dict[str, Any]:
    try:
        index = ROLES.index((subject, rid))
    except ValueError as exc:
        raise ValueError("unadmitted scalar core role") from exc
    return _validated_core_literals(digest)[index]["observation"]


def validate_core_role(
    digest: str, subject: str, rid: str,
    original: raw.RawObservationOccurrenceV1,
    projection: raw.ProjectedRawValueV1,
) -> Decimal:
    # Same exact original/projection predicate on producer and durable readback.
    _exact_original(original, core_literal(digest, subject, rid))
    value = _check_core_original(original, subject, rid)
    _check_projection(projection, original, mapping_for(rid))
    return value


def source_role(
    source: f.ScalarStraddleSourceV1, subject: str, rid: str,
) -> tuple[raw.RawObservationOccurrenceV1, raw.ProjectedRawValueV1]:
    if type(source) is not f.ScalarStraddleSourceV1:
        raise ValueError("exact sealed scalar source required")
    row = _specimen(source.specimen_id)
    if row.full_sha != source.full_specimen_sha256 or row.core_sha != source.core_manifest_sha256:
        raise ValueError("sealed source pins mismatch")
    literal = core_literal(row.core_sha, subject, rid)
    original = _exact_original(
        source.get_raw_observation_occurrence(
            raw.observation_occurrence_id(literal["observation_occurrence_id"]),
        ),
        literal,
    )
    actual, projection = _live_role(source, original, subject, rid)
    validate_core_role(row.core_sha, subject, rid, actual, projection)
    return actual, projection


def build_source(
    admission: f.OwnerAdmissionV1, specimen_id: str,
) -> f.ScalarStraddleSourceV1:
    check_admission(admission)
    row = _specimen(specimen_id)
    identities = [
        member["observation"]["observation_occurrence_id"] for member in row.members
    ]
    if len(identities) != len(set(identities)):
        # M00 deliberately collapses exact replay; refuse before any insert.
        raise f.ScalarStraddleSourceRefusalV1(
            "MANIFEST_ID_UNIQUENESS", "observation.observation_occurrence_id",
            row.name, row.full_sha, (),
        )
    owner = raw.create_owner()
    for member in row.members:
        submitted = _raw_from_literal(member["observation"])
        admitted = owner.commands.admit_raw_observation_occurrence(submitted)
        _exact_original(admitted, member["observation"])
    # Every negative other than duplicate-ID has a genuinely admitted
    # original roster. Obtain actual getter evidence BEFORE any core guard.
    observed = tuple(
        _exact_original(
            owner.reads.get_raw_observation_occurrence(raw.observation_occurrence_id(oid)),
            member["observation"],
        )
        for oid, member in zip(identities, row.members, strict=True)
    )
    try:
        core = _check_roster(observed)
    except _CoreRefusal as exc:
        raise f.ScalarStraddleSourceRefusalV1(
            exc.stage, exc.field, row.name, row.full_sha, observed,
        ) from exc
    for subject, rid in ROLES:
        _live_role(owner.reads, core[subject, rid], subject, rid)
    # No R118 normative check here. Spot-only invalid variants still expose
    # exactly their original roster for D110 to adjudicate after D109.
    reads = owner.reads
    del owner
    return f.ScalarStraddleSourceV1._from_sealed(
        specimen_id=row.name, full=row.full_sha, core=row.core_sha,
        getter=reads.get_raw_observation_occurrence,
        history=reads.list_projected_raw_history,
    )
