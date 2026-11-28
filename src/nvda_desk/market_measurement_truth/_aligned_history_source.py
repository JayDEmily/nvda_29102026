"""Sealed literal M00 source and common original/projection/corpus checks."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, fields
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import _native_codec as native
from . import api as f

ROOT = Path(__file__).resolve().parents[3]
LEAF = "handoff/m02_completion_28_execution/L01a/"
POLICY_PATH = LEAF + "ALIGNED_HISTORY_SOURCE_POLICY_PROPOSED_20261126.json"
MANIFEST_PATH = LEAF + "ALIGNED_HISTORY_FINITE_SPECIMENS_PROPOSED_20261126.json"
INVENTORY_PATH = LEAF + "ALIGNED_HISTORY_JOINT_FIT_FINITE_CASES_PROPOSED_20261126.json"
OWNER_PATH = (
    "handoff/m02_completion_28_execution/OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json"
)
POLICY_SHA = "9ba56098c273007980c893db39931ac86e7a3185bbb665f8c3f1e14f99b72af1"
MANIFEST_SHA = "bb03481de75e1820c7aff61777a4a3aa4f676440ec03e373a05c032a0417c76d"
INVENTORY_SHA = "3be150f2998b4187a81720b424c848099edeba7a9f638ae90d9aae95d4c5d5c1"
OWNER_SHA = "6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41"
# Distinct first-stage owner jurisdictions. Relative configurations are separate.
BRIEFS = {
    "D071": "65f2d0f9135f291773ab6081ec76892a967315df3ecb9c1760a4e2687a296e5e",
    "D072": "4f8214d1ca11eaf0769206f3f322c799f44883bd266e63748e937dea5602b739",
    "D073": "a7234477d581e6cba27e470919fa092c4ed5054d5a1aa31d2019d8fa94d16f48",
    "D074": "524b2d2a4aa94a0c1c55ea376650d14648af67c46e73763ce3e8cc0f2e9e0c0e",
    "D075": "24ec8f08faf1a61059cee69b8c675767345809ae6a0dd90ab852a2fc30977750",
}
BINDINGS = {
    "D071": "30cbb5fe2f8a1b720bc58b55b05f3c88b736401f03d03199404444b60330dc03",
    "D072": "637ff9b90b916ee69ee956db28e191ef86be3764ce2004b5fc24e371fa5869df",
    "D073": "867444cecdf23c191269b1b3856410cc1ee6e3b81b8730dafa6d6528b78d6e0a",
    "D074": "f2a2208a73d291e614577eaf2b81ffd13d699c4efbc2eeeb6258569ac8aa1c34",
    "D075": "50120c02327ed212e8821ac3795d4f64daa3e38d77ecd5c92c7b20f6a2ba8c3f",
}
SUBJECTS = dict(zip(BRIEFS, ("SPY", "QQQ", "SMH", "SOXX", "NVDA"), strict=True))
D076_BRIEF = "c2b30721c0f535d00bb09cb801461ddf875966a93049c47fe572856f43fde480"
D076_BINDING = "6f1324ab9922a1cd8b9994da931ee8f946d7d8666a758f8554269d092d006a80"
D076_PARENTS = ("D072", "D071")
D077_BRIEF = "88bdd385ff91432940f4d27a8cff2bce6af22a8c85b858f53ba2f674d3c30a3c"
D077_BINDING = "7f1b9f882d815616aa8e2fe53d6069800c7524f375202bff4eea5a67bf91a735"
D077_PARENTS = ("D073", "D074", "D072")
ROLES = ("R037", "R042")
LEGAL_CORPORA = ("A", "B", "RANK", "COND", "C_NONPRIOR")
PROVIDER = "foundation-controlled-aligned-history"
VARIANT = "prior_close_history_v1"
SCOPE = PROVIDER + "/" + VARIANT
PRICE_UNIT = "USD_per_share"
META = (
    ("instrument.id", ("instrument", "id")),
    ("session.id", ("session", "id")),
    ("adjustment.basis", ("adjustment", "basis")),
    ("price.kind", ("price", "kind")),
)
MAPS = tuple(
    raw.RawSignalProjectionMappingV1(
        "t01-l01a-" + role.lower() + "-history", 1, raw.RawSignalCatalogueId(role),
        PROVIDER, VARIANT, path, PRICE_UNIT, META,
    )
    for role, path in (("R037", ("trade", "last")), ("R042", ("official_close", "value")))
)
UNIT = f.UnitConventionVersionV1(
    "t01-l01a-underlying-price", 1, PRICE_UNIT, PRICE_UNIT, Decimal("1"), Decimal("0"),
)
Key = tuple[str, str, str]
Pair = tuple[raw.RawObservationOccurrenceV1, raw.ProjectedRawValueV1]


def _pinned(path: str, digest: str) -> bytes:
    data = (ROOT / path).read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError("aligned history authority bytes mismatch: " + path)
    return data


def _document(path: str, digest: str) -> dict[str, Any]:
    value = json.loads(_pinned(path, digest))
    if type(value) is not dict:
        raise ValueError("exact aligned history authority object required")
    return value


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False,
    ).encode("ascii")).hexdigest()


def _literal_native(value: Any) -> Any:
    if type(value) is dict:
        if set(value) == {"decimal"}:
            if type(value["decimal"]) is not str:
                raise ValueError("exact native Decimal text required")
            return Decimal(value["decimal"])
        return {k: _literal_native(v) for k, v in value.items()}
    if type(value) in (str, int, bool) or value is None:
        return value
    raise ValueError("unsupported aligned history native literal")


def _original(literal: dict[str, Any]) -> raw.RawObservationOccurrenceV1:
    values = dict(literal)
    for key, factory in (
        ("concept_id", raw.concept_id), ("contract_id", raw.contract_id),
        ("observation_occurrence_id", raw.observation_occurrence_id),
        ("delivery_artifact_ref", raw.delivery_artifact_ref),
        ("source_provider", raw.provider_id),
        ("ingestion_sequence_scope", raw.ingestion_sequence_scope),
    ):
        values[key] = factory(values[key])
    values["native_record"] = _literal_native(values["native_record"])
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


@dataclass(frozen=True, slots=True)
class Frame:
    slot: str
    as_of: datetime
    reference: datetime
    cutoff: datetime
    as_of_text: str
    reference_text: str
    current_session: str
    reference_session: str
    context: f.WindowContextV1
    seconds: int


@dataclass(frozen=True, slots=True)
class Configuration:
    signal: str
    subject: str
    brief: str
    profile: f.VersionRefV1
    definition: f.CalculationDefinitionV1
    parameter: f.CalculationParameterSetV1
    selection: f.InputSelectionPolicyVersionV1


def _frame(row: dict[str, Any]) -> Frame:
    c = row["context"]
    return Frame(
        row["slot"], datetime.fromisoformat(row["as_of"]),
        datetime.fromisoformat(row["reference"]), datetime.fromisoformat(row["row_cutoff"]),
        row["as_of"], row["reference"], row["session_current"], row["session_reference"],
        f.WindowContextV1(
            f.VersionRefV1(c["id"], c["version"]),
            datetime.fromisoformat(c["start"]), datetime.fromisoformat(c["end"]),
            datetime.fromisoformat(c["history_complete_from"]),
        ),
        row["window_seconds"],
    )


def _configuration(admission: f.OwnerAdmissionV1, policy: dict[str, Any]) -> Configuration:
    if type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02":
        raise ValueError("exact M02 aligned history admission required")
    if admission.implementation_brief_sha256 == D076_BRIEF:
        return _relative_configuration(policy, "D076")
    if admission.implementation_brief_sha256 == D077_BRIEF:
        return _relative_configuration(policy, "D077")
    matching = tuple(k for k, v in BRIEFS.items() if v == admission.implementation_brief_sha256)
    if len(matching) != 1:
        raise ValueError("unadmitted aligned history jurisdiction")
    signal = matching[0]
    subject, brief = SUBJECTS[signal], BRIEFS[signal]
    brief_path = LEAF + f"ALIGNED_HISTORY_{signal}_IMPLEMENTATION_BRIEF.md"
    binding = f"implementation/authority/T01_ALIGNED_HISTORY_{signal}_AUTHORITY_BINDING.yaml"
    _pinned(brief_path, brief)
    _pinned(binding, BINDINGS[signal])
    row = policy["profiles"][signal]
    if (
        row["subject"] != subject or row["members"] != [subject]
        or row["raw_dependencies"] != list(ROLES) or row["derived_dependencies"]
        or row["equation"] != "ln(current/reference)"
        or row["kernel"] != "K03_CHANGE_RETURN" or row["parameter_profile"] != "P_WINDOW"
        or row["units"] != "return" or row["result_shape"] != "scalar_decimal"
        or row["future_own_brief_path"] != brief_path or row["future_binding_path"] != binding
    ):
        raise ValueError("aligned history profile/owner binding mismatch")
    refs = tuple(f.AuthorityArtifactRefV1(r["path"], r["sha256"]) for r in policy["authority_refs"])
    profile, param, selection = (row[k] for k in ("profile_ref", "parameter_ref", "selection_ref"))
    return Configuration(
        signal, subject, brief, f.VersionRefV1(profile["id"], profile["version"]),
        f.CalculationDefinitionV1(
            signal, row["calculation_definition_version"], row["kernel"], row["equation"],
            ROLES, (), row["parameter_profile"], row["units"], row["result_shape"],
            (*refs, f.AuthorityArtifactRefV1(POLICY_PATH, POLICY_SHA),
             f.AuthorityArtifactRefV1(brief_path, brief)),
        ),
        f.CalculationParameterSetV1(
            param["id"], param["version"], "P_WINDOW", subject, (subject,),
        ),
        f.InputSelectionPolicyVersionV1(
            selection["id"], selection["version"],
            ("subject_instrument", "instrument.id", "session.id", "adjustment.basis", "price.kind"),
            timedelta(seconds=86400), timedelta(0), ("true_instant",), (),
            PROVIDER, VARIANT, SCOPE, 100, 2,
        ),
    )


def _relative_configuration(policy: dict[str, Any], signal: str) -> Configuration:
    if signal == "D076":
        subject, members = "US_TECH_VS_BROAD", ("QQQ", "SPY")
        brief, binding_hash = D076_BRIEF, D076_BINDING
        parents, equation = D076_PARENTS, "D072-D071"
    elif signal == "D077":
        subject, members = "SEMIS_VS_TECH", ("SMH", "SOXX", "QQQ")
        brief, binding_hash = D077_BRIEF, D077_BINDING
        parents, equation = D077_PARENTS, "(D073+D074)/2-D072"
    else:
        raise ValueError("unadmitted relative history jurisdiction")
    brief_path = LEAF + f"ALIGNED_HISTORY_{signal}_IMPLEMENTATION_BRIEF.md"
    binding = f"implementation/authority/T01_ALIGNED_HISTORY_{signal}_AUTHORITY_BINDING.yaml"
    _pinned(brief_path, brief)
    _pinned(binding, binding_hash)
    row = policy["profiles"][signal]
    if (
        row["subject"] != subject or row["members"] != list(members)
        or row["raw_dependencies"] != [] or row["derived_dependencies"] != list(parents)
        or row["equation"] != equation or row["kernel"] != "K02_ALGEBRA"
        or row["parameter_profile"] != "P_BASIC" or row["units"] != "return_spread"
        or row["result_shape"] != "exact_ratio"
        or row["future_own_brief_path"] != brief_path or row["future_binding_path"] != binding
    ):
        raise ValueError(f"{signal} relative history profile/owner binding mismatch")
    refs = tuple(f.AuthorityArtifactRefV1(r["path"], r["sha256"]) for r in policy["authority_refs"])
    profile, param, selection = (row[k] for k in ("profile_ref", "parameter_ref", "selection_ref"))
    return Configuration(
        signal, subject, brief, f.VersionRefV1(profile["id"], profile["version"]),
        f.CalculationDefinitionV1(
            signal, row["calculation_definition_version"], row["kernel"], row["equation"],
            (), parents, row["parameter_profile"], row["units"], row["result_shape"],
            (*refs, f.AuthorityArtifactRefV1(POLICY_PATH, POLICY_SHA),
             f.AuthorityArtifactRefV1(brief_path, brief)),
        ),
        f.CalculationParameterSetV1(
            param["id"], param["version"], "P_BASIC", subject, members,
        ),
        f.InputSelectionPolicyVersionV1(
            selection["id"], selection["version"],
            ("subject_instrument", "instrument.id", "session.id", "adjustment.basis", "price.kind"),
            timedelta(seconds=86400), timedelta(0), ("true_instant",), members,
            PROVIDER, VARIANT, SCOPE, 100, 2,
        ),
    )


def _expand(manifest: dict[str, Any], row: dict[str, Any]) -> list[dict[str, Any]]:
    members = list(manifest["base_members"])
    for op in row["operations"]:
        if op["op"] == "append":
            members.append(op["member"])
        elif op["op"] == "replace":
            indexes = [
                i for i, member in enumerate(members)
                if member["observation"]["observation_occurrence_id"] == op["old_id"]
            ]
            if len(indexes) != 1:
                raise ValueError("ambiguous immutable replacement")
            members[indexes[0]] = op["member"]
        else:
            raise ValueError("unadmitted immutable expansion operation")
    members.sort(key=lambda m: (
        datetime.fromisoformat(m["observation"]["received_ts_utc"]),
        m["observation"]["ingestion_sequence"], m["observation"]["observation_occurrence_id"],
    ))
    identities = [m["observation"]["observation_occurrence_id"] for m in members]
    sequences = [m["observation"]["ingestion_sequence"] for m in members]
    if (
        len(members) != row["expanded_count"] or _digest(members) != row["expanded_sha256"]
        or len(set(identities)) != len(identities)
        or len(set(sequences)) != len(sequences) or sequences != sorted(sequences)
    ):
        raise ValueError("immutable aligned history roster mismatch")
    for frame in manifest["frames"]:
        slot = frame["slot"]
        if _digest([m for m in members if m["slot"] == slot]) != row["frame_roster_sha256"][slot]:
            raise ValueError("immutable frame roster mismatch")
    return members


class Authority:
    """Construction-pinned inputs only; expected-result tables are never consulted."""

    def __init__(self, admission: f.OwnerAdmissionV1) -> None:
        policy = _document(POLICY_PATH, POLICY_SHA)
        self.config = _configuration(admission, policy)
        owner = _document(OWNER_PATH, OWNER_SHA)
        _pinned(INVENTORY_PATH, INVENTORY_SHA)
        package, = [x for x in owner["adopted_packages"] if x["package"] == "aligned_history"]
        if (
            owner["exact_total_cases"] != 64
            or package["policy"]["sha256"] != POLICY_SHA
            or package["specimens"]["sha256"] != MANIFEST_SHA
            or package["inventory"]["sha256"] != INVENTORY_SHA
            or package["exact_nonfungible_ceilings"][self.config.signal]
            != (3 if self.config.signal == "D077" else 2)
        ):
            raise ValueError("unaligned controlled history owner grant")
        manifest = _document(MANIFEST_PATH, MANIFEST_SHA)
        self.frames = {row["slot"]: _frame(row) for row in manifest["frames"]}
        if tuple(self.frames) != tuple(f"S{i}" for i in range(8)):
            raise ValueError("exact aligned frame roster required")
        self._specimens: dict[str, tuple[str, tuple[raw.RawObservationOccurrenceV1, ...]]] = {}
        self._legal: dict[str, dict[Key, bytes]] = {}
        allowed = policy["specimen_manifest"]["allowed_specimens"]
        for row in manifest["specimens"]:
            name = row["specimen_id"]
            if name in self._specimens or allowed[name] != {
                "count": row["expanded_count"], "sha256": row["expanded_sha256"],
            }:
                raise ValueError("unadmitted aligned history specimen")
            members = _expand(manifest, row)
            originals = tuple(_original(m["observation"]) for m in members)
            self._specimens[name] = row["expanded_sha256"], originals
            if name in LEGAL_CORPORA:
                expected = {
                    (m["slot"], m["subject"], m["role"]): native.canonical(original)
                    for m, original in zip(members, originals, strict=True)
                }
                if set(expected) != {
                    (slot, subject, role) for slot in self.frames
                    for subject in SUBJECTS.values() for role in ROLES
                } or len(members) != len(expected):
                    raise ValueError("invalid complete legal corpus")
                self._legal[name] = expected
        if set(self._specimens) != set(allowed) or set(self._legal) != set(LEGAL_CORPORA):
            raise ValueError("aligned history specimen inventory mismatch")

    def specimen(self, name: str) -> tuple[str, tuple[raw.RawObservationOccurrenceV1, ...]]:
        if type(name) is not str or name not in self._specimens:
            raise ValueError("exact admitted specimen required")
        return self._specimens[name]

    def check_corpus(
        self, required: tuple[Key, ...],
        actual: tuple[tuple[Key, raw.RawObservationOccurrenceV1], ...],
    ) -> None:
        """One exact original-content intersection, reusable across selected role sets."""
        if len(set(required)) != len(required) or not required:
            raise ValueError("invalid required selected keys")
        observed: dict[Key, bytes] = {}
        for key, original in actual:
            if type(original) is not raw.RawObservationOccurrenceV1 or key in observed:
                raise ValueError("duplicate or nonoriginal selected key")
            observed[key] = native.canonical(original)
        if set(observed) != set(required):
            raise ValueError("missing or extra selected corpus key")
        possible = set(LEGAL_CORPORA)
        for key in required:
            possible.intersection_update(
                name for name, roster in self._legal.items()
                if roster.get(key) == observed[key]
            )
        if not possible:
            raise ValueError("no common legal selected original corpus")


def check_projection(
    original: raw.RawObservationOccurrenceV1, projection: raw.ProjectedRawValueV1,
    mapping: raw.RawSignalProjectionMappingV1,
) -> None:
    """Check the complete projection relation; never replace a public read."""
    if (
        type(original) is not raw.RawObservationOccurrenceV1
        or type(projection) is not raw.ProjectedRawValueV1
    ):
        raise ValueError("actual original and projection DTOs required")
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
        "selection_identity": raw.RawSelectionIdentityV1(tuple(
            (key, _path(original.native_record, path))
            for key, path in mapping.selection_identity_field_paths
        )),
    }
    actual = {field.name: getattr(projection, field.name) for field in fields(projection)}
    if native.canonical(actual) != native.canonical(expected):
        raise ValueError("actual projection/original relation mismatch")


def role_price(
    pair: Pair, frame: Frame, subject: str, mapping: raw.RawSignalProjectionMappingV1,
) -> Decimal | None:
    original, projection = pair
    check_projection(original, projection, mapping)
    role = mapping.raw_signal_catalogue_id.value
    current = role == "R037"
    event = frame.as_of if current else frame.reference
    price_kind = "current_last" if current else "official_close"
    session = frame.current_session if current else frame.reference_session
    allowed = ("10000", "10100", "10201") if current else ("10100",)
    if (
        original.raw_signal_catalogue_ids != (mapping.raw_signal_catalogue_id,)
        or original.subject_instrument != subject or original.source_provider.value != PROVIDER
        or original.source_variant != VARIANT or original.ingestion_sequence_scope.value != SCOPE
        or original.source_temporal_kind != "true_instant"
        or original.source_timezone_native != "UTC"
        or original.source_timestamp_raw != (frame.as_of_text if current else frame.reference_text)
        or not event <= original.received_ts_utc <= frame.cutoff
        or frame.as_of - event > timedelta(seconds=86400)
        or original.native_units != PRICE_UNIT
    ):
        return None
    expected_metadata = (subject, session, "controlled_unadjusted/1", price_kind)
    if any(
        type(_path(original.native_record, path)) is not str
        or _path(original.native_record, path) != expected
        for (_, path), expected in zip(META, expected_metadata, strict=True)
    ):
        return None
    value = projection.native_value
    if (
        type(value) is not Decimal or not value.is_finite()
        or value.as_tuple().exponent != 0 or str(value) not in allowed
    ):
        return None
    return value


def select_role(
    source: f.AlignedHistorySourceV1, frame: Frame, subject: str,
    mapping: raw.RawSignalProjectionMappingV1,
) -> Pair:
    cursor: str | None = None
    cursors: set[str] = set()
    seen: dict[str, bytes] = {}
    selected: list[Pair] = []
    previous: tuple[datetime, str, int, str] | None = None
    for _ in range(2):
        page = source.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,), subject_instrument=subject,
            received_at_or_before_utc=frame.cutoff, event_at_or_before_utc=frame.as_of,
            limit=100, cursor=cursor,
        )
        if (
            type(page) is not raw.ProjectedRawHistoryPageV1
            or type(page.items) is not tuple or len(page.items) > 100
        ):
            raise ValueError("malformed bounded history page")
        for projected in page.items:
            if (
                type(projected) is not raw.ProjectedRawValueV1
                or projected.raw_signal_catalogue_id != mapping.raw_signal_catalogue_id
                or projected.subject_instrument != subject
                or projected.received_ts_utc > frame.cutoff
            ):
                raise ValueError("unexpected public history item")
            oid = projected.observation_occurrence_id
            original = source.get_raw_observation_occurrence(oid)
            direct = source.project_raw_value(
                mapping.raw_signal_catalogue_id, oid, mappings=(mapping,),
            )
            if (
                type(original) is not raw.RawObservationOccurrenceV1
                or type(direct) is not raw.ProjectedRawValueV1
                or original.observation_occurrence_id != oid
                or native.canonical(direct) != native.canonical(projected)
            ):
                raise ValueError("public getter/direct projection/history mismatch")
            # Actual originals and projection must agree even for ineligible roles.
            check_projection(original, projected, mapping)
            if (
                original.source_timestamp_raw is None
                or datetime.fromisoformat(original.source_timestamp_raw) > frame.as_of
            ):
                raise ValueError("public history event ceiling mismatch")
            ordering = (
                projected.received_ts_utc, projected.ingestion_sequence_scope.value,
                projected.ingestion_sequence, oid.value,
            )
            if previous is not None and ordering < previous:
                raise ValueError("nonmonotone public history page")
            previous = ordering
            pair = (original, projected)
            content = native.canonical(pair)
            if oid.value in seen:
                if seen[oid.value] != content:
                    raise ValueError("conflicting duplicate raw identity")
                continue
            seen[oid.value] = content
            if role_price(pair, frame, subject, mapping) is not None:
                selected.append(pair)
        if page.next_cursor is None:
            if len(selected) != 1:
                raise ValueError("exact one eligible distinct original per raw role required")
            return selected[0]
        if (
            type(page.next_cursor) is not str or not page.next_cursor or not page.items
            or page.next_cursor == cursor or page.next_cursor in cursors
        ):
            raise ValueError("nonprogressing public history cursor")
        cursors.add(page.next_cursor)
        cursor = page.next_cursor
    raise ValueError("aligned history page bound exhausted")


def build_source(admission: f.OwnerAdmissionV1, specimen_id: str) -> f.AlignedHistorySourceV1:
    authority = Authority(admission)
    if authority.config.signal in ("D076", "D077"):
        raise ValueError(f"{authority.config.signal} has no own raw source")
    digest, originals = authority.specimen(specimen_id)
    owner = raw.create_owner()
    for original in originals:
        admitted = owner.commands.admit_raw_observation_occurrence(original)
        if type(admitted) is not raw.RawObservationOccurrenceV1 or (
            native.canonical(admitted) != native.canonical(original)
        ):
            raise ValueError("M00 admission changed literal original")
    for original in originals:
        oid = original.observation_occurrence_id
        actual = owner.reads.get_raw_observation_occurrence(oid)
        if type(actual) is not raw.RawObservationOccurrenceV1 or (
            native.canonical(actual) != native.canonical(original)
        ):
            raise ValueError("M00 original readback changed literal")
        # No semantic eligibility filtering here: all sealed negatives must be
        # actual public originals and projections before the owner selects.
        for mapping in MAPS:
            if original.raw_signal_catalogue_ids == (mapping.raw_signal_catalogue_id,):
                projected = owner.reads.project_raw_value(
                    mapping.raw_signal_catalogue_id, oid, mappings=(mapping,),
                )
                if type(projected) is not raw.ProjectedRawValueV1:
                    raise ValueError("M00 sealed original has no actual projection")
                check_projection(actual, projected, mapping)
    reads = owner.reads
    return f.AlignedHistorySourceV1._from_sealed(
        admission=admission, specimen_id=specimen_id, digest=digest, count=len(originals),
        getter=reads.get_raw_observation_occurrence,
        projection=reads.project_raw_value, history=reads.list_projected_raw_history,
    )
