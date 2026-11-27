"""Exact scalar D091 support, isolated from the original receipt-only profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime
from decimal import MAX_EMAX, MIN_EMIN, ROUND_HALF_EVEN, Context, Decimal, localcontext
from typing import cast

from . import _native_codec as native
from . import _native_d091
from . import _scalar_straddle_codec as codec
from . import _scalar_straddle_source as scalar
from . import api as f
from ._record_store import RecordState

NAMESPACE = "neutral_market_measurement_truth/d091/scalar/v1"
SOURCE = f.VersionRefV1("T01-L10C-R112-SCALAR-PAIR-V1", 1)
RULE = f.VersionRefV1("D091-SYNTHETIC-TENTATIVE-V1", 1)
MAPPING = f.VersionRefV1("mmt-r112-option", 1)
UNIT = f.VersionRefV1("mmt-option-delta", 1)
DEFINITION = f.CalculationDefinitionV1(
    "D091", "T01-D091-SCALAR-PAIR-DEF-V1", "K08_RULE_BUCKET_POLICY",
    "categorise(abs(exact signed R112 delta)) under D091-SYNTHETIC-TENTATIVE-V1",
    ("R112",), (), "P_RULE", "category", "category",
    (
        f.AuthorityArtifactRefV1(scalar.POLICY_PATH, scalar.POLICY_SHA),
        f.AuthorityArtifactRefV1(scalar.BRIEF_PATH, scalar.BRIEF),
    ),
)


def _category(value: Decimal) -> f.D091CategoryV1:
    if type(value) is not Decimal or not value.is_finite() or value.copy_abs() > 1:
        raise ValueError("exact finite scalar signed fraction required")
    # The old categoriser calls abs(delta), which is context-sensitive.
    # Reuse its exact accepted law under an explicit sufficient local context;
    # never round away a near-boundary digit or the signed stored original.
    context = Context(
        prec=max(28, len(value.as_tuple().digits)), rounding=ROUND_HALF_EVEN,
        Emin=MIN_EMIN, Emax=MAX_EMAX, clamp=0, flags=[], traps=[],
    )
    with localcontext(context):
        return _native_d091._category(value)


def _request_check(request: f.ScalarD091RequestV1) -> None:
    if type(request) is not f.ScalarD091RequestV1:
        raise TypeError("exact scalar D091 request required")
    if (
        request.derived_signal_id != "D091"
        or request.subject_instrument not in (scalar.C1, scalar.C2)
        or request.as_of_utc != scalar.T
        or request.knowledge_cutoff_utc != scalar.CUTOFF
        or request.calculation_definition_version != DEFINITION.calculation_definition_version
        or request.source_profile_ref != SOURCE
        or request.rule_profile_ref != RULE
        or request.projection_mapping_ref != MAPPING
        or request.unit_convention_ref != UNIT
    ):
        raise ValueError("unadmitted scalar D091 request identity")
    # Resolve to an exact lawfully admitted complete core, not just a hash
    # that has the right syntax. This also rejects all source-invalid cores.
    scalar.core_literal(request.core_manifest_sha256, request.subject_instrument, "R112")


def _validate(value: f.ScalarD091OccurrenceV1) -> None:
    if type(value) is not f.ScalarD091OccurrenceV1:
        raise TypeError("exact scalar D091 occurrence required")
    _request_check(value.request)
    signed = scalar.validate_core_role(
        value.request.core_manifest_sha256, value.request.subject_instrument, "R112",
        value.original_observation, value.selected_projection,
    )
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != scalar.BRIEF
        or value.derived_signal_id != "D091"
        or value.definition != DEFINITION
        or value.source_policy_sha256 != scalar.POLICY_SHA
        or value.core_manifest_sha256 != value.request.core_manifest_sha256
        or value.effective_as_of_utc != scalar.T
        or value.knowledge_cutoff_utc != scalar.CUTOFF
        or value.calculated_at_utc < value.knowledge_cutoff_utc
        or value.units != "category" or value.result_shape != "category"
        or native.canonical(value.signed_delta) != native.canonical(signed)
        or value.result != _category(signed)
        or value.derived_occurrence_id != codec.identity_d091(value)
    ):
        raise ValueError("scalar D091 record/lineage/identity mismatch")


def _store(storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(
        storage, codec.decode_d091, _validate, encode=codec.encode_d091,
    )


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self._state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.ScalarD091OccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty scalar D091 occurrence identity required")
        return next(
            (value for value in self._state.all()
             if value.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.ScalarD091OccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            derived_signal_id != "D091" or subject_instrument not in (scalar.C1, scalar.C2)
            or type(limit) is not int or not 1 <= limit <= 64
        ):
            raise ValueError("bounded scalar D091 read-only history required")
        rows = (
            value for value in self._state.all()
            if value.request.subject_instrument == subject_instrument
            and value.effective_as_of_utc <= effective_at_or_before_utc
            and value.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(sorted(rows, key=lambda value: (
            value.effective_as_of_utc, value.knowledge_cutoff_utc, value.derived_occurrence_id,
        )))[:limit]


class _Owner:
    def __init__(
        self, source: f.ScalarStraddleSourceV1, state: RecordState,
        utc_now: Callable[[], datetime],
    ) -> None:
        self._source, self._state, self._utc_now = source, state, utc_now
        self.reads = _Reads(state)

    def materialise(self, request: f.ScalarD091RequestV1) -> f.ScalarD091OccurrenceV1 | None:
        if type(request) is not f.ScalarD091RequestV1:
            raise TypeError("exact scalar D091 request required")
        now = self._utc_now()
        f._utc(now)
        try:
            _request_check(request)
            if (
                request.core_manifest_sha256 != self._source.core_manifest_sha256
                or now < request.knowledge_cutoff_utc
            ):
                raise ValueError("scalar D091 source core or calculation clock mismatch")
            original, projection = scalar.source_role(
                self._source, request.subject_instrument, "R112",
            )
            signed = scalar.validate_core_role(
                request.core_manifest_sha256, request.subject_instrument, "R112",
                original, projection,
            )
            value = f.ScalarD091OccurrenceV1(
                "M02", NAMESPACE, scalar.BRIEF, "D091", "pending", request, DEFINITION,
                scalar.POLICY_SHA, request.core_manifest_sha256, original, projection,
                signed, _category(signed), "category", "category",
                request.as_of_utc, request.knowledge_cutoff_utc, now,
            )
            value = replace(value, derived_occurrence_id=codec.identity_d091(value))
        except (TypeError, ValueError, ArithmeticError):
            return None
        # Persistence failures (including corrupt readback) are not business
        # refusals. RecordState validates actual bytes and retains first time.
        return cast(f.ScalarD091OccurrenceV1, self._state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, source: f.ScalarStraddleSourceV1,
    storage: f.SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> f.ScalarD091OwnerV1:
    scalar.check_admission(admission)
    if (
        type(source) is not f.ScalarStraddleSourceV1
        or type(storage) is not f.SQLiteStorageV1 or not callable(utc_now)
    ):
        raise ValueError("unadmitted scalar D091 sealed source/storage/clock")
    scalar.core_literal(source.core_manifest_sha256, scalar.C1, "R112")
    return _Owner(source, _store(storage), utc_now)


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1,
) -> f.ScalarD091ReadsV1:
    scalar.check_admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted scalar D091 read-only storage")
    return _Reads(_store(storage))
