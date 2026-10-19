"""FND-P06: pinned static positive and exact negative diagnostic sites/codes."""

import ast
import inspect
import re
import subprocess
import sys
from dataclasses import fields
from pathlib import Path

import pytest
from _support import ROOT, foundation


def test_public_seam_static_compatibility(tmp_path):
    f = foundation()
    folder = Path(__file__).parent / "typing"
    config = tmp_path / "mypy.ini"
    config.write_text("[mypy]\npython_version=3.12\nfollow_untyped_imports=True\n")
    cmd = [
        sys.executable,
        "-m",
        "mypy",
        "--config-file",
        str(config),
        "--strict",
        "--disallow-any-expr",
        "--cache-dir",
        str(tmp_path / "mypy-cache"),
    ]
    good = subprocess.run(
        [*cmd, str(folder / "valid_seam.py")], text=True, capture_output=True, timeout=60
    )
    assert good.returncode == 0, good.stdout + good.stderr
    assert "Any" not in good.stdout
    bad_path = folder / "invalid_seam.py"
    expected = {
        (line, re.search(r"MISUSE\[([^]]+)\]", text).group(1))
        for line, text in enumerate(bad_path.read_text().splitlines(), 1)
        if "MISUSE[" in text
    }
    bad = subprocess.run([*cmd, str(bad_path)], text=True, capture_output=True, timeout=60)
    assert bad.returncode == 1, bad.stdout + bad.stderr
    observed = re.findall(r"invalid_seam.py:(\d+): error: .* \[([^]]+)\]", bad.stdout)
    assert {(int(line), code) for line, code in observed} == expected
    assert len(observed) == len(expected) == 10
    assert bad.stdout.count("error:") == 10 and not bad.stderr
    assert {field.name for field in fields(f.SQLiteStorageV1)} == {"database_path", "create"}
    assert {field.name for field in fields(f.SQLiteReadStorageV1)} == {"database_path"}
    for value in ("true", 1, None):
        with pytest.raises(TypeError):
            f.SQLiteStorageV1("/tmp/pilot.sqlite", value)


def test_exact_frozen_public_record_shapes_from_accepted_authority():
    f = foundation()
    text = (
        ROOT
        / "handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md"
    ).read_text()
    block = text.split("```python\n", 1)[1].split("```", 1)[0]
    expected = {
        item.name: tuple(node.target.id for node in item.body if isinstance(node, ast.AnnAssign))
        for item in ast.parse(block).body
        if isinstance(item, ast.ClassDef)
        and item.decorator_list
        and item.name not in {"PostgresStorageV1", "PostgresReadStorageV1"}
    }
    expected |= {
        "SQLiteStorageV1": ("database_path", "create"),
        "SQLiteReadStorageV1": ("database_path",),
    }
    for name, names in expected.items():
        cls = getattr(f, name)
        assert tuple(field.name for field in fields(cls)) == names
        signature = inspect.signature(cls)
        assert tuple(signature.parameters) == names
        assert all(
            parameter.default is inspect.Parameter.empty
            for parameter in signature.parameters.values()
        )
        assert cls.__dataclass_params__.frozen and hasattr(cls, "__slots__")
        with pytest.raises(TypeError):
            cls(unapproved_field="x")
