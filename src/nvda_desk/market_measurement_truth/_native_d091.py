"""D091 exact controlled R112 absolute-Decimal category, SQLite immutable record.

Only the checked and genuinely sealed in-memory M00 cohort can produce a
success. Negative B cohorts are refusal-only. C/D fault adapters are read-only
selector ports, never replacements for the trusted original getter at B.
Product tests are authored but not executed by the Worker.
"""
from __future__ import annotations

import copy
import hashlib
from collections.abc import Mapping
from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as raw
from . import api as f
from . import _native_codec as codec
from . import _controlled_r112 as controlled
from ._record_store import RecordState

BRIEF = "a79dff57f7ceedfc8ffa47a9b312ad1d22d164c57d6fc43d2d38d2db8c51caf5"
SOURCE_CONTRACT_SHA = "31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63"
SOURCE_ARTIFACT_SHA = "1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"
NAMESPACE = "neutral_market_measurement_truth/d091/v1"
SOURCE = f.VersionRefV1("T01-R112-CONTROLLED-FRACTION-1", 1)
RULE = f.VersionRefV1("D091-SYNTHETIC-TENTATIVE-V1", 1)
SELECTOR = f.VersionRefV1("T01-R112-EXACT-RECEIPT-1", 1)
MAPPING = f.VersionRefV1("t01-controlled-r112-delta", 1)
UNITS = f.VersionRefV1("T01-R112-FRACTION-IDENTITY", 1)
DEFINITION = f.CalculationDefinitionV1(
    derived_signal_id="D091",
    calculation_definition_version="T01-D091-ABS-DELTA-DEF-V1",
    kernel_id="K08_RULE_BUCKET_POLICY",
    equation="categorise(abs(exact signed R112 delta)) under D091-SYNTHETIC-TENTATIVE-V1",
    raw_dependencies=("R112",),
    derived_dependencies=(),
    parameter_profile="P_RULE",
    units="category",
    result_shape="category",
    authority_refs=(
        f.AuthorityArtifactRefV1(
            "handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json",
            SOURCE_CONTRACT_SHA,
        ),
        f.AuthorityArtifactRefV1(
            "handoff/m02_completion_28_execution/L04/D091_PREEDIT_IMPLEMENTATION_BINDING_20261117/IMPLEMENTATION_BRIEF.md",
            BRIEF,
        ),
    ),
)
_IDENTITY = (
    ("contract_id", "SYNTH-NVDA-OPT-C100-20261120"),
    ("underlying", "NVDA"),
    ("security_type", "OPT"),
    ("right", "C"),
    ("expiry_date", "2026-11-20"),
    ("strike", "100"),
    ("currency", "USD"),
    ("model_variant", "CONTROLLED_SIGNED_DELTA_V1"),
    ("scale", "signed_decimal_fraction"),
    ("generation", "T01-R112-CONTROL-G1"),
    ("request_id", "T01-R112-BOUNDARIES-1"),
)


def _mapping() -> raw.RawSignalProjectionMappingV1:
    return raw.RawSignalProjectionMappingV1(
        mapping_id=MAPPING.context_id,
        version=MAPPING.version,
        raw_signal_catalogue_id=raw.RawSignalCatalogueId("R112"),
        source_provider="t01-controlled-option-delta",
        source_variant="controlled-option-model-delta/fraction-v1",
        native_field_path=("model", "delta"),
        native_units="signed_decimal_fraction",
        selection_identity_field_paths=tuple(
            (key, ("identity", key)) for key, _ in _IDENTITY
        ),
    )


def _category(delta: Decimal) -> f.D091CategoryV1:
    if type(delta) is not Decimal or not delta.is_finite():
        raise ValueError("nonfinite native signed Decimal")
    magnitude = abs(delta)
    if magnitude > 1:
        raise ValueError("absolute signed fraction outside domain")
    for lower, upper, label in (
        (Decimal(0), Decimal("0.10"), "ABS_00_10"),
        (Decimal("0.10"), Decimal("0.25"), "ABS_10_25"),
        (Decimal("0.25"), Decimal("0.50"), "ABS_25_50"),
        (Decimal("0.50"), Decimal("0.75"), "ABS_50_75"),
        (Decimal("0.75"), Decimal(1), "ABS_75_100"),
    ):
        if lower <= magnitude and (magnitude < upper or (upper == 1 and magnitude == 1)):
            return f.D091CategoryV1(label)
    raise ValueError("uncovered exact D091 delta bucket")


def _request_check(request: f.D091BucketRequestV1) -> None:
    if (
        type(request) is not f.D091BucketRequestV1
        or request.derived_signal_id != "D091"
        or request.subject_instrument != _IDENTITY[0][1]
        or request.source_profile_ref != SOURCE
        or request.selection_policy_ref != SELECTOR
        or request.projection_mapping_ref != MAPPING
        or request.unit_convention_ref != UNITS
        or request.rule_profile_ref != RULE
        or request.calculation_definition_version != DEFINITION.calculation_definition_version
        or any(getattr(request, field) != expected for field, expected in _IDENTITY)
    ):
        raise ValueError("D091 source/definition identity is not admitted")


def _original_value(observation: raw.RawObservationOccurrenceV1) -> object:
    record = observation.native_record
    model = record.get("model") if isinstance(record, Mapping) else None
    return model.get("delta") if isinstance(model, Mapping) else None


def _real_identity(
    original: raw.RawObservationOccurrenceV1,
    projected: raw.ProjectedRawValueV1 | None = None,
) -> bool:
    if (
        type(original) is not raw.RawObservationOccurrenceV1
        or original.source_provider.value != "t01-controlled-option-delta"
        or original.source_variant != "controlled-option-model-delta/fraction-v1"
        or original.subject_instrument != _IDENTITY[0][1]
        or original.native_units != "signed_decimal_fraction"
        or original.source_temporal_kind != "receipt_only"
        or original.source_timestamp_raw is not None
        or original.source_timezone_native is not None
        or original.ingestion_sequence_scope.value != "T01-R112-CONTROL/G1"
        or original.raw_signal_catalogue_ids != (raw.RawSignalCatalogueId("R112"),)
    ):
        return False
    ident = original.native_record.get("identity")
    if not isinstance(ident, Mapping) or any(
        ident.get(key) != val for key, val in _IDENTITY
    ):
        return False
    if projected is None:
        return True
    return (
        type(projected) is raw.ProjectedRawValueV1
        and projected.observation_occurrence_id == original.observation_occurrence_id
        and projected.raw_signal_catalogue_id == raw.RawSignalCatalogueId("R112")
        and projected.projection_mapping_id == MAPPING.context_id
        and projected.projection_mapping_version == MAPPING.version
        and projected.native_field_path == ("model", "delta")
        and projected.native_units == original.native_units
        and projected.subject_instrument == original.subject_instrument
        and projected.source_provider == original.source_provider.value
        and projected.source_variant == original.source_variant
        and projected.source_temporal_kind == "receipt_only"
        and projected.source_timestamp_raw is None
        and projected.source_timezone_native is None
        and projected.received_ts_utc == original.received_ts_utc
        and projected.ingestion_sequence == original.ingestion_sequence
        and projected.ingestion_sequence_scope == original.ingestion_sequence_scope
        and type(projected.native_value) is Decimal
        and _original_value(original) == projected.native_value
        and projected.selection_identity is not None
        and all(projected.selection_identity.value_for(k) == val for k, val in _IDENTITY)
    )


def _id_input(request: f.D091BucketRequestV1, original, projection,
              result: f.D091CategoryV1, cohort_hash: str) -> dict:
    return {
        "owner_namespace": NAMESPACE,
        "implementation_brief_sha256": BRIEF,
        "request_identity": request.request_identity,
        "calculation_definition_version": DEFINITION.calculation_definition_version,
        "source_contract_sha256": SOURCE_CONTRACT_SHA,
        "source_artifact_sha256": SOURCE_ARTIFACT_SHA,
        "cohort_content_digest": cohort_hash,
        "selected_original_observation_id": original.observation_occurrence_id.value,
        "selected_receipt_ts_utc": original.received_ts_utc,
        "selected_ingestion_sequence": original.ingestion_sequence,
        "rule_profile_ref": RULE,
        "result_label": result.label,
    }


def _logical_id(request, original, projection, result, digest) -> str:
    return "d091-occurrence-v1:" + hashlib.sha256(
        codec.canonical(_id_input(request, original, projection, result, digest))
    ).hexdigest()


def _validate(value: f.D091BucketOccurrenceV1) -> None:
    if type(value) is not f.D091BucketOccurrenceV1:
        raise ValueError("typed D091 record required")
    _request_check(value.request)
    if (
        value.owner_object_id != "M02" or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or value.definition != DEFINITION
        or value.source_contract_sha256 != SOURCE_CONTRACT_SHA
        or value.source_artifact_sha256 != SOURCE_ARTIFACT_SHA
        or value.effective_as_of_utc != value.request.as_of_utc
        or value.knowledge_cutoff_utc != value.request.knowledge_cutoff_utc
        or value.calculated_at_utc < value.knowledge_cutoff_utc
        or value.original_observation.received_ts_utc != value.effective_as_of_utc
        or not _real_identity(value.original_observation, value.selected_projection)
        or value.signed_delta != _original_value(value.original_observation)
        or value.result != _category(value.signed_delta)
        or value.derived_occurrence_id != _logical_id(
            value.request, value.original_observation, value.selected_projection,
            value.result, value.cohort_content_digest,
        )
    ):
        raise ValueError("D091 categorical record/lineage/identity mismatch")


def _store(storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(
        storage,
        lambda payload: codec.decode(payload, f.D091BucketOccurrenceV1),
        _validate,
        encode=codec.canonical,
    )


class _Reads:
    def __init__(self, state: RecordState):
        self._state = state

    def get_derived_occurrence(self, derived_occurrence_id: str):
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty D091 occurrence identity required")
        return next((item for item in self._state.all()
                     if item.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.D091BucketOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (derived_signal_id != "D091" or subject_instrument != _IDENTITY[0][1]
                or type(limit) is not int or limit <= 0 or limit > 64):
            raise ValueError("bounded D091 read-only history request required")
        rows = (
            item for item in self._state.all()
            if item.request.subject_instrument == subject_instrument
            and item.effective_as_of_utc <= effective_at_or_before_utc
            and item.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(sorted(
            rows,
            key=lambda item: (
                item.effective_as_of_utc,
                item.knowledge_cutoff_utc,
                item.derived_occurrence_id,
            ), reverse=True,
        ))[:limit]


class _Owner:
    def __init__(self, source: controlled._ReadOnly, state: RecordState, utc_now,
                 observer=None, *, test_fault: str | None = None):
        self._source = source
        self._state = state
        self._utc_now = utc_now
        self._observer = observer
        self._test_fault = test_fault
        self._materialise_count = 0
        self.reads = _Reads(state)

    def _refuse(self, request, stage: str, source_id: str | None = None):
        if self._observer is not None:
            self._observer(f.D091DiagnosticEventV1(
                request.request_identity, source_id,
                cast(f.D091RefusalStageV1, stage),
                SOURCE, RULE,
            ))
        return None

    def materialise(self, request: f.D091BucketRequestV1):
        _request_check(request)
        now = self._utc_now()
        f._utc(now)
        self._materialise_count += 1
        with self._source.locked():
            source_id = self._source.source_id_for_receipt(request.as_of_utc)
            # A: clock and genuine one-way seal precede any history paging.
            if request.as_of_utc > request.knowledge_cutoff_utc or now < request.knowledge_cutoff_utc:
                return self._refuse(request, "CLOCK_OR_SCOPE", source_id)
            if not self._source.sealed:
                return self._refuse(request, "UNSEALED", source_id)
            # B: full actual private M00 original getter and immutable roster.
            try:
                originals = self._source.trusted_originals()
                if not all(_real_identity(original) for original in originals):
                    raise ValueError("invalid actual M00 source identity")
            except (TypeError, ValueError):
                return self._refuse(request, "ORIGIN_OR_IDENTITY", source_id)
            by_id = {x.observation_occurrence_id: x for x in originals}
            # C: public projection pagination by actually returned cursor.
            cursor = None
            seen_cursors: set[str] = set()
            seen_ids: dict[object, raw.ProjectedRawValueV1] = {}
            history: list[raw.ProjectedRawValueV1] = []
            while True:
                try:
                    page = self._source.list_projected_raw_history(
                        raw.RawSignalCatalogueId("R112"),
                        mappings=(_mapping(),),
                        subject_instrument=request.subject_instrument,
                        received_at_or_before_utc=request.knowledge_cutoff_utc,
                        event_at_or_before_utc=None,
                        limit=8,
                        cursor=cursor,
                    )
                except (ValueError, TypeError, KeyError):
                    return self._refuse(request, "HISTORY_OR_AMBIGUOUS_RANK", source_id)
                if (type(page) is not raw.ProjectedRawHistoryPageV1
                        or type(page.items) is not tuple or not 1 <= len(page.items) <= 8):
                    return self._refuse(request, "HISTORY_OR_AMBIGUOUS_RANK", source_id)
                for item in page.items:
                    if type(item) is not raw.ProjectedRawValueV1:
                        return self._refuse(request, "HISTORY_OR_AMBIGUOUS_RANK", source_id)
                    previous = seen_ids.get(item.observation_occurrence_id)
                    if previous is not None and previous != item:
                        return self._refuse(request, "HISTORY_OR_AMBIGUOUS_RANK", source_id)
                    if previous is not None:
                        return self._refuse(request, "HISTORY_OR_AMBIGUOUS_RANK", source_id)
                    seen_ids[item.observation_occurrence_id] = item
                    history.append(item)
                    if len(history) > 64:
                        return self._refuse(request, "HISTORY_OR_AMBIGUOUS_RANK", source_id)
                new_cursor = page.next_cursor
                if new_cursor is None:
                    break
                if type(new_cursor) is not str or new_cursor == cursor or new_cursor in seen_cursors:
                    return self._refuse(request, "HISTORY_OR_AMBIGUOUS_RANK", source_id)
                seen_cursors.add(new_cursor)
                cursor = new_cursor
            if not history:
                return self._refuse(request, "ABSENT", source_id)
            highest_rank = max((x.received_ts_utc, x.ingestion_sequence) for x in history)
            if sum((x.received_ts_utc, x.ingestion_sequence) == highest_rank for x in history) > 1:
                return self._refuse(request, "HISTORY_OR_AMBIGUOUS_RANK", source_id)
            # D: selector-only read-port original getter comparison after real B/C.
            for projection in history:
                try:
                    original = self._source.get_raw_observation_occurrence(
                        projection.observation_occurrence_id
                    )
                except (ValueError, TypeError, KeyError):
                    return self._refuse(request, "ORIGIN_OR_IDENTITY", source_id)
                if (original is None
                    or original != by_id.get(projection.observation_occurrence_id)
                    or not _real_identity(original, projection)):
                    return self._refuse(request, "ORIGIN_OR_IDENTITY", source_id)
            # E: original receipt target (including t14 absent projection).
            target = next((x for x in originals
                           if x.received_ts_utc == request.as_of_utc), None)
            if target is None:
                return self._refuse(
                    request,
                    "CLOCK_OR_SCOPE" if any(x.received_ts_utc < request.as_of_utc
                                            for x in originals) else "ABSENT",
                    source_id,
                )
            target_id = target.observation_occurrence_id.value
            signed = _original_value(target)
            if signed is None:
                return self._refuse(request, "ABSENT", target_id)
            projection = next((x for x in history
                               if x.observation_occurrence_id == target.observation_occurrence_id), None)
            if projection is None:
                return self._refuse(request, "ABSENT", target_id)
            # F: only selected target's numeric domain is validated.
            if type(signed) is not Decimal or not signed.is_finite():
                return self._refuse(request, "NONFINITE", target_id)
            if abs(signed) > 1:
                return self._refuse(request, "RANGE", target_id)
            category = _category(signed)
            if self._source.cohort_kind != "SUCCESS_15":
                return self._refuse(request, "HISTORY_OR_AMBIGUOUS_RANK", target_id)
            # G: only lawful category flows into the real immutable SQLite store.
            digest = self._source.cohort_digest
            value = f.D091BucketOccurrenceV1(
                owner_object_id="M02", owner_namespace=NAMESPACE,
                implementation_brief_sha256=BRIEF,
                derived_signal_id="D091", derived_occurrence_id="pending",
                request=request, definition=DEFINITION,
                source_contract_sha256=SOURCE_CONTRACT_SHA,
                source_artifact_sha256=SOURCE_ARTIFACT_SHA,
                cohort_content_digest=digest,
                original_observation=target, selected_projection=projection,
                signed_delta=signed, result=category,
                units="category", result_shape="category",
                effective_as_of_utc=request.as_of_utc,
                knowledge_cutoff_utc=request.knowledge_cutoff_utc,
                calculated_at_utc=now,
            )
            value = replace(value, derived_occurrence_id=_logical_id(
                request, target, projection, category, digest,
            ))
            if self._test_fault == "D03" and self._materialise_count == 2:
                if target_id != "T01-R112-BATCH-11" or signed != Decimal("0.499"):
                    raise ValueError("D03 only admitted on exact t11 original")
                alternate = Decimal("0.498")
                native = copy.deepcopy(dict(target.native_record))
                native["model"]["delta"] = alternate
                alternate_original = replace(target, native_record=native)
                value = replace(
                    value,
                    original_observation=alternate_original,
                    selected_projection=replace(projection, native_value=alternate),
                    signed_delta=alternate,
                )
            return self._state.append(value)


def build_owner(admission, source, storage, utc_now, observer=None):
    if (type(admission) is not f.OwnerAdmissionV1
            or admission.object_id != "M02"
            or admission.implementation_brief_sha256 != BRIEF
            or type(source) is not controlled._ReadOnly
            or type(storage) is not f.SQLiteStorageV1
            or not callable(utc_now)
            or (observer is not None and not callable(observer))):
        raise ValueError("unadmitted D091 owner/source/storage/clock")
    return _Owner(source, _store(storage), utc_now, observer)


def build_reader(admission, storage):
    if (type(admission) is not f.OwnerAdmissionV1
            or admission.object_id != "M02"
            or admission.implementation_brief_sha256 != BRIEF
            or type(storage) is not f.SQLiteReadStorageV1):
        raise ValueError("unadmitted D091 read-only SQLite storage")
    return _Reads(_store(storage))


def _build_test_only_owner_from_fixed_policy(
    *, admission, controlled_source_read_capability, storage, utc_now,
    test_fault_id: str,
):
    if test_fault_id not in ("D01", "D02", "D03"):
        raise ValueError("unadmitted persistence fault mode")
    if test_fault_id in ("D01", "D02"):
        # The real COMMIT-boundary test facility requires a separate owner
        # changed-path approval for _record_store.py. Do not fake a successful
        # or precommit failure through a mock store or invented error.
        raise NotImplementedError(
            "D01/D02 held: approved _record_store.py transaction hook not yet released"
        )
    owner = build_owner(
        admission, controlled_source_read_capability, storage, utc_now
    )
    owner._test_fault = "D03"
    return owner
