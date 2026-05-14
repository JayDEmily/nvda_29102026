"""Map bounded native API boundary values into explicit public DTO dictionaries."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any


class ApiDtoAdapter:
    """Project bounded native values into explicit public DTO dictionaries."""

    def to_runtime_dto(self, value: Any) -> dict[str, Any]:
        """Return one public runtime DTO dictionary from a bounded native value."""

        return _coerce_public_mapping(value)

    def to_review_dto(self, value: Any) -> dict[str, Any]:
        """Return one public review DTO dictionary from a bounded native value."""

        return _coerce_public_mapping(value)

    def to_state_dto(self, value: Any) -> dict[str, Any]:
        """Return one public state DTO dictionary from a bounded native value."""

        return _coerce_public_mapping(value)


def _coerce_public_mapping(value: Any) -> dict[str, Any]:
    """Return one plain dictionary without widening into transport-specific behaviour."""

    if hasattr(value, "model_dump"):
        return value.model_dump()
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return dict(value)
    return {"value": value}


def to_api_dto(value: Any) -> dict[str, Any]:
    """Return one DTO dictionary through the admitted API DTO boundary owner."""

    return ApiDtoAdapter().to_runtime_dto(value)
