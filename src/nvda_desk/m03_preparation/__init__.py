"""Public M03 prepared-data authority API."""

from nvda_desk.contracts.prepared_data import (
    CalendarProjectionReference,
    DerivationReceipt,
    PreparedDataEnvelope,
    PreparedDerivationRule,
    PreparedRuntimePayloadV1,
    SourceCaptureReference,
)
from nvda_desk.m03_preparation.builder import PreparedDataBuilder
from nvda_desk.preparation.field_resolution import (
    FieldCandidate,
    FieldResolutionPolicy,
    FieldResolutionReceipt,
    MandatoryFieldConflictError,
    MissingMandatoryFieldError,
    resolve_canonical_field,
)

__all__ = [
    "CalendarProjectionReference",
    "DerivationReceipt",
    "FieldCandidate",
    "FieldResolutionPolicy",
    "FieldResolutionReceipt",
    "MandatoryFieldConflictError",
    "MissingMandatoryFieldError",
    "PreparedDataBuilder",
    "PreparedDataEnvelope",
    "PreparedDerivationRule",
    "PreparedRuntimePayloadV1",
    "SourceCaptureReference",
    "resolve_canonical_field",
]
