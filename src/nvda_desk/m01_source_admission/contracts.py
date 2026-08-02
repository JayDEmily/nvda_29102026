"""M01-owned contracts for bounded offline source admission and raw capture."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from datetime import date, datetime
from enum import StrEnum
from typing import Any, Literal, Protocol

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SerializeAsAny,
    field_validator,
    model_validator,
)


class SourceFactRequirement(StrEnum):
    """Applicability of one source-owned fact under a family contract."""

    REQUIRED = "required"
    OPTIONAL = "optional"
    UNAVAILABLE_BY_SOURCE_DESIGN = "unavailable_by_source_design"
    NOT_APPLICABLE = "not_applicable"


class SourceTimeKind(StrEnum):
    """Original temporal precision admitted by one source family."""

    INSTANT = "instant"
    DATE = "date"


class SourceDownstreamOwner(StrEnum):
    """Lawful next owner for admitted source material."""

    M02 = "M02"
    M03 = "M03"


class SourceOutputContract(StrEnum):
    """M01 output shape selected by the registered family contract."""

    SOURCE_ARTIFACT = "source_artifact"
    RAW_SIGNAL_BATCH = "raw_signal_batch"


class SourceIdentifierContract(BaseModel):
    """Owner and namespace law for one source-issued identifier role."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    requirement: SourceFactRequirement
    owner: str | None = None
    namespace: str | None = None
    uniqueness_scope: str | None = None
    stability_rule: str | None = None
    generation_rule: str | None = None

    @model_validator(mode="after")
    def _validate_identifier_law(self) -> "SourceIdentifierContract":
        semantic_fields = (
            self.owner,
            self.namespace,
            self.uniqueness_scope,
            self.stability_rule,
            self.generation_rule,
        )
        carries_identifier = self.requirement in {
            SourceFactRequirement.REQUIRED,
            SourceFactRequirement.OPTIONAL,
        }
        if carries_identifier and any(not value for value in semantic_fields):
            raise ValueError("source_identifier_contract_requires_owner_scope_and_generation_law")
        if not carries_identifier and any(value is not None for value in semantic_fields):
            raise ValueError("source_identifier_contract_must_not_imply_unavailable_identity")
        return self


class SourceProviderContract(BaseModel):
    """One admitted upstream provider and its allowed acquisition channels."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    provider_id: str = Field(min_length=1)
    acquisition_channels: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_channels(self) -> "SourceProviderContract":
        if len(self.acquisition_channels) != len(set(self.acquisition_channels)):
            raise ValueError("duplicate_acquisition_channel")
        if any(not channel for channel in self.acquisition_channels):
            raise ValueError("empty_acquisition_channel")
        return self


class SourceFamilyContract(BaseModel):
    """Registered, versioned admission contract for one source family."""

    model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)

    family_id: str = Field(min_length=1)
    contract_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    payload_model: type[BaseModel]
    providers: tuple[SourceProviderContract, ...] = Field(min_length=1)
    source_identifier: SourceIdentifierContract
    source_time_kind: SourceTimeKind
    downstream_owner: SourceDownstreamOwner
    output_contract: SourceOutputContract
    signal_family_id: str | None = None
    permitted_limitations: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _validate_output_contract(self) -> "SourceFamilyContract":
        provider_ids = [provider.provider_id for provider in self.providers]
        if len(provider_ids) != len(set(provider_ids)):
            raise ValueError("duplicate_source_provider_contract")
        if self.payload_model is BaseModel:
            raise ValueError("payload_model_must_be_concrete")
        if self.output_contract is SourceOutputContract.RAW_SIGNAL_BATCH:
            if not self.signal_family_id:
                raise ValueError("raw_signal_batch requires signal_family_id")
            if self.downstream_owner is not SourceDownstreamOwner.M03:
                raise ValueError("raw_signal_batch must route to M03")
        elif self.signal_family_id is not None:
            raise ValueError("signal_family_id is not applicable to source_artifact output")
        return self


class SourceFamilyRegistry(BaseModel):
    """Deterministic controlled registry for supported source-family contracts."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    contracts: tuple[SourceFamilyContract, ...]

    @classmethod
    def build(cls, contracts: Iterable[SourceFamilyContract]) -> "SourceFamilyRegistry":
        ordered = tuple(
            sorted(
                contracts,
                key=lambda item: (item.family_id, item.contract_id, item.schema_version),
            )
        )
        keys = [(item.family_id, item.contract_id, item.schema_version) for item in ordered]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate_source_family_contract")
        return cls(contracts=ordered)

    def resolve(
        self,
        *,
        family_id: str,
        contract_id: str,
        schema_version: str,
    ) -> SourceFamilyContract | None:
        for contract in self.contracts:
            if (
                contract.family_id == family_id
                and contract.contract_id == contract_id
                and contract.schema_version == schema_version
            ):
                return contract
        return None


class SourceAdmissionRequest(BaseModel):
    """Already-obtained source material presented to the M01 admission boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)

    family_id: str = Field(min_length=1)
    contract_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    provider_id: str = Field(min_length=1)
    acquisition_channel: str = Field(min_length=1)
    source_object_id: str | None = None
    observed_at_utc: datetime | None = None
    source_date: date | None = None
    source_time_raw: str | None = None
    source_timezone_raw: str | None = None
    captured_at_utc: datetime
    captured_material: bytes = Field(min_length=1)
    typed_payload: SerializeAsAny[BaseModel]
    declared_limitations: tuple[str, ...] = ()

    @field_validator("typed_payload", mode="before")
    @classmethod
    def _require_concrete_typed_payload(cls, value: Any) -> BaseModel:
        if not isinstance(value, BaseModel) or type(value) is BaseModel:
            raise ValueError("typed_payload_must_be_concrete_pydantic_model")
        return value


class CaptureReceipt(BaseModel):
    """Repository-owned receipt for one immutable alpha capture occurrence."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    capture_id: str = Field(min_length=1)
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    captured_at_utc: datetime
    durability_status: Literal["volatile_alpha"] = "volatile_alpha"


class RawSignalBatch(BaseModel):
    """Typed raw-signal-family payload with explicit source/capture lineage."""

    model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)

    signal_family_id: str = Field(min_length=1)
    source_object_id: str | None = None
    capture_id: str = Field(min_length=1)
    source_artifact_id: str = Field(min_length=1)
    contract_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    provider_id: str = Field(min_length=1)
    acquisition_channel: str = Field(min_length=1)
    source_identifier: SourceIdentifierContract
    observed_at_utc: datetime | None = None
    source_date: date | None = None
    payload: BaseModel


class SourceArtifactEnvelope(BaseModel):
    """K01 source/capture carrier preserving identity, time, version and evidence."""

    model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)

    source_artifact_id: str = Field(min_length=1)
    family_id: str = Field(min_length=1)
    contract_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    provider_id: str = Field(min_length=1)
    acquisition_channel: str = Field(min_length=1)
    source_identifier: SourceIdentifierContract
    source_object_id: str | None = None
    observed_at_utc: datetime | None = None
    source_date: date | None = None
    source_time_raw: str | None = None
    source_timezone_raw: str | None = None
    source_time_precision: SourceTimeKind
    capture_receipt: CaptureReceipt
    captured_material: bytes
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    validation_status: Literal["admitted", "degraded"]
    validation_results: tuple[str, ...]
    limitations: tuple[str, ...] = ()
    downstream_owner: SourceDownstreamOwner
    typed_payload: BaseModel


class SourceAdmissionAccepted(BaseModel):
    """Successful M01 admission with no downstream semantic decision authority."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["accepted"] = "accepted"
    source_artifact: SourceArtifactEnvelope
    raw_signal_batch: RawSignalBatch | None = None


class SourceNonAdmission(BaseModel):
    """Explicit fail-closed result for material outside the governed path."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["not_admitted"] = "not_admitted"
    reason: str = Field(min_length=1)
    content_sha256: str | None = None
    capture_receipt: None = None


SourceAdmissionResult = SourceAdmissionAccepted | SourceNonAdmission
CaptureIdFactory = Callable[[str], str]
SourceArtifactIdFactory = Callable[[str, str, str | None, str], str]


class SourceAdapter(Protocol):
    """Port for translating already-obtained provider material into an M01 request."""

    def adapt(self, material: bytes) -> SourceAdmissionRequest: ...
