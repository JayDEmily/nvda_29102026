from __future__ import annotations

import importlib.util
import sys
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]


def _read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_make_install_is_frozen_non_editable_and_lock_owned() -> None:
    makefile = _read("Makefile")

    assert "INSTALL_INPUTS := pyproject.toml uv.lock .python-version" in makefile
    assert "$(UV) sync --frozen --extra dev --no-editable" in makefile
    assert "pip install -e" not in makefile
    assert "pip install --upgrade pip" not in makefile


def test_lockfile_uses_portable_public_package_origins() -> None:
    lockfile = _read("uv.lock")

    assert "applied-caas-gateway" not in lockfile
    assert 'registry = "https://pypi.org/simple"' in lockfile
    assert "https://files.pythonhosted.org/packages/" in lockfile


def test_installed_package_smoke_imports_from_site_packages_outside_repo() -> None:
    makefile = _read("Makefile")

    assert ".PHONY: installed-package-smoke" in makefile
    assert 'tmp_dir="$$(mktemp -d)"' in makefile
    assert '$(abspath $(PYTHON))" -I -c' in makefile
    assert 'sysconfig.get_paths()["purelib"]' in makefile
    assert "module.is_relative_to(purelib)" in makefile


def test_pr_ci_uses_pinned_uv_and_authoritative_promotion_gate() -> None:
    workflow = _read(".github/workflows/pr-preflight.yml")

    assert "astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b" in workflow
    assert 'version: "0.11.16"' in workflow
    assert 'cache-dependency-glob: "uv.lock"' in workflow
    assert "run: make install" in workflow
    assert "run: make installed-package-smoke" in workflow
    assert "run: make promotion-gate" in workflow
    assert "run: make test" not in workflow
    assert "cache: pip" not in workflow


def test_remote_patch_ci_delegates_authority_and_gates_before_push() -> None:
    workflow = _read(".github/workflows/apply-remote-bridge-patch.yml")

    assert "run: make promotion-check" in workflow
    assert "run: make promotion-gate" in workflow
    assert "git push origin" in workflow
    assert workflow.index("run: make promotion-gate") < workflow.index("git push origin")
    assert "proof['schema_version']" not in workflow
    assert "block_id" not in workflow
    assert "proof.get('blocks'" not in workflow
    assert "tier_a_test_count" not in workflow
    assert "registered_retained_seed_tier_a" not in workflow


def test_make_offline_install_delegates_to_repository_bootstrap() -> None:
    makefile = _read("Makefile")

    assert ".PHONY: install-offline" in makefile
    assert "scripts/bootstrap_offline_environment.py" in makefile
    assert "RUNTIME_WHEELHOUSE_ZIP" in makefile
    assert "DEV_WHEELHOUSE_ZIP" in makefile


def test_offline_bootstrap_is_hash_pinned_lock_exported_and_non_editable() -> None:
    bootstrap = _read("scripts/bootstrap_offline_environment.py")

    assert "6e4459f4e5508303bdb2e03bcca7701ee72e640f36a716c20b3cd6b0c09b0b42" in bootstrap
    assert "d71a1f5f22aaaa588a59012833c8d797258ea1505feec37e77d7948c818cc249" in bootstrap
    assert '"export"' in bootstrap
    assert '"--frozen"' in bootstrap
    assert '"--no-editable"' in bootstrap
    assert '"--no-emit-project"' in bootstrap
    assert '"venv"' in bootstrap
    assert '"pip"' in bootstrap
    assert '"install"' in bootstrap
    assert '"--offline"' in bootstrap
    assert '"--no-index"' in bootstrap
    assert '"--no-cache"' in bootstrap
    assert '"--find-links"' in bootstrap
    assert '"--no-build-isolation"' in bootstrap
    assert '"--no-deps"' in bootstrap
    assert "hatchling==1.29.0" in bootstrap
    assert "editables==0.6" in bootstrap
    assert "pip install --upgrade pip" not in bootstrap
    assert '"-e"' not in bootstrap


def _load_offline_bootstrap():
    path = REPO_ROOT / "scripts/bootstrap_offline_environment.py"
    spec = importlib.util.spec_from_file_location("bootstrap_offline_environment", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_offline_bootstrap_rejects_hash_mismatch(tmp_path: Path) -> None:
    bootstrap = _load_offline_bootstrap()
    archive = tmp_path / "runtime.zip"
    archive.write_bytes(b"not-the-accepted-archive")

    with pytest.raises(bootstrap.BootstrapError, match="SHA-256 mismatch"):
        bootstrap.verify_archive(archive, "0" * 64, expected_size=None)


def test_offline_bootstrap_rejects_zip_path_escape(tmp_path: Path) -> None:
    bootstrap = _load_offline_bootstrap()
    archive = tmp_path / "unsafe.zip"
    destination = tmp_path / "extract"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("../escape.txt", "blocked")

    with pytest.raises(bootstrap.BootstrapError, match="unsafe ZIP member"):
        bootstrap.safe_extract_zip(archive, destination)
    assert not (tmp_path / "escape.txt").exists()
