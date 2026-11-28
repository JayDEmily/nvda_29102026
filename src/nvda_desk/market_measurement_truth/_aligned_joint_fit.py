"""One exact controlled aligned joint fit, three separate coefficient owners."""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Iterable
from dataclasses import replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import Any, cast

from . import _aligned_history_codec as history_codec
from . import _aligned_history_returns as history
from . import _aligned_history_source as source
from . import _log_return, _native_codec as native
from . import api as f
from ._record_store import RecordState

ROLES = ("D075", "D071", "D076", "D077")
UNDERLYING = ("D075", "D071", "D072", "D073", "D074")
MEMBERS = ("NVDA", "SPY", "QQQ", "SMH", "SOXX")
OWN = {
    "D079": (
        "beta_market", "47b4c5d27d7ffc57710d70973825500524e3d9bbc179cc59df0d356381612127",
        "c90aec925d606bcf9537ffad014338a579ab856884d659a85dd4ecd10050cf54", 6,
    ),
    "D080": (
        "beta_tech", "69f38747173cd464ae8586f919caa23f8ae754fbb1190b001675cae05e5a709e",
        "dcc6589fe36f091f4ea68da97b011ec67ea416e706e1ba9089da8223e1cd84d7", 5,
    ),
    "D081": (
        "beta_semi", "cf2bf8c51611b8b5baf8a98d1f42fcecd63f069dd45b20dc9135844b99b6e90f",
        "a2dfca758a22fbe7898d7534a86d094457333ad74ef5022ffd0d968334183eae", 3,
    ),
}
FIT_PROFILE = f.VersionRefV1("t01-l01a-shared-joint-ols", 1)
MODEL = "T01-L01A-JOINT-OLS-WITH-INTERCEPT-V1"
NUMERIC = "T01-L01A-EXACT-FRACTION-GRAM-INF-V1"
Rows = tuple[tuple[f.AlignedHistoryOccurrenceV1, ...], ...]
Original = tuple[source.Key, source.raw.RawObservationOccurrenceV1]


def _ref(value: dict[str, Any]) -> f.VersionRefV1:
    return f.VersionRefV1(value["id"], value["version"])


def _parent_admission(signal: str) -> f.OwnerAdmissionV1:
    briefs = {**source.BRIEFS, "D076": source.D076_BRIEF, "D077": source.D077_BRIEF}
    return f.OwnerAdmissionV1("M02", briefs[signal])


class Authority:
    """Exact own profile and unchanged, separately admitted parent authorities."""

    def __init__(self, admission: f.OwnerAdmissionV1) -> None:
        if type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02":
            raise ValueError("exact M02 coefficient admission required")
        matches = [s for s, (_, brief, _, _) in OWN.items()
                   if brief == admission.implementation_brief_sha256]
        if len(matches) != 1:
            raise ValueError("unadmitted coefficient jurisdiction")
        signal = matches[0]
        self.component, brief, binding_hash, count = OWN[signal]
        policy = source._document(source.POLICY_PATH, source.POLICY_SHA)
        brief_path = source.LEAF + f"ALIGNED_HISTORY_{signal}_IMPLEMENTATION_BRIEF.md"
        binding_path = f"implementation/authority/T01_ALIGNED_HISTORY_{signal}_AUTHORITY_BINDING.yaml"
        source._pinned(brief_path, brief)
        source._pinned(binding_path, binding_hash)
        owner = source._document(source.OWNER_PATH, source.OWNER_SHA)
        source._pinned(source.INVENTORY_PATH, source.INVENTORY_SHA)
        package, = [p for p in owner["adopted_packages"] if p["package"] == "aligned_history"]
        if (
            owner["exact_total_cases"] != 64
            or package["policy"]["sha256"] != source.POLICY_SHA
            or package["specimens"]["sha256"] != source.MANIFEST_SHA
            or package["inventory"]["sha256"] != source.INVENTORY_SHA
            or package["exact_nonfungible_ceilings"][signal] != count
        ):
            raise ValueError("unaligned coefficient grant")
        row = policy["profiles"][signal]
        if (
            row["subject"] != "NVDA" or tuple(row["members"]) != MEMBERS
            or row["raw_dependencies"] != [] or tuple(row["derived_dependencies"]) != ROLES
            or row["kernel"] != "K06_REGRESSION_DEPENDENCE"
            or row["parameter_profile"] != "P_REGRESSION"
            or row["equation"] != self.component + " from joint OLS with intercept"
            or row["units"] != "beta" or row["result_shape"] != "exact_ratio"
            or row["future_own_brief_path"] != brief_path or row["future_binding_path"] != binding_path
            or policy["joint_fit"]["fit_profile"] != "t01-l01a-shared-joint-ols/1"
            or tuple(policy["joint_fit"]["ordered_row_members"]) != ROLES
            or policy["joint_fit"]["training_rows"] != 6
        ):
            raise ValueError("coefficient profile/authority mismatch")
        refs = tuple(f.AuthorityArtifactRefV1(r["path"], r["sha256"])
                     for r in policy["authority_refs"])
        profile, param, selection = (_ref(row[k]) for k in
                                     ("profile_ref", "parameter_ref", "selection_ref"))
        self.config = source.Configuration(
            signal, "NVDA", brief, profile,
            f.CalculationDefinitionV1(
                signal, row["calculation_definition_version"], row["kernel"], row["equation"],
                (), ROLES, row["parameter_profile"], row["units"], row["result_shape"],
                (*refs, f.AuthorityArtifactRefV1(source.POLICY_PATH, source.POLICY_SHA),
                 f.AuthorityArtifactRefV1(brief_path, brief)),
            ),
            f.CalculationParameterSetV1(
                param.context_id, param.version, row["parameter_profile"], "NVDA", MEMBERS,
            ),
            f.InputSelectionPolicyVersionV1(
                selection.context_id, selection.version,
                ("subject_instrument", "instrument.id", "session.id", "adjustment.basis", "price.kind"),
                timedelta(seconds=86400), timedelta(0), ("true_instant",), MEMBERS,
                source.PROVIDER, source.VARIANT, source.SCOPE, 100, 2,
            ),
        )
        self.parents = {s: source.Authority(_parent_admission(s)) for s in (*UNDERLYING, "D076", "D077")}
        self.corpus = self.parents["D075"]
        self.frames = self.corpus.frames
        self.windows = {
            w["origin_slot"]: (
                tuple(w["ordered_training_slots"]), datetime.fromisoformat(w["as_of"]),
                datetime.fromisoformat(w["cutoff"]),
            ) for w in policy["clocks"]["fit_windows"]
        }
        if self.windows != {
            s: (tuple(f"S{i}" for i in range(start, start + 6)),
                self.frames[s].as_of, self.frames[s].as_of + timedelta(seconds=4))
            for s, start in (("S6", 1), ("S7", 2))
        }:
            raise ValueError("exact admitted joint-fit windows required")


def _request_frame(
    authority: Authority, request: f.AlignedFitRequestV1, now: datetime,
) -> source.Frame:
    if type(request) is not f.AlignedFitRequestV1:
        raise TypeError("exact coefficient fit request required")
    f._Validated.__post_init__(request)
    f._utc(now)
    cfg = authority.config
    window = authority.windows.get(request.origin_slot)
    if window is None:
        raise ValueError("unadmitted fit origin")
    slots, asof, cutoff = window
    frame = authority.frames[request.origin_slot]
    for row in request.rows:
        row.__post_init__()
    expected = f.AlignedFitRequestV1(
        cfg.signal, cfg.subject, frame.slot, asof, cutoff,
        cfg.definition.calculation_definition_version, cfg.profile,
        f.VersionRefV1(cfg.parameter.context_id, cfg.parameter.version),
        f.VersionRefV1(cfg.selection.context_id, cfg.selection.version),
        (frame.context.ref,), request.rows,
    )
    if request != expected or tuple(row.slot for row in request.rows) != slots or now < cutoff:
        raise ValueError("unadmitted fit request, metadata or calculation clock")
    return frame


def _unique_sample(request: f.AlignedFitRequestV1) -> None:
    ids = tuple(identity for row in request.rows for identity in row.member_occurrence_ids)
    if len(ids) != 24 or len(set(ids)) != 24:
        raise ValueError("24 distinct actual sample member identities required")


def _lookup_rows(
    readers: tuple[f.AlignedHistoryReadsV1, ...], requests: tuple[f.AlignedFitRowRequestV1, ...],
) -> Rows:
    rows = []
    for row in requests:
        parents = []
        for reader, identity in zip(readers, row.member_occurrence_ids, strict=True):
            parent = reader.get_derived_occurrence(identity)
            if type(parent) is not f.AlignedHistoryOccurrenceV1:
                raise ValueError("actual ordered history parent not found")
            parents.append(parent)
        rows.append(tuple(parents))
    return tuple(rows)


def _align_row(
    authority: Authority, request: f.AlignedFitRowRequestV1,
    row: tuple[f.AlignedHistoryOccurrenceV1, ...],
) -> None:
    frame = authority.frames[request.slot]
    if len(row) != 4:
        raise ValueError("exact four actual history roles required")
    for sig, identity, parent in zip(ROLES, request.member_occurrence_ids, row, strict=True):
        pa = authority.parents[sig]
        if (
            type(parent) is not f.AlignedHistoryOccurrenceV1
            or parent.derived_occurrence_id != identity or parent.derived_signal_id != sig
            or parent.request.slot != frame.slot or parent.effective_as_of_utc != frame.as_of
            or parent.knowledge_cutoff_utc != frame.cutoff
            or parent.window_context != frame.context or parent.window_seconds != frame.seconds
        ):
            raise ValueError("actual history row alignment mismatch")
        f._Validated.__post_init__(parent)
        if sig in ("D076", "D077"):
            expected = history._relative_produce(
                pa, tuple(authority.parents[s] for s in pa.config.definition.derived_dependencies),
                parent.request, parent.predecessors, parent.calculated_at_utc,
            )
        else:
            expected = history._produce(
                pa, parent.request,
                tuple(zip(parent.original_observations, parent.selected_projections, strict=True)),
                parent.calculated_at_utc,
            )
        if history_codec.encode(parent) != history_codec.encode(expected):
            raise ValueError("actual history parent profile, lineage or identity mismatch")


def _same_parent(a: f.AlignedHistoryOccurrenceV1, b: f.AlignedHistoryOccurrenceV1) -> None:
    if (
        a.derived_occurrence_id != b.derived_occurrence_id
        or history_codec.encode(a) != history_codec.encode(b)
    ):
        raise ValueError("shared actual history parent identity or payload mismatch")


def _shared_underlying(
    row: tuple[f.AlignedHistoryOccurrenceV1, ...],
) -> tuple[f.AlignedHistoryOccurrenceV1, ...]:
    target, market, tech, semi = row
    qqq, nested_market = tech.predecessors
    smh, soxx, nested_qqq = semi.predecessors
    _same_parent(market, nested_market)
    _same_parent(qqq, nested_qqq)
    return target, market, qqq, smh, soxx


def _visible(
    parent: f.AlignedHistoryOccurrenceV1 | f.AlignedCoefficientOccurrenceV1, ceiling: datetime,
) -> None:
    f._utc(ceiling)
    f._utc(parent.knowledge_cutoff_utc)
    f._utc(parent.calculated_at_utc)
    if parent.knowledge_cutoff_utc > ceiling or parent.calculated_at_utc > ceiling:
        raise ValueError("actual parent unavailable at decision ceiling")


def _row_originals(
    authority: Authority, slot: str, histories: tuple[f.AlignedHistoryOccurrenceV1, ...],
) -> tuple[Original, ...]:
    actual = tuple(
        ((slot, authority.parents[sig].config.subject, role), original)
        for sig, parent in zip(UNDERLYING, histories, strict=True)
        for role, original in zip(source.ROLES, parent.original_observations, strict=True)
    )
    if len(actual) != 10 or len({v.observation_occurrence_id for _, v in actual}) != 10:
        raise ValueError("ten distinct actual row original facts required")
    return actual


def _checked_rows(
    authority: Authority, requests: tuple[f.AlignedFitRowRequestV1, ...],
    rows: Rows, ceiling: datetime,
) -> tuple[Original, ...]:
    # Stage-major order: no later invariant can hide an earlier row failure.
    for request, row in zip(requests, rows, strict=True):
        _align_row(authority, request, row)
    histories = tuple(_shared_underlying(row) for row in rows)
    for row in rows:
        for parent in row:
            _visible(parent, ceiling)
    return tuple(
        original for request, members in zip(requests, histories, strict=True)
        for original in _row_originals(authority, request.slot, members)
    )


def _check_corpus(
    authority: Authority, slots: tuple[str, ...], actual: tuple[Original, ...],
) -> None:
    required = tuple((slot, subject, role) for slot in slots
                     for subject in MEMBERS for role in source.ROLES)
    if len({value.observation_occurrence_id for _, value in actual}) != len(required):
        raise ValueError("distinct actual original facts across the complete sample required")
    authority.corpus.check_corpus(required, actual)


def _bounded(value: Fraction) -> Fraction:
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > 4096:
        raise ValueError("exact fit arithmetic bound exceeded")
    return value


def _sum(values: Iterable[Fraction]) -> Fraction:
    total = Fraction(0)
    for value in values:
        total = _bounded(total + value)
    return total


def _ratio(value: Decimal | f.ExactRatioV1) -> Fraction:
    if type(value) is Decimal:
        return _bounded(Fraction(value))
    if type(value) is f.ExactRatioV1:
        value.__post_init__()
        return _bounded(Fraction(value.numerator, value.denominator))
    raise TypeError("exact actual history result required")


def _norm(matrix: list[list[Fraction]]) -> Fraction:
    return max(_sum(abs(v) for v in row) for row in matrix)


def _numeric(rows: Rows) -> tuple[Fraction, Fraction, tuple[Fraction, ...]]:
    a = _bounded(Fraction(_log_return._logarithm(Decimal(101), Decimal(100))))
    x, y = [], []
    for row in rows:
        target, *predictors = (_bounded(_ratio(p.result) / a) for p in row)
        if abs(target) > 1 or target.denominator > 2 or any(
            abs(v) > 2 or v.denominator > 2 for v in predictors
        ):
            raise ValueError("actual normalized fit domain exceeded")
        x.append([Fraction(1), *predictors])
        y.append(target)
    if len(x) != 6 or any(len(row) != 4 for row in x):
        raise ValueError("exact six-row four-column design required")
    gram = [[_sum(_bounded(r[i] * r[j]) for r in x) for j in range(4)] for i in range(4)]
    h = [_sum(_bounded(r[i] * v) for r, v in zip(x, y, strict=True)) for i in range(4)]
    # The augmented matrix simultaneously carries the inverse and one vector.
    augmented = [
        [*gram[i], *(Fraction(int(i == j)) for j in range(4)), h[i]] for i in range(4)
    ]
    determinant = Fraction(1)
    for col in range(4):
        pivot = next((i for i in range(col, 4) if augmented[i][col]), None)
        if pivot is None:
            raise ValueError("rank-deficient exact joint design")
        if pivot != col:
            augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
            determinant = _bounded(-determinant)
        scale = augmented[col][col]
        determinant = _bounded(determinant * scale)
        augmented[col] = [_bounded(v / scale) for v in augmented[col]]
        for i in range(4):
            if i == col:
                continue
            factor = augmented[i][col]
            augmented[i] = [
                _bounded(v - _bounded(factor * p))
                for v, p in zip(augmented[i], augmented[col], strict=True)
            ]
    inverse = [row[4:8] for row in augmented]
    condition = _bounded(_norm(gram) * _norm(inverse))
    if condition > 50:
        raise ValueError("exact joint Gram condition outside admitted domain")
    vector = tuple(row[8] for row in augmented)
    return determinant, condition, (_bounded(a * vector[0]), *vector[1:])


def _exact(value: Fraction) -> f.ExactRatioV1:
    _bounded(value)
    return f.ExactRatioV1(value.numerator, value.denominator)


def _digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _envelope(cls: type[Any], content: dict[str, Any]) -> bytes:
    return native.canonical({"record": cls.__name__, "version": 1, "content": content})


def _unpack(payload: bytes, cls: type[Any]) -> dict[str, Any]:
    from dataclasses import fields

    envelope = native.decode(payload, dict)
    if (
        set(envelope) != {"record", "version", "content"} or envelope["record"] != cls.__name__
        or type(envelope["version"]) is not int or envelope["version"] != 1
        or type(envelope["content"]) is not dict
        or set(envelope["content"]) != {field.name for field in fields(cls)}
    ):
        raise ValueError("unadmitted joint-fit envelope")
    return cast(dict[str, Any], envelope["content"])


def _fit_content(value: f.AlignedFitManifestV1) -> dict[str, Any]:
    content = history_codec._record(value, f.AlignedFitManifestV1)
    content["rows"] = tuple(tuple(history_codec.encode(parent) for parent in row) for row in value.rows)
    return content


def _fit_bytes(value: f.AlignedFitManifestV1) -> bytes:
    return _envelope(f.AlignedFitManifestV1, _fit_content(value))


def _fit_identity(value: f.AlignedFitManifestV1) -> str:
    content = _fit_content(value)
    del content["fit_id"]
    return "mmtafit1:" + _digest(_envelope(f.AlignedFitManifestV1, content))


def _fit_decode(payload: bytes) -> f.AlignedFitManifestV1:
    content = _unpack(payload, f.AlignedFitManifestV1)
    rows = content["rows"]
    if type(rows) is not tuple or any(
        type(row) is not tuple or any(type(parent) is not bytes for parent in row) for row in rows
    ):
        raise ValueError("exact nested actual history envelopes required")
    content["rows"] = tuple(tuple(history_codec.decode(parent) for parent in row) for row in rows)
    fit = f.AlignedFitManifestV1(**content)
    if _fit_bytes(fit) != payload:
        raise ValueError("fit canonical round-trip mismatch")
    return fit


_METADATA = {
    "parameter_set": f.CalculationParameterSetV1,
    "input_selection_policy": f.InputSelectionPolicyVersionV1,
    "window_context": f.WindowContextV1,
}


def _content(value: f.AlignedCoefficientOccurrenceV1) -> dict[str, Any]:
    content = history_codec._record(value, f.AlignedCoefficientOccurrenceV1)
    request = history_codec._record(value.request, f.AlignedFitRequestV1)
    request["rows"] = tuple(history_codec._record(row, f.AlignedFitRowRequestV1)
                            for row in value.request.rows)
    content["request"] = request
    content["fit"] = _fit_bytes(value.fit)
    for name, cls in _METADATA.items():
        content[name] = history_codec._record(getattr(value, name), cls)
    return content


def _encode(value: f.AlignedCoefficientOccurrenceV1) -> bytes:
    return _envelope(f.AlignedCoefficientOccurrenceV1, _content(value))


def _identity(value: f.AlignedCoefficientOccurrenceV1) -> str:
    content = _content(value)
    del content["derived_occurrence_id"]
    del content["calculated_at_utc"]
    return "mmtacoef1:" + _digest(_envelope(f.AlignedCoefficientOccurrenceV1, content))


def _decode(payload: bytes) -> f.AlignedCoefficientOccurrenceV1:
    content = _unpack(payload, f.AlignedCoefficientOccurrenceV1)
    request = content["request"]
    if type(request) is not dict or type(request.get("rows")) is not tuple or type(content["fit"]) is not bytes:
        raise ValueError("invalid joint-fit request or manifest envelope")
    request["rows"] = tuple(history_codec._rebuild(row, f.AlignedFitRowRequestV1)
                            for row in request["rows"])
    content["request"] = history_codec._rebuild(request, f.AlignedFitRequestV1)
    content["fit"] = _fit_decode(content["fit"])
    for name, cls in _METADATA.items():
        content[name] = history_codec._rebuild(content[name], cls)
    value = f.AlignedCoefficientOccurrenceV1(**content)
    if _encode(value) != payload:
        raise ValueError("coefficient canonical round-trip mismatch")
    return value


def _produce(
    authority: Authority, request: f.AlignedFitRequestV1, rows: Rows, now: datetime,
) -> f.AlignedCoefficientOccurrenceV1:
    frame = _request_frame(authority, request, now)
    _unique_sample(request)
    actual = _checked_rows(authority, request.rows, rows, request.knowledge_cutoff_utc)
    slots = tuple(row.slot for row in request.rows)
    _check_corpus(authority, slots, actual)
    determinant, condition, vector = _numeric(rows)
    fit = f.AlignedFitManifestV1(
        "pending", FIT_PROFILE, source.POLICY_SHA, MODEL, NUMERIC, request.origin_slot,
        request.as_of_utc, request.knowledge_cutoff_utc, slots, rows,
        tuple(tuple(p.derived_occurrence_id for p in row) for row in rows),
        tuple(tuple(_digest(history_codec.encode(p)) for p in row) for row in rows),
        _exact(determinant), _exact(condition), *(_exact(v) for v in vector),
    )
    fit = replace(fit, fit_id=_fit_identity(fit))
    cfg = authority.config
    value = f.AlignedCoefficientOccurrenceV1(
        "M02", history.NAMESPACE, cfg.brief, cfg.signal, "pending", request, cfg.definition,
        source.POLICY_SHA, cfg.profile, cfg.parameter, cfg.selection, frame.context,
        authority.component, fit, getattr(fit, authority.component), cfg.definition.units,
        cfg.definition.result_shape, request.as_of_utc, request.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def _store(
    authority: Authority, storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1,
) -> RecordState:
    def validate(value: f.AlignedCoefficientOccurrenceV1) -> None:
        if type(value) is not f.AlignedCoefficientOccurrenceV1:
            raise TypeError("exact coefficient occurrence required")
        f._Validated.__post_init__(value)
        expected = _produce(authority, value.request, value.fit.rows, value.calculated_at_utc)
        if _encode(value) != _encode(expected):
            raise ValueError("coefficient actual evidence, vector, metadata or identity mismatch")

    return RecordState(storage, _decode, validate, encode=_encode)


class _Reads:
    def __init__(self, authority: Authority, state: RecordState) -> None:
        self._authority, self._state = authority, state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.AlignedCoefficientOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty coefficient identity required")
        return next((row for row in cast(tuple[f.AlignedCoefficientOccurrenceV1, ...], self._state.all())
                     if row.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.AlignedCoefficientOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        cfg = self._authority.config
        if (
            derived_signal_id != cfg.signal or subject_instrument != cfg.subject
            or type(limit) is not int or not 1 <= limit <= 1000
        ):
            raise ValueError("bounded own-jurisdiction coefficient history required")
        rows = (
            row for row in cast(tuple[f.AlignedCoefficientOccurrenceV1, ...], self._state.all())
            if row.effective_as_of_utc <= effective_at_or_before_utc
            and row.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(sorted(rows, key=lambda row: (
            row.effective_as_of_utc, row.knowledge_cutoff_utc, row.derived_occurrence_id,
        ), reverse=True))[:limit]


class _Owner:
    def __init__(
        self, authority: Authority, readers: tuple[f.AlignedHistoryReadsV1, ...],
        state: RecordState, utc_now: Callable[[], datetime],
    ) -> None:
        self._authority, self._readers = authority, readers
        self._state, self._utc_now = state, utc_now
        self.reads = _Reads(authority, state)

    def materialise(self, request: f.AlignedFitRequestV1) -> f.AlignedCoefficientOccurrenceV1 | None:
        if type(request) is not f.AlignedFitRequestV1:
            raise TypeError("exact coefficient fit request required")
        now = self._utc_now()
        f._utc(now)
        try:
            _request_frame(self._authority, request, now)
            _unique_sample(request)
            rows = _lookup_rows(self._readers, request.rows)
            value = _produce(self._authority, request, rows, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.AlignedCoefficientOccurrenceV1, self._state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, predecessor_read_storages: tuple[f.SQLiteReadStorageV1, ...],
    storage: f.SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> f.AlignedCoefficientOwnerV1:
    authority = Authority(admission)
    if (
        type(predecessor_read_storages) is not tuple or len(predecessor_read_storages) != 4
        or any(type(s) is not f.SQLiteReadStorageV1 for s in predecessor_read_storages)
        or len({s.database_path for s in predecessor_read_storages}) != 4
        or type(storage) is not f.SQLiteStorageV1 or storage.create is not True or not callable(utc_now)
        or storage.database_path in {s.database_path for s in predecessor_read_storages}
    ):
        raise ValueError("ordered concrete parent readers and fresh own SQLite storage required")
    readers = tuple(
        f.create_aligned_history_reader(admission=_parent_admission(signal), storage=parent_storage)
        for signal, parent_storage in zip(ROLES, predecessor_read_storages, strict=True)
    )
    return _Owner(authority, readers, _store(authority, storage), utc_now)


def build_reader(admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1) -> f.AlignedCoefficientReadsV1:
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("exact read-only coefficient SQLite storage required")
    authority = Authority(admission)
    return _Reads(authority, _store(authority, storage))
