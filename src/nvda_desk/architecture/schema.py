"""Small, explicit validator for the JSON Schema subset used by this kernel."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any


class SchemaValidationError(ValueError):
    """Raised when a registry document violates its admitted schema."""


def _fail(path: str, message: str) -> None:
    raise SchemaValidationError(f"{path}: {message}")


def _is_type(instance: Any, expected: str) -> bool:
    return {
        "object": isinstance(instance, Mapping),
        "array": isinstance(instance, list),
        "string": isinstance(instance, str),
        "integer": isinstance(instance, int) and not isinstance(instance, bool),
        "number": isinstance(instance, (int, float)) and not isinstance(instance, bool),
        "boolean": isinstance(instance, bool),
        "null": instance is None,
    }.get(expected, False)


def validate_instance(instance: Any, schema: Mapping[str, Any], path: str = "$") -> None:
    """Validate the standards subset used by the committed schemas.

    Supported keywords are deliberately bounded: type, required, properties,
    patternProperties, additionalProperties, items, enum, const, pattern,
    minLength, minItems and uniqueItems.
    """

    expected = schema.get("type")
    if expected is not None:
        expected_types = [expected] if isinstance(expected, str) else list(expected)
        if not any(_is_type(instance, item) for item in expected_types):
            _fail(path, f"expected type {expected_types}, got {type(instance).__name__}")

    if "const" in schema and instance != schema["const"]:
        _fail(path, f"expected constant {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        _fail(path, f"value {instance!r} is not in {schema['enum']!r}")

    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            _fail(path, "string is shorter than minLength")
        pattern = schema.get("pattern")
        if pattern is not None and re.fullmatch(pattern, instance) is None:
            _fail(path, f"value {instance!r} does not match {pattern!r}")

    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            _fail(path, "array is shorter than minItems")
        if schema.get("uniqueItems"):
            canonical = [json.dumps(item, sort_keys=True) for item in instance]
            if len(canonical) != len(set(canonical)):
                _fail(path, "array items are not unique")
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, item in enumerate(instance):
                validate_instance(item, item_schema, f"{path}[{index}]")

    if isinstance(instance, Mapping):
        required = schema.get("required", [])
        missing = [name for name in required if name not in instance]
        if missing:
            _fail(path, f"missing required properties: {missing}")
        properties = schema.get("properties", {})
        pattern_properties = schema.get("patternProperties", {})
        for name, value in instance.items():
            if name in properties:
                validate_instance(value, properties[name], f"{path}.{name}")
                continue
            matching = [
                subschema
                for pattern, subschema in pattern_properties.items()
                if re.fullmatch(pattern, name)
            ]
            if matching:
                for subschema in matching:
                    validate_instance(value, subschema, f"{path}.{name}")
                continue
            additional = schema.get("additionalProperties", True)
            if additional is False:
                _fail(path, f"unexpected property {name!r}")
            if isinstance(additional, Mapping):
                validate_instance(value, additional, f"{path}.{name}")


def validate_document(document_path: Path, schema_path: Path) -> None:
    document = __import__("yaml").safe_load(document_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate_instance(document, schema)
