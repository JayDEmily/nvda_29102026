"""M12-owned deterministic semantic fingerprint mechanics."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from typing import Any

from pydantic import BaseModel


def _canonical(value: Any) -> Any:
    """Canonicalise one replay-evidence value without importing another owner."""
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("decimal_must_be_finite")
        return "0" if value == 0 else format(value.normalize(), "f")
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def semantic_fingerprint(value: Any) -> str:
    """Return the stable SHA-256 semantic identity of one M12 evidence value."""
    return sha256(
        json.dumps(_canonical(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
