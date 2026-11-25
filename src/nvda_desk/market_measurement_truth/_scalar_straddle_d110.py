"""Fixed scalar D110 percentage from actual D109 and exactly aligned C1 R118."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from typing import Any, cast

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import _scalar_straddle_codec as codec
from . import _scalar_straddle_d109 as d109
from . import _scalar_straddle_source as scalar
from . import api as f
from ._record_store import RecordState

NAMESPACE = "neutral_market_measurement_truth/d110/scalar/v1"
DEFINITION = f.CalculationDefinitionV1(
    "D110", "T01-D110-SCALAR-PAIR-DEF-V1", "K02_ALGEBRA",
    "100 * D109 / R118", ("R118",), ("D109",), "P_BASIC",
    "percent", "exact_ratio",
    (
        f.AuthorityArtifactRefV1(scalar.POLICY_PATH, scalar.POLICY_SHA),
        f.AuthorityArtifactRefV1(scalar.BRIEF_PATH, scalar.BRIEF),
    ),
)


def _request_check(request: f.D110ScalarRequestV1) -> scalar._Specimen:
    if type(request) is not f.D110ScalarRequestV1:
        raise TypeError("exact D110 scalar request required")
    f._Validated.__post_init__(request)
    if (
        request.derived_signal_id != "D110"
        or request.subject_instrument != scalar.SUBJECT
        or request.as_of_utc != scalar.T
        or request.knowledge_cutoff_utc != scalar.CUTOFF
        or request.calculation_definition_version != DEFINITION.calculation_definition_version
    ):
        raise ValueError("unadmitted D110 scalar request identity")
    # Resolve both pins to an actual owner-admitted ordered literal roster.
    # Do not filter by spot eligibility here: all spot-only negative cases
    # must be able to reach the consumer's actual R118 selection.
    matches = tuple(
        row for row in scalar._load_specimens()
        if row.full_sha == request.full_specimen_sha256
        and row.core_sha == request.core_manifest_sha256
    )
    if len(matches) != 1:
        raise ValueError("D110 exact full/core specimen identity mismatch")
    scalar.core_literal(request.core_manifest_sha256, scalar.C1, "R034")
    return matches[0]


def _parent_check(
    request: f.D110ScalarRequestV1, straddle: f.D109ScalarOccurrenceV1,
) -> None:
    # Shared live/durable validation includes the complete nested D109
    # semantics and identity, not merely an equal numerical premium.
    d109._validate(straddle)
    if (
        straddle.derived_occurrence_id != request.straddle
        or straddle.core_manifest_sha256 != request.core_manifest_sha256
        or straddle.request.subject_instrument != request.subject_instrument
        or straddle.effective_as_of_utc != request.as_of_utc
        or straddle.knowledge_cutoff_utc != request.knowledge_cutoff_utc
        or straddle.units != "USD_per_share"
        or straddle.result_shape != "exact_ratio"
    ):
        raise ValueError("D110 actual parent identity/core/frame/units mismatch")
    # The D109 validator binds all six actual originals/projections to the
    # exact ordered core. The sealed source and request share that same core
    # with the full specimen resolved above. No raw reconstruction of D109.


def _spot_literal(row: scalar._Specimen) -> dict[str, Any]:
    spots = tuple(
        member["observation"] for member in row.members
        if member["observation"]["raw_signal_catalogue_ids"] == ["R118"]
    )
    if len(spots) != 1 or spots[0]["subject_instrument"] != scalar.C1:
        raise ValueError("exactly one admitted C1 R118 original required")
    return spots[0]


def _validate_spot(
    row: scalar._Specimen, original: raw.RawObservationOccurrenceV1,
    projection: raw.ProjectedRawValueV1,
) -> Decimal:
    # Same actual original/complete projection predicate for live and durable
    # paths. The manifest supplies expected facts, not a substitute raw read.
    scalar._exact_original(original, _spot_literal(row))
    if original.native_units != "USD_per_share":
        raise ValueError("D110 incompatible original spot native units")
    if (
        original.source_timestamp_raw != scalar.STAMP
        or original.received_ts_utc != scalar.T
        or original.source_temporal_kind != "true_instant"
        or original.source_timezone_native != "UTC"
    ):
        raise ValueError("D110 exact original spot clock mismatch")
    if (
        scalar._core_slot(original) != (scalar.C1, "R118")
        or original.source_provider.value != scalar.PROVIDER
        or original.source_variant != scalar.VARIANT
        or original.ingestion_sequence_scope.value != scalar.SCOPE
    ):
        raise ValueError("D110 exact original spot source identity mismatch")
    expected_identity = (
        scalar.C1, "NVDA", "2026-10-23", "110", "C", "USD", "100",
        "option", "controlled-model/1", "model_underlying_price",
    )
    for (_, path), expected in zip(scalar.META, expected_identity, strict=True):
        actual = scalar._literal_value(original.native_record, path)
        if type(actual) is not str or actual != expected:
            raise ValueError("D110 exact original spot role/contract/model mismatch")
    mapping = scalar.mapping_for("R118")
    scalar._check_projection(projection, original, mapping)
    value = scalar._literal_value(original.native_record, mapping.native_field_path)
    if type(value) is not Decimal or not value.is_finite():
        raise ValueError("D110 finite exact native Decimal spot required")
    if value <= 0:
        raise ValueError("D110 strictly positive spot required")
    return value


def _select_spot(
    source: f.ScalarStraddleSourceV1, row: scalar._Specimen,
) -> tuple[raw.RawObservationOccurrenceV1, raw.ProjectedRawValueV1, Decimal]:
    # Exhaust the actual public histories before deciding cardinality. The
    # existing bounded history helper validates every page, cursor and identity.
    c1 = scalar._history(source, scalar.C1, "R118")
    c2 = scalar._history(source, scalar.C2, "R118")
    if len(c1) != 1 or c2:
        raise ValueError("D110 exactly one actual C1 spot and no second spot required")
    projection = c1[0]
    original = source.get_raw_observation_occurrence(projection.observation_occurrence_id)
    if type(original) is not raw.RawObservationOccurrenceV1:
        raise ValueError("D110 selected actual spot original absent")
    return original, projection, _validate_spot(row, original, projection)


def _ratio(straddle: f.D109ScalarOccurrenceV1, spot: Decimal) -> f.ExactRatioV1:
    premium = straddle.result
    if type(premium) is not f.ExactRatioV1:
        raise TypeError("D110 exact D109 ratio required")
    result = 100 * Fraction(premium.numerator, premium.denominator) / Fraction(spot)
    return f.ExactRatioV1(result.numerator, result.denominator)


def _validate(value: f.D110ScalarOccurrenceV1) -> None:
    if type(value) is not f.D110ScalarOccurrenceV1:
        raise TypeError("exact D110 scalar occurrence required")
    f._Validated.__post_init__(value)
    row = _request_check(value.request)
    _parent_check(value.request, value.straddle)
    # The exact full ordered manifest is the verified six-member parent core
    # plus the actual uniquely matched R118 original. No live source required.
    spot = _validate_spot(row, value.original_observation, value.selected_projection)
    expected = _ratio(value.straddle, spot)
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != scalar.BRIEF
        or value.derived_signal_id != "D110"
        or value.definition != DEFINITION
        or value.source_policy_sha256 != scalar.POLICY_SHA
        or value.core_manifest_sha256 != value.request.core_manifest_sha256
        or value.full_specimen_sha256 != value.request.full_specimen_sha256
        or value.effective_as_of_utc != scalar.T
        or value.knowledge_cutoff_utc != scalar.CUTOFF
        or value.calculated_at_utc < value.knowledge_cutoff_utc
        or value.units != "percent" or value.result_shape != "exact_ratio"
        or value.result != expected
        or value.derived_occurrence_id != codec.identity_d110(value)
    ):
        raise ValueError("D110 scalar record/lineage/identity mismatch")


def _store(storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(storage, codec.decode_d110, _validate, encode=codec.encode_d110)


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self._state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.D110ScalarOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty D110 scalar occurrence identity required")
        return next(
            (value for value in self._state.all()
             if value.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.D110ScalarOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            derived_signal_id != "D110" or subject_instrument != scalar.SUBJECT
            or type(limit) is not int or not 1 <= limit <= 64
        ):
            raise ValueError("bounded D110 scalar read-only history required")
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
        self, source: f.ScalarStraddleSourceV1, straddle_reader: f.D109ScalarReadsV1,
        state: RecordState, utc_now: Callable[[], datetime],
    ) -> None:
        self._source, self._straddle_reader = source, straddle_reader
        self._state, self._utc_now = state, utc_now
        self.reads = _Reads(state)

    def materialise(self, request: f.D110ScalarRequestV1) -> f.D110ScalarOccurrenceV1 | None:
        if type(request) is not f.D110ScalarRequestV1:
            raise TypeError("exact D110 scalar request required")
        now = self._utc_now()
        f._utc(now)
        try:
            row = _request_check(request)
            if (
                request.core_manifest_sha256 != self._source.core_manifest_sha256
                or request.full_specimen_sha256 != self._source.full_specimen_sha256
                or row.name != self._source.specimen_id
                or now < request.knowledge_cutoff_utc
            ):
                raise ValueError("D110 scalar sealed source or calculation clock mismatch")
        except (TypeError, ValueError, ArithmeticError):
            return None

        # Actual ordinary parent lookup before R118 reads. No nearest/fallback
        # and no conversion of technical/storage failures into business None.
        straddle = self._straddle_reader.get_derived_occurrence(request.straddle)
        if type(straddle) is not f.D109ScalarOccurrenceV1:
            return None
        try:
            _parent_check(request, straddle)
            original, projection, spot = _select_spot(self._source, row)
            result = _ratio(straddle, spot)
            value = f.D110ScalarOccurrenceV1(
                "M02", NAMESPACE, scalar.BRIEF, "D110", "pending", request, DEFINITION,
                scalar.POLICY_SHA, request.core_manifest_sha256, request.full_specimen_sha256,
                straddle, original, projection, result, "percent", "exact_ratio",
                request.as_of_utc, request.knowledge_cutoff_utc, now,
            )
            value = replace(value, derived_occurrence_id=codec.identity_d110(value))
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.D110ScalarOccurrenceV1, self._state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, source: f.ScalarStraddleSourceV1,
    straddle_read_storage: f.SQLiteReadStorageV1,
    storage: f.SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> f.D110ScalarOwnerV1:
    scalar.check_admission(admission)
    if (
        type(source) is not f.ScalarStraddleSourceV1
        or type(straddle_read_storage) is not f.SQLiteReadStorageV1
        or type(storage) is not f.SQLiteStorageV1 or not callable(utc_now)
    ):
        raise ValueError("unadmitted D110 scalar source/storage/clock")
    row = scalar._specimen(source.specimen_id)
    if row.full_sha != source.full_specimen_sha256 or row.core_sha != source.core_manifest_sha256:
        raise ValueError("D110 scalar sealed source pins mismatch")
    scalar.core_literal(row.core_sha, scalar.C1, "R034")
    reader = f.create_d109_scalar_reader(admission=admission, storage=straddle_read_storage)
    return _Owner(source, reader, _store(storage), utc_now)


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1,
) -> f.D110ScalarReadsV1:
    scalar.check_admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D110 scalar read-only storage")
    return _Reads(_store(storage))
