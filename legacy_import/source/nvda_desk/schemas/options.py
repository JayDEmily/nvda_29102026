from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class OptionType(StrEnum):
    CALL = "Call"
    PUT = "Put"


class OptionSnapshotPayload(BaseModel):
    as_of_date: date
    expiry: date | None = None
    option_type: OptionType
    strike: Decimal
    bid: Decimal | None = None
    ask: Decimal | None = None
    last: Decimal | None = None
    volume: int | None = None
    open_interest: int | None = None
    iv: Decimal | None = None
    delta: Decimal | None = None
    gamma: Decimal | None = None
    delta_change: Decimal | None = None
    provenance: str
    confidence: str
    source_document: str
    source_pages: str


class OptionSurfaceResponse(BaseModel):
    symbol: str
    requested_at: datetime
    as_of_date: date
    expiry: date | None = None
    option_type: OptionType | None = None
    snapshots: list[OptionSnapshotPayload]


class OptionSurfaceQuery(BaseModel):
    symbol: str = Field(default="NVDA", min_length=1)
    as_of_date: date
    expiry: date | None = None
    option_type: OptionType | None = None
