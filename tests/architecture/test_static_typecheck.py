import os
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run_mypy(*paths: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("MYPYPATH", None)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--config-file",
            str(ROOT / "pyproject.toml"),
            *paths,
        ],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_current_source_tree_passes_admitted_static_typecheck() -> None:
    completed = _run_mypy("src")
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_static_type_checker_is_pinned_development_only() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert "mypy==1.20.1" in project["optional-dependencies"]["dev"]
    assert all(not dependency.startswith("mypy") for dependency in project["dependencies"])


def test_incompatible_python_visible_public_seam_use_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "src"
    producer = source / "nvda_desk/m02/api.py"
    consumer = source / "nvda_desk/m01/impl.py"
    package_markers = (
        source / "nvda_desk/__init__.py",
        producer.parent / "__init__.py",
        consumer.parent / "__init__.py",
    )
    for path in package_markers:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
    producer.write_text(
        "def normalize(value: int) -> int:\n    return value\n",
        encoding="utf-8",
    )
    consumer.write_text(
        'from nvda_desk.m02.api import normalize\nresult = normalize("wrong")\n',
        encoding="utf-8",
    )

    completed = _run_mypy("--explicit-package-bases", str(source))

    assert completed.returncode == 1
    assert '[arg-type]' in completed.stdout
    assert 'incompatible type "str"; expected "int"' in completed.stdout
