"""D095 fixed matched-contract prior-session IV source, owner and durable reader."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import fields, replace
from datetime import date, datetime
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import _native_codec as native
from . import api as f
from ._record_store import RecordState

ROOT = Path(__file__).resolve().parents[3]
LEAF = "handoff/m02_completion_28_execution/L10a/"
POLICY_PATH = LEAF + "OPTION_IV_PRIOR_SESSION_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json"
POLICY_SHA = "050d167a6f15ae210f3a0b7a776957e6ebb00ce8f674ad9d417e7082951b6a39"
BRIEF_PATH = LEAF + "D095_IMPLEMENTATION_BRIEF.md"
BRIEF = "4885ee1efe9f5832f33a8bf0552caf288990f9f992542c26f535bf378bcbc703"
BINDING_PATH = "implementation/authority/T01_D095_PRIOR_SESSION_IV_AUTHORITY_BINDING.yaml"
BINDING_SHA = "2a4530490537b2552b320db240ac09eb24508ccc9d9347316e517463c4548f32"
OWNER_PATH = (
    "handoff/m02_completion_28_execution/"
    "OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json"
)
OWNER_SHA = "6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41"
SUBJECT = "controlled-nvda-c110-20261023"
SPECIMENS = (
    "VALID_LATEST_VISIBLE",
    "WRONG_SESSION_ONLY",
    "LATE_ONLY",
    "WRONG_CONTRACT",
    "WRONG_MODEL",
    "WRONG_ORIGINAL_UNITS",
    "DUPLICATE_HIGHEST_VINTAGE",
)
ROLES = ("R111", "R183")


def _pinned(path: str, digest: str) -> bytes:
    data = (ROOT / path).read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError("prior-session IV authority bytes mismatch: " + path)
    return data


def policy() -> dict[str, Any]:
    for path, digest in ((BRIEF_PATH, BRIEF), (BINDING_PATH, BINDING_SHA), (OWNER_PATH, OWNER_SHA)):
        _pinned(path, digest)
    return json.loads(_pinned(POLICY_PATH, POLICY_SHA))["source"]


def check_admission(admission: f.OwnerAdmissionV1) -> None:
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted prior-session IV owner")
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
        raise ValueError("unadmitted first-stage IV specimen")
    (row,) = [item for item in policy()["exact_specimens"] if item["id"] == name]
    members = row["members"]
    digest = _digest(members)
    originals = tuple(_original(item) for item in members)
    roles = tuple(_role(item) for item in originals)
    if (
        digest != row["expanded_member_sha256"]
        or len(members) != row["member_count"]
        or len({item.observation_occurrence_id for item in originals}) != len(originals)
        or not 2 <= len(originals) <= 5
        or roles.count("R111") != 1
        or set(roles) != set(ROLES)
    ):
        raise ValueError("immutable prior-session IV roster mismatch")
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


def build_source(admission: f.OwnerAdmissionV1, specimen_id: str) -> f.OptionIVPriorSessionSourceV1:
    check_admission(admission)
    digest, originals = _specimen(specimen_id)
    owner = raw.create_owner()
    for original in originals:
        _exact_original(owner.commands.admit_raw_observation_occurrence(original), original)
    for original in originals:
        _direct(owner.reads, original)
    reads = owner.reads
    del owner
    return f.OptionIVPriorSessionSourceV1._from_sealed(
        admission=admission,
        specimen_id=specimen_id,
        digest=digest,
        count=len(originals),
        getter=reads.get_raw_observation_occurrence,
        projection=reads.project_raw_value,
        history=reads.list_projected_raw_history,
    )


def live_roster(
    source: f.OptionIVPriorSessionSourceV1,
    cutoff: datetime,
) -> tuple[tuple[raw.RawObservationOccurrenceV1, ...], tuple[raw.ProjectedRawValueV1, ...]]:
    digest, originals = _specimen(source.specimen_id)
    if source.expanded_sha256 != digest or source.expanded_count != len(originals):
        raise ValueError("sealed prior-session IV roster mismatch")
    pairs = []
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
                raise ValueError("invalid bounded prior-session IV history")
            for projection in page.items:
                if (
                    type(projection) is not raw.ProjectedRawValueV1
                    or projection.observation_occurrence_id in seen
                ):
                    raise ValueError("invalid or duplicate IV projection")
                seen.add(projection.observation_occurrence_id)
                actual.append(projection)
                if len(actual) > len(originals):
                    raise ValueError("IV history exceeds admitted source")
            if page.next_cursor is None:
                break
            if (
                not page.items
                or type(page.next_cursor) is not str
                or not page.next_cursor
                or page.next_cursor in cursors
            ):
                raise ValueError("nonprogressing IV history cursor")
            cursors.add(page.next_cursor)
            cursor = page.next_cursor
        else:
            raise ValueError("IV history page bound exhausted")
        if len(expected) != len(actual):
            raise ValueError("incomplete IV visible roster")
        for original, projection in zip(expected, actual, strict=True):
            observed = _exact_original(
                source.get_raw_observation_occurrence(original.observation_occurrence_id),
                original,
            )
            direct = _direct(source, observed)
            if native.canonical(direct) != native.canonical(projection):
                raise ValueError("direct and history IV projection mismatch")
            pairs.append((observed, projection))
    ordered = sorted(pairs, key=lambda pair: _order(pair[0]))
    return tuple(o for o, _ in ordered), tuple(p for _, p in ordered)


def _validate_roster(
    originals: tuple[raw.RawObservationOccurrenceV1, ...],
    projections: tuple[raw.ProjectedRawValueV1, ...],
    cutoff: datetime,
) -> None:
    if len(originals) != len(projections) or not originals:
        raise ValueError("exact nonempty IV original/projection roster required")
    actual = native.canonical(originals)
    # Match the full visible roster, not a caller-supplied digest or just the
    # chosen reference. Late observations are deliberately not part of identity.
    if not any(
        actual
        == native.canonical(
            tuple(
                sorted(
                    (o for o in _specimen(name)[1] if o.received_ts_utc <= cutoff),
                    key=_order,
                )
            )
        )
        for name in SPECIMENS
    ):
        raise ValueError("IV visible original roster not admitted")
    for original, projection in zip(originals, projections, strict=True):
        check_projection(original, projection, mapping_for(_role(original)))


SIGNAL = "D095"
PROFILE = f.VersionRefV1("t01-option-iv-prior-session-d095", 1)
CALENDAR = f.VersionRefV1("t01-option-iv-session-calendar", 1)
NAMESPACE = "neutral_market_measurement_truth/option_iv_prior_session/v1"
DEFINITION = f.CalculationDefinitionV1(
    SIGNAL,
    "T01-D095-OPTION-IV-PRIOR-SESSION-DEF-V1",
    "K03_CHANGE_RETURN",
    "100*(current IV - unique highest eligible final prior trading-session IV).",
    ("R111", "R183"),
    (),
    "P_WINDOW",
    "volatility_points",
    "exact_ratio",
    (
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
            "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
        ),
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
            "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
        ),
        f.AuthorityArtifactRefV1(POLICY_PATH, POLICY_SHA),
        f.AuthorityArtifactRefV1(BRIEF_PATH, BRIEF),
    ),
)
CONTRACT = {
    "contract": {"id": SUBJECT, "multiplier": "100"},
    "underlying": {"id": "NVDA"},
    "expiry": {"date": "2026-10-23"},
    "strike": {"key": "110"},
    "option": {"right": "C"},
    "currency": {"code": "USD"},
    "instrument": {"kind": "option"},
}


def _request_check(request: f.OptionIVPriorSessionRequestV1) -> None:
    if type(request) is not f.OptionIVPriorSessionRequestV1:
        raise TypeError("exact D095 request required")
    f._Validated.__post_init__(request)
    source_policy = policy()
    if (
        request.derived_signal_id != SIGNAL
        or request.subject_instrument != SUBJECT
        or request.source_profile_ref != PROFILE
        or request.calendar_ref != CALENDAR
        or request.calculation_definition_version != DEFINITION.calculation_definition_version
        or request.predecessor_occurrence_ids != ()
        or request.as_of_utc != datetime.fromisoformat(source_policy["as_of_utc"])
        or request.knowledge_cutoff_utc
        != datetime.fromisoformat(source_policy["knowledge_cutoff_utc"])
    ):
        raise ValueError("unadmitted D095 request identity or clock")


def _prior_session(request: f.OptionIVPriorSessionRequestV1) -> tuple[date, datetime]:
    calendar = policy()["calendar"]
    if calendar["ref"] != f"{CALENDAR.context_id}/{CALENDAR.version}":
        raise ValueError("D095 calendar identity mismatch")
    intervals = calendar["intervals"]
    open_intervals = [interval for interval in intervals if interval["trading_date"] is not None]
    (current,) = [
        interval
        for interval in open_intervals
        if datetime.fromisoformat(interval["start_utc"])
        <= request.as_of_utc
        < datetime.fromisoformat(interval["end_utc"])
    ]
    prior = max(
        (
            interval
            for interval in open_intervals
            if interval["trading_date"] < current["trading_date"]
        ),
        key=lambda interval: interval["trading_date"],
    )
    return date.fromisoformat(prior["trading_date"]), datetime.fromisoformat(prior["end_utc"])


def _compatible(
    original: raw.RawObservationOccurrenceV1,
    projection: raw.ProjectedRawValueV1,
    source_policy: dict[str, Any],
    role: str,
) -> bool:
    record = original.native_record
    value = projection.native_value
    return (
        original.subject_instrument == SUBJECT
        and original.native_units == projection.native_units == source_policy["units"]
        and all(record[key] == expected for key, expected in CONTRACT.items())
        and record["model"]["convention"] == source_policy["model_convention"]
        and record["value"]["role"] == role
        and type(value) is Decimal
        and value.is_finite()
        and value >= 0
    )


def _calculate(
    request: f.OptionIVPriorSessionRequestV1,
    originals: tuple[raw.RawObservationOccurrenceV1, ...],
    projections: tuple[raw.ProjectedRawValueV1, ...],
) -> tuple[
    raw.RawObservationOccurrenceV1,
    raw.RawObservationOccurrenceV1,
    date,
    datetime,
    f.ExactRatioV1,
]:
    _request_check(request)
    _validate_roster(originals, projections, request.knowledge_cutoff_utc)
    source_policy = policy()
    pairs = tuple(zip(originals, projections, strict=True))
    (current,) = [pair for pair in pairs if _role(pair[0]) == "R111"]
    original, projection = current
    if (
        not _compatible(original, projection, source_policy, "model_iv")
        or original.source_temporal_kind != "receipt_only"
        or original.source_timestamp_raw is not None
        or original.source_timezone_native is not None
        or original.received_ts_utc != request.as_of_utc
        or original.received_ts_utc > request.knowledge_cutoff_utc
    ):
        raise ValueError("D095 actual current role/clock/contract invariant")
    model = original.native_record["model"]
    for name in ("quote_receipt_utc", "underlying_receipt_utc"):
        receipt = datetime.fromisoformat(model[name])
        f._utc(receipt)
        if receipt >= original.received_ts_utc:
            raise ValueError("D095 related actual receipt must precede current")
    prior, close = _prior_session(request)
    eligible = []
    for ref, projected in pairs:
        if _role(ref) != "R183":
            continue
        bar = ref.native_record["bar"]
        revision = bar["revision"]
        if (
            not _compatible(ref, projected, source_policy, "historical_iv_close")
            or ref.source_temporal_kind != "date_only"
            or ref.source_timestamp_raw != bar["date"]
            or bar["date"] != prior.isoformat()
            or bar["bar_size"] != "1 day"
            or bar["what_to_show"] != "OPTION_IMPLIED_VOLATILITY"
            or bar["session_calendar_ref"] != source_policy["calendar"]["ref"]
            or ref.source_timezone_native != source_policy["calendar"]["iana_zone"]
            or bar["final"] is not True
            or type(revision) is not int
            or revision <= 0
            or revision not in source_policy["admitted_vintages"]
            or ref.revision_vintage_native != f"controlled-final/{revision}"
            or not close <= ref.received_ts_utc <= request.knowledge_cutoff_utc
        ):
            continue
        eligible.append((revision, ref, projected))
    if not eligible:
        raise ValueError("D095 no eligible exact prior-session reference")
    highest = max(item[0] for item in eligible)
    winners = [(ref, projected) for rev, ref, projected in eligible if rev == highest]
    if len(winners) != 1:
        raise ValueError("D095 ambiguous highest visible final revision")
    reference, ref_projection = winners[0]
    current_iv, ref_iv = projection.native_value, ref_projection.native_value
    assert type(current_iv) is Decimal and type(ref_iv) is Decimal
    result = 100 * (Fraction(current_iv) - Fraction(ref_iv))
    return original, reference, prior, close, f.ExactRatioV1(result.numerator, result.denominator)


_TAG = "OptionIVPriorSessionOccurrenceV1"


def _record(value: Any, cls: type[Any]) -> dict[str, Any]:
    if type(value) is not cls:
        raise TypeError("exact D095 record required")
    return {field.name: getattr(value, field.name) for field in fields(cls)}


def _rebuild(content: Any, cls: type[Any]) -> Any:
    if type(content) is not dict or set(content) != {field.name for field in fields(cls)}:
        raise ValueError("D095 record field set mismatch")
    return cls(**content)


def _content(value: f.OptionIVPriorSessionOccurrenceV1) -> dict[str, Any]:
    content = _record(value, f.OptionIVPriorSessionOccurrenceV1)
    content["request"] = _record(value.request, f.OptionIVPriorSessionRequestV1)
    if type(value.prior_trading_date) is not date:
        raise TypeError("D095 exact typed session date required")
    content["prior_trading_date"] = value.prior_trading_date.isoformat()
    return content


def _envelope(content: dict[str, Any]) -> bytes:
    return native.canonical({"record": _TAG, "version": 1, "content": content})


def _encode(value: f.OptionIVPriorSessionOccurrenceV1) -> bytes:
    return _envelope(_content(value))


def _identity(value: f.OptionIVPriorSessionOccurrenceV1) -> str:
    content = _content(value)
    del content["derived_occurrence_id"]
    del content["calculated_at_utc"]
    return "mmtoptionivprior1:" + hashlib.sha256(_envelope(content)).hexdigest()


def _decode(payload: bytes) -> f.OptionIVPriorSessionOccurrenceV1:
    envelope = native.decode(payload, dict)
    if (
        set(envelope) != {"record", "version", "content"}
        or envelope["record"] != _TAG
        or type(envelope["version"]) is not int
        or envelope["version"] != 1
    ):
        raise ValueError("unadmitted D095 record envelope")
    content = envelope["content"]
    if type(content) is not dict or type(content["prior_trading_date"]) is not str:
        raise ValueError("invalid D095 content/session date")
    content["request"] = _rebuild(content["request"], f.OptionIVPriorSessionRequestV1)
    content["prior_trading_date"] = date.fromisoformat(content["prior_trading_date"])
    value = _rebuild(content, f.OptionIVPriorSessionOccurrenceV1)
    if _encode(value) != payload:
        raise ValueError("D095 canonical durable readback mismatch")
    return value


def _validate(value: f.OptionIVPriorSessionOccurrenceV1) -> None:
    if type(value) is not f.OptionIVPriorSessionOccurrenceV1:
        raise TypeError("exact D095 occurrence required")
    f._Validated.__post_init__(value)
    current, reference, prior, close, result = _calculate(
        value.request,
        value.visible_originals,
        value.visible_projections,
    )
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or value.derived_signal_id != SIGNAL
        or value.definition != DEFINITION
        or value.source_policy_sha256 != POLICY_SHA
        or value.source_profile_ref != PROFILE
        or value.calendar_ref != CALENDAR
        or value.predecessor_occurrence_ids != ()
        or native.canonical(value.projection_mappings)
        != native.canonical(tuple(mapping_for(rid) for rid in ROLES))
        or value.selected_current_id != current.observation_occurrence_id
        or value.selected_reference_id != reference.observation_occurrence_id
        or value.prior_trading_date != prior
        or value.configured_reference_close_utc != close
        or value.result != result
        or value.units != "volatility_points"
        or value.result_shape != "exact_ratio"
        or value.effective_as_of_utc != value.request.as_of_utc
        or value.knowledge_cutoff_utc != value.request.knowledge_cutoff_utc
        or value.calculated_at_utc < value.knowledge_cutoff_utc
        or value.derived_occurrence_id != _identity(value)
    ):
        raise ValueError("D095 durable semantic or identity mismatch")


def _store(storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(storage, _decode, _validate, encode=_encode)


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self._state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> f.OptionIVPriorSessionOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("exact nonempty D095 occurrence identity required")
        return next(
            (
                value
                for value in self._state.all()
                if value.derived_occurrence_id == derived_occurrence_id
            ),
            None,
        )

    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.OptionIVPriorSessionOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            derived_signal_id != SIGNAL
            or subject_instrument != SUBJECT
            or type(limit) is not int
            or not 1 <= limit <= 64
        ):
            raise ValueError("bounded D095 history required")
        rows = (
            value
            for value in self._state.all()
            if value.effective_as_of_utc <= effective_at_or_before_utc
            and value.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(
            sorted(
                rows,
                key=lambda value: (
                    value.effective_as_of_utc,
                    value.knowledge_cutoff_utc,
                    value.derived_occurrence_id,
                ),
            )
        )[:limit]


class _Owner:
    def __init__(
        self,
        source: f.OptionIVPriorSessionSourceV1,
        state: RecordState,
        utc_now: Callable[[], datetime],
    ) -> None:
        self._source, self._state, self._utc_now = source, state, utc_now
        self.reads = _Reads(state)

    def materialise(
        self,
        request: f.OptionIVPriorSessionRequestV1,
    ) -> f.OptionIVPriorSessionOccurrenceV1 | None:
        if type(request) is not f.OptionIVPriorSessionRequestV1:
            raise TypeError("exact D095 request required")
        now = self._utc_now()
        f._utc(now)
        try:
            _request_check(request)
            if now < request.knowledge_cutoff_utc:
                return None
            originals, projections = live_roster(self._source, request.knowledge_cutoff_utc)
            current, reference, prior, close, result = _calculate(request, originals, projections)
            row = f.OptionIVPriorSessionOccurrenceV1(
                "M02",
                NAMESPACE,
                BRIEF,
                SIGNAL,
                "pending",
                request,
                DEFINITION,
                POLICY_SHA,
                PROFILE,
                CALENDAR,
                tuple(mapping_for(r) for r in ROLES),
                originals,
                projections,
                current.observation_occurrence_id,
                reference.observation_occurrence_id,
                prior,
                close,
                (),
                result,
                "volatility_points",
                "exact_ratio",
                request.as_of_utc,
                request.knowledge_cutoff_utc,
                now,
            )
            row = replace(row, derived_occurrence_id=_identity(row))
        except (TypeError, ValueError, ArithmeticError, KeyError):
            return None
        return cast(f.OptionIVPriorSessionOccurrenceV1, self._state.append(row))


def build_owner(
    admission: f.OwnerAdmissionV1,
    source: f.OptionIVPriorSessionSourceV1,
    storage: f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.OptionIVPriorSessionOwnerV1:
    check_admission(admission)
    if (
        type(source) is not f.OptionIVPriorSessionSourceV1
        or not source._matches_admission(admission)
        or type(storage) is not f.SQLiteStorageV1
        or storage.create is not True
        or not callable(utc_now)
    ):
        raise ValueError("unadmitted D095 source/storage/clock")
    return _Owner(source, _store(storage), utc_now)


def build_reader(
    admission: f.OwnerAdmissionV1,
    storage: f.SQLiteReadStorageV1,
) -> f.OptionIVPriorSessionReadsV1:
    check_admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D095 read-only storage")
    return _Reads(_store(storage))
