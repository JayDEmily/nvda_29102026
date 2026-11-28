"""Own D078 aligned same-fit residual from seven actual public parent occurrences."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, cast

from . import _aligned_history_codec as history_codec
from . import _aligned_history_returns as history
from . import _aligned_history_source as source
from . import _aligned_joint_fit as fit
from . import api as f
from ._record_store import RecordState
from ._sqlite import _path

BRIEF = "b1fc6fe2b84f53d59b47c72c01f6265bb9a7c668a4e7f89fd7b963b0b11aa792"
BINDING = "d09915e073f9faf1f7c8a3b6371025ab3aee95d0cf25577420c8b934b136f194"
COEFFICIENTS = ("D079", "D080", "D081")
ROLES = (*fit.ROLES, *COEFFICIENTS)
HistoryRow = tuple[f.AlignedHistoryOccurrenceV1, ...]
Coefficients = tuple[f.AlignedCoefficientOccurrenceV1, ...]


def _coefficient_admission(signal: str) -> f.OwnerAdmissionV1:
    return f.OwnerAdmissionV1("M02", fit.OWN[signal][1])


class Authority:
    """Own residual configuration and separately admitted actual parent contexts."""

    def __init__(self, admission: f.OwnerAdmissionV1) -> None:
        if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1(
            "M02", BRIEF,
        ):
            raise ValueError("exact own D078 admission required")
        policy = source._document(source.POLICY_PATH, source.POLICY_SHA)
        brief_path = source.LEAF + "ALIGNED_HISTORY_D078_IMPLEMENTATION_BRIEF.md"
        binding_path = "implementation/authority/T01_ALIGNED_HISTORY_D078_AUTHORITY_BINDING.yaml"
        source._pinned(brief_path, BRIEF)
        source._pinned(binding_path, BINDING)
        owner = source._document(source.OWNER_PATH, source.OWNER_SHA)
        source._pinned(source.INVENTORY_PATH, source.INVENTORY_SHA)
        package, = [p for p in owner["adopted_packages"] if p["package"] == "aligned_history"]
        if (
            owner["exact_total_cases"] != 64
            or package["policy"]["sha256"] != source.POLICY_SHA
            or package["specimens"]["sha256"] != source.MANIFEST_SHA
            or package["inventory"]["sha256"] != source.INVENTORY_SHA
            or package["exact_nonfungible_ceilings"]["D078"] != 5
        ):
            raise ValueError("unaligned residual grant")
        row = policy["profiles"]["D078"]
        if (
            row["subject"] != "NVDA" or tuple(row["members"]) != fit.MEMBERS
            or row["raw_dependencies"] != [] or tuple(row["derived_dependencies"]) != ROLES
            or row["kernel"] != "K06_REGRESSION_DEPENDENCE"
            or row["parameter_profile"] != "P_REGRESSION"
            or row["equation"] != "D075-(alpha+D079*D071+D080*D076+D081*D077)"
            or row["units"] != "return" or row["result_shape"] != "exact_ratio"
            or row["future_own_brief_path"] != brief_path or row["future_binding_path"] != binding_path
            or row["calculation_definition_version"] != "T01-D078-ALIGNED-JOINT-FIT-DEF-V1"
        ):
            raise ValueError("residual profile/authority mismatch")
        refs = tuple(f.AuthorityArtifactRefV1(r["path"], r["sha256"])
                     for r in policy["authority_refs"])
        profile, param, selection = (fit._ref(row[k]) for k in
                                     ("profile_ref", "parameter_ref", "selection_ref"))
        if (profile, param, selection) != (
            f.VersionRefV1("t01-l01a-d078-joint-fit", 1),
            f.VersionRefV1("t01-l01a-joint-fit-parameters", 1),
            f.VersionRefV1("t01-l01a-d078-selection", 1),
        ):
            raise ValueError("exact residual version references required")
        self.config = source.Configuration(
            "D078", "NVDA", BRIEF, profile,
            f.CalculationDefinitionV1(
                "D078", row["calculation_definition_version"], row["kernel"], row["equation"],
                (), ROLES, row["parameter_profile"], row["units"], row["result_shape"],
                (*refs, f.AuthorityArtifactRefV1(source.POLICY_PATH, source.POLICY_SHA),
                 f.AuthorityArtifactRefV1(brief_path, BRIEF)),
            ),
            f.CalculationParameterSetV1(
                param.context_id, param.version, row["parameter_profile"], "NVDA", fit.MEMBERS,
            ),
            f.InputSelectionPolicyVersionV1(
                selection.context_id, selection.version,
                ("subject_instrument", "instrument.id", "session.id", "adjustment.basis", "price.kind"),
                timedelta(seconds=86400), timedelta(0), ("true_instant",), fit.MEMBERS,
                source.PROVIDER, source.VARIANT, source.SCOPE, 100, 2,
            ),
        )
        self.coefficient_authorities = tuple(
            fit.Authority(_coefficient_admission(signal)) for signal in COEFFICIENTS
        )
        # The unchanged shared row/corpus routines take the actual parent fit
        # context. It is not the residual's admission or own configuration.
        self.row_authority = self.coefficient_authorities[0]
        self.frame = self.row_authority.frames["S7"]
        clock = policy["clocks"]["residual_current"]
        self.cutoffs = tuple(datetime.fromisoformat(t) for t in clock["allowed_residual_knowledge_cutoffs"])
        if (
            clock["slot"] != self.frame.slot
            or datetime.fromisoformat(clock["as_of"]) != self.frame.as_of
            or datetime.fromisoformat(clock["current_row_cutoff"]) != self.frame.cutoff
            or self.cutoffs != tuple(self.frame.as_of + timedelta(seconds=s) for s in (4, 7))
        ):
            raise ValueError("exact admitted residual clock required")


def _request_frame(authority: Authority, request: f.AlignedResidualRequestV1, now: datetime) -> source.Frame:
    if type(request) is not f.AlignedResidualRequestV1:
        raise TypeError("exact residual request required")
    f._Validated.__post_init__(request)
    f._utc(now)
    cfg, frame = authority.config, authority.frame
    expected = f.AlignedResidualRequestV1(
        cfg.signal, cfg.subject, frame.slot, frame.as_of, request.knowledge_cutoff_utc,
        cfg.definition.calculation_definition_version, cfg.profile,
        f.VersionRefV1(cfg.parameter.context_id, cfg.parameter.version),
        f.VersionRefV1(cfg.selection.context_id, cfg.selection.version),
        (frame.context.ref,), request.predecessor_occurrence_ids,
    )
    if (
        request != expected or request.knowledge_cutoff_utc not in authority.cutoffs
        or now < request.knowledge_cutoff_utc
    ):
        raise ValueError("unadmitted residual request, metadata or calculation clock")
    return frame


def _unique_parents(request: f.AlignedResidualRequestV1) -> None:
    ids = request.predecessor_occurrence_ids
    if len(ids) != 7 or len(set(ids)) != 7 or any(not identity for identity in ids):
        raise ValueError("seven distinct actual predecessor identities required")


def _checked_coefficients(
    authority: Authority, request: f.AlignedResidualRequestV1, coefficients: Coefficients,
) -> f.AlignedFitManifestV1:
    if len(coefficients) != 3:
        raise ValueError("exact three actual coefficient roles required")
    for signal, pa, identity, value in zip(
        COEFFICIENTS, authority.coefficient_authorities,
        request.predecessor_occurrence_ids[4:], coefficients, strict=True,
    ):
        if (
            type(value) is not f.AlignedCoefficientOccurrenceV1
            or value.derived_occurrence_id != identity or value.derived_signal_id != signal
            or value.component != pa.component
        ):
            raise ValueError("exact named coefficient role and identity required")
        f._Validated.__post_init__(value)
        # Identical local parent semantic reconstruction to the ordinary parent
        # store. The residual arithmetic below uses only actual retained values.
        expected = fit._produce(pa, value.request, value.fit.rows, value.calculated_at_utc)
        if fit._encode(value) != fit._encode(expected):
            raise ValueError("coefficient actual evidence or role mismatch")
    common = coefficients[0].fit
    common_bytes = fit._fit_bytes(common)
    if any(
        value.fit.fit_id != common.fit_id or fit._fit_bytes(value.fit) != common_bytes
        for value in coefficients[1:]
    ):
        raise ValueError("same actual fit identity and complete manifest required")
    if (
        common.origin_slot != "S6" or common.effective_as_of_utc >= request.as_of_utc
    ):
        raise ValueError("strictly prior actual fit origin required")
    for value in coefficients:
        fit._visible(value, request.knowledge_cutoff_utc)
    if common.knowledge_cutoff_utc > request.knowledge_cutoff_utc:
        raise ValueError("actual fit cutoff unavailable at residual decision")
    return common


def _content(value: f.AlignedResidualOccurrenceV1) -> dict[str, Any]:
    content = history_codec._record(value, f.AlignedResidualOccurrenceV1)
    content["request"] = history_codec._record(value.request, f.AlignedResidualRequestV1)
    content["current_histories"] = tuple(history_codec.encode(p) for p in value.current_histories)
    content["coefficients"] = tuple(fit._encode(p) for p in value.coefficients)
    for name, cls in fit._METADATA.items():
        content[name] = history_codec._record(getattr(value, name), cls)
    return content


def _encode(value: f.AlignedResidualOccurrenceV1) -> bytes:
    return fit._envelope(f.AlignedResidualOccurrenceV1, _content(value))


def _identity(value: f.AlignedResidualOccurrenceV1) -> str:
    content = _content(value)
    del content["derived_occurrence_id"]
    del content["calculated_at_utc"]
    return "mmtaresidual1:" + fit._digest(fit._envelope(f.AlignedResidualOccurrenceV1, content))


def _decode(payload: bytes) -> f.AlignedResidualOccurrenceV1:
    content = fit._unpack(payload, f.AlignedResidualOccurrenceV1)
    for name in ("current_histories", "coefficients"):
        values = content[name]
        if type(values) is not tuple or any(type(value) is not bytes for value in values):
            raise ValueError("exact nested actual residual envelopes required")
    content["request"] = history_codec._rebuild(content["request"], f.AlignedResidualRequestV1)
    content["current_histories"] = tuple(history_codec.decode(p) for p in content["current_histories"])
    content["coefficients"] = tuple(fit._decode(p) for p in content["coefficients"])
    for name, cls in fit._METADATA.items():
        content[name] = history_codec._rebuild(content[name], cls)
    value = f.AlignedResidualOccurrenceV1(**content)
    if _encode(value) != payload:
        raise ValueError("residual canonical round-trip mismatch")
    return value


def _produce(
    authority: Authority, request: f.AlignedResidualRequestV1,
    current: HistoryRow, coefficients: Coefficients, now: datetime,
) -> f.AlignedResidualOccurrenceV1:
    frame = _request_frame(authority, request, now)
    _unique_parents(request)
    common = _checked_coefficients(authority, request, coefficients)
    row_request = f.AlignedFitRowRequestV1(frame.slot, request.predecessor_occurrence_ids[:4])
    pa = authority.row_authority
    current_originals = fit._checked_rows(pa, (row_request,), (current,), request.knowledge_cutoff_utc)
    prior_originals = fit._checked_rows(
        pa, coefficients[0].request.rows, common.rows, common.knowledge_cutoff_utc,
    )
    fit._check_corpus(pa, (*common.row_slots, frame.slot), (*prior_originals, *current_originals))
    target, *predictors = (fit._ratio(p.result) for p in current)
    prediction = fit._ratio(common.intercept)
    for coefficient, predictor in zip(coefficients, predictors, strict=True):
        prediction = fit._bounded(prediction + fit._bounded(fit._ratio(coefficient.result) * predictor))
    result = fit._exact(fit._bounded(target - prediction))
    cfg = authority.config
    value = f.AlignedResidualOccurrenceV1(
        "M02", history.NAMESPACE, cfg.brief, cfg.signal, "pending", request, cfg.definition,
        source.POLICY_SHA, cfg.profile, cfg.parameter, cfg.selection, frame.context,
        current, coefficients, result, cfg.definition.units, cfg.definition.result_shape,
        request.as_of_utc, request.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def _store(
    authority: Authority, storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1,
) -> RecordState:
    def validate(value: f.AlignedResidualOccurrenceV1) -> None:
        if type(value) is not f.AlignedResidualOccurrenceV1:
            raise TypeError("exact residual occurrence required")
        f._Validated.__post_init__(value)
        expected = _produce(
            authority, value.request, value.current_histories, value.coefficients, value.calculated_at_utc,
        )
        if _encode(value) != _encode(expected):
            raise ValueError("residual actual evidence, metadata, result or identity mismatch")

    return RecordState(storage, _decode, validate, encode=_encode)


class _Reads:
    def __init__(self, authority: Authority, state: RecordState) -> None:
        self._authority, self._state = authority, state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.AlignedResidualOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty residual identity required")
        return next((row for row in cast(tuple[f.AlignedResidualOccurrenceV1, ...], self._state.all())
                     if row.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.AlignedResidualOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        cfg = self._authority.config
        if (
            derived_signal_id != cfg.signal or subject_instrument != cfg.subject
            or type(limit) is not int or not 1 <= limit <= 1000
        ):
            raise ValueError("bounded own-jurisdiction residual history required")
        rows = (
            row for row in cast(tuple[f.AlignedResidualOccurrenceV1, ...], self._state.all())
            if row.effective_as_of_utc <= effective_at_or_before_utc
            and row.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(sorted(rows, key=lambda row: (
            row.effective_as_of_utc, row.knowledge_cutoff_utc, row.derived_occurrence_id,
        ), reverse=True))[:limit]


class _Owner:
    def __init__(
        self, authority: Authority, history_readers: tuple[f.AlignedHistoryReadsV1, ...],
        coefficient_readers: tuple[f.AlignedCoefficientReadsV1, ...],
        state: RecordState, utc_now: Callable[[], datetime],
    ) -> None:
        self._authority, self._history_readers = authority, history_readers
        self._coefficient_readers = coefficient_readers
        self._state, self._utc_now = state, utc_now
        self.reads = _Reads(authority, state)

    def materialise(self, request: f.AlignedResidualRequestV1) -> f.AlignedResidualOccurrenceV1 | None:
        if type(request) is not f.AlignedResidualRequestV1:
            raise TypeError("exact residual request required")
        now = self._utc_now()
        f._utc(now)
        try:
            frame = _request_frame(self._authority, request, now)
            _unique_parents(request)
            current, = fit._lookup_rows(
                self._history_readers,
                (f.AlignedFitRowRequestV1(frame.slot, request.predecessor_occurrence_ids[:4]),),
            )
            coefficients = []
            for reader, identity in zip(
                self._coefficient_readers, request.predecessor_occurrence_ids[4:], strict=True,
            ):
                coefficient = reader.get_derived_occurrence(identity)
                if type(coefficient) is not f.AlignedCoefficientOccurrenceV1:
                    raise ValueError("actual ordered coefficient parent not found")
                coefficients.append(coefficient)
            value = _produce(self._authority, request, current, tuple(coefficients), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.AlignedResidualOccurrenceV1, self._state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, predecessor_read_storages: tuple[f.SQLiteReadStorageV1, ...],
    storage: f.SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> f.AlignedResidualOwnerV1:
    authority = Authority(admission)
    if (
        type(predecessor_read_storages) is not tuple or len(predecessor_read_storages) != 7
        or any(type(s) is not f.SQLiteReadStorageV1 for s in predecessor_read_storages)
        or type(storage) is not f.SQLiteStorageV1 or storage.create is not True or not callable(utc_now)
    ):
        raise ValueError("ordered distinct concrete parent readers and fresh own SQLite storage required")
    paths = tuple(_path(s.database_path) for s in predecessor_read_storages)
    target = _path(storage.database_path)
    if len(set(paths)) != 7 or target in paths:
        raise ValueError("distinct actual residual and predecessor stores required")
    try:
        stats = tuple(Path(path).stat() for path in paths)
    except OSError as exc:
        raise f.PersistenceFailureV1("residual predecessor storage unavailable") from exc
    if len({(info.st_dev, info.st_ino) for info in stats}) != 7:
        raise ValueError("distinct physical predecessor stores required")
    history_readers = tuple(
        f.create_aligned_history_reader(admission=fit._parent_admission(signal), storage=parent_storage)
        for signal, parent_storage in zip(fit.ROLES, predecessor_read_storages[:4], strict=True)
    )
    coefficient_readers = tuple(
        f.create_aligned_coefficient_reader(admission=_coefficient_admission(signal), storage=parent_storage)
        for signal, parent_storage in zip(COEFFICIENTS, predecessor_read_storages[4:], strict=True)
    )
    return _Owner(authority, history_readers, coefficient_readers, _store(authority, storage), utc_now)


def build_reader(admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1) -> f.AlignedResidualReadsV1:
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("exact read-only residual SQLite storage required")
    authority = Authority(admission)
    return _Reads(authority, _store(authority, storage))
